#!/usr/bin/env python3
"""R292 synthetic TPB control calibration. C is perceived; F actual feasibility."""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import unittest
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="eaec7179a52e01fa86130e7c496c620093205500"
Z,O=Q(0),Q(1)
PROFILES={"BALANCED":(1,1,1),"CONTROL_HEAVY":(1,1,2),
          "CONTROL_NULL":(1,1,0),"NORM_HEAVY":(1,2,1)}
CALIBRATIONS={0:"UNINFORMATIVE",1:"INFORMATIVE"}
WORLDS=tuple((name,k) for name in PROFILES for k in CALIBRATIONS)
SOURCES=tuple(itertools.product((-1,1),(-1,1),(-1,1),(0,1),(0,1)))
FORECASTERS=("FULL_ANC","TRA_AN","CONTROL_ONLY_C","CONSTANT")
SOURCE_CSV="R292_ALL_256_ORIGINAL_TPB_CONTROL_FEASIBILITY_SOURCES.csv"
RESULT_JSON="R292_EXACT_CONTROL_RESULTS.json"
RECEIPT_JSON="R292_MACHINE_RECEIPT.json"

def validate_world(name,k):
    if (name,k) not in WORLDS:raise ValueError("unfrozen TPB artificial world")

def intent_probability(name,k,A,N,C):
    validate_world(name,k)
    if A not in (-1,1) or N not in (-1,1) or C not in (-1,1):raise ValueError("bad attitude, norm or perceived control")
    a,n,c=PROFILES[name]
    return Q(1,2)+Q(a*A+n*N+c*C,16)

def actual_feasibility_probability(name,k,C):
    validate_world(name,k)
    if C not in (-1,1):raise ValueError("bad perceived control")
    return Q(1,2)+Q(k*C,4)

def probability_action_before_intent(name,k,A,N,C):
    return intent_probability(name,k,A,N,C)*actual_feasibility_probability(name,k,C)

def forecasts(name,k,A,N,C):
    validate_world(name,k)
    a,n,c=PROFILES[name]
    mu=Q(1,4)+Q(c*k,64)
    return {"FULL_ANC":probability_action_before_intent(name,k,A,N,C),
       "TRA_AN":mu+Q(a*A+n*N,32),
       "CONTROL_ONLY_C":(Q(1,2)+Q(c*C,16))*(Q(1,2)+Q(k*C,4)),
       "CONSTANT":mu}

def source_row(name,k,A,N,C,I,F):
    validate_world(name,k)
    if (A,N,C,I,F) not in SOURCES:raise ValueError("bad complete joint source")
    pi=intent_probability(name,k,A,N,C)
    pf=actual_feasibility_probability(name,k,C)
    joint=Q(1,8)*(pi if I else O-pi)*(pf if F else O-pf)
    B=I*F
    predictions=forecasts(name,k,A,N,C)
    row={"world":name+"__"+CALIBRATIONS[k],"profile":name,
         "control_calibration":CALIBRATIONS[k],"kappa":k,
         "attitude":A,"subjective_norm":N,"perceived_control":C,
         "intention":I,"actual_feasibility":F,"behavior":B,
         "joint_source_probability":joint,"p_intention_1":pi,"p_actual_feasibility_1":pf,
         "true_p_behavior_1_pre_intention":predictions["FULL_ANC"]}
    for f in FORECASTERS:row["forecast_"+f]=predictions[f]
    return row

def source_rows(name,k):
    return tuple(source_row(name,k,*s) for s in SOURCES)

def source_brier_risks(name,k):
    rs=source_rows(name,k)
    assert len(rs)==32 and sum((x["joint_source_probability"] for x in rs),Z)==O
    return {f:sum((r["joint_source_probability"]*(Q(r["behavior"])-r["forecast_"+f])**2 for r in rs),Z) for f in FORECASTERS}

