#!/usr/bin/env python3
"""R278 complete artificial Bernoulli ensemble and heldout-scoring study.
12 worlds x 64 ordered primitive sources, exact Fraction arithmetic.
Route A independently evaluates all ordered outcomes, route B only training K
and an analytically expected future Bernoulli loss. No external dependencies.
"""
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
FREEZE="eb1c8df38349c36ed10d7a2103969818b14d7500"
PS=(F(1,4),F(1,2),F(3,4))
MODELS=("HARD_SELECT","BAYES_AVERAGE","FIXED_HALF","TRUTH_ORACLE")
WORLDS=tuple((p,m) for p in PS for m in MODELS)
BITS=tuple(itertools.product((0,1), repeat=6))
ZERO,ONE=F(0),F(1)
LOCKED={
 (F(1,4),"HARD_SELECT"):(F(89,512),F(205,1024)),
 (F(1,4),"BAYES_AVERAGE"):(F(267,1640),F(87,410)),
 (F(1,4),"FIXED_HALF"):(F(1,4),F(1,4)),
 (F(1,4),"TRUTH_ORACLE"):(F(3,16),F(3,16)),
 (F(1,2),"HARD_SELECT"):(F(7,32),F(5,16)),
 (F(1,2),"BAYES_AVERAGE"):(F(33107,168100),F(46637,168100)),
 (F(1,2),"FIXED_HALF"):(F(1,4),F(1,4)),
 (F(1,2),"TRUTH_ORACLE"):(F(1,4),F(1,4)),
 (F(3,4),"HARD_SELECT"):(F(89,512),F(259,1024)),
 (F(3,4),"BAYES_AVERAGE"):(F(267,1640),F(87,410)),
 (F(3,4),"FIXED_HALF"):(F(1,4),F(1,4)),
 (F(3,4),"TRUTH_ORACLE"):(F(3,16),F(3,16))}
CANDIDATES=(F(1,4),F(3,4))

def check(p,m):
    if (p,m) not in WORLDS:raise ValueError("unfrozen world")

def likelihoods(k):
    if not isinstance(k,int) or not 0<=k<=4:raise ValueError("training count 0-4 only")
    return tuple(q**k*(ONE-q)**(4-k) for q in CANDIDATES)

def posterior_low(k):
    a,b=likelihoods(k)
    return a/(a+b)

def predict(p,m,k):
    check(p,m)
    a,b=likelihoods(k)
    if m=="HARD_SELECT":return CANDIDATES[0] if a>=b else CANDIDATES[1]
    if m=="BAYES_AVERAGE":return (a*CANDIDATES[0]+b*CANDIDATES[1])/(a+b)
    if m=="FIXED_HALF":return F(1,2)
    return p

def world_name(p,m):
    check(p,m)
    return "P"+str(p).replace("/","OF")+"_"+m

def source_rows(p,m):
    """Route A: every ordered primitive 6bit type and separate future scoring."""
    check(p,m)
    for bits in BITS:
        x=bits[:4];y=bits[4:]
        k=sum(x);j=sum(y)
        w=p**(k+j)*(ONE-p)**(6-k-j)
        q=predict(p,m,k)
        train_loss=tuple((F(z)-q)**2 for z in x)
        test_loss=tuple((F(z)-q)**2 for z in y)
        yield dict(world=world_name(p,m),true_p=p,model_policy=m,
          original_full_sixbit_source="".join(map(str,bits)),
          original_training_fourbit="".join(map(str,x)),
          original_holdout_twobit="".join(map(str,y)),
          original_train_successes=k,original_test_successes=j,
          original_source_probability=w,
          posterior_probability_of_low_candidate=posterior_low(k),
          frozen_after_training_singlebit_prediction=q,
          hard_selection_tie_at_k2=int(k==2),
          policy_uses_unavailable_true_p=int(m=="TRUTH_ORACLE"),
          train_row_Brier=";".join(map(str,train_loss)),
          holdout_row_Brier=";".join(map(str,test_loss)),
          mean_train_Brier=sum(train_loss,ZERO)/4,
          mean_holdout_Brier=sum(test_loss,ZERO)/2)

def source_means(p,m):
    check(p,m)
    rows=tuple(source_rows(p,m))
    assert len(rows)==64
    assert len({r["original_full_sixbit_source"] for r in rows})==64
    assert sum((r["original_source_probability"] for r in rows),ZERO)==ONE
    return (sum((r["original_source_probability"]*r["mean_train_Brier"] for r in rows),ZERO),
            sum((r["original_source_probability"]*r["mean_holdout_Brier"] for r in rows),ZERO))

def analytic_means(p,m):
    """Route B: uses Binomial K, true future Bernoulli risk; no source rows."""
    check(p,m)
    tr=fu=ZERO
    for k in range(5):
        mass=F(comb(4,k))*p**k*(ONE-p)**(4-k)
        q=predict(p,m,k)
        tr+=mass*(k*(ONE-q)**2+(4-k)*q*q)/4
        fu+=mass*(p*(ONE-q)**2+(ONE-p)*q*q)
    return tr,fu

