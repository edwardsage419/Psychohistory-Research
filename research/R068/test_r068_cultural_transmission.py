import math
import unittest
from r068_cultural_transmission import (
    benchmark,choose_raw,finite_drift_stats,symmetric_mutation
)


class CulturalTransmissionTests(unittest.TestCase):
    def test_neutral_copy_identity(self):
        self.assertEqual(choose_raw("neutral",.2),.2)

    def test_conformist_majority_exact(self):
        self.assertAlmostEqual(choose_raw("conformist_three",.2),.104,12)

    def test_conformist_midpoint(self):
        self.assertAlmostEqual(choose_raw("conformist_three",.5),.5,12)

    def test_conformist_rare_trait_disfavored(self):
        self.assertLess(choose_raw("conformist_three",.2),.2)
        self.assertGreater(choose_raw("conformist_three",.8),.8)

    def test_success_weighting_twofold_example(self):
        self.assertAlmostEqual(choose_raw("success_weighted",.2,math.log(2)),1/3,12)

    def test_success_s_zero_is_neutral(self):
        self.assertAlmostEqual(choose_raw("success_weighted",.2,0),.2,12)

    def test_success_negative_weight_disfavors_A(self):
        self.assertLess(choose_raw("success_weighted",.2,-1),.2)

    def test_mutation_half_forces_half(self):
        self.assertEqual(symmetric_mutation(.02,.5),.5)

    def test_mutation_zero_leaves_probability(self):
        self.assertEqual(symmetric_mutation(.7,0),.7)

    def test_absorbing_zero_one_with_zero_mutation(self):
        for rule in ("neutral","conformist_three","success_weighted"):
            self.assertEqual(finite_drift_stats(rule,0,0,100)["mutated_probability_A"],0)
            self.assertEqual(finite_drift_stats(rule,1,0,100)["mutated_probability_A"],1)

    def test_finite_drift_variance_inverse_population(self):
        one=finite_drift_stats("neutral",.2,.01,100)
        two=finite_drift_stats("neutral",.2,.01,200)
        self.assertAlmostEqual(one["variance_frequency_after_finite_binomial_sampling"],
                               2*two["variance_frequency_after_finite_binomial_sampling"],12)

    def test_no_random_data_or_model_claims(self):
        q=benchmark()
        self.assertEqual(q["status"],"E1_MECHANISM_PASS")
        self.assertEqual(q["true_empirical_cultural_transmission_data"],"OPEN")
        self.assertEqual(q["history_extrapolation"],"UNSUPPORTED")

    def test_reject_nonfinite_trait_frequency(self):
        for bad in (-.1,1.1,math.nan,math.inf):
            with self.assertRaises(ValueError):
                choose_raw("neutral",bad)

    def test_reject_impossible_mutation(self):
        for bad in (-.1,.6,math.inf,math.nan):
            with self.assertRaises(ValueError):
                symmetric_mutation(.2,bad)

    def test_reject_invalid_population_n(self):
        for bad in (0,-1,2.1,True):
            with self.assertRaises(ValueError):
                finite_drift_stats("neutral",.2,.01,bad)

    def test_reject_nonfinite_or_oversized_success(self):
        for bad in (math.nan,21,-21,math.inf):
            with self.assertRaises(ValueError):
                choose_raw("success_weighted",.2,bad)

    def test_reject_unrecognized_culture_rule(self):
        with self.assertRaises(ValueError):
            choose_raw("unrecognized",.2)

    def test_frozen_benchmark_numbers(self):
        q=benchmark()
        self.assertAlmostEqual(q["models"]["neutral"]["mutated_probability_A"],.206)
        self.assertAlmostEqual(q["models"]["conformist_three"]["mutated_probability_A"],.11192)
        self.assertAlmostEqual(q["models"]["success_weighted"]["mutated_probability_A"],.01+.98/3)


if __name__=="__main__":
    unittest.main()
