"""TH185: exact synthetic checks only. No ICPSR data or documentation is loaded."""
from fractions import Fraction as F
from itertools import combinations
import unittest


def exact_exposure(n_eligible, n_seeds, nominated):
    """Probability at least one nominated eligible peer is a seed, fixed-size draw."""
    if not (0 <= n_seeds <= n_eligible and 0 <= nominated <= n_eligible):
        raise ValueError("invalid design")
    total = 0
    hit = 0
    nominated_ids = set(range(nominated))
    for selected in combinations(range(n_eligible), n_seeds):
        total += 1
        hit += bool(nominated_ids.intersection(selected))
    return F(hit, total)


def school_binary_ate_bounds(treated_observed, control_observed,
                             treated_total, control_total, treated_mean,
                             control_mean):
    """Equal-school-weighted bounds, outcome in [0,1], arbitrary missingness."""
    for x, n in ((treated_observed, treated_total),
                 (control_observed, control_total)):
        if not (0 < n and 0 <= x <= n):
            raise ValueError("invalid school counts")
    if not (F(0) <= treated_mean <= F(1) and
            F(0) <= control_mean <= F(1)):
        raise ValueError("invalid observed mean")
    t_low = F(treated_observed, treated_total) * treated_mean
    t_high = t_low + F(treated_total - treated_observed, treated_total)
    c_low = F(control_observed, control_total) * control_mean
    c_high = c_low + F(control_total - control_observed, control_total)
    return t_low - c_high, t_high - c_low


class TestTH185(unittest.TestCase):
    def test_public_metadata_case_delta(self):
        self.assertEqual(24471 - 24191, 280)

    def test_public_metadata_case_delta_relative(self):
        self.assertEqual(F(280, 24191), F(24471 - 24191, 24191))

    def test_variable_count_candidate_arithmetic_only(self):
        self.assertEqual(482 + 17, 499)

    def test_four_school_blocks(self):
        self.assertEqual(56 // 4, 14)

    def test_conditional_assignments(self):
        self.assertEqual(len(list(combinations(range(4), 2))) ** 14, 6 ** 14)

    def test_school_admin_missing_total(self):
        self.assertEqual(56 - 49, 7)

    def test_school_admin_missing_by_arm(self):
        self.assertEqual((28 - 23, 28 - 26), (5, 2))

    def test_school_admin_arms_sum(self):
        self.assertEqual(23 + 26, 49)

    def test_one_friend(self):
        self.assertEqual(exact_exposure(4, 2, 1), F(1, 2))

    def test_two_friends_fixed_size(self):
        self.assertEqual(exact_exposure(4, 2, 2), F(5, 6))

    def test_two_friends_independent_draw_is_different(self):
        self.assertNotEqual(exact_exposure(4, 2, 2), 1 - F(1, 2) ** 2)

    def test_no_friends(self):
        self.assertEqual(exact_exposure(4, 2, 0), F(0))

    def test_all_friends(self):
        self.assertEqual(exact_exposure(4, 2, 4), F(1))

    def test_two_stage_exposure(self):
        self.assertEqual(F(1, 2) * exact_exposure(4, 2, 2), F(5, 12))

    def test_bounds_width(self):
        lo, hi = school_binary_ate_bounds(23, 26, 28, 28, F(2, 5), F(1, 2))
        self.assertEqual(hi - lo, F(1, 4))

    def test_bounds_example(self):
        lo, hi = school_binary_ate_bounds(23, 26, 28, 28, F(2, 5), F(1, 2))
        self.assertEqual((lo, hi), (F(-29, 140), F(3, 70)))

    def test_bounds_include_zero(self):
        lo, hi = school_binary_ate_bounds(23, 26, 28, 28, F(2, 5), F(1, 2))
        self.assertTrue(lo < 0 < hi)

    def test_bounds_no_missing(self):
        self.assertEqual(school_binary_ate_bounds(4, 4, 4, 4, F(3, 4), F(1, 2)), (F(1, 4), F(1, 4)))

    def test_invalid_exposure_rejected(self):
        with self.assertRaises(ValueError):
            exact_exposure(4, 5, 2)

    def test_invalid_bounds_rejected(self):
        with self.assertRaises(ValueError):
            school_binary_ate_bounds(5, 4, 4, 4, F(1, 2), F(1, 2))


if __name__ == "__main__":
    unittest.main(verbosity=2)
