#!/usr/bin/env python3
"""R125 source-grounded exact finite random graphs, NOT human social networks.

Original 1959 Erdős & Rényi, On Random Graphs I, Publ Math Debrecen 6:290-297:
uniform among exactly C(n,2)-candidate-edge graphs with m chosen links.
Original 1959 E N Gilbert, Random Graphs, Ann Math Stat 30:1141-1144:
all candidate undirected edges independent Bernoulli(p), Eq(4) connectivity.
No estimated empirical person level networks, forecasts, or giant-component
asymptotic theorem reproducibility is claimed.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from math import comb
import json


class RandomGraphAuditError(ValueError):
    pass


def _n(n):
    if type(n) is not int or not 1 <= n <= 5:
        raise RandomGraphAuditError("R125_N_INTEGER_1_TO_5")
    return n


def _p(p):
    if type(p) is not F or not F(0)<=p<=F(1):
        raise RandomGraphAuditError("R125_PROBABILITY_EXACT_FRACTION_0_TO_1")
    return p


def _m(n,m):
    n=_n(n)
    k=n*(n-1)//2
    if type(m) is not int or not 0<=m<=k:
        raise RandomGraphAuditError("R125_M_INTEGER_WITHIN_EDGE_SUPPORT")
    return m


def candidate_edges(n):
    _n(n)
    return tuple(combinations(range(n),2))


def validate_edges(n, edges):
    n=_n(n)
    if type(edges) not in (tuple,list):
        raise RandomGraphAuditError("R125_EXPLICIT_EDGE_CONTAINER")
    seen=set()
    for e in edges:
        if type(e) not in (tuple,list) or len(e)!=2:
            raise RandomGraphAuditError("R125_EDGE_UNDIRECTED_PAIR")
        u,v=e
        if type(u) is not int or type(v) is not int or not (0<=u<n and 0<=v<n):
            raise RandomGraphAuditError("R125_EDGE_ENDPOINT_INVALID")
        if u==v:
            raise RandomGraphAuditError("R125_NO_SELF_LOOPS")
        pair=(min(u,v),max(u,v))
        if pair in seen:
            raise RandomGraphAuditError("R125_DUPLICATE_UNDIRECTED_EDGE")
        seen.add(pair)
    return tuple(sorted(seen))


def components(n,edges):
    """Independent DFS connected components, including zero degree vertices."""
    n=_n(n)
    links=validate_edges(n,edges)
    graph=[set() for _ in range(n)]
    for u,v in links:
        graph[u].add(v)
        graph[v].add(u)
    remain=set(range(n))
    out=[]
    while remain:
        start=min(remain)
        stack=[start]
        seen={start}
        remain.remove(start)
        while stack:
            u=stack.pop()
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    remain.remove(v)
                    stack.append(v)
        out.append(frozenset(seen))
    return tuple(out)


def graph_properties(n,edges):
    _n(n)
    links=validate_edges(n,edges)
    comps=components(n,links)
    degree=[0]*n
    for u,v in links:
        degree[u]+=1;degree[v]+=1
    return {
        "edges":len(links),
        "connected":len(comps)==1,
        "largest_component":max(map(len,comps)),
        "component_count":len(comps),
        "isolates":sum(k==0 for k in degree),
        "degree_of_node_zero":degree[0],
    }


def all_labeled_graphs(n):
    n=_n(n)
    options=candidate_edges(n)
    for mask in range(1<<len(options)):
        yield tuple(edge for i,edge in enumerate(options) if mask & (1<<i))


def gnm_graph_mass(n,m,edges):
    n=_n(n)
    m=_m(n,m)
    e=validate_edges(n,edges)
    if len(e)!=m:
        return F(0)
    return F(1,comb(n*(n-1)//2,m))


def gnp_graph_mass(n,p,edges):
    n=_n(n)
    p=_p(p)
    e=validate_edges(n,edges)
    k=n*(n-1)//2
    return p**len(e)*(F(1)-p)**(k-len(e))


def gnp_edge_count_mass(n,p,m):
    n=_n(n);p=_p(p);m=_m(n,m)
    k=n*(n-1)//2
    return F(comb(k,m))*p**m*(F(1)-p)**(k-m)


def gnp_conditional_on_edge_count_mass(n,p,m,edges):
    """Exact G(n,p) conditional on edge count m, only if event is possible."""
    n=_n(n);p=_p(p);m=_m(n,m)
    e=validate_edges(n,edges)
    event=gnp_edge_count_mass(n,p,m)
    if event==0:
        raise RandomGraphAuditError("R125_CONDITION_ON_ZERO_PROBABILITY_EVENT_UNDEFINED")
    return gnp_graph_mass(n,p,e)/event if len(e)==m else F(0)


def gnp_degree_zero_mass(n,p,j):
    """Node 0 degree j has Bin(n-1,p)."""
    n=_n(n);p=_p(p)
    if type(j) is not int or not 0<=j<n:
        raise RandomGraphAuditError("R125_DEGREE_J_INVALID")
    return F(comb(n-1,j))*p**j*(F(1)-p)**(n-1-j)


def gnm_degree_zero_mass(n,m,j):
    """Hypergeometric: among K candidate edges, n-1 incident to node 0."""
    n=_n(n);m=_m(n,m)
    if type(j) is not int or not 0<=j<n:
        raise RandomGraphAuditError("R125_DEGREE_J_INVALID")
    k=n*(n-1)//2
    non_incident=k-(n-1)
    if j>m or m-j>non_incident:
        return F(0)
    return F(comb(n-1,j)*comb(non_incident,m-j),comb(k,m))


def gnp_expected_isolates(n,p):
    n=_n(n);p=_p(p)
    return n*(F(1)-p)**(n-1)


def gnp_edge_count_moments(n,p):
    n=_n(n);p=_p(p)
    k=n*(n-1)//2
    return {"mean":F(k)*p,"variance":F(k)*p*(F(1)-p)}


def gnm_edge_count_moments(n,m):
    n=_n(n);m=_m(n,m)
    return {"mean":F(m),"variance":F(0)}


def independent_gilbert1959_connected_recurrence(n,p):
    """Original Gilbert 1959 printed p1142 Eq(4): no graph enumeration.

    1-P_n = sum_{k=1}^{n-1} C(n-1,k-1) P_k q^{k(n-k)}.
    The fixed vertex 0 lies in a connected component of size k.
    """
    n=_n(n);p=_p(p)
    q=F(1)-p
    pn={1:F(1)}
    for size in range(2,n+1):
        disconnected=sum((F(comb(size-1,k-1))*pn[k]*q**(k*(size-k))
                          for k in range(1,size)),F(0))
        pn[size]=F(1)-disconnected
        if not F(0)<=pn[size]<=F(1):
            raise RandomGraphAuditError("R125_ORIGINAL_GILBERT_EQ4_OUT_OF_PROBABILITY_RANGE")
    return pn[n]


def full_exact_gnp_graph_distribution(n,p):
    """Enumerate *every* labeled undirected graph and its whole graph statistics."""
    n=_n(n);p=_p(p)
    connect=F(0)
    expect_isolates=F(0)
    deg=Counter()
    largest=Counter()
    edge_count=Counter()
    total=F(0)
    graph_count=0
    for edges in all_labeled_graphs(n):
        prob=gnp_graph_mass(n,p,edges)
        props=graph_properties(n,edges)
        total+=prob
        if props["connected"]:
            connect+=prob
        expect_isolates+=prob*props["isolates"]
        deg[props["degree_of_node_zero"]]+=prob
        largest[props["largest_component"]]+=prob
        edge_count[props["edges"]]+=prob
        graph_count+=1
    if total!=1 or graph_count!=(1<<(n*(n-1)//2)):
        raise RandomGraphAuditError("R125_GNP_ENUMERATION_NORMALIZATION_FAILED")
    if connect!=independent_gilbert1959_connected_recurrence(n,p):
        raise RandomGraphAuditError("R125_GILBERT_ORIGINAL_EQ4_VS_ENUMERATION_DIVERGED")
    if expect_isolates!=gnp_expected_isolates(n,p):
        raise RandomGraphAuditError("R125_ISOLATES_EXPECTATION_VS_COMBINATORICS_DIVERGED")
    if any(deg[j]!=gnp_degree_zero_mass(n,p,j) for j in range(n)):
        raise RandomGraphAuditError("R125_BINOMIAL_DEGREE_LAW_VS_ENUMERATION_DIVERGED")
    if any(edge_count[m]!=gnp_edge_count_mass(n,p,m) for m in range(n*(n-1)//2+1)):
        raise RandomGraphAuditError("R125_GNP_EDGE_COUNT_BINOMIAL_DIVERGED")
    if sum(largest.values(),F(0))!=1:
        raise RandomGraphAuditError("R125_LARGEST_COMPONENT_DIST_INVALID")
    return {
        "graph_count":graph_count,
        "total_mass":total,"connectivity_probability":connect,
        "expected_isolates":expect_isolates,
        "degree_zero_distribution":dict(sorted(deg.items())),
        "largest_component_distribution":dict(sorted(largest.items())),
        "edge_count_distribution":dict(sorted(edge_count.items())),
    }


def full_exact_gnm_edge_conditioned_distribution(n,m):
    """Enumerate fixed-m graphs with equal exact mass, no replacement."""
    n=_n(n);m=_m(n,m)
    connected=F(0);isolates=F(0);total=F(0);count=0
    largest=Counter()
    deg=Counter()
    for edges in all_labeled_graphs(n):
        if len(edges)!=m:
            continue
        prob=gnm_graph_mass(n,m,edges)
        props=graph_properties(n,edges)
        total+=prob;count+=1
        connected+=prob*int(props["connected"])
        isolates+=prob*props["isolates"]
        deg[props["degree_of_node_zero"]]+=prob
        largest[props["largest_component"]]+=prob
    if total!=1 or count!=comb(n*(n-1)//2,m):
        raise RandomGraphAuditError("R125_GNM_TOTAL_COUNT_OR_MASS_INVALID")
    if any(deg[j]!=gnm_degree_zero_mass(n,m,j) for j in range(n)):
        raise RandomGraphAuditError("R125_GNM_HYPERGEOMETRIC_DEGREE_DIVERGED")
    return {
        "graph_count":count,"total_mass":total,
        "connectivity_probability":connected,"expected_isolates":isolates,
        "degree_zero_distribution":dict(sorted(deg.items())),
        "largest_component_distribution":dict(sorted(largest.items())),
    }


def audit_all_small_graphs():
    """Exact audit: 1099 graphs x four Gnp p, and 25 Gnm(n,m) buckets."""
    probs=(F(0),F(1,3),F(1,2),F(1))
    graph_counts={}
    conditional_buckets={}
    gnp_results={}
    gnm_total_buckets=0
    for n in range(1,6):
        k=n*(n-1)//2
        graph_counts[str(n)]=1<<k
        conditional_buckets[str(n)]=k+1
        for m in range(k+1):
            gnm=full_exact_gnm_edge_conditioned_distribution(n,m)
            gnm_total_buckets+=1
            for p in (F(1,3),F(1,2)):
                if gnp_edge_count_mass(n,p,m)==0:
                    raise RandomGraphAuditError("R125_POSITIVE_P_CONDITION_UNDEFINED")
                for edges in all_labeled_graphs(n):
                    if len(edges)==m and gnp_conditional_on_edge_count_mass(n,p,m,edges)!=gnm_graph_mass(n,m,edges):
                        raise RandomGraphAuditError("R125_CONDITIONAL_GNP_NOT_GNM")
            if gnm["total_mass"]!=1:
                raise RandomGraphAuditError("R125_GNM_BUCKET_FAILURE")
        for p in probs:
            result=full_exact_gnp_graph_distribution(n,p)
            gnp_results[f"{n}:{p}"]={
                "connectivity_probability":str(result["connectivity_probability"]),
                "expected_isolates":str(result["expected_isolates"]),
            }
    if sum(graph_counts.values())!=1099 or gnm_total_buckets!=25:
        raise RandomGraphAuditError("R125_SYNTHETIC_AUDIT_COVERAGE_NOT_1099_25")
    return {
        "enumerated_graphs_by_n":graph_counts,
        "unique_labeled_graphs_total":sum(graph_counts.values()),
        "Gnp_graph_probability_weighings_total":4*sum(graph_counts.values()),
        "Gnm_fixed_m_distribution_buckets_by_n":conditional_buckets,
        "Gnm_distribution_bucket_count":gnm_total_buckets,
        "Gnp_connected_and_isolates_by_n_p":gnp_results,
        "same_exact_distribution_Gnp_conditioned_edge_count_as_Gnm_all_valid_n_m":True,
        "1960_asymptotic_giant_component_theorem_is_not_claimed_as_finite_graph_result":True,
        "real_person_observations":0,
    }


def frozen_four_vertex_comparison():
    n=4;k=6;p=F(1,2);m=3
    fixed=full_exact_gnm_edge_conditioned_distribution(n,m)
    independent=full_exact_gnp_graph_distribution(n,p)
    return {
        "n":n,"available_edges":k,
        "fixed_m":m,"independent_p":str(p),
        "Gnm_m3_number_of_possible_graphs":fixed["graph_count"],
        "Gnm_m3_connected_graphs":fixed["connectivity_probability"]*fixed["graph_count"],
        "Gnm_m3_connectivity":str(fixed["connectivity_probability"]),
        "Gnp_p_half_connected_graphs":independent["connectivity_probability"]*64,
        "Gnp_p_half_connectivity":str(independent["connectivity_probability"]),
        "Gnp_p_half_exactly_3_edges_mass":str(gnp_edge_count_mass(n,p,3)),
        "Gnp_conditional_specific_three_edge_graph_mass":str(F(1,20)),
        "Gnm_expected_isolates":str(fixed["expected_isolates"]),
        "Gnp_expected_isolates":str(independent["expected_isolates"]),
        "Gnm_edge_number_variance":str(gnm_edge_count_moments(n,m)["variance"]),
        "Gnp_edge_number_variance":str(gnp_edge_count_moments(n,p)["variance"]),
        "source_Gilbert1959_eq4_recursion_checked":True,
        "source_ErdosRenyi1959_fixed_m_definition_checked":True,
    }


def stage_receipt():
    return {
        "research_id":"R125","catalogue_id":"04-018",
        "ER1959_original_fixed_m_primary":"https://www.cse.cuhk.edu.hk/~cslui/CMSC5734/erdos-1959-11.pdf",
        "Gilbert1959_original_independent_p_DOI":"10.1214/aoms/1177706098",
        "ER1960_critical_giant_asymptotic_not_empirically_reproduced":True,
        "finite_graph_conditional_and_unconditional_counterexample":frozen_four_vertex_comparison(),
        "exhaustive_exact_small_graph_verification":audit_all_small_graphs(),
        "new_real_human_E2_prediction_scores":0,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN"
    }


if __name__=="__main__":
    print(json.dumps(stage_receipt(),indent=2,sort_keys=True))
