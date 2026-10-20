"""R130 true first-party Science1981 and Nature1993 source-level math tests."""
import unittest
from fractions import Fraction as F
from itertools import product
from unittest.mock import patch
import r130_axelrod1981_tft_nowak1993_pavlov_repeated_exact as m


class Original1981AxelrodTwoIndependentConstraints(unittest.TestCase):
    def test_001_primary_source_science_1981_doi(self):
        self.assertIn("10.1126/science.7466396",m.__doc__)

    def test_002_true_original_R_S_T_P_values(self):
        self.assertEqual((m.REWARD,m.SUCKER,m.TEMPTATION,m.PUNISHMENT),
                         (F(3),F(0),F(5),F(1)))

    def test_003_original_PD_order_T_R_P_S(self):
        self.assertGreater(m.TEMPTATION,m.REWARD)
        self.assertGreater(m.REWARD,m.PUNISHMENT)
        self.assertGreater(m.PUNISHMENT,m.SUCKER)
        self.assertGreater(2*m.REWARD,m.TEMPTATION+m.SUCKER)

    def test_004_original_each_CC_payoff_three(self):
        self.assertEqual(m.stage_payoffs("C","C"),(F(3),F(3)))

    def test_005_original_C_D_payoff_zero_five(self):
        self.assertEqual(m.stage_payoffs("C","D"),(F(0),F(5)))

    def test_006_original_D_C_payoff_five_zero(self):
        self.assertEqual(m.stage_payoffs("D","C"),(F(5),F(0)))

    def test_007_original_D_D_payoff_one_each(self):
        self.assertEqual(m.stage_payoffs("D","D"),(F(1),F(1)))

    def test_008_original_TFT_ALWAYS_cooperates_first(self):
        self.assertEqual(m.policy_choice("TFT",None,None,0),"C")

    def test_009_original_TFT_next_mirrors_opponent_D(self):
        self.assertEqual(m.policy_choice("TFT","C","D",1),"D")

    def test_010_original_TFT_next_mirrors_opponent_C(self):
        self.assertEqual(m.policy_choice("TFT","D","C",1),"C")

    def test_011_original_alternator_first_D_second_C(self):
        self.assertEqual([m.policy_choice("ALT_DC",None,None,0),
                          m.policy_choice("ALT_DC","D","C",1),
                          m.policy_choice("ALT_DC","C","D",2)],["D","C","D"])

    def test_012_alld_vs_tft_first_D_C_then_D_D(self):
        seq=m.simulate_explicit_rounds("ALLD","TFT",4)
        self.assertEqual([x["row"]+x["col"] for x in seq],["DC","DD","DD","DD"])

    def test_013_alt_vs_tft_rounds_exact_D_C_and_C_D(self):
        seq=m.simulate_explicit_rounds("ALT_DC","TFT",6)
        self.assertEqual([x["row"]+x["col"] for x in seq],["DC","CD","DC","CD","DC","CD"])

    def test_014_tft_self_every_CC(self):
        seq=m.simulate_explicit_rounds("TFT","TFT",8)
        self.assertEqual({x["row"]+x["col"] for x in seq},{"CC"})

    def test_015_original_TFT_SELF_at_w3_over5_fifteen_halves(self):
        self.assertEqual(m.original_1981_stability_formulas(F(3,5))["original_tft_self_payoff"],F(15,2))

    def test_016_original_ALLD_vs_TFT_at_w3_over5_thirteen_halves(self):
        self.assertEqual(m.original_1981_stability_formulas(F(3,5))["original_alld_vs_tft_payoff"],F(13,2))

    def test_017_original_ALT_vs_TFT_at_w3_over5_125_over16(self):
        self.assertEqual(m.original_1981_stability_formulas(F(3,5))["original_alternating_DC_vs_tft_payoff"],F(125,16))

    def test_018_frozen_two_boundaries_are_half_and_two_thirds(self):
        x=m.original_1981_stability_formulas(F(3,5))
        self.assertEqual((x["original_alld_noninvading_boundary"],
                          x["original_alt_DC_noninvading_boundary"]),(F(1,2),F(2,3)))

    def test_019_w3_over5_ALLD_not_better_but_ALT_better(self):
        x=m.original_1981_stability_formulas(F(3,5))
        self.assertTrue(x["original_alld_not_better_than_TFT_self"])
        self.assertFalse(x["original_alt_DC_not_better_than_TFT_self"])
        self.assertFalse(x["both_printed_payoff_defenses_hold"])

    def test_020_w0_both_invaders_better_than_TFT(self):
        x=m.original_1981_stability_formulas(F(0))
        self.assertEqual((x["original_tft_self_payoff"],
                          x["original_alld_vs_tft_payoff"],
                          x["original_alternating_DC_vs_tft_payoff"]),(3,5,5))
        self.assertFalse(x["both_printed_payoff_defenses_hold"])

    def test_021_w_half_ALLD_ties_TFT_but_ALT_better(self):
        x=m.original_1981_stability_formulas(F(1,2))
        self.assertEqual((x["original_tft_self_payoff"],
                          x["original_alld_vs_tft_payoff"],
                          x["original_alternating_DC_vs_tft_payoff"]),
                         (F(6),F(6),F(20,3)))

    def test_022_w_two_thirds_ALT_ties_TFT_and_both_pass_noninvasion(self):
        x=m.original_1981_stability_formulas(F(2,3))
        self.assertEqual((x["original_tft_self_payoff"],
                          x["original_alternating_DC_vs_tft_payoff"]),(F(9),F(9)))
        self.assertTrue(x["both_printed_payoff_defenses_hold"])

    def test_023_original_primary_exact_formulas_against_full_independent_cycles(self):
        x=m.audit_original_1981_double_constraint()
        self.assertEqual((x["original_source_1981_TFT_ALLD_payoff_boundary"],
                          x["original_source_1981_TFT_ALT_DC_payoff_boundary"]),("1/2","2/3"))
        self.assertEqual(x["w_grid_exact_independent_closed_forms_against_state_cycles"]["3/5"][
            "ALT_DC_vs_TFT"],"125/16")

    def test_024_original_1981_not_completely_reproving_full_ESS(self):
        self.assertFalse(m.audit_original_1981_double_constraint()[
            "original_full_strategy_evolutionary_stability_theorem_newly_reproved"])

    def test_025_closed_form_does_not_call_finite_state_cycle(self):
        with patch.object(m,"independent_infinite_state_cycle_value",
                          side_effect=AssertionError("NO_CYCLE")):
            self.assertEqual(m.original_1981_stability_formulas(F(1,2))[
                "original_tft_self_payoff"],F(6))


