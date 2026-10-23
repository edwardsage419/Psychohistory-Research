#!/usr/bin/env python3
"""Original catalogue P1 01-001: artificial vNM expected-utility mixture audit."""
from __future__ import annotations
import argparse,csv,hashlib,itertools,json,unittest
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FREEZE="524211361d5180624d4350559d53112de31139ab"
Z,O=F(0),F(1)
UTILITY={"LINEAR":{0:Z,1:O,4:F(4),9:F(9)},
         "SQRT_ON_SQUARES":{0:Z,1:O,4:F(2),9:F(3)},
         "SATURATING":{0:Z,1:O,4:F(3,2),9:F(2)}}
LAMBDA=(F(1,4),F(1,2),F(3,4))
SOURCES=tuple("".join(t) for t in itertools.product("01",repeat=8))
WORLD=tuple((name,l) for name in UTILITY for l in LAMBDA)
def check(name,l):
    if (name,l) not in WORLD:raise ValueError("unfrozen profile/mix")
def source_bits(s):
    if not isinstance(s,str) or len(s)!=8 or any(x not in "01" for x in s):raise ValueError("8 original M/X bits")
    return tuple(map(int,s))
def source_mass(l,s):
    if l not in LAMBDA:raise ValueError("lambda")
    bits=source_bits(s);m=sum(bits[::2])
    return l**m*(O-l)**(4-m)*F(1,16)
def payoffs(s):
    b=source_bits(s)
    return tuple(((1 if b[2*i] else 4),(1 if b[2*i] else (9 if b[2*i+1] else 0))) for i in range(4))
def source_row(name,l,s):
    check(name,l)
    ps=payoffs(s)
    u=UTILITY[name]
    vals_a=[u[a] for a,b in ps]
    vals_b=[u[b] for a,b in ps]
    mean_a=sum(vals_a,Z)/4;mean_b=sum(vals_b,Z)/4
    return dict(world=name+"_"+str(l),utility_profile=name,lambda_common=l,
      full_ordered_M1X1_M2X2_M3X3_M4X4=s,source_probability=source_mass(l,s),
      actual_payoffs_A=";".join(str(a) for a,b in ps),
      actual_payoffs_B=";".join(str(b) for a,b in ps),
      realized_mean_utility_A=mean_a,
      realized_mean_utility_B=mean_b,realized_mean_difference_A_minus_B=mean_a-mean_b)
def full_rows(name,l):
    for s in SOURCES:yield source_row(name,l,s)
def exhaustive(name,l):
    records=tuple(full_rows(name,l))
    assert len(records)==256
    assert sum((r["source_probability"] for r in records),Z)==O
    a=sum((r["source_probability"]*r["realized_mean_utility_A"] for r in records),Z)
    b=sum((r["source_probability"]*r["realized_mean_utility_B"] for r in records),Z)
    return a,b,a-b
def independent_formula(name,l):
    check(name,l)
    u=UTILITY[name]
    a=(O-l)*u[4]+l*u[1]
    b=(O-l)*(u[0]+u[9])/2+l*u[1]
    return a,b,a-b
def affine_profile_formula(name,l):
    a,b,d=independent_formula(name,l)
    transformed={x:F(3)*v+7 for x,v in UTILITY[name].items()}
    va=(O-l)*transformed[4]+l*transformed[1]
    vb=(O-l)*(transformed[0]+transformed[9])/2+l*transformed[1]
    assert (va,vb)==(3*a+7,3*b+7)
    return va,vb,va-vb
def all_claims():
    assert len(WORLD)==9 and len(SOURCES)==256
    for n,l in WORLD:
        assert exhaustive(n,l)==independent_formula(n,l)
        affine_profile_formula(n,l)
        d0=UTILITY[n][4]-(UTILITY[n][0]+UTILITY[n][9])/2
        assert independent_formula(n,l)[2]==(1-l)*d0
    assert UTILITY["LINEAR"][4]-(UTILITY["LINEAR"][0]+UTILITY["LINEAR"][9])/2==F(-1,2)
    assert UTILITY["SQRT_ON_SQUARES"][4]-(UTILITY["SQRT_ON_SQUARES"][0]+UTILITY["SQRT_ON_SQUARES"][9])/2==F(1,2)
    return True
