#!/usr/bin/env python3
"""R315: exact two-edge Watts-Strogatz clockwise rewiring, finite E1 only."""
from __future__ import annotations
import argparse
import csv
import json
import unittest
from fractions import Fraction
from pathlib import Path

DIR=Path(__file__).resolve().parent
SRC=DIR/"R315_ALL_210_ORIGINAL_REWIRING_ATOMS.csv"
OUT=DIR/"R315_EXACT_180_TWO_EVENT_GRAPH_PATHS.json"
PARAMS=(Fraction(0), Fraction(1,2), Fraction(1))
COLUMNS=("N","p","stage","prior_action","prior_target","active","old_target",
         "action","new_target","edges_before","conditional_probability","edges_after")

def pair(a,b):
    assert a!=b
    return (min(a,b),max(a,b))

def edge_string(edges):
    return ";".join(f"{a}-{b}" for a,b in sorted(edges))

def baseline(n):
    assert n in (8,10)
    return frozenset(pair(i,(i+shift)%n) for i in range(n) for shift in (1,2))

def neighbours(edges,v):
    return {b if a==v else a for a,b in edges if a==v or b==v}

def choices(edges,n,actor,old,p):
    original=pair(actor,old)
    assert original in edges
    candidates=[t for t in range(n) if t!=actor and t not in neighbours(edges,actor)]
    assert candidates
    options=[("keep",-1,Fraction(1)-p,edges)]
    for t in candidates:
        after=frozenset((set(edges)-{original})|{pair(actor,t)})
        assert len(after)==len(edges)
        options.append(("rewire",t,p/len(candidates),after))
    return options

