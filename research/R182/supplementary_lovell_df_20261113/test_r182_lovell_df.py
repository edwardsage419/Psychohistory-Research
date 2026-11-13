import unittest
from fractions import Fraction as F
import r182_lovell_df_correction as m

class TestLovellResidualizationDF(unittest.TestCase):
    def test_four_design_group_sxx(self):
        expected={'BALANCED':F(2), 'POSITIVE':F(8,3),
                  'NEGATIVE':F(8,3), 'STRONG_POSITIVE':F(3)}
        for name,counts in m.DESIGNS.items():
            self.assertEqual(m.independent_cell_sxx(counts),expected[name])

    def test_original_240_world_count_and_2880_rows(self):
        a=m.calculate()
        self.assertEqual((a['worlds'],a['artificial_rows_total']),(240,2880))

    def test_all_nonzero_case_correction(self):
        a=m.calculate()
        self.assertEqual(a['worlds_nonzero_residual'],160)
        for d,row in a['fixed_artificial_world_cases'].items():
            self.assertEqual(F(row['corrected_se_squared']),
                             F(row['naive_se_squared'])*F(int(row['naive_df']),int(row['full_df'])))

    def test_zero_sse_not_a_standard_error_inflation_claim(self):
        a=m.calculate()
        self.assertEqual(a['worlds_zero_residual_undefined_se_ratio'],80)
        for name,counts in m.DESIGNS.items():
            w=m.one_world(counts,F(0),F(1,4),F(-2),F(0))
            self.assertEqual(w['corrected_se_squared'],0)
            self.assertIsNone(w['naive_over_corrected_se_squared'])

    def test_balance_small_sample(self):
        w=m.one_world(m.DESIGNS['BALANCED'],F(0),F(1,4),F(-2),F(1,4))
        self.assertEqual((w['corrected_se_squared'],w['naive_se_squared']),
                         (F(1,20),F(1,28)))

    def test_strong_positive_small_sample(self):
        w=m.one_world(m.DESIGNS['STRONG_POSITIVE'],F(0),F(1,4),F(-2),F(1,4))
        self.assertEqual((w['corrected_se_squared'],w['naive_se_squared']),
                         (F(1,39),F(1,45)))

    def test_never_confuse_same_sse_with_same_se(self):
        for counts in m.DESIGNS.values():
            w=m.one_world(counts,F(1),F(1,2),F(2),F(1,2))
            self.assertGreater(w['corrected_se_squared'],w['naive_se_squared'])
            self.assertEqual(w['beta_x'],F(1,2))

    def test_validation_fail_closed(self):
        with self.assertRaises(ValueError):
            m.make_rows((2,2,2,3),F(0),F(1,4),F(1),F(1,4))
        with self.assertRaises(ValueError):
            m.residualized_slope_and_sse([(F(1),F(0),F(1)), (F(1),F(0),F(2))])

if __name__ == '__main__':
    unittest.main()
