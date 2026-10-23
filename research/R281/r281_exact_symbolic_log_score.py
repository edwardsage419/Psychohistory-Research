#!/usr/bin/env python3
"""R281 exact symbolic log-score audit over 240 fourbit Bernoulli source types.

Finite log scores are stored as rational a*ln(2)+b*ln(3), with any loss at a
reported zero probability represented as +INF, never clipped or discarded.
"""
import argparse
import csv
import hashlib
import itertools
import json
import math
import unittest
from fractions import Fraction as F
from math import comb
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="cbf8eec7db1ab7d78e4c8d3a03b0e0ae5acad2f3"
PS=(F(1,4),F(1,2),F(3,4))
QS=(F(0),F(1,4),F(1,2),F(3,4),F(1))
WORLDS=tuple((p,q) for p in PS for q in QS)
ALL_BITS=tuple("".join(z) for z in itertools.product("01",repeat=4))
ZERO,ONE=F(0),F(1)
def check(p,q):
    if (p,q) not in WORLDS:raise ValueError("outside frozen truth/report log-score world")

def model_name(p,q):
    check(p,q)
    return "TRUE_"+str(p).replace("/","OF")+"_REPORT_"+str(q).replace("/","OF")

def row_symbolic_score(q,y):
    """Return pair of rational ln2/ln3 coefficients, or None for +infinity."""
    if q not in QS or y not in (0,1):raise ValueError("unfrozen q or invalid outcome")
    if q==ZERO:return (ZERO,ZERO) if y==0 else None
    if q==ONE:return (ZERO,ZERO) if y==1 else None
    if q==F(1,2):return ONE,ZERO
    if q==F(1,4):return (F(2),ZERO) if y==1 else (F(2),F(-1))
    return (F(2),F(-1)) if y==1 else (F(2),ZERO)

def source_score(bits,q):
    if len(bits)!=4 or any(c not in "01" for c in bits) or q not in QS:
        raise ValueError("fourbit original source and frozen q needed")
    vals=tuple(row_symbolic_score(q,int(c)) for c in bits)
    if any(v is None for v in vals):return None,vals
    return (sum((v[0] for v in vals),ZERO)/4,
            sum((v[1] for v in vals),ZERO)/4),vals

def source_rows(p,q):
    """Route A all 16 original ordered fourbit types, exact source masses."""
    check(p,q)
    for bits in ALL_BITS:
        k=bits.count("1")
        result,rows=source_score(bits,q)
        inf=int(result is None)
        yield dict(world=model_name(p,q),true_p=p,reported_q=q,
          original_complete_fourbit_source=bits,original_success_count=k,
          original_source_probability=p**k*(ONE-p)**(4-k),
          original_four_symbolic_log_losses=";".join(
             "INF" if v is None else str(v[0])+","+str(v[1]) for v in rows),
          full_sample_infinite_log_loss_flag=inf,
          source_mean_log2_coefficient="" if result is None else result[0],
          source_mean_log3_coefficient="" if result is None else result[1])

def enumerated_world(p,q):
    """Route A exact probability of infinite score and symbolic finite expectation."""
    check(p,q)
    rows=tuple(source_rows(p,q))
    assert len(rows)==16 and len({r["original_complete_fourbit_source"] for r in rows})==16
    assert sum((r["original_source_probability"] for r in rows),ZERO)==ONE
    infin=sum((r["original_source_probability"]*r["full_sample_infinite_log_loss_flag"] for r in rows),ZERO)
    if infin>ZERO:return (True,infin,None)
    a=sum((r["original_source_probability"]*r["source_mean_log2_coefficient"] for r in rows),ZERO)
    b=sum((r["original_source_probability"]*r["source_mean_log3_coefficient"] for r in rows),ZERO)
    return False,ZERO,(a,b)

def independent_analytic_world(p,q):
    """Route B: no ordered source enumeration; Bernoulli(p) analytic row risk.

    For q boundaries, use complement probability of all four successes/failures.
    """
    check(p,q)
    if q==ZERO:return True,ONE-(ONE-p)**4,None
    if q==ONE:return True,ONE-p**4,None
    if q==F(1,4):return False,ZERO,(F(2),-(ONE-p))
    if q==F(1,2):return False,ZERO,(ONE,ZERO)
    return False,ZERO,(F(2),-p)

def truth_entropy_symbolic(p):
    if p not in PS:raise ValueError("unfrozen p")
    return independent_analytic_world(p,p)[2]

def kl_regret_symbolic(p,q):
    if q not in (F(1,4),F(1,2),F(3,4)):return None
    (_,_,reported)=independent_analytic_world(p,q)
    truth=truth_entropy_symbolic(p)
    return reported[0]-truth[0],reported[1]-truth[1]

def frozen_claims():
    assert len(WORLDS)==15 and len(ALL_BITS)==16
    assert len(WORLDS)*len(ALL_BITS)==240
    for p,q in WORLDS:
        a=enumerated_world(p,q)
        b=independent_analytic_world(p,q)
        assert a==b,(p,q,a,b)
        if q in (ZERO,ONE):
            assert a[0] and a[1]>ZERO and a[2] is None
        else:
            assert not a[0] and a[1]==ZERO
            regret=kl_regret_symbolic(p,q)
            if p==q:assert regret==(ZERO,ZERO)
            else:assert float(regret[0])*math.log(2)+float(regret[1])*math.log(3)>0
    assert enumerated_world(F(1,4),ZERO)[1]==F(175,256)
    assert enumerated_world(F(3,4),ONE)[1]==F(175,256)
    assert enumerated_world(F(1,2),ZERO)[1]==F(15,16)
    return True

