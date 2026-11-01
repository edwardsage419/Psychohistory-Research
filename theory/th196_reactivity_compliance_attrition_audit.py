"""TH196: exact synthetic audit of retrieval reactivity, noncompliance and attrition.

Only Python standard library. No personal data, network requests or random sampling.
Run: python -m unittest -v th196_reactivity_compliance_attrition_audit
     python -O -m unittest -v th196_reactivity_compliance_attrition_audit
"""
from fractions import Fraction as F
import unittest

# Each outcome is a hypothetical probability of a false report.
# Keys: (initial retrieval test, subsequent misinformation exposure).
FALSE_REPORT = {
    (0, 0): F(1, 10),
    (1, 0): F(1, 20),
    (0, 1): F(1, 4),
    (1, 1): F(9, 20),
}


def testing_effect(misinformation):
    return FALSE_REPORT[(1, misinformation)] - FALSE_REPORT[(0, misinformation)]


def misinformation_effect(test):
    return FALSE_REPORT[(test, 1)] - FALSE_REPORT[(test, 0)]


def factorial_interaction():
    return testing_effect(1) - testing_effect(0)


# Four artificial principal strata rows: (mass, D(0), D(1), Y(0), Y(1)).
# Y values are expected false-report probabilities under received exposure D.
STRATA = (
    (F(1, 4), 0, 0, F(0), F(0)),      # never exposed
    (F(1, 2), 0, 1, F(1, 4), F(3, 4)), # compliers
    (F(1, 4), 1, 1, F(1), F(1)),      # always exposed
)


def assigned_means(z, direct_assignment_effect=F(0)):
    exposure = sum(mass * (d0 if z == 0 else d1)
                   for mass, d0, d1, y0, y1 in STRATA)
    outcome = sum(mass * (y0 if (d0 if z == 0 else d1) == 0 else y1)
                  for mass, d0, d1, y0, y1 in STRATA)
    return exposure, outcome + (direct_assignment_effect if z else F(0))


def wald(direct_assignment_effect=F(0)):
    d0, y0 = assigned_means(0, direct_assignment_effect)
    d1, y1 = assigned_means(1, direct_assignment_effect)
    return (y1 - y0) / (d1 - d0)


def missing_binary_bounds(response_fraction, observed_positive_fraction):
    """Sharp population mean bounds without any assumption on missing binary Y."""
    known_positive = response_fraction * observed_positive_fraction
    return known_positive, known_positive + (1 - response_fraction)


def ate_bounds(control_response, control_positive, treated_response, treated_positive):
    c_lo, c_hi = missing_binary_bounds(control_response, control_positive)
    t_lo, t_hi = missing_binary_bounds(treated_response, treated_positive)
    return t_lo - c_hi, t_hi - c_lo


def lee_always_observed_bounds(s0, s1, y0, y1):
    """Binary outcome and monotone selection S(1)>=S(0); s1>=s0>0.

    Bounds concern the always-observed stratum only, not the full population.
    """
    if not (F(0) < s0 <= s1 <= F(1)):
        raise ValueError("Requires 0 < s0 <= s1 <= 1")
    if not (F(0) <= y0 <= F(1) and F(0) <= y1 <= F(1)):
        raise ValueError("Binary mean outside [0,1]")
    positives_treated_observed = s1 * y1
    selected_only = s1 - s0
    always_y1_low = max(F(0), positives_treated_observed - selected_only) / s0
    always_y1_high = min(s0, positives_treated_observed) / s0
    return always_y1_low - y0, always_y1_high - y0


class TH196SyntheticAudit(unittest.TestCase):
    def test_four_cells_are_probabilities(self):
        self.assertEqual(len(FALSE_REPORT), 4)
        self.assertTrue(all(F(0) <= v <= F(1) for v in FALSE_REPORT.values()))

    def test_testing_protects_without_misinformation(self):
        self.assertEqual(testing_effect(0), F(-1, 20))

    def test_testing_increases_error_with_misinformation(self):
        self.assertEqual(testing_effect(1), F(1, 5))

    def test_misinformation_effect_without_testing(self):
        self.assertEqual(misinformation_effect(0), F(3, 20))

    def test_misinformation_effect_with_testing(self):
        self.assertEqual(misinformation_effect(1), F(2, 5))

    def test_factorial_interaction(self):
        self.assertEqual(factorial_interaction(), F(1, 4))

    def test_interaction_independent_difference_of_differences(self):
        a = FALSE_REPORT[(1, 1)] - FALSE_REPORT[(1, 0)]
        b = FALSE_REPORT[(0, 1)] - FALSE_REPORT[(0, 0)]
        self.assertEqual(a - b, factorial_interaction())

    def test_stratum_mass(self):
        self.assertEqual(sum(s[0] for s in STRATA), 1)

    def test_monotone_compliance(self):
        self.assertTrue(all(s[1] <= s[2] for s in STRATA))

    def test_assignment_exposure_means(self):
        self.assertEqual((assigned_means(0)[0], assigned_means(1)[0]), (F(1, 4), F(3, 4)))

    def test_assignment_outcome_means(self):
        self.assertEqual((assigned_means(0)[1], assigned_means(1)[1]), (F(3, 8), F(5, 8)))

    def test_assignment_itt(self):
        self.assertEqual(assigned_means(1)[1] - assigned_means(0)[1], F(1, 4))

    def test_exposure_first_stage(self):
        self.assertEqual(assigned_means(1)[0] - assigned_means(0)[0], F(1, 2))

    def test_wald_recovers_complier_effect_under_exclusion(self):
        self.assertEqual(wald(), F(1, 2))

    def test_direct_assignment_effect_breaks_wald(self):
        self.assertEqual(wald(F(1, 10)), F(7, 10))

    def test_control_missing_bounds(self):
        self.assertEqual(missing_binary_bounds(F(3, 4), F(1, 3)), (F(1, 4), F(1, 2)))

    def test_treated_missing_bounds(self):
        self.assertEqual(missing_binary_bounds(F(1, 2), F(3, 4)), (F(3, 8), F(7, 8)))

    def test_complete_case_contrast(self):
        self.assertEqual(F(3, 4) - F(1, 3), F(5, 12))

    def test_full_ate_bounds_cross_zero(self):
        self.assertEqual(ate_bounds(F(3, 4), F(1, 3), F(1, 2), F(3, 4)), (F(-1, 8), F(5, 8)))

    def test_lower_endpoint_witness(self):
        self.assertEqual(F(3, 8) - F(1, 2), F(-1, 8))

    def test_upper_endpoint_witness(self):
        self.assertEqual(F(7, 8) - F(1, 4), F(5, 8))

    def test_lee_bounds_always_observed(self):
        self.assertEqual(lee_always_observed_bounds(F(1, 2), F(3, 4), F(1, 2), F(2, 3)), (F(0), F(1, 2)))

    def test_lee_requires_monotone_selection(self):
        with self.assertRaises(ValueError):
            lee_always_observed_bounds(F(3, 4), F(1, 2), F(1, 2), F(2, 3))

    def test_lee_requires_valid_binary_outcomes(self):
        with self.assertRaises(ValueError):
            lee_always_observed_bounds(F(1, 2), F(3, 4), F(1, 2), F(4, 3))

    def test_no_outcome_data_are_loaded(self):
        self.assertEqual(sum(mass for mass, *_ in STRATA), F(1))
        self.assertTrue(all(isinstance(x, F) for x in FALSE_REPORT.values()))


if __name__ == "__main__":
    unittest.main()
