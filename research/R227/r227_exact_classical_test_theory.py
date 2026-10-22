#!/usr/bin/env python3
"""R227 exact classical test theory, two items and independent retest.

Eight immutable finite artificial worlds; independent errors repeat between
occasions while stable latent trait T remains fixed. Fraction computations
separate observed-score covariance, conditional true-score variance and
cross-occasion reproducibility. No real psychometric evidence is asserted.

python research/R227/r227_exact_classical_test_theory.py --test
python research/R227/r227_exact_classical_test_theory.py --emit
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
Z=F(0)
ONE=F(1)
TYPES=(-1,1)
NOISE=tuple(itertools.product(TYPES,repeat=3))
FREEZE="176e057bcc121a66633181d6e184b12019ca6e32"
# Coefficients multiply stable T, occasion E1, occasion E2, occasion M, constant.
WORLD_COEFFS={
 "PARALLEL_INDEPENDENT":((1,1,0,0,0),(1,0,1,0,0)),
 "SHARED_METHOD_WITH_TRAIT":((1,1,0,1,0),(1,0,1,1,0)),
 "PERFECT_TRAIT":((1,0,0,0,0),(1,0,0,0,0)),
 "PERFECT_METHOD":((0,0,0,1,0),(0,0,0,1,0)),
 "UNEQUAL_ERRORS":((1,1,0,0,0),(1,0,2,0,0)),
 "OPPOSING_METHOD":((1,0,0,1,0),(1,0,0,-1,0)),
 "OPPOSING_TRAIT":((1,1,0,0,0),(-1,0,1,0,0)),
 "NON_EQUIVALENT_ITEM":((1,1,0,0,0),(2,0,1,0,1)),
}
ANALYTIC_TARGETS={
 "PARALLEL_INDEPENDENT":("2","2","1","2/3","2/3"),
 "SHARED_METHOD_WITH_TRAIT":("3","3","2","4/5","2/5"),
 "PERFECT_TRAIT":("1","1","1","1","1"),
 "PERFECT_METHOD":("1","1","1","1","0"),
 "UNEQUAL_ERRORS":("2","5","1","4/9","4/9"),
 "OPPOSING_METHOD":("2","2","0","0","1"),
 "OPPOSING_TRAIT":("2","2","-1","-2","0"),
 "NON_EQUIVALENT_ITEM":("2","5","2","8/11","9/11"),
}

def linear(coeff,t,e1,e2,m):
    return F(coeff[0]*t+coeff[1]*e1+coeff[2]*e2+coeff[3]*m+coeff[4])

def items(world,t,e):
    if world not in WORLD_COEFFS or t not in TYPES or e not in NOISE:
        raise ValueError("source outside frozen model")
    a,b=WORLD_COEFFS[world]
    return linear(a,t,*e),linear(b,t,*e)

def single_sources(world):
    if world not in WORLD_COEFFS: raise ValueError("unknown world")
    data=[]
    for t in TYPES:
        for e in NOISE:
            x,y=items(world,t,e)
            data.append(dict(world=world,stable_trait_T=t,occasion_E1=e[0],
                             occasion_E2=e[1],occasion_shared_M=e[2],
                             observed_item_X=x,observed_item_Y=y,observed_sum_S=x+y,
                             source_probability=F(1,16)))
    assert len(data)==16 and sum((r["source_probability"] for r in data),Z)==ONE
    return tuple(data)

def retest_sources(world):
    if world not in WORLD_COEFFS: raise ValueError("unknown world")
    data=[]
    for t in TYPES:
        for e in NOISE:
            x1,y1=items(world,t,e)
            for ee in NOISE:
                x2,y2=items(world,t,ee)
                data.append(dict(world=world,stable_trait_T=t,
                                 first_E1=e[0],first_E2=e[1],first_shared_M=e[2],
                                 second_E1=ee[0],second_E2=ee[1],second_shared_M=ee[2],
                                 first_item_X=x1,first_item_Y=y1,first_sum_S=x1+y1,
                                 second_item_X=x2,second_item_Y=y2,second_sum_S=x2+y2,
                                 source_probability=F(1,128)))
    assert len(data)==128 and sum((r["source_probability"] for r in data),Z)==ONE
    return tuple(data)

def moments(rows, keys):
    """Weighted covariances computed exclusively from observable score columns."""
    p=sum((r["source_probability"] for r in rows),Z)
    if p!=ONE: raise AssertionError("source weights do not total one")
    mu={k:sum((r["source_probability"]*r[k] for r in rows),Z) for k in keys}
    v={(a,b):sum((r["source_probability"]*(r[a]-mu[a])*(r[b]-mu[b])
                  for r in rows),Z) for a in keys for b in keys}
    return mu,v

def true_score_conditional(rows):
    """Only artificial oracle may condition on the fixed latent trait."""
    mean_by_trait={}
    for t in TYPES:
        subs=[r for r in rows if r["stable_trait_T"]==t]
        weight=sum((r["source_probability"] for r in subs),Z)
        if weight!=F(1,2): raise AssertionError("wrong stable trait mix")
        mean_by_trait[t]=sum((r["source_probability"]*r["observed_sum_S"]
                             for r in subs),Z)/weight
    qbar=sum(mean_by_trait.values(),Z)/2
    v=sum(((mean_by_trait[t]-qbar)**2 for t in TYPES),Z)/2
    return mean_by_trait,v

def direct_analytic(world):
    # Independent coefficient-square route, no source rows, score fit or moment API.
    a,b=WORLD_COEFFS[world]
    v_x=F(sum(a[i]**2 for i in range(4)))
    v_y=F(sum(b[i]**2 for i in range(4)))
    cov=F(sum(a[i]*b[i] for i in range(4)))
    v_sum=F(sum((a[i]+b[i])**2 for i in range(4)))
    v_true=F((a[0]+b[0])**2)
    mean_sum=F(a[4]+b[4])
    if v_sum<=0: return None
    return dict(var_x=v_x,var_y=v_y,cov_xy=cov,var_sum=v_sum,
                mean_sum=mean_sum,true_variance=v_true,
                alpha=4*cov/v_sum,true_reliability=v_true/v_sum,
                retest_cov=v_true,retest_reliability=v_true/v_sum)

def observed_joint(world):
    joint=defaultdict(F)
    for r in single_sources(world):
        joint[(r["observed_item_X"],r["observed_item_Y"])]+=r["source_probability"]
    return dict(sorted(joint.items()))

def retest_joint(world):
    joint=defaultdict(F)
    for r in retest_sources(world):
        joint[(r["first_sum_S"],r["second_sum_S"])]+=r["source_probability"]
    return dict(sorted(joint.items()))

def world_result(world):
    singles=single_sources(world)
    pairs=retest_sources(world)
    mu,v=moments(singles,("observed_item_X","observed_item_Y","observed_sum_S"))
    a=direct_analytic(world)
    if a is None: raise AssertionError("unsupported frozen zero score variance")
    var_x=v["observed_item_X","observed_item_X"]
    var_y=v["observed_item_Y","observed_item_Y"]
    cov=v["observed_item_X","observed_item_Y"]
    var_s=v["observed_sum_S","observed_sum_S"]
    if var_s==0: raise AssertionError("unfrozen degenerate score")
    alpha=2*(1-(var_x+var_y)/var_s)
    if alpha!=4*cov/var_s: raise AssertionError("two alpha formulae diverged")
    q_by_t,true_var=true_score_conditional(singles)
    mup,vp=moments(pairs,("first_sum_S","second_sum_S"))
    retest_cov=vp["first_sum_S","second_sum_S"]
    retest_reliability=retest_cov/vp["first_sum_S","first_sum_S"]
    computed=dict(var_x=var_x,var_y=var_y,cov_xy=cov,
                  var_sum=var_s,mean_sum=mu["observed_sum_S"],
                  true_variance=true_var,alpha=alpha,
                  true_reliability=true_var/var_s,
                  retest_cov=retest_cov,retest_reliability=retest_reliability)
    if computed!=a: raise AssertionError("independent symbolic variance mismatch")
    if vp["first_sum_S","first_sum_S"]!=var_s or vp["second_sum_S","second_sum_S"]!=var_s:
        raise AssertionError("retest marginal score scale differs")
    if retest_reliability!=true_var/var_s:
        raise AssertionError("conditional repeated error independence failed")
    expected=ANALYTIC_TARGETS[world]
    if tuple(str(computed[k]) for k in ("var_x","var_y","cov_xy","alpha",
                                         "true_reliability"))!=expected:
        raise AssertionError("precommitted exact values do not hold")
    return dict(world=world,original_single_source_atoms=16,
                original_independent_retest_pairs=128,
                two_item_alpha=str(alpha),
                true_reliability_conditional_stable_trait=str(true_var/var_s),
                retest_reliability_from_independent_occasion_pairs=str(retest_reliability),
                variance_item_X=str(var_x),variance_item_Y=str(var_y),
                covariance_items=str(cov),variance_sum=str(var_s),
                true_score_variance=str(true_var),
                total_score_mean=str(mu["observed_sum_S"]),
                stable_trait_true_score_by_T={str(t):str(q_by_t[t]) for t in TYPES},
                single_observation_joint={f"{x},{y}":str(p) for (x,y),p in observed_joint(world).items()},
                retest_sum_joint={f"{x},{y}":str(p) for (x,y),p in retest_joint(world).items()})

def write_outputs():
    worlds=[world_result(w) for w in WORLD_COEFFS]
    assert observed_joint("PERFECT_TRAIT")==observed_joint("PERFECT_METHOD")
    assert retest_joint("PERFECT_TRAIT")!=retest_joint("PERFECT_METHOD")
    data=dict(research_id="R227",actual_catalogue_id="10-001",
              frozen_protocol_commit=FREEZE,scientific_scope="FINITE_ARTIFICIAL_E1_ONLY",
              worlds_count=8,complete_single_source_atoms=128,
              complete_independent_retest_source_pairs=1024,
              observational_alias_same_P_XY_different_true_reliability=True,
              retest_distribution_distinguishes_alias=True,
              new_real_human_E2=0,new_real_historical_E3=0,
              R073="FROZEN",PESEN_v0_1="FROZEN",world_results=worlds)
    paths=[]
    for filename, rows in (
            ("R227_ALL_128_ORIGINAL_SINGLE_TEST_SOURCES.csv",
             [r for w in WORLD_COEFFS for r in single_sources(w)]),
            ("R227_ALL_1024_ORIGINAL_RETEST_SOURCE_PAIRS.csv",
             [r for w in WORLD_COEFFS for r in retest_sources(w)])):
        path=HERE/filename
        with path.open("w",encoding="utf-8",newline="") as f:
            out=csv.DictWriter(f,fieldnames=tuple(rows[0]),lineterminator="\n")
            out.writeheader()
            for row in rows: out.writerow({k:str(v) for k,v in row.items()})
        paths.append(path)
    result=HERE/"R227_EXACT_RESULTS.json"
    result.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R227",catalogue_id="10-001",worlds=8,
                 original_single_source_rows=128,original_retest_pair_rows=1024,
                 two_independent_fraction_moment_and_coefficient_routes=True,
                 exact_conditional_and_retest_reliability_match=True,
                 observational_reliability_alias_verified=True,
                 single_sources_sha256=hashlib.sha256(paths[0].read_bytes()).hexdigest(),
                 retest_pairs_sha256=hashlib.sha256(paths[1].read_bytes()).hexdigest(),
                 results_sha256=hashlib.sha256(result.read_bytes()).hexdigest(),
                 new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R227_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_world_count(self): self.assertEqual(len(WORLD_COEFFS),8)
    def test_single_count(self): self.assertEqual(sum(len(single_sources(w)) for w in WORLD_COEFFS),128)
    def test_retest_count(self): self.assertEqual(sum(len(retest_sources(w)) for w in WORLD_COEFFS),1024)
    def test_joint_alias(self): self.assertEqual(observed_joint("PERFECT_TRAIT"),observed_joint("PERFECT_METHOD"))
    def test_retest_alias_break(self): self.assertNotEqual(retest_joint("PERFECT_TRAIT"),retest_joint("PERFECT_METHOD"))
    def test_error_inflates_alpha(self):
        x=world_result("SHARED_METHOD_WITH_TRAIT")
        self.assertEqual((x["two_item_alpha"],x["true_reliability_conditional_stable_trait"]),("4/5","2/5"))
    def test_method_only_retest_zero(self):
        x=world_result("PERFECT_METHOD")
        self.assertEqual((x["two_item_alpha"],x["retest_reliability_from_independent_occasion_pairs"]),("1","0"))
    def test_anti_method_zero_alpha(self):
        x=world_result("OPPOSING_METHOD")
        self.assertEqual((x["two_item_alpha"],x["true_reliability_conditional_stable_trait"]),("0","1"))
    def test_negative_alpha(self):
        self.assertEqual(world_result("OPPOSING_TRAIT")["two_item_alpha"],"-2")
    def test_nonequivalence(self):
        x=world_result("NON_EQUIVALENT_ITEM")
        self.assertEqual((x["two_item_alpha"],x["true_reliability_conditional_stable_trait"]),("8/11","9/11"))
    def test_bad_world(self):
        with self.assertRaises(ValueError): single_sources("UNKNOWN")
    def test_bad_trait(self):
        with self.assertRaises(ValueError): items("PERFECT_TRAIT",2,NOISE[0])

def _case(world,kind):
    def t(self):
        rows=single_sources(world)
        paired=retest_sources(world)
        if kind=="mass":
            self.assertEqual(sum((r["source_probability"] for r in rows),Z),ONE)
        elif kind=="pair_mass":
            self.assertEqual(sum((r["source_probability"] for r in paired),Z),ONE)
        elif kind=="uniqueness":
            self.assertEqual(len({(r["stable_trait_T"],r["occasion_E1"],
                                   r["occasion_E2"],r["occasion_shared_M"]) for r in rows}),16)
        elif kind=="pair_uniqueness":
            self.assertEqual(len({(r["stable_trait_T"],r["first_E1"],r["first_E2"],r["first_shared_M"],
                                   r["second_E1"],r["second_E2"],r["second_shared_M"]) for r in paired}),128)
        elif kind=="analytic":
            result=world_result(world)
            analytic=direct_analytic(world)
            self.assertEqual(F(result["two_item_alpha"]),analytic["alpha"])
        elif kind=="repeat":
            result=world_result(world)
            self.assertEqual(result["true_reliability_conditional_stable_trait"],
                             result["retest_reliability_from_independent_occasion_pairs"])
        else: raise AssertionError("unsupported test")
    return t

for _world in WORLD_COEFFS:
    for _kind in ("mass","pair_mass","uniqueness","pair_uniqueness","analytic","repeat"):
        setattr(Tests,"test_"+_world.lower()+"_"+_kind,_case(_world,_kind))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.test:unittest.main(argv=["r227"],verbosity=2)
    else:print(json.dumps(write_outputs(),indent=2))
