"""R164 synthetic content-salience copying, exact rational arithmetic only.

No actual experimental memory, cognitive measure, true content quality or
original psychological model coefficient is present in these artificial worlds.
"""
from __future__ import annotations

from fractions import Fraction as F
import json

STARTS=(F(1,5),F(2,5),F(3,5),F(4,5))
SALIENCE=(1,2,4)
CONTENT_COPY=(F(0),F(1,2),F(1))
RESET=(F(0),F(1,4))
HORIZON=4


def unit(value,name):
    if isinstance(value,bool) or not isinstance(value,(int,F)):
        raise ValueError(f"{name} must be exactly rational")
    p=F(value)
    if p<0 or p>1:
        raise ValueError(f"{name} outside [0,1]")
    return p


def params(r,h,e):
    if type(r) is not int or r not in SALIENCE:
        raise ValueError("salience weight must be one of 1, 2, 4")
    return r,unit(h,"content copying strength"),unit(e,"symmetric replacement")


def content_weight(p,r):
    p=unit(p,"A frequency")
    r,_,_=params(r,0,0)
    return r*p/(r*p+(1-p))


def direct_step(p,r,h,e):
    p=unit(p,"A frequency")
    r,h,e=params(r,h,e)
    observed=content_weight(p,r)
    copied=(1-h)*p+h*observed
    return (1-e)*copied+e/2


def urn_step(p,r,h,e):
    """Separate sum-of-masses and three-channel update, never calls direct_step."""
    p=unit(p,"A frequency")
    r,h,e=params(r,h,e)
    a_weight=p*F(r)
    b_weight=F(1)-p
    selected_A=a_weight/(a_weight+b_weight)
    # Mass of A from random selection plus separately sampled content selection.
    random_A=(F(1)-h)*p
    content_A=h*selected_A
    before_replacement=random_A+content_A
    preserved=(F(1)-e)*before_replacement
    replacement_A=e*F(1,2)
    return preserved+replacement_A


def direct_history(p0,r,h,e,horizon=HORIZON):
    if type(horizon) is not int or horizon<0:
        raise ValueError("nonnegative integer horizon required")
    p=unit(p0,"initial A prevalence")
    params(r,h,e)
    out=[p]
    for _ in range(horizon):
        p=direct_step(p,r,h,e)
        out.append(p)
    return tuple(out)


def urn_history(p0,r,h,e,horizon=HORIZON):
    if type(horizon) is not int or horizon<0:
        raise ValueError("nonnegative integer horizon required")
    p=unit(p0,"initial A prevalence")
    params(r,h,e)
    values=[p]
    for _ in range(horizon):
        p=urn_step(p,r,h,e)
        values.append(p)
    return tuple(values)


def analytic_full_copy_no_reset(p0,r,t):
    p=unit(p0,"initial")
    r,_,_=params(r,1,0)
    if type(t) is not int or t<0:
        raise ValueError("time must be nonnegative integer")
    return F(r**t)*p/(1-p+F(r**t)*p)


def analytic_only_reset(p0,e,t):
    p0=unit(p0,"initial")
    e=unit(e,"reset")
    if type(t) is not int or t<0:
        raise ValueError("invalid time")
    return F(1,2)+(1-e)**t*(p0-F(1,2))


def result_document():
    rows=[]
    for pi,p0 in enumerate(STARTS):
        for ri,r in enumerate(SALIENCE):
            for hi,h in enumerate(CONTENT_COPY):
                for ei,e in enumerate(RESET):
                    direct=direct_history(p0,r,h,e)
                    independent=urn_history(p0,r,h,e)
                    if direct!=independent or len(direct)!=5:
                        raise AssertionError("independent exact salience paths differ")
                    if any(not F(0)<=x<=F(1) for x in direct):
                        raise AssertionError("invalid probability state")
                    steps=[]
                    for t in range(5):
                        p=direct[t]
                        favored=content_weight(p,r)
                        copied=(1-h)*p+h*favored
                        obj={
                            "t":t,
                            "A_frequency":str(p),
                            "content_weighted_A":str(favored),
                            "before_symmetric_reset_A":str(copied)
                        }
                        if t<4:
                            obj["next_A"]=str(direct[t+1])
                            if (1-e)*copied+e/2 != direct[t+1]:
                                raise AssertionError("exact transition mismatch")
                        steps.append(obj)
                    rows.append({
                        "id":f"p{pi}_r{ri}_h{hi}_e{ei}",
                        "initial_A":str(p0),
                        "salience_multiplier":r,
                        "content_copy_strength":str(h),
                        "symmetric_reset":str(e),
                        "two_exact_independent_routes_equal":True,
                        "points":steps
                    })
    if len(rows)!=72 or len({row["id"] for row in rows})!=72:
        raise AssertionError("frozen 72 worlds not identified")
    ctl={
        "r4_p_one_fifth_weighted_A":str(content_weight(F(1,5),4)),
        "r2_p_four_fifths_h1_reset_quarter_next":str(direct_step(F(4,5),2,1,F(1,4))),
        "r2_p_four_fifths_h1_reset_quarter_decreases_prevalence":
             direct_step(F(4,5),2,1,F(1,4))<F(4,5),
        "all_r_equal_if_content_copy_is_zero":all(
            direct_history(p,1,0,F(1,4))==direct_history(p,r,0,F(1,4))
            for p in STARTS for r in SALIENCE),
        "all_h_equal_when_r_is_one":all(
            direct_history(p,1,0,F(1,4))==direct_history(p,1,h,F(1,4))
            for p in STARTS for h in CONTENT_COPY)
    }
    if ctl["r4_p_one_fifth_weighted_A"]!="1/2" or ctl["r2_p_four_fifths_h1_reset_quarter_next"]!="19/24":
        raise AssertionError("frozen controls not matched")
    return {
        "research_id":"R164",
        "evidence":"E1_SYNTHETIC_CONTENT_SELECTION_FRACTION_ONLY",
        "original_author_recall_models_recreated":False,
        "human_recall_or_transmission_data_used":False,
        "salience_as_measured_validity_claimed":False,
        "frozen_world_count":72,
        "five_timepoints_per_world":5,
        "worlds":rows,
        "controls":ctl
    }


def main():
    print(json.dumps(result_document(),indent=2,sort_keys=True,ensure_ascii=False))


if __name__=="__main__":
    main()
