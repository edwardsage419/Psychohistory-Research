#!/usr/bin/env python3
"""TH172: exact synthetic binary-proxy misclassification and invariance audit.

Only artificial fractions are used. No external packages, network, user data, or CI.
Run: python th172_proxy_invariance_exact_audit_20261031.py
"""
from fractions import Fraction as F
import unittest


def rate(true_rate, sensitivity, specificity):
    """P(proxy=1) for a binary true state and binary proxy."""
    p, se, sp = F(true_rate), F(sensitivity), F(specificity)
    if not all(F(0) <= x <= F(1) for x in (p, se, sp)):
        raise ValueError("probabilities must be in [0, 1]")
    return se * p + (F(1) - sp) * (F(1) - p)


def invert(proxy_rate, sensitivity, specificity):
    """Recover prevalence only with externally justified, known error rates."""
    q, se, sp = F(proxy_rate), F(sensitivity), F(specificity)
    if not all(F(0) <= x <= F(1) for x in (q, se, sp)):
        raise ValueError("probabilities must be in [0, 1]")
    denominator = se + sp - F(1)
    if denominator == 0:
        raise ValueError("singular proxy: sensitivity + specificity = 1")
    p = (q + sp - F(1)) / denominator
    if not F(0) <= p <= F(1):
        raise ValueError("proxy prevalence incompatible with calibration")
    return p


def bounded_prevalence(q, min_sensitivity, min_specificity):
    """Sharp interval when se in [s0,1], sp in [t0,1], s0+t0>1.

    Derivation: q=f+(se-f)*p, f=1-sp in [0,1-t0].
    q is minimized at se=s0,f=0; maximized at se=1,f=1-t0.
    """
    q, s0, t0 = map(F, (q, min_sensitivity, min_specificity))
    if not (F(0) <= q <= F(1) and F(0) <= s0 <= 1 and F(0) <= t0 <= 1):
        raise ValueError("invalid bounds")
    if s0 + t0 <= 1:
        raise ValueError("requires uniformly informative proxy")
    lower = max(F(0), (q - (1 - t0)) / t0)
    upper = min(F(1), q / s0)
    if lower > upper:
        raise ValueError("no compatible prevalence")
    return lower, upper


class TestTH172(unittest.TestCase):
    def test_01_perfect_measurement(self):
        self.assertEqual(rate(F(1, 3), 1, 1), F(1, 3))

    def test_02_two_worlds_same_proxy(self):
        self.assertEqual(rate(F(1, 4), 1, F(2, 3)), F(1, 2))
        self.assertEqual(rate(F(3, 4), F(2, 3), 1), F(1, 2))

    def test_03_true_gap_hidden(self):
        self.assertEqual(F(1, 4) - F(3, 4), -F(1, 2))
        self.assertEqual(F(1, 2) - F(1, 2), 0)

    def test_04_reverse_worlds(self):
        self.assertEqual(F(3, 4) - F(1, 4), F(1, 2))

    def test_05_false_proxy_gap(self):
        self.assertEqual(rate(F(1, 2), 1, F(1, 2)) - rate(F(1, 2), 1, 1), F(1, 4))

    def test_06_version_drift(self):
        before = rate(F(1, 2), F(4, 5), F(9, 10))
        after = rate(F(1, 2), F(9, 10), F(7, 10))
        self.assertEqual((before, after, after - before), (F(9, 20), F(3, 5), F(3, 20)))

    def test_07_known_calibration_inverts(self):
        self.assertEqual(invert(F(1, 2), 1, F(2, 3)), F(1, 4))
        self.assertEqual(invert(F(1, 2), F(2, 3), 1), F(3, 4))

    def test_08_singular_proxy(self):
        with self.assertRaises(ValueError):
            invert(F(1, 2), F(1, 2), F(1, 2))

    def test_09_invalid_probability(self):
        with self.assertRaises(ValueError):
            rate(F(5, 4), 1, 1)

    def test_10_incompatible_calibration(self):
        with self.assertRaises(ValueError):
            invert(F(9, 10), F(3, 4), 1)

    def test_11_partial_bounds(self):
        self.assertEqual(bounded_prevalence(F(1, 2), F(3, 4), F(3, 4)), (F(1, 3), F(2, 3)))

    def test_12_lower_endpoint_attained(self):
        self.assertEqual(rate(F(1, 3), 1, F(3, 4)), F(1, 2))

    def test_13_upper_endpoint_attained(self):
        self.assertEqual(rate(F(2, 3), F(3, 4), 1), F(1, 2))

    def test_14_group_difference_interval(self):
        low, high = bounded_prevalence(F(1, 2), F(3, 4), F(3, 4))
        self.assertEqual((low - high, high - low), (-F(1, 3), F(1, 3)))

    def test_15_uninformative_error_bounds_rejected(self):
        with self.assertRaises(ValueError):
            bounded_prevalence(F(1, 2), F(1, 2), F(1, 2))

    def test_16_sensitivity_to_near_singular_calibration(self):
        self.assertEqual(invert(F(1, 2), F(51, 100), F(51, 100)), F(1, 2))
        self.assertEqual(invert(F(501, 1000), F(51, 100), F(51, 100)), F(11, 20))


if __name__ == '__main__':
    unittest.main(verbosity=2)
