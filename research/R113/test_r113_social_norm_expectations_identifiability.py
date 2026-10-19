"""R113 source-table arithmetic and synthetic nonidentification tests, no human rows."""
import json
import math
import unittest
import r113_social_norm_expectations_identifiability as m


class R113SourceAndMechanismTests(unittest.TestCase):
    def test_table_source_is_fixed_first_party_publication(self):
        x=m.published_table_2_arithmetic()
        self.assertEqual(x["source"],"10.3389/fpsyg.2014.01418")
        self.assertEqual(x["source_table"],"Table 2")

    def test_table_2_actual_behavior(self):
        self.assertEqual(m.published_table_2_arithmetic()["published_actor_behavior_percent"],[44,12,44])

    def test_table_2_responder_empirical_belief(self):
        self.assertEqual(m.published_table_2_arithmetic()["published_responder_empirical_expectation_percent"],[44,28,28])

    def test_empirical_minus_actual_published_arithmetic(self):
        self.assertEqual(m.published_table_2_arithmetic()["empirical_minus_behavior_percentage_points"],[0,16,-16])

    def test_normative_personal_belief_published_arithmetic(self):
        self.assertEqual(m.published_table_2_arithmetic()["normative_minus_personal_ought_percentage_points"],[0,-12,27])

    def test_actual_and_empirical_are_exclusive_100(self):
        x=m.published_table_2_arithmetic()
        self.assertEqual(x["sum_actual_behavior_percent"],100)
        self.assertEqual(x["sum_empirical_expectation_percent"],100)

    def test_personal_normative_multiresponse_not_simplex(self):
        self.assertEqual(m.published_table_2_arithmetic()["sum_personal_normative_judgment_percent"],174)
        with self.assertRaises(m.R113MeasurementError):
            m._validate_three((100,22,52), mutually_exclusive=True)

    def test_normative_expectation_multiresponse_not_simplex(self):
        self.assertEqual(m.published_table_2_arithmetic()["sum_normative_expectation_judgment_percent"],189)
        with self.assertRaises(m.R113MeasurementError):
            m._validate_three((100,10,79), mutually_exclusive=True)

    def test_fairness_multiple_acceptable_options_preserved(self):
        x=m.published_table_2_arithmetic()
        self.assertTrue(x["fairness_judgments_allow_multiple_options"])
        self.assertEqual(x["categories"],["equal_split_5_5","unequal_split_8_2","coin_flip"])

    def test_two_by_two_factual_vs_personal_normative(self):
        self.assertEqual(m.measure_kind(social=False,normative=False),"factual_belief")
        self.assertEqual(m.measure_kind(social=False,normative=True),"personal_normative_belief_about_ought")

    def test_two_by_two_empirical_vs_normative_expectation(self):
        self.assertEqual(m.measure_kind(social=True,normative=False),"empirical_expectation_about_others_actions")
        self.assertEqual(m.measure_kind(social=True,normative=True),"normative_expectation_about_others_ought_beliefs")

    def test_kind_flags_must_be_bool(self):
        with self.assertRaises(m.R113MeasurementError):
            m.measure_kind(social=1,normative=False)

    def test_percentage_reject_nan_inf_negative_over100(self):
        for v in (float("nan"),float("inf"),float("-inf"),-0.1,100.01):
            with self.subTest(value=v), self.assertRaises(m.R113MeasurementError):
                m._percentage(v)

    def test_percentage_reject_boolean(self):
        for v in (True,False):
            with self.subTest(v=v),self.assertRaises(m.R113MeasurementError):
                m._percentage(v)

    def test_wrong_count_rejected(self):
        with self.assertRaises(m.R113MeasurementError):
            m._validate_three((10,90),mutually_exclusive=True)

    def test_not_exclusive_option_total_rejected(self):
        with self.assertRaises(m.R113MeasurementError):
            m._validate_three((20,20,20),mutually_exclusive=True)

    def test_same_observed_action_different_motives(self):
        x=m.observational_equivalence_counterexample()
        self.assertEqual(x["unconditional_world"]["observed_action"],1)
        self.assertEqual(x["conditional_world"]["observed_action"],1)
        self.assertNotEqual(x["unconditional_world"]["parameters"],
                            x["conditional_world"]["parameters"])

    def test_counterfactual_resolves_synthetic_mechanism_difference(self):
        x=m.observational_equivalence_counterexample()
        self.assertEqual(x["unconditional_world"]["intervened_action"],1)
        self.assertEqual(x["conditional_world"]["intervened_action"],0)

    def test_empirical_specific_perturbation(self):
        x=m.isolated_expectation_manipulation()["empirical_only"]
        self.assertEqual(x,{"original":1,"switch_empirical_only":0,"switch_normative_only":1})

    def test_normative_specific_perturbation(self):
        x=m.isolated_expectation_manipulation()["normative_only"]
        self.assertEqual(x,{"original":1,"switch_empirical_only":1,"switch_normative_only":0})

    def test_unconditional_world_ignores_beliefs(self):
        m0=m.SyntheticChoiceMechanism(.1,0,0)
        for e,n in ((0,0),(1,1),(0,1),(1,0),(.3,.5)):
            with self.subTest(e=e,n=n):
                self.assertEqual(m0.choice(e,n),1)

    def test_syn_margin_scale_and_determinism(self):
        mm=m.SyntheticChoiceMechanism(-.2,.5,.5)
        self.assertAlmostEqual(mm.margin(.8,.8),.1)
        self.assertAlmostEqual(mm.margin(.2,.2),-.5)
        self.assertEqual(m.observational_equivalence_counterexample(),
                         m.observational_equivalence_counterexample())

    def test_invalid_synthetic_belief_rejected(self):
        m0=m.SyntheticChoiceMechanism(0,1,1)
        for invalid in (True,None,-.1,1.1,float("nan"),float("inf")):
            with self.subTest(v=invalid),self.assertRaises(m.R113MeasurementError):
                m0.choice(invalid,.5)

    def test_invalid_synthetic_coefficient_rejected(self):
        for invalid in (True,float("nan"),float("inf"),"1"):
            with self.subTest(v=invalid),self.assertRaises(m.R113MeasurementError):
                m.SyntheticChoiceMechanism(invalid,0,0)

    def test_no_individual_data_causality_claimed(self):
        x=m.published_table_2_arithmetic()
        self.assertTrue(x["source_values_rounded_published_percentages_not_individual_rows"])
        self.assertFalse(x["original_individual_human_experiment_data_read"])
        self.assertFalse(x["causal_effect_or_uncertainty_identified_from_aggregate_table"])
        self.assertTrue(m.observational_equivalence_counterexample()["models_are_synthetic_not_fitted"])

if __name__=="__main__":
    unittest.main()
