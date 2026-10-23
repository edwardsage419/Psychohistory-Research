#!/usr/bin/env python3
"""R291 synthetic TRA mediation and direct-norm negative control; no human data."""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="161d40a01451f1e89be045910f95ec536768754c"
Z,O=F(0),F(1)
PROFILES={"BALANCED":(1,1),"ATTITUDE_HEAVY":(2,1),"NORM_HEAVY":(1,2),"NORM_NULL":(2,0)}
MODES=("MEDIATED","DIRECT_NORM_STRESS")
WORLDS=tuple((name,mode) for name in PROFILES for mode in MODES)
CELLS=tuple(itertools.product((-1,1),(-1,1),(0,1),(0,1)))
FORECASTERS=("FULL_AN","ATTITUDE_ONLY","NORM_ONLY","CONSTANT")
CSV_NAME="R291_ALL_128_ORIGINAL_TRA_LABELED_JOINT_SOURCES.csv"
RESULT_NAME="R291_EXACT_TRA_RESULTS.json"
RECEIPT_NAME="R291_MACHINE_RECEIPT.json"

def check(name,mode):
    if (name,mode) not in WORLDS:raise ValueError("unfrozen R291 profile or behavior mode")

def cpar(name,mode):
    check(name,mode)
    a,n=PROFILES[name]
    return a,n,int(mode=="DIRECT_NORM_STRESS")

def probability_intention(name,mode,A,N):
    a,n,_=cpar(name,mode)
    if A not in (-1,1) or N not in (-1,1):raise ValueError("invalid A,N")
    return F(1,2)+F(a*A+n*N,8)

def probability_behavior_given_intent(name,mode,I,A,N):
    _,_,d=cpar(name,mode)
    if I not in (0,1) or A not in (-1,1) or N not in (-1,1):raise ValueError("invalid latent state")
    return F(1,4)+F(I,2)+F(d*N,8)

def probability_behavior_pre_intent(name,mode,A,N):
    a,n,d=cpar(name,mode)
    if A not in (-1,1) or N not in (-1,1):raise ValueError("invalid features")
    return F(1,2)+F(a*A+(n+2*d)*N,16)

def forecasts(name,mode,A,N):
    a,n,d=cpar(name,mode)
    return {
        "FULL_AN":probability_behavior_pre_intent(name,mode,A,N),
        "ATTITUDE_ONLY":F(1,2)+F(a*A,16),
        "NORM_ONLY":F(1,2)+F((n+2*d)*N,16),
        "CONSTANT":F(1,2)
    }

def source_row(name,mode,A,N,I,B):
    check(name,mode)
    if (A,N,I,B) not in CELLS:raise ValueError("invalid full labeled cell")
    pi=probability_intention(name,mode,A,N)
    pb=probability_behavior_given_intent(name,mode,I,A,N)
    weight=F(1,4)*(pi if I else O-pi)*(pb if B else O-pb)
    q=forecasts(name,mode,A,N)
    row={"world":name+"__"+mode,"profile":name,"mode":mode,
         "attitude":A,"subjective_norm":N,"intention":I,"behavior":B,
         "joint_source_probability":weight,"p_intention_1_given_A_N":pi,
         "p_behavior_1_given_I_A_N":pb,"p_behavior_1_pre_intention_A_N":q["FULL_AN"]}
    for k in FORECASTERS:row["forecast_"+k]=q[k]
    return row

def source_rows(name,mode):
    return tuple(source_row(name,mode,*cell) for cell in CELLS)

def brier(b,q):return (F(b)-q)**2

def exact_source_risks(name,mode):
    rows=source_rows(name,mode)
    assert len(rows)==16
    assert sum((r["joint_source_probability"] for r in rows),Z)==O
    return {k:sum((r["joint_source_probability"]*brier(r["behavior"],r["forecast_"+k]) for r in rows),Z)
            for k in FORECASTERS}

def analytic_risks(name,mode):
    a,n,d=cpar(name,mode)
    coeff=n+2*d
    full=F(1,4)-F(a*a+coeff*coeff,256)
    return {"FULL_AN":full,"ATTITUDE_ONLY":full+F(coeff*coeff,256),
            "NORM_ONLY":full+F(a*a,256),"CONSTANT":F(1,4)}

