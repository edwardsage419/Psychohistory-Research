"""TH183/C009 synthetic exact arithmetic audit. Standard library only.

No participant data or causal re-estimation. Run:
  python -m unittest -v th183_paluck_correction_audit
  python -O -m unittest -v th183_paluck_correction_audit
"""
from fractions import Fraction as F
import unittest


def projected_reduction():
    """Ratio of the original paper's projected event totals, not a fitted ATE."""
    return F(2695 - 2012, 2695)


def missing_school_bounds(t_obs, c_obs, maximum=F(1)):
    """Equal-school weighted mean contrast with 5/28 T and 2/28 C missing.

    Requires an artificial bound 0 <= school outcome <= maximum.
    Not applicable without a defensible bound or to unequal school weights.
    """
    return ((23*t_obs - 26*c_obs - 2*maximum)/28,
            (23*t_obs + 5*maximum - 26*c_obs)/28)


def best_now(payoffs, probs):
    return max(sum((probs[s]*v[s] for s in probs), F(0)) for v in payoffs.values())


def perfect_information_value(payoffs, probs):
    return sum((probs[s]*max(v[s] for v in payoffs.values()) for s in probs), F(0))


def binary_signal_value(payoffs, accuracy):
    """Equal prior on H/L, symmetric signal accuracy q, free signal."""
    q = F(accuracy)
    pos = max(q*v['H'] + (1-q)*v['L'] for v in payoffs.values())
    neg = max((1-q)*v['H'] + q*v['L'] for v in payoffs.values())
    return (pos + neg)/2


class OriginalPublishedArithmetic(unittest.TestCase):
    def test_total_reduction(self):
        self.assertEqual(projected_reduction(), F(683, 2695))

    def test_total_reduction_percent(self):
        self.assertTrue(F(25, 100) < projected_reduction() < F(26, 100))

    def test_per_student_projection(self):
        self.assertEqual(F(2695, 11938) - F(2012, 11938), F(683, 11938))

    def test_rounded_mixed_ratio(self):
        self.assertEqual(F(6, 100)/F(20, 100), F(3, 10))

    def test_missing_schools(self):
        self.assertEqual(28-23, 5)
        self.assertEqual(28-26, 2)
        self.assertEqual(56-49, 7)


class ArtificialMissingnessBounds(unittest.TestCase):
    def setUp(self):
        self.lo, self.hi = missing_school_bounds(F(15, 100), F(20, 100))

    def test_lower(self):
        self.assertEqual(self.lo, F(-15, 112))

    def test_upper(self):
        self.assertEqual(self.hi, F(13, 112))

    def test_crosses_zero(self):
        self.assertLess(self.lo, 0)
        self.assertGreater(self.hi, 0)

    def test_all_missing_at_zero_or_one_attain_bounds(self):
        self.assertEqual(self.lo, (23*F(15,100)-26*F(20,100)-2)/28)
        self.assertEqual(self.hi, (23*F(15,100)+5-26*F(20,100))/28)

    def test_uncertainty_grows_with_cap(self):
        a,b=missing_school_bounds(F(15,100), F(20,100), F(2))
        self.assertLess(a,self.lo)
        self.assertGreater(b,self.hi)


class SyntheticOptionValue(unittest.TestCase):
    def setUp(self):
        self.p={'H':F(1,2),'L':F(1,2)}
        self.actions={'A':{'H':F(8),'L':F(-2)},'B':{'H':F(1),'L':F(3)}}

    def test_now(self):
        self.assertEqual(best_now(self.actions,self.p),F(3))

    def test_perfect_signal(self):
        self.assertEqual(perfect_information_value(self.actions,self.p),F(11,2))

    def test_perfect_signal_net_delay_cost(self):
        self.assertEqual(perfect_information_value(self.actions,self.p)-F(1),F(9,2))

    def test_high_delay_cost_reverses_preference(self):
        self.assertLess(perfect_information_value(self.actions,self.p)-F(3),best_now(self.actions,self.p))

    def test_noisy_signal(self):
        self.assertEqual(binary_signal_value(self.actions,F(3,4)),F(4))

    def test_no_information(self):
        self.assertEqual(binary_signal_value(self.actions,F(1,2)),F(3))

    def test_noisy_net_equal_to_now(self):
        self.assertEqual(binary_signal_value(self.actions,F(3,4))-F(1),best_now(self.actions,self.p))


if __name__ == '__main__':
    unittest.main()
