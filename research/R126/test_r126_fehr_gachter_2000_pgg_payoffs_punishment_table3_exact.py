"""R126 first-hand Fehr-Gächter (2000) PGG payoffs and printed-aggregate tests."""
import unittest
from fractions import Fraction as F
from itertools import product
from unittest.mock import patch
import r126_fehr_gachter_2000_pgg_payoffs_punishment_table3_exact as m


class Original2000PublicGoodsMechanismTests(unittest.TestCase):
    def test_original_article_doi_identified(self):
        self.assertIn("10.1257/aer.90.4.980",m.__doc__)

    def test_source_four_people_each_twenty_endowment_and_alpha_two_fifths(self):
        self.assertEqual((m.N,m.ENDOWMENT,m.ALPHA),(4,20,F(2,5)))

    def test_source_cost_table_exact_all_eleven_levels(self):
        self.assertEqual(m.PUNISHMENT_COST,(0,1,2,4,6,9,12,16,20,25,30))

    def test_source_cost_table_nonlinear_not_single_token_each(self):
        self.assertEqual(m.punishment_cost(3),4)
        self.assertEqual(m.punishment_cost(10),30)
        self.assertNotEqual(m.punishment_cost(10),10)

    def test_cost_increments_positive_all_source_levels(self):
        increments=tuple(m.punishment_cost(k)-m.punishment_cost(k-1) for k in range(1,11))
        self.assertEqual(increments,(1,1,2,2,3,3,4,4,5,5))

    def test_all_zero_private_payoff_twenty_each(self):
        self.assertEqual(m.stage1_payoff((0,0,0,0)),(F(20),)*4)

    def test_all_zero_social_sum_eighty(self):
        self.assertEqual(m.independent_stage1_group_surplus((0,)*4),80)

    def test_all_twenty_private_payoff_thirtytwo_each(self):
        self.assertEqual(m.stage1_payoff((20,)*4),(F(32),)*4)

    def test_all_twenty_social_sum_one_hundred_twenty_eight(self):
        self.assertEqual(m.independent_stage1_group_surplus((20,)*4),128)

    def test_one_token_lone_contributor_has_payoff_nineteen_point_four(self):
        self.assertEqual(m.stage1_payoff((1,0,0,0))[0],F(97,5))

    def test_one_token_lone_contributor_gives_others_twenty_point_four(self):
        self.assertEqual(m.stage1_payoff((1,0,0,0))[1:],(F(102,5),)*3)

    def test_one_token_lone_contributor_total_positive_group_gain_three_fifths(self):
        self.assertEqual(m.independent_stage1_group_surplus((1,0,0,0)),F(403,5))

    def test_private_marginal_negative_three_fifths(self):
        self.assertEqual(m.independent_marginal_incentives()["one_extra_token_private_gain"],F(-3,5))

    def test_group_marginal_positive_three_fifths(self):
        self.assertEqual(m.independent_marginal_incentives()["one_extra_token_total_group_gain"],F(3,5))

    def test_source_selfish_stage_game_best_contribute_zero(self):
        self.assertEqual(m.independent_marginal_incentives()["single_round_selfish_best_contribution"],0)

    def test_social_first_stage_optimum_each_twenty(self):
        self.assertEqual(m.independent_marginal_incentives()["first_stage_social_optimum_each_contribution"],20)

    def test_10_period_pure_selfish_backward_induction_benchmark_zero(self):
        x=m.independent_marginal_incentives()
        self.assertEqual(x["finite_ten_round_pure_money_common_knowledge_SPNE_contribution"],0)
        self.assertEqual(x["finite_ten_round_pure_money_common_knowledge_SPNE_sent_punishment"],0)

    def test_source_2000_20_20_20_0_first_stage_payoffs(self):
        self.assertEqual(m.stage1_payoff((20,20,20,0)),(F(24),F(24),F(24),F(44)))

    def test_source_2000_20_20_20_0_group_surplus(self):
        self.assertEqual(m.independent_stage1_group_surplus((20,20,20,0)),116)

    def test_all_zero_punishment_unchanged_from_first_stage(self):
        g=(20,20,20,0)
        self.assertEqual(m.punishment_payoff(g,m.zero_punishment()),m.stage1_payoff(g))

    def test_one_and_two_points_target_receives_three(self):
        p=((0,0,0,1),(0,0,0,2),(0,0,0,0),(0,0,0,0))
        self.assertEqual(m.effective_received_points(p),(0,0,0,3))

    def test_one_and_two_points_target_payoff_thirty_point_eight(self):
        p=((0,0,0,1),(0,0,0,2),(0,0,0,0),(0,0,0,0))
        self.assertEqual(m.punishment_payoff((20,20,20,0),p)[3],F(154,5))

    def test_one_and_two_points_punishers_pay_one_and_two_token_costs(self):
        p=((0,0,0,1),(0,0,0,2),(0,0,0,0),(0,0,0,0))
        self.assertEqual(m.punishment_payoff((20,20,20,0),p)[:3],(F(23),F(22),F(24)))

    def test_one_and_two_points_four_net_payoffs_total_499_fifths(self):
        p=((0,0,0,1),(0,0,0,2),(0,0,0,0),(0,0,0,0))
        self.assertEqual(m.independent_punishment_group_surplus((20,20,20,0),p),F(499,5))

    def test_two_independent_punishment_methods_exact_same_total(self):
        p=((0,0,0,1),(0,0,0,2),(0,0,0,0),(0,0,0,0))
        self.assertEqual(sum(m.punishment_payoff((20,20,20,0),p),F(0)),
                         m.independent_punishment_group_surplus((20,20,20,0),p))

    def test_punishment_total_independent_of_person_aggregation(self):
        with patch.object(m,"punishment_payoff",side_effect=AssertionError("FORBIDDEN")):
            self.assertEqual(m.independent_punishment_group_surplus(
                (20,20,20,0),((0,0,0,1),(0,0,0,2),(0,0,0,0),(0,0,0,0))),F(499,5))

    def test_punishment_individual_payoff_independent_of_group_aggregation(self):
        with patch.object(m,"independent_punishment_group_surplus",side_effect=AssertionError("FORBIDDEN")):
            self.assertEqual(m.punishment_payoff((20,20,20,0),m.zero_punishment())[3],44)

    def test_multiple_sender_points_over_ten_are_capped(self):
        p=((0,0,0,6),(0,0,0,7),(0,0,0,10),(0,0,0,0))
        self.assertEqual(m.effective_received_points(p)[3],10)

    def test_multiple_sender_twenty_three_raw_points_target_gets_zero_first_payoff(self):
        p=((0,0,0,6),(0,0,0,7),(0,0,0,10),(0,0,0,0))
        self.assertEqual(m.punishment_payoff((20,20,20,0),p)[3],0)

    def test_multiple_sender_twenty_three_points_cost_fifty_eight(self):
        self.assertEqual(sum((m.punishment_cost(k) for k in (6,7,10)),F(0)),58)

    def test_multiple_sender_twenty_three_points_total_social_fourteen(self):
        p=((0,0,0,6),(0,0,0,7),(0,0,0,10),(0,0,0,0))
        self.assertEqual(m.independent_punishment_group_surplus((20,20,20,0),p),14)

    def test_punisher_net_payoff_can_be_negative_without_extra_cap(self):
        p=((0,0,0,6),(0,0,0,7),(0,0,0,10),(0,0,0,0))
        self.assertEqual(m.punishment_payoff((20,20,20,0),p)[2],F(-6))

    def test_punish_receiver_same_stage_payoff_fractional_discount_not_fixed_three(self):
        p=((0,0,0,1),(0,0,0,0),(0,0,0,0),(0,0,0,0))
        baseline=m.stage1_payoff((20,20,20,0))[3]
        self.assertEqual(baseline-m.punishment_payoff((20,20,20,0),p)[3],F(22,5))

    def test_multiple_targets_costs_separately_nonlinear(self):
        p=((0,2,3,0),(0,0,0,0),(0,0,0,0),(0,0,0,0))
        assert_sum=sum(m.punishment_payoff((0,0,0,0),p),F(0))
        self.assertEqual(assert_sum,m.independent_punishment_group_surplus((0,0,0,0),p))
        self.assertEqual(m.punishment_payoff((0,0,0,0),p)[0],F(14))

    def test_published_Table3_all_three_session_values_exact(self):
        self.assertEqual(m.TABLE3_PRINTED_SESSIONS[1],(F(27,10),F(109,10),F(13,10),F(98,10)))
        self.assertEqual(m.TABLE3_PRINTED_SESSIONS[2],(F(4),F(129,10),F(23,10),F(143,10)))
        self.assertEqual(m.TABLE3_PRINTED_SESSIONS[3],(F(9,2),F(107,10),F(2),F(131,10)))

    def test_published_Table3_original_printed_mean_row_must_be_12_point_three_final(self):
        self.assertEqual(m.TABLE3_PRINTED_MEAN,(F(37,10),F(23,2),F(19,10),F(123,10)))

    def test_published_Table3_session1_overall_difference_8_point_two(self):
        self.assertEqual(m.TABLE3_PRINTED_SESSIONS[1][1]-m.TABLE3_PRINTED_SESSIONS[1][0],F(41,5))

    def test_published_Table3_session2_overall_difference_8_point_nine(self):
        self.assertEqual(m.TABLE3_PRINTED_SESSIONS[2][1]-m.TABLE3_PRINTED_SESSIONS[2][0],F(89,10))

    def test_published_Table3_session3_overall_difference_6_point_two(self):
        self.assertEqual(m.TABLE3_PRINTED_SESSIONS[3][1]-m.TABLE3_PRINTED_SESSIONS[3][0],F(31,5))

    def test_published_Table3_all_sessions_printed_punishment_means_above_no(self):
        for row in m.TABLE3_PRINTED_SESSIONS.values():
            self.assertTrue(row[1]>row[0] and row[3]>row[2])

    def test_published_Table3_final_punished_equal_mean_of_displayed_session_rows_12_point_four(self):
        self.assertEqual(sum((row[3] for row in m.TABLE3_PRINTED_SESSIONS.values()),F(0))/3,F(62,5))

    def test_published_Table3_last_punishment_mean_row_discrepancy_flagged(self):
        x=m.printed_table3_audit()
        self.assertEqual(x["source_published_Mean_row"][3],"123/10")
        self.assertEqual(x["independent_equal_session_average_of_PRINTED_rows"][3],"62/5")
        self.assertEqual(x["last_punishment_published_Mean_minus_equal_average_PRINTED_rows"],"-1/10")
        self.assertTrue(x["last_punishment_printed_row_mean_discrepancy_unresolved"])

    def test_published_Table3_2000_real_humans_only_as_original_authors_count(self):
        x=m.printed_table3_audit()
        self.assertEqual(x["source_human_subjects_reported_by_authors_not_loaded_as_microdata"],112)
        self.assertEqual(x["individual_level_E2_scores"],0)

    def test_published_Table3_does_not_claim_reestimation_of_Wilcoxon(self):
        self.assertTrue(m.printed_table3_audit()["not_a_reproduction_of_original_Wilcoxon_p_value"])

    def test_published_Table3_contribution_fractions_printed_mean_over_twenty(self):
        x=m.printed_table3_audit()
        self.assertEqual(x["published_overall_punishment_contribution_fraction_endowment"],"23/40")
        self.assertEqual(x["published_overall_no_punishment_contribution_fraction_endowment"],"37/200")

    def test_strict_contribution_domain_rejects_bad_container_and_length(self):
        for bad in ((),(0,0,0),(0,0,0,0,0),"0000",(i for i in range(4))):
            with self.subTest(case=str(type(bad))),self.assertRaises(m.PGGAuditError):
                m.stage1_payoff(bad)

    def test_strict_contribution_domain_rejects_nonint_boolean_negative_out_of_range(self):
        for bad in (True,False,F(1),1.0,-1,21,"20",None):
            with self.subTest(value=bad),self.assertRaises(m.PGGAuditError):
                m.stage1_payoff((0,0,0,bad))

    def test_punishment_matrix_rejects_wrong_shape(self):
        for bad in ((),((0,)*4,)*3,((0,)*5,)*4,"0000"):
            with self.subTest(case=str(type(bad))),self.assertRaises(m.PGGAuditError):
                m.punishment_payoff((0,)*4,bad)

    def test_punishment_matrix_rejects_nonint_invalid_point_levels(self):
        for bad in (True,False,F(1),0.5,-1,11,"1",None):
            p=[[0]*4 for _ in range(4)]
            p[0][1]=bad
            with self.subTest(k=bad),self.assertRaises(m.PGGAuditError):
                m.punishment_payoff((0,)*4,p)

    def test_punishment_matrix_self_target_must_be_zero(self):
        p=[[0]*4 for _ in range(4)]
        p[0][0]=1
        with self.assertRaisesRegex(m.PGGAuditError,"SELF"):
            m.punishment_payoff((0,)*4,p)

    def test_source_table2_cost_rejects_invalid_int_or_bool(self):
        for bad in (True,False,F(1),1.0,-1,11,"3"):
            with self.subTest(k=bad),self.assertRaises(m.PGGAuditError):
                m.punishment_cost(bad)

    def test_frozen_source_independent_report_expected_values(self):
        x=m.project_frozen_exact_cases()
        self.assertEqual(x["all_zero_stage1_group"],"80")
        self.assertEqual(x["all_twenty_stage1_group"],"128")
        self.assertEqual(x["three_twenty_one_zero_group_stage1"],"116")
        self.assertEqual(x["one_and_two_points_sent_stage2_group"],"499/5")
        self.assertEqual(x["saturated_group_net_surplus"],"14")

    def test_625_synthetic_profiles_and_52500_best_response_checks(self):
        x=m.exhaustive_mathematical_incentives()
        self.assertEqual(x["purely_mathematical_contribution_profiles"],625)
        self.assertEqual(x["player_specific_0_to20_deviation_checks"],52500)

    def test_all_possible_21_costs_and_one_target_punishment_11_cube_exact(self):
        g=(20,20,20,0)
        for a,b,c in product(range(11),repeat=3):
            p=((0,0,0,a),(0,0,0,b),(0,0,0,c),(0,0,0,0))
            self.assertEqual(sum(m.punishment_payoff(g,p),F(0)),
                             m.independent_punishment_group_surplus(g,p))

    def test_all_625_profile_source_eq1_vs_social_surplus_under_deterministic_punishment(self):
        for g in product((0,5,10,15,20),repeat=4):
            p=tuple(tuple(0 if i==j else ((g[i]+2*g[j]+i+j)%11)
                          for j in range(4)) for i in range(4))
            self.assertEqual(sum(m.punishment_payoff(g,p),F(0)),
                             m.independent_punishment_group_surplus(g,p))

    def test_no_cross_project_R105_CPR_as_E2(self):
        self.assertEqual(m.published_model_receipt()["new_real_person_predictive_E2_scores"],0)
        self.assertTrue(m.published_model_receipt()["different_source_than_R105_2024_CPR_Zenodo"])

    def test_frozen_research_baselines_not_changed(self):
        x=m.published_model_receipt()
        self.assertEqual((x["R073"],x["PESEN_v0_1"]),("FROZEN","FROZEN"))


if __name__=="__main__":
    unittest.main()
