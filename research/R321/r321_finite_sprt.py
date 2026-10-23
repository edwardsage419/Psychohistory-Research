#!/usr/bin/env python3
"""R321: exact finite Wald-inspired Bernoulli SPRT; artificial E1 only."""
from __future__ import annotations
import argparse,csv,io,itertools,json,unittest
from fractions import Fraction as F
from math import comb
from pathlib import Path
HERE=Path(__file__).resolve().parent
CSV=HERE/"R321_ALL_1024_ORIGINAL_SEVEN_BIT_PATHS.csv"
JSON=HERE/"R321_EXACT_8_WORLDS.json"
PAIRS=((F(1,4),F(3,4)),(F(1,3),F(2,3)))
KS=(2,3); TRUTHS=("H0","H1"); T=7
FIELDS=("world_id","p0","p1","K","true_hypothesis","p_true","path_bits","ones","full_path_probability","stop_time","decision","censored")
def first_stop(bits,k):
    if len(bits)!=T or k not in KS or any(b not in (0,1) for b in bits):raise ValueError("outside frozen universe")
    score=0
    for t,b in enumerate(bits,1):
        score+=1 if b else -1
        if score>=k:return t,"H1"
        if score<=-k:return t,"H0"
    return None,"none"
def mass(bits,p):
    if len(bits)!=T or p not in (F(1,4),F(3,4),F(1,3),F(2,3)):raise ValueError("outside frozen probability grid")
    n=sum(bits);return p**n*(1-p)**(T-n)
def generate():
    rows=[];worlds=[]
    for p0,p1 in PAIRS:
        for k in KS:
            for truth in TRUTHS:
                wid=len(worlds);p=p0 if truth=="H0" else p1
                h0=h1=censor=expected=F(0)
                cells={(t,side):F(0) for t in range(1,T+1) for side in TRUTHS}
                fixed=F(0)
                for bits in itertools.product((0,1),repeat=T):
                    m=mass(bits,p);t,decision=first_stop(bits,k)
                    if decision=="H0":h0+=m;cells[(t,"H0")]+=m
                    elif decision=="H1":h1+=m;cells[(t,"H1")]+=m
                    else:censor+=m
                    expected+=m*(t if t is not None else T)
                    if sum(bits)>=4:fixed+=m
                    rows.append(dict(zip(FIELDS,map(str,(wid,p0,p1,k,truth,p,
                        "".join(map(str,bits)),sum(bits),m,
                        "" if t is None else t,decision,str(t is None).lower())))))
                worlds.append({"world_id":wid,"p0":str(p0),"p1":str(p1),
                    "K":k,"true_hypothesis":truth,"accept_H0":str(h0),
                    "accept_H1":str(h1),"censored":str(censor),
                    "expected_truncated_samples":str(expected),
                    "fixed7_majority_choose_H1":str(fixed),
                    "first_stop_cells":[{"time":t,"accept_H0":str(cells[(t,"H0")]),
                        "accept_H1":str(cells[(t,"H1")])} for t in range(1,T+1)]})
    return rows,{"schema":"r321_finite_bernoulli_sprt_e1_v1",
        "original_catalogue_id":"01-010","finite_wald_inspired_only":True,
        "original_source_rows":len(rows),"world_count":len(worlds),
        "horizon":T,"worlds":worlds}
def csv_text(rows):
    f=io.StringIO(newline="");w=csv.DictWriter(f,fieldnames=FIELDS,lineterminator="\n")
    w.writeheader();w.writerows(rows);return f.getvalue()
def json_text(obj):return json.dumps(obj,indent=2,ensure_ascii=False)+"\n"
def verify_source(csv_data,json_data):
    rows,obj=generate()
    if csv_data!=csv_text(rows):raise AssertionError("source bytes changed")
    if json.loads(json_data)!=obj:raise AssertionError("world results changed")
    return True
def replay():return verify_source(CSV.read_text(encoding="utf-8"),JSON.read_text(encoding="utf-8"))
def world(pair,k,truth):
    p0,p1=PAIRS[pair]
    return next(w for w in generate()[1]["worlds"] if w["p0"]==str(p0) and w["K"]==k and w["true_hypothesis"]==truth)
