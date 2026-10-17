"""R078 32 purely synthetic rigorous counterexample checks (no original humans)."""
from __future__ import annotations
from fractions import Fraction as F
import json
import math
import unittest
from r078_exact_micro_causal_macro_bridge import (
    OBS_PREVALENCE,LOW,HIGH,Q,
    bernoulli_prob,direct_observational_joint,latent_observational_joint,
    joint_conditional_on_own_prior,full_observational_joint,
    expected_brier_with_history,expected_brier_source_only_baseline,
    expected_logloss_with_history,expected_logloss_baseline,
    do_prob_direct,do_prob_latent,individual_causal_effect,
    variance_direct_group,variance_latent_group,
    covariance_latent_between_people,fraction_string,
    validate_exact_contract,build_result,
)

class EquivalenceTests(unittest.TestCase):
    def setUp(self):
        self.a=direct_observational_joint()
        self.b=latent_observational_joint()

    def test_01_source_prior_is_half(self):
        self.assertEqual(OBS_PREVALENCE,F(1,2))
    def test_02_exact_qs(self):
        self.assertEqual((LOW,HIGH),(F(3,10),F(7,10)))
    def test_03_observational_joint_identical(self):
        self.assertEqual(self.a,self.b)
    def test_04_four_joint_cells(self):
        self.assertEqual(self.a,{(0,0):F(7,20),(0,1):F(3,20),
                                 (1,0):F(3,20),(1,1):F(7,20)})
    def test_05_person_joint_sum_unity(self):
        self.assertEqual(sum(self.a.values()),1)
    def test_06_person_own_history_independence_conditional_x0(self):
        self.assertEqual(joint_conditional_on_own_prior(self.a,0),
                         joint_conditional_on_own_prior(self.b,0))
    def test_07_person_own_history_independence_conditional_x1(self):
        self.assertEqual(joint_conditional_on_own_prior(self.a,1),
                         joint_conditional_on_own_prior(self.b,1))
    def test_08_full_joint_eight_cells_identical(self):
        self.assertEqual(full_observational_joint(self.a),
                         full_observational_joint(self.b))
    def test_09_full_joint_eight_cells_sum(self):
        self.assertEqual(sum(full_observational_joint(self.a).values()),1)
    def test_10_own_prior_x_each_half(self):
        f=full_observational_joint(self.a)
        for x in (0,1):
            self.assertEqual(sum(v for (xx,o,y),v in f.items() if xx==x),F(1,2))
    def test_11_conditional_history_brier_is_exact_21_percent(self):
        self.assertEqual(expected_brier_with_history(self.a),F(21,100))
    def test_12_conditional_history_brier_same_both(self):
        self.assertEqual(expected_brier_with_history(self.a),
                         expected_brier_with_history(self.b))
    def test_13_nolag_brier_25_percent(self):
        self.assertEqual(expected_brier_source_only_baseline(self.a),F(1,4))
    def test_14_nolag_brier_same_both(self):
        self.assertEqual(expected_brier_source_only_baseline(self.a),
                         expected_brier_source_only_baseline(self.b))
    def test_15_brier_gain_4_percent_exact(self):
        self.assertEqual(expected_brier_source_only_baseline(self.a)
                         - expected_brier_with_history(self.a),F(1,25))
    def test_16_logloss_history_matches_binary_entropy(self):
        want=-(.3*math.log(.3)+.7*math.log(.7))
        self.assertAlmostEqual(expected_logloss_with_history(self.a),want,places=12)
    def test_17_logloss_baseline_is_ln2(self):
        self.assertAlmostEqual(expected_logloss_baseline(self.a),math.log(2),places=12)
    def test_18_logloss_two_models_identical(self):
        self.assertAlmostEqual(expected_logloss_with_history(self.a),
                               expected_logloss_with_history(self.b),places=12)
    def test_19_direct_model_do0(self):
        self.assertEqual(do_prob_direct(0),F(3,10))
    def test_20_direct_model_do1(self):
        self.assertEqual(do_prob_direct(1),F(7,10))
    def test_21_direct_causal_effect(self):
        self.assertEqual(individual_causal_effect("direct"),F(2,5))
    def test_22_latent_intervention_is_neutral(self):
        self.assertEqual(do_prob_latent(0),do_prob_latent(1))
        self.assertEqual(do_prob_latent(0),F(1,2))
    def test_23_latent_causal_effect_zero(self):
        self.assertEqual(individual_causal_effect("latent"),F(0))
    def test_24_social_conditional_predictive_not_causal(self):
        self.assertEqual(self.a,self.b)
        self.assertNotEqual(individual_causal_effect("direct"),
                            individual_causal_effect("latent"))
    def test_25_direct_group_n1_var(self):
        self.assertEqual(variance_direct_group(1),F(1,4))
    def test_26_latent_group_n1_var(self):
        self.assertEqual(variance_latent_group(1),F(1,4))
    def test_27_group_n10_exact_variances(self):
        self.assertEqual((variance_direct_group(10),variance_latent_group(10)),
                         (F(1,40),F(61,1000)))
    def test_28_group_covariance_shared_U(self):
        self.assertEqual(covariance_latent_between_people(),F(1,25))
    def test_29_group_var_decomposition_n100(self):
        self.assertEqual(variance_direct_group(100),F(1,400))
        self.assertEqual(variance_latent_group(100),F(421,10000))
    def test_30_group_var_gap_nonzero_n_gt1(self):
        for n in (2,3,10,100,10_000):
            self.assertGreater(variance_latent_group(n),
                               variance_direct_group(n))
    def test_31_large_groups_direct_go_zero(self):
        self.assertLess(variance_direct_group(1000),F(1,1000))
        self.assertGreater(variance_latent_group(1000),F(1,25))
    def test_32_causal_type_unknown_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"UNKNOWN_CAUSAL_MODEL"):
            individual_causal_effect("social_learning")
    def test_33_intervention_binary_only(self):
        with self.assertRaisesRegex(ValueError,"INTERVENTION"):
            do_prob_latent(2)
    def test_34_bernoulli_binary_only(self):
        with self.assertRaisesRegex(ValueError,"BINARY"):
            bernoulli_prob(-1,F(1,2))
    def test_35_invalid_probability_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"PROBABILITY"):
            bernoulli_prob(1,F(3,2))
    def test_36_group_n_nonpositive_rejected(self):
        for n in (0,-2,0.5):
            with self.assertRaisesRegex(ValueError,"GROUP_N"):
                variance_direct_group(n)
    def test_37_latent_group_nonpositive_rejected(self):
        for n in (0,-3,4.5):
            with self.assertRaisesRegex(ValueError,"GROUP_N"):
                variance_latent_group(n)
    def test_38_exact_fraction_encoding(self):
        self.assertEqual(fraction_string(F(7,20)),"7/20")
    def test_39_run_validates_all_exact_identities(self):
        self.assertTrue(validate_exact_contract())
    def test_40_output_no_human_data_and_model_frozen(self):
        r=build_result()
        self.assertEqual(r["human_data_rows_consumed"],0)
        self.assertEqual(r["synthetic_evidence_grade"],"E1_EXACT_ENUMERATION")
        self.assertEqual(r["PESEN_v0.1"],"FROZEN")
    def test_41_output_distinguishes_inferential_levels(self):
        r=build_result()
        self.assertFalse(r["intervention_do_O"]["causal_effect_identified_from_equal_observational_table"])
        self.assertEqual(r["unvalidated_projections"]["historical_long_horizon_prediction"],"NOT_VALIDATED")
    def test_42_json_serializable(self):
        self.assertEqual(json.loads(json.dumps(build_result()))["research_id"],"R078")

if __name__=="__main__":
    unittest.main()
