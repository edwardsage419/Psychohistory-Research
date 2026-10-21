"""R167 exact synthetic two-group covariance and aggregation reversal tests."""
import json
import unittest
from fractions import Fraction as F
from pathlib import Path

from r167_cultural_group_covariance_exact import (
    START_PAIRS,HIGH_WEIGHTS,WITHIN_DELTAS,BETWEEN_KAPPAS,HORIZON,
    unit,checked_state,params,population_mean,direct_step,
    covariance_oracle,trajectory,oracle_trajectory,main_results
)

class TestR167(unittest.TestCase):
    def check_world(self,pi,wi,di,ki):
        p=START_PAIRS[pi];high=HIGH_WEIGHTS[wi]
        d=WITHIN_DELTAS[di];k=BETWEEN_KAPPAS[ki]
        initial=p+(1-high,high)
        a=trajectory(initial,d,k)
        b=oracle_trajectory(initial,d,k)
        self.assertEqual(a,b)
        self.assertEqual(len(a),4)
        self.assertEqual(a[0]['state'],initial)
        for t,record in enumerate(a):
            p0,p1,w0,w1=record["state"]
            self.assertTrue(all(isinstance(x,F) for x in record["state"]))
            self.assertTrue(0<=p0<=p1<=1)
            self.assertEqual(w0+w1,1)
            self.assertTrue(0<w0<=1 and 0<w1<=1)
            self.assertEqual(record["mean"],w0*p0+w1*p1)
            if t:
                within,between,total=record["change"]
                self.assertEqual(within+between,total)
                self.assertEqual(a[t]['mean']-a[t-1]['mean'],total)
                self.assertEqual(a[t]['state'],direct_step(a[t-1]['state'],d,k)[0])
                self.assertEqual(a[t]['state'],covariance_oracle(a[t-1]['state'],d,k)[0])
                if k==0:
                    self.assertEqual(between,0)
                    self.assertEqual((w0,w1),initial[2:])
                if p[0]==p[1]:
                    self.assertEqual(between,0)
        if d==0:
            self.assertTrue(all(x["state"][:2]==p for x in a))
        if d>0:
            self.assertTrue(all(x["state"][0]<=p[0] and x["state"][1]<=p[1] for x in a))
        if d<0:
            self.assertTrue(all(x["state"][0]>=p[0] and x["state"][1]>=p[1] for x in a))

    def test_frozen_72_factorial(self):
        self.assertEqual(len(START_PAIRS)*len(HIGH_WEIGHTS)*len(WITHIN_DELTAS)*len(BETWEEN_KAPPAS),72)

    def test_exact_reversal_local_frequencies(self):
        state=(F(1,4),F(3,4),F(1,2),F(1,2))
        result=direct_step(state,F(1,4),2)
        self.assertEqual(result[0][:2],(F(13,64),F(45,64)))

    def test_exact_reversal_within_loss(self):
        state=(F(1,4),F(3,4),F(1,2),F(1,2))
        self.assertEqual(direct_step(state,F(1,4),2)[1],F(-3,64))

    def test_exact_reversal_between_gain(self):
        state=(F(1,4),F(3,4),F(1,2),F(1,2))
        self.assertEqual(direct_step(state,F(1,4),2)[2],F(1,16))

    def test_exact_reversal_total_gain(self):
        state=(F(1,4),F(3,4),F(1,2),F(1,2))
        self.assertEqual(direct_step(state,F(1,4),2)[3],F(1,64))

    def test_exact_reversal_next_total(self):
        state=(F(1,4),F(3,4),F(1,2),F(1,2))
        self.assertEqual(population_mean(direct_step(state,F(1,4),2)[0]),F(33,64))

    def test_both_local_groups_decrease_but_aggregate_increases(self):
        state=(F(1,4),F(3,4),F(1,2),F(1,2))
        after,within,between,total=direct_step(state,F(1,4),2)
        self.assertLess(after[0],state[0])
        self.assertLess(after[1],state[1])
        self.assertLess(within,0)
        self.assertGreater(between,0)
        self.assertGreater(total,0)

    def test_covariance_identity_always_equal_direct(self):
        for p in START_PAIRS:
            for high in HIGH_WEIGHTS:
                for delta in WITHIN_DELTAS:
                    for kappa in BETWEEN_KAPPAS:
                        state=p+(1-high,high)
                        self.assertEqual(direct_step(state,delta,kappa),
                                         covariance_oracle(state,delta,kappa))

    def test_kappa_zero_between_component_zero(self):
        for p in START_PAIRS:
            for high in HIGH_WEIGHTS:
                for delta in WITHIN_DELTAS:
                    state=p+(1-high,high)
                    self.assertEqual(direct_step(state,delta,0)[2],0)

    def test_kappa_zero_group_weights_constant(self):
        for p in START_PAIRS:
            for high in HIGH_WEIGHTS:
                s=p+(1-high,high)
                a=trajectory(s,F(1,4),0)
                self.assertTrue(all(x["state"][2:]==s[2:] for x in a))

    def test_delta_zero_local_frequencies_constant(self):
        for p in START_PAIRS:
            for high in HIGH_WEIGHTS:
                for k in BETWEEN_KAPPAS:
                    s=p+(1-high,high)
                    a=trajectory(s,0,k)
                    self.assertTrue(all(x["state"][:2]==p for x in a))

    def test_equal_fractions_disable_between_group_component(self):
        for high in HIGH_WEIGHTS:
            for d in WITHIN_DELTAS:
                for k in BETWEEN_KAPPAS:
                    a=trajectory((F(1,2),F(1,2),1-high,high),d,k)
                    self.assertTrue(all(t["change"][1]==0 for t in a[1:]))

    def test_equal_fractions_group_weights_unchanged(self):
        for high in HIGH_WEIGHTS:
            for d in WITHIN_DELTAS:
                for k in BETWEEN_KAPPAS:
                    a=trajectory((F(1,2),F(1,2),1-high,high),d,k)
                    self.assertTrue(all(t["state"][2:]==(1-high,high) for t in a))

    def test_positive_kappa_higher_A_group_gains_weight(self):
        for p in START_PAIRS[:3]:
            for high in HIGH_WEIGHTS:
                for k in BETWEEN_KAPPAS[1:]:
                    after=direct_step(p+(1-high,high),0,k)[0]
                    self.assertGreater(after[3],high)

    def test_positive_kappa_between_component_nonnegative(self):
        for p in START_PAIRS:
            for high in HIGH_WEIGHTS:
                for d in WITHIN_DELTAS:
                    for k in BETWEEN_KAPPAS:
                        result=direct_step(p+(1-high,high),d,k)
                        self.assertGreaterEqual(result[2],0)

    def test_negative_within_delta_favors_A(self):
        for p in START_PAIRS[:3]:
            state=p+(F(1,2),F(1,2))
            after=direct_step(state,F(-1,4),0)[0]
            self.assertGreater(after[0],p[0])
            self.assertGreater(after[1],p[1])

    def test_positive_within_delta_suppresses_A(self):
        for p in START_PAIRS[:3]:
            state=p+(F(1,2),F(1,2))
            after=direct_step(state,F(1,4),0)[0]
            self.assertLess(after[0],p[0])
            self.assertLess(after[1],p[1])

    def test_delta_zero_group_selection_can_change_aggregate(self):
        start=(F(1,4),F(3,4),F(1,2),F(1,2))
        after,within,between,total=direct_step(start,0,2)
        self.assertEqual(within,0)
        self.assertGreater(between,0)
        self.assertGreater(total,0)

    def test_within_only_can_change_aggregate(self):
        start=(F(1,4),F(3,4),F(1,2),F(1,2))
        _,within,between,total=direct_step(start,F(1,4),0)
        self.assertLess(within,0)
        self.assertEqual(between,0)
        self.assertEqual(within,total)

    def test_multi_generation_group_weights_sum_one(self):
        for p in START_PAIRS:
            s=p+(F(1,4),F(3,4))
            for row in trajectory(s,F(1,4),2):
                self.assertEqual(sum(row['state'][2:]),1)

    def test_multi_generation_within_between_identity(self):
        s=(F(1,5),F(4,5),F(1,4),F(3,4))
        t=trajectory(s,F(1,4),2)
        for i in range(1,len(t)):
            w,b,tot=t[i]['change']
            self.assertEqual(w+b,tot)
            self.assertEqual(t[i]['mean']-t[i-1]['mean'],tot)

    def test_total_relative_to_group_decomposition(self):
        s=(F(1,3),F(2,3),F(1,2),F(1,2))
        a=direct_step(s,F(-1,4),2)
        b=covariance_oracle(s,F(-1,4),2)
        self.assertEqual(a,b)
        self.assertEqual(a[3],population_mean(a[0])-population_mean(s))

    def test_group_labels_have_no_empirical_measurement(self):
        d=main_results()
        self.assertFalse(d["real_group_data_used"])
        self.assertFalse(d["original_structured_imitation_paper_reproduced"])
        self.assertFalse(d["original_Price_formula_full_general_derivation_reproduced"])

    def test_reject_unit_invalid_types(self):
        for bad in (True,False,0.5,"1/4",None):
            with self.assertRaises(ValueError): unit(bad,"bad")

    def test_reject_unit_out_of_interval(self):
        for bad in (F(-1,4),F(5,4),2):
            with self.assertRaises(ValueError): unit(bad,"bad")

    def test_reject_bad_group_state(self):
        for state in ((),(F(1,4),F(3,4)),(F(3,4),F(1,4),F(1,2),F(1,2)),
                      (F(1,4),F(3,4),F(1,4),F(1,4)),
                      (F(1,4),F(3,4),0.5,F(1,2)),None):
            with self.assertRaises(ValueError): checked_state(state)

    def test_reject_bad_delta_kappa(self):
        for d in (-1,F(1,8),0.25,True,"1/4"):
            with self.assertRaises(ValueError): params(d,1)
        for k in (-1,3,True,0.0,"1"):
            with self.assertRaises(ValueError): params(F(1,4),k)

    def test_reject_invalid_horizon(self):
        s=(F(1,4),F(3,4),F(1,2),F(1,2))
        for h in (-1,F(1,2),True,False,2.0,"3"):
            with self.assertRaises(ValueError): trajectory(s,0,0,h)
            with self.assertRaises(ValueError): oracle_trajectory(s,0,0,h)

    def test_full_72_worlds_and_exact_paths(self):
        d=main_results()
        self.assertEqual(d["world_count"],72)
        self.assertEqual(len(d["worlds"]),72)
        self.assertEqual(len({w["id"] for w in d["worlds"]}),72)
        self.assertTrue(all(w["independent_covariance_oracles_equal"] for w in d["worlds"]))
        self.assertTrue(all(len(w["points"])==4 for w in d["worlds"]))

    def test_frozen_reversal_certificate(self):
        r=main_results()["prespecified_reversal"]
        self.assertTrue(r["both_local_frequencies_decrease"])
        self.assertEqual(r["within_delta_component"],"-3/64")
        self.assertEqual(r["between_delta_component"],"1/16")
        self.assertEqual(r["total_delta"],"1/64")
        self.assertEqual(r["new_overall_A"],"33/64")

    def test_canonical_json_file_byte_replay(self):
        p=Path(__file__).with_name("R167_EXACT_RESULTS.json")
        if not p.exists(): self.skipTest("CI generates JSON before test")
        expected=(json.dumps(main_results(),sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode()
        self.assertEqual(p.read_bytes(),expected)


for pi in range(len(START_PAIRS)):
    for wi in range(len(HIGH_WEIGHTS)):
        for di in range(len(WITHIN_DELTAS)):
            for ki in range(len(BETWEEN_KAPPAS)):
                def make(pi=pi,wi=wi,di=di,ki=ki):
                    def test(self): self.check_world(pi,wi,di,ki)
                    return test
                setattr(TestR167,f"test_frozen_p{pi}_w{wi}_d{di}_k{ki}",make())


if __name__=="__main__":
    unittest.main()
