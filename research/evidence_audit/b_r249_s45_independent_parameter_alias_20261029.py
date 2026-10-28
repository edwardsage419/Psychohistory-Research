#!/usr/bin/env python3
"""Independent exact Fraction audit of R249 S45 parameter interpolation aliases.

No imports from R-track JavaScript or original R249 scripts.
Run: python b_r249_s45_independent_parameter_alias_20261029.py
"""
import json
from fractions import Fraction as F
from math import prod

L = tuple(map(F, ("1/2", "1", "2", "3", "4")))
H = tuple(map(F, ("-1/4", "0", "1/4", "1")))


def product_at(x, nodes):
    return prod((x - a for a in nodes), start=F(1))


def product_derivative_at_node(x, nodes):
    assert x in nodes and nodes.count(x) == 1
    return prod((x - a for a in nodes if a != x), start=F(1))


def logistic_alias(r, coefficient=F(16, 15)):
    return r + coefficient * product_at(r, L)


def fold_alias(mu, coefficient=F(-192, 7)):
    return mu + coefficient * product_at(mu, H)


def audit():
    checks = 0
    for r in L:
        assert product_at(r, L) == 0
        assert logistic_alias(r) == r
        checks += 2
    for mu in H:
        assert product_at(mu, H) == 0
        assert fold_alias(mu) == mu
        checks += 2

    r = F(3, 2)
    mu = F(1, 8)
    assert product_at(r, L) == F(-15, 16)
    assert logistic_alias(r) == F(1, 2)
    assert abs(r) > 1 and abs(logistic_alias(r)) < 1
    checks += 3
    assert product_at(mu, H) == F(21, 4096)
    assert fold_alias(mu) == F(-1, 64)
    assert mu > 0 > fold_alias(mu)
    assert fold_alias(F(1, 4)) == F(1, 4) > 0
    checks += 4

    # Parameter derivatives differ at observed nodes. The 405 source rows
    # record initial-state sensitivities, not derivatives w.r.t. parameters.
    dl = 1 + F(16, 15) * product_derivative_at_node(F(1), L)
    dh = 1 - F(192, 7) * product_derivative_at_node(F(0), H)
    assert dl == F(-11, 5) and dh == F(-5, 7)
    checks += 2

    rejected = 0
    for family in ("logistic", "fold"):
        mismatch = (logistic_alias(r, F(17, 15)) != F(1, 2)) if family == "logistic" else (
            fold_alias(mu, F(-191, 7)) != F(-1, 64))
        assert mismatch
        rejected += 1

    return {
        "study": "B_R249_S45", "evidence": "E1_INTERNAL_INDEPENDENT_METHOD",
        "grid_node_zero_checks": 9, "deterministic_assertions": checks,
        "off_grid_logistic": {"parameter": str(r), "base_multiplier": str(r),
                              "alias_multiplier": str(logistic_alias(r))},
        "off_grid_fold": {"parameter": str(mu), "base_fixed_points": 2,
                          "alias_fixed_points": 0,
                          "additional_zero_exists_in": "(1/8,1/4) by IVT"},
        "parameter_derivative_at_logistic_r1": str(dl),
        "parameter_derivative_at_fold_mu0": str(dh),
        "negative_controls_rejected": rejected,
        "external_independent_replication": False,
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
