#!/usr/bin/env python3
"""R342 finite three-actor directed local choice analogue. Artificial E1 only."""
import argparse
import csv
import io
import json
import unittest
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parent
EDGES=((0,1),(0,2),(1,0),(1,2),(2,0),(2,1))
NETWORKS=tuple(format(i,"06b") for i in range(64))
RATES=("1","2")
CHOICES=("stay","toggle_first","toggle_second")
CSV_PATH=ROOT/"R342_ALL_1152_ARTIFICIAL_ACTOR_CHOICE_ATOMS.csv"
JSON_PATH=ROOT/"R342_EXACT_384_LOCAL_DECISIONS.json"

def local_candidates(bits,actor,r_text):
    targets=tuple(k for k in range(3) if k!=actor)
    rows=[]
    for choice in CHOICES:
        target=None if choice=="stay" else targets[0 if choice=="toggle_first" else 1]
        result=list(bits)
        if target is not None:
            idx=EDGES.index((actor,target))
            result[idx]="1" if result[idx]=="0" else "0"
        result="".join(result)
        reciprocity=sum(int(result[EDGES.index((actor,k))]=="1" and result[EDGES.index((k,actor))]=="1") for k in targets)
        weight=int(r_text)**reciprocity
        rows.append((choice,"NONE" if target is None else str(target),result,reciprocity,weight))
    z=sum(row[4] for row in rows)
    return [(choice,target,result,u,w,Fraction(w,z)) for choice,target,result,u,w in rows]

def artifacts():
    out=io.StringIO(newline="")
    writer=csv.writer(out,lineterminator="\n")
    writer.writerow(("r","network_bits","actor","choice","target","result_bits","reciprocity","weight","probability"))
    decisions=[]
    for r in RATES:
        for bits in NETWORKS:
            for actor in range(3):
                rows=local_candidates(bits,actor,r)
                for choice,target,result,u,w,p in rows:
                    writer.writerow((r,bits,str(actor),choice,target,result,str(u),str(Fraction(w)),str(p)))
                decisions.append({"r":r,"network_bits":bits,"actor":actor,"probabilities":[str(row[5]) for row in rows]})
    result={
        "schema":"R342_frozen_three_actor_local_choice_v1",
        "checks":{
            "worlds":2,"networks":64,"actors":3,"decisions":384,"source_rows":1152,
            "uniform_choice_decisions":192,"normalized_decisions":384,
        },
        "decisions":decisions,
    }
    return out.getvalue().encode("utf-8"),(json.dumps(result,indent=2,ensure_ascii=True)+"\n").encode("utf-8")

def audit():
    a,b=artifacts()
    assert CSV_PATH.read_bytes()==a,"CSV mismatch"
    assert JSON_PATH.read_bytes()==b,"JSON mismatch"

class FrozenTests(unittest.TestCase):
    def test_universe(self):
        self.assertEqual(len(NETWORKS),64)
        self.assertEqual(len(RATES)*len(NETWORKS)*3*len(CHOICES),1152)
        self.assertEqual(len(artifacts()[0].decode().splitlines()),1153)
    def test_normalization(self):
        for r in RATES:
            for bits in NETWORKS:
                for actor in range(3):
                    rows=local_candidates(bits,actor,r)
                    self.assertEqual(sum(row[5] for row in rows),1)
                    self.assertTrue(all(row[5]>0 for row in rows))
    def test_uniform_baseline(self):
        for bits in NETWORKS:
            for actor in range(3):
                self.assertEqual([row[5] for row in local_candidates(bits,actor,"1")],[Fraction(1,3)]*3)
    def test_single_outgoing_toggle(self):
        for bits in NETWORKS:
            for actor in range(3):
                rows=local_candidates(bits,actor,"2")
                self.assertEqual(rows[0][2],bits)
                for row in rows[1:]:
                    changed=[i for i in range(6) if row[2][i]!=bits[i]]
                    self.assertEqual(len(changed),1)
                    self.assertEqual(EDGES[changed[0]][0],actor)
    def test_odds(self):
        for bits in NETWORKS:
            for actor in range(3):
                rows=local_candidates(bits,actor,"2")
                for x in rows:
                    for y in rows:
                        self.assertEqual(x[5]/y[5],Fraction(2**x[3],2**y[3]))
    def test_nonuniform_witness(self):
        bits="001000"
        rows=local_candidates(bits,0,"2")
        self.assertTrue(len({x[5] for x in rows})>1)
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
        print("R342_PRODUCTION_BYTE_REPLAY=PASS")
    if args.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(FrozenTests))
        if not result.wasSuccessful():
            raise SystemExit(1)
    if not (args.write or args.test or args.audit):p.print_help()

if __name__=="__main__":
    main()
