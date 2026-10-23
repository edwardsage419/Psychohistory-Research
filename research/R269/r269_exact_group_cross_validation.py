#!/usr/bin/env python3
"""R269: exact 576-source, six-group row-LOO versus group-LOGO audit.

Only six independent Bernoulli group latents exist in each artificial world.
Two rows share each latent label. The genuine out-of-group task holds out both.
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
FREEZE = "1ba86be0a35b77c0d5e5f6a72bb102ba08c48795"
PS = (F(1,4), F(1,2), F(3,4))
MODELS = ("GROUP_ID_MEMORIZER", "GLOBAL_LAPLACE", "CONSTANT_HALF")
PROTOCOLS = ("LOOR", "LOGO")
WORLDS = tuple((p, model) for p in PS for model in MODELS)
ZERO, ONE, HALF = F(0), F(1), F(1,2)
BITS = tuple(itertools.product((0,1), repeat=6))

def label(p, model):
    if (p,model) not in WORLDS:
        raise ValueError("not a frozen world")
    return "P" + str(p).replace("/", "OF") + "_" + model

def make_rows(bits):
    if len(bits)!=6 or any(v not in (0,1) for v in bits):
        raise ValueError("six binary latent group outcomes required")
    return tuple((group, bits[group]) for group in range(6) for _ in range(2))

def fold_indices(target_row, protocol):
    if not 0 <= target_row < 12 or protocol not in PROTOCOLS:
        raise ValueError("unknown fold")
    group = target_row//2
    if protocol == "LOOR":
        training = tuple(i for i in range(12) if i!=target_row)
        testing = (target_row,)
    else:
        training = tuple(i for i in range(12) if i//2!=group)
        testing = (2*group,2*group+1)
    assert set(training).isdisjoint(testing)
    return training, testing

def fitted_predictor(model, training_rows, target_group):
    if model not in MODELS or not 0 <= target_group < 6:
        raise ValueError("unknown predictor/target")
    if model == "CONSTANT_HALF":
        return HALF
    if model == "GLOBAL_LAPLACE":
        return F(1+sum(y for group,y in training_rows),2+len(training_rows))
    matches=[y for group,y in training_rows if group==target_group]
    if matches:
        assert len(set(matches)) == 1
        return F(matches[0])
    return HALF

def fold_evaluation(bits, model, protocol):
    """Route A: fit each model from actual indexed training rows at each fold."""
    if model not in MODELS or protocol not in PROTOCOLS:
        raise ValueError("unknown model/protocol")
    rows=make_rows(bits)
    predicted=[]
    losses=[]
    same_group_training=[]
    for i,(g,y) in enumerate(rows):
        training_ids,test_ids=fold_indices(i,protocol)
        assert i in test_ids
        training=tuple(rows[k] for k in training_ids)
        q=fitted_predictor(model, training, g)
        leak=sum(k//2==g for k in training_ids)
        same_group_training.append(leak)
        predicted.append(q)
        losses.append((F(y)-q)**2)
    assert len(predicted)==len(losses)==12
    assert same_group_training==([1]*12 if protocol=="LOOR" else [0]*12)
    return dict(average_brier=sum(losses,ZERO)/12,
                predicted=tuple(predicted), losses=tuple(losses),
                same_group_train_counts=tuple(same_group_training))

def source_rows(p,model):
    label(p,model)
    for bits in BITS:
        mass=p**sum(bits)*(ONE-p)**(6-sum(bits))
        loor=fold_evaluation(bits,model,"LOOR")
        logo=fold_evaluation(bits,model,"LOGO")
        yield dict(world=label(p,model), predictor=model, true_p=p,
             original_six_independent_group_latents="".join(map(str,bits)),
             original_complete_source_probability=mass,
             original_twelve_row_groups=";".join(str(i//2) for i in range(12)),
             original_twelve_row_outcomes=";".join(str(bits[i//2]) for i in range(12)),
             loor_row_predictions=";".join(str(v) for v in loor["predicted"]),
             loor_row_squared_losses=";".join(str(v) for v in loor["losses"]),
             loor_average_brier=loor["average_brier"],
             logo_row_predictions=";".join(str(v) for v in logo["predicted"]),
             logo_row_squared_losses=";".join(str(v) for v in logo["losses"]),
             logo_average_brier=logo["average_brier"])

def exact_source_expectation(p,model):
    label(p,model)
    rows=tuple(source_rows(p,model))
    assert len(rows)==64
    assert len({r["original_six_independent_group_latents"] for r in rows})==64
    assert sum((r["original_complete_source_probability"] for r in rows),ZERO)==ONE
    return dict(LOOR=sum((r["original_complete_source_probability"]*
                          r["loor_average_brier"] for r in rows),ZERO),
                LOGO=sum((r["original_complete_source_probability"]*
                          r["logo_average_brier"] for r in rows),ZERO))

def independent_binomial_theory(p,model):
    """Route B: no source enumeration or model fit; use B and S binomial laws."""
    label(p,model)
    if model=="GROUP_ID_MEMORIZER":
        return dict(LOOR=ZERO,LOGO=F(1,4))
    if model=="CONSTANT_HALF":
        return dict(LOOR=F(1,4),LOGO=F(1,4))
    expectation={"LOOR":ZERO,"LOGO":ZERO}
    for b in (0,1):
        pb=p if b else ONE-p
        for s in range(6):
            ps=F(comb(5,s))*p**s*(ONE-p)**(5-s)
            rowq=F(2*s+b+1,13)
            groupq=F(2*s+1,12)
            expectation["LOOR"]+=pb*ps*(F(b)-rowq)**2
            expectation["LOGO"]+=pb*ps*(F(b)-groupq)**2
    numerator=ONE+160*p*(ONE-p)
    assert expectation=={"LOOR":numerator/169,"LOGO":numerator/144}
    return expectation

def locked_claims():
    assert len(WORLDS)==9 and len(BITS)==64
    assert len(tuple(make_rows((0,)*6)))==12
    assert sum(len(tuple(source_rows(p,m))) for p,m in WORLDS)==576
    for p,model in WORLDS:
        a=exact_source_expectation(p,model)
        b=independent_binomial_theory(p,model)
        assert a==b,(p,model,a,b)
        if model=="GROUP_ID_MEMORIZER":
            assert a=={"LOOR":ZERO,"LOGO":F(1,4)}
        elif model=="CONSTANT_HALF":
            assert a=={"LOOR":F(1,4),"LOGO":F(1,4)}
        else:
            x=F(31) if p!=F(1,2) else F(41)
            assert a=={"LOOR":x/169,"LOGO":x/144}
    return True

def emit():
    locked_claims()
    source_path=HERE/"R269_ALL_576_ORIGINAL_CLUSTERED_CV_SOURCE_TYPES.csv"
    columns=("world","predictor","true_p",
      "original_six_independent_group_latents",
      "original_complete_source_probability",
      "original_twelve_row_groups","original_twelve_row_outcomes",
      "loor_row_predictions","loor_row_squared_losses","loor_average_brier",
      "logo_row_predictions","logo_row_squared_losses","logo_average_brier")
    with source_path.open("w",encoding="utf-8",newline="") as handle:
        wr=csv.DictWriter(handle,fieldnames=columns,lineterminator="\n")
        wr.writeheader()
        for p,model in WORLDS:
            for row in source_rows(p,model):
                wr.writerow({key:str(row[key]) for key in columns})
    results=dict(research_id="R269",original_catalogue_id="11-029",
       prescore_freeze_commit=FREEZE,
       scope="ARTIFICIAL_E1_EXACT_SIX_INDEPENDENT_GROUPS_TWELVE_CORRELATED_ROWS",
       world_count=9,source_types=576,distinct_group_latent_sequences_per_true_p=64,
       independent_latent_groups_per_source=6,observed_repeated_rows_per_source=12,
       row_leave_one_out_folds_per_source=12,
       leave_one_group_out_folds_per_source=6,
       each_observation_scored_once_each_protocol=True,
       all_nine_independent_Binomial5_Bernoulli1_expected_scores_verified=True,
       no_genuine_human_out_of_sample_evidence=True,
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[dict(world=label(p,m),true_p=str(p),predictor=m,
          complete_original_source_types=64,
          expected_LOOR_Brier=str(exact_source_expectation(p,m)["LOOR"]),
          expected_LOGO_Brier=str(exact_source_expectation(p,m)["LOGO"]),
          source_enumeration_equals_independent_analytic=True)
          for p,m in WORLDS])
    result_path=HERE/"R269_EXACT_RESULTS.json"
    result_path.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R269",prescore_freeze_commit=FREEZE,
       complete_source_types=576,independent_expected_score_worlds=9,
       source_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(result_path.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R269_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_locked(self):self.assertTrue(locked_claims())
    def test_world_count(self):self.assertEqual(len(WORLDS),9)
    def test_original_sources(self):self.assertEqual(len(BITS),64)
    def test_row_count(self):self.assertEqual(len(make_rows((1,)*6)),12)
    def test_loor_train(self):self.assertEqual(len(fold_indices(0,"LOOR")[0]),11)
    def test_logo_train(self):self.assertEqual(len(fold_indices(0,"LOGO")[0]),10)
    def test_fold_groups_disjoint(self):
        tr,te=fold_indices(1,"LOGO")
        self.assertTrue(set(i//2 for i in tr).isdisjoint(i//2 for i in te))
    def test_loor_leaks_mate(self):
        tr,te=fold_indices(0,"LOOR")
        self.assertIn(1,tr)
    def test_unknown_world(self):
        with self.assertRaises(ValueError):list(source_rows(F(1,3),"GLOBAL_LAPLACE"))
    def test_unknown_model(self):
        with self.assertRaises(ValueError):fitted_predictor("INVALID",(),0)
    def test_bad_fold(self):
        with self.assertRaises(ValueError):fold_indices(0,"FAKE")

def world_case(p,model,kind):
    def test(self):
        rows=tuple(source_rows(p,model))
        theory=independent_binomial_theory(p,model)
        if kind=="mass":
            self.assertEqual(sum((r["original_complete_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="unique":
            self.assertEqual(len({r["original_six_independent_group_latents"] for r in rows}),64)
        elif kind=="number":
            self.assertEqual(len(rows),64)
        elif kind=="mean":
            self.assertEqual(exact_source_expectation(p,model),theory)
        elif kind=="loss":
            for r in rows:
                for protocol in ("loor","logo"):
                    vals=[F(z) for z in r[protocol+"_row_squared_losses"].split(";")]
                    self.assertEqual(sum(vals,ZERO)/12,r[protocol+"_average_brier"])
        elif kind=="predictions":
            for r in rows:
                for proto in ("loor","logo"):
                    vals=[F(v) for v in r[proto+"_row_predictions"].split(";")]
                    self.assertEqual(len(vals),12)
                    self.assertTrue(all(0<=q<=1 for q in vals))
        elif kind=="group_split":
            for i in range(12):
                tr,te=fold_indices(i,"LOGO")
                self.assertTrue(set(j//2 for j in tr).isdisjoint(j//2 for j in te))
        elif kind=="row_split":
            for i in range(12):
                tr,te=fold_indices(i,"LOOR")
                self.assertIn(i^1,tr)
                self.assertNotIn(i,tr)
        else:raise AssertionError("invalid frozen unittest")
    return test

for p,model in WORLDS:
    for kind in ("mass","unique","number","mean","loss","predictions","group_split","row_split"):
        setattr(Tests,"test_"+str(p).replace("/","of")+"_"+model.lower()+"_"+kind,
                world_case(p,model,kind))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    grp=ap.add_mutually_exclusive_group(required=True)
    grp.add_argument("--test",action="store_true")
    grp.add_argument("--emit",action="store_true")
    a=ap.parse_args()
    if a.test:unittest.main(argv=["r269"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