def frozen_claims():
    assert len(WORLDS)==12 and len(BITS)==64
    assert len(LOCKED)==12
    assert [predict(F(1,2),"BAYES_AVERAGE",k) for k in range(5)]==[
        F(21,82),F(3,10),F(1,2),F(7,10),F(61,82)]
    assert predict(F(3,4),"HARD_SELECT",2)==F(1,4)
    for p,m in WORLDS:
        assert source_means(p,m)==analytic_means(p,m)==LOCKED[p,m]
    assert LOCKED[F(1,4),"HARD_SELECT"][1]<LOCKED[F(1,4),"BAYES_AVERAGE"][1]
    assert LOCKED[F(3,4),"HARD_SELECT"][1]>LOCKED[F(3,4),"BAYES_AVERAGE"][1]
    assert LOCKED[F(1,2),"BAYES_AVERAGE"][1]>LOCKED[F(1,2),"FIXED_HALF"][1]
    return True

def emit():
    frozen_claims()
    src=HERE/"R278_ALL_768_ORIGINAL_MODEL_AVERAGING_SOURCES.csv"
    cols=("world","true_p","model_policy","original_full_sixbit_source",
          "original_training_fourbit","original_holdout_twobit",
          "original_train_successes","original_test_successes",
          "original_source_probability","posterior_probability_of_low_candidate",
          "frozen_after_training_singlebit_prediction","hard_selection_tie_at_k2",
          "policy_uses_unavailable_true_p","train_row_Brier","holdout_row_Brier",
          "mean_train_Brier","mean_holdout_Brier")
    with src.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        writer.writeheader()
        for p,m in WORLDS:
            for row in source_rows(p,m):
                writer.writerow({key:str(row[key]) for key in cols})
    results=dict(research_id="R278",original_catalogue_id="12-008",
       prescore_freeze_commit=FREEZE,
       evidence="BOUNDED_E1_ARTIFICIAL_TWO_MODEL_BAYES_AVERAGING_VS_HARD_SELECTION",
       artificial_worlds=12,original_complete_model_labelled_sources=768,
       original_bit_types_per_p=64,train_bits=4,heldout_bits=2,
       model_weight_prior="1/2 each on candidate q=1/4 and q=3/4",
       hard_selection_tie_break="q=1/4 if K=2",
       target_oracle_infeasible_as_source_only_forecaster=True,
       two_holdout_bit_Brier="separately scored single-bit marginals, no joint independence claim",
       all_twelve_exact_source_means_equal_independent_binomial_means=True,
       no_real_human_E2=0,no_real_historical_E3=0,R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[dict(world=world_name(p,m),true_p=str(p),policy=m,
           primitive_sources=64,
           expected_training_Brier=str(source_means(p,m)[0]),
           expected_independent_holdout_Brier=str(source_means(p,m)[1]),
           independent_binomial_risk_verified=True)
          for p,m in WORLDS])
    jp=HERE/"R278_EXACT_RESULTS.json"
    jp.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R278",prescore_freeze_commit=FREEZE,source_types=768,
       independent_analytic_risk_worlds=12,
       source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
       no_real_human_E2=0,no_real_historical_E3=0)
    (HERE/"R278_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_frozen(self):self.assertTrue(frozen_claims())
    def test_worlds(self):self.assertEqual(len(WORLDS),12)
    def test_total_sources(self):self.assertEqual(len(WORLDS)*len(BITS),768)
    def test_likelihood_tie(self):self.assertEqual(*likelihoods(2))
    def test_hard_tie_low(self):self.assertEqual(predict(F(3,4),"HARD_SELECT",2),F(1,4))
    def test_bma_k2(self):self.assertEqual(predict(F(1,2),"BAYES_AVERAGE",2),F(1,2))
    def test_invalid_k(self):
        with self.assertRaises(ValueError):likelihoods(5)
    def test_bad_model(self):
        with self.assertRaises(ValueError):list(source_rows(F(1,4),"NOT_A_MODEL"))
    def test_oracle(self):self.assertEqual(predict(F(3,4),"TRUTH_ORACLE",0),F(3,4))
    def test_center_case(self):self.assertGreater(analytic_means(F(1,2),"BAYES_AVERAGE")[1],F(1,4))
    def test_source_unique(self):self.assertEqual(len({v for v in BITS}),64)
    def test_bma_low(self):self.assertEqual(posterior_low(0),F(81,82))

def case(p,m,kind):
    def test(self):
        rows=tuple(source_rows(p,m))
        if kind=="mass":self.assertEqual(sum((r["original_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="count":self.assertEqual(len(rows),64)
        elif kind=="unique":self.assertEqual(len({r["original_full_sixbit_source"] for r in rows}),64)
        elif kind=="means":self.assertEqual(source_means(p,m),analytic_means(p,m))
        elif kind=="locked":self.assertEqual(source_means(p,m),LOCKED[p,m])
        elif kind=="train_only":
            for row in rows:
                k=row["original_train_successes"]
                self.assertEqual(row["frozen_after_training_singlebit_prediction"],predict(p,m,k))
        elif kind=="source":
            for row in rows:
                bits=row["original_full_sixbit_source"]
                self.assertEqual(row["original_source_probability"],
                   p**bits.count("1")*(ONE-p)**(6-bits.count("1")))
        elif kind=="predictions":
            self.assertTrue(all(ZERO<=r["frozen_after_training_singlebit_prediction"]<=ONE for r in rows))
        else:raise AssertionError("unfrozen")
    return test
for p,m in WORLDS:
    for kind in ("mass","count","unique","means","locked","train_only","source","predictions"):
        setattr(Tests,"test_p"+str(p).replace("/","of")+"_"+m.lower()+"_"+kind,case(p,m,kind))
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.test:unittest.main(argv=["r278"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