def analytic_brier_risks(name,k):
    validate_world(name,k)
    a,n,c=PROFILES[name]
    mu=Q(1,4)+Q(c*k,64)
    r0=mu*(O-mu)
    v_an=Q(a*a+n*n,1024)
    v_c=Q((4*k+c)**2,1024)
    v_interaction=Q(k*k*(a*a+n*n),4096)
    return {"FULL_ANC":r0-v_an-v_c-v_interaction,
            "TRA_AN":r0-v_an,
            "CONTROL_ONLY_C":r0-v_c,
            "CONSTANT":r0}

def verify():
    assert len(WORLDS)==8 and len(SOURCES)==32
    total=0
    for name,k in WORLDS:
        rows=source_rows(name,k)
        total+=len(rows)
        assert all(x["joint_source_probability"]>0 for x in rows)
        assert all(x["behavior"]==x["intention"]*x["actual_feasibility"] for x in rows)
        assert source_brier_risks(name,k)==analytic_brier_risks(name,k)
        r=source_brier_risks(name,k)
        assert r["FULL_ANC"]<=r["TRA_AN"]<=r["CONSTANT"]
        assert r["FULL_ANC"]<=r["CONTROL_ONLY_C"]<=r["CONSTANT"]
        for A,N,C in itertools.product((-1,1),repeat=3):
            forecast=forecasts(name,k,A,N,C)
            assert all(Z<=x<=O for x in forecast.values())
            pi=intent_probability(name,k,A,N,C)
            pf=actual_feasibility_probability(name,k,C)
            assert probability_action_before_intent(name,k,A,N,C)==pi*pf
            assert all(Z<q<O for q in (pi,pf))
    assert total==256
    assert source_brier_risks("CONTROL_NULL",0)["TRA_AN"]==source_brier_risks("CONTROL_NULL",0)["FULL_ANC"]
    null_one=source_brier_risks("CONTROL_NULL",1)
    assert null_one["TRA_AN"]-null_one["FULL_ANC"]==Q(1,64)+Q(2,4096)
    for name in PROFILES:
        for k in CALIBRATIONS:
            assert actual_feasibility_probability(name,k,1)-actual_feasibility_probability(name,k,-1)==Q(k,2)
    return True

