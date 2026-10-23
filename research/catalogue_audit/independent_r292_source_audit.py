#!/usr/bin/env python3
"""Independent R292 complete original source verifier; no production module imports."""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import itertools
import json
import unittest
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R292"
CSV=ROOT/"R292_ALL_256_ORIGINAL_TPB_CONTROL_FEASIBILITY_SOURCES.csv"
JSON=ROOT/"R292_EXACT_CONTROL_RESULTS.json"
RECEIPT=ROOT/"R292_MACHINE_RECEIPT.json"
PROFILES={"BALANCED":(1,1,1),"CONTROL_HEAVY":(1,1,2),"CONTROL_NULL":(1,1,0),"NORM_HEAVY":(1,2,1)}
MODES={0:"UNINFORMATIVE",1:"INFORMATIVE"}
WORLDS=[(n,k) for n in PROFILES for k in MODES]
CELLS=set(itertools.product((-1,1),repeat=3))
FULL=set(itertools.product((-1,1),(-1,1),(-1,1),(0,1),(0,1)))
FORECASTERS=("FULL_ANC","TRA_AN","CONTROL_ONLY_C","CONSTANT")
Z,O=Q(0),Q(1)

def loadobj(p):return json.loads(p.read_text(encoding="utf-8"))
def loadcsv():
    with CSV.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def recalc(name,k,A,N,C,I,F):
    a,n,c=PROFILES[name]
    p_i=Q(8+a*A+n*N+c*C,16)
    p_f=Q(2+k*C,4)
    b=I*F
    w=Q(1,8)*(p_i if I else O-p_i)*(p_f if F else O-p_f)
    conditional=p_i*p_f
    constant=Q(1,4)+Q(c*k,64)
    preds={"FULL_ANC":conditional,
           "TRA_AN":constant+Q(a*A+n*N,32),
           "CONTROL_ONLY_C":Q(8+c*C,16)*p_f,
           "CONSTANT":constant}
    return b,w,p_i,p_f,preds

def independent_verification(rows,results):
    if len(rows)!=256:raise AssertionError("source count must be exactly 256")
    if len(results["worlds"])!=8:raise AssertionError("results count must be eight worlds")
    by=collections.defaultdict(list)
    for row in rows:
        name=row["profile"]
        k=int(row["kappa"])
        if (name,k) not in WORLDS:raise AssertionError("unexpected world name")
        if row["world"]!=name+"__"+MODES[k] or row["control_calibration"]!=MODES[k]:raise AssertionError("mismatched calibration label")
        A,N,C,I,F=(int(row[x]) for x in ("attitude","subjective_norm","perceived_control","intention","actual_feasibility"))
        if (A,N,C,I,F) not in FULL:raise AssertionError("invalid combination")
        b,w,p_i,p_f,preds=recalc(name,k,A,N,C,I,F)
        if int(row["behavior"])!=b:raise AssertionError("actual feasibility gate violated")
        if Q(row["joint_source_probability"])!=w:raise AssertionError("source probability incorrect")
        if Q(row["p_intention_1"])!=p_i or Q(row["p_actual_feasibility_1"])!=p_f:raise AssertionError("conditional probability mismatch")
        if Q(row["true_p_behavior_1_pre_intention"])!=preds["FULL_ANC"]:raise AssertionError("pre-intention probability mismatch")
        for key in FORECASTERS:
            if Q(row["forecast_"+key])!=preds[key]:raise AssertionError("predictor incorrect: "+key)
        by[(name,k)].append((A,N,C,I,F,b,w,preds))
    for pos,(name,k) in enumerate(WORLDS):
        arr=by[(name,k)]
        if len(arr)!=32 or set((A,N,C,I,F) for A,N,C,I,F,_,_,_ in arr)!=FULL:raise AssertionError("duplicate/missing complete source cell")
        if sum((x[6] for x in arr),Z)!=O:raise AssertionError("source does not integrate to 1")
        a,n,c=PROFILES[name]
        mu=Q(1,4)+Q(c*k,64)
        r_const=mu*(O-mu)
        v_an=Q(a*a+n*n,1024)
        v_c=Q((4*k+c)**2,1024)
        cross=Q(k*k*(a*a+n*n),4096)
        expected={"FULL_ANC":r_const-v_an-v_c-cross,
                  "TRA_AN":r_const-v_an,
                  "CONTROL_ONLY_C":r_const-v_c,
                  "CONSTANT":r_const}
        risks={key:sum((w*(Q(b)-pred[key])**2 for A,N,C,I,F,b,w,pred in arr),Z) for key in FORECASTERS}
        if risks!=expected:raise AssertionError("exact Brier formula wrong")
        result=results["worlds"][pos]
        if result["world"]!=name+"__"+MODES[k] or result["kappa"]!=k:raise AssertionError("wrong result world")
        if (result["a"],result["n"],result["c"])!=(a,n,c):raise AssertionError("weight mismatch")
        if result["complete_source_cells"]!=32 or result["source_mass"]!="1":raise AssertionError("source count or mass metadata")
        if result["Brier_risk"]!={key:str(v) for key,v in risks.items()}:raise AssertionError("result JSON risk mismatch")
        if Q(result["omitting_perceived_control_excess_risk"])!=v_c+cross:raise AssertionError("control effect mismatch")
        if Q(result["behavior_given_intention_1_control_contrast"])!=Q(k,2):raise AssertionError("positive intent control contrast")
        if result["behavior_given_intention_0_control_contrast"]!="0" or result["matches_independent_closed_form"] is not True:raise AssertionError("negative intent control contrast")
    return {"original_joint_source_cells":256,"independently_checked_worlds":8,"Brier_exact_forecast_evaluations":32,"perceived_vs_actual_control_separate":True,"added_human_E2":0,"added_historical_E3":0}

