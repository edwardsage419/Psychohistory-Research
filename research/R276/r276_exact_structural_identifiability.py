#!/usr/bin/env python3
"""R276: three theta vectors sharing q=theta1*theta2=1/4.

Four Bernoulli(q) Y observations cannot distinguish any theta candidate.
Two auxiliary Bernoulli(theta1) Z observations can distinguish their joint
distributions but finite-sample MAP remains imperfect.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import unittest
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="58e192c523cc87b4fd4f6b9758af118d620a1951"
THETAS={"PARAM_A":(F(1,2),F(1,2)),
        "PARAM_B":(F(1,4),F(1)),
        "PARAM_C":(F(1),F(1,4))}
MODELS=tuple(THETAS)
ALL_BITS=tuple("".join(bits) for bits in itertools.product("01",repeat=6))
ZERO,ONE=F(0),F(1)
FROZEN_Y={"PARAM_A":ONE,"PARAM_B":ZERO,"PARAM_C":ZERO}
FROZEN_FULL={"PARAM_A":F(1,2),"PARAM_B":F(9,16),"PARAM_C":ONE}

def validate(model):
    if model not in MODELS:raise ValueError("outside frozen parameter vectors")

def split(seq):
    if len(seq)!=6 or any(x not in "01" for x in seq):
        raise ValueError("requires four Y and two Z ordered binary observations")
    return seq[:4],seq[4:]

def q(model):
    validate(model)
    theta1,theta2=THETAS[model]
    return theta1*theta2

def likelihood(model,seq,design):
    validate(model)
    y,z=split(seq)
    k=y.count("1");j=z.count("1")
    a,b=THETAS[model]
    base=q(model)**k*(ONE-q(model))**(4-k)
    if design=="OBSERVE_Y_ONLY":return base
    if design=="OBSERVE_Y_AND_Z":return base*a**j*(ONE-a)**(2-j)
    raise ValueError("unknown frozen observation design")

def model_likelihoods(seq,design):
    return tuple(likelihood(m,seq,design) for m in MODELS)

def posterior(seq,design):
    vals=model_likelihoods(seq,design)
    denom=sum(vals,ZERO)
    assert denom>ZERO
    return tuple(v/denom for v in vals)

def map_model(seq,design):
    vals=model_likelihoods(seq,design)
    best=max(vals)
    return next(m for i,m in enumerate(MODELS) if vals[i]==best)

def source_rows(model):
    """Route A complete ordered sixbit original support (including zero mass)."""
    validate(model)
    for seq in ALL_BITS:
        y,z=split(seq)
        l_y=model_likelihoods(seq,"OBSERVE_Y_ONLY")
        l_yz=model_likelihoods(seq,"OBSERVE_Y_AND_Z")
        post_y=posterior(seq,"OBSERVE_Y_ONLY")
        post_yz=posterior(seq,"OBSERVE_Y_AND_Z")
        ychoice=map_model(seq,"OBSERVE_Y_ONLY")
        yzchoice=map_model(seq,"OBSERVE_Y_AND_Z")
        yield dict(true_parameter_model=model,
          true_theta1=THETAS[model][0],true_theta2=THETAS[model][1],
          observed_q_product=q(model),
          original_complete_Y4_Z2_sixbit_source=seq,
          original_Y_fourbits=y,original_Z_twobits=z,
          original_Y_successes=y.count("1"),original_Z_successes=z.count("1"),
          complete_original_source_probability=likelihood(model,seq,"OBSERVE_Y_AND_Z"),
          Y_only_all_three_parameter_likelihoods=";".join(map(str,l_y)),
          YZ_all_three_parameter_likelihoods=";".join(map(str,l_yz)),
          Y_only_three_parameter_posteriors=";".join(map(str,post_y)),
          YZ_three_parameter_posteriors=";".join(map(str,post_yz)),
          Y_only_MAP_selection=ychoice,YZ_MAP_selection=yzchoice,
          Y_only_MAP_correct=int(ychoice==model),
          YZ_MAP_correct=int(yzchoice==model))

def original_moments(model):
    validate(model)
    rows=tuple(source_rows(model))
    assert len(rows)==64 and len({r["original_complete_Y4_Z2_sixbit_source"] for r in rows})==64
    assert sum((r["complete_original_source_probability"] for r in rows),ZERO)==ONE
    p_y=sum((r["complete_original_source_probability"]*r["Y_only_MAP_correct"] for r in rows),ZERO)
    p_yz=sum((r["complete_original_source_probability"]*r["YZ_MAP_correct"] for r in rows),ZERO)
    positive=sum(r["complete_original_source_probability"]>ZERO for r in rows)
    return p_y,p_yz,positive

def independent_analytical(model):
    """Route B only needs theta1 and category P(Z=00/mixed/11), not source rows."""
    validate(model)
    a,_=THETAS[model]
    py=ONE if model=="PARAM_A" else ZERO
    pfull={"PARAM_A":2*a*(ONE-a),
           "PARAM_B":(ONE-a)**2,
           "PARAM_C":a**2}[model]
    positive=16 if a==ONE else 64
    return py,pfull,positive

def marginal_Y_by_source(model):
    masses=defaultdict(lambda:ZERO)
    for row in source_rows(model):
        masses[row["original_Y_fourbits"]]+=row["complete_original_source_probability"]
    return dict(masses)

def independent_Y_distribution():
    p=F(1,4)
    return {"".join(bit):p**sum(map(int,bit))*(ONE-p)**(4-sum(map(int,bit)))
            for bit in itertools.product("01",repeat=4)}

def frozen_claims():
    assert len(MODELS)==3 and len(ALL_BITS)==64
    assert all(q(m)==F(1,4) for m in MODELS)
    for m in MODELS:
        assert original_moments(m)==independent_analytical(m)
        assert original_moments(m)[:2]==(FROZEN_Y[m],FROZEN_FULL[m])
        assert marginal_Y_by_source(m)==independent_Y_distribution()
    assert sum(FROZEN_Y.values(),ZERO)/3==F(1,3)
    assert sum(FROZEN_FULL.values(),ZERO)/3==F(11,16)
    for z,post in (("00",(F(4,13),F(9,13),ZERO)),
                   ("01",(F(4,7),F(3,7),ZERO)),
                   ("10",(F(4,7),F(3,7),ZERO)),
                   ("11",(F(4,21),F(1,21),F(16,21)))):
        assert posterior("0000"+z,"OBSERVE_Y_AND_Z")==post
    return True

def emit():
    frozen_claims()
    path=HERE/"R276_ALL_192_ORIGINAL_IDENTIFIABILITY_PARAMETER_SOURCES.csv"
    columns=("true_parameter_model","true_theta1","true_theta2","observed_q_product",
        "original_complete_Y4_Z2_sixbit_source","original_Y_fourbits","original_Z_twobits",
        "original_Y_successes","original_Z_successes",
        "complete_original_source_probability",
        "Y_only_all_three_parameter_likelihoods","YZ_all_three_parameter_likelihoods",
        "Y_only_three_parameter_posteriors","YZ_three_parameter_posteriors",
        "Y_only_MAP_selection","YZ_MAP_selection",
        "Y_only_MAP_correct","YZ_MAP_correct")
    with path.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=columns,lineterminator="\n")
        writer.writeheader()
        for m in MODELS:
            for row in source_rows(m):
                writer.writerow({key:str(row[key]) for key in columns})
    results=dict(research_id="R276",original_catalogue_id="12-006",
        prescore_freeze_commit=FREEZE,
        evidence_scope="E1_ARTIFICIAL_DISCRETE_PARAMETER_STRUCTURAL_IDENTIFIABILITY",
        fixed_product_q="1/4",parameter_candidates=3,
        original_complete_source_types=192,positive_probability_source_types=144,
        Y_only_full_joint_distributions_identical=True,
        augmented_YZ_joint_distributions_distinct=True,
        equal_prior_Y_only_MAP_correct_probability="1/3",
        equal_prior_YZ_MAP_correct_probability="11/16",
        all_source_enumerated_vs_independent_category_formulas_equal=True,
        no_real_human_E2=0,no_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",
        world_results=[dict(true_parameter_model=m,
          theta1=str(THETAS[m][0]),theta2=str(THETAS[m][1]),
          primitive_original_source_types=64,
          positive_probability_source_types=original_moments(m)[2],
          Y_only_MAP_correct_probability=str(original_moments(m)[0]),
          YZ_MAP_correct_probability=str(original_moments(m)[1]),
          independent_parameter_category_formula_verified=True) for m in MODELS])
    jsonpath=HERE/"R276_EXACT_RESULTS.json"
    jsonpath.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R276",prescore_freeze_commit=FREEZE,
        complete_original_source_types=192,positive_source_types=144,
        source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(jsonpath.read_bytes()).hexdigest(),
        no_real_human_E2=0,no_real_historical_E3=0)
    (HERE/"R276_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_frozen(self):self.assertTrue(frozen_claims())
    def test_model_count(self):self.assertEqual(len(MODELS),3)
    def test_source_count(self):self.assertEqual(len(MODELS)*len(ALL_BITS),192)
    def test_product(self):self.assertEqual({q(m) for m in MODELS},{F(1,4)})
    def test_partial_likelihood(self):
        self.assertEqual(model_likelihoods("101000","OBSERVE_Y_ONLY"),(F(1,4)**2*F(3,4)**2,)*3)
    def test_full_posterior_00(self):
        self.assertEqual(posterior("000000","OBSERVE_Y_AND_Z"),(F(4,13),F(9,13),ZERO))
    def test_full_posterior_11(self):
        self.assertEqual(posterior("000011","OBSERVE_Y_AND_Z"),(F(4,21),F(1,21),F(16,21)))
    def test_map_00(self):self.assertEqual(map_model("000000","OBSERVE_Y_AND_Z"),"PARAM_B")
    def test_map_11(self):self.assertEqual(map_model("000011","OBSERVE_Y_AND_Z"),"PARAM_C")
    def test_map_mix(self):self.assertEqual(map_model("000001","OBSERVE_Y_AND_Z"),"PARAM_A")
    def test_invalid_model(self):
        with self.assertRaises(ValueError):list(source_rows("NONE"))
    def test_invalid_original(self):
        with self.assertRaises(ValueError):split("0011")
    def test_unknown_design(self):
        with self.assertRaises(ValueError):posterior("000000","INVALID")
    def test_Y_marginal(self):self.assertEqual(len(independent_Y_distribution()),16)

def case(model,kind):
    def test(self):
        rows=tuple(source_rows(model))
        if kind=="count":self.assertEqual(len(rows),64)
        elif kind=="mass":self.assertEqual(sum((r["complete_original_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="support":self.assertEqual(original_moments(model)[2],16 if model=="PARAM_C" else 64)
        elif kind=="unique":self.assertEqual(len({r["original_complete_Y4_Z2_sixbit_source"] for r in rows}),64)
        elif kind=="Y_equiv":self.assertEqual(marginal_Y_by_source(model),independent_Y_distribution())
        elif kind=="analytic":self.assertEqual(original_moments(model),independent_analytical(model))
        elif kind=="Y_correct":self.assertEqual(original_moments(model)[0],FROZEN_Y[model])
        elif kind=="YZ_correct":self.assertEqual(original_moments(model)[1],FROZEN_FULL[model])
        elif kind=="posterior":
            for r in rows:
                self.assertEqual(sum((F(z) for z in r["YZ_three_parameter_posteriors"].split(";")),ZERO),ONE)
        elif kind=="fit_independence":
            for r in rows:
                self.assertEqual(r["original_complete_Y4_Z2_sixbit_source"],
                      r["original_Y_fourbits"]+r["original_Z_twobits"])
        elif kind=="choices":
            for r in rows:
                self.assertEqual(r["Y_only_MAP_correct"],int(r["Y_only_MAP_selection"]==model))
                self.assertEqual(r["YZ_MAP_correct"],int(r["YZ_MAP_selection"]==model))
        elif kind=="product":
            for r in rows:self.assertEqual(r["true_theta1"]*r["true_theta2"],F(1,4))
        else:raise AssertionError("invalid case")
    return test
for m in MODELS:
    for kind in ("count","mass","support","unique","Y_equiv","analytic","Y_correct","YZ_correct",
                 "posterior","fit_independence","choices","product"):
        setattr(Tests,"test_"+m.lower()+"_"+kind,case(m,kind))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    grp=parser.add_mutually_exclusive_group(required=True)
    grp.add_argument("--test",action="store_true")
    grp.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.test:unittest.main(argv=["r276"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
