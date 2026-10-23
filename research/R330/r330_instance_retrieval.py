#!/usr/bin/env python3
"""R330 exact finite cue and recency instance retrieval. Standard library only."""
import argparse
import csv
import io
import json
import unittest
from fractions import Fraction as F
from itertools import product
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CSV="R330_ALL_256_ARTIFICIAL_MEMORY_ATOMS.csv"
RESULT="R330_EXACT_64_RETRIEVAL_WORLDS.json"
FIELDS=["history","query_cue","decay","time","action","instance_cue","utility","weight","action_score","chosen_action"]
INSTANCES=((1,"A",0),(2,"B",1),(3,"A",1),(4,"B",0))

def solve(history,cue,decay):
    memories=[]
    for i,(time,action,instance_cue) in enumerate(INSTANCES):
        weight=(F(1) if cue==instance_cue else F(1,2))*F(1,5-time)**decay
        memories.append((time,action,instance_cue,history[i],weight))
    scores={}
    for action in ("A","B"):
        matching=[m for m in memories if m[1]==action]
        scores[action]=sum((m[4]*m[3] for m in matching),F(0))/sum((m[4] for m in matching),F(0))
    chosen="A" if scores["A"]>=scores["B"] else "B"
    return memories,scores,chosen

def generate():
    rows,worlds=[],[]
    for history in product((0,1),repeat=4):
        label="".join(map(str,history))
        for cue in (0,1):
            for decay in (0,1):
                memories,scores,chosen=solve(history,cue,decay)
                worlds.append(dict(history=label,query_cue=cue,decay=decay,
                                   score_a=str(scores["A"]),score_b=str(scores["B"]),chosen_action=chosen))
                for time,action,instance_cue,utility,weight in memories:
                    rows.append(dict(history=label,query_cue=str(cue),decay=str(decay),
                                     time=str(time),action=action,instance_cue=str(instance_cue),
                                     utility=str(utility),weight=str(weight),
                                     action_score=str(scores[action]),chosen_action=chosen))
    return rows,dict(model="R330_CONSTRUCTED_CUE_RECENCY_INSTANCE_RETRIEVAL_E1",
                     source_row_count=256,world_count=64,worlds=worlds)

def serialized():
    rows,result=generate()
    buffer=io.StringIO(newline="")
    writer=csv.DictWriter(buffer,fieldnames=FIELDS,lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue(),json.dumps(result,sort_keys=True,separators=(",",":"))+"\n"

def replay():
    a,b=serialized()
    assert (ROOT/CSV).read_bytes()==a.encode(), "CSV byte mismatch"
    assert (ROOT/RESULT).read_bytes()==b.encode(), "JSON byte mismatch"

class Tests(unittest.TestCase):
    def test_count(self):
        rows,result=generate()
        self.assertEqual((len(rows),len(result["worlds"])),(256,64))
    def test_score_range(self):
        for h in product((0,1),repeat=4):
            for z in (0,1):
                for d in (0,1):
                    memories,scores,chosen=solve(h,z,d)
                    self.assertTrue(all(m[4]>0 for m in memories))
                    self.assertTrue(all(F(0)<=v<=F(1) for v in scores.values()))
                    self.assertEqual(chosen,"A" if scores["A"]>=scores["B"] else "B")
    def test_recency_counterexample(self):
        _,s0,a0=solve((1,0,0,1),0,0)
        _,s1,a1=solve((1,0,0,1),0,1)
        self.assertEqual((s0["A"],s0["B"],a0),(F(2,3),F(2,3),"A"))
        self.assertEqual((s1["A"],s1["B"],a1),(F(1,2),F(6,7),"B"))
    def test_cue_counterexample(self):
        _,s0,a0=solve((1,1,0,0),0,0)
        _,s1,a1=solve((1,1,0,0),1,0)
        self.assertEqual((s0["A"],s0["B"],a0),(F(2,3),F(1,3),"A"))
        self.assertEqual((s1["A"],s1["B"],a1),(F(1,3),F(2,3),"B"))
    def test_zero_outcomes(self):
        for z in (0,1):
            for d in (0,1):
                _,s,a=solve((0,0,0,0),z,d)
                self.assertEqual((s["A"],s["B"],a),(F(0),F(0),"A"))
    def test_exact_replay(self):
        replay()

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--generate",action="store_true")
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--audit",action="store_true")
    args=parser.parse_args()
    if args.generate:
        a,b=serialized()
        (ROOT/CSV).write_bytes(a.encode())
        (ROOT/RESULT).write_bytes(b.encode())
        print("generated 256 source rows, 64 worlds")
    if args.audit:
        replay()
        print("R330 exact byte replay PASS")
    if args.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        if not result.wasSuccessful():raise SystemExit(1)
