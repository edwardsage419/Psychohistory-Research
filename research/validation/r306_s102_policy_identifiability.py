#!/usr/bin/env python3
"""R306 S102: exact artificial policy identifiability, standard library only."""
import argparse
import csv
import hashlib
import itertools
import json
from collections import defaultdict, Counter
from fractions import Fraction as F
from pathlib import Path

LEVELS = (F(-1, 2), F(0), F(1, 2))
POLICIES = {'AVG': (F(0), F(0)), 'SOCIAL': (F(1, 2), F(0)),
            'ARG': (F(0), F(1, 2)), 'COMBINED': (F(1, 2), F(1, 2))}
CONTEXTS = ('SUPPORT', 'COUNTER')
DESIGNS = ('SUPPORT_ONLY', 'COUNTER_ONLY', 'BOTH_CONTEXTS')
COLS = ('group_id', 'pre_opinions', 'context', 'policy', 'pre_mean',
        'comparator', 'argument', 'alpha', 'beta', 'post_mean')


def outcomes(group):
    m = sum(group, F(0)) / 3
    q = (m > 0) - (m < 0)
    c = max(group) if q > 0 else min(group) if q < 0 else F(0)
    result = {}
    for policy, (alpha, beta) in POLICIES.items():
        result[policy] = {}
        for context in CONTEXTS:
            a = F(q if context == 'SUPPORT' else -q)
            post = m + alpha * (c - m) + beta * (a - m)
            result[policy][context] = (m, c, a, alpha, beta, post)
    return result


def partition(results, design):
    buckets = defaultdict(list)
    for policy in POLICIES:
        values = results[policy]
        signature = (values['SUPPORT'][-1] if design == 'SUPPORT_ONLY'
                     else values['COUNTER'][-1] if design == 'COUNTER_ONLY'
                     else (values['SUPPORT'][-1], values['COUNTER'][-1]))
        buckets[signature].append(policy)
    return list(buckets.values())


def build():
    rows, groups = [], []
    stats = {d: {'classes': 0, 'unique': 0, 'ambiguous': 0,
                 'fully_identified_groups': 0, 'histogram': Counter()} for d in DESIGNS}
    for idx, group in enumerate(itertools.product(LEVELS, repeat=3)):
        gid = f'{idx:02d}'
        gstr = ';'.join(map(str, group))
        result = outcomes(group)
        for context in CONTEXTS:
            for policy in POLICIES:
                m, c, a, alpha, beta, post = result[policy][context]
                rows.append(dict(zip(COLS, (gid, gstr, context, policy, str(m),
                                            str(c), str(a), str(alpha), str(beta), str(post)))))
        partitions = {}
        for design in DESIGNS:
            parts = partition(result, design)
            partitions[design] = parts
            st = stats[design]
            st['classes'] += len(parts)
            st['unique'] += sum(len(p) == 1 for p in parts)
            st['ambiguous'] += sum(len(p) for p in parts if len(p) > 1)
            st['fully_identified_groups'] += (len(parts) == 4)
            st['histogram'][','.join(map(str, sorted(map(len, parts))))] += 1
        groups.append({'group_id': gid, 'pre_opinions': gstr, 'partitions': partitions})
    summary = {}
    for d in DESIGNS:
        st = stats[d]
        summary[d] = {'total_classes': st['classes'],
                      'unique_policy_worlds': st['unique'],
                      'ambiguous_policy_worlds': st['ambiguous'],
                      'fully_identified_groups': st['fully_identified_groups'],
                      'accuracy_uniform_prior': str(F(st['classes'], 108)),
                      'class_size_histogram': dict(sorted(st['histogram'].items(), key=lambda kv: (0 if kv[0].isdigit() else 1, kv[0])))}
    data = {'research_id': 'R306', 'extension': 'S102',
            'scope': 'E1_ARTIFICIAL_NO_REAL_HUMAN_OR_HISTORICAL_DATA',
            'original_worlds': 216, 'ordered_groups': 27,
            'mechanism_policies': list(POLICIES), 'argument_contexts': list(CONTEXTS),
            'design_summaries': summary, 'group_partitions': groups,
            'R073': 'FROZEN', 'PESEN_v0_1': 'FROZEN', 'new_E2': 0, 'new_E3': 0}
    return rows, data


def emit(directory):
    rows, data = build()
    directory.mkdir(parents=True, exist_ok=True)
    cp = directory / 'R306_S102_ALL_216_POLICY_CONTEXT_WORLDS.csv'
    jp = directory / 'R306_S102_IDENTIFIABILITY_RESULTS.json'
    with cp.open('w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=COLS, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    jp.write_text(json.dumps(data, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (cp, jp)}


def selftest():
    rows, data = build()
    if len(rows) != 216 or len({(r['group_id'], r['context'], r['policy']) for r in rows}) != 216:
        raise ValueError('incomplete or duplicated universe')
    for d in DESIGNS:
        st = data['design_summaries'][d]
        if st['total_classes'] != 83 or st['unique_policy_worlds'] != 72:
            raise ValueError('unexpected frozen finite partition')
    for group in data['group_partitions']:
        parts = group['partitions']
        if len(parts['BOTH_CONTEXTS']) < max(len(parts['SUPPORT_ONLY']), len(parts['COUNTER_ONLY'])):
            raise ValueError('joint information lost')
        if group['pre_opinions'] == '0;0;0' and parts['BOTH_CONTEXTS'] != [list(POLICIES)]:
            raise ValueError('neutral group control failed')
    return True


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--emit', type=Path)
    ap.add_argument('--test', action='store_true')
    args = ap.parse_args()
    selftest()
    if args.emit:
        print(json.dumps(emit(args.emit), indent=2))
    else:
        print('PASS: 216 artificial policy-context worlds; 27 group partitions; 3 designs')
