#!/usr/bin/env python3
"""R122: Centola & Macy (2007), bounded graph-and-bridge theoretical learning.

Source: AJS 113(3):702-734, DOI 10.1086/521848, printed pp706,710-714.
Independent deterministic toy illustrating distinct-source reinforcement; NOT
a reimplementation of their full stochastic rewiring simulations, and there
are no real human social-network data or model-prediction E2 scores.
"""
from __future__ import annotations

from fractions import Fraction
from itertools import combinations, product
import json


PRIMARY_DOI = "10.1086/521848"


class ContagionDesignError(ValueError):
    """Invalid exact graph/threshold contract, or mathematical disagreement."""


def validate(n, edges, thresholds, seeds):
    if type(n) is not int or not 1 <= n <= 8:
        raise ContagionDesignError("R122_N_INTEGER_1_TO_8_REQUIRED")
    if type(edges) not in (tuple, list) or type(thresholds) not in (tuple, list):
        raise ContagionDesignError("R122_EXPLICIT_EDGE_AND_THRESHOLD_SEQUENCES_REQUIRED")
    if len(thresholds) != n or any(type(t) is not int or not 1 <= t <= n for t in thresholds):
        raise ContagionDesignError("R122_THRESHOLD_POSITIVE_INTEGER_1_TO_N_REQUIRED")
    if type(seeds) not in (tuple, list, set, frozenset):
        raise ContagionDesignError("R122_EXPLICIT_SEED_COLLECTION_REQUIRED")
    seed_list = list(seeds)
    if any(type(x) is not int or not 0 <= x < n for x in seed_list):
        raise ContagionDesignError("R122_SEED_NODE_INVALID")
    if len(set(seed_list)) != len(seed_list):
        raise ContagionDesignError("R122_DUPLICATE_SEED")
    graph = [set() for _ in range(n)]
    seen = set()
    for pair in edges:
        if type(pair) not in (tuple, list) or len(pair) != 2:
            raise ContagionDesignError("R122_UNDIRECTED_EDGE_PAIR_REQUIRED")
        a,b = pair
        if type(a) is not int or type(b) is not int or not 0 <= a < n or not 0 <= b < n:
            raise ContagionDesignError("R122_EDGE_ENDPOINT_INVALID")
        if a == b:
            raise ContagionDesignError("R122_NO_SELF_LOOPS")
        undirected = (min(a,b),max(a,b))
        if undirected in seen:
            raise ContagionDesignError("R122_DUPLICATE_UNDIRECTED_EDGE")
        seen.add(undirected)
        graph[a].add(b)
        graph[b].add(a)
    return tuple(frozenset(row) for row in graph), tuple(thresholds), frozenset(seed_list)


def synchronous_distinct_neighbor_cascade(n, edges, thresholds, seeds):
    """One irreversible synchronous adoption at a time from distinct alters."""
    adj, cutoff, initial = validate(n,edges,thresholds,seeds)
    active = initial
    trajectory = (active,)
    for _ in range(n):
        newcomers = frozenset(
            v for v in range(n) if v not in active
            and len(adj[v].intersection(active)) >= cutoff[v]
        )
        if not newcomers:
            return {
                "final":active,
                "count":len(active),
                "trajectory":trajectory,
                "rounds_with_adoption":len(trajectory)-1,
            }
        active = active | newcomers
        trajectory = trajectory+(active,)
    raise ContagionDesignError("R122_SYNC_NONTERMINATION")


def independent_least_closed_set(n, edges, thresholds, seeds):
    """Independently find intersection of ALL closed supersets of seeds.

    Enumerates subsets rather than invoking synchronous/async dynamics.
    Monotone activation's least closed superset is the intersection of all
    closed supersets. At n<=8 enumeration is intentionally bounded.
    """
    adj, cutoff, initial = validate(n,edges,thresholds,seeds)
    required_mask = sum(1 << v for v in initial)
    neigh_masks = tuple(sum(1<<j for j in row) for row in adj)
    intersection = (1 << n)-1
    closed_count = 0
    for mask in range(1 << n):
        if (mask & required_mask) != required_mask:
            continue
        closed = True
        for v in range(n):
            if (mask & (1<<v)) == 0 and (mask & neigh_masks[v]).bit_count() >= cutoff[v]:
                closed = False
                break
        if closed:
            intersection &= mask
            closed_count += 1
    if not closed_count:
        raise ContagionDesignError("R122_NO_CLOSED_SEED_SUPERSET")
    return frozenset(v for v in range(n) if intersection & (1<<v))


