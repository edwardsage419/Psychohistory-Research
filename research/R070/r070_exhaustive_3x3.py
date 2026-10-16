#!/usr/bin/env python3
"""R070 exhaustive 3x3 grid with two abstract A, two B, five vacancies.

All C(9,2)*C(7,2) = 756 states, five fixed tau: 3780 independent E1
deterministic trajectories. Calls frozen R070 source run, not a surrogate.
"""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import combinations
import json
import math
from pathlib import Path
from r070_schelling_spatial_migration import run,metrics,validate

TOLERANCES=(0.,.25,.5,.75,1.)
N_BOARDS=756
MOVE_BUDGET=40
TERMINATIONS=("STABLE_ALL_SATISFIED","STALLED_NO_SATISFYING_VACANCY",
              "MAX_STEP_BUDGET")


def all_boards():
    indexes=tuple(range(9))
    for first in combinations(indexes,2):
        leftover=tuple(i for i in indexes if i not in first)
        for second in combinations(leftover,2):
            flat=[0]*9
            for i in first: flat[i]=1
            for i in second:flat[i]=2
            board=tuple(tuple(flat[k*3:k*3+3]) for k in range(3))
            yield board


def board_digest(board):
    return "".join(str(x) for row in board for x in row)


def summarize_tolerance(tau,boards):
    if tau not in TOLERANCES:
        raise ValueError("threshold must be in predeclared exhaustive family")
    totals=Counter()
    seen=set()
    start_defined=[]
    end_defined=[]
    first={}
    for board in boards:
        state=validate(board,tau)
        digest=board_digest(state)
        if digest in seen:raise ValueError("duplicate state in exhaustive enumeration")
        seen.add(digest)
        initial=metrics(state,tau)
        if (initial["type_A_agents"],initial["type_B_agents"],
            initial["empty_cells"])!=(2,2,5):
            raise ValueError("incorrect finite state universe")
        result=run(state,tau,MOVE_BUDGET)
        if not result["source_type_counts_preserved"]:
            raise ValueError("agent/vacancy conservation violated")
        if result["termination"] not in TERMINATIONS:
            raise ValueError("unexpected termination, not an accepted scientific status")
        snap=result["snapshots"]
        if len(snap)!=result["actual_moves"]+1:
            raise ValueError("single move trace count drift")
        for sample in snap:
            typ=sample["metrics"]
            if (typ["type_A_agents"],typ["type_B_agents"],
                typ["empty_cells"])!=(2,2,5):
                raise ValueError("agent/vacancy conservation fails per intermediate tick")
        terminal=snap[-1]["metrics"]
        if (result["termination"]=="STABLE_ALL_SATISFIED" and
            terminal["unhappy_agents"]!=0):
            raise ValueError("false fully satisfied scientific status")
        if (result["termination"]=="STALLED_NO_SATISFYING_VACANCY" and
            terminal["unhappy_agents"]==0):
            raise ValueError("stalled incorrectly labelled as unsatisfied")
        if result["actual_moves"]>MOVE_BUDGET:
            raise ValueError("budget exceeded")
        totals["states"]+=1
        totals["terminal_"+result["termination"]]+=1
        totals["total_moves"]+=result["actual_moves"]
        totals["max_moves"]=max(totals["max_moves"],result["actual_moves"])
        totals["initial_unhappy_agents_sum"]+=initial["unhappy_agents"]
        totals["terminal_unhappy_agents_sum"]+=terminal["unhappy_agents"]
        if initial["unhappy_agents"]>0:totals["initially_nonzero_unhappy_boards"]+=1
        if terminal["unhappy_agents"]>0:totals["terminal_nonzero_unhappy_boards"]+=1
        if terminal["unhappy_agents"]>initial["unhappy_agents"]:
            totals["final_more_unhappy_than_initial_boards"]+=1
            if "more_unhappy" not in first:
                first["more_unhappy"]={"board":state,
                    "initial_unhappy":initial["unhappy_agents"],
                    "final_unhappy":terminal["unhappy_agents"],
                    "moves":result["actual_moves"]}
        a=initial["cardinal_different_type_edge_share"]
        b=terminal["cardinal_different_type_edge_share"]
        if a is not None:start_defined.append(a)
        if b is not None:end_defined.append(b)
        if a is not None and b is not None:
            totals["paired_cardinal_contact_share_defined"]+=1
            if b>a+1e-12:
                totals["final_heterotypic_share_increased_boards"]+=1
                if "final_higher_heterotypic_contact" not in first:
                    first["final_higher_heterotypic_contact"]={
                        "board":state,"initial_share":a,"final_share":b,
                        "moves":result["actual_moves"]}
            if b<a-1e-12:
                totals["final_heterotypic_share_decreased_boards"]+=1
        for prev,nxt in zip(snap[:-1],snap[1:]):
            x=prev["metrics"]["cardinal_different_type_edge_share"]
            y=nxt["metrics"]["cardinal_different_type_edge_share"]
            if x is not None and y is not None:
                totals["scorable_move_cardinal_share_pairs"]+=1
                if y>x+1e-12:
                    totals["moves_with_increase_heterotypic_cardinal_share"]+=1
                    if "single_move_higher_heterotypic_contact" not in first:
                        first["single_move_higher_heterotypic_contact"]={
                            "board":state,"before":x,"after":y,
                            "move_index":nxt["tick"]}
        f0=initial["mean_local_same_type_fraction_if_neighbors"]
        f1=terminal["mean_local_same_type_fraction_if_neighbors"]
        if f0 is not None and f1 is not None:
            totals["paired_mean_local_same_defined"]+=1
            if f1+1e-12<f0:
                totals["final_mean_local_same_decreased_boards"]+=1
                if "final_lower_mean_same" not in first:
                    first["final_lower_mean_same"]={"board":state,
                        "initial":f0,"final":f1,
                        "moves":result["actual_moves"]}
        if result["termination"]=="STALLED_NO_SATISFYING_VACANCY":
            if "stalled" not in first:
                first["stalled"]={"board":state,"moves":result["actual_moves"],
                                  "unhappy_remaining":terminal["unhappy_agents"]}
        if result["termination"]=="MAX_STEP_BUDGET":
            if "max_budget" not in first:
                first["max_budget"]={"board":state,"moves":result["actual_moves"],
                                     "unhappy_remaining":terminal["unhappy_agents"]}
    if len(seen)!=N_BOARDS:
        raise ValueError("exhaustive 756-board universe incomplete")
    if tau==0. and (totals["total_moves"]!=0 or
                     totals["terminal_STABLE_ALL_SATISFIED"]!=N_BOARDS):
        raise ValueError("tau=0 absorbing property contradicted")
    return {
        "tau":tau,"distinct_initial_boards":totals["states"],
        "terminal_status_counts":{k:totals["terminal_"+k] for k in TERMINATIONS},
        "total_moves":totals["total_moves"],
        "mean_moves":totals["total_moves"]/N_BOARDS,
        "max_moves":totals["max_moves"],
        "initially_unhappy_board_count":totals["initially_nonzero_unhappy_boards"],
        "terminal_with_unhappy_board_count":totals["terminal_nonzero_unhappy_boards"],
        "initial_total_unhappy_agents":totals["initial_unhappy_agents_sum"],
        "final_total_unhappy_agents":totals["terminal_unhappy_agents_sum"],
        "final_more_unhappy_than_initial_board_count":totals["final_more_unhappy_than_initial_boards"],
        "initial_cardinal_share_defined_boards":len(start_defined),
        "final_cardinal_share_defined_boards":len(end_defined),
        "mean_initial_cardinal_heterotypic_share_where_defined":
           sum(start_defined)/len(start_defined) if start_defined else None,
        "mean_final_cardinal_heterotypic_share_where_defined":
           sum(end_defined)/len(end_defined) if end_defined else None,
        "paired_cardinal_share_defined_boards":totals["paired_cardinal_contact_share_defined"],
        "final_higher_heterotypic_contact_share_boards":
           totals["final_heterotypic_share_increased_boards"],
        "final_lower_heterotypic_contact_share_boards":
           totals["final_heterotypic_share_decreased_boards"],
        "scorable_single_move_cardinal_share_pairs":totals["scorable_move_cardinal_share_pairs"],
        "single_moves_raising_heterotypic_cardinal_share":
           totals["moves_with_increase_heterotypic_cardinal_share"],
        "paired_local_same_fraction_defined_boards":totals["paired_mean_local_same_defined"],
        "final_lower_local_same_fraction_boards":totals["final_mean_local_same_decreased_boards"],
        "first_lexicographic_synthetic_counterexamples":first,
    }


