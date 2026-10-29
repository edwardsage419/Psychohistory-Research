#!/usr/bin/env python3
"""Independent Fraction breakpoint audit for frozen R259 S55.

This auditor reads frozen objective tables and enumerates ALL crossings of
pairwise affine weighted costs, without calling the R endpoint shortcut.
This is an internal, nonblind method replication, not an external replication.
"""
import argparse
import json
from fractions import Fraction as F

LABELS = 'ABCDE'
BASE = [(0, 4), (1, 3), (2, 2), (3, 1), (4, 0)]
CONFIG = {
    'LINEAR_FIVE_ALL_SUPPORTED': BASE,
    'CONCAVE_THREE_UNSUPPORTED': [(0, 4), (1, F(7, 2)), (2, 3), (3, 2), (4, 0)],
    'DOMINATED_EXTRAS': [(0, 4), (1, 5), (2, 2), (5, 1), (4, 0)],
    'OBJECTIVE1_MULTIPLY10': [(0, 4), (10, 3), (20, 2), (30, 1), (40, 0)],
    'DUPLICATE_TIE': [(0, 4), (0, 4), (2, 2), (4, 0), (5, 5)],
    'STRICTLY_CONVEX_DISCRETE_FRONT': [(0, 4), (1, F(9, 4)), (2, 1), (3, F(1, 4)), (4, 0)],
    'OBJECTIVE2_MULTIPLY10': [(0, 40), (1, 30), (2, 20), (3, 10), (4, 0)],
    'REVERSE_LABELS': list(reversed(BASE)),
    'LINEAR_COST2_STEEPER': [(0, 8), (1, 6), (2, 4), (3, 2), (4, 0)],
}
INTERVALS = {'FULL': (F(0), F(1)), 'CENTRAL': (F(1, 4), F(3, 4))}


def value(cost, weight):
    a, b = map(F, cost)
    return weight * a + (1 - weight) * b


def breakpoints(costs, lower, upper):
    """Build arrangement vertices of all pairwise affine cost lines."""
    points = {lower, upper}
    for i, (ai, bi) in enumerate(costs):
        for aj, bj in costs[i + 1:]:
            ai, bi, aj, bj = map(F, (ai, bi, aj, bj))
            slope = (ai - bi) - (aj - bj)
            if slope:
                cross = (bj - bi) / slope
                if lower <= cross <= upper:
                    points.add(cross)
    return sorted(points)


def calculate():
    all_rows = []
    for world, costs in CONFIG.items():
        groups = []
        for name, (lower, upper) in INTERVALS.items():
            points = breakpoints(costs, lower, upper)
            # Entire interval is partitioned by pairwise crossings. All
            # regrets are affine within each partition, so vertices suffice.
            scores = [[value(c, w) for c in costs] for w in points]
            regret = {}
            worst = {}
            for i, label in enumerate(LABELS):
                regret[label] = max(row[i] - min(row) for row in scores)
                worst[label] = max(row[i] for row in scores)
            mr, mw = min(regret.values()), min(worst.values())
            groups.append({
                'interval': name,
                'breakpoint_count': len(points),
                'minimax_regret_value': str(mr),
                'minimax_regret_winners': [d for d in LABELS if regret[d] == mr],
                'minimax_worst_weighted_loss_value': str(mw),
                'minimax_worst_weighted_loss_winners': [d for d in LABELS if worst[d] == mw],
                'regret_all_actions': {d: str(regret[d]) for d in LABELS},
                'worst_all_actions': {d: str(worst[d]) for d in LABELS},
            })
        all_rows.append({'world': world, 'intervals': groups})
    return all_rows


def verify_r_receipt(audit, r_receipt):
    assert r_receipt['research_id'] == 'R259_S55'
    assert r_receipt['original_rows'] == 225
    assert len(r_receipt['world_results']) == len(audit) == 9
    comparisons = 0
    for a, b in zip(audit, r_receipt['world_results']):
        assert a['world'] == b['world']
        for x, y in zip(a['intervals'], b['intervals']):
            assert x['interval'] == y['interval']
            for field in ('minimax_regret_value', 'minimax_regret_winners',
                          'minimax_worst_weighted_loss_value', 'minimax_worst_weighted_loss_winners'):
                assert x[field] == y[field], (a['world'], x['interval'], field)
                comparisons += 1
            for d in LABELS:
                assert x['regret_all_actions'][d] == y['all_actions'][d]['worst_regret']
                assert x['worst_all_actions'][d] == y['all_actions'][d]['worst_weighted_loss']
                comparisons += 2
    return comparisons


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--r-receipt', help='R result JSON; optional for independent standalone run')
    args = p.parse_args()
    rows = calculate()
    if args.r_receipt:
        with open(args.r_receipt, encoding='utf-8') as f:
            count = verify_r_receipt(rows, json.load(f))
        print('R259_S55_CROSS_ROUTE_EXACT_PASS', count)
    else:
        print('R259_S55_INDEPENDENT_BREAKPOINT_ORACLE', json.dumps(rows, ensure_ascii=False))


if __name__ == '__main__':
    main()
