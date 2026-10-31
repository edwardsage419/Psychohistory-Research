"""TH174: exact synthetic checks for measurement transport and verification selection.
No real participants, external services, or repository state are read.
"""
from fractions import Fraction as F
import unittest


def proxy_rate(prevalence, sensitivity, specificity):
    """P(X=1) with a binary latent truth and a fallible proxy."""
    return prevalence * sensitivity + (1 - prevalence) * (1 - specificity)


def inverse_calibration(observed, sensitivity, specificity):
    slope = sensitivity + specificity - 1
    if slope == 0:
        raise ValueError("uninformative proxy: inverse is unidentified")
    result = (observed + specificity - 1) / slope
    if not 0 <= result <= 1:
        raise ValueError("observed rate is incompatible with calibration")
    return result


def selection_bounds(verified_n, verified_positive, unverified_n,
                     missing_low=F(0), missing_high=F(1)):
    """Sharp finite-population fractions under stated missing-stratum bounds."""
    assert verified_n > 0 and 0 <= verified_positive <= verified_n
    assert unverified_n >= 0 and 0 <= missing_low <= missing_high <= 1
    n = verified_n + unverified_n
    return ((F(verified_positive) + unverified_n * missing_low) / n,
            (F(verified_positive) + unverified_n * missing_high) / n)


def sensitivity_bounds(observed, sensitivity_lo, sensitivity_hi,
                       specificity_lo, specificity_hi):
    """Corner extrema for informative proxies, q inside all feasible ranges.

    Assumes s >= q, 1-c <= q, s+c>1 throughout rectangle.
    These restrictions make p increase with c and decrease with s.
    """
    q = observed
    assert sensitivity_lo <= sensitivity_hi and specificity_lo <= specificity_hi
    assert sensitivity_lo >= q >= 1 - specificity_lo
    assert sensitivity_lo + specificity_lo > 1
    return (inverse_calibration(q, sensitivity_hi, specificity_lo),
            inverse_calibration(q, sensitivity_lo, specificity_hi))


class TH174ExactAudit(unittest.TestCase):
    def setUp(self):
        self.source = (F(1, 2), F(4, 5), F(9, 10))
        self.target = (F(1, 4), F(3, 5), F(3, 5))

    def test_source_observation(self):
        self.assertEqual(proxy_rate(*self.source), F(9, 20))

    def test_target_observation_same(self):
        self.assertEqual(proxy_rate(*self.target), F(9, 20))

    def test_true_prevalences_differ(self):
        self.assertEqual(self.source[0] - self.target[0], F(1, 4))

    def test_source_inverse(self):
        self.assertEqual(inverse_calibration(F(9, 20), *self.source[1:]), F(1, 2))

    def test_wrong_target_transport(self):
        self.assertEqual(inverse_calibration(F(9, 20), *self.source[1:]), F(1, 2))
        self.assertEqual(inverse_calibration(F(9, 20), *self.target[1:]), F(1, 4))

    def test_source_and_target_informative(self):
        for _, s, c in (self.source, self.target):
            self.assertGreater(s + c, 1)

    def test_negative_control_null_with_true_gap(self):
        p0, p1 = F(1, 4), F(3, 4)
        self.assertEqual(proxy_rate(p1, F(3, 4), F(3, 4)) -
                         proxy_rate(p0, F(3, 4), F(3, 4)), F(1, 4))
        self.assertEqual(F(1, 2) - F(1, 2), 0)  # insensitive control
        self.assertEqual(p1 - p0, F(1, 2))

    def test_version_drift_without_truth_drift(self):
        p = F(1, 2)
        self.assertEqual(proxy_rate(p, F(4, 5), F(9, 10)), F(9, 20))
        self.assertEqual(proxy_rate(p, F(9, 10), F(9, 10)), F(1, 2))
        self.assertEqual(F(1, 2) - F(9, 20), F(1, 20))

    def test_uninformative_proxy_rejected(self):
        with self.assertRaises(ValueError):
            inverse_calibration(F(1, 2), F(1, 2), F(1, 2))

    def test_incompatible_proxy_rejected(self):
        with self.assertRaises(ValueError):
            inverse_calibration(F(9, 10), F(3, 5), F(3, 5))

    def test_calibration_sensitivity_bounds(self):
        self.assertEqual(sensitivity_bounds(F(9, 20), F(3, 5), F(4, 5),
                                            F(3, 5), F(9, 10)),
                         (F(1, 8), F(7, 10)))

    def test_sensitivity_bound_endpoints_attainable(self):
        lo, hi = sensitivity_bounds(F(9, 20), F(3, 5), F(4, 5),
                                    F(3, 5), F(9, 10))
        self.assertEqual(proxy_rate(lo, F(4, 5), F(3, 5)), F(9, 20))
        self.assertEqual(proxy_rate(hi, F(3, 5), F(9, 10)), F(9, 20))

    def test_verification_no_assumptions(self):
        self.assertEqual(selection_bounds(40, 30, 60), (F(3, 10), F(9, 10)))

    def test_verification_bounded_missing(self):
        self.assertEqual(selection_bounds(40, 30, 60, F(1, 5), F(4, 5)),
                         (F(21, 50), F(39, 50)))

    def test_verification_all_observed(self):
        self.assertEqual(selection_bounds(40, 30, 0), (F(3, 4), F(3, 4)))

    def test_verification_endpoints_same_observed_records(self):
        # 40 verified: 30 positives, 10 negatives. 60 unverified: 30
        # proxy-positive and 30 proxy-negative in both worlds. Truth differs.
        observed = (40, 30, 10, 30, 30)
        self.assertEqual(observed, (40, 30, 10, 30, 30))
        self.assertEqual(F(30 + 0, 100), F(3, 10))
        self.assertEqual(F(30 + 60, 100), F(9, 10))


if __name__ == "__main__":
    unittest.main(verbosity=2)