def verify_independent_final_sets(n, edges, thresholds, seeds):
    sync = synchronous_distinct_neighbor_cascade(n,edges,thresholds,seeds)
    closed = independent_least_closed_set(n,edges,thresholds,seeds)
    if sync["final"] != closed:
        raise ContagionDesignError("R122_INDEPENDENT_FINAL_SETS_DIVERGED")
    trace=sync["trajectory"]
    if trace[0] != frozenset(seeds) or any(not x < y for x,y in zip(trace,trace[1:])):
        raise ContagionDesignError("R122_TRAJECTORY_NOT_STRICTLY_MONOTONE")
    adj,t,_=validate(n,edges,thresholds,seeds)
    if any(len(adj[v] & closed) >= t[v] for v in range(n) if v not in closed):
        raise ContagionDesignError("R122_FINAL_SET_NOT_CLOSED")
    return sync


def ring_max_effective_bridge_width(z):
    """Original AJS p713 Eq(2): z even ring degree, Wmax=z(z+2)/8."""
    if type(z) is not int or z <= 0 or z%2:
        raise ContagionDesignError("R122_RING_DEGREE_MUST_BE_POSITIVE_EVEN_INT")
    return Fraction(z*(z+2),8)


def ring_critical_bridge_width(a):
    """Original AJS p714 Eq(4): Wc=a(a+1)/2; specific ring bridge design."""
    if type(a) is not int or a < 1:
        raise ContagionDesignError("R122_RING_REQUIRED_ACTIVATED_NEIGHBORS_POSITIVE_INT")
    return Fraction(a*(a+1),2)


def ring_bridge_condition(z,a):
    """Necessary bridge-width criterion for the original special ring model.

    No general finite graph guarantee and no random rewiring simulation.
    """
    max_width=ring_max_effective_bridge_width(z)
    critical=ring_critical_bridge_width(a)
    return {
        "max_width":max_width,
        "critical_width":critical,
        "special_ring_width_sufficient":critical <= max_width,
    }


def _two_cliques():
    group_a=tuple(combinations((0,1,2),2))
    group_b=tuple(combinations((3,4,5),2))
    return group_a+group_b


def frozen_bridge_topologies():
    """OUR toy: two triangles, equal cross-edge count but unequal reinforcement.

    Authors' ring Wc=3 is NOT applied as a generic sufficiency condition.
    """
    within = _two_cliques()
    options = {
        "narrow_one":within+((2,3),),
        "misallocated_three":within+((0,3),(1,4),(2,5)),
        "functional_three":within+((1,3),(2,3),(2,4)),
    }
    return options


def toy_bridge_results():
    topologies = frozen_bridge_topologies()
    result={}
    for name,edges in topologies.items():
        result[name]={
            "cross_edges":len(edges)-len(_two_cliques()),
            "simple_all_A_seeds_final_count":verify_independent_final_sets(
                6,edges,(1,)*6,(0,1,2))["count"],
            "complex_all_A_seeds_final_count":verify_independent_final_sets(
                6,edges,(2,)*6,(0,1,2))["count"],
            "complex_all_A_seeds_round_counts":[len(s) for s in
                verify_independent_final_sets(6,edges,(2,)*6,(0,1,2))["trajectory"]],
        }
    return result


def exact_small_graph_exhaustion():
    """Undirected n<=4 graph x each threshold 1/2 x each seed subset.

    Exactly 4+32+512+16384 = 16932 pure synthetic mathematics examples.
    """
    counts={}
    for n in range(1,5):
        all_pairs=tuple(combinations(range(n),2))
        checks=0
        for mask in range(1<<len(all_pairs)):
            edges=tuple(pair for j,pair in enumerate(all_pairs) if (mask>>j)&1)
            for thresholds in product((1,2),repeat=n):
                for mask_seeds in range(1<<n):
                    seeds=tuple(j for j in range(n) if mask_seeds & (1<<j))
                    verify_independent_final_sets(n,edges,thresholds,seeds)
                    checks+=1
        if checks != 2**len(all_pairs)*2**n*2**n:
            raise ContagionDesignError("R122_EXHAUSTIVE_CASE_COUNT_DRIFT")
        counts[str(n)]=checks
    if counts != {"1":4,"2":32,"3":512,"4":16384}:
        raise ContagionDesignError("R122_EXHAUSTIVE_AUDIT_EXPECTED_COUNTS_DRIFT")
    return counts


def source_and_toy_receipt():
    return {
        "research_id":"R122",
        "original_paper_DOI":PRIMARY_DOI,
        "frozen_bridge_math":{
            "z4_a1":{k:str(v) for k,v in ring_bridge_condition(4,1).items()},
            "z4_a2":{k:str(v) for k,v in ring_bridge_condition(4,2).items()},
            "z4_a3":{k:str(v) for k,v in ring_bridge_condition(4,3).items()},
            "z6_a3":{k:str(v) for k,v in ring_bridge_condition(6,3).items()},
        },
        "original_paper_inspired_not_original_empirical_cases":toy_bridge_results(),
        "full_graph_threshold_seed_synthetic_cases":exact_small_graph_exhaustion(),
        "original_real_human_behavior_E2_reanalysis":0,
        "original_2007_random_rewiring_phase_diagram_replicated":False,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }


if __name__=="__main__":
    print(json.dumps(source_and_toy_receipt(),sort_keys=True,indent=2))
