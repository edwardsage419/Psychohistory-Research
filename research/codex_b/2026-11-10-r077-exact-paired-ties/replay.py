#!/usr/bin/env python3
"""Offline artificial tie witness and exact supplement; output must be NEW.

Use either installed Python3.12 or3.13, with -B and optionally -O.
The original scoring regression is REQUIRED to fail, not represented as fixed.
"""
import argparse
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
OWN = "research/codex_b/2026-11-10-r077-exact-paired-ties"
DEPS = ("R067", "R073", "R074", "R075", "R076", "R077")
SUITES = (("r073", "research/R073", "test_r073_human_ipd_memory_loso.py", 23),
          ("r077", "research/R077", "test_r077_fourth_real_human_source_only_e3.py", 24),
          ("new", OWN, "test_exact_pair.py", 12))
PINNED = {"research/R073/r073_human_ipd_memory_loso.py": "c8a0b47fd27bf05e7be5b87419a0824355fc911a",
          "research/R077/r077_fourth_real_human_source_only_e3.py": "70889bd15c6fd943bdb07ab3ae1f60c943ebc538"}
DIAGNOSTICS = '''import json,sys
sys.path.insert(0,sys.argv[1])
from case import legacy_fit,target_cases,exact_sessions,integer_witness
from exact_pair import summarize,validate_legacy_pair
from legacy_regression import score_with_frozen_source
from collections import Counter
records=[];histogram=Counter();blocked=0
for positions,sessions in target_cases():
    expected=summarize(exact_sessions(sessions))
    proof=integer_witness([e[4] for e in next(iter(sessions.values()))["events"]])
    if proof!={"integer_squared_sums":{"candidate":343,"reference":343},"denominator":1372,"risks":{"candidate":"1/4","reference":"1/4"}}:
        raise RuntimeError("INTEGER_PROOF_MISMATCH")
    if str(expected["candidate_macro_Brier"])!="1/4" or str(expected["reference_macro_Brier"])!="1/4":
        raise RuntimeError("EXACT_SUPPLEMENT_MISMATCH")
    pair=score_with_frozen_source(legacy_fit(),sessions)["paired_differences"]["M3_JOINT_LAST_VS_M1_OWN_LAST"]
    votes=(pair["sessions_better"],pair["sessions_equal"],pair["sessions_worse"])
    histogram[str(votes)]+=1
    rejected=False
    try:validate_legacy_pair(pair,expected["paired"])
    except ValueError as exc:
        if str(exc)!="PAIRED_DIRECTION_MISMATCH":raise
        rejected=True;blocked+=1
    if rejected!=(votes!=(0,2,0)):raise RuntimeError("WRONG_GUARD_CLASSIFICATION")
    records.append({"positive_positions":positions,"original":pair,"exact":expected,
                    "integer_witness":proof,"original_rejected_by_exact_votes":rejected})
if len(records)!=35 or len(histogram)<2 or blocked==0:raise RuntimeError("ORDER_DEFECT_NOT_REPRODUCED")
print(json.dumps({"data_class":"ARTIFICIAL_ONLY","permutations":records,
                  "original_vote_histogram":dict(histogram),"guard_rejections":blocked,
                  "exact_ties":35,"integer_proofs":35},default=str,indent=2))
'''


