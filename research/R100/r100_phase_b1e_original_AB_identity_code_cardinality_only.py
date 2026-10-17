#!/usr/bin/env python3
"""R100 B1e: final bounded A/B cardinality audit, no contribution or survey values.

All source A/B strings stay in process. Only anonymous counts are committed.
"""
from __future__ import annotations
import argparse
from collections import Counter
import json
import pathlib
import urllib.request

from r100_2025_original_threshold_pgg_zenodo_xlsx_source_directory_only import (
    URL, MAX_SOURCE, ExactOfficialOriginRedirect, SourceError, validate_url
)
from r100_phase_b1b_original_AB_role_partner_reciprocal_graph import (
    extracted_ab_source_blocks, OFFICIAL_MD5, PINNED_SHA256
)


def anonymous_ab_cardinality(blocks):
    treatments = list(dict.fromkeys(t for t, _, _, _ in blocks))
    if len(treatments) != 5:
        raise SourceError("R100_B1E_EXPECT_FIVE_ORIGINAL_TREATMENTS")
    result = []
    for slot, treatment in enumerate(treatments, 1):
        subsets={}
        for role in (1,2):
            source=[(a,b) for t,typ,a,b in blocks if t==treatment and typ==role]
            if not source:
                raise SourceError("R100_B1E_MISSING_ROLE_SHEET")
            all_a, all_b=[],[]
            pos=[set(),set(),set(),set()]
            three=two=repeat=0
            for a,b in source:
                if len(a)!=4 or len(b)!=4 or a[0] is None or any(x is not None for x in a[1:]) or any(x is None for x in b):
                    raise SourceError("R100_B1E_AB_BLOCK_SHAPE_CHANGED")
                all_a.append(a[0])
                all_b.extend(b)
                for i,x in enumerate(b):pos[i].add(x)
                three += len(set(b))==3
                two += len(set(b))==2
                if role==1:
                    repeat += b[0]==b[3]
                else:
                    repeat += b[1]==b[2]
            subsets[role]={"a":set(all_a),"b":set(all_b)}
            subsets[role]["counts"]={
                "anonymous_role_slot":role,"four_row_focal_blocks":len(source),
                "distinct_A_source_number_strings":len(set(all_a)),
                "distinct_all_B_strings_in_sheet":len(set(all_b)),
                "distinct_B_by_four_positions":[len(v) for v in pos],
                "B_three_distinct_in_block_count":three,
                "B_two_distinct_in_block_count":two,
                "author_role_expected_repeated_B_positions_count":repeat,
            }
        a1,a2=subsets[1]["a"],subsets[2]["a"]
        b1,b2=subsets[1]["b"],subsets[2]["b"]
        per={
            "anonymous_treatment_slot":slot,
            "role_sheets":[subsets[1]["counts"],subsets[2]["counts"]],
            "A_number_strings_shared_across_both_role_sheets":len(a1&a2),
            "distinct_B_strings_shared_across_role_sheets":len(b1&b2),
            "distinct_B_strings_entire_treatment":len(b1|b2),
            "B_unique_person_code_sufficient_from_repeated_focal_position":
                all(subsets[role]["counts"]["distinct_B_by_four_positions"][0 if role==1 else 1]
                    ==subsets[role]["counts"]["four_row_focal_blocks"] for role in (1,2))
        }
        result.append(per)
    return {
        "research_id":"R100","phase":"B1e",
        "status":"B1E_REAL_AB_IDENTIFIABILITY_CARDINALITY_AUDITED_ONLY",
        "source_pair_identity_uniquely_verified":False,
        "anonymous_treatment_summaries":result,
        "candidate_focus_record_total":sum(v["four_row_focal_blocks"] for t in result for v in t["role_sheets"]),
        "original_A_B_literal_values_or_pairs_exported":False,
        "C_to_Z_cell_values_dereferenced":0,
        "original_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }


def source_check(raw):
    blocks, ident=extracted_ab_source_blocks(raw)
    r=anonymous_ab_cardinality(blocks)
    r["official_original_MD5"]=OFFICIAL_MD5
    r["official_original_SHA256"]=PINNED_SHA256
    r["official_original_bytes"]=ident["original_bytes"]
    return r


def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",type=pathlib.Path,required=True)
    args=a.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R100-B1e-AB-cardinality-only/1.0"})
        with urllib.request.build_opener(ExactOfficialOriginRedirect()).open(req,timeout=55) as response:
            validate_url(response.geturl())
            raw=response.read(MAX_SOURCE+1)
        result=source_check(raw)
    except (ValueError,OSError,TypeError,KeyError) as exc:
        result={"research_id":"R100","phase":"B1e","status":"B1E_SOURCE_FAIL_CLOSED",
                "safe_failure":str(exc) if isinstance(exc,SourceError) else "R100_B1E_ORIGINAL_UNVERIFIED",
                "original_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="B1E_REAL_AB_IDENTIFIABILITY_CARDINALITY_AUDITED_ONLY":
        raise SystemExit(1)

if __name__=="__main__":
    main()
