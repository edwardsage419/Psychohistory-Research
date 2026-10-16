#!/usr/bin/env python3
"""R070 E1: 15,120 paired tiny-board runs with explicit mobility restrictions.

Contrasts existing row-major arbitrary-distance satisfaction policy with
Manhattan radius<=1, radius<=2, and nearest-satisfying destination.
Strictly synthetic, no demographic data or inference on housing preferences.
"""
from __future__ import annotations
import argparse,json
from collections import Counter
from pathlib import Path

from r070_schelling_spatial_migration import (
    validate, metrics, happy, fraction, run as original_run,
)
from r070_exhaustive_3x3 import (
    all_boards, board_digest, TOLERANCES, N_BOARDS, MOVE_BUDGET, TERMINATIONS,
)

POLICIES=("GLOBAL_ROW_MAJOR","RADIUS_1","RADIUS_2","NEAREST_SATISFICING")
EXPECTED_TOTAL=N_BOARDS*len(TOLERANCES)*len(POLICIES)


def distance(src,dest):
    if (len(src)!=2 or len(dest)!=2
        or any(type(v) is not int for v in tuple(src)+tuple(dest))):
        raise ValueError("Manhattan distance requires two integer coordinates")
    return abs(src[0]-dest[0])+abs(src[1]-dest[1])


def candidate_destinations(board, source, tau, policy):
    if policy not in POLICIES:
        raise ValueError("mobility policy not frozen")
    b=validate(board,tau)
    r0,c0=source
    if (type(r0) is not int or type(c0) is not int or
        not 0<=r0<len(b) or not 0<=c0<len(b[0]) or
        not b[r0][c0]):
        raise ValueError("source must be occupied in bounds")
    kind=b[r0][c0]
    staged=[list(row) for row in b]
    staged[r0][c0]=0
    staged=tuple(tuple(row) for row in staged)
    possible=[]
    for r in range(len(b)):
        for c in range(len(b[0])):
            if staged[r][c]!=0:continue
            d=distance(source,(r,c))
            if d==0:continue
            if policy=="RADIUS_1" and d>1:continue
            if policy=="RADIUS_2" and d>2:continue
            score=fraction(staged,r,c,kind)
            if score is None or score<tau:continue
            possible.append((r,c,d,score))
    if policy=="NEAREST_SATISFICING":
        possible.sort(key=lambda z:(z[2],z[0],z[1]))
    return possible


def unsatisfied(board,tau):
    b=validate(board,tau)
    return [(r,c) for r in range(len(b)) for c in range(len(b[0]))
            if b[r][c]!=0 and not happy(b,r,c,tau)]


def step(board,tau,policy):
    b=validate(board,tau)
    if policy not in POLICIES:
        raise ValueError("mobility policy not frozen")
    unhappy=unsatisfied(b,tau)
    if not unhappy:
        return b,{"status":"STABLE_ALL_SATISFIED","moved":False}
    origin=unhappy[0]
    options=candidate_destinations(b,origin,tau,policy)
    if not options:
        return b,{"status":"STALLED_NO_SATISFYING_VACANCY",
                  "moved":False,
                  "unsatisfied_agent_count":len(unhappy)}
    rr,cc,d,score=options[0]
    staged=[list(row) for row in b]
    typ=staged[origin[0]][origin[1]]
    staged[origin[0]][origin[1]]=0
    staged[rr][cc]=typ
    nxt=tuple(tuple(row) for row in staged)
    if not happy(nxt,rr,cc,tau):
        raise ValueError("relocated agent unexpectedly unhappy")
    if any(metrics(nxt,tau)[k]!=metrics(b,tau)[k]
           for k in ("type_A_agents","type_B_agents","empty_cells")):
        raise ValueError("population/vacancy conservation violation")
    return nxt,{"status":"MOVED","moved":True,
                "from":[origin[0],origin[1]],"to":[rr,cc],
                "abstract_type":typ,
                "destination_same_neighbor_fraction":score,
                "Manhattan_move_length":d}


def stalled_first_while_other_may_move(board,tau,policy):
    unhappy=unsatisfied(board,tau)
    if not unhappy:return False
    if candidate_destinations(board,unhappy[0],tau,policy):
        return False
    return any(candidate_destinations(board,u,tau,policy) for u in unhappy[1:])


