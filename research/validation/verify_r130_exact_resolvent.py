#!/usr/bin/env python3
"""R130 exact finite-state resolvent, independently derived E1. No paid dependencies."""
import argparse
import csv
import hashlib
import importlib.util
import io
import itertools
import pathlib
import subprocess
from fractions import Fraction as F

ROOT = pathlib.Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / "research/R130/r130_axelrod1981_tft_nowak1993_pavlov_repeated_exact.py"
ORIGINAL_BLOB = "acc82d15b23de015ca8e448cf622b077a4e8e6cd"
CSV_PATH = ROOT / "research/validation/R130_EXACT_RESOLVENT_175_CASES_2026-10-25.csv"
EXPECTED_SHA256 = "7f9f44076ef039122e56d08b8c4d5cf5f42041cb90ee9a90b82f6b06d0a01ec3"
STRATEGIES = ("TFT", "ALLD", "ALLC", "ALT_DC", "WSLS")
DISCOUNTS = (F(0), F(1, 4), F(1, 2), F(3, 5), F(2, 3), F(4, 5), F(9, 10))
PAYOFFS = {"CC": (3, 3), "CD": (0, 5), "DC": (5, 0), "DD": (1, 1)}

def choose(strategy, previous, parity, is_row):
    if strategy == "ALLD":
        return "D"
    if strategy == "ALLC":
        return "C"
    if strategy == "ALT_DC":
        return "D" if parity == 0 else "C"
    if previous is None:
        return "C"
    own, other = (previous[0], previous[1]) if is_row else (previous[1], previous[0])
    if strategy == "TFT":
        return other
    if strategy == "WSLS":
        return "C" if own == other else "D"
    raise AssertionError("unknown strategy")

def graph(row, col, reward=3):
    states, payouts, seen = [], [], {}
    state = (None, 0)
    while state not in seen:
        seen[state] = len(states)
        states.append(state)
        prev, parity = state
        action = choose(row, prev, parity, True) + choose(col, prev, parity, False)
        r, c = PAYOFFS[action]
        if action == "CC":
            r = c = reward
        payouts.append((F(r), F(c)))
        state = (action, 1 - parity)
    successors = []
    for prev, parity in states:
        action = choose(row, prev, parity, True) + choose(col, prev, parity, False)
        successors.append(seen[(action, 1 - parity)])
    assert 1 <= len(states) <= 10
    return states, successors, payouts

def solve(matrix, rhs):
    n = len(rhs)
    a = [list(matrix[i]) + [rhs[i]] for i in range(n)]
    for col in range(n):
        pivot = next((i for i in range(col, n) if a[i][col]), None)
        if pivot is None:
            raise AssertionError("singular exact resolvent")
        a[col], a[pivot] = a[pivot], a[col]
        factor = a[col][col]
        a[col] = [v / factor for v in a[col]]
        for i in range(n):
            if i == col:
                continue
            factor = a[i][col]
            if factor:
                a[i] = [a[i][k] - factor * a[col][k] for k in range(n + 1)]
    return [a[i][-1] for i in range(n)]

def exact_value(row, col, w, reward=3):
    states, successors, payouts = graph(row, col, reward)
    n = len(states)
    matrix = [[F(i == j) - (w if successors[i] == j else F(0))
               for j in range(n)] for i in range(n)]
    result = []
    for player in (0, 1):
        rhs = [p[player] for p in payouts]
        values = solve(matrix, rhs)
        assert all(sum(matrix[i][j] * values[j] for j in range(n)) == rhs[i]
                   for i in range(n))
        result.append(values[0])
    return tuple(result), n

def audit(original):
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(["row_strategy", "col_strategy", "discount", "reachable_states",
                     "row_value", "col_value", "exact_original_match"])
    cases = 0
    for row, col in itertools.product(STRATEGIES, repeat=2):
        for w in DISCOUNTS:
            result, count = exact_value(row, col, w)
            expected = original.independent_infinite_state_cycle_value(row, col, w)
            if result != expected:
                raise AssertionError(f"R130 original comparison failed {row} {col} {w}")
            writer.writerow([row, col, str(w), count, str(result[0]), str(result[1]), "PASS"])
            cases += 1
    assert cases == 175
    w = F(3, 5)
    assert exact_value("TFT", "TFT", w)[0][0] == F(15, 2)
    assert exact_value("ALLD", "TFT", w)[0][0] == F(13, 2)
    assert exact_value("ALT_DC", "TFT", w)[0][0] == F(125, 16)
    assert exact_value("TFT", "TFT", F(1, 2))[0][0] == exact_value("ALLD", "TFT", F(1, 2))[0][0]
    assert exact_value("TFT", "TFT", F(2, 3))[0][0] == exact_value("ALT_DC", "TFT", F(2, 3))[0][0]
    negatives = 0
    try:
        assert exact_value("TFT", "TFT", w)[0][0] + 1 == F(15, 2)
    except AssertionError:
        negatives += 1
    try:
        assert exact_value("TFT", "TFT", w, reward=4)[0][0] == F(15, 2)
    except AssertionError:
        negatives += 1
    assert negatives == 2
    data = output.getvalue().encode("utf-8")
    assert hashlib.sha256(data).hexdigest() == EXPECTED_SHA256
    return data

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-existing", action="store_true")
    parser.add_argument("--write-csv", type=pathlib.Path)
    args = parser.parse_args()
    blob = subprocess.check_output(["git", "hash-object", str(ORIGINAL)], text=True).strip()
    assert blob == ORIGINAL_BLOB, "original R130 source identity changed"
    spec = importlib.util.spec_from_file_location("r130_original_source", ORIGINAL)
    original = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(original)
    data = audit(original)
    if args.verify_existing:
        assert CSV_PATH.read_bytes() == data, "archived R130 exact CSV mismatch"
    if args.write_csv:
        args.write_csv.write_bytes(data)
    print(f"R130 exact resolvent PASS 175 cases, 350 scalar payoffs, 2 tamper controls; "
          f"csv_bytes={len(data)}; sha256={hashlib.sha256(data).hexdigest()}")

if __name__ == "__main__":
    main()
