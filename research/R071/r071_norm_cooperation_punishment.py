#!/usr/bin/env python3
"""R071 E1: fixed-strategy five-agent norm feedback and costly enforcement.

Not a Fehr/Gaechter or Boyd evolutionary-model reproduction. No human data.
"""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import product
import json
import math
from pathlib import Path

STRATEGIES=("C","D","P","N")
INSTITUTIONS={
    "NONE":{"fine":0.,"variable_cost":0.,"monitor_cost":0.},
    "VARIABLE_PUNISHMENT":{"fine":.8,"variable_cost":.2,"monitor_cost":0.},
    "FIXED_MONITORING":{"fine":.8,"variable_cost":.2,"monitor_cost":1.2},
}
THRESHOLDS=(.5,.75)
INITIAL_NORMS=(0.,1.)
N=5
BENEFIT=2.
CONTRIBUTION_COST=1.
STEPS=8
EXPECTED_COMPOSITIONS=56
EXPECTED_CASES=EXPECTED_COMPOSITIONS*len(THRESHOLDS)*len(INITIAL_NORMS)*len(INSTITUTIONS)


def compositions():
    for c in range(N+1):
        for d in range(N-c+1):
            for p in range(N-c-d+1):
                n=N-c-d-p
                yield (c,d,p,n)


def check_config(group,theta,initial_norm,institution,rounds):
    if (not isinstance(group,(tuple,list)) or len(group)!=4 or
        any(type(x) is not int or x<0 for x in group) or sum(group)!=N):
        raise ValueError("fixed composition must contain five nonnegative integer roles C/D/P/N")
    if not isinstance(theta,(int,float)) or not math.isfinite(theta) or not 0<=theta<=1:
        raise ValueError("theta must be finite inside [0,1]")
    if initial_norm not in INITIAL_NORMS or type(initial_norm) not in (int,float):
        raise ValueError("initial public norm only 0 or 1")
    if institution not in INSTITUTIONS:
        raise ValueError("unknown institution")
    if type(rounds) is not int or not 1<=rounds<=40:
        raise ValueError("invalid finite step count")
    return tuple(group)


def calculate_round(group,previous_coop_fraction,theta,institution):
    g=check_config(group,theta,0.,institution,1)
    if (not isinstance(previous_coop_fraction,(int,float))
        or not math.isfinite(previous_coop_fraction)
        or not 0<=previous_coop_fraction<=1):
        raise ValueError("previous cooperation fraction outside probability interval")
    c,d,p,n=g
    fine=INSTITUTIONS[institution]["fine"]
    k=INSTITUTIONS[institution]["variable_cost"]
    m=INSTITUTIONS[institution]["monitor_cost"]
    # N's utility difference between cooperating and not cooperating:
    # own share of extra group return minus contribution cost plus avoided fine.
    marginal=BENEFIT/N-CONTRIBUTION_COST+fine*p
    norm_action=(previous_coop_fraction>=theta) or (fine>0 and marginal>=0)
    n_coop=n if norm_action else 0
    coop=c+p+n_coop
    noncoop=N-coop
    public_return=BENEFIT*coop/N
    payoffs={
        "C":public_return-CONTRIBUTION_COST,
        "D":public_return-fine*p,
        "P":public_return-CONTRIBUTION_COST-k*noncoop-m,
        "N":public_return-CONTRIBUTION_COST if norm_action else public_return-fine*p,
    }
    all_sum=sum(payoffs[s]*g[i] for i,s in enumerate(STRATEGIES))
    accounting=BENEFIT*coop-CONTRIBUTION_COST*coop-(
        fine+k)*p*noncoop-m*p
    if not math.isclose(all_sum,accounting,abs_tol=1e-9,rel_tol=1e-12):
        raise ValueError("institution fiscal accounting balance failed")
    if not 0<=coop<=N:
        raise ValueError("cooperation action out of range")
    return {
        "prior_coop_fraction":previous_coop_fraction,
        "N_strategy_cooperates":bool(norm_action),
        "N_current_contributors":n_coop,
        "contributor_count":coop,
        "noncontributor_count":noncoop,
        "contributor_fraction":coop/N,
        "marginal_payoff_N_coop_vs_defect":marginal,
        "per_role_payoff":payoffs,
        "group_total_payoff":all_sum,
        "accounting_expected_total":accounting,
        "sanction_event_count":p*noncoop if fine>0 else 0,
        "monitoring_cost_total":m*p,
        "variable_sanction_cost_total":k*p*noncoop,
        "destructive_fines_total":fine*p*noncoop,
    }


