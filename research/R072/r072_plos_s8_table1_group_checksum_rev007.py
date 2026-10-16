#!/usr/bin/env python3
"""R072 REV007: post-exploratory original field S8 group-count checksum ONLY.

Source published Table 1 defines eight (requests, any-response) pairs.
This DOES NOT identify a treatment mapping, infer motives, or reproduce an
effect. It never writes original numeric profile codes or participant rows.
"""
from __future__ import annotations
import argparse
from collections import Counter
from decimal import Decimal
import hashlib,io,json
from pathlib import Path
from zipfile import ZipFile

from r072_plos_s8_signed_redirect_rev002 import retrieve,audit as verify_original
from r072_plos_s8_anonymous_schema_rev003 import EXACT_SHA,PREFIX,SHEET_RE,safe_xml,shared_strings
from r072_plos_s8_column_domains_rev004 import decode_cell,cell_column

PUBLISHED_UNLABELLED_PAIRS=tuple(sorted([
    (30,16),(30,6),(28,14),(25,11),
    (19,11),(19,12),(19,10),(19,9),
]))
PUBLISHED_REQUESTS=189
PUBLISHED_ANY_RESPONSES=89
SOURCE_SHA=EXACT_SHA


def count_anonymous_pairs(raw:bytes):
    if hashlib.sha256(raw).hexdigest()!=SOURCE_SHA:
        raise ValueError("PREVIOUSLY_PINNED_PUBLISHER_S8_SHA_MISMATCH")
    verify_original(raw,"PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT")
    with ZipFile(io.BytesIO(raw)) as z:
        sheets=[n for n in z.namelist() if SHEET_RE.fullmatch(n)]
        if len(sheets)!=1:
            raise ValueError("EXPECTED_ONE_S8_WORKSHEET")
        shared=shared_strings(z)
        root=safe_xml(z.read(sheets[0]))
        sheet=root.find(f"{PREFIX}sheetData")
        if sheet is None:
            raise ValueError("SOURCE_HAS_NO_SHEETDATA")
        counters={}
        noncase_count=0
        ids=set()
        for row in sheet.findall(f"{PREFIX}row"):
            try:rowindex=int(row.attrib["r"])
            except (ValueError,KeyError):
                raise ValueError("ROW_INDEX_NOT_IN_OOXML_FORMAT") from None
            if rowindex<1 or rowindex in ids:
                raise ValueError("DUPLICATE_OR_INVALID_ROW_TAG")
            ids.add(rowindex)
            if rowindex==1:
                continue
            values={}
            for cell in row.findall(f"{PREFIX}c"):
                index=cell_column(cell.attrib.get("r",""))
                if index in values:
                    raise ValueError("DUPLICATE_CELL_COLUMN")
                values[index]=decode_cell(cell,shared)
            first=values.get(1,(None,"empty"))
            second=values.get(2,(None,"empty"))
            if first[1]=="numeric" and second[1]=="numeric":
                if second[0] not in (Decimal(0),Decimal(1)):
                    raise ValueError("SECOND_COL_MUST_BE_PREDEFINED_BINARY")
                state=counters.setdefault(first[0],Counter())
                state["requests"]+=1
                state["coded_one"]+=int(second[0]==Decimal(1))
            else:
                noncase_count+=1
    if len(counters)!=8:
        raise ValueError("ANONYMOUS_PROFILE_GROUP_COUNT_NOT_EIGHT")
    pairs=tuple(sorted((x["requests"],x["coded_one"]) for x in counters.values()))
    # Suppression contracts: no tiny or unique person-level quantities.
    if any(n<10 or response<5 or n-response<5 for n,response in pairs):
        raise ValueError("PROFILE_GROUP_COUNTS_BELOW_PUBLIC_AGGREGATE_DISCLOSURE_THRESHOLD")
    candidate_requests=sum(p[0] for p in pairs)
    candidate_ones=sum(p[1] for p in pairs)
    weak_match=(candidate_requests==PUBLISHED_REQUESTS
                and candidate_ones==PUBLISHED_ANY_RESPONSES)
    strict_match=pairs==PUBLISHED_UNLABELLED_PAIRS
    flipped_total=candidate_requests-candidate_ones
    return {
        "research_id":"R072",
        "stage":"E2_POSTEXPLORATORY_PUBLISHED_TABLE1_UNLABELLED_PAIR_CHECKSUM_REV007",
        "status":"REAL_HUMAN_PUBLISHED_GROUP_AGGREGATE_PARITY_CHECKED",
        "source_DOI":"10.1371/journal.pone.0152076.s008",
        "publisher_report_reference":"10.1371/journal.pone.0152076.t001",
        "locked_source_sha256":SOURCE_SHA,
        "protocol":"protocols/R072_E2_S8_REV007_PUBLISHED_GROUP_RESPONSE_CHECKSUM_2026-10-16.md",
        "predeclared_published_aggregate_pairs_without_labels":[list(p) for p in PUBLISHED_UNLABELLED_PAIRS],
        "actual_anonymous_source_pairs_without_codes":[list(p) for p in pairs],
        "candidate_requests":candidate_requests,
        "candidate_coded_one":candidate_ones,
        "noncandidate_format_rows":noncase_count,
        "weak_totals_match_published_189_89":weak_match,
        "strong_eight_paired_multiset_matches_published_table1":strict_match,
        "flipped_second_column_total_would_match_published_89":
            flipped_total==PUBLISHED_ANY_RESPONSES,
        "column_2_semantics":"CANDIDATE_ANY_RESPONSE_1_ONLY_FROM_POSTEXPLORATORY_PAPER_COUNT_PARITY",
        "author_numerical_profile_to_serving_neutral_mapping":"NOT_RECOVERED",
        "real_serving_neutral_effect_96_93":"NOT_CALCULATED",
        "real_yes_maybe_no_effect":"NOT_CALCULATED",
        "individual_records_group_IDs_or_codes_exported":False,
        "R072_IMAGE_STANDING_STERN_E2":"NOT_TESTED",
        "independent_E3":"OPEN",
        "pesen_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    try:
        raw,mode=retrieve()
        if mode not in ("PLOS_DIRECT_PUBLISHER","PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT"):
            raise ValueError("UNEXPECTED_OFFICIAL_SOURCE_CHAIN")
        result=count_anonymous_pairs(raw)
    except (ValueError,OSError) as exc:
        result={"research_id":"R072","stage":"E2_POSTEXPLORATORY_TABLE1_GROUP_PARITY_REV007",
                "status":"REAL_ORIGINAL_SOURCE_CHECKSUM_UNRESOLVED",
                "error_code":str(exc)[:90] if isinstance(exc,ValueError) else "SOURCE_NETWORK_OR_IO",
                "original_human_data_disclosed":False,
                "pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="REAL_HUMAN_PUBLISHED_GROUP_AGGREGATE_PARITY_CHECKED":
        raise RuntimeError("R072 S8 source checksum gate unresolved")


if __name__=="__main__":
    main()
