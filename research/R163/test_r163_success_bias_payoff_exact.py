"""R163 direct exact tests of synthetic success signals and payoff strategies."""
from __future__ import annotations

import json
import unittest
from fractions import Fraction as F
from pathlib import Path
from r163_success_bias_payoff_exact import (
    PROFILES, TRANSFORMS, STRATEGIES, CORRECT_TOKENS,
    valid_actions, valid_payoffs, valid_controls, transformed,
    direct_choice, enumerated_choice, direct_case, enumerated_case, document
)


class TestSuccessBias(unittest.TestCase):
    def check_world(self,pi,ti,si,ci):
        name,acts,pays=PROFILES[pi]
        tr=TRANSFORMS[ti];strategy=STRATEGIES[si];correct=CORRECT_TOKENS[ci]
        a=direct_case(acts,pays,tr,strategy,correct)
        b=enumerated_case(acts,pays,tr,strategy,correct)
        self.assertEqual(a,b)
        self.assertTrue(all(isinstance(v,F) for v in a))
        self.assertTrue(all(F(0)<=v<=F(1) for v in a[:4]))
        self.assertEqual(a[1],F(sum(acts),3))
        self.assertEqual(a[-1],a[2]-a[3])
        if correct==1:
            self.assertEqual(a[2],a[0])
        else:
            self.assertEqual(a[2],1-a[0])
        if tr=="raw":
            self.assertEqual(transformed(pays,tr),pays)
        if tr=="flat":
            self.assertEqual(transformed(pays,tr),(6,6,6))
        self.assertEqual(a[0],direct_choice(acts,transformed(pays,tr),strategy))

    def test_72_world_count(self):
        self.assertEqual(len(PROFILES)*len(TRANSFORMS)*len(STRATEGIES)*len(CORRECT_TOKENS),72)

    def test_original_A_outlier_best(self):
        self.assertEqual(direct_choice((1,1,0),(12,0,8),"best"),1)

    def test_original_A_outlier_means(self):
        self.assertEqual(direct_choice((1,1,0),(12,0,8),"means"),0)

    def test_original_B_outlier_best(self):
        self.assertEqual(direct_choice((1,0,0),(8,12,0),"best"),0)

    def test_original_B_outlier_means(self):
        self.assertEqual(direct_choice((1,0,0),(8,12,0),"means"),1)

    def test_agreement_A_both_strategies(self):
        for strat in STRATEGIES:
            self.assertEqual(direct_choice((1,1,0),(10,9,2),strat),1)

    def test_agreement_B_both_strategies(self):
        for strat in STRATEGIES:
            self.assertEqual(direct_choice((1,0,0),(2,10,9),strat),0)

    def test_best_person_tie_is_uniform_over_people(self):
        self.assertEqual(direct_choice((1,0,0),(8,8,2),"best"),F(1,2))

    def test_best_tie_means_does_not_follow_person_tie(self):
        self.assertEqual(direct_choice((1,0,0),(8,8,2),"means"),1)

    def test_mean_variant_tie_is_uniform_over_action_types(self):
        self.assertEqual(direct_choice((1,1,0),(8,0,4),"means"),F(1,2))

    def test_mean_tie_best_chooses_unique_person(self):
        self.assertEqual(direct_choice((1,1,0),(8,0,4),"best"),1)

    def test_flat_imitate_best_reduces_to_person_baseline(self):
        for _,act,pay in PROFILES:
            self.assertEqual(direct_choice(act,transformed(pay,"flat"),"best"),
                             F(sum(act),3))

    def test_flat_compare_means_reduces_to_variant_tie(self):
        for _,act,pay in PROFILES:
            self.assertEqual(direct_choice(act,transformed(pay,"flat"),"means"),F(1,2))

    def test_flat_is_not_strategy_identity_with_unequal_action_counts(self):
        a=PROFILES[0]
        self.assertEqual(direct_case(a[1],a[2],"flat","best",1)[0],F(2,3))
        self.assertEqual(direct_case(a[1],a[2],"flat","means",1)[0],F(1,2))

    def test_success_bias_helps_when_selected_A_correct(self):
        a=PROFILES[0]
        self.assertEqual(direct_case(a[1],a[2],"raw","best",1)[-1],F(1,3))

    def test_success_bias_harms_when_selected_A_wrong(self):
        a=PROFILES[0]
        self.assertEqual(direct_case(a[1],a[2],"raw","best",0)[-1],F(-1,3))

    def test_true_correctness_complement_reverses_advantage(self):
        for _,actions,payoffs in PROFILES:
            for trans in TRANSFORMS:
                for strat in STRATEGIES:
                    a=direct_case(actions,payoffs,trans,strat,0)[-1]
                    b=direct_case(actions,payoffs,trans,strat,1)[-1]
                    self.assertEqual(a,-b)

    def test_reversing_signal_can_change_selection(self):
        a=PROFILES[2]
        self.assertNotEqual(direct_case(a[1],a[2],"raw","best",1)[0],
                            direct_case(a[1],a[2],"reverse","best",1)[0])

    def test_order_preserving_score_shift_does_not_change_rule(self):
        for _,acts,pays in PROFILES:
            for strat in STRATEGIES:
                # Adding a constant is ranking-preserving even when source values exceed grid.
                shifted=tuple(x+2 for x in pays)
                # Test using pure local rank arithmetic without input-range enforcement.
                if strat=="best":
                    first=max(pays);second=max(shifted)
                    A=[acts[i] for i,p in enumerate(pays) if p==first]
                    B=[acts[i] for i,p in enumerate(shifted) if p==second]
                    self.assertEqual(F(sum(A),len(A)),F(sum(B),len(B)))
                else:
                    for act in (0,1):
                        old=F(sum(pays[i] for i in range(3) if acts[i]==act),
                              sum(acts[i]==act for i in range(3)))
                        new=F(sum(shifted[i] for i in range(3) if acts[i]==act),
                              sum(acts[i]==act for i in range(3)))
                        self.assertEqual(new-old,2)

    def test_reverse_signal_is_exact_integer_map(self):
        for _,_,pays in PROFILES:
            self.assertEqual(transformed(transformed(pays,"reverse"),"reverse"),pays)

    def test_direct_and_cross_product_mean_oracles_agree(self):
        for _,acts,pays in PROFILES:
            for transform in TRANSFORMS:
                v=transformed(pays,transform)
                self.assertEqual(direct_choice(acts,v,"means"),
                                 enumerated_choice(acts,v,"means"))

    def test_direct_and_independently_enumerated_best_agree(self):
        for _,acts,pays in PROFILES:
            for transform in TRANSFORMS:
                v=transformed(pays,transform)
                self.assertEqual(direct_choice(acts,v,"best"),
                                 enumerated_choice(acts,v,"best"))

    def test_reject_invalid_action_profiles(self):
        for actions in ((),(0,1),(1,1,1),(0,0,0),(True,0,1),(2,0,1),("1",0,1),None):
            with self.assertRaises(ValueError): valid_actions(actions)

    def test_reject_invalid_payoff_profiles(self):
        for values in ((),(1,2),(-1,2,3),(13,2,3),(True,2,3),(0.5,2,3),("5",2,3),None):
            with self.assertRaises(ValueError): valid_payoffs(values)

    def test_reject_invalid_payoff_transform(self):
        for tr in (None,False,"reverse-unknown",0):
            with self.assertRaises(ValueError): transformed((1,2,3),tr)

    def test_reject_unknown_strategy(self):
        for strat in (None,False,"imitate-best",2):
            with self.assertRaises(ValueError): direct_choice((1,0,0),(3,2,1),strat)
            with self.assertRaises(ValueError): enumerated_choice((1,0,0),(3,2,1),strat)

    def test_reject_invalid_objective_correctness(self):
        for c in (False,True,-1,2,"1",F(1,2),0.5):
            with self.assertRaises(ValueError): valid_controls("raw","best",c)

    def test_no_original_empirical_evidence_claimed(self):
        d=document()
        self.assertFalse(d["original_Baldini_dynamics_recreated"])
        self.assertFalse(d["Mesoudi_human_behavior_data_reused"])
        self.assertFalse(d["real_success_signal_reliability_estimated"])

    def test_ledger_unique_72_ids_and_strict_fraction(self):
        d=document()
        self.assertEqual(d["world_count"],72)
        self.assertEqual(len(d["worlds"]),72)
        self.assertEqual(len({w["id"] for w in d["worlds"]}),72)
        self.assertTrue(all(w["independent_exact_oracles_equal"] for w in d["worlds"]))
        self.assertEqual(d["prespecified_counterexamples"]["A_outlier_raw_imitate_best_A"],"1")
        self.assertEqual(d["prespecified_counterexamples"]["A_outlier_raw_compare_means_A"],"0")

    def test_saved_JSON_byte_identity(self):
        path=Path(__file__).with_name("R163_EXACT_RESULTS.json")
        if not path.exists():
            self.skipTest("CI regenerates result JSON before testing")
        expect=(json.dumps(document(),sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode()
        self.assertEqual(path.read_bytes(),expect)


for pi in range(len(PROFILES)):
    for ti in range(len(TRANSFORMS)):
        for si in range(len(STRATEGIES)):
            for ci in range(len(CORRECT_TOKENS)):
                def build(pi=pi,ti=ti,si=si,ci=ci):
                    def test(self):
                        self.check_world(pi,ti,si,ci)
                    return test
                setattr(TestSuccessBias,f"test_frozen_p{pi}_t{ti}_s{si}_c{ci}",build())


if __name__=="__main__":
    unittest.main()
