"""R163 synthetic payoff-sensitive one-step copying, exact rational outcomes.

The 6 payoff profiles and every true correct token are artificial. Only the
literature's distinctions between success signals and social learning rules
motivate the exercise. No original author's full dynamical model is reproduced.
"""
from __future__ import annotations
from fractions import Fraction as F
import json

PROFILES = (
    ("A_outlier", (1,1,0), (12,0,8)),
    ("B_outlier", (1,0,0), (8,12,0)),
    ("A_agreement", (1,1,0), (10,9,2)),
    ("B_agreement", (1,0,0), (2,10,9)),
    ("best_tie", (1,0,0), (8,8,2)),
    ("mean_tie", (1,1,0), (8,0,4)),
)
TRANSFORMS = ("raw", "reverse", "flat")
STRATEGIES = ("best", "means")
CORRECT_TOKENS = (0,1)


def valid_actions(values):
    if not isinstance(values, (list,tuple)) or len(values) != 3:
        raise ValueError("exactly three synthetic actions required")
    if any(type(x) is not int or x not in (0,1) for x in values):
        raise ValueError("synthetic actions must be 0 or 1 integers")
    if 0 not in values or 1 not in values:
        raise ValueError("this 72-case contrast requires both cultural variants")
    return tuple(values)


def valid_payoffs(values):
    if not isinstance(values,(list,tuple)) or len(values)!=3:
        raise ValueError("exactly three payoff signals required")
    if any(type(x) is not int or x<0 or x>12 for x in values):
        raise ValueError("payoff signals must be integers 0..12")
    return tuple(values)


def valid_controls(transform,strategy,correct):
    if transform not in TRANSFORMS or not isinstance(transform,str):
        raise ValueError("unknown frozen payoff transform")
    if strategy not in STRATEGIES or not isinstance(strategy,str):
        raise ValueError("unknown success copying strategy")
    if type(correct) is not int or correct not in CORRECT_TOKENS:
        raise ValueError("synthetic correctness token must be 0 or 1")
    return transform,strategy,correct


def transformed(payoffs,transform):
    scores=valid_payoffs(payoffs)
    if transform not in TRANSFORMS or not isinstance(transform,str):
        raise ValueError("unknown display transformation")
    if transform=="raw":
        return scores
    if transform=="reverse":
        return tuple(12-x for x in scores)
    return (6,6,6)


def direct_choice(actions,payoffs,strategy):
    actions=valid_actions(actions)
    payoffs=valid_payoffs(payoffs)
    if strategy=="best":
        highest=max(payoffs)
        winners=[i for i,v in enumerate(payoffs) if v==highest]
        return F(sum(actions[i] for i in winners),len(winners))
    if strategy=="means":
        means={}
        for a in (0,1):
            selected=[v for i,v in enumerate(payoffs) if actions[i]==a]
            means[a]=F(sum(selected),len(selected))
        if means[1]>means[0]:
            return F(1)
        if means[1]<means[0]:
            return F(0)
        return F(1,2)
    raise ValueError("unknown strategy")


def enumerated_choice(actions,payoffs,strategy):
    """Independent enumeration/cross products, no calls to direct_choice."""
    actions=valid_actions(actions)
    payoffs=valid_payoffs(payoffs)
    if strategy=="best":
        sorted_values=sorted(payoffs,reverse=True)
        champion=sorted_values[0]
        votes=[]
        for index in range(len(payoffs)):
            if payoffs[index]==champion:
                votes.append(actions[index])
        return F(sum(votes),len(votes))
    if strategy=="means":
        sumA=sum(payoffs[i] for i in range(3) if actions[i]==1)
        numA=sum(actions)
        sumB=sum(payoffs[i] for i in range(3) if actions[i]==0)
        numB=3-numA
        comparison=sumA*numB-sumB*numA
        if comparison>0:
            return F(1)
        if comparison<0:
            return F(0)
        # Draw from the two represented *variants*, not the three persons.
        return F(sum(v for v in (0,1)),2)
    raise ValueError("unknown strategy")


def direct_case(actions,payoffs,transform,strategy,correct):
    transform,strategy,correct=valid_controls(transform,strategy,correct)
    actions=valid_actions(actions)
    displayed=transformed(payoffs,transform)
    pA=direct_choice(actions,displayed,strategy)
    base=F(sum(actions),3)
    accuracy=pA if correct==1 else F(1)-pA
    base_accuracy=base if correct==1 else F(1)-base
    return (pA,base,accuracy,base_accuracy,accuracy-base_accuracy)


