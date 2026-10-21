"""R159 synthetic cultural majority transmission with exact Fraction arithmetic.

Only a project-authored one-trait imitation analogue, not an original genetic
and cultural dual-inheritance system and not historical behavioral evidence.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import json

INITIAL_FREQUENCIES=(F(1,4),F(2,5),F(3,5),F(3,4))
CONFORMISM=(F(0),F(1,4),F(1,2),F(1))
RESET=(F(0),F(1,10),F(1,4))
HORIZON=6


def unit(value, name):
    if isinstance(value,bool) or not isinstance(value,(F,int)):
        raise ValueError(f"{name} must be integer or Fraction")
    value=F(value)
    if not 0<=value<=1:
        raise ValueError(f"{name} must be in [0,1]")
    return value


def majority_polynomial(p):
    p=unit(p,"frequency")
    return 3*p*p-2*p*p*p


def majority_enumerated(p):
    """All eight independent 3-demonstrator outcomes, separate polynomial oracle."""
    p=unit(p,"frequency")
    total=F(0)
    for triple in product((0,1),repeat=3):
        n=sum(triple)
        if n>=2:
            total+=(p**n)*((1-p)**(3-n))
    return total


def direct_history(p0,h,u,horizon=HORIZON):
    if isinstance(horizon,bool) or not isinstance(horizon,int) or horizon<0:
        raise ValueError("horizon must be a nonnegative integer")
    p,h,u=unit(p0,"initial frequency"),unit(h,"conformism"),unit(u,"reset")
    values=[p]
    for _ in range(horizon):
        conform=majority_polynomial(p)
        p=(1-u)*((1-h)*p+h*conform)+u/2
        values.append(p)
    return tuple(values)


def independent_history(p0,h,u,horizon=HORIZON):
    """Independent enumerated majority route, never uses majority_polynomial."""
    if isinstance(horizon,bool) or not isinstance(horizon,int) or horizon<0:
        raise ValueError("horizon must be a nonnegative integer")
    value=unit(p0,"initial frequency")
    h,u=unit(h,"conformism"),unit(u,"reset")
    result=[value]
    for _ in range(horizon):
        # Deliberately enumerate copying mechanisms separately from direct_history.
        favorable=F(0)
        for b0 in (0,1):
            for b1 in (0,1):
                for b2 in (0,1):
                    count=b0+b1+b2
                    if count>=2:
                        favorable+=value**count*(1-value)**(3-count)
        value=((1-u)*((1-h)*value+h*favorable))+u/2
        result.append(value)
    return tuple(result)


def result_document():
    worlds=[]
    for pi,p0 in enumerate(INITIAL_FREQUENCIES):
        for hi,h in enumerate(CONFORMISM):
            for ui,u in enumerate(RESET):
                d=direct_history(p0,h,u)
                e=independent_history(p0,h,u)
                if d!=e:
                    raise AssertionError("Fraction majority independent enumerator mismatch")
                points=[]
                for t,p in enumerate(d):
                    c=majority_polynomial(p)
                    if c!=majority_enumerated(p) or not (0<=p<=1 and 0<=c<=1):
                        raise AssertionError("probability out of bounds or disagreement")
                    points.append({"t":t,"trait_A_frequency":str(p),
                                   "independent_three_demo_majority":str(c)})
                worlds.append({
                    "case_id":f"p{pi}_h{hi}_u{ui}",
                    "initial_frequency":str(p0),"conformity_fraction":str(h),
                    "symmetric_innovation_reset":str(u),
                    "two_independent_Fraction_routes_identical":True,
                    "points":points,
                })
    if len(worlds)!=48 or len(set(x["case_id"] for x in worlds))!=48:
        raise AssertionError("frozen count mismatch")
    return {
        "research_id":"R159","evidence":"E1_SYNTHETIC_CULTURAL_COPYING_ONLY",
        "not_a_gene_culture_coevolution_model":True,
        "historical_cultural_data_used":False,
        "author_original_equations_reproduced":False,
        "scenario_count":48,"observations_per_world":7,
        "worlds":worlds,
        "predeclared_controls":{
            "majority_at_quarter":str(majority_polynomial(F(1,4))),
            "majority_at_half":str(majority_polynomial(F(1,2))),
            "majority_at_threequarters":str(majority_polynomial(F(3,4))),
            "equilibrium_half_maintained_for_all_h_u":all(
                all(x==F(1,2) for x in direct_history(F(1,2),h,u))
                for h in CONFORMISM for u in RESET),
            "zero_reset_full_conformist_quarter_at_t6":
                str(direct_history(F(1,4),1,0)[-1]),
            "no_conformism_no_reset_remains_constant":
                all(all(x==p0 for x in direct_history(p0,0,0))
                    for p0 in INITIAL_FREQUENCIES),
        }
    }


def main():
    print(json.dumps(result_document(),sort_keys=True,indent=2,ensure_ascii=False))


if __name__=='__main__':
    main()
