"""Independent R339 enumeration: no import of production module."""
import csv
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "R339"

def independent():
    header = ["objective_available","candidate_a","candidate_b","policy","target","estimate","absolute_error"]
    records, conditions = [], []
    counts = dict.fromkeys(("worlds","rows","objective_worlds","no_objective_worlds",
        "objective_both_none","agreement","disagreement","similar_A","similar_B",
        "high_A","high_B","similar_better","similar_equal","similar_worse"),0)
    for n in range(50):
        objective = n // 25
        a = (n % 25) // 5
        b = n % 5
        s = "NONE" if objective else ("A" if abs(2-a) <= abs(2-b) else "B")
        h = "NONE" if objective else ("A" if a >= b else "B")
        se = 2 if objective else (a if s == "A" else b)
        he = 2 if objective else (a if h == "A" else b)
        sd, hd = abs(2-se), abs(2-he)
        conditions.append({"objective_available":objective,"candidate_a":a,"candidate_b":b,
            "similar_target":s,"similar_estimate":se,"similar_error":sd,
            "high_target":h,"high_estimate":he,"high_error":hd})
        records.extend([[objective,a,b,"SIMILARITY",s,se,sd],[objective,a,b,"HIGH_SCORE",h,he,hd]])
        counts["worlds"] += 1
        counts["rows"] += 2
        counts["objective_worlds"] += objective
        counts["no_objective_worlds"] += 1-objective
        counts["objective_both_none"] += (objective == 1 and s == h == "NONE")
        counts["agreement"] += (s == h)
        counts["disagreement"] += (s != h)
        counts["similar_A"] += (s == "A")
        counts["similar_B"] += (s == "B")
        counts["high_A"] += (h == "A")
        counts["high_B"] += (h == "B")
        counts["similar_better"] += (not objective and sd < hd)
        counts["similar_equal"] += (not objective and sd == hd)
        counts["similar_worse"] += (not objective and sd > hd)
    buf = io.StringIO(newline="")
    writer = csv.writer(buf, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(records)
    return buf.getvalue().encode(), (json.dumps({"schema":"R339_frozen_two_target_similarity_v1",
        "conditions":conditions,"checks":counts},indent=2,ensure_ascii=True)+"\n").encode(), counts

def verify(actual_csv,actual_json,expected_csv,expected_json):
    assert actual_csv == expected_csv, "CSV replay mismatch"
    assert actual_json == expected_json, "JSON replay mismatch"

if __name__ == "__main__":
    source, result, checks = independent()
    assert checks == {"worlds":50,"rows":100,"objective_worlds":25,"no_objective_worlds":25,
        "objective_both_none":25,"agreement":40,"disagreement":10,"similar_A":17,
        "similar_B":8,"high_A":15,"high_B":10,"similar_better":8,"similar_equal":17,"similar_worse":0}
    verify((ROOT/"R339_ALL_100_ARTIFICIAL_TARGET_ATOMS.csv").read_bytes(),
           (ROOT/"R339_EXACT_50_CONDITIONS.json").read_bytes(),source,result)
    corrupt_csv = source.replace(b",SIMILARITY,A,2,0\n",b",SIMILARITY,B,2,0\n",1)
    assert corrupt_csv != source
    try: verify(corrupt_csv,result,source,result)
    except AssertionError: pass
    else: raise AssertionError("CSV tamper accepted")
    corrupt_json = result.replace(b'"similar_error": 0',b'"similar_error": 1',1)
    assert corrupt_json != result
    try: verify(source,corrupt_json,source,result)
    except AssertionError: pass
    else: raise AssertionError("JSON tamper accepted")
    print("R339 INDEPENDENT_AUDIT_PASS 100 artificial atoms 50 worlds two tamper rejections")
