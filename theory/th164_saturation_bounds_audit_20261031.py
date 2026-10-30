"""TH164 synthetic saturation-policy partial-identification audit.
Only standard library, exact rational arithmetic; no human data or CI.
"""
from fractions import Fraction as F
from itertools import combinations, product

N = 4
GRID = tuple(F(k, 5) for k in range(6))
F1, F2 = F(2, 5), F(3, 5)
COST_FULL = F(3, 10)


def feasible(curve, monotone=False, slope_cap=False):
    if monotone and any(curve[k + 1] < curve[k] for k in range(N)):
        return False
    if slope_cap and any(abs(curve[k + 1] - curve[k]) > F(1, 5)
                         for k in range(N)):
        return False
    return True


def extrema(curves, statistic):
    values = [statistic(c) for c in curves]
    return min(values), max(values)


def as_text(pair):
    return tuple(str(x) for x in pair)


def main():
    all_curves = [(f0, F1, F2, f3, f4)
                  for f0, f3, f4 in product(GRID, repeat=3)]
    mono = [f for f in all_curves if feasible(f, monotone=True)]
    mono_lip = [f for f in mono if feasible(f, slope_cap=True)]
    assert (len(all_curves), len(mono), len(mono_lip)) == (216, 18, 8)

    tte = lambda f: f[4] - f[0]
    net = lambda f: tte(f) - COST_FULL
    four_vs_two = lambda f: f[4] - f[2] - COST_FULL * F(2, 4)
    expected = {
        'bounded': ((F(-1), F(1)), (F(-13, 10), F(7, 10)),
                    (F(-3, 4), F(1, 4))),
        'monotone': ((F(1, 5), F(1)), (F(-1, 10), F(7, 10)),
                     (F(-3, 20), F(1, 4))),
        'monotone_and_slope_cap': ((F(1, 5), F(4, 5)),
                                   (F(-1, 10), F(1, 2)),
                                   (F(-3, 20), F(1, 4))),
    }
    for label, curves in [('bounded', all_curves), ('monotone', mono),
                          ('monotone_and_slope_cap', mono_lip)]:
        observed = (extrema(curves, tte), extrema(curves, net),
                    extrema(curves, four_vs_two))
        assert observed == expected[label], (label, observed)
        print(label, 'count', len(curves),
              'TTE', as_text(observed[0]),
              'net4v0', as_text(observed[1]),
              'net4v2', as_text(observed[2]))

    low = (F(2, 5), F(2, 5), F(3, 5), F(3, 5), F(3, 5))
    high = (F(1, 5), F(2, 5), F(3, 5), F(4, 5), F(1))
    congestion = (F(2, 5), F(2, 5), F(3, 5), F(2, 5), F(1, 5))
    assert low in mono_lip and high in mono_lip
    assert congestion in all_curves and feasible(congestion, slope_cap=True)
    assert not feasible(congestion, monotone=True)
    assert (tte(low), tte(high), tte(congestion)) == (F(1, 5), F(4, 5), F(-1, 5))
    assert (net(low), net(high)) == (F(-1, 10), F(1, 2))

    # Every supported K=1 or K=2 assignment has identical potential outcomes
    # in the three synthetic worlds, despite different full-policy outcomes.
    legal = tuple(z for z in product((0, 1), repeat=N) if sum(z) in (1, 2))
    assert len(legal) == 10
    for z in legal:
        assert tuple(low[sum(z)] for _ in z) == tuple(high[sum(z)] for _ in z)
        assert tuple(low[sum(z)] for _ in z) == tuple(congestion[sum(z)] for _ in z)
    assert len(list(combinations(range(N), 1))) == 4
    assert len(list(combinations(range(N), 2))) == 6
    print('legal_assignments', len(legal), 'low_high_congestion_identical', True)
    print('synthetic_exact_assertions', 'PASS')


if __name__ == '__main__':
    main()
