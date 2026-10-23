#!/usr/bin/env python3
"""R282: reproducible two-agent ABM, ODD2020 seven-element contract, full source replay.

Three explicit activation schedules each replay all 64 equally likely
primitive sixbit streams. There is no PRNG or human observational evidence.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import itertools
import json
import re
import unittest
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
FREEZE="5447354be84992df49810b59cd258405851d2eb9"
SCHEDULES=("SYNC","A_THEN_B","B_THEN_A")
SOURCE_INDEXES=tuple(range(64))
ODD=HERE/"R282_ODD2020_SEVEN_ELEMENT_MODEL_DESCRIPTION.md"
ODD_SECTIONS=(
 "Purpose and patterns",
 "Entities, state variables, and scales",
 "Process overview and scheduling",
 "Design concepts",
 "Initialization",
 "Input data",
 "Submodels",
)

def binary_source(i):
    if type(i) is not int or i not in SOURCE_INDEXES:
        raise ValueError("source index must be integer 0..63")
    return format(i,"06b")

def unpack(source):
    if not isinstance(source,str) or len(source)!=6 or any(c not in "01" for c in source):
        raise ValueError("expected six-bit a0,b0,eA0,eB0,eA1,eB1 source")
    return tuple(map(int,source))

def transition(state,innovations,schedule):
    if schedule not in SCHEDULES:raise ValueError("unfrozen schedule")
    a,b=state
    ea,eb=innovations
    if any(type(c) is not int or c not in (0,1) for c in (a,b,ea,eb)):
        raise ValueError("bits required")
    if schedule=="SYNC":return b^ea,a^eb
    if schedule=="A_THEN_B":
        new_a=b^ea
        return new_a,new_a^eb
    new_b=a^eb
    return new_b^ea,new_b

def replay(source,schedule):
    a,b,eA0,eB0,eA1,eB1=unpack(source)
    first=transition((a,b),(eA0,eB0),schedule)
    second=transition(first,(eA1,eB1),schedule)
    return ((a,b),first,second)

def row(source_index,schedule):
    source=binary_source(source_index)
    states=replay(source,schedule)
    return dict(schedule=schedule,
      primitive_source_index=source_index,
      original_sixbit_source=source,
      original_initial_A=states[0][0],original_initial_B=states[0][1],
      original_eA_t0=int(source[2]),original_eB_t0=int(source[3]),
      original_eA_t1=int(source[4]),original_eB_t1=int(source[5]),
      t0_state="".join(map(str,states[0])),
      t1_state="".join(map(str,states[1])),
      t2_state="".join(map(str,states[2])),
      exact_original_source_mass=F(1,64))

def original_rows():
    """Route A complete original source enumeration, schedule-major ordered."""
    for schedule in SCHEDULES:
        for index in SOURCE_INDEXES:
            yield row(index,schedule)

def independent_closed_form(source,schedule):
    """Route B: bit-algebra closed form t2, never calls transition or replay."""
    a,b,ea0,eb0,ea1,eb1=unpack(source)
    if schedule=="SYNC":
        # a1=b^ea0,b1=a^eb0; a2=b1^ea1,b2=a1^eb1.
        return (a^eb0^ea1,b^ea0^eb1)
    if schedule=="A_THEN_B":
        # a1=b^ea0, b1=b^ea0^eb0; a2=b1^ea1, b2=a2^eb1
        x=b^ea0^eb0^ea1
        return (x,x^eb1)
    if schedule=="B_THEN_A":
        # b1=a^eb0, a1=a^eb0^ea0; b2=a1^eb1, a2=b2^ea1
        x=a^eb0^ea0^eb1
        return (x^ea1,x)
    raise ValueError("not a frozen schedule")

def compute():
    rows=tuple(original_rows())
    assert len(rows)==192
    by_schedule={s:[r for r in rows if r["schedule"]==s] for s in SCHEDULES}
    summary=[]
    for schedule in SCHEDULES:
        data=by_schedule[schedule]
        assert len(data)==64
        assert len({r["original_sixbit_source"] for r in data})==64
        assert sum((r["exact_original_source_mass"] for r in data),F(0))==1
        final_counts=Counter(r["t2_state"] for r in data)
        assert final_counts=={"00":16,"01":16,"10":16,"11":16}
        assert all(r["t2_state"]=="".join(map(str,independent_closed_form(
           r["original_sixbit_source"],schedule))) for r in data)
        summary.append(dict(schedule=schedule,
          primitive_complete_source_types=64,
          terminal_joint_state_counts={k:final_counts[k] for k in ("00","01","10","11")},
          terminal_joint_state_probabilities={k:str(F(final_counts[k],64)) for k in ("00","01","10","11")}))
    paired={}
    for other in SCHEDULES[1:]:
        paired[other]={"t1_disagreement_source_count":sum(
          by_schedule["SYNC"][i]["t1_state"]!=by_schedule[other][i]["t1_state"] for i in SOURCE_INDEXES),
          "t2_disagreement_source_count":sum(
          by_schedule["SYNC"][i]["t2_state"]!=by_schedule[other][i]["t2_state"] for i in SOURCE_INDEXES)}
        assert paired[other]=={"t1_disagreement_source_count":32,
                               "t2_disagreement_source_count":48}
    compare=sum(by_schedule["A_THEN_B"][i]["t2_state"]!=
                by_schedule["B_THEN_A"][i]["t2_state"] for i in SOURCE_INDEXES)
    assert compare==48
    assert [by_schedule[s][1]["t2_state"] for s in SCHEDULES]==["01","01","11"]
    return summary,paired,compare

def verify_odd_7(text):
    """Minimal machine gate for structural seven-element ODD documentation.

    Existence of headings is necessary, not sufficient for standards compliance.
    """
    if not isinstance(text,str):raise ValueError("ODD must be text")
    sections=re.findall(r"^## ([1-7])\. (.+)$",text,re.MULTILINE)
    if len(sections)!=7:
        raise ValueError("all seven ODD headings required")
    if tuple((int(n),label) for n,label in sections)!=(tuple(enumerate(ODD_SECTIONS,1))):
        raise ValueError("ODD headings missing, reordered, renamed or duplicated")
    tokens=("SYNC","A_THEN_B","B_THEN_A","source_index","eA0","eB0","eA1","eB1")
    for token in tokens:
        if token not in text:raise ValueError("missing source and scheduling terms: "+token)
    return True

def frozen_claims():
    assert len(SOURCE_INDEXES)==64 and len(SCHEDULES)==3
    assert verify_odd_7(ODD.read_text(encoding="utf-8"))
    assert compute()[2]==48
    return True

def emit():
    frozen_claims()
    source_path=HERE/"R282_ALL_192_ORIGINAL_ODD_SCHEDULE_SOURCES.csv"
    fields=("schedule","primitive_source_index","original_sixbit_source",
         "original_initial_A","original_initial_B",
         "original_eA_t0","original_eB_t0","original_eA_t1","original_eB_t1",
         "t0_state","t1_state","t2_state","exact_original_source_mass")
    with source_path.open("w",encoding="utf-8",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        writer.writeheader()
        for r in original_rows():
            writer.writerow({k:str(r[k]) for k in fields})
    schedules,paired,between=compute()
    result=dict(research_id="R282",original_catalogue_id="12-012",
       prescore_freeze_commit=FREEZE,
       evidence="E1_COMPLETE_ARTIFICIAL_ABM_ODD_2020_SEVEN_SECTIONS_SCHEDULE_REPLAY",
       odd2020_sections=list(ODD_SECTIONS),odd_has_all_seven_structural_headings=True,
       complete_schedule_labeled_source_types=192,complete_primitive_sources_per_schedule=64,
       original_source_index_is_bitstream_enumerator_not_prng_seed=True,
       real_empirical_input_data=False,
       all_schedule_terminal_marginals_identical_uniform=True,
       source_index_1_terminal_counterexample={"SYNC":"01","A_THEN_B":"01","B_THEN_A":"11"},
       synchronous_vs_asynchronous_paired_source_disagreements=paired,
       two_asynchronous_schedules_t2_disagreement_count=between,
       schedule_results=schedules,
       no_real_human_E2=0,no_real_historical_E3=0,
       R073="FROZEN",PESEN_v0_1="FROZEN")
    result_path=HERE/"R282_EXACT_ODD_REPLAY_RESULTS.json"
    result_path.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    receipt=dict(research_id="R282",prescore_freeze_commit=FREEZE,
       complete_original_source_types=192,independent_closed_form_checks=192,
       original_source_sha256=hashlib.sha256(source_path.read_bytes()).hexdigest(),
       results_sha256=hashlib.sha256(result_path.read_bytes()).hexdigest(),
       odd_seven_sections_sha256=hashlib.sha256(ODD.read_bytes()).hexdigest(),
       no_real_human_E2=0,no_real_historical_E3=0)
    (HERE/"R282_MACHINE_RECEIPT.json").write_text(json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_complete(self):self.assertTrue(frozen_claims())
    def test_64_indexes(self):self.assertEqual(len(SOURCE_INDEXES),64)
    def test_3_schedules(self):self.assertEqual(len(SCHEDULES),3)
    def test_zero(self):self.assertEqual(binary_source(0),"000000")
    def test_last(self):self.assertEqual(binary_source(63),"111111")
    def test_invalid_negative(self):
        with self.assertRaises(ValueError):binary_source(-1)
    def test_invalid_bool(self):
        with self.assertRaises(ValueError):binary_source(True)
    def test_invalid_source(self):
        with self.assertRaises(ValueError):unpack("001")
    def test_invalid_schedule(self):
        with self.assertRaises(ValueError):replay("000000","WRONG")
    def test_source_one(self):
        self.assertEqual(tuple("".join(map(str,replay("000001",s)[-1])) for s in SCHEDULES),
          ("01","01","11"))
    def test_repeat(self):self.assertEqual(replay("100101","SYNC"),replay("100101","SYNC"))
    def test_per_schedule_balanced(self):
        self.assertTrue(all(v==16 for obj in compute()[0] for v in obj["terminal_joint_state_counts"].values()))
    def test_pair_divergence(self):self.assertEqual(compute()[2],48)
    def test_odd_headings(self):self.assertTrue(verify_odd_7(ODD.read_text()))
    def test_odd_missing_last(self):
        text=ODD.read_text().replace("## 7. Submodels","## 7. INVALID")
        with self.assertRaises(ValueError):verify_odd_7(text)
    def test_odd_missing_schedule(self):
        text=ODD.read_text().replace("## 3. Process overview and scheduling","## 3. UNKNOWN")
        with self.assertRaises(ValueError):verify_odd_7(text)
    def test_odd_duplicate_heading(self):
        text=ODD.read_text()+"\n## 1. Purpose and patterns\n"
        with self.assertRaises(ValueError):verify_odd_7(text)

def _case(schedule,kind):
    def test(self):
        rows=[r for r in original_rows() if r["schedule"]==schedule]
        if kind=="count":self.assertEqual(len(rows),64)
        elif kind=="mass":self.assertEqual(sum((r["exact_original_source_mass"] for r in rows),F(0)),F(1))
        elif kind=="all_sources":self.assertEqual({r["original_sixbit_source"] for r in rows},{binary_source(i) for i in SOURCE_INDEXES})
        elif kind=="replay":
            self.assertTrue(all(r["t2_state"]=="".join(map(str,replay(r["original_sixbit_source"],schedule)[-1])) for r in rows))
        elif kind=="algebra":
            self.assertTrue(all(r["t2_state"]=="".join(map(str,independent_closed_form(r["original_sixbit_source"],schedule))) for r in rows))
        elif kind=="terminal":
            self.assertEqual(Counter(r["t2_state"] for r in rows),{"00":16,"01":16,"10":16,"11":16})
        elif kind=="first":
            self.assertTrue(all(r["t0_state"]==r["original_sixbit_source"][:2] for r in rows))
        elif kind=="disturbances":
            self.assertTrue(all(r["original_eA_t0"]==int(r["original_sixbit_source"][2]) for r in rows))
        elif kind=="indexes":
            self.assertTrue(all(binary_source(r["primitive_source_index"])==r["original_sixbit_source"] for r in rows))
        elif kind=="stable":
            self.assertEqual(tuple(row(i,schedule) for i in SOURCE_INDEXES),tuple(row(i,schedule) for i in SOURCE_INDEXES))
        elif kind=="equalbits":
            self.assertEqual(sum(r["t2_state"][0]==r["t2_state"][1] for r in rows),32)
        else:raise AssertionError("unknown test")
    return test

for schedule in SCHEDULES:
    for kind in ("count","mass","all_sources","replay","algebra","terminal","first",
                 "disturbances","indexes","stable","equalbits"):
        setattr(Tests,"test_"+schedule.lower()+"_"+kind,_case(schedule,kind))

for index in SOURCE_INDEXES:
    def make_case(i):
        def tester(self):
            bits=binary_source(i)
            for s in SCHEDULES:
                self.assertEqual(replay(bits,s)[-1],independent_closed_form(bits,s))
        return tester
    setattr(Tests,"test_independent_bit_formula_"+str(index),make_case(index))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    opts=parser.parse_args()
    if opts.test:unittest.main(argv=["r282"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
