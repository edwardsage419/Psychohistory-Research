#!/usr/bin/env python3
"""R069 E1: exact small graph threshold adoption, IC live-edge probabilities,
and macro Bass Euler approximation. No empirical diffusion inferred.
"""
from __future__ import annotations
import argparse,itertools,json,math
from collections import deque
from pathlib import Path

N=6
PATH=tuple((i,i+1) for i in range(N-1))
SEED=(0,)


def validate_graph(n,edges,directed=False):
    if type(n) is not int or not 1<=n<=100:
        raise ValueError("node universe must be positive bounded integer")
    out=set()
    for pair in edges:
        if not isinstance(pair,(tuple,list)) or len(pair)!=2:
            raise ValueError("invalid graph edge format")
        a,b=pair
        if (type(a) is not int or type(b) is not int or
            not 0<=a<n or not 0<=b<n or a==b):
            raise ValueError("invalid node reference or self-loop")
        val=(a,b) if directed or a<b else (b,a)
        if val in out:
            raise ValueError("graph repeated edge")
        out.add(val)
    return tuple(sorted(out))


def validate_seed(n,seeds):
    try:members=set(seeds)
    except TypeError:raise ValueError("invalid seed collection") from None
    if not members or any(type(x) is not int or not 0<=x<n for x in members):
        raise ValueError("initial adopters required and in node universe")
    return frozenset(members)


def threshold_trace(n,edges,seeds,threshold,steps=5):
    un=validate_graph(n,edges,directed=False)
    active=validate_seed(n,seeds)
    if (not isinstance(threshold,(int,float)) or not math.isfinite(threshold)
        or not 0<=threshold<=1):
        raise ValueError("nonfinite or impossible node threshold")
    if type(steps) is not int or not 0<=steps<=100:
        raise ValueError("invalid step budget")
    neighbors=[set() for _ in range(n)]
    for a,b in un:
        neighbors[a].add(b);neighbors[b].add(a)
    trace=[tuple(sorted(active))]
    for _ in range(steps):
        new=set(active)
        for i in range(n):
            if i in active or not neighbors[i]:
                continue
            frac=sum(j in active for j in neighbors[i])/len(neighbors[i])
            if frac>=threshold:
                new.add(i)
        if not new.issuperset(active):
            raise AssertionError("irreversible adoption violated")
        active=frozenset(new)
        trace.append(tuple(sorted(active)))
    return trace


def reachability(n,edges,seeds):
    adj=[set() for _ in range(n)]
    for a,b in edges:
        adj[a].add(b)
    visited=set(seeds)
    queue=deque(seeds)
    while queue:
        node=queue.popleft()
        for dest in adj[node]:
            if dest not in visited:
                visited.add(dest)
                queue.append(dest)
    return visited


def independent_cascade_exact(n,edges,seeds,probability):
    directed=validate_graph(n,edges,directed=True)
    initial=validate_seed(n,seeds)
    if len(directed)>12:
        raise ValueError("exact live-edge enumerator capped at 12 directed edges")
    if (not isinstance(probability,(int,float)) or
        not math.isfinite(probability) or not 0<=probability<=1):
        raise ValueError("invalid independent edge exposure probability")
    node_prob=[0.]*n
    total_weight=0.
    m=len(directed)
    for mask in range(1<<m):
        live=[e for i,e in enumerate(directed) if mask & (1<<i)]
        successes=len(live)
        weight=(probability**successes)*((1-probability)**(m-successes))
        activated=reachability(n,live,initial)
        total_weight+=weight
        for i in activated:
            node_prob[i]+=weight
    if abs(total_weight-1)>1e-10 or any(not 0<=x<=1+1e-12 for x in node_prob):
        raise ValueError("exact live-edge probability measure not normalised")
    return {
        "node_adoption_probabilities":node_prob,
        "expected_final_adopters":sum(node_prob),
        "expected_final_adoption_fraction":sum(node_prob)/n,
        "graph_edge_count":m,
        "live_edge_subsets_enumerated":1<<m,
        "independent_per_edge_transmission_probability":float(probability),
        "simulation_or_monte_carlo_used":False,
    }