class Tests(unittest.TestCase):
    def test_01_worlds(self):self.assertEqual(len(generate()[1]["worlds"]),8)
    def test_02_rows(self):self.assertEqual(len(generate()[0]),1024)
    def test_03_unique(self):self.assertEqual(len({(r["world_id"],r["path_bits"]) for r in generate()[0]}),1024)
    def test_04_mass(self):
        for w in generate()[1]["worlds"]:self.assertEqual(F(w["accept_H0"])+F(w["accept_H1"])+F(w["censored"]),1)
    def test_05_rows_per_world(self):
        for i in range(8):self.assertEqual(sum(int(r["world_id"])==i for r in generate()[0]),128)
    def test_06_witness_correct(self):self.assertEqual(F(world(0,2,"H1")["accept_H1"]),F(873,1024))
    def test_07_witness_error(self):self.assertEqual(F(world(0,2,"H1")["accept_H0"]),F(97,1024))
    def test_08_witness_censor(self):self.assertEqual(F(world(0,2,"H1")["censored"]),F(27,512))
    def test_09_witness_time(self):self.assertEqual(F(world(0,2,"H1")["expected_truncated_samples"]),F(1579,512))
    def test_10_k3_correct(self):self.assertEqual(F(world(0,3,"H1")["accept_H1"]),F(12987,16384))
    def test_11_k3_error(self):self.assertEqual(F(world(0,3,"H1")["accept_H0"]),F(481,16384))
    def test_12_k3_censor(self):self.assertEqual(F(world(0,3,"H1")["censored"]),F(729,4096))
    def test_13_k3_time(self):self.assertEqual(F(world(0,3,"H1")["expected_truncated_samples"]),F(609,128))
    def test_14_symmetry(self):
        for pair in range(2):
            for k in KS:
                a,b=world(pair,k,"H0"),world(pair,k,"H1")
                self.assertEqual(a["accept_H0"],b["accept_H1"])
                self.assertEqual(a["accept_H1"],b["accept_H0"])
                self.assertEqual(a["censored"],b["censored"])
    def test_15_threshold_censor(self):
        for pair in range(2):
            for truth in TRUTHS:self.assertLess(F(world(pair,2,truth)["censored"]),F(world(pair,3,truth)["censored"]))
    def test_16_threshold_time(self):
        for pair in range(2):
            for truth in TRUTHS:self.assertLess(F(world(pair,2,truth)["expected_truncated_samples"]),F(world(pair,3,truth)["expected_truncated_samples"]))
    def test_17_first_hit_ones(self):self.assertEqual(first_stop((1,)*T,2),(2,"H1"))
    def test_18_first_hit_zeros(self):self.assertEqual(first_stop((0,)*T,3),(3,"H0"))
    def test_19_censor(self):self.assertEqual(first_stop((0,1,0,1,0,1,0),2),(None,"none"))
    def test_20_no_t1(self):
        for w in generate()[1]["worlds"]:self.assertEqual(w["first_stop_cells"][0]["accept_H1"],"0")
    def test_21_censor_flag(self):
        for r in generate()[0]:self.assertEqual(r["censored"]=="true",r["decision"]=="none")
    def test_22_time_flag(self):
        for r in generate()[0]:self.assertEqual(r["stop_time"]=="",r["decision"]=="none")
    def test_23_mass_positive(self):self.assertTrue(all(F(r["full_path_probability"])>0 for r in generate()[0]))
    def test_24_invalid_k(self):
        with self.assertRaises(ValueError):first_stop((1,)*T,4)
    def test_25_invalid_bits(self):
        with self.assertRaises(ValueError):first_stop((1,)*6,2)
    def test_26_invalid_p(self):
        with self.assertRaises(ValueError):mass((1,)*T,F(1,2))
    def test_27_fixed_binomial(self):
        for w in generate()[1]["worlds"]:
            p=F(w["p0"]) if w["true_hypothesis"]=="H0" else F(w["p1"])
            self.assertEqual(F(w["fixed7_majority_choose_H1"]),sum((comb(7,j)*p**j*(1-p)**(7-j) for j in range(4,8)),F(0)))
    def test_28_replay(self):self.assertTrue(replay())
    def test_29_corrupt(self):
        c=csv_text(generate()[0]);j=json_text(generate()[1])
        with self.assertRaises(AssertionError):verify_source(c.replace("1/16384","2/16384",1),j)
    def test_30_cells(self):
        for w in generate()[1]["worlds"]:
            self.assertEqual(sum((F(x["accept_H0"])+F(x["accept_H1"]) for x in w["first_stop_cells"]),F(0)),F(w["accept_H0"])+F(w["accept_H1"]))
    def test_31_stop_immutable_suffix(self):self.assertEqual(first_stop((1,1,0,0,0,0,0),2),first_stop((1,1,1,1,1,1,1),2))
    def test_32_meta(self):self.assertEqual(generate()[1]["original_catalogue_id"],"01-010")
    def test_33_fixed_truth_symmetry(self):
        for pair in range(2):
            self.assertEqual(F(world(pair,2,"H0")["fixed7_majority_choose_H1"])+F(world(pair,2,"H1")["fixed7_majority_choose_H1"]),1)
    def test_34_censor_unassigned(self):
        self.assertTrue(all(r["decision"]=="none" for r in generate()[0] if r["censored"]=="true"))
    def test_35_horizon(self):self.assertEqual(generate()[1]["horizon"],7)
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--write",action="store_true")
    parser.add_argument("--audit",action="store_true");parser.add_argument("--test",action="store_true")
    args=parser.parse_args()
    if args.write:
        r,o=generate();CSV.write_text(csv_text(r),encoding="utf-8");JSON.write_text(json_text(o),encoding="utf-8")
        print("WROTE",len(r),"paths",len(o["worlds"]),"worlds")
    elif args.audit:print("R321_REPLAY_PASS",replay())
    elif args.test:unittest.main(argv=["r321"],verbosity=2)
    else:parser.print_help()
