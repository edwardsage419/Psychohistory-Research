#!/usr/bin/env python3
"""Original native Node/B replay plus complete receipt mutation checks, offline.

Use python -B or python -O -B; --output must be a NEW directory. Original
research files stay read-only. All960 atoms are archived artificial E1 records.
"""
import argparse
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OWN = "research/codex_b/2026-11-10-r278-complete-receipt"
CSV_NAME = "R278_S74_ALL_960_ARTIFICIAL_SOURCES_2026-10-30.csv"
JSON_NAME = "R278_S74_EXACT_RESULTS_2026-10-30.json"
MACHINE_NAME = "R278_S74_RECEIPT_2026-10-30.json"
CSV_PATH, JSON_PATH = ROOT/"research/validation"/CSV_NAME, ROOT/"research/validation"/JSON_NAME
JS_PATH = ROOT/"research/validation/r278_s74_joint_20261030.js"
B_PATH = ROOT/"research/evidence_audit/b_r278_s74_receipt_check_20261030.py"
PINS = {
    str(JS_PATH.relative_to(ROOT)): "4fc696cd690a182968dfa0e930933025982286ab",
    str(B_PATH.relative_to(ROOT)): "f1ba4dcb2e80a612f14b3d7c10896c1d6fccfa62",
    str(CSV_PATH.relative_to(ROOT)): "494c688596cda6186fb6f0e1c588584009659934",
    str(JSON_PATH.relative_to(ROOT)): "1d9963435f044b72b69704e64e7ba8fe1609a021",
}


def fingerprints():
    paths = [ROOT/name for name in PINS]
    paths += [ROOT/"research/validation/R278_S74_TWO_STEP_JOINT_PREDICTIVE_PROTOCOL_FREEZE_2026-10-30.md"]
    paths += sorted(HERE.glob("*.py"))
    found = {}
    for path in paths:
        data = path.read_bytes(); name = str(path.relative_to(ROOT))
        blob = hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
        if not name.startswith(OWN+"/"):
            tracked = subprocess.check_output(["git", "rev-parse", "HEAD:"+name], cwd=ROOT, text=True).strip()
            if blob != tracked: raise RuntimeError("HISTORICAL_INPUT_CHANGED:"+name)
        if name in PINS and blob != PINS[name]: raise RuntimeError("PINNED_INPUT_CHANGED:"+name)
        found[name] = {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "git_blob": blob}
    return found


