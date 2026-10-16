#!/usr/bin/env python3
"""R070 tiny deterministic Schelling-style relocation, pure E1 math only.

Two anonymous abstract A/B types on 4x4 board; no empirical demographic
observations, no assertion of original Schelling's exact spatial algorithm.
"""
from __future__ import annotations
import argparse,json,math
from collections import Counter
from pathlib import Path

INITIAL=(
    (1,2,0,0),
    (1,2,0,0),
    (0,0,0,0),
    (0,0,0,0),
)
VALUES=frozenset((0,1,2))


def validate(board,tau):
    if (not isinstance(board,(tuple,list)) or not board or
        any(not isinstance(row,(tuple,list)) or len(row)!=len(board[0]) for row in board)
        or not 1<=len(board)<=50 or not 1<=len(board[0])<=50):
        raise ValueError("nonrectangular or oversize spatial board")
    if any(type(v) is not int or v not in VALUES for row in board for v in row):
        raise ValueError("board cells must be empty 0, abstract type 1 or 2")
    if not isinstance(tau,(int,float)) or not math.isfinite(tau) or not 0<=tau<=1:
        raise ValueError("tau must be finite in [0,1]")
    return tuple(tuple(row) for row in board)


def neighbors(board,row,col):
    h=len(board);w=len(board[0])
    for dr in (-1,0,1):
        for dc in (-1,0,1):
            if not dr and not dc:continue
            nr=row+dr;nc=col+dc
            if 0<=nr<h and 0<=nc<w:
                yield nr,nc


def fraction(board,row,col,kind):
    occupied=[board[r][c] for r,c in neighbors(board,row,col) if board[r][c]!=0]
    if not occupied:
        return None
    return sum(v==kind for v in occupied)/len(occupied)


def happy(board,row,col,tau):
    kind=board[row][col]
    if kind==0:
        raise ValueError("vacant cell is not an agent")
    ratio=fraction(board,row,col,kind)
    return ratio is None or ratio>=tau


def metrics(board,tau):
    b=validate(board,tau)
    unhappy=0
    ratios=[]
    current_count=Counter(v for row in b for v in row)
    for row in range(len(b)):
        for col in range(len(b[0])):
            if not b[row][col]:continue
            f=fraction(b,row,col,b[row][col])
            if f is not None:ratios.append(f)
            unhappy+=int(not happy(b,row,col,tau))
    same=0
    diff=0
    for row in range(len(b)):
        for col in range(len(b[0])):
            here=b[row][col]
            if not here:continue
            for dr,dc in ((0,1),(1,0)):
                rr=row+dr;cc=col+dc
                if rr>=len(b) or cc>=len(b[0]) or not b[rr][cc]:continue
                if here==b[rr][cc]:same+=1
                else:diff+=1
    return {
        "unhappy_agents":unhappy,
        "agents_with_occupied_neighbor":len(ratios),
        "mean_local_same_type_fraction_if_neighbors":
            sum(ratios)/len(ratios) if ratios else None,
        "cardinal_occupied_same_type_edges":same,
        "cardinal_occupied_different_type_edges":diff,
        "cardinal_different_type_edge_share":
            diff/(same+diff) if same+diff else None,
        "type_A_agents":current_count[1],
        "type_B_agents":current_count[2],
        "empty_cells":current_count[0],
        "board_cells":sum(current_count.values()),
    }


