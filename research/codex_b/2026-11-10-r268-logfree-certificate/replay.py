#!/usr/bin/env python3
"""Offline R268/S64 exact certificate and archived CLI replay; output must be NEW."""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import re
import runpy
import shutil
import subprocess
import sys
import tempfile

from certificate import SIZES, certify
from test_certificate import CSV_PATH, CORE_PATH, S64_PATH, coordinated_mutation, write_case

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OWN = "research/codex_b/2026-11-10-r268-logfree-certificate"
ORIGINAL = ROOT/"research/R268/r268_exact_aic_bic_bernoulli.py"
MACHINE = ROOT/"research/R268/R268_MACHINE_RECEIPT.json"
B = ROOT/"research/validation/r268_s64_independent_binomial.py"
PINS = {
    str(ORIGINAL.relative_to(ROOT)): "c173a250ed231cf92641f29aa1e11afe52e78c0b",
    str(CSV_PATH.relative_to(ROOT)): "6296528507012dd1d8d11e3556fcdeb7b6aeb2b5",
    str(CORE_PATH.relative_to(ROOT)): "3d407ddcf524bfc55c0a076d57383c6655a36441",
    str(S64_PATH.relative_to(ROOT)): "7dd11a986ceda4c48b1414af2042d1d521eb49c5",
}


