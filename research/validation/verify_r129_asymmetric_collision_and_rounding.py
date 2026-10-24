#!/usr/bin/env python3
"""R129 independent finite E1 replay. Does not import original R129 payoff functions."""
import argparse
import csv
import hashlib
import io
import itertools
import pathlib
import subprocess
from fractions import Fraction as F

ROOT = pathlib.Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / "research/R129/r129_chicken_original_table_and_exact_conflict.py"
EXPECTED_ORIGINAL_BLOB = "2e5dd6aa387011b1ddbe39ff09b6ec850e51d027"
OUT_COLLISION = ROOT / "research/validation/R129_ASYMMETRIC_COLLISION_49_CASES_2026-10-24.csv"
OUT_TABLE = ROOT / "research/validation/R129_ROUNDED_TABLE_25_INTERVAL_CHECKS_2026-10-24.csv"
NAMES = ("Mouse", "Hawk", "Bully", "Retaliator", "Prober-Retaliator")
TABLE = (
    ("29.0", "19.5", "19.5", "29.0", "17.2"),
    ("80.0", "-19.5", "74.6", "-18.1", "-18.9"),
    ("80.0", "4.9", "41.5", "11.9", "11.2"),
    ("29.0", "-22.3", "57.1", "29.0", "23.1"),
    ("56.7", "-20.1", "59.4", "26.9", "21.9"),
)
GRID = (F(0), F(1, 4), F(1, 3), F(1, 2), F(2, 3), F(3, 4), F(1))

def csv_bytes(header, rows):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(header)
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")

def build_table():
    a = tuple(tuple(F(x) for x in row) for row in TABLE)
    delta = F(1, 20)
    rows = []
    possible_count = robust_count = 0
    for j, opponent in enumerate(NAMES):
        for i, respondent in enumerate(NAMES):
            x = a[i][j]
            possible = all(i == t or x + delta >= a[t][j] - delta for t in range(5))
            robust = all(i == t or x - delta > a[t][j] + delta for t in range(5))
            possible_count += possible
            robust_count += robust
            rows.append([opponent, respondent, str(x), str(x - delta),
                         str(x + delta), str(bool(possible)).upper(), str(bool(robust)).upper()])
    assert (len(rows), possible_count, robust_count) == (25, 7, 3)
    return csv_bytes(["opponent", "respondent", "printed", "rounding_lower",
                      "rounding_upper", "possible_max", "robust_strict_max"], rows)

def check_count(observed, expected):
    if observed != expected:
        raise AssertionError("altered coupling count rejected")

def build_collision():
    rows = []
    for p, q in itertools.product(GRID, repeat=2):
        a, b = int(12 * p), int(12 * q)
        A = set(range(a))
        B_lower = set(range(12 - b, 12))
        B_upper = set(range(b))
        lower = len(A & B_lower)
        upper = len(A & B_upper)
        check_count(lower, max(0, a + b - 12))
        check_count(upper, min(a, b))
        assert (len(A), len(B_lower), len(B_upper)) == (a, b, b)
        assert F(lower, 12) <= p * q <= F(upper, 12)
        def total_welfare(B):
            return sum(-4 if t in A and t in B else 2 for t in range(12))
        assert total_welfare(B_lower) == 24 - 6 * lower
        assert total_welfare(B_upper) == 24 - 6 * upper
        rows.append([str(p), str(q), str(F(lower, 12)), str(F(upper, 12)),
                     str(p * q), str(F(24 - 6 * upper, 12)),
                     str(F(24 - 6 * lower, 12)), lower, upper, a, b])
    assert len(rows) == 49
    # Two frozen negative controls: corrupted HH count and corrupted marginal.
    try:
        check_count(2, 1)
    except AssertionError:
        pass
    else:
        raise AssertionError("HH tamper accepted")
    try:
        check_count(5, 4)
    except AssertionError:
        pass
    else:
        raise AssertionError("marginal tamper accepted")
    return csv_bytes(["p_H_A", "q_H_B", "lower_HH", "upper_HH", "independent_HH",
                      "lower_welfare", "upper_welfare", "lower_HH_atoms",
                      "upper_HH_atoms", "A_H_atoms", "B_H_atoms"], rows)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-existing", action="store_true")
    args = parser.parse_args()
    blob = subprocess.check_output(["git", "hash-object", str(ORIGINAL)], text=True).strip()
    if blob != EXPECTED_ORIGINAL_BLOB:
        raise AssertionError("original R129 source blob mismatch")
    c = build_collision()
    t = build_table()
    if args.verify_existing:
        if OUT_COLLISION.read_bytes() != c or OUT_TABLE.read_bytes() != t:
            raise AssertionError("archived R129 finite evidence differs")
    print(f"R129 third-method E1 PASS: 49 coupling worlds, 25 source-table cells; "
          f"collision_sha256={hashlib.sha256(c).hexdigest()}, "
          f"table_sha256={hashlib.sha256(t).hexdigest()}")

if __name__ == "__main__":
    main()
