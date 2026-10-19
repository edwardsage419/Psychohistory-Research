#!/usr/bin/env python3
"""R124: categorical homophily, finite opportunity baselines & identification.

Primary sources:
- McPherson et al. (2001), ARS 27:415-444 (esp p419 baseline vs inbreeding).
- Newman (2003), PRE 67:026126 (p026126-2 Eq2 assortative mixing).
- Kossinets and Watts (2009), AJS 115:405-450 (public ORIGINAL abstract ONLY).
All networks and longitudinal histories below are project-created mathematics,
not original human network data, observational inference, or a causal fit.
"""
from __future__ import annotations

from collections import Counter
from fractions import Fraction as F
from itertools import combinations, product
from math import comb
import json


class HomophilyAuditError(ValueError):
    """Strict category, graph, and finite-null domain violation."""


def graph(n, categories, edges, require_edge=True):
    if type(n) is not int or not 2 <= n <= 8:
        raise HomophilyAuditError("R124_N_STRICT_INT_2_TO_8")
    if type(categories) not in (tuple,list) or len(categories)!=n:
        raise HomophilyAuditError("R124_CATEGORY_VECTOR_LENGTH")
    if any(type(v) is not str or v not in ("A","B") for v in categories):
        raise HomophilyAuditError("R124_ONLY_EXPLICIT_BINARY_CATEGORIES_A_B")
    labels=tuple(categories)
    if set(labels)!={"A","B"}:
        raise HomophilyAuditError("R124_BOTH_LABEL_CATEGORIES_REQUIRED")
    if type(edges) not in (tuple,list):
        raise HomophilyAuditError("R124_EXPLICIT_EDGE_TUPLE_OR_LIST")
    seen=set()
    for edge in edges:
        if type(edge) not in (tuple,list) or len(edge)!=2:
            raise HomophilyAuditError("R124_UNDIRECTED_TWO_NODE_EDGE_REQUIRED")
        u,v=edge
        if type(u) is not int or type(v) is not int or not 0<=u<n or not 0<=v<n:
            raise HomophilyAuditError("R124_NODE_ENDPOINT_INVALID")
        if u==v:
            raise HomophilyAuditError("R124_NO_SELF_LOOP")
        pair=(min(u,v),max(u,v))
        if pair in seen:
            raise HomophilyAuditError("R124_DUPLICATE_UNDIRECTED_EDGE")
        seen.add(pair)
    if require_edge and not seen:
        raise HomophilyAuditError("R124_NONEMPTY_EDGES_REQUIRED_FOR_ASSORTATIVITY")
    return labels,tuple(sorted(seen))


def newman_mixing_direct(n,categories,edges):
    """Newman Eq(1),(2): EACH edge contributes two directed half-edges.

    Diagonal e_ii gets 2 counts for same-type edge. Off-diagonal each
    directed ordered A->B and B->A gets one. Divisor = 2*m.
    """
    labels, e=graph(n,categories,edges)
    counts=[[0,0],[0,0]]
    ind={"A":0,"B":1}
    for u,v in e:
        a,b=ind[labels[u]],ind[labels[v]]
        counts[a][b]+=1
        counts[b][a]+=1
    m=len(e)
    mix=tuple(tuple(F(x,2*m) for x in row) for row in counts)
    marg=tuple(sum(row,F(0)) for row in mix)
    trace=mix[0][0]+mix[1][1]
    base=sum((x*x for x in marg),F(0))
    denominator=1-base
    r=None if denominator==0 else (trace-base)/denominator
    if sum((sum(row,F(0)) for row in mix),F(0))!=1:
        raise HomophilyAuditError("R124_NEWMan_E_MATRIX_NOT_NORMALIZED")
    return {
        "edges":m,"same_edge_fraction":trace,"endpoint_marginals":marg,
        "mixing_matrix":mix,"stub_independence_baseline":base,
        "assortativity":r,
        "undefined_reason":"ONLY_ONE_CATEGORY_AT_ALL_EDGE_ENDPOINTS" if r is None else None,
    }


