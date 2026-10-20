"""R131 original Taylor & Jonker 1978 firsthand examples and project drift."""
import unittest
from fractions import Fraction as F
from itertools import product
from unittest.mock import patch
import r131_taylor_jonker_1978_evolutionary_game_exact as m


def cyclic():
    return m.source_1978_cyclic_matrix(F(1,2))


def alpha_one():
    return m.source_1978_alpha_matrix(F(1))


def pcyc():
    return (F(1,3),)*3


def palpha():
    return (F(15,35),F(11,35),F(9,35))


def e3():
    return (F(0),F(0),F(1))


class True1978MatrixSourceTests(unittest.TestCase):
    def test_001_1978_publisher_doi_and_actual_original(self):
        self.assertIn("10.1016/0025-5564(78)90077-9",m.__doc__)

    def test_002_1978_original_three_strategy_cyclic_matrix(self):
        self.assertEqual(cyclic(),((F(-1,2),F(1),F(-1)),
                                   (F(-1),F(-1,2),F(1)),
                                   (F(1),F(-1),F(-1,2))))

    def test_003_1978_original_alpha_one_matrix(self):
        self.assertEqual(alpha_one(),((F(2),F(1),F(5)),
                                      (F(5),F(1),F(0)),
                                      (F(1),F(4),F(3))))

    def test_004_source_epsilon_zero_and_float_rejected(self):
        for x in (F(0),F(-1),F(3,2),True,False,1.0,0.5,"1/2",None):
            with self.subTest(x=x),self.assertRaises(m.EvolutionaryAuditError):
                m.source_1978_cyclic_matrix(x)

    def test_005_source_alpha_only_true_fractions(self):
        for x in (0,1,True,None,1.0,"1"):
            with self.subTest(x=x),self.assertRaises(m.EvolutionaryAuditError):
                m.source_1978_alpha_matrix(x)

    def test_006_source_alpha_equilibrium_interior_range(self):
        for x in (F(-8),F(17,2),F(-9),F(9),0,1,1.0):
            with self.subTest(x=x),self.assertRaises(m.EvolutionaryAuditError):
                m.alpha_interior_equilibrium(x)

    def test_007_original_alpha_one_equilibrium_15_11_9_over35(self):
        self.assertEqual(m.alpha_interior_equilibrium(F(1)),palpha())

    def test_008_original_alpha_negative_one_equilibrium_19_11_7_over37(self):
        self.assertEqual(m.alpha_interior_equilibrium(F(-1)),
                         (F(19,37),F(11,37),F(7,37)))

    def test_009_source_cyclic_each_type_equal_fitness_negative_one_sixth(self):
        self.assertEqual(m.payoff_each(cyclic(),pcyc()),(F(-1,6),)*3)

    def test_010_original_alpha_one_each_fitness_86_over35(self):
        self.assertEqual(m.payoff_each(alpha_one(),palpha()),(F(86,35),)*3)

    def test_011_independent_population_pairwise_mean_cyclic(self):
        self.assertEqual(m.population_mean_payoff(cyclic(),pcyc()),F(-1,6))

    def test_012_independent_population_pairwise_mean_alpha_one(self):
        self.assertEqual(m.population_mean_payoff(alpha_one(),palpha()),F(86,35))

    def test_013_payoff_each_average_equals_direct_all_nine_contributions(self):
        for matrix,p in ((cyclic(),pcyc()),(alpha_one(),palpha())):
            self.assertEqual(m.dot(m.payoff_each(matrix,p),p),
                             m.population_mean_payoff(matrix,p))

    def test_014_source_continuous_fixed_cyclic(self):
        self.assertEqual(m.continuous_original_eq2_field(cyclic(),pcyc()),(F(0),)*3)

    def test_015_source_continuous_fixed_alpha_one(self):
        self.assertEqual(m.continuous_original_eq2_field(alpha_one(),palpha()),(F(0),)*3)

    def test_016_source_discrete_fixed_cyclic(self):
        self.assertEqual(m.discrete_original_eq3_one_generation(cyclic(),pcyc()),pcyc())

    def test_017_source_discrete_fixed_alpha_one(self):
        self.assertEqual(m.discrete_original_eq3_one_generation(alpha_one(),palpha()),palpha())

    def test_018_source_discrete_adds_one_to_fitness_not_raw_fitness(self):
        game=cyclic()
        pure=(F(1),F(0),F(0))
        self.assertEqual(m.discrete_original_eq3_one_generation(game,pure),pure)

    def test_019_discrete_negative_reproduction_multiplier_fails_closed(self):
        bad=((F(-2),F(0),F(0)),(F(0),F(0),F(0)),(F(0),F(0),F(0)))
        with self.assertRaises(m.EvolutionaryAuditError):
            m.discrete_original_eq3_one_generation(bad,(F(1),F(0),F(0)))

    def test_020_explicit_zero_support_not_spontaneously_created_discrete(self):
        y=m.discrete_original_eq3_one_generation(cyclic(),(F(0),F(1,2),F(1,2)))
        self.assertEqual(y[0],F(0))

    def test_021_matrix_wrong_shape_and_precision_rejected(self):
        good=cyclic()
        for bad in ((),good[:2],((F(0),)*4,)*3,"notmatrix",
                    ((0,F(1),F(1)),good[1],good[2])):
            with self.subTest(case=str(type(bad))),self.assertRaises(m.EvolutionaryAuditError):
                m.payoff_each(bad,pcyc())

    def test_022_probabilities_strict_simplex_fails_closed(self):
        for bad in ((),(F(1),),[F(1),F(1),F(0)],
                    (F(-1),F(1),F(1)),(True,F(0),F(0)),
                    (1.0,F(0),F(0))):
            with self.subTest(bad=str(bad)),self.assertRaises(m.EvolutionaryAuditError):
                m.payoff_each(cyclic(),bad)

    def test_023_two_independent_source_invasion_algorithms_agree(self):
        q=e3()
        for eps in (F(0),F(1,10),F(1,2),F(1)):
            self.assertEqual(m.invasion_advantage_direct(alpha_one(),palpha(),q,eps),
                             m.invasion_advantage_independent_expansion(alpha_one(),palpha(),q,eps))


