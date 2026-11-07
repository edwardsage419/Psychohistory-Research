#!/usr/bin/env python3
"""Nonblind archived R258/S54 replay; writes only output and temporary sandboxes.

Run from repo root:
python -B research/codex_audit/r258_s54_replay/run_audit.py . --output /tmp/r258-s54
Each concurrent process must use a distinct output directory.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile

NATIVE = "research/R258/r258_exact_finite_stochastic_control.py"
CSV = "research/R258/R258_ALL_1728_ORIGINAL_THREESTEP_CONTROL_SOURCE_ATOMS.csv"
ORIGINAL = "research/R258/R258_EXACT_RESULTS.json"
MACHINE = "research/R258/R258_FINAL_MACHINE_ACCEPTANCE.json"
FORMAL = "research/R258/R258_FINAL_ACCEPTANCE_STATUS.json"
R = "research/validation/r258_s54_coarse_state_observation_20261029.py"
B = "research/evidence_audit/b_r258_s54_distribution_oracle_20261029.py"
GATE = "research/evidence_audit/b_r258_s54_crossroute_gate_20261029.py"
RECEIPT = "research/validation/R258_S54_COARSE_OBSERVATION_EXACT_RECEIPT_2026-10-29.json"
SOURCES = (NATIVE, CSV, ORIGINAL, MACHINE, FORMAL, R, B, GATE, RECEIPT)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def check_archive(actual, archived):
    # Unlike Python ==, serialized JSON distinguishes false from 0.
    def canonical(value):
        return json.dumps(value, sort_keys=True, allow_nan=False)
    require(canonical(actual) == canonical(archived), "archive JSON mismatch")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root, out = args.root.resolve(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "execution.json").unlink(missing_ok=True)
    commands = []

    def run(label, script, *arguments):
        command = [sys.executable, "-B", str(script), *arguments]
        p = subprocess.run(command, cwd=root, text=True, capture_output=True, timeout=90)
        (out / (label + ".stdout")).write_text(p.stdout)
        (out / (label + ".stderr")).write_text(p.stderr)
        commands.append({"label": label, "command": command, "cwd": str(root), "exit_code": p.returncode})
        require(p.returncode == 0, label + " failed; see stderr log")
        return p

    def sha(path):
        return hashlib.sha256(path.read_bytes()).hexdigest()

    formal = json.loads((root / FORMAL).read_text())
    require(sha(root / CSV) == formal["source_sha256"], "original CSV hash")
    require(sha(root / ORIGINAL) == formal["results_sha256"], "original result hash")
    tests = {}
    for label, script, count in (("native_tests", NATIVE, 82), ("r_tests", R, 8), ("b_tests", B, 7)):
        p = run(label, root / script, "--test")
        match = re.search(r"Ran (\d+) tests", p.stderr)
        require(match is not None and int(match.group(1)) == count, label + " count")
        tests[label] = {"passed": count, "failures": 0, "errors": 0}
    r = json.loads(run("r_emit", root / R, "--emit").stdout)
    b = json.loads(run("b_emit", root / B, "--emit").stdout)
    archived = json.loads((root / RECEIPT).read_text())
    check_archive(r, archived)
    check_archive(b["results"], archived["results"])
    gate = json.loads(run("crossroute_gate", root / GATE).stdout)
    require(gate["exact_policy_comparisons"] == 3456 and gate["negative_mutations_rejected"] == 4
            and gate["complete_world_initial_pairs"] == 27, "crossroute coverage")

    # emit() writes adjacent files; run it solely in an isolated copy.
    with tempfile.TemporaryDirectory() as tmp:
        sandbox = Path(tmp)
        for path in SOURCES:
            target = sandbox / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / path, target)
        native_machine = json.loads(run("native_emit_sandbox", sandbox / NATIVE, "--emit").stdout)
        regenerated = {}
        for path in (CSV, ORIGINAL, MACHINE):
            require((sandbox / path).read_bytes() == (root / path).read_bytes(),
                    "native regeneration differs: " + path)
            regenerated[path] = {"bytes_equal": True, "sha256": sha(sandbox / path)}
        check_archive(native_machine, json.loads((root / MACHINE).read_text()))
        # Characterize what the archived gate actually consumes.
        corrupted = copy.deepcopy(archived)
        corrupted["results"][0]["gap_A"] = "999"
        (sandbox / RECEIPT).write_text(json.dumps(corrupted))
        ignored = json.loads(run("gate_with_corrupted_archive", sandbox / GATE).stdout)
        require(ignored == gate, "archived gate behavior changed")
        try:
            check_archive(r, corrupted)
        except ValueError:
            corrupted_archive_rejected = True
        else:
            raise ValueError("new replay accepted corrupt archive")

    controls = []
    for label, mutate in (
        ("gap", lambda d: d["results"][0].update(gap_A="999")),
        ("duplicate_pair", lambda d: d["results"].__setitem__(1, copy.deepcopy(d["results"][0]))),
        ("evidence", lambda d: d.update(evidence="E3")),
        ("boolean_zero", lambda d: d.update(new_human_E2=False)),
    ):
        changed = copy.deepcopy(archived)
        mutate(changed)
        try:
            check_archive(r, changed)
        except ValueError:
            controls.append({"mutation": label, "rejected": True})
        else:
            raise ValueError("negative control accepted: " + label)
    source_hashes = {path: sha(root / path) for path in SOURCES}
    source_blobs = {}
    for path in SOURCES:
        raw = (root / path).read_bytes()
        source_blobs[path] = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    result = {
        "status": "COMPLETE", "scope": "NONBLIND_INTERNAL_FINITE_ARTIFICIAL_E1_REPLAY",
        "python": sys.version, "platform": platform.platform(), "seed": "N/A; exhaustive",
        "unittests": tests, "s54_full_receipt_matches_r_emit": True,
        "all_27_rows_match_b_emit": True, "archived_crossroute_gate": gate,
        "original_native_regeneration": regenerated, "new_negative_controls": controls,
        "archived_gate_ignores_persisted_receipt": True,
        "corrupted_persisted_receipt_rejected_by_new_replay": corrupted_archive_rejected,
        "source_sha256": source_hashes, "source_git_blob": source_blobs, "commands": commands,
        "new_E2": 0, "new_E3": 0, "external_team_replications": 0,
        "blindness": "Results read before this audit; cannot retroactively change historical blind status",
        "ci_status": "NOT_RUN", "full_repository_checkout": False,
    }
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=out, delete=False) as tmp:
        tmp.write(json.dumps(result, indent=2) + "\n")
        staged = Path(tmp.name)
    staged.replace(out / "execution.json")
    print(json.dumps({"status": "COMPLETE", "archived_tests_passed": 97,
                      "policy_comparisons": 3456, "new_negative_controls_rejected": 4,
                      "full_s54_receipt_matches": True, "original_files_regenerated_exactly": 3,
                      "archived_gate_ignores_persisted_receipt": True}, indent=2))


if __name__ == "__main__":
    main()
