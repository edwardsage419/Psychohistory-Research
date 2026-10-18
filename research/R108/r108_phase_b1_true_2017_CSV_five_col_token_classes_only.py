#!/usr/bin/env python3
"""R108 B1 limited authenticated original human CSV TOKEN CLASSES only.

Original cell strings are transiently classified; they are never printed,
stored in receipts, emitted as example values or used in a predictive model.
"""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import io
import json
import pathlib
import re

import r108_phase_a1_original_2017_Leicester_fixed_pair_CSV_MD5_double_SHA_header_only as a
import r108_phase_a3_verified_Figshare_publisher_S3_delegate_MD5_double_source as s
import r108_phase_a4_verified_full_original_MD5_header_class_only as b

PINNED_ORIGINAL_SHA="e7dbb6ddc96cc5c65368be0d1918c3ebc7a83c14addd03ab44eeb07790575c18"
PINNED_DATA_ROWS=1804
TOKENS=("EMPTY","BIT_0","BIT_1","UNSIGNED_INTEGER","SIGNED_INTEGER",
        "DECIMAL","LETTER_ONLY","ALPHANUMERIC","OTHER_PRINTABLE","NONASCII_CONTROL_OR_LONG")

def classify_token(token):
    if not isinstance(token,str):return "NONASCII_CONTROL_OR_LONG"
    val=token.strip()
    if not val:return "EMPTY"
    if len(val)>200 or not val.isascii() or not val.isprintable():
        return "NONASCII_CONTROL_OR_LONG"
    if val=="0":return "BIT_0"
    if val=="1":return "BIT_1"
    if re.fullmatch(r"[0-9]+",val,flags=re.ASCII):
        return "UNSIGNED_INTEGER"
    if re.fullmatch(r"-[0-9]+",val,flags=re.ASCII):
        return "SIGNED_INTEGER"
    if re.fullmatch(r"-?[0-9]+\.[0-9]+",val,flags=re.ASCII):
        return "DECIMAL"
    if re.fullmatch(r"[A-Za-z]{1,80}",val,flags=re.ASCII):
        return "LETTER_ONLY"
    if len(val)<=80 and re.fullmatch(r"[A-Za-z0-9_ /-]+",val,flags=re.ASCII):
        return "ALPHANUMERIC"
    return "OTHER_PRINTABLE"

def original_anonymous_token_classes(raw):
    check=b.class_only(raw)
    if check["project_original_complete_SHA256"]!=PINNED_ORIGINAL_SHA:
        raise a.SourceError("R108_B1_TRUE_ORIGINAL_SOURCE_FULL_SHA_NOT_PINNED")
    rd=csv.reader(io.StringIO(raw.decode("utf-8-sig"),newline=""),strict=True)
    columns=[Counter() for _ in range(5)]
    first=[]
    last=[]
    prev=None
    transitions=0
    total=0
    all_empty=0
    try:
        for idx,row in enumerate(rd):
            if len(row)!=5:
                raise a.SourceError("R108_B1_TRUE_ORIGINAL_ROW_NOT_FIVE_FIELDS")
            if idx==0:continue
            # At B1 the source cell tokens are actually examined ONLY here.
            # No original cell token or value is put into the result.
            types=tuple(classify_token(x) for x in row)
            total+=1
            if all(t=="EMPTY" for t in types):all_empty+=1
            for i,t in enumerate(types):columns[i][t]+=1
            if len(first)<8:first.append(list(types))
            last.append(list(types))
            if len(last)>8:last.pop(0)
            if prev is not None and prev!=types:transitions+=1
            prev=types
    except (UnicodeError,csv.Error) as exc:
        raise a.SourceError("R108_B1_ORIGINAL_SOURCE_TOKEN_CLASS_CSV_UNVERIFIED") from exc
    if total!=PINNED_DATA_ROWS or total!=check["source_physical_data_lines_unparsed"]:
        raise a.SourceError("R108_B1_ORIGINAL_SOURCE_1804_ROW_UNIVERSE_UNVERIFIED")
    hist={str(i):{t:columns[i][t] for t in TOKENS} for i in range(5)}
    if any(sum(z.values())!=PINNED_DATA_ROWS for z in hist.values()):
        raise a.SourceError("R108_B1_ORIGINAL_ANONYMOUS_TYPE_COUNT_NOT_CLOSED")
    return {
        "research_id":"R108","phase":"B1",
        "status":"R108_B1_AUTHENTIC_2017_ORIGINAL_FIVE_COLUMN_ANONYMOUS_VALUE_TYPE_CENSUS_ONLY",
        "publisher_original_MD5_verified":check["publisher_original_MD5_whole_file_matched"],
        "original_whole_SHA256":PINNED_ORIGINAL_SHA,
        "original_source_bytes":check["genuine_original_whole_file_bytes"],
        "original_body_rows":total,
        "original_anonymous_column_slot_type_histograms":hist,
        "first_eight_rows_TYPE_LABELS_ONLY":first,
        "last_eight_rows_TYPE_LABELS_ONLY":last,
        "source_row_type_pattern_transition_count":transitions,
        "original_all_five_fields_empty_row_count":all_empty,
        "original_data_cell_values_transiently_examined_for_syntax":True,
        "raw_original_human_person_gender_game_partner_action_values_exported":False,
        "original_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        meta=a.get_url(a.METADATA,"metadata",262144)
        if len(meta)>262144:raise a.SourceError("R108_B1_SOURCE_METADATA_SIZE_UNSAFE")
        a.validate_article_original_file_catalog(json.loads(meta.decode("utf-8")))
        result=original_anonymous_token_classes(s.real_publisher_download())
    except (ValueError,TypeError,KeyError,OSError,UnicodeError,csv.Error) as exc:
        result={"research_id":"R108","phase":"B1",
                "status":"R108_B1_TRUE_ORIGINAL_TOKEN_CLASS_SOURCE_FAIL_CLOSED",
                "safe_failure":str(exc) if isinstance(exc,a.SourceError) else "R108_B1_ORIGINAL_SOURCE_UNVERIFIED",
                "original_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R108_B1_AUTHENTIC_2017_ORIGINAL_FIVE_COLUMN_ANONYMOUS_VALUE_TYPE_CENSUS_ONLY":
        raise SystemExit(1)
if __name__=="__main__":main()
