"""R159 genuine controlled tests for 48 cultural imitation worlds."""
import json
import unittest
from fractions import Fraction as F
from pathlib import Path
from r159_cultural_transmission_exact import (
    INITIAL_FREQUENCIES,CONFORMISM,RESET,HORIZON,unit,majority_polynomial,
    majority_enumerated,direct_history,independent_history,result_document
)


class TestR159(unittest.TestCase):
    def check_world(self,pi,hi,ui):
        p0,h,u=INITIAL_FREQUENCIES[pi],CONFORMISM[hi],RESET[ui]
        a=direct_history(p0,h,u)
        b=independent_history(p0,h,u)
        self.assertEqual(a,b)
        self.assertEqual(len(a),7)
        self.assertEqual(a[0],p0)
        for t,p in enumerate(a):
            self.assertIsInstance(p,F)
            self.assertTrue(F(0)<=p<=F(1))
            c=majority_polynomial(p)
            self.assertEqual(c,majority_enumerated(p))
            if t<6:
                self.assertEqual(a[t+1],(1-u)*((1-h)*p+h*c)+u/2)
        if u==0 and h>0:
            if p0<F(1,2):
                self.assertTrue(all(x>y for x,y in zip(a,a[1:])))
            elif p0>F(1,2):
                self.assertTrue(all(x<y for x,y in zip(a,a[1:])))

    def test_exact_factorial_count(self):
        self.assertEqual(len(INITIAL_FREQUENCIES)*len(CONFORMISM)*len(RESET),48)

    def test_majority_at_zero_one_and_half(self):
        self.assertEqual(majority_polynomial(0),0)
        self.assertEqual(majority_polynomial(1),1)
        self.assertEqual(majority_polynomial(F(1,2)),F(1,2))

    def test_majority_at_one_quarter(self):
        self.assertEqual(majority_polynomial(F(1,4)),F(5,32))
        self.assertEqual(majority_enumerated(F(1,4)),F(5,32))

    def test_majority_at_three_quarters(self):
        self.assertEqual(majority_polynomial(F(3,4)),F(27,32))
        self.assertEqual(majority_enumerated(F(3,4)),F(27,32))

    def test_polynomial_equals_exhaustive_enumeration(self):
        for denominator in (2,3,4,5,7,13):
            for numerator in range(denominator+1):
                p=F(numerator,denominator)
                self.assertEqual(majority_polynomial(p),majority_enumerated(p))

    def test_majority_symmetry(self):
        for p in (F(1,7),F(2,5),F(3,4),F(1,2)):
            self.assertEqual(majority_polynomial(1-p),1-majority_polynomial(p))

    def test_majority_protects_probability_bounds(self):
        for i in range(101):
            p=F(i,100)
            self.assertTrue(0<=majority_polynomial(p)<=1)

    def test_majority_below_half_lowers_frequency(self):
        for p in (F(1,4),F(2,5)):
            self.assertLess(majority_polynomial(p),p)

    def test_majority_above_half_raises_frequency(self):
        for p in (F(3,5),F(3,4)):
            self.assertGreater(majority_polynomial(p),p)

    def test_unbiased_copying_without_reset_constant(self):
        for p in INITIAL_FREQUENCIES:
            self.assertEqual(direct_history(p,0,0),(p,)*7)

    def test_unbiased_copying_with_reset_exact_exponential(self):
        for p0 in INITIAL_FREQUENCIES:
            for u in RESET[1:]:
                actual=direct_history(p0,0,u)
                expected=tuple(F(1,2)+(1-u)**t*(p0-F(1,2)) for t in range(7))
                self.assertEqual(actual,expected)

    def test_half_frequency_invariant_under_all_parameters(self):
        for h in CONFORMISM:
            for u in RESET:
                self.assertEqual(direct_history(F(1,2),h,u),(F(1,2),)*7)

    def test_half_frequency_parameters_not_identified(self):
        self.assertEqual(direct_history(F(1,2),0,0),
                         direct_history(F(1,2),1,F(1,4)))

    def test_strict_conformist_dynamics_when_reset_zero(self):
        for p in INITIAL_FREQUENCIES:
            for h in CONFORMISM[1:]:
                x=direct_history(p,h,0)
                if p<F(1,2):
                    self.assertTrue(all(a>b for a,b in zip(x,x[1:])))
                else:
                    self.assertTrue(all(a<b for a,b in zip(x,x[1:])))

    def test_reset_breaks_absorption_at_zero_and_one(self):
        self.assertEqual(direct_history(0,1,0),(F(0),)*7)
        self.assertEqual(direct_history(1,1,0),(F(1),)*7)
        self.assertGreater(direct_history(0,1,F(1,10))[1],0)
        self.assertLess(direct_history(1,1,F(1,10))[1],1)

    def test_reset_changes_first_step_toward_half(self):
        for p0 in INITIAL_FREQUENCIES:
            for h in CONFORMISM:
                without=direct_history(p0,h,0)[1]
                with_reset=direct_history(p0,h,F(1,10))[1]
                self.assertLess(abs(with_reset-F(1,2)),abs(without-F(1,2)))

    def test_full_transmission_mirror_symmetry(self):
        for h in CONFORMISM:
            for u in RESET:
                a=direct_history(F(2,5),h,u)
                b=direct_history(F(3,5),h,u)
                self.assertEqual(tuple(1-x for x in a),b)

    def test_independent_method_no_float(self):
        for p0 in INITIAL_FREQUENCIES:
            for h in CONFORMISM:
                for u in RESET:
                    self.assertTrue(all(isinstance(x,F) for x in independent_history(p0,h,u)))

    def test_invalid_cultural_parameter_bounds(self):
        for bad in (-1,F(101,100),3):
            with self.assertRaises(ValueError): unit(bad,"bad")
            with self.assertRaises(ValueError): direct_history(bad,F(1,2),F(1,10))

    def test_invalid_parameter_types(self):
        for bad in (True,False,0.25,"1/4",None):
            with self.assertRaises(ValueError): unit(bad,"bad")
            with self.assertRaises(ValueError): independent_history(F(1,4),bad,F(1,10))

    def test_invalid_horizons(self):
        for value in (-1,False,1.2,"5"):
            with self.assertRaises(ValueError): direct_history(F(1,4),1,0,value)
            with self.assertRaises(ValueError): independent_history(F(1,4),1,0,value)

    def test_no_empirical_or_genetic_source_claim(self):
        d=result_document()
        self.assertTrue(d["not_a_gene_culture_coevolution_model"])
        self.assertFalse(d["historical_cultural_data_used"])
        self.assertFalse(d["author_original_equations_reproduced"])

    def test_exact_majority_advantage_factorization(self):
        for denominator in (2,3,4,5,7,11):
            for numerator in range(denominator+1):
                p=F(numerator,denominator)
                self.assertEqual(majority_polynomial(p)-p,p*(1-p)*(2*p-1))

    def test_full_world_ledger(self):
        d=result_document()
        self.assertEqual(d['scenario_count'],48)
        self.assertEqual(len(d['worlds']),48)
        self.assertEqual(len({w["case_id"] for w in d["worlds"]}),48)
        self.assertTrue(all(len(w["points"])==7 for w in d["worlds"]))
        self.assertTrue(all(w["two_independent_Fraction_routes_identical"] for w in d["worlds"]))

    def test_complete_json_replay(self):
        p=Path(__file__).with_name("R159_EXACT_RESULTS.json")
        if not p.exists(): self.skipTest("CI generates canonical archive JSON first")
        expected=(json.dumps(result_document(),sort_keys=True,indent=2,ensure_ascii=False)+"\n").encode()
        self.assertEqual(p.read_bytes(),expected)


for pi in range(len(INITIAL_FREQUENCIES)):
    for hi in range(len(CONFORMISM)):
        for ui in range(len(RESET)):
            def make(pi=pi,hi=hi,ui=ui):
                def case(self): self.check_world(pi,hi,ui)
                return case
            setattr(TestR159,f'test_frozen_p{pi}_h{hi}_u{ui}',make())


if __name__=='__main__':
    unittest.main()
