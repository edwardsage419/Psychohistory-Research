#!/usr/bin/env python3
"""R275: exact observational equivalence and mechanism discrimination.

IID, COPY, and FLIP all generate the same joint distribution of four A bits.
Full 4x(A,B) pairing differentiates these mechanisms with finite ambiguity.
All probabilities are Fractions and zero-mass primitive sources are retained.
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
FREEZE="c29ff305375f8510137f3a50bf20005fd695768d"
MECHANISMS=("IID_PAIR","COPY_PAIR","FLIP_PAIR")
DESIGNS=("PARTIAL_A_ONLY","FULL_AB_PAIR")
ALL_SOURCE_BITS=tuple("".join(bits) for bits in itertools.product("01",repeat=8))
ZERO,ONE=F(0),F(1)
EXPECTED_PARTIAL={"IID_PAIR":ONE,"COPY_PAIR":ZERO,"FLIP_PAIR":ZERO}
EXPECTED_FULL={"IID_PAIR":F(7,8),"COPY_PAIR":ONE,"FLIP_PAIR":ONE}

def validate(model):
    if model not in MECHANISMS:raise ValueError("unfrozen mechanism")

def separate_pairs(eight):
    if len(eight)!=8 or any(z not in "01" for z in eight):
        raise ValueError("requires four ordered two-bit pairs")
    return tuple((int(eight[2*i]),int(eight[2*i+1])) for i in range(4))

def partial_projection(eight):
    return "".join(str(a) for a,b in separate_pairs(eight))

def equal_pair_count(eight):
    return sum(a==b for a,b in separate_pairs(eight))

def joint_likelihood(model,eight):
    validate(model)
    pairs=separate_pairs(eight)
    if model=="IID_PAIR":return F(1,256)
    if model=="COPY_PAIR":
        return F(1,16) if all(a==b for a,b in pairs) else ZERO
    return F(1,16) if all(a!=b for a,b in pairs) else ZERO

def likelihoods_for_design(design,eight):
    if design not in DESIGNS:raise ValueError("unfrozen design")
    separate_pairs(eight)
    if design=="PARTIAL_A_ONLY":
        return (F(1,16),)*3
    return tuple(joint_likelihood(m,eight) for m in MECHANISMS)

def posterior(design,eight):
    values=likelihoods_for_design(design,eight)
    norm=sum(values,ZERO)
    assert norm>ZERO
    return tuple(v/norm for v in values)

def classified(design,eight):
    values=likelihoods_for_design(design,eight)
    maxv=max(values)
    return next(model for i,model in enumerate(MECHANISMS) if values[i]==maxv)

def original_source_rows(model):
    """Route A: all primitive eight-bit source configurations, including zeros."""
    validate(model)
    for eight in ALL_SOURCE_BITS:
        lhs_a=likelihoods_for_design("PARTIAL_A_ONLY",eight)
        lhs_ab=likelihoods_for_design("FULL_AB_PAIR",eight)
        pa=posterior("PARTIAL_A_ONLY",eight)
        pab=posterior("FULL_AB_PAIR",eight)
        sel_a=classified("PARTIAL_A_ONLY",eight)
        sel_ab=classified("FULL_AB_PAIR",eight)
        yield dict(true_mechanism=model,
          original_full_four_pair_eightbits=eight,
          partial_observed_first_bits_only=partial_projection(eight),
          complete_pair_equal_count=equal_pair_count(eight),
          exact_true_source_mass=joint_likelihood(model,eight),
          partial_all_mechanism_likelihoods=";".join(map(str,lhs_a)),
          full_all_mechanism_likelihoods=";".join(map(str,lhs_ab)),
          partial_three_mechanism_posterior=";".join(map(str,pa)),
          full_three_mechanism_posterior=";".join(map(str,pab)),
          partial_MAP_selection=sel_a,full_MAP_selection=sel_ab,
          partial_MAP_correct=int(sel_a==model),
          full_MAP_correct=int(sel_ab==model))

def source_moments(model):
    validate(model)
    rows=tuple(original_source_rows(model))
    assert len(rows)==256
    assert len({r["original_full_four_pair_eightbits"] for r in rows})==256
    assert sum((r["exact_true_source_mass"] for r in rows),ZERO)==ONE
    partial=sum((r["exact_true_source_mass"]*r["partial_MAP_correct"] for r in rows),ZERO)
    full=sum((r["exact_true_source_mass"]*r["full_MAP_correct"] for r in rows),ZERO)
    positives=sum(r["exact_true_source_mass"]>ZERO for r in rows)
    return partial,full,positives

def independent_probabilistic_theory(model):
    """Route B: mechanism support logic, no 8-bit source enumeration."""
    validate(model)
    if model=="IID_PAIR":
        return ONE, ONE-2*(F(1,2)**4),256
    return ZERO,ONE,16

def analytic_partial_marginals():
    """One direct latent-A route, distinct from ordered AB source generation."""
    return {''.join(bits):F(1,16) for bits in itertools.product("01",repeat=4)}

def exhaustive_partial_marginals(model):
    masses=defaultdict(lambda:ZERO)
    for r in original_source_rows(model):
        masses[r["partial_observed_first_bits_only"]]+=r["exact_true_source_mass"]
    return dict(masses)

def frozen_claims():
    assert len(ALL_SOURCE_BITS)==256 and len(MECHANISMS)==3
    assert 3*len(ALL_SOURCE_BITS)==768
    theory=analytic_partial_marginals()
    for model in MECHANISMS:
        r=source_moments(model)
        assert r==independent_probabilistic_theory(model)
        assert r[:2]==(EXPECTED_PARTIAL[model],EXPECTED_FULL[model])
        assert exhaustive_partial_marginals(model)==theory
    assert sum((EXPECTED_FULL[m] for m in MECHANISMS),ZERO)/3==F(23,24)
    assert sum((EXPECTED_PARTIAL[m] for m in MECHANISMS),ZERO)/3==F(1,3)
    assert posterior("FULL_AB_PAIR","00000000")==(F(1,17),F(16,17),ZERO)
    assert posterior("FULL_AB_PAIR","01010101")==(F(1,17),ZERO,F(16,17))
    assert posterior("FULL_AB_PAIR","00000101")==(ONE,ZERO,ZERO)
    return True

def emit():
    frozen_claims()
    source_path=HERE/"R275_ALL_768_ORIGINAL_EQUIFINALITY_PAIR_SOURCES.csv"
    cols=("true_mechanism","original_full_four_pair_eightbits",
          "partial_observed_first_bits_only","complete_pair_equal_count",
          "exact_true_source_mass",
          "partial_all_mechanism_likelihoods",
          "full_all_mechanism_likelihoods",
          "partial_three_mechanism_posterior",
          "full_three_mechanism_posterior",
          "partial_MAP_selection","full_MAP_selection",
          "partial_MAP_correct","full_MAP_correct")
    with source_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        w.writeheader()
        for model in MECHANISMS:
            for row in original_source_rows(model):
                w.writerow({key:str(row[key]) for key in cols})
    report=dict(research_id="R275",original_catalogue_id="12-005",
      prescore_freeze_commit=FREEZE,
      research_scope="E1_FINITE_ARTIFICIAL_OBSERVATIONAL_EQUIFINALITY_VS_PAIR_DISCRIMINATION",
      mechanism_count=3,original_complete_source_types=768,
      primitive_eightbit_sources_per_mechanism=256,
      positive_probability_configurations_across_worlds=288,
      observed_partial_A_fourbit_sequences=16,
      full_pair_observation_length=8,
      all_three_full_A_joint_distributions_equal=True,
      prior_equal_mechanism_probability=str(F(1,3)),
      average_partial_MAP_correct_probability=str(F(1,3)),
      average_full_pair_MAP_correct_probability=str(F(23,24)),
      original_full_and_independent_support_math_identical=True,
      new_real_human_E2=0,new_real_historical_E3=0,
      R073="FROZEN",PESEN_v0_1="FROZEN",
      world_results=[dict(true_mechanism=m,
         exact_original_source_count=256,
         positive_probability_original_source_count=source_moments(m)[2],
         partial_A_only_MAP_correct_probability=str(source_moments(m)[0]),
         full_AB_pair_MAP_correct_probability=str(source_moments(m)[1]),
         independent_support_combinatorics_match=True)
         for m in MECHANISMS])
    result_path=HERE/"R275_EXACT_EQUIFINALITY_RESULTS.json"
    result_path.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R275",prescore_freeze_commit=FREEZE,
       original_complete_source_types=768,source_support_nonzero=288,
       source_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(result_path.read_bytes()).hexdigest(),
       no_real_human_E2=0,no_real_historical_E3=0)
    (HERE/"R275_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_frozen(self):self.assertTrue(frozen_claims())
    def test_models(self):self.assertEqual(len(MECHANISMS),3)
    def test_all_atoms(self):self.assertEqual(len(ALL_SOURCE_BITS),256)
    def test_partial_likelihood(self):self.assertEqual(likelihoods_for_design("PARTIAL_A_ONLY","10101101"),(F(1,16),)*3)
    def test_full_copy(self):self.assertEqual(likelihoods_for_design("FULL_AB_PAIR","00000000"),(F(1,256),F(1,16),ZERO))
    def test_full_flip(self):self.assertEqual(likelihoods_for_design("FULL_AB_PAIR","01010101"),(F(1,256),ZERO,F(1,16)))
    def test_full_mixed(self):self.assertEqual(likelihoods_for_design("FULL_AB_PAIR","00000101"),(F(1,256),ZERO,ZERO))
    def test_partial_class(self):self.assertEqual(classified("PARTIAL_A_ONLY","11111111"),"IID_PAIR")
    def test_average_full(self):self.assertEqual(sum(EXPECTED_FULL.values(),ZERO)/3,F(23,24))
    def test_invalid_model(self):
        with self.assertRaises(ValueError):list(original_source_rows("INVALID"))
    def test_invalid_source(self):
        with self.assertRaises(ValueError):separate_pairs("0101")
    def test_invalid_design(self):
        with self.assertRaises(ValueError):posterior("INVALID","01010101")
    def test_full_marginal_count(self):self.assertEqual(len(analytic_partial_marginals()),16)
    def test_edge_posteriors(self):self.assertEqual(posterior("FULL_AB_PAIR","00000000")[1],F(16,17))

def _case(model,kind):
    def test(self):
        rows=tuple(original_source_rows(model))
        if kind=="count":self.assertEqual(len(rows),256)
        elif kind=="mass":self.assertEqual(sum((r["exact_true_source_mass"] for r in rows),ZERO),ONE)
        elif kind=="unique":self.assertEqual(len({r["original_full_four_pair_eightbits"] for r in rows}),256)
        elif kind=="positive":self.assertEqual(source_moments(model)[2],256 if model=="IID_PAIR" else 16)
        elif kind=="partial":self.assertEqual(source_moments(model)[0],EXPECTED_PARTIAL[model])
        elif kind=="full":self.assertEqual(source_moments(model)[1],EXPECTED_FULL[model])
        elif kind=="marginals":self.assertEqual(exhaustive_partial_marginals(model),analytic_partial_marginals())
        elif kind=="analytic":self.assertEqual(source_moments(model),independent_probabilistic_theory(model))
        elif kind=="posterior":
            for r in rows:
                self.assertEqual(sum((F(q) for q in r["full_three_mechanism_posterior"].split(";")),ZERO),ONE)
        elif kind=="partialposterior":
            for r in rows:self.assertEqual(r["partial_three_mechanism_posterior"],"1/3;1/3;1/3")
        elif kind=="decisions":
            for r in rows:
                self.assertEqual(r["partial_MAP_correct"],int(r["partial_MAP_selection"]==model))
                self.assertEqual(r["full_MAP_correct"],int(r["full_MAP_selection"]==model))
        elif kind=="pairs":
            for r in rows:self.assertEqual(r["complete_pair_equal_count"],equal_pair_count(r["original_full_four_pair_eightbits"]))
        else:raise AssertionError("invalid test")
    return test
for model in MECHANISMS:
    for kind in ("count","mass","unique","positive","partial","full","marginals","analytic",
                 "posterior","partialposterior","decisions","pairs"):
        setattr(Tests,"test_"+model.lower()+"_"+kind,_case(model,kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    opts=p.parse_args()
    if opts.test:unittest.main(argv=["r275"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
