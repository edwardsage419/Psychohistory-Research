#!/usr/bin/env python3
"""MKT125: exact synthetic delayed-label calibration and identification bounds.

Python standard library only. All cases are artificial. No external data.
"""
from fractions import Fraction as F
import json

PRED = {"high": F(4, 5), "low": F(1, 5)}
OBS = {"high": {1: 15, 0: 30}, "low": {1: 30, 0: 15}}
MISSING_A = {"high": {1: 45, 0: 10}, "low": {1: 10, 0: 45}}
MISSING_B = {"high": {1: 0, 0: 55}, "low": {1: 55, 0: 0}}


def loss(p, y):
    assert isinstance(p, F) and y in (0, 1)
    return (p - y) ** 2


def totals(missing):
    return {g: {y: OBS[g][y] + missing[g][y] for y in (0, 1)} for g in PRED}


def risk(counts):
    n = sum(counts[g][y] for g in PRED for y in (0, 1))
    assert n > 0
    return sum((loss(PRED[g], y) * counts[g][y] for g in PRED for y in (0, 1)), F(0)) / n


def empirical_rate(counts, group):
    return F(counts[group][1], sum(counts[group].values()))


def propensities(full):
    result = {}
    for g in PRED:
        result[g] = {}
        for y in (0, 1):
            denom = full[g][y]
            result[g][y] = F(OBS[g][y], denom) if denom else None
    return result


def oracle_ipw(full):
    """Only valid with known, positive, correct outcome-specific propensities."""
    pi = propensities(full)
    assert all(pi[g][y] is not None and pi[g][y] > 0 for g in PRED for y in (0, 1))
    num = sum((F(OBS[g][y]) / pi[g][y] * loss(PRED[g], y) for g in PRED for y in (0, 1)), F(0))
    den = sum((F(OBS[g][y]) / pi[g][y] for g in PRED for y in (0, 1)), F(0))
    return num / den


def fmt(x):
    return str(x)


def main():
    a, b = totals(MISSING_A), totals(MISSING_B)
    assert all(sum(OBS[g].values()) == 45 for g in PRED)
    assert all(sum(a[g].values()) == sum(b[g].values()) == 100 for g in PRED)
    assert sum(sum(OBS[g].values()) for g in PRED) == 90
    assert sum(sum(MISSING_A[g].values()) for g in PRED) == 110
    assert sum(sum(MISSING_B[g].values()) for g in PRED) == 110
    assert risk(OBS) == F(11, 25)  # 0.44
    assert risk(a) == F(7, 25)  # 0.28
    assert risk(b) == F(11, 20)  # 0.55
    assert oracle_ipw(a) == risk(a)
    assert oracle_ipw(b) == risk(b)
    assert empirical_rate(OBS, "high") == F(1, 3)
    assert empirical_rate(OBS, "low") == F(2, 3)
    assert empirical_rate(a, "high") == F(3, 5)
    assert empirical_rate(a, "low") == F(2, 5)
    assert empirical_rate(b, "high") == F(3, 20)
    assert empirical_rate(b, "low") == F(17, 20)
    # For each missing record, Brier is between 1/25 and 16/25.
    observed_loss = risk(OBS) * 90
    lower = (observed_loss + 110 * F(1, 25)) / 200
    upper = (observed_loss + 110 * F(16, 25)) / 200
    assert lower == F(11, 50)  # 0.22
    assert upper == F(11, 20)  # 0.55
    assert lower <= risk(a) <= upper and lower <= risk(b) <= upper
    # Incorrect MAR assumption: one common observation propensity 90/200.
    naive_ipw = risk(OBS)
    assert naive_ipw != risk(a) and naive_ipw != risk(b)
    # The two worlds have the same visible observations and predictions.
    assert OBS == {g: dict(OBS[g]) for g in PRED}
    result = {
        "synthetic_only": True,
        "observed_records": 90,
        "unobserved_records": 110,
        "full_records": 200,
        "observed_brier": fmt(risk(OBS)),
        "world_A_full_brier": fmt(risk(a)),
        "world_B_full_brier": fmt(risk(b)),
        "oracle_ipw_A": fmt(oracle_ipw(a)),
        "oracle_ipw_B": fmt(oracle_ipw(b)),
        "naive_constant_propensity_ipw": fmt(naive_ipw),
        "population_brier_identification_interval": [fmt(lower), fmt(upper)],
        "observed_high_positive_rate": fmt(empirical_rate(OBS, "high")),
        "observed_low_positive_rate": fmt(empirical_rate(OBS, "low")),
        "A_full_high_positive_rate": fmt(empirical_rate(a, "high")),
        "A_full_low_positive_rate": fmt(empirical_rate(a, "low")),
        "B_full_high_positive_rate": fmt(empirical_rate(b, "high")),
        "B_full_low_positive_rate": fmt(empirical_rate(b, "low")),
        "A_propensity": {g: {str(y): fmt(propensities(a)[g][y]) for y in (0, 1)} for g in PRED},
        "B_propensity": {g: {str(y): fmt(propensities(b)[g][y]) for y in (0, 1)} for g in PRED},
        "tests": "all explicit assertions and two oracle IPW calculations passed",
    }
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
