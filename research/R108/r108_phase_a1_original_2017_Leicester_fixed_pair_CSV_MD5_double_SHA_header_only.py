#!/usr/bin/env python3
"""R108 A1: genuine 2017 Leicester fixed-dyad original CSV MD5 + 2x SHA, header only."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import pathlib
import re
import urllib.parse
import urllib.request
import urllib.error

METADATA="https://api.figshare.com/v2/articles/10194938"
SOURCE="https://ndownloader.figshare.com/files/18370526"
EXPECTED_MD5="7afc755c293dc261d696d1b3f9ba796a"
EXPECTED_SIZE=36526
FILE_ID=18370526
FILENAME="Repeated Prisoner's Dilemma_raw data-data.csv"
CAP=131072
HEADER_RE=re.compile(r"[A-Za-z_][A-Za-z0-9_ .\-]{0,99}")

class SourceError(ValueError):pass

def strict_url(value,mode):
    p=urllib.parse.urlsplit(value)
    good=("https","api.figshare.com","/v2/articles/10194938","","") if mode=="metadata" else ("https","ndownloader.figshare.com","/files/18370526","","")
    if (p.scheme,p.netloc,p.path,p.query,p.fragment)!=good:
        raise SourceError("R108_A1_OFFICIAL_PUBLISHER_URL_UNTRUSTED")

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise SourceError("R108_A1_UNAUTHORIZED_ORIGINAL_SOURCE_REDIRECT")

def validate_article_original_file_catalog(obj):
    if not isinstance(obj,dict) or obj.get("id")!=10194938 or not isinstance(obj.get("files"),list):
        raise SourceError("R108_A1_PUBLISHER_ARTICLE_OR_FILE_LIST_MISMATCH")
    matching=[f for f in obj["files"] if isinstance(f,dict) and f.get("id")==FILE_ID]
    if len(matching)!=1:
        raise SourceError("R108_A1_PUBLISHER_ORIGINAL_FILE_ID_MISSING_OR_DUPLICATED")
    f=matching[0]
    if (f.get("name")!=FILENAME or f.get("size")!=EXPECTED_SIZE
        or f.get("computed_md5","").lower()!=EXPECTED_MD5
        or f.get("download_url")!=SOURCE):
        raise SourceError("R108_A1_PUBLISHER_ORIGINAL_FILE_MD5_SIZE_NAME_URL_NOT_BOUND")
    strict_url(f["download_url"],"source")
    return True

def authentic_original_header_only(raw):
    if type(raw) is not bytes or len(raw)!=EXPECTED_SIZE or len(raw)>CAP:
        raise SourceError("R108_A1_PUBLISHED_ORIGINAL_FILE_SIZE_NOT_MATCHED")
    if hashlib.md5(raw).hexdigest()!=EXPECTED_MD5:
        raise SourceError("R108_A1_PUBLISHED_ORIGINAL_MD5_MISMATCH")
    if b"\x00" in raw or raw.lstrip()[:100].lower().startswith((b"<html",b"<!doctype",b"{",b"[")):
        raise SourceError("R108_A1_PUBLISHER_RESPONSE_NOT_PLAIN_CSV")
    header,lf,_=raw.partition(b"\n")
    if not lf or len(header)>10000:
        raise SourceError("R108_A1_PUBLISHER_CSV_HEADER_INVALID")
    try:
        names=next(csv.reader([header.rstrip(b"\r").decode("utf-8-sig")],strict=True))
    except (UnicodeError,ValueError,csv.Error,StopIteration) as exc:
        raise SourceError("R108_A1_ORIGINAL_CSV_HEADER_PARSE_REFUSED") from exc
    if not 2<=len(names)<=100 or len(set(names))!=len(names) or any(HEADER_RE.fullmatch(name) is None for name in names):
        raise SourceError("R108_A1_ORIGINAL_HEADER_NAMES_NOT_ASCII_SAFE")
    lines=raw.count(b"\n")-1 if raw.endswith(b"\n") else raw.count(b"\n")
    if lines<1:
        raise SourceError("R108_A1_NO_ORIGINAL_CSV_DATA_LINES")
    return {"research_id":"R108","phase":"A1",
        "status":"R108_A1_LEICESTER_2017_PUBLISHER_MD5_VERIFIED_DOUBLE_SOURCE_CSV_E1",
        "original_dataset_article_ID":10194938,
        "original_file_ID":FILE_ID,
        "original_source_file_bytes":len(raw),
        "original_publisher_whole_MD5_verified":EXPECTED_MD5,
        "source_whole_file_SHA256":hashlib.sha256(raw).hexdigest(),
        "original_csv_header_columns":names,
        "original_csv_column_count":len(names),
        "original_CSV_physical_data_lines_unparsed":lines,
        "original_participant_or_choice_cells_dereferenced":False,
        "original_human_model_scores":0,"PESEN_v0_1":"FROZEN"}

def verified_source_pair(one,two):
    first=authentic_original_header_only(one)
    second=authentic_original_header_only(two)
    if one!=two or first["source_whole_file_SHA256"]!=second["source_whole_file_SHA256"]:
        raise SourceError("R108_A1_TWO_ORIGINAL_OFFICIAL_DOWNLOADS_DIFFER")
    first["two_independent_official_publisher_downloads_byte_identical"]=True
    return first

def get_url(value,mode,cap):
    strict_url(value,mode)
    req=urllib.request.Request(value,headers={
        "User-Agent":"Psychohistory-R108-2017-Leicester-MD5-Frozen-HeaderOnly/1.0",
        "Accept":"application/json" if mode=="metadata" else "text/csv,application/octet-stream"})
    try:
        with urllib.request.build_opener(NoRedirect()).open(req,timeout=45) as response:
            strict_url(response.geturl(),mode)
            if response.status!=200:
                raise SourceError("R108_A1_FIRSTPARTY_SOURCE_HTTP_NON200")
            return response.read(cap+1)
    except urllib.error.HTTPError as exc:
        if exc.code in (401,403,404):
            raise SourceError("R108_A1_FIRSTPARTY_SOURCE_HTTP_"+str(exc.code)) from exc
        raise SourceError("R108_A1_FIRSTPARTY_SOURCE_HTTP_OTHER") from exc

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=pathlib.Path,required=True)
    x=ap.parse_args()
    try:
        raw_metadata=get_url(METADATA,"metadata",262144)
        if len(raw_metadata)>262144:raise SourceError("R108_A1_PUBLISHER_METADATA_TOO_LARGE")
        validate_article_original_file_catalog(json.loads(raw_metadata.decode("utf-8")))
        result=verified_source_pair(get_url(SOURCE,"source",CAP),get_url(SOURCE,"source",CAP))
    except (OSError,ValueError,TypeError,KeyError,UnicodeError,csv.Error) as exc:
        result={"research_id":"R108","phase":"A1",
            "status":"R108_A1_ORIGINAL_FIRSTPARTY_CSV_SOURCE_FAIL_CLOSED",
            "safe_failure":str(exc) if isinstance(exc,SourceError) else "R108_A1_AUTHENTIC_SOURCE_UNVERIFIED",
            "original_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R108_A1_LEICESTER_2017_PUBLISHER_MD5_VERIFIED_DOUBLE_SOURCE_CSV_E1":
        raise SystemExit(1)
if __name__=="__main__":main()
