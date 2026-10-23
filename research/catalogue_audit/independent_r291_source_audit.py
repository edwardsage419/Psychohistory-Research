#!/usr/bin/env python3
"""R291 independent exact source audit. Never imports the primary R291 module."""
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

ROOT=Path(__file__).resolve().parents[2]/"research"/"R291"
SOURCE=ROOT/"R291_ALL_128_ORIGINAL_TRA_LABELED_JOINT_SOURCES.csv"
RESULT=ROOT/"R291_EXACT_TRA_RESULTS.json"
RECEIPT=ROOT/"R291_MACHINE_RECEIPT.json"
PROFILES={"BALANCED":(1,1),"ATTITUDE_HEAVY":(2,1),"NORM_HEAVY":(1,2),"NORM_NULL":(2,0)}
MODES=("MEDIATED","DIRECT_NORM_STRESS")
WORLDS=[(p,m) for p in PROFILES for m in MODES]
CELLS=list(itertools.product((-1,1),(-1,1),(0,1),(0,1)))
KEYS=("FULL_AN","ATTITUDE_ONLY","NORM_ONLY","CONSTANT")
ZERO,ONE=Q(0),Q(1)

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def load():
    with SOURCE.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def computed(name,mode,A,N,I,B):
    a,n=PROFILES[name]
    d=(mode=="DIRECT_NORM_STRESS")
    pi=(Q(4+a*A+n*N,8))
    after=(Q(2+4*I+d*N,8))
    weight=Q(1,4)*(pi if I else ONE-pi)*(after if B else ONE-after)
    # Independent integration of unobserved I. Formula is intentionally
    # separately calculated from the production forecast implementation.
    unconditional=(ONE-pi)*Q(2+d*N,8)+pi*Q(6+d*N,8)
    predictions={
      "FULL_AN":unconditional,
      "ATTITUDE_ONLY":Q(1,2)+Q(a*A,16),
      "NORM_ONLY":Q(1,2)+Q((n+2*int(d))*N,16),
      "CONSTANT":Q(1,2)}
    return weight,pi,after,predictions

def verify_rows(rows,results):
    if len(rows)!=128:raise AssertionError("exact 128 complete labeled sources required")
    if len(results["worlds"])!=8:raise AssertionError("expected 8 result worlds")
    counter=collections.defaultdict(list)
    allcells=[]
    for row in rows:
        name,mode=row["profile"],row["mode"]
        if (name,mode) not in WORLDS:raise AssertionError("unfrozen world")
        A,N,I,B=[int(row[x]) for x in ("attitude","subjective_norm","intention","behavior")]
        if (A,N,I,B) not in CELLS:raise AssertionError("unfrozen source cell")
        if row["world"]!=name+"__"+mode:raise AssertionError("world label disagreement")
        w,pi,pb,predictors=computed(name,mode,A,N,I,B)
        if Q(row["joint_source_probability"])!=w:raise AssertionError("original joint probability mismatch")
        if Q(row["p_intention_1_given_A_N"])!=pi:raise AssertionError("intention conditional mismatch")
        if Q(row["p_behavior_1_given_I_A_N"])!=pb:raise AssertionError("behavior conditional mismatch")
        if Q(row["p_behavior_1_pre_intention_A_N"])!=predictors["FULL_AN"]:raise AssertionError("pre-intention marginal mismatch")
        for key in KEYS:
            if Q(row["forecast_"+key])!=predictors[key]:raise AssertionError("forecast mismatch for "+key)
        counter[(name,mode)].append((A,N,I,B,w,predictors))
        allcells.append((name,mode,A,N,I,B))
    if len(set(allcells))!=128:raise AssertionError("duplicate or missing source")
    for i,(name,mode) in enumerate(WORLDS):
        observed=counter[(name,mode)]
        if len(observed)!=16:raise AssertionError("incomplete world")
        if set((A,N,I,B) for A,N,I,B,_,_ in observed)!=set(CELLS):raise AssertionError("missing cell")
        if sum((w for A,N,I,B,w,p in observed),ZERO)!=ONE:raise AssertionError("mass mismatch")
        a,n=PROFILES[name]
        d=int(mode=="DIRECT_NORM_STRESS")
        penalties={"FULL_AN":ZERO,"ATTITUDE_ONLY":Q((n+2*d)**2,256),
                   "NORM_ONLY":Q(a*a,256),"CONSTANT":Q(a*a+(n+2*d)**2,256)}
        analytic_full=Q(1,4)-penalties["CONSTANT"]
        scores={key:sum((w*(Q(B)-p[key])**2 for A,N,I,B,w,p in observed),ZERO) for key in KEYS}
        for key in KEYS:
            if scores[key]!=analytic_full+penalties[key]:raise AssertionError("closed form mismatch "+key)
        expected=results["worlds"][i]
        if expected["world"]!=name+"__"+mode:raise AssertionError("world output ordering altered")
        if expected["attitude_weight_a"]!=a or expected["norm_weight_n"]!=n or expected["behavior_direct_norm_d"]!=d:raise AssertionError("profile coefficient mismatch")
        if expected["labeled_source_cells"]!=16 or expected["full_source_mass"]!="1":raise AssertionError("output count mismatch")
        if expected["risks_Brier"]!={k:str(v) for k,v in scores.items()}:raise AssertionError("risk JSON mismatch")
        if Q(expected["regret_attitude_only"])!=penalties["ATTITUDE_ONLY"]:raise AssertionError("attitude gap mismatch")
        if Q(expected["regret_norm_only"])!=penalties["NORM_ONLY"]:raise AssertionError("norm gap mismatch")
        if Q(expected["regret_constant"])!=penalties["CONSTANT"]:raise AssertionError("base gap mismatch")
        if Q(expected["given_intention_norm_contrast"])!=Q(d,4):raise AssertionError("mediator negative-control contrast mismatch")
        if expected["analytic_risk_agreement"] is not True:raise AssertionError("false claimed math closure")
    return {"research_id":"R291","worlds":8,"complete_original_sources":128,
            "Brier_policy_evaluations":4*8,"mediation_worlds":4,"direct_norm_counterexample_worlds":4,
            "independent_math_and_source_audit":"PASS","added_real_E2":0,"added_real_E3":0}

