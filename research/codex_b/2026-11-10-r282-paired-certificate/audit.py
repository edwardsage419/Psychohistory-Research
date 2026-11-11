"""Bind S78 same-source pair declarations to a new GF(2) rank certificate.

Pinned archived B retains observational/inverse checks. This adds four previously
unchecked paired integers and schedule declaration, not new scientific scoring.
"""
import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile

from algebra import SCHEDULES, linear_states, evaluate, certificates, paired_counts, require

ROOT = Path(__file__).resolve().parents[3]
B_PATH = ROOT/"research/evidence_audit/b_r282_s78_strict_remote_receipt_gate_20261030.js"
B_BLOB = "b5fbbe829512f5d9d1790f55947773d23acec9e3"
FIELDS = ("schedule","source_index","source_bits","t0","t1","t2","eA0","eB0","eA1","eB1","TERMINAL","TRACE","TRACE_E0","TRACE_EALL")
ROOT_KEYS = {"study","freeze_commit","evidence","schedules","source_cases","source_mass","regimes",
             "original_R282_paired_counts","R073","PESEN_v0_1","new_E2","new_E3"}


def strict_json(raw):
    def unique(pairs):
        result = {}
        for key,value in pairs:
            require(key not in result, "DUPLICATE_JSON_KEY")
            result[key] = value
        return result
    def invalid(_): raise ValueError("NONFINITE_JSON_CONSTANT")
    return json.loads(raw, object_pairs_hook=unique, parse_constant=invalid)


def audit(csv_path, json_path):
    # Each route gets these same captured bytes, not a second live input read.
    csv_raw, json_raw, b_raw = Path(csv_path).read_bytes(), Path(json_path).read_bytes(), B_PATH.read_bytes()
    blob = hashlib.sha1(b"blob "+str(len(b_raw)).encode()+b"\0"+b_raw).hexdigest()
    require(blob == B_BLOB, "ORIGINAL_B_CODE_CHANGED")
    doc = strict_json(json_raw)
    require(type(doc) is dict and set(doc) == ROOT_KEYS, "JSON_SCHEMA")
    require(type(doc["schedules"]) is list and doc["schedules"] == list(SCHEDULES), "SCHEDULE_DECLARATION")
    declared = doc["original_R282_paired_counts"]
    require(type(declared) is dict and set(declared) == set(SCHEDULES[1:]) and
            all(type(v) is list and len(v) == 2 and all(type(x) is int for x in v) for v in declared.values()), "PAIRED_SHAPE_OR_TYPE")
    derived = paired_counts()
    require(declared == derived, "PAIRED_RECEIPT")
    # Preserve the independent archived inverse route rather than rewrite it.
    with tempfile.TemporaryDirectory(prefix="codex-b-r282-gate-") as temporary:
        folder = Path(temporary); script, data, receipt = folder/"original_B.js",folder/"sources.csv",folder/"receipt.json"
        for path,raw in ((script,b_raw),(data,csv_raw),(receipt,json_raw)): path.write_bytes(raw)
        child = subprocess.run(["node",str(script),str(data),str(receipt)],capture_output=True,timeout=60)
        require(child.returncode == 0, "ORIGINAL_B_REJECTED")
        original = strict_json(child.stdout)
        expected = {"rows":192,"regimes":4,"independent_schedule_state_triples":192,"tv_cells":36}
        require(type(original) is dict and original == expected and
                all(type(original.get(key)) is int for key in expected), "ORIGINAL_B_SUMMARY")
    table = list(csv.reader(io.StringIO(csv_raw.decode("utf-8"),newline=""),strict=True))
    require(len(table) == 193 and tuple(table[0]) == FIELDS, "CSV_SHAPE")
    trajectories = {}; output_checks = 0
    for cells in table[1:]:
        require(len(cells) == 14, "CSV_WIDTH")
        row = dict(zip(FIELDS,cells)); schedule,bits = row["schedule"],row["source_bits"]
        require(schedule in SCHEDULES and bits == f'{int(row["source_index"]):06b}', "SOURCE_KEY")
        identity = (schedule,int(row["source_index"]))
        require(identity not in trajectories, "DUPLICATE_SOURCE")
        states = tuple(''.join(str(evaluate(mask,bits)) for mask in state) for state in linear_states(schedule))
        require(tuple(row[f"t{time}"] for time in (0,1,2)) == states, "SYMBOLIC_TRACE")
        output_checks += 4
        trajectories[identity] = states
    require(set(trajectories) == {(s,i) for s in SCHEDULES for i in range(64)}, "SOURCE_UNIVERSE")
    counted = {s: [sum(trajectories[(s,i)][t] != trajectories[("SYNC",i)][t] for i in range(64)) for t in (1,2)] for s in SCHEDULES[1:]}
    require(counted == derived, "CSV_PAIRS_VS_RANK")
    return {"status":"PASS_PAIRED_GF2_SUPPLEMENT", "source_rows":192,
            "symbolic_output_bit_checks":output_checks, "paired_integer_fields":4,
            "paired_counts_from_GF2":derived, "paired_counts_from_CSV":counted,
            "certificate":certificates(), "linear_state_masks":{s:linear_states(s) for s in SCHEDULES},
            "original_B":original, "snapshot_sha256":{name:hashlib.sha256(raw).hexdigest() for name,raw in (("csv",csv_raw),("json",json_raw),("original_B",b_raw))},
            "new_human_scores":0,"new_E2_E3":0,"formal_scientific_reacceptance":"NOT_RUN"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__);parser.add_argument("csv");parser.add_argument("json")
    args = parser.parse_args()
    try: result = audit(args.csv,args.json)
    except (OSError,ValueError,KeyError,TypeError,UnicodeError,csv.Error,subprocess.SubprocessError) as exc:
        print(json.dumps({"status":"REJECTED","reason":str(exc)[:160]}));raise SystemExit(2)
    print(json.dumps(result,indent=2))
