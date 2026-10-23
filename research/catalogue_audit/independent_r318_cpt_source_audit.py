#!/usr/bin/env python3
"""R318 independent no-import CPT outcome factor audit using manual likelihood tabs."""
from __future__ import annotations
import argparse
import csv
import json
from fractions import Fraction
from itertools import combinations
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]/"R318"
CSV=ROOT/"R318_ALL_72_ORIGINAL_RANK_SIGN_OUTCOME_SOURCE_ATOMS.csv"
OUT=ROOT/"R318_EXACT_36_TWO_OUTCOME_CPT_VALUES.json"

def independent_transform(p,kind):
    if kind=="identity":return p
    if kind=="quadratic_asymmetric_noncanonical":
        # Odds representation to avoid sharing generator weighting code.
        if p==1:return Fraction(1)
        if p==0:return Fraction(0)
        odds=p/(1-p)
        return odds*odds/(odds*odds+2)
    raise AssertionError(kind)

def independent_contributions(low,high,p,kind):
    q=1-p
    if 0<low:
        t="gain"
        weights=(1-independent_transform(q,kind),independent_transform(q,kind))
    elif high<0:
        t="loss"
        weights=(independent_transform(p,kind),1-independent_transform(p,kind))
    else:
        t="mixed"
        weights=(independent_transform(p,kind),independent_transform(q,kind))
    vals=(low if low>0 else low*2,high if high>0 else high*2)
    return t,weights,(weights[0]*vals[0],weights[1]*vals[1]),vals

def audit():
    with CSV.open(newline="",encoding="utf-8") as f:rows=list(csv.DictReader(f))
    data=json.loads(OUT.read_text(encoding="utf-8"))
    assert len(rows)==72 and data["source_atoms"]==72
    assert len(data["outcomes"])==data["lotteries"]==36
    assert data["weighting_noncanonical"] is True
    id=0
    for kind in ("identity","quadratic_asymmetric_noncanonical"):
        for low,high in combinations((-2,-1,1,2),2):
            for p in (Fraction(1,4),Fraction(1,2),Fraction(3,4)):
                domain,w,c,vals=independent_contributions(low,high,p,kind)
                total=c[0]+c[1]
                expect={"world":id,"transform":kind,"x_low":low,"x_high":high,
                    "p_low":str(p),"domain":domain,
                    "low_weight":str(w[0]),"high_weight":str(w[1]),
                    "weight_sum":str(sum(w)),"lottery_value":str(total)}
                assert data["outcomes"][id]==expect
                for i,x in enumerate((low,high)):
                    r=rows[2*id+i]
                    want=[id,kind,low,high,str(p),i,x,str((p,1-p)[i]),
                          domain,str(w[i]),vals[i],str(c[i]),str(total)]
                    if tuple(r.values())!=tuple(map(str,want)):
                        raise AssertionError(f"atom not identical {id=} {i=}")
                if kind=="identity":
                    assert total==p*vals[0]+(1-p)*vals[1]
                if domain!="mixed":assert sum(w)==1
                id+=1
    assert id==36
    witness=[x for x in data["outcomes"] if x["transform"]=="quadratic_asymmetric_noncanonical" and x["x_low"]==-2 and x["x_high"]==2 and x["p_low"]=="1/4"]
    assert len(witness)==1
    assert witness[0]["lottery_value"]=="298/209"
    assert witness[0]["weight_sum"]=="182/209"
    return {"status":"PASS","source_atoms":72,"lottery_worlds":36,"illustrative_noncanonical":True,"human_E2":0,"historical_E3":0}
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--audit",action="store_true");parser.add_argument("--test",action="store_true")
    parser.parse_args()
    print(json.dumps(audit(),sort_keys=True))
