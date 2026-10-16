#!/usr/bin/env python3
"""R072 E1 binary public reputation and indirect-donation signal mechanisms.

Fixed 4 synthetic agents, 3 reputation assessment rules, 3 signal regimes.
Not a reproduction of Ohtsuki-Iwasa evolutionary ESS and not real people.
"""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import product,combinations
import json
from pathlib import Path

ROLES=("ALLC","ALLD","DISC")
NORMS=("IMAGE_SCORING","SIMPLE_STANDING","STERN_JUDGING")
CHANNELS=("VERIFIED","FLIP_EVERY_FOURTH","NO_OBSERVATION")
N=4
COST=1
BENEFIT=2
SCHEDULE=tuple((actor,receiver) for actor in range(N)
               for receiver in range(N) if receiver!=actor)*2
EXPECTED_STRATEGIES=3**N
EXPECTED_SEEDS=2**N
EXPECTED_CASES=EXPECTED_STRATEGIES*EXPECTED_SEEDS*len(NORMS)*len(CHANNELS)
EXPECTED_DECISIONS=EXPECTED_CASES*len(SCHEDULE)


def validate(roles,initial_reputations,norm,channel):
    if (not isinstance(roles,(list,tuple)) or len(roles)!=N or
        any(x not in ROLES or not isinstance(x,str) for x in roles)):
        raise ValueError("EXACT_FOUR_ABSTRACT_ROLES_REQUIRED")
    if (not isinstance(initial_reputations,(list,tuple)) or
        len(initial_reputations)!=N or
        any(type(x) is not int or x not in (0,1) for x in initial_reputations)):
        raise ValueError("EXACT_FOUR_BINARY_PRIOR_REPUTATIONS_REQUIRED")
    if norm not in NORMS:
        raise ValueError("UNKNOWN_REPUTATION_NORM")
    if channel not in CHANNELS:
        raise ValueError("UNKNOWN_SIGNAL_REGIME")
    return tuple(roles),tuple(initial_reputations)


def assess(reported_help,recipient_good,norm):
    if type(reported_help) is not bool or type(recipient_good) is not bool:
        raise ValueError("ASSESS_TWO_BOOLEAN_MEASUREMENTS_REQUIRED")
    if norm=="IMAGE_SCORING":
        return int(reported_help)
    if norm=="SIMPLE_STANDING":
        return int(reported_help or not recipient_good)
    if norm=="STERN_JUDGING":
        return int(reported_help==recipient_good)
    raise ValueError("UNKNOWN_REPUTATION_NORM")


def true_action(role,recipient_good):
    if type(recipient_good) is not bool:
        raise ValueError("RECIPIENT_REPUTATION_BEFORE_ACTION_REQUIRED")
    if role=="ALLC":return True
    if role=="ALLD":return False
    if role=="DISC":return recipient_good
    raise ValueError("UNKNOWN_DONOR_STRATEGY")


def reported_action(real_help,index_1_based,channel):
    if type(real_help) is not bool or type(index_1_based) is not int or index_1_based<1:
        raise ValueError("INVALID_REAL_ACTION_OR_TIME")
    if channel=="VERIFIED":return real_help
    if channel=="FLIP_EVERY_FOURTH":
        return (not real_help) if index_1_based%4==0 else real_help
    if channel=="NO_OBSERVATION":return None
    raise ValueError("UNKNOWN_SIGNAL_REGIME")


def run(roles,initial_reputations,norm,channel,include_trace=False):
    roles,initial_reputations=validate(roles,initial_reputations,norm,channel)
    reputations=list(initial_reputations)
    balances=[0]*N
    real_help_count=0
    halves=[0,0]
    false_reports=0
    transitions=0
    trace=[] if include_trace else None
    for time,(donor,receiver) in enumerate(SCHEDULE,1):
        previous_recipient=bool(reputations[receiver])
        donor_before=reputations[donor]
        help_actual=true_action(roles[donor],previous_recipient)
        if help_actual:
            balances[donor]-=COST
            balances[receiver]+=BENEFIT
            real_help_count+=1
            halves[0 if time<=12 else 1]+=1
        announcement=reported_action(help_actual,time,channel)
        if announcement is not None:
            if announcement!=help_actual:false_reports+=1
            reputations[donor]=assess(announcement,previous_recipient,norm)
            if reputations[donor]!=donor_before:transitions+=1
        if include_trace:
            trace.append({
                "event":time,"donor":donor,"recipient":receiver,
                "recipient_good_at_choice":int(previous_recipient),
                "actual_help":help_actual,
                "reported_help":announcement,
                "donor_reputation_before":donor_before,
                "donor_reputation_after":reputations[donor],
                "balance_after":list(balances),
            })
        if sum(balances)!=(BENEFIT-COST)*real_help_count:
            raise ValueError("TRUE_TRANSACTION_PAYOFF_ACCOUNTING_FAILED")
        if any(v not in (0,1) for v in reputations):
            raise ValueError("REPUTATION_NOT_BINARY")
    if (channel=="NO_OBSERVATION" and
        (tuple(reputations)!=initial_reputations or transitions or false_reports)):
        raise ValueError("UNOBSERVED_REPUTATIONS_MUST_BE_FROZEN")
    if false_reports!=(6 if channel=="FLIP_EVERY_FOURTH" else 0):
        raise ValueError("PRE_REGISTERED_SIGNAL_ERROR_SCHEDULE_CHANGED")
    result={
        "roles":list(roles),
        "initial_public_reputations":list(initial_reputations),
        "norm":norm,"channel":channel,
        "true_help_count":real_help_count,
        "first_12_true_helps":halves[0],"last_12_true_helps":halves[1],
        "group_payoff_sum":sum(balances),
        "per_agent_payoffs":balances,
        "final_reputation_good_count":sum(reputations),
        "final_public_reputations":reputations,
        "false_reports":false_reports,
        "public_reputation_changes":transitions,
    }
    if include_trace:result["synthetic_trace"]=trace
    return result


