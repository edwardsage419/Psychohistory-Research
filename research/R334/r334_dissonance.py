"""R334 finite artificial induced-compliance contrasts, frozen protocol replay."""
import argparse
import csv
import io
import json
import unittest
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "R334_ALL_48_ARTIFICIAL_CONTRAST_ATOMS.csv"
RESULT = ROOT / "R334_EXACT_16_CONDITIONS.json"
HEADER = ["model","a","b","j","c","m","latent_strain","post_attitude"]
MODELS = ("DISSONANCE","RESPONSE_DEMAND","INCENTIVE")
EXPECTED = {"rows":48,"conditions":16,"unchanged_conditions":12,"identical_reports":16,
            "latent_strain_disagreements":4,"low_justification_larger_dissonance_shifts":2,
            "high_justification_larger_incentive_shifts":2}

def build():
    rows, conditions = [], []
    for a in (-1,1):
        for b in (-1,1):
            for j in (1,3):
                for c in (0,1):
                    m = int(a != b)
                    d = F(c*m,1+j)
                    y = F(a) + F(b-a)*d
                    yi = F(a) + F(b-a)*F(c*m*j,1+j)
                    for model in MODELS:
                        rows.append([model,a,b,j,c,m,str(d if model=="DISSONANCE" else F(0)),
                                     str(yi if model=="INCENTIVE" else y)])
                    conditions.append(dict(a=a,b=b,j=j,c=c,post_dissonance=str(y),
                        post_response_demand=str(y),post_incentive=str(yi),
                        strain_dissonance=str(d),strain_response_demand="0",strain_incentive="0"))
    unchanged = sum((w["c"]==0 or w["a"]==w["b"]) and
                    w["post_dissonance"]==str(w["a"]) and w["post_incentive"]==str(w["a"])
                    for w in conditions)
    low, high = 0, 0
    for a in (-1,1):
        pair = [w for w in conditions if w["a"]==a and w["b"]==-a and w["c"]==1]
        lo = next(w for w in pair if w["j"]==1)
        hi = next(w for w in pair if w["j"]==3)
        low += abs(F(lo["post_dissonance"])-a) > abs(F(hi["post_dissonance"])-a)
        high += abs(F(lo["post_incentive"])-a) < abs(F(hi["post_incentive"])-a)
    checks = dict(rows=len(rows),conditions=len(conditions),unchanged_conditions=unchanged,
        identical_reports=sum(w["post_dissonance"]==w["post_response_demand"] for w in conditions),
        latent_strain_disagreements=sum(w["strain_dissonance"]!="0" for w in conditions),
        low_justification_larger_dissonance_shifts=low,
        high_justification_larger_incentive_shifts=high)
    return rows,dict(schema="R334_frozen_induced_compliance_v1",conditions=conditions,checks=checks)

def render():
    rows,obj=build()
    output=io.StringIO(newline="")
    writer=csv.writer(output,lineterminator="\\r\\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return output.getvalue().encode(),(json.dumps(obj,indent=2,ensure_ascii=False)+"\\n").encode()

def audit():
    cb,jb=render()
    assert SOURCE.read_bytes()==cb, "CSV byte replay mismatch"
    assert RESULT.read_bytes()==jb, "JSON byte replay mismatch"
    rows,obj=build()
    assert len(rows)==48 and len(obj["conditions"])==16
    assert obj["checks"]==EXPECTED
    assert all(-1<=F(r[-1])<=1 for r in rows)

class Tests(unittest.TestCase):
    def test_counts(self):
        self.assertEqual((len(build()[0]),len(build()[1]["conditions"])),(48,16))
    def test_falsifiers(self):
        self.assertEqual(build()[1]["checks"],EXPECTED)
    def test_fraction_range(self):
        self.assertTrue(all(-1<=F(r[-1])<=1 for r in build()[0]))
    def test_countermodel(self):
        self.assertEqual(sum(w["strain_dissonance"]!="0" for w in build()[1]["conditions"]),4)
    def test_byte_replay(self):
        audit()

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--audit",action="store_true")
    args=parser.parse_args()
    if args.test:
        r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        if not r.wasSuccessful(): raise SystemExit(1)
    if args.audit:
        audit()
        print("R334 PRODUCTION_REPLAY_PASS 48 artificial atoms 16 conditions")
