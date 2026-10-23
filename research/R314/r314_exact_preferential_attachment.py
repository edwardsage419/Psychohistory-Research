#!/usr/bin/env python3
"""R314 exact two-arrival Barabasi-Albert attachment, synthetic bounded E1 only."""
from __future__ import annotations
import argparse
import csv
import json
from collections import defaultdict
from fractions import Fraction
from pathlib import Path
import unittest

DIR=Path(__file__).resolve().parent
CSV=DIR/"R314_ALL_54_ORIGINAL_TARGET_SOURCE_ATOMS.csv"
JSON=DIR/"R314_EXACT_44_TWO_ARRIVAL_PATH_RESULTS.json"
SEEDS={
    "P3":((0,1),(1,2)),
    "K3":((0,1),(0,2),(1,2)),
    "S4":((0,1),(0,2),(0,3)),
}
FIELDS=("seed","stage","prefix","edges_before","old_node_count","target",
        "target_degree","degree_sum","choice_probability","edges_after")

def vertices(edges):
    nodes={v for e in edges for v in e}
    assert nodes==set(range(max(nodes)+1))
    return len(nodes)

def edges_token(edges):
    assert len(set(edges))==len(edges)
    assert all(a<b for a,b in edges)
    return ";".join(f"{a}-{b}" for a,b in sorted(edges))

def degrees(edges):
    d=[0]*vertices(edges)
    for a,b in edges:
        d[a]+=1
        d[b]+=1
    assert sum(d)==2*len(edges)
    return d

def choices(edges):
    d=degrees(edges)
    assert all(x>0 for x in d)
    return [Fraction(x,sum(d)) for x in d]

def attach(edges,target):
    old_n=vertices(edges)
    assert 0<=target<old_n
    assert (target,old_n) not in edges and (old_n,target) not in edges
    new=tuple(sorted(tuple(edges)+((target,old_n),)))
    assert vertices(new)==old_n+1
    return new

def generate():
    atoms=[]
    result=[]
    for seed,seed_edges in SEEDS.items():
        base=tuple(seed_edges)
        n=vertices(base)
        first=choices(base)
        paths=[]
        for target,p in enumerate(first):
            atoms.append(dict(zip(FIELDS,map(str,(
                seed,1,"none",edges_token(base),n,target,degrees(base)[target],
                2*len(base),p,edges_token(attach(base,target))
            )))))
        for first_target,p1 in enumerate(first):
            intermediate=attach(base,first_target)
            second=choices(intermediate)
            for second_target,p2 in enumerate(second):
                final=attach(intermediate,second_target)
                atoms.append(dict(zip(FIELDS,map(str,(
                    seed,2,first_target,edges_token(intermediate),n+1,second_target,
                    degrees(intermediate)[second_target],2*len(intermediate),p2,
                    edges_token(final)
                )))))
                paths.append({
                    "first_target":first_target,
                    "second_target":second_target,
                    "path_probability":str(p1*p2),
                    "final_edges":edges_token(final),
                })
        assert sum(Fraction(p["path_probability"]) for p in paths)==1
        result.append({
            "seed":seed,
            "initial_edges":edges_token(base),
            "first_choices":n,
            "second_choice_atoms":n*(n+1),
            "paths":paths,
        })
    return atoms,{
        "schema":"r314_ba_degree_preferential_attachment_m1_3_seeds_2_arrivals_e1_v1",
        "catalogue_id":"04-016","grade":"SYNTHETIC_EXACT_E1_ONLY",
        "source_atoms":len(atoms),
        "two_arrival_paths":sum(len(r["paths"]) for r in result),
        "seed_results":result,
    }

def verify_archive():
    with CSV.open(newline="",encoding="utf-8") as h:
        saved=list(csv.DictReader(h))
    expected,js=generate()
    if saved!=expected:
        raise AssertionError("archived conditional degree-proportional source changed")
    if json.loads(JSON.read_text(encoding="utf-8"))!=js:
        raise AssertionError("archived path distributions changed")
    assert len(saved)==54 and js["two_arrival_paths"]==44

