"""R188 postscore E1 analysis: degenerate cluster scores from deterministic balance.

This script recreates, but does not alter, the 180 frozen R188 synthetic worlds.
All calculations are exact fractions and use no external software/data.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product, combinations_with_replacement
from collections import Counter
from pathlib import Path
from hashlib import sha256
import json
import unittest
import sys

HERE=Path(__file__).resolve().parent
DESIGNS={
    "BALANCED":(4,4,4,4,4,4),
    "WEAK_BETWEEN":(2,2,4,4,6,6),
    "STRONG_BETWEEN":(2,2,2,6,6,6),
}
A=(F(0),F(1))
B=(F(1,4),F(1,2))
C=(F(-4),F(-2),F(0),F(2),F(4))
E=(F(0),F(1,4),F(1,2))
DELTA=F(1,16)
G,N=6,8


def worlds():
    for (name,k),a,b,c,e in product(DESIGNS.items(),A,B,C,E):
        yield name,k,a,b,c,e


def make_rows(k,a,b,c,e):
    rows=[]
    for group,t in enumerate(k):
        mean=F(t,N)
        for x,m in ((0,N-t),(1,t)):
            for j in range(m):
                eps=e if j<m//2 else -e
                rows.append((group,F(x),a+b*x+c*mean+eps))
    if len(rows)!=G*N:
        raise ValueError("unexpected N")
    return rows


def cluster_stats(rows):
    grouped=[[] for _ in range(G)]
    for g,x,y in rows:
        if not isinstance(g,int) or not 0<=g<G:
            raise ValueError("invalid group")
        grouped[g].append((x,y))
    if any(len(v)!=N for v in grouped):
        raise ValueError("nonconforming group sizes")
    out=[]
    for group in grouped:
        xm=sum((x for x,y in group),F())/N
        ym=sum((y for x,y in group),F())/N
        centered=[(x-xm,y-ym) for x,y in group]
        s=sum((x*x for x,y in centered),F())
        t=sum((x*y for x,y in centered),F())
        if s<=0:
            raise ValueError("zero within-cluster exposure variance")
        out.append((s,t,centered))
    return out


def audit(rows):
    groups=cluster_stats(rows)
    S=sum((s for s,t,v in groups),F())
    beta=sum((t for s,t,v in groups),F())/S
    scores=[]
    hc0_num=F()
    sse=F()
    for s,t,centered in groups:
        score=F()
        for x,y in centered:
            resid=y-beta*x
            score+=x*resid
            hc0_num+=(x*resid)**2
            sse+=resid**2
        scores.append(score)
        if score!=t-beta*s:
            raise AssertionError("cluster score vs sufficient statistics mismatch")
    if sum(scores,F())!=0:
        raise AssertionError("OLS score not zero")
    return {
        "beta":beta,"Sxx":S,"scores":tuple(scores),
        "CR0_variance":sum((x*x for x in scores),F())/(S*S),
        "HC0_variance":hc0_num/(S*S),
        "FE_homoskedastic_variance":sse/(G*N-G-1)/S,
        "SSE":sse,
        "cluster_sxx":tuple(s for s,t,v in groups),
        "cluster_sxy":tuple(t for s,t,v in groups),
    }


def all_group_bootstrap_slopes(rows):
    groups=cluster_stats(rows)
    seen=0
    baseline=None
    for draw in combinations_with_replacement(range(G),G):
        weights=Counter(draw)
        numerator=sum((groups[g][1]*w for g,w in weights.items()),F())
        denominator=sum((groups[g][0]*w for g,w in weights.items()),F())
        val=numerator/denominator
        if baseline is None:
            baseline=val
        if val!=baseline:
            raise AssertionError("cluster-resample slope changed")
        seen+=1
    if seen!=462:
        raise AssertionError("incorrect number of unlabeled bootstrap multisets")
    return baseline,seen


def leave_one_cluster_out(rows):
    groups=cluster_stats(rows)
    results=[]
    for omitted in range(G):
        num=sum((t for g,(s,t,v) in enumerate(groups) if g!=omitted),F())
        den=sum((s for g,(s,t,v) in enumerate(groups) if g!=omitted),F())
        results.append(num/den)
    return tuple(results)


def paired_identity(k,e):
    return sum((F(t*(N-t),N) for t in k),F()),F(e*e)


def run():
    results=[]
    for name,k,a,b,c,e in worlds():
        rows=make_rows(k,a,b,c,e)
        exact=audit(rows)
        S,_=paired_identity(k,e)
        if exact["Sxx"]!=S or exact["beta"]!=b or exact["SSE"]!=G*N*e*e:
            raise AssertionError("historical R188 invariant mismatch")
        if any(exact["scores"]) or exact["CR0_variance"]!=0:
            raise AssertionError("exact group score degeneracy failed")
        if exact["HC0_variance"]!=e*e/S:
            raise AssertionError("independent analytic HC0 identity failed")
        if exact["FE_homoskedastic_variance"]!=G*N*e*e/F(G*N-G-1)/S:
            raise AssertionError("homoskedastic FE variance identity failed")
        jackknife=leave_one_cluster_out(rows)
        if any(x!=b for x in jackknife):
            raise AssertionError("six leave-one-cluster-out estimators disagree")
        boot,nboot=all_group_bootstrap_slopes(rows)
        if boot!=b:
            raise AssertionError("all group bootstrap resamples disagree")
        # Deliberately break the exact cell-pair balance in one source observation.
        g,x,y=rows[0]
        changed=list(rows)
        changed[0]=(g,x,y+DELTA)
        damaged=audit(changed)
        if damaged["CR0_variance"]<=0 or damaged["beta"]==b:
            raise AssertionError("predefined perturbation not detected")
        exact_delta_beta=DELTA*(x-F(k[0],N))/S
        if damaged["beta"]-b!=exact_delta_beta:
            raise AssertionError("perturbation effect not exact")
        results.append({
            "design":name,"a":str(a),"b":str(b),"c":str(c),"e":str(e),
            "Sxx":str(S),"sse":str(exact["SSE"]),
            "FE_beta":str(b),
            "FE_cluster_scores":[str(z) for z in exact["scores"]],
            "CR0_variance":str(exact["CR0_variance"]),
            "HC0_variance":str(exact["HC0_variance"]),
            "homoskedastic_FE_variance":str(exact["FE_homoskedastic_variance"]),
            "all_six_leave_one_cluster_out_equal":True,
            "all_462_unlabeled_six_cluster_bootstrap_equal":True,
            "perturbed_beta":str(damaged["beta"]),
            "perturbed_CR0_variance":str(damaged["CR0_variance"]),
            "perturbed_delta_beta":str(exact_delta_beta)
        })
    positive=sum(F(z["HC0_variance"])>0 for z in results)
    if len(results)!=180 or positive!=120:
        raise AssertionError("unexpected outcomes")
    sample=next(z for z in results if z["design"]=="STRONG_BETWEEN" and z["a"]=="0" and z["b"]=="1/4" and z["c"]=="-4" and z["e"]=="1/4")
    if (sample["Sxx"],sample["HC0_variance"],sample["homoskedastic_FE_variance"],sample["CR0_variance"])!=("9","1/144","1/123","0"):
        raise AssertionError("fixed R188 source example incorrect")
    payload={
        "study":"R188_FIXED_GROUP_SCORE_DEGENERACY_AND_PERTURBATION_POSTSCORE", 
        "date":"2026-11-14",
        "status":"E1_EXACT_SYNTHETIC_POSTSCORE",
        "frozen_protocol_modified":False,
        "scientific_scope":"descriptive residual-based estimators on deterministic artificial data, not repeated-sampling variance",
        "original_worlds":180,"source_rows_rebuilt":8640,
        "clusters_per_world":6,"rows_per_cluster":8,
        "bootstrap_unlabeled_multisets_per_world":462,
        "bootstrap_resamples_checked":180*462,
        "leave_one_out_recalculations":180*6,
        "zero_CR0_all_worlds":True,
        "positive_HC0_worlds":positive,
        "zero_HC0_worlds":len(results)-positive,
        "positive_CR0_after_fixed_perturbation_worlds":sum(F(z["perturbed_CR0_variance"])>0 for z in results),
        "evidence_grade":"INTERNAL_ARTIFICIAL_MATHEMATICAL_E1",
        "new_E2":0,"new_E3":0,"external_independent_researcher_reproductions":0,
        "fixed_example":sample,
        "all_worlds":results
    }
    p=HERE/"R188_CLUSTER_SCORE_EXACT_RESULTS_20261114.json"
    p.write_text(json.dumps(payload,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return payload

class Tests(unittest.TestCase):
    def test_factorial_size(self):self.assertEqual(len(list(worlds())),180)
    def test_six_groups_and_48_observations(self):self.assertEqual(len(make_rows((2,2,2,6,6,6),F(0),F(1,4),F(-4),F(1,4))),48)
    def test_handpicked_within_Sxx(self):
        self.assertEqual(paired_identity((4,)*6,F(1,4))[0],12)
        self.assertEqual(paired_identity((2,2,4,4,6,6),F(1,4))[0],10)
        self.assertEqual(paired_identity((2,2,2,6,6,6),F(1,4))[0],9)
    def test_cr0_exact_zero(self):self.assertEqual(audit(make_rows((2,2,2,6,6,6),F(0),F(1,4),F(-4),F(1,4)))["CR0_variance"],0)
    def test_hc0_fixed(self):self.assertEqual(audit(make_rows((2,2,2,6,6,6),F(0),F(1,4),F(-4),F(1,4)))["HC0_variance"],F(1,144))
    def test_naive_finite_df(self):self.assertEqual(audit(make_rows((2,2,2,6,6,6),F(0),F(1,4),F(-4),F(1,4)))["FE_homoskedastic_variance"],F(1,123))
    def test_bootstrap_462(self):
        rows=make_rows((2,2,2,6,6,6),F(0),F(1,4),F(-4),F(1,4))
        self.assertEqual(all_group_bootstrap_slopes(rows),(F(1,4),462))
    def test_looclust(self):
        rows=make_rows((2,2,2,6,6,6),F(0),F(1,4),F(-4),F(1,4))
        self.assertEqual(leave_one_cluster_out(rows),(F(1,4),)*6)
    def test_perturb_b(self):
        rows=make_rows((2,2,2,6,6,6),F(0),F(1,4),F(-4),F(1,4))
        g,x,y=rows[0];rows[0]=(g,x,y+DELTA)
        self.assertEqual(audit(rows)["beta"],F(1,4)-F(1,576))
    def test_perturb_cr0_positive(self):
        rows=make_rows((2,2,2,6,6,6),F(0),F(1,4),F(-4),F(1,4))
        g,x,y=rows[0];rows[0]=(g,x,y+DELTA)
        self.assertGreater(audit(rows)["CR0_variance"],0)
    def test_all_worlds(self):self.assertEqual(run()["positive_HC0_worlds"],120)
    def test_balance_breaks_when_cell_perturbed(self):
        rows=make_rows((4,)*6,F(1),F(1,2),F(2),F(0))
        a=audit(rows)
        g,x,y=rows[0];rows[0]=(g,x,y+DELTA)
        b=audit(rows)
        self.assertEqual(a["CR0_variance"],0)
        self.assertGreater(b["CR0_variance"],0)
    def test_bootstrap_invariant_weak(self):
        rows=make_rows((2,2,4,4,6,6),F(1),F(1,2),F(4),F(1,2))
        self.assertEqual(all_group_bootstrap_slopes(rows),(F(1,2),462))
    def test_bad_group_fails(self):
        rows=make_rows((4,)*6,F(0),F(1,4),F(0),F(0))
        rows[0]=(-1,rows[0][1],rows[0][2])
        with self.assertRaises(ValueError):audit(rows)
    def test_bad_group_size_fails(self):
        rows=make_rows((4,)*6,F(0),F(1,4),F(0),F(0))
        with self.assertRaises(ValueError):audit(rows[:-1])

if __name__=="__main__":
    if len(sys.argv)>1 and sys.argv[1]=="--run":
        r=run();print(json.dumps({k:v for k,v in r.items() if k!="all_worlds"},ensure_ascii=False,sort_keys=True))
    else:unittest.main()
