"""R128 original Skyrms ch1 pp3,5,11 and original 1755 story boundaries."""
import unittest
from fractions import Fraction as F
from unittest.mock import patch
import r128_skyrms2004_stag_hunt_exact as m


class SkyrmsOriginalAndGroupTrustTests(unittest.TestCase):
    def test_001_source_2004_publisher_original_book_identified(self):
        self.assertIn("Skyrms (2004)",m.__doc__)
    def test_002_source_not_rewriting_Rousseau_as_number_data(self):
        self.assertIn("NO modern payoff matrix",m.__doc__)
    def test_003_original_two_person_row_payoff_exact(self):
        self.assertEqual(m.skyrms_original_two_person_payoff(),((F(4),F(0)),(F(3),F(3))))
    def test_004_original_both_stag_payoff_four(self):
        self.assertEqual(m.stag_profile_payoffs(("S","S")),(F(4),F(4)))
    def test_005_original_stag_lone_failure_vs_hare_three(self):
        self.assertEqual(m.stag_profile_payoffs(("S","H")),(F(0),F(3)))
    def test_006_original_hare_both_each_three(self):
        self.assertEqual(m.stag_profile_payoffs(("H","H")),(F(3),F(3)))
    def test_007_source_original_opponent_q_three_quarters_tie(self):
        self.assertEqual(m.best_action_given_success_probability(F(3,4))["best"],"TIE")
    def test_008_original_q_one_half_choose_hare(self):
        self.assertEqual(m.best_action_given_success_probability(F(1,2))["best"],"H")
    def test_009_original_q_four_fifths_choose_stag(self):
        self.assertEqual(m.best_action_given_success_probability(F(4,5))["best"],"S")
    def test_010_original_source_q_zero_and_one(self):
        self.assertEqual(m.best_action_given_success_probability(F(0))["best"],"H")
        self.assertEqual(m.best_action_given_success_probability(F(1))["best"],"S")
    def test_011_group_two_p_four_fifths_stag_optimal(self):
        x=m.independence_prediction(2,F(4,5))
        self.assertEqual((x["expected_stag"],x["best"]),(F(16,5),"S"))
    def test_012_group_three_p_four_fifths_hare_optimal(self):
        x=m.independence_prediction(3,F(4,5))
        self.assertEqual((x["expected_stag"],x["best"]),(F(64,25),"H"))
    def test_013_group_three_independent_joint_sixteen_25(self):
        self.assertEqual(m.independence_prediction(3,F(4,5))["joint_all_other_stag"],F(16,25))
    def test_014_group_six_p_half_all_cooperate_probability_one_32(self):
        self.assertEqual(m.independence_prediction(6,F(1,2))["joint_all_other_stag"],F(1,32))
    def test_015_explicit_other_profile_distribution_two_agent(self):
        self.assertEqual(m.exhaustive_other_action_probabilities(2,F(3,4))["profiles"],2)
    def test_016_explicit_other_profile_distribution_n8_128(self):
        self.assertEqual(m.exhaustive_other_action_probabilities(8,F(1,2))["profiles"],128)
    def test_017_direct_profile_weighted_n3_four_fifths_equals_analytic(self):
        x=m.exhaustive_other_action_probabilities(3,F(4,5))
        self.assertEqual((x["joint_all_stag"],x["expected_stag"]),(F(16,25),F(64,25)))
    def test_018_all_1524_independent_profiles_and_42_cases(self):
        x=m.independent_group_full_audit()
        self.assertEqual(x["complete_independent_agent_profile_mass_computations"],1524)
        self.assertEqual(x["independent_n_probability_combinations"],42)
        self.assertTrue(x["all_analytic_vs_independent_enumeration_agreed"])
    def test_019_large_group_audit_changes_best_between_2_and_3(self):
        x=m.independent_group_full_audit()
        self.assertEqual((x["n2_p4over5_best"],x["n3_p4over5_best"]),("S","H"))
    def test_020_joint_independent_four_cell_masses_exact(self):
        x=m.frozen_correlated_trust_counterexample()["distributions"]["independent"]
        self.assertEqual(x["four_profile_masses"],["16/25","4/25","4/25","1/25"])
    def test_021_same_marginals_full_correlation_success_four_fifths(self):
        x=m.joint_two_other_beliefs((F(4,5),F(0),F(0),F(1,5)))
        self.assertEqual((x["marginal_other1_stag"],x["marginal_other2_stag"],x["joint_all_stag"]),
                         (F(4,5),F(4,5),F(4,5)))
    def test_022_correlated_marginals_switch_expected_action(self):
        x=m.frozen_correlated_trust_counterexample()["distributions"]
        self.assertEqual((x["independent"]["best"],x["perfect_positive_correlation"]["best"]),("H","S"))
    def test_023_lower_frechet_joint_three_fifths(self):
        x=m.joint_two_other_beliefs((F(3,5),F(1,5),F(1,5),F(0)))
        self.assertEqual(x["joint_all_stag"],F(3,5))
        self.assertEqual(x["expected_stag"],F(12,5))
    def test_024_joint_coupling_common_marginals_all_three(self):
        x=m.frozen_correlated_trust_counterexample()
        self.assertEqual(x["same_individual_marginal_each"],"4/5")
        self.assertFalse(x["real_human_belief_distribution_observed"])
    def test_025_joint_invalid_shape(self):
        for bad in ((),(F(1),),(F(1),)*3,(F(1),)*5,(x for x in (F(1),))):
            with self.subTest(bad=str(bad)),self.assertRaises(m.StagHuntError):
                m.validate_two_other_joint(bad)
    def test_026_joint_invalid_sum_fails_closed(self):
        with self.assertRaisesRegex(m.StagHuntError,"SUM"):
            m.joint_two_other_beliefs((F(1,2),F(0),F(0),F(0)))
    def test_027_joint_invalid_negative_and_probability_gt_one(self):
        for val in (F(-1,3),F(4,3)):
            with self.subTest(val=val),self.assertRaises(m.StagHuntError):
                m.validate_two_other_joint((val,F(0),F(0),F(1)))
    def test_028_individual_marginal_invalid_type_and_n(self):
        for bad in (0,1,True,False,0.5,"1/2",F(-1,2),F(3,2)):
            with self.subTest(bad=bad),self.assertRaises(m.StagHuntError):
                m.independence_prediction(2,bad)
        for bad in (1,9,True,2.0,"3"):
            with self.subTest(n=bad),self.assertRaises(m.StagHuntError):
                m.independence_prediction(bad,F(1,2))
    def test_029_stag_profile_rejects_invalid_actions_and_containers(self):
        for bad in ((),("S",),("S","H","X"),("S",True),["H"]*9,"SS",(x for x in ("S","H"))):
            with self.subTest(v=str(bad)),self.assertRaises(m.StagHuntError):
                m.stag_profile_payoffs(bad)
    def test_030_two_strict_nash_of_original_two_person_via_deviations(self):
        for action in ("S","H"):
            base=m.stag_profile_payoffs((action,action))[0]
            other="H" if action=="S" else "S"
            self.assertGreater(base,m.stag_profile_payoffs((other,action))[0])
    def test_031_two_person_source_book_payoff_dominance_and_risk_difference(self):
        p=m.skyrms_original_two_person_payoff()
        self.assertGreater(p[0][0],p[1][1])
        self.assertLess(p[0][0]-p[1][0],p[1][1]-p[0][1])