def emit():
    frozen_claims()
    src=HERE/"R281_ALL_240_ORIGINAL_LOG_SCORE_SYMBOLIC_SOURCES.csv"
    cols=("world","true_p","reported_q","original_complete_fourbit_source",
          "original_success_count","original_source_probability",
          "original_four_symbolic_log_losses","full_sample_infinite_log_loss_flag",
          "source_mean_log2_coefficient","source_mean_log3_coefficient")
    with src.open("w",encoding="utf-8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=cols,lineterminator="\n")
        w.writeheader()
        for p,q in WORLDS:
            for row in source_rows(p,q):
                w.writerow({k:str(row[k]) for k in cols})
    results=dict(research_id="R281",original_catalogue_id="12-011",
       prescore_freeze_commit=FREEZE,
       evidence="BOUNDED_E1_ARTIFICIAL_SYMBOLIC_STRICTLY_PROPER_LOG_SCORE_WITH_INFINITY",
       world_count=15,complete_ordered_source_types=240,
       truth_rates=list(map(str,PS)),reports=list(map(str,QS)),
       finite_log_scores_are_exact_rational_ln2_ln3_linear_combinations=True,
       probability_zero_event_never_clipped=True,
       zero_probability_boundary_worlds_have_infinite_expected_log_loss=True,
       symbolic_expected_score_from_source_equals_independent_row_theory=True,
       no_real_human_E2=0,no_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       world_results=[dict(world=model_name(p,q),true_p=str(p),reported_q=str(q),
           original_sources=16,
           event_probability_infinite_log_score=str(enumerated_world(p,q)[1]),
           expected_log_score_infinite=enumerated_world(p,q)[0],
           expected_log2_coefficient=None if enumerated_world(p,q)[2] is None else str(enumerated_world(p,q)[2][0]),
           expected_log3_coefficient=None if enumerated_world(p,q)[2] is None else str(enumerated_world(p,q)[2][1]),
           expected_regret_log2_coefficient=None if kl_regret_symbolic(p,q) is None else str(kl_regret_symbolic(p,q)[0]),
           expected_regret_log3_coefficient=None if kl_regret_symbolic(p,q) is None else str(kl_regret_symbolic(p,q)[1]),
           analytic_score_and_infinite_probability_match=True)
           for p,q in WORLDS])
    jp=HERE/"R281_EXACT_RESULTS.json"
    jp.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R281",prescore_freeze_commit=FREEZE,
        all_complete_original_source_types=240,independent_analytic_worlds=15,
        source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
        results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
        no_real_human_E2=0,no_real_historical_E3=0)
    (HERE/"R281_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_frozen(self):self.assertTrue(frozen_claims())
    def test_world_count(self):self.assertEqual(len(WORLDS),15)
    def test_originals(self):self.assertEqual(len(ALL_BITS)*len(WORLDS),240)
    def test_ln2(self):self.assertEqual(row_symbolic_score(F(1,2),1),(ONE,ZERO))
    def test_ln4(self):self.assertEqual(row_symbolic_score(F(1,4),1),(F(2),ZERO))
    def test_ln43(self):self.assertEqual(row_symbolic_score(F(1,4),0),(F(2),F(-1)))
    def test_zero_outcome_boundary(self):self.assertIsNone(row_symbolic_score(ZERO,1))
    def test_one_outcome_boundary(self):self.assertIsNone(row_symbolic_score(ONE,0))
    def test_all_zero_bdry(self):self.assertEqual(source_score("0000",ZERO)[0],(ZERO,ZERO))
    def test_all_one_bdry(self):self.assertEqual(source_score("1111",ONE)[0],(ZERO,ZERO))
    def test_bad_score_source(self):
        with self.assertRaises(ValueError):source_score("011",F(1,2))
    def test_truth_entropy(self):self.assertEqual(truth_entropy_symbolic(F(1,4)),(F(2),F(-3,4)))
    def test_center_boundary(self):self.assertEqual(enumerated_world(F(1,2),ONE)[1],F(15,16))
    def test_posterior_not(self):
        with self.assertRaises(ValueError):list(source_rows(F(1,3),F(1,2)))

def case(p,q,kind):
    def test(self):
        rows=tuple(source_rows(p,q))
        if kind=="mass":self.assertEqual(sum((r["original_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="count":self.assertEqual(len(rows),16)
        elif kind=="unique":self.assertEqual(len({r["original_complete_fourbit_source"] for r in rows}),16)
        elif kind=="analytical":self.assertEqual(enumerated_world(p,q),independent_analytic_world(p,q))
        elif kind=="source":
            for r in rows:
                k=r["original_success_count"]
                self.assertEqual(r["original_source_probability"],p**k*(ONE-p)**(4-k))
        elif kind=="flags":
            for r in rows:
                score,_=source_score(r["original_complete_fourbit_source"],q)
                self.assertEqual(r["full_sample_infinite_log_loss_flag"],int(score is None))
        elif kind=="symbolic":
            for r in rows:
                value,_=source_score(r["original_complete_fourbit_source"],q)
                if value is None:self.assertEqual(r["source_mean_log2_coefficient"],"")
                else:self.assertEqual(r["source_mean_log2_coefficient"],value[0])
        elif kind=="strict":
            if q not in (ZERO,ONE) and q==p:
                self.assertEqual(kl_regret_symbolic(p,q),(ZERO,ZERO))
        else:raise AssertionError("unknown frozen test")
    return test
for p,q in WORLDS:
    for kind in ("mass","count","unique","analytical","source","flags","symbolic","strict"):
        setattr(Tests,"test_p"+str(p).replace("/","of")+"_q"+str(q).replace("/","of")+"_"+kind,case(p,q,kind))
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    args=parser.parse_args()
    if args.test:unittest.main(argv=["r281"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