def fingerprints():
    paths = [p for dep in DEPS for p in sorted((ROOT/"research"/dep).glob("*.py"))]
    paths += sorted(HERE.glob("*.py"))
    paths += [ROOT/p for p in (
        "protocols/R073_HUMAN_IPD_LAGGED_SOCIAL_MEMORY_LOSO_2026-10-17.md",
        "protocols/R077_ZENODO_FOURTH_AUTHOR_TRUE_HUMAN_PROSPECTIVE_MODEL_SCORE_FREEZE_2026-10-17.md",
        "protocols/R077_PRE_FIRST_TARGET_MODEL_SCORE_SOURCE_SEMANTICS_AMENDMENT_REV002_2026-10-17.md",
        "research/R077/R077_FOURTH_INDEPENDENT_HUMAN_SOURCE_ONLY_E3_RESULTS.json")]
    found = {}
    for path in paths:
        content = path.read_bytes(); name = str(path.relative_to(ROOT))
        blob = hashlib.sha1(b"blob "+str(len(content)).encode()+b"\0"+content).hexdigest()
        if not name.startswith(OWN+"/"):
            tracked = subprocess.check_output(["git", "rev-parse", "HEAD:"+name], cwd=ROOT, text=True).strip()
            if blob != tracked: raise RuntimeError("HISTORICAL_SOURCE_CHANGED:"+name)
        if name in PINNED and blob != PINNED[name]: raise RuntimeError("FROZEN_PREIMAGE_CHANGED:"+name)
        found[name] = {"bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(), "git_blob": blob}
    return found


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    commands = []; before = fingerprints()
    python = [sys.executable, "-B"]+(["-O"] if sys.flags.optimize else [])

    def execute(tag, args, cwd=ROOT):
        child = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=60)
        (output/f"{tag}.stdout").write_text(child.stdout)
        (output/f"{tag}.stderr").write_text(child.stderr)
        commands.append({"tag": tag, "argv": args, "cwd": str(cwd), "exit_code": child.returncode})
        (output/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
        return child

    suites = {}
    for tag, folder, pattern, count in SUITES:
        child = execute(tag, python+["-m", "unittest", "discover", "-s", str(ROOT/folder), "-p", pattern, "-v"])
        match = re.search(r"Ran (\d+) tests? in", child.stderr)
        if child.returncode or match is None or int(match[1]) != count: raise RuntimeError("POSITIVE_SUITE_FAIL:"+tag)
        suites[tag] = count
    regression = execute("original-regression-expected-fail", python+[str(HERE/"legacy_regression.py")])
    failure = re.search(r"FAILED \(failures=(\d+)\)", regression.stderr)
    if (regression.returncode != 1 or failure is None or "Ran 1 test" not in regression.stderr
            or "ERROR:" in regression.stderr): raise RuntimeError("ORIGINAL_REGRESSION_NOT_REPRODUCED")
    diagnostics = execute("permutation-diagnostics", python+["-c", DIAGNOSTICS, str(HERE)])
    if diagnostics.returncode: raise RuntimeError("DIAGNOSTICS_FAIL")
    evidence = json.loads(diagnostics.stdout)
    if int(failure[1]) != evidence["guard_rejections"]: raise RuntimeError("REGRESSION_COUNT_MISMATCH")

    # A plausible repair error: compute exact risks, then round them to float
    # BEFORE subtracting. It hides a genuine tiny effect and must be detected.
    with tempfile.TemporaryDirectory(prefix="codex-b-exact-delta-mutation-") as tmp:
        sandbox = Path(tmp)
        for name in ("exact_pair.py", "case.py", "test_exact_pair.py"):
            shutil.copyfile(HERE/name, sandbox/name)
        target = sandbox/"exact_pair.py"; source = target.read_text()
        old, new = "delta = candidate-reference", "delta = Fraction(float(candidate)-float(reference))"
        if source.count(old) != 1: raise RuntimeError("MUTATION_PREIMAGE")
        target.write_text(source.replace(old, new))
        mutant = execute("rounded-delta-negative", python+["-m", "unittest", "discover", "-s", str(sandbox), "-p", "test_exact_pair.py", "-v"])
        if (mutant.returncode != 1 or "FAIL: test_genuine_tiny_nonzero_delta_keeps_its_sign" not in mutant.stderr
                or "ERROR:" in mutant.stderr or "Ran 12 tests" not in mutant.stderr):
            raise RuntimeError("ROUNDING_MUTATION_NOT_DETECTED")
        mutant_sha = hashlib.sha256(target.read_bytes()).hexdigest()
    after = fingerprints()
    if before != after: raise RuntimeError("SOURCE_CHANGED_DURING_REPLAY")
    result = {
        "status": "PASS_EXACT_SUPPLEMENT_WITH_ORIGINAL_REGRESSION_FAIL_RETAINED",
        "data_class": "ARTIFICIAL_ONLY", "utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "python_executable": sys.executable, "optimized": bool(sys.flags.optimize),
        "platform": platform.platform(), "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "positive_test_methods": suites, "original_regression": {"test_methods": 1, "permutations": 35, "assertion_failures": int(failure[1]), "exit_code": 1},
        "permutation_summary": {k: evidence[k] for k in ("original_vote_histogram", "guard_rejections", "exact_ties", "integer_proofs")},
        "rounding_mutation": {"old": old, "new": new, "sha256": mutant_sha, "detected": True},
        "sources_before_after_equal": True, "sources": before,
        "new_human_scores": 0, "new_E2_E3": 0, "external_team_replications": 0,
        "historical_human_ties_or_vote_changes": "NOT_RUN", "full_repository_tests": "NOT_RUN",
        "production_adoption": "NOT_RUN", "github_actions": "NOT_RUN",
        "R073": "FROZEN_UNCHANGED", "PESEN_v0.1": "FROZEN_UNCHANGED",
    }
    (output/"summary.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: result[k] for k in ("status", "python", "optimized", "positive_test_methods", "original_regression", "permutation_summary")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
