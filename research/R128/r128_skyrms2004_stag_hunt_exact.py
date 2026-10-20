#!/usr/bin/env python3
"""R128 exact primary Skyrms (2004), chapter 1 Stag Hunt pp3,5,10-12.

Primary publisher excerpt: https://assets.cambridge.org/052182/6519/sample/0521826519ws.pdf
Rousseau 1755 original hunting anecdote contains NO modern payoff matrix.
Other n-player threshold, dependence and discrete map are explicitly
PROJECT-CREATED counterexamples, not Skyrms human results.
No 2001 Battalio experimental participant rows have been loaded.
"""
from __future__ import annotations
from fractions import Fraction as F
from itertools import product
import json


class StagHuntError(ValueError):
    pass


def _prob(q, allow_one=True):
    if type(q) is not F or not F(0)<=q<=F(1) or (not allow_one and q==F(1)):
        raise StagHuntError("R128_EXACT_FRACTION_PROBABILITY_RANGE")
    return q


def _n(n):
    if type(n) is not int or not 2<=n<=8:
        raise StagHuntError("R128_N_INT_2_THROUGH_8")
    return n


def _actions(actions):
    if type(actions) not in (tuple,list):
        raise StagHuntError("R128_EXPLICIT_ACTIONS_REQUIRED")
    _n(len(actions))
    if any(type(v) is not str or v not in ("S","H") for v in actions):
        raise StagHuntError("R128_ONLY_S_OR_H_ACTIONS")
    return tuple(actions)


def skyrms_original_two_person_payoff():
    """Book p3 exactly: hare=3 always, stag with stag=4, alone=0."""
    return ((F(4),F(0)),(F(3),F(3)))


def stag_profile_payoffs(actions):
    """PROJECT n-player all-or-nothing extension, NOT source experiment."""
    acts=_actions(actions)
    all_stag=all(a=="S" for a in acts)
    return tuple(F(3) if a=="H" else (F(4) if all_stag else F(0))
                 for a in acts)


def best_action_given_success_probability(p_success):
    """Here p_success is the JOINT probability all necessary others cooperate."""
    p=_prob(p_success)
    stag=4*p
    hare=F(3)
    return {
        "expected_stag":stag,
        "expected_hare":hare,
        "best":"S" if stag>hare else "H" if stag<hare else "TIE",
    }


def independence_prediction(n,p):
    """Exact analytic assuming INDEPENDENT identical marginal beliefs p."""
    n=_n(n);p=_prob(p)
    joint=p**(n-1)
    result=best_action_given_success_probability(joint)
    return {"n":n,"marginal_each_other":p,
            "joint_all_other_stag":joint,**result}


def exhaustive_other_action_probabilities(n,p):
    """Second independent enumeration of all 2**(n-1) ordered profiles."""
    n=_n(n);p=_prob(p)
    total=F(0);joint=F(0);expected_stag=F(0);count=0
    for profile in product(("S","H"),repeat=n-1):
        mass=F(1)
        for action in profile:
            mass *= p if action=="S" else (F(1)-p)
        total+=mass
        stag_payoff=stag_profile_payoffs(("S",)+profile)[0]
        joint+=mass*int(all(action=="S" for action in profile))
        expected_stag+=mass*stag_payoff
        count+=1
    if total!=1:
        raise StagHuntError("R128_INDEPENDENT_PROFILE_PROBABILITIES_NOT_NORMALIZED")
    return {"profiles":count,"mass_total":total,"joint_all_stag":joint,
            "expected_stag":expected_stag}


def validate_two_other_joint(joint):
    """Explicit probabilities in order SS,SH,HS,HH; NO implicit independence."""
    if type(joint) not in (tuple,list) or len(joint)!=4:
        raise StagHuntError("R128_JOINT_FOUR_EXPLICIT_CELLS")
    z=tuple(_prob(x) for x in joint)
    if sum(z,F(0))!=1:
        raise StagHuntError("R128_JOINT_PROBABILITIES_SUM_NOT_ONE")
    return z


def joint_two_other_beliefs(joint):
    a,b,c,d=validate_two_other_joint(joint)
    mass_a_stag=a+b
    mass_b_stag=a+c
    decision=best_action_given_success_probability(a)
    return {
        "joint_all_stag":a,
        "marginal_other1_stag":mass_a_stag,
        "marginal_other2_stag":mass_b_stag,
        **decision,
    }