def mediation_contrasts(name,mode):
    check(name,mode)
    return tuple(probability_behavior_given_intent(name,mode,I,A,1)-
                 probability_behavior_given_intent(name,mode,I,A,-1)
                 for A in (-1,1) for I in (0,1))

def validate_all():
    assert len(WORLDS)==8 and len(CELLS)==16
    total=0
    for name,mode in WORLDS:
        rows=source_rows(name,mode)
        total+=len(rows)
        assert all(r["joint_source_probability"]>0 for r in rows)
        assert sum((r["joint_source_probability"] for r in rows),Z)==O
        assert exact_source_risks(name,mode)==analytic_risks(name,mode)
        d=int(mode=="DIRECT_NORM_STRESS")
        assert set(mediation_contrasts(name,mode))=={F(d,4)}
        for A in (-1,1):
            for N in (-1,1):
                pi=probability_intention(name,mode,A,N)
                mixture=(O-pi)*probability_behavior_given_intent(name,mode,0,A,N)+pi*probability_behavior_given_intent(name,mode,1,A,N)
                assert mixture==probability_behavior_pre_intent(name,mode,A,N)
                assert all(Z<=q<=O for q in forecasts(name,mode,A,N).values())
        risks=exact_source_risks(name,mode)
        assert risks["FULL_AN"]<=risks["ATTITUDE_ONLY"]<=risks["CONSTANT"]
        assert risks["FULL_AN"]<=risks["NORM_ONLY"]<=risks["CONSTANT"]
    assert total==128
    assert exact_source_risks("NORM_NULL","MEDIATED")["ATTITUDE_ONLY"]==exact_source_risks("NORM_NULL","MEDIATED")["FULL_AN"]
    s=exact_source_risks("NORM_NULL","DIRECT_NORM_STRESS")
    assert s["ATTITUDE_ONLY"]-s["FULL_AN"]==F(1,64)
    assert exact_source_risks("ATTITUDE_HEAVY","MEDIATED")["NORM_ONLY"]-exact_source_risks("ATTITUDE_HEAVY","MEDIATED")["FULL_AN"]==F(1,64)
    assert exact_source_risks("NORM_HEAVY","MEDIATED")["ATTITUDE_ONLY"]-exact_source_risks("NORM_HEAVY","MEDIATED")["FULL_AN"]==F(1,64)
    return True

