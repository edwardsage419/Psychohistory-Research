"""TH188 synthetic-only cultural transmission and homophily audit.

All worlds are constructed for exact mathematical checks. No personal or empirical data.
Run: python -m unittest -v th188_cultural_frequency_selection_audit.py
"""
from collections import Counter
from fractions import Fraction as F
from math import comb
import unittest


def majority_probability(p, n):
    """Probability of strict majority of successes in an odd, iid sample."""
    assert 0 <= p <= 1 and n > 0 and n % 2 == 1
    return sum((F(comb(n, k)) * p**k * (1-p)**(n-k)
                for k in range(n // 2 + 1, n + 1)), F(0))


def mixture_probability(p, n, conformist_weight):
    """Artificial mixture of strict-majority and frequency-proportional copying."""
    assert 0 <= conformist_weight <= 1
    return conformist_weight * majority_probability(p, n) + (1-conformist_weight)*p


def observed_joint(world):
    """Two observationally equivalent, artificially defined causal worlds."""
    assert world in ("common_cause", "copying")
    outcomes = Counter()
    for latent in (0, 1):
        a = latent
        b = latent if world == "common_cause" else a
        outcomes[(a, b)] += F(1, 2)
    return outcomes


def interventional_effect(world):
    """E[B|do(A=1)] minus E[B|do(A=0)] in each synthetic world."""
    assert world in ("common_cause", "copying")
    def mean_b(a_intervened):
        return sum((F(1, 2) * (latent if world == "common_cause" else a_intervened)
                    for latent in (0, 1)), F(0))
    return mean_b(1) - mean_b(0)


def within_group_agreement_no_learning():
    """All within-group edges agree when traits are selected, with no updating."""
    labels = (0, 0, 1, 1)
    undirected_edges = ((0, 1), (2, 3))
    return F(sum(labels[a] == labels[b] for a, b in undirected_edges), len(undirected_edges))


class TestTH188(unittest.TestCase):
    def test_majority_three_quarter(self):
        self.assertEqual(majority_probability(F(1, 4), 3), F(5, 32))

    def test_majority_three_three_quarters(self):
        self.assertEqual(majority_probability(F(3, 4), 3), F(27, 32))

    def test_majority_five_quarter(self):
        self.assertEqual(majority_probability(F(1, 4), 5), F(53, 512))

    def test_majority_five_three_quarters(self):
        self.assertEqual(majority_probability(F(3, 4), 5), F(459, 512))

    def test_majority_half(self):
        for n in (1, 3, 5, 7):
            self.assertEqual(majority_probability(F(1, 2), n), F(1, 2))

    def test_majority_endpoints(self):
        for n in (1, 3, 5):
            self.assertEqual(majority_probability(F(0), n), F(0))
            self.assertEqual(majority_probability(F(1), n), F(1))

    def test_majority_symmetry(self):
        for n in (1, 3, 5):
            for p in (F(1, 4), F(1, 3), F(2, 5)):
                self.assertEqual(majority_probability(p, n) + majority_probability(1-p, n), 1)

    def test_good_majority_amplified(self):
        self.assertGreater(majority_probability(F(3, 4), 3), F(3, 4))

    def test_bad_majority_amplified(self):
        self.assertLess(majority_probability(F(1, 4), 3), F(1, 4))

    def test_group_separation_three(self):
        self.assertEqual(majority_probability(F(3, 4), 3) - majority_probability(F(1, 4), 3), F(11, 16))

    def test_group_separation_five(self):
        self.assertEqual(majority_probability(F(3, 4), 5) - majority_probability(F(1, 4), 5), F(203, 256))

    def test_group_separation_increases(self):
        self.assertGreater(F(203, 256), F(11, 16))

    def test_mixed_frequency_response(self):
        self.assertEqual(mixture_probability(F(1, 4), 3, F(1, 2)), F(13, 64))

    def test_mixed_frequency_response_upper(self):
        self.assertEqual(mixture_probability(F(3, 4), 3, F(1, 2)), F(51, 64))

    def test_linear_copying_is_not_conformist_amplification(self):
        for p in (F(1, 4), F(1, 2), F(3, 4)):
            self.assertEqual(mixture_probability(p, 3, F(0)), p)

    def test_observational_equivalence(self):
        self.assertEqual(observed_joint("common_cause"), observed_joint("copying"))
        self.assertEqual(observed_joint("copying"), Counter({(0, 0): F(1, 2), (1, 1): F(1, 2)}))

    def test_intervention_difference(self):
        self.assertEqual(interventional_effect("common_cause"), 0)
        self.assertEqual(interventional_effect("copying"), 1)

    def test_selection_alone_creates_homogeneity(self):
        self.assertEqual(within_group_agreement_no_learning(), 1)


if __name__ == "__main__":
    unittest.main()
