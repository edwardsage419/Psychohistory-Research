"""R157 authentic structural-pressure E1 tests.

Checks refer to a synthetic dynamic and the schematic published PSI product.
No claim is made that these are empirical political-instability forecasts.
"""
import json
import unittest
from fractions import Fraction as F
from pathlib import Path
from r157_structural_pressure_exact import (
    TARGETS,LAGS,RELIEFS,HORIZON,ZERO,unit,valid_params,
    scoring,step,direct_history,matrix_history,record
)


class TestPressure(unittest.TestCase):
    def check_world(self,hi,ai,bi,ci,ri):
        h,a,b,c,r=(TARGETS[hi],LAGS[ai],LAGS[bi],LAGS[ci],RELIEFS[ri])
        path=direct_history(h,a,b,c,r)
        independent=matrix_history(h,a,b,c,r)
        self.assertEqual(path,independent)
        self.assertEqual(len(path),13)
        self.assertEqual(path[0],ZERO)
        for t,state in enumerate(path):
            psi,mean=scoring(state)
            self.assertGreaterEqual(psi,0)
            self.assertLessEqual(psi,1)
            self.assertGreaterEqual(mean,0)
            self.assertLessEqual(mean,1)
            self.assertTrue(all(F(0)<=x<=F(1) for x in state))
            if t<12:
                self.assertEqual(path[t+1],(
                    (1-a)*state[0]+a*h,
                    (1-b)*state[1]+b*state[0],
                    (1-c)*state[2]+c*(1-r)*state[1]
                ))
        self.assertEqual(path[1],(a*h,F(0),F(0)))
        self.assertEqual(path[2][2],F(0))
        if r==1:
            self.assertTrue(all(s[2]==0 for s in path))

    def test_frozen_world_count(self):
        self.assertEqual(len(TARGETS)*len(LAGS)**3*len(RELIEFS),72)

    def test_initial_zero_vector(self):
        self.assertEqual(direct_history(1,F(1,4),F(1,4),F(1,4),0,0),(ZERO,))

    def test_first_mass_onset(self):
        self.assertEqual(direct_history(1,F(1,4),F(1,4),F(1,4),0)[1],
                         (F(1,4),F(0),F(0)))

    def test_second_elite_onset(self):
        p=direct_history(1,F(1,4),F(1,4),F(1,4),0)
        self.assertEqual(p[2][1],F(1,16))
        self.assertEqual(p[2][2],F(0))

    def test_third_fiscal_onset(self):
        p=direct_history(1,F(1,4),F(1,4),F(1,4),0)
        self.assertEqual(p[3][2],F(1,64))
        self.assertEqual(next(i for i,s in enumerate(p) if s[2]>0),3)

    def test_psi_product_zero_during_first_two_lags(self):
        p=direct_history(1,F(1,4),F(1,4),F(1,4),0)
        self.assertEqual([scoring(x)[0] for x in p[:3]],[0,0,0])

    def test_psi_positive_after_first_three_component_onsets(self):
        p=direct_history(1,F(1,4),F(1,4),F(1,4),0)
        self.assertGreater(scoring(p[3])[0],0)

    def test_all_adjustments_one_step_pipeline(self):
        p=direct_history(1,1,1,1,0)
        self.assertEqual(p[:4],(ZERO,(F(1),F(0),F(0)),
                                (F(1),F(1),F(0)),(F(1),F(1),F(1))))

    def test_perfect_buffer_forces_fiscal_and_psi_zero(self):
        p=direct_history(1,F(1,2),F(1,2),F(1,2),1)
        self.assertTrue(all(x[2]==0 and scoring(x)[0]==0 for x in p))
        self.assertGreater(p[-1][0],0)
        self.assertGreater(p[-1][1],0)

    def test_buffer_leaves_mass_and_elite_invariant(self):
        paths=[direct_history(1,F(1,4),F(1,2),F(1,4),r) for r in RELIEFS]
        for t in range(13):
            self.assertEqual(paths[0][t][:2],paths[1][t][:2])
            self.assertEqual(paths[1][t][:2],paths[2][t][:2])

    def test_buffer_monotone_reduces_fiscal_and_index(self):
        for h in TARGETS:
            paths=[direct_history(h,F(1,4),F(1,2),F(1,4),r) for r in RELIEFS]
            for t in range(13):
                self.assertGreaterEqual(paths[0][t][2],paths[1][t][2])
                self.assertGreaterEqual(paths[1][t][2],paths[2][t][2])
                self.assertGreaterEqual(scoring(paths[0][t])[0],scoring(paths[1][t])[0])
                self.assertGreaterEqual(scoring(paths[1][t])[0],scoring(paths[2][t])[0])

    def test_steady_limit_asymptotic(self):
        h,a,b,c,r=F(1,2),F(1,2),F(1,2),F(1,2),F(1,2)
        path=direct_history(h,a,b,c,r,100)
        target=(h,h,(1-r)*h)
        self.assertTrue(all(abs(x-y)<F(1,10**15) for x,y in zip(path[-1],target)))

    def test_no_external_mass_target_stays_zero(self):
        self.assertTrue(all(x==ZERO for x in direct_history(0,F(1,2),F(1,4),F(1,2),0)))

    def test_zero_mass_adjustment_stays_zero(self):
        self.assertTrue(all(x==ZERO for x in direct_history(1,0,F(1,4),F(1,2),0)))

    def test_zero_elite_lag_prevents_elite_fiscal(self):
        p=direct_history(1,F(1,4),0,F(1,2),0)
        self.assertGreater(p[-1][0],0)
        self.assertTrue(all(x[1]==0 and x[2]==0 for x in p))

    def test_zero_fiscal_lag_prevents_fiscal(self):
        p=direct_history(1,F(1,4),F(1,2),0,0)
        self.assertGreater(p[-1][1],0)
        self.assertTrue(all(x[2]==0 for x in p))

    def test_scoring_turchin_multiplicative_schematic(self):
        self.assertEqual(scoring((F(1,2),F(1,4),F(1,2)))[0],F(1,16))

    def test_mean_is_diagnostic_and_separate(self):
        self.assertEqual(scoring((1,1,0)),(F(0),F(2,3)))
        self.assertEqual(scoring((F(1,2),)*3),(F(1,8),F(1,2)))

    def test_mean_and_product_reverse_aggregation_ranks(self):
        a=scoring((1,1,0))
        b=scoring((F(1,2),)*3)
        self.assertGreater(a[1],b[1])
        self.assertLess(a[0],b[0])

    def test_equal_initial_state_but_different_next_step(self):
        a=direct_history(1,F(1,4),F(1,4),F(1,4),0)
        b=direct_history(F(1,2),F(1,2),F(1,4),F(1,4),0)
        self.assertEqual(a[1],b[1])
        self.assertEqual(a[2][0],F(7,16))
        self.assertEqual(b[2][0],F(3,8))
        self.assertNotEqual(a[2],b[2])

    def test_zero_psi_not_zero_component_stress(self):
        self.assertEqual(scoring((1,1,0))[0],0)
        self.assertGreater(scoring((1,1,0))[1],0)

    def test_invalid_pressure_value_bounds(self):
        for x in (-1,F(101,100),2):
            with self.assertRaises(ValueError): unit(x,"artificial")
            with self.assertRaises(ValueError): direct_history(x,F(1,2),F(1,2),F(1,2),0)

    def test_invalid_unit_types_rejected(self):
        for x in (False,0.5,"1/2",None):
            with self.assertRaises(ValueError): unit(x,"bad")

    def test_invalid_state_dimension_rejected(self):
        for x in ((1,1),(1,1,1,1),()):
            with self.assertRaises(ValueError): scoring(x)
            with self.assertRaises(ValueError): step(x,1,F(1,2),F(1,2),F(1,2),0)

    def test_invalid_horizon_rejected(self):
        for t in (-1,2.5,False,"12"):
            with self.assertRaises(ValueError): direct_history(1,F(1,2),F(1,2),F(1,2),0,t)
            with self.assertRaises(ValueError): matrix_history(1,F(1,2),F(1,2),F(1,2),0,t)

    def test_direct_matrix_short_horizons(self):
        for n in (0,1,2,3,7):
            self.assertEqual(direct_history(F(1,2),F(1,4),F(1,2),F(1,2),F(1,2),n),
                             matrix_history(F(1,2),F(1,4),F(1,2),F(1,2),F(1,2),n))

    def test_alternative_pressure_mean_is_not_causal_event_probability(self):
        doc=record()
        self.assertFalse(doc["real_event_probabilities_estimated"])
        self.assertFalse(doc["historical_instability_outcomes_used"])
        self.assertFalse(doc["author_original_dynamics_recreated"])

    def test_complete_world_ledger_identity(self):
        doc=record()
        self.assertEqual(doc["scenario_count"],72)
        self.assertEqual(len(doc["worlds"]),72)
        self.assertEqual(len({w["id"] for w in doc["worlds"]}),72)
        self.assertTrue(all(len(w["points"])==13 for w in doc["worlds"]))
        self.assertTrue(all(w["direct_equals_independent_affine"] for w in doc["worlds"]))
        self.assertEqual(doc["predeclared_counterexamples"]["first_nonzero_fiscal_t"],3)

    def test_full_json_replay_bytes_if_present(self):
        p=Path(__file__).with_name("R157_EXACT_RESULTS.json")
        if not p.exists(): self.skipTest("canonical archive generated by CI before tests")
        exact=(json.dumps(record(),indent=2,sort_keys=True,ensure_ascii=False)+"\n").encode()
        self.assertEqual(p.read_bytes(),exact)


for hi in range(len(TARGETS)):
    for ai in range(len(LAGS)):
        for bi in range(len(LAGS)):
            for ci in range(len(LAGS)):
                for ri in range(len(RELIEFS)):
                    def produce(hi=hi,ai=ai,bi=bi,ci=ci,ri=ri):
                        def case(self): self.check_world(hi,ai,bi,ci,ri)
                        return case
                    setattr(TestPressure,f"test_frozen_h{hi}_a{ai}_b{bi}_c{ci}_r{ri}",produce())


if __name__=="__main__":
    unittest.main()
