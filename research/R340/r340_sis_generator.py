#!/usr/bin/env python3
"""R340 frozen two-node SIS generator. Artificial E1 only."""
import argparse
import csv
import io
import json
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STATES = ("00", "01", "10", "11")
BETAS = ("1/2", "1", "2")
CSV_PATH = ROOT / "R340_ALL_48_ARTIFICIAL_GENERATOR_ATOMS.csv"
JSON_PATH = ROOT / "R340_EXACT_3_GENERATORS.json"

def matrix(beta_text):
    beta = Fraction(beta_text)
    q = [[Fraction(0) for _ in STATES] for _ in STATES]
    for i, state in enumerate(STATES):
        for bit in range(2):
            nxt = list(state)
            if state[bit] == "1":
                nxt[bit] = "0"
                rate = Fraction(1)
            elif state[1-bit] == "1":
                nxt[bit] = "1"
                rate = beta
            else:
                continue
            j = STATES.index("".join(nxt))
            q[i][j] += rate
        q[i][i] = -sum(q[i][j] for j in range(4) if j != i)
    return q

def artifacts():
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(("beta", "origin", "destination", "rate"))
    worlds = []
    for beta_text in BETAS:
        q = matrix(beta_text)
        for i, origin in enumerate(STATES):
            for j, destination in enumerate(STATES):
                writer.writerow((beta_text, origin, destination, str(q[i][j])))
        beta = Fraction(beta_text)
        worlds.append({
            "beta": beta_text,
            "matrix": [[str(v) for v in row] for row in q],
            "first_event_infection": str(beta / (1 + beta)),
            "first_event_recovery": str(Fraction(1) / (1 + beta)),
        })
    results = {
        "schema": "R340_frozen_two_node_sis_generator_v1",
        "worlds": worlds,
        "checks": {
            "worlds": 3,
            "source_rows": 48,
            "absorbing_worlds": 3,
            "zero_sum_rows": 12,
            "nonnegative_offdiagonal_entries": 36,
            "correct_01_10_transitions": 6,
            "correct_11_recoveries": 3,
        },
    }
    return output.getvalue().encode("utf-8"), (json.dumps(results, indent=2, ensure_ascii=True) + "\n").encode("utf-8")

def audit():
    expected_csv, expected_json = artifacts()
    assert CSV_PATH.read_bytes() == expected_csv, "CSV byte mismatch"
    assert JSON_PATH.read_bytes() == expected_json, "JSON byte mismatch"
    return True

class FrozenTests(unittest.TestCase):
    def test_exact_universe(self):
        self.assertEqual(len(BETAS), 3)
        self.assertEqual(len(STATES), 4)
        self.assertEqual(len(artifacts()[0].decode().splitlines()), 49)

    def test_absorbing(self):
        for beta in BETAS:
            self.assertEqual(matrix(beta)[0], [Fraction(0)] * 4)

    def test_row_sums(self):
        for beta in BETAS:
            for row in matrix(beta):
                self.assertEqual(sum(row), 0)

    def test_nonnegative_offdiagonal(self):
        for beta in BETAS:
            q = matrix(beta)
            self.assertTrue(all(q[i][j] >= 0 for i in range(4) for j in range(4) if i != j))

    def test_transitions(self):
        for beta in BETAS:
            q = matrix(beta)
            b = Fraction(beta)
            for i in (1, 2):
                self.assertEqual(q[i][0], 1)
                self.assertEqual(q[i][3], b)
                self.assertEqual(q[i][i], -(1+b))
            self.assertEqual(q[3], [Fraction(0), Fraction(1), Fraction(1), Fraction(-2)])

    def test_first_event(self):
        expected = (Fraction(1,3), Fraction(1,2), Fraction(2,3))
        for beta, p in zip(BETAS, expected):
            self.assertEqual(Fraction(beta)/(1+Fraction(beta)), p)

    def test_byte_replay(self):
        self.assertTrue(audit())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()
    if args.write:
        csv_bytes, json_bytes = artifacts()
        CSV_PATH.write_bytes(csv_bytes)
        JSON_PATH.write_bytes(json_bytes)
    if args.audit:
        audit()
        print("R340_PRODUCTION_BYTE_REPLAY=PASS")
    if args.test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(FrozenTests)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        if not result.wasSuccessful():
            raise SystemExit(1)
    if not (args.write or args.audit or args.test):
        parser.print_help()

if __name__ == "__main__":
    main()
