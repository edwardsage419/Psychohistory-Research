#!/usr/bin/env python3
"""Offline synthetic acceptance replay. --output must name a NEW directory.

Run with python -B or python -O -B; children inherit the optimization mode.
Historical inputs are read only. Real human sources are never loaded/scored.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction
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
OWN = "research/codex_b/2026-11-10-r077-score-leakage"
DEPS = ("R067", "R073", "R074", "R075", "R076", "R077")
ORIGINAL = "research/R077/r077_fourth_real_human_source_only_e3.py"
SUITES = (
    ("r073", "research/R073", "test_r073_human_ipd_memory_loso.py", 23),
    ("r077", "research/R077", "test_r077_fourth_real_human_source_only_e3.py", 24),
    ("new", OWN, "test_score_oracle.py", 12),
)
MUTANTS = {
    "current_label_leak": (
        "pred=predict(model,row,fit)",
        "pred=(predict(model,row,fit)+row[4])/2", True),
    "brier_as_log_loss": (
        "total_l+=logloss(row[-1],pred)",
        "total_l+=brier(row[-1],pred)", True),
    "row_weighted_macro": (
        'avg([macro_session[k][model]["Brier"] for k in names])',
        'sum(macro_session[k][model]["Brier"]*len(target_sessions[k]["events"]) for k in names)/sum(len(info["events"]) for info in target_sessions.values())', False),
}
PROBE = '''import json,sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()/"research/codex_b/2026-11-10-r077-score-leakage"))
from test_score_oracle import run_contract,score_with_frozen_source
import test_r077_fourth_real_human_source_only_e3 as legacy
score=score_with_frozen_source(legacy.fake_fit(),legacy.cases())
m0=score["models"]["M0_TREATMENT_PREVALENCE"]
example={"data_class":"ARTIFICIAL_LEGACY_TEST_FIXTURE_ONLY",
         "M0_Brier":m0["all_original_sessions_equal_Brier"],
         "M0_log_loss":m0["all_original_sessions_equal_log_loss"],
         "declared_target_labels_used_in_training":score["target_labels_used_in_training"]}
try:
    checks=run_contract(score_with_frozen_source)
except ValueError as exc:
    if not str(exc).startswith("SCORE_MISMATCH:"):
        raise
    print(json.dumps({"status":"REJECTED","reason":str(exc),"counterexample":example}))
    sys.exit(42)
print(json.dumps({"status":"PASS","checks":checks,"counterexample":example}))
'''


def fingerprints():
    paths = [p for dep in DEPS for p in sorted((ROOT/"research"/dep).glob("*.py"))]
    paths += sorted(HERE.glob("*.py"))
    paths += [ROOT/path for path in (
        "protocols/R073_HUMAN_IPD_LAGGED_SOCIAL_MEMORY_LOSO_2026-10-17.md",
        "protocols/R077_ZENODO_FOURTH_AUTHOR_TRUE_HUMAN_PROSPECTIVE_MODEL_SCORE_FREEZE_2026-10-17.md",
        "protocols/R077_PRE_FIRST_TARGET_MODEL_SCORE_SOURCE_SEMANTICS_AMENDMENT_REV002_2026-10-17.md",
        "research/R077/R077_FOURTH_INDEPENDENT_HUMAN_SOURCE_ONLY_E3_RESULTS.json",
    )]
    found = {}
    for path in paths:
        content = path.read_bytes()
        name = str(path.relative_to(ROOT))
        blob = hashlib.sha1(b"blob "+str(len(content)).encode()+b"\0"+content).hexdigest()
        if not name.startswith(OWN+"/"):
            tracked = subprocess.check_output(["git", "rev-parse", "HEAD:"+name], cwd=ROOT, text=True).strip()
            if blob != tracked:
                raise RuntimeError("HISTORICAL_BLOB_MISMATCH:"+name)
        found[name] = {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(), "git_blob": blob}
    return found


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    commands = []
    before = fingerprints()
    python = [sys.executable, "-B"] + (["-O"] if sys.flags.optimize else [])

    def execute(tag, args, cwd):
        result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=60)
        (output/f"{tag}.stdout").write_text(result.stdout)
        (output/f"{tag}.stderr").write_text(result.stderr)
        commands.append({"tag": tag, "argv": args, "cwd": str(cwd), "exit_code": result.returncode})
        (output/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
        return result

    def suite(tag, root, relative, pattern, expected, should_pass=True):
        child = execute(tag, python+["-m", "unittest", "discover", "-s", str(root/relative), "-p", pattern, "-v"], root)
        match = re.search(r"Ran (\d+) tests? in", child.stderr)
        if match is None or int(match[1]) != expected or (child.returncode == 0) != should_pass:
            raise RuntimeError("UNEXPECTED_SUITE_RESULT:"+tag)
        if not should_pass and ("FAIL:" not in child.stderr or "ERROR:" in child.stderr):
            raise RuntimeError("CONTROL_NOT_ASSERTION_FAILURE:"+tag)
        return {"test_methods": expected, "exit_code": child.returncode}

    def probe(tag, root, should_pass):
        child = execute(tag, python+["-c", PROBE], root)
        if child.returncode != (0 if should_pass else 42):
            raise RuntimeError("UNEXPECTED_PROBE_EXIT:"+tag)
        data = json.loads(child.stdout)
        if data["status"] != ("PASS" if should_pass else "REJECTED"):
            raise RuntimeError("UNEXPECTED_PROBE_STATUS:"+tag)
        if should_pass and data["checks"] != {"score_calls": 68, "output_leaf_comparisons": 10200}:
            raise RuntimeError("INCOMPLETE_POSITIVE_CONTRACT")
        return data

    tests = {tag: suite("original-"+tag, ROOT, relative, pattern, count)
             for tag, relative, pattern, count in SUITES}
    positive = probe("original-numeric-gate", ROOT, True)
    if abs(positive["counterexample"]["M0_Brier"]-float(Fraction(17, 75))) > 1e-15:
        raise RuntimeError("LEGACY_SYNTHETIC_CONTROL_CHANGED")
    mutants = {}
    for kind, (old, new, survives) in MUTANTS.items():
        with tempfile.TemporaryDirectory(prefix="codex-b-r077-"+kind+"-") as tmp:
            sandbox = Path(tmp)
            for dep in DEPS:
                dest = sandbox/"research"/dep
                dest.mkdir(parents=True)
                for source in (ROOT/"research"/dep).glob("*.py"):
                    shutil.copyfile(source, dest/source.name)
            dest = sandbox/OWN
            dest.mkdir(parents=True)
            for name in ("score_oracle.py", "test_score_oracle.py"):
                shutil.copyfile(HERE/name, dest/name)
            target = sandbox/ORIGINAL
            source = target.read_text()
            if source.count(old) != 1:
                raise RuntimeError("MUTATION_PREIMAGE_MISMATCH:"+kind)
            target.write_text(source.replace(old, new))
            old_test = suite(kind+"-old-suite", sandbox, "research/R077",
                             SUITES[1][2], 24, should_pass=survives)
            rejected = probe(kind+"-new-gate", sandbox, False)
            mutants[kind] = {"old": old, "new": new, "old_suite": old_test, "new_gate": rejected,
                             "mutated_source_sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
    leak = mutants["current_label_leak"]["new_gate"]["counterexample"]
    if abs(leak["M0_Brier"]-float(Fraction(17, 300))) > 1e-15 or leak["declared_target_labels_used_in_training"] != 0:
        raise RuntimeError("TARGET_LEAK_COUNTEREXAMPLE_NOT_REPRODUCED")
    after = fingerprints()
    if before != after:
        raise RuntimeError("SOURCE_CHANGED_DURING_REPLAY")
    result = {
        "status": "PASS_BOUNDED_SYNTHETIC_NUMERICAL_ACCEPTANCE",
        "data_class": "ARTIFICIAL_ONLY_NO_HUMAN_SOURCES_LOADED",
        "utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
        "platform": platform.platform(), "optimized": bool(sys.flags.optimize),
        "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "positive_test_methods": tests, "positive_numeric_contract": positive, "mutants": mutants,
        "sources_before_after_equal": True, "sources": before,
        "historical_source_git_blobs_match_HEAD": True,
        "new_human_scores": 0, "new_E2_E3": 0, "external_team_replications": 0,
        "raw_source_identity_and_timeline_validation": "NOT_RUN",
        "historical_human_score_correctness": "NOT_REASSESSED",
        "full_repository_tests": "NOT_RUN", "github_actions": "NOT_RUN",
        "R073": "FROZEN_UNCHANGED", "PESEN_v0.1": "FROZEN_UNCHANGED",
    }
    (output/"summary.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({"status": result["status"], "optimized": result["optimized"],
                      "positive_tests": sum(t["test_methods"] for t in tests.values()),
                      "numeric_contract": positive["checks"], "rejected_mutants": list(mutants)}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
