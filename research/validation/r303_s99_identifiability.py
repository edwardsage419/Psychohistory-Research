#!/usr/bin/env python3
"""R303 S99 exact finite synthetic observational-equivalence study.

No import of the original R303 generator. No empirical data.
"""
import argparse
import csv
import hashlib
import itertools
import json
import unittest
from collections import Counter, defaultdict
from fractions import Fraction as F
from pathlib import Path

LEVELS = (F(0), F(1, 2), F(1))
CONSEQUENCES = (('REWARDED', F(1)), ('NO_CONSEQUENCE', F(1, 2)), ('PUNISHED', F(1, 4)))
FREEZE = '47c82ad9419913b121ae64d655a806eccd071b55'
CSV_NAME = 'R303_S99_ALL_81_IDENTIFIABILITY_WORLDS.csv'
JSON_NAME = 'R303_S99_EXACT_EQUIVALENCE_CLASSES.json'
RECEIPT_NAME = 'R303_S99_MACHINE_RECEIPT.json'
FIELDS = ('world_id', 'attention', 'retention', 'production', 'motivation',
          'latent_acquisition', 'available_response', 'spontaneous_rewarded',
          'incentivized_rewarded', 'spontaneous_neutral', 'incentivized_neutral',
          'spontaneous_punished', 'incentivized_punished', 'class_id')


def make_rows():
    raw = []
    for i, (a, r, p, m) in enumerate(itertools.product(LEVELS, repeat=4), 1):
        learned = a * r
        available = learned * p
        obs = tuple(x for _, c in CONSEQUENCES for x in (available * m * c, available))
        raw.append((i, a, r, p, m, learned, available, obs))
    signatures = sorted({t[-1] for t in raw})
    labels = {sig: f'C{n:03d}' for n, sig in enumerate(signatures, 1)}
    rows = []
    for i, a, r, p, m, learned, available, obs in raw:
        values = (f'W{i:03d}', a, r, p, m, learned, available, *obs, labels[obs])
        rows.append(dict(zip(FIELDS, (str(v) for v in values))))
    return rows


def build():
    rows = make_rows()
    by_class = defaultdict(list)
    for row in rows:
        by_class[row['class_id']].append(row)
    classes = []
    for cid, members in sorted(by_class.items()):
        ls = sorted({F(x['latent_acquisition']) for x in members})
        vs = sorted({F(x['available_response']) for x in members})
        ms = sorted({F(x['motivation']) for x in members})
        signature = [members[0][field] for field in FIELDS[7:13]]
        classes.append({'class_id': cid, 'signature': signature,
                        'member_ids': [x['world_id'] for x in members],
                        'size': len(members), 'latent_acquisition_values': list(map(str, ls)),
                        'available_response_values': list(map(str, vs)),
                        'motivation_values': list(map(str, ms)),
                        'latent_min': str(ls[0]), 'latent_max': str(ls[-1])})
    hist = Counter(x['size'] for x in classes)
    ambiguous = [x for x in classes if len(x['latent_acquisition_values']) > 1]
    max_range = max(F(x['latent_max']) - F(x['latent_min']) for x in classes)
    summary = {
        'total_worlds': len(rows), 'distinct_observable_classes': len(classes),
        'class_size_histogram': {str(k): v for k, v in sorted(hist.items())},
        'largest_class_size': max(x['size'] for x in classes),
        'classes_with_multiple_latent_acquisition': len(ambiguous),
        'worlds_in_multiple_latent_acquisition_classes': sum(x['size'] for x in ambiguous),
        'classes_with_multiple_available_response': sum(len(x['available_response_values']) > 1 for x in classes),
        'classes_with_multiple_motivation': sum(len(x['motivation_values']) > 1 for x in classes),
        'largest_latent_acquisition_range': str(max_range),
        'counterexample': {
            'first_gates': ['1/2', '1', '1', '1'],
            'second_gates': ['1', '1', '1/2', '1'],
            'first_latent_acquisition': '1/2',
            'second_latent_acquisition': '1',
            'shared_signature': ['1/2', '1/2', '1/4', '1/2', '1/8', '1/2'],
        },
    }
    result = {'research_id': 'R303', 'extension': 'S99-v1',
              'freeze_commit': FREEZE, 'original_R303_unchanged': True,
              'scope': 'E1_EXACT_FINITE_SYNTHETIC_IDENTIFIABILITY',
              'new_E2': 0, 'new_E3': 0, 'R073': 'FROZEN', 'PESEN_v0_1': 'FROZEN',
              'summary': summary, 'classes': classes}
    return rows, result


def check(rows, result):
    assert len(rows) == 81
    assert len({(x['attention'], x['retention'], x['production'], x['motivation']) for x in rows}) == 81
    classes = result['classes']
    assert sum(c['size'] for c in classes) == 81
    assert sorted(x for c in classes for x in c['member_ids']) == sorted(x['world_id'] for x in rows)
    assert all(len(c['available_response_values']) == 1 for c in classes)
    by_gate = {(x['attention'], x['retention'], x['production'], x['motivation']): x for x in rows}
    x = by_gate[('1/2', '1', '1', '1')]
    y = by_gate[('1', '1', '1/2', '1')]
    assert x['class_id'] == y['class_id']
    assert x['latent_acquisition'] != y['latent_acquisition']
    assert [x[f] for f in FIELDS[7:13]] == result['summary']['counterexample']['shared_signature']
    assert all(x['spontaneous_rewarded'] == '0' and x['incentivized_rewarded'] == '0'
               for x in rows if x['attention'] == '0')
    return True


def emit(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    rows, result = build()
    check(rows, result)
    with (directory / CSV_NAME).open('w', encoding='utf-8', newline='') as fp:
        w = csv.DictWriter(fp, fieldnames=FIELDS, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    (directory / JSON_NAME).write_text(json.dumps(result, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    receipt = {'research_id': 'R303', 'extension': 'S99-v1', 'freeze_commit': FREEZE,
               'rows': 81, 'classes': result['summary']['distinct_observable_classes'],
               'csv_sha256': hashlib.sha256((directory / CSV_NAME).read_bytes()).hexdigest(),
               'json_sha256': hashlib.sha256((directory / JSON_NAME).read_bytes()).hexdigest(),
               'new_E2': 0, 'new_E3': 0}
    (directory / RECEIPT_NAME).write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    return receipt


class Tests(unittest.TestCase):
    def test_full_partition(self):
        rows, res = build()
        self.assertTrue(check(rows, res))

    def test_zero_gate(self):
        rows, _ = build()
        self.assertTrue(all(x['spontaneous_rewarded'] == '0' for x in rows if x['attention'] == '0'))

    def test_class_consistency(self):
        rows, _ = build()
        for x in rows:
            self.assertEqual(F(x['spontaneous_rewarded']), F(x['available_response']) * F(x['motivation']))
            self.assertEqual(F(x['spontaneous_neutral']), F(x['spontaneous_rewarded']) / 2)
            self.assertEqual(F(x['spontaneous_punished']), F(x['spontaneous_rewarded']) / 4)
            self.assertEqual(F(x['incentivized_rewarded']), F(x['available_response']))


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--emit', metavar='OUTPUT_DIR')
    p.add_argument('--test', action='store_true')
    args = p.parse_args()
    if args.test:
        unittest.main(argv=['R303-S99'], exit=False)
    if args.emit:
        print(json.dumps(emit(args.emit), indent=2))
    if not args.test and not args.emit:
        p.error('specify --test and/or --emit OUTPUT_DIR')
