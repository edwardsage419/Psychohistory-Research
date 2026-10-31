#!/usr/bin/env python3
"""Original R306 B checker metadata mutation; supply original source file path."""
import copy
import hashlib
import importlib.util
import itertools
import sys
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

SOURCE_SHA256 = '96caccf4d55e878fa7f48d02d344232136cd331fe7e28ccc1bb94e10d9950daa'
POLICIES = ('AVG', 'SOCIAL', 'ARG', 'COMBINED')
DESIGNS = ('SUPPORT_ONLY', 'COUNTER_ONLY', 'BOTH_CONTEXTS')


def fixture(b):
    rows, groups_out = [], []
    totals = {d: [0, 0, 0, 0, defaultdict(int)] for d in DESIGNS}
    for i, group in enumerate(itertools.product((F(-1, 2), F(0), F(1, 2)), repeat=3)):
        gid, outputs = f'{i:02d}', {}
        for context in ('SUPPORT', 'COUNTER'):
            for policy in POLICIES:
                vals = b.oracle(group, policy, context)
                fields = (gid, ';'.join(map(str, group)), context, policy, *map(str, vals))
                keys = ('group_id', 'pre_opinions', 'context', 'policy', 'pre_mean', 'comparator', 'argument', 'alpha', 'beta', 'post_mean')
                rows.append(dict(zip(keys, fields)))
                outputs[(context, policy)] = vals[-1]
        record = dict(group_id=gid, pre_opinions=';'.join(map(str, group)), partitions={})
        for design in DESIGNS:
            classes = {}
            for policy in POLICIES:
                key = (outputs[('SUPPORT', policy)] if design == 'SUPPORT_ONLY' else
                       outputs[('COUNTER', policy)] if design == 'COUNTER_ONLY' else
                       (outputs[('SUPPORT', policy)], outputs[('COUNTER', policy)]))
                classes.setdefault(key, []).append(policy)
            parts = list(classes.values())
            record['partitions'][design] = parts
            t = totals[design]
            t[0] += len(parts)
            t[1] += sum(len(p) == 1 for p in parts)
            t[2] += sum(len(p) for p in parts if len(p) > 1)
            t[3] += len(parts) == 4
            t[4][','.join(map(str, sorted(map(len, parts))))] += 1
        groups_out.append(record)
    doc = dict(research_id='R306', extension='S102', scope='E1_ARTIFICIAL_NO_REAL_HUMAN_OR_HISTORICAL_DATA', original_worlds=216, ordered_groups=27, mechanism_policies=list(POLICIES), argument_contexts=['SUPPORT', 'COUNTER'], group_partitions=groups_out, design_summaries={}, R073='FROZEN', PESEN_v0_1='FROZEN', new_E2=0, new_E3=0)
    for d in DESIGNS:
        t = totals[d]
        doc['design_summaries'][d] = dict(total_classes=t[0], unique_policy_worlds=t[1], ambiguous_policy_worlds=t[2], fully_identified_groups=t[3], accuracy_uniform_prior=str(F(t[0], 108)), class_size_histogram=dict(sorted(t[4].items())))
    return rows, doc


def run(source_path):
    assert hashlib.sha256(Path(source_path).read_bytes()).hexdigest() == SOURCE_SHA256
    spec = importlib.util.spec_from_file_location('original_B', source_path)
    b = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(b)
    rows, doc = fixture(b)
    assert b.validate(rows, doc)
    escaped = []
    for field in ('research_id', 'extension', 'mechanism_policies', 'argument_contexts'):
        for operation in ('change', 'delete'):
            candidate = copy.deepcopy(doc)
            if operation == 'delete':
                del candidate[field]
            else:
                candidate[field] = 'INVALID' if isinstance(candidate[field], str) else ['INVALID']
            if b.validate(rows, candidate):
                escaped.append(f'{operation}:{field}')
    assert len(escaped) == 8
    rejected = 0
    for field, value in (('new_E2', 1), ('original_worlds', 999), ('R073', 'UNFROZEN')):
        candidate = copy.deepcopy(doc)
        candidate[field] = value
        try:
            b.validate(rows, candidate)
        except (ValueError, KeyError, TypeError):
            rejected += 1
    assert rejected == 3
    print(f'PASS pinned original B; 216 synthetic rows, 27 groups; {len(escaped)} false accepts; {rejected} controls rejected')
    print('False accepts:', ', '.join(escaped))
    print('Nonblind function-level synthetic fixture; original persisted CSV/JSON CLI NOT_RUN')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise SystemExit('usage: python e136_r306_s102_metadata_mutation_20261031.py original_B.py')
    run(sys.argv[1])
