#!/usr/bin/env python3
"""R111 McFadden random-utility conditional logit: pure mathematical study.

No external data, no fitted behavioral claims. Standard-library Python 3.10+.
"""
from __future__ import annotations
import math
import random

def probabilities(utilities, scale=1.0, available=None):
    """Gumbel-iid RUM probabilities with strict choice-set and finite checks.

    epsilon_j iid EV1 with the same location and positive scale, so P_j is
    conditional logit. Availability is part of the choice occasion.
    """
    v=tuple(float(u) for u in utilities)
    if not v:
        raise ValueError("R111_EMPTY_CHOICE_SET")
    if not math.isfinite(scale) or scale<=0:
        raise ValueError("R111_NONPOSITIVE_OR_NONFINITE_NOISE_SCALE")
    if any(not math.isfinite(x) for x in v):
        raise ValueError("R111_NONFINITE_SYSTEMATIC_UTILITY")
    if available is None:
        mask=(True,)*len(v)
    else:
        mask=tuple(available)
        if len(mask)!=len(v) or any(type(x) is not bool for x in mask):
            raise ValueError("R111_AVAILABILITY_MASK_INVALID")
    positions=[j for j,yes in enumerate(mask) if yes]
    if not positions:
        raise ValueError("R111_NO_AVAILABLE_ALTERNATIVE")
    pivot=max(v[j] for j in positions)
    exps=[math.exp((v[j]-pivot)/scale) for j in positions]
    total=math.fsum(exps)
    if not math.isfinite(total) or not total>0:
        raise ValueError("R111_LOGSUM_NUMERIC_FAILURE")
    probs=[0.0]*len(v)
    for j,num in zip(positions,exps):
        probs[j]=num/total
    return probs

def conditional_logit(features,theta,scale=1.0,available=None):
    """Representational utility V_j = sum_k feature[j,k]*theta[k]."""
    t=tuple(float(x) for x in theta)
    if not t or any(not math.isfinite(x) for x in t):
        raise ValueError("R111_THETA_INVALID")
    xs=tuple(tuple(float(z) for z in item) for item in features)
    if not xs or any(len(x)!=len(t) for x in xs):
        raise ValueError("R111_FEATURE_DIMENSION_INVALID")
    return probabilities([math.fsum(a*b for a,b in zip(x,t)) for x in xs],
                         scale,available)

def negative_log_likelihood(rows,theta,scale=1.0):
    """Choice occasions: (feature_matrix, chosen_index, availability_mask)."""
    nll=0.0
    n=0
    for features,choice,available in rows:
        t=tuple(float(x) for x in theta)
        feats=tuple(tuple(float(x) for x in item) for item in features)
        p=conditional_logit(feats,t,scale,available)  # strict common validation
        mask=(True,)*len(p) if available is None else tuple(available)
        if type(choice) is not int or not 0<=choice<len(p) or not mask[choice]:
            raise ValueError("R111_OBSERVED_CHOICE_UNAVAILABLE_OR_UNSUPPORTED")
        v=[math.fsum(a*b for a,b in zip(f,t)) for f in feats]
        pivot=max(v[j] for j,yes in enumerate(mask) if yes)
        logdenom=math.log(math.fsum(math.exp((v[j]-pivot)/scale)
                                   for j,yes in enumerate(mask) if yes))
        # Stable even when an extremely unlikely available choice has p rounded to 0.
        nll += (pivot-v[choice])/scale+logdenom
        n+=1
    if n==0:
        raise ValueError("R111_NO_OBSERVATIONS")
    return nll

def iid_gumbel_mc_probabilities(utilities,scale=1.0,draws=20000,seed=111):
    """Monte Carlo sanity check. Never report as empirical human behavior."""
    if type(draws) is not int or draws<=0:
        raise ValueError("R111_MC_DRAWS_INVALID")
    probabilities(utilities,scale)  # validates the deterministic source inputs
    r=random.Random(seed)
    values=tuple(float(x) for x in utilities)
    counts=[0]*len(values)
    for _ in range(draws):
        shocks=[]
        for _ in values:
            x=max(r.random(),1e-300)
            shocks.append(-math.log(-math.log(x))*scale)
        argmax=max(range(len(values)),key=lambda k:values[k]+shocks[k])
        counts[argmax]+=1
    return [x/draws for x in counts]

def red_bus_blue_bus_counterexample():
    """IIA limitation: one cloned bus draws probability from every option."""
    car=math.log(2.0)
    before=probabilities((car,0.0))
    after=probabilities((car,0.0,0.0))
    return {"before_car":before[0],"before_bus":before[1],
            "after_car":after[0],"after_red_bus":after[1],
            "after_blue_bus":after[2],
            "iiA_is_restrictive_when_options_are_near_clones":True}

if __name__=="__main__":
    print("R111_SYNTHETIC_ONLY",red_bus_blue_bus_counterexample())