class OriginalRepeatedPrisonerToStagTests(unittest.TestCase):
    def test_032_source_p5_discount_three_fifths_exact_matrix(self):
        self.assertEqual(m.repeated_pd_infinite_payoffs(F(3,5)),
                         ((F(5),F(3,2)),(F(9,2),F(5,2))))
    def test_033_source_repeated_project_receipt_includes_exact_book_values(self):
        x=m.original_skyrms_printed_transformation()
        self.assertEqual(x["original_printed_book_p5_row_matrix"],[["5","3/2"],["9/2","5/2"]])
    def test_034_source_delta_three_fifths_TriggerTrigger_five(self):
        self.assertEqual(m.repeated_pd_infinite_payoffs(F(3,5))[0][0],5)
    def test_035_source_delta_three_fifths_TriggerFoole_three_halves(self):
        self.assertEqual(m.repeated_pd_infinite_payoffs(F(3,5))[0][1],F(3,2))
    def test_036_source_delta_three_fifths_FooleTrigger_nine_halves(self):
        self.assertEqual(m.repeated_pd_infinite_payoffs(F(3,5))[1][0],F(9,2))
    def test_037_source_delta_three_fifths_FooleFoole_five_halves(self):
        self.assertEqual(m.repeated_pd_infinite_payoffs(F(3,5))[1][1],F(5,2))
    def test_038_source_actual_single_stage_trigger_versus_foole_C_D(self):
        p=m.discounted_pd_prefix("T","F",F(3,5),3)
        self.assertEqual(p["stage_action_pairs"],("CD","DD","DD"))
    def test_039_source_actual_single_stage_foole_versus_trigger_D_C(self):
        p=m.discounted_pd_prefix("F","T",F(3,5),3)
        self.assertEqual(p["stage_action_pairs"],("DC","DD","DD"))
    def test_040_source_actual_single_stage_both_trigger_C_C(self):
        p=m.discounted_pd_prefix("T","T",F(3,5),3)
        self.assertEqual(p["stage_action_pairs"],("CC","CC","CC"))
    def test_041_source_actual_single_stage_both_foole_D_D(self):
        p=m.discounted_pd_prefix("F","F",F(3,5),3)
        self.assertEqual(p["stage_action_pairs"],("DD","DD","DD"))
    def test_042_independent_one_step_exact_geom_tail(self):
        d=F(3,5)
        prefix=m.discounted_pd_prefix("T","T",d,1)["row_discounted_total"]
        tail=m.discounted_pd_tail("T","T",d,1)
        self.assertEqual((prefix,tail,prefix+tail),(F(2),F(3),F(5)))
    def test_043_independent_finite_prefix_beyond_one_step(self):
        d=F(3,5)
        x=m.discounted_pd_prefix("F","T",d,3)
        self.assertEqual(x["row_discounted_total"],F(3)+d+d*d)
        self.assertEqual(x["row_discounted_total"]+m.discounted_pd_tail("F","T",d,3),F(9,2))
    def test_044_all_140_discount_prefix_and_exact_tail_checks(self):
        x=m.independent_longrun_source_test_audit()
        self.assertEqual(x["mathematically_exact_prefix_plus_tail_checks"],140)
    def test_045_source_delta_zero_not_stag_hunt(self):
        s=m.true_repeated_coordination_selection(F(0))
        self.assertFalse(s["two_strict_diagonal_Nash"])
        self.assertFalse(s["Trigger_Strict_Nash"])
    def test_046_at_delta_half_trigger_strict_False(self):
        s=m.true_repeated_coordination_selection(F(1,2))
        self.assertFalse(s["two_strict_diagonal_Nash"])
        self.assertFalse(s["Trigger_Strict_Nash"])
        self.assertTrue(s["Foole_Strict_Nash"])
    def test_047_delta_three_fifths_two_pure_strict_equilibria(self):
        self.assertTrue(m.true_repeated_coordination_selection(F(3,5))["two_strict_diagonal_Nash"])
    def test_048_delta_three_fifths_Foole_risk_dominant(self):
        self.assertEqual(m.true_repeated_coordination_selection(F(3,5))["risk_dominant"],"F")
    def test_049_delta_three_fifths_trigger_payoff_dominant(self):
        self.assertEqual(m.true_repeated_coordination_selection(F(3,5))["payoff_dominant"],"T")
    def test_050_delta_three_fifths_belief_two_thirds(self):
        self.assertEqual(m.true_repeated_coordination_selection(F(3,5))["threshold_opponent_Trigger"],F(2,3))
    def test_051_delta_two_thirds_risk_tie(self):
        s=m.true_repeated_coordination_selection(F(2,3))
        self.assertEqual(s["risk_dominant"],"TIE")
        self.assertEqual(s["threshold_opponent_Trigger"],F(1,2))
    def test_052_delta_three_quarters_trigger_risk_dominant(self):
        self.assertEqual(m.true_repeated_coordination_selection(F(3,4))["risk_dominant"],"T")
    def test_053_delta_one_excluded_from_infinite_payoffs(self):
        with self.assertRaises(m.StagHuntError):
            m.repeated_pd_infinite_payoffs(F(1))
    def test_054_discount_invalid_type_or_range(self):
        for d in (0,1,True,False,0.5,F(-1,3),F(5,4),"3/5"):
            with self.subTest(d=d),self.assertRaises(m.StagHuntError):
                m.repeated_pd_infinite_payoffs(d)
    def test_055_strategy_names_invalid(self):
        for name in ("X","C","D",None,0,True):
            with self.subTest(name=name),self.assertRaises(m.StagHuntError):
                m.discounted_pd_prefix(name,"T",F(1,2),1)
    def test_056_horizons_reject_0_bool_float_and_13(self):
        for horizon in (0,13,True,False,1.0,"5"):
            with self.subTest(h=horizon),self.assertRaises(m.StagHuntError):
                m.discounted_pd_prefix("T","F",F(1,2),horizon)
    def test_057_discounted_prefix_independent_from_closed_form(self):
        with patch.object(m,"repeated_pd_infinite_payoffs",side_effect=AssertionError("CLOSED_NOT_CALLED")):
            self.assertEqual(m.discounted_pd_prefix("T","T",F(3,5),1)["row_discounted_total"],2)
    def test_058_repeated_closed_form_independent_from_prefix(self):
        with patch.object(m,"discounted_pd_prefix",side_effect=AssertionError("PREFIX_NOT_CALLED")):
            self.assertEqual(m.repeated_pd_infinite_payoffs(F(3,5))[0][0],5)


