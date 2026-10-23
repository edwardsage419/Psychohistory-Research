#!/usr/bin/env python3
"""R274: strict forward holdout versus forbidden hindsight label leakage.

Nine sixbit finite artificial temporal worlds, each 4 past and 2 future bits.
All nine future mean Brier risks are exactly aggregated by ordered source space
and independently by Binomial past/future success counts.
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
FREEZE="47b75b49afb5c72c5ca2599ab38499e0f2856354"
REGIMES={
 "STABLE_HALF":(F(1,2),F(1,2)),
 "RISING_RATE":(F(1,4),F(3,4)),
 "FALLING_RATE":(F(3,4),F(1,4)),
}
MODELS=("PAST_ONLY_LAPLACE","HINDSIGHT_POOLED","PRECOMMITTED_HALF")
WORLDS=tuple((name,m) for name in REGIMES for m in MODELS)
ALL_BITS=tuple(itertools.product((0,1),repeat=6))
ZERO,ONE=F(0),F(1)
LOCKED={
 ("STABLE_HALF","PAST_ONLY_LAPLACE"):F(5,18),
 ("STABLE_HALF","HINDSIGHT_POOLED"):F(27,128),
 ("STABLE_HALF","PRECOMMITTED_HALF"):F(1,4),
 ("RISING_RATE","PAST_ONLY_LAPLACE"):F(55,144),
 ("RISING_RATE","HINDSIGHT_POOLED"):F(131,512),
 ("RISING_RATE","PRECOMMITTED_HALF"):F(1,4),
 ("FALLING_RATE","PAST_ONLY_LAPLACE"):F(55,144),
 ("FALLING_RATE","HINDSIGHT_POOLED"):F(131,512),
 ("FALLING_RATE","PRECOMMITTED_HALF"):F(1,4),
}

def validate(regime,model):
    if (regime,model) not in WORLDS:
        raise ValueError("outside frozen temporal model")

def forecast(regime,model,K,J):
    validate(regime,model)
    if not isinstance(K,int) or not isinstance(J,int) or K not in range(5) or J not in range(3):
        raise ValueError("requires four past and two future bit counts")
    if model=="PAST_ONLY_LAPLACE":return F(K+1,6)
    if model=="HINDSIGHT_POOLED":return F(K+J+1,8)
    return F(1,2)

def square(y,q):
    if y not in (0,1) or not 0<=q<=1:
        raise ValueError("invalid forecast/outcome")
    return (F(y)-q)**2

def primitive_sources(regime,model):
    """Route A: complete ordered original 4 past + 2 future bit types."""
    validate(regime,model)
    a,b=REGIMES[regime]
    for bits in ALL_BITS:
        old=bits[:4];future=bits[4:]
        K=sum(old);J=sum(future)
        q=forecast(regime,model,K,J)
        mass=a**K*(ONE-a)**(4-K)*b**J*(ONE-b)**(2-J)
        losses=tuple(square(v,q) for v in future)
        yield dict(world=regime+"_"+model,time_regime=regime,model=model,
           past_true_bernoulli_p=a,future_true_bernoulli_p=b,
           original_sixbit_ordered_temporal_source="".join(map(str,bits)),
           original_past_t1_to_t4_bits="".join(map(str,old)),
           original_future_t5_to_t6_bits="".join(map(str,future)),
           original_past_successes=K,original_future_successes=J,
           exact_original_temporal_source_mass=mass,
           reported_probability_for_t5_t6=q,
           future_outcomes_illegally_seen_during_fit=int(model=="HINDSIGHT_POOLED"),
           future_t5_t6_brier_each=";".join(map(str,losses)),
           future_t5_t6_mean_brier=sum(losses,ZERO)/2)

def source_risk(regime,model):
    validate(regime,model)
    rows=tuple(primitive_sources(regime,model))
    assert len(rows)==64
    assert len({r["original_sixbit_ordered_temporal_source"] for r in rows})==64
    assert sum((r["exact_original_temporal_source_mass"] for r in rows),ZERO)==ONE
    return sum((r["exact_original_temporal_source_mass"]*
               r["future_t5_t6_mean_brier"] for r in rows),ZERO)

def independent_count_risk(regime,model):
    """Route B: count distribution Binom(4,a)*Binom(2,b), not source rows."""
    validate(regime,model)
    a,b=REGIMES[regime]
    total=ZERO
    for k in range(5):
        pk=F(comb(4,k))*a**k*(ONE-a)**(4-k)
        for j in range(3):
            pj=F(comb(2,j))*b**j*(ONE-b)**(2-j)
            q=forecast(regime,model,k,j)
            actual_loss=(F(j)*(ONE-q)**2+F(2-j)*q*q)/2
            total+=pk*pj*actual_loss
    return total

def leakage_audit(regime,model):
    validate(regime,model)
    observations=[]
    for k in range(5):
        forecasts={forecast(regime,model,k,j) for j in range(3)}
        observations.append(len(forecasts))
    if model=="HINDSIGHT_POOLED":
        assert observations==[3]*5
        return True
    assert observations==[1]*5
    return False

def frozen_claims():
    assert len(WORLDS)==9 and len(ALL_BITS)==64
    assert 9*64==576
    for regime,model in WORLDS:
        a=source_risk(regime,model)
        b=independent_count_risk(regime,model)
        assert a==b==LOCKED[regime,model],(regime,model,a,b)
        assert leakage_audit(regime,model)==(model=="HINDSIGHT_POOLED")
    assert LOCKED["STABLE_HALF","HINDSIGHT_POOLED"]<LOCKED["STABLE_HALF","PRECOMMITTED_HALF"]
    assert LOCKED["RISING_RATE","PAST_ONLY_LAPLACE"]>LOCKED["RISING_RATE","PRECOMMITTED_HALF"]
    return True

def emit():
    frozen_claims()
    src=HERE/"R274_ALL_576_ORIGINAL_FORWARD_HOLDOUT_SOURCES.csv"
    columns=("world","time_regime","model","past_true_bernoulli_p",
      "future_true_bernoulli_p","original_sixbit_ordered_temporal_source",
      "original_past_t1_to_t4_bits","original_future_t5_to_t6_bits",
      "original_past_successes","original_future_successes",
      "exact_original_temporal_source_mass","reported_probability_for_t5_t6",
      "future_outcomes_illegally_seen_during_fit",
      "future_t5_t6_brier_each","future_t5_t6_mean_brier")
    with src.open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=columns,lineterminator="\n")
        writer.writeheader()
        for r,m in WORLDS:
            for z in primitive_sources(r,m):
                writer.writerow({k:str(z[k]) for k in columns})
    output=dict(research_id="R274",original_catalogue_id="12-004",
        prescore_freeze_commit=FREEZE,
        evidence_scope="ARTIFICIAL_E1_FINITE_TEMPORAL_HOLDOUT_VS_INVALID_HINDSIGHT_SCORE",
        original_complete_source_types=576,
        artificial_regimes=3,models_per_regime=3,worlds=9,
        history_length=4,future_test_length=2,
        future_label_leakage_explicitly_recorded=True,
        all_nine_binomial_analytic_risks_verified=True,
        no_real_human_E2=0,no_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=[dict(world=r+"_"+m,regime=r,model=m,
          past_p=str(REGIMES[r][0]),future_p=str(REGIMES[r][1]),
          full_ordered_primitive_source_types=64,
          exact_source_weighted_future_test_Brier=str(source_risk(r,m)),
          future_labels_illegally_used_in_model_fit=(m=="HINDSIGHT_POOLED"),
          independent_K_and_J_count_expectation_verified=True)
          for r,m in WORLDS])
    jp=HERE/"R274_EXACT_RESULTS.json"
    jp.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R274",prescore_freeze_commit=FREEZE,
        total_original_source_types=576,independently_verified_temporal_worlds=9,
        source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
        no_real_human_E2=0,no_real_historical_E3=0)
    (HERE/"R274_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_frozen(self):self.assertTrue(frozen_claims())
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_total_source_types(self):self.assertEqual(len(ALL_BITS)*len(WORLDS),576)
    def test_past_only(self):self.assertEqual(forecast("STABLE_HALF","PAST_ONLY_LAPLACE",2,0),forecast("STABLE_HALF","PAST_ONLY_LAPLACE",2,2))
    def test_hindsight_leakage(self):self.assertNotEqual(forecast("STABLE_HALF","HINDSIGHT_POOLED",2,0),forecast("STABLE_HALF","HINDSIGHT_POOLED",2,2))
    def test_baseline(self):self.assertEqual(forecast("STABLE_HALF","PRECOMMITTED_HALF",0,0),F(1,2))
    def test_regime_order(self):self.assertEqual(REGIMES["RISING_RATE"],(F(1,4),F(3,4)))
    def test_zero_loss(self):self.assertEqual(square(1,ONE),ZERO)
    def test_invalid(self):
        with self.assertRaises(ValueError):list(primitive_sources("UNKNOWN","PAST_ONLY_LAPLACE"))
    def test_unfrozen_future(self):
        with self.assertRaises(ValueError):forecast("STABLE_HALF","HINDSIGHT_POOLED",2,3)

def _case(regime,model,mode):
    def test(self):
        rows=tuple(primitive_sources(regime,model))
        if mode=="mass":
            self.assertEqual(sum((r["exact_original_temporal_source_mass"] for r in rows),ZERO),ONE)
        elif mode=="unique":
            self.assertEqual(len({r["original_sixbit_ordered_temporal_source"] for r in rows}),64)
        elif mode=="future":
            self.assertTrue(all(r["original_sixbit_ordered_temporal_source"] ==
                r["original_past_t1_to_t4_bits"]+r["original_future_t5_to_t6_bits"] for r in rows))
        elif mode=="risk":
            self.assertEqual(source_risk(regime,model),independent_count_risk(regime,model))
        elif mode=="locked":
            self.assertEqual(source_risk(regime,model),LOCKED[regime,model])
        elif mode=="leak":
            self.assertEqual(leakage_audit(regime,model),model=="HINDSIGHT_POOLED")
        elif mode=="score":
            for r in rows:
                q=r["reported_probability_for_t5_t6"]
                two=[square(int(z),q) for z in r["original_future_t5_to_t6_bits"]]
                self.assertEqual(r["future_t5_t6_brier_each"],";".join(map(str,two)))
                self.assertEqual(r["future_t5_t6_mean_brier"],sum(two,ZERO)/2)
        elif mode=="prob":
            a,b=REGIMES[regime]
            self.assertTrue(all(r["exact_original_temporal_source_mass"] ==
                a**r["original_past_successes"]*(ONE-a)**(4-r["original_past_successes"])*
                b**r["original_future_successes"]*(ONE-b)**(2-r["original_future_successes"]) for r in rows))
        else:raise AssertionError("bad test")
    return test

for regime,model in WORLDS:
    for kind in ("mass","unique","future","risk","locked","leak","score","prob"):
        setattr(Tests,"test_"+regime.lower()+"_"+model.lower()+"_"+kind,_case(regime,model,kind))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.test:unittest.main(argv=["r274"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
