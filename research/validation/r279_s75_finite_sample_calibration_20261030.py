#!/usr/bin/env python3
"""R279 S75: exact finite-sample empirical versus population Murphy decomposition.
Usage: python r279_s75_finite_sample_calibration_20261030.py --emit /tmp/r279_s75
       python r279_s75_finite_sample_calibration_20261030.py --selftest
Python standard library only; artificial E1, internal nonblind.
"""
import argparse
import csv
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F
from math import comb
from pathlib import Path

REGIMES = {
    "CALIBRATED_RATE": (F(1, 4), F(3, 4)),
    "DETERMINISTIC_GROUP": (F(0), F(1)),
    "INVERTED_RATE": (F(3, 4), F(1, 4)),
}
POLICIES = {
    "ORIGINAL_BUCKETS": (F(1, 4), F(3, 4)),
    "FLAT_HALF": (F(1, 2), F(1, 2)),
    "REVERSED_BUCKETS": (F(3, 4), F(1, 4)),
}
FIELDS = ("regime", "policy", "bits", "source_mass", "empirical_REL",
          "empirical_RES", "empirical_UNC", "sample_Brier")
ZERO = F(0)
ONE = F(1)


def population(theta, q):
    base = sum(theta) / 2
    buckets = defaultdict(list)
    for t, forecast in zip(theta, q):
        buckets[forecast].append(t)
    rel = sum((F(len(values), 2) *
               (forecast - sum(values) / len(values)) ** 2
               for forecast, values in buckets.items()), ZERO)
    res = sum((F(len(values), 2) *
               (sum(values) / len(values) - base) ** 2
               for values in buckets.values()), ZERO)
    unc = base * (1 - base)
    return (rel, res, unc, rel - res + unc)


