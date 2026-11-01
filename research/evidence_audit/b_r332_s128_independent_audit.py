#!/usr/bin/env python3
"""Independent nonblind E1 audit of R332 S128 persisted artificial receipts."""
import csv
import io
import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'validation'
CSV_NAME = 'R332_S128_ALL_480_CAPACITY_SUBSETS.csv'
JSON_NAME = 'R332_S128_EXACT_60_CAPACITY_WORLDS.json'
FIELDS = ('recoded','lower_capacity','high_probability_quarters','bits','cost','utility','low_realized','high_realized','expected_utility_quarters','precommit_bits','precommit_expected_quarters','robust_bits','robust_expected_quarters','oracle_low_bits','oracle_high_bits','oracle_expected_quarters','information_value_quarters')
WORLD_FIELDS = ('recoded','lower_capacity','high_probability_quarters','precommit_bits','precommit_expected_quarters','robust_bits','robust_expected_quarters','oracle_low_bits','oracle_high_bits','oracle_expected_quarters','information_value_quarters')


def optimal(recoded, capacity):
    feasible = []
    for flags in product((0, 1), repeat=3):
        bits = ''.join(map(str, flags))
        cost = flags[0] + (1 if recoded else 2) * flags[1] + 3 * flags[2]
        utility = flags[0] + 3 * flags[1] + 4 * flags[2]
        if cost <= capacity:
            feasible.append((utility, bits))
    best = max(x[0] for x in feasible)
    return min(bits for value, bits in feasible if value == best), best


def expected_rows(recoded, lower, quarters):
    low_bits, low_u = optimal(recoded, lower)
    high_bits, high_u = optimal(recoded, lower + 1)
    candidates = []
    for flags in product((0, 1), repeat=3):
        bits = ''.join(map(str, flags))
        cost = flags[0] + (1 if recoded else 2) * flags[1] + 3 * flags[2]
        utility = flags[0] + 3 * flags[1] + 4 * flags[2]
        low = utility if cost <= lower else 0
        high = utility if cost <= lower + 1 else 0
        expected = (4 - quarters) * low + quarters * high
        candidates.append((bits, cost, utility, low, high, expected))
    best = max(x[5] for x in candidates)
    chosen = min(x[0] for x in candidates if x[5] == best)
    robust = 4 * low_u
    oracle = (4 - quarters) * low_u + quarters * high_u
    gap = oracle - best
    if not (oracle >= best >= robust):
        raise ValueError('dominance')
    world = dict(zip(WORLD_FIELDS, (recoded,lower,quarters,chosen,best,low_bits,robust,low_bits,high_bits,oracle,gap)))
    rows = []
    for bits, cost, utility, low, high, expected in candidates:
        rows.append(dict(zip(FIELDS, map(str, (recoded,lower,quarters,bits,cost,utility,low,high,expected,chosen,best,low_bits,robust,low_bits,high_bits,oracle,gap)))))
    return world, rows


def audit(csv_text, json_text):
    reader = csv.DictReader(io.StringIO(csv_text))
    if tuple(reader.fieldnames or ()) != FIELDS:
        raise ValueError('CSV fields')
    actual_rows = list(reader)
    if len(actual_rows) != 480:
        raise ValueError('CSV row count')
    payload = json.loads(json_text)
    if set(payload) != {'model','protocol','source_row_count','world_count','worlds'} or payload['model'] != 'R332_S128_UNCERTAIN_CAPACITY_E1' or payload['protocol'] != 'S128-v1' or payload['source_row_count'] != 480 or payload['world_count'] != 60:
        raise ValueError('JSON identity or evidence tier')
    actual_worlds = payload['worlds']
    if len(actual_worlds) != 60:
        raise ValueError('JSON world count')
    expected_all = []
    expected_worlds = []
    for recoded in (0,1):
        for lower in range(6):
            for quarters in range(5):
                world, rows = expected_rows(recoded, lower, quarters)
                expected_worlds.append(world)
                expected_all.extend(rows)
    if actual_rows != expected_all:
        raise ValueError('CSV source or order mismatch')
    if actual_worlds != expected_worlds:
        raise ValueError('JSON world or summary mismatch')
    return expected_worlds


def selftest(csv_text, json_text):
    original = audit(csv_text, json_text)
    lines = csv_text.splitlines(keepends=True)
    mutations = []
    mutations.append(('missing_row', ''.join(lines[:2] + lines[3:]), json_text))
    mutations.append(('duplicate_row', ''.join(lines[:2] + [lines[1]] + lines[2:]), json_text))
    mutations.append(('cost', csv_text.replace('0,0,000,0,0,0,0,0,0', '0,0,000,1,0,0,0,0,0', 1), json_text))
    mutations.append(('expected', csv_text.replace('0,0,0,000,0,0,0,0,0,', '0,0,0,000,0,0,0,0,1,', 1), json_text))
    obj = json.loads(json_text)
    obj['worlds'][0]['precommit_bits'] = '111'
    mutations.append(('winner', csv_text, json.dumps(obj)))
    obj = json.loads(json_text)
    obj['model'] = 'E2_HUMAN'
    mutations.append(('evidence_upgrade', csv_text, json.dumps(obj)))
    obj = json.loads(json_text)
    obj['worlds'].append(obj['worlds'][0])
    mutations.append(('duplicate_world', csv_text, json.dumps(obj)))
    obj = json.loads(json_text)
    obj['worlds'][0]['information_value_quarters'] = 999
    mutations.append(('gap', csv_text, json.dumps(obj)))
    for name, csv_variant, json_variant in mutations:
        if csv_variant == csv_text and json_variant == json_text:
            raise ValueError('no-op mutation: ' + name)
        try:
            audit(csv_variant, json_variant)
        except (ValueError, KeyError, TypeError):
            continue
        raise ValueError('mutation accepted: ' + name)
    return len(original), len(mutations)


if __name__ == '__main__':
    csv_text = (ROOT / CSV_NAME).read_text(encoding='utf-8')
    json_text = (ROOT / JSON_NAME).read_text(encoding='utf-8')
    n, m = selftest(csv_text, json_text)
    print(f'PASS_NONBLIND_INTERNAL_E1: {n} worlds, {n*8} rows, {m} live mutations rejected')
