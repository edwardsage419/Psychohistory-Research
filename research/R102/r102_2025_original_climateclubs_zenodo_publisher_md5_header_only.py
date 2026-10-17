#!/usr/bin/env python3
"""R102 Phase A source-only original Zenodo full MD5 & 27-column HEADER audit.

Never parse or expose a source CSV data row or human contribution value.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import json
import pathlib
import urllib.parse
import urllib.request

RECORD="17610157"
NAME="Climate_Clubs_data.csv"
URL=f"https://zenodo.org/records/{RECORD}/files/{NAME}?download=1"
PUBLISHER_MD5="56931608b717aea06105ad10a58ff937"
CAP=1048576
EXPECTED_HEADER=(
    "participant.id_in_session","participant.code","participant._index_in_pages",
    "participant._max_page_index","participant._current_app_name","participant._round_number",
    "participant._current_page_name","participant.time_started","player.id_in_group",
    "player.automatic_decision","player.pledge","player.commitment","player.endowment",
    "player.contribution","player.my_total_payment","player.payoff_ronda","player.X",
    "player.Y","player.timeout_pledge","player.timeout_commit","player.timeout_contr",
    "group.id_in_subsession","group.coalition_flag","subsession.round_number",
    "session.code","group","treatment",
)
ROSTER_NAMES=("participant.code","participant.id_in_session","session.code",
              "group.id_in_subsession","group","player.id_in_group","subsession.round_number","treatment")

class SourceError(ValueError):
    pass

def validate_url(url):
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or p.netloc!="zenodo.org" or p.path!=f"/records/{RECORD}/files/{NAME}" or p.query not in ("","download=1") or p.fragment:
        raise SourceError("R102_ORIGINAL_ZENODO_URL_NOT_PINNED")

class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        validate_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def source_identity_header_only(raw):
    if type(raw) is not bytes or not (100<=len(raw)<=CAP):
        raise SourceError("R102_SOURCE_SIZE_INVALID")
    if hashlib.md5(raw).hexdigest()!=PUBLISHER_MD5:
        raise SourceError("R102_OFFICIAL_ORIGINAL_WHOLEFILE_MD5_MISMATCH")
    if b"\x00" in raw:
        raise SourceError("R102_SOURCE_BINARY_NUL_INVALID")
    # The original CSV header is the sole CSV source row interpreted here.
    first,sep,rest=raw.partition(b"\n")
    if not sep or len(first)>8192:
        raise SourceError("R102_SOURCE_HEADER_MISSING")
    try:
        header=next(csv.reader([first.rstrip(b"\r").decode("utf-8-sig")]))
    except (UnicodeError,csv.Error) as exc:
        raise SourceError("R102_CSV_HEADER_INVALID") from exc
    if tuple(header)!=EXPECTED_HEADER:
        raise SourceError("R102_OFFICIAL_27_COLUMN_HEADER_MISMATCH")
    # Count physical newline endings without parsing any real data cell value.
    if not raw.endswith(b"\n"):
        raise SourceError("R102_ORIGINAL_FINAL_LINE_TERMINATOR_UNEXPECTED")
    rows=raw.count(b"\n")-1
    if rows!=2700:
        raise SourceError("R102_PUBLISHER_2700_ROW_SHAPE_NOT_MATCHED")
    return {
        "research_id":"R102","phase":"A",
        "status":"R102_REAL_ZENODO_FIRST_PARTY_CSV_MD5_AND_HEADER_E1",
        "publisher_dataset_DOI":"10.5281/zenodo.17610157",
        "official_original_filename":NAME,
        "source_bytes":len(raw),
        "publisher_MD5":PUBLISHER_MD5,
        "actual_original_full_SHA256":hashlib.sha256(raw).hexdigest(),
        "original_CSV_header_column_count":len(header),
        "required_nonbehavior_roster_fields_present":all(k in header for k in ROSTER_NAMES),
        "physical_source_data_rows":rows,
        "any_original_human_decision_value_dereferenced":False,
        "any_original_person_or_session_identifier_exported":False,
        "real_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    x=p.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R102-Antonioni-2025-Original-CSV-MD5-HeaderOnly/1.0"})
        with urllib.request.build_opener(SafeRedirect()).open(req,timeout=55) as resp:
            validate_url(resp.geturl())
            raw=resp.read(CAP+1)
        result=source_identity_header_only(raw)
    except (ValueError,TypeError,OSError,KeyError,StopIteration) as exc:
        result={
            "research_id":"R102","phase":"A",
            "status":"R102_OFFICIAL_SOURCE_FAIL_CLOSED",
            "safe_failure":str(exc) if isinstance(exc,SourceError) else "R102_ORIGINAL_PUBLISHER_CSV_UNVERIFIED",
            "real_human_model_scores":0,
            "PESEN_v0_1":"FROZEN",
        }
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R102_REAL_ZENODO_FIRST_PARTY_CSV_MD5_AND_HEADER_E1":
        raise SystemExit(1)

if __name__=="__main__":
    main()
