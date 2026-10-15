import unittest
from r063_fig6_check import RATE,FREQ,summarize

class AuthorFigureTests(unittest.TestCase):
    def test_exp1_counts_are_paired(self):
        self.assertEqual(len(RATE['exp1']['skilled']),24)
        self.assertEqual(len(RATE['exp1']['unskilled']),24)

    def test_exp2_counts_are_independent(self):
        self.assertEqual(len(RATE['exp2']['skilled']),22)
        self.assertEqual(len(RATE['exp2']['unskilled']),22)

    def test_two_model_frequencies_sum_to_one(self):
        for k,v in FREQ.items():
            self.assertAlmostEqual(v['VS']+v['metaVS'],1,places=12)

    def test_rate_direction(self):
        s=summarize()
        self.assertGreater(s['exp1']['mean_difference'],0)
        self.assertGreater(s['exp2']['mean_difference'],0)

    def test_exp1_exact_signed_rank_p_published(self):
        s=summarize()['exp1']
        self.assertEqual(s['paired_positive_n'],24)
        if 'wilcoxon_two_sided_p' in s:
            self.assertAlmostEqual(s['wilcoxon_two_sided_p'],1.1920928955078125e-7,places=14)

    def test_exp2_exact_rank_sum_p_published(self):
        s=summarize()['exp2']
        if 'mann_whitney_two_sided_p' in s:
            self.assertAlmostEqual(s['mann_whitney_two_sided_p'],.00017424674044409113,places=13)

if __name__=='__main__':
    unittest.main(verbosity=2)
