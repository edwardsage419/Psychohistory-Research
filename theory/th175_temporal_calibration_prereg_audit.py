#!/usr/bin/env python3
"""TH175 synthetic exact arithmetic audit. Python standard library only.

All inputs are invented for algebraic counterexamples. No human or administrative
microdata are used. This is not a test of causal identification in real data.
"""
from fractions import Fraction as F
from math import comb, ceil, log, exp
import unittest


def q_proxy(p, sensitivity, specificity):
    assert F(0) <= p <= F(1)
    assert F(0) <= sensitivity <= F(1)
    assert F(0) <= specificity <= F(1)
    return sensitivity * p + (1 - specificity) * (1 - p)


def invert_proxy(q, sensitivity, specificity):
    denom = sensitivity + specificity - 1
    if denom <= 0:
        raise ValueError("non-positive measurement discrimination")
    p = (q + specificity - 1) / denom
    if not F(0) <= p <= F(1):
        raise ValueError("incompatible observed proxy proportion")
    return p


def exact_binomial_pmf(n, k, p):
    if not (0 <= k <= n and F(0) <= p <= F(1)):
        raise ValueError("invalid binomial inputs")
    return F(comb(n, k)) * p**k * (1-p)**(n-k)


def exact_two_panel_flag_probability(n, p0, p1, threshold=F(1, 5)):
    """P(|X1/n - X0/n| >= threshold), independent equal-size panels."""
    if n <= 0:
        raise ValueError("n must be positive")
    return sum((exact_binomial_pmf(n, i, p0) * exact_binomial_pmf(n, j, p1)
                for i in range(n + 1) for j in range(n + 1)
                if abs(F(j-i, n)) >= threshold), F(0))


def union_hoeffding_sufficient_n(m=4, eps=0.1, alpha=0.05):
    """Conservative sufficient per-stratum n, NOT a universal minimum.

    Assumes m independent Bernoulli validation strata with unbiased iid
    sampling conditional on known gold labels and no selection/cluster effects.
    Hoeffding and union bound: P(any |p_hat-p| > eps) <= 2*m*exp(-2*n*eps^2).
    """
    if not (m > 0 and 0 < eps < 1 and 0 < alpha < 1):
        raise ValueError("invalid design constants")
    return ceil(log(2*m/alpha) / (2*eps*eps))


