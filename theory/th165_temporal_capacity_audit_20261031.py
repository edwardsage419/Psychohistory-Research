"""TH165 exact synthetic audit: temporal policy support and capacity threshold.

Only Python standard library. All outcomes and costs are invented rational values.
This script is not an empirical causal estimate or an R-series acceptance test.
"""
from fractions import Fraction as F
from itertools import product

VECTORS = tuple(product((0, 1), repeat=2))
HISTORIES = tuple(product(VECTORS, repeat=2))
FULL = ((1, 1), (1, 1))
ZERO = ((0, 0), (0, 0))
SUPPORTED = tuple(h for h in HISTORIES if h != FULL)


def y1(history):
    return F(2, 5) + F(sum(history[0]), 10)


def y2(history, capacity_interaction):
    k1, k2 = (sum(z) for z in history)
    return F(2, 5) + F(k1 + k2, 10) + (
        capacity_interaction if history == FULL else F(0)
    )


WORLD_A = F(1, 10)   # adaptation, full/full Y2 = 9/10
WORLD_B = F(-3, 5)   # repeated saturation congestion, Y2 = 1/5
assert len(HISTORIES) == 16 and len(SUPPORTED) == 15
assert len(set(SUPPORTED)) == 15 and FULL not in SUPPORTED
assert set(y1(h) for h in HISTORIES) == {F(2, 5), F(1, 2), F(3, 5)}
assert all(y2(h, WORLD_A) == y2(h, WORLD_B) for h in SUPPORTED)
assert all(F(0) <= y2(h, q) <= F(1)
           for h in HISTORIES for q in (WORLD_A, WORLD_B))
assert y2(FULL, WORLD_A) == F(9, 10)
assert y2(FULL, WORLD_B) == F(1, 5)
assert y2(ZERO, WORLD_A) == y2(ZERO, WORLD_B) == F(2, 5)

TTE_A = y2(FULL, WORLD_A) - y2(ZERO, WORLD_A)
TTE_B = y2(FULL, WORLD_B) - y2(ZERO, WORLD_B)
assert (TTE_A, TTE_B) == (F(1, 2), F(-1, 5))

# The four histories adjacent to FULL have K=(1,2) or (2,1).
adjacent = tuple(h for h in SUPPORTED if sum(
    a != b for z, w in zip(h, FULL) for a, b in zip(z, w)
) == 1)
assert len(adjacent) == 4
assert set(y2(h, WORLD_A) for h in adjacent) == {F(7, 10)}

# Sharp intervals for the missing full/full outcome, with a known zero baseline.
raw_y = (F(0), F(1))
monotone_y = (F(7, 10), F(1))
lipschitz_y = (F(1, 2), F(9, 10))  # absolute adjacent difference <= 1/5
both_y = (F(7, 10), F(9, 10))
base = F(2, 5)
cost = F(1, 5)  # four treated person-periods at 1/20 each
bounds = {
    'outcome_bounded': raw_y,
    'monotone': monotone_y,
    'adjacent_lipschitz': lipschitz_y,
    'monotone_and_lipschitz': both_y,
}
expected_tte = {
    'outcome_bounded': (F(-2, 5), F(3, 5)),
    'monotone': (F(3, 10), F(3, 5)),
    'adjacent_lipschitz': (F(1, 10), F(1, 2)),
    'monotone_and_lipschitz': (F(3, 10), F(1, 2)),
}
for label, (lo, hi) in bounds.items():
    assert (lo - base, hi - base) == expected_tte[label]
    for endpoint in (lo, hi):
        q = endpoint - F(4, 5)
        assert y2(FULL, q) == endpoint
        assert all(y2(h, q) == y2(h, WORLD_A) for h in SUPPORTED)
        if 'monotone' in label:
            assert endpoint >= F(7, 10)
        if 'lipschitz' in label:
            assert all(abs(endpoint - y2(h, q)) <= F(1, 5)
                       for h in adjacent)
assert TTE_A - cost == F(3, 10)
assert TTE_B - cost == F(-2, 5)

# Author-reported aggregate arithmetic; not a microdata replication.
assert F(3307, 6797) * 100 > F(486, 10)
assert F(3307, 6797) * 100 < F(487, 10)
assert 4943 + 200 + 135 == 5278
assert F(4943, 5278) * 100 > F(936, 10)
assert F(4943, 5278) * 100 < F(937, 10)

print('TH165 SYNTHETIC PASS: 16 histories, 15 supported, 2 observationally equivalent worlds')
print('TTE worlds A/B:', TTE_A, TTE_B)
for label, b in expected_tte.items():
    print(label, 'TTE', tuple(map(str, b)), 'net',
          tuple(str(v - cost) for v in b))
print('Author aggregate arithmetic checked; no original microdata used.')
