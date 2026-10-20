"""R132: independent Taylor/Jonker 1978 Eq2/Eq3/Eq4 and trajectory audits."""
import unittest
from fractions import Fraction as F
from math import prod
from unittest.mock import patch
import r132_replicator_1978_exact_invariants_and_trajectories as m


def p(i,j,k):return (F(i),F(j),F(k))


class Original1978EquationsAndSimplexInvariants(unittest.TestCase):
    def test_001_original_source_DOI_in_module(self):
        self.assertIn("10.1016/0025-5564(78)90077-9",m.__doc__)
    def test_002_original_cyclic_matrix_exact(self):
        self.assertEqual(m.source_cyclic_1978(),
            ((F(-1,2),F(1),F(-1)),(F(-1),F(-1,2),F(1)),(F(1),F(-1),F(-1,2))))
    def test_003_original_alpha_matrix_exact(self):
        self.assertEqual(m.source_alpha_1978(),
                         ((F(2),F(1),F(5)),(F(5),F(1),F(0)),(F(1),F(4),F(3))))
    def test_004_exact_payoffs_source_cyclic_uniform(self):
        self.assertEqual(m.exact_payoff_each(m.source_cyclic_1978(),(F(1,3),)*3),(F(-1,6),)*3)
    def test_005_cyclic_uniform_stationary_field(self):
        self.assertEqual(m.source_original_eq2_exact_field(m.source_cyclic_1978(),(F(1,3),)*3),(F(0),)*3)
    def test_006_cyclic_uniform_discrete_fixed_point(self):
        self.assertEqual(m.source_original_eq3_exact_generation(m.source_cyclic_1978(),(F(1,3),)*3),(F(1,3),)*3)
    def test_007_source_eq4_exactly_eq3_minus_identity(self):
        x=(F(1,2),F(1,3),F(1,6));A=m.source_cyclic_1978()
        nxt=m.source_original_eq3_exact_generation(A,x)
        inc=m.source_original_eq4_exact_increment(A,x)
        self.assertEqual(tuple(x[i]+inc[i] for i in range(3)),nxt)
    def test_008_original_eq3_not_generic_forward_Euler_unit_step(self):
        x=(F(1,2),F(1,3),F(1,6));A=m.source_cyclic_1978()
        nxt=m.source_original_eq3_exact_generation(A,x)
        naive=tuple(x[i]+m.source_original_eq2_exact_field(A,x)[i] for i in range(3))
        self.assertNotEqual(nxt,naive)
    def test_009_original_eq3_uses_one_plus_fitness(self):
        A=m.source_cyclic_1978()
        x=(F(1,2),F(1,3),F(1,6))
        f=m.exact_payoff_each(A,x)
        mean=sum((x[i]*f[i] for i in range(3)),F(0))
        self.assertEqual(m.source_original_eq3_exact_generation(A,x),
                         tuple(x[i]*(F(1)+f[i])/(F(1)+mean) for i in range(3)))
    def test_010_two_independent_eq2_fields_identical_at_off_center_state(self):
        A=m.source_alpha_1978();x=(F(1,2),F(1,3),F(1,6))
        self.assertEqual(m.source_original_eq2_exact_field(A,x),
                         m.exact_eq2_independent_pairwise_field(A,x))
    def test_011_pairwise_independent_eq2_does_not_call_source_field(self):
        A=m.zero_sum_rps_project();x=(F(1,2),F(1,3),F(1,6))
        with patch.object(m,"source_original_eq2_exact_field",side_effect=AssertionError("SOURCE")):
            self.assertEqual(sum(m.exact_eq2_independent_pairwise_field(A,x),F(0)),F(0))
    def test_012_source_eq2_does_not_call_pairwise(self):
        A=m.zero_sum_rps_project();x=(F(1,2),F(1,3),F(1,6))
        with patch.object(m,"exact_eq2_independent_pairwise_field",side_effect=AssertionError("PAIRWISE")):
            self.assertEqual(sum(m.source_original_eq2_exact_field(A,x),F(0)),F(0))
    def test_013_exact_field_no_spontaneous_absent_strategy(self):
        for A in (m.source_cyclic_1978(),m.source_alpha_1978(),m.zero_sum_rps_project()):
            x=(F(0),F(1,4),F(3,4))
            self.assertEqual(m.source_original_eq2_exact_field(A,x)[0],F(0))
            self.assertEqual(m.source_original_eq3_exact_generation(A,x)[0],F(0))
    def test_014_all_84_source_fields_match_independent(self):
        x=m.exact_replicator_invariant_grid()
        self.assertEqual(x["exact_field_vs_independent_pairwise_comparisons"],84)
    def test_015_84_original_discrete_generation_exact_eq4(self):
        self.assertEqual(m.exact_replicator_invariant_grid()[
            "source_1978_original_eq3_vs_eq4_increment_checks"],84)
    def test_016_252_constant_payoff_shifts(self):
        self.assertEqual(m.exact_replicator_invariant_grid()[
            "constant_payoff_shift_invariance_checks"],252)
    def test_017_252_positive_payoff_scalings(self):
        self.assertEqual(m.exact_replicator_invariant_grid()[
            "positive_payoff_time_scale_checks"],252)
    def test_018_three_matrices_each_28_simplex_states(self):
        x=m.exact_replicator_invariant_grid()
        self.assertEqual((x["payoff_matrices_checked"],
                          x["three_strategy_simplex_states_per_matrix"]),(3,28))
    def test_019_constant_shift_independent_math_exact(self):
        A=m.skyrms_stag_project_flow();x=(F(1,4),F(3,4))
        raised=tuple(tuple(v+F(8) for v in row) for row in A)
        self.assertEqual(m.source_original_eq2_exact_field(A,x),
                         m.source_original_eq2_exact_field(raised,x))
    def test_020_payoff_times_three_scales_field_exact(self):
        A=m.chicken_project_flow();x=(F(4,5),F(1,5))
        scaled=tuple(tuple(3*v for v in row) for row in A)
        self.assertEqual(m.source_original_eq2_exact_field(scaled,x),
                         tuple(3*v for v in m.source_original_eq2_exact_field(A,x)))
    def test_021_source_1978_invalid_3x3_matrix_shape(self):
        for A in ((),((F(1),),),((F(0),F(0)),(F(0),)),(F(1),F(2))):
            with self.subTest(A=A),self.assertRaises(m.ReplicatorDomainError):
                m.source_original_eq2_exact_field(A,(F(1,2),F(1,2)))
    def test_022_reject_nonfraction_or_bool_payoffs(self):
        for a in (0,0.5,True,False,"0",None):
            with self.subTest(a=a),self.assertRaises(m.ReplicatorDomainError):
                m.source_original_eq2_exact_field(((a,F(0)),(F(0),F(0))),
                                                  (F(1,2),F(1,2)))
    def test_023_reject_non_simplex_and_non_fractions(self):
        for x in ((F(1),F(1)),(F(-1),F(2)),(1,0),(True,F(0)),(F(1),),(),(F(1,3),F(1,3))):
            with self.subTest(x=x),self.assertRaises(m.ReplicatorDomainError):
                m.source_original_eq2_exact_field(m.chicken_project_flow(),x)
    def test_024_discrete_source_reproduction_negative_baseline_rejected(self):
        A=((F(-2),F(-2)),(F(0),F(0)))
        with self.assertRaises(m.ReplicatorDomainError):
            m.source_original_eq3_exact_generation(A,(F(1,2),F(1,2)))
    def test_025_source_parameter_rejects_wrong_types_and_range(self):
        for bad in (0,0.5,True,F(0),F(-1),F(2),"1/2"):
            with self.subTest(eps=bad),self.assertRaises(m.ReplicatorDomainError):
                m.source_cyclic_1978(bad)
        for bad in (1,1.0,True,"1"):
            with self.subTest(alpha=bad),self.assertRaises(m.ReplicatorDomainError):
                m.source_alpha_1978(bad)


