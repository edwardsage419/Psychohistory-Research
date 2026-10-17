#!/usr/bin/env python3
"""R080 true Mendeley Data v1 ZIP byte/structure/source-code audit ONLY.

Inspect original author archive; no human/bot outcome values, node IDs,
individual timestamps, network links or row-level events leave the runner.
"""
from __future__ import annotations
import argparse,hashlib,io,json,pathlib,re,zipfile
from collections import Counter,defaultdict
from urllib.request import Request,urlopen

URL="https://data.mendeley.com/datasets/t963ktp6ft/1/files/download.zip"
MAX_COMPRESSED=200_000_000
MAX_FILE=85_000_000
MAX_ENTRIES=6000
MAX_TOTAL_UNCOMPRESSED=1_500_000_000
SAFE_TOP=re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,39}$")
SOURCE="10.17632/t963ktp6ft.1"
SOURCE_AUTHORS="Shirado & Christakis 2020, Mendeley Data v1"
KEYWORDS=("human","bot","node","edge","network","experiment","exp1","exp2",
          "choice","cooperat","period","round","treat","player","connection","link")

def read_original_zip(url=URL):
    if url!=URL:
        raise ValueError("R080_SOURCE_MUST_BE_FIXED_OFFICIAL_VERSION1_URL")
    req=Request(url,headers={
        "User-Agent":"Psychohistory-R080-64-network-source-original-v1-archive-only/1.0",
        "Accept":"application/zip,application/octet-stream,*/*"})
    with urlopen(req,timeout=95) as r:
        b=r.read(MAX_COMPRESSED+1)
        if len(b)>MAX_COMPRESSED:
            raise ValueError("R080_EXCESSIVE_ORIGINAL_ARCHIVE_BYTES")
        return b,{"http_status":r.status,"mime_type":r.headers.get("Content-Type","").split(";")[0]}

def classify_zip(path):
    normalized=path.replace("\\","/").lower()
    parts=normalized.split("/")
    ex=parts[-1].rsplit(".",1)[-1] if "." in parts[-1] else "NONE"
    if ex not in ("json","csv","tsv","r","rds","txt","pdf","md","zip","png","jpg","jpeg","xls","xlsx"):
        ex="OTHER"
    return {
        "extension":ex,
        "raw":("raw" in parts or "rawdata" in parts),
        "code":("code" in parts or "scripts" in parts or "r"==ex),
        "exp1":("exp1" in parts),
        "exp2":("exp2" in parts),
    }

def summarize_json_structure(raw:bytes):
    try:obj=json.loads(raw.decode("utf-8-sig"))
    except (UnicodeError,ValueError):return {"parses_as_json":False}
    if isinstance(obj,list):
        result={"parses_as_json":True,"root_type":"list","top_level_length":len(obj)}
        if obj and isinstance(obj[0],dict):
            result["first_record_field_names"]=[k for k in obj[0] if isinstance(k,str) and SAFE_TOP.fullmatch(k)][:65]
            result["first_record_field_value_types"]={k:type(obj[0][k]).__name__ for k in result["first_record_field_names"]}
        return result
    if isinstance(obj,dict):
        keys=[k for k in obj if isinstance(k,str) and SAFE_TOP.fullmatch(k)][:70]
        return {"parses_as_json":True,"root_type":"dict",
                "top_level_keys":keys,
                "top_level_value_types":{k:type(obj[k]).__name__ for k in keys},
                "top_level_container_cardinalities":{k:len(obj[k]) for k in keys if isinstance(obj[k],(list,dict))}}
    return {"parses_as_json":True,"root_type":type(obj).__name__}

