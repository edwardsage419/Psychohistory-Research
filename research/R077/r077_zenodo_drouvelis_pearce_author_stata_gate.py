#!/usr/bin/env python3
"""R077 Zenodo Drouvelis/Pearce original fourth-human-study source G0.

Reads author-published study data solely for integrity, schema, session and
source segregation metadata. No human action rows, predictions or per-ID output.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re
from collections import Counter
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError

RECORD_URL="https://zenodo.org/api/records/15462528"
DIRECT_FILE="https://zenodo.org/records/15462528/files/cleandata.dta?download=1"
EXPECTED_MD5="4cce04ea68b7a0492c242b206efebe53"
PUB_DOI="10.5281/zenodo.15462528"
LIMIT=5_000_000

def get(url):
    request=Request(url,headers={
        "User-Agent":"Psychohistory-R077-true-fourth-human-zenodo-eligibility/1.0",
        "Accept":"application/json,application/octet-stream,*/*"
    })
    with urlopen(request,timeout=60) as resp:
        b=resp.read(LIMIT+1)
        if len(b)>LIMIT: raise ValueError("SOURCE_RESPONSE_EXCEEDS_FIVE_MEGABYTES")
        return b,resp.status,resp.headers.get("Content-Type",""),resp.url

def safe_column(col):
    if len(col)>55 or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,54}",col):
        return "<redacted-column-name>"
    return col

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    p.add_argument("--private-dir",type=pathlib.Path,required=True)
    args=p.parse_args()
    result={
        "research_id":"R077","phase":"ORIGINAL_FOURTH_AUTHOR_DATA_SCHEMA_GATE_ONLY",
        "paper_DOI":"10.1016/j.euroecorev.2025.105075",
        "original_zenodo_record_DOI":PUB_DOI,
        "zenodo_record_api":RECORD_URL,"original_author_file_url":DIRECT_FILE,
        "source_expected_md5":EXPECTED_MD5,
        "genuine_human_source_schema":"UNVERIFIED",
        "original_session_identity":"UNVERIFIED",
        "fresh_study_vs_prior_study_separation":"UNVERIFIED",
        "fourth_human_M0_to_M6_scores":"NOT_RUN",
        "person_records_exported":False,
        "PESEN_v0.1":"FROZEN"
    }
    try:
        meta,mstatus,ctype,_=get(RECORD_URL)
        md=json.loads(meta)
        result["zenodo_api_HTTP_status"]=mstatus
        result["zenodo_record_id"]=md.get("id")
        result["record_title_found"]="Intelligence and strategy choice" in str(md.get("metadata",{}).get("title",""))
        filemeta=md.get("files",[])
        # New Zenodo API has list files entries; legacy entries have a links list.
        result["official_file_count"]=len(filemeta)
        result["official_file_safe_descriptors"]=[{
            "extension":"."+v.get("key","").lower().rsplit(".",1)[-1],
            "size":v.get("size"),
            "checksum_method":str(v.get("checksum","")).split(":")[0]
        } for v in filemeta if isinstance(v,dict)]
    except (HTTPError,URLError,ValueError,json.JSONDecodeError) as e:
        result["zenodo_api_failure_type"]=type(e).__name__
        if isinstance(e,HTTPError):result["zenodo_api_HTTP_status"]=e.code
    try:
        data,status,contenttype,target=get(DIRECT_FILE)
        result["original_data_HTTP_status"]=status
        result["original_data_content_type"]=contenttype.split(";")[0]
        result["downloaded_data_bytes"]=len(data)
        result["downloaded_data_md5"]=hashlib.md5(data).hexdigest()
        result["downloaded_data_sha256"]=hashlib.sha256(data).hexdigest()
        if hashlib.md5(data).hexdigest()!=EXPECTED_MD5:
            raise ValueError("ZENODO_ORIGINAL_DTA_MD5_MISMATCH")
        args.private_dir.mkdir(parents=True,exist_ok=True)
        f=args.private_dir/"fourth_human_original.dta"
        f.write_bytes(data)
        import pandas as pd
        reader=pd.io.stata.StataReader(f)
        df=reader.read(convert_categoricals=False)
        result["data_shape"]={"rows":len(df),"columns":len(df.columns)}
        result["data_column_names"]=[safe_column(s) for s in df.columns]
        result["data_column_dtypes"]={safe_column(n):str(df[n].dtype) for n in df.columns}
        # Publishing a cardinality is permitted only for expected structural columns,
        # never public individual values or a row-level excerpt.
        match=re.compile(r"(^|_)(sess|session|subject|player|partner|id|match|pair|round|period|game|supergame|treat|choice|coop|action|strategy|condition|stage|date)($|_)",re.I)
        match2=re.compile(r"session|subject|player|round|period|game|match|treat|decision|cooperat|partner|experiment",re.I)
        inspect=[n for n in df if match.search(n) or match2.search(n)]
        result["potentially_relevant_column_cardinality"]={
            safe_column(n):int(df[n].nunique(dropna=True)) for n in inspect
        }
        result["potentially_relevant_column_missing"]={
            safe_column(n):int(df[n].isna().sum()) for n in inspect
        }
        result["genuine_human_source_schema"]="ORIGINAL_AUTHOR_CHECKSUM_MATCH_AND_DTA_READABLE"
        result["fourth_human_M0_to_M6_scores"]="NOT_RUN"
    except (HTTPError,URLError,ValueError,ImportError,IOError) as e:
        result["data_access_error_type"]=type(e).__name__
        if isinstance(e,HTTPError):result["original_data_HTTP_status"]=e.code
        if isinstance(e,ValueError):result["data_access_error_reason"]=str(e)[:95]
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
if __name__=="__main__":main()
