#!/usr/bin/env python3
"""R068: exact minimal two-trait cultural transmission probabilities and drift.

E1 algebraic/synthetic mechanics only. No historical calibration, causal
inference or original author's full spatial conformist-population model.
"""
from __future__ import annotations
import argparse,json,math
from pathlib import Path

P0=.2
MU=.01
N=100
S=math.log(2)


def probability(p):
    try:x=float(p)
    except (ValueError,TypeError):raise ValueError("frequency must be numeric") from None
    if not math.isfinite(x) or x<0 or x>1:
        raise ValueError("frequency must be finite [0,1]")
    return x


def choose_raw(mode,p,success=0.0):
    x=probability(p)
    if mode=="neutral":
        return x
    if mode=="conformist_three":
        return x*x*x+3*x*x*(1-x)
    if mode=="success_weighted":
        try:s=float(success)
        except (ValueError,TypeError):raise ValueError("success weight must be numeric") from None
        if not math.isfinite(s) or not -20<=s<=20:
            raise ValueError("log success relative weight must be within [-20,20]")
        if x in (0.,1.):
            return x
        # denominator remains bounded for admissible s, including rare types.
        return (x*math.exp(s))/(x*math.exp(s)+1-x)
    raise ValueError("unsupported transmission mechanism")


def symmetric_mutation(raw,mu):
    q=probability(raw)
    try:m=float(mu)
    except (ValueError,TypeError):raise ValueError("mutation must be numeric") from None
    if not math.isfinite(m) or not 0<=m<=0.5:
        raise ValueError("symmetric mutation must be in [0,0.5]")
    answer=m+(1-2*m)*q
    if not 0<=answer<=1:
        raise ValueError("mutation output outside probability simplex")
    return answer


def finite_drift_stats(mode,p,mu,n,success=0.0):
    if type(n) is not int or n<1 or n>10**9:
        raise ValueError("sampled learners must be positive finite integer")
    raw=choose_raw(mode,p,success)
    mutated=symmetric_mutation(raw,mu)
    v=mutated*(1-mutated)/n
    return {
        "rule":mode,
        "raw_probability_A":raw,
        "mutated_probability_A":mutated,
        "expected_frequency_next_population":mutated,
        "variance_frequency_after_finite_binomial_sampling":v,
        "population_size":n,
        "mutation_rate":float(mu),
        "success_log_relative_weight":float(success) if mode=="success_weighted" else None,
        "independent_evidence":"NONE_E1",
    }


def benchmark():
    models={
        "neutral":finite_drift_stats("neutral",P0,MU,N),
        "conformist_three":finite_drift_stats("conformist_three",P0,MU,N),
        "success_weighted":finite_drift_stats("success_weighted",P0,MU,N,S),
    }
    expected={"neutral":(.2,.206),
              "conformist_three":(.104,.11192),
              "success_weighted":(1/3,.01+.98/3)}
    for key,(raw,q) in expected.items():
        if (abs(models[key]["raw_probability_A"]-raw)>1e-12 or
            abs(models[key]["mutated_probability_A"]-q)>1e-12):
            raise AssertionError("frozen E1 cultural transmission probe differs")
    return {
        "research_id":"R068","stage":"E1_MINIMAL_CULTURAL_TRANSMISSION",
        "protocol":"protocols/R068_CULTURAL_TRANSMISSION_BIAS_2026-10-16.md",
        "status":"E1_MECHANISM_PASS",
        "initial_A_frequency":P0,
        "symmetric_mutation":MU,"finite_population":N,
        "success_weighted_log_relative_advantage":S,
        "models":models,
        "evidence":"SYNTHETIC_MATH_ONLY",
        "true_empirical_cultural_transmission_data":"OPEN",
        "history_extrapolation":"UNSUPPORTED",
        "pesen_v01":"FROZEN",
    }


def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    data=benchmark()
    args.output.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"study":data["research_id"],"status":data["status"],
        "expected_A_after_learning_and_mutation":{
            k:v["expected_frequency_next_population"] for k,v in data["models"].items()},
        "sampling_variance":{
            k:v["variance_frequency_after_finite_binomial_sampling"]
            for k,v in data["models"].items()}},sort_keys=True))


if __name__=="__main__":
    main()
