#!/usr/bin/env python3
"""R326 exact project-defined finite hierarchical Bayesian learning, artificial E1."""
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
CSV=HERE/"R326_ALL_64_ARTIFICIAL_GROUP_HISTORIES.csv"
RESULT=HERE/"R326_EXACT_HIERARCHICAL_PREDICTIONS.json"
FIELDS=("history_id","h11","h12","h21","h22","h31","h32","enumeration_weight",
        "posterior_global_high","hier_predict_g1","hier_predict_g2","hier_predict_g3",
        "independent_predict_g1","independent_predict_g2","independent_predict_g3")
HISTORIES=tuple(itertools.product((0,1),repeat=6))
THETAS=(F(1,4),F(3,4))

def likelihood(theta,obs):
    if any(x not in (0,1) for x in obs):raise ValueError("nonbinary history")
    p=F(1)
    for x in obs:p*=theta if x else 1-theta
    return p

def hierarchical(history):
    if len(history)!=6 or any(x not in (0,1) for x in history):
        raise ValueError("invalid history")
    groups=(history[0:2],history[2:4],history[4:6])
    total=F(0); high=F(0); weighted=[F(0),F(0),F(0)]
    for z in (0,1):
        p_high=F(3,4) if z else F(1,4)
        for assignment in itertools.product((0,1),repeat=3):
            mass=F(1,2)
            for g,t in enumerate(assignment):
                theta=THETAS[t]
                mass*= (p_high if t else 1-p_high)*likelihood(theta,groups[g])
            total+=mass
            if z:high+=mass
            for g,t in enumerate(assignment):weighted[g]+=mass*THETAS[t]
    if total<=0:raise AssertionError("zero evidence")
    return high/total,tuple(x/total for x in weighted)

def independent(obs):
    if len(obs)!=2 or any(x not in (0,1) for x in obs):
        raise ValueError("invalid group observations")
    w=[F(1,2)*likelihood(theta,obs) for theta in THETAS]
    return (w[0]*THETAS[0]+w[1]*THETAS[1])/sum(w)

def independent_all(history):
    return tuple(independent(history[i:i+2]) for i in (0,2,4))

def generate():
    rows=[];posteriors=[]
    for i,h in enumerate(HISTORIES):
        p,pred=hierarchical(h)
        flat=independent_all(h)
        posteriors.append(p)
        rows.append(dict(zip(FIELDS,map(str,(i,*h,F(1,64),p,*pred,*flat)))))
    high_hist=(0,1,1,1,1,1)
    low_hist=(0,1,0,0,0,0)
    hp,hi=hierarchical(high_hist)
    lp,li=hierarchical(low_hist)
    witness={"high_other_groups":"011111","low_other_groups":"010000",
        "high_global_posterior":str(hp),"low_global_posterior":str(lp),
        "high_group1_hier_prediction":str(hi[0]),"low_group1_hier_prediction":str(li[0]),
        "independent_group1_both":"1/2","strict_cross_group_borrowing":hi[0]>li[0]}
    symmetry=all(hierarchical(tuple(1-x for x in h))[0]==1-hierarchical(h)[0]
        and all(a==1-b for a,b in zip(hierarchical(tuple(1-x for x in h))[1],hierarchical(h)[1]))
        and all(a==1-b for a,b in zip(independent_all(tuple(1-x for x in h)),independent_all(h)))
        for h in HISTORIES)
    permute=all(hierarchical(h[2:4]+h[0:2]+h[4:6])[0]==hierarchical(h)[0]
        and hierarchical(h[2:4]+h[0:2]+h[4:6])[1]==
            (hierarchical(h)[1][1],hierarchical(h)[1][0],hierarchical(h)[1][2])
        for h in HISTORIES)
    obj={"schema":"r326_finite_hierarchical_bayes_three_group_e1_v1",
        "original_catalogue_id":"02-007","artificial_only":True,"original_source_rows":64,
        "witness":witness,"summary":{"history_count":64,"group_count":3,
        "min_global_posterior":str(min(posteriors)),"max_global_posterior":str(max(posteriors)),
        "distinct_global_posteriors":len(set(posteriors)),
        "complement_symmetry_verified":symmetry,"group_permutation_verified":permute}}
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
    def test_01_histories(self):self.assertEqual(len(HISTORIES),64)
    def test_02_rows(self):self.assertEqual(len(generate()[0]),64)
    def test_03_unique(self):self.assertEqual(len({tuple(r[k] for k in FIELDS[1:7]) for r in generate()[0]}),64)
    def test_04_mass(self):self.assertEqual(sum([F(r["enumeration_weight"]) for r in generate()[0]]),F(1))
    def test_05_prior(self):self.assertEqual(hierarchical((0,1,0,1,0,1))[0],F(1,2))
    def test_06_posterior_bounds(self):
        for h in HISTORIES:
            p,v=hierarchical(h)
            self.assertTrue(0<p<1 and all(0<x<1 for x in v))
    def test_07_flat_bounds(self):
        for h in HISTORIES:self.assertTrue(all(0<x<1 for x in independent_all(h)))
    def test_08_flat_group1(self):self.assertEqual(independent((0,1)),F(1,2))
    def test_09_witness_hier(self):self.assertGreater(hierarchical((0,1,1,1,1,1))[1][0],hierarchical((0,1,0,0,0,0))[1][0])
    def test_10_witness_flat(self):self.assertEqual(independent_all((0,1,1,1,1,1))[0],independent_all((0,1,0,0,0,0))[0])
    def test_11_complement(self):self.assertTrue(generate()[1]["summary"]["complement_symmetry_verified"])
    def test_12_permutation(self):self.assertTrue(generate()[1]["summary"]["group_permutation_verified"])
    def test_13_group_independence(self):
        for h in HISTORIES:self.assertEqual(independent_all(h)[0],independent(h[:2]))
    def test_14_all_success(self):self.assertGreater(hierarchical((1,1,1,1,1,1))[0],F(1,2))
    def test_15_all_fail(self):self.assertLess(hierarchical((0,0,0,0,0,0))[0],F(1,2))
    def test_16_distinct(self):self.assertGreater(generate()[1]["summary"]["distinct_global_posteriors"],2)
    def test_17_invalid_h(self):
        with self.assertRaises(ValueError):hierarchical((0,1,1))
    def test_18_invalid_obs(self):
        with self.assertRaises(ValueError):independent((1,2))
    def test_19_likelihood(self):self.assertEqual(likelihood(F(3,4),(1,1)),F(9,16))
    def test_20_replay(self):self.assertTrue(replay())
    def test_21_mutate_csv(self):
        c=csv_text(generate()[0]);j=json_text(generate()[1])
        with self.assertRaises(AssertionError):verify_bytes(c.replace("1/64","1/63",1),j)
    def test_22_mutate_json(self):
        c=csv_text(generate()[0]);j=json_text(generate()[1])
        with self.assertRaises(AssertionError):verify_bytes(c,j.replace('"original_source_rows": 64','"original_source_rows": 63'))
    def test_23_meta(self):self.assertEqual(generate()[1]["original_catalogue_id"],"02-007")
    def test_24_flat_symmetry(self):self.assertEqual(independent((0,0))+independent((1,1)),1)

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
        print("R326_GENERATED",len(rows))
    elif args.audit:
        print("R326_REPLAY_PASS",replay())
    elif args.test:
        unittest.main(argv=["r326"],verbosity=2)
    else:
        parser.print_help()