def independent_stub_arithmetic(n,categories,edges):
    """Second independent edge/stub tally; DOES NOT call mixing matrix code."""
    labels, e=graph(n,categories,edges)
    same=sum(labels[u]==labels[v] for u,v in e)
    deg=[0]*n
    for u,v in e:
        deg[u]+=1
        deg[v]+=1
    m=len(e)
    da=sum(deg[i] for i in range(n) if labels[i]=="A")
    db=sum(deg[i] for i in range(n) if labels[i]=="B")
    a=F(da,2*m)
    b=F(db,2*m)
    expected=a*a+b*b
    observed=F(same,m)
    r=None if expected==1 else (observed-expected)/(1-expected)
    return {
        "edges":m,"same_edge_count":same,"same_edge_fraction":observed,
        "endpoint_marginals":(a,b),"stub_independence_baseline":expected,
        "assortativity":r,
        "undefined_reason":"ONLY_ONE_CATEGORY_AT_ALL_EDGE_ENDPOINTS" if r is None else None,
    }


def verify_independent_mixing(n,categories,edges):
    x=newman_mixing_direct(n,categories,edges)
    y=independent_stub_arithmetic(n,categories,edges)
    for key in ("edges","same_edge_fraction","endpoint_marginals",
                "stub_independence_baseline","assortativity","undefined_reason"):
        if x[key]!=y[key]:
            raise HomophilyAuditError("R124_TWO_INDEPENDENT_MIXING_METHODS_DIVERGED_"+key)
    return x


def population_without_replacement_baseline(categories):
    """Random unordered DISTINCT population pair under full exposure.

    NOT the independent edge-STUB assortativity r null of Newman!
    """
    if type(categories) not in (tuple,list) or len(categories)<2:
        raise HomophilyAuditError("R124_EXPLICIT_POPULATION_REQUIRED")
    if any(type(v) is not str or v not in ("A","B") for v in categories):
        raise HomophilyAuditError("R124_BAD_POPULATION_LABELS")
    n=len(categories)
    a=sum(x=="A" for x in categories)
    b=n-a
    if a==0 or b==0:
        raise HomophilyAuditError("R124_TWO_POPULATION_CATEGORIES_REQUIRED")
    return F(a*(a-1)+b*(b-1),n*(n-1))


def exact_uniform_label_permutation_null(n,categories,edges):
    """Fix graph and binary group sizes, uniformly permute CATEGORY POSITIONS.

    Probability is purely mathematical, conditional on exchangeable labels;
    no real-world exchangeability, randomization, or causal identification is
    established. Deterministic frequencies in all C(n,n_A) placements.
    """
    labels,e=graph(n,categories,edges)
    na=labels.count("A")
    frequencies=Counter()
    for a_indices in combinations(range(n),na):
        group_a=set(a_indices)
        same=sum((u in group_a)==(v in group_a) for u,v in e)
        frequencies[same]+=1
    cases=comb(n,na)
    if sum(frequencies.values())!=cases:
        raise HomophilyAuditError("R124_CATEGORY_PERMUTATION_COUNT_INVALID")
    direct_expected=sum((F(same*count,cases) for same,count in frequencies.items()),F(0))
    analytic_expected=len(e)*population_without_replacement_baseline(labels)
    if direct_expected!=analytic_expected:
        raise HomophilyAuditError("R124_FINITE_EXACT_NULL_MEAN_DISAGREES_WITH_PAIR_BASELINE")
    current_same=sum(labels[u]==labels[v] for u,v in e)
    right_tail=F(sum(freq for same,freq in frequencies.items() if same>=current_same),cases)
    return {
        "permutations":cases,
        "same_edge_count_frequencies":dict(sorted(frequencies.items())),
        "observed_same_edges":current_same,
        "expected_same_edges":analytic_expected,
        "baseline_fraction_same":population_without_replacement_baseline(labels),
        "right_tail_probability_under_exchangeable_label_null":right_tail,
        "this_is_NOT_an_empirical_p_value":True,
    }


