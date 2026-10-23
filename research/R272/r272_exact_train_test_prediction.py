#!/usr/bin/env python3
"""R272: exact artificial train/test prediction over nine Bernoulli worlds.

Each world enumerates 64 ordered six-bit sources: 4 train and 2 independent
test bits. The source enumeration and analytical binomial formulas are separate.
All probabilities and Brier errors are exact Fractions.
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

HERE = Path(__file__).resolve().parent
FREEZE = "52f84dbfbe8563cf5c9a491e67d5e320223e0a56"
PS = (F(1,4), F(1,2), F(3,4))
MODELS = ("CONSTANT_HALF", "TRAIN_MLE", "LAPLACE_BETA11")
WORLDS = tuple((p,model) for p in PS for model in MODELS)
BITS = tuple(itertools.product((0,1), repeat=6))
ZERO, ONE, HALF = F(0), F(1), F(1,2)
LOCKED = {
 (F(1,4),"CONSTANT_HALF"):("1/4","1/4"),
 (F(1,4),"TRAIN_MLE"):("9/64","15/64"),
 (F(1,4),"LAPLACE_BETA11"):("11/72","31/144"),
 (F(1,2),"CONSTANT_HALF"):("1/4","1/4"),
 (F(1,2),"TRAIN_MLE"):("3/16","5/16"),
 (F(1,2),"LAPLACE_BETA11"):("7/36","5/18"),
 (F(3,4),"CONSTANT_HALF"):("1/4","1/4"),
 (F(3,4),"TRAIN_MLE"):("9/64","15/64"),
 (F(3,4),"LAPLACE_BETA11"):("11/72","31/144"),
}

def validate(p,model):
    if (p,model) not in WORLDS:
        raise ValueError("unfrozen world")

def name_world(p,model):
    validate(p,model)
    return "TRUE_P"+str(p).replace("/","OF")+"_"+model

def forecast(model, k):
    if model not in MODELS or not isinstance(k,int) or not 0<=k<=4:
        raise ValueError("unfrozen model or training count")
    if model=="CONSTANT_HALF":return HALF
    if model=="TRAIN_MLE":return F(k,4)
    return F(k+1,6)

def brier(y,q):
    if y not in (0,1) or not 0<=q<=1:
        raise ValueError("invalid probability/label")
    return (F(y)-q)**2

def average_brier(bits,q):
    if len(bits)==0:raise ValueError("empty evaluation set")
    return sum((brier(y,q) for y in bits),ZERO)/len(bits)

def source_rows(p,model):
    """Route A: each distinct ordered primitive source, no analytical shortcut."""
    validate(p,model)
    mass_cache={}
    for original in BITS:
        train=original[:4];test=original[4:]
        k=sum(train);j=sum(test)
        q=forecast(model,k)
        mass=mass_cache.setdefault(k+j,p**(k+j)*(ONE-p)**(6-k-j))
        train_losses=tuple(brier(y,q) for y in train)
        test_losses=tuple(brier(y,q) for y in test)
        failure=int((q==ZERO and j>=1) or (q==ONE and j<=1))
        yield dict(world=name_world(p,model),true_p=p,predictor=model,
          original_full_sixbit_source="".join(map(str,original)),
          original_training_four_bits="".join(map(str,train)),
          original_future_test_two_bits="".join(map(str,test)),
          train_successes=k,test_successes=j,
          exact_original_source_probability=mass,
          forecast_trained_on_four_bits_only=q,
          original_train_brier_per_row=";".join(map(str,train_losses)),
          original_test_brier_per_row=";".join(map(str,test_losses)),
          exact_train_mean_brier=sum(train_losses,ZERO)/4,
          exact_independent_test_mean_brier=sum(test_losses,ZERO)/2,
          unfloored_future_log_loss_is_infinite=failure)

def exhaustive_moments(p,model):
    validate(p,model)
    rows=tuple(source_rows(p,model))
    assert len(rows)==64
    assert len({r["original_full_sixbit_source"] for r in rows})==64
    assert sum((r["exact_original_source_probability"] for r in rows),ZERO)==ONE
    mass_train=sum((r["exact_original_source_probability"]*r["exact_train_mean_brier"] for r in rows),ZERO)
    mass_future=sum((r["exact_original_source_probability"]*r["exact_independent_test_mean_brier"] for r in rows),ZERO)
    inf_mass=sum((r["exact_original_source_probability"]*r["unfloored_future_log_loss_is_infinite"] for r in rows),ZERO)
    return mass_train,mass_future,inf_mass

def independent_analytic(p,model):
    """Route B: train K Binomial(4,p), conditional future y Bernoulli(p).

    Does not consume source_rows, any ordered source, or actual test outcomes.
    """
    validate(p,model)
    train=future=ZERO
    for k in range(5):
        wk=F(comb(4,k))*p**k*(ONE-p)**(4-k)
        q=forecast(model,k)
        empirical=(F(k)*brier(1,q)+F(4-k)*brier(0,q))/4
        truefuture=p*brier(1,q)+(ONE-p)*brier(0,q)
        train+=wk*empirical
        future+=wk*truefuture
    inf=ZERO
    if model=="TRAIN_MLE":
        inf=(ONE-p)**4*(ONE-(ONE-p)**2)+p**4*(ONE-p**2)
    return train,future,inf

def frozen_claims():
    assert len(WORLDS)==9 and len(BITS)==64
    for p,m in WORLDS:
        actual=exhaustive_moments(p,m)
        oracle=independent_analytic(p,m)
        assert actual==oracle,(p,m,actual,oracle)
        assert tuple(map(str,actual[:2]))==LOCKED[p,m]
        expected_inf=(F(291,2048) if p!=HALF else F(3,32)) if m=="TRAIN_MLE" else ZERO
        assert actual[2]==expected_inf
    assert independent_analytic(HALF,"TRAIN_MLE")[1]>independent_analytic(HALF,"CONSTANT_HALF")[1]
    assert independent_analytic(F(1,4),"LAPLACE_BETA11")[1]<independent_analytic(F(1,4),"TRAIN_MLE")[1]
    return True

def emit():
    frozen_claims()
    src=HERE/"R272_ALL_576_ORIGINAL_TRAIN_AND_TEST_SOURCES.csv"
    cols=("world","true_p","predictor","original_full_sixbit_source",
      "original_training_four_bits","original_future_test_two_bits",
      "train_successes","test_successes","exact_original_source_probability",
      "forecast_trained_on_four_bits_only","original_train_brier_per_row",
      "original_test_brier_per_row","exact_train_mean_brier",
      "exact_independent_test_mean_brier","unfloored_future_log_loss_is_infinite")
    with src.open("w",encoding="utf-8",newline="") as handle:
        wr=csv.DictWriter(handle,fieldnames=cols,lineterminator="\n")
        wr.writeheader()
        for p,m in WORLDS:
            for z in source_rows(p,m):
                wr.writerow({key:str(z[key]) for key in cols})
    results=dict(research_id="R272",original_catalogue_id="12-002",
       prescore_freeze_commit=FREEZE,
       scope="FINITE_ARTIFICIAL_E1_INDEPENDENT_TRAIN4_TEST2_BERNOULLI_PREDICTION",
       artificial_worlds=9,complete_source_types=576,
       independent_source_sequences_per_true_p=64,
       training_bit_count=4,strictly_heldout_test_bit_count=2,
       all_nine_analytical_binomial_scores_verified=True,
       zero_probability_log_loss_failure_separately_recorded=True,
       no_real_human_E2=0,no_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[dict(world=name_world(p,m),true_p=str(p),predictor=m,
         full_ordered_source_types=64,
         exact_design_expected_train_mean_Brier=str(exhaustive_moments(p,m)[0]),
         exact_design_expected_independent_future_mean_Brier=str(exhaustive_moments(p,m)[1]),
         exact_unfloored_infinite_test_log_loss_event_probability=str(exhaustive_moments(p,m)[2]),
         source_enumeration_equals_independent_binomial_theory=True)
          for p,m in WORLDS])
    jp=HERE/"R272_EXACT_RESULTS.json"
    jp.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R272",prescore_freeze_commit=FREEZE,
       all_complete_original_sources=576,independent_analytic_comparisons=9,
       source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R272_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_world_count(self):self.assertEqual(len(WORLDS),9)
    def test_sources(self):self.assertEqual(len(BITS),64)
    def test_locked(self):self.assertTrue(frozen_claims())
    def test_brier_zero(self):self.assertEqual(brier(1,ONE),ZERO)
    def test_brier_one(self):self.assertEqual(brier(1,ZERO),ONE)
    def test_training_size(self):self.assertEqual(len(BITS[0][:4]),4)
    def test_testing_size(self):self.assertEqual(len(BITS[0][4:]),2)
    def test_mle_boundary(self):self.assertEqual(forecast("TRAIN_MLE",0),ZERO)
    def test_laplace_boundary(self):self.assertEqual(forecast("LAPLACE_BETA11",0),F(1,6))
    def test_invalid_world(self):
        with self.assertRaises(ValueError):list(source_rows(F(1,3),"TRAIN_MLE"))
    def test_invalid_forecaster(self):
        with self.assertRaises(ValueError):forecast("INVALID",1)

def _case(p,m,kind):
    def checker(self):
        source=tuple(source_rows(p,m))
        theory=independent_analytic(p,m)
        if kind=="mass":
            self.assertEqual(sum((r["exact_original_source_probability"] for r in source),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({r["original_full_sixbit_source"] for r in source}),64)
        elif kind=="train":
            self.assertTrue(all(r["original_training_four_bits"]==r["original_full_sixbit_source"][:4] for r in source))
        elif kind=="test":
            self.assertTrue(all(r["original_future_test_two_bits"]==r["original_full_sixbit_source"][4:] for r in source))
        elif kind=="frozen":
            self.assertEqual(tuple(map(str,exhaustive_moments(p,m)[:2])),LOCKED[p,m])
        elif kind=="oracle":self.assertEqual(exhaustive_moments(p,m),theory)
        elif kind=="scores":
            for r in source:
                self.assertEqual(r["exact_train_mean_brier"],
                   average_brier(tuple(map(int,r["original_training_four_bits"])),r["forecast_trained_on_four_bits_only"]))
                self.assertEqual(r["exact_independent_test_mean_brier"],
                   average_brier(tuple(map(int,r["original_future_test_two_bits"])),r["forecast_trained_on_four_bits_only"]))
        elif kind=="probability":
            self.assertTrue(all(F(r["exact_original_source_probability"]) ==
                p**sum(map(int,r["original_full_sixbit_source"]))*
                (ONE-p)**(6-sum(map(int,r["original_full_sixbit_source"]))) for r in source))
        else:raise AssertionError("unknown test")
    return checker

for p,m in WORLDS:
    for mode in ("mass","unique","train","test","frozen","oracle","scores","probability"):
        setattr(Tests,"test_p"+str(p).replace("/","of")+"_"+m.lower()+"_"+mode,_case(p,m,mode))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.test:unittest.main(argv=["r272"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
