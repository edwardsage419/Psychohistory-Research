#!/usr/bin/env python3
"""R229 S25: exact enumeration of disconnected Rasch world plus a bridge."""
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F

THETA = (-1, 0, 1)
DIFFICULTY = (-1, 0, 1)
MASK = ((1, 1, 0), (1, 1, 0), (0, 0, 1))
SCENARIOS = [(-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0), (0, 1)]


def prob(theta, difficulty):
    k = theta - difficulty
    odds = F(2 ** k) if k >= 0 else F(1, 2 ** (-k))
    return odds / (1 + odds)


def mass(bits, probs):
    out = F(1)
    for bit, p in zip(bits, probs):
        out *= p if bit else 1 - p
    return out


def f(x):
    return str(x.numerator) if x.denominator == 1 else f'{x.numerator}/{x.denominator}'


def run():
    ps = [prob(THETA[i], DIFFICULTY[j]) for i in range(3) for j in range(3)]
    original = []
    for bits in itertools.product((0, 1), repeat=9):
        p = mass(bits, ps)
        visible = tuple(bits[3*i+j] for i in range(3) for j in range(3) if MASK[i][j])
        original.append((visible, p))
    assert len(original) == 512
    assert sum((p for _, p in original), F(0)) == 1
    base_obs = defaultdict(F)
    for visible, p in original:
        base_obs[visible] += p
    assert len(base_obs) == 32
    out = []
    for theta, drift in SCENARIOS:
        bridge_ps = (prob(theta, DIFFICULTY[1]), prob(theta, DIFFICULTY[2] + drift))
        joint_total = F(0)
        visible_joint = defaultdict(F)
        bridge_patterns = defaultdict(F)
        original_marginal = defaultdict(F)
        states = 0
        for visible, po in original:
            for bridge in itertools.product((0, 1), repeat=2):
                p = po * mass(bridge, bridge_ps)
                joint_total += p
                visible_joint[(visible, bridge)] += p
                bridge_patterns[bridge] += p
                original_marginal[visible] += p
                states += 1
        assert states == 2048 and joint_total == 1
        assert len(visible_joint) == 128
        assert original_marginal == base_obs
        r1 = bridge_patterns[(1, 0)] + bridge_patterns[(0, 1)]
        q = bridge_patterns[(1, 0)] / r1
        ratio = bridge_patterns[(1, 0)] / bridge_patterns[(0, 1)]
        info_cond = q * (1 - q)
        info_expected = r1 * info_cond
        assert ratio == (F(4) if drift else F(2))
        assert sum(bridge_patterns.values(), F(0)) == 1
        out.append({
            'theta': theta, 'bridge_item2_drift': drift, 'source_states': states,
            'positive_source_states': states, 'distinct_observed_keys': len(visible_joint),
            'original_observed_keys': len(base_obs), 'joint_mass': f(joint_total),
            'p10': f(bridge_patterns[(1, 0)]), 'p01': f(bridge_patterns[(0, 1)]),
            'p_r1': f(r1), 'q10_given_r1': f(q), 'conditional_odds': f(ratio),
            'conditional_fisher_coeff': f(info_cond), 'expected_fisher_coeff': f(info_expected),
            'single_item_conditional_fisher_coeff': '0',
            'original_observed_marginal_unchanged': True,
        })
    return {
        'research_id': 'R229_S25', 'evidence': 'E1_ARTIFICIAL',
        'method': 'exact 512 original structural matrices x 4 bridge response states',
        'original_world': 'DISCONNECTED_ITEM3',
        'original_source_states_per_scenario': 512,
        'scenarios': out, 'total_joint_states': sum(s['source_states'] for s in out),
        'R073': 'FROZEN', 'PESEN_v0_1': 'FROZEN', 'new_E2': 0, 'new_E3': 0,
    }


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, indent=2, sort_keys=True))