def summarize_archive(blob):
    if not zipfile.is_zipfile(io.BytesIO(blob)):
        raise ValueError("R080_PUBLIC_DOWNLOAD_IS_NOT_VALID_ARCHIVE")
    z=zipfile.ZipFile(io.BytesIO(blob))
    files=[x for x in z.infolist() if not x.is_dir()]
    if not files or len(files)>MAX_ENTRIES or sum(x.file_size for x in files)>MAX_TOTAL_UNCOMPRESSED:
        raise ValueError("R080_ZIP_ENTRY_COUNT_OR_UNCOMPRESSED_SIZE_GUARD")
    if any(x.file_size>MAX_FILE for x in files):
        raise ValueError("R080_ZIP_SINGLE_ENTRY_TOO_LARGE")
    cats=Counter()
    by_area=defaultdict(Counter)
    hashes_for_files=[]
    for f in files:
        kind=classify_zip(f.filename)
        cats[kind["extension"]]+=1
        area="exp1" if kind["exp1"] else "exp2" if kind["exp2"] else "other"
        by_area[area][kind["extension"]]+=1
        if kind["raw"]:by_area[area]["raw_files"]+=1
        if kind["code"]:by_area[area]["code_files"]+=1
    # Do not enumerate exact filenames, which could contain experiment group IDs.
    # Select at most one eligible JSON per area, only schema keys/types, never values.
    sample={}
    for area in ("exp1","exp2","other"):
        found=next((f for f in files if classify_zip(f.filename)["extension"]=="json"
            and f.file_size<=3_000_000
            and ("exp1" if classify_zip(f.filename)["exp1"] else
                 "exp2" if classify_zip(f.filename)["exp2"] else "other")==area
             ),None)
        if found:
            raw=z.read(found)
            sample[area]=summarize_json_structure(raw)
            sample[area]["sample_file_sha256"]=hashlib.sha256(raw).hexdigest()
            sample[area]["sample_file_size"]=len(raw)
    # Non-record source code semantics hints only, no executable content or raw rows.
    for f in files:
        kind=classify_zip(f.filename)
        if kind["extension"] not in ("r","txt") or f.file_size>350_000:continue
        data=z.read(f)
        source=data.decode("utf-8",errors="replace").lower()
        if kind["extension"]=="r":
            hashes_for_files.append({
             "extension":"r","bytes":f.file_size,
             "original_R_script_sha256":hashlib.sha256(data).hexdigest(),
             "research_keywords_present":[w for w in KEYWORDS if w in source]
            })
    return {
        "original_zip_bytes":len(blob),"original_zip_sha256":hashlib.sha256(blob).hexdigest(),
        "official_v1_source":URL,
        "total_archive_files":len(files),
        "total_declared_uncompressed_bytes":sum(x.file_size for x in files),
        "file_extension_count":dict(sorted(cats.items())),
        "experiment_area_file_types":{k:dict(sorted(v.items())) for k,v in sorted(by_area.items())},
        "sanitized_one_per_area_JSON_schema_without_values":sample,
        "original_author_R_script_digest_and_topic_hints":hashes_for_files[:25],
        "has_exp1_raw_JSON":by_area["exp1"]["json"]>0 and by_area["exp1"]["raw_files"]>0,
        "has_exp2_raw_JSON":by_area["exp2"]["json"]>0 and by_area["exp2"]["raw_files"]>0,
        "real_human_action_rows_scored":0,
        "original_human_node_types_independently_mapped":False,
        "original_network_edges_and_partner_timings_independently_mapped":False,
        "human_64_networks_recounted":False,
        "first_real_model_or_network_scores":"NOT_RUN",
        "raw_participant_ids_or_actions_exported":False
    }
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    a=p.parse_args()
    try:
        blob,http=read_original_zip()
        result={"research_id":"R080",
            "status":"R080_ORIGINAL_AUTHOR_V1_ARCHIVE_BYTES_CONFIRMED_SCHEMA_ONLY",
            "publisher_DOI":SOURCE,
            "original_authors":SOURCE_AUTHORS,"download":http,
            "raw_source_access":summarize_archive(blob)}
    except (OSError,ValueError,zipfile.BadZipFile) as e:
        result={"research_id":"R080","status":"R080_ORIGINAL_ZIP_SOURCE_ACCESS_FAIL_CLOSED",
           "publisher_DOI":SOURCE,"failure_class":type(e).__name__,
           "failure_detail":str(e)[:100] if isinstance(e,ValueError) else "NETWORK_OR_BINARY_ERROR",
           "real_human_action_rows_scored":0}
    result["PESEN_v0.1"]="FROZEN"
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
       "research_id":"R080","status":result["status"],
       "failure":result.get("failure_detail"),
       "zip_sha256":result.get("raw_source_access",{}).get("original_zip_sha256"),
       "archive_files":result.get("raw_source_access",{}).get("total_archive_files"),
       "experiment_areas":result.get("raw_source_access",{}).get("experiment_area_file_types"),
       "one_per_area_structure":result.get("raw_source_access",{}).get("sanitized_one_per_area_JSON_schema_without_values"),
       "real_human_models":"NOT_RUN"
    },sort_keys=True))
if __name__=="__main__":main()
