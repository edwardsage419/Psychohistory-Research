#!/usr/bin/env python3
"""R108 A0: Leicester university Figshare 10194938 publisher file META ONLY."""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import urllib.parse
import urllib.request
import urllib.error

URL="https://api.figshare.com/v2/articles/10194938"
CAP=262144
SAFE_FILENAME=re.compile(r"[A-Za-z0-9_. ()'\-]{1,120}")
HEX32=re.compile(r"[a-fA-F0-9]{32}")
class SourceError(ValueError): pass

def safe_url(u):
    p=urllib.parse.urlsplit(u)
    if (p.scheme,p.netloc,p.path,p.query,p.fragment)!=("https","api.figshare.com","/v2/articles/10194938","",""):
        raise SourceError("R108_A0_ORIGINAL_UK_FIGSHARE_METADATA_URL_UNTRUSTED")

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise SourceError("R108_A0_ORIGINAL_METADATA_REDIRECT_UNAPPROVED")

def valid_digest(item):
    for key in ("computed_md5","supplied_md5"):
        digest=item.get(key)
        if isinstance(digest,str) and HEX32.fullmatch(digest):
            return {"original_publisher_MD5_field":key,"original_publisher_reported_MD5_not_yet_verified":digest.lower()}
    return {}

def sanitize_publisher_metadata(obj):
    if not isinstance(obj,dict) or obj.get("id")!=10194938:
        raise SourceError("R108_A0_PUBLISHER_ARTICLE_ID_UNMATCHED")
    files=obj.get("files")
    if not isinstance(files,list) or not 1<=len(files)<=30:
        raise SourceError("R108_A0_PUBLISHER_ARTICLE_FILE_LIST_INVALID")
    out=[]
    for f in files:
        if not isinstance(f,dict):
            raise SourceError("R108_A0_PUBLISHER_FILE_METADATA_NOT_OBJECT")
        name=f.get("name")
        if not isinstance(name,str) or SAFE_FILENAME.fullmatch(name) is None:
            raise SourceError("R108_A0_ORIGINAL_FILE_NAME_NOT_SAFE_METADATA")
        if not name.lower().endswith((".csv",".pdf")):
            continue
        fid=f.get("id")
        size=f.get("size")
        if type(fid) is not int or not 1<=fid<=1000000000 or type(size) is not int or not 100<=size<=100000000:
            raise SourceError("R108_A0_ORIGINAL_FILE_ID_OR_SIZE_UNVERIFIED")
        entry={"original_file_ID":fid,"original_file_name":name,"publisher_file_bytes":size,
               "source_kind":"CSV" if name.lower().endswith(".csv") else "PDF"}
        if entry["source_kind"]=="CSV":
            entry.update(valid_digest(f))
        out.append(entry)
    if not any(e["source_kind"]=="CSV" for e in out):
        raise SourceError("R108_A0_AUTHOR_ORIGINAL_CSV_NOT_LISTED")
    return {
        "research_id":"R108","phase":"A0",
        "status":"R108_A0_TRUE_UK_FIGSHARE_2017_SOURCE_FILE_METADATA_ONLY",
        "publisher_article_ID":10194938,
        "original_dataset_page":"https://figshare.le.ac.uk/articles/dataset/Repeated_Prisoner_s_Dilemma_Dataset/10194938",
        "official_file_count":len(files),
        "source_publishable_sanitized_file_metadata":out,
        "original_csv_entire_bytes_downloaded":False,
        "original_human_person_round_action_values_accessed":False,
        "actual_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def run():
    safe_url(URL)
    req=urllib.request.Request(URL,headers={
        "User-Agent":"Psychohistory-R108-2017-Leicester-Official-Source-Files-Metadata-Only/1.0",
        "Accept":"application/json"})
    try:
        with urllib.request.build_opener(NoRedirect()).open(req,timeout=45) as resp:
            safe_url(resp.geturl())
            raw=resp.read(CAP+1)
            if len(raw)>CAP:raise SourceError("R108_A0_PUBLISHER_FILE_METADATA_TOO_LARGE")
            return sanitize_publisher_metadata(json.loads(raw.decode("utf-8")))
    except urllib.error.HTTPError as e:
        if e.code in (401,403,404):
            raise SourceError("R108_A0_FIGSHARE_OFFICIAL_API_HTTP_"+str(e.code)) from e
        raise SourceError("R108_A0_FIGSHARE_OFFICIAL_API_HTTP_FAILURE") from e

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:result=run()
    except (ValueError,TypeError,KeyError,OSError,UnicodeError) as exc:
        result={
            "research_id":"R108","phase":"A0",
            "status":"R108_A0_FIRSTPARTY_FIGSHARE_METADATA_FAIL_CLOSED",
            "safe_failure":str(exc) if isinstance(exc,SourceError) else "R108_A0_ORIGINAL_ARTICLE_SOURCE_UNVERIFIED",
            "actual_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R108_A0_TRUE_UK_FIGSHARE_2017_SOURCE_FILE_METADATA_ONLY":
        raise SystemExit(1)

if __name__=="__main__":main()
