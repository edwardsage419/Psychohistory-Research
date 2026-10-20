"""R127: source AER 1990 Eq1, Table A, Table 2 and separate 2x2 math."""
import unittest
from fractions import Fraction as F
from itertools import product
from unittest.mock import patch
import r127_van_huyck_1990_min_effort_coordination_selection_exact as m


def game(a,b,c,d):
    return tuple(F(v) for v in (a,b,c,d))


class Exact1990CoordinationTests(unittest.TestCase):
    def test_original_primary_fulltext_and_1990_source(self):
        self.assertIn("Van Huyck",m.__doc__)
        self.assertIn("1990",m.__doc__)

    def test_original_theory_a_point_two_and_b_point_one(self):
        self.assertEqual((m.A,m.B),(F(1,5),F(1,10)))

    def test_original_experiment_A_has_extra_sixty_cents(self):
        self.assertEqual(m.EXPERIMENT_A_OFFSET,F(3,5))

    def test_original_theory_no_additive_offset_all_one(self):
        self.assertEqual(m.payoff_vector((1,1),experimental=False),(F(1,10),)*2)

    def test_original_experiment_A_all_sevens_each_one_thirty(self):
        self.assertEqual(m.payoff_vector((7,)*16),(F(13,10),)*16)

    def test_original_experiment_A_all_ones_each_point_seventy(self):
        self.assertEqual(m.payoff_vector((1,)*14),(F(7,10),)*14)

    def test_original_A_table_own_seven_min_one_payoff_point_ten(self):
        self.assertEqual(m.independent_payoff_from_others(7,(1,)*13),F(1,10))

    def test_original_A_table_own_six_min_three_payoff_point_sixty(self):
        self.assertEqual(m.independent_payoff_from_others(6,(3,4)),F(3,5))

    def test_original_A_table_own_five_min_five_one_ten(self):
        self.assertEqual(m.independent_payoff_from_others(5,(5,6)),F(11,10))

    def test_original_payoff_table_seven_by_seven_triangle(self):
        t=m.original_payoff_table_A()
        self.assertEqual(len(t),7)
        self.assertEqual(t["7"]["7"],"13/10")
        self.assertEqual(t["7"]["1"],"1/10")
        self.assertEqual(t["6"]["6"],"6/5")
        self.assertEqual(t["5"]["4"],"9/10")
        self.assertEqual(t["1"]["1"],"7/10")
        self.assertIsNone(t["1"]["7"])

    def test_original_payoff_table_all_valid_cells_match_independent_formula(self):
        t=m.original_payoff_table_A()
        for e in range(1,8):
            for q in range(1,e+1):
                self.assertEqual(t[str(e)][str(q)],
                                 str(m.independent_payoff_from_others(e,(q,7))))

    def test_unsupported_source_table_cell_min_greater_than_own_is_None(self):
        t=m.original_payoff_table_A()
        for e in range(1,8):
            for minimum in range(e+1,8):
                self.assertIsNone(t[str(e)][str(minimum)])

    def test_original_source_all_seven_equal_profiles_strict_nash(self):
        for e in range(1,8):
            self.assertTrue(m.strict_pure_nash_minimum_effort((e,)*4))

    def test_original_source_no_nonuniform_profile_strict_nash(self):
        for e in range(1,7):
            self.assertFalse(m.strict_pure_nash_minimum_effort((e,e+1,e)))

    def test_source_security_unique_minimax_effort_one(self):
        self.assertEqual(m.min_effort_security_and_payoff_rank()["unique_maximin_security_effort"],1)

    def test_original_security_payoff_by_own_effort(self):
        self.assertEqual(m.min_effort_security_and_payoff_rank()["own_choices_1_to7_worst_case_payoffs"],
                         ["7/10","3/5","1/2","2/5","3/10","1/5","1/10"])

    def test_source_payoff_dominant_all_seven_conflicts_security_one(self):
        x=m.min_effort_security_and_payoff_rank()
        self.assertEqual(x["source_payoff_dominant_effort"],7)
        self.assertEqual(x["unique_maximin_security_effort"],1)
        self.assertEqual((x["source_payoff_A_all7"],x["source_payoff_A_all1"]),("13/10","7/10"))

    def test_minimum_effort_best_reply_is_other_group_minimum(self):
        for e in range(1,8):
            self.assertEqual(m.strict_best_effort_against_others((e,7,7,7)),e)

    def test_minimum_effort_strict_below_and_above_opponents_min(self):
        others=(4,5,6)
        optimum=m.independent_payoff_from_others(4,others)
        self.assertTrue(all(optimum>m.independent_payoff_from_others(e,others)
                            for e in range(1,8) if e!=4))

    def test_source_A_experiment_sizes_107_published(self):
        x=m.published_1990_table2_verification()
        self.assertEqual(x["experiment_sizes"],[16,16,14,15,16,16,14])
        self.assertEqual(x["source_reported_human_participants_not_reanalyzed"],107)

    def test_source_first_round_choice_7_is_33(self):
        self.assertEqual(m.published_1990_table2_verification()[
            "original_published_aggregate_first_period_choice_7"],33)

    def test_source_first_round_choice_1_is_2(self):
        self.assertEqual(m.published_1990_table2_verification()[
            "original_published_aggregate_first_period_choice_1"],2)

    def test_source_final_round_choice_1_is_77(self):
        self.assertEqual(m.published_1990_table2_verification()[
            "original_published_aggregate_final_period_choice_1"],77)

    def test_source_original_text_31_and_72_percent_rounding(self):
        self.assertEqual(round(F(33,107)*100),31)
        self.assertEqual(round(F(77,107)*100),72)

    def test_source_final_round_every_group_minimum_equals_one(self):
        self.assertEqual(set(m.published_1990_table2_verification()[
            "period10_group_minimums"].values()),{1})

    def test_source_first_round_minima_per_original_table(self):
        self.assertEqual(m.published_1990_table2_verification()[
            "period1_group_minimums"],{"1":2,"2":2,"3":4,"4":4,"5":3,"6":1,"7":1})

    def test_source_table2_no_claim_about_person_level_transitions(self):
        x=m.published_1990_table2_verification()
        self.assertFalse(x["individual_level_transition_matrix_identified_from_printed_counts"])
        self.assertEqual(x["new_real_human_E2_prediction_scores"],0)

    def test_source_experiment_1_count_profiles_both_periods(self):
        self.assertEqual(m.SOURCE_TABLE2[1]["period1"],(8,3,2,1,1,1,0))
        self.assertEqual(m.SOURCE_TABLE2[1]["period10"],(1,0,0,0,1,1,13))

    def test_source_experiment_7_count_profiles_both_periods(self):
        self.assertEqual(m.SOURCE_TABLE2[7]["period1"],(4,1,2,4,1,1,1))
        self.assertEqual(m.SOURCE_TABLE2[7]["period10"],(1,0,0,0,0,3,10))

    def test_source_table2_all_session_vectors_sum_to_original_sample_sizes(self):
        for ex,x in m.SOURCE_TABLE2.items():
            with self.subTest(ex=ex):
                self.assertEqual(sum(x["period1"]),x["n"])
                self.assertEqual(sum(x["period10"]),x["n"])

    def test_count_of_seven_actions_at_final_not_zero(self):
        self.assertEqual(sum(x["period10"][0] for x in m.SOURCE_TABLE2.values()),8)

    def test_test_exhaustive_2793_profiles_and_75117_deviations(self):
        x=m.exhaustive_original_min_effort_payoff_audit()
        self.assertEqual(x["exact_profiles_by_group_size"],{"2":49,"3":343,"4":2401})
        self.assertEqual(x["all_original_payoff_profiles"],2793)
        self.assertEqual(x["all_exact_individual_candidate_deviations"],75117)

    def test_all_exhaustive_games_have_seven_diagonal_equilibria_each(self):
        x=m.exhaustive_original_min_effort_payoff_audit()
        self.assertEqual(x["strict_diagonal_Nash_by_group_size"],{"2":7,"3":7,"4":7})

    def test_min_effort_payoff_algorithm_no_others_function_call(self):
        with patch.object(m,"independent_payoff_from_others",side_effect=AssertionError("NO_OTHERS")):
            self.assertEqual(m.payoff_vector((2,3,4)),(F(4,5),F(7,10),F(3,5)))

    def test_independent_others_payoff_does_not_call_group_payoff(self):
        with patch.object(m,"payoff_vector",side_effect=AssertionError("NO_GROUP")):
            self.assertEqual(m.independent_payoff_from_others(4,(2,7)),F(3,5))

    def test_distinguish_experimental_cash_vs_theoretical_equation(self):
        e=(4,6,7)
        cash=m.payoff_vector(e,True)
        theory=m.payoff_vector(e,False)
        self.assertEqual(tuple(c-t for c,t in zip(cash,theory)),(F(3,5),)*3)

    def test_risk_conflict_source_not_claimed_1990_original_participants(self):
        self.assertTrue(m.frozen_two_person_examples()["not_the_Van_Huyck_1990_n_agent_original_game"])

    def test_2x2_risk_payoff_conflict_dual_diagonal_Nash(self):
        self.assertEqual(m.pure_nash_profiles(*game(5,0,4,4)),((0,0),(1,1)))

    def test_2x2_risk_payoff_conflict_A_is_pareto_dominant(self):
        self.assertEqual(m.payoff_risk_selection(*game(5,0,4,4))["payoff_dominant"],"A")

    def test_2x2_risk_payoff_conflict_B_is_risk_dominant(self):
        self.assertEqual(m.payoff_risk_selection(*game(5,0,4,4))["risk_dominant"],"B")

    def test_2x2_risk_deviation_loss_products_one_and_sixteen(self):
        s=m.payoff_risk_selection(*game(5,0,4,4))
        self.assertEqual((s["A_loss_product"],s["B_loss_product"]),(F(1),F(16)))

    def test_2x2_risk_threshold_exact_four_fifths(self):
        self.assertEqual(m.payoff_risk_selection(*game(5,0,4,4))[
            "belief_opponent_A_indifference"],F(4,5))

    def test_2x2_expected_payoffs_at_three_quarters_choose_B(self):
        self.assertEqual(m.independent_expected_payoff_differences(
            *game(5,0,4,4),F(3,4))["best"],"B")

    def test_2x2_expected_payoffs_at_nine_tenths_choose_A(self):
        self.assertEqual(m.independent_expected_payoff_differences(
            *game(5,0,4,4),F(9,10))["best"],"A")

    def test_2x2_expected_payoffs_at_exact_threshold_tie(self):
        s=m.independent_expected_payoff_differences(*game(5,0,4,4),F(4,5))
        self.assertEqual(s["best"],"TIE")
        self.assertEqual(s["expected_A"],s["expected_B"])

    def test_symmetric_coordination_cross_payoffs_differ_between_players(self):
        self.assertEqual(m.bimatrix_payoffs(*game(5,0,4,4)),
                         (((F(5),F(5)),(F(0),F(4))),
                          ((F(4),F(0)),(F(4),F(4)))))

    def test_source_independent_risk_threshold_tie_example(self):
        s=m.payoff_risk_selection(*game(4,0,2,2))
        self.assertEqual(s["risk_dominant"],"TIE")
        self.assertEqual(s["payoff_dominant"],"A")
        self.assertEqual(s["belief_opponent_A_indifference"],F(1,2))

    def test_risk_tie_does_not_force_B(self):
        self.assertEqual(m.frozen_two_person_examples()["equal_risk_selection"],"TIE")

    def test_risk_dominance_requires_two_strict_diagonal_Nash(self):
        for v in ((F(1),F(2),F(0),F(0)),(F(0),F(0),F(0),F(0)),
                  (F(2),F(1),F(2),F(3))):
            with self.subTest(v=v),self.assertRaises(m.CoordinationAuditError):
                m.payoff_risk_selection(*v)

    def test_positive_affine_payoff_shift_preserves_risk_and_payoff_selection(self):
        vals=game(5,0,4,4)
        initial=m.payoff_risk_selection(*vals)
        after=m.payoff_risk_selection(*(v*2+F(9) for v in vals))
        self.assertEqual((initial["risk_dominant"],initial["payoff_dominant"]),
                         (after["risk_dominant"],after["payoff_dominant"]))
        self.assertEqual(initial["belief_opponent_A_indifference"],
                         after["belief_opponent_A_indifference"])

    def test_source_based_2x2_1296_grid_complete(self):
        x=m.exhaustive_two_player_symmetric_payoff_grid()
        self.assertEqual(x["all_two_by_two_symmetric_integer_payoff_games"],1296)
        self.assertGreater(x["two_strict_diagonal_Nash_games"],0)
        self.assertGreater(x["payoff_vs_risk_strict_conflict_games"],0)

    def test_source_based_2x2_1296_grid_has_equal_risk_cases(self):
        self.assertGreater(m.exhaustive_two_player_symmetric_payoff_grid()["two_equilibria_risk_tie_games"],0)

    def test_2x2_payoff_only_accepts_Fraction_no_float_or_int(self):
        for bad in (0,1.0,True,None,"5"):
            with self.subTest(bad=bad),self.assertRaises(m.CoordinationAuditError):
                m.payoff_risk_selection(bad,F(0),F(1),F(2))

    def test_2x2_probability_input_must_be_exact_range(self):
        for bad in (0,1,True,F(-1,10),F(11,10),0.5,"1/2"):
            with self.subTest(bad=bad),self.assertRaises(m.CoordinationAuditError):
                m.independent_expected_payoff_differences(*game(5,0,4,4),bad)

    def test_effort_invalid_n_float_bool_strings_rejected(self):
        for bad in ((),(1,),(1,)*17,(1,True),("2",3),(0,2),(1,8),(1,1.0),(x for x in (1,2))):
            with self.subTest(value=str(bad)),self.assertRaises(m.CoordinationAuditError):
                m.payoff_vector(bad)

    def test_min_effort_best_response_invalid_others_rejected(self):
        for bad in ((),(1,)*16,(True,),(8,),[0],(x for x in (1,))):
            with self.subTest(value=str(bad)),self.assertRaises(m.CoordinationAuditError):
                m.strict_best_effort_against_others(bad)

    def test_undocumented_experimental_offset_flag_fails_closed(self):
        with self.assertRaises(m.CoordinationAuditError):
            m.payoff_vector((1,2),experimental=1)

    def test_group_size_16_supported_and_17_rejected(self):
        self.assertEqual(len(m.payoff_vector((7,)*16)),16)
        with self.assertRaises(m.CoordinationAuditError):
            m.payoff_vector((7,)*17)

    def test_empirical_evidence_level_no_person_level_E2(self):
        rec=m.published_1990_table2_verification()
        self.assertEqual(rec["new_real_human_E2_prediction_scores"],0)

    def test_all_results_deterministic(self):
        self.assertEqual(m.min_effort_security_and_payoff_rank(),m.min_effort_security_and_payoff_rank())


if __name__=="__main__":
    unittest.main()
