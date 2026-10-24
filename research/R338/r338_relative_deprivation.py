"""R338 constructed relative deprivation: reference gap with four Boolean gates."""
import argparse
import csv
import io
import json
import unittest
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "R338_ALL_128_ARTIFICIAL_COMPARISON_ATOMS.csv"
RESULT = ROOT / "R338_EXACT_64_CONDITIONS.json"
HEADER = ["own","reference","desire","entitlement","feasibility","external_attribution","policy","gap","grievance"]
EXPECTED = {"worlds": 64, "rows": 128, "gap_worlds": 16, "zero_gap_worlds": 48, "conjunctive_positive": 1, "gap_only_positive": 16, "agreement": 49, "disagreement": 15, "single_missing_gate_negative": 4, "zero_gap_both_zero": 48}

def build():
    rows, worlds = [], []
    checks = dict.fromkeys(EXPECTED, 0)
    for x, r, d, e, f, a in product((0, 1), repeat=6):
        gap = int(x == 0 and r == 1)
        conjunction = gap * d * e * f * a
        simple = gap
        worlds.append(dict(own=x, reference=r, desire=d, entitlement=e,
                           feasibility=f, external_attribution=a, gap=gap,
                           conjunctive_grievance=conjunction, gap_only_grievance=simple))
        rows.extend([[x, r, d, e, f, a, "CONJUNCTIVE", gap, conjunction],
                     [x, r, d, e, f, a, "GAP_ONLY", gap, simple]])
        checks["worlds"] += 1
        checks["rows"] += 2
        checks["gap_worlds"] += gap
        checks["zero_gap_worlds"] += 1 - gap
        checks["conjunctive_positive"] += conjunction
        checks["gap_only_positive"] += simple
        checks["agreement"] += int(conjunction == simple)
        checks["disagreement"] += int(conjunction != simple)
        checks["single_missing_gate_negative"] += int(gap == 1 and d+e+f+a == 3 and conjunction == 0)
        checks["zero_gap_both_zero"] += int(gap == 0 and conjunction == 0 and simple == 0)
    return rows, {"schema": "R338_frozen_reference_comparison_four_gate_v1",
                  "conditions": worlds, "checks": checks}

def render():
    rows, result = build()
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8"), (json.dumps(result, indent=2, ensure_ascii=True) + "\n").encode("utf-8")

def audit():
    source, results = render()
    assert SOURCE.read_bytes() == source, "CSV byte replay mismatch"
    assert RESULT.read_bytes() == results, "JSON byte replay mismatch"
    assert build()[1]["checks"] == EXPECTED, "frozen falsifier mismatch"

class Tests(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(build()[1]["checks"], EXPECTED)
    def test_unique_worlds(self):
        self.assertEqual(len({tuple(w[k] for k in ("own","reference","desire","entitlement","feasibility","external_attribution")) for w in build()[1]["conditions"]}), 64)
    def test_four_gate_knockouts(self):
        worlds = build()[1]["conditions"]
        for key in ("desire", "entitlement", "feasibility", "external_attribution"):
            target = [w for w in worlds if w["gap"] == 1 and sum(w[k] for k in ("desire","entitlement","feasibility","external_attribution")) == 3 and w[key] == 0]
            self.assertEqual(len(target), 1)
            self.assertEqual((target[0]["conjunctive_grievance"],target[0]["gap_only_grievance"]), (0,1))
    def test_positive_case(self):
        self.assertEqual(sum(w["conjunctive_grievance"] for w in build()[1]["conditions"]), 1)
    def test_zero_gap(self):
        self.assertTrue(all(w["conjunctive_grievance"] == w["gap_only_grievance"] == 0 for w in build()[1]["conditions"] if not w["gap"]))
    def test_byte_replay(self):
        audit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--audit", action="store_true")
    args = parser.parse_args()
    if args.test:
        outcome = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        if not outcome.wasSuccessful():
            raise SystemExit(1)
    if args.audit:
        audit()
        print("R338 PRODUCTION_REPLAY_PASS 128 constructed atoms 64 worlds")
