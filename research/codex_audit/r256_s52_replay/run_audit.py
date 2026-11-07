#!/usr/bin/env python3
"""Execute pinned archived R256 S52 CLIs and a nonblind Python risk recomputation.

Run at repository root:
python research/codex_audit/r256_s52_replay/run_audit.py . --output /tmp/r256-s52
Only --output and temporary negative-control directories are written.
Use a distinct output directory for each concurrent audit process.
"""
import argparse
from collections import defaultdict
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile

SCRIPTS = {
    "r": "research/validation/r256_s52_rejection_prefix_20261029.js",
    "b": "research/evidence_audit/b_r256_s52_independent_dp_20261029.js",
    "source_replay": "research/evidence_audit/b_r256_s52_original_csv_full_replay_20261029.js",
    "third_route": "research/operations/e086_r256_s52_original_csv_third_route_20261029.js",
}
CSV = "research/R256/R256_ALL_4608_ORIGINAL_FOUR_SLOT_QUEUE_SOURCE_ATOMS.csv"
NATIVE = "research/R256/r256_exact_finite_queue.py"
RECEIPT = "research/validation/R256_S52_EXACT_RECEIPT_2026-10-29.json"
FEATURES = {"F0": (), "F1": (1,), "F12": (1, 2), "F123": (1, 2, 3), "F3": (3,)}
SHA = "8be5360465497321c15bffc554c7088fad48bcef71847e43e2ee2f714ed5119b"


def check(condition, message):
    if not condition:
        raise ValueError(message)


def index(rows, expected):
    check(type(rows) is list and len(rows) == len(expected), "world count")
    names = [r["world"] for r in rows]
    check(len(set(names)) == len(names) and set(names) == set(expected), "world identities")
    return {r["world"]: r for r in rows}


