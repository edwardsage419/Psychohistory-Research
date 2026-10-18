#!/usr/bin/env python3
"""R108 A3: exactly verified publisher Figshare->S3 host + published MD5, double source."""
from __future__ import annotations
import argparse
import json
import pathlib
import urllib.parse
import urllib.request
import urllib.error

import r108_phase_a1_original_2017_Leicester_fixed_pair_CSV_MD5_double_SHA_header_only as a

SIGNED_DELEGATE="s3-eu-west-1.amazonaws.com"
class VerifiedSingleDelegate(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if req.full_url!=a.SOURCE:
            raise a.SourceError("R108_A3_ONLY_ONE_FIRSTPARTY_S3_DELEGATION_PERMITTED")
        try:p=urllib.parse.urlsplit(newurl)
        except ValueError as exc:raise a.SourceError("R108_A3_DELEGATE_URL_PARSE_INVALID") from exc
        if (p.scheme!="https" or p.hostname!=SIGNED_DELEGATE or
            p.username or p.password or p.fragment or p.port not in (None,443)
            or not p.path.startswith("/")):
            raise a.SourceError("R108_A3_DELEGATED_SOURCE_NOT_EXACT_OBSERVED_S3_HOST")
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def allowed_final_url(u):
    p=urllib.parse.urlsplit(u)
    if p.scheme!="https" or p.hostname!=SIGNED_DELEGATE or p.username or p.password or p.fragment or p.port not in (None,443):
        raise a.SourceError("R108_A3_FINAL_DOWNLOADED_SOURCE_HOST_UNVERIFIED")
    return True

def real_publisher_download():
    a.strict_url(a.SOURCE,"source")
    req=urllib.request.Request(a.SOURCE,headers={
        "User-Agent":"Psychohistory-R108-A3-Figshare-Official-S3-MD5-Verified/1.0",
        "Accept":"text/csv,application/octet-stream"})
    try:
        with urllib.request.build_opener(VerifiedSingleDelegate()).open(req,timeout=55) as res:
            if res.status!=200:
                raise a.SourceError("R108_A3_OFFICIAL_DELEGATED_HTTP_NOT_200")
            allowed_final_url(res.geturl())
            return res.read(a.CAP+1)
    except urllib.error.HTTPError as exc:
        if exc.code in (401,403,404):
            raise a.SourceError("R108_A3_PUBLISHER_DELEGATED_HTTP_"+str(exc.code)) from exc
        raise a.SourceError("R108_A3_PUBLISHER_DELEGATED_HTTP_ERROR") from exc

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        metadata=a.get_url(a.METADATA,"metadata",262144)
        if len(metadata)>262144:raise a.SourceError("R108_A3_METADATA_EXCEEDS_LIMIT")
        a.validate_article_original_file_catalog(json.loads(metadata.decode("utf-8")))
        result=a.verified_source_pair(real_publisher_download(),real_publisher_download())
        result["phase"]="A3"
        result["status"]="R108_A3_TRUE_2017_LEICESTER_FIGSHARE_PUBLISHER_MD5_DOUBLE_S3_SOURCE_E1"
        result["verified_publisher_file_delegated_storage_host_only"]=SIGNED_DELEGATE
        result["raw_signed_URL_or_original_human_behavior_exported"]=False
    except (OSError,ValueError,TypeError,KeyError,UnicodeError) as exc:
        result={
            "research_id":"R108","phase":"A3",
            "status":"R108_A3_ORIGINAL_OFFICIAL_DELEGATED_SOURCE_FAIL_CLOSED",
            "safe_failure":str(exc) if isinstance(exc,a.SourceError) else "R108_A3_PUBLISHER_ORIGINAL_SOURCE_UNVERIFIED",
            "actual_human_model_scores":0,"PESEN_v0_1":"FROZEN",
        }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R108_A3_TRUE_2017_LEICESTER_FIGSHARE_PUBLISHER_MD5_DOUBLE_S3_SOURCE_E1":
        raise SystemExit(1)
if __name__=="__main__":main()
