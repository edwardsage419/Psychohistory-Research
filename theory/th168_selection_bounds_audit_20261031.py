#!/usr/bin/env python3
"""TH168: exact arithmetic only, synthetic scenarios, no participant records."""
from fractions import Fraction as F

OLD_TOTAL, NEW_TOTAL = 353, 296
OLD_T, OLD_B, OLD_C = 113, 195, 45
NEW_T, NEW_B, NEW_C = 112, 139, 45
assert OLD_T + OLD_B + OLD_C == OLD_TOTAL
assert NEW_T + NEW_B + NEW_C == NEW_TOTAL
assert OLD_TOTAL - NEW_TOTAL == 57
assert OLD_T - NEW_T == 1 and OLD_B - NEW_B == 56 and OLD_C - NEW_C == 0
assert 405 - 52 == OLD_TOTAL and 405 - 109 == NEW_TOTAL
assert 112 + 45 == 157 and 113 + 45 == 158
assert 8572 - 1000 - 102 == 7470
assert 8527 - 1000 - 102 == 7425
assert 8572 - 8527 == 45
assert 8774 - 295 - 365 == 8114

# Transport sensitivity: purely hypothetical common 353-unit target,
# equal unit weights, 296 observed conditional effects and 57 unknown,
# bounded individual causal effects in [-1, 1]. The 2014 and 2016
# universes have NOT been shown to be nested in reality.
known_effect = F(1, 10)
retained_weight = F(NEW_TOTAL, OLD_TOTAL)
unknown_weight = F(OLD_TOTAL - NEW_TOTAL, OLD_TOTAL)
lo = retained_weight * known_effect - unknown_weight
hi = retained_weight * known_effect + unknown_weight
assert (lo, hi) == (F(-137, 1765), F(433, 1765))
assert hi - lo == F(114, 353)
assert lo < 0 < hi
# Synthetic positive/negative missing-world outcomes attain the endpoints.
assert retained_weight * known_effect + unknown_weight * F(-1) == lo
assert retained_weight * known_effect + unknown_weight * F(1) == hi

# Different hypothetical target district weighting; two regions have
# treatment effects +0.2 and -0.2, respectively. No observed India effects.
region_effects = (F(1, 5), F(-1, 5))
source_weights = (F(3, 4), F(1, 4))
target_weights = (F(1, 4), F(3, 4))
source_effect = sum(w * t for w, t in zip(source_weights, region_effects))
target_effect = sum(w * t for w, t in zip(target_weights, region_effects))
assert source_effect == F(1, 10) and target_effect == F(-1, 10)

# TH167 conditional nested 113 -> 112 equal-cluster sensitivity,
# Y in [0,1], unchanged outcomes for the other 112.
assert F(1, OLD_T) == F(1, 113)
print('PASS TH168 exact arithmetic and synthetic bounds')
print(f'population inclusion weight={retained_weight}, unknown={unknown_weight}')
print(f'conditional full-target ATE interval=[{lo}, {hi}] ~ [{float(lo):.6f}, {float(hi):.6f}]')
print(f'interval width={hi-lo} ~ {float(hi-lo):.6f}')
print(f'synthetic reweighting: source={source_effect}, target={target_effect}')