def bass_euler(initial,p,q,dt,steps):
    vals=(initial,p,q,dt)
    if any(not isinstance(x,(int,float)) or not math.isfinite(x) for x in vals):
        raise ValueError("Bass requires finite numeric input")
    if not 0<=initial<=1 or not 0<=p<=1 or not 0<=q<=1 or not 0<=dt<=1:
        raise ValueError("Bass data or time step out of frozen domain")
    if type(steps) is not int or not 0<=steps<=100:
        raise ValueError("Bass step budget invalid")
    trace=[float(initial)]
    x=trace[0]
    for _ in range(steps):
        nx=x+dt*(p+q*x)*(1-x)
        if not math.isfinite(nx) or nx<0 or nx>1:
            raise ValueError("Bass Euler step left unit interval; no clipping")
        if nx<x:
            raise ValueError("Bass irreversible adoption violated")
        x=nx;trace.append(x)
    return trace


def benchmark():
    half=threshold_trace(N,PATH,SEED,.5,5)
    strict=threshold_trace(N,PATH,SEED,.75,5)
    cascade=independent_cascade_exact(N,PATH,SEED,.5)
    bass=bass_euler(1/N,.03,.4,1,5)
    expected_trace=[tuple(range(k+1)) for k in range(6)]
    expected_nodes=[1,.5,.25,.125,.0625,.03125]
    if half!=expected_trace or any(x!=(0,) for x in strict):
        raise AssertionError("fixed Watts path threshold counterexample differs")
    if cascade["live_edge_subsets_enumerated"]!=32 or any(
        abs(a-b)>1e-12 for a,b in zip(cascade["node_adoption_probabilities"],expected_nodes)):
        raise AssertionError("fixed exact IC probability counterexample differs")
    if abs(cascade["expected_final_adopters"]-1.96875)>1e-12:
        raise AssertionError("IC expected final size differs")
    if abs(bass[1]-.24722222222222223)>1e-12 or abs(bass[5]-.6807123398817322)>1e-12:
        raise AssertionError("Bass original Euler fixed vector differs")
    return {
        "research_id":"R069","stage":"E1_NETWORK_THRESHOLDS_IC_AND_BASS",
        "protocol":"protocols/R069_NETWORK_CASCADE_THREE_MECHANISMS_2026-10-16.md",
        "status":"E1_MECHANISM_PASS",
        "graph":{"nodes":N,"undirected_path_edges":PATH,"directed_IC_edges":PATH,
                 "initial_adopters":SEED},
        "threshold":{"phi_0_5_synchronous_traces":half,
                     "phi_0_75_synchronous_traces":strict},
        "independent_cascade":cascade,
        "bass_discrete_Euler":{"initial":1/N,"innovation_p":.03,"imitation_q":.4,
                                "dt":1,"frequency_trace":bass},
        "source_status":"SYNTHETIC_MATHEMATICS_ONLY",
        "all_three_models_equivalent":"NO_DIFFERENT_INFORMATION_AND_MECHANISMS",
        "historical_technology_adoption_calibration":"NOT_PERFORMED",
        "true_network_exposure_times":"OPEN",
        "e2_empirical_adoption_network":"OPEN",
        "e3_external":"OPEN",
        "pesen_v01":"FROZEN",
    }


def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    data=benchmark()
    args.output.write_text(json.dumps(data,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"study":data["research_id"],"status":data["status"],
                     "Watts_phi_half_active_at_t5":len(data["threshold"]["phi_0_5_synchronous_traces"][-1]),
                     "Watts_phi_high_active_at_t5":len(data["threshold"]["phi_0_75_synchronous_traces"][-1]),
                     "IC_expected_final_adopters":data["independent_cascade"]["expected_final_adopters"],
                     "Bass_Euler_t1":data["bass_discrete_Euler"]["frequency_trace"][1],
                     "Bass_Euler_t5":data["bass_discrete_Euler"]["frequency_trace"][-1]},sort_keys=True))


if __name__=="__main__":
    main()
