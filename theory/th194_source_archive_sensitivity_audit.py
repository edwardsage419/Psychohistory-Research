"""TH194 synthetic-only exact audit of source lineage and archival selection.

No external data, network, third-party packages, or individual records.
Run: python -m unittest -v th194_source_archive_sensitivity_audit.py
     python -O -m unittest -v th194_source_archive_sensitivity_audit.py
"""
from fractions import Fraction as F
import unittest

ZERO, ONE = F(0), F(1)


def paired_reports(p, shared):
    """P(R1,R2|Y) under a mixture of shared and independent sources."""
    if not (ZERO <= p <= ONE and ZERO <= shared <= ONE):
        raise ValueError("probabilities outside [0,1]")
    independent = ONE - shared
    return {
        (1, 1): shared * p + independent * p * p,
        (1, 0): independent * p * (ONE - p),
        (0, 1): independent * p * (ONE - p),
        (0, 0): shared * (ONE - p) + independent * (ONE - p) ** 2,
    }


def archive_world(prevalence, retained_positive, retained_negative):
    """Observed (S=1,Y=1), (S=1,Y=0), and (S=0) probabilities."""
    for x in (prevalence, retained_positive, retained_negative):
        if not ZERO <= x <= ONE:
            raise ValueError("probabilities outside [0,1]")
    positive = prevalence * retained_positive
    negative = (ONE - prevalence) * retained_negative
    return positive, negative, ONE - positive - negative


def selection_bounds(observed_positive, observed_negative, max_ratio=None):
    """Sharp prevalence bounds when 1 <= P(S|Y=1)/P(S|Y=0) <= max_ratio.

    max_ratio=None removes both selection restrictions, retaining only support.
    Assumes positive observed cells; excludes zero-cell degeneracies.
    """
    a, b = observed_positive, observed_negative
    if a <= ZERO or b <= ZERO or a + b > ONE:
        raise ValueError("positive observed cells with a+b<=1 required")
    lo, hi = a, ONE - b
    if max_ratio is not None:
        if max_ratio < ONE:
            raise ValueError("max_ratio must be >= 1")
        lo = max(lo, a / (a + max_ratio * b))
        hi = min(hi, a / (a + b))
    if lo > hi:
        raise ValueError("assumptions inconsistent with observed data")
    return lo, hi


def retention_given_prevalence(a, b, prevalence):
    if not (a <= prevalence <= ONE - b and ZERO < prevalence < ONE):
        raise ValueError("prevalence infeasible")
    return a / prevalence, b / (ONE - prevalence)


def posterior_both_positive(prevalence, shared, sensitivity=F(3, 4), false_positive=F(1, 4)):
    """P(Y=1|R1=R2=1) with known parameters and unselected reports.

    Conditional report process is assumed independent of archive survival given Y.
    This is NOT an identified posterior from archival data alone.
    """
    if not ZERO <= prevalence <= ONE:
        raise ValueError("prevalence outside [0,1]")
    true_likelihood = paired_reports(sensitivity, shared)[(1, 1)]
    false_likelihood = paired_reports(false_positive, shared)[(1, 1)]
    numerator = prevalence * true_likelihood
    denominator = numerator + (ONE - prevalence) * false_likelihood
    if denominator == ZERO:
        raise ValueError("conditioning event has zero probability")
    return numerator / denominator


