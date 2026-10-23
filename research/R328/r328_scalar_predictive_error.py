#!/usr/bin/env python3
"""R328 exact finite scalar precision-weighted predictive error E1."""
import argparse
import csv
import io
import json
import unittest
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CSV="R328_ALL_120_ARTIFICIAL_PREDICTION_ERROR_STATES.csv"
RESULT="R328_EXACT_24_PRECISION_WORLDS.json"
FIELDS=["prior","target","prior_precision","sensory_precision","step","estimate","sensory_error","prior_error","energy","analytic_optimum"]


def energy(x,m,y,r,p):
    return (r*(x-m)**2+p*(y-x)**2)/2


def generate():
    rows,worlds=[],[]
    for m in (F(0),F(1)):
        for y in (F(0),F(1),F(2)):
            for r in (F(1),F(2)):
                for p in (F(1),F(2)):
                    x=m
                    optimum=(r*m+p*y)/(r+p)
                    energies=[]
                    for t in range(5):
                        e=energy(x,m,y,r,p)
                        energies.append(e)
                        rows.append(dict(prior=str(m),target=str(y),prior_precision=str(r),
                                         sensory_precision=str(p),step=str(t),estimate=str(x),
                                         sensory_error=str(y-x),prior_error=str(m-x),
                                         energy=str(e),analytic_optimum=str(optimum)))
                        if t<4:
                            x=x+F(1,4)*(p*(y-x)+r*(m-x))
                    worlds.append(dict(prior=str(m),target=str(y),prior_precision=str(r),
                                       sensory_precision=str(p),analytic_optimum=str(optimum),
                                       estimate_step4=str(x),energy_step0=str(energies[0]),
                                       energy_step4=str(energies[4]),
                                       monotone=all(energies[i+1]<=energies[i] for i in range(4))))
    return rows,dict(model="R328_FINITE_SCALAR_PREDICTIVE_ERROR_E1",source_row_count=120,
                     world_count=24,worlds=worlds)


def serialized():
    rows,result=generate()
    buffer=io.StringIO(newline="")
    writer=csv.DictWriter(buffer,fieldnames=FIELDS,lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue(),json.dumps(result,sort_keys=True,separators=(",",":"))+"\n"


def verify():
    a,b=serialized()
    assert (ROOT/CSV).read_bytes()==a.encode(), "CSV byte mismatch"
    assert (ROOT/RESULT).read_bytes()==b.encode(), "JSON byte mismatch"


class Tests(unittest.TestCase):
    def test_count(self):
        rows,result=generate()
        self.assertEqual((len(rows),len(result["worlds"])),(120,24))

    def test_monotone(self):
        self.assertTrue(all(w["monotone"] for w in generate()[1]["worlds"]))

    def test_witness_high_sensor(self):
        w=[w for w in generate()[1]["worlds"] if (w["prior"],w["target"],w["prior_precision"],w["sensory_precision"])==("0","2","1","2")][0]
        self.assertEqual((w["analytic_optimum"],w["estimate_step4"]),("4/3","85/64"))

    def test_witness_high_prior(self):
        w=[w for w in generate()[1]["worlds"] if (w["prior"],w["target"],w["prior_precision"],w["sensory_precision"])==("0","2","2","1")][0]
        self.assertEqual((w["analytic_optimum"],w["estimate_step4"]),("2/3","85/128"))

    def test_zero_error_control(self):
        rows,_=generate()
        self.assertTrue(all(r["sensory_error"]=="0" and r["prior_error"]=="0"
                            for r in rows if r["prior"]==r["target"]))

    def test_analytic_gradient(self):
        for m in (F(0),F(1)):
            for y in (F(0),F(1),F(2)):
                for r in (F(1),F(2)):
                    for p in (F(1),F(2)):
                        opt=(r*m+p*y)/(r+p)
                        self.assertEqual(p*(y-opt)+r*(m-opt),0)

    def test_exact_replay(self):
        verify()


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--generate",action="store_true")
    p.add_argument("--test",action="store_true")
    p.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.generate:
        c,j=serialized()
        (ROOT/CSV).write_bytes(c.encode())
        (ROOT/RESULT).write_bytes(j.encode())
        print("R328 generated 120 states, 24 worlds")
    if a.audit:
        verify()
        print("R328 exact byte replay PASS")
    if a.test:
        result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        if not result.wasSuccessful():
            raise SystemExit(1)


if __name__=="__main__":
    main()
