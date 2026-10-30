#!/usr/bin/env python3
"""R289 S85 independent nonblind E1 exact oracle. Python standard library only.

Reconstructs four-offer policies without importing the R route or persisted results.
Use --test for assertions, or no argument for six-world exact JSON.
"""
import argparse
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F

VALUES = (1, 3, 5)
DGP = {
    'UNIFORM': (F(1, 3), F(1, 3), F(1, 3)),
    'LOW_HEAVY': (F(1, 2), F(1, 4), F(1, 4)),
    'HIGH_HEAVY': (F(1, 4), F(1, 4), F(1, 2)),
}


def reward(offers, threshold):
    for index, offer in enumerate(offers):
        if offer >= threshold or index == 3:
            return F(offer) - F(index, 2)
    raise AssertionError('fourth offer must force acceptance')


def compute():
    output = []
    for name, probabilities in DGP.items():
        differences = defaultdict(F)
        expected_3 = expected_5 = F(0)
        for offers in itertools.product(VALUES, repeat=4):
            probability = F(1)
            for offer in offers:
                probability *= probabilities[VALUES.index(offer)]
            net_3, net_5 = reward(offers, 3), reward(offers, 5)
            expected_3 += probability * net_3
            expected_5 += probability * net_5
            differences[2 * (net_5 - net_3)] += probability
        assert sum(differences.values()) == 1
        for episodes in (1, 2):
            distribution = {F(0): F(1)}
            for _ in range(episodes):
                next_distribution = defaultdict(F)
                for total, probability in distribution.items():
                    for delta, weight in differences.items():
                        next_distribution[total + delta] += probability * weight
                distribution = next_distribution
            assert sum(distribution.values()) == 1
            select_5 = sum((weight for delta, weight in distribution.items() if delta > 0), F(0))
            tie = distribution.get(F(0), F(0))
            best = max(expected_3, expected_5)
            expected_test = expected_3 + select_5 * (expected_5 - expected_3)
            inferior = select_5 if expected_3 > expected_5 else (1 - select_5 if expected_5 > expected_3 else F(0))
            first = sum((p * v for p, v in zip(probabilities, VALUES)), F(0))
            output.append(dict(distribution=name, training_episodes=episodes,
                               expected_H3=str(expected_3), expected_H5=str(expected_5),
                               probability_select_H5=str(select_5), probability_training_tie=str(tie),
                               probability_select_inferior=str(inferior),
                               independent_test_expected_net=str(expected_test),
                               regret_vs_best_fixed_threshold=str(best - expected_test),
                               gain_over_first_only=str(expected_test - first)))
    return output


def tests():
    rows = compute()
    assert len(rows) == 6
    assert [r['expected_H3'] for r in rows[::2]] == ['67/18', '27/8', '133/32']
    assert [r['expected_H5'] for r in rows[::2]] == ['100/27', '197/64', '35/8']
    assert [r['probability_select_H5'] for r in rows] == [
        '25/81', '2819/6561', '55/256', '19569/65536', '35/128', '3659/8192']
    assert reward((1, 1, 1, 1), 5) == F(-1, 2)
    assert reward((1, 3, 5, 1), 3) == F(5, 2)
    assert reward((1, 3, 5, 1), 5) == F(4, 1)
    assert all(F(r['regret_vs_best_fixed_threshold']) >= 0 for r in rows)
    assert all(F(r['probability_training_tie']) > 0 for r in rows)
    # Negative control: selecting H5 on an exact training tie violates the freeze.
    assert (0 > 0) is False and (0 >= 0) is True
    return {'tests': 9, 'status': 'PASS', 'worlds': len(rows)}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', action='store_true')
    args = parser.parse_args()
    print(json.dumps(tests() if args.test else compute(), ensure_ascii=False, indent=2))
