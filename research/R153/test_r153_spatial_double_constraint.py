"""R153 tests: independent 3x3 IPF, exact 2x2, structural zeros, identifiability."""
import unittest
from decimal import Decimal as D, getcontext
from fractions import Fraction as F
from functools import lru_cache
import json
import r153_spatial_double_constraint as m

@lru_cache(maxsize=1)
def all_results(): return m.output()

class TestR153(unittest.TestCase):
    def test_001_registered_24_unique(self):
        a=list(m.spec_cases());self.assertEqual(len(a),24);self.assertEqual(len(set(a)),24)
    def test_002_full_results(self):
        self.assertEqual(len(all_results()['scenarios']),24)
    def test_003_decimal_precision(self):self.assertGreaterEqual(getcontext().prec,65)
    def test_004_iteration_cap_amended(self):self.assertEqual(m.MAX_ITERATIONS,450)
    def test_005_residual_threshold_frozen(self):self.assertEqual(m.RESIDUAL_TOL,D('1e-25'))
    def test_006_disagreement_threshold_frozen(self):self.assertEqual(m.METHOD_TOL,D('1e-24'))
    def test_007_three_origins_each(self):
        for c in all_results()['scenarios']:self.assertEqual(len(c['balanced_flow_28dp']),3)
    def test_008_three_destinations_each(self):
        for c in all_results()['scenarios']:
            self.assertTrue(all(len(row)==3 for row in c['balanced_flow_28dp']))
    def test_009_row_margin_24(self):
        for c in all_results()['scenarios']:
            for i,row in enumerate(c['balanced_flow_28dp']):
                self.assertLess(abs(sum(map(D,row))-D(c['origin_budgets'][i])),D('1e-25'))
    def test_010_column_margin_24(self):
        for c in all_results()['scenarios']:
            for j in range(3):
                self.assertLess(abs(sum(D(row[j]) for row in c['balanced_flow_28dp'])-D(c['destination_budgets'][j])),D('1e-25'))
    def test_011_positive_balanced_flow_24(self):
        for c in all_results()['scenarios']:
            self.assertTrue(all(D(v)>0 for row in c['balanced_flow_28dp'] for v in row))
    def test_012_both_methods_converged(self):
        for c in all_results()['scenarios']:
            self.assertLessEqual(D(c['direct_max_balance_residual']),m.RESIDUAL_TOL)
            self.assertLessEqual(D(c['independent_max_balance_residual']),m.RESIDUAL_TOL)
    def test_013_both_methods_agree(self):
        for c in all_results()['scenarios']:
            self.assertLessEqual(D(c['max_algorithm_disagreement']),m.METHOD_TOL)
    def test_014_amended_iteration_cap_suffices(self):
        self.assertLessEqual(max(max(c['direct_iterations'],c['independent_scaler_iterations']) for c in all_results()['scenarios']),450)
    def test_015_amendment_is_actually_necessary(self):
        self.assertGreater(max(c['direct_iterations'] for c in all_results()['scenarios']),150)
    def test_016_two_by_two_witness(self):
        d=m.exact_two_by_two_witness();self.assertEqual(d['balanced'],[['3/2','1/2'],['3/2','3/2']])
    def test_017_two_by_two_cross_ratio(self):self.assertEqual(m.exact_two_by_two_witness()['cross_product_ratio'],'3')
    def test_018_positive_kernel_alpha0(self):self.assertEqual(m.kernel('near',0,'flat'),tuple((D(1),)*3 for _ in range(3)))
    def test_019_origin_only_rows(self):
        K=m.kernel('near',2,'flat');v=m.origin_only(K,m.MARGINS['m0'][0]);self.assertEqual([sum(row) for row in v],list(map(D,m.MARGINS['m0'][0])))
    def test_020_origin_only_not_destination_constrained(self):
        self.assertGreater(D(m.run_case('near',2,'flat','m0')['origin_only_destination_gap_28dp']),0)
    def test_021_balanced_rerouting_positive(self):
        self.assertGreater(D(m.run_case('far',2,'flat','m1')['rerouting_L1_gap_28dp']),0)
    def test_022_alpha0_exacts_outer_product(self):
        for c in all_results()['scenarios']:
            if c['exponent']==0:
                r,d=m.MARGINS[c['margin']]
                for i in range(3):
                    for j in range(3):self.assertLess(abs(D(c['balanced_flow_28dp'][i][j])-D(F(r[i]*d[j],60).numerator)/D(F(r[i]*d[j],60).denominator)),D('1e-24'))
    def test_023_flat_and_column_attraction_invariant(self):
        self.assertTrue(all_results()['all_column_multiplier_effects_absorbed_by_destination_constraint'])
    def test_024_alpha1_and_alpha2_have_different_flows(self):
        a=m.run_case('near',1,'flat','m0')['balanced_flow_28dp'];b=m.run_case('near',2,'flat','m0')['balanced_flow_28dp'];self.assertNotEqual(a,b)
    def test_025_layout_effect_at_positive_alpha(self):
        a=m.run_case('near',1,'flat','m0')['balanced_flow_28dp'];b=m.run_case('far',1,'flat','m0')['balanced_flow_28dp'];self.assertNotEqual(a,b)
    def test_026_equal_margins_support_possible(self):self.assertTrue(m.hall_feasible(((1,0),(0,1)),(1,1),(1,1)))
    def test_027_mismatched_support_infeasible(self):self.assertFalse(m.hall_feasible(((1,0),(0,1)),(2,1),(1,2)))
    def test_028_three_by_three_full_support_feasible(self):self.assertTrue(m.hall_feasible(((1,1,1),)*3,*m.MARGINS['m0']))
    def test_029_three_by_three_no_outgoing_infeasible(self):self.assertFalse(m.hall_feasible(((0,0,0),(1,1,1),(1,1,1)),*m.MARGINS['m0']))
    def test_030_zero_kernel_refused_by_strict_positive_IPF(self):
        with self.assertRaises(ValueError):m.positive_kernel(((D(1),D(0),D(1)),(D(1),)*3,(D(1),)*3))
    def test_031_negative_kernel_refused(self):
        with self.assertRaises(ValueError):m.positive_kernel(((D(1),D(-1),D(1)),(D(1),)*3,(D(1),)*3))
    def test_032_NaN_kernel_refused(self):
        with self.assertRaises(ValueError):m.positive_kernel(((D('NaN'),D(1),D(1)),(D(1),)*3,(D(1),)*3))
    def test_033_bool_margins_rejected(self):
        with self.assertRaises(TypeError):m.validate_margins((True,20,30),(15,25,20))
    def test_034_float_margins_rejected(self):
        with self.assertRaises(TypeError):m.validate_margins((10.0,20,30),(15,25,20))
    def test_035_negative_margins_rejected(self):
        with self.assertRaises(ValueError):m.validate_margins((-10,20,50),(15,25,20))
    def test_036_zero_margins_rejected(self):
        with self.assertRaises(ValueError):m.validate_margins((0,20,40),(15,25,20))
    def test_037_mismatched_margins_rejected(self):
        with self.assertRaises(ValueError):m.validate_margins((10,20,30),(15,25,21))
    def test_038_wrong_vector_length_rejected(self):
        with self.assertRaises(ValueError):m.vector((1,2))
    def test_039_unknown_layout_rejected(self):
        with self.assertRaises(ValueError):m.kernel('unknown',1,'flat')
    def test_040_unknown_attraction_rejected(self):
        with self.assertRaises(ValueError):m.kernel('near',1,'unknown')
    def test_041_unknown_exponent_rejected(self):
        with self.assertRaises(ValueError):m.kernel('near',3,'flat')
    def test_042_bool_exponent_rejected(self):
        with self.assertRaises(TypeError):m.kernel('near',True,'flat')
    def test_043_float_exponent_rejected(self):
        with self.assertRaises(TypeError):m.kernel('near',1.0,'flat')
    def test_044_unknown_margin_scheme_rejected(self):
        with self.assertRaises(ValueError):m.run_case('near',1,'flat','unknown')
    def test_045_nondecimal_kernel_rejected(self):
        with self.assertRaises(TypeError):m.positive_kernel(((1,2,3),(4,5,6),(7,8,9)))
    def test_046_nonsquare_kernel_rejected(self):
        with self.assertRaises(ValueError):m.positive_kernel(((D(1),D(1)),(D(1),D(1))))
    def test_047_negative_support_rejected(self):
        with self.assertRaises(ValueError):m.hall_feasible(((1,-1),(1,1)),(1,1),(1,1))
    def test_048_float_support_rejected(self):
        with self.assertRaises(TypeError):m.hall_feasible(((1,0.0),(0,1)),(1,1),(1,1))
    def test_049_unsupported_support_shape_rejected(self):
        with self.assertRaises(ValueError):m.hall_feasible(((1,),),(1,),(1,))
    def test_050_support_total_mismatch_rejected(self):
        with self.assertRaises(ValueError):m.hall_feasible(((1,0),(0,1)),(2,1),(1,1))
    def test_051_canonical_json_deterministic(self):self.assertEqual(m.canonical_json(),m.canonical_json())
    def test_052_json_parse_replay(self):self.assertEqual(json.loads(m.canonical_json())['scenarios_count'],24)
    def test_053_no_fake_empirical_claim(self):self.assertFalse(all_results()['original_author_historical_data_reproduced'])
    def test_054_historical_source_access_declared(self):self.assertEqual(all_results()['source_SinkhornKnopp1967_print_pages_visually_read'],[343,344])
    def test_055_e2_e3_zero(self):self.assertEqual((all_results()['new_E2'],all_results()['new_E3']),(0,0))
    def test_056_double_constraint_is_distinct_from_R152(self):
        self.assertTrue(any(D(x['rerouting_L1_gap_28dp'])>0 for x in all_results()['scenarios']))