def create_bucket():
    return {"cases":0,"transactions":0,"true_help_total":0,
            "first_12_helps_total":0,"last_12_helps_total":0,
            "final_good_reputation_slots_total":0,
            "true_group_net_payoff_total":0,"reputation_changed_count":0}


def record(bucket,result):
    bucket["cases"]+=1
    bucket["transactions"]+=len(SCHEDULE)
    for key,field in (
        ("true_help_total","true_help_count"),
        ("first_12_helps_total","first_12_true_helps"),
        ("last_12_helps_total","last_12_true_helps"),
        ("final_good_reputation_slots_total","final_reputation_good_count"),
        ("true_group_net_payoff_total","group_payoff_sum"),
        ("reputation_changed_count","public_reputation_changes"),
    ):bucket[key]+=result[field]


def summarise_bucket(b,required_cases):
    if b["cases"]!=required_cases or b["transactions"]!=required_cases*24:
        raise ValueError("LOSS_OF_COMPLETE_E1_POPULATION")
    if b["true_group_net_payoff_total"]!=(BENEFIT-COST)*b["true_help_total"]:
        raise ValueError("GROUP_PAYOFF_SUM_DRIFT")
    return {
        **b,
        "true_help_rate_all_scheduled_24_transactions":
            b["true_help_total"]/b["transactions"],
        "true_help_rate_first_12":b["first_12_helps_total"]/(12*required_cases),
        "true_help_rate_last_12":b["last_12_helps_total"]/(12*required_cases),
        "change_help_rate_last_minus_first":
            (b["last_12_helps_total"]-b["first_12_helps_total"])/(12*required_cases),
        "final_good_reputation_slot_fraction":
            b["final_good_reputation_slots_total"]/(4*required_cases),
    }


def witness(roles,seed,x,y,comparison):
    return {
        "abstract_roles":list(roles),
        "initial_public_reputations":list(seed),
        "comparison":comparison,
        "first_result":{k:x[k] for k in ("norm","channel","true_help_count",
                                          "final_public_reputations")},
        "second_result":{k:y[k] for k in ("norm","channel","true_help_count",
                                           "final_public_reputations")},
    }


