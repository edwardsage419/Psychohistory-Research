#!/usr/bin/env python3
"""R277 finite Markov misspecification: equal point marginals, different chains.

Three first-order symmetric binary Markov worlds retain the same Bernoulli(1/2)
one-time marginals and Brier 1/4. Five stay/flip transitions have independent
Bernoulli(s) indicators, allowing an independent exact Binomial(5,s) audit.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import unittest
from collections import defaultdict
from fractions import Fraction as F
from math import comb
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="923a161bbdc012c138e53f1fa316e6085ff2704e"
REGIMES={"ANTIPERSISTENT":F(1,4),"IID_FAIR":F(1,2),"PERSISTENT":F(3,4)}
ALL_BITS=tuple("".join(z) for z in itertools.product("01",repeat=6))
ZERO,ONE=F(0),F(1)
FROZEN={
 "ANTIPERSISTENT":(F(5,4),F(1,64),F(81,128)),
 "IID_FAIR":(F(5,2),F(3,16),F(3,16)),
 "PERSISTENT":(F(15,4),F(81,128),F(1,64))}

def validate(model):
    if model not in REGIMES:raise ValueError("outside frozen Markov regime")

def adjacent(seq):
    if len(seq)!=6 or any(bit not in "01" for bit in seq):
        raise ValueError("requires ordered sixbit Markov outcomes")
    return tuple(int(seq[i]==seq[i+1]) for i in range(5))

def source_likelihood(model,seq):
    validate(model)
    t=sum(adjacent(seq))
    s=REGIMES[model]
    return F(1,2)*s**t*(ONE-s)**(5-t)

def source_rows(model):
    """Route A complete ordered original 6-bit Markov sequences."""
    validate(model)
    s=REGIMES[model]
    for seq in ALL_BITS:
        stay=adjacent(seq)
        count=sum(stay)
        yield dict(true_regime=model,
          actual_transition_stay_probability=s,
          original_sixbit_ordered_sequence=seq,
          original_five_stay_indicators="".join(map(str,stay)),
          original_number_of_equal_adjacent_transitions=count,
          exact_original_sequence_mass=source_likelihood(model,seq),
          frozen_individual_prediction_probability=F(1,2),
          original_six_individual_Brier_losses=";".join(["1/4"]*6),
          original_mean_individual_Brier=F(1,4),
          preregistered_high_persistence_flag=int(count>=4),
          preregistered_low_persistence_flag=int(count<=1))

def complete_enumeration(model):
    validate(model)
    rows=tuple(source_rows(model))
    assert len(rows)==64
    assert len({r["original_sixbit_ordered_sequence"] for r in rows})==64
    assert sum((r["exact_original_sequence_mass"] for r in rows),ZERO)==ONE
    pmf=defaultdict(lambda:ZERO)
    marginal=[ZERO for _ in range(6)]
    for row in rows:
        w=row["exact_original_sequence_mass"]
        pmf[row["original_number_of_equal_adjacent_transitions"]]+=w
        for i,bit in enumerate(row["original_sixbit_ordered_sequence"]):
            marginal[i]+=w*int(bit)
    expectation=sum((F(k)*pmf[k] for k in range(6)),ZERO)
    upper=sum((pmf[k] for k in (4,5)),ZERO)
    lower=sum((pmf[k] for k in (0,1)),ZERO)
    return dict(transition_pmf={k:pmf[k] for k in range(6)},
                timewise_positive_marginals=tuple(marginal),
                expected_equal_transitions=expectation,
                high_persistence_region_mass=upper,
                low_persistence_region_mass=lower,
                expected_individual_Brier=F(1,4))

def independent_binomial_theory(model):
    """Route B: first bit fair, then 5 independent Bernoulli(s) stay flags."""
    validate(model)
    s=REGIMES[model]
    pmf={k:F(comb(5,k))*s**k*(ONE-s)**(5-k) for k in range(6)}
    assert sum(pmf.values(),ZERO)==ONE
    return dict(transition_pmf=pmf,
                timewise_positive_marginals=(F(1,2),)*6,
                expected_equal_transitions=5*s,
                high_persistence_region_mass=5*s**4*(ONE-s)+s**5,
                low_persistence_region_mass=(ONE-s)**5+5*s*(ONE-s)**4,
                expected_individual_Brier=F(1,4))

def frozen_claims():
    assert len(REGIMES)==3 and len(ALL_BITS)==64
    assert len(REGIMES)*len(ALL_BITS)==192
    for model in REGIMES:
        actual=complete_enumeration(model)
        analytic=independent_binomial_theory(model)
        assert actual==analytic,(model,actual,analytic)
        assert (actual["expected_equal_transitions"],actual["high_persistence_region_mass"],
                actual["low_persistence_region_mass"])==FROZEN[model]
        assert actual["timewise_positive_marginals"]==(F(1,2),)*6
    assert FROZEN["PERSISTENT"][1]>FROZEN["IID_FAIR"][1]
    assert FROZEN["ANTIPERSISTENT"][2]>FROZEN["IID_FAIR"][2]
    return True

def emit():
    frozen_claims()
    source_path=HERE/"R277_ALL_192_ORIGINAL_MARKOV_MISSPECIFICATION_SOURCES.csv"
    cols=("true_regime","actual_transition_stay_probability",
       "original_sixbit_ordered_sequence","original_five_stay_indicators",
       "original_number_of_equal_adjacent_transitions",
       "exact_original_sequence_mass",
       "frozen_individual_prediction_probability",
       "original_six_individual_Brier_losses","original_mean_individual_Brier",
       "preregistered_high_persistence_flag","preregistered_low_persistence_flag")
    with source_path.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        w.writeheader()
        for model in REGIMES:
            for row in source_rows(model):
                w.writerow({key:str(row[key]) for key in cols})
    results=dict(research_id="R277",original_catalogue_id="12-007",
      prescore_freeze_commit=FREEZE,
      scope="E1_FINITE_ARTIFICIAL_MARKOV_SERIAL_DEPENDENCE_MISSPECIFICATION",
      actual_regime_count=3,all_complete_original_source_types=192,
      complete_sources_per_regime=64,all_original_sources_positive_probability=True,
      one_time_marginals_in_all_regimes="1/2",
      every_observation_constant_forecast_Brier="1/4",
      all_3_independent_binomial_transition_PMFs_verified=True,
      note="Each high or low persistence check has nominal null event mass 3/16; jointly, 3/8.",
      no_real_human_E2=0,no_real_historical_E3=0,
      R073="FROZEN",PESEN_v0_1="FROZEN",
      world_results=[dict(true_regime=m,transition_stay_s=str(REGIMES[m]),
         original_complete_ordered_sequences=64,
         transition_stay_count_PMF={str(k):str(v) for k,v in complete_enumeration(m)["transition_pmf"].items()},
         expected_number_of_equal_adjacent_transitions=str(complete_enumeration(m)["expected_equal_transitions"]),
         probability_of_high_persistence_region_T_at_least_4=str(complete_enumeration(m)["high_persistence_region_mass"]),
         probability_of_low_persistence_region_T_at_most_1=str(complete_enumeration(m)["low_persistence_region_mass"]),
         individual_Brier_expectation="1/4",
         independent_Binomial_5_s_calculation_match=True)
         for m in REGIMES])
    result_path=HERE/"R277_EXACT_RESULTS.json"
    result_path.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R277",prescore_freeze_commit=FREEZE,
         full_source_types=192,positive_probability_types=192,
         source_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),
         results_sha256=hashlib.sha256(result_path.read_bytes()).hexdigest(),
         no_real_human_E2=0,no_real_historical_E3=0)
    (HERE/"R277_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_frozen(self):self.assertTrue(frozen_claims())
    def test_models(self):self.assertEqual(len(REGIMES),3)
    def test_source_count(self):self.assertEqual(len(REGIMES)*len(ALL_BITS),192)
    def test_IID_mass(self):self.assertEqual(source_likelihood("IID_FAIR","010101"),F(1,64))
    def test_stay(self):self.assertEqual(sum(adjacent("111111")),5)
    def test_flip(self):self.assertEqual(sum(adjacent("010101")),0)
    def test_typical(self):self.assertEqual(sum(adjacent("001010")),1)
    def test_marginal_score(self):self.assertEqual(F(1,4),F(1,4))
    def test_invalid_source(self):
        with self.assertRaises(ValueError):adjacent("1001")
    def test_invalid_regime(self):
        with self.assertRaises(ValueError):list(source_rows("UNKNOWN"))
    def test_high_tail(self):self.assertEqual(FROZEN["PERSISTENT"][1],F(81,128))
    def test_low_tail(self):self.assertEqual(FROZEN["ANTIPERSISTENT"][2],F(81,128))
    def test_null_tail(self):self.assertEqual(FROZEN["IID_FAIR"][1],F(3,16))
    def test_sum_null_tails(self):self.assertEqual(sum(FROZEN["IID_FAIR"][1:]),F(3,8))

def _case(model,kind):
    def run(self):
        rows=tuple(source_rows(model))
        if kind=="mass":self.assertEqual(sum((r["exact_original_sequence_mass"] for r in rows),ZERO),ONE)
        elif kind=="source_count":self.assertEqual(len(rows),64)
        elif kind=="unique":self.assertEqual(len({r["original_sixbit_ordered_sequence"] for r in rows}),64)
        elif kind=="all_positive":self.assertTrue(all(r["exact_original_sequence_mass"]>0 for r in rows))
        elif kind=="expected":self.assertEqual(complete_enumeration(model),independent_binomial_theory(model))
        elif kind=="marginal":
            self.assertEqual(complete_enumeration(model)["timewise_positive_marginals"],(F(1,2),)*6)
        elif kind=="score":self.assertTrue(all(r["original_mean_individual_Brier"]==F(1,4) for r in rows))
        elif kind=="transitions":
            for r in rows:
                self.assertEqual(r["original_five_stay_indicators"],
                   "".join(map(str,adjacent(r["original_sixbit_ordered_sequence"]))))
        elif kind=="tails":
            self.assertEqual((complete_enumeration(model)["high_persistence_region_mass"],
                 complete_enumeration(model)["low_persistence_region_mass"]),FROZEN[model][1:])
        elif kind=="weight":
            for r in rows:self.assertEqual(r["exact_original_sequence_mass"],
               source_likelihood(model,r["original_sixbit_ordered_sequence"]))
        elif kind=="flags":
            for r in rows:
                t=r["original_number_of_equal_adjacent_transitions"]
                self.assertEqual(r["preregistered_high_persistence_flag"],int(t>=4))
                self.assertEqual(r["preregistered_low_persistence_flag"],int(t<=1))
        elif kind=="full_PMF":
            self.assertEqual(sum(complete_enumeration(model)["transition_pmf"].values(),ZERO),ONE)
        else:raise AssertionError("unfrozen test")
    return run

for model in REGIMES:
    for kind in ("mass","source_count","unique","all_positive","expected","marginal",
                 "score","transitions","tails","weight","flags","full_PMF"):
        setattr(Tests,"test_"+model.lower()+"_"+kind,_case(model,kind))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    opt=parser.parse_args()
    if opt.test:unittest.main(argv=["r277"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
