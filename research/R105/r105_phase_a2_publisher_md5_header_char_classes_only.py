#!/usr/bin/env python3
"""R105 A2 firstparty original Zenodo full publisher MD5, header classes ONLY."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import hashlib
import json
import pathlib
import urllib.request

from r105_phase_a_original_2024_cpr_defaults_zenodo_md5_header_only import (
    SOURCE_URL,CAP,PUBLISHED_MD5,OnlyExactPublisherRedirect,
    SourceGateError,validate_url
)

def category(c):
    if "a"<=c<="z":return "ascii_lower"
    if "A"<=c<="Z":return "ascii_upper"
    if "0"<=c<="9":return "ascii_digit"
    if c in (" ","\t"):return "ascii_whitespace"
    if 33<=ord(c)<=126:return "ascii_punctuation"
    return "nonascii_or_control"

def only_header_classes(b):
    if type(b) is not bytes or not 100<=len(b)<=CAP:
        raise SourceGateError("R105_A2_SOURCE_SIZE_INVALID")
    if hashlib.md5(b).hexdigest()!=PUBLISHED_MD5:
        raise SourceGateError("R105_A2_ORIGINAL_PUBLISHER_MD5_MISMATCH")
    head,sep,_=b.partition(b"\n")
    if not sep or len(head)>16384:
        raise SourceGateError("R105_A2_HEADER_ABSENT")
    try:
        names=next(csv.reader([head.rstrip(b"\r").decode("utf-8-sig")],strict=True))
    except (UnicodeError,csv.Error,StopIteration) as ex:
        raise SourceGateError("R105_A2_ORIGINAL_HEADER_CSV_INVALID") from ex
    if not 3<=len(names)<=150 or any(not isinstance(x,str) or len(x)>160 for x in names):
        raise SourceGateError("R105_A2_ORIGINAL_HEADER_NUMBERS_INVALID")
    classes=Counter()
    punct=set()
    lengths=Counter()
    ascii_initial=0
    for name in names:
        lengths[len(name)]+=1
        if name and (name[0].isascii() and (name[0].isalpha() or name[0]=="_")):
            ascii_initial+=1
        for c in name:
            kind=category(c)
            classes[kind]+=1
            if kind=="ascii_punctuation":punct.add(ord(c))
    return {
        "research_id":"R105","phase":"A2",
        "status":"R105_TRUE_ORIGINAL_PUBLISHER_MD5_HEADER_ANON_CHAR_DIAGNOSTIC_ONLY",
        "publisher_source_DOI":"10.5281/zenodo.10818840",
        "firstparty_whole_MD5_match":True,
        "full_original_file_bytes":len(b),
        "full_original_project_SHA256":hashlib.sha256(b).hexdigest(),
        "actual_header_field_count":len(names),
        "duplicate_source_column_names_count":len(names)-len(set(names)),
        "header_names_starting_safe_ASCII_count":ascii_initial,
        "anonymous_header_name_length_histogram":dict(sorted(lengths.items())),
        "anonymous_header_character_class_counts":dict(sorted(classes.items())),
        "ASCII_header_punctuation_ordinal_list_only":sorted(punct),
        "exact_header_names_or_person_values_exported":False,
        "any_original_human_behavior_or_identity_data_row_read":False,
        "real_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",required=True,type=pathlib.Path)
    x=a.parse_args()
    try:
        validate_url(SOURCE_URL)
        req=urllib.request.Request(SOURCE_URL,headers={"User-Agent":"Psychohistory-R105-A2-OnlyOriginalHeaderClasses/1.0"})
        with urllib.request.build_opener(OnlyExactPublisherRedirect()).open(req,timeout=55) as resp:
            validate_url(resp.geturl())
            raw=resp.read(CAP+1)
        result=only_header_classes(raw)
    except (ValueError,TypeError,OSError,KeyError) as exc:
        result={"research_id":"R105","phase":"A2","status":"R105_A2_HEADER_SOURCE_FAIL_CLOSED",
                "safe_failure":str(exc) if isinstance(exc,SourceGateError) else "R105_A2_ORIGINAL_HEADER_NOT_AUTHENTICATED",
                "real_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R105_TRUE_ORIGINAL_PUBLISHER_MD5_HEADER_ANON_CHAR_DIAGNOSTIC_ONLY":raise SystemExit(1)
if __name__=="__main__":main()
