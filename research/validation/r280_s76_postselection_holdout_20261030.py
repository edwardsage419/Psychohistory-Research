#!/usr/bin/env python3
"""R280 S76: exact eight-bit train/heldout Brier selection, artificial E1.

Usage:
 python r280_s76_postselection_holdout_20261030.py --selftest
 python r280_s76_postselection_holdout_20261030.py --emit /tmp/r280_s76
Standard library only. Independent B verification is a separate program.
"""
import argparse
import csv
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

P = (F(1, 4), F(1, 2), F(3, 4))
Q = (F(1, 4), F(1, 2), F(3, 4))
PRIORITY = {F(1, 2): 0, F(1, 4): 1, F(3, 4): 2}
BITS = tuple(''.join(b) for b in itertools.product('01', repeat=4))
FREEZE_PATH = 'research/validation/R280_S76_POSTSELECTION_HOLDOUT_BRIER_FREEZE_2026-10-30.md'
FREEZE_COMMIT = '468ebb3006e864437fb8fc17cfcb39ed70b1bc1e'
FIELDS = ('true_p', 'train_bits', 'test_bits', 'source_mass', 'chosen_q',
          'train_score_q_1of4', 'train_score_q_1of2', 'train_score_q_3of4',
          'train_chosen_brier', 'train_oracle_brier', 'test_chosen_brier',
          'test_oracle_brier', 'test_regret', 'test_chosen_strictly_better',
          'test_chosen_tied')


def score(bits, q):
    if len(bits) != 4 or any(b not in '01' for b in bits) or q not in Q:
        raise ValueError('four bits and frozen q required')
    return sum(((F(int(b)) - q) ** 2 for b in bits), F(0)) / 4


def choose(train_bits):
    return min(Q, key=lambda q: (score(train_bits, q), PRIORITY[q]))


def probability(p, train_bits, test_bits):
    k = train_bits.count('1') + test_bits.count('1')
    return p ** k * (1 - p) ** (8 - k)


def generate():
    rows = []
    summaries = []
    for p in P:
        sums = {k: F(0) for k in (
            'train_chosen', 'train_oracle', 'test_chosen', 'test_oracle',
            'train_regret', 'test_regret', 'test_minus_train', 'test_better',
            'test_tie', 'squared_bias')}
        chosen_mass = {q: F(0) for q in Q}
        mass_total = F(0)
        for train in BITS:
            q = choose(train)
            train_q = score(train, q)
            train_p = score(train, p)
            for test in BITS:
                mass = probability(p, train, test)
                test_q = score(test, q)
                test_p = score(test, p)
                regret = test_q - test_p
                better = int(test_q < test_p)
                tie = int(test_q == test_p)
                row = dict(zip(FIELDS, (str(p), train, test, str(mass), str(q),
                    str(score(train, Q[0])), str(score(train, Q[1])), str(score(train, Q[2])),
                    str(train_q), str(train_p), str(test_q), str(test_p),
                    str(regret), str(better), str(tie))))
                rows.append(row)
                mass_total += mass
                chosen_mass[q] += mass
                metrics = dict(train_chosen=train_q, train_oracle=train_p,
                    test_chosen=test_q, test_oracle=test_p,
                    train_regret=train_q - train_p, test_regret=regret,
                    test_minus_train=test_q - train_q,
                    test_better=F(better), test_tie=F(tie), squared_bias=(q - p) ** 2)
                for key, value in metrics.items():
                    sums[key] += mass * value
        if mass_total != 1 or sum(chosen_mass.values(), F(0)) != 1:
            raise AssertionError('source probability not normalized')
        if sums['test_regret'] != sums['squared_bias']:
            raise AssertionError('heldout regret is not expected squared bias')
        if sums['test_oracle'] != p * (1 - p):
            raise AssertionError('oracle expected risk wrong')
        summaries.append({
            'true_p': str(p), 'source_types': 256, 'mass': str(mass_total),
            'chosen_probabilities': {str(q): str(chosen_mass[q]) for q in Q},
            'expectations': {k: str(v) for k, v in sums.items()}})
    if len(rows) != 768 or len({(r['true_p'], r['train_bits'], r['test_bits']) for r in rows}) != 768:
        raise AssertionError('full source universe not covered')
    return rows, {
        'research_id': 'R280_S76', 'original_catalogue_id': '12-010',
        'freeze_commit': FREEZE_COMMIT, 'freeze_path': FREEZE_PATH,
        'evidence': 'E1_ARTIFICIAL_EXPLORATORY_NONBLIND',
        'world_count': 3, 'source_types': 768, 'source_types_per_world': 256,
        'train_size': 4, 'heldout_size': 4,
        'candidate_q': [str(q) for q in Q],
        'tie_priority': ['1/2', '1/4', '3/4'],
        'R073': 'FROZEN', 'PESEN_v0_1': 'FROZEN',
        'new_real_human_E2_prediction': 0, 'new_real_historical_E3_prediction': 0,
        'world_results': summaries}


def selftest():
    rows, receipt = generate()
    for p in P:
        subset = [r for r in rows if r['true_p'] == str(p)]
        if len(subset) != 256 or sum((F(r['source_mass']) for r in subset), F(0)) != 1:
            raise AssertionError('per-world coverage or mass failure')
        for train in BITS:
            same_train = [r for r in subset if r['train_bits'] == train]
            if len(same_train) != 16 or len({r['chosen_q'] for r in same_train}) != 1:
                raise AssertionError('future test labels contaminated selection')
            if F(same_train[0]['chosen_q']) != choose(train):
                raise AssertionError('training argmin failure')
    if len(receipt['world_results']) != 3:
        raise AssertionError('three-world completeness failure')
    return True


def emit(destination):
    selftest()
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    rows, receipt = generate()
    csvpath = destination / 'R280_S76_ALL_768_TRAIN_TEST_SOURCE_ATOMS.csv'
    jsonpath = destination / 'R280_S76_EXACT_RESULTS.json'
    with csvpath.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=FIELDS, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)
    jsonpath.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'PASS selftest; {len(rows)} exact sources; {len(receipt["world_results"])} worlds')
    for world in receipt['world_results']:
        print(world['true_p'], world['chosen_probabilities'], world['expectations'])
    print(csvpath)
    print(jsonpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--selftest', action='store_true')
    group.add_argument('--emit', metavar='OUTPUT_DIRECTORY')
    args = parser.parse_args()
    if args.selftest:
        selftest()
        print('PASS selftest: 768 sources, three worlds, future-label invariance')
    else:
        emit(args.emit)