class ExactSyntheticTests(unittest.TestCase):
    def test_source_marginals(self):
        for p in (F(1, 4), F(3, 4)):
            for s in (ZERO, F(1, 2), ONE):
                d = paired_reports(p, s)
                self.assertEqual(sum(d.values()), ONE)
                self.assertEqual(d[(1, 1)] + d[(1, 0)], p)
                self.assertEqual(d[(1, 1)] + d[(0, 1)], p)

    def test_independent_false_positive(self):
        self.assertEqual(paired_reports(F(1, 4), ZERO)[(1, 1)], F(1, 16))

    def test_shared_false_positive(self):
        self.assertEqual(paired_reports(F(1, 4), ONE)[(1, 1)], F(1, 4))

    def test_half_shared_false_positive(self):
        self.assertEqual(paired_reports(F(1, 4), F(1, 2))[(1, 1)], F(5, 32))

    def test_independent_true_positive(self):
        self.assertEqual(paired_reports(F(3, 4), ZERO)[(1, 1)], F(9, 16))

    def test_shared_true_positive(self):
        self.assertEqual(paired_reports(F(3, 4), ONE)[(1, 1)], F(3, 4))

    def test_half_shared_true_positive(self):
        self.assertEqual(paired_reports(F(3, 4), F(1, 2))[(1, 1)], F(21, 32))

    def test_independent_posterior(self):
        self.assertEqual(posterior_both_positive(F(1, 2), ZERO), F(9, 10))

    def test_shared_posterior(self):
        self.assertEqual(posterior_both_positive(F(1, 2), ONE), F(3, 4))

    def test_half_shared_posterior(self):
        self.assertEqual(posterior_both_positive(F(1, 2), F(1, 2)), F(21, 26))

    def test_extreme_posterior(self):
        self.assertEqual(posterior_both_positive(F(3, 4), ZERO), F(27, 28))

    def test_two_worlds_same_archive(self):
        a = archive_world(F(1, 2), F(3, 4), F(1, 4))
        b = archive_world(F(3, 4), F(1, 2), F(1, 2))
        self.assertEqual(a, b)
        self.assertEqual(a, (F(3, 8), F(1, 8), F(1, 2)))

    def test_unrestricted_selection_bounds(self):
        self.assertEqual(selection_bounds(F(3, 8), F(1, 8)), (F(3, 8), F(7, 8)))

    def test_monotone_selection_bounds(self):
        self.assertEqual(selection_bounds(F(3, 8), F(1, 8), F(100)), (F(3, 8), F(3, 4)))

    def test_ratio_three_bounds(self):
        self.assertEqual(selection_bounds(F(3, 8), F(1, 8), F(3)), (F(1, 2), F(3, 4)))

    def test_ratio_one_bounds(self):
        self.assertEqual(selection_bounds(F(3, 8), F(1, 8), ONE), (F(3, 4), F(3, 4)))

    def test_world_a_retention(self):
        self.assertEqual(retention_given_prevalence(F(3, 8), F(1, 8), F(1, 2)), (F(3, 4), F(1, 4)))

    def test_world_b_retention(self):
        self.assertEqual(retention_given_prevalence(F(3, 8), F(1, 8), F(3, 4)), (F(1, 2), F(1, 2)))

    def test_interior_sharpness(self):
        a, b = F(3, 8), F(1, 8)
        for q in (F(1, 2), F(5, 8), F(3, 4)):
            p1, p0 = retention_given_prevalence(a, b, q)
            self.assertEqual(archive_world(q, p1, p0), (a, b, F(1, 2)))
            self.assertTrue(ONE <= p1 / p0 <= F(3))

    def test_invalid_source_probabilities(self):
        with self.assertRaises(ValueError):
            paired_reports(F(-1), ZERO)

    def test_invalid_ratio(self):
        with self.assertRaises(ValueError):
            selection_bounds(F(3, 8), F(1, 8), F(1, 2))

    def test_invalid_prevalence(self):
        with self.assertRaises(ValueError):
            retention_given_prevalence(F(3, 8), F(1, 8), F(1, 4))

    def test_joint_posterior_range_under_extra_assumptions(self):
        values = [posterior_both_positive(q, s)
                  for q in (F(1, 2), F(5, 8), F(3, 4))
                  for s in (ZERO, F(1, 2), ONE)]
        self.assertEqual((min(values), max(values)), (F(3, 4), F(27, 28)))


if __name__ == "__main__":
    unittest.main()
