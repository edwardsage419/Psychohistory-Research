#!/usr/bin/env python3
"""R104 A: genuine publisher PLOS S1 CSV downloaded twice, whole SHA, HEADER only."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import pathlib
import re
import urllib.parse
import urllib.request

OFFICIAL_DOI="10.1371/journal.pone.0299196.s002"
URL="https://journals.plos.org/plosone/article/file?id="+OFFICIAL_DOI+"&type=supplementary"
CAP=1024*1024
IDENTIFIER=re.compile(r"[A-Za-z_][A-Za-z0-9_. -]{0,99}")

class SourceError(ValueError):
    pass

def validate_url(url):
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or p.netloc!="journals.plos.org" or p.path!="/plosone/article/file" or p.fragment:
        raise SourceError("R104_PLOS_ORIGINAL_URL_NOT_PINNED")
    query=urllib.parse.parse_qs(p.query,strict_parsing=True)
    if query!={"id":[OFFICIAL_DOI],"type":["supplementary"]}:
        raise SourceError("R104_PLOS_ORIGINAL_FILE_QUERY_NOT_PINNED")

class ExactSourceRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        validate_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def source_header_only(b):
    if type(b) is not bytes or not (100<=len(b)<=CAP):
        raise SourceError("R104_PLOS_ORIGINAL_SIZE_OUT_OF_BOUNDS")
    if b"\x00" in b or b.lstrip()[:100].lower().startswith((b"<html",b"<!doctype",b"<?xml")):
        raise SourceError("R104_PLOS_SOURCE_NOT_CSV_OR_IS_HTML")
    first,sep,_=b.partition(b"\n")
    if not sep or len(first)>8192:
        raise SourceError("R104_PLOS_ORIGINAL_HEADER_NOT_PRESENT")
    try:
        text=first.rstrip(b"\r").decode("utf-8-sig")
        names=next(csv.reader([text],strict=True))
    except (UnicodeError,csv.Error,StopIteration) as exc:
        raise SourceError("R104_PLOS_CSV_HEADER_SYNTAX_INVALID") from exc
    if not 3<=len(names)<=100 or len(names)!=len(set(names)) or any(IDENTIFIER.fullmatch(n) is None for n in names):
        raise SourceError("R104_PLOS_ORIGINAL_HEADER_FIELDS_NOT_SAFE_UNIQUE_ASCII")
    line_count=b.count(b"\n")-1 if b.endswith(b"\n") else b.count(b"\n")
    if line_count<=0 or line_count>100000:
        raise SourceError("R104_PLOS_ORIGINAL_PHYSICAL_DATA_LINE_COUNT_INVALID")
    return {
        "research_id":"R104","phase":"A",
        "status":"R104_ORIGINAL_PLOS_PUBLISHER_CSV_DOUBLE_SHA_HEADER_ONLY_E1",
        "original_publisher_supplementary_DOI":OFFICIAL_DOI,
        "publisher_md5_published_and_verified":False,
        "original_source_bytes":len(b),
        "project_computed_wholefile_SHA256":hashlib.sha256(b).hexdigest(),
        "original_csv_header_field_count":len(names),
        "sanitized_public_original_header_names":names,
        "original_physical_data_lines_unparsed":line_count,
        "any_original_human_behavior_or_identity_cells_accessed":False,
        "actual_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def complete_double_source(a,b):
    first=source_header_only(a)
    second=source_header_only(b)
    if a!=b or first["project_computed_wholefile_SHA256"]!=second["project_computed_wholefile_SHA256"]:
        raise SourceError("R104_PLOS_TWO_INDEPENDENT_SOURCE_GETS_DO_NOT_MATCH")
    first["two_independent_publisher_downloads_byte_for_byte_equal"]=True
    return first

def download():
    validate_url(URL)
    req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R104-2024-PLOS-One-Firstparty-Source-Header-Only/1.0","Accept":"text/csv,application/octet-stream;q=0.8"})
    with urllib.request.build_opener(ExactSourceRedirect()).open(req,timeout=55) as response:
        validate_url(response.geturl())
        if response.status!=200:
            raise SourceError("R104_PLOS_FINAL_ORIGINAL_HTTP_NOT_200")
        return response.read(CAP+1)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        result=complete_double_source(download(),download())
    except (ValueError,OSError,TypeError,KeyError,UnicodeError) as exc:
        result={"research_id":"R104","phase":"A",
                "status":"R104_PLOS_FIRSTPARTY_ORIGINAL_SOURCE_FAIL_CLOSED",
                "safe_failure":str(exc) if isinstance(exc,SourceError) else "R104_PLOS_PUBLISHER_SOURCE_UNVERIFIED",
                "actual_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R104_ORIGINAL_PLOS_PUBLISHER_CSV_DOUBLE_SHA_HEADER_ONLY_E1":
        raise SystemExit(1)

if __name__=="__main__":
    main()
