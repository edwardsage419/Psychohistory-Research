#!/usr/bin/env python3
"""Independent nonblind Fraction oracle for archived R306 S102 finite sources."""
import argparse
import csv
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

POLICIES = {'AVG': (0, 0), 'SOCIAL': (1, 0), 'ARG': (0, 1), 'COMBINED': (1, 1)}
DESIGNS = ('SUPPORT_ONLY', 'COUNTER_ONLY', 'BOTH_CONTEXTS')


def ensure(condition, message):
    if not condition:
        raise ValueError(message)


def oracle(group, policy, context):
    m = sum(group, F(0)) / 3
    q = (m > 0) - (m < 0)
    c = max(group) if q > 0 else min(group) if q < 0 else F(0)
    a = F(q if context == 'SUPPORT' else -q)
    alpha, beta = POLICIES[policy]
    return m, c, a, F(alpha, 2), F(beta, 2), (2-alpha-beta)*m/2 + F(alpha, 2)*c + F(beta, 2)*a


def validate(rows, doc):
    ensure(doc['scope'] == 'E1_ARTIFICIAL_NO_REAL_HUMAN_OR_HISTORICAL_DATA', 'evidence scope')
    ensure(doc['new_E2'] == 0 and doc['new_E3'] == 0, 'evidence inflation')
    ensure(doc['R073'] == 'FROZEN' and doc['PESEN_v0_1'] == 'FROZEN', 'freeze')
    ensure(doc['original_worlds'] == 216 and doc['ordered_groups'] == 27, 'metadata')
    groups = list(itertools.product((F(-1,2), F(0), F(1,2)), repeat=3))
    expected = {}
    for idx, group in enumerate(groups):
        for context in ('SUPPORT', 'COUNTER'):
            for policy in POLICIES:
                expected[(f'{idx:02d}', context, policy)] = (group, oracle(group, policy, context))
    ensure(len(rows) == len(expected), 'missing or extra rows')
    seen = set()
    for row in rows:
        key = (row['group_id'], row['context'], row['policy'])
        ensure(key in expected and key not in seen, 'unknown or duplicate row')
        seen.add(key)
        group, vals = expected[key]
        ensure(row['pre_opinions'] == ';'.join(map(str, group)), 'triplet identity')
        for field, value in zip(('pre_mean','comparator','argument','alpha','beta','post_mean'), vals):
            ensure(F(row[field]) == value, 'numeric field: '+field)
    ensure(seen == set(expected), 'source coverage')
    ensure(len(doc['group_partitions']) == 27, 'partition group coverage')
    totals = {d: [0, 0, 0, 0, defaultdict(int)] for d in DESIGNS}
    for idx, group in enumerate(groups):
        rec = doc['group_partitions'][idx]
        ensure(rec['group_id'] == f'{idx:02d}' and rec['pre_opinions'] == ';'.join(map(str, group)), 'group order')
        for design in DESIGNS:
            signatures = defaultdict(list)
            for policy in POLICIES:
                s = oracle(group, policy, 'SUPPORT')[-1]
                c = oracle(group, policy, 'COUNTER')[-1]
                key = s if design == 'SUPPORT_ONLY' else c if design == 'COUNTER_ONLY' else (s, c)
                signatures[key].append(policy)
            parts = list(signatures.values())
            ensure(rec['partitions'][design] == parts, 'wrong partition: '+design)
            t = totals[design]
            t[0] += len(parts)
            t[1] += sum(len(p) == 1 for p in parts)
            t[2] += sum(len(p) for p in parts if len(p) > 1)
            t[3] += len(parts) == 4
            t[4][','.join(map(str, sorted(map(len, parts))))] += 1
    for design in DESIGNS:
        t = totals[design]
        actual = doc['design_summaries'][design]
        ensure(actual == {'total_classes':t[0], 'unique_policy_worlds':t[1],
                          'ambiguous_policy_worlds':t[2], 'fully_identified_groups':t[3],
                          'accuracy_uniform_prior':str(F(t[0],108)),
                          'class_size_histogram':dict(sorted(t[4].items()))}, 'summary: '+design)
    return True


def mutation_tests(rows, doc):
    import copy
    tests = []
    def rejects(r, d):
        try:
            validate(r, d)
        except (ValueError, KeyError, IndexError, TypeError, ZeroDivisionError):
            return True
        return False
    r = copy.deepcopy(rows); r.append(dict(r[0])); tests.append(rejects(r,doc))
    r = copy.deepcopy(rows); r.pop(); tests.append(rejects(r,doc))
    r = copy.deepcopy(rows); r[0]['post_mean']='99'; tests.append(rejects(r,doc))
    r = copy.deepcopy(rows); r[0]['context']='COUNTER'; tests.append(rejects(r,doc))
    d = copy.deepcopy(doc); d['group_partitions'][0]['partitions']['SUPPORT_ONLY']=[['AVG','SOCIAL','ARG','COMBINED']]; tests.append(rejects(rows,d))
    d = copy.deepcopy(doc); d['design_summaries']['BOTH_CONTEXTS']['accuracy_uniform_prior']='1'; tests.append(rejects(rows,d))
    d = copy.deepcopy(doc); d['design_summaries']['SUPPORT_ONLY']['class_size_histogram']={}; tests.append(rejects(rows,d))
    d = copy.deepcopy(doc); d['new_E2']=1; tests.append(rejects(rows,d))
    d = copy.deepcopy(doc); d['R073']='UNFROZEN'; tests.append(rejects(rows,d))
    ensure(all(tests), 'a mutation escaped validation')
    return len(tests)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('directory', type=Path)
    args = ap.parse_args()
    rows = list(csv.DictReader((args.directory/'R306_S102_ALL_216_POLICY_CONTEXT_WORLDS.csv').open(encoding='utf-8')))
    doc = json.loads((args.directory/'R306_S102_IDENTIFIABILITY_RESULTS.json').read_text(encoding='utf-8'))
    validate(rows, doc)
    print('PASS independent nonblind Fraction source+partition audit; rejected mutations:', mutation_tests(rows, doc))