def compare(actual, expected):
    a, e = index(actual, expected), expected
    n = 0
    for name, want in e.items():
        got = a[name]
        check(got["target"] == want["target"], "target mismatch")
        check(got["event_count"] == want["event_count"], "event count")
        n += 1
        check(set(got["features"]) == set(FEATURES), "feature identities")
        for f in FEATURES:
            for field in ("risk", "groups", "mixed"):
                check(type(got["features"][f][field]) is type(want["features"][f][field])
                      and got["features"][f][field] == want["features"][f][field],
                      name + "/" + f + "/" + field)
                n += 1
    return n


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("root", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root, out = args.root.resolve(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    # A failed rerun must not leave a prior COMPLETE receipt next to new logs.
    (out / 'execution.json').unlink(missing_ok=True)
    commands = []

    def run(label, command, cwd, ok=True):
        proc = subprocess.run(command, cwd=cwd, text=True, capture_output=True, timeout=60)
        (out / (label + ".stdout")).write_text(proc.stdout)
        (out / (label + ".stderr")).write_text(proc.stderr)
        commands.append({"label": label, "command": command, "cwd": str(cwd),
                         "exit_code": proc.returncode})
        check((proc.returncode == 0) if ok else (proc.returncode != 0), label + ": unexpected exit")
        return proc

    raw = (root / CSV).read_bytes()
    check(hashlib.sha256(raw).hexdigest() == SHA, "source hash mismatch")
    native_run = run("native_tests", [sys.executable, str(root / NATIVE), "--test"], root)
    match = re.search(r"Ran (\d+) tests", native_run.stderr)
    check(match is not None and int(match.group(1)) == 82, "native suite count")
    outputs = {}
    for label, script in SCRIPTS.items():
        outputs[label] = json.loads(run(label, ["node", str(root / script)], root).stdout)
    archived = json.loads((root / RECEIPT).read_text())
    # The archived receipt appends separate verifier attestations not emitted by R.
    extra = {k: archived[k] for k in archived.keys() - outputs['r'].keys()}
    check(set(extra) == {'negative_injection', 'independent_dp_exact_comparison',
                         'comparison_fields', 'future_label_leakage_risk'},
          'unexpected archive-only fields')
    check(all(k in archived and archived[k] == value for k, value in outputs['r'].items()),
          'R computation fields differ from archive')
    check(outputs["source_replay"]["compared_cells"] == 202752, "source coverage")
    check(outputs["source_replay"]["actual_source_sha256"] == SHA, "Node hash")
    check(outputs["third_route"]["checks"] == 60605 and outputs["third_route"]["failures"] == 0,
          "third route result")

    spec = importlib.util.spec_from_file_location("native_r256", root / NATIVE)
    native = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(native)
    expected = {}
    for world in native.WORLDS:
        rows = native.sources(world)
        check(len(rows) == 512, "native source coverage")
        scores = {}
        for feature, times in FEATURES.items():
            grouped = defaultdict(lambda: [0, 0])
            for row in rows:
                key = tuple(row["observed_reported_queue_Q" + str(t)] for t in times)
                grouped[key][0] += 1
                grouped[key][1] += row["oracle_model_rejected_r4"]
            risk = Fraction(0)
            for n, k in grouped.values():
                probability = Fraction(k, n)
                # Sum per-label squared errors, not the JS k*(n-k)/(512*n) expression.
                risk += ((n-k)*probability**2 + k*(1-probability)**2) / 512
            scores[feature] = {"risk": str(risk), "groups": len(grouped),
                              "mixed": sum(0 < k < n for n, k in grouped.values())}
        expected[world] = {"world": world, "target": "reported_rejection_r4",
                           "event_count": sum(r["oracle_model_rejected_r4"] for r in rows),
                           "features": scores}
    comparisons = {label: compare(rows, expected) for label, rows in
                   (("r", outputs["r"]["results"]), ("b", outputs["b"]["worlds"]))}
    (out / "python_expected.json").write_text(json.dumps(expected, indent=2) + "\n")

    # Real CLI corruption probes use isolated copies; archived source is untouched.
    with tempfile.TemporaryDirectory() as tmp:
        sandbox = Path(tmp)
        for path in (CSV, RECEIPT, SCRIPTS["source_replay"], SCRIPTS["third_route"]):
            target = sandbox / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / path, target)
        for name in ('source_replay', 'third_route'):
            clean = run('clean_sandbox_' + name, ['node', str(sandbox / SCRIPTS[name])], sandbox)
            check(json.loads(clean.stdout) == outputs[name], 'sandbox clean control mismatch')
        bad = json.loads(json.dumps(archived))
        bad["results"][0]["features"]["F0"]["risk"] = "999"
        (sandbox / RECEIPT).write_text(json.dumps(bad))
        rejected_risk = run("negative_wrong_risk", ["node", str(sandbox / SCRIPTS["third_route"])], sandbox, ok=False)
        check('AssertionError [ERR_ASSERTION]: risk' in rejected_risk.stderr,
              'wrong-risk probe failed for an unexpected reason')
        (sandbox / CSV).write_bytes(b"X" + raw[1:])
        rejected_csv = run("negative_csv_byte", ["node", str(sandbox / SCRIPTS["source_replay"])], sandbox, ok=False)
        check('Error: original source SHA256 mismatch' in rejected_csv.stderr,
              'CSV probe failed for an unexpected reason')
    negative_comparator = []
    for label, change in (
        ("wrong_risk", lambda rs: rs[0]["features"]["F0"].update(risk="999")),
        ("duplicate_world", lambda rs: rs.__setitem__(1, json.loads(json.dumps(rs[0])))),
    ):
        bad = json.loads(json.dumps(outputs["r"]["results"]))
        change(bad)
        try:
            compare(bad, expected)
        except ValueError:
            negative_comparator.append({"case": label, "rejected": True})
        else:
            raise ValueError("Python comparison accepted " + label)
    paths = [NATIVE, CSV, RECEIPT, *SCRIPTS.values()]
    result = {
        "status": "COMPLETE", "research_id": "CODEX_R256_S52_ARCHIVED_CLI_REPLAY",
        "python": sys.version, "node": subprocess.check_output(["node", "--version"], text=True).strip(),
        "platform": platform.platform(), "seed": "N/A; full finite enumeration",
        "native_unittests": {"passed": 82, "failures": 0, "errors": 0},
        "archived_node_clis": {"passed": 4, "failed": 0}, "r_json_matches_archive": False,
        "r_computation_fields_match_archive": True, "archive_only_attestations": extra,
        "archive_only_attestations_not_direct_r_output": True,
        "cross_runtime_comparisons": comparisons, "source_replay": outputs["source_replay"],
        "third_route": outputs["third_route"], "negative_cli_probes_rejected": 2,
        "sandbox_clean_controls_passed": 2,
        "negative_comparator_probes": negative_comparator, "commands": commands,
        "source_sha256": {p: hashlib.sha256((root / p).read_bytes()).hexdigest() for p in paths},
        "source_git_blob": {p: hashlib.sha1(b"blob " + str(len((root/p).read_bytes())).encode()
                            + b"\0" + (root/p).read_bytes()).hexdigest() for p in paths},
        "scope": "NONBLIND_INTERNAL_ARTIFICIAL_E1; not external replication or empirical prediction",
        "new_E2": 0, "new_E3": 0, "external_team_replications": 0, "ci_status": "NOT_RUN",
        "historical_source_status": "Original R receipt kept unchanged; read with source audit addendum",
    }
    # Same-directory replace prevents readers seeing a truncated success receipt.
    with tempfile.NamedTemporaryFile(mode='w', dir=out, delete=False, encoding='utf-8') as tmp:
        tmp.write(json.dumps(result, indent=2) + '\n')
        receipt_tmp = Path(tmp.name)
    receipt_tmp.replace(out / 'execution.json')
    print(json.dumps({"status": "COMPLETE", "native_unittests": 82, "node_clis": 4,
                      "cross_runtime": comparisons, "negative_controls": 4}, indent=2))


if __name__ == "__main__":
    main()
