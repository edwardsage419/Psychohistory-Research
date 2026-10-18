#!/usr/bin/env python3
"""R108 B2: six 300-source-row blocks versus person-level original eligibility.

Five original column values parsed transiently; no raw values included in report.
Original actor/dyad identity and human action outcomes never inferred from codes.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
from decimal import Decimal,InvalidOperation
import io
import json
import pathlib
import re

import r108_phase_a1_original_2017_Leicester_fixed_pair_CSV_MD5_double_SHA_header_only as a
import r108_phase_a3_verified_Figshare_publisher_S3_delegate_MD5_double_source as s
import r108_phase_a4_verified_full_original_MD5_header_class_only as b

PINNED_SHA="e7dbb6ddc96cc5c65368be0d1918c3ebc7a83c14addd03ab44eeb07790575c18"
DATA_N=1800
BLOCKS=6
BLOCK_N=300
PREAMBLE_N=4
VALUE_CLASSES=("NONNUMERIC","NEGATIVE","ZERO","ONE","BETWEEN_ZERO_ONE","GREATER_THAN_ONE")

def posinteger(x):
    if not isinstance(x,str) or re.fullmatch(r"[0-9]{1,20}",x.strip(),flags=re.ASCII) is None:
        return None
    try:v=int(x)
    except ValueError:return None
    return v if v>0 else None

def valclass(x):
    try:
        d=Decimal(x.strip())
    except (InvalidOperation,ValueError,AttributeError):
        return "NONNUMERIC"
    if not d.is_finite():return "NONNUMERIC"
    if d<0:return "NEGATIVE"
    if d==0:return "ZERO"
    if d==1:return "ONE"
    if d<1:return "BETWEEN_ZERO_ONE"
    return "GREATER_THAN_ONE"

def real_source_block_schema_only(raw):
    e1=b.class_only(raw)
    if e1["project_original_complete_SHA256"]!=PINNED_SHA:
        raise a.SourceError("R108_B2_ORIGINAL_FULL_SOURCE_SHA_NOT_PINNED")
    try:
        rows=list(csv.reader(io.StringIO(raw.decode("utf-8-sig"),newline=""),strict=True))
    except (UnicodeError,csv.Error) as exc:
        raise a.SourceError("R108_B2_ORIGINAL_SOURCE_CSV_SYNTAX_INVALID") from exc
    if len(rows)!=1+PREAMBLE_N+DATA_N or any(len(r)!=5 for r in rows):
        raise a.SourceError("R108_B2_SOURCE_FIVE_FIELD_1804_ROWS_NOT_VERIFIED")
    # Header and four preamble lines are skipped verbatim; NEVER export their text.
    body=rows[1+PREAMBLE_N:]
    numeric_valid=[0,0,0]
    all_codes=[set(),set(),set()]
    value_hists=[Counter(),Counter()]
    source_blocks=[]
    group_pairs=[]
    exact_rounds=True
    for block in range(BLOCKS):
        segment=body[block*BLOCK_N:(block+1)*BLOCK_N]
        slot1=set();slot2=set()
        for j,row in enumerate(segment):
            ints=[posinteger(row[i]) for i in (0,1,2)]
            for slot,val in enumerate(ints):
                if val is not None:
                    numeric_valid[slot]+=1
                    all_codes[slot].add(val)
            if ints[0]!=j+1:exact_rounds=False
            if ints[1] is not None:slot1.add(ints[1])
            if ints[2] is not None:slot2.add(ints[2])
            for z in (0,1):value_hists[z][valclass(row[3+z])]+=1
        source_blocks.append({
            "anonymous_block_slot":block+1,
            "source_rows":len(segment),
            "slot1_distinct_undecoded_code_count":len(slot1),
            "slot2_distinct_undecoded_code_count":len(slot2),
            "slot1_invariant_within_block":len(slot1)==1,
            "slot2_invariant_within_block":len(slot2)==1,
        })
        if len(slot1)==len(slot2)==1:
            group_pairs.append((next(iter(slot1)),next(iter(slot2))))
    all_valid=all(v==DATA_N for v in numeric_valid)
    condition_matrix=(all_valid and exact_rounds and
        len(all_codes[1])==2 and len(all_codes[2])==3 and
        all(z["slot1_invariant_within_block"] and z["slot2_invariant_within_block"] for z in source_blocks)
        and len(group_pairs)==6 and len(set(group_pairs))==6)
    # This is a structural categorical time-series flag, NOT an assertion
    # that any source condition code is a real participant or session.
    return {
        "research_id":"R108","phase":"B2",
        "status":"R108_B2_ORIGINAL_SIX_300_CONDITION_SOURCE_TRACES_E1_NOT_ACTOR_E2" if condition_matrix else "R108_B2_ORIGINAL_SOURCE_BLOCK_SCHEMA_INCONCLUSIVE_E1_NOT_ACTOR_E2",
        "original_whole_SHA256":PINNED_SHA,
        "original_publisher_MD5_matched":e1["publisher_original_MD5_whole_file_matched"],
        "original_file_bytes":e1["genuine_original_whole_file_bytes"],
        "total_original_logical_data_rows":PREAMBLE_N+DATA_N,
        "separately_excluded_first_four_source_annotation_rows":PREAMBLE_N,
        "candidate_numeric_source_rows":DATA_N,
        "six_300_sequential_first_slot_ordinal_blocks_exact":exact_rounds,
        "slot0_slot1_slot2_positive_integer_count":numeric_valid,
        "slot0_slot1_slot2_distinct_undecoded_numeric_code_counts":[len(s) for s in all_codes],
        "six_anonymous_original_block_aggregates":source_blocks,
        "source_six_slot1_slot2_code_pairs_all_distinct":len(group_pairs)==6 and len(set(group_pairs))==6,
        "source_exact_two_by_three_condition_series_structure":condition_matrix,
        "slot3_4_numeric_value_range_class_aggregate":{
            "slot3":{n:value_hists[0][n] for n in VALUE_CLASSES},
            "slot4":{n:value_hists[1][n] for n in VALUE_CLASSES},
        },
        "individual_human_identity_from_source_established":False,
        "real_focal_partner_identity_from_source_established":False,
        "real_independent_original_lab_session_from_source_established":False,
        "actor_round_E2_eligible_with_current_source_codebook":False,
        "original_CSV_person_gender_partner_action_values_exported":False,
        "original_data_cells_accessed_for_bounded_structural_audit":True,
        "original_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        metadata=a.get_url(a.METADATA,"metadata",262144)
        if len(metadata)>262144:raise a.SourceError("R108_B2_SOURCE_METADATA_TOO_LARGE")
        a.validate_article_original_file_catalog(json.loads(metadata.decode("utf-8")))
        out=real_source_block_schema_only(s.real_publisher_download())
    except (ValueError,TypeError,KeyError,OSError,UnicodeError,csv.Error) as e:
        out={"research_id":"R108","phase":"B2",
             "status":"R108_B2_TRUE_ORIGINAL_SOURCE_COHORT_BLOCK_SCHEMA_FAIL_CLOSED",
             "safe_failure":str(e) if isinstance(e,a.SourceError) else "R108_B2_ORIGINAL_SOURCE_NOT_VERIFIED",
             "original_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print(json.dumps(out,sort_keys=True))
    if out["status"] not in (
        "R108_B2_ORIGINAL_SIX_300_CONDITION_SOURCE_TRACES_E1_NOT_ACTOR_E2",
        "R108_B2_ORIGINAL_SOURCE_BLOCK_SCHEMA_INCONCLUSIVE_E1_NOT_ACTOR_E2",
    ):
        raise SystemExit(1)
if __name__=="__main__":main()
