#!/usr/bin/env python3
"""R332 exact three-task artificial cognitive resource allocation."""
import argparse
import csv
import io
import json
import unittest
from itertools import product
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CSV="R332_ALL_112_ARTIFICIAL_RESOURCE_SUBSETS.csv"
RESULT="R332_EXACT_14_RESOURCE_WORLDS.json"
FIELDS=["recoded","capacity","bits","cost","utility","feasible","chosen_bits","optimal_utility"]
BASE_COST=(1,2,3)
UTILITY=(1,3,4)

def enumerate_world(recoded,capacity):
    costs=(1,1 if recoded else 2,3)
    subsets=[]
    for flags in product((0,1),repeat=3):
        bits="".join(map(str,flags))
        cost=sum(x*y for x,y in zip(flags,costs))
        utility=sum(x*y for x,y in zip(flags,UTILITY))
        subsets.append(dict(bits=bits,cost=cost,utility=utility,feasible=cost<=capacity))
    eligible=[x for x in subsets if x["feasible"]]
    optimum=max(x["utility"] for x in eligible)
    chosen=min(x["bits"] for x in eligible if x["utility"]==optimum)
    return subsets,chosen,optimum

def generate():
    rows,worlds=[],[]
    for recoded in (0,1):
        for capacity in range(7):
            subsets,chosen,optimum=enumerate_world(recoded,capacity)
            for x in subsets:
                rows.append(dict(recoded=str(recoded),capacity=str(capacity),
                                 bits=x["bits"],cost=str(x["cost"]),utility=str(x["utility"]),
                                 feasible=str(int(x["feasible"])),chosen_bits=chosen,
                                 optimal_utility=str(optimum)))
            worlds.append(dict(recoded=recoded,capacity=capacity,chosen_bits=chosen,
                               optimal_utility=optimum,
                               feasible_count=sum(x["feasible"] for x in subsets),
                               optimal_tie_count=sum(x["feasible"] and x["utility"]==optimum for x in subsets)))
    return rows,dict(model="R332_CONSTRUCTED_THREE_TASK_RESOURCE_E1",
                     source_row_count=len(rows),world_count=len(worlds),worlds=worlds)

def serialized():
    rows,data=generate()
    output=io.StringIO(newline="")
    writer=csv.DictWriter(output,fieldnames=FIELDS,lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue(),json.dumps(data,separators=(",",":"))+"\n"

def replay():
    a,b=serialized()
    assert (ROOT/CSV).read_bytes()==a.encode(),"CSV byte mismatch"
    assert (ROOT/RESULT).read_bytes()==b.encode(),"JSON byte mismatch"

class Tests(unittest.TestCase):
    def test_counts(self):
        rows,data=generate()
        self.assertEqual((len(rows),len(data["worlds"])),(112,14))
    def test_baseline(self):
        self.assertEqual([enumerate_world(0,c)[2] for c in range(7)],[0,1,3,4,5,7,8])
    def test_recoding(self):
        self.assertEqual([enumerate_world(1,c)[2] for c in range(7)],[0,3,4,4,7,8,8])
    def test_gains(self):
        self.assertEqual([enumerate_world(1,c)[2]-enumerate_world(0,c)[2] for c in range(7)],[0,2,1,0,2,1,0])
    def test_counterexamples(self):
        self.assertEqual(enumerate_world(0,4)[1:],("101",5))
        self.assertEqual(enumerate_world(1,4)[1:],("011",7))
        self.assertEqual(enumerate_world(0,3)[1:],("001",4))
        self.assertEqual(enumerate_world(1,3)[1:],("001",4))
    def test_feasible_and_monotonic(self):
        for r in (0,1):
            v=[]
            for c in range(7):
                subsets,chosen,u=enumerate_world(r,c)
                self.assertEqual(len(subsets),8)
                self.assertEqual(sum(x["bits"]==chosen for x in subsets),1)
                self.assertTrue(any(x["bits"]==chosen and x["feasible"] and x["utility"]==u for x in subsets))
                v.append(u)
            self.assertTrue(all(v[i+1]>=v[i] for i in range(6)))
    def test_byte_replay(self):
        replay()

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true")
    p.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        if not result.wasSuccessful():raise SystemExit(1)
    if args.audit:
        replay()
        print("R332 source byte replay PASS: 112 artificial subsets, 14 worlds")
    if not (args.test or args.audit):print(serialized()[1])
