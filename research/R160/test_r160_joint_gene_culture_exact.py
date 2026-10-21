"""R160 strict tests of 60 artificial G/C frequency joint distributions.

The worlds contain no actual inherited human trait, no datasets and no
empirical fit. Fraction exact arithmetic is validated against enumerated flow.
"""
from __future__ import annotations

import json
import unittest
from fractions import Fraction as F
from pathlib import Path
from r160_joint_gene_culture_exact import (
    INITIAL_TABLES,SELECTION,IMITATION,HORIZONTAL,HORIZON,
    unit,checked_table,checked_params,marginals,majority_polynomial,
    step_direct,step_enumerated,direct_history,independent_history,
    result_document
)


class TestR160(unittest.TestCase):
    def check_world(self,ii,si,hi,ui):
        p,s,h,u=INITIAL_TABLES[ii],SELECTION[si],IMITATION[hi],HORIZONTAL[ui]
        a=direct_history(p,s,h,u)
        b=independent_history(p,s,h,u)
        self.assertEqual(a,b)
        self.assertEqual(len(a),HORIZON+1)
        for t,tab in enumerate(a):
            self.assertEqual(sum(tab,F(0)),F(1))
            self.assertTrue(all(isinstance(x,F) and 0<=x<=1 for x in tab))
            g,c,d=marginals(tab)
            self.assertEqual(d,tab[3]-g*c)
            self.assertTrue(0<=g<=1 and 0<=c<=1)
            if t<HORIZON:
                self.assertEqual(a[t+1],step_direct(tab,s,h,u))
                self.assertEqual(a[t+1],step_enumerated(tab,s,h,u))
        if s==0:
            self.assertTrue(all(marginals(tab)[0]==marginals(p)[0] for tab in a))
        if u==0 and s==0:
            self.assertEqual(a,(p,)*(HORIZON+1))
        if ii==3:
            self.assertTrue(all(marginals(tab)[1]==0 for tab in a))
        if ii==4:
            self.assertTrue(all(marginals(tab)[1]==1 for tab in a))

    def test_frozen_scenario_count(self):
        self.assertEqual(len(INITIAL_TABLES)*len(SELECTION)*len(IMITATION)*len(HORIZONTAL),60)

    def test_all_initial_tables_normalized(self):
        for table in INITIAL_TABLES:
            self.assertEqual(sum(checked_table(table),F(0)),1)

    def test_initial_two_marginals_match_for_opposite_association(self):
        pos=marginals(INITIAL_TABLES[1])
        neg=marginals(INITIAL_TABLES[2])
        self.assertEqual(pos[:2],(F(1,2),F(1,2)))
        self.assertEqual(neg[:2],pos[:2])

    def test_initial_association_sign(self):
        self.assertEqual(marginals(INITIAL_TABLES[1])[2],F(1,8))
        self.assertEqual(marginals(INITIAL_TABLES[2])[2],F(-1,8))

    def test_same_marginals_distinct_selection_gene(self):
        a=step_direct(INITIAL_TABLES[1],F(1,2),0,0)
        b=step_direct(INITIAL_TABLES[2],F(1,2),0,0)
        self.assertEqual(marginals(a)[0],F(11,19))
        self.assertEqual(marginals(b)[0],F(9,17))
        self.assertNotEqual(marginals(a)[0],marginals(b)[0])

    def test_independent_enumerator_matches_one_step_selection(self):
        for p in INITIAL_TABLES:
            for s in SELECTION:
                for h in IMITATION:
                    for u in HORIZONTAL:
                        self.assertEqual(step_direct(p,s,h,u),step_enumerated(p,s,h,u))

    def test_zero_selection_keeps_gene_marginal(self):
        for p in INITIAL_TABLES:
            g0=marginals(p)[0]
            for h in IMITATION:
                for u in HORIZONTAL:
                    self.assertTrue(all(marginals(t)[0]==g0 for t in direct_history(p,0,h,u)))

    def test_zero_horizontal_learning_ignores_conformism(self):
        for p in INITIAL_TABLES:
            for s in SELECTION:
                reference=direct_history(p,s,0,0)
                for h in IMITATION:
                    self.assertEqual(reference,direct_history(p,s,h,0))

    def test_zero_selection_and_zero_learning_static_joint(self):
        for p in INITIAL_TABLES:
            for h in IMITATION:
                self.assertEqual(direct_history(p,0,h,0),(p,)*5)

    def test_positive_association_contracts_by_three_quarters(self):
        t=step_direct(INITIAL_TABLES[1],0,1,F(1,4))
        self.assertEqual(marginals(t)[:2],(F(1,2),F(1,2)))
        self.assertEqual(marginals(t)[2],F(3,32))

    def test_negative_association_contracts_by_three_quarters(self):
        t=step_direct(INITIAL_TABLES[2],0,1,F(1,4))
        self.assertEqual(marginals(t)[:2],(F(1,2),F(1,2)))
        self.assertEqual(marginals(t)[2],F(-3,32))

    def test_contraction_independent_of_h_when_culture_half(self):
        for h in IMITATION:
            self.assertEqual(marginals(step_direct(INITIAL_TABLES[1],0,h,F(1,4)))[2],F(3,32))
            self.assertEqual(marginals(step_direct(INITIAL_TABLES[2],0,h,F(1,4)))[2],F(-3,32))

    def test_no_C1_origin_always_no_C1(self):
        for s in SELECTION:
            for h in IMITATION:
                for u in HORIZONTAL:
                    self.assertTrue(all(marginals(t)[1]==0 for t in direct_history(INITIAL_TABLES[3],s,h,u)))

    def test_all_C1_origin_stays_all_C1(self):
        for s in SELECTION:
            for h in IMITATION:
                for u in HORIZONTAL:
                    self.assertTrue(all(marginals(t)[1]==1 for t in direct_history(INITIAL_TABLES[4],s,h,u)))

    def test_selection_can_change_gene_marginal(self):
        g_before=marginals(INITIAL_TABLES[0])[0]
        g_after=marginals(step_direct(INITIAL_TABLES[0],F(1,2),0,0))[0]
        self.assertGreater(g_after,g_before)

    def test_gene_response_independent_of_cultural_update_within_step(self):
        p=INITIAL_TABLES[1]
        g_after0=marginals(step_direct(p,F(1,2),0,0))[0]
        for h in IMITATION:
            for u in HORIZONTAL:
                self.assertEqual(g_after0,marginals(step_direct(p,F(1,2),h,u))[0])

    def test_selection_positive_non_decrease_for_all_frozen_worlds(self):
        for p in INITIAL_TABLES:
            for h in IMITATION:
                for u in HORIZONTAL:
                    history=direct_history(p,F(1,2),h,u)
                    self.assertTrue(all(marginals(b)[0]>=marginals(a)[0]
                                        for a,b in zip(history,history[1:])))

    def test_majority_half_fixed(self):
        self.assertEqual(majority_polynomial(F(1,2)),F(1,2))

    def test_majority_bounds_exact(self):
        for n in range(21):
            self.assertTrue(0<=majority_polynomial(F(n,20))<=1)

    def test_majority_mirror_symmetry(self):
        for n in range(11):
            p=F(n,10)
            self.assertEqual(majority_polynomial(1-p),1-majority_polynomial(p))

    def test_original_toy_cultural_connection_uses_postselection_fraction(self):
        p=INITIAL_TABLES[1]
        s=F(1,2);h=F(1);u=F(1,4)
        sel=step_direct(p,s,0,0)
        selected_c=marginals(sel)[1]
        predicted_c=(1-u)*selected_c+u*majority_polynomial(selected_c)
        self.assertEqual(marginals(step_direct(p,s,h,u))[1],predicted_c)

    def test_reject_bad_total_mass(self):
        with self.assertRaises(ValueError): checked_table((F(1,4),)*3+(F(1,8),))

    def test_reject_bad_table_dimension(self):
        for t in ((),(1,),[F(1,3)]*3,("1","0","0","0"),None):
            with self.assertRaises(ValueError): checked_table(t)

    def test_reject_bad_component_values(self):
        for bad in (F(-1,4),F(5,4),2,False,F(3,2),0.25):
            with self.assertRaises(ValueError): unit(bad,"component")

    def test_reject_bad_selection_and_copying_type(self):
        for bad in (True,-1,F(11,10),0.1,"1/4"):
            with self.assertRaises(ValueError): checked_params(bad,F(1,2),F(1,4))
            with self.assertRaises(ValueError): checked_params(F(1,2),bad,F(1,4))

    def test_reject_bad_horizon(self):
        for bad in (-1,False,1.2,"3"):
            with self.assertRaises(ValueError): direct_history(INITIAL_TABLES[0],0,0,0,bad)
            with self.assertRaises(ValueError): independent_history(INITIAL_TABLES[0],0,0,0,bad)

    def test_exact_score_uses_fraction_values(self):
        p=direct_history(INITIAL_TABLES[1],F(1,2),F(1),F(1,4))
        self.assertTrue(all(isinstance(z,F) for x in p for z in x))
        self.assertTrue(all(isinstance(z,F) for x in p for z in marginals(x)))

    def test_real_evidence_absent_in_result(self):
        d=result_document()
        self.assertFalse(d["real_genetic_or_cultural_data_used"])
        self.assertFalse(d["human_population_predictions"])
        self.assertFalse(d["original_gene_culture_equations_recreated"])

    def test_result_has_60_full_worlds(self):
        d=result_document()
        self.assertEqual(d["main_worlds"],60)
        self.assertEqual(len(d["worlds"]),60)
        self.assertEqual(len({v["id"] for v in d["worlds"]}),60)
        self.assertTrue(all(len(v["points"])==5 for v in d["worlds"]))
        self.assertEqual(d["frozen_controls"]["genetic_G1_after_selection_positive_association"],"11/19")
        self.assertEqual(d["frozen_controls"]["genetic_G1_after_selection_negative_association"],"9/17")

    def test_results_byte_replay(self):
        path=Path(__file__).with_name("R160_EXACT_RESULTS.json")
        if not path.exists():
            self.skipTest("canonical results generated before CI test execution")
        canonical=(json.dumps(result_document(),sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode()
        self.assertEqual(path.read_bytes(),canonical)


for ii in range(len(INITIAL_TABLES)):
    for si in range(len(SELECTION)):
        for hi in range(len(IMITATION)):
            for ui in range(len(HORIZONTAL)):
                def make(ii=ii,si=si,hi=hi,ui=ui):
                    def check(self): self.check_world(ii,si,hi,ui)
                    return check
                setattr(TestR160,f"test_frozen_i{ii}_s{si}_h{hi}_u{ui}",make())


if __name__ == "__main__":
    unittest.main()
