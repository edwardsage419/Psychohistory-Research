#!/usr/bin/env python3
"""R107 A: first-party 2020 Dryad 296893 exact CSV, double SHA and header ONLY."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request

URL="https://datadryad.org/downloads/file_stream/296893"
CAP=1048576
SAFE_HEADER=re.compile(r"[A-Za-z_][A-Za-z0-9_. \-]{0,99}")
class SourceError(ValueError):
    pass

def validate_url(url):
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or p.netloc!="datadryad.org" or p.path!="/downloads/file_stream/296893" or p.query or p.fragment:
        raise SourceError("R107_A_OFFICIAL_DRYAD_296893_FILE_URL_UNTRUSTED")

class ExactOriginalRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        validate_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def validate_complete_csv_header_only(raw):
    if type(raw) is not bytes or not 1000<=len(raw)<=CAP:
        raise SourceError("R107_A_ORIGINAL_SOURCE_SIZE_OUT_OF_BOUNDS")
    if b"\x00" in raw or raw.lstrip()[:128].lower().startswith((b"<html",b"<!doctype",b"<?xml",b"{",b"[")):
        raise SourceError("R107_A_ORIGINAL_SOURCE_NOT_PLAIN_CSV")
    first,found,_=raw.partition(b"\n")
    if not found or len(first)>20000:
        raise SourceError("R107_A_ORIGINAL_CSV_HEADER_LINE_NOT_BOUNDED")
    try:
        header=next(csv.reader([first.rstrip(b"\r").decode("utf-8-sig")],strict=True))
    except (UnicodeError,csv.Error,StopIteration) as exc:
        raise SourceError("R107_A_ORIGINAL_CSV_HEADER_PARSE_FAIL") from exc
    if not 2<=len(header)<=150 or len(header)!=len(set(header)) or any(SAFE_HEADER.fullmatch(h) is None for h in header):
        raise SourceError("R107_A_ORIGINAL_CSV_HEADER_UNSAFE_OR_DUPLICATE")
    lines=raw.count(b"\n")-1 if raw.endswith(b"\n") else raw.count(b"\n")
    if lines<1:
        raise SourceError("R107_A_NO_PHYSICAL_ORIGINAL_CSV_DATA_LINES")
    return {
        "research_id":"R107","phase":"A",
        "status":"R107_A_GENUINE_2020_DRYAD_ORIGINAL_DATASET_CSV_DOUBLE_SHA_HEADER_E1",
        "official_dataset_DOI":"10.5061/dryad.7fq25s8",
        "official_original_file_ID":296893,
        "publisher_origin":"https://datadryad.org",
        "original_filename":"DataSet.csv",
        "actual_whole_file_bytes":len(raw),
        "project_calculated_original_whole_SHA256":hashlib.sha256(raw).hexdigest(),
        "publisher_independent_MD5_available_and_verified":False,
        "original_csv_field_count":len(header),
        "original_public_csv_header_names":header,
        "original_physical_data_lines_without_parsing":lines,
        "any_original_human_action_or_person_or_session_value_accessed":False,
        "human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def double_source(raw1,raw2):
    first=validate_complete_csv_header_only(raw1)
    second=validate_complete_csv_header_only(raw2)
    if raw1!=raw2 or first["project_calculated_original_whole_SHA256"]!=second["project_calculated_original_whole_SHA256"]:
        raise SourceError("R107_A_TWO_INDEPENDENT_OFFICIAL_DOWNLOADS_DIFFER")
    first["two_independent_full_original_official_downloads_bytes_equal"]=True
    return first

def original_get():
    validate_url(URL)
    req=urllib.request.Request(URL,headers={
        "User-Agent":"Psychohistory-R107-2020-Dryad-Original-Header-Only/1.0",
        "Accept":"text/csv,application/octet-stream;q=0.8"})
    try:
        with urllib.request.build_opener(ExactOriginalRedirect()).open(req,timeout=55) as response:
            validate_url(response.geturl())
            if response.status!=200:
                raise SourceError("R107_A_OFFICIAL_DRYAD_FINAL_HTTP_NOT_200")
            return response.read(CAP+1)
    except urllib.error.HTTPError as exc:
        if exc.code==403:raise SourceError("R107_A_OFFICIAL_DRYAD_403_FORBIDDEN") from exc
        if exc.code==401:raise SourceError("R107_A_OFFICIAL_DRYAD_401_AUTH_REQUIRED") from exc
        if exc.code==404:raise SourceError("R107_A_OFFICIAL_DRYAD_404_NOT_FOUND") from exc
        raise SourceError("R107_A_OFFICIAL_DRYAD_HTTP_FAILURE") from exc

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        result=double_source(original_get(),original_get())
    except (ValueError,TypeError,OSError,KeyError,UnicodeError,csv.Error) as exc:
        result={"research_id":"R107","phase":"A",
                "status":"R107_A_OFFICIAL_SOURCE_E1_FAIL_CLOSED",
                "safe_failure":str(exc) if isinstance(exc,SourceError) else "R107_A_OFFICIAL_DRYAD_SOURCE_UNVERIFIED",
                "human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R107_A_GENUINE_2020_DRYAD_ORIGINAL_DATASET_CSV_DOUBLE_SHA_HEADER_E1":
        raise SystemExit(1)

if __name__=="__main__":
    main()
