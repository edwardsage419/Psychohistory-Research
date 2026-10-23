#!/usr/bin/env python3
"""R316: exact 4-node, two known-block undirected Bernoulli SBM E1."""
from __future__ import annotations
import argparse
import csv
import json
import unittest
from fractions import Fraction
from pathlib import Path

DIR=Path(__file__).resolve().parent
SOURCE=DIR/"R316_ALL_768_ORIGINAL_GRAPH_DYAD_PROBABILITY_ATOMS.csv"
RESULT=DIR/"R316_EXACT_128_GRAPH_LIKELIHOODS.json"
BLOCKS=(0,0,1,1)
DYADS=((0,1),(0,2),(0,3),(1,2),(1,3),(2,3))
PARAMS=(("A",Fraction(3,4),Fraction(1,4)),("D",Fraction(1,4),Fraction(3,4)))
FIELDS=("regime","mask","edge_vector","dyad_index","node_i","node_j",
        "same_block","edge_present","bernoulIi_parameter","realized_factor",
        "full_graph_probability")

def bits(mask):
    assert 0<=mask<64
    return tuple(int(v) for v in f"{mask:06b}")

def parameter(i,pw,pc):
    u,v=DYADS[i]
    return pw if BLOCKS[u]==BLOCKS[v] else pc

def factor(mask,i,pw,pc):
    p=parameter(i,pw,pc)
    return p if bits(mask)[i] else Fraction(1)-p

def likelihood(mask,pw,pc):
    ans=Fraction(1)
    for i in range(6): ans*=factor(mask,i,pw,pc)
    return ans

def exact_tv():
    a,d=PARAMS
    return sum((abs(likelihood(m,a[1],a[2])-likelihood(m,d[1],d[2])) for m in range(64)),Fraction(0))/2

def generate():
    atoms=[];models=[]
    for name,pw,pc in PARAMS:
        worlds=[]
        for mask in range(64):
            b=bits(mask);like=likelihood(mask,pw,pc)
            for i,(u,v) in enumerate(DYADS):
                q=parameter(i,pw,pc)
                atom={
                    "regime":name,"mask":str(mask),"edge_vector":"".join(map(str,b)),
                    "dyad_index":str(i),"node_i":str(u),"node_j":str(v),
                    "same_block":str(int(BLOCKS[u]==BLOCKS[v])),
                    "edge_present":str(b[i]),
                    "bernoulIi_parameter":str(q),
                    "realized_factor":str(factor(mask,i,pw,pc)),
                    "full_graph_probability":str(like),
                }
                atoms.append(atom)
            worlds.append({
                "mask":mask,
                "edge_vector":"".join(map(str,b)),
                "within_edges":b[0]+b[5],
                "cross_edges":sum(b[1:5]),
                "probability":str(like),
            })
        assert sum(Fraction(w["probability"]) for w in worlds)==1
        models.append({
            "regime":name,"within_p":str(pw),"cross_p":str(pc),
            "expected_within_edges":str(2*pw),
            "expected_cross_edges":str(4*pc),
            "expected_total_edges":str(2*pw+4*pc),
            "complete_graphs":worlds
        })
    output={
        "schema":"r316_sbm_known_block_4node_all_graphs_exact_E1_v1",
        "original_catalogue_id":"04-019",
        "source_scope":"SYNTHETIC_EXACT_E1_ONLY",
        "fixed_blocks":[0,0,1,1],
        "dyads":[list(x) for x in DYADS],
        "source_atom_count":len(atoms),
        "graph_count":sum(len(x["complete_graphs"]) for x in models),
        "total_variation_A_D":str(exact_tv()),
        "regimes":models
    }
    return atoms,output

def replay():
    with SOURCE.open(encoding="utf-8",newline="") as f:
        archived=list(csv.DictReader(f))
    atoms,result=generate()
    assert len(archived)==len(atoms)==768
    assert archived==atoms
    assert json.loads(RESULT.read_text(encoding="utf-8"))==result
    assert result["graph_count"]==128

