#!/usr/bin/env python3
"""R070 E1: exhaustively compare first-unhappy versus first-FEASIBLE actor.

Four frozen mobility policies, five tolerance values, all 756 3x3 states.
Only activation priority changes. No real demographic or participant data.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path

from r070_schelling_spatial_migration import validate, metrics, happy
from r070_exhaustive_3x3 import all_boards, board_digest, TOLERANCES, N_BOARDS, MOVE_BUDGET
from r070_distance_competitors import (
    POLICIES, candidate_destinations, unsatisfied, run_policy
)

ACTIVATIONS=("FIRST_UNHAPPY","FIRST_FEASIBLE_UNHAPPY")
EXPECTED_RUNS=2*len(POLICIES)*len(TOLERANCES)*N_BOARDS
TERMINATIONS_NEW=("STABLE_ALL_SATISFIED",
                  "STALLED_ALL_UNHAPPY_IMMOBILE","MAX_STEP_BUDGET")
TERMINATIONS_OLD=("STABLE_ALL_SATISFIED",
                  "STALLED_NO_SATISFYING_VACANCY","MAX_STEP_BUDGET")


def feasible_step(board,tau,policy):
    """Skip immobile unhappy actors; preserve frozen destination ranking."""
    b=validate(board,tau)
    if policy not in POLICIES:
        raise ValueError("mobility policy not frozen")
    missing=unsatisfied(b,tau)
    if not missing:
        return b,{"status":"STABLE_ALL_SATISFIED","moved":False,
                  "skipped_immobile_unhappy":0}
    for rank,src in enumerate(missing):
        options=candidate_destinations(b,src,tau,policy)
        if not options:
            continue
        dst_r,dst_c,d,score=options[0]
        if (dst_r,dst_c)==src:
            raise ValueError("same-source destination prohibited")
        rows=[list(row) for row in b]
        typ=rows[src[0]][src[1]]
        rows[src[0]][src[1]]=0
        if rows[dst_r][dst_c]!=0:
            raise ValueError("destination must be vacant in original board")
        rows[dst_r][dst_c]=typ
        nxt=tuple(tuple(row) for row in rows)
        if not happy(nxt,dst_r,dst_c,tau):
            raise ValueError("selected relocated person remains unhappy")
        base=metrics(b,tau)
        after=metrics(nxt,tau)
        if any(base[k]!=after[k] for k in ("type_A_agents","type_B_agents","empty_cells")):
            raise ValueError("population/vacancy conservation violated")
        if sum(b[rr][cc]!=nxt[rr][cc]
               for rr in range(len(b)) for cc in range(len(b[0])))!=2:
            raise ValueError("one agent must move exactly once")
        return nxt,{"status":"MOVED","moved":True,
                    "from":[src[0],src[1]],"to":[dst_r,dst_c],
                    "abstract_type":typ,
                    "Manhattan_move_length":d,
                    "destination_same_neighbor_fraction":score,
                    "skipped_immobile_unhappy":rank}
    return b,{"status":"STALLED_ALL_UNHAPPY_IMMOBILE","moved":False,
              "skipped_immobile_unhappy":len(missing),
              "unsatisfied_agent_count":len(missing)}


def run_feasible(board,tau,policy,steps=MOVE_BUDGET):
    if policy not in POLICIES:
        raise ValueError("invalid frozen mobility policy")
    if type(steps) is not int or not 0<=steps<=100:
        raise ValueError("invalid step budget")
    state=validate(board,tau)
    history=[{"tick":0,"board":state,"metrics":metrics(state,tau)}]
    initial_counts=history[0]["metrics"]
    events=[]
    skipped_total=0
    repeats=0
    seen={state}
    termination="MAX_STEP_BUDGET"
    for tick in range(1,steps+1):
        nxt,evt=feasible_step(state,tau,policy)
        if not evt["moved"]:
            termination=evt["status"]
            break
        skipped_total+=evt["skipped_immobile_unhappy"]
        if nxt in seen:
            repeats+=1
        seen.add(nxt)
        state=nxt
        events.append(evt)
        sample=metrics(state,tau)
        if any(sample[k]!=initial_counts[k] for k in ("type_A_agents","type_B_agents","empty_cells")):
            raise ValueError("agent conservation failed on intermediate tick")
        history.append({"tick":tick,"board":state,"metrics":sample})
    else:
        if history[-1]["metrics"]["unhappy_agents"]==0:
            termination="STABLE_ALL_SATISFIED"
    if termination=="STABLE_ALL_SATISFIED" and history[-1]["metrics"]["unhappy_agents"]!=0:
        raise ValueError("false fully satisfied termination")
    if termination=="STALLED_ALL_UNHAPPY_IMMOBILE":
        if not unsatisfied(state,tau):
            raise ValueError("empty unsatisfied list at stalled termination")
        if any(candidate_destinations(state,agent,tau,policy)
               for agent in unsatisfied(state,tau)):
            raise ValueError("global immobility label false")
    return {
        "policy":policy,"activation":"FIRST_FEASIBLE_UNHAPPY",
        "tau":tau,"initial_board":board,
        "budget":steps,"actual_moves":len(events),
        "termination":termination,
        "move_log":events,"snapshots":history,
        "total_earlier_immobile_unhappy_candidates_skipped":skipped_total,
        "used_skip_on_any_move":skipped_total>0,
        "repeat_state_visits_after_moves":repeats,
        "source_type_counts_preserved":True,
    }


def first_witness(details,kind,board,tau,old,new):
    details.setdefault(kind,{
        "initial_board":board,
        "tau":tau,
        "old_status":old["termination"],
        "new_status":new["termination"],
        "old_moves":old["actual_moves"],
        "new_moves":new["actual_moves"],
        "old_final_board":old["snapshots"][-1]["board"],
        "new_final_board":new["snapshots"][-1]["board"],
        "new_skipped_immobile_unhappy":new["total_earlier_immobile_unhappy_candidates_skipped"]
    })


def score_one(table,board,tau,old,new):
    x=table["counts"]
    x["cases"]+=1
    x["old_"+old["termination"]]+=1
    x["new_"+new["termination"]]+=1
    if not new["source_type_counts_preserved"]:
        raise ValueError("actor population changed")
    for trial in (old,new):
        if trial["actual_moves"]>MOVE_BUDGET:
            raise ValueError("budget breached")
        end=trial["snapshots"][-1]["metrics"]
        if (end["type_A_agents"],end["type_B_agents"],end["empty_cells"])!=(2,2,5):
            raise ValueError("unexpected A/B/empty counts")
    x["old_total_moves"]+=old["actual_moves"]
    x["new_total_moves"]+=new["actual_moves"]
    x["new_total_immobile_candidates_skipped"]+=new["total_earlier_immobile_unhappy_candidates_skipped"]
    x["new_revisited_states_across_moves"]+=new["repeat_state_visits_after_moves"]
    x["new_max_moves"]=max(x["new_max_moves"],new["actual_moves"])
    if new["used_skip_on_any_move"]:
        x["new_initial_boards_using_skip"]+=1
        first_witness(table["first"],"skip_immobile_first_actor",board,tau,old,new)
    ostatus=old["termination"];nstatus=new["termination"]
    if ostatus=="STALLED_NO_SATISFYING_VACANCY" and nstatus=="STABLE_ALL_SATISFIED":
        x["old_stall_new_stable"]+=1
        first_witness(table["first"],"old_stall_new_stable",board,tau,old,new)
    if ostatus=="STABLE_ALL_SATISFIED" and nstatus=="STALLED_ALL_UNHAPPY_IMMOBILE":
        x["old_stable_new_stall"]+=1
        first_witness(table["first"],"old_stable_new_stall",board,tau,old,new)
    if ostatus=="STABLE_ALL_SATISFIED" and nstatus=="MAX_STEP_BUDGET":
        x["old_stable_new_budget"]+=1
        first_witness(table["first"],"old_stable_new_budget",board,tau,old,new)
    if ostatus=="STALLED_NO_SATISFYING_VACANCY" and nstatus=="MAX_STEP_BUDGET":
        x["old_stall_new_budget"]+=1
        first_witness(table["first"],"old_stall_new_budget",board,tau,old,new)
    if old["snapshots"][-1]["board"]!=new["snapshots"][-1]["board"]:
        x["different_final_boards"]+=1
        first_witness(table["first"],"different_final_board",board,tau,old,new)
    if new["actual_moves"]>old["actual_moves"]:
        x["new_more_moves"]+=1
    elif new["actual_moves"]<old["actual_moves"]:
        x["new_fewer_moves"]+=1
    else:x["equal_moves"]+=1
    old_m=old["snapshots"][-1]["metrics"]
    new_m=new["snapshots"][-1]["metrics"]
    if new_m["unhappy_agents"]<old_m["unhappy_agents"]:
        x["new_less_unhappy"]+=1
        first_witness(table["first"],"new_less_unhappy",board,tau,old,new)
    elif new_m["unhappy_agents"]>old_m["unhappy_agents"]:
        x["new_more_unhappy"]+=1
        first_witness(table["first"],"new_more_unhappy",board,tau,old,new)
    else:x["equal_unhappy"]+=1
    a=old_m["cardinal_different_type_edge_share"]
    b=new_m["cardinal_different_type_edge_share"]
    if a is not None and b is not None:
        x["macro_contact_paired_defined"]+=1
        table["old_heterotypic_share_sum"]+=a
        table["new_heterotypic_share_sum"]+=b
        if b>a+1e-12:
            x["new_higher_heterotypic_share"]+=1
            first_witness(table["first"],"new_higher_heterotypic_contact",board,tau,old,new)
        elif b<a-1e-12:
            x["new_lower_heterotypic_share"]+=1
        else:
            x["equal_heterotypic_share"]+=1


def summarize(tbl):
    c=tbl["counts"]
    if c["cases"]!=N_BOARDS:
        raise ValueError("incomplete 756-board universe")
    if sum(c["old_"+k] for k in TERMINATIONS_OLD)!=N_BOARDS:
        raise ValueError("original status cohorts not exhaustive")
    if sum(c["new_"+k] for k in TERMINATIONS_NEW)!=N_BOARDS:
        raise ValueError("new status cohorts not exhaustive")
    for labels in (("new_more_moves","new_fewer_moves","equal_moves"),
                   ("new_less_unhappy","new_more_unhappy","equal_unhappy")):
        if sum(c[k] for k in labels)!=N_BOARDS:
            raise ValueError("paired denominators drifted")
    valid=c["macro_contact_paired_defined"]
    if sum(c[k] for k in ("new_higher_heterotypic_share",
                            "new_lower_heterotypic_share",
                            "equal_heterotypic_share"))!=valid:
        raise ValueError("null macro contact mishandled")
    return {
        "total_initial_boards":N_BOARDS,
        "original_first_unhappy":{
            "satisfied":c["old_STABLE_ALL_SATISFIED"],
            "first_actor_stalled":c["old_STALLED_NO_SATISFYING_VACANCY"],
            "budget_exhausted":c["old_MAX_STEP_BUDGET"],
            "total_moves":c["old_total_moves"],
        },
        "new_first_feasible_unhappy":{
            "satisfied":c["new_STABLE_ALL_SATISFIED"],
            "all_unhappy_agents_immobile":c["new_STALLED_ALL_UNHAPPY_IMMOBILE"],
            "budget_exhausted":c["new_MAX_STEP_BUDGET"],
            "total_moves":c["new_total_moves"],
            "mean_moves":c["new_total_moves"]/N_BOARDS,
            "max_moves":c["new_max_moves"],
            "initial_boards_actually_using_skip":c["new_initial_boards_using_skip"],
            "total_earlier_immobile_candidates_skipped_in_actual_moves":c["new_total_immobile_candidates_skipped"],
            "revisited_board_states_across_moves":c["new_revisited_states_across_moves"],
        },
        "paired_comparison":{
            "old_stalled_new_satisfied":c["old_stall_new_stable"],
            "old_satisfied_new_stalled":c["old_stable_new_stall"],
            "old_satisfied_new_budget":c["old_stable_new_budget"],
            "old_stalled_new_budget":c["old_stall_new_budget"],
            "different_terminal_boards":c["different_final_boards"],
            "new_more_moves":c["new_more_moves"],
            "new_fewer_moves":c["new_fewer_moves"],
            "equal_moves":c["equal_moves"],
            "new_less_unhappy":c["new_less_unhappy"],
            "new_more_unhappy":c["new_more_unhappy"],
            "equal_unhappy":c["equal_unhappy"],
            "macro_both_defined_cases":valid,
            "new_higher_heterotypic_contact_share":c["new_higher_heterotypic_share"],
            "new_lower_heterotypic_contact_share":c["new_lower_heterotypic_share"],
            "equal_heterotypic_contact_share":c["equal_heterotypic_share"],
            "old_mean_macro_contact_in_paired_defined":
                tbl["old_heterotypic_share_sum"]/valid if valid else None,
            "new_mean_macro_contact_in_paired_defined":
                tbl["new_heterotypic_share_sum"]/valid if valid else None,
        },
        "first_lexicographic_synthetic_witnesses":tbl["first"],
    }


def evaluate():
    boards=list(all_boards())
    if len(boards)!=N_BOARDS or len({board_digest(x) for x in boards})!=N_BOARDS:
        raise ValueError("original 756-board universe mutated")
    output={}
    run_count=0
    for tau in TOLERANCES:
        grouped={}
        for policy in POLICIES:
            tbl={"counts":Counter(),"first":{},
                 "old_heterotypic_share_sum":0.,
                 "new_heterotypic_share_sum":0.}
            for board in boards:
                old=run_policy(board,tau,policy,MOVE_BUDGET)
                new=run_feasible(board,tau,policy,MOVE_BUDGET)
                score_one(tbl,board,tau,old,new)
                run_count+=2
            q=summarize(tbl)
            expected={
                .0:[756,756,756,756],
                .25:[756,496,720,756],
                .5:[642,294,528,646],
                .75:[210,90,170,210],
                1.:[210,90,170,210]
            }
            if q["original_first_unhappy"]["satisfied"]!=expected[tau][POLICIES.index(policy)]:
                raise ValueError("frozen prior mobility competition baseline drifted")
            if tau==0. and (q["new_first_feasible_unhappy"]["satisfied"]!=N_BOARDS
                           or q["new_first_feasible_unhappy"]["total_moves"]!=0):
                raise ValueError("tau zero guaranteed no-action property failed")
            grouped[policy]=q
        output[str(tau)]=grouped
    if run_count!=EXPECTED_RUNS:
        raise ValueError("complete activation-by-policy experiments not executed")
    return {
        "research_id":"R070",
        "stage":"E1_FIRST_FEASIBLE_ACTOR_ACTIVATION_PAIRED_ENUMERATION",
        "status":"E1_AGENT_ACTIVATION_COMPETITION_PASS",
        "protocol":"protocols/R070_E1_FEASIBLE_ACTOR_ACTIVATION_2026-10-16.md",
        "fixed_chessboard":"3x3 with 2 of abstract A, 2 of B and 5 vacancies",
        "initial_layouts":N_BOARDS,
        "threshold_values":list(TOLERANCES),
        "frozen_mobility_policies":list(POLICIES),
        "compared_activation_rules":list(ACTIVATIONS),
        "executed_trajectories":run_count,
        "maximum_moves":MOVE_BUDGET,
        "experimental_results":output,
        "historical_baseline_reused_unchanged":True,
        "hypothesis_causal_real_world":"NOT_TESTED",
        "human_event_level_E2":"BLOCKED_EVENT_LEVEL_SOURCE_AND_RULE_PARITY",
        "external_E3":"OPEN",
        "pesen_v01":"FROZEN",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    z=evaluate()
    args.output.write_text(json.dumps(z,indent=2)+"\n",encoding="utf-8")
    brief={tau:{policy:{
        "old_satisfied":case["original_first_unhappy"]["satisfied"],
        "new_satisfied":case["new_first_feasible_unhappy"]["satisfied"],
        "new_fully_immobile":case["new_first_feasible_unhappy"]["all_unhappy_agents_immobile"],
        "new_budget":case["new_first_feasible_unhappy"]["budget_exhausted"],
        "old_stall_rescued":case["paired_comparison"]["old_stalled_new_satisfied"],
        "new_worse_terminal_unhappy":case["paired_comparison"]["new_more_unhappy"],
    } for policy,case in groups.items()} for tau,groups in z["experimental_results"].items()}
    print(json.dumps({"status":z["status"],
                      "runs":z["executed_trajectories"],
                      "summary":brief},sort_keys=True))


if __name__=="__main__":
    main()
