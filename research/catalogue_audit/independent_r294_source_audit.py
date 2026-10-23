#!/usr/bin/env python3
"""Independent audit of R294 144 exact decision sources, no production import."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]/"research/R294"
CSV=ROOT/"R294_ALL_144_EXACT_INTERTEMPORAL_DECISION_SOURCES.csv"
RESULT=ROOT/"R294_EXACT_DISCOUNT_REVERSALS.json"
RECEIPT=ROOT/"R294_MACHINE_RECEIPT.json"
MODELS=("HYPERBOLIC","EXPONENTIAL","QUASI_HYPERBOLIC_BETA_DELTA")
PAIRS=tuple(itertools.product((2,3,4),(5,7)))
Q0,Q1=Q(0),Q(1)

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def load():
    with CSV.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def worlds():
    entries=[]
    for a,b in PAIRS:
        entries.extend(("HYPERBOLIC",a,b,k,None,None) for k in (Q0,Q(1,2),Q1,Q(2),Q(3)))
        entries.extend(("EXPONENTIAL",a,b,None,None,d) for d in (Q(1,2),Q(3,5),Q(4,5)))
        entries.extend(("QUASI_HYPERBOLIC_BETA_DELTA",a,b,None,beta,d) for beta,d in itertools.product((Q(1,2),Q1),(Q(3,5),Q(4,5))))
    assert len(entries)==72
    return entries

def ident(w):
    family,a,b,k,beta,d=w
    return family+"_a"+str(a)+"_b"+str(b)+"_k"+(str(k) if k is not None else "NA")+"_beta"+(str(beta) if beta is not None else "NA")+"_delta"+(str(d) if d is not None else "NA")

def utility(w,reward,delay):
    family,a,b,k,beta,delta=w
    if family=="HYPERBOLIC":return Q(reward)/(Q1+k*delay)
    if family=="EXPONENTIAL":return reward*(delta**delay)
    if family=="QUASI_HYPERBOLIC_BETA_DELTA":return Q(reward)*(Q1 if delay==0 else beta*(delta**delay))
    raise AssertionError("unknown model")

def independent_reversal(w):
    family,a,b,k,beta,d=w
    if family=="HYPERBOLIC":return Q(b,a)*(Q1+k)>Q1+2*k and Q(b,a)<=Q1+k
    if family=="EXPONENTIAL":return False
    if family=="QUASI_HYPERBOLIC_BETA_DELTA":return b*d>a and b*beta*d<=a
    raise AssertionError("model")

def verify(rows,results):
    if len(rows)!=144 or len(results["worlds"])!=72:raise AssertionError("missing source or results")
    by=defaultdict(dict)
    for row in rows:
        try:
            key=(row["family"],int(row["earlier_reward"]),int(row["later_reward"]),
                 Q(row["parameter_k"]) if row["parameter_k"] else None,
                 Q(row["parameter_beta"]) if row["parameter_beta"] else None,
                 Q(row["parameter_delta"]) if row["parameter_delta"] else None)
            t=int(row["decision_at"])
        except (KeyError,ValueError,ZeroDivisionError) as err:raise AssertionError("bad row input") from err
        if key not in worlds() or t not in (0,1):raise AssertionError("outside frozen source universe")
        if row["world"]!=ident(key):raise AssertionError("mislabeled world")
        if t in by[key]:raise AssertionError("duplicate date")
        a,b=key[1:3]
        ua=utility(key,a,1-t);ub=utility(key,b,2-t)
        if int(row["earlier_delay"])!=1-t or int(row["later_delay"])!=2-t:raise AssertionError("date shift mismatch")
        if Q(row["earlier_utility"])!=ua or Q(row["later_utility"])!=ub:raise AssertionError("discount utility wrong")
        if row["selected_option"]!=("A" if ua>=ub else "B"):raise AssertionError("choice tie rule incorrect")
        if row["exact_tie"]!=str(ua==ub):raise AssertionError("tie status wrong")
        if row["world_reversal"] not in ("True","False"):raise AssertionError("flag invalid")
        by[key][t]=row
    expected=worlds()
    if set(by)!=set(expected):raise AssertionError("missing entire world")
    reversing={"HYPERBOLIC":0,"EXPONENTIAL":0,"QUASI_HYPERBOLIC_BETA_DELTA":0}
    for idx,w in enumerate(expected):
        if set(by[w])!={0,1}:raise AssertionError("each date must exist")
        r0,r1=by[w][0],by[w][1]
        isrev=(r0["selected_option"]=="B" and r1["selected_option"]=="A")
        if isrev!=(r0["selected_option"]!=r1["selected_option"]):raise AssertionError("wrong reversal direction")
        if isrev!=independent_reversal(w):raise AssertionError("reversal math mismatch")
        if any(row["world_reversal"]!=str(isrev) for row in (r0,r1)):raise AssertionError("reversal flag mismatch")
        o=results["worlds"][idx]
        family,a,b,k,beta,d=w
        if o["world"]!=ident(w) or o["family"]!=family or o["earlier_reward"]!=a or o["later_reward"]!=b:raise AssertionError("results world mismatch")
        if (o["k"],o["beta"],o["delta"])!=tuple(None if x is None else str(x) for x in (k,beta,d)):raise AssertionError("parameter mismatch")
        if o["choice_at_t0"]!=r0["selected_option"] or o["choice_at_t1"]!=r1["selected_option"]:raise AssertionError("results choice mismatch")
        if o["reversal_B_to_A"]!=isrev or o["analytic_condition_verified"] is not True:raise AssertionError("results reversal incorrect")
        reversing[family]+=int(isrev)
    if reversing["EXPONENTIAL"]!=0:raise AssertionError("exponential reversed")
    return {"research_id":"R294","original_worlds":72,"original_decision_source_rows":144,
            "reversals_by_family":reversing,"independent_formula_and_two_date_source_audit":"PASS",
            "added_real_E2":0,"added_historical_E3":0}

def audit():
    r,j=obj(RECEIPT),obj(RESULT)
    if r["freeze_commit"]!="9c78d082902cedffb8ad64159915d8d6f5e12299" or j["freeze_commit"]!=r["freeze_commit"]:raise AssertionError("freeze not original")
    if j["original_catalogue_id"]!="01-018" or j["artificial_worlds"]!=72 or j["exact_decision_source_rows"]!=144:raise AssertionError("scope mismatch")
    if r["source_sha256"]!=hashlib.sha256(CSV.read_bytes()).hexdigest():raise AssertionError("CSV tamper")
    if r["result_sha256"]!=hashlib.sha256(RESULT.read_bytes()).hexdigest():raise AssertionError("JSON tamper")
    if r["E2_added"]!=0 or r["E3_added"]!=0:raise AssertionError("empirical overclaim")
    return {**verify(load(),j),"source_sha256":r["source_sha256"],"result_sha256":r["result_sha256"]}

class Tests(unittest.TestCase):
    def test_whole(self):self.assertEqual(audit()["original_decision_source_rows"],144)
    def test_worlds(self):self.assertEqual(len(worlds()),72)
    def test_exp_zero(self):self.assertFalse(any(independent_reversal(w) for w in worlds() if w[0]=="EXPONENTIAL"))
    def test_hyper_special(self):
        w=next(w for w in worlds() if w[0]=="HYPERBOLIC" and w[1:3]==(3,5) and w[3]==1)
        self.assertTrue(independent_reversal(w))
    def test_quasi_special(self):
        w=next(w for w in worlds() if w[0]=="QUASI_HYPERBOLIC_BETA_DELTA" and w[1:3]==(3,5) and w[4:]==(Q(1,2),Q(4,5)))
        self.assertTrue(independent_reversal(w))
    def test_missing_date(self):
        with self.assertRaises(AssertionError):verify(load()[:-1],obj(RESULT))
    def test_utility_tamper(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["earlier_utility"]="0"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_choice_tamper(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["selected_option"]="NEITHER"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_reversal_tamper(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["world_reversal"]="MAYBE"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_result_tamper(self):
        result=obj(RESULT);result["worlds"][0]["choice_at_t0"]="WRONG"
        with self.assertRaises(AssertionError):verify(load(),result)
    def test_bad_parameters(self):
        rows=load();rows[0]=dict(rows[0]);rows[0]["parameter_k"]="7"
        with self.assertRaises(AssertionError):verify(rows,obj(RESULT))
    def test_hash_tamper(self):self.assertNotEqual(hashlib.sha256(CSV.read_bytes()+b"changed").hexdigest(),obj(RECEIPT)["source_sha256"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R294"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
