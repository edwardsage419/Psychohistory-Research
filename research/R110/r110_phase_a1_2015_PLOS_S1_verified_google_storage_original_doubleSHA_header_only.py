#!/usr/bin/env python3
"""R110 A1 official PLOS S1 original human experimental CSV E1, header-only.

One exact firstparty PLOS S1 DOI publisher URL -> one A0-verified official
Google Storage delegated host. Whole source SHA twice; no original body cells.
"""
from __future__ import annotations
import argparse,csv,hashlib,json,pathlib,urllib.error,urllib.parse,urllib.request
from r110_phase_a0_2015_bone_UCL_PLOS_s1_original_CSV_delivery_no_body import URL,origin,SourceError

DELEGATE="storage.googleapis.com"
CAP=2097152
MINIMUM=10240
MAX_REDIRECT_URL=8192

def delegated_final(u):
    try:p=urllib.parse.urlsplit(u)
    except ValueError as e:raise SourceError("R110_A1_DELEGATE_URL_INVALID") from e
    if (p.scheme!="https" or p.hostname!=DELEGATE or p.username or p.password
        or p.fragment or p.port not in (None,443) or not p.path.startswith("/")
        or len(u)>MAX_REDIRECT_URL):
        raise SourceError("R110_A1_DELEGATE_HOST_NOT_PREAPPROVED_OFFICIAL_PLOS")
    return True

class SinglePublisherDelegation(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if req.full_url!=URL:
            raise SourceError("R110_A1_DOUBLE_PUBLISHER_DELEGATION_DENIED")
        delegated_final(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def authenticate_header_and_whole_SHA(raw):
    if type(raw) is not bytes or not MINIMUM<=len(raw)<=CAP:
        raise SourceError("R110_A1_TRUE_OFFICIAL_ORIGINAL_CSV_SIZE_NOT_BOUNDED")
    if b"\x00" in raw or raw.lstrip()[:128].lower().startswith((
        b"<html",b"<!doctype",b"<?xml",b"{",b"[")):
        raise SourceError("R110_A1_OFFICIAL_SOURCE_BODY_NOT_PLAIN_CSV")
    head,sep,_=raw.partition(b"\n")
    if not sep or len(head)>16384:
        raise SourceError("R110_A1_TRUE_S1_CSV_HEADER_NOT_BOUNDED")
    try:
        columns=next(csv.reader([head.rstrip(b"\r").decode("utf-8-sig")],strict=True))
    except (UnicodeError,csv.Error,StopIteration) as e:
        raise SourceError("R110_A1_S1_SOURCE_HEADER_PARSE_INVALID") from e
    if not 2<=len(columns)<=500:
        raise SourceError("R110_A1_S1_SOURCE_HEADER_FIELD_COUNT_NOT_VALID")
    if any(len(c)>256 for c in columns):
        raise SourceError("R110_A1_S1_SOURCE_HEADER_FIELD_TOO_LONG")
    data_lines=raw.count(b"\n")-1 if raw.endswith(b"\n") else raw.count(b"\n")
    if data_lines<1:
        raise SourceError("R110_A1_NO_SOURCE_DATA_LINES")
    return {
        "research_id":"R110","phase":"A1",
        "status":"R110_A1_TRUE_PLOS_2015_S1_OFFICIAL_DELEGATED_ORIGINAL_CSV_DOUBLE_SHA_E1",
        "paper_DOI":"10.1371/journal.pone.0117183",
        "publisher_supplement_DOI":"10.1371/journal.pone.0117183.s001",
        "original_source_complete_bytes":len(raw),
        "project_computed_whole_original_SHA256":hashlib.sha256(raw).hexdigest(),
        "publisher_MD5_independently_published_and_verified":False,
        "source_S1_first_CSV_header_column_count":len(columns),
        "source_header_blank_column_count":sum(not c.strip() for c in columns),
        "source_header_duplicate_column_count":len(columns)-len(set(columns)),
        "source_header_nonASCII_or_control_name_count":sum(any(ord(ch)<32 or ord(ch)>126 for ch in c) for c in columns),
        "source_maximum_CSV_header_name_length":max(map(len,columns)),
        "source_physical_CSV_data_lines_no_behavior_values_read":data_lines,
        "verified_official_A0_observed_delegated_hostname_only":DELEGATE,
        "original_CSV_actor_pair_action_or_round_value_accessed":False,
        "real_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def two_independent_full_sources(b1,b2):
    x=authenticate_header_and_whole_SHA(b1)
    y=authenticate_header_and_whole_SHA(b2)
    if b1!=b2 or x["project_computed_whole_original_SHA256"]!=y["project_computed_whole_original_SHA256"]:
        raise SourceError("R110_A1_TWO_SEPARATE_OFFICIAL_PLOS_CSV_DOWNLOADS_NOT_IDENTICAL")
    x["two_separate_official_PLOS_S1_downloads_byte_identical"]=True
    return x

def actual_official_source():
    origin(URL)
    req=urllib.request.Request(URL,headers={
        "User-Agent":"Psychohistory-R110-2015-PLOS-One-S1-Official-Google-Delegate-E1/1.0",
        "Accept":"text/csv,application/octet-stream;q=0.9,*/*;q=0.2"})
    try:
        with urllib.request.build_opener(SinglePublisherDelegation()).open(req,timeout=75) as res:
            if res.status!=200:
                raise SourceError("R110_A1_ORIGINAL_OFFICIAL_S1_FINAL_STATUS_NOT_200")
            delegated_final(res.geturl())
            return res.read(CAP+1)
    except urllib.error.HTTPError as e:
        if e.code in (401,403,404,429):
            raise SourceError("R110_A1_ORIGINAL_OFFICIAL_S1_HTTP_"+str(e.code)) from e
        raise SourceError("R110_A1_ORIGINAL_OFFICIAL_S1_HTTP_FAILURE") from e

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    arg=p.parse_args()
    try:
        result=two_independent_full_sources(actual_official_source(),actual_official_source())
    except (OSError,ValueError,TypeError,KeyError,UnicodeError,csv.Error) as e:
        result={"research_id":"R110","phase":"A1",
            "status":"R110_A1_FIRSTPARTY_PUBLISHED_S1_SOURCE_NOT_AUTHENTICATED",
            "safe_failure":str(e) if isinstance(e,SourceError) else "R110_A1_TRUE_PLOS_FIRSTPARTY_ORIGINAL_SOURCE_FAILED",
            "real_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    arg.output.parent.mkdir(parents=True,exist_ok=True)
    arg.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R110_A1_TRUE_PLOS_2015_S1_OFFICIAL_DELEGATED_ORIGINAL_CSV_DOUBLE_SHA_E1":
        raise SystemExit(1)

if __name__=="__main__":main()
