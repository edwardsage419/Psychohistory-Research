#!/usr/bin/env python3
"""TH177: exact arithmetic audit of published aggregate tables and synthetic counterexamples.

Source transcription: Locker & Mason (2005 BMJ; 2006 EMJ), Propper et al.
(October 2008 Bristol CMPO Working Paper 08/205, Table 5). No patient-level data.
Run: python3 th177_target_incentives_original_table_audit.py
"""
from fractions import Fraction as F
import unittest

EPISODES_2005 = {
    'discharged': 311957, 'admitted': 94200, 'transferred': 4452,
    'died': 975, 'left_without_being_seen': 16504, 'unknown': 505,
}
TOTAL_2005 = 428593
TOTAL_2006 = 621674
VALID_2006 = 616067

# EMJ 2006 Table 1, digit order 0..9. Table columns sum exactly.
DIGITS_230_239 = (1918,1773,1870,1879,1946,2407,2190,2301,2426,3217)
DIGITS_240_249 = (1438,423,378,347,303,322,324,307,337,326)
# Contradictory text in 2006 narrative, values explicitly labeled as prose.
PROSE_2006 = {'230_0':1915,'230_9':3215,'240_0':1434,'240_9':329}
TABLE_2006 = {'230_0':DIGITS_230_239[0], '230_9':DIGITS_230_239[9],
              '240_0':DIGITS_240_249[0], '240_9':DIGITS_240_249[9]}


def published_table_sums():
    return sum(DIGITS_230_239), sum(DIGITS_240_249)


def last_digit_excess(p=F(1,10)):
    """Excess counts against a user-specified digit baseline p, not a gaming estimate."""
    n1, n2 = published_table_sums()
    return (F(DIGITS_230_239[9]) - p*n1,
            F(DIGITS_240_249[0]) - p*n2)


def baseline_sensitivity(lo=F(8,100), hi=F(12,100)):
    """Arithmetic range of summed digit excess for shared baseline p in [lo,hi]."""
    assert F(0) <= lo <= hi <= F(1)
    return sum(last_digit_excess(hi)), sum(last_digit_excess(lo))


def synthetic_two_worlds(k=200):
    """Same reported digits; different unobserved true threshold compliance.

    World A: all reported 239-minute records correspond to true 239 minutes.
    World B: k of these records have true duration 241 minutes but are
    reported as 239. This is a mathematical possibility, not an allegation.
    """
    assert 0 <= k <= DIGITS_230_239[9]
    reported_239 = DIGITS_230_239[9]
    return {
        'observed_239_A': reported_239,
        'observed_239_B': reported_239,
        'true_under_240_among_observed_239_A': reported_239,
        'true_under_240_among_observed_239_B': reported_239-k,
        'unidentified_true_compliance_gap': k,
    }


def propper_2008_gmm_coefficients():
    """Table 5, one point increase in the 0..100 target-pressure measure."""
    return {'suspensions': F(19,1000), 'removals': F(27,1000)}


def report():
    a,b=published_table_sums()
    ex1,ex2=last_digit_excess()
    low,high=baseline_sensitivity()
    return {
        '2005_outcome_sum':sum(EPISODES_2005.values()),
        '2006_valid_and_invalid':(VALID_2006,TOTAL_2006-VALID_2006),
        '2006_table_sums':(a,b),
        'table_vs_prose_deltas':{k:TABLE_2006[k]-PROSE_2006[k] for k in TABLE_2006},
        'digit_9_rate_230_239':F(DIGITS_230_239[9],a),
        'digit_0_rate_240_249':F(DIGITS_240_249[0],b),
        'excess_uniform':(ex1,ex2,ex1+ex2),
        'excess_uniform_as_share_valid':(ex1+ex2)/VALID_2006,
        'sensitivity_8_to_12pct':(low,high),
        'propper_gmm':propper_2008_gmm_coefficients(),
        'two_worlds':synthetic_two_worlds(),
    }


class TestTH177(unittest.TestCase):
    def test_01_2005_total(self): self.assertEqual(sum(EPISODES_2005.values()),TOTAL_2005)
    def test_02_2005_discharged(self): self.assertEqual(EPISODES_2005['discharged'],311957)
    def test_03_2005_admitted(self): self.assertEqual(EPISODES_2005['admitted'],94200)
    def test_04_2005_rest(self): self.assertEqual(sum(v for k,v in EPISODES_2005.items() if k not in ('discharged','admitted')),22436)
    def test_05_2006_invalid(self): self.assertEqual(TOTAL_2006-VALID_2006,5607)
    def test_06_2006_valid_share(self): self.assertTrue(F(VALID_2006,TOTAL_2006)>F(99,100))
    def test_07_230_table_total(self): self.assertEqual(sum(DIGITS_230_239),21927)
    def test_08_240_table_total(self): self.assertEqual(sum(DIGITS_240_249),4505)
    def test_09_230_digit9(self): self.assertEqual(DIGITS_230_239[9],3217)
    def test_10_240_digit0(self): self.assertEqual(DIGITS_240_249[0],1438)
    def test_11_230_digit0_discrepancy(self): self.assertEqual(TABLE_2006['230_0']-PROSE_2006['230_0'],3)
    def test_12_230_digit9_discrepancy(self): self.assertEqual(TABLE_2006['230_9']-PROSE_2006['230_9'],2)
    def test_13_240_digit0_discrepancy(self): self.assertEqual(TABLE_2006['240_0']-PROSE_2006['240_0'],4)
    def test_14_240_digit9_discrepancy(self): self.assertEqual(TABLE_2006['240_9']-PROSE_2006['240_9'],-3)
    def test_15_uniform_excess_239(self): self.assertEqual(last_digit_excess()[0],F(10243,10))
    def test_16_uniform_excess_240(self): self.assertEqual(last_digit_excess()[1],F(1975,2))
    def test_17_uniform_excess_total(self): self.assertEqual(sum(last_digit_excess()),F(10059,5))
    def test_18_sensitivity_low(self): self.assertEqual(baseline_sensitivity()[0],F(37079,25))
    def test_19_sensitivity_high(self): self.assertEqual(baseline_sensitivity()[1],F(63511,25))
    def test_20_sensitivity_contains_uniform(self):
        lo,hi=baseline_sensitivity(); self.assertTrue(lo<sum(last_digit_excess())<hi)
    def test_21_gmm_order(self):
        x=propper_2008_gmm_coefficients(); self.assertLess(x['suspensions'],x['removals'])
    def test_22_synthetic_same_observed(self):
        w=synthetic_two_worlds();self.assertEqual(w['observed_239_A'],w['observed_239_B'])
    def test_23_synthetic_diff_true(self):
        w=synthetic_two_worlds();self.assertEqual(w['unidentified_true_compliance_gap'],200)
    def test_24_synthetic_zero(self):
        w=synthetic_two_worlds(0);self.assertEqual(w['true_under_240_among_observed_239_A'],w['true_under_240_among_observed_239_B'])
    def test_25_synthetic_max(self):
        w=synthetic_two_worlds(3217);self.assertEqual(w['true_under_240_among_observed_239_B'],0)
    def test_26_zero_digit_baseline(self): self.assertEqual(sum(last_digit_excess(F(0))),4655)
    def test_27_full_digit_baseline(self): self.assertEqual(sum(last_digit_excess(F(1))),4655-26432)
    def test_28_2005_sample_composition(self):
        self.assertEqual(F(EPISODES_2005['admitted'],TOTAL_2005),F(94200,428593))


if __name__ == '__main__':
    print('TH177 exact source table audit:', report())
    unittest.main(verbosity=2)
