#!/usr/bin/env python3
"""R258 S54: exhaustive coarse-state control on original six-bit source design.

Only E1 artificial finite control. This script reconstructs the frozen six-bit
design mathematically; it does not assert that original CSV bytes were read.
The independent B forward-distribution oracle was committed first.
"""
from __future__ import annotations
import argparse
import itertools
import json
import unittest
from fractions import Fraction as F

# p numerator over 4, kappa numerator over 4, terminal weight
WORLDS={
 "NO_SHOCK_EXPENSIVE":(0,8,1),
 "NO_SHOCK_CHEAP":(0,1,1),
 "HALF_SHOCK_LOW_ACTION":(2,1,1),
 "HALF_SHOCK_MEDIUM":(2,4,1),
 "HALF_SHOCK_HIGH":(2,16,1),
 "QUARTER_SHOCK_MEDIUM":(1,4,1),
 "THREEQUARTER_SHOCK_MEDIUM":(3,4,1),
 "ALWAYS_SHOCK_MEDIUM":(4,4,1),
 "HALF_SHOCK_NO_TERMINAL":(2,4,0)
}
BASELINE={
 "NO_SHOCK_EXPENSIVE":(("0","3","9"),("0","3","9")),
 "NO_SHOCK_CHEAP":(("0","5/4","11/2"),("0","5/4","11/2")),
 "HALF_SHOCK_LOW_ACTION":(("3/4","21/8","77/8"),("3/4","21/8","77/8")),
 "HALF_SHOCK_MEDIUM":(("5/2","9/2","47/4"),("5/2","19/4","95/8")),
 "HALF_SHOCK_HIGH":(("35/8","75/8","16"),("35/8","75/8","16")),
 "QUARTER_SHOCK_MEDIUM":(("5/4","13/4","293/32"),("53/32","117/32","603/64")),
 "THREEQUARTER_SHOCK_MEDIUM":(("11/4","45/8","949/64"),("11/4","367/64","959/64")),
 "ALWAYS_SHOCK_MEDIUM":(("3","7","16"),("3","7","16")),
 "HALF_SHOCK_NO_TERMINAL":(("3/2","7/2","10"),("3/2","15/4","10"))
}
POLICIES=tuple(itertools.product((0,1),repeat=6))
SOURCE_BITS=tuple(itertools.product((0,1),repeat=6))

def sensor(sensor_id,x):
    if sensor_id=="A":return int(x>=1)
    if sensor_id=="B":return int(x==2)
    raise ValueError("unknown sensor")

def exact_path_cost_quarters(world,x0,sensor_id,policy,bits):
    p4,k4,tau=WORLDS[world]
    x=x0
    total=0
    for t in range(3):
        u=policy[2*t+sensor(sensor_id,x)]
        total+=4*x*x+k4*u
        pair=2*bits[2*t]+bits[2*t+1]
        d=int(pair<p4)
        x=max(0,min(2,x+d-u))
    return total+4*tau*x*x

def expected_cost(world,x0,sensor_id,policy):
    # 64 independent equiprobable six-bit sources, quarter-cost integer units.
    total=sum(exact_path_cost_quarters(world,x0,sensor_id,policy,b)
              for b in SOURCE_BITS)
    return F(total,256)

def results():
    rows=[]
    for world in WORLDS:
        for x0 in range(3):
            full=F(BASELINE[world][0][x0])
            opened=F(BASELINE[world][1][x0])
            row={"world":world,"x0":x0,"V_full":str(full),"V_open":str(opened)}
            for sensor_id in ("A","B"):
                costs=[expected_cost(world,x0,sensor_id,p) for p in POLICIES]
                value=min(costs)
                if not full<=value<=opened:raise AssertionError("policy information nesting")
                row["V_"+sensor_id]=str(value)
                row["gap_"+sensor_id]=str(value-full)
                row["open_minus_"+sensor_id]=str(opened-value)
                row["minimizer_count_"+sensor_id]=sum(v==value for v in costs)
            rows.append(row)
    assert len(rows)==27
    return rows

def receipt():
    rows=results()
    return {
      "research_id":"R258","stage":"S54",
      "evidence":"E1_ARTIFICIAL_ONLY",
      "frozen_original_R258_protocol_commit":"62b3cff2023ec7f4d0a35dbb408a6b24c8d6f5ae",
      "source_method":"64_reconstructed_sixbit_atoms_per_world_x0_no_original_CSV_byte_read",
      "world_count":9,"initial_states_per_world":3,
      "total_source_types":1728,"policy_count_per_sensor":64,
      "sensor_A_positive_gap_count":sum(F(r["gap_A"])>0 for r in rows),
      "sensor_B_positive_gap_count":sum(F(r["gap_B"])>0 for r in rows),
      "sensor_A_zero_gap_count":sum(F(r["gap_A"])==0 for r in rows),
      "sensor_B_zero_gap_count":sum(F(r["gap_B"])==0 for r in rows),
      "new_human_E2":0,"new_historical_E3":0,
      "external_independent_reproduction":0,
      "R073":"FROZEN","PESEN_v0_1":"FROZEN",
      "results":rows
    }

class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_policy_count(self):self.assertEqual(len(set(POLICIES)),64)
    def test_source_count(self):self.assertEqual(len(set(SOURCE_BITS)),64)
    def test_sensor_A(self):self.assertEqual([sensor("A",i) for i in range(3)],[0,1,1])
    def test_sensor_B(self):self.assertEqual([sensor("B",i) for i in range(3)],[0,0,1])
    def test_reject_sensor(self):
        with self.assertRaises(ValueError):sensor("invalid",1)
    def test_coverage(self):
        r=receipt()
        self.assertEqual(len(r["results"]),27)
        self.assertEqual(len({(v["world"],v["x0"]) for v in r["results"]}),27)
    def test_cost_zero(self):
        self.assertEqual(expected_cost("NO_SHOCK_EXPENSIVE",0,"A",POLICIES[0]),F(0))

def main():
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["r258_s54"],verbosity=2)
    else:print(json.dumps(receipt(),indent=2,ensure_ascii=False))

if __name__=="__main__":main()
