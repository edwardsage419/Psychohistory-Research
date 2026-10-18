#!/usr/bin/env python3
"""R107 A2: two official Dryad PUBLIC JSON metadata requests only, never CSV."""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import urllib.parse
import urllib.request
import urllib.error

ROOT="https://datadryad.org"
PATHS=("/api/v2/datasets/doi%3A10.5061%2Fdryad.7fq25s8",
       "/api/v2/files/296893")
CAP=262144
class SourceError(ValueError):pass
def validate_url(u):
    p=urllib.parse.urlsplit(u)
    if p.scheme!="https" or p.netloc!="datadryad.org" or p.path not in PATHS or p.query or p.fragment:
        raise SourceError("R107_A2_UNAPPROVED_OFFICIAL_METADATA_URL")

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise SourceError("R107_A2_OFFICIAL_METADATA_REDIRECT_NOT_AUTHORIZED")

def digest_fields(x):
    if not isinstance(x,dict):return {}
    name=x.get("digestType")
    dig=x.get("digest")
    if not isinstance(name,str) or not isinstance(dig,str):return {}
    name=name.lower()
    if name=="md5" and re.fullmatch(r"[a-fA-F0-9]{32}",dig):
        return {"published_digest_algorithm":"md5","publisher_reported_unverified_digest":dig.lower()}
    if name in ("sha256","sha-256") and re.fullmatch(r"[a-fA-F0-9]{64}",dig):
        return {"published_digest_algorithm":"sha256","publisher_reported_unverified_digest":dig.lower()}
    return {}

def clean_api_response(path,http_code,object_or_none):
    tag="dataset" if path==PATHS[0] else "file"
    meta=object_or_none if isinstance(object_or_none,dict) else {}
    filename=meta.get("path")
    size=meta.get("size")
    identifier=meta.get("identifier")
    # Metadata external links are not followed; do not export raw URLs.
    links=meta.get("_links")
    official_path_metadata=False
    if isinstance(links,dict):
        for v in links.values():
            if not isinstance(v,dict):continue
            href=v.get("href")
            if not isinstance(href,str):continue
            pathpart=urllib.parse.urlsplit(href).path
            if pathpart in ("/downloads/file_stream/296893","/api/v2/files/296893/download"):
                official_path_metadata=True
    row={
        "source_kind":tag,
        "public_api_http_code":http_code,
        "public_api_response_is_json_object":isinstance(object_or_none,dict),
        "official_dataset_identifier_exact_match":identifier in ("doi:10.5061/dryad.7fq25s8","10.5061/dryad.7fq25s8"),
        "official_file_name_exact_match":filename=="DataSet.csv",
        "official_file_size_if_published":size if type(size) is int and 0<size<=100000000 else None,
        "published_file_download_exact_official_link_metadata_present":official_path_metadata,
    }
    if tag=="file":
        row.update(digest_fields(meta))
    return row

def get(path):
    validate_url(ROOT+path)
    req=urllib.request.Request(ROOT+path,headers={
        "User-Agent":"Psychohistory-R107-Official-Dryad-API-Metadata-Only/1.0",
        "Accept":"application/json"})
    try:
        with urllib.request.build_opener(NoRedirect()).open(req,timeout=35) as response:
            if response.status!=200:
                return clean_api_response(path,response.status,None)
            data=response.read(CAP+1)
            if len(data)>CAP:return clean_api_response(path,413,None)
            try:
                obj=json.loads(data.decode("utf-8"))
            except (ValueError,UnicodeError):
                obj=None
            return clean_api_response(path,200,obj)
    except urllib.error.HTTPError as e:
        return clean_api_response(path,e.code,None)
    except (OSError,ValueError) as e:
        return clean_api_response(path,0,None)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    x=p.parse_args()
    report={
        "research_id":"R107","phase":"A2",
        "status":"R107_A2_DRYAD_PUBLIC_API_METADATA_ONLY_SOURCE_E1_UNESTABLISHED",
        "source_dataset_DOI":"10.5061/dryad.7fq25s8",
        "official_file_stream_initial_human_free_403":True,
        "public_metadata_endpoint_results":[get(p) for p in PATHS],
        "human_original_CSV_payload_bytes_downloaded_or_read":0,
        "actual_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(report,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(report,sort_keys=True))
if __name__=="__main__":main()
