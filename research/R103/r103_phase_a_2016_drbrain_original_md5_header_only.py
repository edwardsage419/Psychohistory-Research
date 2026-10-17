#!/usr/bin/env python3
"""R103 original Dr Brain decisions source full publisher MD5, CSV header ONLY.

Never interpret source action, opponent action, player ID, or game values.
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

RECORD="1127154"
NAME="drbrain_decisions.csv"
URL=f"https://zenodo.org/records/{RECORD}/files/{NAME}?download=1"
OFFICIAL_MD5="712e3a4ae905af3e004b4a31a38b250d"
CAP=1024*1024
MANDATORY_FIELDS=(
    "User_ID","Experiment_number","Round_number","S","T","Game",
    "Action","Opponent_ID","Opponent_Action",
)
HEADER_NAME=re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,79}")

class SourceError(ValueError):
    pass

def validate_url(url):
    p=urllib.parse.urlsplit(url)
    if (p.scheme!="https" or p.netloc!="zenodo.org"
        or p.path!=f"/records/{RECORD}/files/{NAME}"
        or p.query not in ("","download=1") or p.fragment):
        raise SourceError("R103_PUBLISHER_ORIGINAL_FILE_URL_UNTRUSTED")

class ExactOfficialRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        validate_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def audit_firstparty_bytes_header_only(b):
    if type(b) is not bytes or not (120<=len(b)<=CAP):
        raise SourceError("R103_ORIGINAL_SOURCE_SIZE_INVALID")
    if hashlib.md5(b).hexdigest()!=OFFICIAL_MD5:
        raise SourceError("R103_ORIGINAL_PUBLISHER_FULLFILE_MD5_NOT_MATCHED")
    if b"\x00" in b:
        raise SourceError("R103_ORIGINAL_CSV_CONTAINS_NUL")
    first,delimiter,remaining=b.partition(b"\n")
    if not delimiter or len(first)>8192:
        raise SourceError("R103_ORIGINAL_CSV_HEADER_MISSING_OR_TOO_LONG")
    try:
        original_header=next(csv.reader([first.rstrip(b"\r").decode("utf-8-sig")],strict=True))
    except (UnicodeError,csv.Error,StopIteration) as exc:
        raise SourceError("R103_ORIGINAL_HEADER_CSV_SYNTAX_UNVERIFIED") from exc
    if not 1<=len(original_header)<=40 or len(original_header)!=len(set(original_header)):
        raise SourceError("R103_ORIGINAL_CSV_HEADER_COUNT_OR_DUPLICATES")
    if any(HEADER_NAME.fullmatch(field) is None for field in original_header):
        raise SourceError("R103_ORIGINAL_CSV_HEADER_IDENTIFIER_UNSAFE")
    missing=sorted(set(MANDATORY_FIELDS)-set(original_header))
    if missing:
        # Fixed failure code avoids publishing any unexpected source names.
        raise SourceError("R103_ORIGINAL_SOURCE_REQUIRED_DYADIC_HEADER_MISSING")
    physical_lines=b.count(b"\n")-1 if b.endswith(b"\n") else b.count(b"\n")
    if physical_lines<=0:
        raise SourceError("R103_ORIGINAL_CSV_NO_PHYSICAL_DATA_LINES")
    return {
        "research_id":"R103","phase":"A",
        "status":"R103_TRUE_2016_ZENODO_DYADIC_CSV_MD5_AND_HEADER_AUTHENTICATED",
        "source_DOI":"10.5281/zenodo.1127154",
        "official_original_filename":NAME,
        "original_full_file_bytes":len(b),
        "official_original_MD5":OFFICIAL_MD5,
        "original_project_computed_SHA256":hashlib.sha256(b).hexdigest(),
        "original_csv_header_count":len(original_header),
        "all_nine_publisher_declared_dyadic_header_fields_present":True,
        "original_additional_csv_columns_count":len(original_header)-len(MANDATORY_FIELDS),
        "source_physical_data_lines_without_parsing":physical_lines,
        "original_action_or_opponent_action_values_accessed":False,
        "original_person_or_experiment_ID_values_accessed":False,
        "real_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R103-2016-Dyadic-Original-Header-Only-MD5/1.0"})
        with urllib.request.build_opener(ExactOfficialRedirect()).open(req,timeout=55) as resp:
            validate_url(resp.geturl())
            b=resp.read(CAP+1)
        result=audit_firstparty_bytes_header_only(b)
    except (ValueError,TypeError,OSError,KeyError) as exc:
        result={
            "research_id":"R103","phase":"A",
            "status":"R103_A_FIRSTPARTY_SOURCE_FAIL_CLOSED",
            "safe_failure":str(exc) if isinstance(exc,SourceError) else "R103_A_OFFICIAL_SOURCE_OR_HEADER_UNVERIFIED",
            "real_human_model_scores":0,"PESEN_v0_1":"FROZEN",
        }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R103_TRUE_2016_ZENODO_DYADIC_CSV_MD5_AND_HEADER_AUTHENTICATED":
        raise SystemExit(1)

if __name__=="__main__":
    main()
