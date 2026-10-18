#!/usr/bin/env python3
"""R109 A0: exact 2016 publisher Figshare original research file CATALOG ONLY."""
from __future__ import annotations
import argparse,json,pathlib,re,urllib.request,urllib.parse,urllib.error

URL="https://api.figshare.com/v2/articles/3545937"
CAP=262144
EXT=(".csv",".xlsx",".xls",".dta",".zip",".txt",".pdf",".rds",".sav",".rdata")
SAFE_NAME=re.compile(r"[A-Za-z0-9_. ()'\-]{1,160}")
MD5=re.compile(r"[0-9a-fA-F]{32}")
class SourceError(ValueError):pass
def exact_publisher_url(u):
    p=urllib.parse.urlsplit(u)
    if (p.scheme,p.netloc,p.path,p.query,p.fragment)!=("https","api.figshare.com","/v2/articles/3545937","",""):
        raise SourceError("R109_A0_FIGSHARE_ORIGINAL_PUBLISHER_API_NOT_PINNED")

class RefuseRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise SourceError("R109_A0_PUBLISHER_API_UNEXPECTED_REDIRECT")

def source_catalog_only(metadata):
    if not isinstance(metadata,dict) or metadata.get("id")!=3545937:
        raise SourceError("R109_A0_PUBLISHER_ARTICLE_ID_MISMATCH")
    files=metadata.get("files")
    if not isinstance(files,list) or not 1<=len(files)<=40:
        raise SourceError("R109_A0_PUBLISHER_FILE_UNIVERSE_NOT_BOUNDED")
    out=[]
    for f in files:
        if not isinstance(f,dict):raise SourceError("R109_A0_SOURCE_FILE_METADATA_NOT_OBJECT")
        name=f.get("name")
        if not isinstance(name,str) or not SAFE_NAME.fullmatch(name):
            raise SourceError("R109_A0_UNSAFE_PUBLIC_SOURCE_FILENAME")
        if not name.lower().endswith(EXT):continue
        i=f.get("id");n=f.get("size")
        if type(i) is not int or not 1<=i<=2000000000 or type(n) is not int or not 100<=n<=100000000:
            raise SourceError("R109_A0_SOURCE_FILE_ID_OR_BYTE_BOUND_INVALID")
        res={"original_publisher_file_ID":i,"original_public_filename":name,
             "published_original_source_bytes":n,"file_extension":name.rsplit(".",1)[-1].lower()}
        for field in ("computed_md5","supplied_md5"):
            val=f.get(field)
            if isinstance(val,str) and MD5.fullmatch(val):
                res["published_original_MD5_field"]=field
                res["published_original_MD5_unverified_against_source"]=val.lower()
                break
        out.append(res)
    if not any(z["file_extension"] not in ("pdf","txt") for z in out):
        raise SourceError("R109_A0_NO_MACHINE_READABLE_BEHAVIOR_DATA_SOURCE_IN_CATALOG")
    return {
        "research_id":"R109","phase":"A0",
        "status":"R109_A0_OFFICIAL_2016_FIGSHARE_ORIGINAL_SOURCE_FILES_METADATA_ONLY",
        "publisher_article_ID":3545937,
        "reported_study_original_humans_from_paper_unverified_in_file":156,
        "official_record_file_count":len(files),
        "allowlisted_publisher_source_files_meta_only":out,
        "original_human_action_or_pair_rows_accessed":False,
        "actual_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        exact_publisher_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R109-2016-Official-Figshare-Publisher-MetaOnly/1.0","Accept":"application/json"})
        with urllib.request.build_opener(RefuseRedirect()).open(req,timeout=50) as response:
            exact_publisher_url(response.geturl())
            if response.status!=200:raise SourceError("R109_A0_PUBLISHER_HTTP_NOT_200")
            raw=response.read(CAP+1)
        if len(raw)>CAP:raise SourceError("R109_A0_PUBLISHER_METADATA_TOO_LARGE")
        result=source_catalog_only(json.loads(raw.decode("utf-8")))
    except (OSError,ValueError,TypeError,KeyError,UnicodeError) as exc:
        result={"research_id":"R109","phase":"A0",
                "status":"R109_A0_ORIGINAL_PUBLISHER_CATALOG_FAIL_CLOSED",
                "safe_failure":str(exc) if isinstance(exc,SourceError) else "R109_A0_ORIGINAL_PUBLISHER_UNVERIFIED",
                "actual_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R109_A0_OFFICIAL_2016_FIGSHARE_ORIGINAL_SOURCE_FILES_METADATA_ONLY":
        raise SystemExit(1)
if __name__=="__main__":main()
