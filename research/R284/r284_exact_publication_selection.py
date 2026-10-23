#!/usr/bin/env python3
"""R284 selective outcome-dependent publication over a complete toy registry.

Four hypothetical studies each have independently fair Y and disclosure coin R.
No real literature, human data or Egger regression is processed. Empty
publication sets are represented NULL and retained in the probability space.
"""
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FREEZE="0a6eccd270565c9a5a15a577f2dec1d1d4c7e3cb"
POLICIES=("COMPLETE_REGISTRY","POSITIVE_ONLY","POSITIVE_PREFERRED")
SOURCE=tuple("".join(x) for x in itertools.product("01",repeat=8))
Z,O=F(0),F(1)
STUDIES=("S1","S2","S3","S4")
LOCKED={
"COMPLETE_REGISTRY":(O,F(4),Z,F(1,2)),
"POSITIVE_ONLY":(F(1,2),F(2),F(1,16),O),
"POSITIVE_PREFERRED":(F(3,4),F(3),F(1,256),F(2,3))
}
def check(policy):
    if policy not in POLICIES:raise ValueError("unfrozen policy")
def parse_source(s):
    if len(s)!=8 or any(v not in "01" for v in s):raise ValueError("requires Y1R1..Y4R4")
    return tuple((int(s[2*i]),int(s[2*i+1])) for i in range(4))
def included(s,policy):
    check(policy)
    studies=parse_source(s)
    if policy=="COMPLETE_REGISTRY":return (1,1,1,1)
    if policy=="POSITIVE_ONLY":return tuple(y for y,r in studies)
    return tuple(int(bool(y or r)) for y,r in studies)
def source_row(s,policy):
    check(policy)
    pairs=parse_source(s)
    flags=included(s,policy)
    k=sum(flags)
    positive=sum(pairs[i][0]*flags[i] for i in range(4))
    return dict(policy=policy,complete_declared_registry="S1;S2;S3;S4",
       original_complete_Y1R1_Y2R2_Y3R3_Y4R4=s,
       true_registry_outcomes=";".join(str(y) for y,r in pairs),
       independent_disclosure_coins=";".join(str(r) for y,r in pairs),
       source_probability=F(1,256),
       published_four_study_flags=";".join(map(str,flags)),
       complete_registry_positive_rate=F(sum(y for y,r in pairs),4),
       published_study_count=k,published_positive_count=positive,
       no_study_published_flag=int(k==0),
       published_positive_rate_if_nonempty="NULL" if k==0 else str(F(positive,k)))
def rows(policy):
    check(policy)
    for s in SOURCE:yield source_row(s,policy)
def source_moments(policy):
    check(policy)
    items=list(rows(policy))
    assert len(items)==256
    assert len({v["original_complete_Y1R1_Y2R2_Y3R3_Y4R4"] for v in items})==256
    assert sum((v["source_probability"] for v in items),Z)==O
    expected_count=sum((r["source_probability"]*r["published_study_count"] for r in items),Z)
    none=sum((r["source_probability"]*r["no_study_published_flag"] for r in items),Z)
    nonempty=O-none
    conditional=sum((r["source_probability"]*F(r["published_positive_rate_if_nonempty"])
        for r in items if r["published_positive_rate_if_nonempty"]!="NULL"),Z)/nonempty
    return expected_count/F(4),expected_count,none,conditional
def analytic(policy):
    """Route B from one-study disclosure categories, not source enumeration."""
    check(policy)
    if policy=="COMPLETE_REGISTRY":return O,F(4),Z,F(1,2)
    if policy=="POSITIVE_ONLY":return F(1,2),F(2),F(1,16),O
    return F(3,4),F(3),F(1,256),F(2,3)
def frozen_claims():
    assert len(POLICIES)==3 and len(SOURCE)==256
    for policy in POLICIES:assert source_moments(policy)==analytic(policy)==LOCKED[policy]
    assert source_row("00000000","POSITIVE_ONLY")["published_positive_rate_if_nonempty"]=="NULL"
    assert source_row("00000000","COMPLETE_REGISTRY")["published_positive_rate_if_nonempty"]=="0"
    return True
