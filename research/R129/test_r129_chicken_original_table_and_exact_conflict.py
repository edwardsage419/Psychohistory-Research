"""R129 original Smith-Price 1973 one-decimal 5x5 and bounded Chicken math."""
import unittest
from fractions import Fraction as F
from unittest.mock import patch

import r129_chicken_original_table_and_exact_conflict as m


class OriginalNature1973SimulationAudit(unittest.TestCase):
    def test_001_first_party_original_1973_source_doi(self):
        self.assertIn("10.1038/246015a0",m.__doc__)

    def test_002_original_has_five_not_two_strategies(self):
        self.assertEqual(m.ORIGINAL_1973_STRATEGIES,
                         ("Mouse","Hawk","Bully","Retaliator","Prober-Retaliator"))

    def test_003_original_25_table_cells_are_exact_fractions(self):
        a=m.ORIGINAL_1973_SIMULATED_ROUNDED_TABLE
        self.assertEqual(sum(len(r) for r in a),25)
        self.assertTrue(all(type(x) is F for row in a for x in row))

    def test_004_original_mouse_row_all_values(self):
        self.assertEqual(m.ORIGINAL_1973_SIMULATED_ROUNDED_TABLE[0],
                         (F(29),F(39,2),F(39,2),F(29),F(86,5)))

    def test_005_original_hawk_row_all_values(self):
        self.assertEqual(m.ORIGINAL_1973_SIMULATED_ROUNDED_TABLE[1],
                         (F(80),F(-39,2),F(373,5),F(-181,10),F(-189,10)))

    def test_006_original_bully_row_all_values(self):
        self.assertEqual(m.ORIGINAL_1973_SIMULATED_ROUNDED_TABLE[2],
                         (F(80),F(49,10),F(83,2),F(119,10),F(56,5)))

    def test_007_original_retaliator_row_all_values(self):
        self.assertEqual(m.ORIGINAL_1973_SIMULATED_ROUNDED_TABLE[3],
                         (F(29),F(-223,10),F(571,10),F(29),F(231,10)))

    def test_008_original_prober_retaliator_row_all_values(self):
        self.assertEqual(m.ORIGINAL_1973_SIMULATED_ROUNDED_TABLE[4],
                         (F(567,10),F(-201,10),F(297,5),F(269,10),F(219,10)))

    def test_009_source_reports_fifteen_pair_types(self):
        self.assertEqual(m.original_published_table_audit()[
            "original_simulated_unordered_strategy_pairs"],15)

    def test_010_source_reports_2000_simulations_per_pair(self):
        self.assertEqual(m.original_published_table_audit()[
            "source_reported_stochastic_contests_per_pair"],2000)

    def test_011_project_no_original_stochastic_battles_resimulated(self):
        self.assertEqual(m.original_published_table_audit()[
            "source_simulated_contests_replayed_by_R129"],0)

    def test_012_against_Mouse_Hawk_and_Bully_equal_best(self):
        self.assertEqual(m.original_published_table_audit()[
            "best_replies_to_published_rounded_columns"]["Mouse"],["Hawk","Bully"])

    def test_013_against_Hawk_Mouse_is_best(self):
        self.assertEqual(m.original_published_table_audit()[
            "best_replies_to_published_rounded_columns"]["Hawk"],["Mouse"])

    def test_014_against_Bully_Hawk_is_best(self):
        self.assertEqual(m.original_published_table_audit()[
            "best_replies_to_published_rounded_columns"]["Bully"],["Hawk"])

    def test_015_against_Retaliator_Mouse_and_Retaliator_tie(self):
        self.assertEqual(m.original_published_table_audit()[
            "best_replies_to_published_rounded_columns"]["Retaliator"],["Mouse","Retaliator"])

    def test_016_against_Prober_Retaliator_Retaliator_best(self):
        self.assertEqual(m.original_published_table_audit()[
            "best_replies_to_published_rounded_columns"]["Prober-Retaliator"],["Retaliator"])

    def test_017_one_weak_symmetric_Nash_in_rounded_table(self):
        self.assertEqual(m.original_published_table_audit()[
            "pure_symmetric_Nash_from_rounded_table"],["Retaliator"])

    def test_018_rounded_table_cannot_certify_strict_second_order_ESS(self):
        x=m.original_published_table_audit()
        self.assertFalse(x["strict_second_order_ESS_Retaliator_proven_from_rounded_table"])
        self.assertTrue(x[
            "author_1973_claimed_Retaliator_ESS_but_rounded_table_cannot_verify_strict_refinement"])

    def test_019_original_rounded_Mouse_Retaliator_ties_four_cells(self):
        a=m.ORIGINAL_1973_SIMULATED_ROUNDED_TABLE
        self.assertEqual((a[0][0],a[0][3],a[3][0],a[3][3]),(F(29),)*4)

    def test_020_primary_original_not_one_raw_animal_observation(self):
        self.assertEqual(m.original_published_table_audit()[
            "real_human_or_animal_individual_raw_observations_reanalyzed"],0)