def run_policy(board,tau,policy,steps=MOVE_BUDGET):
    if policy not in POLICIES:raise ValueError("invalid frozen mobility policy")
    if type(steps) is not int or not 0<=steps<=100:
        raise ValueError("invalid move budget")
    state=validate(board,tau)
    snapshots=[{"tick":0,"board":state,"metrics":metrics(state,tau)}]
    moves=[]
    termination="MAX_STEP_BUDGET"
    for tick in range(1,steps+1):
        new,event=step(state,tau,policy)
        if not event["moved"]:
            termination=event["status"]
            break
        state=new
        moves.append(event)
        snapshots.append({"tick":tick,"board":state,"metrics":metrics(state,tau)})
    else:
        if metrics(state,tau)["unhappy_agents"]==0:
            termination="STABLE_ALL_SATISFIED"
    if len(moves)!=len(snapshots)-1:
        raise ValueError("one relocated actor per step violated")
    if termination=="STABLE_ALL_SATISFIED" and metrics(state,tau)["unhappy_agents"]!=0:
        raise ValueError("false all-satisfied claim")
    if termination=="STALLED_NO_SATISFYING_VACANCY" and metrics(state,tau)["unhappy_agents"]==0:
        raise ValueError("false stalled claim")
    return {"initial_board":board,"tau":tau,"budget":steps,
            "policy":policy,"actual_moves":len(moves),
            "termination":termination,
            "move_log":moves,"snapshots":snapshots,
            "stalled_first_unhappy_while_another_could_move":
                termination=="STALLED_NO_SATISFYING_VACANCY"
                and stalled_first_while_other_may_move(state,tau,policy),
            "source_type_counts_preserved":all(all(
                s["metrics"][k]==snapshots[0]["metrics"][k]
                for k in ("type_A_agents","type_B_agents","empty_cells"))
                for s in snapshots)}


def assert_original_exact_parity(board,tau,comp):
    ref=original_run(board,tau,MOVE_BUDGET)
    if ref["termination"]!=comp["termination"]:
        raise ValueError("unrestricted reference termination mismatched")
    if ref["actual_moves"]!=comp["actual_moves"]:
        raise ValueError("unrestricted reference move count mismatched")
    if len(ref["snapshots"])!=len(comp["snapshots"]):
        raise ValueError("unrestricted reference trajectory length mismatched")
    for a,b in zip(ref["snapshots"],comp["snapshots"]):
        if a!=b:
            raise ValueError("unrestricted reference spatial trace changed")
    for a,b in zip(ref["move_log"],comp["move_log"]):
        if (a["from"]!=b["from"] or a["to"]!=b["to"]
            or a["abstract_type"]!=b["abstract_type"]
            or a["destination_same_neighbor_fraction"]!=b["destination_same_neighbor_fraction"]):
            raise ValueError("unrestricted reference action changed")


def init_aggregate():
    return {"count":Counter(),
            "paired_macro_baseline":[],
            "paired_macro_competitor":[],
            "examples":{}}


