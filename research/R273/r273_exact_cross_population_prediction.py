#!/usr/bin/env python3
"""R273: complete source-to-target Bernoulli population shift worlds.

Each of 27 worlds enumerates 64 sixbit configurations: four labelled source
training outcomes followed by two independent target outcomes. The two oracle
baselines are nondeployable comparators, not source-only learned predictors.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import unittest
from fractions import Fraction as F
from math import comb
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="91abafbaf627dbf67f86208a82008a5be419e507"
PS=(F(1,4),F(1,2),F(3,4))
MODELS=("SOURCE_ORACLE","SOURCE_LAPLACE","TARGET_ORACLE")
WORLDS=tuple((a,b,m) for a in PS for b in PS for m in MODELS)
BITS=tuple(itertools.product((0,1),repeat=6))
ZERO,ONE=F(0),F(1)

def validate(a,b,m):
    if (a,b,m) not in WORLDS:raise ValueError("unfrozen source target model")

def world_name(a,b,m):
    validate(a,b,m)
    return "A"+str(a).replace("/","OF")+"_B"+str(b).replace("/","OF")+"_"+m

def forecast(a,b,m,k):
    validate(a,b,m)
    if not isinstance(k,int) or not 0<=k<=4:raise ValueError("invalid train successes")
    if m=="SOURCE_ORACLE":return a
    if m=="SOURCE_LAPLACE":return F(k+1,6)
    return b

def brier(y,q):
    if y not in (0,1) or not 0<=q<=1:raise ValueError("invalid brier")
    return (F(y)-q)**2

def source_rows(a,b,m):
    """Route A: original 4-bit source, 2-bit target ordered source enumeration."""
    validate(a,b,m)
    for bits in BITS:
        train=bits[:4]
        test=bits[4:]
        k=sum(train);j=sum(test)
        q=forecast(a,b,m,k)
        prob=a**k*(ONE-a)**(4-k)*b**j*(ONE-b)**(2-j)
        trainloss=tuple(brier(y,q) for y in train)
        testloss=tuple(brier(y,q) for y in test)
        yield dict(world=world_name(a,b,m),source_group_true_p=a,target_group_true_p=b,
          fixed_predictor=m,original_full_source_target_sixbits="".join(map(str,bits)),
          original_source_group_fourbits="".join(map(str,train)),
          original_target_group_twobits="".join(map(str,test)),
          source_training_successes=k,target_test_successes=j,
          exact_two_population_source_probability=prob,
          frozen_before_target_observation_forecast=q,
          original_source_group_train_Brier_per_row=";".join(map(str,trainloss)),
          original_target_group_test_Brier_per_row=";".join(map(str,testloss)),
          source_mean_Brier=sum(trainloss,ZERO)/4,
          target_independent_mean_Brier=sum(testloss,ZERO)/2,
          target_forecast_bias=q-b)

def source_integrated(a,b,m):
    validate(a,b,m)
    rows=tuple(source_rows(a,b,m))
    assert len(rows)==64
    assert len({r["original_full_source_target_sixbits"] for r in rows})==64
    assert sum((r["exact_two_population_source_probability"] for r in rows),ZERO)==ONE
    in_sample=sum((r["exact_two_population_source_probability"]*r["source_mean_Brier"] for r in rows),ZERO)
    target=sum((r["exact_two_population_source_probability"]*r["target_independent_mean_Brier"] for r in rows),ZERO)
    bias=sum((r["exact_two_population_source_probability"]*r["target_forecast_bias"] for r in rows),ZERO)
    return in_sample,target,bias

def independent_analytic(a,b,m):
    """Route B: K Binomial(4,a) and target Bernoulli(b), no test enumeration."""
    validate(a,b,m)
    if m=="SOURCE_ORACLE":
        return b*(ONE-b)+(a-b)**2,a-b
    if m=="TARGET_ORACLE":
        return b*(ONE-b),ZERO
    mu=F(4*a+1,6)
    variance=a*(ONE-a)/9
    return b*(ONE-b)+variance+(mu-b)**2,mu-b

def independent_train_risk(a,b,m):
    """Separate source-distribution aggregate over K, not any ordered source."""
    validate(a,b,m)
    result=ZERO
    for k in range(5):
        mass=F(comb(4,k))*a**k*(ONE-a)**(4-k)
        q=forecast(a,b,m,k)
        result+=mass*(F(k)*(ONE-q)**2+F(4-k)*q*q)/4
    return result

def frozen_claims():
    assert len(WORLDS)==27 and len(BITS)==64
    assert 27*64==1728
    for a,b,m in WORLDS:
        empirical=source_integrated(a,b,m)
        target,bias=independent_analytic(a,b,m)
        inrisk=independent_train_risk(a,b,m)
        assert empirical==(inrisk,target,bias),(a,b,m,empirical,inrisk,target,bias)
        if a==b and m in ("SOURCE_ORACLE","TARGET_ORACLE"):
            assert target==a*(ONE-a)
    assert independent_analytic(F(1,4),F(3,4),"SOURCE_ORACLE")[0]==F(7,16)
    assert independent_analytic(F(1,4),F(3,4),"TARGET_ORACLE")[0]==F(3,16)
    assert independent_analytic(F(1,4),F(3,4),"SOURCE_LAPLACE")[0]==F(55,144)
    assert independent_analytic(F(1,4),F(1,2),"SOURCE_LAPLACE")[0]==F(43,144)
    assert independent_analytic(F(1,4),F(1,4),"SOURCE_LAPLACE")[0]==F(31,144)
    return True

def emit():
    frozen_claims()
    csvpath=HERE/"R273_ALL_1728_ORIGINAL_CROSS_POPULATION_SOURCES.csv"
    cols=("world","source_group_true_p","target_group_true_p","fixed_predictor",
      "original_full_source_target_sixbits",
      "original_source_group_fourbits","original_target_group_twobits",
      "source_training_successes","target_test_successes",
      "exact_two_population_source_probability",
      "frozen_before_target_observation_forecast",
      "original_source_group_train_Brier_per_row",
      "original_target_group_test_Brier_per_row",
      "source_mean_Brier","target_independent_mean_Brier","target_forecast_bias")
    with csvpath.open("w",encoding="utf-8",newline="") as handle:
        wr=csv.DictWriter(handle,fieldnames=cols,lineterminator="\n")
        wr.writeheader()
        for a,b,m in WORLDS:
            for row in source_rows(a,b,m):
                wr.writerow({key:str(row[key]) for key in cols})
    results=dict(research_id="R273",original_catalogue_id="12-003",
       prescore_freeze_commit=FREEZE,
       evidence="E1_ARTIFICIAL_COMPLETE_SOURCE_TO_TARGET_BERNOULLI_POPULATION_TRANSFER",
       all_artificial_source_types=1728,worlds=27,
       original_source_group_train_bits=4,original_independent_target_group_test_bits=2,
       source_and_target_probability_space="all pairs from [1/4,1/2,3/4]",
       oracle_comparators_not_source_only_deployable=True,
       all_27_source_versus_independent_analytic_expected_risk_checks_pass=True,
       real_human_E2=0,real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[dict(world=world_name(a,b,m),source_p=str(a),target_p=str(b),
         predictor=m,original_source_types=64,
         complete_source_expected_training_Brier=str(source_integrated(a,b,m)[0]),
         complete_source_expected_target_test_Brier=str(source_integrated(a,b,m)[1]),
         expected_forecast_minus_target_probability=str(source_integrated(a,b,m)[2]),
         independent_analytic_target_risk_verified=True)
         for a,b,m in WORLDS])
    resultpath=HERE/"R273_EXACT_CROSS_POPULATION_RESULTS.json"
    resultpath.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R273",prescore_freeze_commit=FREEZE,
      original_complete_source_types=1728,independent_analytical_worlds=27,
      source_sha256=hashlib.sha256(csvpath.read_bytes()).hexdigest(),
      results_sha256=hashlib.sha256(resultpath.read_bytes()).hexdigest(),
      real_human_E2=0,real_historical_E3=0)
    (HERE/"R273_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLDS),27)
    def test_source_count(self):self.assertEqual(len(BITS)*len(WORLDS),1728)
    def test_frozen(self):self.assertTrue(frozen_claims())
    def test_source_oracle(self):self.assertEqual(forecast(F(1,4),F(3,4),"SOURCE_ORACLE",0),F(1,4))
    def test_target_oracle(self):self.assertEqual(forecast(F(1,4),F(3,4),"TARGET_ORACLE",0),F(3,4))
    def test_laplace(self):self.assertEqual(forecast(F(1,4),F(3,4),"SOURCE_LAPLACE",0),F(1,6))
    def test_brier_zero(self):self.assertEqual(brier(1,ONE),ZERO)
    def test_brier_one(self):self.assertEqual(brier(1,ZERO),ONE)
    def test_invalid_world(self):
        with self.assertRaises(ValueError):list(source_rows(F(1,3),F(1,4),"SOURCE_LAPLACE"))
    def test_invalid_successes(self):
        with self.assertRaises(ValueError):forecast(F(1,4),F(1,2),"SOURCE_LAPLACE",5)

def _case(a,b,m,kind):
    def test(self):
        rows=tuple(source_rows(a,b,m))
        if kind=="mass":
            self.assertEqual(sum((r["exact_two_population_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({r["original_full_source_target_sixbits"] for r in rows}),64)
        elif kind=="split":
            self.assertTrue(all(r["original_full_source_target_sixbits"] ==
                r["original_source_group_fourbits"]+r["original_target_group_twobits"] for r in rows))
        elif kind=="oracle":
            res=source_integrated(a,b,m)
            target,bias=independent_analytic(a,b,m)
            self.assertEqual(res,(independent_train_risk(a,b,m),target,bias))
        elif kind=="moments":
            self.assertEqual(source_integrated(a,b,m)[1],independent_analytic(a,b,m)[0])
        elif kind=="scores":
            for r in rows:
                q=r["frozen_before_target_observation_forecast"]
                self.assertEqual(r["source_mean_Brier"],
                   sum((brier(int(z),q) for z in r["original_source_group_fourbits"]),ZERO)/4)
                self.assertEqual(r["target_independent_mean_Brier"],
                   sum((brier(int(z),q) for z in r["original_target_group_twobits"]),ZERO)/2)
        else:raise AssertionError("unfrozen test")
    return test

for a,b,m in WORLDS:
    for k in ("mass","unique","split","oracle","moments","scores"):
        setattr(Tests,"test_a"+str(a).replace("/","of")+"_b"+str(b).replace("/","of")+"_"+m.lower()+"_"+k,
           _case(a,b,m,k))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    z=ap.parse_args()
    if z.test:unittest.main(argv=["r273"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
