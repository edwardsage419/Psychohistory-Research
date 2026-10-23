#!/usr/bin/env python3
"""Third-party style R290 audit. Never imports the R290 production module."""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import itertools
import json
import unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parents[1] / 'R290'
FREEZE = '696e86b029581d2b00dc79bdd2219c59427a7980'
SCENARIOS = {
    'MONOTONE': ((8, 6, 4, 2, 1), (1, 2, 4, 6, 8), 21),
    'CENTERED': ((8, 2, 1, 2, 8), (1, 3, 13, 3, 1), 21),
    'IDENTICAL': ((1, 2, 3, 2, 1), (1, 2, 3, 2, 1), 9),
}
EXPECTED = {
    (k, F(n, d), cp, cn): f'{k}_PI{n}of{d}_FP{cp}_FN{cn}'
    for k in SCENARIOS for (n, d) in ((1, 2), (3, 4))
    for cp, cn in ((1, 1), (1, 3))
}


def take_risk(masses, bits, fp, fn):
    # Fully brute-force via truth / evidence joint distribution, no production risk function.
    return sum((masses[0, x] * fp * bits[x] + masses[1, x] * fn * (1-bits[x])
                for x in range(5)), F(0))


def verify(rows, result, receipt, source_bytes, result_bytes):
    if result['freeze_commit'] != FREEZE or receipt['freeze_commit'] != FREEZE:
        raise AssertionError('frozen protocol pointer differs')
    if result['new_human_E2'] != 0 or result['new_historical_E3'] != 0:
        raise AssertionError('evidence promotion forbidden')
    if len(rows) != 120 or len(result['results']) != 12:
        raise AssertionError('incomplete source/summary archive')
    if receipt['sources_sha256'] != hashlib.sha256(source_bytes).hexdigest():
        raise AssertionError('CSV SHA256 mismatch')
    if receipt['results_sha256'] != hashlib.sha256(result_bytes).hexdigest():
        raise AssertionError('JSON SHA256 mismatch')
    by_world = defaultdict(list)
    for row in rows:
        by_world[row['world']].append(row)
    if set(by_world) != set(EXPECTED.values()):
        raise AssertionError('incorrect or missing world names')
    reported = {w['world']: w for w in result['results']}
    if set(reported) != set(by_world):
        raise AssertionError('result world coverage mismatch')
    for (dg, pi, fp, fn), world in EXPECTED.items():
        group = by_world[world]
        if len(group) != 10:
            raise AssertionError('each world requires exactly ten cells')
        if {(int(r['truth']), int(r['evidence_x'])) for r in group} != set(itertools.product((0,1),range(5))):
            raise AssertionError('missing / duplicate truth-evidence combination')
        masses = {}
        n, s, den = SCENARIOS[dg]
        for row in group:
            y, x = int(row['truth']), int(row['evidence_x'])
            expected_likelihood = F((n,s)[y][x], den)
            expected_joint = expected_likelihood * (pi if y else 1-pi)
            if row['dgp'] != dg or F(row['signal_prior']) != pi or int(row['cost_false_positive']) != fp or int(row['cost_false_negative']) != fn:
                raise AssertionError('mislabelled world')
            if F(row['conditional_probability']) != expected_likelihood or F(row['joint_source_probability']) != expected_joint:
                raise AssertionError('false raw probability')
            masses[y,x] = expected_joint
        if sum(masses.values(), F(0)) != 1:
            raise AssertionError('non-normalized joint distribution')
        # Enumerate ALL 32 deterministic binary decision rules independently.
        all_rules = tuple(itertools.product((0,1), repeat=5))
        brute_min = min(take_risk(masses,b,fp,fn) for b in all_rules)
        strict_decisions = tuple(int(masses[1,x]*fn > masses[0,x]*fp) for x in range(5))
        cutoff = tuple((take_risk(masses,tuple(int(x>=t) for x in range(5)),fp,fn),t) for t in range(6))
        crisk, ct = min(cutoff)
        fr = take_risk(masses,tuple(int(x>=3) for x in range(5)),fp,fn)
        br = take_risk(masses,strict_decisions,fp,fn)
        if br != brute_min or br > crisk or crisk > fr:
            raise AssertionError('global loss ordering failed')
        stat = reported[world]
        if (F(stat['bayes_risk']), F(stat['exact_independent_cell_minimum']),
            F(stat['best_single_cutoff_risk']), F(stat['fixed_t3_risk'])) != (br, brute_min, crisk, fr):
            raise AssertionError('risk summary does not recompute')
        if stat['smallest_best_single_cutoff'] != ct or stat['bayes_signal_evidence_bins'] != [i for i,v in enumerate(strict_decisions) if v]:
            raise AssertionError('best cutoff/tie decision not followed')
        if F(stat['gain_over_best_single_cutoff']) != crisk-br:
            raise AssertionError('gap does not recompute')
        if len(stat['roc_thresholds']) != 6:
            raise AssertionError('threshold ROC incomplete')
        hr = sum(F((s[x]),den)*strict_decisions[x] for x in range(5))
        far = sum(F((n[x]),den)*strict_decisions[x] for x in range(5))
        if (F(stat['bayes_hit_rate']), F(stat['bayes_false_alarm_rate'])) != (hr,far):
            raise AssertionError('hit / FA rates are incorrect')
        for t, item in enumerate(stat['roc_thresholds']):
            thit = sum(F(s[x],den) for x in range(t,5))
            tfa = sum(F(n[x],den) for x in range(t,5))
            if (item['t'],F(item['hit_rate']),F(item['false_alarm_rate']),F(item['weighted_risk'])) != (t,thit,tfa,cutoff[t][0]):
                raise AssertionError('ROC point / risk tampered')
        for row in group:
            y, x = int(row['truth']), int(row['evidence_x'])
            if (int(row['bayes_predict_signal']), int(row['best_cutoff_predict_signal']), int(row['fixed_t3_predict_signal'])) != (strict_decisions[x],int(x>=ct),int(x>=3)):
                raise AssertionError('CSV predictions incorrect')
            if int(row['best_cutoff_t']) != ct:
                raise AssertionError('CSV selected threshold incorrect')
            for column, guess in (('bayes_weighted_loss', strict_decisions[x]),
                                  ('best_cutoff_weighted_loss', int(x>=ct)),
                                  ('fixed_t3_weighted_loss', int(x>=3))):
                cell_cost = fp if y == 0 and guess else fn if y == 1 and not guess else 0
                if F(row[column]) != masses[y,x]*cell_cost:
                    raise AssertionError('CSV source-level loss incorrect')
    centered = reported['CENTERED_PI1of2_FP1_FN1']
    if (centered['bayes_signal_evidence_bins'], F(centered['bayes_risk']),
        centered['smallest_best_single_cutoff'], F(centered['best_single_cutoff_risk'])) != ([1,2,3],F(1,6),1,F(1,3)):
        raise AssertionError('nonmonotone counterexample lost')
    return dict(scientific_evidence='E1_EXACT_ARTIFICIAL_ONLY', source_cells=120,
                worlds=12, globally_enumerated_binary_rules_per_world=32,
                independently_recomputed_roc_points=72, csv_and_json_sha256='PASS',
                original_research='R290', new_human_E2=0, new_historical_E3=0)


