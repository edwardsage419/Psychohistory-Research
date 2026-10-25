"""B independent R163 finite-choice oracle using original six artificial profiles.
Python Fraction binomial enumeration; no R163 source or R main solver imports.
"""
from fractions import Fraction as F
from math import comb
import json

PROFILES = (
    ("A_outlier", (1, 1, 0), (12, 0, 8)),
    ("B_outlier", (1, 0, 0), (8, 12, 0)),
    ("A_agreement", (1, 1, 0), (10, 9, 2)),
    ("B_agreement", (1, 0, 0), (2, 10, 9)),
    ("best_tie", (1, 0, 0), (8, 8, 2)),
    ("mean_tie", (1, 1, 0), (8, 0, 4)),
)

def best(actions, scores):
    maximum = max(scores)
    winners = [actions[i] for i in range(3) if scores[i] == maximum]
    return F(sum(winners), len(winners))

def means(actions, scores):
    n1 = sum(actions)
    m1 = F(sum(scores[i] for i in range(3) if actions[i]), n1)
    m0 = F(sum(scores[i] for i in range(3) if not actions[i]), 3-n1)
    return F(1) if m1 > m0 else F(0) if m1 < m0 else F(1, 2)

def error(p, q, n):
    return sum((min(F(comb(n, k)) * p**k * (1-p)**(n-k),
                    F(comb(n, k)) * q**k * (1-q)**(n-k))
                for k in range(n+1)), F(0)) / 2

def run():
    rows = []
    for name, actions, scores in PROFILES:
        for transform in ("raw", "reverse", "flat"):
            values = (scores if transform == "raw" else
                      tuple(12-x for x in scores) if transform == "reverse"
                      else (6, 6, 6))
            p, q = best(actions, values), means(actions, values)
            errs = [error(p, q, n) for n in (1, 2, 4, 8)]
            assert all(F(0) <= e <= F(1, 2) for e in errs)
            assert all(errs[i+1] <= errs[i] for i in range(3))
            rows.append((name, transform, p, q, errs))
    assert len(rows) == 18
    assert sum(p == q for _, _, p, q, _ in rows) == 7
    assert sum(p != q for _, _, p, q, _ in rows) == 11
    assert sum(errs[0] == 0 for *_, errs in rows) == 2
    assert sum(errs[3] == 0 for *_, errs in rows) == 2
    assert next(errs[3] for name, transform, p, q, errs in rows
                if name == "A_outlier" and transform == "flat") == F(1044605,3359232)
    return {"audit":"B_R163_INTERNAL_PYTHON_BINOMIAL_ORACLE",
            "contexts":18,"identical":7,"distinguishable":11,
            "zero_error_at_n1":2,"zero_error_at_n8":2,
            "flat_A_outlier_n8":"1044605/3359232",
            "evidence":"E1_SYNTHETIC_ONLY","external_reproduction":0}

if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
