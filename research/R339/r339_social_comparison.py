"""R339 constructed social comparison target-selection contrast."""
import argparse
import csv
import io
import json
import unittest
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "R339_ALL_100_ARTIFICIAL_TARGET_ATOMS.csv"
RESULT = ROOT / "R339_EXACT_50_CONDITIONS.json"
HEADER = ["objective_available","candidate_a","candidate_b","policy","target","estimate","absolute_error"]
EXPECTED = {"worlds":50,"rows":100,"objective_worlds":25,"no_objective_worlds":25,"objective_both_none":25,"agreement":40,"disagreement":10,"similar_A":17,"similar_B":8,"high_A":15,"high_B":10,"similar_better":8,"similar_equal":17,"similar_worse":0}

def build():
    rows, worlds = [], []
    checks = dict.fromkeys(EXPECTED, 0)
    for objective, a, b in product((0,1), range(5), range(5)):
        similar = "NONE" if objective else ("A" if abs(a-2) <= abs(b-2) else "B")
        high = "NONE" if objective else ("A" if a >= b else "B")
        s_est = 2 if objective else (a if similar == "A" else b)
        h_est = 2 if objective else (a if high == "A" else b)
        s_err, h_err = abs(s_est-2), abs(h_est-2)
        worlds.append(dict(objective_available=objective, candidate_a=a, candidate_b=b,
                           similar_target=similar, similar_estimate=s_est, similar_error=s_err,
                           high_target=high, high_estimate=h_est, high_error=h_err))
        rows.extend([[objective,a,b,"SIMILARITY",similar,s_est,s_err],
                     [objective,a,b,"HIGH_SCORE",high,h_est,h_err]])
        checks["worlds"] += 1
        checks["rows"] += 2
        checks["objective_worlds"] += objective
        checks["no_objective_worlds"] += 1-objective
        checks["objective_both_none"] += int(objective == 1 and similar == high == "NONE")
        checks["agreement"] += int(similar == high)
        checks["disagreement"] += int(similar != high)
        checks["similar_A"] += int(similar == "A")
        checks["similar_B"] += int(similar == "B")
        checks["high_A"] += int(high == "A")
        checks["high_B"] += int(high == "B")
        checks["similar_better"] += int(not objective and s_err < h_err)
        checks["similar_equal"] += int(not objective and s_err == h_err)
        checks["similar_worse"] += int(not objective and s_err > h_err)
    return rows, {"schema":"R339_frozen_two_target_similarity_v1","conditions":worlds,"checks":checks}

def render():
    rows, results = build()
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return stream.getvalue().encode(), (json.dumps(results,indent=2,ensure_ascii=True)+"\n").encode()

def audit():
    source, result = render()
    assert SOURCE.read_bytes() == source, "CSV byte replay mismatch"
    assert RESULT.read_bytes() == result, "JSON byte replay mismatch"
    assert build()[1]["checks"] == EXPECTED

class Tests(unittest.TestCase):
    def test_counts(self): self.assertEqual(build()[1]["checks"], EXPECTED)
    def test_unique_worlds(self):
        w = build()[1]["conditions"]
        self.assertEqual(len({(z["objective_available"],z["candidate_a"],z["candidate_b"]) for z in w}),50)
    def test_objective_none(self):
        self.assertTrue(all(z["similar_target"] == z["high_target"] == "NONE" and z["similar_estimate"] == z["high_estimate"] == 2 for z in build()[1]["conditions"] if z["objective_available"]))
    def test_nearest_target_never_worse(self):
        self.assertTrue(all(z["similar_error"] <= z["high_error"] for z in build()[1]["conditions"] if not z["objective_available"]))
    def test_witnesses(self):
        w = build()[1]["conditions"]
        get = lambda a,b: next(z for z in w if (z["objective_available"],z["candidate_a"],z["candidate_b"]) == (0,a,b))
        self.assertEqual((get(2,4)["similar_target"],get(2,4)["high_target"]),("A","B"))
        self.assertEqual((get(4,2)["similar_target"],get(4,2)["high_target"]),("B","A"))
    def test_byte_replay(self): audit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--audit",action="store_true")
    args = parser.parse_args()
    if args.test:
        outcome = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        if not outcome.wasSuccessful(): raise SystemExit(1)
    if args.audit:
        audit()
        print("R339 PRODUCTION_REPLAY_PASS 100 artificial atoms 50 worlds")
