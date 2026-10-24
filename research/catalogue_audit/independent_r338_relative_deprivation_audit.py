"""Independent R338 enumerator; never imports R338 production code."""
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "R338"
CSV_PATH = ROOT / "R338_ALL_128_ARTIFICIAL_COMPARISON_ATOMS.csv"
JSON_PATH = ROOT / "R338_EXACT_64_CONDITIONS.json"

def independent():
    header = ["own","reference","desire","entitlement","feasibility","external_attribution","policy","gap","grievance"]
    records = []
    conditions = []
    counts = {"worlds":0,"rows":0,"gap_worlds":0,"zero_gap_worlds":0,
              "conjunctive_positive":0,"gap_only_positive":0,"agreement":0,
              "disagreement":0,"single_missing_gate_negative":0,"zero_gap_both_zero":0}
    for index in range(64):
        x, r, d, e, f, a = [(index >> shift) & 1 for shift in (5,4,3,2,1,0)]
        gap = 1 if (r > x) else 0
        full = 1 if (gap and all((d,e,f,a))) else 0
        simple = gap
        conditions.append({"own":x,"reference":r,"desire":d,"entitlement":e,
                           "feasibility":f,"external_attribution":a,"gap":gap,
                           "conjunctive_grievance":full,"gap_only_grievance":simple})
        records.append([x,r,d,e,f,a,"CONJUNCTIVE",gap,full])
        records.append([x,r,d,e,f,a,"GAP_ONLY",gap,simple])
        counts["worlds"] += 1
        counts["rows"] += 2
        counts["gap_worlds"] += gap
        counts["zero_gap_worlds"] += 1-gap
        counts["conjunctive_positive"] += full
        counts["gap_only_positive"] += simple
        counts["agreement"] += (full == simple)
        counts["disagreement"] += (full != simple)
        counts["single_missing_gate_negative"] += (gap == 1 and d+e+f+a == 3 and full == 0)
        counts["zero_gap_both_zero"] += (gap == 0 and full == simple == 0)
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(records)
    source = buf.getvalue().encode()
    results = (json.dumps({"schema":"R338_frozen_reference_comparison_four_gate_v1",
                           "conditions":conditions,"checks":counts}, indent=2, ensure_ascii=True)+"\n").encode()
    return source, results, counts

def verify(actual_csv, actual_json, expected_csv, expected_json):
    assert actual_csv == expected_csv, "independent CSV replay mismatch"
    assert actual_json == expected_json, "independent JSON replay mismatch"

if __name__ == "__main__":
    expected_csv, expected_json, checks = independent()
    assert checks == {"worlds":64,"rows":128,"gap_worlds":16,"zero_gap_worlds":48,
                      "conjunctive_positive":1,"gap_only_positive":16,"agreement":49,
                      "disagreement":15,"single_missing_gate_negative":4,"zero_gap_both_zero":48}
    verify(CSV_PATH.read_bytes(), JSON_PATH.read_bytes(), expected_csv, expected_json)
    mutated_csv = expected_csv.replace(b",CONJUNCTIVE,1,1\n", b",CONJUNCTIVE,1,0\n", 1)
    assert mutated_csv != expected_csv
    try:
        verify(mutated_csv, expected_json, expected_csv, expected_json)
    except AssertionError:
        pass
    else:
        raise AssertionError("CSV tamper was accepted")
    mutated_json = expected_json.replace(b'"conjunctive_grievance": 1', b'"conjunctive_grievance": 0', 1)
    assert mutated_json != expected_json
    try:
        verify(expected_csv, mutated_json, expected_csv, expected_json)
    except AssertionError:
        pass
    else:
        raise AssertionError("JSON tamper was accepted")
    print("R338 INDEPENDENT_AUDIT_PASS 128 rows 64 worlds two tamper rejections")
