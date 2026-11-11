#!/usr/bin/env python3
"""Offline native R279/S75 replay; output must be a NEW directory.

Uses archived original programs and independent B gate as authored. Exact byte
identity and explicit checks remain active under -O; old asserts do not.
No third-party dependencies, network, research source edits or new scoring.
"""
import argparse
import csv
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CORE = "research/R279/"
S75 = "research/validation/"
CORE_SCRIPT = CORE+"r279_exact_forecast_calibration.py"
S75_SCRIPT = S75+"r279_s75_finite_sample_calibration_20261030.py"
B_SCRIPT = "research/evidence_audit/b_r279_s75_strict_receipt_20261030.js"
CORE_CSV = CORE+"R279_ALL_144_ORIGINAL_FORECAST_CALIBRATION_SOURCES.csv"
CORE_JSON = CORE+"R279_EXACT_RESULTS.json"
MACHINE = CORE+"R279_MACHINE_RECEIPT.json"
S75_CSV = S75+"R279_S75_ALL_144_EMPIRICAL_SOURCE_ATOMS.csv"
S75_JSON = S75+"R279_S75_EXACT_RESULTS.json"
PINS_SHA256 = "6baba19b76830c1be16657b8ce72dd4a718b6d53832e3f0845656870f0d2b69c"


def require(condition, reason):
    if not condition:
        raise ValueError(reason)


def sha(raw): return hashlib.sha256(raw).hexdigest()


def capture():
    """Single immutable byte snapshot, checked against committed source versions."""
    pin_bytes = (HERE/"pins.json").read_bytes()
    require(sha(pin_bytes) == PINS_SHA256, "PIN_MANIFEST_CHANGED")
    pins = json.loads(pin_bytes)
    found, inputs = {}, {}
    for name, pinned in pins.items():
        raw = (ROOT/name).read_bytes()
        blob = hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
        tracked = subprocess.check_output(["git", "rev-parse", "HEAD:"+name], cwd=ROOT, text=True).strip()
        require(blob == pinned == tracked, "PIN_MISMATCH:"+name)
        inputs[name] = raw
        found[name] = {"bytes": len(raw), "sha256": sha(raw), "git_blob": blob}
    for path, raw in ((HERE/"pins.json", pin_bytes), (HERE/"replay.py", Path(__file__).read_bytes())):
        found[str(path.relative_to(ROOT))] = {"bytes": len(raw), "sha256": sha(raw)}
    return inputs, found


def population_link(core, s75):
    original, empirical = json.loads(core), json.loads(s75)
    old = {(row["regime"], row["policy"]): row for row in original["world_results"]}
    new = {(row["regime"], row["policy"]): row for row in empirical["results"]}
    require(len(old) == len(new) == 9 and set(old) == set(new), "POPULATION_WORLD_LINK")
    names = {"REL": "population_reliability", "RES": "population_resolution",
             "UNC": "population_uncertainty", "Brier": "expected_population_Brier"}
    checks = 0
    for key in old:
        for metric, field in names.items():
            a, b = old[key][field], new[key]["population"][metric]
            require(type(a) is str and type(b) is str and Fraction(a) == Fraction(b), "POPULATION_VALUE_LINK")
            checks += 1
    return checks


