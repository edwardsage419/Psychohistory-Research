#!/usr/bin/env python3
"""R235 exact finite DIF: distinguish ability mix, anchor contamination, uniform
and nonuniform focal-item functioning from a single MH common odds ratio.

All nine models, their group ability priors and item parameters are frozen
before source generation. Only observable group/response columns feed the
MH matching statistic; oracle comparisons condition on the artificial k.
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
ZERO=F(0)
ONE=F(1)
K=(-1,0,1)
GS=(0,1)
PATTERNS=tuple(itertools.product((0,1),repeat=3))
FREEZE="b71bff10ce9e21affd0a7619fa9c7fd72551e080"
WORLD_OVERRIDES={
 "BASE_NO_DIF":{},
 "ABILITY_MIX_NO_DIF":{"mix":True},
 "UNIFORM_FOCAL_HARDER":{"focal_b_shift":1},
 "UNIFORM_FOCAL_EASIER":{"focal_b_shift":-1},
 "NONUNIFORM_FOCAL_DISCRIMINATION":{"focal_a_group1":2},
 "ANCHOR_ITEM1_DRIFT":{"anchor1_b_shift":1},
 "ANCHOR_ITEM3_DRIFT":{"anchor3_b_shift":1},
 "GLOBAL_REANCHOR_ALIAS":{"all_b_shift":1,"theta_shift":1},
 "COMPOSITION_PLUS_TRUE_DIF":{"mix":True,"focal_b_shift":1}
}

def config(world):
    if world not in WORLD_OVERRIDES: raise ValueError("world not in prescore frozen list")
    return WORLD_OVERRIDES[world]

def logit2(k):
    if not isinstance(k,int):raise ValueError("rational-grid logit needs integer exponent")
    t=F(2)**k
    return t/(1+t)

def prior(world,g):
    c=config(world)
    return (F(1,6),F(1,3),F(1,2)) if g==1 and c.get("mix") else (F(1,3),)*3

def item_parameters(world,g):
    c=config(world)
    if g not in GS:raise ValueError("unknown group")
    a=(1,1,1)
    b=(-1,0,1)
    if g==1:
        a=(1,c.get("focal_a_group1",1),1)
        offset=c.get("all_b_shift",0)
        b=(b[0]+c.get("anchor1_b_shift",0)+offset,
           b[1]+c.get("focal_b_shift",0)+offset,
           b[2]+c.get("anchor3_b_shift",0)+offset)
    return a,b

def item_probabilities(world,g,k):
    if k not in K or g not in GS:raise ValueError("unknown group or ability")
    c=config(world)
    theta=k+(c.get("theta_shift",0) if g==1 else 0)
    a,b=item_parameters(world,g)
    return tuple(logit2(a[j]*(theta-b[j])) for j in range(3))

def pattern_probability(world,g,k,pat):
    if pat not in PATTERNS:raise ValueError("not a full three item response")
    pp=item_probabilities(world,g,k)
    p=ONE
    for y,q in zip(pat,pp):
        p*=q if y==1 else ONE-q
    return p

def source_rows(world):
    cfg=config(world)
    del cfg
    out=[]
    for g in GS:
        for k in K:
            grp_prior=prior(world,g)[k+1]
            ps=item_probabilities(world,g,k)
            for pat in PATTERNS:
                conditional=pattern_probability(world,g,k,pat)
                r=dict(world=world,
                    observed_group_G=g,oracle_latent_ability_index_k=k,
                    oracle_numeric_theta=k+(config(world).get("theta_shift",0) if g==1 else 0),
                    observed_Y1=pat[0],observed_Y2=pat[1],observed_Y3=pat[2],
                    observed_anchor_score=pat[0]+pat[2],
                    original_group_prior=F(1,2),
                    original_conditional_ability_probability=grp_prior,
                    oracle_item1_probability=ps[0],oracle_focal_item2_probability=ps[1],
                    oracle_item3_probability=ps[2],
                    conditional_response_pattern_probability=conditional,
                    original_source_probability=F(1,2)*grp_prior*conditional)
                out.append(r)
    if len(out)!=48 or sum((x["original_source_probability"] for x in out),ZERO)!=ONE:
        raise AssertionError("incomplete frozen DIF source mass")
    return tuple(out)

def observed_joint(world):
    """Group and three item pattern are the ONLY observable columns."""
    d=defaultdict(F)
    for r in source_rows(world):
        k=(r["observed_group_G"],r["observed_Y1"],r["observed_Y2"],r["observed_Y3"])
        d[k]+=r["original_source_probability"]
    return dict(sorted(d.items()))

def independent_observed_joint(world):
    """Integrate latent k directly using independent item Bernoulli formulae."""
    d={}
    for g in GS:
        for y in PATTERNS:
            d[(g,)+y]=F(1,2)*sum((prior(world,g)[k+1]*
                          pattern_probability(world,g,k,y) for k in K),ZERO)
    return d

def observable_group_focal_rates(world):
    d=observed_joint(world)
    return tuple(sum((p for (group,a,focal,c),p in d.items()
                      if group==g and focal==1),ZERO)/F(1,2) for g in GS)

def oracle_ability_conditional_focal_difference(world):
    return tuple(item_probabilities(world,1,k)[1]-item_probabilities(world,0,k)[1] for k in K)

def observed_anchor_strata(world):
    tables={}
    for s in (0,1,2):
        t={(g,y):ZERO for g in GS for y in (0,1)}
        for (g,a,y,c),p in observed_joint(world).items():
            if a+c==s:
                t[g,y]+=p
        if any(v<=0 for v in t.values()):
            raise AssertionError("unsupported frozen MH stratum")
        tables[s]=t
    return tables

def observed_MH_odds_and_anchor_differences(world):
    """MH OR comparing group1 vs group0, stratified on Y1+Y3 only.

    No oracle k or IRT item parameter is inspected.
    """
    tables=observed_anchor_strata(world)
    num=ZERO
    den=ZERO
    conditional_dif=[]
    for s in (0,1,2):
        t=tables[s]
        A=t[1,1]; B=t[1,0]; C=t[0,1]; D=t[0,0]
        n=A+B+C+D
        num+=A*D/n
        den+=B*C/n
        conditional_dif.append(A/(A+B)-C/(C+D))
    if den<=0:raise AssertionError("MH denominator unsupported")
    return num/den,tuple(conditional_dif)

def world_result(world):
    rs=source_rows(world)
    if observed_joint(world)!=independent_observed_joint(world):
        raise AssertionError("independent latent ability marginal route disagrees")
    rates=observable_group_focal_rates(world)
    ability=oracle_ability_conditional_focal_difference(world)
    mh,strata=observed_MH_odds_and_anchor_differences(world)
    if world=="BASE_NO_DIF":
        assert rates==(F(1,2),F(1,2)) and mh==ONE and ability==(ZERO,ZERO,ZERO)
    if world=="ABILITY_MIX_NO_DIF":
        assert rates==(F(1,2),F(5,9))
        assert ability==(ZERO,ZERO,ZERO) and mh>ONE
    if world=="UNIFORM_FOCAL_HARDER":
        assert all(v<0 for v in ability) and mh<ONE
    if world=="UNIFORM_FOCAL_EASIER":
        assert all(v>0 for v in ability) and mh>ONE
    if world=="NONUNIFORM_FOCAL_DISCRIMINATION":
        assert ability[0]<0 and ability[1]==0 and ability[2]>0
        assert rates==(F(1,2),F(1,2)) and mh==ONE
        assert strata[0]<0 and strata[1]==0 and strata[2]>0
    if world in ("ANCHOR_ITEM1_DRIFT","ANCHOR_ITEM3_DRIFT"):
        assert ability==(ZERO,ZERO,ZERO) and mh>ONE and rates==(F(1,2),F(1,2))
    if world=="GLOBAL_REANCHOR_ALIAS":
        assert rates==(F(1,2),F(1,2)) and ability==(ZERO,ZERO,ZERO) and mh==ONE
    if world=="COMPOSITION_PLUS_TRUE_DIF":
        assert all(v<0 for v in ability) and mh<ONE
    raw_grp_b=item_parameters(world,1)[1]
    raw_grp_a=item_parameters(world,1)[0]
    return {
        "world":world,
        "full_original_response_structure_source_atoms":48,
        "full_source_probability_mass":"1",
        "observable_focal_success_rates_by_group":[str(v) for v in rates],
        "observable_group1_minus_group0_focal_success_rate":str(rates[1]-rates[0]),
        "observable_matching_anchor_score":"observed_Y1 + observed_Y3",
        "observable_mantel_haenszel_common_odds_ratio_group1_vs_group0":str(mh),
        "observable_focal_success_differences_by_anchor_score":[str(v) for v in strata],
        "oracle_fixed_ability_group1_minus_group0_focal_probabilities":[str(v) for v in ability],
        "oracle_raw_group1_item_difficulties":list(raw_grp_b),
        "oracle_raw_group1_item_discriminations":list(raw_grp_a),
        "oracle_group1_numeric_ability_origin_shift":config(world).get("theta_shift",0),
        "full_observed_group_three_item_joint_signature":{
            "".join(map(str,k)):str(v) for k,v in observed_joint(world).items()
        }
    }

def generate():
    all_worlds=[world_result(w) for w in WORLD_OVERRIDES]
    if observed_joint("BASE_NO_DIF")!=observed_joint("GLOBAL_REANCHOR_ALIAS"):
        raise AssertionError("global raw IRT scale origin is not observably equivalent")
    for g in GS:
        for k in K:
            for p in PATTERNS:
                if pattern_probability("BASE_NO_DIF",g,k,p)!=pattern_probability("GLOBAL_REANCHOR_ALIAS",g,k,p):
                    raise AssertionError("global anchoring fails ability-index conditional equivalence")
    result=dict(research_id="R235",original_catalogue_id="10-009",
        prescore_freeze_commit=FREEZE,
        scientific_scope="FINITE_ARTIFICIAL_E1_DIF_MH_AND_ANCHOR_CONTAMINATION",
        nine_worlds=9,full_original_response_structure_atoms=432,
        finite_nonuniform_DIF_with_MH_exact_null=True,
        finite_no_DIF_with_ability_mix_or_anchor_contamination_MH_false_positive=True,
        coordinate_reanchoring_full_observation_alias=True,
        new_real_human_E2=0,new_real_historical_E3=0,
        R073="FROZEN",PESEN_v0_1="FROZEN",world_results=all_worlds)
    src=HERE/"R235_ALL_432_ORIGINAL_DIF_ITEM_RESPONSE_SOURCES.csv"
    sample=source_rows("BASE_NO_DIF")[0]
    fields=list(sample)
    with src.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        writer.writeheader()
        for w in WORLD_OVERRIDES:
            for row in source_rows(w):
                writer.writerow({k:str(row[k]) for k in fields})
    rpath=HERE/"R235_EXACT_RESULTS.json"
    rpath.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(
        research_id="R235",original_catalogue_id="10-009",
        frozen_worlds=9,complete_original_structural_response_rows=432,
        independent_ability_marginal_observation_route=True,
        exact_MH_common_odds_by_nonfocal_anchor_score=True,
        nonuniform_MH_cancellation_and_false_positives=True,
        source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(rpath.read_bytes()).hexdigest(),
        new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R235_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLD_OVERRIDES),9)
    def test_count(self):self.assertEqual(sum(len(source_rows(w)) for w in WORLD_OVERRIDES),432)
    def test_base(self):self.assertEqual(observed_MH_odds_and_anchor_differences("BASE_NO_DIF")[0],ONE)
    def test_ability_mix_no_focal_dif(self):
        self.assertEqual(oracle_ability_conditional_focal_difference("ABILITY_MIX_NO_DIF"),(ZERO,ZERO,ZERO))
        self.assertGreater(observed_MH_odds_and_anchor_differences("ABILITY_MIX_NO_DIF")[0],ONE)
    def test_ability_mix_rate(self):
        self.assertEqual(observable_group_focal_rates("ABILITY_MIX_NO_DIF"),(F(1,2),F(5,9)))
    def test_nonuniform_cancellation(self):
        a=world_result("NONUNIFORM_FOCAL_DISCRIMINATION")
        self.assertEqual(a["observable_mantel_haenszel_common_odds_ratio_group1_vs_group0"],"1")
        self.assertEqual(a["observable_focal_success_rates_by_group"],["1/2","1/2"])
        self.assertEqual(a["oracle_fixed_ability_group1_minus_group0_focal_probabilities"],["-2/15","0","2/15"])
    def test_nonuniform_sign_with_anchor(self):
        dif=observed_MH_odds_and_anchor_differences("NONUNIFORM_FOCAL_DISCRIMINATION")[1]
        self.assertEqual(dif,(F(-18,325),ZERO,F(18,325)))
    def test_uniform_harder(self):self.assertLess(observed_MH_odds_and_anchor_differences("UNIFORM_FOCAL_HARDER")[0],ONE)
    def test_uniform_easier(self):self.assertGreater(observed_MH_odds_and_anchor_differences("UNIFORM_FOCAL_EASIER")[0],ONE)
    def test_anchor1_false_positive(self):
        self.assertEqual(oracle_ability_conditional_focal_difference("ANCHOR_ITEM1_DRIFT"),(ZERO,ZERO,ZERO))
        self.assertGreater(observed_MH_odds_and_anchor_differences("ANCHOR_ITEM1_DRIFT")[0],ONE)
    def test_anchor3_false_positive(self):
        self.assertEqual(oracle_ability_conditional_focal_difference("ANCHOR_ITEM3_DRIFT"),(ZERO,ZERO,ZERO))
        self.assertGreater(observed_MH_odds_and_anchor_differences("ANCHOR_ITEM3_DRIFT")[0],ONE)
    def test_global_reanchor(self):
        self.assertEqual(observed_joint("BASE_NO_DIF"),observed_joint("GLOBAL_REANCHOR_ALIAS"))
    def test_true_dif_plus_mix(self):
        self.assertTrue(all(x<0 for x in oracle_ability_conditional_focal_difference("COMPOSITION_PLUS_TRUE_DIF")))
    def test_invalid(self):
        with self.assertRaises(ValueError):source_rows("not-frozen")

def _case(world,kind):
    def test(self):
        rows=source_rows(world)
        if kind=="mass":
            self.assertEqual(sum((r["original_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="structure":
            self.assertEqual(len({(r["observed_group_G"],r["oracle_latent_ability_index_k"],
                                   r["observed_Y1"],r["observed_Y2"],r["observed_Y3"]) for r in rows}),48)
        elif kind=="positive":
            self.assertTrue(all(r["original_source_probability"]>0 for r in rows))
        elif kind=="marginal":
            self.assertEqual(observed_joint(world),independent_observed_joint(world))
        elif kind=="mh":
            self.assertGreater(observed_MH_odds_and_anchor_differences(world)[0],ZERO)
        elif kind=="three_strata":
            self.assertEqual(len(observed_anchor_strata(world)),3)
        elif kind=="summary":
            self.assertEqual(world_result(world)["full_original_response_structure_source_atoms"],48)
        else:raise AssertionError("unfrozen test")
    return test
for _w in WORLD_OVERRIDES:
    for _kind in ("mass","structure","positive","marginal","mh","three_strata","summary"):
        setattr(Tests,f"test_{_w.lower()}_{_kind}",_case(_w,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    arg=p.parse_args()
    if arg.test:unittest.main(argv=["r235"],verbosity=2)
    else:print(json.dumps(generate(),indent=2))