def fingerprints():
    files = [ROOT/name for name in PINS]+[MACHINE, B]
    files += [ROOT/name for name in (
        "protocols/R268_AIC_BIC_NINE_BERNOULLI_WORLDS_3312_COMPLETE_SOURCE_PRESCORE_FREEZE_2026-10-23.md",
        "protocols/R268_S64_ONE_STEP_HOLDOUT_BRIER_PRESCORE_FREEZE_2026-10-29.md")]
    files += sorted(HERE.glob("*.py"))
    found = {}
    for path in files:
        raw = path.read_bytes(); name = str(path.relative_to(ROOT))
        blob = hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
        if not name.startswith(OWN+"/"):
            tracked = subprocess.check_output(["git", "rev-parse", "HEAD:"+name], cwd=ROOT, text=True).strip()
            if blob != tracked: raise RuntimeError("HISTORICAL_INPUT_CHANGED:"+name)
        if name in PINS and blob != PINS[name]: raise RuntimeError("PINNED_INPUT_CHANGED:"+name)
        found[name] = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "git_blob": blob}
    return found


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    before = fingerprints(); commands = []
    python = [sys.executable, "-B"]+(["-O"] if sys.flags.optimize else [])

    def execute(tag, args):
        child = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=60)
        streams = {}
        for suffix, text in (("stdout", child.stdout), ("stderr", child.stderr)):
            raw = text.encode(); filename = tag+"."+suffix
            # Empty streams are faithfully represented in the command manifest;
            # avoid hundreds of empty evidence files.
            if text: (output/filename).write_text(text)
            streams[suffix] = {"bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "file": filename if text else None}
        commands.append({"tag": tag, "argv": args, "cwd": str(ROOT), "exit_code": child.returncode, "streams": streams})
        (output/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
        return child

    positive = execute("new-tests", python+["-m", "unittest", "discover", "-s", str(HERE), "-p", "test_certificate.py", "-v"])
    if positive.returncode or re.search(r"Ran (\d+) tests in", positive.stderr)[1] != "14": raise RuntimeError("NEW_TESTS_FAIL")
    archive = execute("exact-audit-archive", python+[str(HERE/"audit.py"), str(CSV_PATH), str(CORE_PATH), str(S64_PATH)])
    if archive.returncode: raise RuntimeError("ARCHIVE_AUDIT_FAIL")
    certificate = json.loads(archive.stdout)
    identity = {}; negatives = {}
    with tempfile.TemporaryDirectory(prefix="codex-b-r268-native-") as tmp:
        sandbox = Path(tmp); script = sandbox/ORIGINAL.name
        script.write_bytes(ORIGINAL.read_bytes())
        original_tests = execute("original-84-tests", python+[str(script), "--test"])
        if original_tests.returncode or re.search(r"Ran (\d+) tests in", original_tests.stderr)[1] != "84": raise RuntimeError("ORIGINAL_TESTS_FAIL")
        emit = execute("original-emit", python+[str(script), "--emit"])
        if emit.returncode: raise RuntimeError("ORIGINAL_EMIT_FAIL")
        for path in (CSV_PATH, CORE_PATH, MACHINE):
            emitted = (sandbox/path.name).read_bytes(); persisted = path.read_bytes()
            if emitted != persisted: raise RuntimeError("NATIVE_BYTE_MISMATCH:"+path.name)
            identity[path.name] = {"bytes": len(emitted), "sha256": hashlib.sha256(emitted).hexdigest(), "byte_equal": True}
        machine = json.loads((sandbox/MACHINE.name).read_text())
        if machine != json.loads(emit.stdout) or machine["source_sha256"] != identity[CSV_PATH.name]["sha256"] or machine["results_sha256"] != identity[CORE_PATH.name]["sha256"]:
            raise RuntimeError("MACHINE_RECEIPT_MISMATCH")
        (output/"native-machine-receipt.json").write_bytes((sandbox/MACHINE.name).read_bytes())
        emitted_audit = execute("exact-audit-emitted", python+[str(HERE/"audit.py"), str(sandbox/CSV_PATH.name), str(sandbox/CORE_PATH.name), str(S64_PATH)])
        if emitted_audit.returncode or json.loads(emitted_audit.stdout) != certificate: raise RuntimeError("EMITTED_CERTIFICATE_MISMATCH")
        b_output = sandbox/"original-B.json"
        b_run = execute("original-S64-B", python+[str(B), "--output", str(b_output)])
        if b_run.returncode: raise RuntimeError("ORIGINAL_B_FAIL")
        old_b = json.loads(b_output.read_text()); checks = 0
        if old_b["negative_controls"]["count"] != 4 or old_b["world_count"] != 9: raise RuntimeError("ORIGINAL_B_COVERAGE")
        for row in old_b["results"]:
            expected = certificate["world_metrics"][row["world"]]
            for field in ("risk", "excess"):
                for method, value in row[field].items():
                    if F(value) != F(expected[field][method]): raise RuntimeError("B_RISK_MISMATCH")
                    checks += 1
            if F(row["AIC_minus_BIC"]) != F(expected["AIC_minus_BIC"]): raise RuntimeError("B_DELTA_MISMATCH")
            checks += 1
        if checks != 81: raise RuntimeError("B_FIELD_COUNT")
        old_choices = runpy.run_path(str(B), run_name="codex_b_archived_s64_input")["DECISIONS"]
        for n in SIZES:
            derived = tuple("".join(str(int(certify(n, k)[criterion] == "M1_FITTED")) for k in range(n+1)) for criterion in ("AIC", "BIC"))
            if old_choices[n] != derived: raise RuntimeError("SHARED_INPUT_DECISIONS_NOT_CERTIFIED")
        for label in ("coordinated_wrong_labels", "S64_risk_999", "missing_source", "E2_bool"):
            case_dir = sandbox/label; case_dir.mkdir()
            if label == "coordinated_wrong_labels": args = write_case(case_dir, *coordinated_mutation())
            elif label == "S64_risk_999":
                s64 = json.loads(S64_PATH.read_text()); s64["results"][0]["risk"]["AIC_SELECTED"] = "999"
                args = write_case(case_dir, s64=s64)
            elif label == "missing_source":
                import csv, io
                rows = list(csv.reader(io.StringIO(CSV_PATH.read_text()))); rows.pop()
                args = write_case(case_dir, rows=rows)
            else:
                core = json.loads(CORE_PATH.read_text()); core["new_real_human_E2"] = False
                args = write_case(case_dir, core=core)
            child = execute(label, python+[str(HERE/"audit.py"), *map(str, args)])
            result = json.loads(child.stdout)
            if child.returncode != 2 or result["status"] != "REJECTED": raise RuntimeError("UNDETECTED_CONTROL:"+label)
            negatives[label] = {"exit_code": child.returncode, "reason": result["reason"],
                                "sha256": [hashlib.sha256(path.read_bytes()).hexdigest() for path in args]}
        mutant_own = sandbox/OWN; mutant_own.mkdir(parents=True)
        for filename in ("certificate.py", "audit.py", "test_certificate.py"):
            shutil.copyfile(HERE/filename, mutant_own/filename)
        path = mutant_own/"certificate.py"; code = path.read_text()
        old = 'bic = "M1_FITTED" if r > n else "M0_FIXED"'
        new = 'bic = "M1_FITTED" if r > 3312 else "M0_FIXED"'
        if code.count(old) != 1: raise RuntimeError("BIC_MUTATION_PREIMAGE")
        path.write_text(code.replace(old, new))
        test_code = 'import sys,unittest;sys.path.insert(0,sys.argv[1]);from test_certificate import CertificateTests;r=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite([CertificateTests("test_hand_reversed_penalty_decisions")]));sys.exit(0 if r.wasSuccessful() else 1)'
        mutant = execute("wrong-total-n-negative", python+["-c", test_code, str(mutant_own)])
        if mutant.returncode != 1 or "FAILED (failures=1)" not in mutant.stderr or "ERROR:" in mutant.stderr: raise RuntimeError("WRONG_N_MUTATION_NOT_DETECTED")
        negatives["wrong_BIC_total_n"] = {"exit_code": 1, "old": old, "new": new, "mutant_sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    after = fingerprints()
    if before != after: raise RuntimeError("INPUT_CHANGED_DURING_REPLAY")
    result = {"status": "PASS_INDEPENDENT_LOGFREE_CERTIFICATE_NO_NUMERICAL_DISCREPANCY_FOUND",
              "utc": datetime.now(timezone.utc).isoformat(), "python": sys.version, "optimized": bool(sys.flags.optimize),
              "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "positive_tests": {"original": 84, "new": 14}, "certificate_counts": {key: certificate[key] for key in ("states", "source_rows", "core_decision_records", "selection_probabilities", "S64_fraction_checks")},
              "native_identity": identity, "original_B_risk_checks": checks, "original_B_shared_decision_bits_checked": 46,
              "original_B_negative_controls": 4, "new_negative_controls": negatives,
              "sources_before_after_equal": True, "sources": before,
              "scalar_log_value_error_certification": "NOT_RUN_FINITE_REPRESENTATION_AND_NATIVE_BYTE_REPLAY_ONLY",
              "original_S64_R_source_CLI": "NOT_RUN_NOT_ARCHIVED", "original_asserts_under_optimized_python": "DISABLED_NOT_CLAIMED_AS_INDEPENDENT_CHECKS",
              "new_human_scores": 0, "new_E2_E3": 0, "external_team_replications": 0,
              "full_repository_tests": "NOT_RUN", "production_adoption": "NOT_RUN", "github_actions": "NOT_RUN",
              "R073": "FROZEN_UNCHANGED", "PESEN_v0.1": "FROZEN_UNCHANGED"}
    (output/"summary.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({key: result[key] for key in ("status", "python", "optimized", "positive_tests", "certificate_counts", "native_identity")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
