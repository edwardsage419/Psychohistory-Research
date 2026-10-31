"""TH187 synthetic finite-population conditional randomization audit.

No personal, empirical, or restricted data. Python standard library only.
All probability statements are finite exact Fractions.
"""
from fractions import Fraction as F
from itertools import combinations, product
import unittest

CANDIDATES = (4, 5, 6, 7)
FOCALS = (0, 1, 2, 3)
WEIGHTS = (8, 4, 2, 1)
FIXED = tuple(combinations(CANDIDATES, 2))
BERNOULLI = tuple(tuple(CANDIDATES[i] for i, b in enumerate(bits) if b)
                  for bits in product((0, 1), repeat=4))


def statistic(assignment, weights=WEIGHTS):
    """A predeclared synthetic statistic on untreated focal outcomes."""
    return sum(w for w, j in zip(weights, CANDIDATES) if j in assignment)


def tail_probability(observed, support=FIXED, weights=WEIGHTS, strict=False):
    """Exact one-sided randomization tail under uniform assignment support."""
    if observed not in support:
        raise ValueError('observed assignment outside declared design')
    threshold = statistic(observed, weights)
    compare = (lambda v: v > threshold) if strict else (lambda v: v >= threshold)
    return F(sum(compare(statistic(z, weights)) for z in support), len(support))


def null_rejection_probability(alpha, support=FIXED, weights=WEIGHTS, strict=False):
    """Type I rejection probability under a sharp null on focal outcomes."""
    return F(sum(tail_probability(z, support, weights, strict) <= alpha for z in support), len(support))


def probability_of_event(support, predicate):
    return F(sum(bool(predicate(z)) for z in support), len(support))


def mispecified_exposure_contrast():
    """True outcome depends on B; analyst incorrectly records A exposure."""
    a, b = CANDIDATES[:2]
    y = lambda z: int(b in z)
    mean_a1 = sum(F(y(z), 1) for z in FIXED if a in z) / 3
    mean_a0 = sum(F(y(z), 1) for z in FIXED if a not in z) / 3
    return mean_a1, mean_a0, mean_a1 - mean_a0


class TH187ExactAudit(unittest.TestCase):
    def test_design_size(self):
        self.assertEqual(len(FIXED), 6)

    def test_design_unique(self):
        self.assertEqual(len(set(FIXED)), 6)

    def test_exactly_two_candidates(self):
        self.assertTrue(all(len(z) == 2 for z in FIXED))

    def test_all_focals_remain_untreated(self):
        self.assertTrue(all(set(z).isdisjoint(FOCALS) for z in FIXED))

    def test_biclique_null_imputability(self):
        # All focal outcomes fixed under no-spillover null; candidate outcomes unused.
        y = {0: 8, 1: 4, 2: 2, 3: 1}
        self.assertEqual(len({sum(y[i] * int(j in z)
                                  for i, j in zip(FOCALS, CANDIDATES))
                              for z in FIXED}), 6)

    def test_statistic_support(self):
        self.assertEqual(sorted(statistic(z) for z in FIXED), [3, 5, 6, 9, 10, 12])

    def test_observed_max(self):
        self.assertEqual(statistic((4, 5)), 12)

    def test_conservative_max_tail(self):
        self.assertEqual(tail_probability((4, 5)), F(1, 6))

    def test_strict_max_tail_zero(self):
        self.assertEqual(tail_probability((4, 5), strict=True), F(0))

    def test_all_six_rank_probabilities(self):
        self.assertEqual(sorted(tail_probability(z) for z in FIXED),
                         [F(k, 6) for k in range(1, 7)])

    def test_superuniform_for_all_six_cutoffs(self):
        for k in range(7):
            a = F(k, 6)
            self.assertLessEqual(null_rejection_probability(a), a)

    def test_strict_tail_is_anti_conservative_at_zero(self):
        self.assertEqual(null_rejection_probability(F(0), strict=True), F(1, 6))

    def test_strict_tail_is_anti_conservative_at_one_sixth(self):
        self.assertEqual(null_rejection_probability(F(1, 6), strict=True), F(2, 6))

    def test_all_tied_conservative(self):
        self.assertEqual(tail_probability((4, 5), weights=(0, 0, 0, 0)), F(1))

    def test_all_tied_strict(self):
        self.assertEqual(tail_probability((4, 5), weights=(0, 0, 0, 0), strict=True), F(0))

    def test_bernoulli_support(self):
        self.assertEqual(len(BERNOULLI), 16)

    def test_design_mismatch_pvalue(self):
        self.assertEqual(tail_probability((4, 5), support=BERNOULLI), F(1, 4))

    def test_mismatch_does_not_equal_fixed(self):
        self.assertNotEqual(tail_probability((4, 5), support=BERNOULLI),
                            tail_probability((4, 5)))

    def test_reject_off_support(self):
        with self.assertRaises(ValueError):
            tail_probability((0, 4))

    def test_exposure_probability(self):
        self.assertEqual(probability_of_event(FIXED, lambda z: 4 in z), F(1, 2))

    def test_negative_misspecified_contrast(self):
        self.assertEqual(mispecified_exposure_contrast(), (F(1, 3), F(2, 3), -F(1, 3)))

    def test_true_B_exposure_contrast(self):
        b = CANDIDATES[1]
        self.assertEqual(F(sum(int(b in z) for z in FIXED if b in z), 3) -
                         F(sum(int(b in z) for z in FIXED if b not in z), 3), F(1))

    def test_zero_structural_A_effect(self):
        # Hypothetical intervention changes A only, leaves B fixed.
        b = CANDIDATES[1]
        for other in product((0, 1), repeat=3):
            z0 = set(j for bit, j in zip(other, (5, 6, 7)) if bit)
            z1 = z0 | {4}
            self.assertEqual(int(b in z0), int(b in z1))

    def test_fixed_K_negative_assignment_correlation(self):
        a, b = CANDIDATES[:2]
        pab = probability_of_event(FIXED, lambda z: a in z and b in z)
        pa = probability_of_event(FIXED, lambda z: a in z)
        pb = probability_of_event(FIXED, lambda z: b in z)
        self.assertEqual(pab - pa * pb, -F(1, 12))


if __name__ == '__main__':
    unittest.main(verbosity=2)
