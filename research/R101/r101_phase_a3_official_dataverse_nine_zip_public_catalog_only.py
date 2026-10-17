#!/usr/bin/env python3
"""R101 A3 official metadata only: public dataset ZIP filenames and file IDs.

Never request or inspect archive payloads or participant records.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import pathlib
import re
import urllib.request

from r101_stallen_2023_original_DataverseNL_official_metadata_only import (
    URL, DOI, CAP, GateError, SafeRedirect, validate_url, metadata_only
)

FILENAME=re.compile(r"[A-Za-z0-9_.() -]{1,120}\.zip",re.I)
DESCRIPTION=re.compile(r"[A-Za-z0-9 _.,;:()/+&'?!#= -]{0,300}")
TOTAL=43631177
COUNT=9


def safe_description(x):
    if x is None or x=="":
        return None
    if not isinstance(x,str) or not DESCRIPTION.fullmatch(x):
        return None
    if "://" in x or "@" in x or ".." in x:
        return None
    return x


def public_zip_inventory(raw):
    # Validate complete publication DOI and archive-only catalog first.
    base=metadata_only(raw)
    if base["official_dataset_file_count"]!=COUNT or base["anonymous_extension_counts"]!={"zip":COUNT} or base["official_file_catalog_total_reported_bytes"]!=TOTAL:
        raise GateError("R101_A3_OFFICIAL_NINE_ZIP_UNIVERSE_MISMATCH")
    obj=json.loads(raw.decode("utf-8"))["data"]["latestVersion"]
    out=[]
    ids=set()
    for entry in obj["files"]:
        df=entry["dataFile"]
        file_id=df.get("id")
        filename=df.get("filename",entry.get("label"))
        nbytes=df["filesize"]
        if type(file_id) is not int or file_id <= 0 or file_id in ids:
            raise GateError("R101_A3_DATAFILE_ID_NOT_UNIQUE_OR_INVALID")
        ids.add(file_id)
        if not isinstance(filename,str) or not FILENAME.fullmatch(filename) or filename.startswith(".") or ".." in filename:
            raise GateError("R101_A3_PUBLIC_ZIP_FILENAME_UNSAFE")
        description=safe_description(entry.get("description",""))
        md5=df.get("md5")
        out.append({
            "official_public_filename":filename,
            "official_public_datafile_id":file_id,
            "official_reported_file_bytes":nbytes,
            "official_md5_published":md5 is not None,
            "official_public_file_description_sanitized":description,
            "description_withheld_due_to_safety": bool(entry.get("description")) and description is None,
            "raw_archive_payload_downloaded":False,
        })
    out.sort(key=lambda r:(r["official_public_filename"].lower(),r["official_public_datafile_id"]))
    return {
        "research_id":"R101","phase":"A3",
        "status":"R101_OFFICIAL_NINE_ZIP_PUBLIC_FILE_SELECTION_CATALOG_ONLY",
        "official_dataset_doi":"10.34894/EYFM5L",
        "official_file_count":len(out),
        "official_total_file_bytes":sum(r["official_reported_file_bytes"] for r in out),
        "public_file_metadata":out,
        "downloaded_original_file_payload_bytes":0,
        "accessed_original_human_action_values":False,
        "score_count_actual_human":0,
        "PESEN_v0_1":"FROZEN",
    }


def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",required=True,type=pathlib.Path)
    x=a.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R101-A3-original-public-file-inventory-no-data/1.0","Accept":"application/json"})
        with urllib.request.build_opener(SafeRedirect()).open(req,timeout=40) as r:
            validate_url(r.geturl())
            raw=r.read(CAP+1)
        result=public_zip_inventory(raw)
    except (OSError,TypeError,ValueError,KeyError) as e:
        result={"research_id":"R101","phase":"A3","status":"R101_A3_CATALOG_FAIL_CLOSED",
                "safe_failure":str(e) if isinstance(e,GateError) else "R101_A3_SOURCE_UNVERIFIED",
                "score_count_actual_human":0,"PESEN_v0_1":"FROZEN"}
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R101_OFFICIAL_NINE_ZIP_PUBLIC_FILE_SELECTION_CATALOG_ONLY":
        raise SystemExit(1)


if __name__=="__main__":
    main()