class SourceNature1993PavlovAndOneExecutionError(unittest.TestCase):
    def test_026_primary_1993_nature_doi_identified(self):
        self.assertIn("10.1038/364056a0",m.__doc__)

    def test_027_source_Nature_R_S_T_P_memory_response(self):
        self.assertEqual(m.pavlov_original_1993_realized_action_mapping(),
                         {"CC":"C","CD":"D","DC":"D","DD":"C"})

    def test_028_pavlov_initial_cooperation(self):
        self.assertEqual(m.policy_choice("WSLS",None,None,0),"C")

    def test_029_pavlov_previous_reward_keeps_C(self):
        self.assertEqual(m.policy_choice("WSLS","C","C",1),"C")

    def test_030_pavlov_previous_sucker_switches_C_to_D(self):
        self.assertEqual(m.policy_choice("WSLS","C","D",1),"D")

    def test_031_pavlov_previous_temptation_keeps_D(self):
        self.assertEqual(m.policy_choice("WSLS","D","C",1),"D")

    def test_032_pavlov_previous_punishment_switches_D_to_C(self):
        self.assertEqual(m.policy_choice("WSLS","D","D",1),"C")

    def test_033_forced_first_round_tft_both_one_error_cycle(self):
        self.assertEqual(m.single_first_round_implementation_error("TFT",8),
                         ("DC","CD","DC","CD","DC","CD","DC","CD"))

    def test_034_forced_first_round_pavlov_recovers_on_round3(self):
        self.assertEqual(m.single_first_round_implementation_error("WSLS",8),
                         ("DC","DD","CC","CC","CC","CC","CC","CC"))

    def test_035_errors_change_executed_action_but_strategy_remains_tft(self):
        first=m.simulate_explicit_rounds("TFT","TFT",1,initial_forced_row="D")
        second=m.simulate_explicit_rounds("TFT","TFT",2,initial_forced_row="D")
        self.assertEqual((first[0]["row"],first[0]["col"]),("D","C"))
        self.assertEqual((second[1]["row"],second[1]["col"]),("C","D"))

    def test_036_pavlov_unforced_self_play_all_CC(self):
        self.assertEqual({z["row"]+z["col"] for z in m.simulate_explicit_rounds("WSLS","WSLS",8)},
                         {"CC"})

    def test_037_tft_one_sided_error_not_equivalent_pavlov(self):
        self.assertNotEqual(m.single_first_round_implementation_error("TFT",8),
                            m.single_first_round_implementation_error("WSLS",8))

    def test_038_original_1993_population_simulation_not_claimed_replayed(self):
        self.assertFalse(m.exhaustive_true_finite_vs_infinite_checks()[
            "original_1993_Nowak_population_mutation_selection_simulation_rerun"])


