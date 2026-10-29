#!/usr/bin/env python3
"""R258 S54 independent exact state-distribution oracle.

Frozen coarse sensors; independent forward mass propagation rather than
original six-bit trajectory simulation. Source: R258 S54 protocol.
This script was written and committed before viewing S54 R-route outputs.
The original R258 baseline was read in advance: this is not fully blind.
"""
from __future__ import annotations
import argparse
import itertools
import json
import unittest
from fractions import Fraction as F

CONFIG = {
 "NO_SHOCK_EXPENSIVE": (F(0),F(2),F(1)),
 "NO_SHOCK_CHEAP": (F(0),F(1,4),F(1)),
 "HALF_SHOCK_LOW_ACTION": (F(1,2),F(1,4),F(1)),
 "HALF_SHOCK_MEDIUM": (F(1,2),F(1),F(1)),
 "HALF_SHOCK_HIGH": (F(1,2),F(4),F(1)),
 "QUARTER_SHOCK_MEDIUM": (F(1,4),F(1),F(1)),
 "THREEQUARTER_SHOCK_MEDIUM": (F(3,4),F(1),F(1)),
 "ALWAYS_SHOCK_MEDIUM": (F(1),F(1),F(1)),
 "HALF_SHOCK_NO_TERMINAL": (F(1,2),F(1),F(0))
}
EXPECTED_FULL = {
 "NO_SHOCK_EXPENSIVE": ("0","3","9"),
 "NO_SHOCK_CHEAP": ("0","5/4","11/2"),
 "HALF_SHOCK_LOW_ACTION": ("3/4","21/8","77/8"),
 "HALF_SHOCK_MEDIUM": ("5/2","9/2","47/4"),
 "HALF_SHOCK_HIGH": ("35/8","75/8","16"),
 "QUARTER_SHOCK_MEDIUM": ("5/4","13/4","293/32"),
 "THREEQUARTER_SHOCK_MEDIUM": ("11/4","45/8","949/64"),
 "ALWAYS_SHOCK_MEDIUM": ("3","7","16"),
 "HALF_SHOCK_NO_TERMINAL": ("3/2","7/2","10")
}
EXPECTED_OPEN = {
 "NO_SHOCK_EXPENSIVE": ("0","3","9"),
 "NO_SHOCK_CHEAP": ("0","5/4","11/2"),
 "HALF_SHOCK_LOW_ACTION": ("3/4","21/8","77/8"),
 "HALF_SHOCK_MEDIUM": ("5/2","19/4","95/8"),
 "HALF_SHOCK_HIGH": ("35/8","75/8","16"),
 "QUARTER_SHOCK_MEDIUM": ("53/32","117/32","603/64"),
 "THREEQUARTER_SHOCK_MEDIUM": ("11/4","367/64","959/64"),
 "ALWAYS_SHOCK_MEDIUM": ("3","7","16"),
 "HALF_SHOCK_NO_TERMINAL": ("3/2","15/4","10")
}
POLICIES = tuple(itertools.product((0,1), repeat=6))

def sensor_value(sensor, state):
    if sensor == "A": return int(state >= 1)
    if sensor == "B": return int(state == 2)
    raise ValueError("unknown frozen sensor")

def evaluate_distribution(config, x0, sensor, policy):
    p, kappa, tau = config
    if len(policy) != 6 or any(u not in (0,1) for u in policy):
        raise ValueError("invalid policy")
    mass = {x0:F(1)}
    cost = F(0)
    for t in range(3):
        next_mass = {}
        for x, weight in mass.items():
            action = policy[2*t + sensor_value(sensor,x)]
            cost += weight*(x*x + kappa*action)
            for shock, shock_prob in ((0,1-p),(1,p)):
                xnew = max(0,min(2,x + shock - action))
                next_mass[xnew] = next_mass.get(xnew,F(0)) + weight*shock_prob
        if sum(next_mass.values(),F(0)) != 1:
            raise AssertionError("mass conservation failure")
        mass = next_mass
    return cost + sum((weight*tau*x*x for x,weight in mass.items()),F(0))

def results():
    out=[]
    for name, config in CONFIG.items():
        for x0 in range(3):
            full=F(EXPECTED_FULL[name][x0])
            opened=F(EXPECTED_OPEN[name][x0])
            row={"world":name,"x0":x0,"V_full":str(full),"V_open":str(opened)}
            for sensor in ("A","B"):
                vals=[evaluate_distribution(config,x0,sensor,pol) for pol in POLICIES]
                best=min(vals)
                if not full <= best <= opened:
                    raise AssertionError("nested policy class ordering violated")
                row["V_"+sensor]=str(best)
                row["gap_"+sensor]=str(best-full)
                row["open_minus_"+sensor]=str(opened-best)
                row["minimizer_count_"+sensor]=sum(v==best for v in vals)
            out.append(row)
    assert len(out)==27
    return out

class Tests(unittest.TestCase):
    def test_worlds(self): self.assertEqual(len(CONFIG),9)
    def test_policy_unique(self): self.assertEqual(len(POLICIES),64)
    def test_policy_shape(self): self.assertTrue(all(len(x)==6 for x in POLICIES))
    def test_sensor_partition(self):
        self.assertEqual([sensor_value("A",x) for x in range(3)],[0,1,1])
        self.assertEqual([sensor_value("B",x) for x in range(3)],[0,0,1])
    def test_invalid_sensor(self):
        with self.assertRaises(ValueError): sensor_value("C",0)
    def test_mass_and_27_coverage(self):
        r=results()
        self.assertEqual(len({(v["world"],v["x0"]) for v in r}),27)
    def test_no_shock_nonnegative(self):
        self.assertGreaterEqual(evaluate_distribution(CONFIG["NO_SHOCK_CHEAP"],0,"A",POLICIES[0]),0)

def main():
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--emit",action="store_true")
    group.add_argument("--test",action="store_true")
    args=parser.parse_args()
    if args.test: unittest.main(argv=["r258_s54_b"],verbosity=2)
    else:
        print(json.dumps({"research_id":"R258","stage":"S54","method":"independent_forward_state_mass",
                          "source":"frozen_R258_math_no_original_CSV_byte_read",
                          "results":results()},indent=2))

if __name__ == "__main__": main()
