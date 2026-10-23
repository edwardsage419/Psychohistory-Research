#!/usr/bin/env python3
"""R318: exact finite CPT cumulative rank/sign weights, noncanonical toy weighting."""
from __future__ import annotations
import argparse
import csv
import json
import unittest
from fractions import Fraction
from itertools import combinations
from pathlib import Path
DIR=Path(__file__).resolve().parent
SOURCE=DIR/"R318_ALL_72_ORIGINAL_RANK_SIGN_OUTCOME_SOURCE_ATOMS.csv"
RESULT=DIR/"R318_EXACT_36_TWO_OUTCOME_CPT_VALUES.json"
OUTCOMES=(-2,-1,1,2)
PAIRS=tuple(combinations(OUTCOMES,2))
PROBS=(Fraction(1,4),Fraction(1,2),Fraction(3,4))
TRANSFORMS=("identity","quadratic_asymmetric_noncanonical")
FIELDS=("world","transform","x_low","x_high","p_low","outcome_index",
        "outcome","outcome_probability","domain","decision_weight",
        "reference_value","weighted_contribution","lottery_value")

def value(x):
    assert x in OUTCOMES
    return x if x>0 else 2*x

def weight(p,kind):
    assert Fraction(0)<=p<=Fraction(1)
    if kind=="identity":return p
    if kind=="quadratic_asymmetric_noncanonical":
        return p*p/(p*p+2*(1-p)*(1-p))
    raise ValueError(kind)

def decision_weights(low,high,p,kind):
    assert low<high and p in PROBS
    if low>0:return (1-weight(1-p,kind),weight(1-p,kind))
    if high<0:return (weight(p,kind),1-weight(p,kind))
    return (weight(p,kind),weight(1-p,kind))

def lottery(low,high,p,kind):
    a,b=decision_weights(low,high,p,kind)
    return a*value(low)+b*value(high)

def generate():
    atoms=[];outcomes=[];world=0
    for kind in TRANSFORMS:
        for low,high in PAIRS:
            for p in PROBS:
                wlow,whigh=decision_weights(low,high,p,kind)
                V=lottery(low,high,p,kind)
                domain="mixed" if low<0<high else ("gain" if low>0 else "loss")
                for i,(x,raw_prob,decision_weight) in enumerate(((low,p,wlow),(high,1-p,whigh))):
                    atoms.append(dict(zip(FIELDS,map(str,(
                        world,kind,low,high,p,i,x,raw_prob,domain,
                        decision_weight,value(x),decision_weight*value(x),V
                    )))))
                outcomes.append({
                    "world":world,"transform":kind,"x_low":low,"x_high":high,
                    "p_low":str(p),"domain":domain,
                    "low_weight":str(wlow),"high_weight":str(whigh),
                    "weight_sum":str(wlow+whigh),
                    "lottery_value":str(V),
                })
                world+=1
    return atoms,{
        "schema":"r318_cpt_finite_two_outcome_sign_rank_exact_e1_v1",
        "original_catalogue_id":"01-003",
        "weighting_noncanonical":True,
        "source_scope":"FINITE_SYNTHETIC_E1_ONLY",
        "source_atoms":len(atoms),
        "lotteries":len(outcomes),
        "outcomes":outcomes,
    }

def replay():
    with SOURCE.open(encoding="utf-8",newline="") as f:
        rows=list(csv.DictReader(f))
    s,o=generate()
    assert len(rows)==72 and rows==s
    assert json.loads(RESULT.read_text(encoding="utf-8"))==o
    assert len(o["outcomes"])==36