class StrictTwoStrategyAntiCoordinationMath(unittest.TestCase):
    def test_021_project_V2_C6_exact_row_matrix(self):
        self.assertEqual(m.frozen_chicken_math()["project_row_payoffs"],
                         [["-2","2"],["0","1"]])

    def test_022_project_H_H_each_negative_two(self):
        self.assertEqual(m.two_person_payoffs(F(2),F(6),"H","H"),(F(-2),F(-2)))

    def test_023_project_H_D_row_two_col_zero(self):
        self.assertEqual(m.two_person_payoffs(F(2),F(6),"H","D"),(F(2),F(0)))

    def test_024_project_D_H_row_zero_col_two(self):
        self.assertEqual(m.two_person_payoffs(F(2),F(6),"D","H"),(F(0),F(2)))

    def test_025_project_D_D_each_one(self):
        self.assertEqual(m.two_person_payoffs(F(2),F(6),"D","D"),(F(1),F(1)))

    def test_026_project_symmetry_reversing_roles(self):
        for i in ("H","D"):
            for j in ("H","D"):
                u=m.two_person_payoffs(F(2),F(6),i,j)
                v=m.two_person_payoffs(F(2),F(6),j,i)
                self.assertEqual(u,v[::-1])

    def test_027_independent_single_row_solver_agrees_all_four(self):
        for i in ("H","D"):
            for j in ("H","D"):
                self.assertEqual(m.row_payoff_for_pair(F(2),F(6),i,j),
                                 m.two_person_payoffs(F(2),F(6),i,j)[0])

    def test_028_two_non_diagonal_strict_pure_nash(self):
        self.assertEqual(m.independently_enumerated_pure_nash(F(2),F(6)),
                         (("H","D"),("D","H")))

    def test_029_project_H_H_not_nash_if_cost_greater_than_value(self):
        self.assertGreater(m.two_person_payoffs(F(2),F(6),"D","H")[0],
                           m.two_person_payoffs(F(2),F(6),"H","H")[0])

    def test_030_project_D_D_not_nash_due_to_hawk_deviation(self):
        self.assertGreater(m.two_person_payoffs(F(2),F(6),"H","D")[0],
                           m.two_person_payoffs(F(2),F(6),"D","D")[0])

    def test_031_mixed_hawk_rate_one_third(self):
        self.assertEqual(m.mixed_nash_solution(F(2),F(6))["hawk_marginal"],F(1,3))

    def test_032_mixed_uncoordinated_collision_one_ninth(self):
        self.assertEqual(m.mixed_nash_solution(F(2),F(6))[
            "both_hawk_under_independent_mixing"],F(1,9))

    def test_033_mixed_each_payoff_two_thirds(self):
        self.assertEqual(m.mixed_nash_solution(F(2),F(6))[
            "each_player_expected_payoff"],F(2,3))

    def test_034_mixed_total_payoff_four_thirds(self):
        self.assertEqual(m.mixed_nash_solution(F(2),F(6))[
            "two_players_total_expected"],F(4,3))

    def test_035_q_below_one_third_hawk_best(self):
        self.assertEqual(m.expected_from_independent_opponent(
            F(2),F(6),F(1,4))["best"],"H")

    def test_036_q_above_one_third_dove_best(self):
        self.assertEqual(m.expected_from_independent_opponent(
            F(2),F(6),F(1,2))["best"],"D")

    def test_037_q_one_third_indifferent_exact(self):
        x=m.expected_from_independent_opponent(F(2),F(6),F(1,3))
        self.assertEqual((x["hawk"],x["dove"],x["difference"],x["best"]),
                         (F(2,3),F(2,3),F(0),"TIE"))

    def test_038_direct_expected_payoff_independent_of_analytic_difference_function(self):
        with patch.object(m,"independent_analytic_expected_difference",
                          side_effect=AssertionError("FORBIDDEN")):
            self.assertEqual(m.expected_from_independent_opponent(
                F(2),F(6),F(1,3))["difference"],0)

    def test_039_analytic_difference_no_call_to_direct_payoffs(self):
        with patch.object(m,"expected_from_independent_opponent",
                          side_effect=AssertionError("FORBIDDEN")):
            self.assertEqual(m.independent_analytic_expected_difference(
                F(2),F(6),F(1,3)),0)

    def test_040_51_games_663_belief_comparisons(self):
        x=m.strict_grid_anti_coordination_audit()
        self.assertEqual(x["exact_value_cost_games"],51)
        self.assertEqual(x["exact_opponent_belief_and_payoff_cross_checks"],663)

    def test_041_every_one_of_51_games_two_asymmetric_nash(self):
        self.assertEqual(m.strict_grid_anti_coordination_audit()[
            "pure_Nash_in_every_game"],[["H","D"],["D","H"]])

    def test_042_at_C12_equilibrium_hawk_one_sixth_and_collision_one_36(self):
        x=m.mixed_nash_solution(F(2),F(12))
        self.assertEqual((x["hawk_marginal"],x["both_hawk_under_independent_mixing"]),
                         (F(1,6),F(1,36)))

    def test_043_strict_fraction_parameter_validation(self):
        for v,c in ((2,6),(F(2),6),(True,F(6)),(F(0),F(2)),
                    (F(2),F(2)),(F(3),F(2)),(F(-1),F(5)),
                    (F(2),F(-5))):
            with self.subTest(v=v,c=c),self.assertRaises(m.ChickenDomainError):
                m.two_person_payoffs(v,c,"H","D")

    def test_044_strict_actions_validation(self):
        for bad in (0,True,None,"S","h",""):
            with self.subTest(bad=bad),self.assertRaises(m.ChickenDomainError):
                m.two_person_payoffs(F(2),F(6),bad,"H")

    def test_045_strict_probability_fraction_and_support(self):
        for bad in (0,1,True,False,0.5,"1/3",F(-1,3),F(4,3)):
            with self.subTest(bad=bad),self.assertRaises(m.ChickenDomainError):
                m.expected_from_independent_opponent(F(2),F(6),bad)


