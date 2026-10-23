#!/usr/bin/env python3
"""R271 finite artificial null worlds: preregistered test versus p-value search.

The exact source space comprises 13,104 policy-labelled configurations.
These are mathematical types, not observational samples or evidence for real
registered-report institutions.
"""
from __future__ import annotations
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
FREEZE="b5a1d888ee830759f599cf39cae8120ed3f84d59"
ALPHA=F(1,8)
M=(1,2,3)
POLICIES=("FROZEN_FIRST","FLEXIBLE_ANY","BONFERRONI_ANY")
WORLDS=tuple((m,p) for m in M for p in POLICIES)
ZERO,ONE=F(0),F(1)
LOCKED={
 (1,"FROZEN_FIRST"):F(1,16),
 (1,"FLEXIBLE_ANY"):F(1,16),
 (1,"BONFERRONI_ANY"):F(1,16),
 (2,"FROZEN_FIRST"):F(1,16),
 (2,"FLEXIBLE_ANY"):F(31,256),
 (2,"BONFERRONI_ANY"):F(31,256),
 (3,"FROZEN_FIRST"):F(1,16),
 (3,"FLEXIBLE_ANY"):F(721,4096),
 (3,"BONFERRONI_ANY"):ZERO}


def validate(m,policy):
    if (m,policy) not in WORLDS:
        raise ValueError("outside frozen nine preregistration worlds")


def raw_p_value(k):
    if not isinstance(k,int) or not 0<=k<=4:
        raise ValueError("four-bit success count required")
    return F(sum(comb(4,t) for t in range(k,5)),16)


def extract_blocks(bits,m):
    if m not in M or len(bits)!=4*m or any(c not in "01" for c in bits):
        raise ValueError("requires full ordered 4m null binary sequence")
    return tuple(bits[4*j:4*j+4] for j in range(m))


def decide(m,policy,ps):
    validate(m,policy)
    if len(ps)!=m or any(not 0<=v<=1 for v in ps):
        raise ValueError("all candidates required")
    if policy=="FROZEN_FIRST":
        return 0 if ps[0]<=ALPHA else -1
    cutoff=ALPHA if policy=="FLEXIBLE_ANY" else ALPHA/m
    for i,v in enumerate(ps):
        if v<=cutoff:
            return i
    return -1


def original_source_rows(m,policy):
    """Route A: full ordered independent fair bit configurations."""
    validate(m,policy)
    mass=F(1,2**(4*m))
    for tup in itertools.product("01",repeat=4*m):
        original="".join(tup)
        blocks=extract_blocks(original,m)
        counts=tuple(block.count("1") for block in blocks)
        ps=tuple(raw_p_value(k) for k in counts)
        selected=decide(m,policy,ps)
        yield dict(world=f"M{m}_{policy}",family_test_count=m,policy=policy,
          original_complete_independent_null_bit_sequence=original,
          original_block_success_counts=";".join(map(str,counts)),
          original_all_block_raw_one_sided_pvalues=";".join(map(str,ps)),
          original_source_probability=mass,
          frozen_familywise_nominal_alpha=ALPHA,
          declared_positive=int(selected>=0),
          reported_test_index=selected)


def exact_source_probability(m,policy):
    validate(m,policy)
    total=ZERO
    declared=ZERO
    unique=set()
    count=0
    for row in original_source_rows(m,policy):
        token=row["original_complete_independent_null_bit_sequence"]
        assert token not in unique
        unique.add(token)
        count+=1
        mass=row["original_source_probability"]
        total+=mass
        if row["declared_positive"]:declared+=mass
    assert total==ONE and count==2**(4*m)
    return declared,count


def independent_analytic_null_risk(m,policy):
    """Route B: independent Bernoulli block probability algebra; no enumeration."""
    validate(m,policy)
    each=F(1,16)
    if policy=="FROZEN_FIRST":
        return each
    if policy=="FLEXIBLE_ANY":
        return ONE-(ONE-each)**m
    return (ONE-(ONE-each)**m) if each<=ALPHA/m else ZERO


def frozen_claims():
    assert len(WORLDS)==len(LOCKED)==9
    assert sum(3*2**(4*m) for m in M)==13104
    assert [raw_p_value(i) for i in range(5)]==[
        ONE,F(15,16),F(11,16),F(5,16),F(1,16)]
    for m,policy in WORLDS:
        risk,count=exact_source_probability(m,policy)
        analytical=independent_analytic_null_risk(m,policy)
        assert risk==analytical==LOCKED[m,policy],(m,policy,risk,analytical)
        assert count==2**(4*m)
    assert LOCKED[3,"FLEXIBLE_ANY"]>ALPHA
    assert LOCKED[2,"BONFERRONI_ANY"]<ALPHA
    return True