class CPTTests(unittest.TestCase):
    def test_outcome_count(self):self.assertEqual(len(OUTCOMES),4)
    def test_pair_count(self):self.assertEqual(len(PAIRS),6)
    def test_pair_unique(self):self.assertEqual(len(set(PAIRS)),6)
    def test_pair_ranked(self):self.assertTrue(all(a<b for a,b in PAIRS))
    def test_probability_count(self):self.assertEqual(len(PROBS),3)
    def test_probability_sum(self):
        for p in PROBS:self.assertEqual(p+(1-p),1)
    def test_value_gain(self):self.assertEqual(value(2),2)
    def test_value_loss(self):self.assertEqual(value(-2),-4)
    def test_identity_weight(self):
        for p in PROBS:self.assertEqual(weight(p,"identity"),p)
    def test_noncanonical_endpoints(self):
        self.assertEqual(weight(Fraction(0),"quadratic_asymmetric_noncanonical"),0)
        self.assertEqual(weight(Fraction(1),"quadratic_asymmetric_noncanonical"),1)
    def test_noncanonical_quarter(self):
        self.assertEqual(weight(Fraction(1,4),TRANSFORMS[1]),Fraction(1,19))
    def test_noncanonical_threequarter(self):
        self.assertEqual(weight(Fraction(3,4),TRANSFORMS[1]),Fraction(9,11))
    def test_nonlinear_half(self):self.assertEqual(weight(Fraction(1,2),TRANSFORMS[1]),Fraction(1,3))
    def test_weight_monotone(self):
        q=[weight(p,TRANSFORMS[1]) for p in PROBS]
        self.assertEqual(sorted(q),q)
    def test_gain_decision_sum(self):
        for k in TRANSFORMS:
            for p in PROBS:self.assertEqual(sum(decision_weights(1,2,p,k)),1)
    def test_loss_decision_sum(self):
        for k in TRANSFORMS:
            for p in PROBS:self.assertEqual(sum(decision_weights(-2,-1,p,k)),1)
    def test_mixed_noncanonical_nonadditive(self):
        a,b=decision_weights(-2,2,Fraction(1,4),TRANSFORMS[1])
        self.assertEqual(a+b,Fraction(182,209))
    def test_mixed_identity_additive(self):
        a,b=decision_weights(-2,2,Fraction(1,4),"identity")
        self.assertEqual(a+b,1)
    def test_witness_identity_value(self):
        self.assertEqual(lottery(-2,2,Fraction(1,4),"identity"),Fraction(1,2))
    def test_witness_noncanonical_value(self):
        self.assertEqual(lottery(-2,2,Fraction(1,4),TRANSFORMS[1]),Fraction(298,209))
    def test_identity_matches_expected_signed_value(self):
        for low,high in PAIRS:
            for p in PROBS:
                self.assertEqual(lottery(low,high,p,"identity"),p*value(low)+(1-p)*value(high))
    def test_weight_positive(self):
        for low,high in PAIRS:
            for p in PROBS:
                for k in TRANSFORMS:
                    self.assertTrue(all(Fraction(0)<x<Fraction(1) for x in decision_weights(low,high,p,k)))
    def test_no_zero_event(self):
        for x in generate()[0]:
            self.assertNotEqual(Fraction(x["outcome_probability"]),0)
    def test_finite_lottery_count(self):self.assertEqual(generate()[1]["lotteries"],36)
    def test_finite_source_count(self):self.assertEqual(generate()[1]["source_atoms"],72)
    def test_two_rows_per_lottery(self):
        a,b=generate()
        for i in range(36):
            self.assertEqual([a[2*i]["world"],a[2*i+1]["world"]],[str(i)]*2)
    def test_all_domains_present(self):
        self.assertEqual({x["domain"] for x in generate()[1]["outcomes"]},{"loss","mixed","gain"})
    def test_source_weighted_contribution(self):
        for a in generate()[0]:
            self.assertEqual(Fraction(a["weighted_contribution"]),Fraction(a["decision_weight"])*int(a["reference_value"]))
    def test_source_pair_total(self):
        a,_=generate()
        for i in range(0,72,2):
            self.assertEqual(Fraction(a[i]["weighted_contribution"])+Fraction(a[i+1]["weighted_contribution"]),Fraction(a[i]["lottery_value"]))
    def test_archive_replay(self):replay()

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true")
    p.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:
        result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(CPTTests))
        if not result.wasSuccessful():raise SystemExit(1)
    elif a.audit:
        replay()
        print("PASS R318: 72 exact signed rank contributions and 36 complete lotteries")
    else:
        print(json.dumps(generate()[1],indent=2))
