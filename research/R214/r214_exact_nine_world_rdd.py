#!/usr/bin/env python3
"""R214-S9. Execute the already frozen nine-world / 576-source design.

Only the finite artificial complete probability space is evaluated. All
observable estimators use R, U (only for the declared adjusted estimator),
D, observed Y and source weights. True Y0/Y1 and tau enter oracle audit only.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
Z = F(0)
ONE = F(1)
RS = tuple(F(i, 8) for i in list(range(-8, 0)) + list(range(1, 9)))
HS = tuple(F(i, 8) for i in (1, 2, 3, 4))
WORLDS = (
    'LINEAR_CONSTANT', 'LINEAR_EFFECT_SLOPE', 'COMMON_CURVATURE',
    'DIFFERENTIAL_CURVATURE', 'BASELINE_JUMP', 'SORTED_LATENT_TYPE',
    'DENSITY_JUMP_ONLY', 'PLACEBO_JUMP_NO_TREATMENT',
    'TREATED_SIDE_CURVATURE'
)


def base(world, r, u):
    if world not in WORLDS or u not in (0, 1):
        raise ValueError('invalid world or latent type')
    if world == 'LINEAR_EFFECT_SLOPE':
        return 1 + 2 * r
    if world in ('COMMON_CURVATURE', 'DIFFERENTIAL_CURVATURE'):
        return 1 + r + r*r
    if world in ('BASELINE_JUMP', 'PLACEBO_JUMP_NO_TREATMENT'):
        return 1 + r + int(r >= 0)
    if world == 'SORTED_LATENT_TYPE':
        return 1 + r + 2*u
    if world == 'TREATED_SIDE_CURVATURE':
        return 1 + r + (r*r if r >= 0 else Z)
    return 1 + r


def tau(world, r):
    if world == 'PLACEBO_JUMP_NO_TREATMENT':
        return Z
    if world == 'LINEAR_EFFECT_SLOPE':
        return 2 + 3*r
    if world == 'DIFFERENTIAL_CURVATURE':
        return 2 + 2*r*r
    return F(2)


def original_source_rows(world):
    if world not in WORLDS:
        raise ValueError('unknown artificial world')
    rows = []
    for r in RS:
        pr = F(1, 16) if world != 'DENSITY_JUMP_ONLY' else (F(3, 32) if r > 0 else F(1, 32))
        p1 = F(1, 2) if world != 'SORTED_LATENT_TYPE' else (F(3, 4) if r > 0 else F(1, 4))
        for u in (0, 1):
            pu = p1 if u else 1-p1
            for e in (-1, 1):
                d = int(r > 0)
                y0, y1 = base(world, r, u)+F(e, 4), base(world, r, u)+tau(world, r)+F(e, 4)
                rows.append(dict(world=world, observed_R=r, observed_U=u,
                                 assigned_D=d, noise_E=e,
                                 observed_Y=y1 if d else y0,
                                 source_probability=pr*pu/F(2),
                                 oracle_Y0=y0, oracle_Y1=y1,
                                 oracle_true_tau_at_R=tau(world, r)))
    assert len(rows) == 64 and sum((a['source_probability'] for a in rows), Z) == 1
    return tuple(rows)


def conditional_means(rows, include_u=False):
    numerator, denominator = defaultdict(F), defaultdict(F)
    for row in rows:
        key = (row['observed_R'], row['observed_U']) if include_u else row['observed_R']
        numerator[key] += row['source_probability']*row['observed_Y']
        denominator[key] += row['source_probability']
    if any(m <= 0 for m in denominator.values()):
        raise AssertionError('unsupported conditional cell')
    return {k: numerator[k]/denominator[k] for k in numerator}


def fitted_two_site_intercept(h, means, side):
    # Normal equations are independent of the 2*y(h)-y(2h) closed form.
    x1, x2 = side*h, side*2*h
    y1, y2 = means[x1], means[x2]
    det = F(2)*(x1*x1+x2*x2) - (x1+x2)**2
    assert det > 0
    normal = ((x1*x1+x2*x2)*(y1+y2) - (x1+x2)*(x1*y1+x2*y2))/det
    assert normal == 2*y1-y2
    return normal


def fitted_estimators(rows, h):
    if h not in HS:
        raise ValueError('unfrozen bandwidth')
    mu = conditional_means(rows)
    adjusted = conditional_means(rows, include_u=True)
    loc = mu[h]-mu[-h]
    linear = fitted_two_site_intercept(h, mu, 1)-fitted_two_site_intercept(h, mu, -1)
    by_u = []
    for u in (0, 1):
        umu = {r:adjusted[(r,u)] for r in RS}
        by_u.append(fitted_two_site_intercept(h, umu, 1)-fitted_two_site_intercept(h, umu, -1))
    return dict(local_constant=loc, local_linear=linear,
                observed_U_standardized_linear=sum(by_u, Z)/2)


def world_result(world):
    rows = original_source_rows(world)
    mu = conditional_means(rows)
    pm = {r:sum((a['source_probability'] for a in rows if a['observed_R'] == r), Z) for r in RS}
    target = tau(world, Z)
    fits = []
    for h in HS:
        estim = fitted_estimators(rows, h)
        fits.append(dict(h=str(h), **{k:str(v) for k,v in estim.items()},
                         local_linear_bias=str(estim['local_linear']-target),
                         adjusted_linear_bias=str(estim['observed_U_standardized_linear']-target)))
    return dict(world=world, source_rows=len(rows), probability_sum='1',
                oracle_tau_cutoff=str(target),
                marginal_R_positive_negative_site_ratio=str(pm[F(1,8)]/pm[F(-1,8)]),
                observed_mean_R_near_cutoff=[str(mu[-F(1,8)]),str(mu[F(1,8)])],
                four_frozen_h_estimators=fits)


def generate():
    worlds=[world_result(w) for w in WORLDS]
    out = dict(research_id='R214-S9', catalog_id='09-005',
               evidence='ARTIFICIAL_FINITE_E1_ONLY', scientific_status='BOUNDED_E1',
               protocol='protocols/R214_RDD_9_WORLDS_576_ORIGINAL_SOURCES_36_LOCAL_EXTRAPOLATIONS_PRESCORE_FREEZE_2026-10-22.md',
               worlds=worlds, complete_source_rows=576, fixed_local_fit_rows=36,
               new_real_human_E2=0, new_real_history_E3=0)
    source_file=HERE/'R214_S9_ALL_576_ORIGINAL_RDD_SOURCES.csv'
    flds=('world','observed_R','observed_U','assigned_D','noise_E','observed_Y','source_probability','oracle_Y0','oracle_Y1','oracle_true_tau_at_R')
    with source_file.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=flds,lineterminator='\n')
        writer.writeheader()
        for w in WORLDS:
            for row in original_source_rows(w):
                writer.writerow({k:str(row[k]) for k in flds})
    fits_file=HERE/'R214_S9_ALL_36_LOCAL_EXTRAPOLATIONS.csv'
    with fits_file.open('w',newline='',encoding='utf-8') as f:
        fields=('world','h','local_constant','local_linear','observed_U_standardized_linear','local_linear_bias','adjusted_linear_bias')
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator='\n')
        writer.writeheader()
        for w in worlds:
            for fit in w['four_frozen_h_estimators']:
                writer.writerow(dict(world=w['world'],**fit))
    result_file=HERE/'R214_S9_EXACT_RESULTS.json'
    result_file.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    receipt=dict(research_id='R214-S9', frozen_original_worlds=9,
                 complete_source_rows=576, four_bandwidths=4, total_estimator_rows=36,
                 new_E2=0,new_E3=0,
                 source_sha256=hashlib.sha256(source_file.read_bytes()).hexdigest(),
                 fits_sha256=hashlib.sha256(fits_file.read_bytes()).hexdigest(),
                 results_sha256=hashlib.sha256(result_file.read_bytes()).hexdigest())
    (HERE/'R214_S9_FINAL_MACHINE_ACCEPTANCE.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    return receipt


class TestR214S9(unittest.TestCase):
    def test_number_of_worlds(self): self.assertEqual(len(WORLDS),9)
    def test_source_worlds(self): self.assertEqual(sum(len(original_source_rows(w)) for w in WORLDS),576)
    def test_bandwidths(self): self.assertEqual(len(HS),4)
    def test_missing_cutoff(self): self.assertNotIn(Z,RS)
    def test_both_sides(self): self.assertEqual((sum(r<0 for r in RS),sum(r>0 for r in RS)),(8,8))
    def test_sorted_latent_adjustment(self):
        e=fitted_estimators(original_source_rows('SORTED_LATENT_TYPE'),F(1,8))
        self.assertEqual(e['local_linear'],3)
        self.assertEqual(e['observed_U_standardized_linear'],2)
    def test_density_only_ratio(self):
        self.assertEqual(world_result('DENSITY_JUMP_ONLY')['marginal_R_positive_negative_site_ratio'],'3')
    def test_linear_treatment_target(self):
        self.assertEqual(tau('LINEAR_EFFECT_SLOPE',F(1,2)),F(7,2))
    def test_observed_assignment(self):
        for w in WORLDS:
            for row in original_source_rows(w):
                self.assertEqual(row['assigned_D'],int(row['observed_R']>0))
                self.assertEqual(row['observed_Y'],row['oracle_Y1'] if row['assigned_D'] else row['oracle_Y0'])
    def test_unknown_world(self):
        with self.assertRaises(ValueError): original_source_rows('UNKNOWN')
    def test_unknown_h(self):
        with self.assertRaises(ValueError): fitted_estimators(original_source_rows('LINEAR_CONSTANT'),F(3,4))
    def test_alias_identical_means_different_tau(self):
        a=conditional_means(original_source_rows('BASELINE_JUMP'))
        b=conditional_means(original_source_rows('PLACEBO_JUMP_NO_TREATMENT'))
        self.assertNotEqual(a,b)


def _case(world, kind):
    def t(self):
        rows=original_source_rows(world)
        if kind=='mass':
            self.assertEqual(sum((r['source_probability'] for r in rows),Z),1)
        elif kind=='conditional':
            mu=conditional_means(rows)
            self.assertEqual(len(mu),16)
            for r in RS: self.assertIn(r,mu)
        elif kind=='oracle':
            for row in rows: self.assertEqual(row['oracle_Y1']-row['oracle_Y0'],row['oracle_true_tau_at_R'])
        elif kind=='fit':
            for h in HS:
                obs=fitted_estimators(rows,h)
                self.assertEqual(set(obs),{'local_constant','local_linear','observed_U_standardized_linear'})
        else: raise AssertionError('unknown test kind')
    return t
for _w in WORLDS:
    for _kind in ('mass','conditional','oracle','fit'):
        setattr(TestR214S9,'test_'+_w.lower()+'_'+_kind,_case(_w,_kind))

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--test',action='store_true')
    group.add_argument('--emit',action='store_true')
    opts=ap.parse_args()
    if opts.test:
        unittest.main(argv=['r214_s9'],verbosity=2)
    else:
        print(json.dumps(generate(),indent=2))