def run(group,theta,initial_norm,institution,rounds=STEPS):
    g=check_config(group,theta,initial_norm,institution,rounds)
    preceding=float(initial_norm)
    history=[]
    for t in range(1,rounds+1):
        r=calculate_round(g,preceding,theta,institution)
        r["round"]=t
        history.append(r)
        preceding=r["contributor_fraction"]
    if len(history)!=rounds:
        raise ValueError("round count drifted")
    return {
        "composition_by_C_D_P_N":list(g),
        "theta":theta,
        "initial_public_norm":initial_norm,
        "institution":institution,
        "rounds":rounds,
        "trajectory":history,
        "end_contributor_count":history[-1]["contributor_count"],
        "end_fraction":history[-1]["contributor_fraction"],
        "average_contributor_fraction":sum(x["contributor_fraction"] for x in history)/rounds,
        "total_group_payoff_over_rounds":sum(x["group_total_payoff"] for x in history),
        "true_human_behavior_observed":False,
    }


def fixed_synthetic_witnesses():
    alln=(0,0,0,5)
    with_p=(0,0,1,4)
    against_D=(0,4,1,0)
    paths={
        "norm_seed_zero_all_N_no_sanction":run(alln,.5,0.,"NONE"),
        "norm_seed_one_all_N_no_sanction":run(alln,.5,1.,"NONE"),
        "P_one_N_four_no_punishment":run(with_p,.5,0.,"NONE"),
        "P_one_N_four_variable_punishment":run(with_p,.5,0.,"VARIABLE_PUNISHMENT"),
        "P_one_N_four_fixed_monitoring":run(with_p,.5,0.,"FIXED_MONITORING"),
        "P_one_D_four_variable_punishment":run(against_D,.5,0.,"VARIABLE_PUNISHMENT"),
        "D_five_all_regimes":{name:run((0,5,0,0),.5,0.,name)
                              for name in INSTITUTIONS},
    }
    if [paths[k]["end_contributor_count"] for k in (
            "norm_seed_zero_all_N_no_sanction",
            "norm_seed_one_all_N_no_sanction",
            "P_one_N_four_no_punishment",
            "P_one_N_four_variable_punishment",
            "P_one_N_four_fixed_monitoring",
            "P_one_D_four_variable_punishment")]!=[0,5,1,5,5,1]:
        raise ValueError("fixed E1 mechanism witness contradicted")
    for v in paths["D_five_all_regimes"].values():
        if v["end_contributor_count"]:
            raise ValueError("unresponsive D strategy falsely deterred")
    # Keep an 8-round trajectory only for small, explicitly synthetic witnesses.
    return paths


