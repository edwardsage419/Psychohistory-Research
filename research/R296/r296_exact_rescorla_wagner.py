#!/usr/bin/env python3
"""R296 exact synthetic Rescorla-Wagner shared-error cue competition vs independent error."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="78e947a3de8dbeb209edc473ae74f98eb6937904"
Z,O=F(0),F(1)
ALPHAS=(F(1,4),F(1,2))
PRETRAIN=(0,8)
TARGETS=(1,2)
STAGES=tuple(range(5))
WORLDS=tuple(itertools.product(ALPHAS,PRETRAIN,TARGETS))
CSV_NAME="R296_ALL_40_ORIGINAL_RW_CUE_BLOCKING_STATES.csv"
RESULT_NAME="R296_EXACT_BLOCKING_UNBLOCKING_RESULTS.json"
RECEIPT_NAME="R296_MACHINE_RECEIPT.json"

def world_id(alpha,npre,target):
    return f"alpha={alpha}|npre={npre}|compound_reward={target}"

def initial_p(alpha,npre):
    if alpha not in ALPHAS or npre not in PRETRAIN:raise ValueError("unfrozen pretraining")
    p=Z
    for _ in range(npre):p=p+alpha*(O-p)
    return p

def formula(alpha,npre,target,m):
    if (alpha,npre,target) not in WORLDS or m not in STAGES:raise ValueError("unfrozen model source")
    p=initial_p(alpha,npre)
    d=(O-2*alpha)**m
    B=F(target-p,2)*(O-d)
    A=p+B
    ind_B=F(target)*(O-(O-alpha)**m)
    ind_A=F(target)+(p-F(target))*(O-alpha)**m
    return {"pretrained_A":p,"RW_A":A,"RW_B":B,"RW_compound_sum":A+B,
            "RW_remaining_compound_error":F(target)-(A+B),
            "INDEPENDENT_A":ind_A,"INDEPENDENT_B":ind_B}

def simulate(alpha,npre,target,m):
    if (alpha,npre,target) not in WORLDS or m not in STAGES:raise ValueError("unfrozen model source")
    A=initial_p(alpha,npre);B=Z
    C=A;D=Z
    for _ in range(m):
        shared=F(target)-(A+B)
        A+=alpha*shared
        B+=alpha*shared
        C+=alpha*(F(target)-C)
        D+=alpha*(F(target)-D)
    return {"pretrained_A":initial_p(alpha,npre),"RW_A":A,"RW_B":B,
            "RW_compound_sum":A+B,"RW_remaining_compound_error":F(target)-(A+B),
            "INDEPENDENT_A":C,"INDEPENDENT_B":D}

def row(alpha,npre,target,m):
    expected=formula(alpha,npre,target,m)
    actual=simulate(alpha,npre,target,m)
    if actual!=expected:raise AssertionError("independent recurrence disagrees with analytic expression")
    return {"world":world_id(alpha,npre,target),"alpha":alpha,
      "A_only_pretraining_trials":npre,"compound_reward_target":target,
      "compound_training_trials":m,**actual}

def rows():return tuple(row(a,n,r,m) for a,n,r in WORLDS for m in STAGES)

def blocking(alpha):
    return row(alpha,8,1,4)["RW_B"]<row(alpha,0,1,4)["RW_B"]

def unblocking(alpha):
    return row(alpha,8,2,4)["RW_B"]>row(alpha,8,1,4)["RW_B"]

def verify():
    assert len(WORLDS)==8 and len(rows())==40
    assert len(set((r["world"],r["compound_training_trials"]) for r in rows()))==40
    for alpha,npre,target in WORLDS:
        p=initial_p(alpha,npre)
        assert p==O-(O-alpha)**npre
        vals=[row(alpha,npre,target,m) for m in STAGES]
        for m,x in enumerate(vals):
            assert x["RW_A"]-x["RW_B"]==p
            assert x["RW_compound_sum"]==x["RW_A"]+x["RW_B"]
            assert x["RW_remaining_compound_error"]==target-x["RW_compound_sum"]
            assert x["INDEPENDENT_B"]==F(target)*(O-(O-alpha)**m)
            if m==0:assert x["RW_B"]==x["INDEPENDENT_B"]==Z
            if m<4:
                y=vals[m+1]
                assert y["RW_A"]-x["RW_A"]==alpha*x["RW_remaining_compound_error"]
                assert y["RW_B"]-x["RW_B"]==alpha*x["RW_remaining_compound_error"]
                assert y["INDEPENDENT_A"]-x["INDEPENDENT_A"]==alpha*(target-x["INDEPENDENT_A"])
                assert y["INDEPENDENT_B"]-x["INDEPENDENT_B"]==alpha*(target-x["INDEPENDENT_B"])
    assert all(blocking(a) for a in ALPHAS)
    assert all(unblocking(a) for a in ALPHAS)
    assert initial_p(F(1,2),8)==F(255,256)
    assert row(F(1,2),8,1,4)["RW_B"]==F(1,512)
    assert row(F(1,2),0,1,4)["RW_B"]==F(1,2)
    assert row(F(1,2),8,2,4)["RW_B"]==F(257,512)
    assert row(F(1,2),8,1,4)["INDEPENDENT_B"]==row(F(1,2),0,1,4)["INDEPENDENT_B"]==F(15,16)
    return True

def emit():
    verify()
    fields=("world","alpha","A_only_pretraining_trials","compound_reward_target",
            "compound_training_trials","pretrained_A","RW_A","RW_B","RW_compound_sum",
            "RW_remaining_compound_error","INDEPENDENT_A","INDEPENDENT_B")
    csvpath=ROOT/CSV_NAME
    with csvpath.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader()
        for r in rows():w.writerow({field:str(r[field]) for field in fields})
    records=[]
    for a,n,t in WORLDS:
        series=[row(a,n,t,m) for m in STAGES]
        records.append({"world":world_id(a,n,t),"alpha":str(a),"pretraining_trials":n,
             "compound_reward_target":t,"original_source_rows":5,"stages":[{
                "m":m,"pretrained_A":str(item["pretrained_A"]),
                "RW_A":str(item["RW_A"]),"RW_B":str(item["RW_B"]),
                "RW_compound_sum":str(item["RW_compound_sum"]),
                "RW_remaining_compound_error":str(item["RW_remaining_compound_error"]),
                "INDEPENDENT_A":str(item["INDEPENDENT_A"]),
                "INDEPENDENT_B":str(item["INDEPENDENT_B"])} for m,item in enumerate(series)]})
    result={"research_id":"R296","original_catalogue_id":"02-001","freeze_commit":FREEZE,
       "scope":"EXACT_ARTIFICIAL_RW_COMPOUND_CUE_BLOCKING_UNBLOCKING_NOT_AUTHOR_ANIMAL_EXPERIMENT_REPRODUCTION",
       "world_count":8,"complete_artificial_source_rows":40,"source_states_per_world":5,
       "blocking_under_A_pretraining_for_both_alphas":all(blocking(a) for a in ALPHAS),
       "unblocking_under_reward_upshift_for_both_alphas":all(unblocking(a) for a in ALPHAS),
       "reference_alpha_half":{
         "A_after_eight_pretrain":"255/256",
         "RW_B_after_pretrain_reinforced_AB_four":"1/512",
         "RW_B_without_pretrain_reinforced_AB_four":"1/2",
         "RW_B_after_pretrain_AB_reward_double_four":"257/512",
         "independent_B_pretraining_invariant_with_AB_reward_one":"15/16"},
       "worlds":records,"new_real_human_E2":0,"new_real_animal_E2":0,
       "new_historical_E3":0,"R073":"FROZEN","PESEN_v0_1":"FROZEN"}
    resultpath=ROOT/RESULT_NAME
    resultpath.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R296","freeze_commit":FREEZE,"complete_artificial_sources":40,
       "source_sha256":hashlib.sha256(csvpath.read_bytes()).hexdigest(),
       "results_sha256":hashlib.sha256(resultpath.read_bytes()).hexdigest(),
       "E2_added":0,"E3_added":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_all(self):self.assertTrue(verify())
    def test_count(self):self.assertEqual(len(rows()),40)
    def test_worlds(self):self.assertEqual(len(WORLDS),8)
    def test_blocking_each_alpha(self):self.assertTrue(all(blocking(a) for a in ALPHAS))
    def test_upshift_each_alpha(self):self.assertTrue(all(unblocking(a) for a in ALPHAS))
    def test_independent_neg_control(self):self.assertEqual(row(F(1,2),8,1,4)["INDEPENDENT_B"],row(F(1,2),0,1,4)["INDEPENDENT_B"])
    def test_special_blocked(self):self.assertEqual(row(F(1,2),8,1,4)["RW_B"],F(1,512))
    def test_special_unblocked(self):self.assertEqual(row(F(1,2),8,2,4)["RW_B"],F(257,512))
    def test_bad_alpha(self):
        with self.assertRaises(ValueError):initial_p(F(1,3),8)
    def test_bad_stage(self):
        with self.assertRaises(ValueError):row(F(1,4),8,1,5)
    def test_bad_target(self):
        with self.assertRaises(ValueError):row(F(1,4),8,3,4)
def generated(a,n,t,m,kind):
    def check(self):
        r=row(a,n,t,m);e=formula(a,n,t,m)
        if kind=="source":self.assertEqual({k:r[k] for k in e},e)
        elif kind=="sum":self.assertEqual(r["RW_compound_sum"],r["RW_A"]+r["RW_B"])
        elif kind=="difference":self.assertEqual(r["RW_A"]-r["RW_B"],r["pretrained_A"])
        elif kind=="independent":self.assertEqual(r["INDEPENDENT_B"],F(t)*(O-(O-a)**m))
        elif kind=="error":self.assertEqual(r["RW_remaining_compound_error"],t-r["RW_compound_sum"])
        else:raise AssertionError(kind)
    return check
for i,(alpha,pre,target) in enumerate(WORLDS):
    for m in STAGES:
        for kind in ("source","sum","difference","independent","error"):
            setattr(Tests,f"test_world{i}_m{m}_{kind}",generated(alpha,pre,target,m,kind))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R296"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