def fixed_opportunity_baseline(n,categories,edges,eligible_pairs):
    """Measure exposure-restricted excess, not preference or causal selection."""
    labels,observed=graph(n,categories,edges)
    _,eligible=graph(n,categories,eligible_pairs)
    if not set(observed)<=set(eligible):
        raise HomophilyAuditError("R124_OBSERVED_EDGE_OUTSIDE_PERMITTED_OPPORTUNITY")
    p_opp=F(sum(labels[u]==labels[v] for u,v in eligible),len(eligible))
    p_obs=F(sum(labels[u]==labels[v] for u,v in observed),len(observed))
    return {
        "observed_same_fraction":p_obs,
        "opportunity_same_fraction":p_opp,
        "opportunity_excess":p_obs-p_opp,
        "global_population_pair_baseline":population_without_replacement_baseline(labels),
        "global_population_pair_excess":p_obs-population_without_replacement_baseline(labels),
        "eligible_pair_count":len(eligible),"observed_edges":len(observed),
        "opportunity_model_is_assumed_not_inferred":True,
    }


def original_project_frozen_graph_examples():
    labels=("A","A","A","B","B","B")
    triangles=tuple(combinations(range(3),2))+tuple(combinations(range(3,6),2))
    cycle=tuple((i,(i+1)%6) for i in range(6))
    complete_bipartite=tuple((u,v) for u in range(3) for v in range(3,6))
    skewed_labels=("A",)*5+("B",)
    full_six=tuple(combinations(range(6),2))
    base=verify_independent_mixing(6,labels,triangles)
    ring=verify_independent_mixing(6,labels,cycle)
    opposite=verify_independent_mixing(6,labels,complete_bipartite)
    full=verify_independent_mixing(6,skewed_labels,full_six)
    permutation=exact_uniform_label_permutation_null(6,labels,triangles)
    restricted=fixed_opportunity_baseline(6,labels,triangles,triangles)
    unrestricted=fixed_opportunity_baseline(6,labels,triangles,full_six)
    return {
        "triangles_perfect_r":str(base["assortativity"]),
        "triangles_same_fraction":str(base["same_edge_fraction"]),
        "cycle_r":str(ring["assortativity"]),
        "cycle_same_fraction":str(ring["same_edge_fraction"]),
        "K3_3_cross_only_r":str(opposite["assortativity"]),
        "complete_graph_5A_1B_raw_same":str(full["same_edge_fraction"]),
        "complete_graph_5A_1B_population_baseline":str(population_without_replacement_baseline(skewed_labels)),
        "complete_graph_5A_1B_Newman_r":str(full["assortativity"]),
        "two_triangles_exact_permutation_null":{
            k:({str(a):b for a,b in v.items()} if k=="same_edge_count_frequencies"
               else str(v) if type(v) is F else v)
            for k,v in permutation.items()},
        "focal_opportunity_same_fraction":str(restricted["opportunity_same_fraction"]),
        "focal_opportunity_excess":str(restricted["opportunity_excess"]),
        "global_opportunity_excess":str(unrestricted["opportunity_excess"]),
        "no_causal_effect_or_real_people_fitted":True,
    }