def empirical(bits, q):
    buckets = defaultdict(list)
    for index, bit in enumerate(bits):
        buckets[q[index // 2]].append(int(bit))
    base = F(sum(map(int, bits)), 4)
    rel = sum((F(len(values), 4) *
               (forecast - F(sum(values), len(values))) ** 2
               for forecast, values in buckets.items()), ZERO)
    res = sum((F(len(values), 4) *
               (F(sum(values), len(values)) - base) ** 2
               for values in buckets.values()), ZERO)
    unc = base * (1 - base)
    brier = sum(((F(int(bit)) - q[i // 2]) ** 2
                 for i, bit in enumerate(bits)), ZERO) / 4
    if brier != rel - res + unc:
        raise AssertionError("empirical Murphy identity failed")
    return (rel, res, unc, brier)


def source_mass(bits, theta):
    k_l = bits[:2].count("1")
    k_h = bits[2:].count("1")
    return (theta[0] ** k_l * (1 - theta[0]) ** (2 - k_l) *
            theta[1] ** k_h * (1 - theta[1]) ** (2 - k_h))


def independent_count_route(theta, q):
    """Independent count oracle, no ordered four-bit enumeration."""
    sums = [ZERO] * 4
    prob_zero = prob_le = mass_total = ZERO
    pop_rel = population(theta, q)[0]
    for k_l in range(3):
        for k_h in range(3):
            mass = (comb(2, k_l) * theta[0] ** k_l *
                    (1 - theta[0]) ** (2 - k_l) *
                    comb(2, k_h) * theta[1] ** k_h *
                    (1 - theta[1]) ** (2 - k_h))
            mass_total += mass
            total = k_l + k_h
            overall = F(total, 4)
            if q[0] == q[1]:
                rel = (q[0] - overall) ** 2
                res = ZERO
            else:
                rate_l = F(k_l, 2)
                rate_h = F(k_h, 2)
                rel = ((q[0] - rate_l) ** 2 +
                       (q[1] - rate_h) ** 2) / 2
                res = ((rate_l - overall) ** 2 +
                       (rate_h - overall) ** 2) / 2
            unc = overall * (1 - overall)
            brier = rel - res + unc
            for j, value in enumerate((rel, res, unc, brier)):
                sums[j] += mass * value
            if rel == ZERO:
                prob_zero += mass
            if rel <= pop_rel:
                prob_le += mass
    assert mass_total == ONE
    return tuple(sums), prob_zero, prob_le


def run():
    source_rows = []
    results = []
    for regime, theta in REGIMES.items():
        for policy, q in POLICIES.items():
            pop = population(theta, q)
            sums = [ZERO] * 4
            p_zero = p_le = mass_total = ZERO
            positive = 0
            for bit_tuple in itertools.product("01", repeat=4):
                bits = "".join(bit_tuple)
                mass = source_mass(bits, theta)
                stats = empirical(bits, q)
                source_rows.append((regime, policy, bits, mass, *stats))
                mass_total += mass
                positive += (mass > 0)
                for i, value in enumerate(stats):
                    sums[i] += mass * value
                if stats[0] == ZERO:
                    p_zero += mass
                if stats[0] <= pop[0]:
                    p_le += mass
            assert mass_total == ONE
            assert positive == (1 if regime == "DETERMINISTIC_GROUP" else 16)
            count_sums, count_zero, count_le = independent_count_route(theta, q)
            assert tuple(sums) == count_sums
            assert (p_zero, p_le) == (count_zero, count_le)
            assert sums[3] == pop[3]
            v_sum = sum((t * (1 - t) for t in theta), ZERO)
            if policy == "FLAT_HALF":
                expected_bias = (v_sum / 8, ZERO, -v_sum / 8, ZERO)
            else:
                expected_bias = (v_sum / 4, v_sum / 8, -v_sum / 8, ZERO)
            observed_bias = tuple(sums[i] - pop[i] for i in range(4))
            assert observed_bias == expected_bias, (regime, policy, observed_bias)
            results.append({
                "regime": regime,
                "policy": policy,
                "source_atoms": 16,
                "positive_source_atoms": positive,
                "population": dict(zip(("REL", "RES", "UNC", "Brier"), map(str, pop))),
                "expected_empirical": dict(zip(("REL", "RES", "UNC", "Brier"), map(str, sums))),
                "empirical_minus_population": dict(zip(("REL", "RES", "UNC", "Brier"), map(str, observed_bias))),
                "P_empirical_REL_equals_zero": str(p_zero),
                "P_empirical_REL_at_most_population_REL": str(p_le),
                "count_oracle_equal": True,
                "variance_formula_equal": True,
            })
    assert len(source_rows) == 144
    assert sum(row[3] > 0 for row in source_rows) == 99
    assert len(results) == 9
    return source_rows, {
        "research": "R279_S75",
        "evidence": "ARTIFICIAL_E1_INTERNAL_NONBLIND_EXPLORATORY",
        "protocol_path": "research/validation/R279_S75_FINITE_SAMPLE_CALIBRATION_BIAS_FREEZE_2026-10-30.md",
        "source_atoms": 144,
        "positive_source_atoms": 99,
        "original_R279_unchanged": True,
        "R073": "FROZEN",
        "PESEN_v0_1": "FROZEN",
        "E2": 0,
        "E3": 0,
        "results": results,
    }


def emit(directory):
    rows, report = run()
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / "R279_S75_ALL_144_EMPIRICAL_SOURCE_ATOMS.csv").open(
            "w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(FIELDS)
        for row in rows:
            writer.writerow([str(v) for v in row])
    (directory / "R279_S75_EXACT_RESULTS.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit", type=Path)
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if bool(args.emit) == bool(args.selftest):
        parser.error("select exactly one of --emit or --selftest")
    if args.selftest:
        rows, result = run()
        print("PASS: 144 sources, 9 worlds, independent count route and exact variance identities")
        for entry in result["results"]:
            print(entry["regime"], entry["policy"],
                  "RELbias=" + entry["empirical_minus_population"]["REL"],
                  "Pzero=" + entry["P_empirical_REL_equals_zero"])
    else:
        emit(args.emit)
        print("PASS: persisted exact CSV and JSON")
