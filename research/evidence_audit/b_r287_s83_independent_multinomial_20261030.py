#!/usr/bin/env python3
"""Independent exact multinomial oracle for R287 S83 artificial finite preference signs.

Usage:
  python b_r287_s83_independent_multinomial_20261030.py
  python b_r287_s83_independent_multinomial_20261030.py --compare R287_S83_EXACT_RESULTS.json

This program does not import the original R287 code or enumerate original eight-bit sources.
"""
from fractions import Fraction as F
from math import factorial
import argparse
import json

UTILITY_DIFFERENCES = {
    "LINEAR": (F(4), F(-5)),
    "SQRT_ON_SQUARES": (F(2), F(-1)),
    "SATURATING": (F(3, 2), F(-1, 2)),
}
COMMON_PROBABILITIES = (F(1, 4), F(1, 2), F(3, 4))


def exact_world(profile, lam):
    positive, negative = UTILITY_DIFFERENCES[profile]
    truth = 1 if positive + negative > 0 else -1
    masses = {"CORRECT": F(0), "WRONG": F(0), "TIE": F(0)}
    count_cells = 0
    for a in range(5):
        for b in range(5 - a):
            c = 4 - a - b
            multiplicity = factorial(4) // (factorial(a) * factorial(b) * factorial(c))
            probability = multiplicity * ((1 - lam) / 2) ** (a + b) * lam ** c
            difference = a * positive + b * negative
            category = "TIE" if difference == 0 else "CORRECT" if difference * truth > 0 else "WRONG"
            masses[category] += probability
            count_cells += 1
    assert count_cells == 15 and sum(masses.values()) == 1
    assert masses["CORRECT"] + masses["WRONG"] > 0
    return {
        "profile": profile, "lambda_common": str(lam), "original_sources": 256,
        "probability_correct": str(masses["CORRECT"]),
        "probability_wrong": str(masses["WRONG"]),
        "probability_tie": str(masses["TIE"]),
        "wrong_given_non_tie": str(masses["WRONG"] / (1 - masses["TIE"])),
        "probability_all_common": str(lam ** 4),
        "affine_3u_plus_7_sign_invariant": True,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare", help="Path to the persisted R result JSON")
    args = parser.parse_args()
    results = [exact_world(p, l) for p in UTILITY_DIFFERENCES for l in COMMON_PROBABILITIES]
    assert len(results) == 9
    if args.compare:
        with open(args.compare, encoding="utf-8") as f:
            persisted = json.load(f)
        if results != persisted["results"]:
            raise SystemExit("FAIL: exact multinomial result mismatch")
        print("PASS: nine exact multinomial worlds equal persisted R result")
    else:
        print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