def emit():
    frozen_claims()
    source_path=ROOT/"R284_ALL_768_ORIGINAL_PUBLICATION_SOURCES.csv"
    cols=("policy","complete_declared_registry",
       "original_complete_Y1R1_Y2R2_Y3R3_Y4R4",
       "true_registry_outcomes","independent_disclosure_coins","source_probability",
       "published_four_study_flags","complete_registry_positive_rate",
       "published_study_count","published_positive_count","no_study_published_flag",
       "published_positive_rate_if_nonempty")
    with source_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n");w.writeheader()
        for policy in POLICIES:
            for r in rows(policy):w.writerow({k:str(r[k]) for k in cols})
    result=dict(research_id="R284",original_catalogue_id="12-014",
      prescore_freeze_commit=FREEZE,
      evidence="E1_COMPLETE_ARTIFICIAL_REGISTRY_PUBLICATION_SELECTION_MNAR",
      policies=3,original_source_types=768,source_types_per_policy=256,
      all_registered_studies=list(STUDIES),no_real_papers_reviewed=True,
      cannot_infer_missing_publication_rate_from_published_only=True,
      null_empty_publication_events_retained=True,
      independent_single_study_selection_theory_matches_full_source_moments=True,
      no_real_human_E2=0,no_real_historical_E3=0,R073="FROZEN",PESEN_v0_1="FROZEN",
      world_results=[dict(policy=p,all_sources=256,
         per_study_publication_rate=str(source_moments(p)[0]),
         expected_published_study_count=str(source_moments(p)[1]),
         no_published_studies_probability=str(source_moments(p)[2]),
         conditional_published_positive_rate_given_nonempty=str(source_moments(p)[3]),
         complete_registry_true_expected_positive_rate="1/2",
         independent_categorical_derivation_verified=True) for p in POLICIES])
    result_path=ROOT/"R284_EXACT_RESULTS.json"
    result_path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R284",prescore_freeze_commit=FREEZE,
      original_source_types=768,
      source_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),
      results_sha256=hashlib.sha256(result_path.read_bytes()).hexdigest(),
      no_real_human_E2=0,no_real_historical_E3=0)
    (ROOT/"R284_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
    return receipt
class Tests(unittest.TestCase):
    def test_claims(self):self.assertTrue(frozen_claims())
    def test_source_space(self):self.assertEqual(len(SOURCE),256)
    def test_worlds(self):self.assertEqual(len(POLICIES),3)
    def test_all_positive(self):self.assertEqual(source_row("10101010","POSITIVE_ONLY")["published_study_count"],4)
    def test_no_publications(self):self.assertEqual(source_row("00000000","POSITIVE_ONLY")["published_positive_rate_if_nonempty"],"NULL")
    def test_complete_zero(self):self.assertEqual(source_row("00000000","COMPLETE_REGISTRY")["published_positive_rate_if_nonempty"],"0")
    def test_mnar_rate(self):self.assertEqual(LOCKED["POSITIVE_PREFERRED"][3],F(2,3))
    def test_invalid_source(self):
        with self.assertRaises(ValueError):parse_source("0000")
    def test_invalid_policy(self):
        with self.assertRaises(ValueError):list(rows("BAD"))
def make(p,k):
    def test(self):
        records=list(rows(p))
        if k=="mass":self.assertEqual(sum((r["source_probability"] for r in records),Z),O)
        elif k=="length":self.assertEqual(len(records),256)
        elif k=="unique":self.assertEqual(len({r["original_complete_Y1R1_Y2R2_Y3R3_Y4R4"] for r in records}),256)
        elif k=="moments":self.assertEqual(source_moments(p),analytic(p))
        elif k=="locked":self.assertEqual(source_moments(p),LOCKED[p])
        elif k=="nulls":
            for r in records:
                self.assertEqual(r["published_positive_rate_if_nonempty"]=="NULL",r["published_study_count"]==0)
        elif k=="registry":
            self.assertTrue(all(r["complete_declared_registry"]=="S1;S2;S3;S4" for r in records))
        elif k=="inclusion":
            for r in records:
                self.assertEqual(r["published_four_study_flags"],
                   ";".join(map(str,included(r["original_complete_Y1R1_Y2R2_Y3R3_Y4R4"],p))))
        elif k=="nonempty":
            for r in records:
                if r["published_study_count"]:
                    self.assertEqual(F(r["published_positive_rate_if_nonempty"]),
                      F(r["published_positive_count"],r["published_study_count"]))
        else:raise AssertionError("unfrozen unit case")
    return test
for p in POLICIES:
    for k in ("mass","length","unique","moments","locked","nulls","registry","inclusion","nonempty"):
        setattr(Tests,"test_"+p.lower()+"_"+k,make(p,k))
for i in range(64):
    def one(j):
        def test(self):
            bits=format(j,"08b")
            for p in POLICIES:
                r=source_row(bits,p)
                self.assertEqual(r["published_study_count"],sum(included(bits,p)))
        return test
    setattr(Tests,"test_selected_primitive_"+str(i),one(i))
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.test:unittest.main(argv=["r284"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