def enumerated_case(actions,payoffs,transform,strategy,correct):
    transform,strategy,correct=valid_controls(transform,strategy,correct)
    actions=valid_actions(actions)
    displayed=transformed(payoffs,transform)
    pA=enumerated_choice(actions,displayed,strategy)
    baseline=F(len([v for v in actions if v==1]),3)
    success=F(pA) if correct==1 else F(1)-pA
    neutral=baseline if correct==1 else F(1)-baseline
    return (pA,baseline,success,neutral,success-neutral)


def document():
    cases=[]
    for pi,(name,actions,payoffs) in enumerate(PROFILES):
        for ti,transform in enumerate(TRANSFORMS):
            for si,strategy in enumerate(STRATEGIES):
                for ci,correct in enumerate(CORRECT_TOKENS):
                    a=direct_case(actions,payoffs,transform,strategy,correct)
                    b=enumerated_case(actions,payoffs,transform,strategy,correct)
                    if a!=b:
                        raise AssertionError("independent rational strategy checks disagree")
                    if any(not (F(0)<=x<=F(1)) for x in a[:4]):
                        raise AssertionError("copying/accuracy outside probability range")
                    cases.append({
                        "id":f"p{pi}_t{ti}_s{si}_c{ci}",
                        "profile_name":name,
                        "demonstrator_actions":list(actions),
                        "original_display_payoffs":list(payoffs),
                        "transformation":transform,
                        "displayed_payoffs":list(transformed(payoffs,transform)),
                        "copying_strategy":strategy,
                        "synthetic_correct_action":correct,
                        "probability_copy_A":str(a[0]),
                        "random_person_baseline_copy_A":str(a[1]),
                        "synthetic_accuracy":str(a[2]),
                        "synthetic_baseline_accuracy":str(a[3]),
                        "advantage_over_random_person":str(a[4]),
                        "independent_exact_oracles_equal":True,
                    })
    if len(cases)!=72 or len({c["id"] for c in cases})!=72:
        raise AssertionError("frozen factorial cases not exhausted")

    p0=PROFILES[0]
    p1=PROFILES[1]
    p4=PROFILES[4]
    p5=PROFILES[5]
    ctl={
        "A_outlier_raw_imitate_best_A":str(direct_choice(p0[1],p0[2],"best")),
        "A_outlier_raw_compare_means_A":str(direct_choice(p0[1],p0[2],"means")),
        "B_outlier_raw_imitate_best_A":str(direct_choice(p1[1],p1[2],"best")),
        "B_outlier_raw_compare_means_A":str(direct_choice(p1[1],p1[2],"means")),
        "best_tie_raw_best_A":str(direct_choice(p4[1],p4[2],"best")),
        "best_tie_raw_means_A":str(direct_choice(p4[1],p4[2],"means")),
        "mean_tie_raw_best_A":str(direct_choice(p5[1],p5[2],"best")),
        "mean_tie_raw_means_A":str(direct_choice(p5[1],p5[2],"means")),
        "A_outlier_best_A_correct_gain":str(direct_case(p0[1],p0[2],"raw","best",1)[-1]),
        "A_outlier_best_B_correct_loss":str(direct_case(p0[1],p0[2],"raw","best",0)[-1]),
        "flat_A_outlier_best_A":str(direct_case(p0[1],p0[2],"flat","best",1)[0]),
        "flat_A_outlier_means_A":str(direct_case(p0[1],p0[2],"flat","means",1)[0]),
    }
    fixed={
        "A_outlier_raw_imitate_best_A":"1",
        "A_outlier_raw_compare_means_A":"0",
        "B_outlier_raw_imitate_best_A":"0",
        "B_outlier_raw_compare_means_A":"1",
        "best_tie_raw_best_A":"1/2",
        "best_tie_raw_means_A":"1",
        "mean_tie_raw_best_A":"1",
        "mean_tie_raw_means_A":"1/2",
        "A_outlier_best_A_correct_gain":"1/3",
        "A_outlier_best_B_correct_loss":"-1/3",
        "flat_A_outlier_best_A":"2/3",
        "flat_A_outlier_means_A":"1/2",
    }
    if ctl != fixed:
        raise AssertionError(f"protocol expected contrasting outcomes {ctl} != {fixed}")
    return {
        "research_id":"R163",
        "evidence":"E1_SYNTHETIC_STATIC_PAYOFF_BIAS_ONLY",
        "original_Baldini_dynamics_recreated":False,
        "Mesoudi_human_behavior_data_reused":False,
        "real_success_signal_reliability_estimated":False,
        "world_count":72,
        "methods":["Compare Means artificial within-variant payoff mean","Imitate the Best artificial highest individual payoff"],
        "tie_convention":"best: equal highest-score persons uniformly; means: equal-mean represented cultural variants uniformly",
        "worlds":cases,
        "prespecified_counterexamples":ctl,
    }


def main():
    print(json.dumps(document(),sort_keys=True,indent=2,ensure_ascii=False))


if __name__=="__main__":
    main()
