#!/usr/bin/env python3
"""R325 finite project-created statewise regret comparison; artificial E1 only."""
from __future__ import annotations
import argparse
import csv
import io
import itertools
import json
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
CSV=HERE/"R325_ALL_1029_ARTIFICIAL_REGRET_STATES.csv"
RESULT=HERE/"R325_EXACT_THREE_REGRET_WORLDS.json"
FIELDS=("world_id","policy","kappa","d1","d2","d3","weight","eu_advantage","regret_advantage","choice")
VALUES=tuple(range(-3,4))
STATES=tuple(itertools.product(VALUES,repeat=3))
WORLDS=(("linear_eu",F(0)),("mild_cubic",F(1,4)),("strong_cubic",F(1)))

def q(d,kappa):
    if not isinstance(d,int) or d not in VALUES or kappa<0:
        raise ValueError("invalid statewise difference or coefficient")
    return F(d)+kappa*d**3

def advantage(ds,kappa):
    if len(ds)!=3:
        raise ValueError("expected three states")
    return sum((q(d,kappa) for d in ds),F(0))/3

def sign(x):
    return "A" if x>0 else "B" if x<0 else "TIE"

def generate():
    rows=[];worlds=[]
    for world_id,(name,kappa) in enumerate(WORLDS):
        counts={"A":0,"B":0,"TIE":0}; reversals=0
        for ds in STATES:
            eu=F(sum(ds),3); reg=advantage(ds,kappa)
            choice=sign(reg);counts[choice]+=1
            reversals+=int(eu*reg<0)
            rows.append(dict(zip(FIELDS,map(str,(world_id,name,kappa,*ds,F(1,343),eu,reg,choice)))))
        worlds.append({"world_id":world_id,"policy":name,"kappa":str(kappa),
            "state_count":343,"total_weight":"1","choice_A":counts["A"],
            "choice_B":counts["B"],"choice_TIE":counts["TIE"],
            "strict_eu_regret_reversals":reversals,
            "witness_regret_advantage":str(advantage((3,-2,-2),kappa))})
    witness={"difference_vector":[3,-2,-2],"eu_advantage":"-1/3",
        "linear_regret_advantage":"-1/3","mild_regret_advantage":"7/12",
        "strong_regret_advantage":"10/3",
        "mild_strict_reversal":advantage((3,-2,-2),F(1,4))>0,
        "strong_strict_reversal":advantage((3,-2,-2),F(1))>0,
        "sign_symmetry_all":all(advantage(tuple(-x for x in ds),k)==-advantage(ds,k) for _,k in WORLDS for ds in STATES)}
    obj={"schema":"r325_constructed_statewise_regret_cubic_e1_v1",
        "original_catalogue_id":"01-020","artificial_only":True,
        "original_source_rows":1029,"worlds":worlds,"witness":witness}
    return rows,obj

def csv_text(rows):
    stream=io.StringIO(newline="")
    writer=csv.DictWriter(stream,fieldnames=FIELDS,lineterminator="\n")
    writer.writeheader();writer.writerows(rows)
    return stream.getvalue()

def json_text(obj):
    return json.dumps(obj,indent=2,ensure_ascii=False)+"\n"

def verify_bytes(c,j):
    rows,obj=generate()
    if c!=csv_text(rows):raise AssertionError("CSV mismatch")
    if j!=json_text(obj):raise AssertionError("JSON mismatch")
    return True

def replay():
    return verify_bytes(CSV.read_text(encoding="utf-8"),RESULT.read_text(encoding="utf-8"))

class Tests(unittest.TestCase):
    def test_01_worlds(self):self.assertEqual(len(WORLDS),3)
    def test_02_states(self):self.assertEqual(len(STATES),343)
    def test_03_rows(self):self.assertEqual(len(generate()[0]),1029)
    def test_04_unique(self):self.assertEqual(len({tuple(r[k] for k in FIELDS[:6]) for r in generate()[0]}),1029)
    def test_05_weight(self):self.assertTrue(all(r["weight"]=="1/343" for r in generate()[0]))
    def test_06_mass(self):
        for i in range(3):
            self.assertEqual(sum([F(r["weight"]) for r in generate()[0] if r["world_id"]==str(i)]),F(1))
    def test_07_q_linear(self):
        for d in VALUES:self.assertEqual(q(d,F(0)),d)
    def test_08_q_odd(self):
        for _,k in WORLDS:
            for d in VALUES:self.assertEqual(q(-d,k),-q(d,k))
    def test_09_q_increasing(self):
        for _,k in WORLDS:
            self.assertTrue(all(q(x,k)<q(y,k) for x,y in zip(VALUES,VALUES[1:])))
    def test_10_witness_eu(self):self.assertEqual(F(sum((3,-2,-2)),3),F(-1,3))
    def test_11_witness_linear(self):self.assertEqual(advantage((3,-2,-2),F(0)),F(-1,3))
    def test_12_witness_mild(self):self.assertEqual(advantage((3,-2,-2),F(1,4)),F(7,12))
    def test_13_witness_strong(self):self.assertEqual(advantage((3,-2,-2),F(1)),F(10,3))
    def test_14_linear_all(self):
        for ds in STATES:self.assertEqual(advantage(ds,F(0)),F(sum(ds),3))
    def test_15_linear_reversals(self):self.assertEqual(generate()[1]["worlds"][0]["strict_eu_regret_reversals"],0)
    def test_16_positive_reversals(self):
        for w in generate()[1]["worlds"][1:]:self.assertGreater(w["strict_eu_regret_reversals"],0)
    def test_17_symmetry(self):self.assertTrue(generate()[1]["witness"]["sign_symmetry_all"])
    def test_18_choice_counts(self):
        for w in generate()[1]["worlds"]:self.assertEqual(w["choice_A"]+w["choice_B"]+w["choice_TIE"],343)
    def test_19_invalid_d(self):
        with self.assertRaises(ValueError):q(4,F(1))
    def test_20_invalid_k(self):
        with self.assertRaises(ValueError):q(1,F(-1))
    def test_21_invalid_length(self):
        with self.assertRaises(ValueError):advantage((1,2),F(0))
    def test_22_replay(self):self.assertTrue(replay())
    def test_23_csv_mutation(self):
        c=csv_text(generate()[0]);j=json_text(generate()[1])
        with self.assertRaises(AssertionError):verify_bytes(c.replace("1/343","1/342",1),j)
    def test_24_json_mutation(self):
        c=csv_text(generate()[0]);j=json_text(generate()[1])
        with self.assertRaises(AssertionError):verify_bytes(c,j.replace('"original_source_rows": 1029','"original_source_rows": 1028'))
    def test_25_zero(self):
        for _,k in WORLDS:self.assertEqual(advantage((0,0,0),k),F(0))
    def test_26_meta(self):self.assertEqual(generate()[1]["original_catalogue_id"],"01-020")

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
        print("R325_GENERATED",len(rows))
    elif args.audit:
        print("R325_REPLAY_PASS",replay())
    elif args.test:
        unittest.main(argv=["r325"],verbosity=2)
    else:
        parser.print_help()
