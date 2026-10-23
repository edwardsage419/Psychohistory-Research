#!/usr/bin/env python3
"""R320: finite six-step two-boundary walk, only a discrete DDM analogue (E1)."""
from __future__ import annotations
import argparse
import csv
import io
import itertools
import json
import unittest
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/"R320_ALL_384_ORIGINAL_SIX_STEP_PATHS.csv"
RESULT=ROOT/"R320_EXACT_6_FIRST_HIT_WORLDS.json"
BOUNDS=(4,6)
PS=(Fraction(1,4),Fraction(1,2),Fraction(3,4))
T=6
FIELDS=("world_id","upper_bound","start","p_up","path_bits","up_steps","down_steps",
        "full_path_probability","first_hit_time","first_hit_side","censored")

def first_hit(upper, bits):
    if upper not in BOUNDS or len(bits)!=T or any(bit not in (0,1) for bit in bits):
        raise ValueError("invalid frozen walk grid")
    x=upper//2
    for t,bit in enumerate(bits,1):
        x+=1 if bit==1 else -1
        if x==0:return t,"lower"
        if x==upper:return t,"upper"
    return None,"none"

def path_mass(p,bits):
    if p not in PS or not isinstance(p,Fraction) or len(bits)!=T or any(b not in (0,1) for b in bits):
        raise ValueError("invalid frozen Bernoulli source")
    ups=sum(bits)
    return p**ups*(1-p)**(T-ups)

def generate():
    rows=[]; worlds=[]
    for upper in BOUNDS:
        for p in PS:
            world_id=len(worlds)
            hit={(t,side):Fraction(0) for t in range(1,T+1) for side in ("lower","upper")}
            survival=Fraction(0); weighted_time=Fraction(0); truncated=Fraction(0)
            for bits in itertools.product((0,1),repeat=T):
                prob=path_mass(p,bits)
                t,side=first_hit(upper,bits)
                censored=t is None
                if censored: survival+=prob
                else:
                    hit[(t,side)]+=prob
                    weighted_time+=t*prob
                truncated+=(T if censored else t)*prob
                rows.append(dict(zip(FIELDS,map(str,(
                    world_id,upper,upper//2,p,"".join(map(str,bits)),sum(bits),
                    T-sum(bits),prob,"" if censored else t,side,
                    str(censored).lower())))))
            total_hit=sum(hit.values(),Fraction(0))
            worlds.append({
                "world_id":world_id,"upper_bound":upper,"start":upper//2,
                "p_up":str(p),
                "hit_by_time_and_side":[{"time":t,"lower":str(hit[(t,"lower")]),
                                         "upper":str(hit[(t,"upper")])}
                                        for t in range(1,T+1)],
                "survival":str(survival),"hit_total":str(total_hit),
                "conditional_mean_decision_steps_among_hits":str(weighted_time/total_hit),
                "expected_truncated_steps":str(truncated)})
    return rows,{"schema":"r320_six_step_absorbing_walk_ddm_analogue_e1_v1",
                 "original_catalogue_id":"01-009","discrete_analogue_only":True,
                 "original_path_source_rows":len(rows),"world_count":len(worlds),
                 "horizon":T,"worlds":worlds}

def csv_text(rows):
    f=io.StringIO(newline="")
    w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n")
    w.writeheader();w.writerows(rows)
    return f.getvalue()

def json_text(obj):
    return json.dumps(obj,indent=2,ensure_ascii=False)+"\n"

def verify_source(csv_data,json_data):
    rows,obj=generate()
    if csv_data!=csv_text(rows):raise AssertionError("R320 path-source bytes differ")
    if json.loads(json_data)!=obj:raise AssertionError("R320 first-hit summary differs")
    return True

def replay():
    return verify_source(SOURCE.read_text(encoding="utf-8"),
                         RESULT.read_text(encoding="utf-8"))

def world(upper,p):
    return next(w for w in generate()[1]["worlds"] if w["upper_bound"]==upper and w["p_up"]==str(p))

