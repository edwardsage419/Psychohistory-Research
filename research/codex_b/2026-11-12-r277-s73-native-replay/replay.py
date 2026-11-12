#!/usr/bin/env python3
"""Run the unchanged archived S73 Node entry points; no new scientific algorithm."""
import argparse
import copy
import hashlib
import io
import json
import platform
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BASE = "d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c"
R = "research/validation/r277_s73_temporal_subsampling_20261030.js"
B = "research/evidence_audit/b_r277_s73_transition_kernel_receipt_audit_20261030.js"
CSV = "research/validation/R277_S73_OBSERVED_TRIPLETS_72_ROWS_2026-10-30.csv"
JSON = "research/validation/R277_S73_EXACT_RESULTS_2026-10-30.json"
CONTROLS = ["probability", "confusion", "TV", "evidence", "freeze",
            "missing-window", "duplicate-CSV", "missing-CSV"]
EXPECTED = {"audit": {"status": "PASS", "probability_cells": 72,
                      "confusion_cells": 27, "tv_cells": 9, "csv_rows": 72},
            "mutations_rejected": CONTROLS}


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def identity(data):
    return {"bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()}


def capture(pins):
    result = {}
    for path, expected in pins.items():
        data = (ROOT / path).read_bytes()
        require(identity(data) == expected, "SOURCE_IDENTITY:" + path)
        frozen = subprocess.check_output(["git", "show", BASE + ":" + path], cwd=ROOT)
        require(data == frozen, "SOURCE_VERSION:" + path)
        result[path] = expected
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    require(not out.exists(), "OUTPUT_EXISTS: use a new output directory")
    out.mkdir(parents=True)
    pins = json.loads((HERE / "pins.json").read_text())
    summary = {"status": "FAIL", "base_main": BASE,
               "source_freeze": "923a161bbdc012c138e53f1fa316e6085ff2704e",
               "S73_freeze": "53e3b18b28d46c0c5e26194dd8e85bc408450af6",
               "python": sys.version, "platform": platform.platform(),
               "harness": identity(Path(__file__).read_bytes()),
               "pin_manifest": identity((HERE / "pins.json").read_bytes()),
               "commands": [], "external_bad_files": [], "artifact_comparisons": []}
    streams = {}

    def run(label, argv, code=0, error=None):
        p = subprocess.run(argv, cwd=ROOT, capture_output=True, timeout=30)
        record = {"label": label, "argv": [str(a) for a in argv], "exit_code": p.returncode,
                  "expected_exit": code, "expected_domain_error": error, "streams": {}}
        for kind, data in [("stdout", p.stdout), ("stderr", p.stderr)]:
            name = label + "." + kind
            streams[name] = data
            record["streams"][kind] = {"member": name, **identity(data)}
        summary["commands"].append(record)
        require(p.returncode == code, "EXIT:" + label)
        if error:
            require(not p.stdout, "BAD_INPUT_SUCCESS_OUTPUT:" + label)
            require(("Error: " + error + "\n").encode() in p.stderr,
                    "DOMAIN_ERROR:" + label)
            require(b"SyntaxError:" not in p.stderr and b"ReferenceError:" not in p.stderr,
                    "INVALID_REJECTION:" + label)
        else:
            require(not p.stderr, "UNEXPECTED_STDERR:" + label)
        return p.stdout

    def audit(label, node, b, js, csv):
        data = run(label, [node, b, js, csv])
        require(json.loads(data) == EXPECTED, "INCOMPLETE_AUDIT:" + label)

    try:
        summary["sources_before"] = capture(pins)
        node = shutil.which("node")
        require(node is not None, "NODE_NOT_AVAILABLE")
        summary["node"] = run("node-version", [node, "--version"]).decode().strip()
        with tempfile.TemporaryDirectory(prefix="r277-s73-native-") as tmp:
            t = Path(tmp)
            r, b = t / "R.js", t / "B.js"
            r.write_bytes((ROOT / R).read_bytes())
            b.write_bytes((ROOT / B).read_bytes())
            original_json, original_csv = t / "archived.json", t / "archived.csv"
            original_json.write_bytes((ROOT / JSON).read_bytes())
            original_csv.write_bytes((ROOT / CSV).read_bytes())
            default = run("R-default", [node, r])
            require(default == b"PASS R277 S73 192 source, 72 observations, analytic crosscheck, 2 mutation controls\n",
                    "R_DEFAULT_OUTPUT")
            generated = {}
            for label, flag, path, archived in [
                ("R-csv", "--csv", t / "generated.csv", original_csv),
                ("R-json", "--json", t / "generated.json", original_json),
            ]:
                data = run(label, [node, r, flag])
                path.write_bytes(data)
                equal = data == archived.read_bytes()
                summary["artifact_comparisons"].append({"label": label,
                    "archive_path": CSV if flag == "--csv" else JSON,
                    "generated": identity(data), "byte_identical": equal})
                require(equal, "ARTIFACT_BYTES:" + label)
                generated[flag] = path
            audit("B-archived", node, b, original_json, original_csv)
            audit("B-generated", node, b, generated["--json"], generated["--csv"])
            lines = original_csv.read_text().splitlines()
            reversed_csv = t / "reversed.csv"
            reversed_csv.write_text("\n".join([lines[0], *reversed(lines[1:])]) + "\n")
            audit("B-reversed-rows", node, b, original_json, reversed_csv)
            summary["reordered_csv"] = identity(reversed_csv.read_bytes())

            # Exactly the eight archived B controls, now supplied as real CLI files.
            base = json.loads(original_json.read_bytes())
            for label, error in zip(CONTROLS, ["probability", "confusion", "TV", "evidence",
                                             "source identity", "windows", "CSV coverage", "CSV coverage"]):
                obj, raw = copy.deepcopy(base), original_csv.read_bytes()
                if label == "probability":
                    obj["windows"]["B_ODD"]["observation_probability"]["ANTIPERSISTENT"]["000"] = "0"
                elif label == "confusion":
                    obj["windows"]["A_ADJACENT"]["confusion"]["IID_FAIR"]["IID_FAIR"] = "0"
                elif label == "TV":
                    obj["windows"]["B_ODD"]["tv"]["ANTIPERSISTENT|PERSISTENT"] = "1/8"
                elif label == "evidence":
                    obj["evidence"] = "E3"
                elif label == "freeze":
                    obj["original_R277_freeze"] = "wrong"
                elif label == "missing-window":
                    del obj["windows"]["C_EVEN"]
                elif label == "duplicate-CSV":
                    raw += (lines[1] + "\n").encode()
                elif label == "missing-CSV":
                    raw = ("\n".join(lines[:-1]) + "\n").encode()
                js, csv = t / (label + ".json"), t / (label + ".csv")
                js.write_text(json.dumps(obj, indent=2) + "\n")
                csv.write_bytes(raw)
                summary["external_bad_files"].append({"label": label, "json": identity(js.read_bytes()),
                    "csv": identity(raw), "domain_error": error})
                run("B-reject-" + label, [node, b, js, csv], 1, error)
            require(r.read_bytes() == (ROOT / R).read_bytes(), "TEMP_R_CHANGED")
            require(b.read_bytes() == (ROOT / B).read_bytes(), "TEMP_B_CHANGED")
            require(original_json.read_bytes() == (ROOT / JSON).read_bytes(), "TEMP_JSON_CHANGED")
            require(original_csv.read_bytes() == (ROOT / CSV).read_bytes(), "TEMP_CSV_CHANGED")
        summary["sources_after"] = capture(pins)
        summary["status"] = "COMPLETE_BOUNDED_NATIVE_REPLAY"
        summary["scientific_status"] = "UNCHANGED_EXPLORATORY_E1_NONBLIND_INTERNAL"
        summary["human_scoring"] = "NOT_RUN"
        summary["external_team_replication"] = "NOT_RUN"
    except Exception as exc:
        summary["failure"] = str(exc)
        raise
    finally:
        archive = out / "streams.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            for name, data in streams.items():
                info = tarfile.TarInfo(name)
                info.size = len(data)
                info.mtime = 0
                tar.addfile(info, io.BytesIO(data))
        summary["stream_archive"] = identity(archive.read_bytes())
        (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"status": summary["status"], "commands": len(summary["commands"]),
                      "streams": len(streams), "source_identities": len(pins),
                      "byte_identical_artifacts": len(summary["artifact_comparisons"]),
                      "bad_files_rejected": len(summary["external_bad_files"])}))


if __name__ == "__main__":
    main()
