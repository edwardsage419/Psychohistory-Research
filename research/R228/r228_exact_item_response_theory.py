#!/usr/bin/env python3
"""R228: finite exact Rasch, 2PL, item DIF and local independence audit.

Eight frozen three-item binary response worlds with rational base-2 logistic
probabilities. All 384 complete artificial latent/observed source atoms are
permanently archived by GitHub Actions; no human E2 evidence is asserted.
Fourth-item predictive Brier risk is evaluated on an independent oracle item
using only the observed response pattern or observed total score and group.

Run:
 python research/R228/r228_exact_item_response_theory.py --test
 python research/R228/r228_exact_item_response_theory.py --emit
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
Z=F(0); ONE=F(1)
KS=(-1,0,1)
GS=(0,1)
PATTERNS=tuple(itertools.product((0,1),repeat=3))
FROZEN_COMMIT="ed9aa23bfb634beb9dbf1aa1efb1cbb6ab4711da"
WORLD_CONFIGS={
 "BASE_RASCH":dict(theta=(-1,0,1),a=(1,1,1),b0=(-1,0,1),b1=(-1,0,1),clone=False),
 "LOCATION_SHIFT_ALIAS":dict(theta=(0,1,2),a=(1,1,1),b0=(0,1,2),b1=(0,1,2),clone=False),
 "TWO_PARAMETER_UNEQUAL":dict(theta=(-1,0,1),a=(1,2,1),b0=(-1,0,1),b1=(-1,0,1),clone=False),
 "DIF_SECOND_ITEM":dict(theta=(-1,0,1),a=(1,1,1),b0=(-1,0,1),b1=(-1,1,1),clone=False),
 "EQUAL_ITEM_DIFFICULTY":dict(theta=(-1,0,1),a=(1,1,1),b0=(0,0,0),b1=(0,0,0),clone=False),
 "LOCAL_DEPENDENT_CLONE":dict(theta=(-1,0,1),a=(1,1,1),b0=(-1,0,-1),b1=(-1,0,-1),clone=True),
 "SCALE_HIGH_DISCRIM":dict(theta=(-1,0,1),a=(2,2,2),b0=(-1,0,1),b1=(-1,0,1),clone=False),
 "SCALE_LOW_DISCRIM_ALIAS":dict(theta=(-2,0,2),a=(1,1,1),b0=(-2,0,2),b1=(-2,0,2),clone=False),
}
RASCH_WORLDS=(
 "BASE_RASCH","LOCATION_SHIFT_ALIAS","DIF_SECOND_ITEM",
 "EQUAL_ITEM_DIFFICULTY","SCALE_HIGH_DISCRIM","SCALE_LOW_DISCRIM_ALIAS"
)
ALIASES=(
 ("BASE_RASCH","LOCATION_SHIFT_ALIAS"),
 ("SCALE_HIGH_DISCRIM","SCALE_LOW_DISCRIM_ALIAS")
)

def config(world):
    if world not in WORLD_CONFIGS: raise ValueError("unknown frozen IRT world")
    return WORLD_CONFIGS[world]

def logistic_base2(exponent):
    if not isinstance(exponent,int): raise ValueError("only frozen integer logits allowed")
    odds=F(2)**exponent
    return odds/(1+odds)

def probabilities(world,k,g):
    c=config(world)
    if k not in KS or g not in GS: raise ValueError("bad fixed ability or group")
    th=c["theta"][k+1]
    bs=c["b0"] if g==0 else c["b1"]
    return tuple(logistic_base2(c["a"][j]*(th-bs[j])) for j in range(3))

def likelihood(world,k,g,pattern):
    if pattern not in PATTERNS: raise ValueError("not a frozen three item pattern")
    ps=probabilities(world,k,g)
    if config(world)["clone"]:
        if pattern[2]!=pattern[0]: return Z
        return (ps[0] if pattern[0] else ONE-ps[0]) * (
            ps[1] if pattern[1] else ONE-ps[1])
    p=ONE
    for y,pr in zip(pattern,ps):
        p*=pr if y else ONE-pr
    return p

def source_rows(world):
    r=[]
    for g in GS:
        for k in KS:
            probs=probabilities(world,k,g)
            for y in PATTERNS:
                pp=likelihood(world,k,g,y)
                r.append(dict(world=world,observed_group_G=g,latent_index_k=k,
                              oracle_theta=config(world)["theta"][k+1],
                              observed_Y1=y[0],observed_Y2=y[1],observed_Y3=y[2],
                              observed_total_score=sum(y),
                              source_probability=F(1,6)*pp,
                              pattern_conditional_probability=pp,
                              oracle_item_prob_1=probs[0],
                              oracle_item_prob_2=probs[1],
                              oracle_item_prob_3=probs[2],
                              structural_zero_probability=int(pp==0)))
    assert len(r)==48 and sum((a["source_probability"] for a in r),Z)==ONE
    return tuple(r)

def observation_signature(world):
    """Only G and item response pattern; no hidden k,theta or oracle column."""
    d=defaultdict(F)
    for r in source_rows(world):
        key=(r["observed_group_G"],r["observed_Y1"],r["observed_Y2"],r["observed_Y3"])
        d[key]+=r["source_probability"]
    return dict(sorted(d.items()))

def condition_total_pattern(world,k,g,score):
    numerator={y:likelihood(world,k,g,y) for y in PATTERNS if sum(y)==score}
    mass=sum(numerator.values(),Z)
    if mass<=0: raise AssertionError("zero score support under frozen model")
    return {y:v/mass for y,v in numerator.items()}

def score_sufficiency_violations(world):
    count=0
    for g in GS:
        for s in range(4):
            by_theta=[condition_total_pattern(world,k,g,s) for k in KS]
            for y in (yy for yy in PATTERNS if sum(yy)==s):
                if len({d[y] for d in by_theta})>1:
                    count+=1
    return count

def independent_rasch_conditional(world,g,s):
    """Rasch conditional form cancels ability, independently of all source rows."""
    c=config(world)
    if c["clone"] or len(set(c["a"]))!=1:
        return None
    b=c["b0"] if g==0 else c["b1"]
    common=c["a"][0]
    terms={}
    for pat in PATTERNS:
        if sum(pat)==s:
            # Score-conditioned response odds relative to all-zero event.
            terms[pat]=F(2)**(-common*sum(b[j]*pat[j] for j in range(3)))
    den=sum(terms.values(),Z)
    return {y:v/den for y,v in terms.items()}

def conditional_dependency(world,k,g):
    d={y:likelihood(world,k,g,y) for y in PATTERNS}
    e1=sum((p for y,p in d.items() if y[0]==1),Z)
    e3=sum((p for y,p in d.items() if y[2]==1),Z)
    e13=sum((p for y,p in d.items() if y[0]==1 and y[2]==1),Z)
    return e13-e1*e3

def fourth_item_probability(k):
    # The real independent fourth item is anchored to fixed latent index k,
    # even if the first three items are shifted or rescaled.
    if k not in KS: raise ValueError("bad true ability index")
    return logistic_base2(k)

def posterior_item_prob(world,g,y,source_type):
    if source_type not in ("full","score"): raise ValueError("bad predictor")
    if y not in PATTERNS or g not in GS: raise ValueError("bad observation")
    if source_type=="full":
        weights={k:likelihood(world,k,g,y) for k in KS}
    else:
        s=sum(y)
        weights={k:sum((likelihood(world,k,g,z) for z in PATTERNS if sum(z)==s),Z) for k in KS}
    mass=sum(weights.values(),Z)
    if mass<=0: return None
    return sum((weights[k]*fourth_item_probability(k) for k in KS),Z)/mass

def prediction_risk(world):
    risks={}
    for kind in ("full","score"):
        direct=Z
        independent=Z
        for g in GS:
            for k in KS:
                q=fourth_item_probability(k)
                for y in PATTERNS:
                    p_source=likelihood(world,k,g,y)/6
                    if p_source==0: continue
                    predicted=posterior_item_prob(world,g,y,kind)
                    assert predicted is not None
                    # Two-point independent held-out future response source.
                    direct+=p_source*(q*(1-predicted)**2+(1-q)*predicted**2)
                    # Independent conditional variance decomposition.
                    independent+=p_source*(q*(1-q)+(q-predicted)**2)
        if direct!=independent: raise AssertionError("two independent Brier risk routes diverged")
        risks[kind]=direct
    improvement=risks["score"]-risks["full"]
    if improvement<0: raise AssertionError("using more available information worsened Bayes risk")
    if world in RASCH_WORLDS and improvement!=0:
        raise AssertionError("Rasch full pattern should be score sufficient")
    if world=="TWO_PARAMETER_UNEQUAL" and improvement<=0:
        raise AssertionError("unequal discrimination must add pattern information")
    return risks["full"],risks["score"],improvement

def world_summary(world):
    rows=source_rows(world)
    suf=score_sufficiency_violations(world)
    if world in RASCH_WORLDS:
        if suf!=0: raise AssertionError("Rasch response conditioned on score depends on theta")
        for g in GS:
            for s in range(4):
                expected=independent_rasch_conditional(world,g,s)
                for k in KS:
                    if condition_total_pattern(world,k,g,s)!=expected:
                        raise AssertionError("independent Rasch conditional odds disagree")
    if world=="TWO_PARAMETER_UNEQUAL" and suf==0:
        raise AssertionError("2PL total-score sufficiency incorrectly accepted")
    deps=[conditional_dependency(world,k,g) for k in KS for g in GS]
    if world=="LOCAL_DEPENDENT_CLONE":
        if any(v<=0 for v in deps): raise AssertionError("copied third response has positive local dependence")
    elif any(v!=0 for v in deps):
        raise AssertionError("locally independent world has residual item covariance")
    g0=probabilities(world,0,0)
    g1=probabilities(world,0,1)
    if (g0[1]!=g1[1])!=(world=="DIF_SECOND_ITEM"):
        raise AssertionError("frozen item2 DIF condition mismatched")
    f,s,improve=prediction_risk(world)
    return dict(world=world,complete_structural_response_atoms=len(rows),
                actual_positive_probability_atoms=sum(r["source_probability"]>0 for r in rows),
                structural_zero_probability_atoms=sum(r["source_probability"]==0 for r in rows),
                conditional_total_score_sufficiency_violations=suf,
                conditional_item1_item3_cov_by_k_g={
                    f"k{k}_g{g}":str(conditional_dependency(world,k,g)) for k in KS for g in GS
                },
                item2_differential_functioning_by_group=g0[1]!=g1[1],
                group0_item_prob_at_k0=[str(p) for p in g0],
                group1_item_prob_at_k0=[str(p) for p in g1],
                independent_fourth_item_full_pattern_brier=str(f),
                independent_fourth_item_total_score_brier=str(s),
                total_minus_full_pattern_brier_gain=str(improve),
                observable_joint_response_group_signature={
                    "".join(map(str,k)):str(v) for k,v in observation_signature(world).items()
                })

def generate():
    out=[world_summary(w) for w in WORLD_CONFIGS]
    for a,b in ALIASES:
        if observation_signature(a)!=observation_signature(b):
            raise AssertionError("IRT reparameterization altered observed response distribution")
        for k in KS:
            for g in GS:
                for y in PATTERNS:
                    if likelihood(a,k,g,y)!=likelihood(b,k,g,y):
                        raise AssertionError("IRT alias not identical conditional on ability index")
    dataset=dict(research_id="R228",catalogue_id="10-002",
                 scientific_scope="FINITE_ARTIFICIAL_E1_ONLY",
                 prescore_freeze_commit=FROZEN_COMMIT,
                 complete_frozen_worlds=8,
                 complete_original_structural_response_atoms=384,
                 positive_probability_source_atoms=360,
                 structural_zero_probability_rows=24,
                 both_reparameterization_observation_alias_pairs_verified=True,
                 fourth_item_prediction_uses_fresh_independent_Bernoulli=True,
                 new_real_human_E2=0,new_real_historical_E3=0,
                 R073="FROZEN",PESEN_v0_1="FROZEN",world_results=out)
    sources=HERE/"R228_ALL_384_ORIGINAL_IRT_RESPONSE_ATOMS.csv"
    rows=[r for w in WORLD_CONFIGS for r in source_rows(w)]
    keys=list(rows[0])
    with sources.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=keys,lineterminator="\n")
        writer.writeheader()
        for row in rows: writer.writerow({k:str(row[k]) for k in keys})
    result=HERE/"R228_EXACT_RESULTS.json"
    result.write_text(json.dumps(dataset,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R228",original_catalogue_id="10-002",
                 frozen_worlds=8,complete_structural_source_rows=384,
                 positive_probability_source_rows=360,zero_probability_structural_rows=24,
                 independent_Rasch_conditional_formula_checks=True,
                 independent_future_Brier_equivalence_verified=True,
                 observation_alias_pairs=2,
                 original_source_sha256=hashlib.sha256(sources.read_bytes()).hexdigest(),
                 exact_results_sha256=hashlib.sha256(result.read_bytes()).hexdigest(),
                 new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R228_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_world_count(self):self.assertEqual(len(WORLD_CONFIGS),8)
    def test_atoms_count(self):self.assertEqual(sum(len(source_rows(w)) for w in WORLD_CONFIGS),384)
    def test_zero_count(self):
        self.assertEqual(sum(sum(r["source_probability"]==0 for r in source_rows(w)) for w in WORLD_CONFIGS),24)
    def test_location_alias(self):
        self.assertEqual(observation_signature("BASE_RASCH"),observation_signature("LOCATION_SHIFT_ALIAS"))
    def test_scale_alias(self):
        self.assertEqual(observation_signature("SCALE_HIGH_DISCRIM"),observation_signature("SCALE_LOW_DISCRIM_ALIAS"))
    def test_rasch_score_sufficient(self):
        for w in RASCH_WORLDS:self.assertEqual(score_sufficiency_violations(w),0)
    def test_2pl_score_insufficient(self):
        self.assertGreater(score_sufficiency_violations("TWO_PARAMETER_UNEQUAL"),0)
    def test_dif_item2(self):
        self.assertNotEqual(probabilities("DIF_SECOND_ITEM",0,0)[1],
                            probabilities("DIF_SECOND_ITEM",0,1)[1])
    def test_clone_local_dependence(self):
        self.assertGreater(conditional_dependency("LOCAL_DEPENDENT_CLONE",0,0),0)
    def test_2pl_prediction_gain(self):
        self.assertGreater(prediction_risk("TWO_PARAMETER_UNEQUAL")[2],0)
    def test_rasch_prediction_equal(self):
        for w in RASCH_WORLDS:self.assertEqual(prediction_risk(w)[2],0)
    def test_invalid_world(self):
        with self.assertRaises(ValueError):source_rows("UNKNOWN")
    def test_invalid_posterior(self):
        with self.assertRaises(ValueError):posterior_item_prob("BASE_RASCH",0,(1,1,1),"bad")

def _case(world,kind):
    def t(self):
        rows=source_rows(world)
        if kind=="mass":
            self.assertEqual(sum((r["source_probability"] for r in rows),Z),ONE)
        elif kind=="group_k_masses":
            for g in GS:
                for k in KS:
                    self.assertEqual(sum((r["source_probability"] for r in rows if r["observed_group_G"]==g and r["latent_index_k"]==k),Z),F(1,6))
        elif kind=="score":
            self.assertTrue(all(r["observed_total_score"]==r["observed_Y1"]+r["observed_Y2"]+r["observed_Y3"] for r in rows))
        elif kind=="prob":
            self.assertTrue(all(r["source_probability"]==F(1,6)*r["pattern_conditional_probability"] for r in rows))
        elif kind=="prediction":
            a,b,gain=prediction_risk(world)
            self.assertGreaterEqual(gain,Z)
            self.assertGreater(a,Z)
        elif kind=="replay":
            d=world_summary(world)
            self.assertEqual(d["complete_structural_response_atoms"],48)
        else:raise AssertionError("invalid test")
    return t
for _w in WORLD_CONFIGS:
    for _kind in ("mass","group_k_masses","score","prob","prediction","replay"):
        setattr(Tests,"test_"+_w.lower()+"_"+_kind,_case(_w,_kind))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.test:unittest.main(argv=["r228"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
