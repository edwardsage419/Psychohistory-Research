#!/usr/bin/env python3
"""R341: frozen exact 3-node ERGM graph enumeration; artificial E1 only."""
import argparse
import csv
import io
import json
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GRAPHS = tuple(format(k, "03b") for k in range(8))
WORLDS = (("1", "1"), ("1", "2"), ("2", "1"), ("2", "2"))
CSV_PATH = ROOT / "R341_ALL_32_ARTIFICIAL_GRAPH_ATOMS.csv"
JSON_PATH = ROOT / "R341_EXACT_4_GRAPH_WORLDS.json"

def graph_atoms(a_text, b_text):
    a, b = int(a_text), int(b_text)
    return [(bits, bits.count("1"), int(bits == "111"),
             a**bits.count("1") * b**int(bits == "111")) for bits in GRAPHS]

def artifacts():
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(("a","b","graph_bits","edges","triangles","unnormalized_weight","probability"))
    worlds = []
    for a, b in WORLDS:
        atoms = graph_atoms(a,b)
        z = sum(weight for _,_,_,weight in atoms)
        probabilities = [Fraction(weight,z) for _,_,_,weight in atoms]
        for (bits,edges,triangles,weight),p in zip(atoms,probabilities):
            writer.writerow((a,b,bits,str(edges),str(triangles),str(Fraction(weight)),str(p)))
        marginal = sum((p for (bits,_,_,_),p in zip(atoms,probabilities) if bits[0]=="1"),Fraction(0))
        worlds.append({
            "a": a,
            "b": b,
            "Z": str(Fraction(z)),
            "edge_marginal": str(marginal),
            "triangle_probability": str(probabilities[7]),
            "closure_odds_ratio": str(Fraction(b)),
            "graph_probabilities": [str(p) for p in probabilities],
        })
    result = {
        "schema": "R341_frozen_three_node_ergm_v1",
        "worlds": worlds,
        "checks": {
            "worlds": 4,
            "source_rows": 32,
            "normalization_worlds": 4,
            "expected_partition_functions": ["8","9","27","35"],
            "baseline_independent_worlds": 2,
            "closure_contrast_worlds": 2,
        },
    }
    return out.getvalue().encode("utf-8"), (json.dumps(result,indent=2,ensure_ascii=True)+"\n").encode("utf-8")

def audit():
    csv_expected,json_expected=artifacts()
    assert CSV_PATH.read_bytes()==csv_expected, "CSV mismatch"
    assert JSON_PATH.read_bytes()==json_expected, "JSON mismatch"

class FrozenTests(unittest.TestCase):
    def test_universe(self):
        self.assertEqual(len(GRAPHS),8)
        self.assertEqual(len(WORLDS),4)
        self.assertEqual(len(artifacts()[0].decode().splitlines()),33)
    def test_normalizers(self):
        self.assertEqual([sum(x[3] for x in graph_atoms(a,b)) for a,b in WORLDS],[8,9,27,35])
    def test_probabilities(self):
        for a,b in WORLDS:
            atoms=graph_atoms(a,b)
            z=sum(x[3] for x in atoms)
            self.assertEqual(sum(Fraction(x[3],z) for x in atoms),1)
    def test_edge_marginals(self):
        observed=[]
        for a,b in WORLDS:
            atoms=graph_atoms(a,b)
            z=sum(x[3] for x in atoms)
            observed.append(sum((Fraction(w,z) for bits,e,t,w in atoms if bits[0]=="1"),Fraction(0)))
        self.assertEqual(observed,[Fraction(1,2),Fraction(5,9),Fraction(2,3),Fraction(26,35)])
    def test_triangle_probabilities(self):
        self.assertEqual([Fraction(int(a)**3*int(b),sum(x[3] for x in graph_atoms(a,b))) for a,b in WORLDS],
                         [Fraction(1,8),Fraction(2,9),Fraction(8,27),Fraction(16,35)])
    def test_conditional_closure_odds(self):
        for a,b in WORLDS:
            atoms={bits:w for bits,e,t,w in graph_atoms(a,b)}
            baseline=Fraction(atoms["100"],atoms["000"])
            closure=Fraction(atoms["111"],atoms["011"])
            self.assertEqual(closure/baseline,int(b))
    def test_independent_baselines(self):
        for a in ("1","2"):
            atoms=graph_atoms(a,"1")
            z=sum(x[3] for x in atoms)
            p=Fraction(int(a),1+int(a))
            for bits,e,t,w in atoms:
                self.assertEqual(Fraction(w,z),p**e*(1-p)**(3-e))
    def test_byte_replay(self):
        audit()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--write",action="store_true")
    p.add_argument("--test",action="store_true")
    p.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.write:
        x,y=artifacts()
        CSV_PATH.write_bytes(x)
        JSON_PATH.write_bytes(y)
    if args.audit:
        audit()
        print("R341_PRODUCTION_BYTE_REPLAY=PASS")
    if args.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(FrozenTests))
        if not result.wasSuccessful():
            raise SystemExit(1)
    if not (args.write or args.test or args.audit):
        p.print_help()

if __name__=="__main__":
    main()
