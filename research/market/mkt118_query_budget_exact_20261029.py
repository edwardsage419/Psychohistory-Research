#!/usr/bin/env python3
"""MKT118: exact finite-query preference-identification risk, synthetic only.
Python standard library; no personal data, network, API or random draws.
"""
from fractions import Fraction as Q
from itertools import product
import json

QUERIES = ((0, 0), (1, 1), (0, 1), (1, 0))
DESIGNS = {
    'ALIGNED': (QUERIES[0], QUERIES[1], QUERIES[0], QUERIES[1]),
    'CROSS': tuple(QUERIES),
    'REPEAT_ONE_CONTEXT': (QUERIES[2],) * 4,
    'STRATIFIED_CROSS': (QUERIES[2], QUERIES[3]) * 2,
}
THRESHOLD = Q(19, 20)


def prob_a(model, query, failure=False):
    t, c = query
    if failure and query == (0, 1):
        return Q(1, 2)  # Synthetic context-specific non-informative feedback
    bit = t if model == 'TIME' else c
    return Q(9, 10) if bit == 0 else Q(1, 10)


def outcome_likelihood(model, design, outcome, failure=False):
    p = Q(1)
    for query, ans in zip(design, outcome):
        q = prob_a(model, query, failure)
        p *= q if ans else 1 - q
    return p


def evaluate(design, failure=False):
    assert len(design) == 4
    error = Q(0)
    abstain = Q(0)
    error_when_decided = Q(0)
    total = Q(0)
    checks = 0
    for bits in product((0, 1), repeat=4):
        t = outcome_likelihood('TIME', design, bits, failure)
        c = outcome_likelihood('CONTEXT', design, bits, failure)
        assert t >= 0 and c >= 0
        mass = (t + c) / 2
        total += mass
        error += min(t, c) / 2
        if max(t, c) * 20 < (t + c) * 19:
            abstain += mass
        else:
            error_when_decided += min(t, c) / 2
        checks += 1
    assert total == 1
    assert error <= Q(1, 2)
    assert 0 <= error_when_decided <= error
    assert 0 <= abstain <= 1
    return {'bayes_error': error, 'abstain_probability': abstain,
            'decided_error_unconditional': error_when_decided,
            'checks': checks}


def fmt(q):
    return {'exact': str(q), 'decimal': round(float(q), 9)}


def main():
    results = {}
    checks = 0
    for condition, failure in [('BASELINE', False), ('ONE_CONTEXT_UNINFORMATIVE', True)]:
        results[condition] = {}
        for name, design in DESIGNS.items():
            r = evaluate(design, failure)
            checks += r.pop('checks')
            results[condition][name] = {k: fmt(v) for k, v in r.items()}
        random_aggregate = {'bayes_error': Q(0), 'abstain_probability': Q(0),
                            'decided_error_unconditional': Q(0)}
        for design in product(QUERIES, repeat=4):
            r = evaluate(design, failure)
            checks += r.pop('checks')
            for k in random_aggregate:
                random_aggregate[k] += r[k] / 256
        results[condition]['UNIFORM_RANDOM_WITH_REPLACEMENT'] = {
            k: fmt(v) for k, v in random_aggregate.items()}
    assert results['BASELINE']['ALIGNED']['bayes_error']['exact'] == '1/2'
    assert results['BASELINE']['CROSS']['bayes_error']['exact'] == '1/10'
    assert results['BASELINE']['REPEAT_ONE_CONTEXT']['bayes_error']['exact'] == '7/250'
    assert results['BASELINE']['STRATIFIED_CROSS']['bayes_error']['exact'] == '7/250'
    assert results['ONE_CONTEXT_UNINFORMATIVE']['REPEAT_ONE_CONTEXT']['bayes_error']['exact'] == '1/2'
    assert results['ONE_CONTEXT_UNINFORMATIVE']['STRATIFIED_CROSS']['bayes_error']['exact'] == '1/10'
    checks += 6
    print(json.dumps({'research_id':'MKT118','scope':'SYNTHETIC_E1',
      'queries_per_design':4,'hypotheses':['TIME','CONTEXT'],
      'prior':'1/2 each','threshold':'19/20',
      'random_designs_enumerated_per_condition':256,
      'assertions_passed':checks,'failures':0,'results':results},
      indent=2,ensure_ascii=False))


if __name__ == '__main__':
    main()
