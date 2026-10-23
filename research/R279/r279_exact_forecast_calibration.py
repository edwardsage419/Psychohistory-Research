#!/usr/bin/env python3
"""R279: exact population calibration, resolution and reliability decomposition.

Two groups each contribute two independent Bernoulli observations. All 16
ordered source atoms are retained in nine forecast-policy worlds. Population
Brier = reliability - resolution + uncertainty; zero-mass atoms retained.
"""
import argparse
import csv
import hashlib
import itertools
import json
import unittest
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="acb48cd4e0640ac36c56d9bfdfa2fc111c720d11"
REGIMES={"CALIBRATED_RATE":(F(1,4),F(3,4)),
         "DETERMINISTIC_GROUP":(F(0),F(1)),
         "INVERTED_RATE":(F(3,4),F(1,4))}
POLICIES={"ORIGINAL_BUCKETS":(F(1,4),F(3,4)),
          "FLAT_HALF":(F(1,2),F(1,2)),
          "REVERSED_BUCKETS":(F(3,4),F(1,4))}
WORLDS=tuple((r,m) for r in REGIMES for m in POLICIES)
ALL_BITS=tuple("".join(bit) for bit in itertools.product("01",repeat=4))
ZERO,ONE=F(0),F(1)
LOCKED={
 ("CALIBRATED_RATE","ORIGINAL_BUCKETS"):(ZERO,F(1,16),F(1,4),F(3,16)),
 ("CALIBRATED_RATE","FLAT_HALF"):(ZERO,ZERO,F(1,4),F(1,4)),
 ("CALIBRATED_RATE","REVERSED_BUCKETS"):(F(1,4),F(1,16),F(1,4),F(7,16)),
 ("DETERMINISTIC_GROUP","ORIGINAL_BUCKETS"):(F(1,16),F(1,4),F(1,4),F(1,16)),
 ("DETERMINISTIC_GROUP","FLAT_HALF"):(ZERO,ZERO,F(1,4),F(1,4)),
 ("DETERMINISTIC_GROUP","REVERSED_BUCKETS"):(F(9,16),F(1,4),F(1,4),F(9,16)),
 ("INVERTED_RATE","ORIGINAL_BUCKETS"):(F(1,4),F(1,16),F(1,4),F(7,16)),
 ("INVERTED_RATE","FLAT_HALF"):(ZERO,ZERO,F(1,4),F(1,4)),
 ("INVERTED_RATE","REVERSED_BUCKETS"):(ZERO,F(1,16),F(1,4),F(3,16))
}
def check(regime,policy):
    if (regime,policy) not in WORLDS:raise ValueError("unfrozen regime/policy")

def four_source_probability(regime,bits):
    if regime not in REGIMES or len(bits)!=4 or any(x not in "01" for x in bits):
        raise ValueError("frozen fourbit source required")
    a,b=REGIMES[regime]
    kl=bits[:2].count("1");kh=bits[2:].count("1")
    return a**kl*(ONE-a)**(2-kl)*b**kh*(ONE-b)**(2-kh)

