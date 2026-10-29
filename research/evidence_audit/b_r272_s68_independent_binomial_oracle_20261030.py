#!/usr/bin/env python3
"""Independent 15-cell binomial oracle for R272 S68, Python standard library."""
import argparse
import csv
import json
from fractions import Fraction as F
from math import comb
from collections import Counter

PS = (F(1, 4), F(1, 2), F(3, 4))
PAIRS = (("TRAIN_MLE", "LAPLACE_BETA11"),
         ("TRAIN_MLE", "CONSTANT_HALF"),
         ("LAPLACE_BETA11", "CONSTANT_HALF"))


def forecast(name, k):
    if name == "TRAIN_MLE":
        return F(k, 4)
    if name == "LAPLACE_BETA11":
        return F(k + 1, 6)
    if name == "CONSTANT_HALF":
        return F(1, 2)
    raise ValueError("unknown model")


def score(q, successes):
    return (successes * (1 - q) ** 2 + (2 - successes) * q ** 2) / 2


def oracle(p, first, second):
    atoms = []
    for k in range(5):
        wk = comb(4, k) * p ** k * (1 - p) ** (4 - k)
        for j in range(3):
            w = wk * comb(2, j) * p ** j * (1 - p) ** (2 - j)
            d = score(forecast(first, k), j) - score(forecast(second, k), j)
            atoms.append((w, d))
    assert len(atoms) == 15 and sum(w for w, _ in atoms) == 1
    mean = sum(w * d for w, d in atoms)
    second_moment = sum(w * d * d for w, d in atoms)
    variance = second_moment - mean * mean
    less = sum(w for w, d in atoms if d < 0)
    tie = sum(w for w, d in atoms if d == 0)
    more = sum(w for w, d in atoms if d > 0)
    wrong = sum(w for w, d in atoms if d * mean < 0)
    assert less + tie + more == 1 and variance >= 0
    return {
        "true_p": str(p), "first": first, "second": second,
        "primitive_source_types": 64,
        "mean_difference": str(mean), "second_moment": str(second_moment),
        "variance": str(variance), "prob_first_better": str(less),
        "prob_tie": str(tie), "prob_first_worse": str(more),
        "prob_strict_wrong_population_ranking": str(wrong),
        "independent_binomial_route_agrees": True,
    }


def verify_receipt(path):
    with open(path, encoding="utf-8") as stream:
        document = json.load(stream)
    expected = [oracle(p, a, b) for p in PS for a, b in PAIRS]
    assert isinstance(document, dict) and document.get("research_id") == "R272_S68"
    rows = document.get("results")
    assert isinstance(rows, list) and len(rows) == 9
    assert rows == expected, "receipt differs from independent 15-cell oracle"
    return len(rows)


def verify_csv(path):
    with open(path, newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 576
    seen = set()
    for row in rows:
        p = F(row["true_p"])
        a, b = row["first"], row["second"]
        bits = row["original_six_bits"]
        assert p in PS and (a, b) in PAIRS
        assert len(bits) == 6 and set(bits) <= {"0", "1"}
        key = (p, a, b, bits)
        assert key not in seen
        seen.add(key)
        k = bits[:4].count("1")
        j = bits[4:].count("1")
        assert int(row["train_successes"]) == k and int(row["test_successes"]) == j
        assert F(row["first_forecast"]) == forecast(a, k)
        assert F(row["second_forecast"]) == forecast(b, k)
        assert F(row["paired_test_brier_difference"]) == score(forecast(a, k), j) - score(forecast(b, k), j)
        assert F(row["exact_source_mass"]) == p ** (k + j) * (1 - p) ** (6 - k - j)
    for p in PS:
        for a, b in PAIRS:
            assert sum((F(r["exact_source_mass"]) for r in rows
                        if r["true_p"] == str(p) and r["first"] == a and r["second"] == b), F(0)) == 1
    return len(rows)


def selftest():
    assert len([oracle(p, a, b) for p in PS for a, b in PAIRS]) == 9
    assert oracle(F(1, 4), "TRAIN_MLE", "LAPLACE_BETA11")["mean_difference"] == "11/576"
    assert oracle(F(1, 2), "TRAIN_MLE", "CONSTANT_HALF")["prob_tie"] == "3/8"
    # A swapped comparison must negate mean and reverse strict win probabilities.
    forward = oracle(F(1, 4), "TRAIN_MLE", "LAPLACE_BETA11")
    reverse = oracle(F(1, 4), "LAPLACE_BETA11", "TRAIN_MLE")
    assert F(forward["mean_difference"]) == -F(reverse["mean_difference"])
    assert forward["prob_first_better"] == reverse["prob_first_worse"]
    # Equal forecasts have no spurious model winner.
    same = oracle(F(1, 2), "TRAIN_MLE", "TRAIN_MLE")
    assert same["prob_tie"] == "1" and same["variance"] == "0"
    return 4


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt")
    parser.add_argument("--csv")
    args = parser.parse_args()
    print(json.dumps({"selftest": selftest(),
                      "receipt_rows": verify_receipt(args.receipt) if args.receipt else "NOT_RUN",
                      "csv_rows": verify_csv(args.csv) if args.csv else "NOT_RUN"}, sort_keys=True))