def graph_metrics(edges,n):
    degrees=[len(neighbours(edges,v)) for v in range(n)]
    clustering=[]
    for v in range(n):
        neigh=sorted(neighbours(edges,v))
        if len(neigh)<2: clustering.append(Fraction(0));continue
        links=sum(pair(a,b) in edges for i,a in enumerate(neigh) for b in neigh[i+1:])
        clustering.append(Fraction(2*links,len(neigh)*(len(neigh)-1)))
    C=sum(clustering,Fraction(0))/n
    distances={}
    for start in range(n):
        distance={start:0}
        q=[start]
        for node in q:
            for nbr in neighbours(edges,node):
                if nbr not in distance:
                    distance[nbr]=distance[node]+1
                    q.append(nbr)
        distances[start]=distance
    visited=set()
    components=0
    for v in range(n):
        if v not in visited:
            components+=1
            visited.update(distances[v])
    L=None
    if components==1:
        L=sum((distances[i][j] for i in range(n) for j in range(i+1,n)),0)
        L=Fraction(L,n*(n-1)//2)
    return C,L,components

def generate():
    atoms=[]
    outcomes=[]
    for n in (8,10):
        start=baseline(n)
        assert len(start)==2*n
        for p in PARAMS:
            paths=[]
            first=choices(start,n,0,1,p)
            for a1,t1,w1,e1 in first:
                atoms.append(dict(zip(COLUMNS,map(str,(
                    n,p,1,"none",-1,0,1,a1,t1,
                    edge_string(start),w1,edge_string(e1)
                )))))
                second=choices(e1,n,1,2,p)
                for a2,t2,w2,e2 in second:
                    atoms.append(dict(zip(COLUMNS,map(str,(
                        n,p,2,a1,t1,1,2,a2,t2,
                        edge_string(e1),w2,edge_string(e2)
                    )))))
                    C,L,components=graph_metrics(e2,n)
                    paths.append({
                        "first_action":a1,"first_target":t1,
                        "second_action":a2,"second_target":t2,
                        "probability":str(w1*w2),
                        "final_edges":edge_string(e2),
                        "clustering":str(C),
                        "mean_shortest_path":str(L) if L is not None else None,
                        "components":components,
                    })
            assert sum(Fraction(row["probability"]) for row in paths)==1
            C0,L0,k0=graph_metrics(start,n)
            outcomes.append({
                "N":n,"p":str(p),
                "baseline_edges":edge_string(start),
                "baseline_clustering":str(C0),
                "baseline_mean_shortest_path":str(L0),
                "baseline_components":k0,
                "complete_paths":paths
            })
    result={
        "schema":"r315_ws_first_two_clockwise_edges_exact_e1_v1",
        "original_catalogue_id":"04-017",
        "source_scope":"FINITE_ARTIFICIAL_E1_ONLY",
        "source_atom_count":len(atoms),
        "full_path_count":sum(len(r["complete_paths"]) for r in outcomes),
        "parameter_worlds":outcomes
    }
    return atoms,result

def archive_replay():
    with SRC.open(encoding="utf-8",newline="") as f:
        existing=list(csv.DictReader(f))
    atoms,out=generate()
    assert len(existing)==len(atoms)==210
    assert existing==atoms
    assert json.loads(OUT.read_text(encoding="utf-8"))==out
    assert out["full_path_count"]==180

class FiniteWSTests(unittest.TestCase):
    def test_n8_edges(self): self.assertEqual(len(baseline(8)),16)
    def test_n10_edges(self): self.assertEqual(len(baseline(10)),20)
    def test_n8_degree_four(self):
        for i in range(8): self.assertEqual(len(neighbours(baseline(8),i)),4)
    def test_n10_degree_four(self):
        for i in range(10): self.assertEqual(len(neighbours(baseline(10),i)),4)
    def test_first_edge(self): self.assertIn((0,1),baseline(8))
    def test_second_edge_clockwise(self): self.assertIn((1,2),baseline(8))
    def test_first_n8_choices(self): self.assertEqual(len(choices(baseline(8),8,0,1,Fraction(1,2))),4)
    def test_first_n10_choices(self): self.assertEqual(len(choices(baseline(10),10,0,1,Fraction(1,2))),6)
    def test_first_n8_rewire_targets(self):
        self.assertEqual([x[1] for x in choices(baseline(8),8,0,1,Fraction(1,2))][1:],[3,4,5])
    def test_first_n10_rewire_targets(self):
        self.assertEqual([x[1] for x in choices(baseline(10),10,0,1,Fraction(1,2))][1:],[3,4,5,6,7])
    def test_second_n8_after_keep(self):
        self.assertEqual(len(choices(baseline(8),8,1,2,Fraction(1,2))),4)
    def test_second_n8_after_rewire(self):
        x=choices(baseline(8),8,0,1,Fraction(1,2))[1]
        self.assertEqual(len(choices(x[3],8,1,2,Fraction(1,2))),5)
    def test_second_n10_after_rewire(self):
        x=choices(baseline(10),10,0,1,Fraction(1,2))[1]
        self.assertEqual(len(choices(x[3],10,1,2,Fraction(1,2))),7)
    def test_first_conditional_mass(self):
        for n in (8,10):
            for p in PARAMS:
                self.assertEqual(sum(x[2] for x in choices(baseline(n),n,0,1,p)),1)
    def test_second_conditional_mass(self):
        for n in (8,10):
            for p in PARAMS:
                for _,_,_,e in choices(baseline(n),n,0,1,p):
                    self.assertEqual(sum(x[2] for x in choices(e,n,1,2,p)),1)
    def test_zero_rewire_probability_at_pzero(self):
        self.assertTrue(all(x[2]==0 for x in choices(baseline(8),8,0,1,Fraction(0))[1:]))
    def test_one_retention_zero_at_pone(self):
        self.assertEqual(choices(baseline(8),8,0,1,Fraction(1))[0][2],0)
    def test_rewire_edge_number_constant(self):
        for n in (8,10):
            for _,_,_,e in choices(baseline(n),n,0,1,Fraction(1,2)):
                self.assertEqual(len(e),2*n)
    def test_rewire_no_self_loop(self):
        for n in (8,10):
            for _,_,_,e in choices(baseline(n),n,0,1,Fraction(1,2)):
                self.assertTrue(all(a<b for a,b in e))
    def test_actor_degree_invariant(self):
        for n in (8,10):
            for _,_,_,e in choices(baseline(n),n,0,1,Fraction(1,2)):
                self.assertEqual(len(neighbours(e,0)),4)
    def test_old_target_degree_decreases(self):
        x=choices(baseline(8),8,0,1,Fraction(1,2))[1][3]
        self.assertEqual(len(neighbours(x,1)),3)
    def test_new_target_degree_increases(self):
        x=choices(baseline(8),8,0,1,Fraction(1,2))[1][3]
        self.assertEqual(len(neighbours(x,3)),5)
    def test_ring_clustering_positive(self):
        for n in (8,10): self.assertGreater(graph_metrics(baseline(n),n)[0],0)
    def test_ring_connected(self):
        for n in (8,10): self.assertEqual(graph_metrics(baseline(n),n)[2],1)
    def test_no_null_baseline_path(self):
        for n in (8,10): self.assertIsNotNone(graph_metrics(baseline(n),n)[1])
    def test_all_atom_count(self): self.assertEqual(len(generate()[0]),210)
    def test_all_path_count(self): self.assertEqual(generate()[1]["full_path_count"],180)
    def test_n8_paths_per_p(self):
        for x in generate()[1]["parameter_worlds"]:
            if x["N"]==8: self.assertEqual(len(x["complete_paths"]),19)
    def test_n10_paths_per_p(self):
        for x in generate()[1]["parameter_worlds"]:
            if x["N"]==10: self.assertEqual(len(x["complete_paths"]),41)
    def test_path_mass_all(self):
        for x in generate()[1]["parameter_worlds"]:
            self.assertEqual(sum(Fraction(y["probability"]) for y in x["complete_paths"]),1)
    def test_p0_retains_baseline(self):
        for x in generate()[1]["parameter_worlds"]:
            if x["p"]=="0":
                active=[y for y in x["complete_paths"] if Fraction(y["probability"])>0]
                self.assertEqual(len(active),1)
                self.assertEqual(active[0]["final_edges"],x["baseline_edges"])
    def test_p1_excludes_keep(self):
        for x in generate()[1]["parameter_worlds"]:
            if x["p"]=="1":
                self.assertTrue(all(y["probability"]=="0" for y in x["complete_paths"] if "keep" in (y["first_action"],y["second_action"])))
    def test_all_edges_constant(self):
        for x in generate()[1]["parameter_worlds"]:
            self.assertTrue(all(len(y["final_edges"].split(";"))==2*x["N"] for y in x["complete_paths"]))
    def test_archive_equality(self): archive_replay()

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true")
    p.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:
        result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(FiniteWSTests))
        if not result.wasSuccessful():raise SystemExit(1)
    elif args.audit:
        archive_replay()
        print("PASS R315: 210 exact source atoms, 180 two-event paths, C and L replayed")
    else:
        print(json.dumps(generate()[1],indent=2))