def emit():
    frozen_claims()
    src=HERE/"R271_ALL_13104_ORIGINAL_NULL_POLICY_SOURCE_TYPES.csv"
    columns=("world","family_test_count","policy",
      "original_complete_independent_null_bit_sequence",
      "original_block_success_counts",
      "original_all_block_raw_one_sided_pvalues",
      "original_source_probability","frozen_familywise_nominal_alpha",
      "declared_positive","reported_test_index")
    with src.open("w",encoding="utf-8",newline="") as f:
        wr=csv.DictWriter(f,fieldnames=columns,lineterminator="\n")
        wr.writeheader()
        for m,policy in WORLDS:
            for row in original_source_rows(m,policy):
                wr.writerow({key:str(row[key]) for key in columns})
    results=dict(research_id="R271",original_catalogue_id="12-001",
       prescore_freeze_commit=FREEZE,
       evidence="E1_FINITE_ARTIFICIAL_NULL_MULTIPLE_TESTING_DECISION_PROTOCOL",
       true_null="all original observations iid Bernoulli(1/2)",
       nominal_familywise_alpha=str(ALPHA),
       candidate_block_size=4,frozen_candidate_family_sizes=list(M),
       total_original_source_types=13104,
       distinct_primitive_source_types_across_m=16+256+4096,
       all_nine_independent_exact_analytic_source_risks_match=True,
       preregistration_governance_or_real_registered_report_effect_not_tested=True,
       no_real_human_E2=0,no_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN",
       worlds=[dict(world=f"M{m}_{policy}",family_count=m,decision_policy=policy,
          original_complete_source_types=2**(4*m),
          exact_null_probability_of_any_reported_positive=str(exact_source_probability(m,policy)[0]),
          independent_math_verified=True)
          for m,policy in WORLDS])
    jp=HERE/"R271_EXACT_NULL_REPORTING_RESULTS.json"
    jp.write_text(json.dumps(results,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(research_id="R271",prescore_freeze_commit=FREEZE,
       all_complete_original_source_types=13104,
       independent_analytic_policy_worlds=9,
       source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(jp.read_bytes()).hexdigest(),
       no_real_human_E2=0,no_real_historical_E3=0)
    (HERE/"R271_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt


class Tests(unittest.TestCase):
    def test_all_frozen(self):self.assertTrue(frozen_claims())
    def test_alpha(self):self.assertEqual(ALPHA,F(1,8))
    def test_worlds(self):self.assertEqual(len(WORLDS),9)
    def test_complete_sources(self):self.assertEqual(sum(3*2**(4*m) for m in M),13104)
    def test_probability_all_ones(self):self.assertEqual(raw_p_value(4),F(1,16))
    def test_raw_p_monotone(self):self.assertEqual([raw_p_value(k) for k in range(5)],sorted([raw_p_value(k) for k in range(5)],reverse=True))
    def test_flexible_inflated(self):self.assertGreater(independent_analytic_null_risk(3,"FLEXIBLE_ANY"),ALPHA)
    def test_bonf_m3(self):self.assertEqual(independent_analytic_null_risk(3,"BONFERRONI_ANY"),ZERO)
    def test_invalid_count(self):
        with self.assertRaises(ValueError):raw_p_value(5)
    def test_invalid_design(self):
        with self.assertRaises(ValueError):list(original_source_rows(4,"FLEXIBLE_ANY"))


def _case(m,policy,kind):
    def test(self):
        rows=tuple(original_source_rows(m,policy))
        if kind=="count":self.assertEqual(len(rows),2**(4*m))
        elif kind=="unique":
            self.assertEqual(len({r["original_complete_independent_null_bit_sequence"] for r in rows}),len(rows))
        elif kind=="source":
            self.assertTrue(all(F(r["original_source_probability"])==F(1,2**(4*m)) for r in rows))
        elif kind=="mass":
            self.assertEqual(sum((r["original_source_probability"] for r in rows),ZERO),ONE)
        elif kind=="pvalues":
            for row in rows:
                bits=row["original_complete_independent_null_bit_sequence"]
                cnts=[b.count("1") for b in extract_blocks(bits,m)]
                self.assertEqual(row["original_block_success_counts"],";".join(map(str,cnts)))
                self.assertEqual(row["original_all_block_raw_one_sided_pvalues"],";".join(str(raw_p_value(c)) for c in cnts))
        elif kind=="risk":
            self.assertEqual(exact_source_probability(m,policy)[0],LOCKED[m,policy])
        elif kind=="decisions":
            for row in rows:
                values=tuple(F(v) for v in row["original_all_block_raw_one_sided_pvalues"].split(";"))
                choice=decide(m,policy,values)
                self.assertEqual(int(row["reported_test_index"]),choice)
                self.assertEqual(int(row["declared_positive"]),int(choice>=0))
        elif kind=="formula":
            self.assertEqual(independent_analytic_null_risk(m,policy),LOCKED[m,policy])
        else:raise AssertionError("unfrozen test")
    return test

for m,policy in WORLDS:
    for kind in ("count","unique","source","mass","pvalues","risk","decisions","formula"):
        setattr(Tests,f"test_m{m}_{policy.lower()}_{kind}",_case(m,policy,kind))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--emit",action="store_true")
    z=parser.parse_args()
    if z.test:unittest.main(argv=["r271"],verbosity=2)
    else:print(json.dumps(emit(),indent=2))
