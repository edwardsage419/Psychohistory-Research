#!/usr/bin/env python3
"""R285: exact Holm FWER and Benjamini-Hochberg FDR on two independent tests.

All 2304 ordered eightbit policy-labeled artificial source configurations
are kept. Independent oracle computes 25 Binomial count classes per world.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from math import comb
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="923b083cc61cbafdd339136fe9b5c407cffb88bf"
ZERO,ONE=F(0),F(1)
ALPHA=F(1,2)
PVALUES=(ONE,F(15,16),F(11,16),F(5,16),F(1,16))
REGIMES={"BOTH_NULL":(F(1,2),F(1,2)),
         "ONE_SIGNAL":(F(3,4),F(1,2)),
         "BOTH_SIGNAL":(F(3,4),F(3,4))}
POLICIES=("RAW_UNADJUSTED","HOLM_FWER","BH_FDR")
WORLDS=tuple((r,m) for r in REGIMES for m in POLICIES)
SOURCES=tuple("".join(z) for z in itertools.product("01",repeat=8))
FROZEN={
("BOTH_NULL","RAW_UNADJUSTED"):(F(135,256),F(135,256),F(5,8),ZERO,F(5,8)),
("BOTH_NULL","HOLM_FWER"):(F(31,256),F(31,256),F(5,32),ZERO,F(5,32)),
("BOTH_NULL","BH_FDR"):(F(47,256),F(47,256),F(9,32),ZERO,F(9,32)),
("ONE_SIGNAL","RAW_UNADJUSTED"):(F(5,16),F(1615,8192),F(5,16),F(189,256),F(269,256)),
("ONE_SIGNAL","HOLM_FWER"):(F(145,1024),F(647,8192),F(145,1024),F(351,1024),F(31,64)),
("ONE_SIGNAL","BH_FDR"):(F(253,1024),F(1079,8192),F(253,1024),F(459,1024),F(89,128)),
("BOTH_SIGNAL","RAW_UNADJUSTED"):(ZERO,ZERO,ZERO,F(189,128),F(189,128)),
("BOTH_SIGNAL","HOLM_FWER"):(ZERO,ZERO,ZERO,F(7371,8192),F(7371,8192)),
("BOTH_SIGNAL","BH_FDR"):(ZERO,ZERO,ZERO,F(10287,8192),F(10287,8192))}
def check(regime,policy):
    if (regime,policy) not in WORLDS:raise ValueError("unfrozen world or policy")
def pvalue(k):
    if type(k) is not int or not 0<=k<=4:raise ValueError("K in 0..4 required")
    return PVALUES[k]
def choose(pvals,policy):
    if policy not in POLICIES:raise ValueError("unfrozen multiple-testing rule")
    if len(pvals)!=2 or any(x not in PVALUES for x in pvals):raise ValueError("two frozen p-values needed")
    if policy=="RAW_UNADJUSTED":return tuple(int(p<=ALPHA) for p in pvals)
    order=sorted(range(2),key=lambda i:(pvals[i],i))
    mask=[0,0]
    if policy=="HOLM_FWER":
        for rank,i in enumerate(order):
            if pvals[i]<=ALPHA/F(2-rank):mask[i]=1
            else:break
    else:
        r=0
        for rank,i in enumerate(order,1):
            if pvals[i]<=ALPHA*rank/2:r=rank
        for i in order[:r]:mask[i]=1
    return tuple(mask)
def source_probability(regime,s):
    if regime not in REGIMES:raise ValueError("unknown regime")
    if len(s)!=8 or any(v not in "01" for v in s):raise ValueError("need eight ordered outcomes")
    a,b=REGIMES[regime]
    k1=s[:4].count("1");k2=s[4:].count("1")
    return a**k1*(ONE-a)**(4-k1)*b**k2*(ONE-b)**(4-k2)
def scores(regime,policy,k1,k2):
    check(regime,policy)
    null=tuple(p==F(1,2) for p in REGIMES[regime])
    ps=(pvalue(k1),pvalue(k2))
    mask=choose(ps,policy)
    R=sum(mask)
    V=sum(int(mask[i] and null[i]) for i in range(2))
    S=R-V
    return ps,mask,R,V,S,F(V,max(R,1)),int(V>0)
def original_rows(regime,policy):
    check(regime,policy)
    for s in SOURCES:
        k1=s[:4].count("1");k2=s[4:].count("1")
        ps,mask,R,V,S,FDP,FWER=scores(regime,policy,k1,k2)
        yield dict(world=regime+"_"+policy,regime=regime,policy=policy,
          true_H1_success_probability=REGIMES[regime][0],
          true_H2_success_probability=REGIMES[regime][1],
          original_eightbit_two_fourtrial_sources=s,
          count_H1=k1,count_H2=k2,
          original_source_probability=source_probability(regime,s),
          one_sided_exact_pvalue_H1=ps[0],one_sided_exact_pvalue_H2=ps[1],
          reject_H1=mask[0],reject_H2=mask[1],
          total_rejections_R=R,false_discoveries_V=V,
          true_discoveries_S=S,false_discovery_proportion=FDP,
          familywise_false_positive_flag=FWER)
def source_moments(regime,policy):
    items=tuple(original_rows(regime,policy))
    assert len(items)==256
    assert len({r["original_eightbit_two_fourtrial_sources"] for r in items})==256
    assert sum((r["original_source_probability"] for r in items),ZERO)==ONE
    return tuple(sum((r["original_source_probability"]*r[field] for r in items),ZERO)
      for field in ("familywise_false_positive_flag","false_discovery_proportion",
                   "false_discoveries_V","true_discoveries_S","total_rejections_R"))
def independent_binomial_oracle(regime,policy):
    check(regime,policy)
    a,b=REGIMES[regime]
    arr=[ZERO]*5
    for k1,k2 in itertools.product(range(5),repeat=2):
        mass=F(comb(4,k1))*a**k1*(ONE-a)**(4-k1)
        mass*=F(comb(4,k2))*b**k2*(ONE-b)**(4-k2)
        _,_,R,V,S,FDP,FWER=scores(regime,policy,k1,k2)
        for index,x in enumerate((FWER,FDP,V,S,R)):arr[index]+=mass*x
    return tuple(arr)
def frozen_claims():
    assert len(WORLDS)==9 and len(SOURCES)==256
    for r,m in WORLDS:assert source_moments(r,m)==independent_binomial_oracle(r,m)==FROZEN[r,m]
    assert choose((F(5,16),F(5,16)),"RAW_UNADJUSTED")==(1,1)
    assert choose((F(5,16),F(5,16)),"HOLM_FWER")==(0,0)
    assert choose((F(5,16),F(5,16)),"BH_FDR")==(1,1)
    return True
def emit():
    frozen_claims()
    src=ROOT/"R285_ALL_2304_ORIGINAL_MULTIPLE_TESTING_SOURCES.csv"
    fields=("world","regime","policy","true_H1_success_probability",
      "true_H2_success_probability","original_eightbit_two_fourtrial_sources",
      "count_H1","count_H2","original_source_probability",
      "one_sided_exact_pvalue_H1","one_sided_exact_pvalue_H2","reject_H1",
      "reject_H2","total_rejections_R","false_discoveries_V",
      "true_discoveries_S","false_discovery_proportion",
      "familywise_false_positive_flag")
    with src.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        writer.writeheader()
        for r,m in WORLDS:
            for s in original_rows(r,m):writer.writerow({k:str(s[k]) for k in fields})
    out=dict(research_id="R285",original_catalogue_id="12-015",
      prescore_freeze_commit=FREEZE,scope="E1_ARTIFICIAL_TWO_HYPOTHESIS_DISCRETE_MULTIPLE_TESTING",
      worlds=9,complete_original_source_types=2304,
      primitive_eightbit_source_space_size_per_world=256,
      family_nominal_alpha="1/2",alpha_purpose="illustrative discrete threshold, not recommended real-world significance level",
      frozen_null_one_sided_pvalues=list(map(str,PVALUES)),
      no_real_human_E2=0,no_real_historical_E3=0,
      R073="FROZEN",PESEN_v0_1="FROZEN",
      all_nine_source_vs_binomial_25_class_moments_verified=True,
      world_results=[dict(world=r+"_"+m,regime=r,policy=m,original_source_types=256,
        expected_FWER=str(source_moments(r,m)[0]),
        expected_FDR=str(source_moments(r,m)[1]),
        expected_false_discoveries=str(source_moments(r,m)[2]),
        expected_true_discoveries=str(source_moments(r,m)[3]),
        expected_total_rejections=str(source_moments(r,m)[4]),
        independent_25_class_binomial_analysis_verified=True) for r,m in WORLDS])
    resultpath=ROOT/"R285_EXACT_RESULTS.json"
    resultpath.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R285",prescore_freeze_commit=FREEZE,
      original_complete_source_types=2304,analytic_count_classes_per_world=25,
      source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
      result_sha256=hashlib.sha256(resultpath.read_bytes()).hexdigest(),
      new_real_human_E2=0,new_real_historical_E3=0)
    (ROOT/"R285_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
    return receipt
class Tests(unittest.TestCase):
    def test_claims(self):self.assertTrue(frozen_claims())
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_sources(self):self.assertEqual(len(SOURCES),256)
    def test_exact_p(self):self.assertEqual(PVALUES,(ONE,F(15,16),F(11,16),F(5,16),F(1,16)))
    def test_holm_vs_bh(self):self.assertNotEqual(choose((F(5,16),F(5,16)),"HOLM_FWER"),choose((F(5,16),F(5,16)),"BH_FDR"))
    def test_bad_count(self):
        with self.assertRaises(ValueError):pvalue(5)
    def test_bad_source(self):
        with self.assertRaises(ValueError):source_probability("BOTH_NULL","111")
    def test_bad_policy(self):
        with self.assertRaises(ValueError):choose((F(1),F(1)),"UNKNOWN")
def make(r,m,kind):
    def test(self):
        items=tuple(original_rows(r,m))
        if kind=="count":self.assertEqual(len(items),256)
        elif kind=="mass":self.assertEqual(sum((z["original_source_probability"] for z in items),ZERO),ONE)
        elif kind=="unique":self.assertEqual(len({z["original_eightbit_two_fourtrial_sources"] for z in items}),256)
        elif kind=="analysis":self.assertEqual(source_moments(r,m),independent_binomial_oracle(r,m))
        elif kind=="locked":self.assertEqual(source_moments(r,m),FROZEN[r,m])
        elif kind=="pvalues":
            for z in items:
                self.assertEqual(z["one_sided_exact_pvalue_H1"],PVALUES[z["count_H1"]])
                self.assertEqual(z["one_sided_exact_pvalue_H2"],PVALUES[z["count_H2"]])
        elif kind=="decisions":
            for z in items:self.assertEqual((z["reject_H1"],z["reject_H2"]),
              choose((z["one_sided_exact_pvalue_H1"],z["one_sided_exact_pvalue_H2"]),m))
        elif kind=="fdp":
            for z in items:self.assertEqual(z["false_discovery_proportion"],F(z["false_discoveries_V"],max(z["total_rejections_R"],1)))
        else:raise AssertionError("unknown frozen mode")
    return test
for r,m in WORLDS:
    for kind in ("count","mass","unique","analysis","locked","pvalues","decisions","fdp"):
        setattr(Tests,"test_"+r.lower()+"_"+m.lower()+"_"+kind,make(r,m,kind))
if __name__=="__main__":
    a=argparse.ArgumentParser()
    group=a.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    args=a.parse_args()
    if args.test:unittest.main(argv=["r285"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