def record(stats,board,reference,comp):
    counts=stats["count"]
    term=comp["termination"]
    counts["total_cases"]+=1
    counts[term]+=1
    counts["sum_moves"]+=comp["actual_moves"]
    counts["max_moves"]=max(counts["max_moves"],comp["actual_moves"])
    end=comp["snapshots"][-1]["metrics"]
    start=comp["snapshots"][0]["metrics"]
    counts["total_terminal_unhappy_agents"]+=end["unhappy_agents"]
    if comp["stalled_first_unhappy_while_another_could_move"]:
        counts["stalled_first_with_other_relocation_available"]+=1
        stats["examples"].setdefault("other_agent_could_relocate",
                                    {"initial_board":board,"tau":comp["tau"],
                                     "final_board":comp["snapshots"][-1]["board"]})
    if not comp["source_type_counts_preserved"]:
        raise ValueError("A/B/vacancy conservation violated")
    a=start["cardinal_different_type_edge_share"]
    b=end["cardinal_different_type_edge_share"]
    if a is not None and b is not None:
        counts["initial_and_terminal_cardinal_contact_share_defined"]+=1
        if b>a+1e-12:
            counts["terminal_heterotypic_cardinal_share_increased"]+=1
    ba=reference["snapshots"][-1]["metrics"]["cardinal_different_type_edge_share"]
    if b is not None and ba is not None:
        stats["paired_macro_baseline"].append(ba)
        stats["paired_macro_competitor"].append(b)
        if b>ba+1e-12:counts["more_heterotypic_contact_than_unrestricted"]+=1
        if b<ba-1e-12:counts["less_heterotypic_contact_than_unrestricted"]+=1
    if comp["snapshots"][-1]["board"]!=reference["snapshots"][-1]["board"]:
        counts["different_terminal_boards"]+=1
        stats["examples"].setdefault("different_terminal_board",{
            "initial_board":board,"tau":comp["tau"],
            "global_terminal":reference["snapshots"][-1]["board"],
            "competitor_terminal":comp["snapshots"][-1]["board"]})
    if comp["actual_moves"]<reference["actual_moves"]:
        counts["competitor_fewer_moves"]+=1
    elif comp["actual_moves"]>reference["actual_moves"]:
        counts["competitor_more_moves"]+=1
    else:
        counts["equal_moves"]+=1
    if end["unhappy_agents"]>reference["snapshots"][-1]["metrics"]["unhappy_agents"]:
        counts["competitor_more_unhappy"]+=1
    elif end["unhappy_agents"]<reference["snapshots"][-1]["metrics"]["unhappy_agents"]:
        counts["competitor_fewer_unhappy"]+=1
    else:counts["equal_unhappy"]+=1
    if (reference["termination"]=="STABLE_ALL_SATISFIED"
        and comp["termination"]=="STALLED_NO_SATISFYING_VACANCY"):
        counts["global_stable_but_competitor_stalled"]+=1
        stats["examples"].setdefault("global_stable_competitor_stalled",{
            "initial_board":board,"tau":comp["tau"],
            "global_moves":reference["actual_moves"],
            "competitor_moves":comp["actual_moves"]})
    if (reference["termination"]=="STALLED_NO_SATISFYING_VACANCY"
        and comp["termination"]=="STABLE_ALL_SATISFIED"):
        counts["global_stalled_but_competitor_stable"]+=1
        stats["examples"].setdefault("global_stalled_competitor_stable",{
            "initial_board":board,"tau":comp["tau"],
            "global_moves":reference["actual_moves"],
            "competitor_moves":comp["actual_moves"]})


def summarize(stat):
    count=stat["count"]
    if count["total_cases"]!=N_BOARDS:
        raise ValueError("exhaustive group is not 756 boards")
    if sum(count[t] for t in TERMINATIONS)!=N_BOARDS:
        raise ValueError("all 756 terminal statuses not accounted")
    if sum(count[x] for x in ("competitor_fewer_moves","competitor_more_moves","equal_moves"))!=N_BOARDS:
        raise ValueError("paired movement comparison lost boards")
    if sum(count[x] for x in ("competitor_more_unhappy","competitor_fewer_unhappy","equal_unhappy"))!=N_BOARDS:
        raise ValueError("paired unhappy comparison lost boards")
    n=len(stat["paired_macro_baseline"])
    if n!=len(stat["paired_macro_competitor"]):
        raise ValueError("paired macro statistic mismatch")
    return {
        "configs":N_BOARDS,
        "all_satisfied":count["STABLE_ALL_SATISFIED"],
        "stalled":count["STALLED_NO_SATISFYING_VACANCY"],
        "step_budget":count["MAX_STEP_BUDGET"],
        "total_moves":count["sum_moves"],
        "average_moves":count["sum_moves"]/N_BOARDS,
        "maximum_moves":count["max_moves"],
        "remaining_unhappy_agents_total":count["total_terminal_unhappy_agents"],
        "stalled_first_agent_while_another_can_move":count["stalled_first_with_other_relocation_available"],
        "terminal_contact_ratio_increased_vs_initial":
            count["terminal_heterotypic_cardinal_share_increased"],
        "initial_and_terminal_cardinal_contact_share_defined":
            count["initial_and_terminal_cardinal_contact_share_defined"],
        "paired_macro_baseline_and_competitor_valid":n,
        "paired_mean_terminal_heterotypic_contact_ratio_baseline":
            sum(stat["paired_macro_baseline"])/n if n else None,
        "paired_mean_terminal_heterotypic_contact_ratio_competitor":
            sum(stat["paired_macro_competitor"])/n if n else None,
        "competitor_more_heterotypic_contact_than_unrestricted":
            count["more_heterotypic_contact_than_unrestricted"],
        "competitor_less_heterotypic_contact_than_unrestricted":
            count["less_heterotypic_contact_than_unrestricted"],
        "different_terminal_boards":count["different_terminal_boards"],
        "global_stable_but_competitor_stalled":count["global_stable_but_competitor_stalled"],
        "global_stalled_but_competitor_stable":count["global_stalled_but_competitor_stable"],
        "competitor_fewer_moves":count["competitor_fewer_moves"],
        "competitor_more_moves":count["competitor_more_moves"],
        "equal_moves":count["equal_moves"],
        "competitor_more_unhappy":count["competitor_more_unhappy"],
        "competitor_fewer_unhappy":count["competitor_fewer_unhappy"],
        "equal_unhappy":count["equal_unhappy"],
        "first_lexicographic_synthetic_witnesses":stat["examples"]}