def frozen_correlated_trust_counterexample():
    """Same 4/5 marginals; THREE distinct full joint laws, best action flips."""
    distributions={
        "independent":(F(16,25),F(4,25),F(4,25),F(1,25)),
        "perfect_positive_correlation":(F(4,5),F(0),F(0),F(1,5)),
        "minimum_possible_joint":(F(3,5),F(1,5),F(1,5),F(0)),
    }
    out={}
    for key,mass in distributions.items():
        result=joint_two_other_beliefs(mass)
        if result["marginal_other1_stag"]!=F(4,5) or result["marginal_other2_stag"]!=F(4,5):
            raise StagHuntError("R128_EXACT_SAME_MARGINALS_NOT_MET")
        out[key]={
            "probability_SS":str(result["joint_all_stag"]),
            "expected_stag":str(result["expected_stag"]),
            "expected_hare":str(result["expected_hare"]),
            "best":result["best"],
            "four_profile_masses":[str(v) for v in mass],
        }
    if [out[k]["best"] for k in distributions]!=["H","S","H"]:
        raise StagHuntError("R128_DIFFERENT_CORRELATIONS_NOT_SWITCHING_ACTION")
    return {"same_individual_marginal_each":"4/5",
            "distributions":out,
            "real_human_belief_distribution_observed":False}


def independent_group_full_audit():
    probs=(F(0),F(1,4),F(1,2),F(3,4),F(4,5),F(1))
    profile_comparisons=0
    combinations_count=0
    cases=[]
    for n in range(2,9):
        for p in probs:
            expected=independence_prediction(n,p)
            enumeration=exhaustive_other_action_probabilities(n,p)
            if enumeration["joint_all_stag"]!=expected["joint_all_other_stag"]:
                raise StagHuntError("R128_ANALYTIC_JOINT_VS_EXHAUSTION_DIVERGED")
            if enumeration["expected_stag"]!=expected["expected_stag"]:
                raise StagHuntError("R128_GROUP_PAYOFF_VS_EXHAUSTION_DIVERGED")
            if enumeration["profiles"]!=2**(n-1):
                raise StagHuntError("R128_NOT_ALL_OTHER_AGENT_PROFILES_ENUMERATED")
            profile_comparisons+=enumeration["profiles"]
            combinations_count+=1
            cases.append({"n":n,"individual_marginal":str(p),
                          "joint_all_stag":str(expected["joint_all_other_stag"]),
                          "best":expected["best"]})
    if profile_comparisons!=1524 or combinations_count!=42:
        raise StagHuntError("R128_N2_TO8_SIX_PROB_COVERAGE_NOT_COMPLETE")
    return {"n":list(range(2,9)),
            "independent_marginals":["0","1/4","1/2","3/4","4/5","1"],
            "independent_n_probability_combinations":combinations_count,
            "complete_independent_agent_profile_mass_computations":profile_comparisons,
            "all_analytic_vs_independent_enumeration_agreed":True,
            "n2_p4over5_best":next(t["best"] for t in cases if t["n"]==2 and t["individual_marginal"]=="4/5"),
            "n3_p4over5_best":next(t["best"] for t in cases if t["n"]==3 and t["individual_marginal"]=="4/5")}


def _delta(delta):
    return _prob(delta,allow_one=False)


def repeated_pd_infinite_payoffs(delta):
    """Exact FIRST-PARTY Skyrms ch1 p5 shadow of future example.

    Restricts pure strategies to Trigger (cooperate until rival first defects,
    then defect forever) and Foole (always defect). No hidden data and no
    claims about other repeated-game strategies.
    """
    d=_delta(delta)
    inv=F(1)/(F(1)-d)
    return ((F(2)*inv,d*inv),(F(3)+d*inv,inv))


def _stage_pd_bimatrix(row_action,col_action):
    if (row_action,col_action)==("C","C"):return (F(2),F(2))
    if (row_action,col_action)==("C","D"):return (F(0),F(3))
    if (row_action,col_action)==("D","C"):return (F(3),F(0))
    if (row_action,col_action)==("D","D"):return (F(1),F(1))
    raise StagHuntError("R128_UNRECOGNIZED_PRISONERS_DILEMMA_ACTION")


