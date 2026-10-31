"""TH190 synthetic two-state cultural chain: exact finite-sample audit.
No third-party data, dependencies, network access, or random sampling.
"""
from fractions import Fraction as F
from itertools import product
from unittest import TestCase, main

NEUTRAL = ((F(3, 4), F(1, 4)), (F(1, 4), F(3, 4)))
ATTRACTION = ((F(3, 4), F(1, 4)), (F(1, 8), F(7, 8)))

def path_probability(path, matrix):
    p = F(1)
    for left, right in zip(path, path[1:]):
        p *= matrix[left][right]
    return p

def paths(initial, steps):
    return [(initial, *suffix) for suffix in product((0, 1), repeat=steps)]

def tv_distance(initial, steps):
    return sum(abs(path_probability(p, NEUTRAL) - path_probability(p, ATTRACTION))
               for p in paths(initial, steps)) / 2

def event_all_ones(initial, steps, matrix):
    return path_probability((initial, *(1 for _ in range(steps))), matrix)

def exact_binomial_upper(n, k, p):
    from math import comb
    return sum(F(comb(n, j)) * p ** j * (1 - p) ** (n - j)
               for j in range(k, n + 1))

class ExactAudit(TestCase):
    def test_stochastic(self):
        for matrix in (NEUTRAL, ATTRACTION):
            for row in matrix:
                self.assertEqual(sum(row), 1)
                self.assertTrue(all(0 <= x <= 1 for x in row))

    def test_first_step_zero_identical(self):
        self.assertEqual(tv_distance(0, 1), 0)

    def test_first_step_one_differs(self):
        self.assertEqual(tv_distance(1, 1), F(1, 8))

    def test_second_step_zero_differs(self):
        self.assertEqual(tv_distance(0, 2), F(1, 32))

    def test_mass_conserved(self):
        for initial in (0, 1):
            for steps in range(7):
                for matrix in (NEUTRAL, ATTRACTION):
                    self.assertEqual(sum(path_probability(p, matrix)
                                         for p in paths(initial, steps)), 1)

    def test_no_perfect_separation(self):
        for initial in (0, 1):
            for steps in range(1, 7):
                self.assertLess(tv_distance(initial, steps), 1)

    def test_longer_chain_more_distinguishable(self):
        for initial in (0, 1):
            distances = [tv_distance(initial, steps) for steps in range(1, 7)]
            self.assertEqual(distances, sorted(distances))

    def test_all_ones_four(self):
        self.assertEqual(event_all_ones(1, 4, NEUTRAL), F(81, 256))
        self.assertEqual(event_all_ones(1, 4, ATTRACTION), F(2401, 4096))

    def test_all_ones_four_not_rare_under_neutral(self):
        self.assertGreater(event_all_ones(1, 4, NEUTRAL), F(1, 20))

    def test_one_step_binomial_tail(self):
        self.assertEqual(exact_binomial_upper(4, 4, F(3, 4)), F(81, 256))

    def test_identical_kernel_two_mechanisms(self):
        # Model A: copy with 3/4, otherwise flip; model B: copy with
        # 1/2, otherwise draw a fair coin. Both yield P(match)=3/4.
        for parent in (0, 1):
            for child in (0, 1):
                a = F(3, 4) if child == parent else F(1, 4)
                b = F(1, 2) * int(child == parent) + F(1, 2) * F(1, 2)
                self.assertEqual(a, b)
                self.assertEqual(a, NEUTRAL[parent][child])

    def test_heterogeneous_start_effect(self):
        self.assertEqual(ATTRACTION[0], NEUTRAL[0])
        self.assertNotEqual(ATTRACTION[1], NEUTRAL[1])

    def test_perturbation_vs_observation(self):
        # Identifying parent=1 transition needs actual or randomized
        # exposure to that parent state; parent=0 only cannot do it.
        self.assertEqual(NEUTRAL[0][1], ATTRACTION[0][1])
        self.assertEqual(ATTRACTION[1][1] - NEUTRAL[1][1], F(1, 8))

if __name__ == '__main__':
    main(verbosity=2)
