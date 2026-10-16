#!/usr/bin/env python3
"""Bounded Dryad v8 human-IPD source audit. No human rows retained or printed."""
from __future__ import annotations
import argparse,csv,hashlib,io,json,re
from pathlib import Path
from urllib import request,error

DOI="10.5061/dryad.37pvmcvmk"
SOURCES={"fix.csv":1514373,"rand.csv":1514372,"README.txt":1514376}
MAX_BYTES=3_000_000
MAX_ROWS=500_000
MAX_COLUMNS=200
BASE="https://datadryad.org"


def safe_name(name: str):
    return name if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.-]{0,75}",name) else "[nonstandard-field]"


def summarize_csv(raw: bytes):
    text=raw.decode("utf-8-sig")
    rd=csv.reader(io.StringIO(text,newline=""))
    try:head=next(rd)
    except StopIteration:raise ValueError("empty CSV") from None
    if not (1<=len(head)<=MAX_COLUMNS):
        raise ValueError("invalid column count")
    if len(set(head))!=len(head):
        raise ValueError("ambiguous duplicate CSV fields")
    rows=0;bad_shapes=0;empty_by_col=[0]*len(head)
    for row in rd:
        rows+=1
        if rows>MAX_ROWS:
            raise ValueError("source rows exceed cap")
        if len(row)!=len(head):
            bad_shapes+=1
            continue
        for i,val in enumerate(row):
            if val.strip() in ("", "NA", "NaN", "."):
                empty_by_col[i]+=1
    if rows<2:
        raise ValueError("source has too few rows to represent repeated human PD")
    if bad_shapes:
        raise ValueError("ragged source rows")
    return {"record_rows":rows,"columns":len(head),
            "safe_column_names":[safe_name(x) for x in head],
            "total_missing_cells":sum(empty_by_col),
            "source_columns_unique":True,
            "all_rows_shape_consistent":True,
            "individual_actions_interpreted":False}


def bounded_get(url,opener=request.urlopen):
    req=request.Request(url,headers={"User-Agent":"Psychohistory-R067-CC0-DOI-source-gate/1.0",
                                     "Accept":"*/*"})
    try:
        with opener(req,timeout=20) as res:
            raw=res.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES:
            return None,"OVER_LIMIT"
        return raw,"OK"
    except error.HTTPError as ex:
        return None,"HTTP_"+str(ex.code)
    except (error.URLError,TimeoutError,OSError):
        return None,"NETWORK_OR_API_ERROR"


def audit_download(name,identity,opener=request.urlopen):
    urls=[
        ("public_file_stream",f"{BASE}/downloads/file_stream/{identity}"),
        ("dryad_api_public_file",f"{BASE}/api/v2/files/{identity}/download"),
    ]
    attempts=[]
    for label,url in urls:
        raw,status=bounded_get(url,opener)
        attempts.append({"route":label,"status":status})
        if raw is None:
            continue
        if raw[:200].lower().startswith((b"<!doctype html",b"<html")):
            attempts[-1]["status"]="RETURNED_HTML_NOT_SOURCE"
            continue
        if name.lower().endswith(".csv"):
            try:
                parsed=summarize_csv(raw)
            except (UnicodeError,csv.Error,ValueError) as ex:
                attempts[-1]["status"]="STRUCTURE_UNRESOLVED_"+type(ex).__name__
                continue
        else:
            try:
                txt=raw.decode("utf-8-sig")
            except UnicodeError:
                attempts[-1]["status"]="README_ENCODING_UNRESOLVED"
                continue
            parsed={"readme_line_count":len(txt.splitlines()),
                    "has_fields_hint":("round" in txt.lower() or "turn" in txt.lower()),
                    "contents_redistributed":False}
        return {"status":"SOURCE_BYTES_PARSED","name":name,"public_file_id":identity,
                "download_bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),
                "structure":parsed,"download_paths_tried":attempts}
    return {"status":"SOURCE_DOWNLOAD_UNRESOLVED","name":name,
            "public_file_id":identity,"download_paths_tried":attempts}


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    sources={name:audit_download(name,file_id) for name,file_id in SOURCES.items()}
    complete=all(sources[n]["status"]=="SOURCE_BYTES_PARSED" for n in ("fix.csv","rand.csv"))
    report={
        "research_id":"R067","stage":"E2_DRYAD_IPD_REAL_SOURCE_SCHEMA",
        "protocol":"protocols/R067_E2_DRYAD_BINARY_IPD_SOURCE_GATE_2026-10-16.md",
        "source_doi":DOI,"reported_dataset_version":8,
        "files":sources,
        "source_schema_status":"FIX_RAND_SOURCE_SCHEMA_PASS" if complete
            else "SOURCE_DOWNLOAD_OR_SCHEMA_UNRESOLVED",
        "human_pd_action_schema_verified":False,
        "experimental_payoff_matrix_not_the_same_as_R067_E1":True,
        "human_real_model_fit_performed":False,
        "no_individual_data_redistributed":True,
        "pesen_v01":"FROZEN",
    }
    args.output.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["source_schema_status"],
                      "files":{k:{"status":v["status"],"rows":v.get("structure",{}).get("record_rows"),
                                  "cols":v.get("structure",{}).get("columns")}
                               for k,v in sources.items()}},sort_keys=True))


if __name__=="__main__":
    main()