class WalkTests(unittest.TestCase):
    def test_01_bounds(self):self.assertEqual(BOUNDS,(4,6))
    def test_02_ps(self):self.assertEqual(len(PS),3)
    def test_03_horizon(self):self.assertEqual(T,6)
    def test_04_worlds(self):self.assertEqual(len(generate()[1]["worlds"]),6)
    def test_05_rows(self):self.assertEqual(len(generate()[0]),384)
    def test_06_paths_unique(self):
        rows,_=generate()
        self.assertEqual(len({(r["world_id"],r["path_bits"]) for r in rows}),384)
    def test_07_mass_per_world(self):
        for w in generate()[1]["worlds"]:
            p=Fraction(w["p_up"])
            self.assertEqual(sum(path_mass(p,bits) for bits in itertools.product((0,1),repeat=T)),1)
    def test_08_hit_survival_sum(self):
        for w in generate()[1]["worlds"]:
            self.assertEqual(Fraction(w["hit_total"])+Fraction(w["survival"]),1)
    def test_09_witness_survival(self):
        self.assertEqual(Fraction(world(4,Fraction(1,2))["survival"]),Fraction(1,8))
    def test_10_witness_hit(self):
        self.assertEqual(Fraction(world(4,Fraction(1,2))["hit_total"]),Fraction(7,8))
    def test_11_witness_each_side(self):
        w=world(4,Fraction(1,2))
        for side in ("lower","upper"):
            self.assertEqual(sum((Fraction(t[side]) for t in w["hit_by_time_and_side"]),Fraction(0)),Fraction(7,16))
    def test_12_symmetric_half(self):
        for a in BOUNDS:
            w=world(a,Fraction(1,2))
            for t in w["hit_by_time_and_side"]:self.assertEqual(t["lower"],t["upper"])
    def test_13_type_complement(self):
        for a in BOUNDS:
            lo=world(a,Fraction(1,4));hi=world(a,Fraction(3,4))
            self.assertEqual(lo["survival"],hi["survival"])
            for x,y in zip(lo["hit_by_time_and_side"],hi["hit_by_time_and_side"]):
                self.assertEqual(x["lower"],y["upper"])
                self.assertEqual(x["upper"],y["lower"])
    def test_14_wider_survival(self):
        self.assertGreater(Fraction(world(6,Fraction(1,2))["survival"]),
                           Fraction(world(4,Fraction(1,2))["survival"]))
    def test_15_no_t1_hit(self):
        for w in generate()[1]["worlds"]:
            self.assertEqual(w["hit_by_time_and_side"][0]["lower"],"0")
            self.assertEqual(w["hit_by_time_and_side"][0]["upper"],"0")
    def test_16_hit_parity(self):
        for r in generate()[0]:
            if r["first_hit_time"]:
                self.assertEqual(int(r["first_hit_time"])%2,int(r["upper_bound"])//2%2)
    def test_17_zeros_lower(self):
        self.assertEqual(first_hit(4,(0,)*T),(2,"lower"))
    def test_18_ones_upper(self):
        self.assertEqual(first_hit(6,(1,)*T),(3,"upper"))
    def test_19_alternating_censored(self):
        self.assertEqual(first_hit(4,(0,1,0,1,0,1)),(None,"none"))
    def test_20_positive_masses(self):
        self.assertTrue(all(Fraction(r["full_path_probability"])>0 for r in generate()[0]))
    def test_21_no_double_side(self):
        self.assertTrue(all(r["first_hit_side"] in ("lower","upper","none") for r in generate()[0]))
    def test_22_censor_correspondence(self):
        for r in generate()[0]:
            self.assertEqual(r["censored"]=="true",r["first_hit_time"]=="")
    def test_23_conditional_mean(self):
        for w in generate()[1]["worlds"]:
            self.assertTrue(1<=Fraction(w["conditional_mean_decision_steps_among_hits"])<=T)
    def test_24_truncated_mean(self):
        for w in generate()[1]["worlds"]:
            self.assertTrue(1<=Fraction(w["expected_truncated_steps"])<=T)
    def test_25_invalid_upper(self):
        with self.assertRaises(ValueError):first_hit(5,(0,)*T)
    def test_26_invalid_path(self):
        with self.assertRaises(ValueError):first_hit(4,(0,)*5)
    def test_27_invalid_probability(self):
        with self.assertRaises(ValueError):path_mass(Fraction(1,3),(0,)*T)
    def test_28_replay(self):self.assertTrue(replay())
    def test_29_corrupt_rejected(self):
        with self.assertRaises(AssertionError):
            verify_source(csv_text(generate()[0]).replace("1/4096","1/8192",1),
                          json_text(generate()[1]))
    def test_30_all_path_mass_count(self):
        self.assertEqual(len([r for r in generate()[0] if r["world_id"]=="0"]),64)
    def test_31_path_probability_complement(self):
        for bits in itertools.product((0,1),repeat=T):
            comp=tuple(1-b for b in bits)
            self.assertEqual(path_mass(Fraction(1,4),bits),path_mass(Fraction(3,4),comp))
    def test_32_metadata(self):
        obj=generate()[1]
        self.assertTrue(obj["discrete_analogue_only"])
        self.assertEqual(obj["original_catalogue_id"],"01-009")
    def test_33_source_parity(self):
        for r in generate()[0]:
            self.assertEqual(int(r["up_steps"])+int(r["down_steps"]),6)
    def test_34_first_hit_immutable_suffix(self):
        self.assertEqual(first_hit(4,(0,0,0,0,0,0)),first_hit(4,(0,0,1,1,1,1)))
    def test_35_all_summary_cells(self):
        self.assertEqual(sum(len(w["hit_by_time_and_side"]) for w in generate()[1]["worlds"]),36)

if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--generate",action="store_true")
    p.add_argument("--audit",action="store_true")
    p.add_argument("--test",action="store_true")
    args=p.parse_args()
    if args.generate:
        rows,obj=generate()
        SOURCE.write_text(csv_text(rows),encoding="utf-8")
        RESULT.write_text(json_text(obj),encoding="utf-8")
        print("R320_GENERATED",len(rows),len(obj["worlds"]))
    elif args.audit:
        replay();print("R320_REPLAY_PASS 384_PATHS 6_WORLDS")
    else:
        unittest.main(argv=["r320"] if args.test else None)
