#!/usr/bin/env python3
"""R072 REV005 human S8: anonymous structural profile group-size count parity.

Postexploratory hypothesis based on observed REV004 column *types*, frozen
before examining 8-group counts. Never exports raw human codes or behavior.
"""
from __future__ import annotations
from collections import Counter
from decimal import Decimal
import argparse,io,json
from pathlib import Path
from zipfile import ZipFile
from r072_plos_s8_signed_redirect_rev002 import retrieve,audit as audit_original
from r072_plos_s8_anonymous_schema_rev003 import (
    PREFIX, EXACT_SHA, SHEET_RE, safe_xml,shared_strings)
from r072_plos_s8_column_domains_rev004 import decode_cell,cell_column
from hashlib import sha256

EXPECTED_S8_SHA=EXACT_SHA
PUB_N=189
PUB_GROUP_SORTED=[19,19,19,19,25,28,30,30]


def make_receipt(blob):
    if sha256(blob).hexdigest()!=EXPECTED_S8_SHA:
        raise ValueError("UNEXPECTED_OFFICIAL_SOURCE_SHA")
    audit_original(blob,"PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT")
    with ZipFile(io.BytesIO(blob)) as z:
        names=[s for s in z.namelist() if SHEET_RE.fullmatch(s)]
        if len(names)!=1:raise ValueError("EXPECTED_EXACT_S8_SHEET")
        shared=shared_strings(z)
        root=safe_xml(z.read(names[0]))
        container=root.find(f"{PREFIX}sheetData")
        if container is None:raise ValueError("NO_SHEETDATA")
        physical=container.findall(f"{PREFIX}row")
        parsed={}
        for row in physical:
            try:rid=int(row.attrib["r"])
            except (KeyError,ValueError):
                raise ValueError("BAD_XML_ROW") from None
            if rid<1 or rid in parsed:raise ValueError("BAD_DUPLICATE_ROW")
            cells={}
            for cell in row.findall(f"{PREFIX}c"):
                col=cell_column(cell.attrib.get("r",""))
                if col in cells:raise ValueError("DUPLICATE_CELL_COL")
                cells[col]=decode_cell(cell,shared)
            parsed[rid]=cells
    if 1 not in parsed:raise ValueError("NO_HEADER_ROW")
    rows=[(rid,parsed[rid]) for rid in sorted(parsed) if rid!=1]
    candidates=[]
    other=[]
    numeric_runs=[]
    current_run=0
    for rid,cells in rows:
        first=cells.get(1,(None,"empty"))
        second=cells.get(2,(None,"empty"))
        if first[1]=="numeric" and second[1]=="numeric":
            candidates.append(cells)
            current_run+=1
        else:
            other.append(cells)
            if current_run:
                numeric_runs.append(current_run)
                current_run=0
    if current_run:numeric_runs.append(current_run)
    if len(rows)!=len(candidates)+len(other):
        raise ValueError("CANDIDATE_AND_NONCANDIDATE_NOT_PARTITION")
    if not candidates:raise ValueError("NO_CANDIDATE_SOURCE_ROWS")
    first=Counter(row[1][0] for row in candidates)
    groups=sorted(first.values())
    published_parity= len(candidates)==PUB_N and groups==PUB_GROUP_SORTED
    if min(groups)<10:raise ValueError("SOURCE_CONTAINS_SMALL_CODE_GROUPS")
    binary=Counter(row[2][0] for row in candidates)
    is_binary=(set(binary.keys())=={Decimal(0),Decimal(1)} and
               min(binary.values())>=10)
    # Candidate condition is independent of row answer or any human response.
    return {
        "study":"R072",
        "stage":"E2_S8_POSTEXPLORATORY_ANONYMOUS_PROFILE_SIZE_PARITY_REV005",
        "status":"R072_E2_CANDIDATE_PROFILE_SIZE_PARITY_CHECKED",
        "protocol":"protocols/R072_E2_S8_REV005_ANONYMOUS_BLOCK_COHORT_PARITY_2026-10-16.md",
        "original_SHA256":EXPECTED_S8_SHA,
        "total_nonheader_physical_rows":len(rows),
        "candidate_rows_by_numeric_col1_and_col2":len(candidates),
        "noncandidate_annotation_format_rows":len(other),
        "candidate_row_definition":"numeric first and numeric second worksheet cell, postexploratory",
        "anonymous_col1_unique_numeric_codes":len(first),
        "anonymous_col1_group_sizes_sorted_suppressed_if_any_less10":groups,
        "published_table3_anonymous_size_multiset_expected":PUB_GROUP_SORTED,
        "eight_anonymous_group_multiset_matches_table3":groups==PUB_GROUP_SORTED,
        "candidate_request_count_matches_published_189":len(candidates)==PUB_N,
        "source_structural_189_x_8group_parity":published_parity,
        "candidate_data_runs_orderless_sorted_if_min_ge10":sorted(numeric_runs)
            if numeric_runs and min(numeric_runs)>=10 else None,
        "binary_second_column_all_zero_one_and_both_groups_ge10":is_binary,
        "binary_second_column_code_counts_not_a_treatment_mapping":
            {"zero":binary[Decimal(0)],"one":binary[Decimal(1)]} if is_binary else None,
        "author_serving_vs_neutral_profile_label_mapping":"NOT_RECOVERED",
        "author_yes_maybe_no_reply_semantics":"NOT_RECOVERED",
        "treatment_randomization_replication":"NOT_PERFORMED",
        "published_response_analysis_replication":"NOT_PERFORMED",
        "participant_codes_names_values_released":False,
        "individual_human_response_rows_released":False,
        "human_image_standing_stern_reputation_model":"NOT_TESTED",
        "prior_REV004_nonheader_row_count_198_preserved":True,
        "external_E3":"OPEN",
        "PESEN_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    try:
        data,mode=retrieve()
        if mode not in ("PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT","PLOS_DIRECT_PUBLISHER"):
            raise ValueError("SOURCE_CHANGING_NOT_ALLOWED")
        result=make_receipt(data)
    except (ValueError,OSError) as ex:
        result={"study":"R072","status":"SOURCE_PROFILE_GROUP_PARITY_UNRESOLVED",
                "bounded_error":str(ex)[:100] if isinstance(ex,ValueError) else "NETWORK_IO",
                "human_rows_exported":False,"PESEN_v01":"FROZEN"}
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R072_E2_CANDIDATE_PROFILE_SIZE_PARITY_CHECKED":
        raise RuntimeError("R072 exact original candidate profile count audit failed")


if __name__=="__main__":main()