class SBMTests(unittest.TestCase):
    def test_four_nodes(self): self.assertEqual(len(BLOCKS),4)
    def test_two_known_labels(self): self.assertEqual(BLOCKS,(0,0,1,1))
    def test_six_dyads(self): self.assertEqual(len(DYADS),6)
    def test_undirected_unique_dyads(self): self.assertEqual(len(set(DYADS)),6)
    def test_no_self_dyads(self): self.assertTrue(all(a<b for a,b in DYADS))
    def test_two_within_pairs(self):
        self.assertEqual([i for i,(a,b) in enumerate(DYADS) if BLOCKS[a]==BLOCKS[b]],[0,5])
    def test_four_cross_pairs(self):
        self.assertEqual([i for i,(a,b) in enumerate(DYADS) if BLOCKS[a]!=BLOCKS[b]],[1,2,3,4])
    def test_empty_mask(self): self.assertEqual(bits(0),(0,)*6)
    def test_full_mask(self): self.assertEqual(bits(63),(1,)*6)
    def test_within_only_mask(self): self.assertEqual(bits(33),(1,0,0,0,0,1))
    def test_all_mask_unique(self): self.assertEqual(len({bits(i) for i in range(64)}),64)
    def test_assortative_within_prob(self): self.assertEqual(parameter(0,PARAMS[0][1],PARAMS[0][2]),Fraction(3,4))
    def test_assortative_cross_prob(self): self.assertEqual(parameter(1,PARAMS[0][1],PARAMS[0][2]),Fraction(1,4))
    def test_disassortative_within_prob(self): self.assertEqual(parameter(5,PARAMS[1][1],PARAMS[1][2]),Fraction(1,4))
    def test_disassortative_cross_prob(self): self.assertEqual(parameter(4,PARAMS[1][1],PARAMS[1][2]),Fraction(3,4))
    def test_present_factor(self): self.assertEqual(factor(33,0,PARAMS[0][1],PARAMS[0][2]),Fraction(3,4))
    def test_absent_factor(self): self.assertEqual(factor(0,0,PARAMS[0][1],PARAMS[0][2]),Fraction(1,4))
    def test_regime_A_within_graph_prob(self): self.assertEqual(likelihood(33,PARAMS[0][1],PARAMS[0][2]),Fraction(729,4096))
    def test_regime_D_within_graph_prob(self): self.assertEqual(likelihood(33,PARAMS[1][1],PARAMS[1][2]),Fraction(1,4096))
    def test_within_only_bayes_factor_729(self):
        self.assertEqual(likelihood(33,PARAMS[0][1],PARAMS[0][2])/likelihood(33,PARAMS[1][1],PARAMS[1][2]),729)
    def test_empty_regime_A(self): self.assertEqual(likelihood(0,PARAMS[0][1],PARAMS[0][2]),Fraction(81,4096))
    def test_empty_regime_D(self): self.assertEqual(likelihood(0,PARAMS[1][1],PARAMS[1][2]),Fraction(9,4096))
    def test_full_regime_A(self): self.assertEqual(likelihood(63,PARAMS[0][1],PARAMS[0][2]),Fraction(9,4096))
    def test_full_regime_D(self): self.assertEqual(likelihood(63,PARAMS[1][1],PARAMS[1][2]),Fraction(81,4096))
    def test_normalization(self):
        for _,a,b in PARAMS:
            self.assertEqual(sum(likelihood(i,a,b) for i in range(64)),1)
    def test_positive_graph_likelihoods(self):
        for _,a,b in PARAMS:
            self.assertTrue(all(likelihood(i,a,b)>0 for i in range(64)))
    def test_expected_within_A(self): self.assertEqual(2*PARAMS[0][1],Fraction(3,2))
    def test_expected_cross_A(self): self.assertEqual(4*PARAMS[0][2],1)
    def test_expected_total_A(self): self.assertEqual(2*PARAMS[0][1]+4*PARAMS[0][2],Fraction(5,2))
    def test_expected_total_D(self): self.assertEqual(2*PARAMS[1][1]+4*PARAMS[1][2],Fraction(7,2))
    def test_all_atoms(self): self.assertEqual(len(generate()[0]),768)
    def test_all_graphs(self): self.assertEqual(generate()[1]["graph_count"],128)
    def test_total_variation_in_unit(self): self.assertTrue(Fraction(0)<exact_tv()<Fraction(1))
    def test_archive_replay(self): replay()

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true")
    p.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:
        r=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(SBMTests))
        if not r.wasSuccessful():raise SystemExit(1)
    elif args.audit:
        replay()
        print("PASS R316: 768 graph-dyad original atoms, 128 graph probabilities, 2 regimes")
    else:
        print(json.dumps(generate()[1],indent=2))
