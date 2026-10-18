#!/usr/bin/env python3
"""R106 A official 2025 Zenodo .dta original whole-file MD5 gate only."""
from __future__ import annotations
import argparse
import hashlib
import json
import pathlib
import urllib.parse
import urllib.request

DOI="10.5281/zenodo.15462528"
NAME="cleandata.dta"
URL=f"https://zenodo.org/records/15462528/files/{NAME}?download=1"
OFFICIAL_MD5="4cce04ea68b7a0492c242b206efebe53"
CAP=2*1024*1024

class SourceError(ValueError):
    pass

def validate_url(url):
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or p.netloc!="zenodo.org" or p.path!="/records/15462528/files/cleandata.dta" or p.query not in ("","download=1") or p.fragment:
        raise SourceError("R106_OFFICIAL_DTA_FILE_URL_NOT_PINNED")

class ExactRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        validate_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def verify_only(b):
    if type(b) is not bytes or not 100<=len(b)<=CAP:
        raise SourceError("R106_ORIGINAL_PUBLISHED_DTA_SIZE_INVALID")
    if hashlib.md5(b).hexdigest()!=OFFICIAL_MD5:
        raise SourceError("R106_ORIGINAL_PUBLISHED_MD5_MISMATCH")
    return {
        "research_id":"R106","phase":"A",
        "status":"R106_TRUE_ZENODO_PEARCE_DROUVELIS_DTA_MD5_SOURCE_E1_ONLY",
        "original_dataset_DOI":DOI,
        "original_source_filename":NAME,
        "original_publisher_MD5":OFFICIAL_MD5,
        "original_full_file_bytes":len(b),
        "study_computed_original_SHA256":hashlib.sha256(b).hexdigest(),
        "original_first_bytes_stata_XML_header_class":b.startswith(b"<stata_dta>"),
        "original_person_session_opponent_cohort_verified":False,
        "new_independent_recruited_cohort_verified":False,
        "original_human_data_records_or_variables_parsed":False,
        "real_human_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",required=True,type=pathlib.Path)
    x=ap.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R106-2025-Exact-Official-Stata-DTA-MD5-SourceOnly/1.0"})
        with urllib.request.build_opener(ExactRedirect()).open(req,timeout=60) as resp:
            validate_url(resp.geturl())
            raw=resp.read(CAP+1)
        out=verify_only(raw)
    except (OSError,ValueError,TypeError) as exc:
        out={
            "research_id":"R106","phase":"A","status":"R106_A_ORIGINAL_DTA_SOURCE_FAIL_CLOSED",
            "safe_failure":str(exc) if isinstance(exc,SourceError) else "R106_A_GENUINE_SOURCE_UNVERIFIED",
            "real_human_scores":0,"PESEN_v0_1":"FROZEN",
        }
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,sort_keys=True))
    if out["status"]!="R106_TRUE_ZENODO_PEARCE_DROUVELIS_DTA_MD5_SOURCE_E1_ONLY":
        raise SystemExit(1)

if __name__=="__main__":
    main()
