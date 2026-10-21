"""R167 fictional two-group cultural frequencies and exact within-between covariance.

Every group identifier is a mathematical placeholder. These equations are
project-authored and never calibrated to population or cooperation datasets.
"""
from __future__ import annotations

import json
from fractions import Fraction as F

START_PAIRS=((F(1,4),F(3,4)),(F(1,3),F(2,3)),
             (F(1,5),F(4,5)),(F(1,2),F(1,2)))
HIGH_WEIGHTS=(F(1,2),F(3,4))
WITHIN_DELTAS=(F(-1,4),F(0),F(1,4))
BETWEEN_KAPPAS=(0,1,2)
HORIZON=3


def unit(x,name):
    if isinstance(x,bool) or not isinstance(x,(int,F)):
        raise ValueError(f"{name}: exact Fraction/int required")
    v=F(x)
    if not 0<=v<=1:
        raise ValueError(f"{name}: outside [0,1]")
    return v


def checked_state(state):
    if not isinstance(state,(tuple,list)) or len(state)!=4:
        raise ValueError("state requires p_low,p_high,w_low,w_high")
    p0,p1,w0,w1=tuple(unit(x,"state") for x in state)
    if w0+w1!=1:
        raise ValueError("initial group weights must sum to one")
    if p0>p1:
        raise ValueError("predeclared group indices must be ordered by A frequency")
    return (p0,p1,w0,w1)


def params(delta,kappa):
    if isinstance(delta,bool) or not isinstance(delta,(F,int)):
        raise ValueError("delta must be exact rational")
    delta=F(delta)
    if delta not in WITHIN_DELTAS:
        raise ValueError("delta outside frozen grid")
    if type(kappa) is not int or kappa not in BETWEEN_KAPPAS:
        raise ValueError("kappa outside frozen grid")
    return delta,kappa


def population_mean(state):
    p0,p1,w0,w1=checked_state(state)
    return w0*p0+w1*p1


def direct_step(state,delta,kappa):
    """Within group A response followed by pre-state group reproduction."""
    p0,p1,w0,w1=checked_state(state)
    delta,kappa=params(delta,kappa)
    q0=p0-delta*p0*(1-p0)
    q1=p1-delta*p1*(1-p1)
    R0=1+F(kappa)*p0
    R1=1+F(kappa)*p1
    norm=w0*R0+w1*R1
    next_state=checked_state((q0,q1,w0*R0/norm,w1*R1/norm))
    old=w0*p0+w1*p1
    within=w0*(q0-p0)+w1*(q1-p1)
    unweighted=w0*q0+w1*q1
    after=population_mean(next_state)
    between=after-unweighted
    if after-old!=within+between:
        raise AssertionError("within-between decomposition broken")
    return next_state,within,between,after-old


def covariance_oracle(state,delta,kappa):
    """Independent covariance algebra; does not call direct_step."""
    a,b,x,y=checked_state(state)
    delta,kappa=params(delta,kappa)
    # Alternative factorization of an individual within-group transition.
    aa=a*(1-delta*(1-a))
    bb=b*(1-delta*(1-b))
    before=x*a+y*b
    within=-delta*(x*a*(1-a)+y*b*(1-b))
    low_growth=F(1)+F(kappa)*a
    high_growth=F(1)+F(kappa)*b
    normalizer=x*low_growth+y*high_growth
    between=x*y*(high_growth-low_growth)*(bb-aa)/normalizer
    new_mean=before+within+between
    # Independently calculate group mass contributions without direct_step.
    low_mass=x*low_growth/normalizer
    high_mass=F(1)-low_mass
    next_state=checked_state((aa,bb,low_mass,high_mass))
    if new_mean!=low_mass*aa+high_mass*bb:
        raise AssertionError("two-group covariance identity residual")
    return next_state,within,between,new_mean-before


