#!/usr/bin/env python3
"""R270: exact six-bit Beta-Bernoulli posterior predictive checking.

Nine frozen worlds, 576 complete artificial replicate source configurations.
Route A enumerates ordered replicas. Route B uses beta-binomial and positive
run-composition counting without the ordered source enumeration.
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
FREEZE="5771124558a4c033cca9f5e2d0e6d7ea5315cc8c"
PRIORS=((1,1),(2,2),(1,3))
OBS={"BLOCKED":"111000","ALTERNATING":"101010","MIXED":"110010"}
WORLDS=tuple((a,b,name) for a,b in PRIORS for name in OBS)
ALL_REPLICAS=tuple("".join(v) for v in itertools.product("01",repeat=6))
ZERO,ONE=F(0),F(1)
LOCKED={
 ((1,1),"BLOCKED"):("26/99","129/143","529/858"),
 ((1,1),"ALTERNATING"):("1","10/429","529/858"),
 ((1,1),"MIXED"):("28/33","175/429","529/858"),
 ((2,2),"BLOCKED"):("71/286","131/143","89/143"),
 ((2,2),"ALTERNATING"):("1","7/286","89/143"),
 ((2,2),"MIXED"):("241/286","11/26","89/143"),
 ((1,3),"BLOCKED"):("196/715","49/55","5/11"),
 ((1,3),"ALTERNATING"):("1","16/715","5/11"),
 ((1,3),"MIXED"):("122/143","283/715","5/11")}

def validate(a,b,name):
    if (a,b,name) not in WORLDS:
        raise ValueError("outside frozen posterior predictive worlds")

def rising(x,n):
    if x<=0 or n<0:
        raise ValueError("invalid rising factorial")
    z=1
    for i in range(n):z*=x+i
    return z

def count(seq):
    if len(seq)!=6 or any(c not in "01" for c in seq):
        raise ValueError("requires ordered six bits")
    return seq.count("1")

def adjacent(seq):
    count(seq)
    return sum(seq[i]==seq[i+1] for i in range(5))

def name_id(a,b,name):
    validate(a,b,name)
    return f"BETA_{a}_{b}_{name}"

def posterior(a,b,name):
    validate(a,b,name)
    observed=OBS[name]
    k=count(observed)
    return a+k,b+6-k

def single_replicate_mass(A,B,seq):
    k=count(seq)
    return F(rising(A,k)*rising(B,6-k),rising(A+B,6))

def source_rows(a,b,name):
    """Route A: independent original enumeration of all 64 ordered replicas."""
    validate(a,b,name)
    obs=OBS[name]
    A,B=posterior(a,b,name)
    for seq in ALL_REPLICAS:
        yield dict(world=name_id(a,b,name),prior_a=a,prior_b=b,
           observed_design_name=name,original_observed_sixbit=obs,
           posterior_a=A,posterior_b=B,
           original_complete_replicate_sixbit=seq,
           original_replicate_success_count=count(seq),
           original_replicate_equal_adjacency_count=adjacent(seq),
           exact_original_posterior_predictive_mass=single_replicate_mass(A,B,seq))

def enumerated_distribution(a,b,name):
    validate(a,b,name)
    count_mass=defaultdict(lambda:ZERO)
    adj_mass=defaultdict(lambda:ZERO)
    total=ZERO
    ids=set()
    for row in source_rows(a,b,name):
        ids.add(row["original_complete_replicate_sixbit"])
        p=row["exact_original_posterior_predictive_mass"]
        count_mass[row["original_replicate_success_count"]]+=p
        adj_mass[row["original_replicate_equal_adjacency_count"]]+=p
        total+=p
    assert len(ids)==64 and total==ONE
    return {k:count_mass[k] for k in range(7)},{t:adj_mass[t] for t in range(6)}

def positive_compositions(total,runs):
    """How many ordered runs of strictly positive length sum to total."""
    if runs==0:return 1 if total==0 else 0
    if total<runs or runs<0:return 0
    return comb(total-1,runs-1)

def run_count(n,k,t):
    """Route B combinatorial sequence count, no enumeration of 2^n bitstrings."""
    if n!=6 or not 0<=k<=n or not 0<=t<n:
        raise ValueError("outside frozen adjacency count")
    if k in (0,n):
        return 1 if t==n-1 else 0
    r=n-t
    answer=0
    for first in (0,1):
        one_runs=(r+1)//2 if first==1 else r//2
        zero_runs=r-one_runs
        answer+=positive_compositions(k,one_runs)*positive_compositions(n-k,zero_runs)
    return answer

def independent_distribution(a,b,name):
    """Route B: k beta-binomial masses and combinatorial run counts."""
    validate(a,b,name)
    A,B=posterior(a,b,name)
    count_pmf={}
    adjacent_pmf={t:ZERO for t in range(6)}
    for k in range(7):
        sequence_weight=F(rising(A,k)*rising(B,6-k),rising(A+B,6))
        count_pmf[k]=comb(6,k)*sequence_weight
        assert sum(run_count(6,k,t) for t in range(6))==comb(6,k)
        for t in range(6):
            adjacent_pmf[t]+=run_count(6,k,t)*sequence_weight
    assert sum(count_pmf.values(),ZERO)==ONE
    assert sum(adjacent_pmf.values(),ZERO)==ONE
    return count_pmf,adjacent_pmf

def world_result(a,b,name):
    observed=OBS[name]
    observed_k=count(observed)
    observed_t=adjacent(observed)
    ecount,eadj=enumerated_distribution(a,b,name)
    bcount,badj=independent_distribution(a,b,name)
    if ecount!=bcount or eadj!=badj:
        raise AssertionError("exact replica enumeration vs run-composition mismatch")
    top=sum((v for t,v in eadj.items() if t>=observed_t),ZERO)
    bottom=sum((v for t,v in eadj.items() if t<=observed_t),ZERO)
    count_upper=sum((v for k,v in ecount.items() if k>=observed_k),ZERO)
    return dict(world=name_id(a,b,name),prior_a=a,prior_b=b,
      observed_name=name,original_observed_sixbit=observed,
      observed_count_K=observed_k,observed_equal_adjacencies_T=observed_t,
      posterior_Beta_a=posterior(a,b,name)[0],
      posterior_Beta_b=posterior(a,b,name)[1],
      original_full_ordered_replicate_sources=64,
      exact_replicate_success_count_PMF={str(k):str(v) for k,v in ecount.items()},
      exact_replicate_equal_adjacency_PMF={str(k):str(v) for k,v in eadj.items()},
      count_success_upper_tail=str(count_upper),
      adjacency_equal_upper_tail=str(top),
      adjacency_equal_lower_tail=str(bottom),
      independent_beta_binomial_and_run_composition_PMFs_verified=True)

def frozen_claims():
    assert len(WORLDS)==9 and len(ALL_REPLICAS)==64
    assert set(OBS.values())=={"111000","101010","110010"}
    assert all(count(s)==3 for s in OBS.values())
    assert adjacent(OBS["BLOCKED"])==4
    assert adjacent(OBS["ALTERNATING"])==0
    assert adjacent(OBS["MIXED"])==2
    assert sum(run_count(6,k,t) for k in range(7) for t in range(6))==64
    for a,b,name in WORLDS:
        r=world_result(a,b,name)
        expected=LOCKED[((a,b),name)]
        actual=(r["adjacency_equal_upper_tail"],r["adjacency_equal_lower_tail"],r["count_success_upper_tail"])
        assert actual==expected,(a,b,name,actual,expected)
    return True

def emit():
    frozen_claims()
    src=HERE/"R270_ALL_576_ORIGINAL_POSTERIOR_PREDICTIVE_REPLICATES.csv"
    keys=("world","prior_a","prior_b","observed_design_name",
      "original_observed_sixbit","posterior_a","posterior_b",
      "original_complete_replicate_sixbit","original_replicate_success_count",
      "original_replicate_equal_adjacency_count","exact_original_posterior_predictive_mass")
    with src.open("w",encoding="utf-8",newline="") as handle:
        writer=csv.DictWriter(handle,fieldnames=keys,lineterminator="\n")
        writer.writeheader()
        for a,b,name in WORLDS:
            for row in source_rows(a,b,name):
                writer.writerow({key:str(row[key]) for key in keys})
    results=dict(research_id="R270",original_catalogue_id="11-030",
      prescore_freeze_commit=FREEZE,
      scope="E1_ARTIFICIAL_EXACT_BETA_BERNOULLI_POSTERIOR_PREDICTIVE_ORDER_CHECK",
      world_count=9,complete_ordered_original_source_types=576,
      each_world_replicate_length=6,
      each_world_complete_replica_atoms=64,
      frozen_observation_success_count=3,
      all_nine_independent_beta_binomial_run_count_PMFs_verified=True,
      adjacency_lower_tail_flags_alternating_under_all_three_priors=True,
      count_statistic_blind_to_order_given_equal_success_count=True,
      no_real_human_E2=0,no_real_historical_E3=0,
      R073="FROZEN",PESEN_v0_1="FROZEN",
      world_results=[world_result(a,b,name) for a,b,name in WORLDS])
    resultpath=HERE/"R270_EXACT_POSTERIOR_PREDICTIVE_RESULTS.json"
    resultpath.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R270",prescore_freeze_commit=FREEZE,
      complete_source_types=576,independent_complete_PMF_pairs=9,
      source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
      results_sha256=hashlib.sha256(resultpath.read_bytes()).hexdigest(),
      no_real_human_E2=0,no_real_historical_E3=0)
    (HERE/"R270_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_64_sources(self):self.assertEqual(len(ALL_REPLICAS),64)
    def test_locked(self):self.assertTrue(frozen_claims())
    def test_observed_same_count(self):self.assertEqual({count(s) for s in OBS.values()},{3})
    def test_sequence_invalid(self):
        with self.assertRaises(ValueError):count("0000000")
    def test_rising(self):self.assertEqual(rising(3,4),360)
    def test_run_count_edge(self):self.assertEqual(run_count(6,0,5),1)
    def test_run_count_other_edge(self):self.assertEqual(run_count(6,6,5),1)
    def test_run_count_parity(self):self.assertEqual(sum(run_count(6,3,t) for t in range(6)),20)
    def test_outside_prior(self):
        with self.assertRaises(ValueError):list(source_rows(2,3,"BLOCKED"))
    def test_count_replicas(self):self.assertEqual(sum(len(tuple(source_rows(a,b,n))) for a,b,n in WORLDS),576)

def case(a,b,name,kind):
    def test(self):
        rows=tuple(source_rows(a,b,name))
        vals=world_result(a,b,name)
        if kind=="count":self.assertEqual(len(rows),64)
        elif kind=="unique":
            self.assertEqual({r["original_complete_replicate_sixbit"] for r in rows},set(ALL_REPLICAS))
        elif kind=="mass":
            self.assertEqual(sum((r["exact_original_posterior_predictive_mass"] for r in rows),ZERO),ONE)
        elif kind=="posterior":
            self.assertTrue(all(r["posterior_a"]==a+3 and r["posterior_b"]==b+3 for r in rows))
        elif kind=="count_stat":
            self.assertTrue(all(r["original_replicate_success_count"]==count(r["original_complete_replicate_sixbit"]) for r in rows))
        elif kind=="adj_stat":
            self.assertTrue(all(r["original_replicate_equal_adjacency_count"]==adjacent(r["original_complete_replicate_sixbit"]) for r in rows))
        elif kind=="independent":
            self.assertEqual(enumerated_distribution(a,b,name),independent_distribution(a,b,name))
        elif kind=="tails":
            self.assertEqual((vals["adjacency_equal_upper_tail"],vals["adjacency_equal_lower_tail"],vals["count_success_upper_tail"]),LOCKED[((a,b),name)])
        else:raise AssertionError("unknown testcase")
    return test

for a,b,name in WORLDS:
    for kind in ("count","unique","mass","posterior","count_stat","adj_stat","independent","tails"):
        setattr(Tests,f"test_beta_{a}_{b}_{name.lower()}_{kind}",case(a,b,name,kind))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    z=parser.parse_args()
    if z.test:unittest.main(argv=["r270"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
