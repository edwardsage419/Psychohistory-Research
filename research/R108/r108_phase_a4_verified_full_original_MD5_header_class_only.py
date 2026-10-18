#!/usr/bin/env python3
"""R108 A4: exact published MD5+two full firstparty sources; header class only.

Do not dereference CSV body/participant data. Header anomalies are metadata,
not authorization to change any original action encoding or sample inclusion.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import pathlib
import re

import r108_phase_a1_original_2017_Leicester_fixed_pair_CSV_MD5_double_SHA_header_only as a
import r108_phase_a3_verified_Figshare_publisher_S3_delegate_MD5_double_source as b

def class_only(raw):
    if type(raw) is not bytes or len(raw)!=a.EXPECTED_SIZE:
        raise a.SourceError("R108_A4_ORIGINAL_FIRSTPARTY_SIZE_NOT_MATCHED")
    if hashlib.md5(raw).hexdigest()!=a.EXPECTED_MD5:
        raise a.SourceError("R108_A4_ORIGINAL_FIRSTPARTY_MD5_NOT_MATCHED")
    if b"\x00" in raw or raw.lstrip()[:120].lower().startswith((b"<html",b"<!doctype",b"<?xml",b"{")):
        raise a.SourceError("R108_A4_OFFICIAL_ORIGINAL_NOT_PLAIN_CSV")
    header,sep,_=raw.partition(b"\n")
    if not sep or len(header)>20000:
        raise a.SourceError("R108_A4_CSV_HEADER_NOT_BOUNDED")
    try:names=next(csv.reader([header.rstrip(b"\r").decode("utf-8-sig")],strict=True))
    except (UnicodeError,csv.Error,StopIteration) as e:
        raise a.SourceError("R108_A4_HEADER_UTF8_CSV_SYNTAX_INVALID") from e
    if not 1<=len(names)<=500:
        raise a.SourceError("R108_A4_CSV_HEADER_FIELD_COUNT_OUT_OF_BOUNDS")
    nonascii=sum(any(ord(c)>126 or ord(c)<32 for c in s) for s in names)
    punct={ord(c) for n in names for c in n if 33<=ord(c)<=126 and not(c.isascii() and (c.isalnum() or c=="_"))}
    n_violations=sum(a.HEADER_RE.fullmatch(n) is None for n in names)
    lines=raw.count(b"\n")-1 if raw.endswith(b"\n") else raw.count(b"\n")
    return {
        "research_id":"R108","phase":"A4",
        "status":"R108_A4_GENUINE_2017_LEICESTER_ORIGINAL_MD5_DOUBLE_SHA_HEADER_CLASS_E1",
        "publisher_figshare_article_ID":10194938,
        "publisher_original_file_ID":18370526,
        "genuine_original_whole_file_bytes":len(raw),
        "publisher_original_MD5_whole_file_matched":a.EXPECTED_MD5,
        "project_original_complete_SHA256":hashlib.sha256(raw).hexdigest(),
        "source_csv_header_column_count":len(names),
        "anonymous_source_header_duplicate_name_count":len(names)-len(set(names)),
        "anonymous_source_header_empty_name_count":sum(n=="" for n in names),
        "anonymous_source_header_nonASCII_or_control_field_count":nonascii,
        "anonymous_source_header_maximum_field_name_length":max(map(len,names)),
        "anonymous_source_header_strict_ASCII_identifier_violation_count":n_violations,
        "anonymous_header_ASCII_punctuation_decimal_codepoints_only":sorted(punct),
        "source_physical_data_lines_unparsed":lines,
        "source_human_person_pair_action_body_cells_accessed":False,
        "original_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def double_source(one,two):
    x=class_only(one);y=class_only(two)
    if one!=two or x["project_original_complete_SHA256"]!=y["project_original_complete_SHA256"]:
        raise a.SourceError("R108_A4_ORIGINAL_DOUBLE_SOURCE_BYTES_NOT_IDENTICAL")
    x["two_independent_exact_official_publisher_sources_byte_identical"]=True
    return x

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        m=a.get_url(a.METADATA,"metadata",262144)
        if len(m)>262144:raise a.SourceError("R108_A4_FIRSTPARTY_METADATA_TOO_LARGE")
        a.validate_article_original_file_catalog(json.loads(m.decode("utf-8")))
        result=double_source(b.real_publisher_download(),b.real_publisher_download())
    except (ValueError,TypeError,KeyError,OSError,UnicodeError,csv.Error) as e:
        result={
            "research_id":"R108","phase":"A4",
            "status":"R108_A4_GENUINE_ORIGINAL_HEADER_CLASS_FAIL_CLOSED",
            "safe_failure":str(e) if isinstance(e,a.SourceError) else "R108_A4_ORIGINAL_PUBLISHER_SOURCE_UNVERIFIED",
            "original_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R108_A4_GENUINE_2017_LEICESTER_ORIGINAL_MD5_DOUBLE_SHA_HEADER_CLASS_E1":
        raise SystemExit(1)
if __name__=="__main__":main()