def evaluate():
    initial=list(all_boards())
    if len(initial)!=N_BOARDS or len({board_digest(b) for b in initial})!=N_BOARDS:
        raise ValueError("original enumerator universe drift")
    results={}
    run_count=0
    for tau in TOLERANCES:
        aggs={p:init_aggregate() for p in POLICIES}
        for board in initial:
            base=run_policy(board,tau,"GLOBAL_ROW_MAJOR")
            assert_original_exact_parity(board,tau,base)
            for policy in POLICIES:
                scenario=base if policy=="GLOBAL_ROW_MAJOR" else run_policy(board,tau,policy)
                record(aggs[policy],board,base,scenario)
                run_count+=1
        result={p:summarize(aggs[p]) for p in POLICIES}
        if tau==0 and any(q["all_satisfied"]!=N_BOARDS or q["total_moves"]!=0 for q in result.values()):
            raise ValueError("tau zero prior invariant contradicted")
        if result["GLOBAL_ROW_MAJOR"]["all_satisfied"]!={
            0.:756,.25:756,.5:642,.75:210,1.:210}[tau]:
            raise ValueError("previous E1 global original result changed")
        results[str(tau)]=result
    if run_count!=EXPECTED_TOTAL:
        raise ValueError("15,120 experimental conditions not run")
    return {
        "research_id":"R070",
        "stage":"E1_MOBILITY_DISTANCE_RESTRICTION_FULL_PAIRED_ENUMERATION",
        "status":"E1_MOBILITY_DISTANCE_COMPETITION_PASS",
        "protocol":"protocols/R070_E1_MOVEMENT_DISTANCE_COMPETITOR_2026-10-16.md",
        "original_model_reference":"research/R070/r070_schelling_spatial_migration.py",
        "original_unrestricted_every_trajectory_verified":True,
        "initial_board_state_universe":N_BOARDS,
        "tolerance_grid":list(TOLERANCES),
        "policies":list(POLICIES),
        "total_deterministic_agent_experiments":run_count,
        "movement_cost_metric":"Manhattan distance, no wrap",
        "policy_differentiation":"radius hard cap vs nearest viable rank; all require satisfying position",
        "maximum_moves_per_run":MOVE_BUDGET,
        "results":results,
        "individual_or_human_data_loaded":False,
        "E2_human_behavior_fit":"BLOCKED_NO_MATCHED_EVENT_LEVEL_REAL_MOVES",
        "cultural_or_institutional_causal_inference":"NOT_ESTABLISHED",
        "independent_E3":"OPEN",
        "pesen_v01":"FROZEN"}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    result=evaluate()
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],
        "total_runs":result["total_deterministic_agent_experiments"],
        "summary":{tau:{p:{"satisfied":q["all_satisfied"],
                             "stalled":q["stalled"],
                             "baseline_succeeded_limited_stalled":q["global_stable_but_competitor_stalled"],
                             "baseline_stalled_limited_succeeded":q["global_stalled_but_competitor_stable"],
                             "policy_selection_blocked_another_can_move":
                                  q["stalled_first_agent_while_another_can_move"]}
                      for p,q in t.items()}
                   for tau,t in result["results"].items()}},sort_keys=True))


if __name__=="__main__":
    main()
