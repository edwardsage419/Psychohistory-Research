#!/usr/bin/env python3
"""R208 exhaustive five-node graph centrality vs independent live-edge outcomes.

All 2^10 labelled simple undirected graphs, two precommitted live-edge
probabilities 1/4 and 3/4; enumerate 2^m original live-edge events per graph.
Compare four topology-only centrality seed heuristics against exact expected
bond-percolation component size. All quantities are exact Fraction arithmetic.
The 'outcome' is an artificial live-edge ensemble; no new graph, no real data.

python r208_exact_network_centrality.py --test
python r208_exact_network_centrality.py --emit
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import unittest
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

F=Fraction
Z=F(0)
O=F(1)
N=5
ALL_EDGES=tuple(itertools.combinations(range(N),2))
P_VALUES=(F(1,4),F(3,4))
METHODS=("DEGREE","HARMONIC","BETWEENNESS","KATZ")
ALPHA=F(1,8)
HERE=Path(__file__).resolve().parent

def graph_edges(graph_mask):
    if not isinstance(graph_mask,int) or not (0<=graph_mask<1<<len(ALL_EDGES)):
        raise ValueError("graph mask not in frozen 10-bit range")
    return tuple(edge for k,edge in enumerate(ALL_EDGES) if graph_mask & (1<<k))

def adjacency(edges):
    graph=[set() for _ in range(N)]
    for a,b in edges:
        if not (0<=a<N and 0<=b<N and a!=b):
            raise ValueError("invalid simple edge")
        graph[a].add(b)
        graph[b].add(a)
    return tuple(tuple(sorted(nodes)) for nodes in graph)

def distances_from(source,adj):
    d=[-1]*N
    d[source]=0
    queue=[source]
    for i in queue:
        for v in adj[i]:
            if d[v]<0:
                d[v]=d[i]+1
                queue.append(v)
    return tuple(d)

def degree_scores(adj):
    return tuple(F(len(neighbors)) for neighbors in adj)

def harmonic_scores(adj):
    return tuple(sum((F(1,d) for j,d in enumerate(distances_from(i,adj))
                      if j!=i and d>0),Z) for i in range(N))

def all_simple_paths(adj,start,end):
    paths=[]
    def visit(current,path):
        if current==end:
            paths.append(path)
            return
        for nxt in adj[current]:
            if nxt not in path:
                visit(nxt,path+(nxt,))
    visit(start,(start,))
    return tuple(paths)

def betweenness_scores(adj):
    total=[Z]*N
    for start,end in itertools.combinations(range(N),2):
        paths=all_simple_paths(adj,start,end)
        if not paths:
            continue
        min_edges=min(len(path)-1 for path in paths)
        shortest=tuple(path for path in paths if len(path)-1==min_edges)
        n=len(shortest)
        for k in range(N):
            if k in (start,end):
                continue
            passing=sum(k in path[1:-1] for path in shortest)
            total[k]+=F(passing,n)
    return tuple(total)

def inverse_solve_fraction(matrix,b):
    n=len(b)
    if len(matrix)!=n or any(len(row)!=n for row in matrix):
        raise ValueError("square coefficient matrix required")
    work=[[matrix[i][j] for j in range(n)]+[b[i]] for i in range(n)]
    for col in range(n):
        pivot=next((r for r in range(col,n) if work[r][col]!=0),None)
        if pivot is None:
            raise ValueError("singular linear system")
        work[col],work[pivot]=work[pivot],work[col]
        pivot_val=work[col][col]
        work[col]=[v/pivot_val for v in work[col]]
        for i in range(n):
            if i==col:
                continue
            factor=work[i][col]
            work[i]=[work[i][j]-factor*work[col][j] for j in range(n+1)]
    x=tuple(work[i][-1] for i in range(n))
    if any(sum((matrix[i][j]*x[j] for j in range(n)),Z)!=b[i] for i in range(n)):
        raise AssertionError("exact inverse system identity failed")
    return x

def katz_scores(adj):
    m=tuple(tuple(
        (O if i==j else Z)-(ALPHA if j in adj[i] else Z)
        for j in range(N)) for i in range(N))
    out=inverse_solve_fraction(m,(O,)*N)
    if any(out[i]!=O+ALPHA*sum((out[j] for j in adj[i]),Z) for i in range(N)):
        raise AssertionError("Katz exact fixed point identity failed")
    return out

def centrality_scores(edges):
    adj=adjacency(edges)
    return {
        "DEGREE":degree_scores(adj),
        "HARMONIC":harmonic_scores(adj),
        "BETWEENNESS":betweenness_scores(adj),
        "KATZ":katz_scores(adj),
    }

def choose_max_earliest(scores):
    top=max(scores)
    return next(i for i,val in enumerate(scores) if val==top)

def reach_bfs(edges):
    """Independent complete component traversal on each live-edge set."""
    adj=adjacency(edges)
    return tuple(sum(d>=0 for d in distances_from(v,adj)) for v in range(N))

def reach_union_find(edges):
    """Independent DSU algorithm; no adjacency traversal."""
    parent=list(range(N))
    def find(x):
        while parent[x]!=x:
            x=parent[x]
        return x
    for i,j in edges:
        a,b=find(i),find(j)
        if a!=b:
            parent[b]=a
    roots=tuple(find(i) for i in range(N))
    return tuple(sum(roots[i]==roots[j] for j in range(N)) for i in range(N))

def enumerate_live_sources(edges,p):
    if not Z<p<O:
        raise ValueError("probability in (0,1)")
    m=len(edges)
    for live_bits in range(1<<m):
        active=tuple(edge for i,edge in enumerate(edges) if live_bits&(1<<i))
        k=len(active)
        weight=(p**k)*((O-p)**(m-k))
        bfs=reach_bfs(active)
        dsu=reach_union_find(active)
        if bfs!=dsu:
            raise AssertionError("independent exact BFS and DSU disagree")
        yield (live_bits,k,weight,bfs)

def expected_spread_from_live_sources(edges,p,save_raw=False):
    spread=[Z]*N
    mass=Z
    records=[] if save_raw else None
    for bits,k,prob,reachable in enumerate_live_sources(edges,p):
        mass+=prob
        for v in range(N):
            spread[v]+=prob*reachable[v]
        if save_raw:
            records.append((bits,k,prob,reachable))
    if mass!=O:
        raise AssertionError("live-edge original probability mass != 1")
    if any(not (O<=v<=N) for v in spread):
        raise AssertionError("invalid reached population")
    return tuple(spread),records

def max_seed_spread_stats(graph_mask,p,raw_writer=None):
    edges=graph_edges(graph_mask)
    scores=centrality_scores(edges)
    seeds={method:choose_max_earliest(scores[method]) for method in METHODS}
    spreads,raw=expected_spread_from_live_sources(edges,p,save_raw=raw_writer is not None)
    opt=max(spreads)
    oracle=choose_max_earliest(spreads)
    fixed_node0=spreads[0]
    random_node=sum(spreads,Z)/N
    regrets={k:opt-spreads[seeds[k]] for k in METHODS}
    if any(v<0 for v in regrets.values()):
        raise AssertionError("oracle was beaten")
    if raw_writer:
        for bits,k,prob,reach in raw:
            raw_writer.writerow({
                "graph_mask":graph_mask,
                "original_graph_edges":"|".join(f"{i}{j}" for i,j in edges),
                "original_graph_edge_count":len(edges),
                "fixed_bond_probability":str(p),
                "active_original_graph_edge_bitmask":bits,
                "live_edges":k,
                "original_live_source_probability":str(prob),
                "true_actual_five_seed_reach_counts":"|".join(map(str,reach)),
            })
    row={
        "graph_mask":graph_mask,
        "graph_edges":"|".join(f"{i}{j}" for i,j in edges),
        "edge_count":len(edges),
        "p":str(p),
        "full_original_live_source_count":1<<len(edges),
        "original_live_probability_sum":"1",
        "five_exact_expected_reach":[str(v) for v in spreads],
        "true_informed_oracle_best_seed":oracle,
        "true_informed_oracle_expected_reach_exact":str(opt),
        "fixed_seed0_expected_reach_exact":str(fixed_node0),
        "uniform_random_seed_expected_reach_exact":str(random_node),
    }
    for method in METHODS:
        row[method+"_selected_seed"]=seeds[method]
        row[method+"_centrality_five_exact_scores"]=[str(v) for v in scores[method]]
        row[method+"_actual_expected_reach_exact"]=str(spreads[seeds[method]])
        row[method+"_oracle_regret_exact"]=str(regrets[method])
        row[method+"_true_optimal_seed_tie_allowed"]=int(regrets[method]==Z)
    return row

def compute(raw_csv_path=None):
    all_worlds=[]
    by_group=defaultdict(list)
    if raw_csv_path:
        f=open(raw_csv_path,"w",newline="",encoding="utf-8")
        writer=csv.DictWriter(f,fieldnames=[
            "graph_mask","original_graph_edges","original_graph_edge_count",
            "fixed_bond_probability","active_original_graph_edge_bitmask",
            "live_edges","original_live_source_probability","true_actual_five_seed_reach_counts"])
        writer.writeheader()
    else:
        f=None
        writer=None
    try:
        for mask in range(1<<len(ALL_EDGES)):
            for p in P_VALUES:
                outcome=max_seed_spread_stats(mask,p,raw_writer=writer)
                all_worlds.append(outcome)
                by_group[(str(p),len(graph_edges(mask)))].append(outcome)
    finally:
        if f:
            f.close()
    if len(all_worlds)!=2048:
        raise AssertionError("not all 1024 graphs under two probabilities")
    source_count=sum(w["full_original_live_source_count"] for w in all_worlds)
    if source_count!=118098:
        raise AssertionError("not all 118098 exact live-edge source records")
    p_summaries={}
    edge_strata=[]
    for p in P_VALUES:
        worlds=[w for w in all_worlds if w["p"]==str(p)]
        p_result={"graphs":len(worlds)}
        p_result["oracle_expected_reach"]=str(sum(
            (F(w["true_informed_oracle_expected_reach_exact"]) for w in worlds),Z)/len(worlds))
        p_result["fixed_seed0_expected_reach"]=str(sum(
            (F(w["fixed_seed0_expected_reach_exact"]) for w in worlds),Z)/len(worlds))
        p_result["uniform_random_seed_expected_reach"]=str(sum(
            (F(w["uniform_random_seed_expected_reach_exact"]) for w in worlds),Z)/len(worlds))
        for method in METHODS:
            p_result[method+"_expected_oracle_regret"]=str(
                sum((F(w[method+"_oracle_regret_exact"]) for w in worlds),Z)/len(worlds))
            p_result[method+"_optimal_seed_probability"]=str(
                F(sum(w[method+"_true_optimal_seed_tie_allowed"] for w in worlds),len(worlds)))
        p_summaries[str(p)]=p_result
        for edge_count in range(11):
            sub=by_group[(str(p),edge_count)]
            if len(sub)!=len(tuple(itertools.combinations(ALL_EDGES,edge_count))):
                raise AssertionError("binomial graph counts per edge count mismatch")
            info={"p":str(p),"edge_count":edge_count,"graphs":len(sub)}
            for method in METHODS:
                info[method+"_average_regret"]=str(sum(
                    (F(w[method+"_oracle_regret_exact"]) for w in sub),Z)/len(sub))
            edge_strata.append(info)
    different=[]
    wrong=[]
    for w in all_worlds:
        method_seeds={k:w[k+"_selected_seed"] for k in METHODS}
        if len(set(method_seeds.values()))>1:
            different.append({
                "graph_mask":w["graph_mask"],"edges":w["graph_edges"],
                "p":w["p"],"seed_choices":method_seeds,
                "exact_true_five_node_spread":w["five_exact_expected_reach"],
                "oracle_node":w["true_informed_oracle_best_seed"],
            })
        if any(F(w[k+"_oracle_regret_exact"])>0 for k in METHODS):
            wrong.append(w["graph_mask"])
    summary={
        "research_id":"R208",
        "status":"ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "all_labeled_undirected_graphs":1024,
        "graph_p_worlds":2048,
        "all_original_live_edge_source_records":source_count,
        "original_graph_edges_possible":10,
        "graph_nodes":N,
        "two_fixed_bond_probabilities":[str(p) for p in P_VALUES],
        "four_precommitted_structural_centralities":list(METHODS),
        "per_probability_source_complete":p_summaries,
        "per_graph_edge_count_comparison":edge_strata,
        "source_graphs_with_any_distinct_centrality_seed_choices":len(set(d["graph_mask"] for d in different)),
        "graph_p_worlds_with_different_center_selections":len(different),
        "graph_p_worlds_with_any_method_regret_positive":len(wrong),
        "first_12_disagreement_examples_in_canonical_order":different[:12],
        "new_real_human_E2":0,
        "new_real_historical_E3":0,
        "limits":[
            "Exactly 5 labeled undirected nodes, all 1024 graphs are designed artificial conditions",
            "Independent Bernoulli bond-percolation edges, not human behavioral transmission",
            "No unseen graph heldout or real event out-of-sample performance",
            "No empirical inferential population from the artificial graph ensemble",
            "Four centrality methods have no access to true randomized live-edge outcomes",
        ],
    }
    return summary,all_worlds

def emit():
    raw_path=HERE/"R208_ALL_118098_ORIGINAL_BOND_ACTIVATION_SOURCES.csv"
    r,rows=compute(raw_path)
    result_path=HERE/"R208_EXACT_RESULTS.json"
    graph_path=HERE/"R208_ALL_2048_GRAPH_P_SEED_RANKING_WORLDS.csv"
    result_path.write_text(json.dumps(r,indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8")
    graph_records=[]
    for w in rows:
        row={k:("|".join(map(str,v)) if isinstance(v,list) else v)
             for k,v in w.items()}
        graph_records.append(row)
    with graph_path.open("w",newline="",encoding="utf-8") as f:
        writer=csv.DictWriter(f,fieldnames=list(graph_records[0]))
        writer.writeheader()
        writer.writerows(graph_records)
    a={
        "model_id":"R208",
        "graphs":1024,
        "graph_p_worlds":2048,
        "raw_original_live_sources":118098,
        "independent_BFS_and_DSU_all_reaches_agree":True,
        "Katz_exact_linear_system_identity":True,
        "original_probabilities_every_graph_world_sum_one":True,
        "new_E2":0,
        "new_E3":0,
        "result_sha256":hashlib.sha256(result_path.read_bytes()).hexdigest(),
        "graph_worlds_sha256":hashlib.sha256(graph_path.read_bytes()).hexdigest(),
        "raw_live_sources_sha256":hashlib.sha256(raw_path.read_bytes()).hexdigest(),
    }
    (HERE/"R208_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(a,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(a,indent=2))

class Tests(unittest.TestCase):
    def test_five_nodes(self):
        self.assertEqual(N,5)
    def test_edges_ten(self):
        self.assertEqual(len(ALL_EDGES),10)
    def test_all_graphs(self):
        self.assertEqual(1<<len(ALL_EDGES),1024)
    def test_fixed_bond_probability(self):
        self.assertEqual(P_VALUES,(F(1,4),F(3,4)))
    def test_fixed_methods(self):
        self.assertEqual(len(METHODS),4)
    def test_full_raw_source_formula(self):
        self.assertEqual(2*sum(2**len(graph_edges(m)) for m in range(1024)),118098)
    def test_empty_graph_mask(self):
        self.assertEqual(graph_edges(0),())
    def test_complete_graph_mask(self):
        self.assertEqual(len(graph_edges(1023)),10)
    def test_mask_1_first_edge(self):
        self.assertEqual(graph_edges(1),((0,1),))
    def test_adjacency_symmetry(self):
        for mask in (0,1,44,712,1023):
            adj=adjacency(graph_edges(mask))
            self.assertTrue(all((v in adj[i])==(i in adj[v]) for i in range(N) for v in range(N)))
    def test_adjacency_degree_sum(self):
        for mask in (0,1,44,712,1023):
            self.assertEqual(sum(map(len,adjacency(graph_edges(mask)))),2*len(graph_edges(mask)))
    def test_empty_graph_degree_zero(self):
        self.assertEqual(degree_scores(adjacency(())),(Z,)*N)
    def test_complete_graph_degree_four(self):
        self.assertEqual(degree_scores(adjacency(ALL_EDGES)),(F(4),)*N)
    def test_empty_graph_harmonic_zero(self):
        self.assertEqual(harmonic_scores(adjacency(())),(Z,)*N)
    def test_empty_graph_between_zero(self):
        self.assertEqual(betweenness_scores(adjacency(())),(Z,)*N)
    def test_empty_graph_katz_one(self):
        self.assertEqual(katz_scores(adjacency(())),(O,)*N)
    def test_katz_exact_fixed_point_path(self):
        adj=adjacency(((0,1),(1,2),(2,3),(3,4)))
        x=katz_scores(adj)
        self.assertTrue(all(x[i]==O+ALPHA*sum((x[j] for j in adj[i]),Z) for i in range(N)))
    def test_degree_path_center(self):
        self.assertEqual(choose_max_earliest(degree_scores(adjacency(
            ((0,1),(1,2),(2,3),(3,4))))),1)
    def test_harmonic_path_center(self):
        self.assertEqual(choose_max_earliest(harmonic_scores(adjacency(
            ((0,1),(1,2),(2,3),(3,4))))),2)
    def test_between_path_center_score(self):
        x=betweenness_scores(adjacency(((0,1),(1,2),(2,3),(3,4))))
        self.assertEqual(x[2],F(4))
    def test_between_triangle_zero(self):
        adj=adjacency(((0,1),(1,2),(0,2)))
        self.assertEqual(betweenness_scores(adj),(Z,)*N)
    def test_between_star_four_pairs_six(self):
        x=betweenness_scores(adjacency(((0,1),(0,2),(0,3),(0,4))))
        self.assertEqual(x[0],F(6))
    def test_shortest_paths_simple(self):
        adj=adjacency(((0,1),(1,2),(0,2)))
        self.assertIn((0,2),all_simple_paths(adj,0,2))
    def test_distance_unreachable_is_negative_one(self):
        x=distances_from(0,adjacency(((0,1),)))
        self.assertEqual(x,(0,1,-1,-1,-1))
    def test_live_bfs_union_forest(self):
        for edges in ((),((0,1),),((0,1),(1,2),(3,4)),ALL_EDGES):
            self.assertEqual(reach_bfs(edges),reach_union_find(edges))
    def test_single_live_edge_spread(self):
        self.assertEqual(reach_bfs(((0,1),)),(2,2,1,1,1))
    def test_all_edges_live_reach_five(self):
        self.assertEqual(reach_bfs(ALL_EDGES),(5,)*N)
    def test_empty_graph_expected_reach_one(self):
        for p in P_VALUES:
            self.assertEqual(expected_spread_from_live_sources((),p)[0],(O,)*N)
    def test_one_edge_expected_reach(self):
        for p in P_VALUES:
            out,_=expected_spread_from_live_sources(((0,1),),p)
            self.assertEqual(out,(O+p,O+p,O,O,O))
    def test_live_probabilities_sum_one(self):
        for mask in (0,1,17,255,1023):
            for p in P_VALUES:
                self.assertEqual(sum((w for _,_,w,_ in enumerate_live_sources(graph_edges(mask),p)),Z),O)
    def test_prob_low_high_monotone(self):
        edges=((0,1),(1,2),(2,3),(3,4))
        a,_=expected_spread_from_live_sources(edges,F(1,4))
        b,_=expected_spread_from_live_sources(edges,F(3,4))
        self.assertTrue(all(a[i]<=b[i] for i in range(N)))
    def test_katz_matrix_solver_small(self):
        self.assertEqual(inverse_solve_fraction(((F(2),F(0)),(F(0),F(3))), (F(4),F(6))),
                         (F(2),F(2)))
    def test_method_tie_smallest(self):
        self.assertEqual(choose_max_earliest((O,O,O,Z,Z)),0)
    def test_seed_oracle_regret_nonnegative(self):
        for graphmask in (0,1,55,301,1023):
            for p in P_VALUES:
                w=max_seed_spread_stats(graphmask,p)
                for method in METHODS:
                    self.assertGreaterEqual(F(w[method+"_oracle_regret_exact"]),Z)
    def test_complete_graph_all_methods_optimal(self):
        w=max_seed_spread_stats(1023,F(1,4))
        self.assertTrue(all(F(w[method+"_oracle_regret_exact"])==0 for method in METHODS))
    def test_empty_graph_all_methods_optimal(self):
        w=max_seed_spread_stats(0,F(3,4))
        self.assertTrue(all(F(w[method+"_oracle_regret_exact"])==0 for method in METHODS))
    def test_method_reproducibility(self):
        a=centrality_scores(graph_edges(199))
        b=centrality_scores(graph_edges(199))
        self.assertEqual(a,b)
    def test_bad_graph_mask_rejected(self):
        with self.assertRaises(ValueError):
            graph_edges(1024)
    def test_bad_probability_rejected(self):
        with self.assertRaises(ValueError):
            tuple(enumerate_live_sources(((0,1),),F(1)))
    def test_singular_solver_rejected(self):
        with self.assertRaises(ValueError):
            inverse_solve_fraction(((Z,Z),(Z,Z)),(O,O))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true")
    p.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:
        ok=unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if ok.wasSuccessful() else 1)
    if a.emit:
        emit()
    if not a.test and not a.emit:
        p.print_help()
