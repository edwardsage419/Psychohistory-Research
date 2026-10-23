#!/usr/bin/env python3
"""R280: exact binary Brier strict propriety versus finite-sample score ranking.

Nine (true Bernoulli p, reported q) worlds, each 16 complete fourbit ordered
sources with Fraction probability. Nonoracle q fixed before all observations.
"""
import argparse
import csv
import hashlib
import itertools
import json
import unittest
from fractions import Fraction as F
from math import comb
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="b21848cd58d9f9d581ce79c685467c49c32a6897"
PROBS=(F(1,4),F(1,2),F(3,4))
WORLDS=tuple((p,q) for p in PROBS for q in PROBS)
ALL_BITS=tuple("".join(v) for v in itertools.product("01",repeat=4))
ZERO,ONE=F(0),F(1)
LOCKED={
(F(1,4),F(1,4)):(F(3,16),ZERO,ZERO,ONE),
(F(1,4),F(1,2)):(F(1,4),F(1,16),F(67,256),ZERO),
(F(1,4),F(3,4)):(F(7,16),F(1,4),F(13,256),F(27,128)),
(F(1,2),F(1,4)):(F(5,16),F(1,16),F(5,16),ZERO),
(F(1,2),F(1,2)):(F(1,4),ZERO,ZERO,ONE),
(F(1,2),F(3,4)):(F(5,16),F(1,16),F(5,16),ZERO),
(F(3,4),F(1,4)):(F(7,16),F(1,4),F(13,256),F(27,128)),
(F(3,4),F(1,2)):(F(1,4),F(1,16),F(67,256),ZERO),
(F(3,4),F(3,4)):(F(3,16),ZERO,ZERO,ONE)
}
def check(p,q):
    if (p,q) not in WORLDS:raise ValueError("unfrozen truth or forecast")

def name(p,q):
    check(p,q)
    return "TRUE_"+str(p).replace("/","OF")+"_REPORT_"+str(q).replace("/","OF")

def average_loss(bits,q):
    if len(bits)!=4 or any(z not in "01" for z in bits) or q not in PROBS:
        raise ValueError("fourbit source and frozen probability needed")
    return sum(((F(int(z))-q)**2 for z in bits),ZERO)/4

def source_rows(p,q):
    """Route A original ordered primitive source, both fixed-forecast scores."""
    check(p,q)
    for bits in ALL_BITS:
        k=bits.count("1")
        mass=p**k*(ONE-p)**(4-k)
        forecast=average_loss(bits,q)
        oracle=average_loss(bits,p)
        yield dict(world=name(p,q),true_p=p,reported_q=q,
           original_complete_fourbit_source=bits,
           successes=k,source_probability=mass,
           source_four_reported_Brier_losses=";".join(str((F(int(z))-q)**2) for z in bits),
           source_four_oracle_Brier_losses=";".join(str((F(int(z))-p)**2) for z in bits),
           source_mean_reported_Brier=forecast,
           source_mean_truth_oracle_Brier=oracle,
           source_score_regret=forecast-oracle,
           incorrect_fixed_forecast_beats_truth_on_source=int(forecast<oracle),
           score_tied_with_truth_on_source=int(forecast==oracle))

def weighted_results(p,q):
    check(p,q)
    rows=tuple(source_rows(p,q))
    assert len(rows)==16 and len({r["original_complete_fourbit_source"] for r in rows})==16
    assert sum((r["source_probability"] for r in rows),ZERO)==ONE
    return (
       sum((r["source_probability"]*r["source_mean_reported_Brier"] for r in rows),ZERO),
       sum((r["source_probability"]*r["source_score_regret"] for r in rows),ZERO),
       sum((r["source_probability"]*r["incorrect_fixed_forecast_beats_truth_on_source"] for r in rows),ZERO),
       sum((r["source_probability"]*r["score_tied_with_truth_on_source"] for r in rows),ZERO)
    )

def independent_binomial_analytic(p,q):
    """Route B has only K~Binomial(4,p) five count classes, not original bits."""
    check(p,q)
    risk=p*(ONE-q)**2+(ONE-p)*q*q
    regret=(q-p)**2
    winner=tie=ZERO
    for k in range(5):
        mass=F(comb(4,k))*p**k*(ONE-p)**(4-k)
        qscore=(F(k)*(ONE-q)**2+F(4-k)*q*q)/4
        pscore=(F(k)*(ONE-p)**2+F(4-k)*p*p)/4
        if qscore<pscore:winner+=mass
        if qscore==pscore:tie+=mass
    return risk,regret,winner,tie

def frozen_claims():
    assert len(WORLDS)==len(LOCKED)==9
    assert len(ALL_BITS)==16
    for p,q in WORLDS:
        a=weighted_results(p,q)
        b=independent_binomial_analytic(p,q)
        assert a==b==LOCKED[p,q],(p,q,a,b,LOCKED[p,q])
        assert a[1]>=ZERO
        assert a[1]==ZERO if q==p else a[1]>ZERO
    assert LOCKED[F(1,2),F(1,4)][2]==F(5,16)
    return True

