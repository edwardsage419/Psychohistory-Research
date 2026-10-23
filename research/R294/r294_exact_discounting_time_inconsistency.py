#!/usr/bin/env python3
"""R294 fixed two-date artificial intertemporal choices: finite E1 only."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from functools import lru_cache
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
FREEZE="9c78d082902cedffb8ad64159915d8d6f5e12299"
EARLY=(2,3,4)
LATE=(5,7)
RATES=(F(0),F(1,2),F(1),F(2),F(3))
DELTAS=(F(1,2),F(3,5),F(4,5))
BETA=(F(1,2),F(1))
QDELTAS=(F(3,5),F(4,5))
CSV_FILE="R294_ALL_144_EXACT_INTERTEMPORAL_DECISION_SOURCES.csv"
RESULT_FILE="R294_EXACT_DISCOUNT_REVERSALS.json"
RECEIPT_FILE="R294_MACHINE_RECEIPT.json"

def worlds():
    out=[]
    for a,b in itertools.product(EARLY,LATE):
        for k in RATES:out.append(("HYPERBOLIC",a,b,k,None,None))
        for d in DELTAS:out.append(("EXPONENTIAL",a,b,None,None,d))
        for beta,d in itertools.product(BETA,QDELTAS):out.append(("QUASI_HYPERBOLIC_BETA_DELTA",a,b,None,beta,d))
    assert len(out)==72
    return tuple(out)
WORLDS=worlds()

def id_for(w):
    family,a,b,k,beta,delta=w
    return family+"_a"+str(a)+"_b"+str(b)+"_k"+(str(k) if k is not None else "NA")+"_beta"+(str(beta) if beta is not None else "NA")+"_delta"+(str(delta) if delta is not None else "NA")

def discount(w,delay):
    family,a,b,k,beta,delta=w
    if delay not in (0,1,2):raise ValueError("unfrozen distance")
    if family=="HYPERBOLIC":return F(1)/(1+k*delay)
    if family=="EXPONENTIAL":return delta**delay
    if family=="QUASI_HYPERBOLIC_BETA_DELTA":return F(1) if delay==0 else beta*(delta**delay)
    raise ValueError("unfrozen family")

def selected(w,t):
    if w not in WORLDS or t not in (0,1):raise ValueError("unfrozen profile/date")
    _,a,b,_,_,_=w
    ua=F(a)*discount(w,1-t)
    ub=F(b)*discount(w,2-t)
    return {"decision_at":t,"earlier_delay":1-t,"later_delay":2-t,
            "earlier_utility":ua,"later_utility":ub,
            "exact_tie":ua==ub,"selected_option":"A" if ua>=ub else "B"}

def predicted_reversal(w):
    family,a,b,k,beta,delta=w
    ratio=F(b,a)
    if family=="HYPERBOLIC":
        return ratio>F(1+2*k,1+k) and ratio<=1+k
    if family=="EXPONENTIAL":
        return False
    if family=="QUASI_HYPERBOLIC_BETA_DELTA":
        return b*delta>a and b*beta*delta<=a
    raise AssertionError("unfrozen")

def decision_pair(w):
    first,last=selected(w,0),selected(w,1)
    reversal=first["selected_option"]=="B" and last["selected_option"]=="A"
    if (first["selected_option"]!=last["selected_option"])!=reversal:
        raise AssertionError("wrong reversal direction")
    if reversal!=predicted_reversal(w):raise AssertionError("analytic condition disagrees")
    return first,last,reversal

def validate():
    assert len(WORLDS)==72 and len(set(id_for(w) for w in WORLDS))==72
    assert sum(2 for w in WORLDS)==144
    assert sum(w[0]=="HYPERBOLIC" for w in WORLDS)==30
    assert sum(w[0]=="EXPONENTIAL" for w in WORLDS)==18
    assert sum(w[0]=="QUASI_HYPERBOLIC_BETA_DELTA" for w in WORLDS)==24
    for w in WORLDS:
        first,last,rev=decision_pair(w)
        assert all(v["earlier_utility"]>0 and v["later_utility"]>0 for v in (first,last))
        assert first["earlier_delay"]==1 and first["later_delay"]==2
        assert last["earlier_delay"]==0 and last["later_delay"]==1
        if w[0]=="EXPONENTIAL":assert not rev
        if w[0]=="QUASI_HYPERBOLIC_BETA_DELTA" and w[4]==1:assert not rev
    w=next(w for w in WORLDS if w[0]=="HYPERBOLIC" and w[1:3]==(3,5) and w[3]==1)
    p,q,r=decision_pair(w)
    assert r and (p["earlier_utility"],p["later_utility"],q["earlier_utility"],q["later_utility"])==(F(3,2),F(5,3),F(3),F(5,2))
    w=next(w for w in WORLDS if w[0]=="QUASI_HYPERBOLIC_BETA_DELTA" and w[1:3]==(3,5) and w[4:]==(F(1,2),F(4,5)))
    assert decision_pair(w)[2] is True
    return True

def emit():
    validate()
    cols=("world","family","earlier_reward","later_reward","decision_at",
          "parameter_k","parameter_beta","parameter_delta","earlier_delay","later_delay",
          "earlier_utility","later_utility","exact_tie","selected_option","world_reversal")
    csvpath=ROOT/CSV_FILE
    with csvpath.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        wr.writeheader()
        for w in WORLDS:
            family,a,b,k,beta,delta=w
            p,q,reversal=decision_pair(w)
            for dt in (p,q):
                row={"world":id_for(w),"family":family,"earlier_reward":a,"later_reward":b,
                     "parameter_k":"" if k is None else str(k),
                     "parameter_beta":"" if beta is None else str(beta),
                     "parameter_delta":"" if delta is None else str(delta),
                     "world_reversal":str(reversal)}
                row.update({s:(str(value) if not isinstance(value,str) else value) for s,value in dt.items()})
                wr.writerow({column:row[column] for column in cols})
    output={"research_id":"R294","original_catalogue_id":"01-018","freeze_commit":FREEZE,
            "scope":"EXACT_FINITE_ARTIFICIAL_DISCOUNTING_PREFERENCE_REVERSALS_NOT_HUMAN_FIT",
            "artificial_worlds":72,"exact_decision_source_rows":144,
            "new_human_E2":0,"new_historical_E3":0,"R073":"FROZEN","PESEN_v0_1":"FROZEN",
            "worlds":[]}
    for w in WORLDS:
        family,a,b,k,beta,d=w
        p,q,rev=decision_pair(w)
        output["worlds"].append({"world":id_for(w),"family":family,"earlier_reward":a,"later_reward":b,
          "k":None if k is None else str(k),"beta":None if beta is None else str(beta),"delta":None if d is None else str(d),
          "choice_at_t0":p["selected_option"],"choice_at_t1":q["selected_option"],"reversal_B_to_A":rev,
          "analytic_condition_verified":rev==predicted_reversal(w)})
    result=ROOT/RESULT_FILE
    result.write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt={"research_id":"R294","freeze_commit":FREEZE,"worlds":72,"decision_source_rows":144,
       "source_sha256":hashlib.sha256(csvpath.read_bytes()).hexdigest(),
       "result_sha256":hashlib.sha256(result.read_bytes()).hexdigest(),
       "E2_added":0,"E3_added":0}
    (ROOT/RECEIPT_FILE).write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_claims(self):self.assertTrue(validate())
    def test_worlds(self):self.assertEqual(len(WORLDS),72)
    def test_zero_exponential_reversal(self):self.assertFalse(any(decision_pair(w)[2] for w in WORLDS if w[0]=="EXPONENTIAL"))
    def test_beta_one_no_reversal(self):self.assertFalse(any(decision_pair(w)[2] for w in WORLDS if w[0]=="QUASI_HYPERBOLIC_BETA_DELTA" and w[4]==1))
    def test_reject_wrong_date(self):
        with self.assertRaises(ValueError):selected(WORLDS[0],2)
    def test_reject_wrong_delay(self):
        with self.assertRaises(ValueError):discount(WORLDS[0],3)
    def test_reject_wrong_profile(self):
        with self.assertRaises(ValueError):selected(("MISSING",3,5,None,None,None),0)
def make(w,t,k):
    def run(self):
        d=selected(w,t)
        if k=="positive":self.assertGreater(d["earlier_utility"],0)
        elif k=="selected":self.assertEqual(d["selected_option"],"A" if d["earlier_utility"]>=d["later_utility"] else "B")
        elif k=="delay":self.assertEqual((d["earlier_delay"],d["later_delay"]),(1-t,2-t))
        elif k=="reversal":self.assertEqual(decision_pair(w)[2],predicted_reversal(w))
        else:raise AssertionError(k)
    return run
for ix,w in enumerate(WORLDS):
    for t in (0,1):
        for k in ("positive","selected","delay","reversal"):
            setattr(Tests,"test_world"+str(ix)+"_t"+str(t)+"_"+k,make(w,t,k))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true")
    m.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R294"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
