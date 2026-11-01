#!/usr/bin/env python3
"""Independent nonblind R327 S123 exact closed-form auditor; no R import."""
import argparse
import copy
import json
from fractions import Fraction as F
from pathlib import Path

QUALITY=(F(1,2),F(5,8),F(3,4),F(7,8),F(1))
COST=(F(0),F(1,16),F(1,8),F(3,16),F(1,4))
FIELDS=("belief","accuracy","cost","immediate_value","uncosted_sense_value",
        "sense_value","gross_information_value","optimal_value","chosen_action")
FREEZE="5bfd3c13e4ee9d4b6af1defc17469c33bd538c4c"


def check(obj):
    if not isinstance(obj,dict) or set(obj)!={"model","evidence_grade","freeze_commit","world_count","worlds"}:
        raise ValueError("top-level schema")
    if obj["model"]!="R327_S123_FINITE_SENSOR_QUALITY_COST_E1" or obj["evidence_grade"]!="E1_SYNTHETIC_ONLY" or obj["freeze_commit"]!=FREEZE:
        raise ValueError("identity/evidence grade")
    if obj["world_count"]!=225 or not isinstance(obj["worlds"],list) or len(obj["worlds"])!=225:
        raise ValueError("world coverage")
    expected_keys=[(b,q,c) for q in QUALITY for c in COST for b in (F(k,8) for k in range(9))]
    for i,(r,(b,q,c)) in enumerate(zip(obj["worlds"],expected_keys)):
        if not isinstance(r,dict) or set(r)!=set(FIELDS):
            raise ValueError("row schema")
        if (r["belief"],r["accuracy"],r["cost"])!=(str(b),str(q),str(c)):
            raise ValueError(f"row {i}: identity/order")
        # Independent closed form: for binary symmetric observations, the
        # maximum probability of a correct terminal guess is max(prior MAP,q).
        m=max(b,1-b)
        u=max(m,q)
        s=u-c
        gain=u-m
        action="SENSE" if gain>c else ("GUESS_1" if b>F(1,2) else "GUESS_0")
        expected=(str(m),str(u),str(s),str(gain),str(max(m,s)),action)
        got=tuple(r[k] for k in FIELDS[3:])
        if got!=expected:
            raise ValueError(f"row {i}: independent closed-form mismatch")
    return True


def mutations(obj):
    cases=[]
    def mutated(label,change):
        x=copy.deepcopy(obj)
        change(x)
        cases.append((label,x))
    mutated("omission",lambda x:x["worlds"].pop())
    mutated("duplicate",lambda x:x["worlds"].__setitem__(1,x["worlds"][0].copy()))
    mutated("belief_identity",lambda x:x["worlds"][1].__setitem__("belief","7/8"))
    mutated("quality_identity",lambda x:x["worlds"][9].__setitem__("accuracy","1"))
    mutated("cost_identity",lambda x:x["worlds"][45].__setitem__("cost","1/4"))
    mutated("reward",lambda x:x["worlds"][100].__setitem__("optimal_value","999"))
    mutated("decision",lambda x:x["worlds"][112].__setitem__("chosen_action","SENSE" if x["worlds"][112]["chosen_action"]!="SENSE" else "GUESS_0"))
    mutated("grade",lambda x:x.__setitem__("evidence_grade","E2_HUMAN_VALIDATED"))
    mutated("order",lambda x:x["worlds"].reverse())
    mutated("count",lambda x:x.__setitem__("world_count",224))
    rejected=[]
    for name,x in cases:
        try: check(x)
        except (ValueError,TypeError,KeyError): rejected.append(name)
        else: raise AssertionError("mutant accepted: "+name)
    return rejected


def main():
    p=argparse.ArgumentParser()
    p.add_argument("receipt",type=Path)
    args=p.parse_args()
    obj=json.loads(args.receipt.read_text(encoding="utf-8"))
    check(obj)
    rejected=mutations(obj)
    print("PASS_NONBLIND_INTERNAL_E1 225/225 exact closed-form fields")
    print("MUTANTS_REJECTED",len(rejected)," ".join(rejected))
    print("E2=NOT_ESTABLISHED E3=NOT_ESTABLISHED EXTERNAL_INDEPENDENT=NOT_RUN")

if __name__=="__main__":main()