def original_sources(regime,policy):
    """Route A full 4-bit original source enumeration."""
    check(regime,policy)
    theta=REGIMES[regime];q=POLICIES[policy]
    for bits in ALL_BITS:
        loss=tuple((F(int(bit))-q[i//2])**2 for i,bit in enumerate(bits))
        yield dict(world=regime+"_"+policy,regime=regime,policy=policy,
          original_complete_two_group_fourbit=bits,
          original_group_labels="L;L;H;H",
          group_L_true_theta=theta[0],group_H_true_theta=theta[1],
          original_probability_mass=four_source_probability(regime,bits),
          original_four_forecast_probabilities=";".join(str(q[i//2]) for i in range(4)),
          original_four_Brier_losses=";".join(map(str,loss)),
          per_source_mean_Brier=sum(loss,ZERO)/4)

def weighted_source_brier(regime,policy):
    check(regime,policy)
    rows=tuple(original_sources(regime,policy))
    assert len(rows)==16
    assert len({r["original_complete_two_group_fourbit"] for r in rows})==16
    assert sum((r["original_probability_mass"] for r in rows),ZERO)==ONE
    return sum((r["original_probability_mass"]*r["per_source_mean_Brier"] for r in rows),ZERO)

def population_murphy_decomposition(regime,policy):
    """Route B uses only population true rates, forecast bins, no enumeration."""
    check(regime,policy)
    theta=REGIMES[regime];qs=POLICIES[policy]
    base=(theta[0]+theta[1])/2
    uncertainty=base*(ONE-base)
    bins={}
    for index,q in enumerate(qs):
        bins.setdefault(q,[]).append(theta[index])
    reliability=resolution=ZERO
    for q,vals in bins.items():
        weight=F(len(vals),2)
        theta_given_q=sum(vals,ZERO)/len(vals)
        reliability+=weight*(q-theta_given_q)**2
        resolution+=weight*(theta_given_q-base)**2
    independent_brier=sum((F(1,2)*(theta[i]*(ONE-qs[i])**2+(ONE-theta[i])*qs[i]**2)
                           for i in range(2)),ZERO)
    assert independent_brier==reliability-resolution+uncertainty
    return reliability,resolution,uncertainty,independent_brier

def frozen_claims():
    assert len(WORLDS)==len(LOCKED)==9
    assert len(ALL_BITS)==16
    for r,m in WORLDS:
        a=weighted_source_brier(r,m)
        b=population_murphy_decomposition(r,m)
        assert b==LOCKED[r,m],(r,m,b,LOCKED[r,m])
        assert a==b[3],(r,m,a,b)
        if m=="FLAT_HALF":
            assert b[0]==b[1]==ZERO
    assert sum(int(z["original_probability_mass"]>ZERO)
      for r,m in WORLDS for z in original_sources(r,m))==99
    assert LOCKED["DETERMINISTIC_GROUP","ORIGINAL_BUCKETS"][3]<
           LOCKED["DETERMINISTIC_GROUP","FLAT_HALF"][3]
    return True

def emit():
    frozen_claims()
    src=HERE/"R279_ALL_144_ORIGINAL_FORECAST_CALIBRATION_SOURCES.csv"
    fields=("world","regime","policy","original_complete_two_group_fourbit",
            "original_group_labels","group_L_true_theta","group_H_true_theta",
            "original_probability_mass","original_four_forecast_probabilities",
            "original_four_Brier_losses","per_source_mean_Brier")
    with src.open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=fields,lineterminator="\n")
        writer.writeheader()
        for r,m in WORLDS:
            for item in original_sources(r,m):
                writer.writerow({key:str(item[key]) for key in fields})
    result=dict(research_id="R279",original_catalogue_id="12-009",
       prescore_freeze_commit=FREEZE,
       evidence="ARTIFICIAL_E1_POPULATION_MURPHY_BRIER_DECOMPOSITION",
       nine_worlds=9,original_source_types=144,
       positive_probability_original_source_types=99,
       grouped_observations_per_source=4,forecast_buckets_are_unique_predicted_probabilities=True,
       calibration_and_resolution_are_true_population_properties_not_empirical_estimates=True,
       all_nine_source_risks_equal_independent_murphy_decomposition=True,
       no_real_human_E2=0,no_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[dict(world=r+"_"+m,regime=r,policy=m,
         source_atoms=16,
         positive_source_atoms=sum(int(z["original_probability_mass"]>ZERO) for z in original_sources(r,m)),
         true_group_L_probability=str(REGIMES[r][0]),
         true_group_H_probability=str(REGIMES[r][1]),
         population_reliability=str(population_murphy_decomposition(r,m)[0]),
         population_resolution=str(population_murphy_decomposition(r,m)[1]),
         population_uncertainty=str(population_murphy_decomposition(r,m)[2]),
         expected_population_Brier=str(weighted_source_brier(r,m)),
         source_equals_population_decomposition=True) for r,m in WORLDS])
    jp=HERE/"R279_EXACT_RESULTS.json"
    jp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R279",prescore_freeze_commit=FREEZE,
      original_complete_source_types=144,positive_original_source_types=99,
      source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
      results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
      no_real_human_E2=0,no_real_historical_E3=0)
    (HERE/"R279_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_claims(self):self.assertTrue(frozen_claims())
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_source_total(self):self.assertEqual(9*len(ALL_BITS),144)
    def test_mass_calibrated(self):self.assertEqual(four_source_probability("CALIBRATED_RATE","0000"),F(3,4)**2*F(1,4)**2)
    def test_mass_det(self):self.assertEqual(four_source_probability("DETERMINISTIC_GROUP","0011"),ONE)
    def test_mass_det_zero(self):self.assertEqual(four_source_probability("DETERMINISTIC_GROUP","1111"),ZERO)
    def test_flat_pure_cal(self):self.assertEqual(population_murphy_decomposition("INVERTED_RATE","FLAT_HALF")[:2],(ZERO,ZERO))
    def test_resolution(self):self.assertEqual(population_murphy_decomposition("CALIBRATED_RATE","ORIGINAL_BUCKETS")[1],F(1,16))
    def test_det_true_res(self):self.assertEqual(population_murphy_decomposition("DETERMINISTIC_GROUP","ORIGINAL_BUCKETS")[1],F(1,4))
    def test_invalid(self):
        with self.assertRaises(ValueError):list(original_sources("BAD","FLAT_HALF"))
    def test_bad_source(self):
        with self.assertRaises(ValueError):four_source_probability("CALIBRATED_RATE","000")
    def test_source_length(self):self.assertEqual(len(ALL_BITS),16)

def case(r,m,k):
    def test(self):
        rows=tuple(original_sources(r,m))
        if k=="mass":self.assertEqual(sum((z["original_probability_mass"] for z in rows),ZERO),ONE)
        elif k=="source":self.assertEqual(len(rows),16)
        elif k=="unique":self.assertEqual(len({z["original_complete_two_group_fourbit"] for z in rows}),16)
        elif k=="scores":
            for z in rows:
                q=POLICIES[m]
                losses=tuple((F(int(bit))-q[i//2])**2 for i,bit in enumerate(z["original_complete_two_group_fourbit"]))
                self.assertEqual(z["original_four_Brier_losses"],";".join(map(str,losses)))
        elif k=="source_analytic":self.assertEqual(weighted_source_brier(r,m),population_murphy_decomposition(r,m)[3])
        elif k=="frozen":self.assertEqual(population_murphy_decomposition(r,m),LOCKED[r,m])
        elif k=="nonzero":self.assertEqual(sum(z["original_probability_mass"]>0 for z in rows),1 if r=="DETERMINISTIC_GROUP" else 16)
        elif k=="forecasts":
            for z in rows:self.assertEqual(z["original_four_forecast_probabilities"],
                ";".join(map(str,[POLICIES[m][0],POLICIES[m][0],POLICIES[m][1],POLICIES[m][1]])))
        else:raise AssertionError("unfrozen unit case")
    return test
for r,m in WORLDS:
    for k in ("mass","source","unique","scores","source_analytic","frozen","nonzero","forecasts"):
        setattr(Tests,"test_"+r.lower()+"_"+m.lower()+"_"+k,case(r,m,k))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["r279"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
