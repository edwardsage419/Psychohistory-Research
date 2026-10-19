#!/usr/bin/env python3
"""R120 independently reconstruct the exact distribution of Linear Threshold sets.

KKT (2003) SIGKDD, pp137-146, original author's Cornell paper PDF
https://www.cs.cornell.edu/home/kleinber/kdd03-inf.pdf
Theorem 2.5, Claim 2.6: iid Uniform threshold vs one chosen incoming live
edge (or none) per target node have SAME DISTRIBUTION over active sets.
Every mass is an exact Fraction. No human behaviors or original dataset used.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, product
import json

class LinearThresholdError(ValueError):
    pass


def _fraction(value, label, strictly_positive=False):
    if type(value) is not F or not (F(0)<value<=F(1) if strictly_positive else F(0)<=value<=F(1)):
        raise LinearThresholdError("R120_EXACT_UNIT_FRACTION_REQUIRED_"+label)
    return value


def _node(value,n,label):
    if type(value) is not int or not 0 <= value < n:
        raise LinearThresholdError("R120_NODE_ID_INVALID_"+label)
    return value


def _inputs(n, edges, seeds):
    if type(n) is not int or not 1 <= n <= 6:
        raise LinearThresholdError("R120_GRAPH_N_1_TO_6_REQUIRED")
    if type(edges) not in (tuple,list):
        raise LinearThresholdError("R120_EXPLICIT_WEIGHTED_EDGES_REQUIRED")
    if type(seeds) not in (tuple,list,set,frozenset):
        raise LinearThresholdError("R120_EXPLICIT_SEED_COLLECTION_REQUIRED")
    seed_list=list(seeds)
    if len(seed_list)!=len(set((type(x),x) for x in seed_list)):
        raise LinearThresholdError("R120_DUPLICATE_SEED")
    ss=frozenset(_node(x,n,"SEED") for x in seed_list)
    inc=[[] for _ in range(n)]
    seen=set()
    for edge in edges:
        if type(edge) not in (tuple,list) or len(edge)!=3:
            raise LinearThresholdError("R120_EDGE_TRIPLE_SOURCE_TARGET_WEIGHT_REQUIRED")
        u=_node(edge[0],n,"EDGE_SOURCE")
        v=_node(edge[1],n,"EDGE_TARGET")
        if u==v:
            raise LinearThresholdError("R120_SELF_LOOP_FORBIDDEN")
        w=_fraction(edge[2],"EDGE_WEIGHT")
        if (u,v) in seen:
            raise LinearThresholdError("R120_DUPLICATE_DIRECTED_EDGE")
        seen.add((u,v))
        inc[v].append((u,w))
    incoming=tuple(tuple(sorted(row)) for row in inc)
    for row in incoming:
        if sum((w for _,w in row),F(0)) > 1:
            raise LinearThresholdError("R120_TARGET_INCOMING_WEIGHT_EXCEEDS_ONE")
    return incoming,ss


def synchronous_fixed_threshold(n, edges, seeds, thresholds):
    """Irreversible deterministic LT after a realized threshold vector."""
    incoming,ss=_inputs(n,edges,seeds)
    if type(thresholds) not in (tuple,list) or len(thresholds)!=n:
        raise LinearThresholdError("R120_THRESHOLD_VECTOR_LENGTH")
    tt=tuple(_fraction(x,"THRESHOLD",strictly_positive=True) for x in thresholds)
    trace=(ss,)
    active=ss
    for _ in range(n):
        nxt=frozenset(
            v for v in range(n) if v not in active and
            sum((weight for u,weight in incoming[v] if u in active),F(0)) >= tt[v]
        )
        if not nxt:
            return {"active":active,"history":trace,"count":len(active)}
        active=active | nxt
        trace=trace+(active,)
    raise LinearThresholdError("R120_NONTERMINATION")


def _threshold_regions(incoming):
    """Partition [0,1] by ALL possible active-incoming subset sums exactly.

    P(theta in (a,b])=b-a; exact midpoint is representative (endpoints zero
    probability for continuous Uniform). Any threshold from a region yields
    identical eligibility for every possible predecessor active set.
    """
    regions=[]
    for row in incoming:
        boundary={F(0),F(1)}
        for subset_mask in range(1<<len(row)):
            s=sum((weight for j,(_,weight) in enumerate(row)
                   if subset_mask & (1<<j)),F(0))
            boundary.add(s)
        pts=sorted(boundary)
        ranges=tuple(((left+right)/2,right-left)
                     for left,right in zip(pts,pts[1:]) if left<right)
        if sum((mass for _,mass in ranges),F(0))!=1:
            raise LinearThresholdError("R120_UNIFORM_PARTITION_MASS_NOT_ONE")
        regions.append(ranges)
    return tuple(regions)


def exact_threshold_distribution(n, edges, seeds):
    """Explicit independent exact integration of uniform thresholds.

    Calls deterministic activation but does not call live-edge enumeration.
    """
    incoming,ss=_inputs(n,edges,seeds)
    regions=_threshold_regions(incoming)
    combos=1
    for row in regions:
        combos *= len(row)
    if combos>200000:
        raise LinearThresholdError("R120_EXACT_ENUMERATION_TOO_LARGE")
    out={}
    for draw in product(*regions):
        theta=tuple(threshold for threshold,_ in draw)
        mass=F(1)
        for _,p in draw:
            mass*=p
        if mass==0:
            continue
        active=synchronous_fixed_threshold(n,edges,ss,theta)["active"]
        out[active]=out.get(active,F(0))+mass
    if sum(out.values(),F(0))!=1:
        raise LinearThresholdError("R120_THRESHOLD_DISTRIBUTION_NOT_NORMALIZED")
    return out


def _live_edge_options(incoming):
    """Each target picks at most ONE entering edge or none, independently."""
    choices=[]
    for row in incoming:
        active_options=[(source,weight) for source,weight in row if weight>0]
        missing=F(1)-sum((weight for _,weight in row),F(0))
        if missing>0:
            active_options.append((None,missing))
        if sum((p for _,p in active_options),F(0))!=1:
            raise LinearThresholdError("R120_LIVE_EDGE_CHOICE_MASS_INVALID")
        choices.append(tuple(active_options))
    return tuple(choices)


def exact_live_edge_distribution(n,edges,seeds):
    """Independent KKT live edge reachability enumeration. NO threshold calls."""
    incoming,ss=_inputs(n,edges,seeds)
    choices=_live_edge_options(incoming)
    combos=1
    for row in choices:
        combos*=len(row)
    if combos>200000:
        raise LinearThresholdError("R120_EXACT_ENUMERATION_TOO_LARGE")
    out={}
    for outcome in product(*choices):
        parent=tuple(choice[0] for choice in outcome)
        mass=F(1)
        for _,prob in outcome:
            mass*=prob
        reached=set(ss)
        # Direct reachability, not another threshold process.
        stack=list(ss)
        while stack:
            source=stack.pop()
            for v,p in enumerate(parent):
                if p==source and v not in reached:
                    reached.add(v)
                    stack.append(v)
        reached=frozenset(reached)
        out[reached]=out.get(reached,F(0))+mass
    if sum(out.values(),F(0))!=1:
        raise LinearThresholdError("R120_LIVE_EDGE_DISTRIBUTION_NOT_NORMALIZED")
    return out


def verify_distribution_equivalence(n,edges,seeds):
    a=exact_threshold_distribution(n,edges,seeds)
    b=exact_live_edge_distribution(n,edges,seeds)
    if a!=b:
        raise LinearThresholdError("R120_AUTHOR_CLAIM_2_6_DISTRIBUTIONS_NOT_EQUIVALENT")
    return a


def expected_influence(distribution):
    """One expected activation count; exact probability and set keys only."""
    if type(distribution) is not dict or not distribution:
        raise LinearThresholdError("R120_NONEMPTY_EXACT_DISTRIBUTION_REQUIRED")
    if any(type(k) is not frozenset for k in distribution):
        raise LinearThresholdError("R120_DISTRIBUTION_SET_KEYS_REQUIRED")
    if any(type(v) is not F or v<0 for v in distribution.values()):
        raise LinearThresholdError("R120_DISTRIBUTION_PROBS_REQUIRED")
    if sum(distribution.values(),F(0))!=1:
        raise LinearThresholdError("R120_DISTRIBUTION_MUST_NORMALIZE")
    return sum((len(active)*prob for active,prob in distribution.items()),F(0))


def all_seed_influence(n,edges):
    _inputs(n,edges,())
    influence={}
    for mask in range(1<<n):
        seeds=frozenset(i for i in range(n) if mask&(1<<i))
        dist=verify_distribution_equivalence(n,edges,seeds)
        influence[seeds]=expected_influence(dist)
    return influence


def verify_monotone_submodular(influence):
    """Check diminishing expected influence returns for all seed sets A⊆B."""
    if type(influence) is not dict or frozenset() not in influence:
        raise LinearThresholdError("R120_SEED_INFLUENCE_MAP_INVALID")
    sets=list(influence)
    universe=frozenset().union(*sets)
    if len(sets)!=(1<<len(universe)) or any(s not in influence for r in range(len(universe)+1)
                              for s in map(frozenset,combinations(universe,r))):
        raise LinearThresholdError("R120_INCOMPLETE_SEED_SET_POWERSET")
    for a in sets:
        for b in sets:
            if a<=b:
                if influence[a]>influence[b]:
                    raise LinearThresholdError("R120_EXPECTED_INFLUENCE_NONMONOTONE")
                for v in universe-b:
                    lhs=influence[a|{v}]-influence[a]
                    rhs=influence[b|{v}]-influence[b]
                    if lhs<rhs:
                        raise LinearThresholdError("R120_EXPECTED_INFLUENCE_NOT_SUBMODULAR")
    return True


def all_three_node_digraphs():
    """1,4,64 simple directed graphs of n=1,2,3 with weights 1/indegree.

    All 530 (graph, seed_set) cases checked via *distributions*, not just
    expected sums. This is 530 pure mathematics cases, NO humans.
    """
    counts={}
    for n in (1,2,3):
        possible=tuple((u,v) for u in range(n) for v in range(n) if u!=v)
        tested=0
        for mask in range(1<<len(possible)):
            pairs=tuple(edge for i,edge in enumerate(possible) if mask&(1<<i))
            incoming_degree={v:sum(1 for _,target in pairs if target==v) for v in range(n)}
            edges=tuple((u,v,F(1,incoming_degree[v])) for u,v in pairs)
            influence=all_seed_influence(n,edges)
            verify_monotone_submodular(influence)
            tested+=len(influence)
        counts[str(n)]=tested
    if counts!={"1":2,"2":16,"3":512}:
        raise LinearThresholdError("R120_EXHAUSTIVE_TEST_COVERAGE_DRIFT")
    return counts


def fixed_threshold_failure_of_submodularity():
    """Our own counterexample, *not* numbers transcribed from the paper."""
    edges=((0,2,F(1,2)),(1,2,F(1,2)))
    theta=(F(1),F(1),F(3,4))
    def fixed(a):
        return synchronous_fixed_threshold(3,edges,tuple(a),theta)["count"]
    observed={frozenset(a):fixed(a) for a in ((),(0,),(1,),(0,1))}
    expected={frozenset(a):expected_influence(
        verify_distribution_equivalence(3,edges,tuple(a)))
        for a in ((),(0,),(1,),(0,1))}
    return {
        "fixed_empty":observed[frozenset()],
        "fixed_seed0":observed[frozenset((0,))],
        "fixed_seed1":observed[frozenset((1,))],
        "fixed_both":observed[frozenset((0,1))],
        "fixed_marginal_seed0_without_seed1":observed[frozenset((0,))]-observed[frozenset()],
        "fixed_marginal_seed0_with_seed1":observed[frozenset((0,1))]-observed[frozenset((1,))],
        "expected_marginal_seed0_without_seed1":str(expected[frozenset((0,))]-expected[frozenset()]),
        "expected_marginal_seed0_with_seed1":str(expected[frozenset((0,1))]-expected[frozenset((1,))]),
        "fixed_threshold_is_not_necessarily_submodular":True,
        "uniform_random_threshold_expected_influence_is_submodular":True,
    }


def source_analytic_fixtures():
    one=((0,2,F(1,2)),(1,2,F(1,4)))
    chain=((0,1,F(1,2)),(1,2,F(2,3)),(2,3,F(3,4)))
    ring=((0,1,F(1,2)),(1,2,F(1,2)),(2,0,F(1,2)))
    return {
        "single_node_probability_nonlinearity":{
            "seed_0":str(expected_influence(verify_distribution_equivalence(3,one,(0,)))),
            "seed_1":str(expected_influence(verify_distribution_equivalence(3,one,(1,)))),
            "seed_0_and_1":str(expected_influence(verify_distribution_equivalence(3,one,(0,1)))),
        },
        "four_node_weighted_chain_seed_0":str(expected_influence(verify_distribution_equivalence(4,chain,(0,)))),
        "three_node_cycle_seed_0":str(expected_influence(verify_distribution_equivalence(3,ring,(0,)))),
        "fixed_threshold_non_submodularity":fixed_threshold_failure_of_submodularity(),
        "entire_three_node_directed_graph_seed_distribution_audit":all_three_node_digraphs(),
    }


if __name__=="__main__":
    print(json.dumps(source_analytic_fixtures(),sort_keys=True,indent=2))
