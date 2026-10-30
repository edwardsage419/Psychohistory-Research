"""Exact synthetic exposure and policy estimand audit. Standard library only."""
from fractions import Fraction as F
from itertools import product, combinations

BASE = F(1, 2)
WORLDS = {
    "A": (F(1, 10), F(0), F(0)),
    "B": (F(3, 10), F(-2, 5), F(-2, 5)),
}

def outcome(world, own, peer):
    a, b, c = WORLDS[world]
    return BASE + a * own + b * peer + c * own * peer

def exposure(world, p):
    e1 = (1-p)*outcome(world, 1, 0) + p*outcome(world, 1, 1)
    e0 = (1-p)*outcome(world, 0, 0) + p*outcome(world, 0, 1)
    return e1-e0

for name in WORLDS:
    cells = {(own, peer): outcome(name, own, peer)
             for own, peer in product(range(2), repeat=2)}
    assert all(F(0) <= v <= F(1) for v in cells.values())
    tte = outcome(name, 1, 1) - outcome(name, 0, 0)
    print(name, "cells", {str(k): str(v) for k, v in cells.items()}, "TTE", str(tte))
    for p in [F(1, 4), F(1, 2), F(3, 4)]:
        print(name, "p", str(p), "exposure", str(exposure(name, p)))

assert exposure("A", F(1, 2)) == exposure("B", F(1, 2)) == F(1, 10)
assert outcome("A", 1, 1) - outcome("A", 0, 0) == F(1, 10)
assert outcome("B", 1, 1) - outcome("B", 0, 0) == F(-1, 2)
assert [exposure("B", p) for p in [F(1, 4), F(1, 2), F(3, 4)]] == [
    F(1, 5), F(1, 10), F(0)]

# Three people; fixed K=1. Hidden global threshold is never activated
# by a legal experiment allocation, but changes the full-deployment effect.
for z in combinations(range(3), 1):
    outcomes = []
    for gamma in [F(0), F(2, 5), F(-1, 5)]:
        ys = tuple(F(1, 5) + F(1, 10)*int(i in z) +
                   gamma*int(len(z) >= 2) for i in range(3))
        outcomes.append(ys)
    assert outcomes[0] == outcomes[1] == outcomes[2]

for gamma in [F(0), F(2, 5), F(-1, 5)]:
    baseline = F(1, 5)
    full = baseline + F(1, 10) + gamma
    assert F(0) <= full <= F(1)
    print("fixedK gamma", str(gamma), "TTE", str(full-baseline))
print("ALL SYNTHETIC CHECKS PASS")
