#!/usr/bin/env python3
"""R105 Phase A original 2024 Zenodo long CSV publisher MD5, source header only.

No individual, group, session, outcome or choice cell is dereferenced.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import pathlib
import re
import urllib.parse
import urllib.request

RECORD="10818840"
FILENAME="data_long_format.csv"
SOURCE_URL=f"https://zenodo.org/records/{RECORD}/files/{FILENAME}?download=1"
PUBLISHED_MD5="a3afbb4e52179a0e1d8b1b533f076cc9"
CAP=2*1024*1024
HEADER_NAME=re.compile(r"[A-Za-z_][A-Za-z0-9_. -]{0,119}")

class SourceGateError(ValueError):pass

def validate_url(url):
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or p.netloc!="zenodo.org" or p.path!=f"/records/{RECORD}/files/{FILENAME}" or p.query not in ("","download=1") or p.fragment:
        raise SourceGateError("R105_ORIGINAL_PUBLISHER_URL_NOT_PINNED")

class OnlyExactPublisherRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        validate_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def source_header_only(b):
    if type(b) is not bytes or not (100<=len(b)<=CAP):
        raise SourceGateError("R105_ORIGINAL_PUBLISHER_CSV_SIZE_INVALID")
    if hashlib.md5(b).hexdigest()!=PUBLISHED_MD5:
        raise SourceGateError("R105_ORIGINAL_PUBLISHER_FULL_MD5_MISMATCH")
    if b"\x00" in b or b.lstrip()[:60].lower().startswith((b"<html",b"<!doctype",b"<?xml")):
        raise SourceGateError("R105_ORIGINAL_NOT_TEXT_CSV")
    line,sep,_=b.partition(b"\n")
    if not sep or len(line)>16384:
        raise SourceGateError("R105_ORIGINAL_CSV_FIRST_HEADER_MISSING")
    try:
        names=next(csv.reader([line.rstrip(b"\r").decode("utf-8-sig")],strict=True))
    except (UnicodeError,csv.Error,StopIteration) as exc:
        raise SourceGateError("R105_ORIGINAL_FIRST_CSV_HEADER_UNREADABLE") from exc
    if not 3<=len(names)<=150 or len(names)!=len(set(names)) or any(HEADER_NAME.fullmatch(x) is None for x in names):
        raise SourceGateError("R105_ORIGINAL_SOURCE_UNSAFE_OR_DUPLICATED_HEADER")
    physical=b.count(b"\n")-1 if b.endswith(b"\n") else b.count(b"\n")
    if not 1<=physical<=100000:
        raise SourceGateError("R105_ORIGINAL_SOURCE_PHYSICAL_ROW_COUNT_INVALID")
    return {
       "research_id":"R105","phase":"A",
       "status":"R105_ACTUAL_FIRSTPARTY_2024_CPR_LONG_CSV_PUBLISHED_MD5_HEADER_E1",
       "publisher_original_DOI":"10.5281/zenodo.10818840",
       "original_csv_filename":FILENAME,
       "original_full_source_bytes":len(b),
       "official_original_publisher_MD5":PUBLISHED_MD5,
       "project_original_complete_SHA256":hashlib.sha256(b).hexdigest(),
       "original_csv_header_field_count":len(names),
       "public_sanitized_original_header_field_names":names,
       "physical_original_data_row_lines_unparsed":physical,
       "any_original_human_choice_value_read":False,
       "any_original_person_or_group_identifier_cell_read":False,
       "actual_human_predictions_scored":0,
       "PESEN_v0_1":"FROZEN",
    }

def source_download():
    validate_url(SOURCE_URL)
    req=urllib.request.Request(SOURCE_URL,headers={"User-Agent":"Psychohistory-R105-Source-MD5-HeaderOnly/1.0"})
    with urllib.request.build_opener(OnlyExactPublisherRedirect()).open(req,timeout=55) as response:
        validate_url(response.geturl())
        if response.status!=200:
            raise SourceGateError("R105_PUBLISHER_RESPONSE_NOT_200")
        return response.read(CAP+1)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=pathlib.Path)
    args=p.parse_args()
    try:
        result=source_header_only(source_download())
    except (TypeError,ValueError,OSError,KeyError) as exc:
        result={"research_id":"R105","phase":"A",
                "status":"R105_ORIGINAL_SOURCE_FAIL_CLOSED",
                "safe_failure":str(exc) if isinstance(exc,SourceGateError) else "R105_FIRSTPARTY_SOURCE_NOT_AUTHENTICATED",
                "actual_human_predictions_scored":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R105_ACTUAL_FIRSTPARTY_2024_CPR_LONG_CSV_PUBLISHED_MD5_HEADER_E1":
        raise SystemExit(1)

if __name__=="__main__":main()