def cases(csv_bytes, json_bytes):
    """Native reruns of old controls plus explicit zero-atom/type variants."""
    table = list(csv.reader(io.StringIO(csv_bytes.decode(), newline="")))
    for name in ("duplicate_source", "missing_source", "primitive_REL", "summary_Brier",
                 "E2_upgrade", "original_flag", "zero_mass_corruption", "zero_atoms_omitted", "E2_bool"):
        rows = [row[:] for row in table]
        document = json.loads(json_bytes)
        reason = "metadata gate"
        if name == "duplicate_source": rows[-1] = rows[1][:]; reason = "duplicate source"
        elif name == "missing_source": rows.pop(); reason = "CSV coverage"
        elif name == "primitive_REL": rows[1][4] = "999"; reason = "primitive REL"
        elif name == "summary_Brier": document["results"][0]["expected_empirical"]["Brier"] = "999"; reason = "summary Brier"
        elif name == "E2_upgrade": document["E2"] = 1
        elif name == "original_flag": document["original_R279_unchanged"] = False
        elif name == "zero_mass_corruption":
            next(row for row in rows[1:] if Fraction(row[3]) == 0)[3] = "1"; reason = "source mass"
        elif name == "zero_atoms_omitted": rows = [rows[0]]+[row for row in rows[1:] if Fraction(row[3]) > 0]; reason = "CSV coverage"
        else: document["E2"] = False
        text = io.StringIO(newline=""); csv.writer(text, lineterminator="\n").writerows(rows)
        yield name, text.getvalue().encode(), (json.dumps(document, indent=2)+"\n").encode(), reason