def audit():
    result,receipt=loadobj(JSON),loadobj(RECEIPT)
    assert result["original_catalogue_id"]=="01-014"
    assert result["original_positive_source_cells"]==256 and receipt["positive_source_cells"]==256
    assert receipt["freeze_commit"]==result["freeze_commit"]=="eaec7179a52e01fa86130e7c496c620093205500"
    assert receipt["new_real_human_E2"]==receipt["new_historical_E3"]==0
    assert hashlib.sha256(CSV.read_bytes()).hexdigest()==receipt["sources_sha256"]
    assert hashlib.sha256(JSON.read_bytes()).hexdigest()==receipt["results_sha256"]
    return {**independent_verification(loadcsv(),result),
            "source_sha256":receipt["sources_sha256"],
            "results_sha256":receipt["results_sha256"]}

class Tests(unittest.TestCase):
    def test_full(self):self.assertEqual(audit()["original_joint_source_cells"],256)
    def test_worlds(self):self.assertEqual(len(WORLDS),8)
    def test_cells(self):self.assertEqual(len(FULL),32)
    def test_control_proxy_differs_actual(self):self.assertEqual(recalc("BALANCED",1,1,1,1,1,0)[0],0)
    def test_control_informative(self):self.assertEqual(recalc("BALANCED",1,1,1,1,1,1)[3]-recalc("BALANCED",1,1,1,-1,1,1)[3],Q(1,2))
    def test_control_uninformative(self):self.assertEqual(recalc("BALANCED",0,1,1,1,1,1)[3]-recalc("BALANCED",0,1,1,-1,1,1)[3],Z)
    def test_reject_missing_row(self):
        with self.assertRaises(AssertionError):independent_verification(loadcsv()[:-1],loadobj(JSON))
    def test_reject_duplicate_row(self):
        rows=loadcsv()
        rows[1]=dict(rows[0])
        with self.assertRaises(AssertionError):independent_verification(rows,loadobj(JSON))
    def test_reject_changed_joint_mass(self):
        rows=loadcsv();rows[0]=dict(rows[0]);rows[0]["joint_source_probability"]="0"
        with self.assertRaises(AssertionError):independent_verification(rows,loadobj(JSON))
    def test_reject_fake_actual_behavior(self):
        rows=loadcsv();rows[0]=dict(rows[0]);rows[0]["behavior"]=str(1-int(rows[0]["behavior"]))
        with self.assertRaises(AssertionError):independent_verification(rows,loadobj(JSON))
    def test_reject_fake_perceived_control(self):
        rows=loadcsv();rows[0]=dict(rows[0]);rows[0]["perceived_control"]="0"
        with self.assertRaises(AssertionError):independent_verification(rows,loadobj(JSON))
    def test_reject_fake_forecast(self):
        rows=loadcsv();rows[0]=dict(rows[0]);rows[0]["forecast_FULL_ANC"]="0"
        with self.assertRaises(AssertionError):independent_verification(rows,loadobj(JSON))
    def test_reject_result_tamper(self):
        d=loadobj(JSON)
        d["worlds"][0]["Brier_risk"]["FULL_ANC"]="0"
        with self.assertRaises(AssertionError):independent_verification(loadcsv(),d)
    def test_byte_tamper(self):self.assertNotEqual(hashlib.sha256(CSV.read_bytes()+b"x").hexdigest(),loadobj(RECEIPT)["sources_sha256"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R292audit"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