def evaluate():
    schedules=list(SCHEDULE)
    if len(schedules)!=24 or schedules[:12]!=schedules[12:]:
        raise ValueError("FIXED_ORDERED_PAIR_SCHEDULE_CHANGED")
    if len(set(schedules[:12]))!=12 or any(a==b for a,b in schedules):
        raise ValueError("SELF_DONATIONS_OR_MISSING_PAIRS")
    roles_all=list(product(ROLES,repeat=N))
    seeds_all=list(product((0,1),repeat=N))
    if len(roles_all)!=EXPECTED_STRATEGIES or len(seeds_all)!=EXPECTED_SEEDS:
        raise ValueError("FINITE_ASSIGNMENT_UNIVERSE_DRIFT")
    if len(set(roles_all))!=81 or len(set(seeds_all))!=16:
        raise ValueError("DUPLICATE_STATE_IN_UNIVERSE")
    totals={(norm,channel):create_bucket() for norm in NORMS for channel in CHANNELS}
    by_discriminators={(norm,channel,k):create_bucket()
              for norm in NORMS for channel in CHANNELS for k in range(5)}
    channel_differences={(norm,channel):{"different_true_help_cases":0,
                                        "equal_true_help_cases":0,
                                        "first_lexicographic_witness":None}
          for norm in NORMS for channel in CHANNELS if channel!="VERIFIED"}
    norms_differences={(channel,a,b):{"different_true_help_cases":0,
                                    "equal_true_help_cases":0,
                                    "first_lexicographic_witness":None}
          for channel in CHANNELS for a,b in combinations(NORMS,2)}
    cases=0
    without_DISC_cases=0
    for roles in roles_all:
        k=sum(role=="DISC" for role in roles)
        for seed in seeds_all:
            table={}
            for norm in NORMS:
                for channel in CHANNELS:
                    result=run(roles,seed,norm,channel)
                    table[(norm,channel)]=result
                    record(totals[(norm,channel)],result)
                    record(by_discriminators[(norm,channel,k)],result)
                    cases+=1
            if k==0:
                without_DISC_cases+=1
                if len({(z["true_help_count"],z["first_12_true_helps"],
                          z["last_12_true_helps"]) for z in table.values()})!=1:
                    raise ValueError("ROLE_ONLY_ACTION_MUST_NOT_DEPEND_ON_REPUTATION")
            for norm in NORMS:
                a=table[(norm,"VERIFIED")]
                for channel in CHANNELS:
                    if channel=="VERIFIED":continue
                    key=(norm,channel);b=table[key];ctr=channel_differences[key]
                    if a["true_help_count"]!=b["true_help_count"]:
                        ctr["different_true_help_cases"]+=1
                        if ctr["first_lexicographic_witness"] is None:
                            ctr["first_lexicographic_witness"]=witness(roles,seed,a,b,"channel")
                    else:ctr["equal_true_help_cases"]+=1
            for channel in CHANNELS:
                for a,b in combinations(NORMS,2):
                    v1,v2=table[(a,channel)],table[(b,channel)]
                    ctr=norms_differences[(channel,a,b)]
                    if v1["true_help_count"]!=v2["true_help_count"]:
                        ctr["different_true_help_cases"]+=1
                        if ctr["first_lexicographic_witness"] is None:
                            ctr["first_lexicographic_witness"]=witness(roles,seed,v1,v2,"norm")
                    else:ctr["equal_true_help_cases"]+=1
    if cases!=EXPECTED_CASES:
        raise ValueError("11664_EXHAUSTIVE_CASE_UNIVERSE_FAILED")
    group_result={}
    hist={}
    for norm in NORMS:
        group_result[norm]={}
        hist[norm]={}
        for channel in CHANNELS:
            group_result[norm][channel]=summarise_bucket(totals[(norm,channel)],1296)
            hist[norm][channel]={}
            for k in range(5):
                # C(4,k)*2^(4-k) role vectors, 16 reputation seeds:
                number={0:16,1:32,2:24,3:8,4:1}[k]*16
                hist[norm][channel][str(k)]=summarise_bucket(
                    by_discriminators[(norm,channel,k)],number)
    for ctr in list(channel_differences.values())+list(norms_differences.values()):
        if ctr["different_true_help_cases"]+ctr["equal_true_help_cases"]!=1296:
            raise ValueError("PAIRED_COMPARISON_DENOMINATOR_CHANGED")
    return {
        "research_id":"R072",
        "stage":"E1_REPUTATION_ASSESSMENT_AND_PUBLIC_SIGNAL",
        "status":"E1_PUBLIC_REPUTATION_FULL_ENUMERATION_PASS",
        "protocol":"protocols/R072_REPUTATION_PUBLIC_SIGNAL_DONATION_E1_2026-10-16.md",
        "source_papers_DOI":["10.1038/31225","10.1016/j.jtbi.2004.06.005",
                             "10.2307/2297925"],
        "fixed_strategy_population":N,
        "fixed_roles":list(ROLES),
        "public_assessment_norms":list(NORMS),
        "signal_channels":list(CHANNELS),
        "ordered_pairs_each_12_repeated_twice":True,
        "schedule_size":24,
        "strategy_vectors":81,"initial_reputation_vectors":16,
        "complete_model_cases":cases,
        "actual_decision_events":cases*24,
        "cases_with_no_reputation_sensitive_DISC_role_across_role_and_seeds":
           without_DISC_cases,
        "payoff_per_actual_help":{"donor":-COST,"recipient":BENEFIT},
        "norm_channel_results":group_result,
        "cooperation_by_DISC_role_count":hist,
        "paired_channel_counterfactuals":{
            f"{n}|{c}":v for (n,c),v in channel_differences.items()},
        "paired_norm_counterfactuals":{
            f"{c}|{a}|{b}":v for (c,a,b),v in norms_differences.items()},
        "synthetic_only":True,
        "real_human_trust_signal_E2":"NOT_ESTABLISHED",
        "model_evolutionary_ESS":"NOT_CALCULATED",
        "external_E3":"OPEN",
        "pesen_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    result=evaluate()
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    summary={
        norm:{channel:{"help_rate":z["true_help_rate_all_scheduled_24_transactions"],
                       "final_good_fraction":z["final_good_reputation_slot_fraction"],
                       "last_minus_first":z["change_help_rate_last_minus_first"]}
              for channel,z in group.items()}
        for norm,group in result["norm_channel_results"].items()
    }
    print(json.dumps({"status":result["status"],
                      "cases":result["complete_model_cases"],
                      "events":result["actual_decision_events"],
                      "summary":summary},sort_keys=True))


if __name__=="__main__":
    main()