def run(output):
    output.mkdir(parents=True, exist_ok=False)
    inputs, before = capture()
    commands = []
    python = [sys.executable, "-B"]+(["-O"] if sys.flags.optimize else [])

    def execute(tag, argv):
        result = subprocess.run(argv, cwd=ROOT, capture_output=True, timeout=60)
        streams = {}
        for suffix, raw in (("stdout", result.stdout), ("stderr", result.stderr)):
            filename = tag+"."+suffix
            if raw: (output/filename).write_bytes(raw)
            streams[suffix] = {"bytes": len(raw), "sha256": sha(raw), "file": filename if raw else None}
        commands.append({"tag": tag, "argv": list(map(str, argv)), "cwd": str(ROOT),
                         "exit_code": result.returncode, "streams": streams})
        (output/"commands.json").write_text(json.dumps(commands, indent=2)+"\n")
        return result

    native = {}; controls = []
    with tempfile.TemporaryDirectory(prefix="codex-b-r279-native-") as temporary:
        sandbox = Path(temporary)
        core_dir, s75_dir = sandbox/"core", sandbox/"s75"
        core_dir.mkdir(); s75_dir.mkdir()
        core_script = core_dir/Path(CORE_SCRIPT).name
        s75_script = s75_dir/Path(S75_SCRIPT).name
        gate = sandbox/"original_B.js"
        for path, name in ((core_script, CORE_SCRIPT), (s75_script, S75_SCRIPT), (gate, B_SCRIPT)):
            path.write_bytes(inputs[name])
        node_version = execute("node-version", ["node", "--version"])
        require(node_version.returncode == 0, "NODE_UNAVAILABLE")
        tests = execute("original-84-tests", python+[str(core_script), "--test"])
        require(tests.returncode == 0 and re.search(rb"Ran 84 tests in", tests.stderr) is not None, "ORIGINAL_TESTS_FAIL")
        core_emit = execute("original-core-emit", python+[str(core_script), "--emit"])
        require(core_emit.returncode == 0, "CORE_EMIT_FAIL")
        selftest = execute("S75-selftest", python+[str(s75_script), "--selftest"])
        require(selftest.returncode == 0, "S75_SELFTEST_FAIL")
        s75_emit = execute("S75-emit", python+[str(s75_script), "--emit", str(s75_dir)])
        require(s75_emit.returncode == 0, "S75_EMIT_FAIL")
        emitted = {}
        for name in (CORE_CSV, CORE_JSON, MACHINE, S75_CSV, S75_JSON):
            path = (core_dir if name.startswith(CORE) else s75_dir)/Path(name).name
            raw = path.read_bytes()
            require(raw == inputs[name], "NATIVE_BYTE_MISMATCH:"+name)
            emitted[name] = raw
            native[name] = {"bytes": len(raw), "sha256": sha(raw), "byte_equal": True}
        machine = json.loads(emitted[MACHINE])
        require(machine == json.loads(core_emit.stdout) and
                machine["source_sha256"] == sha(emitted[CORE_CSV]) and
                machine["results_sha256"] == sha(emitted[CORE_JSON]), "MACHINE_DIGEST_MISMATCH")
        (output/"native-machine-receipt.json").write_bytes(emitted[MACHINE])
        linked = population_link(emitted[CORE_JSON], emitted[S75_JSON])
        for label, data in (("archive", inputs), ("emitted", emitted)):
            csv_path, json_path = sandbox/(label+".csv"), sandbox/(label+".json")
            csv_path.write_bytes(data[S75_CSV]); json_path.write_bytes(data[S75_JSON])
            result = execute("B-"+label, ["node", str(gate), str(csv_path), str(json_path)])
            require(result.returncode == 0, "B_NATIVE_FAIL:"+label)
            summary = json.loads(result.stdout)
            require(type(summary) is dict and set(summary) == {"status", "rows", "worlds", "positive"} and
                    summary["status"] == "PASS" and all(type(summary[key]) is int and summary[key] == value
                    for key, value in (("rows", 144), ("worlds", 9), ("positive", 99))), "B_NATIVE_SUMMARY")
        for label, bad_csv, bad_json, expected in cases(inputs[S75_CSV], inputs[S75_JSON]):
            csv_path, json_path = sandbox/"bad.csv", sandbox/"bad.json"
            csv_path.write_bytes(bad_csv); json_path.write_bytes(bad_json)
            result = execute(label, ["node", str(gate), str(csv_path), str(json_path)])
            marker = ("Error: "+expected).encode()
            require(result.returncode == 1 and not result.stdout and marker in result.stderr and
                    b"SyntaxError:" not in result.stderr and b"ReferenceError:" not in result.stderr,
                    "NEGATIVE_NOT_SCIENTIFICALLY_REJECTED:"+label)
            controls.append({"name": label, "exit_code": 1, "expected_error": expected,
                             "csv_sha256": sha(bad_csv), "json_sha256": sha(bad_json)})
    _, after = capture()
    require(before == after, "SOURCE_CHANGED_DURING_REPLAY")
    result = {"status": "PASS_BOUNDED_NATIVE_CALIBRATION_REPLAY", "utc": datetime.now(timezone.utc).isoformat(),
              "source_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "python": sys.version, "optimized": bool(sys.flags.optimize),
              "node": node_version.stdout.decode().strip(), "original_unittest_methods": 84,
              "S75_selftest_invocations": 1, "S75_selftest_is_unittest_count": False,
              "B_native_invocations": 2, "B_native_summary": summary,
              "population_field_links": linked, "native_identity": native, "negative_controls": controls,
              "source_rows_per_S75_file": 144, "positive_rows": 99, "zero_mass_rows_retained": 45,
              "original_asserts_under_O": "DISABLED_NOT_CLAIMED_AS_ACTIVE_CHECKS",
              "sources_before_after_equal": True, "sources": before,
              "independent_algorithm_credit": "ARCHIVED_B_GATE_AS_AUTHORED_NO_NEW_MATHEMATICAL_ALGORITHM_CLAIM",
              "numerical_discrepancies_found": 0, "formal_scientific_reacceptance": "NOT_RUN",
              "full_repository_tests": "NOT_RUN", "production_adoption": "NOT_RUN", "CI": "NOT_RUN",
              "other_platforms": "NOT_RUN", "new_human_scores": 0, "new_E2_E3": 0,
              "external_team_replications": 0, "formal_queue_closures": 0,
              "R073": "FROZEN_UNCHANGED", "PESEN_v0.1": "FROZEN_UNCHANGED"}
    (output/"summary.json").write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({key: result[key] for key in ("status", "python", "optimized", "node", "original_unittest_methods", "native_identity", "population_field_links")}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    destination = parser.parse_args().output.resolve()
    try: run(destination)
    except (OSError, ValueError, KeyError, TypeError, ZeroDivisionError, subprocess.SubprocessError) as exc:
        # A failed run never writes a success summary. Existing output is never reused.
        print(json.dumps({"status": "FAILED_NATIVE_REPLAY", "reason": str(exc)[:240]}))
        raise SystemExit(2)
