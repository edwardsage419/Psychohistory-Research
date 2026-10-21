"""R164 full-world exact content selection and measurement-boundary checks."""
from __future__ import annotations

import json
import unittest
from fractions import Fraction as F
from pathlib import Path
from r164_content_salience_exact import (
    STARTS,SALIENCE,CONTENT_COPY,RESET,HORIZON,
    unit,params,content_weight,direct_step,urn_step,direct_history,
    urn_history,analytic_full_copy_no_reset,analytic_only_reset,result_document
)


class TestR164(unittest.TestCase):
    def check_world(self,pi,ri,hi,ei):
        p0=STARTS[pi];r=SALIENCE[ri];h=CONTENT_COPY[hi];e=RESET[ei]
        direct=direct_history(p0,r,h,e)
        urn=urn_history(p0,r,h,e)
        self.assertEqual(direct,urn)
        self.assertEqual(len(direct),5)
        self.assertEqual(direct[0],p0)
        for t,p in enumerate(direct):
            self.assertIsInstance(p,F)
            self.assertTrue(0<=p<=1)
            self.assertEqual(content_weight(p,r),F(r)*p/(F(r)*p+1-p))
            if t<4:
                self.assertEqual(direct[t+1],direct_step(p,r,h,e))
                self.assertEqual(direct[t+1],urn_step(p,r,h,e))
        if r==1 and e==0:
            self.assertEqual(direct,(p0,)*5)
        if h==0 and e==0:
            self.assertEqual(direct,(p0,)*5)
        if h==0:
            self.assertEqual(direct,tuple(analytic_only_reset(p0,e,t) for t in range(5)))
        if h==1 and e==0:
            self.assertEqual(direct,tuple(analytic_full_copy_no_reset(p0,r,t) for t in range(5)))
        if r>1 and h>0 and e==0:
            self.assertTrue(all(a<b for a,b in zip(direct,direct[1:])))

    def test_frozen_72_world_count(self):
        self.assertEqual(len(STARTS)*len(SALIENCE)*len(CONTENT_COPY)*len(RESET),72)

    def test_r4_p_one_fifth_weight_is_half(self):
        self.assertEqual(content_weight(F(1,5),4),F(1,2))

    def test_r2_p_four_fifths_weight(self):
        self.assertEqual(content_weight(F(4,5),2),F(8,9))

    def test_r4_p_four_fifths_weight(self):
        self.assertEqual(content_weight(F(4,5),4),F(16,17))

    def test_salience_weight_one_is_random_copying(self):
        for n in range(1,10):
            self.assertEqual(content_weight(F(n,10),1),F(n,10))

    def test_zero_copy_weight_makes_salience_unidentifiable(self):
        for p in STARTS:
            for e in RESET:
                ref=direct_history(p,1,0,e)
                for r in SALIENCE:
                    self.assertEqual(ref,direct_history(p,r,0,e))

    def test_salience_one_makes_h_unidentifiable(self):
        for p in STARTS:
            for e in RESET:
                ref=direct_history(p,1,0,e)
                for h in CONTENT_COPY:
                    self.assertEqual(ref,direct_history(p,1,h,e))

    def test_no_content_copy_no_reset_keeps_frequency(self):
        for p in STARTS:
            for r in SALIENCE:
                self.assertEqual(direct_history(p,r,0,0),(p,)*5)

    def test_only_reset_closed_form_all_levels(self):
        for p in STARTS:
            for e in RESET:
                self.assertEqual(direct_history(p,4,0,e),
                    tuple(F(1,2)+(1-e)**t*(p-F(1,2)) for t in range(5)))

    def test_full_content_no_reset_odds_exact(self):
        for p in STARTS:
            for r in SALIENCE:
                a=direct_history(p,r,1,0)
                self.assertEqual(a,tuple(analytic_full_copy_no_reset(p,r,t) for t in range(5)))

    def test_odds_ratio_multiplied_by_r_each_generation(self):
        for p in STARTS:
            for r in SALIENCE:
                path=direct_history(p,r,1,0)
                for a,b in zip(path,path[1:]):
                    self.assertEqual(b/(1-b),r*a/(1-a))

    def test_unbiased_salience_exactly_stationary_if_no_reset(self):
        for p in STARTS:
            for h in CONTENT_COPY:
                self.assertEqual(direct_history(p,1,h,0),(p,)*5)

    def test_positive_salience_increases_sampling_probability(self):
        for p in STARTS:
            for r in SALIENCE[1:]:
                self.assertGreater(content_weight(p,r),p)

    def test_content_salience_ordering_monotone_in_r(self):
        for p in STARTS:
            self.assertLess(content_weight(p,1),content_weight(p,2))
            self.assertLess(content_weight(p,2),content_weight(p,4))

    def test_positive_content_copy_no_reset_increases_A(self):
        for p in STARTS:
            for r in SALIENCE[1:]:
                for h in CONTENT_COPY[1:]:
                    seq=direct_history(p,r,h,0)
                    self.assertTrue(all(a<b for a,b in zip(seq,seq[1:])))

    def test_positive_content_bias_does_not_force_growth_with_reset(self):
        p=F(4,5)
        self.assertEqual(direct_step(p,2,1,F(1,4)),F(19,24))
        self.assertLess(F(19,24),p)

    def test_symmetric_reset_pushes_toward_half_if_no_content_copy(self):
        for p in STARTS:
            q=direct_step(p,4,0,F(1,4))
            self.assertLess(abs(q-F(1,2)),abs(p-F(1,2)))

    def test_half_prevalence_is_not_fixed_when_content_bias_active(self):
        self.assertGreater(direct_step(F(1,2),2,1,0),F(1,2))
        self.assertEqual(direct_step(F(1,2),1,1,F(1,4)),F(1,2))

    def test_absorbing_boundaries_when_no_reset(self):
        for r in SALIENCE:
            for h in CONTENT_COPY:
                self.assertEqual(direct_history(0,r,h,0),(F(0),)*5)
                self.assertEqual(direct_history(1,r,h,0),(F(1),)*5)

    def test_reset_breaks_zero_and_one_absorption(self):
        for r in SALIENCE:
            self.assertGreater(direct_step(0,r,1,F(1,4)),0)
            self.assertLess(direct_step(1,r,1,F(1,4)),1)

    def test_independent_weighted_urn_full_fraction(self):
        for p in (F(1,7),F(4,9),F(9,10)):
            for r in SALIENCE:
                for h in CONTENT_COPY:
                    for e in RESET:
                        self.assertEqual(direct_step(p,r,h,e),urn_step(p,r,h,e))

    def test_unit_and_probabilities_remain_fraction(self):
        for p in STARTS:
            for r in SALIENCE:
                seq=direct_history(p,r,F(1,2),F(1,4))
                self.assertTrue(all(isinstance(x,F) for x in seq))
                self.assertTrue(all(0<=x<=1 for x in seq))

    def test_invalid_unit_range_and_types(self):
        for invalid in (False,True,-1,F(5,4),0.5,"1/2",None):
            with self.assertRaises(ValueError): unit(invalid,"bad")

    def test_invalid_salience_multiplier(self):
        for invalid in (0,-1,3,5,False,True,F(1),2.0,"2"):
            with self.assertRaises(ValueError): params(invalid,F(1,2),F(1,4))

    def test_invalid_copy_or_reset_parameter(self):
        for invalid in (-1,F(6,5),0.2,True,"1/4"):
            with self.assertRaises(ValueError): params(2,invalid,0)
            with self.assertRaises(ValueError): params(2,0,invalid)

    def test_invalid_horizon_type_and_sign(self):
        for horizon in (-1,True,False,F(1,2),2.0,"4"):
            with self.assertRaises(ValueError): direct_history(F(1,5),2,1,0,horizon)
            with self.assertRaises(ValueError): urn_history(F(1,5),2,1,0,horizon)

    def test_invalid_analytic_horizon(self):
        for horizon in (-1,True,F(1,2),3.0):
            with self.assertRaises(ValueError): analytic_full_copy_no_reset(F(1,5),4,horizon)
            with self.assertRaises(ValueError): analytic_only_reset(F(1,5),F(1,4),horizon)

    def test_real_source_data_not_claimed(self):
        d=result_document()
        self.assertFalse(d["original_author_recall_models_recreated"])
        self.assertFalse(d["human_recall_or_transmission_data_used"])
        self.assertFalse(d["salience_as_measured_validity_claimed"])

    def test_full_ledger_and_identification_controls(self):
        d=result_document()
        self.assertEqual(d['frozen_world_count'],72)
        self.assertEqual(len(d['worlds']),72)
        self.assertEqual(len({w['id'] for w in d['worlds']}),72)
        self.assertTrue(all(len(w['points'])==5 for w in d['worlds']))
        self.assertTrue(all(w['two_exact_independent_routes_equal'] for w in d['worlds']))
        self.assertTrue(d['controls']['all_r_equal_if_content_copy_is_zero'])
        self.assertTrue(d['controls']['r2_p_four_fifths_h1_reset_quarter_decreases_prevalence'])

    def test_canonical_full_JSON_byte_replay(self):
        path=Path(__file__).with_name("R164_EXACT_RESULTS.json")
        if not path.exists(): self.skipTest("CI must regenerate JSON first")
        canonical=(json.dumps(result_document(),indent=2,sort_keys=True,ensure_ascii=False)+"\n").encode()
        self.assertEqual(path.read_bytes(),canonical)


for pi in range(len(STARTS)):
    for ri in range(len(SALIENCE)):
        for hi in range(len(CONTENT_COPY)):
            for ei in range(len(RESET)):
                def build(pi=pi,ri=ri,hi=hi,ei=ei):
                    def test(self): self.check_world(pi,ri,hi,ei)
                    return test
                setattr(TestR164,f"test_frozen_p{pi}_r{ri}_h{hi}_e{ei}",build())


if __name__=="__main__":
    unittest.main()