def emit():
    frozen_claims()
    csvpath=HERE/"R280_ALL_144_ORIGINAL_BRIER_SCORING_SOURCES.csv"
    cols=("world","true_p","reported_q","original_complete_fourbit_source",
       "successes","source_probability",
       "source_four_reported_Brier_losses","source_four_oracle_Brier_losses",
       "source_mean_reported_Brier","source_mean_truth_oracle_Brier",
       "source_score_regret","incorrect_fixed_forecast_beats_truth_on_source",
       "score_tied_with_truth_on_source")
    with csvpath.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        writer.writeheader()
        for p,q in WORLDS:
            for row in source_rows(p,q):
                writer.writerow({k:str(row[k]) for k in cols})
    result=dict(research_id="R280",original_catalogue_id="12-010",
       prescore_freeze_commit=FREEZE,
       evidence="E1_EXACT_FINITE_BERNOULLI_BRIER_STRICT_PROPRIETY_AND_SAMPLE_WINNER",
       world_count=9,complete_original_source_types=144,
       original_sequences_per_world=16,
       all_nine_exact_source_vs_independent_binomial_results_identical=True,
       expected_Brier_equals_p_times_one_minus_p_plus_squared_forecast_bias=True,
       four_observation_sample_can_favor_misspecified_forecast=True,
       no_real_human_E2=0,no_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[dict(world=name(p,q),true_p=str(p),reported_q=str(q),
         source_types=16,
         expected_reported_Brier=str(weighted_results(p,q)[0]),
         expected_excess_Brier_regret=str(weighted_results(p,q)[1]),
         probability_incorrect_fixed_report_beats_truth_in_fourbit_sample=str(weighted_results(p,q)[2]),
         probability_report_and_truth_tie_in_fourbit_sample=str(weighted_results(p,q)[3]),
         independent_binomial_analytic_verified=True)
         for p,q in WORLDS])
    jp=HERE/"R280_EXACT_RESULTS.json"
    jp.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R280",prescore_freeze_commit=FREEZE,
      source_types=144,analytic_worlds_verified=9,
      source_sha256=hashlib.sha256(csvpath.read_bytes()).hexdigest(),
      results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
      no_real_human_E2=0,no_real_historical_E3=0)
    (HERE/"R280_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_frozen(self):self.assertTrue(frozen_claims())
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_sources(self):self.assertEqual(len(ALL_BITS),16)
    def test_zero_loss(self):self.assertEqual(average_loss("1111",ONE if ONE in PROBS else F(3,4)),F(1,16))
    def test_center_risk(self):self.assertEqual(independent_binomial_analytic(F(1,2),F(1,2))[0],F(1,4))
    def test_oracle_optimum(self):self.assertEqual(independent_binomial_analytic(F(1,4),F(1,4))[1],ZERO)
    def test_finite_wrong_winner(self):self.assertEqual(independent_binomial_analytic(F(1,2),F(1,4))[2],F(5,16))
    def test_finite_tie(self):self.assertEqual(independent_binomial_analytic(F(1,4),F(3,4))[3],F(27,128))
    def test_bad_probability(self):
        with self.assertRaises(ValueError):list(source_rows(F(1,3),F(1,2)))
    def test_bad_seq(self):
        with self.assertRaises(ValueError):average_loss("000",F(1,4))
    def test_strict_regret(self):self.assertEqual(independent_binomial_analytic(F(1,4),F(3,4))[1],F(1,4))

def case(p,q,mode):
    def test(self):
        rows=tuple(source_rows(p,q))
        if mode=="mass":self.assertEqual(sum((r["source_probability"] for r in rows),ZERO),ONE)
        elif mode=="count":self.assertEqual(len(rows),16)
        elif mode=="unique":self.assertEqual(len({r["original_complete_fourbit_source"] for r in rows}),16)
        elif mode=="risk":self.assertEqual(weighted_results(p,q),independent_binomial_analytic(p,q))
        elif mode=="locked":self.assertEqual(weighted_results(p,q),LOCKED[p,q])
        elif mode=="regret":self.assertEqual(weighted_results(p,q)[1],(p-q)**2)
        elif mode=="source":
            for r in rows:
                seq=r["original_complete_fourbit_source"]
                self.assertEqual(r["source_mean_reported_Brier"],average_loss(seq,q))
                self.assertEqual(r["source_mean_truth_oracle_Brier"],average_loss(seq,p))
        elif mode=="flags":
            for r in rows:
                self.assertEqual(r["incorrect_fixed_forecast_beats_truth_on_source"],
                   int(r["source_mean_reported_Brier"]<r["source_mean_truth_oracle_Brier"]))
        else:raise AssertionError("unfrozen test")
    return test
for p,q in WORLDS:
    for mode in ("mass","count","unique","risk","locked","regret","source","flags"):
        setattr(Tests,"test_p"+str(p).replace("/","of")+"_q"+str(q).replace("/","of")+"_"+mode,case(p,q,mode))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    a=parser.parse_args()
    if a.test:unittest.main(argv=["r280"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
