#!/usr/bin/env python3
"""Independent, nonblind exact R303 S99 archive auditor, no R generator import."""
import argparse
import copy
import csv
import hashlib
import io
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction as Q
from pathlib import Path

GATES = (Q(0), Q(1, 2), Q(1))
OBS = ('spontaneous_rewarded', 'incentivized_rewarded',
       'spontaneous_neutral', 'incentivized_neutral',
       'spontaneous_punished', 'incentivized_punished')


def audit(rows, data):
    def require(cond, message):
        if not cond:
            raise ValueError(message)
    require(data.get('research_id') == 'R303' and data.get('extension') == 'S99-v1', 'identity')
    require(data.get('scope') == 'E1_EXACT_FINITE_SYNTHETIC_IDENTIFIABILITY'
            and data.get('new_E2') == 0 and data.get('new_E3') == 0, 'evidence scope')
    require(data.get('R073') == 'FROZEN' and data.get('PESEN_v0_1') == 'FROZEN', 'frozen models')
    require(len(rows) == 81, 'world count')
    observed = {}
    keys = defaultdict(set)
    for row in rows:
        gate = tuple(Q(row[n]) for n in ('attention', 'retention', 'production', 'motivation'))
        require(all(x in GATES for x in gate), 'gate grid')
        require(gate not in observed, 'duplicate world')
        a, r, p, m = gate
        v = a*r*p
        l = a*r
        require(Q(row['latent_acquisition']) == l, 'latent mismatch')
        require(Q(row['available_response']) == v, 'available mismatch')
        actual = tuple(Q(row[n]) for n in OBS)
        expected = (v*m, v, v*m/2, v, v*m/4, v)
        require(actual == expected, 'observable mismatch')
        key = ('ZERO',) if v == 0 else ('POS', v, m)
        observed[gate] = (row, key)
        keys[key].add(row['world_id'])
    require(set(observed) == set(itertools.product(GATES, repeat=4)), 'missing gate tuples')
    require(len({row['world_id'] for row in rows}) == 81, 'duplicate world ID')
    classes = data.get('classes', [])
    require(len(classes) == len(keys), 'class count')
    require(len({c['class_id'] for c in classes}) == len(classes), 'class ID duplication')
    by_id = {c['class_id']: c for c in classes}
    require(set(row['class_id'] for row in rows) == set(by_id), 'class ID mismatch')
    require({frozenset(c['member_ids']) for c in classes} == {frozenset(s) for s in keys.values()}, 'class partition')
    for c in classes:
        members = [row for row in rows if row['class_id'] == c['class_id']]
        require(len(members) == c['size'] == len(c['member_ids']), 'class size')
        require(set(c['member_ids']) == {r['world_id'] for r in members}, 'class membership')
        require(c['signature'] == [members[0][k] for k in OBS], 'signature mismatch')
        lvalues = sorted({Q(row['latent_acquisition']) for row in members})
        vvalues = sorted({Q(row['available_response']) for row in members})
        mvalues = sorted({Q(row['motivation']) for row in members})
        require(c['latent_acquisition_values'] == list(map(str, lvalues)), 'latent values')
        require(c['available_response_values'] == list(map(str, vvalues)), 'available values')
        require(c['motivation_values'] == list(map(str, mvalues)), 'motivation values')
        require(c['latent_min'] == str(lvalues[0]) and c['latent_max'] == str(lvalues[-1]), 'latent bounds')
    hist = Counter(len(v) for v in keys.values())
    summary = data['summary']
    require(summary['total_worlds'] == 81 and summary['distinct_observable_classes'] == len(keys), 'summary counts')
    require(summary['class_size_histogram'] == {str(k):v for k,v in sorted(hist.items())}, 'histogram')
    require(summary['largest_class_size'] == max(hist), 'largest class')
    require(summary['classes_with_multiple_latent_acquisition'] == sum(len(c['latent_acquisition_values'])>1 for c in classes), 'latent ambiguity')
    require(summary['worlds_in_multiple_latent_acquisition_classes'] == sum(c['size'] for c in classes if len(c['latent_acquisition_values'])>1), 'ambiguous worlds')
    require(summary['classes_with_multiple_available_response'] == sum(len(c['available_response_values'])>1 for c in classes), 'available ambiguity')
    require(summary['classes_with_multiple_motivation'] == sum(len(c['motivation_values'])>1 for c in classes), 'motivation ambiguity')
    require(Q(summary['largest_latent_acquisition_range']) == max(Q(c['latent_max'])-Q(c['latent_min']) for c in classes), 'range')
    first = (Q(1,2),Q(1),Q(1),Q(1))
    second = (Q(1),Q(1),Q(1,2),Q(1))
    require(observed[first][1] == observed[second][1], 'counterexample partition')
    counter = summary['counterexample']
    require(counter['first_gates'] == list(map(str, first)) and counter['second_gates'] == list(map(str, second)), 'counterexample gates')
    require(counter['first_latent_acquisition'] == '1/2' and counter['second_latent_acquisition'] == '1', 'counterexample latent')
    require(counter['shared_signature'] == [str(x) for x in (Q(1,2),Q(1,2),Q(1,4),Q(1,2),Q(1,8),Q(1,2))], 'counterexample signature')
    return {'worlds': len(rows), 'classes': len(keys), 'algebraic_keys': len(keys), 'status': 'PASS'}


