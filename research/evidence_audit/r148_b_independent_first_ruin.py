#!/usr/bin/env python3
"""Independent E1 R148 first-ruin audit. Python 3.10+, stdlib only."""
import csv
import json
import sys
from pathlib import Path

YEARS = 8
DEN = 4 ** 16
POLICIES = ('OPEN', 'QUOTA', 'ADAPT')
ORIGINAL_SURVIVAL = {'OPEN': 0, 'QUOTA': 1330196823, 'ADAPT': 1499549355}
ORIGINAL_NET = {'OPEN': 31574720512, 'QUOTA': 29213703324, 'ADAPT': 23770379516}


def independent_transition(stock, rule, weather, failure):
    if stock == 0:
        return 0, 0
    if failure or rule == 'OPEN':
        requested = 2
    elif rule == 'QUOTA':
        requested = 1
    else:
        requested = 0 if stock <= 2 else (1 if stock < 7 else 2)
    take = min(stock, requested)
    remaining = max(0, stock - take - (2 if weather else 0))
    new_stock = min(8, remaining + int(0 < remaining < 7))
    return new_stock, take


def replay(rule):
    stock_mass = {6: 1}
    first = [0] * 9
    harvest = 0
    for year in range(1, 9):
        new_mass = {}
        for stock, old_weight in stock_mass.items():
            for weather in (0, 1):
                for failure in (0, 1):
                    weight = old_weight * (1 if weather else 3) * (1 if failure else 3)
                    successor, extracted = independent_transition(stock, rule, weather, failure)
                    assert stock != 0 or successor == 0
                    new_mass[successor] = new_mass.get(successor, 0) + weight
                    harvest += weight * extracted * 16 ** (8 - year)
                    if stock > 0 and successor == 0:
                        first[year] += weight * 16 ** (8 - year)
        stock_mass = new_mass
        assert sum(stock_mass.values()) == 16 ** year
    survived = sum(m for s, m in stock_mass.items() if s > 0)
    assert sum(first) + survived == DEN
    saved_fee_years = sum(first[t] * (8 - t) for t in range(1, 9))
    fee_eighths = {'OPEN': 0, 'QUOTA': 1, 'ADAPT': 2}[rule]
    net_eighths = 8 * harvest - DEN * 8 * fee_eighths
    assert net_eighths % 8 == 0
    return first[1:], survived, harvest, net_eighths // 8, saved_fee_years


def audit(csv_path):
    rows = list(csv.DictReader(Path(csv_path).open(encoding='utf-8', newline='')))
    assert len(rows) == 3
    checks = 0
    result = {'study': 'R148', 'audit': 'B independent Python DP', 'denominator': DEN, 'evidence': 'E1', 'policies': {}}
    for row in rows:
        policy = row['policy']
        assert policy in POLICIES
        first, survived, harvest, net, saved_years = replay(policy)
        assert int(row['paths']) == 65536
        assert [int(row['first_ruin_t1'])] + [int(row[f't{i}']) for i in range(2, 9)] == first
        assert int(row['survived8']) == survived == ORIGINAL_SURVIVAL[policy]
        assert int(row['weighted_harvest']) == harvest
        assert int(row['weighted_net']) == net == ORIGINAL_NET[policy]
        checks += 4 + 8
        result['policies'][policy] = {
            'first_ruin': first, 'survived': survived, 'harvest_weighted': harvest,
            'net_weighted': net, 'saved_fee_years_weighted': saved_years,
        }
        if policy != 'OPEN':
            assert saved_years > 0
            checks += 1
    # Actual mutated rule: resurrect the absorbing state, which must be rejected.
    def bad_transition(stock):
        return (1, 0) if stock == 0 else independent_transition(stock, 'QUOTA', 0, 0)
    assert bad_transition(0)[0] != independent_transition(0, 'QUOTA', 0, 0)[0]
    try:
        assert bad_transition(0)[0] == 0
    except AssertionError:
        checks += 1
    else:
        raise AssertionError('resurrection mutant escaped')
    # Fee truncation is an adversarial alternative ledger, not the frozen endpoint.
    assert all(result['policies'][p]['saved_fee_years_weighted'] > 0 for p in ('QUOTA', 'ADAPT'))
    checks += 1
    result['checks_passed'] = checks
    result['external_replication'] = False
    result['remote_ci'] = 'NOT_RUN'
    return result


if __name__ == '__main__':
    print(json.dumps(audit(sys.argv[1]), indent=2, ensure_ascii=False))