class TH175Audit(unittest.TestCase):
    def setUp(self):
        self.p0, self.s0, self.c0 = F(1, 2), F(4, 5), F(9, 10)
        self.q0 = q_proxy(self.p0, self.s0, self.c0)

    def test_01_initial_proxy(self):
        self.assertEqual(self.q0, F(9, 20))

    def test_02_world_a_drift_only(self):
        self.assertEqual(q_proxy(F(1, 2), F(9, 10), F(9, 10)), F(1, 2))

    def test_03_world_b_true_trend_only(self):
        self.assertEqual(q_proxy(F(4, 7), F(4, 5), F(9, 10)), F(1, 2))

    def test_04_worlds_same_observations(self):
        self.assertEqual((self.q0, F(1, 2)),
                         (q_proxy(F(1, 2), F(4, 5), F(9, 10)),
                          q_proxy(F(4, 7), F(4, 5), F(9, 10))))

    def test_05_worlds_different_true_trends(self):
        self.assertEqual(F(1, 2) - self.p0, F(0))
        self.assertEqual(F(4, 7) - self.p0, F(1, 14))

    def test_06_positive_gold_sentinel_detects_drift_in_expectation(self):
        self.assertEqual(q_proxy(F(1), F(9, 10), F(9, 10)) -
                         q_proxy(F(1), F(4, 5), F(9, 10)), F(1, 10))

    def test_07_negative_gold_sentinel_stable(self):
        self.assertEqual(q_proxy(F(0), F(9, 10), F(9, 10)) -
                         q_proxy(F(0), F(4, 5), F(9, 10)), F(0))

    def test_08_irrelevant_control_stable(self):
        self.assertEqual(F(1, 2) - F(1, 2), F(0))

    def test_09_source_calibration_bias_under_drift(self):
        self.assertEqual(invert_proxy(F(1, 2), self.s0, self.c0), F(4, 7))
        self.assertEqual(invert_proxy(F(1, 2), F(9, 10), self.c0), F(1, 2))

    def test_10_binomial_normalization(self):
        for p in [F(0), F(1, 10), F(4, 5), F(9, 10), F(1)]:
            self.assertEqual(sum((exact_binomial_pmf(10, k, p)
                                  for k in range(11)), F(0)), F(1))

    def test_11_flag_probability_between_zero_one(self):
        for n in [5, 10, 20]:
            prob = exact_two_panel_flag_probability(n, F(4, 5), F(9, 10))
            self.assertTrue(F(0) < prob < F(1))

    def test_12_no_drift_can_still_flag(self):
        self.assertTrue(exact_two_panel_flag_probability(10, F(4, 5), F(4, 5)) > 0)

    def test_13_power_below_one_under_drift(self):
        self.assertTrue(exact_two_panel_flag_probability(20, F(4, 5), F(9, 10)) < 1)

    def test_14_familywise_ten_independent_tests(self):
        self.assertEqual(1-(F(19, 20)**10), F(1)-(F(19, 20)**10))
        self.assertTrue(1-F(19, 20)**10 > F(2, 5))

    def test_15_holm_first_cutoff(self):
        self.assertEqual(F(1, 20)/10, F(1, 200))

    def test_16_no_gold_positive_probability(self):
        self.assertEqual((1-F(1, 10))**10, F(9, 10)**10)
        self.assertTrue(F(9, 10)**10 > F(1, 3))

    def test_17_hoeffding_four_strata(self):
        self.assertEqual(union_hoeffding_sufficient_n(), 254)

    def test_18_hoeffding_boundary(self):
        self.assertTrue(8*exp(-2*253*.1*.1) > .05)
        self.assertTrue(8*exp(-2*254*.1*.1) <= .05)

    def test_19_total_gold_labels_four_strata(self):
        self.assertEqual(4*union_hoeffding_sufficient_n(), 1016)

    def test_20_near_singular_amplification(self):
        self.assertEqual(invert_proxy(F(1, 2), F(51, 100), F(51, 100)), F(1, 2))
        self.assertEqual(invert_proxy(F(51, 100), F(51, 100), F(51, 100)), F(1))

    def test_21_singular_denominator_rejected(self):
        with self.assertRaises(ValueError):
            invert_proxy(F(1, 2), F(1, 2), F(1, 2))

    def test_22_incompatible_proxy_rejected(self):
        with self.assertRaises(ValueError):
            invert_proxy(F(1), F(4, 5), F(9, 10))

    def test_23_invalid_design_rejected(self):
        with self.assertRaises(ValueError):
            union_hoeffding_sufficient_n(eps=0)

    def test_24_design_precision_doubles_quadruples(self):
        self.assertEqual(union_hoeffding_sufficient_n(eps=.05), 1016)


if __name__ == "__main__":
    print("TH175_SYNTHETIC_AUDIT")
    print("q0=", q_proxy(F(1, 2), F(4, 5), F(9, 10)))
    print("q1_world_A=", q_proxy(F(1, 2), F(9, 10), F(9, 10)))
    print("q1_world_B=", q_proxy(F(4, 7), F(4, 5), F(9, 10)))
    for n in [10, 20]:
        d = exact_two_panel_flag_probability(n, F(4, 5), F(9, 10))
        f = exact_two_panel_flag_probability(n, F(4, 5), F(4, 5))
        print(f"n={n}, drift_flag={float(d):.9f}, no_drift_false_flag={float(f):.9f}")
    print("familywise_10=", float(1-F(19, 20)**10))
    print("no_positive_n10_p0.1=", float(F(9, 10)**10))
    print("hoeffding_per_stratum=", union_hoeffding_sufficient_n())
    unittest.main(argv=["th175", "-v"], exit=False)
