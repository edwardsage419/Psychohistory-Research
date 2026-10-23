#!/usr/bin/env python3
"""R268: exact finite ordered Bernoulli design measures for AIC/BIC choices.

3312 complete original artificial ordered sequences, two fixed candidate models.
Selection probabilities are Fractions. Log scores are explicitly floating point.
An independent Binomial(n,p) route reconstructs choices without source enumeration.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import unittest
from collections import defaultdict
from fractions import Fraction as F
from math import comb
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="6ab880be304cebf916948aa9877e6d233b6a5e69"
PTRUE=(F(1,5),F(1,2),F(4,5))
SIZES=(4,6,10)
WORLDS=tuple((p,n) for p in PTRUE for n in SIZES)
Q0=F(1,5)
ZERO,ONE=F(0),F(1)
LOCKED_DISAGREEMENT={
    (F(1,5),4):F(352,625),
    (F(1,2),4):F(7,16),
    (F(4,5),4):F(97,625),
    (F(1,5),6):ZERO,
    (F(1,2),6):ZERO,
    (F(4,5),6):ZERO,
    (F(1,5),10):F(172032,1953125),
    (F(1,2),10):F(105,512),
    (F(4,5),10):F(10752,1953125)}


def check(p,n):
    if (p,n) not in WORLDS:
        raise ValueError("outside frozen R268 world")


def world_id(p,n):
    check(p,n)
    return "TRUE_P"+str(p).replace("/","OF")+"_N"+str(n)


def loglike(k,n,q):
    if n<=0 or not 0<=k<=n or not 0<=q<=1:
        raise ValueError("invalid Bernoulli likelihood")
    if q==0:return 0.0 if k==0 else -math.inf
    if q==1:return 0.0 if k==n else -math.inf
    return k*math.log(float(q))+(n-k)*math.log1p(-float(q))


def scores(k,n):
    """Direct candidate log likelihoods, AIC and BIC, fixed candidate counts 0/1."""
    if not n in SIZES or not 0<=k<=n:
        raise ValueError("outside frozen sample size/count")
    q=F(k,n)
    l0=loglike(k,n,Q0)
    l1=loglike(k,n,q)
    a0=-2*l0
    a1=-2*l1+2
    b0=-2*l0
    b1=-2*l1+math.log(n)
    delta=2*(l1-l0)
    return dict(mle_q=q,LL0=l0,LL1=l1,likelihood_deviance_gain=delta,
        AIC0=a0,AIC1=a1,BIC0=b0,BIC1=b1,
        select_AIC="M1_FITTED" if a1<a0-1e-12 else "M0_FIXED",
        select_BIC="M1_FITTED" if b1<b0-1e-12 else "M0_FIXED")


def source_rows(p,n):
    """Route A: ordered source sequence enumeration and exact design mass."""
    check(p,n)
    for y in itertools.product((0,1),repeat=n):
        k=sum(y)
        s=scores(k,n)
        mass=p**k*(ONE-p)**(n-k)
        yield dict(world=world_id(p,n),true_p=p,n=n,
            original_ordered_binary_sequence="".join(map(str,y)),
            original_success_count=k,exact_source_probability=mass,
            maximum_likelihood_qhat=s["mle_q"],
            log_likelihood_M0=s["LL0"],log_likelihood_M1=s["LL1"],
            deviance_gain=s["likelihood_deviance_gain"],
            AIC_M0=s["AIC0"],AIC_M1=s["AIC1"],
            BIC_M0=s["BIC0"],BIC_M1=s["BIC1"],
            AIC_selected=s["select_AIC"],BIC_selected=s["select_BIC"],
            criteria_disagree=int(s["select_AIC"]!=s["select_BIC"]))


def independent_log_likelihood_ratio(k,n):
    """Separate formula: KL gain, not the loglike()/scores() routine."""
    if n not in SIZES or k<0 or k>n:
        raise ValueError("invalid count")
    result=0.0
    if k:
        result+=k*math.log(F(k,n)/Q0)
    if k<n:
        result+=(n-k)*math.log(F(n-k,n)/(ONE-Q0))
    return 2*result


def independent_k_rule(k,n):
    dev=independent_log_likelihood_ratio(k,n)
    return ("M1_FITTED" if dev>2+1e-12 else "M0_FIXED",
            "M1_FITTED" if dev>math.log(n)+1e-12 else "M0_FIXED")


def source_aggregate(p,n):
    check(p,n)
    mass=ZERO
    pA=pB=pD=ZERO
    bycount=defaultdict(lambda:ZERO)
    seen=set()
    rows=0
    for row in source_rows(p,n):
        s=row["original_ordered_binary_sequence"]
        assert s not in seen
        seen.add(s)
        w=row["exact_source_probability"]
        mass+=w
        rows+=1
        bycount[row["original_success_count"]]+=w
        if row["AIC_selected"]=="M1_FITTED":pA+=w
        if row["BIC_selected"]=="M1_FITTED":pB+=w
        if row["criteria_disagree"]:pD+=w
    assert mass==ONE and rows==2**n
    return pA,pB,pD,dict(bycount),rows


def binomial_aggregate(p,n):
    """Route B: analytical K distribution; never consume ordered source_rows."""
    check(p,n)
    pa=pb=pd=ZERO
    masses={}
    for k in range(n+1):
        w=F(comb(n,k))*p**k*(ONE-p)**(n-k)
        a,b=independent_k_rule(k,n)
        masses[k]=w
        if a=="M1_FITTED":pa+=w
        if b=="M1_FITTED":pb+=w
        if a!=b:pd+=w
    assert sum(masses.values(),ZERO)==ONE
    return pa,pb,pd,masses


def locked_claims():
    assert len(WORLDS)==len(LOCKED_DISAGREEMENT)==9
    assert sum(2**n for _,n in WORLDS)==3312
    for n in SIZES:
        disagreed=[k for k in range(n+1)
                   if independent_k_rule(k,n)[0]!=independent_k_rule(k,n)[1]]
        assert disagreed==({4:[0,2],6:[],10:[4]}[n])
        for k in range(n+1):
            d=scores(k,n)
            assert math.isclose(d["likelihood_deviance_gain"],independent_log_likelihood_ratio(k,n),
                                rel_tol=0,abs_tol=1e-12)
            assert (d["select_AIC"],d["select_BIC"])==independent_k_rule(k,n)
    for p,n in WORLDS:
        a=source_aggregate(p,n)
        b=binomial_aggregate(p,n)
        assert a[:3]==b[:3] and a[3]==b[3]
        assert a[2]==LOCKED_DISAGREEMENT[p,n],(p,n,a[2])
    return True


def one_step_log_loss(q,y):
    if not 0<=q<=1 or y not in (0,1):
        raise ValueError("invalid forecast/label")
    prob=float(q if y else 1-q)
    return -math.log(prob) if prob else math.inf


def emit():
    locked_claims()
    src=HERE/"R268_ALL_3312_BERNOULLI_ORDERED_SOURCE_TYPES.csv"
    columns=("world","true_p","n","original_ordered_binary_sequence",
       "original_success_count","exact_source_probability","maximum_likelihood_qhat",
       "log_likelihood_M0","log_likelihood_M1","deviance_gain",
       "AIC_M0","AIC_M1","BIC_M0","BIC_M1",
       "AIC_selected","BIC_selected","criteria_disagree")
    with src.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=columns,lineterminator="\n")
        writer.writeheader()
        for p,n in WORLDS:
            for row in source_rows(p,n):
                writer.writerow({k:str(row[k]) for k in columns})
    worlds=[]
    for p,n in WORLDS:
        sa=source_aggregate(p,n)
        sb=binomial_aggregate(p,n)
        worlds.append(dict(world=world_id(p,n),true_p=str(p),n=n,
            full_ordered_original_source_types=sa[4],
            source_weighted_probability_AIC_selects_M1=str(sa[0]),
            source_weighted_probability_BIC_selects_M1=str(sa[1]),
            source_weighted_probability_AIC_BIC_disagree=str(sa[2]),
            independent_binomial_exact_aggregate_verified=sa[:4]==sb,
            frozen_per_K_decisions={str(k):dict(
                 AIC=scores(k,n)["select_AIC"],BIC=scores(k,n)["select_BIC"],
                 deviance_gain=repr(scores(k,n)["likelihood_deviance_gain"]))
                 for k in range(n+1)}))
    results=dict(research_id="R268",original_catalogue_id="11-028",
       prescore_freeze_commit=FREEZE,
       scope="E1_ARTIFICIAL_COMPLETE_ORDERED_BERNOULLI_AIC_BIC",
       worlds=worlds,complete_source_types=3312,
       all_nine_independent_binomial_decision_probabilities_verified=True,
       numerical_logs_used_while_source_probabilities_are_exact_Fraction=True,
       frozen_M0_parameter_count=0,frozen_M1_parameter_count=1,
       frozen_M0_q="1/5",all_parameter_border_cases_handled=True,
       no_out_of_sample_predictive_superiority_claim=True,
       new_real_human_E2=0,new_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN")
    jp=HERE/"R268_EXACT_RESULTS.json"
    jp.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R268",prescore_freeze_commit=FREEZE,
       worlds=9,original_source_types=3312,
       verified_independent_binomial_worlds=9,
       source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
       new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/"R268_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt


class Tests(unittest.TestCase):
    def test_locked(self):self.assertTrue(locked_claims())
    def test_source_count(self):self.assertEqual(sum(2**n for _,n in WORLDS),3312)
    def test_world_count(self):self.assertEqual(len(WORLDS),9)
    def test_parameter_count(self):self.assertEqual(scores(0,4)["mle_q"],ZERO)
    def test_qhat_boundary(self):self.assertEqual(scores(10,10)["mle_q"],ONE)
    def test_future_failure_q0(self):self.assertTrue(math.isinf(one_step_log_loss(ZERO,1)))
    def test_future_failure_q1(self):self.assertTrue(math.isinf(one_step_log_loss(ONE,0)))
    def test_m0_forecast_finite(self):self.assertTrue(math.isfinite(one_step_log_loss(Q0,1)))
    def test_invalid_world(self):
        with self.assertRaises(ValueError):list(source_rows(F(1,3),4))
    def test_invalid_likelihood(self):
        with self.assertRaises(ValueError):loglike(5,4,Q0)
    def test_disagree_4(self):self.assertEqual([k for k in range(5) if independent_k_rule(k,4)[0]!=independent_k_rule(k,4)[1]],[0,2])
    def test_disagree_10(self):self.assertEqual([k for k in range(11) if independent_k_rule(k,10)[0]!=independent_k_rule(k,10)[1]],[4])


def world_test(p,n,mode):
    def test(self):
        a=source_aggregate(p,n);b=binomial_aggregate(p,n)
        if mode=="mass":self.assertEqual(sum((r["exact_source_probability"] for r in source_rows(p,n)),ZERO),ONE)
        elif mode=="unique":self.assertEqual(len({r["original_ordered_binary_sequence"] for r in source_rows(p,n)}),2**n)
        elif mode=="count":self.assertEqual(a[4],2**n)
        elif mode=="binomial":self.assertEqual(a[:4],b)
        elif mode=="locked":self.assertEqual(a[2],LOCKED_DISAGREEMENT[p,n])
        elif mode=="fit":
            self.assertTrue(all(r["maximum_likelihood_qhat"]==F(r["original_success_count"],n) for r in source_rows(p,n)))
        elif mode=="deviance":
            self.assertTrue(all(math.isclose(r["deviance_gain"],independent_log_likelihood_ratio(r["original_success_count"],n),rel_tol=0,abs_tol=1e-12) for r in source_rows(p,n)))
        elif mode=="decision":
            self.assertTrue(all((r["AIC_selected"],r["BIC_selected"])==independent_k_rule(r["original_success_count"],n) for r in source_rows(p,n)))
        else:raise AssertionError("unfrozen test")
    return test


for p,n in WORLDS:
    for mode in ("mass","unique","count","binomial","locked","fit","deviance","decision"):
        setattr(Tests,"test_p"+str(p).replace("/","of")+"_n"+str(n)+"_"+mode,world_test(p,n,mode))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.test:unittest.main(argv=["r268"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