class ExactTwoStrategyBasinsAndOriginalModelSeparation(unittest.TestCase):
    def test_026_stag_two_type_row_payoff_is_four_zero_three_three(self):
        self.assertEqual(m.skyrms_stag_project_flow(),((F(4),F(0)),(F(3),F(3))))
    def test_027_chicken_two_type_row_payoff_is_negative_two_two_zero_one(self):
        self.assertEqual(m.chicken_project_flow(),((F(-2),F(2)),(F(0),F(1))))
    def test_028_logistic_constant_advantage_payoff_is_2_vs_1(self):
        self.assertEqual(m.constant_advantage_project(),((F(2),F(2)),(F(1),F(1))))
    def test_029_stag_source_based_continuous_field_at_one_half_negative_one_quarter(self):
        self.assertEqual(m.exact_two_type_scalar_derivative(m.skyrms_stag_project_flow(),F(1,2)),
                         F(-1,4))
    def test_030_stag_critical_at_three_quarters_zero(self):
        self.assertEqual(m.exact_two_type_scalar_derivative(m.skyrms_stag_project_flow(),F(3,4)),0)
    def test_031_stag_above_threshold_four_fifths_positive_four_over125(self):
        self.assertEqual(m.exact_two_type_scalar_derivative(m.skyrms_stag_project_flow(),F(4,5)),
                         F(4,125))
    def test_032_chicken_critical_at_one_third_zero(self):
        self.assertEqual(m.exact_two_type_scalar_derivative(m.chicken_project_flow(),F(1,3)),0)
    def test_033_chicken_below_critical_rises(self):
        self.assertGreater(m.exact_two_type_scalar_derivative(m.chicken_project_flow(),F(1,4)),0)
    def test_034_chicken_above_critical_falls(self):
        self.assertLess(m.exact_two_type_scalar_derivative(m.chicken_project_flow(),F(4,5)),0)
    def test_035_constant_advantage_logistic_field_at_quarter_three_sixteenth(self):
        self.assertEqual(m.exact_two_type_scalar_derivative(m.constant_advantage_project(),F(1,4)),F(3,16))
    def test_036_all_two_strategy_static_exact_basin_sign_comparisons(self):
        self.assertEqual(m.exact_two_type_source_based_sign_audit()[
            "two_type_13_grid_cross_checks"],39)
    def test_037_two_type_interiors_stag_three_quarters_chicken_one_third(self):
        z=m.exact_two_type_source_based_sign_audit()["two_type_models"]
        self.assertEqual(z["stag_hare"]["exact_interior_fixed_point"],"3/4")
        self.assertEqual(z["chicken"]["exact_interior_fixed_point"],"1/3")
        self.assertIsNone(z["constant_advantage"]["exact_interior_fixed_point"])
    def test_038_two_type_reduction_independent_full_eq2(self):
        for A in (m.constant_advantage_project(),m.skyrms_stag_project_flow(),m.chicken_project_flow()):
            for k in range(13):
                x=F(k,12)
                s=m.exact_two_type_scalar_derivative(A,x)
                self.assertEqual(m.source_original_eq2_exact_field(A,(x,1-x)),(s,-s))
    def test_039_logistic_closed_form_zero_one_absorbing(self):
        self.assertEqual(m.logistic_constant_advantage_closed(0.0,3),0.0)
        self.assertEqual(m.logistic_constant_advantage_closed(1.0,3),1.0)
    def test_040_logistic_at_time_zero_equals_initial(self):
        self.assertAlmostEqual(m.logistic_constant_advantage_closed(0.25,0),0.25,places=14)
    def test_041_logistic_closed_form_time_two_between_quarter_and_one(self):
        x=m.logistic_constant_advantage_closed(0.25,2)
        self.assertTrue(.25<x<1)
    def test_042_logistic_invalid_initial_and_time_rejected(self):
        for x in (0,1,True,"0.25",-0.1,1.1,float("nan")):
            with self.subTest(x=x),self.assertRaises(m.ReplicatorDomainError):
                m.logistic_constant_advantage_closed(x,2)
        for t in (-1,21,True,None,float("nan")):
            with self.subTest(t=t),self.assertRaises(m.ReplicatorDomainError):
                m.logistic_constant_advantage_closed(0.25,t)


