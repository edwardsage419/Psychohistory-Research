#!/usr/bin/env python3
"""R107 A3: one frozen Dryad official REST download alternate; publisher MD5."""
from __future__ import annotations
import argparse
import hashlib
import json
import pathlib
import urllib.request
import urllib.error
import urllib.parse

from r107_phase_a_2020_original_dryad_CSV_double_SHA_header_only import (
    CAP,SourceError,validate_complete_csv_header_only,double_source,
)

URL="https://datadryad.org/api/v2/files/296893/download"
PUBLISHER_MD5="039b5cc661fb62210509ac9f8de388d7"
PUBLISHER_BYTE_SIZE=215221

def validate_url(value):
    p=urllib.parse.urlsplit(value)
    if (p.scheme,p.netloc,p.path,p.query,p.fragment)!=("https","datadryad.org","/api/v2/files/296893/download","",""):
        raise SourceError("R107_A3_OFFICIAL_API_DOWNLOAD_URL_UNAPPROVED")

class DenyRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise SourceError("R107_A3_OFFICIAL_SOURCE_ALTERNATE_REDIRECT_UNVERIFIED")

def verify_firstparty_original_blob(raw):
    if type(raw) is not bytes or len(raw)!=PUBLISHER_BYTE_SIZE:
        raise SourceError("R107_A3_PUBLISHER_FILE_SIZE_NOT_MATCHED")
    if hashlib.md5(raw).hexdigest()!=PUBLISHER_MD5:
        raise SourceError("R107_A3_OFFICIAL_DRYAD_PUBLISHED_MD5_MISMATCH")
    header=validate_complete_csv_header_only(raw)
    return header

def verified_twice(raw1,raw2):
    first=verify_firstparty_original_blob(raw1)
    second=verify_firstparty_original_blob(raw2)
    if raw1!=raw2 or first["project_calculated_original_whole_SHA256"]!=second["project_calculated_original_whole_SHA256"]:
        raise SourceError("R107_A3_ORIGINAL_DOUBLE_SOURCE_BYTES_DISAGREE")
    first["phase"]="A3"
    first["status"]="R107_A3_GENUINE_OFFICIAL_DRYAD_296893_CSV_PUBLISHED_MD5_DOUBLE_SHA_E1"
    first["published_official_MD5_matched"]=PUBLISHER_MD5
    first["published_official_bytes_matched"]=PUBLISHER_BYTE_SIZE
    first["two_separate_exact_official_API_downloads_match"]=True
    first["publisher_independent_MD5_available_and_verified"]=True
    return first

def download():
    validate_url(URL)
    req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R107-2020-Dryad-A3-Exact-Publisher-MD5-Only/1.0",
                                            "Accept":"text/csv,application/octet-stream;q=0.9"})
    try:
        with urllib.request.build_opener(DenyRedirect()).open(req,timeout=50) as resp:
            validate_url(resp.geturl())
            if resp.status!=200:
                raise SourceError("R107_A3_OFFICIAL_API_SOURCE_HTTP_NON200")
            return resp.read(CAP+1)
    except urllib.error.HTTPError as exc:
        if exc.code==401:raise SourceError("R107_A3_OFFICIAL_API_REQUIRES_AUTH_401") from exc
        if exc.code==403:raise SourceError("R107_A3_OFFICIAL_API_FORBIDDEN_403") from exc
        if exc.code==404:raise SourceError("R107_A3_OFFICIAL_API_ROUTE_NOT_FOUND_404") from exc
        raise SourceError("R107_A3_OFFICIAL_API_SOURCE_HTTP_FAILURE") from exc

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    a=p.parse_args()
    try:output=verified_twice(download(),download())
    except (ValueError,OSError,TypeError,UnicodeError,KeyError) as exc:
        output={"research_id":"R107","phase":"A3",
                "status":"R107_A3_OFFICIAL_ALTERNATE_SOURCE_NOT_AUTHENTICATED",
                "safe_failure":str(exc) if isinstance(exc,SourceError) else "R107_A3_REAL_OFFICIAL_SOURCE_UNVERIFIED",
                "human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(output,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(output,sort_keys=True))
    if output["status"]!="R107_A3_GENUINE_OFFICIAL_DRYAD_296893_CSV_PUBLISHED_MD5_DOUBLE_SHA_E1":
        raise SystemExit(1)

if __name__=="__main__":main()
