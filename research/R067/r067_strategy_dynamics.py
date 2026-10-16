#!/usr/bin/env python3
"""R067 E1: three two-strategy learning/evolution dynamics, no empirical claims.

Replicator = Euler step of Taylor-Jonker continuous frequency dynamics.
Dynamic logit = lagged quantal *response*, NOT solved QRE fixed point.
Best response = deterministic payoff argmax, tie leaves share unchanged.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

PRISONERS_DILEMMA=((3.0,0.0),(5.0,1.0))
COORDINATION=((4.0,0.0),(0.0,3.0))
X0=0.5
DT=0.1
LAMBDA=2.0
ETA=0.2


def validate_state(x, A):
    try:
        value=float(x)
        matrix=tuple(tuple(float(z) for z in row) for row in A)
    except (ValueError,TypeError):
        raise ValueError("numeric state and payoff required") from None
    if (not math.isfinite(value) or value<0 or value>1 or
        len(matrix)!=2 or any(len(row)!=2 for row in matrix)
        or any(not math.isfinite(z) for row in matrix for z in row)):
        raise ValueError("state in [0,1] and finite 2x2 payoffs required")
    return value,matrix


def payoffs(x,A):
    x,ma=validate_state(x,A)
    return (ma[0][0]*x+ma[0][1]*(1-x),
            ma[1][0]*x+ma[1][1]*(1-x))


def delta(x,A):
    c,d=payoffs(x,A)
    return c-d


def bounded(name,v,lower,upper):
    try:
        f=float(v)
    except (TypeError,ValueError):
        raise ValueError(name+" should be numeric") from None
    if not math.isfinite(f) or f<lower or f>upper:
        raise ValueError(name+" outside frozen admissible numeric range")
    return f


def replicator_step(x,A,dt=DT):
    x,ma=validate_state(x,A)
    h=bounded("Euler dt",dt,0,1)
    y=x+h*x*(1-x)*delta(x,ma)
    if not math.isfinite(y) or y < 0 or y > 1:
        raise ValueError("replicator Euler step exceeds probability simplex")
    return y


def logit_prob_c(difference,lam=LAMBDA):
    ell=bounded("logit intensity",lam,0,100)
    if not math.isfinite(difference):
        raise ValueError("payoff difference not finite")
    z=ell*difference
    # numerically stable logistic on two tails, no under/overflow.
    if z>=0:
        return 1/(1+math.exp(-z))
    e=math.exp(z)
    return e/(1+e)


def logit_response_step(x,A,lam=LAMBDA,eta=ETA):
    x,ma=validate_state(x,A)
    inertia=bounded("update proportion",eta,0,1)
    p=logit_prob_c(delta(x,ma),lam)
    return (1-inertia)*x+inertia*p


def best_response_step(x,A,eta=ETA):
    x,ma=validate_state(x,A)
    inertia=bounded("update proportion",eta,0,1)
    d=delta(x,ma)
    target=1.0 if d>0 else 0.0 if d<0 else x
    return (1-inertia)*x+inertia*target


def trajectory(mode,x0,A,steps=20):
    if type(steps) is not int or not 0<=steps<=1000:
        raise ValueError("steps outside integer [0,1000]")
    x,_=validate_state(x0,A)
    hist=[x]
    for _ in range(steps):
        if mode=="replicator":
            x=replicator_step(x,A)
        elif mode=="logit_response":
            x=logit_response_step(x,A)
        elif mode=="best_response":
            x=best_response_step(x,A)
        else:
            raise ValueError("unknown evolutionary game dynamics")
        hist.append(x)
    return hist


def benchmark():
    scenarios={}
    for label,A in (("prisoners_dilemma",PRISONERS_DILEMMA),
                    ("coordination",COORDINATION)):
        run={}
        for mode in ("replicator","logit_response","best_response"):
            hist=trajectory(mode,X0,A)
            run[mode]={"x0":hist[0],"step1":hist[1],
                       "step5":hist[5],"step20":hist[20]}
        scenarios[label]=run
    expected_pd={
        "replicator":0.4625,
        "logit_response":.4+.2/(1+math.exp(3)),
        "best_response":.4,
    }
    for name,value in expected_pd.items():
        if abs(scenarios["prisoners_dilemma"][name]["step1"]-value)>1e-12:
            raise AssertionError("frozen PD probe diverged: "+name)
    if abs(scenarios["coordination"]["replicator"]["step1"]-.5125)>1e-12:
        raise AssertionError("coordination replicator probe diverged")
    if abs(scenarios["coordination"]["best_response"]["step1"]-.6)>1e-12:
        raise AssertionError("coordination strict best response probe diverged")
    return {
        "research_id":"R067",
        "status":"E1_MECHANISM_PASS",
        "evidence":"SYNTHETIC_ONLY",
        "protocol":"protocols/R067_EVOLUTIONARY_GAME_STRATEGY_2026-10-16.md",
        "payoff_matrices":{"prisoners_dilemma":PRISONERS_DILEMMA,
                           "coordination":COORDINATION},
        "parameters":{"x0":X0,"replicator_dt":DT,
                      "dynamic_logit_lambda":LAMBDA,
                      "dynamic_logit_eta":ETA,"best_response_eta":ETA},
        "coordination_exact_payoff_indifference_threshold":3/7,
        "results":scenarios,
        "not_a_QRE_fixed_point_solution":True,
        "real_behavioral_experiment_fitted":False,
        "e2_human_data":"OPEN","e3_external":"OPEN",
        "pesen_v01":"FROZEN",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    res=benchmark()
    args.output.write_text(json.dumps(res,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"study":res["research_id"],"status":res["status"],
                      "step1_pd":{m:v["step1"] for m,v in res["results"]["prisoners_dilemma"].items()},
                      "step1_coordination":{m:v["step1"] for m,v in res["results"]["coordination"].items()}},
                     sort_keys=True))


if __name__=="__main__":
    main()
