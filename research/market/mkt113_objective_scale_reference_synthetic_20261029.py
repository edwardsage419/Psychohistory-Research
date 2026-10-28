#!/usr/bin/env python3
"""MKT113: deterministic synthetic multi-objective scale and reference-set audit.
No personal data, external APIs, packages, or network access required.
"""
from fractions import Fraction as F
import json

OPTIONS = {
    "A": (F(0), F(8)),
    "B": (F(40), F(4)),
    "C": (F(100), F(0)),
    "D": (F(1000), F(0)),  # dominated reference outlier
}
checks = 0

def verify(condition, message):
    global checks
    checks += 1
    if not condition:
        raise AssertionError(message)

def dominates(left, right):
    return all(a <= b for a, b in zip(left, right)) and any(
        a < b for a, b in zip(left, right)
    )

def frontier(keys):
    return sorted(k for k in keys if not any(
        dominates(OPTIONS[other], OPTIONS[k]) for other in keys if other != k
    ))

def score(key, reference, scale_cash=F(1)):
    cash, days = OPTIONS[key]
    vals = [(OPTIONS[k][0] * scale_cash, OPTIONS[k][1]) for k in reference]
    lower = [min(p[i] for p in vals) for i in (0, 1)]
    upper = [max(p[i] for p in vals) for i in (0, 1)]
    point = (cash * scale_cash, days)
    verify(all(upper[i] > lower[i] for i in (0, 1)), "degenerate normalization range")
    return sum((point[i] - lower[i]) / (upper[i] - lower[i]) for i in (0, 1))

def best(keys, score_fn):
    values = {k: score_fn(k) for k in keys}
    return min(values, key=lambda k: (values[k], k)), values

verify(frontier("ABC") == ["A", "B", "C"], "three nondominated choices")
verify(frontier("ABCD") == ["A", "B", "C"], "dominated outlier must not change frontier")
verify(dominates(OPTIONS["C"], OPTIONS["D"]), "C dominates D")
for k in "ABC":
    verify(not any(dominates(OPTIONS[j], OPTIONS[k]) for j in "ABC" if j != k), "nondominance")

raw_dollars, raw_dollars_scores = best("ABC", lambda k: OPTIONS[k][0] + OPTIONS[k][1])
raw_thousands, raw_thousands_scores = best("ABC", lambda k: OPTIONS[k][0] / 1000 + OPTIONS[k][1])
verify(raw_dollars == "A", "raw dollar sum")
verify(raw_thousands == "C", "raw thousand-dollar sum")

base_best, base_scores = best("ABC", lambda k: score(k, "ABC"))
outlier_best, outlier_scores = best("ABC", lambda k: score(k, "ABCD"))
verify(base_best == "B", "normalized three-choice winner")
verify(outlier_best == "C", "dominated reference outlier flips winner")
verify(base_scores == {"A": F(1), "B": F(9, 10), "C": F(1)}, "base normalized scores")
verify(outlier_scores == {"A": F(1), "B": F(27, 50), "C": F(1, 10)}, "outlier normalized scores")
for k in "ABC":
    verify(score(k, "ABC", F(100)) == base_scores[k], "scale-invariant normalization")

def epsilon_choice(max_days):
    eligible = [k for k in "ABC" if OPTIONS[k][1] <= max_days]
    return min(eligible, key=lambda k: (OPTIONS[k][0], k)) if eligible else None
verify(epsilon_choice(8) == "A", "8-day cap")
verify(epsilon_choice(4) == "B", "4-day cap")
verify(epsilon_choice(0) == "C", "0-day cap")
verify(epsilon_choice(-1) is None, "infeasible cap")
authorization = False
verify(authorization is False, "no user preference authorization")

print(json.dumps({
    "study": "MKT113", "source": "SYNTHETIC_ONLY", "checks": checks,
    "failures": 0, "pareto_ABC": frontier("ABC"),
    "pareto_with_dominated_outlier": frontier("ABCD"),
    "raw_dollars_winner": raw_dollars, "raw_thousands_winner": raw_thousands,
    "normalized_ABC_winner": base_best,
    "normalized_with_outlier_winner": outlier_best,
    "normalized_ABC": {k: str(v) for k, v in base_scores.items()},
    "normalized_with_outlier": {k: str(v) for k, v in outlier_scores.items()},
    "epsilon_choices": {str(d): epsilon_choice(d) for d in (8, 4, 0, -1)},
    "user_authorization": authorization,
}, ensure_ascii=False, sort_keys=True))