class BAUnitTests(unittest.TestCase):
    def test_seed_count(self): self.assertEqual(len(SEEDS),3)
    def test_p3_vertex_count(self): self.assertEqual(vertices(SEEDS["P3"]),3)
    def test_k3_vertex_count(self): self.assertEqual(vertices(SEEDS["K3"]),3)
    def test_s4_vertex_count(self): self.assertEqual(vertices(SEEDS["S4"]),4)
    def test_p3_degree(self): self.assertEqual(degrees(SEEDS["P3"]),[1,2,1])
    def test_k3_degree(self): self.assertEqual(degrees(SEEDS["K3"]),[2,2,2])
    def test_s4_degree(self): self.assertEqual(degrees(SEEDS["S4"]),[3,1,1,1])
    def test_p3_prob(self): self.assertEqual(choices(SEEDS["P3"]),[Fraction(1,4),Fraction(1,2),Fraction(1,4)])
    def test_k3_prob(self): self.assertEqual(choices(SEEDS["K3"]),[Fraction(1,3)]*3)
    def test_s4_prob(self): self.assertEqual(choices(SEEDS["S4"]),[Fraction(1,2)]+[Fraction(1,6)]*3)
    def test_seed_prob_normalization(self):
        for e in SEEDS.values(): self.assertEqual(sum(choices(e)),1)
    def test_new_node_degree_one(self):
        for e in SEEDS.values():
            for t in range(vertices(e)):
                new=attach(e,t)
                self.assertEqual(degrees(new)[-1],1)
    def test_total_degree_plus_two(self):
        for e in SEEDS.values():
            for t in range(vertices(e)):
                self.assertEqual(sum(degrees(attach(e,t)))-sum(degrees(e)),2)
    def test_target_degree_plus_one(self):
        for e in SEEDS.values():
            for t in range(vertices(e)):
                self.assertEqual(degrees(attach(e,t))[t],degrees(e)[t]+1)
    def test_untouched_old_degrees(self):
        for e in SEEDS.values():
            for t in range(vertices(e)):
                for k in range(vertices(e)):
                    if k!=t: self.assertEqual(degrees(attach(e,t))[k],degrees(e)[k])
    def test_no_duplicate_edges(self):
        for e in SEEDS.values():
            for t in range(vertices(e)):
                self.assertEqual(len(set(attach(e,t))),len(e)+1)
    def test_no_self_loops(self):
        for e in SEEDS.values():
            for t in range(vertices(e)):
                self.assertTrue(all(a!=b for a,b in attach(e,t)))
    def test_stage2_has_added_old_candidate(self):
        for e in SEEDS.values():
            self.assertEqual(len(choices(attach(e,0))),vertices(e)+1)
    def test_second_mass_one(self):
        for e in SEEDS.values():
            for t in range(vertices(e)):
                self.assertEqual(sum(choices(attach(e,t))),1)
    def test_stage1_selected_gets_larger_probability(self):
        e=SEEDS["P3"]
        self.assertGreater(choices(attach(e,0))[0],choices(attach(e,0))[2])
    def test_fixed_conditional_degree_sum(self):
        for e in SEEDS.values():
            for t in range(vertices(e)):
                z=attach(e,t)
                self.assertEqual(sum(degrees(z)),2*len(z))
    def test_source_count(self): self.assertEqual(len(generate()[0]),54)
    def test_path_count(self): self.assertEqual(generate()[1]["two_arrival_paths"],44)
    def test_unique_source_keys(self):
        rows,_=generate()
        self.assertEqual(len({(x["seed"],x["stage"],x["prefix"],x["target"]) for x in rows}),54)
    def test_stage_one_10_atoms(self):
        rows,_=generate()
        self.assertEqual(sum(x["stage"]=="1" for x in rows),10)
    def test_stage_two_44_atoms(self):
        rows,_=generate()
        self.assertEqual(sum(x["stage"]=="2" for x in rows),44)
    def test_per_seed_path_sum_one(self):
        for x in generate()[1]["seed_results"]:
            self.assertEqual(sum(Fraction(p["path_probability"]) for p in x["paths"]),1)
    def test_expected_path_counts(self):
        self.assertEqual([len(x["paths"]) for x in generate()[1]["seed_results"]],[12,12,20])
    def test_p3_first_target_center_double(self):
        d=choices(SEEDS["P3"])
        self.assertEqual(d[1],2*d[0])
    def test_s4_center_threefold_leaf(self):
        d=choices(SEEDS["S4"])
        self.assertEqual(d[0],3*d[1])
    def test_stage2_degree_normalization(self):
        self.assertEqual(sum(degrees(attach(SEEDS["K3"],0))),8)
    def test_archive_matches_recomputation(self): verify_archive()

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true")
    p.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:
        t=unittest.defaultTestLoader.loadTestsFromTestCase(BAUnitTests)
        ok=unittest.TextTestRunner(verbosity=1).run(t)
        if not ok.wasSuccessful(): raise SystemExit(1)
    elif a.audit:
        verify_archive()
        print("PASS R314: 3 seeds, 54 exact conditional source atoms, 44 full paths")
    else:
        print(json.dumps(generate()[1],indent=2))
