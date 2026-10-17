#!/usr/bin/env python3
"""R103 B4 FINAL original experiment/user/opponent/round syntax categories only."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import io
import json
import pathlib
import re
import urllib.request

from r103_phase_a_2016_drbrain_original_md5_header_only import (
    URL,CAP,ExactOfficialRedirect,SourceError,validate_url,audit_firstparty_bytes_header_only
)
PINNED_SHA="c63b99ba7554908e54393eb9f8267a98de1a3d9bdd123a77f60f2b2122236013"
PINNED_N=8477
ID_FIELDS=("Experiment_number","User_ID","Round_number","Opponent_ID")
CATEGORY_NAMES=(
    "ascii_positive_unsigned_int","ascii_zero","ascii_signed_negative_int",
    "ascii_finite_decimal_syntax","blank_or_NA_literal",
    "other_printable_ascii_string","nonascii_or_control"
)

def classify_id_syntax(x):
    if not isinstance(x,str):return "nonascii_or_control"
    v=x.strip()
    if not v or v.upper() in ("NA","NAN","NULL"):return "blank_or_NA_literal"
    if v.isascii() and re.fullmatch(r"[0-9]+",v):
        return "ascii_zero" if int(v)==0 else "ascii_positive_unsigned_int"
    if re.fullmatch(r"-[0-9]+",v,flags=re.ASCII):
        return "ascii_signed_negative_int"
    if re.fullmatch(r"-?[0-9]+\.[0-9]+",v,flags=re.ASCII):
        return "ascii_finite_decimal_syntax"
    if v.isascii() and v.isprintable():return "other_printable_ascii_string"
    return "nonascii_or_control"

def original_id_syntax_only(raw):
    source=audit_firstparty_bytes_header_only(raw)
    if source["original_project_computed_SHA256"]!=PINNED_SHA or source["source_physical_data_lines_without_parsing"]!=PINNED_N:
        raise SourceError("R103_B4_SOURCE_MD5_SHA_OR_LINES_NOT_PINNED")
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""))
    summaries={c:Counter() for c in ID_FIELDS}
    rows=0
    for r in reader:
        rows+=1
        if rows>PINNED_N or None in r:
            raise SourceError("R103_B4_CSV_ROW_STRUCTURE_UNTRUSTED")
        for name in ID_FIELDS:
            summaries[name][classify_id_syntax(r.get(name))]+=1
    if rows!=PINNED_N:
        raise SourceError("R103_B4_ORIGINAL_ROWS_DIFFER")
    output={name:{category:summaries[name][category] for category in CATEGORY_NAMES}
            for name in ID_FIELDS}
    if any(sum(counts.values())!=PINNED_N for counts in output.values()):
        raise SourceError("R103_B4_COLUMN_SYNTAX_COUNTS_NOT_CLOSED")
    return {
        "research_id":"R103","phase":"B4",
        "status":"R103_B4_ORIGINAL_IDENTIFIERS_SYNTAX_ANONYMOUS_COUNTS_ONLY",
        "original_full_SHA256":PINNED_SHA,
        "original_source_rows":rows,
        "source_four_ID_field_syntax_counts":output,
        "raw_source_person_experiment_partner_round_values_exported":False,
        "any_original_Action_or_Opponent_Action_values_accessed":False,
        "actual_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R103-B4-Source-Only-ID-Syntax-No-Choice/1.0"})
        with urllib.request.build_opener(ExactOfficialRedirect()).open(req,timeout=55) as response:
            validate_url(response.geturl())
            raw=response.read(CAP+1)
        result=original_id_syntax_only(raw)
    except (OSError,ValueError,TypeError,KeyError,UnicodeError,csv.Error) as exc:
        result={"research_id":"R103","phase":"B4",
                "status":"R103_B4_FINAL_ID_SYNTAX_SOURCE_BLOCKED",
                "safe_failure":str(exc) if isinstance(exc,SourceError) else "R103_B4_ORIGINAL_ID_SYNTAX_NOT_VERIFIED",
                "actual_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R103_B4_ORIGINAL_IDENTIFIERS_SYNTAX_ANONYMOUS_COUNTS_ONLY":
        raise SystemExit(1)

if __name__=="__main__":
    main()