def step(board,tau):
    b=validate(board,tau)
    unhappy=[(r,c) for r in range(len(b)) for c in range(len(b[0]))
             if b[r][c] and not happy(b,r,c,tau)]
    if not unhappy:
        return b,{"status":"STABLE_ALL_SATISFIED","moved":False}
    source=unhappy[0]
    agent=b[source[0]][source[1]]
    staged=[list(row) for row in b]
    staged[source[0]][source[1]]=0
    for r in range(len(b)):
        for c in range(len(b[0])):
            if staged[r][c]!=0:continue
            f=fraction(staged,r,c,agent)
            if f is None or f<tau:
                continue
            staged[r][c]=agent
            updated=tuple(tuple(row) for row in staged)
            if not happy(updated,r,c,tau):
                raise AssertionError("new location fails relocation acceptance")
            counts0=Counter(v for row in b for v in row)
            counts1=Counter(v for row in updated for v in row)
            if counts0!=counts1:
                raise AssertionError("relocation illegally creates or destroys agents")
            return updated,{"status":"MOVED",
                            "moved":True,
                            "from":[source[0],source[1]],
                            "to":[r,c],
                            "abstract_type":agent,
                            "destination_same_neighbor_fraction":f}
    return b,{"status":"STALLED_NO_SATISFYING_VACANCY",
              "moved":False,"unsatisfied_agent_count":len(unhappy)}


def run(board,tau,steps=8):
    if type(steps) is not int or not 0<=steps<=100:
        raise ValueError("nonnegative bounded integer steps required")
    state=validate(board,tau)
    snapshot=[{"tick":0,"board":state,"metrics":metrics(state,tau)}]
    changes=[]
    status="MAX_STEP_BUDGET"
    for i in range(1,steps+1):
        nxt,event=step(state,tau)
        if not event["moved"]:
            status=event["status"]
            break
        changes.append(event)
        state=nxt
        snapshot.append({"tick":i,"board":state,"metrics":metrics(state,tau)})
    else:
        if metrics(state,tau)["unhappy_agents"]==0:
            status="STABLE_ALL_SATISFIED"
    return {
        "initial_board":board,
        "tau":tau,
        "budget":steps,
        "actual_moves":len(changes),
        "termination":status,
        "move_log":changes,
        "snapshots":snapshot,
        "source_type_counts_preserved":all(
            all(y["metrics"][k]==snapshot[0]["metrics"][k] for k in
                ("type_A_agents","type_B_agents","empty_cells"))
            for y in snapshot),
    }


def benchmark():
    zero=run(INITIAL,0.,8)
    half=run(INITIAL,.5,8)
    if zero["actual_moves"] or zero["snapshots"][-1]["board"]!=INITIAL:
        raise AssertionError("neutral tolerance moves agents")
    if not half["move_log"] or half["move_log"][0]["from"]!=[0,0] or half["move_log"][0]["to"]!=[2,0]:
        raise AssertionError("first fixed relocation expected (0,0)->(2,0)")
    if not half["source_type_counts_preserved"]:
        raise AssertionError("original abstract types or vacancies not preserved")
    return {
        "research_id":"R070",
        "stage":"E1_SCHELLING_LOCAL_SATISFACTION_AND_SPATIAL_PATTERN",
        "status":"E1_SYNTHETIC_SPATIAL_RULE_PASS",
        "protocol":"protocols/R070_SCHELLING_SPATIAL_MICRO_MACRO_2026-10-16.md",
        "original_literature_DOI":"10.1080/0022250X.1971.9989794",
        "experiment_board_dimensions":[4,4],
        "local_neighbor_definition":"Moore8 finite, no wrap",
        "relocation_selection":"row-major unsatisfied source then first nonisolated satisfying vacancy",
        "neutral_tau0":zero,
        "tolerant_tau0_5":half,
        "synthetic_only":True,
        "real_residential_mobility_e2":"OPEN",
        "real_discrimination_or_historical_social_causality":"NOT_IDENTIFIED",
        "pesen_v01":"FROZEN",
    }


def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    output=benchmark()
    args.output.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":output["status"],
        "moves_tau0":output["neutral_tau0"]["actual_moves"],
        "moves_tau0_5":output["tolerant_tau0_5"]["actual_moves"],
        "tau0_5_termination":output["tolerant_tau0_5"]["termination"],
        "tau0_5_final_metrics":output["tolerant_tau0_5"]["snapshots"][-1]["metrics"],
    },sort_keys=True))


if __name__=="__main__":
    main()
