#!/usr/bin/env python3
"""Offline synthetic replay and actual-file mutations in disposable checkouts.

Usage: python -B replay.py --output /tmp/fresh-directory
Use python -O -B replay.py for optimized children as well. Output MUST be new,
so an earlier PASS cannot survive a failed repeat. No historical files are written.
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
DEPENDENCIES = ("R067", "R073", "R074", "R075", "R076", "R077")
SUITES = {
    "R073": ("test_r073_human_ipd_memory_loso.py", 23),
    "R074": ("test_r074_dalbo_external_human_e3.py", 20),
    "R075": ("test_r075_coauthor_real_human_e3.py", 24),
    "R077": ("test_r077_fourth_real_human_source_only_e3.py", 24),
}
MUTATIONS = {
    "R074": (
        "r074_dalbo_external_human_e3.py",
        'events = [ev for s in other for ev in sessions[s]["events"]]',
        'events = [ev for s in other for ev in sessions[other[0]]["events"]]',
        'events = [ev for s in other for ev in sessions[heldout]["events"]]',
    ),
    "R075": (
        "r075_coauthor_real_human_e3.py",
        'events=[event for s in training for event in sessions[s]["events"]]',
        'events=[event for s in training for event in sessions[training[0]]["events"]]',
        'events=[event for s in training for event in sessions[heldout]["events"]]',
    ),
}
PROBE = '''import importlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()/"research/codex_b/2026-11-10-session-isolation"))
from test_fit_oracle import fictional_sessions, TRAINERS
from fit_oracle import check_trainer
module = next(m for m in TRAINERS if m.__name__.startswith(sys.argv[1].lower()+"_"))
try:
    checks = [check_trainer(module.fit_other_sessions, module.predict, fictional_sessions(equal))
              for equal in (False, True)]
except ValueError as exc:
    if str(exc) not in ("FIT_MISMATCH", "PREDICTION_MISMATCH"):
        raise
    print(json.dumps({"status":"REJECTED", "reason":str(exc)}))
    sys.exit(42)
print(json.dumps({"status":"PASS", "checks":checks}))
'''


def fingerprints():
    files = [p for study in DEPENDENCIES for p in sorted((ROOT/"research"/study).glob("*.py"))]
    files += sorted(HERE.glob("*.py"))
    records = {}
    for path in files:
        content = path.read_bytes()
        records[str(path.relative_to(ROOT))] = {
            "bytes": len(content), "sha256": hashlib.sha256(content).hexdigest(),
            "git_blob": hashlib.sha1(b"blob "+str(len(content)).encode()+b"\0"+content).hexdigest(),
        }
    return records


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    commands = []
    python = [sys.executable, "-B"] + (["-O"] if sys.flags.optimize else [])
    before = fingerprints()

    def execute(tag, args, cwd):
        result = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=60)
        (output/f"{tag}.stdout").write_text(result.stdout)
        (output/f"{tag}.stderr").write_text(result.stderr)
        commands.append({"tag": tag, "argv": args, "cwd": str(cwd), "exit_code": result.returncode})
        (output/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
        return result

    def suite(tag, root, study, expected, should_pass=True):
        folder = (root/"research"/study if study != "new" else
                  root/"research/codex_b/2026-11-10-session-isolation")
        pattern = SUITES[study][0] if study != "new" else "test_fit_oracle.py"
        result = execute(tag, python+["-m", "unittest", "discover", "-s", str(folder), "-p", pattern, "-v"], root)
        match = re.search(r"Ran (\d+) tests? in", result.stderr)
        if match is None or int(match[1]) != expected:
            raise RuntimeError(f"WRONG_TEST_COUNT:{tag}")
        if (result.returncode == 0) != should_pass:
            raise RuntimeError(f"UNEXPECTED_SUITE_RESULT:{tag}")
        if not should_pass and ("FAIL:" not in result.stderr or "ERROR:" in result.stderr):
            raise RuntimeError(f"MUTANT_CONTROL_NOT_ASSERTION_FAILURE:{tag}")
        return {"tests": expected, "exit_code": result.returncode}

    originals = {study: suite(f"original-{study}", ROOT, study, count)
                 for study, (_, count) in SUITES.items()}
    added = suite("new-gate-tests", ROOT, "new", 10)
    positive = {}
    for study in MUTATIONS:
        probe = execute(f"original-{study}-gate", python+["-c", PROBE, study], ROOT)
        if probe.returncode != 0 or json.loads(probe.stdout)["status"] != "PASS":
            raise RuntimeError("ORIGINAL_GATE_NOT_PASS")
        positive[study] = json.loads(probe.stdout)
    mutants = {}
    for study, (filename, preimage, duplicate, heldout) in MUTATIONS.items():
        mutants[study] = {}
        for kind, replacement in (("duplicate_donor", duplicate), ("heldout_leak", heldout)):
            with tempfile.TemporaryDirectory(prefix=f"codex-b-{study}-{kind}-") as tmp:
                sandbox = Path(tmp)
                for dep in DEPENDENCIES:
                    dest = sandbox/"research"/dep
                    dest.mkdir(parents=True)
                    for source in (ROOT/"research"/dep).glob("*.py"):
                        shutil.copyfile(source, dest/source.name)
                own = sandbox/"research/codex_b/2026-11-10-session-isolation"
                own.mkdir(parents=True)
                for name in ("fit_oracle.py", "test_fit_oracle.py"):
                    shutil.copyfile(HERE/name, own/name)
                target = sandbox/"research"/study/filename
                content = target.read_text()
                if content.count(preimage) != 1:
                    raise RuntimeError("MUTATION_PREIMAGE_MISMATCH")
                target.write_text(content.replace(preimage, replacement))
                mutant_suite = suite(f"{study}-{kind}-old-suite", sandbox, study,
                                     SUITES[study][1], should_pass=(kind == "duplicate_donor"))
                probe = execute(f"{study}-{kind}-new-gate", python+["-c", PROBE, study], sandbox)
                if probe.returncode != 42 or json.loads(probe.stdout) != {"status": "REJECTED", "reason": "FIT_MISMATCH"}:
                    raise RuntimeError("MUTANT_GATE_NOT_REJECTED")
                mutants[study][kind] = {
                    "source_preimage": preimage, "source_replacement": replacement,
                    "mutant_source_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                    "old_suite": mutant_suite, "new_gate": json.loads(probe.stdout),
                }
    after = fingerprints()
    if before != after:
        raise RuntimeError("SOURCE_CHANGED_DURING_REPLAY")
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True, check=True).stdout.strip()
    result = {
        "status": "PASS_BOUNDED_SYNTHETIC_ENGINEERING", "utc": datetime.now(timezone.utc).isoformat(),
        "source_head": head, "python": sys.version, "platform": platform.platform(),
        "optimized": bool(sys.flags.optimize), "original_suites": originals,
        "new_suite": added, "original_gate": positive, "mutants": mutants,
        "source_fingerprints_before_and_after_equal": True, "sources": before,
        "new_human_scores": 0, "external_team_replications": 0,
        "historical_human_numerical_correctness": "NOT_REASSESSED",
        "full_repository_tests": "NOT_RUN", "github_actions": "NOT_RUN",
        "R073": "FROZEN_UNCHANGED", "PESEN_v0.1": "FROZEN_UNCHANGED",
    }
    (output/"summary.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("sources", "mutants")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    run(parser.parse_args().output.resolve())
