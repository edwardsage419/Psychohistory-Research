"""Independent arithmetic and edge-case checks, no upstream CSV required."""
import math
import unittest
from r065_phase_f_aggregate_certificate import certificate


class AggregateCertificateTests(unittest.TestCase):
    def test_mean_matches_phase_e_archived(self):
        x=certificate()
        self.assertAlmostEqual(x['loo_logloss'], .6334654316626881,places=12)
        self.assertAlmostEqual(x['loo_brier'], .2205921211242944,places=12)
        self.assertAlmostEqual(x['uniform_minus_loo_mean_logloss'], .05968174889725955, places=12)

    def test_exact_conditional_interval_matches_old_bootstrap(self):
        x=certificate()['conditional_exact_bootstrap_percentile_95']
        for actual, past in zip(x['logloss'], [.015134327049981215,.10422917074453737]):
            self.assertAlmostEqual(actual,past,places=12)
        for actual, past in zip(x['brier'], [.008047271428541149,.05076848632286998]):
            self.assertAlmostEqual(actual,past,places=12)

    def test_heldout_probability(self):
        x=certificate()
        self.assertEqual(x['probability_training_loo_when_copy'], 76/233)
        self.assertEqual(x['probability_training_loo_when_not_copy'], 77/233)

    def test_exact_symmetry(self):
        x=certificate(20,10)
        self.assertAlmostEqual(x['loo_logloss'], -math.log(13/27), places=12)

    def test_extreme_all_zero(self):
        x=certificate(20,0)
        self.assertIsNone(x['probability_training_loo_when_copy'])
        self.assertTrue(math.isfinite(x['loo_logloss']))
        self.assertTrue(math.isfinite(x['conditional_exact_bootstrap_percentile_95']['logloss'][0]))

    def test_extreme_all_one(self):
        x=certificate(20,20)
        self.assertIsNone(x['probability_training_loo_when_not_copy'])
        self.assertTrue(math.isfinite(x['loo_logloss']))

    def test_invalid_counts(self):
        for n,k in ((1,1), (20,21),(20,-1),(2.1,1),(True,0)):
            with self.subTest(n=n,k=k),self.assertRaises(ValueError):
                certificate(n,k)

    def test_invalid_smoothing(self):
        for val in (0,-1,float('inf'),float('nan')):
            with self.subTest(pseudo=val),self.assertRaises(ValueError):
                certificate(226,73,val)

    def test_precision_repeats_identically(self):
        self.assertEqual(certificate(),certificate())


if __name__=='__main__':
    unittest.main()
