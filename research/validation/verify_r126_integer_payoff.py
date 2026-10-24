#!/usr/bin/env python3
"""R126 third-method exact integer-payoff E1 audit of frozen 5000 toy worlds."""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import itertools
import json
import sys
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "research/R126/r126_fehr_gachter_2000_pgg_payoffs_punishment_table3_exact.py"
TEST = ROOT / "research/R126/test_r126_fehr_gachter_2000_pgg_payoffs_punishment_table3_exact.py"
REPORT = ROOT / "research/R126/R126_FEHR_GAECHTER_2000_ORIGINAL_PGG_COSTLY_PUNISHMENT_TABLE3_SCIENTIFIC_REPORT_2026-10-20.md"
PINNED = {
    SOURCE: "dc5cc7da900c8175dd14f4751f00e610e52250c7",
    TEST: "c65b29445e8976b9be521996db8ecfc6e633ff05",
    REPORT: "4ef8f1b48dc7191e2e66009d479af0ed5b136827",
}
COST = (0, 1, 2, 4, 6, 9, 12, 16, 20, 25, 30)
HEADER = ("contributions", "punishment_pattern", "payoff0_numerator_50",
          "payoff1_numerator_50", "payoff2_numerator_50",
          "payoff3_numerator_50", "group_numerator_50", "original_matches")

def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()

def verify_pins(pins=PINNED):
    for path, sha in pins.items():
        if blob_sha(path.read_bytes()) != sha:
            raise AssertionError("R126_PINNED_ORIGINAL_SOURCE_MISMATCH " + path.name)

def punishment_patterns():
    p = []
    for index in range(8):
        matrix = [[0] * 4 for _ in range(4)]
        if index == 1:
            matrix[0][3] = 1
        elif index == 2:
            matrix[1][3] = 2
        elif index == 3:
            matrix[0][3], matrix[1][3], matrix[2][3] = 6, 7, 10
        elif index == 4:
            matrix[0][1], matrix[1][0] = 3, 4
        elif index == 5:
            for i in range(4):
                matrix[i][(i + 1) % 4] = 1
        elif index == 6:
            for i in (1, 2, 3):
                matrix[i][0] = 10
        elif index == 7:
            matrix[1][0], matrix[2][1], matrix[3][2] = 5, 3, 2
        p.append(tuple(tuple(row) for row in matrix))
    return tuple(p)

def third_method_numerators(g, matrix):
    """Integer arithmetic only; never call R126 original payoff helpers."""
    total_g = sum(g)
    result = []
    for i in range(4):
        received = min(10, sum(matrix[sender][i] for sender in range(4) if sender != i))
        cost = sum(COST[matrix[i][target]] for target in range(4) if target != i)
        numerator = (100 - 5 * g[i] + 2 * total_g) * (10 - received) - 50 * cost
        result.append(numerator)
    return tuple(result)

def load_original():
    sys.path.insert(0, str(SOURCE.parent))
    import r126_fehr_gachter_2000_pgg_payoffs_punishment_table3_exact as original
    return original

def frozen_controls():
    patterns = punishment_patterns()
    assert third_method_numerators((0, 0, 0, 0), patterns[0]) == (1000,) * 4
    assert third_method_numerators((20, 20, 20, 20), patterns[0]) == (1600,) * 4
    mixed = [[0] * 4 for _ in range(4)]
    mixed[0][3], mixed[1][3] = 1, 2
    nums = third_method_numerators((20, 20, 20, 0), mixed)
    assert tuple(Fraction(n, 50) for n in nums) == (
        Fraction(23), Fraction(22), Fraction(24), Fraction(154, 5))
    assert sum(nums) == 4990
    saturated = third_method_numerators((20, 20, 20, 0), patterns[3])
    assert saturated[3] == 0 and sum(saturated) == 700
    assert saturated[2] < 0
    return 4

def generate(original):
    rows = []
    for g in itertools.product((0, 5, 10, 15, 20), repeat=4):
        for index, matrix in enumerate(punishment_patterns()):
            numerators = third_method_numerators(g, matrix)
            actual = original.punishment_payoff(g, matrix)
            assert tuple(Fraction(v, 50) for v in numerators) == actual, (g, index)
            assert Fraction(sum(numerators), 50) == original.independent_punishment_group_surplus(g, matrix)
            rows.append(("|".join(map(str, g)), index, *numerators, sum(numerators), 1))
    assert len(rows) == 5000
    return rows

def serialize(rows):
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify_pins()
    original = load_original()
    frozen_controls()
    rows = generate(original)
    raw = serialize(rows)
    assert original.TABLE3_PRINTED_MEAN[3] == Fraction(123, 10)
    assert sum((original.TABLE3_PRINTED_SESSIONS[i][3] for i in (1, 2, 3)), Fraction(0)) / 3 == Fraction(124, 10)
    if args.verify:
        assert args.output.read_bytes() == raw, "R126_RAW_CSV_MISMATCH"
        changed = bytearray(raw)
        changed[-2] = 48 if changed[-2] != 48 else 49
        assert bytes(changed) != args.output.read_bytes(), "R126_TAMPER_NEGATIVE_CONTROL_FAILED"
        try:
            verify_pins({SOURCE: "0" * 40})
        except AssertionError:
            pass
        else:
            raise AssertionError("R126_WRONG_SOURCE_SHA_ACCEPTED")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(raw)
    print(json.dumps({
        "constructed_profiles": 625, "punishment_patterns": 8,
        "constructed_worlds": 5000, "exact_person_payoff_comparisons": 20000,
        "raw_csv_sha256": hashlib.sha256(raw).hexdigest(),
        "original_source_blobs": {p.name: h for p, h in PINNED.items()},
        "frozen_controls": 4, "printed_table3_12_4_vs_12_3_unresolved": True,
        "E1": "BOUNDED_INTERNAL_INTEGER_PAYOFF_ONLY", "new_E2": 0, "new_E3": 0
    }, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
