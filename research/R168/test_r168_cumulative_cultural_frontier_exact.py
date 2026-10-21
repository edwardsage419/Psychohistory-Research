"""R168 exact tests of artificial cultural ratchet versus group sampling artifact."""
from __future__ import annotations
import json
import unittest
from fractions import Fraction as F
from pathlib import Path
from r168_cumulative_cultural_frontier_exact import (
    GROUP_SIZES,FIDELITIES,INNOVATIONS,MODES,INITIAL_LEVELS,
    checked,individual_distribution,independent_child_distribution,
    cumulative_kernel,max_dynamic_program_kernel,analytic_path,
    independent_path,stationary,linear_fraction,expected_loss_time,
    mean_frontier,document
)


class TestR168(unittest.TestCase):
    def check_world(self,ni,fi,ui,mi,li):
        n=GROUP_SIZES[ni];f=FIDELITIES[fi];u=INNOVATIONS[ui]
        mode=MODES[mi];initial=INITIAL_LEVELS[li]
        M=cumulative_kernel(n,f,u,mode)
        self.assertEqual(M,max_dynamic_program_kernel(n,f,u,mode))
        a=analytic_path(n,f,u,mode,initial)
        b=independent_path(n,f,u,mode,initial)
        self.assertEqual(a,b)
        self.assertEqual(len(a),5)
        self.assertEqual(a[0][initial],1)
        self.assertTrue(all(len(row)==3 for row in a))
        for t,distribution in enumerate(a):
            self.assertEqual(sum(distribution,F(0)),1)
            self.assertTrue(all(isinstance(x,F) and 0<=x<=1 for x in distribution))
            self.assertTrue(0<=mean_frontier(distribution)<=2)
            if t:
                prev=a[t-1]
                for j in range(3):
                    self.assertEqual(distribution[j],sum(
                        (prev[i]*M[i][j] for i in range(3)),F(0)))
        if mode=="single_channel":
            self.assertEqual(a,analytic_path(2,f,u,mode,initial))
        if initial==0 and u==0:
            self.assertEqual(a,(a[0],)*5)
        if initial==0 and u>0:
            self.assertEqual(a[1][2],0)
            self.assertGreater(a[2][2],0)
        if u==0:
            self.assertEqual(expected_loss_time(n,f,u,mode,initial),
                             F(initial)/(1-f)**(n if mode=="full_pool" else 1))
        else:
            pi=stationary(n,f,u,mode)
            self.assertEqual(sum(pi,F(0)),1)
            self.assertTrue(all(v>0 for v in pi))

    def test_factorial_world_count(self):
        self.assertEqual(len(GROUP_SIZES)*len(FIDELITIES)*len(INNOVATIONS)*
                         len(MODES)*len(INITIAL_LEVELS),64)

    def test_full_matrix_count(self):
        self.assertEqual(len(GROUP_SIZES)*len(FIDELITIES)*len(INNOVATIONS)*len(MODES),32)

    def test_all_32_cdf_and_dynamic_max_kernels_identical(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for u in INNOVATIONS:
                    for mode in MODES:
                        self.assertEqual(cumulative_kernel(n,f,u,mode),
                                         max_dynamic_program_kernel(n,f,u,mode))

    def test_all_rows_exactly_normalized(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for u in INNOVATIONS:
                    for mode in MODES:
                        for row in cumulative_kernel(n,f,u,mode):
                            self.assertEqual(sum(row,F(0)),1)
                            self.assertTrue(all(v>=0 for v in row))

    def test_individual_children_two_independent_routes(self):
        for lev in (0,1,2):
            for f in FIDELITIES:
                for u in INNOVATIONS:
                    a=individual_distribution(lev,f,u)
                    b=independent_child_distribution(lev,f,u)
                    self.assertEqual(a,b)
                    self.assertEqual(sum(a,F(0)),1)

    def test_single_channel_matches_original_individual_distribution(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for u in INNOVATIONS:
                    for lev in (0,1,2):
                        self.assertEqual(cumulative_kernel(n,f,u,"single_channel")[lev],
                                         individual_distribution(lev,f,u))

    def test_group_sample_size_retention_formula(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for u in INNOVATIONS:
                    self.assertEqual(cumulative_kernel(n,f,u,"full_pool")[2][2],
                                     1-(1-f)**n)

    def test_single_channel_retention_equals_fidelity(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for u in INNOVATIONS:
                    self.assertEqual(cumulative_kernel(n,f,u,"single_channel")[2][2],f)

    def test_full_pool_retention_increases_with_N(self):
        for f in FIDELITIES:
            for u in INNOVATIONS:
                vals=[cumulative_kernel(n,f,u,"full_pool")[2][2] for n in GROUP_SIZES]
                self.assertTrue(all(a<b for a,b in zip(vals,vals[1:])))

    def test_single_channel_retention_invariant_with_N(self):
        for f in FIDELITIES:
            for u in INNOVATIONS:
                vals=[cumulative_kernel(n,f,u,"single_channel")[2][2] for n in GROUP_SIZES]
                self.assertEqual(len(set(vals)),1)

    def test_group_extreme_confound_three_quarters(self):
        self.assertEqual(cumulative_kernel(2,F(1,2),0,"full_pool")[2][2],F(3,4))
        self.assertEqual(cumulative_kernel(16,F(3,4),0,"single_channel")[2][2],F(3,4))

    def test_different_fidelities_can_look_identical_as_group_retention(self):
        self.assertNotEqual(F(1,2),F(3,4))
        a=analytic_path(2,F(1,2),0,"full_pool",2)
        b=analytic_path(16,F(3,4),0,"single_channel",2)
        self.assertEqual(a[1][2],b[1][2])

    def test_group_maximum_is_not_average_individual_success(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                chance=cumulative_kernel(n,f,0,"full_pool")[2][2]
                self.assertGreater(chance,f)

    def test_no_innovation_level_zero_absorbs(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for mode in MODES:
                    self.assertEqual(cumulative_kernel(n,f,0,mode)[0],(F(1),F(0),F(0)))

    def test_positive_innovation_exits_level_zero(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for mode in MODES:
                    self.assertLess(cumulative_kernel(n,f,F(1,8),mode)[0][0],1)

    def test_innovation_from_zero_cannot_jump_to_two_in_one_step(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for mode in MODES:
                    self.assertEqual(cumulative_kernel(n,f,F(1,8),mode)[0][2],0)

    def test_innovation_can_reach_two_in_two_steps(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for mode in MODES:
                    self.assertGreater(analytic_path(n,f,F(1,8),mode,0)[2][2],0)

    def test_high_skill_is_not_immortal_without_innovation(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for mode in MODES:
                    self.assertLess(cumulative_kernel(n,f,0,mode)[2][2],1)

    def test_expected_extinction_time_formula_level_one(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for mode in MODES:
                    m=n if mode=="full_pool" else 1
                    self.assertEqual(expected_loss_time(n,f,0,mode,1),1/(1-f)**m)

    def test_expected_extinction_time_formula_level_two(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for mode in MODES:
                    m=n if mode=="full_pool" else 1
                    self.assertEqual(expected_loss_time(n,f,0,mode,2),2/(1-f)**m)

    def test_expected_extinction_level_two_twice_level_one(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for mode in MODES:
                    self.assertEqual(expected_loss_time(n,f,0,mode,2),
                                     2*expected_loss_time(n,f,0,mode,1))

    def test_fhalf_pool_N2_leveltwo_loss_time_eight(self):
        self.assertEqual(expected_loss_time(2,F(1,2),0,"full_pool",2),8)

    def test_fhalf_pool_N16_leveltwo_loss_time_131072(self):
        self.assertEqual(expected_loss_time(16,F(1,2),0,"full_pool",2),131072)

    def test_larger_groups_delay_eventual_loss_without_innovation(self):
        a=[expected_loss_time(n,F(1,2),0,"full_pool",2) for n in GROUP_SIZES]
        self.assertTrue(all(x<y for x,y in zip(a,a[1:])))

    def test_one_channel_same_absorption_time_any_N(self):
        for f in FIDELITIES:
            times=[expected_loss_time(n,f,0,"single_channel",2) for n in GROUP_SIZES]
            self.assertEqual(len(set(times)),1)

    def test_positive_innovation_stationary_unique_solution(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for mode in MODES:
                    self.assertEqual(sum(stationary(n,f,F(1,8),mode),F(0)),1)

    def test_positive_innovation_stationarity_residual_zero(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for mode in MODES:
                    P=cumulative_kernel(n,f,F(1,8),mode)
                    pi=stationary(n,f,F(1,8),mode)
                    for j in range(3):
                        self.assertEqual(pi[j],sum((pi[i]*P[i][j] for i in range(3)),F(0)))

    def test_stationary_vector_all_states_positive(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for mode in MODES:
                    self.assertTrue(all(x>0 for x in stationary(n,f,F(1,8),mode)))

    def test_innovation_zero_has_no_unique_positive_stationary(self):
        for n in GROUP_SIZES:
            for f in FIDELITIES:
                for mode in MODES:
                    with self.assertRaises(ValueError): stationary(n,f,0,mode)

    def test_positive_innovation_absorption_formula_rejected(self):
        with self.assertRaises(ValueError):
            expected_loss_time(2,F(1,2),F(1,8),"full_pool",2)

    def test_group_size_not_relevant_under_single_channel_full_path(self):
        for f in FIDELITIES:
            for u in INNOVATIONS:
                for level in INITIAL_LEVELS:
                    baseline=analytic_path(2,f,u,"single_channel",level)
                    for n in GROUP_SIZES:
                        self.assertEqual(baseline,analytic_path(n,f,u,"single_channel",level))

    def test_real_experimental_data_never_claimed(self):
        d=document()
        self.assertFalse(d["source_nature2013_original_XLS_acquired"])
        self.assertFalse(d["derex2015_original_XLSX_acquired"])
        self.assertFalse(d["original_author_model_reproduced"])
        self.assertFalse(d["2014_criticism_resolved"])
        self.assertEqual(d["external_real_human_rows_scored"],0)

    def test_invalid_population(self):
        for value in (-1,0,1,3,5,32,False,True,2.0,"2"):
            with self.assertRaises(ValueError):
                checked(value,F(1,2),0,"full_pool")

    def test_invalid_fidelity(self):
        for value in (-1,0,F(1,4),1,False,True,0.5,"1/2"):
            with self.assertRaises(ValueError):
                checked(2,value,0,"full_pool")

    def test_invalid_innovation(self):
        for value in (-1,F(1,16),1,False,True,0.125,"1/8"):
            with self.assertRaises(ValueError):
                checked(2,F(1,2),value,"full_pool")

    def test_invalid_mode(self):
        for mode in ("pool","single","",False,True,None,0):
            with self.assertRaises(ValueError):
                checked(2,F(1,2),0,mode)

    def test_invalid_skill_frontier(self):
        for level in (-1,3,False,True,F(1,2),2.0,"2"):
            with self.assertRaises(ValueError):
                checked(2,F(1,2),0,"full_pool",level)

    def test_invalid_horizon(self):
        for h in (-1,False,True,F(1,2),2.0,"4"):
            with self.assertRaises(ValueError):
                analytic_path(2,F(1,2),0,"full_pool",2,h)
            with self.assertRaises(ValueError):
                independent_path(2,F(1,2),0,"full_pool",2,h)

    def test_invalid_child_distribution_controls(self):
        for bad in (-1,3,True,F(1,2)):
            with self.assertRaises(ValueError):
                individual_distribution(bad,F(1,2),0)

    def test_invalid_mean_vector(self):
        for row in ((F(1),F(1),F(0)),(F(1),),(-F(1),F(1),F(1))):
            with self.assertRaises(ValueError):
                mean_frontier(row)

    def test_singular_balance_system_rejected(self):
        with self.assertRaises(ValueError):
            linear_fraction([[1,0],[0,0]],[1,2])

    def test_json_document_has_full_64_worlds(self):
        d=document()
        self.assertEqual(d["world_count"],64)
        self.assertEqual(len(d["worlds"]),64)
        self.assertEqual(len({w["id"] for w in d["worlds"]}),64)
        self.assertTrue(all(w["exact_independent_paths_equal"] for w in d["worlds"]))
        self.assertTrue(all(len(w["points"])==5 for w in d["worlds"]))

    def test_json_document_has_full_32_kernels(self):
        d=document()
        self.assertEqual(d["kernel_count"],32)
        self.assertEqual(len(d["kernels"]),32)
        self.assertTrue(all(len(k["kernel"])==3 for k in d["kernels"]))

    def test_prescored_counterexamples(self):
        c=document()["predeclared_controls"]
        self.assertEqual(c["N2_full_pool_fhalf_top_retention"],"3/4")
        self.assertEqual(c["N16_single_channel_fthreequarters_top_retention"],"3/4")
        self.assertEqual(c["full_pool_fhalf_level2_absorption_N2"],"8")
        self.assertEqual(c["full_pool_fhalf_level2_absorption_N16"],"131072")
        self.assertTrue(c["single_channel_any_N_identical"])

    def test_replay_original_json_exact_bytes(self):
        p=Path(__file__).with_name("R168_EXACT_RESULTS.json")
        if not p.exists():self.skipTest("CI must generate full JSON before testing")
        self.assertEqual(p.read_bytes(),
                         (json.dumps(document(),sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode())


for ni in range(len(GROUP_SIZES)):
    for fi in range(len(FIDELITIES)):
        for ui in range(len(INNOVATIONS)):
            for mi in range(len(MODES)):
                for li in range(len(INITIAL_LEVELS)):
                    def builder(ni=ni,fi=fi,ui=ui,mi=mi,li=li):
                        def test(self):
                            self.check_world(ni,fi,ui,mi,li)
                        return test
                    setattr(TestR168,f"test_frozen_n{ni}_f{fi}_u{ui}_m{mi}_l{li}",builder())


if __name__=="__main__":
    unittest.main()
