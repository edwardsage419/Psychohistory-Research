#!/usr/bin/env python3
"""R229 S25 independent Bernoulli analytic check of enumeration receipt."""
import json
import sys
from fractions import Fraction as F

SCENARIOS = [(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (0, 1)]


def bernoulli(theta, difficulty):
    k = theta - difficulty
    if k >= 0:
        return F(2 ** k, 2 ** k + 1)
    return F(1, 1 + 2 ** (-k))


def analytic(theta, drift):
    a = bernoulli(theta, 0)
    b = bernoulli(theta, 1 + drift)
    p10 = a * (1 - b)
    p01 = (1 - a) * b
    total = p10 + p01
    q = p10 / total
    return {
        'p10': p10, 'p01': p01, 'p_r1': total,
        'q10_given_r1': q, 'conditional_odds': p10 / p01,
        'conditional_fisher_coeff': q * (1 - q),
        'expected_fisher_coeff': p10 * p01 / total,
        'joint_mass': F(1), 'single_item_conditional_fisher_coeff': F(0),
    }


def audit(data):
    assert data['research_id'] == 'R229_S25'
    assert data['evidence'] == 'E1_ARTIFICIAL'
    assert data['total_joint_states'] == 12288
    assert len(data['scenarios']) == 6
    checks = 4
    for observed, (theta, drift) in zip(data['scenarios'], SCENARIOS):
        assert (observed['theta'], observed['bridge_item2_drift']) == (theta, drift)
        checks += 1
        for key, expected in analytic(theta, drift).items():
            assert F(observed[key]) == expected, (theta, drift, key)
            checks += 1
        for key, expected in [('source_states', 2048), ('positive_source_states', 2048),
                              ('distinct_observed_keys', 128), ('original_observed_keys', 32)]:
            assert observed[key] == expected, (theta, drift, key)
            checks += 1
        assert observed['original_observed_marginal_unchanged'] is True
        checks += 1
    assert data['R073'] == 'FROZEN' and data['PESEN_v0_1'] == 'FROZEN'
    checks += 1
    assert data['new_E2'] == data['new_E3'] == 0
    checks += 1
    return checks


if __name__ == '__main__':
    source = sys.argv[1] if len(sys.argv) > 1 else 'research/validation/R229_S25_COMMON_ITEM_BRIDGE_EXACT_RECEIPT_2026-10-28.json'
    with open(source, encoding='utf-8') as f:
        data = json.load(f)
    count = audit(data)
    corrupted = json.loads(json.dumps(data))
    corrupted['scenarios'][2]['conditional_odds'] = '999'
    try:
        audit(corrupted)
    except AssertionError:
        negative_control = 'DETECTED'
    else:
        raise AssertionError('mutation negative control was not detected')
    print(json.dumps({
        'research_id': 'R229_S25', 'checks_passed': count,
        'checks_failed': 0, 'mutation_negative_control': negative_control,
        'method': 'analytic Bernoulli probabilities and Fisher information; no original 512 source enumeration',
        'evidence': 'E1_ARTIFICIAL'
    }, sort_keys=True, indent=2))