class Original1978TwoSeparateStabilityCounterexamples(unittest.TestCase):
    def test_024_original_cyclic_source_ESS_at_uniform(self):
        x=m.original_cyclic_counterexample_audit()
        self.assertIn("for any q!=p",x["universal_linear_game_ESS_proof"])

    def test_025_original_cyclic_continuous_trace_negative_one_third(self):
        self.assertEqual(m.original_cyclic_counterexample_audit()["continuous_trace"],"-1/3")

    def test_026_original_cyclic_continuous_determinant_13_over36(self):
        self.assertEqual(m.original_cyclic_counterexample_audit()["continuous_determinant"],"13/36")

    def test_027_original_cyclic_discrete_trace_8_over5(self):
        self.assertEqual(m.original_cyclic_counterexample_audit()["discrete_trace"],"8/5")

    def test_028_original_cyclic_discrete_det_28over25_unstable(self):
        x=m.original_cyclic_counterexample_audit()
        self.assertEqual(x["discrete_determinant"],"28/25")
        self.assertTrue(x["discrete_locally_unstable"])

    def test_029_source_continuous_cyclic_local_strict_stability(self):
        self.assertTrue(m.original_cyclic_counterexample_audit()["continuous_locally_strictly_stable"])

    def test_030_source_cyclic_jacobian_two_independent_exact_methods(self):
        self.assertEqual(m.tangent_analytic_continuous_jacobian(cyclic(),pcyc()),
                         m.tangent_independent_exact_polynomial_jacobian(cyclic(),pcyc()))

    def test_031_source_cyclic_independent_mutation_e0_loss(self):
        p=pcyc()
        q=(F(1),F(0),F(0))
        self.assertEqual(m.invasion_advantage_direct(cyclic(),p,q,F(1,10)),
                         m.invasion_advantage_independent_expansion(cyclic(),p,q,F(1,10)))
        self.assertLess(m.invasion_advantage_direct(cyclic(),p,q,F(1,10)),0)

    def test_032_source_cyclic_mutants_e0_e1_e2_all_lose(self):
        for q in ((F(1),F(0),F(0)),(F(0),F(1),F(0)),e3()):
            self.assertEqual(m.invasion_advantage_direct(cyclic(),pcyc(),q,F(1,10)),
                             F(-1,30))

    def test_033_source_cyclic_nonuniform_pure_q_proves_quadratic_sign(self):
        A=cyclic();p=pcyc()
        for q in ((F(1),F(0),F(0)),(F(0),F(1),F(0)),e3(),
                  (F(1,2),F(1,2),F(0)),(F(1,4),F(1,4),F(1,2))):
            diff=tuple(q[i]-p[i] for i in range(3))
            direct_quadratic=sum((diff[i]*A[i][j]*diff[j] for i in range(3) for j in range(3)),F(0))
            expected=-F(1,2)*sum((v*v for v in diff),F(0))
            self.assertEqual(direct_quadratic,expected)
            self.assertLess(direct_quadratic,0)

    def test_034_discrete_tangent_linearization_exact_matrix_source(self):
        matrix=m.discrete_tangent_linearization_from_original_eq3(cyclic(),pcyc())
        self.assertEqual(m.trace_and_det_two_by_two(matrix),
                         {"trace":F(8,5),"determinant":F(28,25)})

    def test_035_tangent_exact_Richardson_does_not_call_analytic_jacobian(self):
        with patch.object(m,"tangent_analytic_continuous_jacobian",
                          side_effect=AssertionError("NO_ANALYTIC")):
            J=m.tangent_independent_exact_polynomial_jacobian(cyclic(),pcyc())
            self.assertEqual(m.trace_and_det_two_by_two(J)["trace"],F(-1,3))

    def test_036_analytic_jacobian_does_not_call_Richardson(self):
        with patch.object(m,"tangent_independent_exact_polynomial_jacobian",
                          side_effect=AssertionError("NO_RICHARDSON")):
            J=m.tangent_analytic_continuous_jacobian(cyclic(),pcyc())
            self.assertEqual(m.trace_and_det_two_by_two(J)["determinant"],F(13,36))

    def test_037_source_alpha1_continuous_locally_strictly_stable(self):
        self.assertTrue(m.original_alpha_counterexample_audit()["continuous_locally_strictly_stable"])

    def test_038_source_alpha1_equilibrium_all_types_equal_86over35(self):
        self.assertEqual(m.original_alpha_counterexample_audit()["each_present_pure_type_fitness"],"86/35")

    def test_039_source_alpha1_analytic_jacobian_exact_primary_example(self):
        expected=((F(-291,245),F(-60,49)),(F(2013,1225),F(33,49)))
        self.assertEqual(m.tangent_analytic_continuous_jacobian(alpha_one(),palpha()),expected)

    def test_040_source_alpha1_Richardson_exactly_matches_analytic(self):
        self.assertEqual(m.tangent_independent_exact_polynomial_jacobian(alpha_one(),palpha()),
                         m.tangent_analytic_continuous_jacobian(alpha_one(),palpha()))

    def test_041_source_alpha1_negative_trace_positive_det(self):
        x=m.original_alpha_counterexample_audit()
        self.assertEqual(x["continuous_trace"],"-18/35")
        self.assertEqual(x["continuous_determinant"],"297/245")

    def test_042_source_alpha1_mutant_e3_strictly_better_at_mu_one_tenth(self):
        self.assertEqual(m.original_alpha_counterexample_audit()[
            "mutant_e3_at_share_one_tenth_advantage"],"3/350")

    def test_043_source_alpha1_mutant_gain_is_three_mu_over35(self):
        for mu in (F(1,100),F(1,10),F(1,4),F(1,2),F(1)):
            self.assertEqual(m.invasion_advantage_direct(alpha_one(),palpha(),e3(),mu),
                             3*mu/F(35))

    def test_044_source_alpha1_ESS_not_guaranteed_by_dynamic_stability(self):
        x=m.original_alpha_counterexample_audit()
        self.assertFalse(x["evolutionarily_stable_strategy"])
        self.assertTrue(x["continuous_locally_strictly_stable"])

    def test_045_original_1978_p147_504_exhaustive_exact_equalities(self):
        self.assertEqual(m.original_p147_invasion_grid()[
            "exact_direct_vs_expansion_comparisons"],504)

    def test_046_1978_two_source_distinct_games_not_equal_matrix(self):
        self.assertNotEqual(cyclic(),alpha_one())

    def test_047_discrete_linearization_invalid_for_non_equilibrium(self):
        with self.assertRaises(m.EvolutionaryAuditError):
            m.discrete_tangent_linearization_from_original_eq3(
                alpha_one(),(F(1,2),F(1,4),F(1,4)))

    def test_048_discrete_tangent_specialization_requires_full_support(self):
        with self.assertRaises(m.EvolutionaryAuditError):
            m.discrete_tangent_linearization_from_original_eq3(
                alpha_one(),(F(1),F(0),F(0)))

    def test_049_all_3x3_simplex_grid_cases_preserve_total_probabilities(self):
        for i in range(7):
            for j in range(7-i):
                p=(F(i,6),F(j,6),F(6-i-j,6))
                self.assertEqual(sum(m.continuous_original_eq2_field(cyclic(),p),F(0)),0)
                self.assertEqual(sum(m.discrete_original_eq3_one_generation(cyclic(),p),F(0)),1)

    def test_050_all_synthetic_exact_research_output_is_deterministic(self):
        self.assertEqual(m.original_cyclic_counterexample_audit(),
                         m.original_cyclic_counterexample_audit())