def _strategies(s1,s2):
    if s1 not in ("T","F") or s2 not in ("T","F") or type(s1) is not str or type(s2) is not str:
        raise StagHuntError("R128_ONLY_TRIGGER_OR_FOOLE_STRATEGIES")
    return s1,s2


def discounted_pd_prefix(s1,s2,delta,rounds):
    """Independent finite-round first-player payoff via explicit action path.

    For round 0 T=C,F=D; once one agent D both will play D
    beginning round1 (unless both T, continue C forever).
    """
    s1,s2=_strategies(s1,s2)
    d=_delta(delta)
    if type(rounds) is not int or not 1<=rounds<=12:
        raise StagHuntError("R128_PREFIX_ROUNDS_INT_1_TO12")
    total=F(0)
    actions=[]
    for t in range(rounds):
        first=("C" if s1=="T" and (t==0 or s2=="T") else "D")
        second=("C" if s2=="T" and (t==0 or s1=="T") else "D")
        row_payoff,_=_stage_pd_bimatrix(first,second)
        total+=d**t*row_payoff
        actions.append(first+second)
    return {"row_discounted_total":total,"stage_action_pairs":tuple(actions)}


def discounted_pd_tail(s1,s2,delta,rounds):
    """Analytic exact infinite sum tail after explicitly modeled prefix.

    At all t>=1, only TT gets 2; all other combinations get 1.
    """
    s1,s2=_strategies(s1,s2)
    d=_delta(delta)
    if type(rounds) is not int or not 1<=rounds<=12:
        raise StagHuntError("R128_TAIL_HORIZON")
    return d**rounds*(F(2) if (s1,s2)==("T","T") else F(1))/(F(1)-d)


def true_repeated_coordination_selection(delta):
    """Payoff- and risk-select at the two restricted strategies ONLY."""
    d=_delta(delta)
    matrix=repeated_pd_infinite_payoffs(d)
    aa,ab=matrix[0]
    ba,bb=matrix[1]
    is_two_strict=aa>ba and bb>ab
    if not is_two_strict:
        return {"two_strict_diagonal_Nash":False,
                "Trigger_Strict_Nash":aa>ba,
                "Foole_Strict_Nash":bb>ab,
                "threshold_opponent_Trigger":None,
                "risk_dominant":None}
    delta_trigger=aa-ba
    delta_foole=bb-ab
    q=delta_foole/(delta_trigger+delta_foole)
    loss_product_trigger=delta_trigger**2
    loss_product_foole=delta_foole**2
    if q!=(1-d)/d:
        raise StagHuntError("R128_SKYRMS_SHADOW_MIXED_THRESHOLD_DIVERGED")
    return {
        "two_strict_diagonal_Nash":True,"Trigger_Strict_Nash":True,"Foole_Strict_Nash":True,
        "threshold_opponent_Trigger":q,
        "risk_dominant":"T" if loss_product_trigger>loss_product_foole else
                        "F" if loss_product_foole>loss_product_trigger else "TIE",
        "payoff_dominant":"T" if aa>bb else "F" if aa<bb else "TIE",
        "loss_product_Trigger":loss_product_trigger,
        "loss_product_Foole":loss_product_foole,
    }


def original_skyrms_printed_transformation():
    mat=repeated_pd_infinite_payoffs(F(3,5))
    must=((F(5),F(3,2)),(F(9,2),F(5,2)))
    if mat!=must:
        raise StagHuntError("R128_ORIGINAL_SKYRMS_P5_PRINTED_NUMBERS_WRONG")
    for s1,i in (("T",0),("F",1)):
        for s2,j in (("T",0),("F",1)):
            result=discounted_pd_prefix(s1,s2,F(3,5),12)
            if result["row_discounted_total"]+discounted_pd_tail(s1,s2,F(3,5),12)!=mat[i][j]:
                raise StagHuntError("R128_SECOND_INDEPENDENT_PD_SUM_DOES_NOT_MATCH_SOURCE")
    select=true_repeated_coordination_selection(F(3,5))
    if not select["two_strict_diagonal_Nash"] or select["risk_dominant"]!="F" or select["threshold_opponent_Trigger"]!=F(2,3):
        raise StagHuntError("R128_REPEATED_PD_RISK_SOURCE_BOUNDARY_DRIFT")
    return {
        "original_printed_book_p5_row_matrix":[[str(v) for v in row] for row in mat],
        "original_prisoners_dilemma_one_round_matrix":[["2","0"],["3","1"]],
        "continuation_discount":"3/5",
        "independent_twelve_round_prefix_plus_exact_tail_reconciled":True,
        "project_derived_Trigger_probability_threshold":str(select["threshold_opponent_Trigger"]),
        "project_derived_risk_dominant_given_two_strategies":select["risk_dominant"],
        "not_a_general_subgame_perfect_equilibrium_characterization":True,
    }


