#!/usr/bin/env python3
"""MKT134: exact finite sensitivity counterexamples, standard library only.

All records and outcomes are artificial. No personal data or API calls.
"""
from fractions import Fraction as F
from itertools import product


def selection_masses(prevalence: F, pi_positive: F, pi_negative: F):
    if not F(0) < prevalence < F(1):
        raise ValueError("prevalence must be strictly between 0 and 1")
    if not all(F(0) < p <= F(1) for p in (pi_positive, pi_negative)):
        raise ValueError("selection probabilities must be in (0,1]")
    return prevalence * pi_positive, (1 - prevalence) * pi_negative


def gamma_bounds(selected_positive: F, selected_negative: F, gamma: F):
    if selected_positive <= 0 or selected_negative <= 0:
        raise ValueError("both selected outcome categories must be positive")
    if selected_positive + selected_negative > 1:
        raise ValueError("selected mass cannot exceed one")
    if gamma < 1:
        raise ValueError("gamma must be >= 1")
    q = selected_positive / (selected_positive + selected_negative)
    lo = q / (gamma * (1 - q) + q)
    hi = gamma * q / (1 - q + gamma * q)
    # Physical inclusion constraints: selected-positive <= population-positive,
    # selected-negative <= population-negative.
    lo = max(lo, selected_positive)
    hi = min(hi, 1 - selected_negative)
    if lo > hi:
        raise ValueError("infeasible sensitivity model")
    return lo, hi


def recommendation_interval(lo: F, hi: F, threshold: F):
    if not F(0) < threshold < F(1):
        raise ValueError("threshold must be in (0,1)")
    if lo >= threshold:
        return "POSITIVE_ROBUST"
    if hi < threshold:
        return "NEGATIVE_ROBUST"
    return "ABSTAIN"


def run():
    selected = (F(1, 16), F(3, 16))
    worlds = {
        "equal_inclusion": (F(1, 4), F(1, 4), F(1, 4)),
        "outcome_negative_overselected": (F(1, 2), F(1, 8), F(3, 8)),
        "outcome_positive_overselected": (F(1, 10), F(5, 8), F(5, 24)),
    }
    checks = 0
    for name, (p, pi1, pi0) in worlds.items():
        assert selection_masses(p, pi1, pi0) == selected, name
        checks += 1
    assert len(set(w[0] for w in worlds.values())) == 3
    checks += 1
    assert sum(selected) == F(1, 4)
    checks += 1
    expected = {F(1): (F(1, 4), F(1, 4)),
                F(2): (F(1, 7), F(2, 5)),
                F(3): (F(1, 10), F(1, 2))}
    for gamma, bounds in expected.items():
        assert gamma_bounds(*selected, gamma) == bounds
        checks += 1
    assert gamma_bounds(*selected, F(1000)) == (F(1, 16), F(13, 16))
    checks += 1
    assert recommendation_interval(*expected[F(1)], F(2, 5)) == "NEGATIVE_ROBUST"
    checks += 1
    assert recommendation_interval(*expected[F(2)], F(2, 5)) == "ABSTAIN"
    checks += 1
    assert recommendation_interval(*expected[F(3)], F(2, 5)) == "ABSTAIN"
    checks += 1
    assert recommendation_interval(*expected[F(3)], F(3, 5)) == "NEGATIVE_ROBUST"
    checks += 1
    # Enumerate a coarse grid of feasible prevalences and inclusion rates;
    # every compatible world must lie inside the analytic Gamma=3 bounds.
    feasible = 0
    for numerator in range(1, 16):
        p = F(numerator, 16)
        pi1 = selected[0] / p
        pi0 = selected[1] / (1 - p)
        if pi1 > 1 or pi0 > 1:
            continue
        ratio = pi1 / pi0
        if F(1, 3) <= ratio <= 3:
            assert expected[F(3)][0] <= p <= expected[F(3)][1]
            feasible += 1
    assert feasible >= 5
    checks += 1
    rejected = 0
    bad = [(F(0), F(1, 4), F(1, 4)),
           (F(1, 2), F(0), F(1, 4)),
           (F(1, 2), F(1, 4), F(5, 4))]
    for args in bad:
        try:
            selection_masses(*args)
        except ValueError:
            rejected += 1
    for args in [(F(0), F(1, 4), F(3)),
                 (F(1, 16), F(3, 16), F(1, 2)),
                 (F(1, 2), F(3, 4), F(3))]:
        try:
            gamma_bounds(*args)
        except ValueError:
            rejected += 1
    assert rejected == 6
    checks += 1
    print("MKT134 PASS")
    print("selected joint mass: positive=1/16, negative=3/16, missing=3/4")
    print("three indistinguishable worlds: p=1/10, 1/4, 1/2")
    for gamma, (lo, hi) in expected.items():
        print(f"Gamma={gamma}: population prevalence in [{lo}, {hi}], "
              f"threshold 2/5: {recommendation_interval(lo, hi, F(2, 5))}")
    print(f"checks={checks}; rejected_invalid_inputs={rejected}; grid_worlds={feasible}")


if __name__ == "__main__":
    run()
