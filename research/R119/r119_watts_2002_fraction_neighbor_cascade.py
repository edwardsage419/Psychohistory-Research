#!/usr/bin/env python3
"""R119 exact finite Watts threshold cascades and infinite-graph branching test.

Primary paper: Duncan J Watts (2002), PNAS 99(9):5766-5771,
doi:10.1073/pnas.082090499, https://pmc.ncbi.nlm.nih.gov/articles/PMC122850/
This is independently implemented finite network mathematics and author Eq(5)
branching quantity, NOT human experiment, original ER phase diagram, or
author's random asynchronous update path distribution.
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import combinations, product
import json


class WattsInputError(ValueError):
    pass


def _frac(value, name, positive=False):
    if type(value) is not F or not (F(0) < value <= F(1) if positive else F(0) <= value <= F(1)):
        raise WattsInputError("R119_FRACTION_UNIT_INTERVAL_" + name)
    return value


def _node(value, n, name):
    if type(value) is not int or not 0 <= value < n:
        raise WattsInputError("R119_NODE_ID_INVALID_" + name)
    return value


def validate_graph(n, edges, thresholds, seed):
    if type(n) is not int or not 1 <= n <= 10:
        raise WattsInputError("R119_GRAPH_SIZE_1_TO_10")
    if type(edges) not in (tuple, list) or type(thresholds) not in (tuple, list):
        raise WattsInputError("R119_EXPLICIT_EDGES_AND_THRESHOLDS_REQUIRED")
    if len(thresholds) != n:
        raise WattsInputError("R119_THRESHOLDS_LENGTH_MISMATCH")
    t = tuple(_frac(v, "NODE_THRESHOLD", positive=True) for v in thresholds)
    s = _node(seed, n, "SEED")
    neighbors = [set() for _ in range(n)]
    seen = set()
    for edge in edges:
        if type(edge) not in (tuple,list) or len(edge)!=2:
            raise WattsInputError("R119_EDGE_EXACT_PAIR_REQUIRED")
        a,b = _node(edge[0],n,"EDGE_A"),_node(edge[1],n,"EDGE_B")
        if a==b:
            raise WattsInputError("R119_SELF_LOOP_NOT_ALLOWED")
        pair = (min(a,b), max(a,b))
        if pair in seen:
            raise WattsInputError("R119_DUPLICATE_UNDIRECTED_EDGE")
        seen.add(pair)
        neighbors[a].add(b)
        neighbors[b].add(a)
    return tuple(frozenset(x) for x in neighbors), t, s


def _eligible(v, active, neighbors, thresholds):
    degree = len(neighbors[v])
    return degree>0 and F(len(neighbors[v] & active),degree)>=thresholds[v]


def synchronous_cascade(n,edges,thresholds,seed):
    """Full synchronous turns, do not permit activated nodes to drop out."""
    adj,t,seed = validate_graph(n,edges,thresholds,seed)
    active=frozenset((seed,))
    trace=(active,)
    for _ in range(n):
        new = frozenset(v for v in range(n) if v not in active and _eligible(v,active,adj,t))
        if not new:
            return {"active":active,"history":trace,"size":len(active)}
        active=active | new
        trace=trace+(active,)
    raise WattsInputError("R119_SYNC_CASCADE_NONTERMINATION")


def independently_asynchronous_cascade(n,edges,thresholds,seed):
    """Fair ascending deterministic update, NOT the author's random path law.

    This implementation does not call synchronous_cascade; monotonically
    adds immediately after eligible node checks until a full pass adds none.
    """
    adj,t,seed = validate_graph(n,edges,thresholds,seed)
    active={seed}
    for _ in range(n):
        changed=False
        for v in range(n):
            if v not in active and _eligible(v,frozenset(active),adj,t):
                active.add(v)
                changed=True
        if not changed:
            return frozenset(active)
    raise WattsInputError("R119_ASYNC_CASCADE_NONTERMINATION")


def validate_final_closure(n,edges,thresholds,seed):
    sync=synchronous_cascade(n,edges,thresholds,seed)
    async_result=independently_asynchronous_cascade(n,edges,thresholds,seed)
    if sync["active"] != async_result:
        raise WattsInputError("R119_INDEPENDENT_ALGORITHMS_DIVERGED")
    trace=sync["history"]
    if trace[0]!=frozenset((seed,)) or any(not prev < nxt for prev,nxt in zip(trace,trace[1:])):
        raise WattsInputError("R119_HISTORY_NOT_STRICTLY_MONOTONE")
    adj,t,s=validate_graph(n,edges,thresholds,seed)
    if any(_eligible(v,sync["active"],adj,t) for v in range(n) if v not in sync["active"]):
        raise WattsInputError("R119_RESULT_NOT_CLOSED")
    return sync


def vulnerable_from_one_neighbor(degree, threshold):
    if type(degree) is not int or degree<0:
        raise WattsInputError("R119_DEGREE_NONNEGATIVE_INT_REQUIRED")
    p=_frac(threshold,"VULNERABILITY_THRESHOLD",positive=True)
    return degree>0 and p <= F(1,degree)


def degree_profile(n,edges,thresholds,seed):
    adj,t,_=validate_graph(n,edges,thresholds,seed)
    return tuple(len(v) for v in adj),tuple(vulnerable_from_one_neighbor(len(adj[i]),t[i]) for i in range(n))


def branching_ratio(degree_distribution, vulnerability_by_degree):
    """Infinite locally tree-like random-graph Eq(5): sum k(k-1)pk*rho / z.

    Do NOT apply this number as certain success classifier to any finite graph.
    """
    if type(degree_distribution) not in (tuple,list) or type(vulnerability_by_degree) not in (tuple,list):
        raise WattsInputError("R119_EXPLICIT_DEGREE_PROBABILITIES_REQUIRED")
    if len(degree_distribution)==0 or len(degree_distribution)!=len(vulnerability_by_degree):
        raise WattsInputError("R119_DEGREE_AND_VULNERABLE_DISTRIBUTIONS_SHAPE")
    pk=tuple(_frac(x,"DEGREE_MASS") for x in degree_distribution)
    rho=tuple(_frac(x,"VULNERABILITY_MASS") for x in vulnerability_by_degree)
    if sum(pk,F(0))!=1:
        raise WattsInputError("R119_DEGREE_DISTRIBUTION_NOT_NORMALIZED")
    z=sum((k*x for k,x in enumerate(pk)),F(0))
    if z==0:
        raise WattsInputError("R119_ZERO_MEAN_DEGREE_BRANCHING_UNDEFINED")
    numerator=sum((k*(k-1)*p*rho[k] for k,p in enumerate(pk)),F(0))
    ratio=numerator/z
    regime="SUPERCRITICAL" if ratio>1 else "SUBCRITICAL" if ratio<1 else "CRITICAL_BOUNDARY"
    return {"z":z,"branching_ratio":ratio,"regime":regime}


def frozen_network_counterexamples():
    h=F(1,2)
    path=tuple((i,i+1) for i in range(5))
    star=tuple((0,i) for i in range(1,6))
    cycle=path+((5,0),)
    triangles=((0,1),(1,2),(0,2),(3,4),(4,5),(3,5))
    diamond=((0,1),(0,2),(1,3),(2,3))
    configs={
        "path_seed_endpoint":(6,path,(h,)*6,0),
        "star_seed_leaf":(6,star,(h,)*6,1),
        "star_seed_center":(6,star,(h,)*6,0),
        "cycle_seed_0":(6,cycle,(h,)*6,0),
        "two_triangles_seed_0":(6,triangles,(h,)*6,0),
        "diamond_late_stable":(4,diamond,(h,h,h,F(3,4)),0),
    }
    sizes={k:validate_final_closure(*v)["size"] for k,v in configs.items()}
    degrees={k:degree_profile(*v)[0] for k,v in configs.items()}
    return {
        "final_sizes":sizes,
        "degree_sequences":{k:list(v) for k,v in degrees.items()},
        "cycle_and_triangles_same_degree_multiset":sorted(degrees["cycle_seed_0"])==sorted(degrees["two_triangles_seed_0"]),
        "path_and_star_same_edge_count":len(path)==len(star),
        "diamond_node_3_not_one_neighbor_vulnerable":not degree_profile(*configs["diamond_late_stable"])[1][3],
        "finite_graph_not_random_ER_phase_diagram":True,
    }


def exhaustive_tiny_graphs(max_n=4):
    """All undirected labeled n-node simple graphs x 3^n thresholds x n seeds.

    Sum n=1..4: 3 + 36 + 648 + 20736 = 21423 synthetic examples.
    """
    if type(max_n) is not int or not 1<=max_n<=4:
        raise WattsInputError("R119_TINY_EXHAUSTIVE_MAX_N_1_TO_4")
    palette=(F(1,3),F(1,2),F(2,3))
    counts={}
    for n in range(1,max_n+1):
        pairs=tuple(combinations(range(n),2))
        verified=0
        for graph_mask in range(1 << len(pairs)):
            edges=tuple(pair for i,pair in enumerate(pairs) if (graph_mask>>i)&1)
            for thresholds in product(palette,repeat=n):
                for seed in range(n):
                    validate_final_closure(n,edges,thresholds,seed)
                    verified+=1
        if verified != (1<<len(pairs))*(len(palette)**n)*n:
            raise WattsInputError("R119_EXHAUSTIVE_COUNT_MISMATCH")
        counts[str(n)]=verified
    return counts


def study_receipt():
    result=frozen_network_counterexamples()
    return {
        "research_id":"R119","phase":"A","catalogue_id":"04-002",
        "source_DOI":"10.1073/pnas.082090499",
        "model":"finite_static_fractional_neighbor_threshold_no_withdrawal",
        "first_party_graph_examples":result,
        "branching_eq5_cases":{
            "degree3_all_vulnerable":str(branching_ratio([F(0)]*3+[F(1)],[F(0)]*3+[F(1)])["branching_ratio"]),
            "degree3_none_vulnerable":str(branching_ratio([F(0)]*3+[F(1)],[F(0)]*4)["branching_ratio"]),
            "degree2_all_vulnerable":str(branching_ratio([F(0),F(0),F(1)],[F(0),F(0),F(1)])["branching_ratio"]),
            "degree1_and_degree3_half_each":str(branching_ratio([F(0),F(1,2),F(0),F(1,2)],[F(0),F(1),F(0),F(1)])["branching_ratio"]),
        },
        "tiny_graph_threshold_seed_configs":exhaustive_tiny_graphs(),
        "original_human_E2_model_scores":0,
        "original_2002_ER_10000_node_phase_diagram_reproduced":False,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }


if __name__=="__main__":
    print(json.dumps(study_receipt(),indent=2,sort_keys=True))
