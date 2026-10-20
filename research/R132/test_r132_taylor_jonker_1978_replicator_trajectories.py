"""R132: primary Taylor Jonker 1978 Eq2, Eq3 versus numerical paths."""
import math
import unittest
from fractions import Fraction as F
from unittest.mock import patch
import r132_taylor_jonker_1978_replicator_trajectories as m


def hawk(): return m.PROJECT_GAMES["Hawk-Dove"]
def stag(): return m.PROJECT_GAMES["Stag-Hunt"]
def logistic(): return m.PROJECT_GAMES["Logistic-control"]


class Primary1978ReplicatorEquations(unittest.TestCase):
    def test_001_source_1978_original_doi_and_pdf(self):
        self.assertIn("10.1016/0025-5564(78)90077-9",m.__doc__)
        self.assertIn("page149",m.__doc__)

    def test_002_project_hawk_primary_2x2_params_explicit(self):
        self.assertEqual(hawk(),((F(-2),F(2)),(F(0),F(1))))

    def test_003_project_stag_primary_2x2_params_explicit(self):
        self.assertEqual(stag(),((F(4),F(0)),(F(3),F(3))))

    def test_004_project_logistic_primary_2x2_params_explicit(self):
        self.assertEqual(logistic(),((F(2),F(2)),(F(1),F(1))))

    def test_005_hawk_payoff_difference_cubic_coefficients(self):
        self.assertEqual(m.cubic_coefficients(hawk()),(F(-3),F(1)))

    def test_006_stag_payoff_difference_cubic_coefficients(self):
        self.assertEqual(m.cubic_coefficients(stag()),(F(4),F(-3)))

    def test_007_constant_advantage_payoff_difference_coefficients(self):
        self.assertEqual(m.cubic_coefficients(logistic()),(F(0),F(1)))

    def test_008_hawk_direct_fitness_at_half(self):
        self.assertEqual(m.scalar_payoffs(hawk(),F(1,2)),(F(0),F(1,2)))

    def test_009_stag_direct_fitness_at_half(self):
        self.assertEqual(m.scalar_payoffs(stag(),F(1,2)),(F(2),F(3)))

    def test_010_hawk_eq2_dot_at_half_minus_one_eighth(self):
        self.assertEqual(m.exact_continuous_original_eq2(hawk(),F(1,2)),
                         (F(-1,8),F(1,8)))

    def test_011_stag_eq2_dot_at_half_minus_one_quarter(self):
        self.assertEqual(m.exact_continuous_original_eq2(stag(),F(1,2)),
                         (F(-1,4),F(1,4)))

    def test_012_logistic_eq2_dot_at_half_plus_one_quarter(self):
        self.assertEqual(m.exact_continuous_original_eq2(logistic(),F(1,2)),
                         (F(1,4),F(-1,4)))

    def test_013_hawk_fixed_at_zero_one_and_one_third(self):
        for x in (F(0),F(1,3),F(1)):
            self.assertEqual(m.exact_continuous_original_eq2(hawk(),x),(F(0),F(0)))

    def test_014_stag_fixed_at_zero_three_quarters_one(self):
        for x in (F(0),F(3,4),F(1)):
            self.assertEqual(m.independent_exact_cubic_field(stag(),x),(F(0),F(0)))

    def test_015_three_games_75_exact_independent_fields(self):
        x=m.exhaustive_exact_field_and_discrete_audit()
        self.assertEqual(x["exact_independent_fraction_fields"],75)

    def test_016_actual_eq2_field_algorithm_not_call_cubic(self):
        with patch.object(m,"independent_exact_cubic_field",side_effect=AssertionError("NO_CUBIC")):
            self.assertEqual(m.exact_continuous_original_eq2(hawk(),F(1,2))[0],F(-1,8))

    def test_017_cubic_algorithm_not_call_direct_eq2(self):
        with patch.object(m,"exact_continuous_original_eq2",side_effect=AssertionError("NO_EQ2")):
            self.assertEqual(m.independent_exact_cubic_field(hawk(),F(1,2))[0],F(-1,8))

    def test_018_discrete_original_eq3_hawk_at_half_two_fifths(self):
        self.assertEqual(m.original_1978_discrete_generation(hawk(),F(1,2)),F(2,5))

    def test_019_discrete_original_eq3_hawk_offset_three_eight_seventeenths(self):
        self.assertEqual(m.original_1978_discrete_generation(
            m.shift_all_payoffs(hawk(),F(3)),F(1,2)),F(8,17))

    def test_020_discrete_original_eq4_increment_at_half_minus_one_tenth(self):
        self.assertEqual(m.original_1978_eq4_increment_independent(
            hawk(),F(1,2)),F(-1,10))

    def test_021_original_discrete_eq3_eq4_valid_state_replay_nonzero(self):
        x=m.exhaustive_exact_field_and_discrete_audit()
        self.assertGreater(x["source_eq3_eq4_valid_state_checks"],40)

    def test_022_discrete_original_1978_negative_birth_multiplier_fails_closed(self):
        with self.assertRaises(m.ReplicatorAuditError):
            m.original_1978_discrete_generation(hawk(),F(1))

    def test_023_discrete_stag_at_half_one_third(self):
        self.assertEqual(m.original_1978_discrete_generation(stag(),F(1,2)),F(3,7))

    def test_024_discrete_logistic_at_half_three_fifths(self):
        self.assertEqual(m.original_1978_discrete_generation(logistic(),F(1,2)),F(3,5))

    def test_025_discrete_original_payoff_shift_not_continuous_shift(self):
        x=m.source_discrete_baseline_counterexample()
        self.assertTrue(x["same_continuous_payoff_differences"])
        self.assertEqual((x["original_p149_eq3_unshifted_at_half"],
                          x["original_p149_eq3_add_three_to_all_payoffs_at_half"]),("2/5","8/17"))

    def test_026_fitness_shift_exact_invariance_all_three_games(self):
        for A in m.PROJECT_GAMES.values():
            for x in (F(0),F(1,8),F(1,3),F(1,2),F(3,4),F(1)):
                self.assertEqual(m.exact_continuous_original_eq2(A,x),
                                 m.exact_continuous_original_eq2(
                                     m.shift_all_payoffs(A,F(11)),x))

    def test_027_discrete_biological_rule_distinct_from_euler(self):
        self.assertNotEqual(m.original_1978_discrete_generation(hawk(),F(1,2)),
                            m.exact_euler_step(hawk(),F(1,2),F(1)))

    def test_028_discrete_eq4_algorithm_independent_of_eq3(self):
        with patch.object(m,"original_1978_discrete_generation",
                          side_effect=AssertionError("NO_EQ3")):
            self.assertEqual(m.original_1978_eq4_increment_independent(hawk(),F(1,2)),
                             F(-1,10))

    def test_029_discrete_eq3_does_not_call_eq4(self):
        with patch.object(m,"original_1978_eq4_increment_independent",
                          side_effect=AssertionError("NO_EQ4")):
            self.assertEqual(m.original_1978_discrete_generation(hawk(),F(1,2)),F(2,5))

    def test_030_fail_closed_bad_two_by_two_shapes_and_types(self):
        for bad in ((),((),()),[[F(1),F(2)]],((1,F(1)),(F(2),F(3))),
                    ((F(1),F(2),F(3)),(F(0),F(0))),"text"):
            with self.subTest(bad=str(bad)),self.assertRaises(m.ReplicatorAuditError):
                m.cubic_coefficients(bad)

    def test_031_fail_closed_bad_fraction_shares(self):
        for bad in (-1,1,True,False,0.25,F(-1,5),F(6,5),None,"1/2"):
            with self.subTest(bad=bad),self.assertRaises(m.ReplicatorAuditError):
                m.exact_continuous_original_eq2(hawk(),bad)

    def test_032_fail_closed_nonfraction_shift(self):
        for bad in (0,3,True,3.0,"3"):
            with self.subTest(bad=bad),self.assertRaises(m.ReplicatorAuditError):
                m.shift_all_payoffs(hawk(),bad)


