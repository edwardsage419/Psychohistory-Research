#!/usr/bin/env python3
"""R317 S113 independent nonblind finite E1 oracle and explicit mutation gates.
No imports from the primary JS scorer or original R317 model.
"""
import csv
import hashlib
import io
import json
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

EDGES = ((0, 1), (0, 2), (1, 2))
MAPS = ('PAIR_ONLY', 'FULL', 'MULTISET', 'STATIC', 'FIRST', 'LAST', 'DISTINCT_COUNT')
ORIGINAL_BLOB = '926c1fee6a473da6bbedb9746cf109f5a3a3eb16'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def enumerate_arrivals(contacts, origin):
    # Exhaustively enumerate strictly increasing time-respecting walks.
    arrivals = [None] * 3
    arrivals[origin] = 0
    def explore(node, next_index):
        for idx in range(next_index, 3):
            u, v = EDGES[contacts[idx]]
            if node == u or node == v:
                dest = v if node == u else u
                t = idx + 1
                if arrivals[dest] is None or t < arrivals[dest]:
                    arrivals[dest] = t
                explore(dest, idx + 1)
    explore(origin, 0)
    return arrivals


def observation(channel, contacts, origin, target):
    if channel == 'PAIR_ONLY': feature = 'none'
    elif channel == 'FULL': feature = ''.join(map(str, contacts))
    elif channel == 'MULTISET': feature = ''.join(map(str, sorted(contacts)))
    elif channel == 'STATIC': feature = ''.join(map(str, sorted(set(contacts))))
    elif channel == 'FIRST': feature = str(contacts[0])
    elif channel == 'LAST': feature = str(contacts[-1])
    elif channel == 'DISTINCT_COUNT': feature = str(len(set(contacts)))
    else: raise ValueError('unexpected observation channel')
    return origin, target, feature


def rebuild(schedules):
    require(len(schedules) == 27, 'missing or duplicate schedule')
    require(set(schedules) == set(range(27)), 'schedule identity coverage')
    source = 'schedule_id,schedule_code,time,contact_index,node_u,node_v\n'
    rows = []
    for sid in range(27):
        contacts = schedules[sid]
        require(len(contacts) == 3 and all(isinstance(x, int) and 0 <= x < 3 for x in contacts), 'contact identity')
        require(contacts == (sid // 9, sid // 3 % 3, sid % 3), 'frozen lexicographic source mismatch')
        code = ''.join(map(str, contacts))
        for t, eid in enumerate(contacts, 1):
            u, v = EDGES[eid]
            source += f'{sid},{code},{t},{eid},{u},{v}\n'
        for origin in range(3):
            times = enumerate_arrivals(contacts, origin)
            for target in range(3):
                if target == origin: continue
                rows.append({'schedule_id': sid, 'schedule_code': code,
                             'origin': origin, 'target': target,
                             'reachable': int(times[target] is not None),
                             'arrival': '' if times[target] is None else str(times[target])})
    require(git_blob(source.encode()) == ORIGINAL_BLOB, 'original 81 source Git blob mismatch')
    require(len(rows) == 162, 'directed target count')
    return rows


def score(rows):
    maps = {}
    for channel in MAPS:
        groups = defaultdict(lambda: [0, 0])
        for row in rows:
            contacts = tuple(map(int, row['schedule_code']))
            k = observation(channel, contacts, row['origin'], row['target'])
            label = row['reachable']
            require(label in (0, 1), 'binary outcome')
            groups[k][label] += 1
        correct = sum(max(g) for g in groups.values())
        brier = sum((Fraction(g[0] * g[1], sum(g)) for g in groups.values()), Fraction()) / 162
        maps[channel] = {'keys': len(groups),
                         'mixed_keys': sum(all(g) for g in groups.values()),
                         'tie_keys': sum(g[0] == g[1] for g in groups.values()),
                         'correct': correct,
                         'accuracy': f'{Fraction(correct, 162).numerator}/{Fraction(correct, 162).denominator}',
                         'brier': f'{brier.numerator}/{brier.denominator}'}
    return maps


def validate(schedules, labels, receipt):
    expected = rebuild(schedules)
    require(len(labels) == 162, 'label count')
    require(labels == expected, 'source/label/arrival mismatch')
    require(receipt.get('evidence') == 'E1_FINITE_ARTIFICIAL_ONLY', 'evidence grade promotion')
    require(receipt.get('source_git_blob') == ORIGINAL_BLOB, 'source blob identity')
    require(receipt.get('instances') == 162 and receipt.get('schedules') == 27, 'universe identity')
    totals = {'positive': sum(r['reachable'] for r in expected),
              'negative': sum(1 - r['reachable'] for r in expected)}
    require(receipt.get('totals') == totals, 'outcome counts')
    require(receipt.get('maps') == score(expected), 'group count / accuracy / Brier mismatch')
    return True


def run(labels_path, receipt_path):
    schedules = {i: (i // 9, i // 3 % 3, i % 3) for i in range(27)}
    with open(labels_path, newline='', encoding='utf-8') as fh:
        labels = []
        for raw in csv.DictReader(fh):
            labels.append({k: (int(v) if k in ('schedule_id', 'origin', 'target', 'reachable') else v)
                           for k, v in raw.items()})
    receipt = json.loads(Path(receipt_path).read_text(encoding='utf-8'))
    validate(schedules, labels, receipt)
    # Explicit mutation gates, no Python asserts, effective under -O.
    import copy
    cases = []
    altered = copy.deepcopy(schedules); altered[26] = altered[25]; del altered[25]
    cases.append(('duplicate_and_missing_schedule', altered, labels, receipt))
    altered = copy.deepcopy(schedules); del altered[26]
    cases.append(('missing_schedule', altered, labels, receipt))
    altered = copy.deepcopy(schedules); altered[0] = (0, 0, 1)
    cases.append(('modified_contact', altered, labels, receipt))
    altered = copy.deepcopy(labels); altered[0]['reachable'] ^= 1
    cases.append(('altered_label', schedules, altered, receipt))
    altered = copy.deepcopy(receipt); altered['maps']['FULL']['keys'] -= 1
    cases.append(('altered_group_count', schedules, labels, altered))
    altered = copy.deepcopy(receipt); altered['maps']['STATIC']['accuracy'] = '1/1'
    cases.append(('altered_accuracy', schedules, labels, altered))
    altered = copy.deepcopy(receipt); altered['maps']['STATIC']['brier'] = '0/1'
    cases.append(('altered_brier', schedules, labels, altered))
    altered = copy.deepcopy(receipt); altered['evidence'] = 'E2_HUMAN_VALIDATED'
    cases.append(('evidence_promotion', schedules, labels, altered))
    rejected = []
    for name, src, rows, rec in cases:
        try: validate(src, rows, rec)
        except (ValueError, TypeError, KeyError): rejected.append(name)
        else: raise RuntimeError('mutation falsely accepted: ' + name)
    print(json.dumps({'status':'PASS','source_blob':ORIGINAL_BLOB,
                      'instances':len(labels),'maps':score(rebuild(schedules)),
                      'mutations_rejected':rejected,'audit':'INTERNAL_NONBLIND_E1_ONLY'}, indent=2))


if __name__ == '__main__':
    require(len(sys.argv) == 3, 'usage: script labels.csv receipt.json')
    run(sys.argv[1], sys.argv[2])