def evaluate():
    population=list(all_boards())
    if len(population)!=N_BOARDS or len({board_digest(x) for x in population})!=N_BOARDS:
        raise ValueError("combinatorial state enumerator not bijective")
    outcomes={str(tau):summarize_tolerance(tau,population) for tau in TOLERANCES}
    if sum(x["distinct_initial_boards"] for x in outcomes.values())!=3780:
        raise ValueError("wrong complete test grid count")
    return {
        "research_id":"R070",
        "stage":"E1_COMPLETE_3X3_TWOTYPE_STATE_SPACE_ENUMERATION",
        "status":"E1_EXHAUSTIVE_SMALL_BOARD_PASS",
        "protocol":"protocols/R070_E1_EXHAUSTIVE_SMALL_BOARD_ROBUSTNESS_2026-10-16.md",
        "mechanism_implementation":"research/R070/r070_schelling_spatial_migration.py",
        "board":"3x3 exactly two agents of each abstract type plus 5 empty cells",
        "total_independent_initial_configs":756,
        "tolerance_values":list(TOLERANCES),
        "exhaustive_initial_condition_tolerance_cases":3780,
        "max_moves_per_case":MOVE_BUDGET,
        "status_semantics":"STALLED and MAX_BUDGET are NOT convergence to all satisfied",
        "outcomes":outcomes,
        "empirical_human_e2":"OPEN_NO_EVENT_LEVEL_PUBLIC_LAB_DATA_VERIFIED",
        "real_population_discrimination_or_residential_history":"NOT_ESTABLISHED",
        "paper_primary_human_comparator_DOI":"10.1140/epjds/s13688-016-0065-5",
        "independent_computational_comparator_DOI":"10.1038/s41598-023-38519-6",
        "pesen_v01":"FROZEN",
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    result=evaluate()
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],"cases":result["exhaustive_initial_condition_tolerance_cases"],
         "summary":{name:{"stable":x["terminal_status_counts"]["STABLE_ALL_SATISFIED"],
                          "stalled":x["terminal_status_counts"]["STALLED_NO_SATISFYING_VACANCY"],
                          "capped":x["terminal_status_counts"]["MAX_STEP_BUDGET"],
                          "mean_moves":x["mean_moves"],
                          "rise_contact_boards":x["final_higher_heterotypic_contact_share_boards"]}
             for name,x in result["outcomes"].items()}},sort_keys=True))


if __name__=="__main__":
    main()
