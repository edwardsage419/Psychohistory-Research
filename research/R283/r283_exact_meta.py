#!/usr/bin/env python3
"""R283 finite artificial three-study synthesis; not a real literature review."""
import argparse,csv,itertools,json,hashlib,unittest
from pathlib import Path
from fractions import Fraction as F
from math import comb
ROOT=Path(__file__).resolve().parent
FREEZE="310b134383db1b08b66750d12d7229005426b439"
Z,O=F(0),F(1)
STUDIES=("S1","S2","S3")
DESIGNS={"HOMOGENEOUS":((F(3,4),F(1,4)),)*3,
"BALANCED_HETEROGENEITY":((F(3,4),F(1,4)),(F(1,2),F(1,2)),(F(1,4),F(3,4))),
"ONE_REVERSAL":((F(3,4),F(1,4)),(F(3,4),F(1,4)),(F(1,4),F(3,4)))}
EXPECTED={"HOMOGENEOUS":(F(1,2),F(1,8),F(2),F(469,512)),
"BALANCED_HETEROGENEITY":(Z,F(3,22),F(10,3),F(175,256)),
"ONE_REVERSAL":(F(1,6),F(1,8),F(34,9),F(419,512))}
SOURCES=tuple("".join(x) for x in itertools.product("01",repeat=6))
def check(m):
    if m not in DESIGNS:raise ValueError("invalid frozen regime")
def inclusion(studies):
    if tuple(studies)!=STUDIES:raise ValueError("all S1,S2,S3 required")
    return True
def weights(m):
    check(m)
    var=tuple(t*(O-t)+c*(O-c) for t,c in DESIGNS[m])
    return tuple(O/x for x in var)
def original_mass(m,s):
    check(m)
    if len(s)!=6 or any(v not in "01" for v in s):raise ValueError("six bits needed")
    out=O
    for i,(t,c) in enumerate(DESIGNS[m]):
        a,b=map(int,s[2*i:2*i+2])
        out*=t**a*(O-t)**(1-a)*c**b*(O-c)**(1-b)
    return out
def statistic(m,s):
    inclusion(STUDIES)
    w=weights(m)
    if len(s)!=6 or any(v not in "01" for v in s):raise ValueError("six bits needed")
    d=tuple(int(s[2*i])-int(s[2*i+1]) for i in range(3))
    mu=sum((w[i]*d[i] for i in range(3)),Z)/sum(w,Z)
    Q=sum((w[i]*(F(d[i])-mu)**2 for i in range(3)),Z)
    return d,mu,Q,max(d)
def source_rows(m):
    check(m)
    for s in SOURCES:
        d,mu,Q,mx=statistic(m,s)
        yield dict(regime=m,all_included_studies="S1;S2;S3",
          original_ordered_T1C1T2C2T3C3=s,
          treatment_true_rates=";".join(str(t) for t,c in DESIGNS[m]),
          control_true_rates=";".join(str(c) for t,c in DESIGNS[m]),
          oracle_inverse_variance_weights=";".join(map(str,weights(m))),
          original_source_mass=original_mass(m,s),
          three_reported_risk_differences=";".join(map(str,d)),
          fixed_all_studies_estimate=mu,cochran_Q=Q,
          invalid_posthoc_largest_study_effect=mx)
def exhaustive(m):
    rows=list(source_rows(m))
    assert len(rows)==64 and len({x["original_ordered_T1C1T2C2T3C3"] for x in rows})==64
    assert sum((x["original_source_mass"] for x in rows),Z)==O
    mean=sum((x["original_source_mass"]*x["fixed_all_studies_estimate"] for x in rows),Z)
    second=sum((x["original_source_mass"]*x["fixed_all_studies_estimate"]**2 for x in rows),Z)
    Q=sum((x["original_source_mass"]*x["cochran_Q"] for x in rows),Z)
    largest=sum((x["original_source_mass"]*x["invalid_posthoc_largest_study_effect"] for x in rows),Z)
    return mean,second-mean**2,Q,largest
def independent_theory(m):
    check(m)
    w=weights(m); sw=sum(w,Z)
    delta=[t-c for t,c in DESIGNS[m]]
    mu=sum((w[i]*delta[i] for i in range(3)),Z)/sw
    variance=O/sw
    Q=F(2)+sum((w[i]*(delta[i]-mu)**2 for i in range(3)),Z)
    pmfs=[]
    for t,c in DESIGNS[m]:
        pmfs.append({-1:(O-t)*c,0:t*c+(O-t)*(O-c),1:t*(O-c)})
    selection=Z
    for ds in itertools.product((-1,0,1),repeat=3):
        prob=O
        for i,x in enumerate(ds):prob*=pmfs[i][x]
        selection+=prob*max(ds)
    return mu,variance,Q,selection
