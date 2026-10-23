#!/usr/bin/env python3
"""R331 exact finite artificial heterogeneous retention."""
import argparse
import csv
import io
import json
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CSV="R331_ALL_81_ARTIFICIAL_RETENTION_ATOMS.csv"
RESULT="R331_EXACT_9_RETENTION_WORLDS.json"
FIELDS=["world_id","a","b","w","t","fast_contribution","slow_contribution","mixture","homogeneous","gap"]
PAIRS=((F(1,4),F(1,2)),(F(1,4),F(3,4)),(F(1,2),F(3,4)))
WEIGHTS=(F(1,4),F(1,2),F(3,4))

def values(a,b,w,t):
    fast=w*a**t
    slow=(1-w)*b**t
    mix=fast+slow
    hom=(w*a+(1-w)*b)**t
    return fast,slow,mix,hom,mix-hom

def generate():
    rows,worlds=[],[]
    for n,(pair,w) in enumerate(product(PAIRS,WEIGHTS),1):
        a,b=pair
        ident=f"W{n:02d}"
        for t in range(9):
            fast,slow,mix,hom,gap=values(a,b,w,t)
            rows.append(dict(world_id=ident,a=str(a),b=str(b),w=str(w),t=str(t),
                             fast_contribution=str(fast),slow_contribution=str(slow),
                             mixture=str(mix),homogeneous=str(hom),gap=str(gap)))
        _,_,s2,q2,g2=values(a,b,w,2)
        _,_,s8,q8,g8=values(a,b,w,8)
        worlds.append(dict(world_id=ident,a=str(a),b=str(b),w=str(w),
                           s2=str(s2),q2=str(q2),gap2=str(g2),
                           s8=str(s8),q8=str(q8),gap8=str(g8)))
    return rows,dict(model="R331_CONSTRUCTED_HETEROGENEOUS_RETENTION_E1",
                     source_row_count=len(rows),world_count=len(worlds),worlds=worlds)

def serialized():
    rows,result=generate()
    output=io.StringIO(newline="")
    writer=csv.DictWriter(output,fieldnames=FIELDS,lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue(),json.dumps(result,separators=(",",":"))+"\n"

def replay():
    a,b=serialized()
    assert (ROOT/CSV).read_bytes()==a.encode("utf-8"),"CSV byte mismatch"
    assert (ROOT/RESULT).read_bytes()==b.encode("utf-8"),"JSON byte mismatch"

class Tests(unittest.TestCase):
    def test_counts(self):
        r,d=generate()
        self.assertEqual((len(r),len(d["worlds"])),(81,9))
    def test_initial_and_one_step(self):
        for a,b in PAIRS:
            for w in WEIGHTS:
                for t in (0,1):
                    self.assertEqual(values(a,b,w,t)[-1],F(0))
    def test_variance_identity(self):
        for a,b in PAIRS:
            for w in WEIGHTS:
                self.assertEqual(values(a,b,w,2)[-1],w*(1-w)*(b-a)**2)
                self.assertGreater(values(a,b,w,2)[-1],0)
    def test_late_tail(self):
        for a,b in PAIRS:
            for w in WEIGHTS:
                for t in range(2,9):
                    self.assertGreater(values(a,b,w,t)[-1],0)
    def test_monotone_survival(self):
        for a,b in PAIRS:
            for w in WEIGHTS:
                v=[values(a,b,w,t)[2] for t in range(9)]
                self.assertEqual(v[0],F(1))
                self.assertTrue(all(v[t+1]<v[t] for t in range(8)))
    def test_frozen_counterexample(self):
        self.assertEqual(values(F(1,4),F(3,4),F(1,2),2)[2:],(F(5,16),F(1,4),F(1,16)))
    def test_byte_replay(self):
        replay()

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--audit",action="store_true")
    args=parser.parse_args()
    if args.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        if not result.wasSuccessful():raise SystemExit(1)
    if args.audit:
        replay()
        print("R331 source byte replay PASS: 81 artificial atoms, 9 worlds")
    if not (args.test or args.audit):print(serialized()[1])
