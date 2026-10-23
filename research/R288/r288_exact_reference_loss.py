#!/usr/bin/env python3
"""R288: artificial reference-dependent piecewise-linear prospect-value subset.

No 1979 paper experiments, no decision-probability weights, no human choices.
"""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FREEZE="d94d9d7f275082a6672fbea0e191ac76a54bed87"
Z,O=F(0),F(1)
REFS=(-2,0,2); LOSSES=(1,2,3)
WORLD=tuple((r,L) for r in REFS for L in LOSSES)
SOURCES=tuple("".join(z) for z in itertools.product("01",repeat=6))
def validate(r,L):
    if (r,L) not in WORLD:raise ValueError("only frozen r,L")
def bits(s):
    if not isinstance(s,str) or len(s)!=6 or any(z not in "01" for z in s):raise ValueError("requires six fair payoff bits")
    return tuple(int(x) for x in s)
def value(x,r,L):
    validate(r,L)
    delta=F(x-r)
    return delta if delta>=0 else F(L)*delta
def closed(r,L):
    validate(r,L)
    g=(value(3,r,L)+value(-2,r,L))/2
    sure=value(0,r,L)
    return g,sure,g-sure
def source_row(r,L,s):
    six=bits(s)
    payoffs=tuple(3 if y else -2 for y in six)
    scores=tuple(value(x,r,L) for x in payoffs)
    sg=value(0,r,L)
    mean=sum(scores,Z)/6
    return dict(world=f"REF_{r}_LOSS_{L}",reference=r,loss_multiplier=L,
       ordered_all_six_independent_fair_gamble_bits=s,source_probability=F(1,64),
       realized_gamble_payoffs=";".join(map(str,payoffs)),
       realized_gamble_reference_values=";".join(map(str,scores)),
       sure_zero_reference_value=sg,realized_mean_gamble_reference_value=mean,
       realized_mean_gamble_minus_sure=mean-sg)
def rows(r,L):
    validate(r,L)
    for s in SOURCES:yield source_row(r,L,s)
def exhaustive(r,L):
    z=list(rows(r,L))
    assert len(z)==64 and len({x["ordered_all_six_independent_fair_gamble_bits"] for x in z})==64
    mass=sum((x["source_probability"] for x in z),Z)
    assert mass==O
    g=sum((x["source_probability"]*x["realized_mean_gamble_reference_value"] for x in z),Z)
    s=sum((x["source_probability"]*x["sure_zero_reference_value"] for x in z),Z)
    return g,s,g-s
def claims():
    for r,L in WORLD:assert exhaustive(r,L)==closed(r,L)
    for r in REFS:assert closed(r,1)[2]==F(1,2)
    assert closed(0,2)==(F(-1,2),Z,F(-1,2))
    assert closed(2,2)==(F(-7,2),F(-4),F(1,2))
    return True
def emit():
    claims()
    source=ROOT/"R288_ALL_576_ORIGINAL_REFERENCE_LOSS_SOURCES.csv"
    cols=("world","reference","loss_multiplier",
      "ordered_all_six_independent_fair_gamble_bits","source_probability",
      "realized_gamble_payoffs","realized_gamble_reference_values",
      "sure_zero_reference_value","realized_mean_gamble_reference_value",
      "realized_mean_gamble_minus_sure")
    with source.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=cols,lineterminator="\n");writer.writeheader()
        for r,L in WORLD:
            for row in rows(r,L):writer.writerow({k:str(row[k]) for k in cols})
    obj=dict(research_id="R288",original_catalogue_id="01-002",freeze_commit=FREEZE,
      evidence="E1_ONLY_REFERENCE_DEPENDENCE_AND_LINEAR_LOSS_MULTIPLIER_SUBMODEL_NOT_WHOLE_1979_PROSPECT_THEORY",
      nine_artificial_worlds=9,complete_original_source_atoms=576,
      no_original_subject_data=True,no_probability_distortion_modelled=True,
      human_E2=0,historical_E3=0,R073="FROZEN",PESEN_v0_1="FROZEN",
      result=[dict(reference=r,loss_multiplier=L,full_sources=64,
       exact_expected_gamble_value=str(exhaustive(r,L)[0]),
       exact_sure_reference_value=str(exhaustive(r,L)[1]),
       exact_gamble_minus_sure=str(exhaustive(r,L)[2]),
       independent_closed_form_matched=True) for r,L in WORLD])
    path=ROOT/"R288_EXACT_REFERENCE_RESULTS.json"
    path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
    receipt=dict(research_id="R288",freeze_commit=FREEZE,source_atoms=576,
       source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),human_E2=0,historical_E3=0)
    (ROOT/"R288_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
    return receipt
class Tests(unittest.TestCase):
    def test_claims(self):self.assertTrue(claims())
    def test_count(self):self.assertEqual(len(SOURCES),64)
    def test_worlds(self):self.assertEqual(len(WORLD),9)
    def test_bad(self):
        with self.assertRaises(ValueError):bits("100")
    def test_ref0loss2(self):self.assertEqual(closed(0,2)[2],F(-1,2))
    def test_ref2loss2(self):self.assertEqual(closed(2,2)[2],F(1,2))
    def test_reference_flip(self):self.assertLess(closed(0,2)[2]*closed(2,2)[2],0)
    def test_linear_no_ref_effect(self):self.assertEqual({closed(r,1)[2] for r in REFS},{F(1,2)})
    def test_realized_sure(self):self.assertEqual(source_row(0,3,"000000")["sure_zero_reference_value"],Z)
def make(r,L,kind):
    def tester(self):
        z=tuple(rows(r,L))
        if kind=="count":self.assertEqual(len(z),64)
        elif kind=="mass":self.assertEqual(sum((v["source_probability"] for v in z),Z),O)
        elif kind=="unique":self.assertEqual(len({v["ordered_all_six_independent_fair_gamble_bits"] for v in z}),64)
        elif kind=="analytic":self.assertEqual(exhaustive(r,L),closed(r,L))
        elif kind=="sure":self.assertTrue(all(v["sure_zero_reference_value"]==closed(r,L)[1] for v in z))
        elif kind=="payoff":
            for v in z:
                six=bits(v["ordered_all_six_independent_fair_gamble_bits"])
                self.assertEqual(v["realized_gamble_payoffs"],";".join(str(3 if x else -2) for x in six))
        elif kind=="score":
            for v in z:
                self.assertEqual(v["realized_mean_gamble_minus_sure"],v["realized_mean_gamble_reference_value"]-v["sure_zero_reference_value"])
        elif kind=="constant":self.assertTrue(all(v["source_probability"]==F(1,64) for v in z))
        else:raise AssertionError(kind)
    return tester
for r,L in WORLD:
    for kind in ("count","mass","unique","analytic","sure","payoff","score","constant"):
        setattr(Tests,"test_r"+str(r).replace("-","m")+"_loss"+str(L)+"_"+kind,make(r,L,kind))
if __name__=="__main__":
    a=argparse.ArgumentParser()
    group=a.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true");group.add_argument("--emit",action="store_true")
    cmd=a.parse_args()
    if cmd.test:unittest.main(argv=["r288"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