def evaluate():
    groups=list(compositions())
    if len(groups)!=EXPECTED_COMPOSITIONS or len(set(groups))!=EXPECTED_COMPOSITIONS:
        raise ValueError("56 full composition universe failed")
    aggregated={}
    source_cases={}
    total_cases=0
    for name in INSTITUTIONS:
        aggregated[name]={}
        for theta in THRESHOLDS:
            for seed in INITIAL_NORMS:
                s={"cases":0,"end_cooperators_sum":0,
                   "cooperator_round_total":0,"round_count":0,
                   "group_total_payoff_over_all_rounds":0.,
                   "all_five_cooperate_final":0,
                   "zero_cooperate_final":0,
                   "only_fixed_C_and_P_cooperate_final":0,
                   "P_and_C_coexisting_with_P_lower_payoff_final":0,
                   "costly_P_with_no_defectors_final":0}
                for group in groups:
                    z=run(group,theta,seed,name)
                    s["cases"]+=1
                    total_cases+=1
                    end=z["trajectory"][-1]
                    s["end_cooperators_sum"]+=end["contributor_count"]
                    s["cooperator_round_total"]+=sum(x["contributor_count"] for x in z["trajectory"])
                    s["round_count"]+=len(z["trajectory"])
                    s["group_total_payoff_over_all_rounds"]+=z["total_group_payoff_over_rounds"]
                    s["all_five_cooperate_final"]+=int(end["contributor_count"]==N)
                    s["zero_cooperate_final"]+=int(end["contributor_count"]==0)
                    s["only_fixed_C_and_P_cooperate_final"]+=int(end["contributor_count"]==group[0]+group[2])
                    s["P_and_C_coexisting_with_P_lower_payoff_final"]+=int(
                        group[0]>0 and group[2]>0
                        and end["per_role_payoff"]["P"]<end["per_role_payoff"]["C"]-1e-12)
                    s["costly_P_with_no_defectors_final"]+=int(
                        group[2]>0 and end["noncontributor_count"]==0 and
                        end["monitoring_cost_total"]>0)
                    source_cases[(group,theta,seed,name)]=z
                if s["cases"]!=EXPECTED_COMPOSITIONS or s["round_count"]!=EXPECTED_COMPOSITIONS*STEPS:
                    raise ValueError("group or rounds dropped")
                s["mean_final_coop_fraction_over_compositions"]=s["end_cooperators_sum"]/(N*s["cases"])
                s["mean_round_coop_fraction_over_compositions"]=s["cooperator_round_total"]/(N*s["round_count"])
                aggregated[name][f"theta={theta},initial_norm={seed}"]=s
    if total_cases!=EXPECTED_CASES:
        raise ValueError("672-case full factorial not executed")
    paired={}
    for theta in THRESHOLDS:
        for seed in INITIAL_NORMS:
            for institution in INSTITUTIONS:
                counts=Counter()
                for group in groups:
                    baseline=source_cases[(group,theta,seed,"NONE")]["end_contributor_count"]
                    trial=source_cases[(group,theta,seed,institution)]["end_contributor_count"]
                    if trial>baseline:counts["greater_than_no_institution"]+=1
                    elif trial<baseline:counts["less_than_no_institution"]+=1
                    else:counts["equal_to_no_institution"]+=1
                if sum(counts.values())!=EXPECTED_COMPOSITIONS:
                    raise ValueError("punishment comparator not complete")
                paired[f"theta={theta},initial_norm={seed},institution={institution}"]=dict(counts)
    dependence={}
    for theta in THRESHOLDS:
        for inst in INSTITUTIONS:
            varying=[group for group in groups if
                     source_cases[(group,theta,0.,inst)]["end_contributor_count"]!=
                     source_cases[(group,theta,1.,inst)]["end_contributor_count"]]
            dependence[f"theta={theta},institution={inst}"]={
                "distinct_compositions_with_different_final_outcome_by_seed":len(varying),
                "first_lexicographic_abstract_witness":list(varying[0]) if varying else None}
    return {
        "research_id":"R071",
        "stage":"E1_NORM_FEEDBACK_AND_COSTLY_PUNISHMENT",
        "status":"E1_SYNTHETIC_NORM_INSTITUTION_MECHANISMS_PASS",
        "protocol":"protocols/R071_NORM_COOPERATION_PUNISHMENT_E1_2026-10-16.md",
        "literature_DOI":[
            "10.1257/jep.14.3.137",
            "10.1257/aer.90.4.980",
            "10.1073/pnas.0630443100",
        ],
        "mechanism":"four fixed strategy roles C/D/P/N; N responds to previous visible cooperation or deterrence, not learned psychology",
        "group_size":N,"benefit_per_contribution":BENEFIT,"cost_per_contribution":CONTRIBUTION_COST,
        "institution_parameters":INSTITUTIONS,
        "conditional_thresholds":list(THRESHOLDS),"initial_norm_values":list(INITIAL_NORMS),
        "distinct_group_compositions":EXPECTED_COMPOSITIONS,
        "full_factorial_cases":total_cases,
        "all_verified_group_rounds":total_cases*STEPS,
        "rounds_per_case":STEPS,
        "aggregate":aggregated,
        "pairwise_against_no_institution":paired,
        "initial_norm_path_dependence":dependence,
        "synthetic_witnesses":fixed_synthetic_witnesses(),
        "causal_human_institutional_mechanisms":"NOT_ESTABLISHED",
        "human_E2":"OPEN_REQUIRE_EXACT_PUBLIC_GOODS_INSTITUTION_AND_BEHAVIOR_SOURCE",
        "R047_CPR_extraction_direct_model_match":False,
        "E3_independent_new_cohort":"OPEN",
        "pesen_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    results=evaluate()
    args.output.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":results["status"],
        "compositions":results["distinct_group_compositions"],
        "cases":results["full_factorial_cases"],
        "group_rounds":results["all_verified_group_rounds"],
        "path_dependence":results["initial_norm_path_dependence"],
        "paired_enforcement_gain":results["pairwise_against_no_institution"],
    },sort_keys=True))


if __name__=="__main__":
    main()