def freeze_check():
    assert len(DESIGNS)==3 and len(SOURCES)==64
    for m in DESIGNS:assert exhaustive(m)==independent_theory(m)==EXPECTED[m]
    return True
def emit():
    freeze_check()
    csvfile=ROOT/"R283_ALL_192_ORIGINAL_THREE_STUDY_META_SOURCES.csv"
    fields=("regime","all_included_studies","original_ordered_T1C1T2C2T3C3",
      "treatment_true_rates","control_true_rates","oracle_inverse_variance_weights",
      "original_source_mass","three_reported_risk_differences",
      "fixed_all_studies_estimate","cochran_Q","invalid_posthoc_largest_study_effect")
    with csvfile.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader()
        for m in DESIGNS:
            for x in source_rows(m):w.writerow({k:str(x[k]) for k in fields})
    result=dict(research_id="R283",original_catalogue_id="12-013",
      prescore_freeze_commit=FREEZE,scope="E1_THREE_SYNTHETIC_STUDIES_NOT_REAL_LITERATURE_REVIEW",
      registry=list(STUDIES),complete_original_sources=192,
      no_literature_search_or_real_studies=True,
      oracle_weights_require_unobserved_true_variances=True,
      all_three_independent_three_study_trinomial_checks_match=True,
      human_E2=0,historical_E3=0,R073="FROZEN",PESEN_v0_1="FROZEN",
      results=[dict(regime=m,original_sources=64,
         oracle_weights=list(map(str,weights(m))),
         pooled_mean=str(exhaustive(m)[0]),pooled_variance=str(exhaustive(m)[1]),
         expected_Q=str(exhaustive(m)[2]),posthoc_largest_mean=str(exhaustive(m)[3]))
         for m in DESIGNS])
    jp=ROOT/"R283_EXACT_META_RESULTS.json"
    jp.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R283",prescore_freeze_commit=FREEZE,
      complete_original_sources=192,independent_trinomial_combinations=27,
      source_sha256=hashlib.sha256(csvfile.read_bytes()).hexdigest(),
      result_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
      real_human_E2=0,real_historical_E3=0)
    (ROOT/"R283_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
    return receipt
class Tests(unittest.TestCase):
    def test_theory(self):self.assertTrue(freeze_check())
    def test_worlds(self):self.assertEqual(len(DESIGNS),3)
    def test_64(self):self.assertEqual(len(SOURCES),64)
    def test_all(self):self.assertTrue(inclusion(STUDIES))
    def test_exclude(self):
        with self.assertRaises(ValueError):inclusion(("S1","S2"))
    def test_order(self):
        with self.assertRaises(ValueError):inclusion(("S2","S1","S3"))
    def test_bad_model(self):
        with self.assertRaises(ValueError):list(source_rows("NONE"))
    def test_bad_source(self):
        with self.assertRaises(ValueError):statistic("HOMOGENEOUS","000")
def make(m,k):
    def test(self):
        rows=list(source_rows(m))
        if k=="count":self.assertEqual(len(rows),64)
        elif k=="mass":self.assertEqual(sum((x["original_source_mass"] for x in rows),Z),O)
        elif k=="unique":self.assertEqual(len({x["original_ordered_T1C1T2C2T3C3"] for x in rows}),64)
        elif k=="oracle":self.assertEqual(exhaustive(m),independent_theory(m))
        elif k=="locked":self.assertEqual(exhaustive(m),EXPECTED[m])
        elif k=="include":self.assertTrue(all(x["all_included_studies"]=="S1;S2;S3" for x in rows))
        elif k=="source":self.assertTrue(all(x["original_source_mass"]==original_mass(m,x["original_ordered_T1C1T2C2T3C3"]) for x in rows))
        elif k=="positive":self.assertTrue(all(x["original_source_mass"]>Z for x in rows))
        elif k=="risk":
            for x in rows:
                ds,d,q,largest=statistic(m,x["original_ordered_T1C1T2C2T3C3"])
                self.assertEqual(x["fixed_all_studies_estimate"],d)
                self.assertEqual(x["cochran_Q"],q)
                self.assertEqual(x["invalid_posthoc_largest_study_effect"],largest)
        else:raise AssertionError("invalid test")
    return test
for m in DESIGNS:
    for k in ("count","mass","unique","oracle","locked","include","source","positive","risk"):
        setattr(Tests,"test_"+m.lower()+"_"+k,make(m,k))
for i in range(64):
    def one(j):
        def test(self):
            src=format(j,"06b")
            for m in DESIGNS:
                ds,d,Q,mx=statistic(m,src)
                self.assertTrue(-1<=d<=1 and Q>=0 and mx in (-1,0,1))
        return test
    setattr(Tests,"test_source_"+str(i),one(i))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r283"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