def emit():
    all_claims()
    src=ROOT/"R287_ALL_2304_ORIGINAL_COMMON_CONSEQUENCE_SOURCES.csv"
    fields=("world","utility_profile","lambda_common","full_ordered_M1X1_M2X2_M3X3_M4X4","source_probability",
      "actual_payoffs_A","actual_payoffs_B","realized_mean_utility_A",
      "realized_mean_utility_B","realized_mean_difference_A_minus_B")
    with src.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,lineterminator="\n");w.writeheader()
        for n,l in WORLD:
            for row in full_rows(n,l):w.writerow({key:str(row[key]) for key in fields})
    result=dict(research_id="R287",original_catalogue_id="01-001",prescore_freeze_commit=FREEZE,
      artificial_worlds=9,original_model_labelled_eightbit_source_types=2304,
      scientific_scope="E1_EXACT_ARTIFICIAL_EXPECTED_UTILITY_AND_COMMON_CONSEQUENCE_NOT_GENERAL_VNM_REPRESENTATION",
      no_real_human_E2=0,no_real_historical_E3=0,R073="FROZEN",PESEN_v0_1="FROZEN",
      results=[dict(profile=n,lambda_common=str(l),sources=256,
         expected_utility_A=str(exhaustive(n,l)[0]),expected_utility_B=str(exhaustive(n,l)[1]),
         EU_difference_A_minus_B=str(exhaustive(n,l)[2]),
         affine_transformed_difference=str(affine_profile_formula(n,l)[2]),
         independent_formula_agrees=True) for n,l in WORLD])
    out=ROOT/"R287_EXACT_EU_RESULTS.json"
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R287",prescore_freeze_commit=FREEZE,
      full_source_count=2304,
      source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
      result_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
      new_real_E2=0,new_historical_E3=0)
    (ROOT/"R287_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n")
    return receipt
class Tests(unittest.TestCase):
    def test_claim(self):self.assertTrue(all_claims())
    def test_worlds(self):self.assertEqual(len(WORLD),9)
    def test_sources(self):self.assertEqual(len(SOURCES),256)
    def test_empty(self):
        with self.assertRaises(ValueError):source_bits("0000")
    def test_zeros(self):self.assertEqual(payoffs("00000000"),((4,0),)*4)
    def test_common(self):self.assertEqual(payoffs("11111111"),((1,1),)*4)
    def test_linear_opposite(self):self.assertLess(independent_formula("LINEAR",F(1,2))[2],0)
    def test_sqrt_opposite(self):self.assertGreater(independent_formula("SQRT_ON_SQUARES",F(1,2))[2],0)
    def test_affine(self):self.assertEqual(affine_profile_formula("LINEAR",F(1,2))[2],3*independent_formula("LINEAR",F(1,2))[2])
def make(n,l,kind):
    def test(self):
        records=tuple(full_rows(n,l))
        if kind=="mass":self.assertEqual(sum((x["source_probability"] for x in records),Z),O)
        elif kind=="count":self.assertEqual(len(records),256)
        elif kind=="unique":self.assertEqual(len({x["full_ordered_M1X1_M2X2_M3X3_M4X4"] for x in records}),256)
        elif kind=="formula":self.assertEqual(exhaustive(n,l),independent_formula(n,l))
        elif kind=="sign":
            d0=UTILITY[n][4]-(UTILITY[n][0]+UTILITY[n][9])/2
            self.assertEqual(exhaustive(n,l)[2],(1-l)*d0)
        elif kind=="affine":self.assertEqual(affine_profile_formula(n,l)[2],3*exhaustive(n,l)[2])
        elif kind=="sources":
            for r in records:
                self.assertEqual(r["source_probability"],source_mass(l,r["full_ordered_M1X1_M2X2_M3X3_M4X4"]))
        elif kind=="payoffs":
            for r in records:
                s=r["full_ordered_M1X1_M2X2_M3X3_M4X4"]
                self.assertEqual(r["actual_payoffs_A"],";".join(str(a) for a,b in payoffs(s)))
        elif kind=="difference":
            for r in records:self.assertEqual(r["realized_mean_difference_A_minus_B"],r["realized_mean_utility_A"]-r["realized_mean_utility_B"])
        else:raise AssertionError(kind)
    return test
for n,l in WORLD:
    for kind in ("mass","count","unique","formula","sign","affine","sources","payoffs","difference"):
        setattr(Tests,"test_"+n.lower()+"_"+str(l).replace("/","of")+"_"+kind,make(n,l,kind))
if __name__=="__main__":
    arg=argparse.ArgumentParser()
    g=arg.add_mutually_exclusive_group(required=True);g.add_argument("--test",action="store_true");g.add_argument("--emit",action="store_true")
    v=arg.parse_args()
    if v.test:unittest.main(argv=["r287"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
