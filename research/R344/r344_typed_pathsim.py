#!/usr/bin/env python3
"""R344 frozen exact typed A-B-A PathSim-style enumeration. Artificial E1 only."""
import argparse
import csv
import io
import json
import unittest
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parent
NETWORKS=tuple(format(k,"04b") for k in range(16))
CSV_PATH=ROOT/"R344_ALL_64_ARTIFICIAL_TYPED_PATH_ATOMS.csv"
JSON_PATH=ROOT/"R344_EXACT_16_TYPED_NETWORKS.json"

def compute(bits):
    m=((int(bits[0]),int(bits[1])),(int(bits[2]),int(bits[3])))
    counts=[[sum(m[i][k]*m[j][k] for k in range(2)) for j in range(2)] for i in range(2)]
    scores=[]
    for i in range(2):
        row=[]
        for j in range(2):
            denom=counts[i][i]+counts[j][j]
            row.append(Fraction(2*counts[i][j],denom) if denom else Fraction(0))
        scores.append(row)
    return counts,scores

def artifacts():
    out=io.StringIO(newline="")
    writer=csv.writer(out,lineterminator="\n")
    writer.writerow(("network_bits","source","target","path_count","self_source_count","self_target_count","pathsim"))
    worlds=[]
    for bits in NETWORKS:
        counts,scores=compute(bits)
        for i in range(2):
            for j in range(2):
                writer.writerow((bits,f"A{i}",f"A{j}",str(counts[i][j]),str(counts[i][i]),str(counts[j][j]),str(scores[i][j])))
        worlds.append({"network_bits":bits,"path_count_matrix":counts,"pathsim_matrix":[[str(x) for x in row] for row in scores]})
    result={
        "schema":"R344_frozen_two_type_pathsim_v1",
        "worlds":worlds,
        "checks":{
            "worlds":16,
            "source_rows":64,
            "symmetric_worlds":16,
            "positive_cross_similarity_worlds":7,
            "zero_graph_cross_similarity":"0",
            "layer_B_swap_invariant_worlds":16,
            "projection_collision_witness":["1010","0101"],
        },
    }
    return out.getvalue().encode("utf-8"),(json.dumps(result,indent=2,ensure_ascii=True)+"\n").encode("utf-8")

def audit():
    a,b=artifacts()
    assert CSV_PATH.read_bytes()==a,"CSV mismatch"
    assert JSON_PATH.read_bytes()==b,"JSON mismatch"

class FrozenTests(unittest.TestCase):
    def test_universe(self):
        self.assertEqual(len(NETWORKS),16)
        self.assertEqual(len(artifacts()[0].decode().splitlines()),65)
    def test_symmetry(self):
        for bits in NETWORKS:
            n,p=compute(bits)
            self.assertEqual(n[0][1],n[1][0])
            self.assertEqual(p[0][1],p[1][0])
    def test_positive_cross(self):
        self.assertEqual(sum(compute(bits)[1][0][1]>0 for bits in NETWORKS),7)
    def test_bounds(self):
        for bits in NETWORKS:
            n,p=compute(bits)
            for i in range(2):
                for j in range(2):
                    self.assertTrue(0<=p[i][j]<=1)
                self.assertEqual(p[i][i],1 if n[i][i]>0 else 0)
    def test_swap_B_invariance(self):
        for bits in NETWORKS:
            swapped=bits[1]+bits[0]+bits[3]+bits[2]
            self.assertEqual(compute(bits),compute(swapped))
    def test_projection_collision(self):
        self.assertNotEqual("1010","0101")
        self.assertEqual(compute("1010"),compute("0101"))
    def test_zero_graph(self):
        self.assertEqual(str(compute("0000")[1][0][1]),"0")
    def test_byte_replay(self):
        audit()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--write",action="store_true")
    p.add_argument("--test",action="store_true")
    p.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.write:
        a,b=artifacts()
        CSV_PATH.write_bytes(a)
        JSON_PATH.write_bytes(b)
    if args.audit:
        audit()
        print("R344_PRODUCTION_BYTE_REPLAY=PASS")
    if args.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(FrozenTests))
        if not result.wasSuccessful():raise SystemExit(1)
    if not (args.write or args.test or args.audit):p.print_help()

if __name__=="__main__":
    main()