def identical_snapshot_three_generating_histories():
    """Three different project CONSTRUCTIONS with identical final observation.

    Selection: labels fixed, global pair pool, choose similar ties.
    Focal opportunity: labels fixed, eligible dyads only inside two cliques.
    Influence: ties fixed initially, initially mixed attributes; one ROUND of
    majority over each node's closed neighborhood (self and clique neighbors).
    This teacher-made majority equation is NOT Kossinets-Watts fitted dynamics.
    """
    ending=("A","A","A","B","B","B")
    links=tuple(combinations((0,1,2),2))+tuple(combinations((3,4,5),2))
    full_opportunities=tuple(combinations(range(6),2))
    chosen_selection=tuple((u,v) for u,v in full_opportunities if ending[u]==ending[v])
    if chosen_selection!=links:
        raise HomophilyAuditError("R124_SELECTION_STORY_UNEXPECTED")
    focus_opportunities=links
    influence_initial=("A","A","B","B","B","A")
    adjacency=[{i} for i in range(6)]
    for u,v in links:
        adjacency[u].add(v);adjacency[v].add(u)
    next_state=[]
    for i,group in enumerate(adjacency):
        a=sum(influence_initial[j]=="A" for j in group)
        b=len(group)-a
        if a==b:
            raise HomophilyAuditError("R124_TOY_INFLUENCE_MAJORITY_TIE")
        next_state.append("A" if a>b else "B")
    influence_final=tuple(next_state)
    if influence_final!=ending:
        raise HomophilyAuditError("R124_INFLUENCE_STORY_FINAL_NOT_IDENTICAL")
    return {
        "final_edge_pairs":[list(p) for p in links],
        "final_attributes":list(ending),
        "selection_story_start_attributes":list(ending),
        "selection_story_eligible_pairs":len(full_opportunities),
        "selection_story_formed_ties":len(chosen_selection),
        "opportunity_story_start_attributes":list(ending),
        "opportunity_story_eligible_pairs":len(focus_opportunities),
        "opportunity_story_formed_ties":len(focus_opportunities),
        "influence_story_initial_attributes":list(influence_initial),
        "influence_story_attributes_after_one_majority_step":list(influence_final),
        "influence_story_edge_changes":0,
        "all_final_snapshots_identical":True,
        "selection_preference_effect_not_identified_from_snapshot":True,
        "causal_history_assumptions_are_project_constructions":True,
    }


def exhaustive_small_binary_network_audit():
    """All undirected labeled simple graphs x BOTH binary category placements.

    n2:2 graphs*2 labels=4
    n3:8 graphs*6 labels=48
    n4:64 graphs*14 labels=896 => 948 attempted. Edgeless instances
    are EXPLICITLY counted as undefined, never silently r=0.
    """
    expected={2:4,3:48,4:896}
    totals={}
    nonempty={}
    denominator_zero={}
    empty={}
    for n in (2,3,4):
        pairs=tuple(combinations(range(n),2))
        counts=0; valid=0; no_edges=0; no_denominator=0
        for edge_bits in range(1<<len(pairs)):
            edges=tuple(pair for i,pair in enumerate(pairs) if edge_bits&(1<<i))
            for labels in product(("A","B"),repeat=n):
                if set(labels)!={"A","B"}:
                    continue
                counts+=1
                if not edges:
                    no_edges+=1
                    continue
                observed=verify_independent_mixing(n,labels,edges)
                if observed["assortativity"] is None:
                    no_denominator+=1
                valid+=1
        if counts!=expected[n]:
            raise HomophilyAuditError("R124_EXHAUSTIVE_SMALL_GRAPH_COVERAGE_FAILED")
        totals[str(n)]=counts
        nonempty[str(n)]=valid
        empty[str(n)]=no_edges
        denominator_zero[str(n)]=no_denominator
    return {
        "total_cases_by_n":totals,
        "nonempty_networks_by_n":nonempty,
        "empty_no_metric_by_n":empty,
        "nonempty_newman_denominator_zero_by_n":denominator_zero,
        "all_graph_label_cases":sum(totals.values()),
        "newman_assortativity_never_silently_imputed_when_undefined":True,
    }


def phase_receipt():
    return {
        "research_id":"R124","catalogue_id":"04-015",
        "original_publications_DOI":[
            "10.1146/annurev.soc.27.1.415",
            "10.1103/PhysRevE.67.026126",
            "10.1086/599247"
        ],
        "empirical_2009_full_text_and_original_network_reanalysis":False,
        "frozen_synthetic_examples":original_project_frozen_graph_examples(),
        "three_distinct_histories_identical_snapshot":identical_snapshot_three_generating_histories(),
        "exhaustive_small_exact_graph_category_audit":exhaustive_small_binary_network_audit(),
        "real_original_person_level_network_rows_loaded":False,
        "human_E2_new_prediction_scores":0,
        "R073":"FROZEN","PESEN_v0_1":"FROZEN",
    }


if __name__=="__main__":
    print(json.dumps(phase_receipt(),sort_keys=True,indent=2))
