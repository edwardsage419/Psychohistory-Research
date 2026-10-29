#!/usr/bin/env python3
"""MKT120 synthetic exact audit: shared latent noise, preference drift, stopping.
No network access, personal data, or third-party packages. Python 3.10+.
"""
import json
from collections import defaultdict
from fractions import Fraction as F
from itertools import product

QUALITIES = ((F(3, 4), F(9, 10)), (F(1, 4), F(1, 10)))
CHECKS = 0


def check(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(message)


def likelihood(bits, initial, p_correct, flip):
    p = F(1)
    for t, observed in enumerate(bits):
        truth = initial ^ (flip and t >= 2)
        p *= p_correct if observed == truth else 1 - p_correct
    return p


def conditional(bits, final, model):
    if model == 'naive':
        matches = sum(x == final for x in bits)
        return F(7, 10) ** matches * F(3, 10) ** (len(bits) - matches)
    total = F(0)
    for q_prior, q_correct in QUALITIES:
        for flip in ((0, 1) if model == 'drift' else (0,)):
            flip_prior = (F(1, 4) if flip else F(3, 4)) if model == 'drift' else F(1)
            total += q_prior * flip_prior * likelihood(bits, final ^ flip, q_correct, flip)
    return total


def posterior(bits, model):
    a, b = conditional(bits, 1, model), conditional(bits, 0, model)
    return a / (a + b)


def population():
    rows = []
    for bits in product((0, 1), repeat=4):
        for initial in (0, 1):
            for prior, p_correct in QUALITIES:
                for flip in (0, 1):
                    p = F(1, 2) * prior * (F(1, 4) if flip else F(3, 4))
                    rows.append((bits, initial ^ flip, p * likelihood(bits, initial, p_correct, flip)))
    return rows


def policy(bits, model, threshold, adaptive):
    for t in ((2, 4) if adaptive else (4,)):
        p = posterior(bits[:t], model)
        if max(p, 1-p) >= threshold:
            return int(p > F(1, 2)), t
    return None, 4


def evaluate(rows, model, threshold, adaptive):
    stats = defaultdict(F)
    for bits, final, mass in rows:
        action, n_queries = policy(bits, model, threshold, adaptive)
        stats['queries'] += mass * n_queries
        if action is not None:
            stats['coverage'] += mass
            stats['error'] += mass * (action != final)
            if n_queries == 2:
                stats['early'] += mass
    return {**{key: str(stats[key]) for key in ('coverage', 'error', 'early', 'queries')},
            'conditional_error': str(stats['error'] / stats['coverage']) if stats['coverage'] else None}


def main():
    rows = population()
    check(len(rows) == 128, '128 latent cases')
    check(sum((row[2] for row in rows), F(0)) == 1, 'total mass')
    for model in ('naive', 'shared', 'drift'):
        for bits in product((0, 1), repeat=4):
            p = posterior(bits, model)
            check(0 <= p <= 1, 'posterior bounds')
            check(p + posterior(tuple(1-x for x in bits), model) == 1, 'label symmetry')
        for final in (0, 1):
            check(sum((conditional(bits, final, model)
                       for bits in product((0, 1), repeat=4)), F(0)) == 1,
                  'likelihood normalization')
    expected = {
        ('naive', (1, 1)): F(49, 58),
        ('shared', (1, 1)): F(61, 82),
        ('drift', (1, 1)): F(51, 82),
        ('naive', (1, 1, 1, 1)): F(2401, 2482),
        ('shared', (1, 1, 1, 1)): F(4921, 6562),
        ('drift', (1, 1, 1, 1)): F(1237, 1654),
    }
    for (model, bits), value in expected.items():
        check(posterior(bits, model) == value, 'posterior anchor')
    naive_adaptive = evaluate(rows, 'naive', F(4, 5), True)
    naive_fixed = evaluate(rows, 'naive', F(9, 10), False)
    drift_fixed = evaluate(rows, 'drift', F(7, 10), False)
    shared_strict = evaluate(rows, 'shared', F(3, 4), False)
    for key, value in {'coverage': '2419/2500', 'error': '1739/5000',
                       'early': '41/50', 'queries': '59/25'}.items():
        check(naive_adaptive[key] == value, 'adaptive metric ' + key)
    for key, value in {'coverage': '2481/5000', 'error': '1251/10000'}.items():
        check(naive_fixed[key] == value, 'fixed metric ' + key)
    check(drift_fixed['coverage'] == '41/50', 'drift coverage')
    check(drift_fixed['error'] == '21/100', 'drift error')
    check(shared_strict['coverage'] == '0', 'shared abstention')
    check(evaluate(rows, 'drift', F(4, 5), True)['coverage'] == '0', 'drift abstention')
    check(posterior((1,1,1,1), 'naive') > posterior((1,1,1,1), 'shared'),
          'negative control: independence assumption')
    return {'checks': CHECKS, 'failures': 0, 'latent_cases': len(rows),
            'posteriors_unanimous': {model: str(posterior((1,1,1,1), model))
                                     for model in ('naive', 'shared', 'drift')},
            'naive_adaptive_80': naive_adaptive, 'naive_fixed_90': naive_fixed,
            'drift_aware_fixed_70': drift_fixed, 'shared_fixed_75': shared_strict,
            'evidence': 'synthetic_exact_E1_nonblind'}


if __name__ == '__main__':
    print(json.dumps(main(), ensure_ascii=False, indent=2))