def emit():
    validate_all()
    cols=("world","profile","mode","attitude","subjective_norm","intention","behavior",
          "joint_source_probability","p_intention_1_given_A_N","p_behavior_1_given_I_A_N",
          "p_behavior_1_pre_intention_A_N",*(("forecast_"+k) for k in FORECASTERS))
    data_path=ROOT/CSV_NAME
    with data_path.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        writer.writeheader()
        for name,mode in WORLDS:
            for row in source_rows(name,mode):writer.writerow({k:str(row[k]) for k in cols})
    results={"research_id":"R291","catalogue_original_id":"01-013","freeze_commit":FREEZE,
      "scope":"BOUNDED_ARTIFICIAL_E1_TRA_ARCHITECTURE_NOT_ORIGINAL_HUMAN_FIT",
      "world_count":len(WORLDS),"fully_labeled_joint_source_cells":128,
      "new_human_E2":0,"new_historical_E3":0,"R073":"FROZEN","PESEN_v0_1":"FROZEN",
      "worlds":[]}
    for name,mode in WORLDS:
        a,n,d=cpar(name,mode)
        risks=exact_source_risks(name,mode)
        results["worlds"].append({"world":name+"__"+mode,"profile":name,"mode":mode,
         "attitude_weight_a":a,"norm_weight_n":n,"behavior_direct_norm_d":d,
         "labeled_source_cells":16,"full_source_mass":"1",
         "risks_Brier":{key:str(val) for key,val in risks.items()},
         "regret_attitude_only":str(risks["ATTITUDE_ONLY"]-risks["FULL_AN"]),
         "regret_norm_only":str(risks["NORM_ONLY"]-risks["FULL_AN"]),
         "regret_constant":str(risks["CONSTANT"]-risks["FULL_AN"]),
         "given_intention_norm_contrast":str(mediation_contrasts(name,mode)[0]),
         "analytic_risk_agreement":risks==analytic_risks(name,mode)})
    result_path=ROOT/RESULT_NAME
    result_path.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt={"research_id":"R291","freeze_commit":FREEZE,"source_cells":128,
     "sources_sha256":hashlib.sha256(data_path.read_bytes()).hexdigest(),
     "results_sha256":hashlib.sha256(result_path.read_bytes()).hexdigest(),
     "new_human_E2":0,"new_historical_E3":0}
    (ROOT/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_overall(self):self.assertTrue(validate_all())
    def test_worlds(self):self.assertEqual(len(WORLDS),8)
    def test_complete_cells(self):self.assertEqual(len(CELLS),16)
    def test_negative_control_norm_null(self):self.assertEqual(exact_source_risks("NORM_NULL","MEDIATED")["FULL_AN"],exact_source_risks("NORM_NULL","MEDIATED")["ATTITUDE_ONLY"])
    def test_positive_direct_contrast(self):self.assertEqual(set(mediation_contrasts("BALANCED","DIRECT_NORM_STRESS")),{F(1,4)})
    def test_zero_direct_contrast(self):self.assertEqual(set(mediation_contrasts("BALANCED","MEDIATED")),{Z})
    def test_no_post_intention_leak(self):self.assertEqual(set(forecasts("BALANCED","MEDIATED",1,1)),set(FORECASTERS))
    def test_bad_profile(self):
        with self.assertRaises(ValueError):probability_intention("UNKNOWN","MEDIATED",1,1)
    def test_bad_mode(self):
        with self.assertRaises(ValueError):probability_intention("BALANCED","UNFROZEN",1,1)
    def test_bad_feature(self):
        with self.assertRaises(ValueError):probability_behavior_pre_intent("BALANCED","MEDIATED",0,1)

def _make(name,mode,kind):
    def check_case(self):
        rows=source_rows(name,mode)
        risks=exact_source_risks(name,mode)
        if kind=="mass":self.assertEqual(sum((r["joint_source_probability"] for r in rows),Z),O)
        elif kind=="size":self.assertEqual(len(rows),16)
        elif kind=="positive":self.assertTrue(all(r["joint_source_probability"]>0 for r in rows))
        elif kind=="unique":self.assertEqual(len(set((r["attitude"],r["subjective_norm"],r["intention"],r["behavior"]) for r in rows)),16)
        elif kind=="analytic":self.assertEqual(risks,analytic_risks(name,mode))
        elif kind=="mediation":self.assertEqual(set(mediation_contrasts(name,mode)),{F(int(mode=="DIRECT_NORM_STRESS"),4)})
        elif kind=="base":self.assertEqual(risks["CONSTANT"],F(1,4))
        elif kind=="attitude_regret":
            a,n,d=cpar(name,mode)
            self.assertEqual(risks["ATTITUDE_ONLY"]-risks["FULL_AN"],F((n+2*d)**2,256))
        elif kind=="norm_regret":
            a,n,d=cpar(name,mode)
            self.assertEqual(risks["NORM_ONLY"]-risks["FULL_AN"],F(a*a,256))
        elif kind=="constant_regret":
            a,n,d=cpar(name,mode)
            self.assertEqual(risks["CONSTANT"]-risks["FULL_AN"],F(a*a+(n+2*d)**2,256))
        elif kind=="prob_bounds":self.assertTrue(all(Z<r["joint_source_probability"]<=O for r in rows))
        elif kind=="true_binary":self.assertTrue(all(r["behavior"] in (0,1) and r["intention"] in (0,1) for r in rows))
        else:raise AssertionError(kind)
    return check_case
for _name,_mode in WORLDS:
    for _kind in ("mass","size","positive","unique","analytic","mediation","base","attitude_regret","norm_regret","constant_regret","prob_bounds","true_binary"):
        setattr(Tests,"test_"+_name.lower()+"_"+_mode.lower()+"_"+_kind,_make(_name,_mode,_kind))

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    g=ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=ap.parse_args()
    if a.test:unittest.main(argv=["R291"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