def mutations(original_text):
    original = json.loads(original_text)
    result = {}
    for label in ("missing_conditional_forecasts", "covariance_999", "comparison_delta_999", "R073_modified", "E2_false", "wrong_world_risk"):
        data = copy.deepcopy(original)
        if label == "missing_conditional_forecasts": del data["conditional_forecasts"]
        elif label == "covariance_999": data["conditional_forecasts"][2]["joint_predictive_covariance"] = "999"
        elif label == "comparison_delta_999": data["BMA_joint_minus_product"][0]["delta"] = "999"
        elif label == "R073_modified": data["R073"] = "MODIFIED"
        elif label == "E2_false": data["new_E2_predictions"] = False
        else: data["world_results"][0]["expected_joint_brier"] = "999"
        result[label] = json.dumps(data, indent=2)+"\n"
    old = '"expected_joint_brier": "8643/13120"'
    if old not in original_text: raise RuntimeError("DUPLICATE_KEY_PREIMAGE")
    result["duplicate_checked_risk_key"] = original_text.replace(old, '"expected_joint_brier": "999", '+old, 1)
    old = '"joint_predictive_covariance": "1/16"'
    if original_text.count(old) != 1: raise RuntimeError("NAN_PREIMAGE")
    result["covariance_NaN"] = original_text.replace(old, '"joint_predictive_covariance": NaN')
    return result


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    before = fingerprints(); commands = []
    python = [sys.executable, "-B"]+(["-O"] if sys.flags.optimize else [])
    node = shutil.which("node")
    if node is None: raise RuntimeError("NODE_NOT_AVAILABLE")

    def execute(tag, args):
        child = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=60)
        (output/f"{tag}.stdout").write_text(child.stdout)
        (output/f"{tag}.stderr").write_text(child.stderr)
        commands.append({"tag": tag, "argv": args, "cwd": str(ROOT), "exit_code": child.returncode})
        (output/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
        return child

    tests = execute("unit-tests", python+["-m", "unittest", "discover", "-s", str(HERE), "-p", "test_complete_receipt.py", "-v"])
    if tests.returncode or re.search(r"Ran (\d+) tests? in", tests.stderr)[1] != "14":
        raise RuntimeError("UNIT_TEST_FAILURE")
    archived = execute("original-B-archive", python+[str(B_PATH), str(CSV_PATH), str(JSON_PATH)])
    if archived.returncode or json.loads(archived.stdout)["status"] != "PASS": raise RuntimeError("ORIGINAL_B_FAIL")
    strict = execute("complete-gate-archive", python+[str(HERE/"complete_receipt.py"), str(CSV_PATH), str(JSON_PATH)])
    if strict.returncode or json.loads(strict.stdout)["receipt_leaves"] != 140: raise RuntimeError("COMPLETE_GATE_FAIL")
    native_identity = {}
    outcomes = {}
    with tempfile.TemporaryDirectory(prefix="codex-b-r278-native-") as tmp:
        sandbox = Path(tmp); native = sandbox/"native"
        node_result = execute("original-R-node-emit", [node, str(JS_PATH), str(native)])
        if node_result.returncode: raise RuntimeError("ORIGINAL_NODE_FAIL")
        machine = json.loads((native/MACHINE_NAME).read_text())
        if machine != json.loads(node_result.stdout): raise RuntimeError("NODE_MACHINE_STDOUT_MISMATCH")
        for source, field in ((CSV_PATH, "source_csv_sha256"), (JSON_PATH, "results_json_sha256")):
            emitted = (native/source.name).read_bytes(); persisted = source.read_bytes()
            if emitted != persisted or hashlib.sha256(emitted).hexdigest() != machine[field]:
                raise RuntimeError("NATIVE_BYTE_IDENTITY_FAIL:"+source.name)
            native_identity[source.name] = {"bytes": len(emitted), "sha256": machine[field], "byte_equal": True}
        (output/"native-generated-receipt.json").write_bytes((native/MACHINE_NAME).read_bytes())
        emitted_b = execute("original-B-emitted", python+[str(B_PATH), str(native/CSV_NAME), str(native/JSON_NAME)])
        emitted_gate = execute("complete-gate-emitted", python+[str(HERE/"complete_receipt.py"), str(native/CSV_NAME), str(native/JSON_NAME)])
        if emitted_b.returncode or emitted_gate.returncode: raise RuntimeError("EMITTED_RECHECK_FAIL")
        for label, text in mutations(JSON_PATH.read_text()).items():
            target = sandbox/(label+".json"); target.write_text(text)
            old = execute(label+"-old", python+[str(B_PATH), str(CSV_PATH), str(target)])
            should_pass = label != "wrong_world_risk"
            if (old.returncode == 0) != should_pass: raise RuntimeError("OLD_MUTATION_OUTCOME_CHANGED:"+label)
            if should_pass and json.loads(old.stdout)["status"] != "PASS": raise RuntimeError("OLD_NOT_PASS:"+label)
            if not should_pass and "ValueError: world risk" not in old.stderr: raise RuntimeError("WRONG_OLD_REJECTION")
            new = execute(label+"-complete", python+[str(HERE/"complete_receipt.py"), str(CSV_PATH), str(target)])
            rejection = json.loads(new.stdout)
            if new.returncode != 2 or rejection["status"] != "REJECTED": raise RuntimeError("UNDETECTED_MUTATION:"+label)
            outcomes[label] = {"mutant_sha256": hashlib.sha256(text.encode()).hexdigest(),
                               "old_exit_code": old.returncode, "complete_exit_code": new.returncode,
                               "complete_reason": rejection["reason"]}
        source_rows = [line.split(",") for line in CSV_PATH.read_text().splitlines()]
        for label in ("duplicate_csv_mass_column", "extra_csv_cell", "zero_denominator_mass"):
            rows = [list(row) for row in source_rows]
            if label == "duplicate_csv_mass_column":
                rows = [row[:7]+(["source_probability"] if i == 0 else ["999"])+row[7:] for i, row in enumerate(rows)]
            elif label == "extra_csv_cell": rows[1].append("999")
            else: rows[1][7] = "1/0"
            text = "\n".join(",".join(row) for row in rows)+"\n"
            target = sandbox/(label+".csv"); target.write_text(text)
            old = execute(label+"-old", python+[str(B_PATH), str(target), str(JSON_PATH)])
            new = execute(label+"-complete", python+[str(HERE/"complete_receipt.py"), str(target), str(JSON_PATH)])
            rejection = json.loads(new.stdout)
            expected_reason = {"duplicate_csv_mass_column": "CSV_HEADER_SCHEMA", "extra_csv_cell": "CSV_ROW_SCHEMA", "zero_denominator_mass": "ZeroDivisionError"}[label]
            old_ok = (old.returncode != 0 and "ZeroDivisionError" in old.stderr) if label == "zero_denominator_mass" else (old.returncode == 0 and json.loads(old.stdout)["status"] == "PASS")
            if not old_ok or new.returncode != 2 or rejection != {"status": "REJECTED", "reason": expected_reason}:
                raise RuntimeError("CSV_SCHEMA_COUNTEREXAMPLE_NOT_REPRODUCED:"+label)
            outcomes[label] = {"mutant_sha256": hashlib.sha256(text.encode()).hexdigest(),
                               "old_exit_code": old.returncode, "complete_exit_code": new.returncode,
                               "complete_reason": rejection["reason"]}
    after = fingerprints()
    if before != after: raise RuntimeError("INPUT_CHANGED_DURING_REPLAY")
    node_version = execute("node-version", [node, "--version"])
    result = {
        "status": "PASS_BOUNDED_FULL_RECEIPT_SUPPLEMENT", "utc": datetime.now(timezone.utc).isoformat(),
        "data_class": "ARCHIVED_ARTIFICIAL_E1_ONLY", "python": sys.version, "optimized": bool(sys.flags.optimize),
        "node": node_version.stdout.strip(), "platform": platform.platform(),
        "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "unit_tests": {"methods": 14, "exit_code": 0,
                       "inherited_ResourceWarning_recorded": "ResourceWarning" in tests.stderr}, "receipt_leaves": 140,
        "conditional_forecast_records": 5, "worlds": 15, "source_rows": 960,
        "native_identity": native_identity, "mutations": outcomes,
        "old_false_accepts": sum(v["old_exit_code"] == 0 for v in outcomes.values()),
        "complete_rejections": len(outcomes), "sources_before_after_equal": True, "sources": before,
        "historical_declaration_flags": "MATCHED_NOT_NEW_SCIENTIFIC_CERTIFICATION",
        "new_human_scores": 0, "new_E2_E3": 0, "external_team_replications": 0,
        "original_R278_core_tests": "NOT_RUN", "full_repository_tests": "NOT_RUN",
        "production_adoption": "NOT_RUN", "github_actions": "NOT_RUN",
        "R073": "FROZEN_UNCHANGED", "PESEN_v0.1": "FROZEN_UNCHANGED",
    }
    (output/"summary.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: result[k] for k in ("status", "python", "optimized", "node", "unit_tests", "receipt_leaves", "native_identity", "old_false_accepts", "complete_rejections")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
