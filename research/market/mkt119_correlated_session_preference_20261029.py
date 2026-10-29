#!/usr/bin/env python3
"""MKT119: exact synthetic repeated-pairwise preference with shared session noise.

All parameters are hypothetical. Python standard library only; no network,
personal data, API calls, or sampling. Output is a reproducible JSON receipt.
"""
from fractions import Fraction as Q
from itertools import product
import json

GOOD_PROB = Q(3, 4)
GOOD_ACCURACY = Q(9, 10)
MARGINAL_ACCURACY = GOOD_PROB * GOOD_ACCURACY + (1 - GOOD_PROB) * (1 - GOOD_ACCURACY)
CONFIDENCE = Q(19, 20)
DESIGNS = {
    'FOUR_IN_ONE_SESSION': (4,),
    'TWO_IN_EACH_OF_TWO_SESSIONS': (2, 2),
    'ONE_IN_EACH_OF_FOUR_SESSIONS': (1, 1, 1, 1),
}
CHECKS = 0


def check(condition, label):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise AssertionError(label)


def block_likelihood(block, truth):
    correct = sum(answer == truth for answer in block)
    wrong = len(block) - correct
    p = GOOD_ACCURACY
    return GOOD_PROB * p ** correct * (1 - p) ** wrong + (1 - GOOD_PROB) * (1 - p) ** correct * p ** wrong


def actual_likelihood(answers, truth, blocks):
    i, likelihood = 0, Q(1)
    for size in blocks:
        likelihood *= block_likelihood(answers[i:i + size], truth)
        i += size
    check(i == len(answers), 'blocks cover all answers')
    return likelihood


def naive_likelihood(answers, truth):
    k = sum(answer == truth for answer in answers)
    return MARGINAL_ACCURACY ** k * (1 - MARGINAL_ACCURACY) ** (len(answers) - k)


def exact(q):
    return {'fraction': str(q), 'decimal': round(float(q), 12)}


def evaluate(blocks):
    coverage = error_decided = bayes_error = naive_claimed_error = Q(0)
    exact_coverage = exact_decided_error = Q(0)
    all_same = None
    max_confidence_gap = Q(0)
    for answers in product((0, 1), repeat=sum(blocks)):
        actual = [actual_likelihood(answers, truth, blocks) for truth in (0, 1)]
        naive = [naive_likelihood(answers, truth) for truth in (0, 1)]
        mass = sum(actual) / 2
        check(mass > 0, 'positive outcome probability')
        true_post = actual[1] / sum(actual)
        naive_post = naive[1] / sum(naive)
        bayes_error += min(actual) / 2
        naive_claimed_error += min(naive) / 2
        if naive_post >= CONFIDENCE or naive_post <= 1 - CONFIDENCE:
            prediction = 1 if naive_post >= CONFIDENCE else 0
            coverage += mass
            error_decided += actual[1 - prediction] / 2
            gap = abs(true_post - naive_post)
            max_confidence_gap = max(max_confidence_gap, gap)
        if true_post >= CONFIDENCE or true_post <= 1 - CONFIDENCE:
            prediction = 1 if true_post >= CONFIDENCE else 0
            exact_coverage += mass
            exact_decided_error += actual[1 - prediction] / 2
        if answers == (1, 1, 1, 1):
            all_same = {'actual_posterior_h1': exact(true_post),
                        'naive_posterior_h1': exact(naive_post),
                        'actual_likelihood_h1': exact(actual[1]),
                        'actual_likelihood_h0': exact(actual[0])}
    for truth in (0, 1):
        check(sum(actual_likelihood(ans, truth, blocks)
                  for ans in product((0, 1), repeat=sum(blocks))) == 1,
              'likelihood normalizes')
    check(Q(0) <= error_decided <= coverage / 2, 'decided risk bounds')
    check(Q(0) <= exact_decided_error <= exact_coverage / 2, 'oracle risk bounds')
    check(Q(0) <= coverage <= 1, 'coverage bounds')
    check(all_same is not None, 'all-ones example')
    return {'blocks': list(blocks), 'true_bayes_error': exact(bayes_error),
            'naive_assumed_bayes_error': exact(naive_claimed_error),
            'naive_95pct_decision_coverage': exact(coverage),
            'true_error_among_naive_decisions': exact(error_decided / coverage if coverage else Q(0)),
            'true_95pct_decision_coverage': exact(exact_coverage),
            'true_error_among_true_model_decisions': exact(exact_decided_error / exact_coverage if exact_coverage else Q(0)),
            'max_posterior_gap_on_naive_confident_outcomes': exact(max_confidence_gap),
            'four_identical_positive_answers': all_same}


def main():
    check(MARGINAL_ACCURACY == Q(7, 10), 'marginal accuracy = 7/10')
    results = {name: evaluate(blocks) for name, blocks in DESIGNS.items()}
    shared = results['FOUR_IN_ONE_SESSION']['four_identical_positive_answers']
    independent = results['ONE_IN_EACH_OF_FOUR_SESSIONS']['four_identical_positive_answers']
    check(shared['actual_likelihood_h1']['fraction'] == '4921/10000', 'shared likelihood +')
    check(shared['actual_likelihood_h0']['fraction'] == '1641/10000', 'shared likelihood -')
    check(shared['actual_posterior_h1']['fraction'] == '4921/6562', 'shared posterior')
    check(shared['naive_posterior_h1']['fraction'] == '2401/2482', 'naive posterior')
    check(independent['actual_posterior_h1']['fraction'] == '2401/2482', 'independent sessions')
    check(results['FOUR_IN_ONE_SESSION']['naive_95pct_decision_coverage']['fraction'] != '0', 'naive confidence occurs')
    check(results['FOUR_IN_ONE_SESSION']['true_95pct_decision_coverage']['fraction'] == '0', 'shared session cannot reach 95%')
    check(results['ONE_IN_EACH_OF_FOUR_SESSIONS']['max_posterior_gap_on_naive_confident_outcomes']['fraction'] == '0', 'independent calibrated')
    print(json.dumps({'research_id': 'MKT119', 'evidence_scope': 'SYNTHETIC_MARKET_E1',
                      'assumptions': {'prior_each_hypothesis': '1/2',
                                      'shared_session_good_probability': '3/4',
                                      'good_accuracy': '9/10', 'bad_accuracy': '1/10',
                                      'marginal_accuracy': '7/10',
                                      'decision_threshold': '19/20',
                                      'answers': 4},
                      'results': results, 'assertions_passed': CHECKS, 'failures': 0},
                     indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