class InfiniteFiniteStateReproducibilityAndKnownFiniteHorizon(unittest.TestCase):
    def test_039_five_explicit_strategy_names(self):
        self.assertEqual(m.STRATEGIES,("TFT","ALLD","ALLC","ALT_DC","WSLS"))

    def test_040_tft_self_exact_cycle_has_cooperation(self):
        x=m.detect_finite_state_prefix_cycle("TFT","TFT")
        self.assertEqual(x["cycle_actions"],(("C","C"),("C","C")))
        self.assertEqual(x["cycle_length"],2)

    def test_041_alternator_vs_tft_exact_cycle_payoffs(self):
        x=m.detect_finite_state_prefix_cycle("ALT_DC","TFT")
        self.assertEqual(x["cycle_actions"],(("D","C"),("C","D")))
        self.assertEqual(x["cycle_length"],2)

    def test_042_alld_vs_tft_reaches_permanent_D_D(self):
        x=m.detect_finite_state_prefix_cycle("ALLD","TFT")
        self.assertEqual(set(x["cycle_actions"]),{("D","D")})

    def test_043_state_cycle_no_dependence_on_explicit_prefix_simulator(self):
        with patch.object(m,"simulate_explicit_rounds",side_effect=AssertionError("NO_SIM")):
            self.assertEqual(m.independent_infinite_state_cycle_value(
                "TFT","TFT",F(3,5)),(F(15,2),F(15,2)))

    def test_044_explicit_prefix_does_not_call_periodic_decomposition(self):
        with patch.object(m,"detect_finite_state_prefix_cycle",side_effect=AssertionError("NO_CYCLE")):
            self.assertEqual(m.discounted_explicit_prefix(
                "TFT","TFT",F(1,2),3),(F(21,4),F(21,4)))

    def test_045_independent_tail_matches_direct_one_round_discount_value(self):
        w=F(3,5)
        prefix=m.discounted_explicit_prefix("TFT","TFT",w,1)
        tail=m.independent_state_cycle_tail("TFT","TFT",w,1)
        self.assertEqual((prefix,tail),
                         ((F(3),F(3)),(F(9,2),F(9,2))))

    def test_046_infinite_tft_self_reward_over_one_minus_discount(self):
        for w in m.DELTA_GRID:
            with self.subTest(w=w):
                self.assertEqual(m.independent_infinite_state_cycle_value(
                    "TFT","TFT",w)[0],m.REWARD/(1-w))

    def test_047_infinite_alld_self_punishment_over_one_minus_discount(self):
        for w in m.DELTA_GRID:
            self.assertEqual(m.independent_infinite_state_cycle_value(
                "ALLD","ALLD",w),(F(1)/(1-w),)*2)

    def test_048_finite_1to12_exhaustive_full_1050_crosschecks(self):
        x=m.exhaustive_true_finite_vs_infinite_checks()
        self.assertEqual(x["exact_finite_prefix_plus_independent_periodic_tail_checks"],1050)
        self.assertEqual(x["all_ordered_two_strategy_profiles"],25)

    def test_049_1050_checks_all_use_exact_fraction(self):
        self.assertTrue(m.exhaustive_true_finite_vs_infinite_checks()[
            "all_math_checks_use_exact_rational"])

    def test_050_known_horizon_1_spne_all_defect(self):
        self.assertEqual(m.audited_finite_known_horizon_backward_induction(1)[
            "inductively_unique_SPNE_action_path"],("D",))

    def test_051_known_horizon_5_spne_all_defect(self):
        self.assertEqual(m.audited_finite_known_horizon_backward_induction(5)[
            "inductively_unique_SPNE_action_path"],("D",)*5)

    def test_052_known_horizon_20_spne_all_defect(self):
        self.assertEqual(m.audited_finite_known_horizon_backward_induction(20)[
            "inductively_unique_SPNE_action_path"],("D",)*20)

    def test_053_finite_horizon_not_actual_human_choices(self):
        self.assertEqual(m.audited_finite_known_horizon_backward_induction(10)[
            "real_human_actions_observed"],0)

    def test_054_known_and_unknown_horizon_not_conflated(self):
        self.assertEqual(len(m.audited_finite_known_horizon_backward_induction(5)[
            "inductively_unique_SPNE_action_path"]),5)
        self.assertEqual(m.original_1981_stability_formulas(F(4,5))[
            "both_printed_payoff_defenses_hold"],True)

    def test_055_reject_nonfraction_discount_boolean_float_and_endpoint_one(self):
        for x in (0,1,True,False,0.6,None,"3/5",F(-1,10),F(1),F(11,10)):
            with self.subTest(w=x),self.assertRaises(m.RepeatedGamesAuditError):
                m.independent_infinite_state_cycle_value("TFT","TFT",x)

    def test_056_reject_invalid_strategy_name_and_type(self):
        for x in ("Grim","PAVLOV","",1,True,None):
            with self.subTest(x=x),self.assertRaises(m.RepeatedGamesAuditError):
                m.simulate_explicit_rounds(x,"TFT",2)

    def test_057_reject_invalid_stage_actions(self):
        for x in ("A",0,True,None,""):
            with self.subTest(x=x),self.assertRaises(m.RepeatedGamesAuditError):
                m.stage_payoffs(x,"C")

    def test_058_reject_invalid_prefix_horizons(self):
        for n in (0,-1,101,False,True,2.0,None,"3"):
            with self.subTest(n=n),self.assertRaises(m.RepeatedGamesAuditError):
                m.simulate_explicit_rounds("TFT","TFT",n)

    def test_059_reject_wrong_prev_history_and_first_round_nonempty(self):
        with self.assertRaises(m.RepeatedGamesAuditError):
            m.deterministic_action_pair("TFT","TFT",("C","D"),0)
        with self.assertRaises(m.RepeatedGamesAuditError):
            m.deterministic_action_pair("TFT","TFT",None,1)

    def test_060_reject_invalid_forced_execution(self):
        with self.assertRaises(m.RepeatedGamesAuditError):
            m.simulate_explicit_rounds("TFT","TFT",2,initial_forced_row="X")

    def test_061_reject_wrong_action_policy_history_and_turn(self):
        with self.assertRaises(m.RepeatedGamesAuditError):
            m.policy_choice("TFT","C","D",0)
        with self.assertRaises(m.RepeatedGamesAuditError):
            m.policy_choice("WSLS",None,None,1)
        with self.assertRaises(m.RepeatedGamesAuditError):
            m.policy_choice("ALLD",None,None,True)

    def test_062_report_1981_1993_zero_E2_and_frozen_models(self):
        x=m.source_bounded_receipt()
        self.assertEqual(x["new_real_human_E2_prediction_scores"],0)
        self.assertEqual((x["R073"],x["PESEN_v0_1"]),("FROZEN","FROZEN"))

    def test_063_source_full_tournaments_and_mutation_not_claimed(self):
        x=m.source_bounded_receipt()
        self.assertFalse(x["source_1981_original_tournament_replayed"])
        self.assertFalse(x["source_1993_original_population_evolution_replayed"])

    def test_064_original_1981_double_threshold_versus_R128_single_threshold(self):
        x=m.audit_original_1981_double_constraint()
        self.assertEqual((x["original_source_1981_TFT_ALLD_payoff_boundary"],
                          x["original_source_1981_TFT_ALT_DC_payoff_boundary"]),("1/2","2/3"))

    def test_065_result_determinism(self):
        self.assertEqual(m.original_1981_stability_formulas(F(2,3)),
                         m.original_1981_stability_formulas(F(2,3)))


if __name__=="__main__":
    unittest.main()
