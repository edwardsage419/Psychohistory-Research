#!/usr/bin/env python3
"""R290 S86: exact artificial finite likelihood training, heldout risk.
Run: python r290_s86_finite_likelihood.py --test | --emit
No external dependencies, no changes to original R290 files.
"""
import argparse
import itertools
import json
import unittest
from collections import Counter
from fractions import Fraction as F

DGP = {
    'MONOTONE': ((8, 6, 4, 2, 1), (1, 2, 4, 6, 8), 21),
    'CENTERED': ((8, 2, 1, 2, 8), (1, 3, 13, 3, 1), 21),
    'IDENTICAL': ((1, 2, 3, 2, 1), (1, 2, 3, 2, 1), 9),
}
PRIOR = (F(1, 2), F(3, 4))
COSTS = ((1, 1), (1, 3))
FREEZE = '90998f553dcc2697fdbf61a6355b9b4ffc3e5e95'


def distributions(name):
    n, s, d = DGP[name]
    return tuple(F(v, d) for v in n), tuple(F(v, d) for v in s)


def heldout_risk(n, s, pi, fp, fn, rule):
    return (1-pi)*fp*sum((n[x] for x in range(5) if rule[x]), F(0)) + pi*fn*sum((s[x] for x in range(5) if not rule[x]), F(0))


def trained_rule(noise_train, signal_train, pi, fp, fn):
    cn, cs = Counter(noise_train), Counter(signal_train)
    # Equal labeled sample sizes, so both smoothing denominators cancel.
    return tuple(int(pi*fn*(cs[x]+1) > (1-pi)*fp*(cn[x]+1)) for x in range(5))


def source_rows(name, m):
    n, s = distributions(name)
    for sequence in itertools.product(range(5), repeat=2*m):
        a, b = sequence[:m], sequence[m:]
        mass = F(1)
        for x in a:
            mass *= n[x]
        for x in b:
            mass *= s[x]
        yield a, b, mass


def world(name, pi, fp, fn, m):
    n, s = distributions(name)
    oracle = tuple(int(pi*fn*s[x] > (1-pi)*fp*n[x]) for x in range(5))
    oracle_risk = heldout_risk(n, s, pi, fp, fn, oracle)
    cutoffs = [(heldout_risk(n, s, pi, fp, fn, tuple(int(x >= t) for x in range(5))), t) for t in range(6)]
    cutoff_risk, cutoff_t = min(cutoffs)
    fixed_t3 = next(v for v, t in cutoffs if t == 3)
    const = min((1-pi)*fp, pi*fn)
    total_mass, total_risk, sources = F(0), F(0), 0
    for a, b, mass in source_rows(name, m):
        rule = trained_rule(a, b, pi, fp, fn)
        total_mass += mass
        total_risk += mass * heldout_risk(n, s, pi, fp, fn, rule)
        sources += 1
    if sources != 5**(2*m) or total_mass != 1 or total_risk < oracle_risk:
        raise AssertionError('source coverage, probability mass, or oracle bound failed')
    return dict(world=f'{name}_PI{pi.numerator}of{pi.denominator}_FP{fp}_FN{fn}', m=m,
                sources=sources, training_mass=str(total_mass), expected_heldout_risk=str(total_risk),
                oracle_risk=str(oracle_risk), regret=str(total_risk-oracle_risk),
                best_fixed_cutoff_risk=str(cutoff_risk), best_fixed_cutoff_t=cutoff_t,
                fixed_t3_risk=str(fixed_t3), best_constant_risk=str(const))


def emit():
    rows = [world(name, pi, fp, fn, m) for name in DGP for pi in PRIOR for fp, fn in COSTS for m in (1, 2)]
    return dict(research_id='R290_S86', prescore_commit=FREEZE, evidence='E1_ARTIFICIAL_ONLY',
                original_R290_unchanged=True, R073='FROZEN', PESEN='FROZEN',
                new_E2=0, new_E3=0, worlds=12, results=rows)


class Checks(unittest.TestCase):
    def test_sources(self):
        for name in DGP:
            for m in (1, 2):
                rows = list(source_rows(name, m))
                self.assertEqual(len(rows), 5**(2*m))
                self.assertEqual(sum((p for _, _, p in rows), F(0)), 1)
    def test_worlds(self):
        result = emit()
        self.assertEqual(len(result['results']), 24)
        for row in result['results']:
            self.assertGreaterEqual(F(row['regret']), 0)
            self.assertEqual(row['training_mass'], '1')
    def test_tie_negative(self):
        self.assertEqual(trained_rule((0,), (0,), F(1,2), 1, 1)[0], 0)
    def test_negative_controls(self):
        a = list(source_rows('MONOTONE', 1))
        self.assertNotEqual(sum((v[2] for v in a[:-1]), F(0)), 1)
        self.assertNotEqual(sum((v[2] for v in a + a[:1]), F(0)), 1)
        self.assertNotEqual(sum((v[2] for v in a[:-1] + [(a[-1][0],a[-1][1],a[-1][2]/2)]), F(0)), 1)
        self.assertNotEqual(trained_rule((0,), (4,), F(1,2), 1, 1), trained_rule((4,), (0,), F(1,2), 1, 1))
        self.assertEqual(emit()['evidence'], 'E1_ARTIFICIAL_ONLY')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument('--test', action='store_true')
    g.add_argument('--emit', action='store_true')
    args = parser.parse_args()
    if args.test:
        unittest.main(argv=['r290s86'], verbosity=2)
    else:
        print(json.dumps(emit(), indent=2, ensure_ascii=False))