def emit():
    verify()
    fields=("world","profile","control_calibration","kappa","attitude","subjective_norm",
       "perceived_control","intention","actual_feasibility","behavior",
       "joint_source_probability","p_intention_1","p_actual_feasibility_1",
       "true_p_behavior_1_pre_intention",*(("forecast_"+f) for f in FORECASTERS))
    csv_path=ROOT/SOURCE_CSV
    with csv_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        w.writeheader()
        for name,k in WORLDS:
            for r in source_rows(name,k):w.writerow({field:str(r[field]) for field in fields})
    output={"research_id":"R292","original_catalogue_id":"01-014","freeze_commit":FREEZE,
      "scope":"SYNTHETIC_E1_TPB_PERCEIVED_CONTROL_VS_ACTUAL_FEASIBILITY",
      "worlds_count":8,"original_positive_source_cells":256,
      "new_real_human_E2":0,"new_historical_E3":0,"R073":"FROZEN","PESEN_v0_1":"FROZEN",
      "worlds":[]}
    for name,k in WORLDS:
        a,n,c=PROFILES[name]
        r=source_brier_risks(name,k)
        output["worlds"].append({"world":name+"__"+CALIBRATIONS[k],
          "profile":name,"calibration":CALIBRATIONS[k],"kappa":k,
          "a":a,"n":n,"c":c,"complete_source_cells":32,
          "source_mass":"1","Brier_risk":{key:str(value) for key,value in r.items()},
          "omitting_perceived_control_excess_risk":str(r["TRA_AN"]-r["FULL_ANC"]),
          "behavior_given_intention_1_control_contrast":str(Q(k,2)),
          "behavior_given_intention_0_control_contrast":"0",
          "matches_independent_closed_form":r==analytic_brier_risks(name,k)})
    json_path=ROOT/RESULT_JSON
    json_path.write_text(json.dumps(output,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt={"research_id":"R292","freeze_commit":FREEZE,"positive_source_cells":256,
       "sources_sha256":hashlib.sha256(csv_path.read_bytes()).hexdigest(),
       "results_sha256":hashlib.sha256(json_path.read_bytes()).hexdigest(),
       "new_real_human_E2":0,"new_historical_E3":0}
    (ROOT/RECEIPT_JSON).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_full_claims(self):self.assertTrue(verify())
    def test_world_count(self):self.assertEqual(len(WORLDS),8)
    def test_source_count(self):self.assertEqual(len(SOURCES),32)
    def test_no_perceived_equals_actual(self):self.assertTrue(any(s[-1]!=s[2] for s in SOURCES))
    def test_behavior_gate(self):self.assertEqual(source_row("BALANCED",0,1,1,1,1,0)["behavior"],0)
    def test_no_control_null_penalty(self):self.assertEqual(source_brier_risks("CONTROL_NULL",0)["TRA_AN"],source_brier_risks("CONTROL_NULL",0)["FULL_ANC"])
    def test_control_informative_null_penalty(self):self.assertEqual(source_brier_risks("CONTROL_NULL",1)["TRA_AN"]-source_brier_risks("CONTROL_NULL",1)["FULL_ANC"],Q(33,2048))
    def test_unfrozen_profile(self):
        with self.assertRaises(ValueError):intent_probability("WRONG",1,1,1,1)
    def test_unfrozen_calibration(self):
        with self.assertRaises(ValueError):actual_feasibility_probability("BALANCED",2,1)
    def test_bad_perceived_value(self):
        with self.assertRaises(ValueError):actual_feasibility_probability("BALANCED",1,0)

def make(name,k,kind):
    def test(self):
        rows=source_rows(name,k)
        score=source_brier_risks(name,k)
        a,n,c=PROFILES[name]
        if kind=="size":self.assertEqual(len(rows),32)
        elif kind=="mass":self.assertEqual(sum((r["joint_source_probability"] for r in rows),Z),O)
        elif kind=="allpositive":self.assertTrue(all(r["joint_source_probability"]>0 for r in rows))
        elif kind=="unique":self.assertEqual(len(set((r["attitude"],r["subjective_norm"],r["perceived_control"],r["intention"],r["actual_feasibility"]) for r in rows)),32)
        elif kind=="gate":self.assertTrue(all(r["behavior"]==r["intention"]*r["actual_feasibility"] for r in rows))
        elif kind=="analytic":self.assertEqual(score,analytic_brier_risks(name,k))
        elif kind=="constants":self.assertEqual(score["CONSTANT"],(Q(1,4)+Q(c*k,64))*(Q(3,4)-Q(c*k,64)))
        elif kind=="control_gap":self.assertEqual(score["TRA_AN"]-score["FULL_ANC"],Q((4*k+c)**2,1024)+Q(k*k*(a*a+n*n),4096))
        elif kind=="pre_intention":self.assertTrue(all(r["true_p_behavior_1_pre_intention"]==r["forecast_FULL_ANC"] for r in rows))
        elif kind=="bounded":self.assertTrue(all(Z<r["joint_source_probability"]<O for r in rows))
        elif kind=="control_conditional":self.assertEqual(actual_feasibility_probability(name,k,1)-actual_feasibility_probability(name,k,-1),Q(k,2))
        elif kind=="loss_order":self.assertLessEqual(score["FULL_ANC"],score["TRA_AN"])
        else:raise AssertionError(kind)
    return test

for _name,_k in WORLDS:
    for _kind in ("size","mass","allpositive","unique","gate","analytic","constants","control_gap","pre_intention","bounded","control_conditional","loss_order"):
        setattr(Tests,"test_"+_name.lower()+"_"+str(_k)+"_"+_kind,make(_name,_k,_kind))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R292"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