class ContinuousFullTrajectoryVsIndependentImplicitIntegral(unittest.TestCase):
    def test_033_logistic_explicit_exact_midpoint_t_log3_threequarters(self):
        # x(0)=1/2, x(ln3)=3/4.
        self.assertAlmostEqual(m.analytical_continuous_value(
            logistic(),0.5,float(math.log(3))),0.75,places=12)

    def test_034_logistic_initial_time_returns_initial_share(self):
        self.assertEqual(m.analytical_continuous_value(logistic(),0.25,0.0),0.25)

    def test_035_all_fixed_boundaries_remain_fixed_under_analytic_flow(self):
        for game in m.PROJECT_GAMES.values():
            for x in (0.0,1.0):
                self.assertEqual(m.analytical_continuous_value(game,x,12.0),x)

    def test_036_original_hawk_internal_fixed_exactly_one_third(self):
        self.assertAlmostEqual(m.analytical_continuous_value(
            hawk(),float(F(1,3)),10.0),1/3,places=14)

    def test_037_original_stag_internal_fixed_threequarters(self):
        self.assertEqual(m.analytical_continuous_value(stag(),0.75,16.0),0.75)

    def test_038_hawk_analytic_increases_from_quarter_toward_third(self):
        x=m.analytical_continuous_value(hawk(),0.25,4.0)
        self.assertTrue(0.25<x<1/3)

    def test_039_hawk_analytic_decreases_from_half_toward_third(self):
        x=m.analytical_continuous_value(hawk(),0.5,4.0)
        self.assertTrue(1/3<x<0.5)

    def test_040_stag_analytic_below_threequarters_moves_towards_zero(self):
        self.assertLess(m.analytical_continuous_value(stag(),0.6,4.0),0.6)

    def test_041_stag_analytic_above_threequarters_moves_towards_one(self):
        self.assertGreater(m.analytical_continuous_value(stag(),0.8,4.0),0.8)

    def test_042_stag_basin_threshold_x_equal_threequarters_stays(self):
        self.assertEqual(m.analytical_continuous_value(stag(),0.75,10.0),0.75)

    def test_043_logistic_strictly_increases_for_any_internal_share(self):
        for x in (0.1,0.3,0.5,0.7,0.9):
            self.assertGreater(m.analytical_continuous_value(
                logistic(),x,1.0),x)

    def test_044_analytic_integral_primitive_hawk_phase_time(self):
        x0=.5;t=1.0
        xt=m.analytical_continuous_value(hawk(),x0,t)
        alpha,beta=map(float,m.cubic_coefficients(hawk()))
        delta=m.implicit_integral_primitive(xt,alpha,beta)-m.implicit_integral_primitive(x0,alpha,beta)
        self.assertAlmostEqual(delta,t,places=10)

    def test_045_analytic_integral_primitive_stag_phase_time(self):
        x0=.8;t=3.0
        xt=m.analytical_continuous_value(stag(),x0,t)
        alpha,beta=map(float,m.cubic_coefficients(stag()))
        delta=m.implicit_integral_primitive(xt,alpha,beta)-m.implicit_integral_primitive(x0,alpha,beta)
        self.assertAlmostEqual(delta,t,places=10)

    def test_046_real_216_paths_RK4_versus_independent_integration(self):
        x=m.exhaustive_216_analytic_vs_RK4()
        self.assertEqual(x["trajectory_endpoint_independent_comparisons"],216)
        self.assertTrue(x["all_216_errors_less_than_1e_minus_6"])

    def test_047_real_216_paths_reproducible_max_error_bounded(self):
        x=m.exhaustive_216_analytic_vs_RK4()
        self.assertLess(x["max_numerical_absolute_error"],1e-6)

    def test_048_RK4_no_call_to_analytic_quadrature(self):
        with patch.object(m,"analytical_continuous_value",
                          side_effect=AssertionError("NO_ANALYTIC")):
            self.assertGreater(m.rk4_continuous_trajectory(hawk(),0.25,1.0,120),0.25)

    def test_049_analytic_quadrature_no_call_to_RK4(self):
        with patch.object(m,"rk4_continuous_trajectory",
                          side_effect=AssertionError("NO_RK4")):
            self.assertLess(m.analytical_continuous_value(stag(),0.6,2.0),0.6)

    def test_050_logistic_RK4_close_explicit_at_t4(self):
        x=m.rk4_continuous_trajectory(logistic(),0.5,4.0,480)
        self.assertAlmostEqual(x,1/(1+math.exp(-4)),places=10)

    def test_051_RK4_initial_share_not_mutated_at_zero_time(self):
        self.assertEqual(m.rk4_continuous_trajectory(hawk(),0.5,0.0,1),0.5)

    def test_052_numeric_share_input_requires_finite_float(self):
        for bad in (0,F(1,2),True,math.nan,math.inf,-1.0,1.1,"0.5"):
            with self.subTest(bad=bad),self.assertRaises(m.ReplicatorAuditError):
                m.analytical_continuous_value(hawk(),bad,2.0)

    def test_053_invalid_numeric_time_rejected(self):
        for bad in (-1.0,21.0,math.inf,math.nan,0,F(1),True):
            with self.subTest(bad=bad),self.assertRaises(m.ReplicatorAuditError):
                m.analytical_continuous_value(stag(),0.5,bad)

    def test_054_RK4_coarse_dt_outside_frozen_accuracy_refused(self):
        with self.assertRaises(m.ReplicatorAuditError):
            m.rk4_continuous_trajectory(hawk(),0.5,4.0,10)

    def test_055_RK4_bad_step_type_and_count_refused(self):
        for n in (0,-1,20001,True,False,120.0,"120"):
            with self.subTest(n=n),self.assertRaises(m.ReplicatorAuditError):
                m.rk4_continuous_trajectory(hawk(),0.5,1.0,n)

    def test_056_hawk_implicit_branch_value_t4_not_zero(self):
        self.assertGreater(m.analytical_continuous_value(hawk(),0.5,4.0),1/3)


