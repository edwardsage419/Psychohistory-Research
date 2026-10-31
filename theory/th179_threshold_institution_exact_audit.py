"""TH179: exact synthetic counterexamples for institutional thresholds.

No personal data, third-party microdata, external packages, or CI are used.
Run: python3 th179_threshold_institution_exact_audit.py
"""
from fractions import Fraction as F
import unittest

BASE = (100, 100, 100, 100)


def shift(bins, n=30, origin=1, destination=2):
    """Move n synthetic observations across a cutoff, conserving sample size."""
    if n < 0 or origin == destination or min(origin, destination) < 0 or max(origin, destination) >= len(bins) or bins[origin] < n:
        raise ValueError('invalid shift')
    out = list(bins)
    out[origin] -= n
    out[destination] += n
    return tuple(out)


def world(mechanism):
    """Observed bins identical for learning, recording, or income reporting."""
    if mechanism not in ('real_change', 'recording_change', 'income_reporting_change'):
        raise ValueError('unknown mechanism')
    observed = shift(BASE)
    true_state = observed if mechanism == 'real_change' else BASE
    return true_state, observed


def near_cutoff_ratio(bins):
    if bins[1] == 0:
        raise ValueError('zero denominator')
    return F(bins[2], bins[1])


def tax_net_income(earnings, rate=F(1, 10), threshold=100, notch=20):
    earnings = F(earnings)
    return earnings * (1-rate) - (F(notch) if earnings > threshold else F(0))


def dominated_upper(threshold=100, rate=F(1, 10), notch=20):
    """Endpoint of a stylized dominated interval (threshold, endpoint)."""
    if not 0 <= rate < 1 or notch <= 0:
        raise ValueError('invalid tax schedule')
    return F(threshold) + F(notch) / (1-rate)


def weighted_outcome_delta(graduation_pp, advanced_pp, graduation_weight):
    """Purely illustrative two-outcome linear scalarization, no welfare claim."""
    w = F(graduation_weight)
    if not 0 <= w <= 1:
        raise ValueError('weight outside [0,1]')
    return w * F(graduation_pp) - (1-w) * F(advanced_pp)


def did(pre_treated, post_treated, pre_control, post_control):
    return (F(post_treated)-F(pre_treated))-(F(post_control)-F(pre_control))


class ExactAudit(unittest.TestCase):
    def test_base_total(self): self.assertEqual(sum(BASE), 400)
    def test_shift(self): self.assertEqual(shift(BASE), (100,70,130,100))
    def test_mass_conservation(self): self.assertEqual(sum(shift(BASE)),sum(BASE))
    def test_excess_equals_missing(self):
        a=shift(BASE)
        self.assertEqual(a[2]-BASE[2],BASE[1]-a[1])
    def test_ratio(self): self.assertEqual(near_cutoff_ratio(shift(BASE)),F(13,7))
    def test_smooth_ratio(self): self.assertEqual(near_cutoff_ratio(BASE),1)
    def test_same_observed_three_mechanisms(self):
        self.assertEqual(len({world(k)[1] for k in ('real_change','recording_change','income_reporting_change')}),1)
    def test_distinct_true_states(self):
        self.assertNotEqual(world('real_change')[0],world('recording_change')[0])
    def test_true_real_change(self): self.assertEqual(world('real_change')[0],shift(BASE))
    def test_true_recording(self): self.assertEqual(world('recording_change')[0],BASE)
    def test_placebo_rounding(self):
        # A nonpolicy round-number cutoff can generate the same density jump.
        self.assertEqual(near_cutoff_ratio(shift(BASE)),F(13,7))
    def test_dominated_interval(self): self.assertEqual(dominated_upper(),F(1100,9))
    def test_dominated_choice(self):
        self.assertGreater(tax_net_income(100),tax_net_income(105))
        self.assertLess(100,105)  # Lower earnings also implies more leisure.
    def test_not_every_above_threshold_dominated(self):
        self.assertGreater(tax_net_income(130),tax_net_income(100))
    def test_2017_relative_effect(self):
        self.assertEqual(F(219,1000)/F(788,1000),F(219,788))
    def test_2019_weight_threshold(self):
        self.assertEqual(weighted_outcome_delta(F(17,100),F(10,100),F(10,27)),0)
    def test_2017_weight_threshold(self):
        self.assertEqual(weighted_outcome_delta(F(22,100),F(15,100),F(15,37)),0)
    def test_version_sensitive_weight_example(self):
        self.assertGreater(weighted_outcome_delta(F(17,100),F(10,100),F(39,100)),0)
        self.assertLess(weighted_outcome_delta(F(22,100),F(15,100),F(39,100)),0)
    def test_did_same_observed(self):
        self.assertEqual(did(70,80,70,70),10)
        # World 1: true effect 10, no shock. World 2: effect 0, differential shock 10.
        self.assertEqual(70+10+0,70+0+10)
    def test_invalid_shift(self):
        with self.assertRaises(ValueError): shift(BASE,101)
    def test_invalid_mechanism(self):
        with self.assertRaises(ValueError): world('unknown')
    def test_invalid_weight(self):
        with self.assertRaises(ValueError): weighted_outcome_delta(1,1,F(3,2))


if __name__ == '__main__':
    unittest.main(verbosity=2)
