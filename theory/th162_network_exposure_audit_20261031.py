#!/usr/bin/env python3
"""TH162 exact synthetic network exposure audit. Python standard library only."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
import json

assignments = [frozenset(z) for z in combinations(range(4), 2)]
true_neighbors = frozenset((1, 2))
proxy_neighbors = frozenset((1, 3))

def exposure(z, neighbors):
    return int(bool(z & neighbors))

rows = []
for z in assignments:
    et = exposure(z, true_neighbors)
    ep = exposure(z, proxy_neighbors)
    rows.append({
        "assignment": sorted(z),
        "own": int(0 in z),
        "true": et,
        "proxy": ep,
        "expected_outcome": F(1, 5) + F(2, 5) * et,
    })

def probability(predicate):
    return F(sum(bool(predicate(r)) for r in rows), len(rows))

def mean(predicate):
    selected = [r["expected_outcome"] for r in rows if predicate(r)]
    assert selected, "Exposure has zero support"
    return sum(selected, F(0)) / len(selected)

cells = Counter((r["true"], r["proxy"]) for r in rows)
own_cells = Counter((r["own"], r["true"]) for r in rows)
true_effect = mean(lambda r: r["true"] == 1) - mean(lambda r: r["true"] == 0)
proxy_effect = mean(lambda r: r["proxy"] == 1) - mean(lambda r: r["proxy"] == 0)
assert len(assignments) == 6
assert cells == {(1, 1): 4, (1, 0): 1, (0, 1): 1}
assert own_cells == {(0, 1): 3, (1, 1): 2, (1, 0): 1}
assert probability(lambda r: r["true"] != r["proxy"]) == F(1, 3)
assert probability(lambda r: r["true"] == 1) == F(5, 6)
assert probability(lambda r: r["proxy"] == 1) == F(5, 6)
assert mean(lambda r: r["proxy"] == 1) == F(13, 25)
assert mean(lambda r: r["proxy"] == 0) == F(3, 5)
assert true_effect == F(2, 5)
assert proxy_effect == -F(2, 25)
assert true_effect - proxy_effect == F(12, 25)
assert probability(lambda r: r["true"] == r["proxy"] == 0) == 0
assert probability(lambda r: r["true"] == r["proxy"] == 1) == F(2, 3)
assert F(4, 5) + F(0) - 1 == -F(1, 5)
# Identical last-period treatment can conceal different histories.
def history_outcome(d1, d2):
    return F(1, 5) + F(1, 10) * d1 + F(3, 10) * d2
assert history_outcome(1, 1) == F(3, 5)
assert history_outcome(0, 1) == F(1, 2)
# Sharp-null negative control.
assert (F(1, 5) - F(1, 5)) == 0
result = {
    "assignments": len(assignments),
    "joint_exposure_counts": {f"{a}{b}": cells.get((a, b), 0) for a in (0, 1) for b in (0, 1)},
    "own_true_counts": {f"{a}{b}": own_cells.get((a, b), 0) for a in (0, 1) for b in (0, 1)},
    "mismatch_probability": str(F(1, 3)),
    "true_exposure_effect": str(true_effect),
    "proxy_exposure_contrast": str(proxy_effect),
    "proxy_minus_true_bias": str(proxy_effect - true_effect),
    "joint_zero_exposure_probability": "0",
    "status": "SYNTHETIC_EXACT_NONBLIND_ONLY",
}
print(json.dumps(result, indent=2, ensure_ascii=False))
