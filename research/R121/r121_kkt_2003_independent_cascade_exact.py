#!/usr/bin/env python3
"""R121: exact independent-cascade dynamics vs independent live-edge outcomes.

First-hand 2003 original: Kempe, Kleinberg & Tardos, KDD pp137-146,
doi:10.1145/956750.956769. PDF p2 for one-attempt rule, p4 for Claim 2.3
and Theorem 2.2 (zero-based PDF pages 1,3).

This is a bounded rational mathematical reconstruction, not actual social
network observations, human prediction, psychological or historical forecast.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product
import json


class CascadeAuditError(ValueError):
    """Fail closed on a malformed independent cascade study design."""


def _probability(value):
    if type(value) is not F or not F(0) <= value <= F(1):
        raise CascadeAuditError("R121_EXACT_FRACTION_PROBABILITY_0_TO_1_REQUIRED")
    return value


def _node(x, n):
    if type(x) is not int or not 0 <= x < n:
        raise CascadeAuditError("R121_NODE_ID_INTEGER_0_TO_N_MINUS_1_REQUIRED")
    return x


def validate(n, edges, seeds):
    if type(n) is not int or not 1 <= n <= 5:
        raise CascadeAuditError("R121_GRAPH_SIZE_1_TO_5_REQUIRED")
    if type(edges) not in (tuple, list):
        raise CascadeAuditError("R121_EXPLICIT_EDGE_SEQUENCE_REQUIRED")
    if len(edges) > 12:
        raise CascadeAuditError("R121_AT_MOST_12_EDGES_FOR_EXACT_ENUMERATION")
    if type(seeds) not in (tuple, list, set, frozenset):
        raise CascadeAuditError("R121_EXPLICIT_SEED_CONTAINER_REQUIRED")
    raw_seeds = list(seeds)
    seed_nodes = [_node(x, n) for x in raw_seeds]
    if len(set(seed_nodes)) != len(seed_nodes):
        raise CascadeAuditError("R121_DUPLICATE_SEED")
    result = frozenset(seed_nodes)
    seen = set()
    parsed = []
    for record in edges:
        if type(record) not in (tuple, list) or len(record) != 3:
            raise CascadeAuditError("R121_EDGE_TRIPLE_REQUIRED")
        u, v = _node(record[0], n), _node(record[1], n)
        if u == v:
            raise CascadeAuditError("R121_NO_SELF_LOOPS")
        if (u,v) in seen:
            raise CascadeAuditError("R121_DUPLICATE_DIRECTED_EDGE")
        seen.add((u,v))
        parsed.append((u,v,_probability(record[2])))
    return tuple(parsed), result


def _bernoulli_outcomes(prob):
    """Explicit independent Bernoulli outcomes, drop only zero-prob branches."""
    p = _probability(prob)
    return tuple((success, mass) for success,mass in ((False, F(1)-p), (True, p))
                 if mass > 0)


def exact_one_chance_round_distribution(n, edges, seeds):
    """Independent event-tree dynamics respecting activation frontiers.

    Each edge is attempted only when its source was newly active in the
    preceding step, and only if its target is currently inactive.
    Multiple successful attempts to the same target still activate it once.
    This function NEVER invokes independent-live-edge reachability.
    """
    links, initial = validate(n, edges, seeds)
    distribution = {}

    def visit(active, frontier, path_mass):
        if not frontier:
            distribution[active] = distribution.get(active, F(0)) + path_mass
            return
        available = tuple((u,v,p) for u,v,p in links if u in frontier and v not in active)
        if not available:
            distribution[active] = distribution.get(active, F(0)) + path_mass
            return
        for outcome in product(*(_bernoulli_outcomes(p) for _,_,p in available)):
            mass = path_mass
            newly = set()
            for (_,v,_), (success, prob) in zip(available, outcome):
                mass *= prob
                if success:
                    newly.add(v)
            newcomers = frozenset(newly)
            if newcomers:
                visit(active | newcomers, newcomers, mass)
            else:
                distribution[active] = distribution.get(active,F(0)) + mass

    visit(initial, initial, F(1))
    if sum(distribution.values(),F(0)) != 1:
        raise CascadeAuditError("R121_ROUND_BASED_MASS_NOT_NORMALIZED")
    return distribution


def exact_independent_live_edge_distribution(n, edges, seeds):
    """Pre-flip one INDEPENDENT coin for every directed edge, then reachability.

    Unlike LT, an arbitrary number of incoming edges can be simultaneously
    live. This implementation NEVER invokes the one-chance process.
    """
    links, initial = validate(n, edges, seeds)
    distribution = {}
    for outcome in product(*(_bernoulli_outcomes(p) for _,_,p in links)):
        prob = F(1)
        adjacency = [set() for _ in range(n)]
        for (u,v,_),(success,mass) in zip(links,outcome):
            prob *= mass
            if success:
                adjacency[u].add(v)
        active = set(initial)
        todo = list(initial)
        while todo:
            u = todo.pop()
            for v in adjacency[u]:
                if v not in active:
                    active.add(v)
                    todo.append(v)
        final = frozenset(active)
        distribution[final] = distribution.get(final,F(0)) + prob
    if sum(distribution.values(),F(0)) != 1:
        raise CascadeAuditError("R121_PRE_FLIPPED_EDGE_MASS_NOT_NORMALIZED")
    return distribution


def verify_complete_distribution(n, edges, seeds):
    chronological = exact_one_chance_round_distribution(n,edges,seeds)
    preflipped = exact_independent_live_edge_distribution(n,edges,seeds)
    if chronological != preflipped:
        raise CascadeAuditError("R121_SOURCE_CLAIM_2_3_FULL_FINAL_SET_DISTRIBUTIONS_DIFFER")
    return chronological


def expected_final_count(distribution):
    if type(distribution) is not dict or not distribution:
        raise CascadeAuditError("R121_NONEMPTY_FINAL_SET_PROBABILITY_MAP_REQUIRED")
    if any(type(k) is not frozenset for k in distribution):
        raise CascadeAuditError("R121_FINAL_STATES_ARE_FROZENSETS")
    if any(type(v) is not F or v < 0 for v in distribution.values()) or sum(distribution.values(),F(0))!=1:
        raise CascadeAuditError("R121_MASS_MUST_BE_NORMALIZED_EXACT_FRACTION")
    return sum((len(active)*mass for active,mass in distribution.items()),F(0))


def all_seed_expected_influence(n,edges):
    validate(n,edges,())
    out = {}
    for mask in range(1<<n):
        seeds=frozenset(i for i in range(n) if mask & (1<<i))
        out[seeds]=expected_final_count(verify_complete_distribution(n,edges,seeds))
    return out


def check_monotone_submodular_expected(influence):
    """Independently check finite expected diminishing returns over full powerset."""
    if type(influence) is not dict or not influence or frozenset() not in influence:
        raise CascadeAuditError("R121_EXPECTED_INFLUENCE_POWERSET_REQUIRED")
    if any(type(k) is not frozenset or any(type(v) is not int for v in k)
           for k in influence):
        raise CascadeAuditError("R121_SEED_SET_KEY_TYPE_INVALID")
    if any(type(v) is not F for v in influence.values()):
        raise CascadeAuditError("R121_EXPECTED_SCORE_MUST_BE_FRACTION")
    universe=frozenset().union(*influence)
    if len(influence)!=(1<<len(universe)) or any(
        frozenset(i for i in universe if mask & (1<<i)) not in influence
        for mask in range(1<<len(universe))
    ):
        # The exhaustive callers use canonical labels 0..n-1.
        raise CascadeAuditError("R121_EXPECTED_INFLUENCE_POWSET_INCOMPLETE")
    for a in influence:
        for b in influence:
            if a <= b:
                if influence[a] > influence[b]:
                    raise CascadeAuditError("R121_EXPECTED_INFLUENCE_NOT_MONOTONE")
                for target in universe-b:
                    lhs = influence[a|{target}]-influence[a]
                    rhs = influence[b|{target}]-influence[b]
                    if lhs < rhs:
                        raise CascadeAuditError("R121_EXPECTED_INFLUENCE_NOT_SUBMODULAR")
    return True


def _frozen_edge_cases():
    three=((0,2,F(1,2)), (1,2,F(1,4)))
    chain=((0,1,F(1,2)), (1,2,F(2,3)), (2,3,F(3,4)))
    cycle=((0,1,F(1,2)), (1,2,F(1,2)), (2,0,F(1,2)))
    return three,chain,cycle


def fixed_primary_mechanism_cases():
    three,chain,cycle = _frozen_edge_cases()
    p1 = verify_complete_distribution(3,three,(0,))
    p2 = verify_complete_distribution(3,three,(1,))
    both = verify_complete_distribution(3,three,(0,1))
    return {
        "single_source0_expected":str(expected_final_count(p1)),
        "single_source1_expected":str(expected_final_count(p2)),
        "both_sources_target_activation_probability":str(
            sum((w for a,w in both.items() if 2 in a),F(0))),
        "both_sources_expected":str(expected_final_count(both)),
        "both_edges_live_joint_probability":str(F(1,2)*F(1,4)),
        "four_chain_seed0_expected":str(expected_final_count(
            verify_complete_distribution(4,chain,(0,)))),
        "four_chain_last_node_probability":str(sum((
            w for active,w in verify_complete_distribution(4,chain,(0,)).items()
            if 3 in active),F(0))),
        "three_cycle_seed0_expected":str(expected_final_count(
            verify_complete_distribution(3,cycle,(0,)))),
        "same_weights_as_LT_R120_both_sources_expected":"11/4",
        "IC_vs_LT_random_edge_construction_different":True,
        "human_E2_observations":0,
        "R073":"FROZEN",
        "PESEN_v0_1":"FROZEN",
    }


def deterministic_three_round_trace():
    """Timed single-chance example with 0->2 p=0 (no retry)."""
    n=3
    links=((0,1,F(1)), (1,2,F(1)), (0,2,F(0)))
    parsed,seeds=validate(n,links,(0,))
    active=seeds
    frontier=seeds
    trace=[active]
    for _ in range(n):
        eligible={(u,v) for u,v,p in parsed if u in frontier and v not in active and p==1}
        newcomers=frozenset(v for u,v in eligible)
        if not newcomers:
            break
        active=active|newcomers
        frontier=newcomers
        trace.append(active)
    return tuple(trace)


def exhaustive_small_directed_graphs():
    """All 1+4+64 digraphs x all seeds x TWO fixed edge probability schemes.

    2*(1*2+4*4+64*8)=1060 pure mathematical cases, NOT human experiments.
    """
    totals={}
    for n in (1,2,3):
        possibilities=tuple((u,v) for u in range(n) for v in range(n) if u!=v)
        audited=0
        for mask in range(1<<len(possibilities)):
            selected=tuple(edge for i,edge in enumerate(possibilities) if mask&(1<<i))
            for scheme in ("HALF","PARITY_QUARTERS"):
                links=tuple((u,v,F(1,2) if scheme=="HALF"
                            else F(1,4) if (u+v)%2==0 else F(3,4))
                            for u,v in selected)
                influence=all_seed_expected_influence(n,links)
                check_monotone_submodular_expected(influence)
                audited += len(influence)
        totals[str(n)] = audited
    if totals!={"1":4,"2":32,"3":1024}:
        raise CascadeAuditError("R121_EXHAUSTIVE_COVERAGE_COUNT_WRONG")
    return totals


if __name__=="__main__":
    print(json.dumps({
        "sources":["10.1145/956750.956769","10.1023/A:1011122126881"],
        "primary_original_2003_mechanism":fixed_primary_mechanism_cases(),
        "synthetic_1060_graph_seed_probability_case_counts":exhaustive_small_directed_graphs(),
        "deterministic_round_activation_sets":[sorted(x) for x in deterministic_three_round_trace()],
        "all_real_individual_E2_counts":0,
    }, indent=2,sort_keys=True))