class NumericFullTrajectoryAndInvariantAudit(unittest.TestCase):
    def test_043_euler_logistic_terminal_n320_moves_up(self):
        x=m.numerical_trajectory(m.constant_advantage_project(),(.25,.75),2.0,320,"euler")
        self.assertTrue(.25<x[0]<1)
    def test_044_rk4_logistic_better_than_euler_at_n40(self):
        a=m.constant_advantage_project()
        exact=m.logistic_constant_advantage_closed(.25,2.0)
        e=m.numerical_trajectory(a,(.25,.75),2.0,40,"euler")[0]
        rk=m.numerical_trajectory(a,(.25,.75),2.0,40,"rk4")[0]
        self.assertLess(abs(rk-exact),abs(e-exact))
    def test_045_rk4_logistic_n320_absolute_error_less_1e_minus11(self):
        a=m.constant_advantage_project()
        exact=m.logistic_constant_advantage_closed(.25,2.0)
        x=m.numerical_trajectory(a,(.25,.75),2.0,320,"rk4")[0]
        self.assertLess(abs(x-exact),1e-11)
    def test_046_all_logistic_grid_errors_strictly_decrease(self):
        z=m.numerical_replicator_audit()
        self.assertTrue(all(z["logistic_RK4_absolute_errors"][i]>z["logistic_RK4_absolute_errors"][i+1] for i in range(3)))
        self.assertTrue(all(z["logistic_euler_absolute_errors"][i]>z["logistic_euler_absolute_errors"][i+1] for i in range(3)))
    def test_047_stag_initial_half_moves_down_by_time8(self):
        self.assertLess(m.numerical_trajectory(m.skyrms_stag_project_flow(),(.5,.5),8.0,320,"rk4")[0],.5)
    def test_048_stag_initial_four_fifths_moves_up_by_time8(self):
        self.assertGreater(m.numerical_trajectory(m.skyrms_stag_project_flow(),(.8,.2),8.0,320,"rk4")[0],.8)
    def test_049_stag_exact_threshold_remains_fixed(self):
        self.assertAlmostEqual(m.numerical_trajectory(m.skyrms_stag_project_flow(),(.75,.25),8.0,320,"rk4")[0],.75,places=12)
    def test_050_chicken_initial_one_tenth_rises_to_interior(self):
        x=m.numerical_trajectory(m.chicken_project_flow(),(.1,.9),8.0,320,"rk4")[0]
        self.assertTrue(.1<x<1/3)
    def test_051_chicken_initial_four_fifths_falls_to_interior(self):
        x=m.numerical_trajectory(m.chicken_project_flow(),(.8,.2),8.0,320,"rk4")[0]
        self.assertTrue(1/3<x<.8)
    def test_052_numeric_trajectory_records_every_step(self):
        a=m.constant_advantage_project()
        path=m.numerical_trajectory(a,(.25,.75),2.0,40,"rk4",record=True)
        self.assertEqual(len(path),41)
        self.assertEqual(path[0],(.25,.75))
    def test_053_numeric_trajectory_masses_near_one_at_all_steps(self):
        path=m.numerical_trajectory(m.zero_sum_rps_project(),(.5,.3,.2),12.0,160,"rk4",record=True)
        self.assertTrue(all(abs(sum(x)-1)<1e-11 for x in path))
        self.assertTrue(all(all(v>0 for v in x) for x in path))
    def test_054_rps_zero_sum_payoff_matrix_antisymmetric(self):
        A=m.zero_sum_rps_project()
        self.assertEqual(tuple(sum((A[i][j] for i in range(3)),F(0)) for j in range(3)),
                         (F(0),F(0),F(0)))
        for i in range(3):
            for j in range(3):
                self.assertEqual(A[i][j],-A[j][i])
    def test_055_rps_exact_log_product_invariant_ten_interiors(self):
        z=m.zero_sum_rps_exact_log_product_invariant_grid()
        self.assertEqual(z["interior_exact_simplex_state_checks"],10)
    def test_056_rps_initial_product_exact_three_percent(self):
        self.assertAlmostEqual(prod((.5,.3,.2)),.03,places=14)
    def test_057_rps_euler_integrator_artificially_reduces_product(self):
        y=m.numerical_trajectory(m.zero_sum_rps_project(),(.5,.3,.2),12.0,40,"euler")
        self.assertLess(prod(y),.03-.001)
    def test_058_rps_rk4_preserves_product_better_than_euler(self):
        A=m.zero_sum_rps_project()
        e=m.numerical_trajectory(A,(.5,.3,.2),12.0,40,"euler")
        rk=m.numerical_trajectory(A,(.5,.3,.2),12.0,40,"rk4")
        self.assertLess(abs(prod(rk)-.03),abs(prod(e)-.03))
    def test_059_rps_rk4_n320_product_error_under_one_billionth(self):
        y=m.numerical_trajectory(m.zero_sum_rps_project(),(.5,.3,.2),12.0,320,"rk4")
        self.assertLess(abs(prod(y)-.03),1e-9)
    def test_060_rps_euler_n320_still_has_large_artificial_invariant_drift(self):
        y=m.numerical_trajectory(m.zero_sum_rps_project(),(.5,.3,.2),12.0,320,"euler")
        self.assertGreater(abs(prod(y)-.03),1e-4)
    def test_061_rps_numeric_errors_across_4_steps_frozen(self):
        z=m.numerical_replicator_audit()["numeric_T12_RPS_comparison"]
        self.assertEqual(set(z),{"40","80","160","320"})
        self.assertTrue(all(z[k]["euler_product_error"]<0 for k in z))
    def test_062_source_original_discrete_update_is_not_euler_or_rk4(self):
        self.assertTrue(m.numerical_replicator_audit()[
            "this_numerical_drift_is_not_original_Taylor_Jonker_discrete_Eq3"])
    def test_063_numeric_rejects_illegal_step_counts_and_large_step(self):
        for steps in (0,4097,True,False,2.0,"40",1):
            with self.subTest(steps=steps),self.assertRaises(m.ReplicatorDomainError):
                m.numerical_trajectory(m.constant_advantage_project(),(.25,.75),2.0,steps,"euler")
    def test_064_numeric_rejects_illegal_float_initials(self):
        for x in ((.5,),(.5,.6),(F(1,2),F(1,2)),(True,0.0),
                  (float("nan"),.5),(-.1,1.1),(1.0,1.0)):
            with self.subTest(x=x),self.assertRaises(m.ReplicatorDomainError):
                m.numerical_trajectory(m.constant_advantage_project(),x,2.0,40,"rk4")
    def test_065_numeric_rejects_unrecognized_methods_and_time(self):
        for method in ("RK4","rk45","",None,1):
            with self.subTest(method=method),self.assertRaises(m.ReplicatorDomainError):
                m.numerical_trajectory(m.constant_advantage_project(),(.25,.75),2.0,40,method)
        for time in (0,2,True,21.0,-1.0,float("inf")):
            with self.subTest(time=time),self.assertRaises(m.ReplicatorDomainError):
                m.numerical_trajectory(m.constant_advantage_project(),(.25,.75),time,40,"rk4")
    def test_066_float_numerical_integrator_does_not_call_exact_source_field(self):
        with patch.object(m,"source_original_eq2_exact_field",side_effect=AssertionError("NO_EXACT")):
            self.assertGreater(m.numerical_trajectory(
                m.constant_advantage_project(),(.25,.75),2.0,80,"rk4")[0],.25)
    def test_067_exact_source_field_does_not_call_numerical_integrator(self):
        with patch.object(m,"numerical_trajectory",side_effect=AssertionError("NO_NUMERIC")):
            self.assertEqual(m.source_original_eq2_exact_field(
                m.constant_advantage_project(),(F(1,4),F(3,4))),
                (F(3,16),F(-3,16)))
    def test_068_receipt_explicit_no_real_human_E2(self):
        self.assertEqual(m.phase_receipt()["new_real_human_E2_prediction_scores"],0)
    def test_069_source_published_phase_portraits_not_claimed_fully_recreated(self):
        self.assertFalse(m.phase_receipt()["original_1978_full_population_nonlinear_phase_portraits_recreated"])
    def test_070_R073_and_PESEN_still_frozen(self):
        r=m.phase_receipt()
        self.assertEqual((r["R073"],r["PESEN_v0_1"]),("FROZEN","FROZEN"))


if __name__=="__main__":
    unittest.main()