class SourceInspiredDynamicsScopeTests(unittest.TestCase):
    def test_059_discrete_share_half_goes_to_two_fifths(self):
        self.assertEqual(m.source_inspired_project_discrete_share_step(F(1,2)),F(2,5))
    def test_060_discrete_share_four_fifths_goes_to_sixtyfour_79(self):
        self.assertEqual(m.source_inspired_project_discrete_share_step(F(4,5)),F(64,79))
    def test_061_discrete_share_fixed_points_zero_threequarters_one(self):
        for x in (F(0),F(3,4),F(1)):
            self.assertEqual(m.source_inspired_project_discrete_share_step(x),x)
    def test_062_discrete_down_below_threshold(self):
        for x in (F(1,10),F(1,2),F(2,3)):
            self.assertLess(m.source_inspired_project_discrete_share_step(x),x)
    def test_063_discrete_up_above_threshold(self):
        for x in (F(4,5),F(9,10),F(19,20)):
            self.assertGreater(m.source_inspired_project_discrete_share_step(x),x)
    def test_064_project_discrete_map_marked_not_original_2004_book(self):
        self.assertTrue(m.small_source_inspired_dynamics_audit()["discrete_map_project_not_book_formula"])
    def test_065_source_book_correct_basin_boundary_threequarters(self):
        self.assertEqual(m.small_source_inspired_dynamics_audit()["source_book_p11_basin_boundary"],"3/4")
    def test_066_source_research_receipt_explicit_zero_new_real_E2(self):
        self.assertEqual(m.project_research_receipt()["new_real_person_E2_prediction_scores"],0)
    def test_067_source_research_receipt_R073_PESEN_frozen(self):
        r=m.project_research_receipt()
        self.assertEqual((r["R073"],r["PESEN_v0_1"]),("FROZEN","FROZEN"))
    def test_068_model_scope_source_payoffs_not_original_real_human_actions(self):
        self.assertIn("not Skyrms human results",m.__doc__)
    def test_069_frozen_distribution_repeat_identical(self):
        self.assertEqual(m.frozen_correlated_trust_counterexample(),m.frozen_correlated_trust_counterexample())
    def test_070_frozen_source_transformation_repeat_identical(self):
        self.assertEqual(m.original_skyrms_printed_transformation(),m.original_skyrms_printed_transformation())


if __name__=="__main__":
    unittest.main()
