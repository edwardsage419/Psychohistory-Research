"""TH182 bounded theory audit: exact synthetic exposure and source arithmetic.

Only Python standard library. No personal data, external API, or CI execution.
Run: python3 th182_network_correction_exact_audit.py
"""
from fractions import Fraction as F
from itertools import combinations
import unittest

ELIGIBLE = tuple(range(4))
REF = 0
NONREF = 1
ASSIGNMENTS = tuple(combinations(ELIGIBLE, 2))


def exposure(assigned):
    """One focal observer outside four randomized seed-eligible peers."""
    z = set(assigned)
    if REF in z:
        return "referent"
    if NONREF in z:
        return "nonreferent_only"
    return "no_peer"


def probabilities():
    return {e: F(sum(exposure(z) == e for z in ASSIGNMENTS), len(ASSIGNMENTS))
            for e in ("no_peer", "nonreferent_only", "referent")}


def inv_probability(p):
    if p == 0:
        raise ValueError("Exposure has zero design probability")
    return 1 / p


def policy_world(outcome_all_seed):
    """All K=2 assignments observed; K=4 is outside randomized support."""
    d = {z: F(2, 5) for z in ASSIGNMENTS}
    d[tuple(ELIGIBLE)] = outcome_all_seed
    return d


def missing_school_bounds(observed_treated_mean, observed_control_mean):
    """Binary school outcome [0,1], 23/28 treated and 26/28 controls observed.

This is an artificial illustrative bound, NOT a bound for discipline counts.
"""
    lo = (23 * observed_treated_mean - 26 * observed_control_mean - 2) / 28
    hi = (23 * observed_treated_mean + 5 - 26 * observed_control_mean) / 28
    return lo, hi


class TheoryAudit(unittest.TestCase):
    def test_six_assignments(self):
        self.assertEqual(len(ASSIGNMENTS), 6)

    def test_assignments_unique(self):
        self.assertEqual(len(set(ASSIGNMENTS)), 6)

    def test_no_peer_count(self):
        self.assertEqual(sum(exposure(z) == "no_peer" for z in ASSIGNMENTS), 1)

    def test_nonreferent_count(self):
        self.assertEqual(sum(exposure(z) == "nonreferent_only" for z in ASSIGNMENTS), 2)

    def test_referent_count(self):
        self.assertEqual(sum(exposure(z) == "referent" for z in ASSIGNMENTS), 3)

    def test_no_peer_probability(self):
        self.assertEqual(probabilities()["no_peer"], F(1, 6))

    def test_nonreferent_probability(self):
        self.assertEqual(probabilities()["nonreferent_only"], F(1, 3))

    def test_referent_probability(self):
        self.assertEqual(probabilities()["referent"], F(1, 2))

    def test_probabilities_sum(self):
        self.assertEqual(sum(probabilities().values()), 1)

    def test_positive_inverse_weights(self):
        self.assertEqual(inv_probability(probabilities()["no_peer"]), 6)

    def test_zero_probability_rejected(self):
        with self.assertRaises(ValueError):
            inv_probability(F(0))

    def test_two_worlds_observationally_equal(self):
        a, b = policy_world(F(1, 10)), policy_world(F(9, 10))
        self.assertTrue(all(a[z] == b[z] for z in ASSIGNMENTS))

    def test_two_worlds_full_policy_opposite(self):
        a, b = policy_world(F(1, 10)), policy_world(F(9, 10))
        baseline = F(2, 5)
        self.assertEqual(a[tuple(ELIGIBLE)] - baseline, F(-3, 10))
        self.assertEqual(b[tuple(ELIGIBLE)] - baseline, F(1, 2))

    def test_missing_school_count(self):
        self.assertEqual((28 - 23, 28 - 26), (5, 2))

    def test_binary_missing_bounds_zero_observed(self):
        self.assertEqual(missing_school_bounds(F(0), F(0)), (F(-1, 14), F(5, 28)))

    def test_binary_missing_bounds_nonzero(self):
        self.assertEqual(missing_school_bounds(F(1, 2), F(1, 2)),
                         (F(-7, 56), F(7, 56)))

    def test_transport_can_reverse(self):
        base = F(2, 5)
        source, target = F(1, 2), F(1, 5)
        self.assertEqual((source - base, target - base), (F(1, 10), F(-1, 5)))

    def test_original_mixed_rounded_ratio(self):
        self.assertEqual(F(6, 100) / F(20, 100), F(3, 10))

    def test_source_version_correction(self):
        self.assertEqual(F(30, 100) - F(25, 100), F(1, 20))


if __name__ == "__main__":
    unittest.main(verbosity=2)
