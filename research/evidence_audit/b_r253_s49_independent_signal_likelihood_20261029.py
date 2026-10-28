#!/usr/bin/env python3
"""Independent R253 S49 exact 32-signal-state oracle. E1 artificial only.

Run: python b_r253_s49_independent_signal_likelihood_20261029.py
No packages, network, credentials or paid services required.
"""
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F

WORLDS = (
    'BAYESIAN_CASCADE_Q34', 'PRIVATE_ONLY_Q34', 'FIRST_ACTION_IMITATION_Q34',
    'BAYESIAN_CASCADE_FAIR_Q12', 'HARD_CODED_CASCADE_ALIAS_Q34',
    'INVERTED_SIGNALS_Q14_BAYES', 'PERFECT_PRIVATE_Q1',
    'STATIC_TRUE_PRIVATE_CASCADE_REPORT_ALIAS_Q34', 'COMMON_SIGNAL_NO_SOCIAL_Q34'
)

def actions(w, signals):
    s = tuple(signals)
    if w in ('PRIVATE_ONLY_Q34', 'BAYESIAN_CASCADE_FAIR_Q12'):
        return s
    if w in ('FIRST_ACTION_IMITATION_Q34', 'COMMON_SIGNAL_NO_SOCIAL_Q34'):
        return (s[0],) * 4
    if w == 'INVERTED_SIGNALS_Q14_BAYES':
        s = tuple(1 - x for x in s)
    return (s[0], s[1], s[0], s[0]) if s[0] == s[1] else s

def oracle(w):
    q = F(1, 2) if w == 'BAYESIAN_CASCADE_FAIR_Q12' else (
        F(1, 4) if w == 'INVERTED_SIGNALS_Q14_BAYES' else (
        F(1) if w == 'PERFECT_PRIVATE_Q1' else F(3, 4)))
    atoms = []
    for theta in (0, 1):
        for signals in itertools.product((0, 1), repeat=4):
            p = F(1, 2)
            for s in signals:
                p *= q if s == theta else 1 - q
            if p:
                atoms.append((theta, actions(w, signals), p))
    assert sum((p for _, _, p in atoms), F()) == 1
    risks = []
    for k in range(5):
        groups = defaultdict(lambda: [F(), F()])
        for theta, public, p in atoms:
            groups[public[:k]][theta] += p
        # Exact E[(theta-E[theta|prefix])^2] = sum mass0*mass1/(mass0+mass1).
        risk = sum((n0*n1/(n0+n1) for n0, n1 in groups.values() if n0+n1), F())
        risks.append(risk)
    gains = [risks[i] - risks[i+1] for i in range(4)]
    assert risks[0] == F(1, 4) and all(g >= 0 for g in gains)
    return {'world': w, 'risks': list(map(str, risks)), 'gains': list(map(str, gains)),
            'positive_theta_signal_states': len(atoms)}

def compare(actual, expected):
    if len(actual) != len(expected):
        raise AssertionError('world count mismatch')
    checks = 0
    for a, e in zip(actual, expected):
        assert a['world'] == e['world'], 'world mismatch'
        for key, n in (('risks', 5), ('gains', 4)):
            assert len(a[key]) == len(e[key]) == n
            for x, y in zip(a[key], e[key]):
                assert F(x) == F(y), (a['world'], key, x, y)
                checks += 1
    return checks

def main():
    result = [oracle(w) for w in WORLDS]
    alias = [result[i]['risks'] for i in (0, 4, 7)]
    assert alias[0] == alias[1] == alias[2]
    assert result[2]['risks'] == result[8]['risks']
    assert result[3]['risks'] == ['1/4'] * 5
    assert result[6]['risks'] == ['1/4', '0', '0', '0', '0']
    # Frozen source-route values are a read-only external comparator.
    expected = [
      ('1/4','3/16','3/20','81/640','9/80'),
      ('1/4','3/16','3/20','27/224','81/820'),
      ('1/4','3/16','3/16','3/16','3/16'),
      ('1/4','1/4','1/4','1/4','1/4'),
      ('1/4','3/16','3/20','81/640','9/80'),
      ('1/4','3/16','3/20','81/640','9/80'),
      ('1/4','0','0','0','0'),
      ('1/4','3/16','3/20','81/640','9/80'),
      ('1/4','3/16','3/16','3/16','3/16'),
    ]
    reference = [{'world': w, 'risks': list(e),
                  'gains': [str(F(e[i])-F(e[i+1])) for i in range(4)]}
                 for w, e in zip(WORLDS, expected)]
    checks = compare(result, reference)
    corrupt = json.loads(json.dumps(reference))
    corrupt[0]['risks'][2] = '999'
    rejected = False
    try:
        compare(result, corrupt)
    except AssertionError:
        rejected = True
    assert rejected, 'mutation not rejected'
    output = {'research': 'R253_S49', 'method': 'independent_theta_x_16_signal_product',
              'evidence': 'E1_ONLY', 'worlds': 9, 'risk_cells': 45, 'gain_cells': 36,
              'cross_method_exact_checks': checks, 'failures': 0,
              'mutation_rejected': rejected, 'world_results': result}
    print(json.dumps(output, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