def trajectory(state,delta,kappa,horizon=HORIZON):
    if type(horizon) is not int or horizon<0:
        raise ValueError("horizon must be a nonnegative integer")
    state=checked_state(state);params(delta,kappa)
    current=state;out=[{"state":current,"mean":population_mean(current),"change":None}]
    for _ in range(horizon):
        next_state,within,between,total=direct_step(current,delta,kappa)
        out.append({"state":next_state,"mean":population_mean(next_state),
                    "change":(within,between,total)})
        current=next_state
    return tuple(out)


def oracle_trajectory(state,delta,kappa,horizon=HORIZON):
    if type(horizon) is not int or horizon<0:
        raise ValueError("horizon must be a nonnegative integer")
    state=checked_state(state);params(delta,kappa)
    current=state;out=[{"state":current,"mean":population_mean(current),"change":None}]
    for _ in range(horizon):
        next_state,within,between,total=covariance_oracle(current,delta,kappa)
        out.append({"state":next_state,"mean":population_mean(next_state),
                    "change":(within,between,total)})
        current=next_state
    return tuple(out)


def main_results():
    worlds=[]
    for pi,pair in enumerate(START_PAIRS):
        for wi,high in enumerate(HIGH_WEIGHTS):
            start=pair+(1-high,high)
            for di,delta in enumerate(WITHIN_DELTAS):
                for ki,kappa in enumerate(BETWEEN_KAPPAS):
                    a=trajectory(start,delta,kappa)
                    b=oracle_trajectory(start,delta,kappa)
                    if a!=b:
                        raise AssertionError("two independent exact paths mismatch")
                    points=[]
                    for t,x in enumerate(a):
                        p0,p1,w0,w1=x["state"]
                        steps={"t":t,"A_in_lower_group":str(p0),
                               "A_in_higher_group":str(p1),
                               "group_low_weight":str(w0),
                               "group_high_weight":str(w1),
                               "overall_A":str(x["mean"])}
                        if x["change"] is not None:
                            W,B,T=x["change"]
                            steps["within_component"]=str(W)
                            steps["between_component"]=str(B)
                            steps["total_change"]=str(T)
                        points.append(steps)
                    worlds.append({
                        "id":f"p{pi}_w{wi}_d{di}_k{ki}",
                        "initial_fractions":[str(v) for v in pair],
                        "initial_high_group_weight":str(high),
                        "within_delta":str(delta),"between_kappa":kappa,
                        "independent_covariance_oracles_equal":True,
                        "points":points})
    if len(worlds)!=72 or len({w["id"] for w in worlds})!=72:
        raise AssertionError("frozen group factorial mismatch")
    reversal=trajectory((F(1,4),F(3,4),F(1,2),F(1,2)),F(1,4),2)[1]
    n0,n1,w0,w1=reversal["state"]
    W,B,T=reversal["change"]
    if (n0,n1,W,B,T,reversal["mean"]) != (F(13,64),F(45,64),F(-3,64),F(1,16),F(1,64),F(33,64)):
        raise AssertionError("prescored group-versus-within reversal failed")
    return {
      "research_id":"R167",
      "evidence":"E1_ARTIFICIAL_TWO_GROUP_COVARIANCE_REWEIGHTING_ONLY",
      "original_structured_imitation_paper_reproduced":False,
      "real_group_data_used":False,
      "original_Price_formula_full_general_derivation_reproduced":False,
      "world_count":72,"timepoints_per_world":4,"worlds":worlds,
      "prespecified_reversal":{
          "both_local_frequencies_decrease":n0<F(1,4) and n1<F(3,4),
          "group0_new_A":str(n0),"group1_new_A":str(n1),
          "within_delta_component":str(W),
          "between_delta_component":str(B),
          "total_delta":str(T),
          "new_overall_A":str(reversal["mean"])
       }
    }


if __name__=="__main__":
    print(json.dumps(main_results(),sort_keys=True,indent=2,ensure_ascii=False))
