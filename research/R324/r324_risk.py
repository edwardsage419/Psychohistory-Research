#!/usr/bin/env python3
"""R324: constructed two-axis psychometric risk arithmetic, bounded E1 only."""
from __future__ import annotations
import argparse
import csv
import io
import itertools
import json
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
CSV = HERE / "R324_ALL_64_ARTIFICIAL_RISK_STATES.csv"
RESULT = HERE / "R324_EXACT_FOUR_SCORING_WORLDS.json"
FIELDS = ("world_id","policy","dread1","dread2","unknown1","unknown2","weight","D","U","score")
WORLDS = (("dread_weighted",3,1),("unknown_weighted",1,3),("balanced",1,1),("scaled_balanced",2,2))
STATES = tuple(itertools.product((0,1),repeat=4))

def evaluate(state,a,b):
    if len(state)!=4 or any(x not in (0,1) for x in state):
        raise ValueError("invalid binary descriptor")
    if a<0 or b<0:
        raise ValueError("negative coefficient")
    d=state[0]+state[1]
    u=state[2]+state[3]
    return d,u,a*d+b*u

def generate():
    rows=[]
    worlds=[]
    for world_id,(policy,a,b) in enumerate(WORLDS):
        scores=[]
        for state in STATES:
            d,u,score=evaluate(state,a,b)
            scores.append(score)
            rows.append(dict(zip(FIELDS,map(str,(world_id,policy,*state,F(1,16),d,u,score)))))
        worlds.append({"world_id":world_id,"policy":policy,"a":a,"b":b,
            "state_count":16,"total_weight":"1","min_score":min(scores),
            "max_score":max(scores),"mean_score":str(F(sum(scores),16)),
            "dread_only_score":evaluate((1,1,0,0),a,b)[2],
            "unknown_only_score":evaluate((0,0,1,1),a,b)[2]})
    witness={"dread_only":"1100","unknown_only":"0011",
        "w0_dread_gt_unknown":worlds[0]["dread_only_score"]>worlds[0]["unknown_only_score"],
        "w1_unknown_gt_dread":worlds[1]["unknown_only_score"]>worlds[1]["dread_only_score"],
        "w2_equal":worlds[2]["dread_only_score"]==worlds[2]["unknown_only_score"],
        "w3_double_w2_all_states":all(evaluate(s,2,2)[2]==2*evaluate(s,1,1)[2] for s in STATES)}
    result={"schema":"r324_constructed_two_axis_psychometric_risk_e1_v1",
        "original_catalogue_id":"01-017","artificial_only":True,
        "original_source_rows":64,"worlds":worlds,"witness":witness}
    return rows,result

def csv_text(rows):
    stream=io.StringIO(newline="")
    writer=csv.DictWriter(stream,fieldnames=FIELDS,lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue()

def json_text(result):
    return json.dumps(result,indent=2,ensure_ascii=False)+"\n"

def verify_bytes(csv_bytes,json_bytes):
    rows,result=generate()
    if csv_bytes!=csv_text(rows):
        raise AssertionError("CSV source differs from frozen enumeration")
    if json_bytes!=json_text(result):
        raise AssertionError("JSON exact results differ")
    return True

def replay():
    return verify_bytes(CSV.read_text(encoding="utf-8"),RESULT.read_text(encoding="utf-8"))

class Tests(unittest.TestCase):
    def test_01_worlds(self): self.assertEqual(len(WORLDS),4)
    def test_02_states(self): self.assertEqual(len(STATES),16)
    def test_03_rows(self): self.assertEqual(len(generate()[0]),64)
    def test_04_unique(self): self.assertEqual(len({tuple(r[k] for k in FIELDS[:6]) for r in generate()[0]}),64)
    def test_05_weight(self): self.assertTrue(all(r["weight"]=="1/16" for r in generate()[0]))
    def test_06_mass(self):
        for i in range(4):
            self.assertEqual(sum((F(r["weight"]) for r in generate()[0] if r["world_id"]==str(i)),F(1))
    def test_07_dread_only(self): self.assertEqual(evaluate((1,1,0,0),3,1),(2,0,6))
    def test_08_unknown_only(self): self.assertEqual(evaluate((0,0,1,1),3,1),(0,2,2))
    def test_09_reverse(self): self.assertEqual(evaluate((1,1,0,0),1,3)[2],2)
    def test_10_reverse_unknown(self): self.assertEqual(evaluate((0,0,1,1),1,3)[2],6)
    def test_11_tie(self): self.assertEqual(evaluate((1,1,0,0),1,1)[2],evaluate((0,0,1,1),1,1)[2])
    def test_12_scaling(self):
        for state in STATES: self.assertEqual(evaluate(state,2,2)[2],2*evaluate(state,1,1)[2])
    def test_13_all_zero(self):
        for _,a,b in WORLDS: self.assertEqual(evaluate((0,0,0,0),a,b),(0,0,0))
    def test_14_all_one(self):
        for _,a,b in WORLDS: self.assertEqual(evaluate((1,1,1,1),a,b)[2],2*a+2*b)
    def test_15_min(self): self.assertTrue(all(w["min_score"]==0 for w in generate()[1]["worlds"]))
    def test_16_means(self): self.assertEqual([w["mean_score"] for w in generate()[1]["worlds"]],["4","4","2","4"])
    def test_17_witness(self): self.assertTrue(all(generate()[1]["witness"][k] for k in ("w0_dread_gt_unknown","w1_unknown_gt_dread","w2_equal","w3_double_w2_all_states")))
    def test_18_invalid(self):
        with self.assertRaises(ValueError): evaluate((1,2,0,0),1,1)
    def test_19_invalid_coeff(self):
        with self.assertRaises(ValueError): evaluate((1,0,0,0),-1,1)
    def test_20_replay(self): self.assertTrue(replay())
    def test_21_csv_mutation(self):
        c=csv_text(generate()[0]); j=json_text(generate()[1])
        with self.assertRaises(AssertionError): verify_bytes(c.replace("1/16","1/8",1),j)
    def test_22_json_mutation(self):
        c=csv_text(generate()[0]); j=json_text(generate()[1])
        with self.assertRaises(AssertionError): verify_bytes(c,j.replace('"original_source_rows": 64','"original_source_rows": 65'))
    def test_23_meta(self): self.assertEqual(generate()[1]["original_catalogue_id"],"01-017")
    def test_24_scores_nonnegative(self): self.assertTrue(all(int(r["score"])>=0 for r in generate()[0]))
    def test_25_all_axes(self): self.assertEqual({int(r["D"]) for r in generate()[0]},{0,1,2})
    def test_26_all_unknown(self): self.assertEqual({int(r["U"]) for r in generate()[0]},{0,1,2})

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--write",action="store_true")
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--audit",action="store_true")
    args=parser.parse_args()
    if args.write:
        rows,obj=generate()
        CSV.write_text(csv_text(rows),encoding="utf-8")
        RESULT.write_text(json_text(obj),encoding="utf-8")
        print("R324_GENERATED",len(rows))
    elif args.audit:
        print("R324_REPLAY_PASS",replay())
    elif args.test:
        unittest.main(argv=["r324"],verbosity=2)
    else:
        parser.print_help()