def _scenario_test(spec):
    def check(self):
        cfg=m.run_case(*spec)
        k=m.kernel(spec[0],spec[1],spec[2]);r,c=m.MARGINS[spec[3]]
        p,it,e=m.ipf_matrix_direct(k,r,c)
        q,it2,e2=m.ipf_independent_scalers(k,r,c)
        self.assertLessEqual(e,m.RESIDUAL_TOL);self.assertLessEqual(e2,m.RESIDUAL_TOL)
        self.assertLessEqual(max(abs(p[i][j]-q[i][j]) for i in range(3) for j in range(3)),m.METHOD_TOL)
        self.assertEqual(it,cfg['direct_iterations'])
    return check
for idx,spec in enumerate(m.spec_cases()):
    setattr(TestR153,f'test_2{idx:03d}_parameter_{spec[0]}_a{spec[1]}_{spec[2]}_{spec[3]}',_scenario_test(spec))

def _col_absorption_test(layout,alpha,margin):
    def check(self):
        a=m.ipf_matrix_direct(m.kernel(layout,alpha,'flat'),*m.MARGINS[margin])[0]
        b=m.ipf_matrix_direct(m.kernel(layout,alpha,'column_bonus'),*m.MARGINS[margin])[0]
        self.assertLessEqual(max(abs(a[i][j]-b[i][j]) for i in range(3) for j in range(3)),m.METHOD_TOL)
    return check
for idx,(layout,alpha,margin) in enumerate(__import__('itertools').product(m.LAYOUTS,m.EXPONENTS,m.MARGINS)):
    setattr(TestR153,f'test_3{idx:03d}_column_absorption_{layout}_a{alpha}_{margin}',_col_absorption_test(layout,alpha,margin))

def _origin_gap_test(spec):
    def check(self):
        v=m.run_case(*spec)
        self.assertGreater(D(v['origin_only_destination_gap_28dp']),0)
        self.assertGreater(D(v['rerouting_L1_gap_28dp']),0)
    return check
for idx,spec in enumerate(m.spec_cases()):
    setattr(TestR153,f'test_4{idx:03d}_requires_rebalancing_{spec[0]}_a{spec[1]}_{spec[2]}_{spec[3]}',_origin_gap_test(spec))

if __name__=='__main__':unittest.main()
