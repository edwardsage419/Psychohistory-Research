#!/usr/bin/env python3
"""R327 exact 72-path artificial finite POMDP. Standard library only."""
import argparse
import csv
import io
import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = ["belief","accuracy","hidden","observation","joint_mass","observation_mass","posterior_h1","terminal_guess","terminal_expected_reward","sense_value","immediate_value","optimal_value","chosen_action"]
CSV = "R327_ALL_72_ARTIFICIAL_HIDDEN_OBSERVATION_PATHS.csv"
RESULT = "R327_EXACT_18_BELIEF_WORLDS.json"


def joint(b, q, y):
    return ((1-b)*(q if y == 0 else 1-q), b*(q if y == 1 else 1-q))


def solve(b, q):
    immediate = max(b, 1-b)
    sense = sum(max(joint(b, q, y)) for y in (0, 1)) - F(1,8)
    action = "SENSE" if sense > immediate else ("GUESS_1" if b > F(1,2) else "GUESS_0")
    return dict(belief=str(b), accuracy=str(q), immediate_value=str(immediate),
                sense_value=str(sense), optimal_value=str(max(immediate,sense)),
                chosen_action=action)


def generate():
    rows, worlds = [], []
    for q in (F(1,2),F(3,4)):
        for k in range(9):
            b = F(k,8)
            w = solve(b,q)
            worlds.append(w)
            for h in (0,1):
                for y in (0,1):
                    p0,p1 = joint(b,q,y)
                    obs = p0+p1
                    rows.append(dict(
                        belief=str(b),accuracy=str(q),hidden=str(h),observation=str(y),
                        joint_mass=str(p1 if h else p0),observation_mass=str(obs),
                        posterior_h1=str(p1/obs) if obs else "NULL",
                        terminal_guess=("1" if p1>p0 else "0") if obs else "NULL",
                        terminal_expected_reward=str(max(p0,p1)/obs) if obs else "NULL",
                        sense_value=w["sense_value"],immediate_value=w["immediate_value"],
                        optimal_value=w["optimal_value"],chosen_action=w["chosen_action"]))
    return rows, dict(model="R327_FINITE_TWO_STATE_ONE_SENSE_POMDP_E1",
                      source_row_count=72,world_count=18,worlds=worlds)


def serialized():
    rows, result = generate()
    output = io.StringIO(newline="")
    writer = csv.DictWriter(output,fieldnames=FIELDS,lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue(), json.dumps(result,sort_keys=True,separators=(",",":"))+"\n"


def verify():
    csv_bytes,json_bytes = serialized()
    assert (ROOT/CSV).read_bytes()==csv_bytes.encode(), "CSV byte mismatch"
    assert (ROOT/RESULT).read_bytes()==json_bytes.encode(), "JSON byte mismatch"


class Checks(unittest.TestCase):
    def test_size(self):
        rows,result=generate()
        self.assertEqual((len(rows),len(result["worlds"])),(72,18))

    def test_mass(self):
        for q in (F(1,2),F(3,4)):
            for k in range(9):
                b=F(k,8)
                self.assertEqual(sum(sum(joint(b,q,y)) for y in (0,1)),1)

    def test_bayes(self):
        for q in (F(1,2),F(3,4)):
            for k in range(9):
                for y in (0,1):
                    p0,p1=joint(F(k,8),q,y)
                    if p0+p1:
                        self.assertEqual(p0/(p0+p1)+p1/(p0+p1),1)

    def test_signal(self):
        self.assertEqual(solve(F(1,2),F(3,4))["sense_value"],"5/8")
        self.assertEqual(solve(F(1,2),F(3,4))["chosen_action"],"SENSE")

    def test_no_information(self):
        self.assertEqual(solve(F(1,2),F(1,2))["sense_value"],"3/8")
        self.assertEqual(solve(F(1,2),F(1,2))["chosen_action"],"GUESS_0")

    def test_high_prior(self):
        self.assertEqual(solve(F(3,4),F(3,4))["sense_value"],"5/8")
        self.assertEqual(solve(F(3,4),F(3,4))["chosen_action"],"GUESS_1")

    def test_cost(self):
        for k in range(9):
            b=F(k,8)
            self.assertEqual(F(solve(b,F(1,2))["sense_value"]),max(b,1-b)-F(1,8))

    def test_replay(self):
        verify()


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--generate",action="store_true")
    p.add_argument("--test",action="store_true")
    p.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.generate:
        csv_data,json_data=serialized()
        (ROOT/CSV).write_bytes(csv_data.encode())
        (ROOT/RESULT).write_bytes(json_data.encode())
        print("generated 72 source paths and 18 worlds")
    if a.audit:
        verify()
        print("exact byte replay PASS")
    if a.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Checks))
        if not result.wasSuccessful():
            raise SystemExit(1)


if __name__=="__main__":
    main()
