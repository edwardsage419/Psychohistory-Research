"""Adversarial mutation controls for the archived R272 fail-closed candidate.

Internal nonblind engineering audit. Standard library only.
No import of the original R272 generator or modification of frozen evidence.
"""
import hashlib
import io
import json
import sys
import types
import zipfile
from pathlib import Path

name = "r272_failclosed_independent_receipt_gate_20261102.py"
local = Path(__file__).with_name(name)
if local.exists():
    source = local.read_bytes()
else:
    archive = Path(__file__).with_name("R272_P0_FAILCLOSED_CANDIDATE_20261102.zip")
    archive_bytes = archive.read_bytes()
    expected_zip = "f23b04706b60ac70bdbee6f051a74551779fb9d9a9b9af08c96cda345b055151"
    if hashlib.sha256(archive_bytes).hexdigest() != expected_zip:
        raise RuntimeError("candidate ZIP SHA256 mismatch")
    with zipfile.ZipFile(io.BytesIO(archive_bytes)) as z:
        members = [n for n in z.namelist() if n == name or n.endswith("/" + name)]
        if len(members) != 1:
            raise RuntimeError("candidate ZIP member identity mismatch")
        source = z.read(members[0])

candidate = types.ModuleType("r272_candidate")
exec(compile(source, name, "exec"), candidate.__dict__)
m = candidate
csv_bytes, compact_results, compact_receipt = m.synthetic_fixture()
if hashlib.sha256(csv_bytes).hexdigest() != m.CSV_SHA:
    raise RuntimeError("CSV archived SHA256 mismatch")
result_bytes = (json.dumps(json.loads(compact_results), indent=2) + "\n").encode()
receipt = json.loads(compact_receipt)
receipt["results_sha256"] = m.sha(result_bytes)
receipt_bytes = (json.dumps(receipt, indent=2) + "\n").encode()
if hashlib.sha256(result_bytes).hexdigest() != m.JSON_SHA:
    raise RuntimeError("result archived SHA256 mismatch")
if m.git_blob(receipt_bytes) != "85d36858911a7eb79c73c607cddf45ea88852a60":
    raise RuntimeError("receipt archived Git blob mismatch")
if m.verify(csv_bytes, result_bytes, receipt_bytes, pins=True)["status"] != "PASS":
    raise RuntimeError("archive reconstruction did not pass pinned checker")

def rejected(label, csv_data=csv_bytes, result_data=result_bytes, receipt_data=None):
    if receipt_data is None:
        record = json.loads(receipt_bytes)
        record["source_sha256"] = hashlib.sha256(csv_data).hexdigest()
        record["results_sha256"] = hashlib.sha256(result_data).hexdigest()
        receipt_data = json.dumps(record).encode()
    try:
        m.verify(csv_data, result_data, receipt_data, pins=False)
    except (ValueError, UnicodeError, TypeError, KeyError):
        print(label + ": REJECT")
        return True
    print(label + ": FALSE_ACCEPT")
    return False

outcomes = []
text = csv_bytes.decode()
header = text.split("\n", 1)[0]
outcomes.append(rejected("duplicate_header", csv_data=text.replace(header, header + ",world", 1).encode()))
lines = text.splitlines()
lines[1] += ",unreported"
outcomes.append(rejected("extra_row_field", csv_data=("\n".join(lines) + "\n").encode()))
outcomes.append(rejected("missing_source", csv_data=("\n".join(text.splitlines()[:-1]) + "\n").encode()))
obj = json.loads(result_bytes)
obj["world_results"][0]["source_enumeration_equals_independent_binomial_theory"] = False
outcomes.append(rejected("false_world_analytic_flag", result_data=json.dumps(obj).encode()))
idx = result_bytes.find(b'"full_ordered_source_types": 64')
if idx < 0:
    raise RuntimeError("nested world key missing from archived fixture")
duplicate_key = result_bytes[:idx] + b'"full_ordered_source_types": 64, ' + result_bytes[idx:]
outcomes.append(rejected("duplicate_nested_result_key", result_data=duplicate_key))
obj = json.loads(result_bytes)
obj["external_replication"] = "PASS"
outcomes.append(rejected("unearned_external_claim", result_data=json.dumps(obj).encode()))
obj = json.loads(receipt_bytes)
obj["all_complete_original_sources"] = float("nan")
outcomes.append(rejected("nonstandard_nan_receipt", receipt_data=json.dumps(obj).encode()))
obj = json.loads(receipt_bytes)
obj["external_real_human_E2"] = 1
outcomes.append(rejected("receipt_extra_e2", receipt_data=json.dumps(obj).encode()))
summary = {"archive_hashes_match": True, "controls": len(outcomes),
           "rejected": sum(outcomes), "all_pass": all(outcomes)}
print(json.dumps(summary, sort_keys=True))
if not all(outcomes):
    sys.exit(1)
