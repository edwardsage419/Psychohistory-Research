#!/usr/bin/env python3
"""R329 constructed finite expected-free-energy policy scoring. Standard library only."""
import argparse
import csv
import io
import json
import math
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parent
CSV="R329_ALL_144_ARTIFICIAL_JOINT_ATOMS.csv"
RESULT="R329_EXACT_18_EFE_WORLDS.json"
FIELDS=["belief","preference_one","precise_cost","policy","hidden","observation","likelihood","joint_mass","observation_mass","expected_free_energy","selected_policy"]

def probabilities(b, policy):
    q=F(3,4) if policy=="PRECISE" else F(1,2)
    joint={(s,o):(b if s else 1-b)*(q if s==o else 1-q)
           for s in (0,1) for o in (0,1)}
    obs={o:sum(joint[s,o] for s in (0,1)) for o in (0,1)}
    return q,joint,obs

def scores(b,c,k,policy):
    q,joint,obs=probabilities(b,policy)
    info=sum(float(joint[s,o])*math.log(float((q if s==o else 1-q)/obs[o]))
             for s in (0,1) for o in (0,1))
    extrinsic=sum(float(obs[o])*math.log(float(c if o else 1-c)) for o in (0,1))
    cost=float(k) if policy=="PRECISE" else 0.0
    g=-extrinsic-info+cost
    risk=sum(float(obs[o])*math.log(float(obs[o]/(c if o else 1-c))) for o in (0,1))
    ambiguity=-sum(float(joint[s,o])*math.log(float(q if s==o else 1-q))
                   for s in (0,1) for o in (0,1))
    return g,info,risk+ambiguity+cost

def generate():
    rows,worlds=[],[]
    for b in (F(1,4),F(1,2),F(3,4)):
        for c in (F(1,2),F(3,4)):
            for k in (F(0),F(1,8),F(1,4)):
                precise=scores(b,c,k,"PRECISE")
                noisy=scores(b,c,k,"NOISY")
                choice="PRECISE" if precise[0]<noisy[0]-1e-14 else "NOISY"
                worlds.append(dict(belief=str(b),preference_one=str(c),precise_cost=str(k),
                    chosen_policy=choice,precise_efe=f"{precise[0]:.9f}",
                    noisy_efe=f"{noisy[0]:.9f}",
                    precise_information=f"{precise[1]:.9f}",
                    noisy_information=f"{noisy[1]:.9f}",
                    identity_error=f"{max(abs(precise[0]-precise[2]),abs(noisy[0]-noisy[2])):.12f}"))
                for policy in ("PRECISE","NOISY"):
                    q,joint,obs=probabilities(b,policy)
                    g=scores(b,c,k,policy)[0]
                    for s in (0,1):
                        for o in (0,1):
                            rows.append(dict(belief=str(b),preference_one=str(c),precise_cost=str(k),
                                policy=policy,hidden=str(s),observation=str(o),
                                likelihood=str(q if s==o else 1-q),joint_mass=str(joint[s,o]),
                                observation_mass=str(obs[o]),expected_free_energy=f"{g:.9f}",
                                selected_policy=choice))
    return rows,dict(model="R329_CONSTRUCTED_BINARY_ACTIVE_INFERENCE_E1",
                     source_row_count=144,world_count=18,worlds=worlds)

def serialized():
    rows,result=generate()
    buf=io.StringIO(newline="")
    writer=csv.DictWriter(buf,fieldnames=FIELDS,lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buf.getvalue(),json.dumps(result,sort_keys=True,separators=(",",":"))+"\n"

def replay():
    a,b=serialized()
    assert (ROOT/CSV).read_bytes()==a.encode(), "CSV byte mismatch"
    assert (ROOT/RESULT).read_bytes()==b.encode(), "JSON byte mismatch"

class Tests(unittest.TestCase):
    def test_counts(self):
        rows,result=generate()
        self.assertEqual((len(rows),len(result["worlds"])),(144,18))
    def test_normalization(self):
        for b in (F(1,4),F(1,2),F(3,4)):
            for p in ("PRECISE","NOISY"):
                _,joint,obs=probabilities(b,p)
                self.assertEqual(sum(joint.values()),1)
                self.assertEqual(sum(obs.values()),1)
    def test_identity(self):
        for b in (F(1,4),F(1,2),F(3,4)):
            for c in (F(1,2),F(3,4)):
                for k in (F(0),F(1,8),F(1,4)):
                    for p in ("PRECISE","NOISY"):
                        g,i,alt=scores(b,c,k,p)
                        self.assertLess(abs(g-alt),1e-12)
                        if p=="NOISY": self.assertLess(abs(i),1e-12)
    def test_precise_when_free(self):
        self.assertLess(scores(F(1,2),F(1,2),F(0),"PRECISE")[0],
                        scores(F(1,2),F(1,2),F(0),"NOISY")[0])
    def test_noisy_when_expensive(self):
        self.assertGreater(scores(F(1,2),F(1,2),F(1,4),"PRECISE")[0],
                           scores(F(1,2),F(1,2),F(1,4),"NOISY")[0])
    def test_replay(self):
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
        print("generated 144 atoms and 18 worlds")
    if args.audit:
        replay()
        print("R329 byte replay PASS")
    if args.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        if not result.wasSuccessful(): raise SystemExit(1)
