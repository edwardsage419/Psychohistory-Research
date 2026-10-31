"""TH178: exact arithmetic and synthetic counterexamples only.

No patient-level data, causal estimation, web requests or paid CI.
Source counts: Locker & Mason (2006), Mason et al. (2012),
Woodcock et al. (2013); see accompanying TH178 research note.
"""
from fractions import Fraction as F
import unittest

CONSENTED, IT_FAILURE, NO_SUBMISSION, SUBMITTED = 137, 5, 9, 123
EPISODES, INCOMPLETE = 648203, 9018
HALF_HOUR, OTHER_ZERO_FIVE = 114875, 281890
KNOWN_METHOD, COMPUTER, MANUAL = 105, 42, 63


def valid_episodes():
    return EPISODES - INCOMPLETE


def pooled_whipple():
    """Pooled index; article's 316.9 is a mean of department indices."""
    return F(500 * (HALF_HOUR + OTHER_ZERO_FIVE), valid_episodes())


def recorded_target_bounds(observed_on_time, total, max_misclassified):
    """Sharp logical bounds under an externally justified error-count cap."""
    if not (0 <= observed_on_time <= total and 0 <= max_misclassified <= total):
        raise ValueError("invalid input")
    return (F(max(0, observed_on_time - max_misclassified), total),
            F(min(total, observed_on_time + max_misclassified), total))


def target_worlds():
    """Same recorded 95/100; true on-time can differ across worlds."""
    reported = [True] * 95 + [False] * 5
    true_a = reported.copy()
    true_b = [False] * 5 + [True] * 90 + [False] * 5
    return reported, true_a, true_b


def periodic_placebo_counts():
    """Artificial digit heaping can affect target and placebo cutoffs."""
    counts = {m: 100 for m in range(220, 261)}
    counts[230] += 200
    counts[240] += 200
    return counts


class ExactAudit(unittest.TestCase):
    def test_submitted_departments(self):
        self.assertEqual(CONSENTED - IT_FAILURE - NO_SUBMISSION, SUBMITTED)

    def test_published_response_percentage_conflict(self):
        self.assertNotEqual(F(100 * SUBMITTED, CONSENTED), F(869, 10))
        self.assertTrue(F(89, 1) < F(100 * SUBMITTED, CONSENTED) < F(90, 1))

    def test_invalid_departments_count(self):
        self.assertEqual(IT_FAILURE + NO_SUBMISSION, 14)

    def test_valid_episodes(self):
        self.assertEqual(valid_episodes(), 639185)

    def test_missing_percentage(self):
        self.assertTrue(F(13, 1000) < F(INCOMPLETE, EPISODES) < F(15, 1000))

    def test_half_hour_share(self):
        self.assertTrue(F(179, 1000) < F(HALF_HOUR, valid_episodes()) < F(181, 1000))

    def test_other_ending_share(self):
        self.assertTrue(F(440, 1000) < F(OTHER_ZERO_FIVE, valid_episodes()) < F(442, 1000))

    def test_combined_digit_heaping(self):
        self.assertEqual(HALF_HOUR + OTHER_ZERO_FIVE, 396765)
        self.assertTrue(F(62, 100) < F(396765, valid_episodes()) < F(63, 100))

    def test_uniform_reference_excess_is_conditional(self):
        self.assertEqual(F(396765) - F(valid_episodes(), 5), F(268928))

    def test_pooled_vs_mean_whipple(self):
        self.assertTrue(F(310) < pooled_whipple() < F(311))
        self.assertNotEqual(pooled_whipple(), F(3169, 10))

    def test_known_recording_methods(self):
        self.assertEqual(COMPUTER + MANUAL, KNOWN_METHOD)
        self.assertEqual(SUBMITTED - KNOWN_METHOD, 18)

    def test_manual_computer_index_difference(self):
        self.assertEqual(F(3757, 10) - F(2137, 10), F(162))

    def test_2012_last_twenty_minutes_delta(self):
        self.assertEqual(F(84, 10) - F(47, 10), F(37, 10))
        self.assertEqual(F(84, 47), F(84, 10) / F(47, 10))

    def test_2012_age_interaction_descriptive(self):
        self.assertEqual((F(173, 10) - F(74, 10)) - (F(63, 10) - F(41, 10)), F(77, 10))

    def test_2012_performance_vs_mean_time(self):
        self.assertEqual(F(963, 10) - F(839, 10), F(124, 10))
        self.assertEqual(F(86, 10), F(43, 5))

    def test_2013_standard_relaxation(self):
        self.assertEqual(F(98) - F(95), F(3))

    def test_two_worlds_same_report_different_truth(self):
        reported, true_a, true_b = target_worlds()
        self.assertEqual(sum(reported), 95)
        self.assertEqual(sum(true_a), 95)
        self.assertEqual(sum(true_b), 90)

    def test_error_cap_bounds(self):
        self.assertEqual(recorded_target_bounds(960, 1000, 20), (F(47, 50), F(49, 50)))

    def test_error_cap_invalid(self):
        with self.assertRaises(ValueError):
            recorded_target_bounds(101, 100, 2)

    def test_placebo_can_spike_too(self):
        c = periodic_placebo_counts()
        self.assertEqual(c[230], c[240])
        self.assertEqual(c[230], 300)
        self.assertEqual(c[229], c[239])


if __name__ == "__main__":
    unittest.main(verbosity=2)
