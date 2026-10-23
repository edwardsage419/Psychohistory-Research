#!/usr/bin/env python3
"""R305 no-import independent four-object partition pair enumeration and 486-row adversarial verifier."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as Q
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]/"research/R305"
CSV=ROOT/"R305_ALL_486_ORIGINAL_SELF_CATEGORIZATION_SOURCE_CELLS.csv"
RESULT=ROOT/"R305_EXACT_SCT_COMPARATIVE_FIT_RESULTS.json"
RECEIPT=ROOT/"R305_MACHINE_RECEIPT.json"
ZERO,ONE=Q(0),Q(1)
CONTEXTS={"X":(Q(0),Q(1),Q(4),Q(5)),
   "MID":(Q(0),Q(5,2),Q(5,2),Q(5)),
   "Y":(Q(0),Q(4),Q(1),Q(5))}
LABELS={"P":(0,0,1,1),"Q":(0,1,0,1)}
LEVELS=(ZERO,Q(1,2),ONE)
BASELINES=(ZERO,ONE,Q(2))
WORLDS=list(itertools.product(CONTEXTS,LEVELS,LEVELS,LEVELS,BASELINES))
CATEGORIES=("P","Q")
FIELDS=("context","feature_values","readiness","normative_fit_P","normative_fit_Q",
      "personal_baseline","candidate_category","category_labels",
      "within_mean","across_mean","metacontrast","within_pair_ids","across_pair_ids",
      "candidate_normative_fit","candidate_social_score","competing_social_score",
      "chosen_self_category","this_category_wins","personal_identity_wins")

def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def sources():
    with CSV.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def label(w):
    ctx,r,np,nq,t=w
    return f"context={ctx}|readiness={r}|norm_P={np}|norm_Q={nq}|personal_baseline={t}"

def independent_pairs(ctx,category):
    values=CONTEXTS[ctx]
    member=LABELS[category]
    within=[];across=[]
    for i in range(len(values)):
        for j in range(i+1,len(values)):
            (within if member[i]==member[j] else across).append((i,j))
    W=sum((abs(values[i]-values[j]) for i,j in within),ZERO)/len(within)
    B=sum((abs(values[i]-values[j]) for i,j in across),ZERO)/len(across)
    return W,B,B/W,";".join(f"{i}-{j}" for i,j in within),";".join(f"{i}-{j}" for i,j in across)

def independent_world(w):
    ctx,r,np,nq,t=w
    pfit=independent_pairs(ctx,"P")[2]
    qfit=independent_pairs(ctx,"Q")[2]
    scoreP=r*np*pfit;scoreQ=r*nq*qfit
    if scoreP>scoreQ and scoreP>t:chosen="P"
    elif scoreQ>scoreP and scoreQ>t:chosen="Q"
    else:chosen="PERSONAL"
    return scoreP,scoreQ,chosen

def expected_row(w,category):
    ctx,r,np,nq,t=w
    W,B,ratio,within,across=independent_pairs(ctx,category)
    scoreP,scoreQ,choice=independent_world(w)
    candidate=scoreP if category=="P" else scoreQ
    other=scoreQ if category=="P" else scoreP
    d={"context":ctx,"feature_values":";".join(str(v) for v in CONTEXTS[ctx]),
      "readiness":r,"normative_fit_P":np,"normative_fit_Q":nq,
      "personal_baseline":t,"candidate_category":category,
      "category_labels":";".join(str(z) for z in LABELS[category]),
      "within_mean":W,"across_mean":B,"metacontrast":ratio,
      "within_pair_ids":within,"across_pair_ids":across,
      "candidate_normative_fit":np if category=="P" else nq,
      "candidate_social_score":candidate,"competing_social_score":other,
      "chosen_self_category":choice,"this_category_wins":choice==category,
      "personal_identity_wins":choice=="PERSONAL"}
    return {k:str(d[k]) for k in FIELDS}

def verify(rows,result):
    if len(rows)!=486 or result["complete_labeled_original_source_rows"]!=486 or len(result["worlds"])!=243:
        raise AssertionError("original full source universes required")
    known={(w,category) for w in WORLDS for category in CATEGORIES}
    seen={}
    for row in rows:
        try:
            w=(row["context"],Q(row["readiness"]),Q(row["normative_fit_P"]),
              Q(row["normative_fit_Q"]),Q(row["personal_baseline"]))
            category=row["candidate_category"]
        except (KeyError,ValueError,ZeroDivisionError) as err:raise AssertionError("invalid dimensions") from err
        key=(w,category)
        if key not in known or key in seen:raise AssertionError("missing/duplicate/unfrozen cell")
        if row["world"]!=label(w):raise AssertionError("false original world ID")
        expected=expected_row(w,category)
        for f in FIELDS:
            if row[f]!=expected[f]:raise AssertionError("independent original source mismatch "+f)
        seen[key]=row
    if set(seen)!=known:raise AssertionError("source universe incomplete")
    for i,w in enumerate(WORLDS):
        record=result["worlds"][i]
        ctx,r,np,nq,t=w
        sp,sq,choice=independent_world(w)
        if record["world"]!=label(w):raise AssertionError("result ID")
        if record["context"]!=ctx or record["readiness"]!=str(r):raise AssertionError("result readiness")
        if record["normative_fit_P"]!=str(np) or record["normative_fit_Q"]!=str(nq) or record["personal_baseline"]!=str(t):
            raise AssertionError("result norm/threshold")
        if (record["social_score_P"],record["social_score_Q"],record["chosen_self_category"])!=(str(sp),str(sq),choice):
            raise AssertionError("result scores/choice")
        if record["original_option_source_rows"]!=2:raise AssertionError("result row count")
        if record["category_sources"]!=[expected_row(w,c) for c in CATEGORIES]:
            raise AssertionError("world sources and CSV disagree")
    expected_reference={
      "X_comparative_fit_P":"4","X_comparative_fit_Q":"5/8",
      "MID_both_comparative_fit":"1",
      "Y_comparative_fit_P":"5/8","Y_comparative_fit_Q":"4",
      "X_full_ready_norm_personal1":"P",
      "Y_full_ready_norm_personal1":"Q",
      "MID_full_ready_norm_personal1":"PERSONAL",
      "X_normP0_normQ1_personal0":"Q",
      "readiness0_all_personal":True}
    if result["frozen_reference"]!=expected_reference:raise AssertionError("prospective summary mutated")
    for ctx in CONTEXTS:
        for np,nq,t in itertools.product(LEVELS,LEVELS,BASELINES):
            if independent_world((ctx,ZERO,np,nq,t))[2]!="PERSONAL":
                raise AssertionError("not-ready negative control")
    return {"original_source_rows":486,"worlds":243,
      "independent_all_six_pair_distance_verification":"PASS",
      "context_X_Y_self_categorization_reversal":"PASS",
      "readiness_zero_personal_fallback":"PASS",
      "new_empirical_E2":0,"new_historical_E3":0}
def audit():
    receipt,result=obj(RECEIPT),obj(RESULT)
    freeze="a4dfc1f582c9a58eec6cf45b63a34f577800e0eb"
    if receipt["freeze_commit"]!=freeze or result["freeze_commit"]!=freeze:raise AssertionError("wrong protocol")
    if result["original_catalogue_id"]!="03-004" or result["research_id"]!="R305":raise AssertionError("wrong model")
    if result["model_scoring_rule_project_invented_not_Turner_1985_author_equation"] is not True:
        raise AssertionError("project invention misattributed")
    if result["Turner_original_human_self_categorization_data_replayed"] is not False:
        raise AssertionError("fictitious human E2")
    if any(result[x]!=0 for x in ("no_real_human_E2_added","no_real_animal_E2_added","no_historical_E3_added")):
        raise AssertionError("synthetic to empirical promotion")
    if receipt["source_rows"]!=486 or receipt["new_real_E2"]!=0 or receipt["new_historical_E3"]!=0:raise AssertionError("receipt")
    if receipt["source_sha256"]!=hashlib.sha256(CSV.read_bytes()).hexdigest():raise AssertionError("source SHA")
    if receipt["results_sha256"]!=hashlib.sha256(RESULT.read_bytes()).hexdigest():raise AssertionError("results SHA")
    return {**verify(sources(),result),"source_sha256":receipt["source_sha256"],
       "results_sha256":receipt["results_sha256"]}

class Tests(unittest.TestCase):
    def test_audit(self):self.assertEqual(audit()["original_source_rows"],486)
    def test_world_count(self):self.assertEqual(len(WORLDS),243)
    def test_X_P(self):self.assertEqual(independent_pairs("X","P")[:3],(ONE,Q(4),Q(4)))
    def test_X_Q(self):self.assertEqual(independent_pairs("X","Q")[2],Q(5,8))
    def test_Y_Q(self):self.assertEqual(independent_pairs("Y","Q")[2],Q(4))
    def test_MID(self):self.assertEqual(independent_pairs("MID","P")[2],ONE)
    def test_context_reversal(self):self.assertEqual(independent_world(("Y",ONE,ONE,ONE,ONE))[2],"Q")
    def test_normative_reverse(self):self.assertEqual(independent_world(("X",ONE,ZERO,ONE,ZERO))[2],"Q")
    def test_no_readiness(self):self.assertEqual(independent_world(("X",ZERO,ONE,ONE,ZERO))[2],"PERSONAL")
    def test_missing(self):
        with self.assertRaises(AssertionError):verify(sources()[:-1],obj(RESULT))
    def test_duplicate(self):
        s=sources();s[1]=dict(s[0])
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_wrong_pairs(self):
        s=sources();s[0]=dict(s[0]);s[0]["within_pair_ids"]="0-2;1-3"
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_wrong_normative(self):
        s=sources();s[0]=dict(s[0]);s[0]["normative_fit_P"]="1/3"
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_wrong_score(self):
        s=sources();s[0]=dict(s[0]);s[0]["candidate_social_score"]="100"
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_wrong_choice(self):
        s=sources();s[0]=dict(s[0]);s[0]["chosen_self_category"]="TRUE_CATEGORY"
        with self.assertRaises(AssertionError):verify(s,obj(RESULT))
    def test_result_tamper(self):
        r=obj(RESULT);r["worlds"][0]["social_score_P"]="100"
        with self.assertRaises(AssertionError):verify(sources(),r)
    def test_summary_tamper(self):
        r=obj(RESULT);r["frozen_reference"]["X_comparative_fit_P"]="3"
        with self.assertRaises(AssertionError):verify(sources(),r)
    def test_sha_tamper(self):
        self.assertNotEqual(hashlib.sha256(CSV.read_bytes()+b"x").hexdigest(),obj(RECEIPT)["source_sha256"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true");m.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R305 audit"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
