"""TH180 synthetic classification-feedback audit. Only artificial exact fractions.
Run: python3 -m unittest -v th180_classification_feedback_audit.py
"""
from fractions import Fraction as F
import unittest


def observed(true_share, sensitivity, false_positive):
    """P(record=1) under a two-by-two measurement channel."""
    assert all(F(0) <= x <= F(1) for x in (true_share, sensitivity, false_positive))
    return sensitivity * true_share + false_positive * (1 - true_share)


def next_share(true_share, exposure_share, response_strength):
    """Artificial positive-label reinforcement, not a fitted social law."""
    assert all(F(0) <= x <= F(1) for x in (true_share, exposure_share, response_strength))
    return true_share + response_strength * exposure_share * (1 - true_share)


def mixture(high_share, high_rate=F(4, 5), low_rate=F(1, 5)):
    return high_share * high_rate + (1 - high_share) * low_rate


class TH180SyntheticTests(unittest.TestCase):
    def test_initial_prevalence(self):
        self.assertEqual(observed(F(2, 5), F(1), F(0)), F(2, 5))

    def test_label_feedback(self):
        self.assertEqual(next_share(F(2, 5), F(2, 5), F(5, 6)), F(3, 5))

    def test_label_feedback_observation(self):
        self.assertEqual(observed(next_share(F(2, 5), F(2, 5), F(5, 6)), F(1), F(0)), F(3, 5))

    def test_reclassification_same_observed(self):
        self.assertEqual(observed(F(2, 5), F(1), F(1, 3)), F(3, 5))

    def test_external_shock_same_observed(self):
        self.assertEqual(observed(F(3, 5), F(1), F(0)), F(3, 5))

    def test_mixture_initial(self):
        self.assertEqual(mixture(F(1, 3)), F(2, 5))

    def test_mixture_final(self):
        self.assertEqual(mixture(F(2, 3)), F(3, 5))

    def test_all_four_worlds_same_observation(self):
        worlds = [
            observed(next_share(F(2, 5), F(2, 5), F(5, 6)), F(1), F(0)),
            observed(F(2, 5), F(1), F(1, 3)),
            observed(F(3, 5), F(1), F(0)),
            mixture(F(2, 3)),
        ]
        self.assertEqual(worlds, [F(3, 5)] * 4)

    def test_different_true_prevalences(self):
        self.assertNotEqual(F(2, 5), F(3, 5))

    def test_feedback_strength_zero(self):
        self.assertEqual(next_share(F(2, 5), F(2, 5), F(0)), F(2, 5))

    def test_second_feedback_step(self):
        self.assertEqual(next_share(F(3, 5), F(3, 5), F(5, 6)), F(4, 5))

    def test_negative_response_requires_other_model(self):
        with self.assertRaises(AssertionError):
            next_share(F(2, 5), F(2, 5), F(-1, 2))

    def test_zero_exposure_no_effect(self):
        self.assertEqual(next_share(F(2, 5), F(0), F(5, 6)), F(2, 5))

    def test_classifier_false_positive_impact(self):
        self.assertEqual(observed(F(2, 5), F(1), F(1, 3)) - observed(F(2, 5), F(1), F(0)), F(1, 5))

    def test_mixture_composition_shift(self):
        self.assertEqual(mixture(F(2, 3)) - mixture(F(1, 3)), F(1, 5))

    def test_no_randomized_identification_from_two_aggregate_points(self):
        # Identical observed sequence under different generating mechanisms.
        baseline = observed(F(2, 5), F(1), F(0))
        feedback = observed(next_share(F(2, 5), baseline, F(5, 6)), F(1), F(0))
        coding = observed(F(2, 5), F(1), F(1, 3))
        self.assertEqual((baseline, feedback), (baseline, coding))


if __name__ == '__main__':
    unittest.main()
