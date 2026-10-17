#!/usr/bin/env python3
"""R101 Phase A official DataverseNL DOI metadata only; no raw game records."""
from __future__ import annotations
import argparse
from collections import Counter
import json
import pathlib
import re
import urllib.parse
import urllib.request


URL = "https://dataverse.nl/api/datasets/:persistentId/?persistentId=doi%3A10.34894%2FEYFM5L"
DOI = "doi:10.34894/EYFM5L"
CAP = 2 * 1024 * 1024

class GateError(ValueError):
    pass

def validate_url(url):
    p = urllib.parse.urlsplit(url)
    if (p.scheme != "https" or p.netloc != "dataverse.nl" or
        p.path not in ("/api/datasets/:persistentId/", "/api/datasets/:persistentId") or
        urllib.parse.parse_qs(p.query, strict_parsing=True) != {"persistentId":[DOI]} or p.fragment):
        raise GateError("R101_OFFICIAL_DATAVERSENL_METADATA_URL_REJECTED")

class SafeRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)

def safe_extension(name):
    if not isinstance(name,str) or not (1 <= len(name) <= 180) or "/" in name or "\\" in name:
        raise GateError("R101_FILE_NAME_UNSAFE")
    ext = name.rsplit(".",1)[-1].lower() if "." in name else "none"
    if ext not in ("csv","tsv","txt","zip","xlsx","xls","r","rds","dta","sav","json","do","pdf","md","py","m"):
        ext="other"
    return ext

def metadata_only(raw):
    if type(raw) is not bytes or not (2 <= len(raw) <= CAP):
        raise GateError("R101_METADATA_SIZE_INVALID")
    try:
        data = json.loads(raw.decode("utf-8"))
    except (UnicodeError,ValueError) as e:
        raise GateError("R101_OFFICIAL_METADATA_JSON_INVALID") from e
    if not isinstance(data,dict) or data.get("status") != "OK" or not isinstance(data.get("data"),dict):
        raise GateError("R101_OFFICIAL_API_STATUS_NOT_OK")
    obj=data["data"]
    ver=obj.get("latestVersion")
    if not isinstance(ver,dict) or not isinstance(ver.get("files"),list):
        raise GateError("R101_ORIGINAL_FILE_CATALOG_MISSING")
    pid=obj.get("persistentId")
    alt=ver.get("datasetPersistentId")
    if pid is not None and alt is not None and (not isinstance(pid,str) or not isinstance(alt,str) or pid.casefold()!=alt.casefold()):
        raise GateError("R101_OFFICIAL_DATASET_DOI_CONFLICT")
    source_pid=pid if pid is not None else alt
    if not isinstance(source_pid,str) or source_pid.casefold() != DOI.casefold():
        raise GateError("R101_OFFICIAL_DATASET_DOI_MISMATCH")
    files=ver["files"]
    if not (1 <= len(files) <= 300):
        raise GateError("R101_FILE_CATALOG_SIZE_INVALID")
    types=Counter()
    with_md5=0
    size_total=0
    for entry in files:
        if not isinstance(entry,dict) or not isinstance(entry.get("dataFile"),dict):
            raise GateError("R101_METADATA_FILE_ENTRY_INVALID")
        df=entry["dataFile"]
        typ=safe_extension(df.get("filename",entry.get("label")))
        types[typ]+=1
        size=df.get("filesize")
        if type(size) is not int or not (0 <= size <= 100000000):
            raise GateError("R101_FILE_SOURCE_SIZE_INVALID")
        size_total+=size
        md5=df.get("md5")
        if md5 is not None:
            if not isinstance(md5,str) or not re.fullmatch(r"[a-fA-F0-9]{32}",md5):
                raise GateError("R101_PUBLISHED_MD5_METADATA_INVALID")
            with_md5+=1
    return {
        "research_id":"R101", "phase":"A",
        "status":"R101_OFFICIAL_DATAVERSENL_CATALOG_METADATA_AUTHENTICATED_ONLY",
        "author_dataset_DOI":"10.34894/EYFM5L",
        "official_dataset_file_count":len(files),
        "anonymous_extension_counts":dict(sorted(types.items())),
        "official_file_metadata_MD5_fields_count":with_md5,
        "official_file_catalog_total_reported_bytes":size_total,
        "candidate_text_csv_tsv_count":types["csv"]+types["tsv"]+types["txt"],
        "real_file_bytes_downloaded":0,
        "actual_original_human_behavior_values_read":0,
        "original_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",type=pathlib.Path,required=True)
    args=a.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R101-2023-Stallen-Original-DataverseNL-Metadata-Only/1.0","Accept":"application/json"})
        with urllib.request.build_opener(SafeRedirect()).open(req,timeout=35) as res:
            validate_url(res.geturl())
            blob=res.read(CAP+1)
        result=metadata_only(blob)
    except (ValueError,TypeError,OSError,KeyError) as exc:
        result={"research_id":"R101","phase":"A","status":"R101_E0_METADATA_SOURCE_BLOCKED",
            "safe_failure":str(exc) if isinstance(exc,GateError) else "R101_OFFICIAL_DATAVERSE_NOT_VERIFIED",
            "original_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R101_OFFICIAL_DATAVERSENL_CATALOG_METADATA_AUTHENTICATED_ONLY":
        raise SystemExit(1)

if __name__=="__main__":
    main()