class NumericalArtifactsAndEvidenceBoundaries(unittest.TestCase):
    def test_057_euler_exact_h4_false_extinction_half_to_zero(self):
        self.assertEqual(m.exact_euler_step(hawk(),F(1,2),F(4)),F(0))

    def test_058_euler_h1_half_to_three_eighths(self):
        self.assertEqual(m.exact_euler_step(hawk(),F(1,2),F(1)),F(3,8))

    def test_059_euler_h4_local_multiplier_minus_five_thirds_unstable(self):
        self.assertEqual(m.euler_internal_linear_multiplier(
            hawk(),F(1,3),F(4)),F(-5,3))

    def test_060_euler_h1_local_multiplier_one_third_stable(self):
        self.assertEqual(m.euler_internal_linear_multiplier(
            hawk(),F(1,3),F(1)),F(1,3))

    def test_061_hawk_euler_stability_check_requires_fixed_point(self):
        with self.assertRaises(m.ReplicatorAuditError):
            m.euler_internal_linear_multiplier(hawk(),F(1,2),F(1))

    def test_062_euler_disallows_out_of_simplex_without_clamping(self):
        with self.assertRaises(m.ReplicatorAuditError):
            m.exact_euler_step(hawk(),F(1,2),F(8))

    def test_063_euler_negative_or_nonfraction_step_rejected(self):
        for h in (1,1.0,True,F(-1),None):
            with self.subTest(h=h),self.assertRaises(m.ReplicatorAuditError):
                m.exact_euler_step(hawk(),F(1,2),h)

    def test_064_euler_false_extinction_not_original_source_Eq3(self):
        x=m.project_euler_false_extinction_counterexample()
        self.assertEqual(x["Euler_h4_one_step_share"],"0")
        self.assertTrue(x["Euler_false_extinction_not_original_Taylor_Jonker_1978_Eq3"])

    def test_065_true_flow_at_t4_strictly_above_one_third(self):
        x=m.project_euler_false_extinction_counterexample()
        self.assertGreater(x["true_continuous_t4_share"],1/3)

    def test_066_actual_original_birth_both_k0_k3_different(self):
        r=m.source_discrete_baseline_counterexample()
        self.assertNotEqual(r["original_p149_eq3_unshifted_at_half"],
                            r["original_p149_eq3_add_three_to_all_payoffs_at_half"])

    def test_067_phase_receipt_no_new_real_human_E2(self):
        self.assertEqual(m.phase_receipt()["new_real_person_E2_prediction_scores"],0)

    def test_068_phase_receipt_R073_PESEN_frozen(self):
        x=m.phase_receipt()
        self.assertEqual((x["R073"],x["PESEN_v0_1"]),("FROZEN","FROZEN"))

    def test_069_trajectory_case_types_marked_project_not_actual_humans(self):
        x=m.exhaustive_216_analytic_vs_RK4()
        self.assertEqual(x["real_human_or_animal_time_series_used"],0)

    def test_070_phase_receipt_all_exact_source_fields_and_216_paths(self):
        x=m.phase_receipt()
        self.assertEqual(x["exact_fraction_2type_field_audit"]["exact_independent_fraction_fields"],75)
        self.assertEqual(x["full_continuous_paths"]["trajectory_endpoint_independent_comparisons"],216)


if __name__=="__main__":
    unittest.main()