def load_and_audit():
    csvfile = HERE/'R290_ALL_120_ORIGINAL_LABELED_SIGNAL_SOURCE_CELLS.csv'
    resultfile = HERE/'R290_EXACT_SIGNAL_DETECTION_RESULTS.json'
    receiptfile = HERE/'R290_MACHINE_RECEIPT.json'
    source_bytes, result_bytes = csvfile.read_bytes(), resultfile.read_bytes()
    rows = list(csv.DictReader(io.StringIO(source_bytes.decode('utf-8'))))
    return verify(rows,json.loads(result_bytes),json.loads(receiptfile.read_bytes()),source_bytes,result_bytes)


class NegativeTests(unittest.TestCase):
    def test_audit(self): self.assertEqual(load_and_audit()['source_cells'],120)
    def test_altered_csv_probability_fails(self):
        csvfile=HERE/'R290_ALL_120_ORIGINAL_LABELED_SIGNAL_SOURCE_CELLS.csv'
        resultfile=HERE/'R290_EXACT_SIGNAL_DETECTION_RESULTS.json'
        source_bytes,result_bytes=csvfile.read_bytes(),resultfile.read_bytes()
        rows=list(csv.DictReader(io.StringIO(source_bytes.decode())))
        rows[0]['joint_source_probability']='0'
        with self.assertRaises(AssertionError):
            verify(rows,json.loads(result_bytes),json.loads((HERE/'R290_MACHINE_RECEIPT.json').read_text()),source_bytes,result_bytes)
    def test_bad_digest_fails(self):
        csvfile=HERE/'R290_ALL_120_ORIGINAL_LABELED_SIGNAL_SOURCE_CELLS.csv'
        resultfile=HERE/'R290_EXACT_SIGNAL_DETECTION_RESULTS.json'
        receipt=json.loads((HERE/'R290_MACHINE_RECEIPT.json').read_text())
        receipt['sources_sha256']='0'*64
        with self.assertRaises(AssertionError):
            verify(list(csv.DictReader(io.StringIO(csvfile.read_text()))),json.loads(resultfile.read_text()),
                   receipt,csvfile.read_bytes(),resultfile.read_bytes())

if __name__=='__main__':
    arg=argparse.ArgumentParser()
    group=arg.add_mutually_exclusive_group(required=True)
    group.add_argument('--audit',action='store_true')
    group.add_argument('--test',action='store_true')
    opts=arg.parse_args()
    if opts.test:
        unittest.main(argv=['independent_r290_source_audit'],verbosity=2)
    else:
        print(json.dumps(load_and_audit(),indent=2))