class CorrelationImplementationRiskScope(unittest.TestCase):
    def test_046_same_marginal_three_joint_laws(self):
        x=m.frozen_same_marginals_joint_conflict_examples()
        self.assertEqual(x["same_individual_hawk_marginal"],"1/3")
        self.assertEqual(set(x["joint_hawk_dependence_models"]),{
            "independent","anti_correlated_role_allocation","perfect_positive_correlation"})

    def test_047_independent_joint_collision_one_ninth(self):
        self.assertEqual(m.frozen_same_marginals_joint_conflict_examples()[
            "joint_hawk_dependence_models"]["independent"]["collision_probability"],"1/9")

    def test_048_anticorrelated_role_joint_collision_zero(self):
        self.assertEqual(m.frozen_same_marginals_joint_conflict_examples()[
            "joint_hawk_dependence_models"]["anti_correlated_role_allocation"]["collision_probability"],"0")

    def test_049_perfect_correlation_collision_one_third(self):
        self.assertEqual(m.frozen_same_marginals_joint_conflict_examples()[
            "joint_hawk_dependence_models"]["perfect_positive_correlation"]["collision_probability"],"1/3")

    def test_050_anticorrelation_total_welfare_two(self):
        self.assertEqual(m.frozen_same_marginals_joint_conflict_examples()[
            "joint_hawk_dependence_models"]["anti_correlated_role_allocation"]["joint_total_expected"],"2")

    def test_051_perfect_correlation_total_welfare_zero(self):
        self.assertEqual(m.frozen_same_marginals_joint_conflict_examples()[
            "joint_hawk_dependence_models"]["perfect_positive_correlation"]["joint_total_expected"],"0")

    def test_052_independent_total_welfare_four_thirds(self):
        self.assertEqual(m.frozen_same_marginals_joint_conflict_examples()[
            "joint_hawk_dependence_models"]["independent"]["joint_total_expected"],"4/3")

    def test_053_independent_aggregate_welfare_formula_does_not_call_aggregation(self):
        law=(F(1,9),F(2,9),F(2,9),F(4,9))
        with patch.object(m,"independent_expected_welfare",
                          side_effect=AssertionError("NO_AGGREGATE")):
            self.assertEqual(m.analytic_group_welfare_from_collision(
                F(2),F(6),law),F(4,3))

    def test_054_marginals_from_explicit_joint_both_one_third(self):
        laws=[(F(1,9),F(2,9),F(2,9),F(4,9)),
              (F(0),F(1,3),F(1,3),F(1,3)),
              (F(1,3),F(0),F(0),F(2,3))]
        for law in laws:
            self.assertEqual(m.joint_marginals(law),(F(1,3),F(1,3)))

    def test_055_illegal_joint_mass_or_shape_rejected(self):
        bad=((),(F(1),),(F(1),)*3,(F(1),)*5,
             (F(1,2),F(0),F(0),F(0)),
             (F(-1,2),F(0),F(0),F(3,2)),
             (0,F(0),F(0),F(1)))
        for x in bad:
            with self.subTest(x=x),self.assertRaises(m.ChickenDomainError):
                m.joint_marginals(x)

    def test_056_correlated_distribution_not_claimed_automatically_correlated_equilibrium(self):
        self.assertTrue(m.frozen_same_marginals_joint_conflict_examples()[
            "these_joint_laws_are_not_all_claimed_correlated_equilibria"])

    def test_057_role_flip_zero_probability_no_collision(self):
        self.assertEqual(m.flip_noise_distribution(F(0)),(F(0),F(1),F(0),F(0)))

    def test_058_role_flip_one_probability_reversed_roles(self):
        self.assertEqual(m.flip_noise_distribution(F(1)),(F(0),F(0),F(1),F(0)))

    def test_059_role_flip_half_has_four_equal_outcomes(self):
        self.assertEqual(m.flip_noise_distribution(F(1,2)),(F(1,4),)*4)

    def test_060_role_flip_closed_and_four_event_algorithm_agree(self):
        for k in range(13):
            e=F(k,12)
            self.assertEqual(m.flip_noise_distribution(e),m.flip_noise_direct_enumeration(e))

    def test_061_role_flip_closed_analytic_does_not_call_event_enumeration(self):
        with patch.object(m,"flip_noise_direct_enumeration",
                          side_effect=AssertionError("NO_EVENT_ENUM")):
            self.assertEqual(m.flip_noise_distribution(F(1,2))[0],F(1,4))

    def test_062_role_flip_full_audit_13_implemented_error_rates(self):
        x=m.role_flip_noise_audit()
        self.assertEqual(x["exact_flip_probabilities_checked"],13)
        self.assertEqual(x["max_collisions_probability"],"1/4")
        self.assertEqual(x["max_collisions_at_independent_flip"],"1/2")

    def test_063_same_chicken_cost_higher_changes_equilibrium_not_fixed_exogenous_marginals(self):
        self.assertEqual(m.mixed_nash_solution(F(2),F(12))["hawk_marginal"],F(1,6))
        self.assertEqual(m.joint_marginals((
            F(1,9),F(2,9),F(2,9),F(4,9))),(F(1,3),F(1,3)))

    def test_064_r128_stag_coordinated_diagonal_not_same_nash_set(self):
        self.assertEqual(m.independently_enumerated_pure_nash(F(2),F(6)),
                         (("H","D"),("D","H")))

    def test_065_all_synthetic_examples_repeat_deterministically(self):
        self.assertEqual(m.frozen_chicken_math(),m.frozen_chicken_math())

    def test_066_source_project_receipt_no_raw_human_E2(self):
        x=m.phase_receipt()
        self.assertEqual(x["human_microdata_E2_new_prediction_scores"],0)

    def test_067_R073_and_PESEN_remain_frozen(self):
        x=m.phase_receipt()
        self.assertEqual((x["R073"],x["PESEN_v0_1"]),("FROZEN","FROZEN"))

    def test_068_source_five_strategy_not_project_two_strategy_payoff(self):
        self.assertNotEqual(len(m.ORIGINAL_1973_SIMULATED_ROUNDED_TABLE),
                            len(m.frozen_chicken_math()["project_row_payoffs"]))


if __name__=="__main__":
    unittest.main()