def audit_receipt(csv_bytes, json_bytes, receipt):
    if receipt.get('csv_sha256') != hashlib.sha256(csv_bytes).hexdigest():
        raise ValueError('CSV byte digest mismatch')
    if receipt.get('json_sha256') != hashlib.sha256(json_bytes).hexdigest():
        raise ValueError('JSON byte digest mismatch')
    if receipt.get('rows') != 81 or receipt.get('classes') != 13:
        raise ValueError('receipt count mismatch')


def mutations(rows, data):
    cases = []
    def test(name, mutator):
        r, d = copy.deepcopy(rows), copy.deepcopy(data)
        mutator(r, d)
        try:
            audit(r, d)
        except (ValueError, KeyError, TypeError, IndexError, ZeroDivisionError):
            cases.append((name, 'REJECTED'))
        else:
            cases.append((name, 'FALSE_ACCEPT'))
    test('duplicate_tuple', lambda r,d: r.__setitem__(1, dict(r[0])))
    test('missing_tuple', lambda r,d: r.pop())
    test('alter_observable', lambda r,d: r[-1].__setitem__('spontaneous_rewarded','999'))
    test('alter_latent', lambda r,d: r[-1].__setitem__('latent_acquisition','999'))
    test('alter_class_size', lambda r,d: d['classes'][0].__setitem__('size',999))
    test('alter_class_id', lambda r,d: r[-1].__setitem__('class_id','C999'))
    test('alter_counterexample', lambda r,d: d['summary']['counterexample'].__setitem__('second_latent_acquisition','1/2'))
    test('false_evidence_level', lambda r,d: d.__setitem__('new_E2',1))
    if any(x[1] != 'REJECTED' for x in cases):
        raise AssertionError('mutations not all rejected: '+repr(cases))
    return cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file')
    parser.add_argument('json_file')
    parser.add_argument('receipt_file')
    parser.add_argument('--mutations', action='store_true')
    args = parser.parse_args()
    csv_bytes = Path(args.csv_file).read_bytes()
    json_bytes = Path(args.json_file).read_bytes()
    rows = list(csv.DictReader(io.StringIO(csv_bytes.decode('utf-8'))))
    data = json.loads(json_bytes)
    receipt = json.loads(Path(args.receipt_file).read_text(encoding='utf-8'))
    audit_receipt(csv_bytes, json_bytes, receipt)
    result = audit(rows, data)
    if args.mutations:
        result['mutations'] = mutations(rows, data)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
