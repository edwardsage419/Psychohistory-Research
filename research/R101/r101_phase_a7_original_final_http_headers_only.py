#!/usr/bin/env python3
"""R101 A7: exact A6 request with only final HTTP metadata, zero entity reads."""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request

from r101_phase_a6_dataverse_surf_signed_zip_sha_only import (
    URL, TARGET, OneExactPublisherRedirect, validate_source_url, ArchiveGateError
)

def bounded_final_metadata(final_url, status, redirect_count, content_type, content_length):
    host=urllib.parse.urlsplit(final_url).hostname
    host=host if host in ("dataverse.nl",TARGET) else "OTHER"
    main_type=(content_type or "").split(";",1)[0].strip().lower()
    if not re.fullmatch(r"[a-z0-9.+-]{1,40}/[a-z0-9.+-]{1,80}",main_type):
        main_type="OTHER"
    number=None
    if content_length is not None and str(content_length).isascii() and str(content_length).isdecimal() and int(content_length)<=100000000:
        number=int(content_length)
    if type(status) is not int or not (100<=status<=599) or type(redirect_count) is not int or not (0<=redirect_count<=1):
        raise ArchiveGateError("R101_A7_FINAL_HTTP_METADATA_UNSAFE")
    return {
        "research_id":"R101","phase":"A7",
        "status":"R101_A7_FINAL_HTTP_RESPONSE_HEADER_DIAGNOSTIC_ONLY",
        "final_http_status":status,
        "final_http_host_class":host,
        "publisher_303_follow_count":redirect_count,
        "final_content_type_class":main_type,
        "final_content_length_if_safe":number,
        "original_zip_body_bytes_read":0,
        "original_human_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def actual_metadata_only():
    validate_source_url(URL)
    req=urllib.request.Request(URL,headers={
        "User-Agent":"Psychohistory-R101-A6-DataverseNL-SURF-Exact-2MB-Original-ZIP-SHA/1.0",
        "Accept":"application/octet-stream",
    })
    handler=OneExactPublisherRedirect()
    try:
        with urllib.request.build_opener(handler).open(req,timeout=55) as resp:
            return bounded_final_metadata(resp.geturl(),int(resp.status),handler.count,
                                          resp.headers.get("Content-Type"),resp.headers.get("Content-Length"))
    except urllib.error.HTTPError as exc:
        return bounded_final_metadata(exc.geturl(),int(exc.code),handler.count,
                                      exc.headers.get("Content-Type"),exc.headers.get("Content-Length"))

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    x=p.parse_args()
    try:
        res=actual_metadata_only()
    except (ValueError,OSError,TypeError,KeyError) as e:
        res={"research_id":"R101","phase":"A7","status":"R101_A7_RESPONSE_FAIL_CLOSED",
             "safe_failure":str(e) if isinstance(e,ArchiveGateError) else "R101_A7_PUBLISHER_FINAL_STATUS_UNVERIFIED",
             "original_human_scores":0,"PESEN_v0_1":"FROZEN"}
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(res,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(res,sort_keys=True))
    if res["status"]!="R101_A7_FINAL_HTTP_RESPONSE_HEADER_DIAGNOSTIC_ONLY":
        raise SystemExit(1)

if __name__=="__main__":
    main()
