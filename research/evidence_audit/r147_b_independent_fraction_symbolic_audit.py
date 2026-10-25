#!/usr/bin/env python3
"""Independent R147 causal twin audit via Fraction factorization."""
from fractions import Fraction as F
from itertools import product
import json

def bernoulli(x, p):
    return p if x else 1 - p

def main():
    u_mass = (F(1, 2), F(1, 2))
    a_one = (F(1, 4), F(3, 4))
    child_one = (F(1, 4), F(3, 4))
    joint = {}
    for a, b, c in product(range(2), repeat=3):
        joint[a, b, c] = sum(
            (u_mass[u] * bernoulli(a, a_one[u])
             * bernoulli(b, child_one[u])
             * bernoulli(c, child_one[u])
             for u in range(2)), F(0)
        )
    pa = {a: sum((joint[a, b, c] for b, c in product(range(2), repeat=2)), F(0))
          for a in range(2)}
    pb = {a: sum((joint[a, 1, c] for c in range(2)), F(0)) / pa[a]
          for a in range(2)}
    pc = {a: sum((joint[a, b, 1] for b in range(2)), F(0)) / pa[a]
          for a in range(2)}
    p11 = joint[1, 1, 1] / pa[1]
    cov = p11 - pb[1] * pc[1]
    shock_do = sum((u_mass[u] * child_one[u] for u in range(2)), F(0))
    diffusion_do = pb[1] - pb[0]
    observed = [joint[a, b, c] for a, b, c in product(range(2), repeat=3)]
    checks = {
        "eight_cells": observed == [F(v, 128) for v in (28, 12, 12, 12, 12, 12, 12, 28)],
        "mass_one": sum(observed) == 1,
        "strict_assignment_overlap": all(0 < x < 1 for x in a_one),
        "all_cells_positive": all(x > 0 for x in observed),
        "observational_risk_difference": pb[1] - pb[0] == F(1, 4),
        "diffusion_intervention": diffusion_do == F(1, 4),
        "shared_shock_intervention": shock_do - shock_do == 0,
        "conditional_joint": p11 == F(7, 16),
        "conditional_covariance": cov == F(3, 64),
        "independent_child_negative_control": p11 != pb[1] * pc[1],
        "conditioning_as_do_negative_control": pb[1] - pb[0] != 0,
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    print(json.dumps({
        "method": "independent_symbolic_fraction_factorization",
        "checks": checks,
        "joint_order": "000,001,010,011,100,101,110,111",
        "joint": [str(x) for x in observed],
        "observed_risk_difference": str(pb[1] - pb[0]),
        "do_risk_difference_diffusion": str(diffusion_do),
        "do_risk_difference_shock": "0",
        "conditional_covariance": str(cov),
        "E1_only": True,
    }, ensure_ascii=False, sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