def source_inspired_project_discrete_share_step(x):
    """PROJECT discrete replicator teaching map, not author empirical curve.

    Stag relative payoff 4*x; hare payoff 3; random mix population premise.
    """
    p=_prob(x)
    denominator=p*(4*p)+(F(1)-p)*F(3)
    if denominator<=0:
        raise StagHuntError("R128_ZERO_FITNESS_DISCRETE_MAP")
    out=p*(4*p)/denominator
    if not F(0)<=out<=F(1):
        raise StagHuntError("R128_DISCRETE_MAP_NOT_PROBABILITY")
    return out


def small_source_inspired_dynamics_audit():
    points=(F(0),F(1,4),F(1,2),F(2,3),F(3,4),F(4,5),F(9,10),F(1))
    out={}
    for x in points:
        nxt=source_inspired_project_discrete_share_step(x)
        expected="FIXED" if x in (F(0),F(3,4),F(1)) else "DOWN" if x<F(3,4) else "UP"
        actual="FIXED" if nxt==x else "DOWN" if nxt<x else "UP"
        if expected!=actual:
            raise StagHuntError("R128_DISCRETE_REPLICATOR_DIRECTION_WRONG")
        out[str(x)]={"next_share":str(nxt),"direction":actual}
    return {"discrete_map_project_not_book_formula":True,
            "source_book_p11_basin_boundary":"3/4",
            "fixed_points":["0","3/4","1"],"cases":out}


def independent_longrun_source_test_audit():
    deltas=(F(0),F(1,4),F(1,2),F(3,5),F(2,3),F(3,4),F(9,10))
    verified=0
    for d in deltas:
        mat=repeated_pd_infinite_payoffs(d)
        for i,s1 in enumerate(("T","F")):
            for j,s2 in enumerate(("T","F")):
                for horizon in (1,2,4,7,12):
                    y=discounted_pd_prefix(s1,s2,d,horizon)
                    tail=discounted_pd_tail(s1,s2,d,horizon)
                    if y["row_discounted_total"]+tail!=mat[i][j]:
                        raise StagHuntError("R128_INFINITE_VS_FINITE_PLUS_EXACT_TAIL_DISAGREE")
                    verified+=1
    if verified!=140:
        raise StagHuntError("R128_NOT_140_TRUE_DISCOUNTED_SUM_IDENTITIES")
    return {
        "discount_factors":[str(x) for x in deltas],
        "four_strategy_combinations_per_discount":4,
        "five_finite_prefix_horizons_each":[1,2,4,7,12],
        "mathematically_exact_prefix_plus_tail_checks":verified,
        "book_actual_human_microdata_reproduced":False,
    }


def project_research_receipt():
    return {
        "id":"R128","original_catalogue":"05-004",
        "Skyrms2004_primary_book_chapter_p3_payoffs":[[str(y) for y in x] for x in skyrms_original_two_person_payoff()],
        "book_2004_primary_repeated_pd_payoff_matrix":original_skyrms_printed_transformation(),
        "project_own_independence_7_group_sizes_six_probabilities":independent_group_full_audit(),
        "project_different_dependence_same_marginals":frozen_correlated_trust_counterexample(),
        "project_discount_horizon_checks":independent_longrun_source_test_audit(),
        "project_discrete_map_not_original_book_estimand":small_source_inspired_dynamics_audit(),
        "new_real_person_E2_prediction_scores":0,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }


if __name__=="__main__":
    print(json.dumps(project_research_receipt(),sort_keys=True,indent=2))
