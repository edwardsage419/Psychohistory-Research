#!/usr/bin/env python3
"""R268 S64 independent binomial Brier oracle. Standard library only.

The frozen AIC/BIC K decisions are transcribed from the original R268
persisted JSON and shared as nonblind input. No original source enumerator
or post-result model tuning is used.
"""
from __future__ import annotations
import argparse
import json
from fractions import Fraction as F
from math import comb

DECISIONS = {
    4: ("00011", "10111"),
    6: ("1001111", "1001111"),
    10: ("10001111111", "10000111111"),
}
PS = (F(1, 5), F(1, 2), F(4, 5))
METHODS = ("M0_FIXED", "M1_MLE", "AIC_SELECTED", "BIC_SELECTED")


def risk(p: F, n: int, a: str, b: str) -> dict[str, F]:
    if p not in PS or n not in DECISIONS or len(a) != n+1 or len(b) != n+1:
        raise ValueError("invalid world or decision coverage")
    if any(c not in "01" for c in a+b):
        raise ValueError("invalid decision label")
    out = {key: F(0) for key in METHODS}
    mass = F(0)
    for k in range(n+1):
        w = F(comb(n,k)) * p**k * (1-p)**(n-k)
        mass += w
        q0, q1 = F(1,5), F(k,n)
        qs = (q0, q1, q1 if a[k] == "1" else q0,
              q1 if b[k] == "1" else q0)
        for method, q in zip(METHODS, qs):
            out[method] += w * (p*(1-p) + (q-p)**2)
    if mass != 1 or any(v < 0 or v > 1 for v in out.values()):
        raise AssertionError("invalid probability or Brier range")
    return out


def evaluate() -> dict:
    results=[]
    for p in PS:
        for n,(a,b) in DECISIONS.items():
            v=risk(p,n,a,b)
            base=p*(1-p)
            results.append({
                "world":f"TRUE_P{str(p).replace('/','OF')}_N{n}",
                "true_p":str(p),"n":n,"source_count":2**n,
                "risk":{k:str(v[k]) for k in METHODS},
                "excess":{k:str(v[k]-base) for k in METHODS},
                "AIC_minus_BIC":str(v["AIC_SELECTED"]-v["BIC_SELECTED"]),
            })
    return {"research_id":"R268_S64","method":"independent_binomial_Fraction",
            "world_count":len(results),"field_risk_checks":len(results)*len(METHODS),
            "results":results}


def negative_controls() -> dict:
    tests={
        "missing_k": lambda: risk(F(1,5),4,"0011","10111"),
        "invalid_label":lambda: risk(F(1,5),4,"0001X","10111"),
        "invalid_world":lambda: risk(F(1,3),4,*DECISIONS[4]),
        "wrong_n":lambda: risk(F(1,5),6,*DECISIONS[4]),
    }
    rejected=[]
    for name,fn in tests.items():
        try: fn()
        except ValueError: rejected.append(name)
    if len(rejected)!=len(tests):
        raise AssertionError("negative control incorrectly accepted")
    return {"rejected":rejected,"count":len(rejected)}


if __name__ == "__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="")
    args=parser.parse_args()
    out=evaluate()
    out["negative_controls"]=negative_controls()
    content=json.dumps(out,ensure_ascii=False,indent=2)+"\n"
    if args.output:
        with open(args.output,"w",encoding="utf-8") as fh:fh.write(content)
    print(json.dumps({"worlds":out["world_count"],"risk_checks":out["field_risk_checks"],
                      "negative_rejected":out["negative_controls"]["count"],
                      "results":out["results"]},ensure_ascii=False))
