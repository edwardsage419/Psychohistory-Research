#!/usr/bin/env python3
"""R290: finite discrete signal detection with exact 120 artificial source cells.

Source-level priors/likelihoods and decisions are deterministic. No human data.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FREEZE = '696e86b029581d2b00dc79bdd2219c59427a7980'
Z, O = F(0), F(1)
X = tuple(range(5))
DGP = {
    'MONOTONE': ((8, 6, 4, 2, 1), (1, 2, 4, 6, 8), 21),
    'CENTERED': ((8, 2, 1, 2, 8), (1, 3, 13, 3, 1), 21),
    'IDENTICAL': ((1, 2, 3, 2, 1), (1, 2, 3, 2, 1), 9),
}
PRIORS = (F(1, 2), F(3, 4))
COSTS = ((1, 1), (1, 3))  # false positive, false negative
WORLDS = tuple(itertools.product(DGP, PRIORS, COSTS))
THRESHOLDS = tuple(range(6))


def validate(dgp: str, pi: F, costs: tuple[int, int]) -> None:
    if (dgp, pi, costs) not in WORLDS:
        raise ValueError('outside frozen 12 artificial worlds')


def likelihoods(dgp: str) -> tuple[tuple[F, ...], tuple[F, ...]]:
    noise, signal, den = DGP[dgp]
    return tuple(F(v, den) for v in noise), tuple(F(v, den) for v in signal)


def full_rule(dgp: str, pi: F, costs: tuple[int, int]) -> tuple[int, ...]:
    validate(dgp, pi, costs)
    pn, ps = likelihoods(dgp)
    fp, fn = costs
    return tuple(int(pi * fn * ps[x] > (O - pi) * fp * pn[x]) for x in X)


def cutoff_rule(t: int) -> tuple[int, ...]:
    if t not in THRESHOLDS:
        raise ValueError('invalid frozen cutoff')
    return tuple(int(x >= t) for x in X)


def rates(dgp: str, rule: tuple[int, ...]) -> tuple[F, F]:
    if len(rule) != 5 or any(v not in (0, 1) for v in rule):
        raise ValueError('binary decision required for every evidence bin')
    pn, ps = likelihoods(dgp)
    return sum((ps[x] * rule[x] for x in X), Z), sum((pn[x] * rule[x] for x in X), Z)


def risk(dgp: str, pi: F, costs: tuple[int, int], rule: tuple[int, ...]) -> F:
    validate(dgp, pi, costs)
    hit, fa = rates(dgp, rule)
    fp, fn = costs
    return (O - pi) * fp * fa + pi * fn * (O - hit)


def independent_cell_bound(dgp: str, pi: F, costs: tuple[int, int]) -> F:
    """Five pointwise minimizations, separate from rule implementation."""
    pn, ps = likelihoods(dgp)
    fp, fn = costs
    return sum((min((O - pi) * fp * pn[x], pi * fn * ps[x]) for x in X), Z)


def best_cutoff(dgp: str, pi: F, costs: tuple[int, int]) -> tuple[int, F]:
    validate(dgp, pi, costs)
    pairs = tuple((risk(dgp, pi, costs, cutoff_rule(t)), t) for t in THRESHOLDS)
    best, smallest_t = min(pairs)
    return smallest_t, best


def world_name(dgp: str, pi: F, costs: tuple[int, int]) -> str:
    return f'{dgp}_PI{pi.numerator}of{pi.denominator}_FP{costs[0]}_FN{costs[1]}'


def source_rows(dgp: str, pi: F, costs: tuple[int, int]):
    validate(dgp, pi, costs)
    pn, ps = likelihoods(dgp)
    bayes = full_rule(dgp, pi, costs)
    t, _ = best_cutoff(dgp, pi, costs)
    best = cutoff_rule(t)
    fixed = cutoff_rule(3)
    for truth, distribution, prior in ((0, pn, O - pi), (1, ps, pi)):
        for x in X:
            class_cond = distribution[x]
            p = prior * class_cond
            actual_bayes = bayes[x]
            actual_best = best[x]
            actual_fixed = fixed[x]
            def contribution(decision: int) -> F:
                return p * (costs[0] if truth == 0 and decision else
                            costs[1] if truth == 1 and not decision else 0)
            yield dict(world=world_name(dgp, pi, costs), dgp=dgp,
                       signal_prior=str(pi), cost_false_positive=costs[0],
                       cost_false_negative=costs[1], truth=truth, evidence_x=x,
                       conditional_probability=str(class_cond),
                       joint_source_probability=str(p),
                       bayes_predict_signal=actual_bayes,
                       best_cutoff_t=t, best_cutoff_predict_signal=actual_best,
                       fixed_t3_predict_signal=actual_fixed,
                       bayes_weighted_loss=str(contribution(actual_bayes)),
                       best_cutoff_weighted_loss=str(contribution(actual_best)),
                       fixed_t3_weighted_loss=str(contribution(actual_fixed)))


def analysis(dgp: str, pi: F, costs: tuple[int, int]) -> dict:
    validate(dgp, pi, costs)
    b_rule = full_rule(dgp, pi, costs)
    t, b_cutoff_risk = best_cutoff(dgp, pi, costs)
    bayes_risk = risk(dgp, pi, costs, b_rule)
    fixed_risk = risk(dgp, pi, costs, cutoff_rule(3))
    b_hit, b_fa = rates(dgp, b_rule)
    rows = tuple(source_rows(dgp, pi, costs))
    assert len(rows) == 10
    assert sum((F(r['joint_source_probability']) for r in rows), Z) == O
    assert sum((F(r['bayes_weighted_loss']) for r in rows), Z) == bayes_risk
    assert sum((F(r['best_cutoff_weighted_loss']) for r in rows), Z) == b_cutoff_risk
    assert sum((F(r['fixed_t3_weighted_loss']) for r in rows), Z) == fixed_risk
    assert bayes_risk == independent_cell_bound(dgp, pi, costs)
    assert bayes_risk <= b_cutoff_risk <= fixed_risk
    return dict(world=world_name(dgp, pi, costs), model=dgp,
                signal_prior=str(pi), cost_false_positive=costs[0],
                cost_false_negative=costs[1], sources=10,
                bayes_signal_evidence_bins=[x for x in X if b_rule[x]],
                bayes_risk=str(bayes_risk), bayes_hit_rate=str(b_hit),
                bayes_false_alarm_rate=str(b_fa),
                exact_independent_cell_minimum=str(independent_cell_bound(dgp, pi, costs)),
                smallest_best_single_cutoff=t,
                best_single_cutoff_risk=str(b_cutoff_risk),
                fixed_t3_risk=str(fixed_risk),
                gain_over_best_single_cutoff=str(b_cutoff_risk - bayes_risk),
                roc_thresholds=[dict(t=t, hit_rate=str(rates(dgp, cutoff_rule(t))[0]),
                                     false_alarm_rate=str(rates(dgp, cutoff_rule(t))[1]),
                                     weighted_risk=str(risk(dgp, pi, costs, cutoff_rule(t))))
                                for t in THRESHOLDS])


def claims() -> None:
    assert len(WORLDS) == 12
    for dgp in DGP:
        pn, ps = likelihoods(dgp)
        assert sum(pn, Z) == sum(ps, Z) == O
        assert min(pn + ps) > 0
    for dgp, pi, costs in WORLDS:
        output = analysis(dgp, pi, costs)
        # Exhaust all deterministic policies to check global minimax Bayes risk.
        exact_minimum = min(risk(dgp, pi, costs, rule)
                            for rule in itertools.product((0, 1), repeat=5))
        assert F(output['bayes_risk']) == exact_minimum
        assert all(F(row['hit_rate']) <= O and F(row['false_alarm_rate']) <= O
                   for row in output['roc_thresholds'])
    assert full_rule('CENTERED', F(1, 2), (1, 1)) == (0, 1, 1, 1, 0)
    assert risk('CENTERED', F(1, 2), (1, 1), (0, 1, 1, 1, 0)) == F(1, 6)
    assert best_cutoff('CENTERED', F(1, 2), (1, 1)) == (1, F(1, 3))
    # Indistinguishable signal and noise show the same conditional response rate.
    for pi in PRIORS:
        for costs in COSTS:
            r = full_rule('IDENTICAL', pi, costs)
            hit, fa = rates('IDENTICAL', r)
            assert hit == fa
    # Increasing FN loss or signal base rate can only expand Bayes-positive bins.
    for dgp in DGP:
        for pi in PRIORS:
            old, new = full_rule(dgp, pi, (1, 1)), full_rule(dgp, pi, (1, 3))
            assert all(a <= b for a, b in zip(old, new))
        for costs in COSTS:
            old, new = full_rule(dgp, F(1, 2), costs), full_rule(dgp, F(3, 4), costs)
            assert all(a <= b for a, b in zip(old, new))


def emit() -> dict:
    claims()
    sources = ROOT / 'R290_ALL_120_ORIGINAL_LABELED_SIGNAL_SOURCE_CELLS.csv'
    columns = ('world','dgp','signal_prior','cost_false_positive','cost_false_negative',
               'truth','evidence_x','conditional_probability','joint_source_probability',
               'bayes_predict_signal','best_cutoff_t','best_cutoff_predict_signal',
               'fixed_t3_predict_signal','bayes_weighted_loss',
               'best_cutoff_weighted_loss','fixed_t3_weighted_loss')
    with sources.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=columns, lineterminator='\n')
        writer.writeheader()
        for w in WORLDS:
            for r in source_rows(*w):
                writer.writerow(r)
    result = ROOT / 'R290_EXACT_SIGNAL_DETECTION_RESULTS.json'
    result.write_text(json.dumps(dict(research_id='R290', original_catalogue_id='01-011',
              freeze_commit=FREEZE, scope='EXACT_ARTIFICIAL_DISCRETE_SDT_E1_ONLY',
              worlds=12, labeled_source_cells=120, number_of_roc_cutoffs=6,
              new_human_E2=0, new_historical_E3=0, R073='FROZEN', PESEN_v0_1='FROZEN',
              results=[analysis(*w) for w in WORLDS]), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    receipt = dict(research_id='R290', freeze_commit=FREEZE, source_cells=120,
           sources_sha256=hashlib.sha256(sources.read_bytes()).hexdigest(),
           results_sha256=hashlib.sha256(result.read_bytes()).hexdigest(),
           new_human_E2=0, new_historical_E3=0)
    (ROOT / 'R290_MACHINE_RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n', encoding='utf-8')
    return receipt


class BasicTests(unittest.TestCase):
    def test_world_count(self): self.assertEqual(len(WORLDS), 12)
    def test_source_total(self): self.assertEqual(sum(len(tuple(source_rows(*w))) for w in WORLDS), 120)
    def test_all_claims(self): claims()
    def test_bad_world(self):
        with self.assertRaises(ValueError): full_rule('CENTERED', F(1, 3), (1, 1))
    def test_bad_cutoff(self):
        with self.assertRaises(ValueError): cutoff_rule(6)
    def test_bad_rule(self):
        with self.assertRaises(ValueError): rates('CENTERED', (0, 2, 1, 1, 0))
    def test_nonmonotone_case(self):
        self.assertEqual(full_rule('CENTERED', F(1, 2), (1, 1)), (0, 1, 1, 1, 0))
        self.assertEqual(F(analysis('CENTERED', F(1, 2), (1, 1))['gain_over_best_single_cutoff']), F(1, 6))
    def test_identical(self):
        self.assertEqual(likelihoods('IDENTICAL')[0], likelihoods('IDENTICAL')[1])
        self.assertEqual(full_rule('IDENTICAL', F(1, 2), (1, 1)), (0,)*5)
    def test_source_mass(self):
        for w in WORLDS:
            self.assertEqual(sum((F(r['joint_source_probability']) for r in source_rows(*w)), Z), O)


def create_world_test(dgp, pi, costs, aspect):
    def test(self):
        rr = analysis(dgp, pi, costs)
        rows = tuple(source_rows(dgp, pi, costs))
        b_rule = full_rule(dgp, pi, costs)
        if aspect == 'mass':
            self.assertEqual(sum((F(r['joint_source_probability']) for r in rows), Z), O)
        elif aspect == 'labels':
            self.assertEqual({(int(r['truth']), int(r['evidence_x'])) for r in rows},
                             set(itertools.product((0, 1), range(5))))
        elif aspect == 'cell_bound':
            self.assertEqual(F(rr['bayes_risk']), independent_cell_bound(dgp, pi, costs))
        elif aspect == 'global_best':
            self.assertEqual(F(rr['bayes_risk']), min(risk(dgp, pi, costs, x)
                                      for x in itertools.product((0, 1), repeat=5)))
        elif aspect == 'ordering':
            self.assertLessEqual(F(rr['bayes_risk']), F(rr['best_single_cutoff_risk']))
            self.assertLessEqual(F(rr['best_single_cutoff_risk']), F(rr['fixed_t3_risk']))
        elif aspect == 'loss_sum':
            self.assertEqual(sum((F(r['bayes_weighted_loss']) for r in rows), Z), risk(dgp, pi, costs, b_rule))
        elif aspect == 'min_cutoff':
            self.assertEqual(rr['smallest_best_single_cutoff'], min(
                t for t in THRESHOLDS if risk(dgp, pi, costs, cutoff_rule(t)) ==
                                            F(rr['best_single_cutoff_risk'])))
        elif aspect == 'rates':
            self.assertEqual((F(rr['bayes_hit_rate']), F(rr['bayes_false_alarm_rate'])),rates(dgp, b_rule))
        elif aspect == 'roc':
            self.assertEqual(len(rr['roc_thresholds']), 6)
            self.assertEqual([v['t'] for v in rr['roc_thresholds']], list(THRESHOLDS))
        else: raise AssertionError(aspect)
    return test

for dg, prior, co in WORLDS:
    for kind in ('mass','labels','cell_bound','global_best','ordering','loss_sum','min_cutoff','rates','roc'):
        setattr(BasicTests, 'test_'+world_name(dg,prior,co)+'_'+kind, create_world_test(dg,prior,co,kind))

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--test', action='store_true')
    group.add_argument('--emit', action='store_true')
    args = ap.parse_args()
    if args.test:
        unittest.main(argv=['r290'], verbosity=1)
    else:
        print(json.dumps(emit(), indent=2))
