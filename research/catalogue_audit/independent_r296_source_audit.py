#!/usr/bin/env python3
"""R296 independent original 40-state source audit; never imports model implementation."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R296"
SOURCE=ROOT/"R296_ALL_40_ORIGINAL_RW_CUE_BLOCKING_STATES.csv"
RESULT=ROOT/"R296_EXACT_BLOCKING_UNBLOCKING_RESULTS.json"
RECEIPT=ROOT/"R296_MACHINE_RECEIPT.json"
ALPHAS=(Q(1,4),Q(1,2))
WORLDS=list(itertools.product(ALPHAS,(0,8),(1,2)))
STAGES=range(5)
COMPONENTS=("pretrained_A","RW_A","RW_B","RW_compound_sum",
            "RW_remaining_compound_error","INDEPENDENT_A","INDEPENDENT_B")
ONE,Z=Q(1),Q(0)

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def sources():
    with SOURCE.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def ident(alpha,pre,reward):
    return f"alpha={alpha}|npre={pre}|compound_reward={reward}"

def independent_calculation(alpha,pre,reward,m):
    p=Z
    for _ in range(pre):p+=(ONE-p)*alpha
    x=p;y=Z
    ind_a=p;ind_b=Z
    for _ in range(m):
        error=Q(reward)-x-y
        x+=alpha*error
        y+=alpha*error
        ind_a+=alpha*(Q(reward)-ind_a)
        ind_b+=alpha*(Q(reward)-ind_b)
    return {"pretrained_A":p,"RW_A":x,"RW_B":y,"RW_compound_sum":x+y,
            "RW_remaining_compound_error":Q(reward)-x-y,
            "INDEPENDENT_A":ind_a,"INDEPENDENT_B":ind_b}

def closed_form(alpha,pre,reward,m):
    p=ONE-(ONE-alpha)**pre
    factor=(ONE-2*alpha)**m
    b=(Q(reward)-p)*(ONE-factor)/2
    return {"pretrained_A":p,"RW_A":p+b,"RW_B":b,
      "RW_compound_sum":p+2*b,"RW_remaining_compound_error":Q(reward)-p-2*b,
      "INDEPENDENT_A":Q(reward)+(p-Q(reward))*(ONE-alpha)**m,
      "INDEPENDENT_B":Q(reward)*(ONE-(ONE-alpha)**m)}

def verify(rows,results):
    if len(rows)!=40 or len(results["worlds"])!=8:raise AssertionError("incomplete original universe")
    expected=set((a,n,r,m) for a,n,r in WORLDS for m in STAGES)
    seen={}
    for row in rows:
        try:
            a=Q(row["alpha"]);n=int(row["A_only_pretraining_trials"])
            r=int(row["compound_reward_target"]);m=int(row["compound_training_trials"])
        except (KeyError,ValueError,ZeroDivisionError) as exc:raise AssertionError("corrupt source dimensions") from exc
        key=(a,n,r,m)
        if key not in expected or key in seen:raise AssertionError("unexpected/duplicated original cell")
        if row["world"]!=ident(a,n,r):raise AssertionError("original world label mismatch")
        current=independent_calculation(a,n,r,m)
        formal=closed_form(a,n,r,m)
        if current!=formal:raise AssertionError("recurrence vs separate closed form mismatch")
        for f in COMPONENTS:
            if Q(row[f])!=current[f]:raise AssertionError("corrupt source: "+f)
        seen[key]=current
    if set(seen)!=expected:raise AssertionError("missing original source cells")
    for ix,(a,n,r) in enumerate(WORLDS):
        entry=results["worlds"][ix]
        if entry["world"]!=ident(a,n,r) or entry["alpha"]!=str(a) or entry["pretraining_trials"]!=n or entry["compound_reward_target"]!=r:raise AssertionError("result world mismatch")
        if entry["original_source_rows"]!=5 or len(entry["stages"])!=5:raise AssertionError("result stages incomplete")
        for m in STAGES:
            st=entry["stages"][m]
            exp=seen[(a,n,r,m)]
            if st["m"]!=m:raise AssertionError("result trial index mismatch")
            for f in COMPONENTS:
                if st[f]!=str(exp[f]):raise AssertionError("stored result wrong: "+f)
        if seen[(a,n,r,0)]["RW_B"]!=Z:raise AssertionError("untrained cue starts zero")
    for a in ALPHAS:
        if not seen[(a,8,1,4)]["RW_B"]<seen[(a,0,1,4)]["RW_B"]:raise AssertionError("blocking failed")
        if not seen[(a,8,2,4)]["RW_B"]>seen[(a,8,1,4)]["RW_B"]:raise AssertionError("upshift unblocking failed")
        if seen[(a,8,1,4)]["INDEPENDENT_B"]!=seen[(a,0,1,4)]["INDEPENDENT_B"]:raise AssertionError("independent-control wrong")
    ref=results["reference_alpha_half"]
    expect={"A_after_eight_pretrain":"255/256","RW_B_after_pretrain_reinforced_AB_four":"1/512",
      "RW_B_without_pretrain_reinforced_AB_four":"1/2",
      "RW_B_after_pretrain_AB_reward_double_four":"257/512",
      "independent_B_pretraining_invariant_with_AB_reward_one":"15/16"}
    if ref!=expect:raise AssertionError("conclusion special cases not source grounded")
    if results["blocking_under_A_pretraining_for_both_alphas"] is not True:raise AssertionError("false blocking claim")
    if results["unblocking_under_reward_upshift_for_both_alphas"] is not True:raise AssertionError("false upshift claim")
    return {"original_full_states":40,"artificial_trajectory_worlds":8,
       "original_trials_reconstructed":sum(8+m for _,pre,_ in WORLDS for m in STAGES) if False else 0,
       "blocking_each_alpha":"PASS","reward_upshift_each_alpha":"PASS",
       "independent_negative_control":"PASS","added_human_E2":0,"added_animal_E2":0,"added_historical_E3":0}

def audit():
    r,j=obj(RECEIPT),obj(RESULT)
    freeze="78e947a3de8dbeb209edc473ae74f98eb6937904"
    if r["freeze_commit"]!=freeze or j["freeze_commit"]!=freeze:raise AssertionError("prospective freeze mismatch")
    if j["original_catalogue_id"]!="02-001" or j["world_count"]!=8 or j["complete_artificial_source_rows"]!=40:raise AssertionError("wrong scientific scope")
    if r["E2_added"]!=0 or r["E3_added"]!=0 or j["new_real_human_E2"]!=0 or j["new_real_animal_E2"]!=0 or j["new_historical_E3"]!=0:raise AssertionError("invalid E2 or E3")
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=r["source_sha256"]:raise AssertionError("source digest mismatch")
    if hashlib.sha256(RESULT.read_bytes()).hexdigest()!=r["results_sha256"]:raise AssertionError("result digest mismatch")
    return {**verify(sources(),j),"source_sha256":r["source_sha256"],"results_sha256":r["results_sha256"]}

class Tests(unittest.TestCase):
    def test_full(self):self.assertEqual(audit()["original_full_states"],40)
    def test_worlds(self):self.assertEqual(len(WORLDS),8)
    def test_closed_form(self):self.assertEqual(independent_calculation(Q(1,2),8,1,4),closed_form(Q(1,2),8,1,4))
    def test_block(self):self.assertEqual(closed_form(Q(1,2),8,1,4)["RW_B"],Q(1,512))
    def test_nonblocked(self):self.assertEqual(closed_form(Q(1,2),0,1,4)["RW_B"],Q(1,2))
    def test_upshift(self):self.assertEqual(closed_form(Q(1,2),8,2,4)["RW_B"],Q(257,512))
    def test_independent(self):self.assertEqual(closed_form(Q(1,2),8,1,4)["INDEPENDENT_B"],Q(15,16))
    def test_missing(self):
        with self.assertRaises(AssertionError):verify(sources()[:-1],obj(RESULT))
    def test_duplicate(self):
        bad=sources();bad[1]=dict(bad[0])
        with self.assertRaises(AssertionError):verify(bad,obj(RESULT))
    def test_wrong_association(self):
        bad=sources();bad[0]=dict(bad[0]);bad[0]["RW_B"]="999"
        with self.assertRaises(AssertionError):verify(bad,obj(RESULT))
    def test_wrong_pretraining(self):
        bad=sources();bad[0]=dict(bad[0]);bad[0]["A_only_pretraining_trials"]="4"
        with self.assertRaises(AssertionError):verify(bad,obj(RESULT))
    def test_fake_compound(self):
        bad=sources();bad[0]=dict(bad[0]);bad[0]["RW_compound_sum"]="999"
        with self.assertRaises(AssertionError):verify(bad,obj(RESULT))
    def test_wrong_result(self):
        j=obj(RESULT);j["worlds"][0]["stages"][0]["RW_B"]="2"
        with self.assertRaises(AssertionError):verify(sources(),j)
    def test_sha_tamper(self):self.assertNotEqual(hashlib.sha256(SOURCE.read_bytes()+b"evil").hexdigest(),obj(RECEIPT)["source_sha256"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R296 independent"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