class ProjectFiniteMoranModelExplicitNot1978Theory(unittest.TestCase):
    def test_051_project_moran_birth_death_N5_fitness_A3_B2(self):
        up,down,stay=m.finite_project_moran_transitions(5,1,F(3),F(2))
        self.assertEqual((up,down,stay),(F(4,35),F(6,35),F(5,7)))

    def test_052_project_moran_boundary_absorbing_zero_or_all(self):
        self.assertEqual(m.finite_project_moran_transitions(5,0,F(3),F(2)),
                         (F(0),F(0),F(1)))
        self.assertEqual(m.finite_project_moran_transitions(5,5,F(3),F(2)),
                         (F(0),F(0),F(1)))

    def test_053_project_disadvantaged_mutant_fixation_N5_exact_16over211(self):
        self.assertEqual(m.exact_project_moran_fixation_probability(5,F(3),F(2)),F(16,211))

    def test_054_project_neutral_fixation_N5_one_fifth(self):
        self.assertEqual(m.exact_project_moran_fixation_probability(5,F(1),F(1)),F(1,5))

    def test_055_project_disadvantaged_mutant_can_fix_but_less_than_neutral(self):
        result=m.project_finite_stochastic_drift_counterexample()
        self.assertEqual(result["project_single_mutant_risk_of_eventual_fixation"],"16/211")
        self.assertTrue(result["selection_disadvantage_does_not_imply_zero_finite_fixation"])

    def test_056_project_N2to8_neutral_fixation_inverse_population_size(self):
        for n in range(2,9):
            self.assertEqual(m.exact_project_moran_fixation_probability(n,F(1),F(1)),F(1,n))

    def test_057_project_N2to8_disadvantaged_between_zero_and_neutral(self):
        for n in range(2,9):
            self.assertLess(F(0),m.exact_project_moran_fixation_probability(n,F(3),F(2)))
            self.assertLess(m.exact_project_moran_fixation_probability(n,F(3),F(2)),F(1,n))

    def test_058_project_nonzero_Moran_transitions_normalized(self):
        for n in range(2,9):
            for i in range(n+1):
                parts=m.finite_project_moran_transitions(n,i,F(3),F(2))
                self.assertEqual(sum(parts,F(0)),1)
                self.assertTrue(all(0<=x<=1 for x in parts))

    def test_059_project_finite_sample_invalid_parameters_fails_closed(self):
        for args in ((1,1,F(1),F(1)),(9,1,F(1),F(1)),
                     (5,True,F(1),F(1)),(5,2,1,F(1)),
                     (5,2,F(1),0.5),(5,2,F(0),F(1)),(5,2,F(1),F(-1))):
            with self.subTest(args=args),self.assertRaises(m.EvolutionaryAuditError):
                m.finite_project_moran_transitions(*args)

    def test_060_moran_not_original_source_theory_or_real_animal_data(self):
        r=m.project_finite_stochastic_drift_counterexample()
        self.assertTrue(r["project_created_not_a_1978_source_theorem_or_simulation"])
        self.assertFalse(r["real_population_size_or_behavior_frequency_estimated"])

    def test_061_original_1978_1974_sources_not_claimed_as_new_human_E2(self):
        x=m.stage_receipt()
        self.assertEqual(x["new_real_human_E2_prediction_scores"],0)

    def test_062_frozen_R073_and_PESEN_unchanged(self):
        x=m.stage_receipt()
        self.assertEqual((x["R073"],x["PESEN_v0_1"]),("FROZEN","FROZEN"))

    def test_063_not_claim_original_1978_full_trajectory_reconstructed(self):
        self.assertFalse(m.stage_receipt()["original_1978_numeric_population_trajectories_all_reconstructed"])


if __name__=="__main__":
    unittest.main()