def audit():
    results=obj(RESULT)
    receipt=obj(RECEIPT)
    if receipt["freeze_commit"]!="161d40a01451f1e89be045910f95ec536768754c":raise AssertionError("wrong prospective freeze")
    if results["freeze_commit"]!=receipt["freeze_commit"]:raise AssertionError("freeze disagreement")
    if results["catalogue_original_id"]!="01-013" or results["fully_labeled_joint_source_cells"]!=128:raise AssertionError("original catalogue label mismatch")
    if receipt["source_cells"]!=128:raise AssertionError("receipt cell count mismatch")
    if hashlib.sha256(SOURCE.read_bytes()).hexdigest()!=receipt["sources_sha256"]:raise AssertionError("source bytes mismatch")
    if hashlib.sha256(RESULT.read_bytes()).hexdigest()!=receipt["results_sha256"]:raise AssertionError("results bytes mismatch")
    if receipt["new_human_E2"]!=0 or receipt["new_historical_E3"]!=0:raise AssertionError("human/historical false promotion")
    out=verify_rows(load(),results)
    return {**out,"source_sha256":receipt["sources_sha256"],"results_sha256":receipt["results_sha256"]}

class Tests(unittest.TestCase):
    def test_audit(self):self.assertEqual(audit()["complete_original_sources"],128)
    def test_worlds(self):self.assertEqual(len(WORLDS),8)
    def test_cells(self):self.assertEqual(len(CELLS),16)
    def test_independent_profiles(self):self.assertEqual(PROFILES["NORM_NULL"],(2,0))
    def test_mediated_no_direct(self):
        for A in (-1,1):
            for I in (0,1):
                self.assertEqual(computed("BALANCED","MEDIATED",A,1,I,0)[2],computed("BALANCED","MEDIATED",A,-1,I,0)[2])
    def test_negative_control_has_norm(self):
        p=computed("BALANCED","DIRECT_NORM_STRESS",1,1,1,0)[2]
        q=computed("BALANCED","DIRECT_NORM_STRESS",1,-1,1,0)[2]
        self.assertEqual(p-q,Q(1,4))
    def test_source_probabilities(self):self.assertTrue(all(computed(name,mode,*CELLS[0])[0]>0 for name,mode in WORLDS))
    def test_reject_source_tamper(self):
        bad=load()
        bad[0]=dict(bad[0]);bad[0]["joint_source_probability"]="1/100"
        with self.assertRaises(AssertionError):verify_rows(bad,obj(RESULT))
    def test_reject_forecast_tamper(self):
        bad=load()
        bad[0]=dict(bad[0]);bad[0]["forecast_FULL_AN"]="1/3"
        with self.assertRaises(AssertionError):verify_rows(bad,obj(RESULT))
    def test_reject_duplicate(self):
        bad=load()
        bad[1]=dict(bad[0])
        with self.assertRaises(AssertionError):verify_rows(bad,obj(RESULT))
    def test_reject_missing(self):
        with self.assertRaises(AssertionError):verify_rows(load()[:-1],obj(RESULT))
    def test_reject_result_risk(self):
        bad=obj(RESULT)
        bad["worlds"][0]["risks_Brier"]["FULL_AN"]="0"
        with self.assertRaises(AssertionError):verify_rows(load(),bad)
    def test_reject_wrong_mode(self):
        bad=load()
        bad[0]=dict(bad[0]);bad[0]["mode"]="UNFROZEN"
        with self.assertRaises(AssertionError):verify_rows(bad,obj(RESULT))
    def test_digest_tamper_detectable(self):self.assertNotEqual(hashlib.sha256(SOURCE.read_bytes()+b"altered").hexdigest(),obj(RECEIPT)["sources_sha256"])

if __name__=="__main__":
    ap=argparse.ArgumentParser()
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--audit",action="store_true")
    args=ap.parse_args()
    if args.test:unittest.main(argv=["audit"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
