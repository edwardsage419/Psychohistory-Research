#!/usr/bin/env python3
"""MKT129 exact two-stratum off-policy evaluation oracle, synthetic only.

Python 3 standard library. Each of two fixed strata contributes one independently
logged binary action. The target policy always selects B. All outcomes are
enumerated with rational arithmetic; reward models are frozen, not fitted.
"""
from fractions import Fraction as F
from itertools import product
import json

P = (F(1, 2), F(1, 100))
REWARDS = (F(0), F(1))
GOOD_MODEL = (F(0), F(1))
BAD_MODEL = (F(0), F(3, 4))
WRONG_PSCORE = (F(1, 2), F(1, 50))


def validate(p, q, rewards, model):
    if any(len(x) != 2 for x in (p, q, rewards, model)):
        raise ValueError('exactly two strata required')
    if any(type(v) is not F for seq in (p, q, rewards, model) for v in seq):
        raise ValueError('Fraction required, booleans and floats rejected')
    if any(v <= 0 or v > 1 for seq in (p, q) for v in seq):
        raise ValueError('positive action overlap required')
    if any(v < 0 or v > 1 for seq in (rewards, model) for v in seq):
        raise ValueError('reward and model in [0,1]')


def evaluate(p=P, q=P, rewards=REWARDS, model=BAD_MODEL):
    validate(p, q, rewards, model)
    rows = []
    for b in product((0, 1), repeat=2):
        prob = F(1)
        for i in range(2):
            prob *= p[i] if b[i] else 1 - p[i]
        ipw = sum((F(b[i]) * rewards[i] / q[i] for i in range(2)), F(0)) / 2
        dm = sum(model, F(0)) / 2
        dr = sum((model[i] + F(b[i]) * (rewards[i] - model[i]) / q[i]
                  for i in range(2)), F(0)) / 2
        numerator = sum((F(b[i]) * rewards[i] / q[i] for i in range(2)), F(0))
        denominator = sum((F(b[i]) / q[i] for i in range(2)), F(0))
        snipw = numerator / denominator if denominator else None
        rows.append({'bits': ''.join(map(str, b)), 'prob': prob,
                     'IPW': ipw, 'DM': dm, 'DR': dr, 'SNIPW': snipw})
    assert sum((r['prob'] for r in rows), F(0)) == 1
    target = sum(rewards, F(0)) / 2
    def stats(key):
        mean = sum((r['prob'] * r[key] for r in rows), F(0))
        var = sum((r['prob'] * (r[key] - mean)**2 for r in rows), F(0))
        return {'mean': mean, 'variance': var, 'bias': mean - target}
    covered = sum((r['prob'] for r in rows if r['SNIPW'] is not None), F(0))
    snipw_cond = (sum((r['prob'] * r['SNIPW'] for r in rows
                       if r['SNIPW'] is not None), F(0)) / covered
                  if covered else None)
    return {'target': target, 'IPW': stats('IPW'), 'DM': stats('DM'),
            'DR': stats('DR'), 'SNIPW_coverage': covered,
            'SNIPW_conditional_mean': snipw_cond, 'rows': rows}


def main():
    checks = 0
    def eq(actual, expected, label):
        nonlocal checks
        assert actual == expected, f'{label}: {actual} != {expected}'
        checks += 1
    baseline = evaluate()
    eq(baseline['target'], F(1, 2), 'target')
    eq(baseline['IPW']['mean'], F(1, 2), 'IPW unbiased')
    eq(baseline['IPW']['variance'], F(99, 4), 'IPW variance')
    eq(baseline['DM']['mean'], F(3, 8), 'bad DM')
    eq(baseline['DR']['mean'], F(1, 2), 'DR correct propensity')
    eq(baseline['DR']['variance'], F(99, 64), 'DR variance')
    eq(baseline['SNIPW_coverage'], F(101, 200), 'SNIPW coverage')
    eq(baseline['SNIPW_conditional_mean'], F(1, 51), 'SNIPW selection bias')
    eq(len(baseline['rows']), 4, 'complete action outcomes')
    correct_model_wrong_pscore = evaluate(q=WRONG_PSCORE, model=GOOD_MODEL)
    eq(correct_model_wrong_pscore['DR']['mean'], F(1, 2), 'correct model rescues DR')
    eq(correct_model_wrong_pscore['DR']['variance'], F(0), 'deterministic reward exact model')
    both_wrong = evaluate(q=WRONG_PSCORE, model=BAD_MODEL)
    eq(both_wrong['DR']['mean'], F(7, 16), 'both nuisance models wrong')
    eq(both_wrong['DR']['bias'], -F(1, 16), 'both wrong bias')
    eq(both_wrong['IPW']['mean'], F(1, 4), 'wrong propensity IPW bias')
    eq(both_wrong['SNIPW_coverage'], F(101, 200), 'coverage depends on true logging')
    constant = evaluate(rewards=(F(1), F(1)), model=(F(3,4), F(3,4)))
    eq(constant['SNIPW_conditional_mean'], F(1), 'constant reward control')
    bad_inputs = [
        {'q': (F(1,2), F(0))},
        {'q': (F(1,2), F(2))},
        {'model': (F(0), True)},
        {'rewards': (F(0), F(1), F(1))},
    ]
    rejected = 0
    for kwargs in bad_inputs:
        try:
            evaluate(**kwargs)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError(f'bad input accepted: {kwargs}')
    eq(rejected, len(bad_inputs), 'invalid controls')
    def render(obj):
        if isinstance(obj, F):
            return str(obj)
        if isinstance(obj, dict):
            return {k: render(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [render(v) for v in obj]
        return obj
    print(json.dumps(render({
        'status': 'PASS', 'assertions': checks, 'negative_controls_rejected': rejected,
        'world': 'two synthetic fixed strata, two logged actions each',
        'baseline': {k:v for k,v in baseline.items() if k != 'rows'},
        'correct_model_wrong_pscore': {k:v for k,v in correct_model_wrong_pscore.items() if k != 'rows'},
        'both_wrong': {k:v for k,v in both_wrong.items() if k != 'rows'},
        'constant_reward_SNIPW_conditional_mean': constant['SNIPW_conditional_mean'],
    }), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
