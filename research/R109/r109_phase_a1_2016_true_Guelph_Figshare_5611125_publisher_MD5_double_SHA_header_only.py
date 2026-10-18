#!/usr/bin/env python3
"""R109 A1 original 2016 Guelph human PD: publisher MD5 source, header ONLY."""
from __future__ import annotations
import argparse,csv,hashlib,io,json,pathlib,urllib.parse,urllib.request,urllib.error

ARTICLE=3545937
FILE=5611125
NAME="Barclay_Raihani_data supplement.csv"
PUBLISHED_SIZE=13127
PUBLISHED_MD5="86970b375515176e299686b1b6f70310"
META=f"https://api.figshare.com/v2/articles/{ARTICLE}"
ORIGINAL=f"https://ndownloader.figshare.com/files/{FILE}"
DELEGATE="s3-eu-west-1.amazonaws.com"
CAP=131072
class SourceError(ValueError):pass
def exact_meta(u):
    p=urllib.parse.urlsplit(u)
    if (p.scheme,p.netloc,p.path,p.query,p.fragment)!=("https","api.figshare.com",f"/v2/articles/{ARTICLE}","",""):
        raise SourceError("R109_A1_ORIGINAL_PUBLISHER_ARTICLE_API_NOT_PINNED")
def exact_downloader(u):
    p=urllib.parse.urlsplit(u)
    if (p.scheme,p.netloc,p.path,p.query,p.fragment)!=("https","ndownloader.figshare.com",f"/files/{FILE}","",""):
        raise SourceError("R109_A1_ORIGINAL_PUBLISHER_FILE_URL_NOT_PINNED")
def approved_final(u):
    p=urllib.parse.urlsplit(u)
    if p.scheme!="https" or p.username or p.password or p.fragment or p.port not in (None,443):
        raise SourceError("R109_A1_DELEGATED_FINAL_SOURCE_URL_UNTRUSTED")
    if (p.hostname,p.path,p.query) == ("ndownloader.figshare.com",f"/files/{FILE}",""):
        return "figshare_direct"
    if p.hostname==DELEGATE and p.path.startswith("/"):
        return "verified_figshare_s3_delegate"
    raise SourceError("R109_A1_FINAL_SOURCE_NOT_PREAPPROVED_DELEGATE")
class NoMetadataRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        raise SourceError("R109_A1_METADATA_UNEXPECTED_REDIRECT")
class OnePublisherDelegate(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if req.full_url!=ORIGINAL:
            raise SourceError("R109_A1_ORIGINAL_SOURCE_SECOND_REDIRECT_NOT_ALLOWED")
        if approved_final(newurl)!="verified_figshare_s3_delegate":
            raise SourceError("R109_A1_ORIGINAL_SOURCE_REDIRECT_NOT_EXACT_S3_HOST")
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def official_metadata_accept(obj):
    if not isinstance(obj,dict) or obj.get("id")!=ARTICLE or not isinstance(obj.get("files"),list):
        raise SourceError("R109_A1_PUBLISHER_ARTICLE_ID_NOT_AUTHENTIC")
    matches=[z for z in obj["files"] if isinstance(z,dict) and z.get("id")==FILE]
    if len(matches)!=1:raise SourceError("R109_A1_ORIGINAL_FILE_ID_DUPLICATED_OR_ABSENT")
    z=matches[0]
    if (z.get("name")!=NAME or z.get("size")!=PUBLISHED_SIZE
        or z.get("computed_md5","").lower()!=PUBLISHED_MD5 or z.get("download_url")!=ORIGINAL):
        raise SourceError("R109_A1_PUBLISHER_SOURCE_MD5_BYTES_NAME_DOWNLOAD_NOT_MATCHED")
    exact_downloader(z["download_url"])
    return True

def source_header_only(raw):
    if type(raw) is not bytes or len(raw)!=PUBLISHED_SIZE or len(raw)>CAP:
        raise SourceError("R109_A1_PUBLISHER_FULL_CSV_BYTE_COUNT_NOT_MATCHED")
    if hashlib.md5(raw).hexdigest()!=PUBLISHED_MD5:
        raise SourceError("R109_A1_PUBLISHER_MD5_FULL_FILE_NOT_MATCHED")
    if b"\x00" in raw or raw.lstrip()[:120].lower().startswith((b"<html",b"<!doctype",b"<?xml",b"{",b"[")):
        raise SourceError("R109_A1_ORIGINAL_NOT_BOUNDED_PLAIN_CSV")
    first,found,_=raw.partition(b"\n")
    if not found or len(first)>12288:raise SourceError("R109_A1_CSV_HEADER_TOO_LONG_OR_MISSING")
    try:
        header=next(csv.reader([first.rstrip(b"\r").decode("utf-8-sig")],strict=True))
    except (UnicodeError,csv.Error,StopIteration) as exc:
        raise SourceError("R109_A1_HEADER_NOT_VALID_UTF8_CSV") from exc
    if not 2<=len(header)<=150:raise SourceError("R109_A1_HEADER_COLUMN_COUNT_UNTRUSTED")
    lines=raw.count(b"\n")-1 if raw.endswith(b"\n") else raw.count(b"\n")
    if not 1<=lines<=500000:raise SourceError("R109_A1_CSV_BODY_PHYSICAL_ROWS_UNTRUSTED")
    return {
        "research_id":"R109","phase":"A1",
        "status":"R109_A1_TRUE_2016_FIGSHARE_ORIGINAL_PUBLISHED_MD5_DOUBLE_SHA_E1_HEADER_ONLY",
        "source_Figshare_article_ID":ARTICLE,
        "source_Figshare_file_ID":FILE,
        "publisher_MD5_full_original_verified":PUBLISHED_MD5,
        "published_full_original_csv_bytes":len(raw),
        "computed_complete_original_SHA256":hashlib.sha256(raw).hexdigest(),
        "header_column_count_no_original_header_labels_exported":len(header),
        "anonymous_header_empty_name_count":sum(not x.strip() for x in header),
        "anonymous_header_duplicate_name_count":len(header)-len(set(header)),
        "anonymous_header_nonASCII_or_control_name_count":sum(any(ord(c)<32 or ord(c)>126 for c in x) for x in header),
        "CSV_physical_data_lines_unparsed":lines,
        "original_source_human_actor_partner_action_cells_accessed":False,
        "real_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def two_authenticated_originals(first,second):
    one=source_header_only(first);other=source_header_only(second)
    if first!=second or one["computed_complete_original_SHA256"]!=other["computed_complete_original_SHA256"]:
        raise SourceError("R109_A1_TWO_INDEPENDENT_FIRSTPARTY_DOWNLOADS_NOT_EQUAL")
    one["two_official_full_original_downloads_identical"]=True
    return one

def get_author_original():
    exact_downloader(ORIGINAL)
    req=urllib.request.Request(ORIGINAL,headers={"User-Agent":"Psychohistory-R109-2016-Official-Guelph-MD5-Firstparty/1.0","Accept":"text/csv,application/octet-stream"})
    try:
        with urllib.request.build_opener(OnePublisherDelegate()).open(req,timeout=55) as res:
            if res.status!=200:raise SourceError("R109_A1_REAL_DOWNLOADER_NON200")
            approved_final(res.geturl())
            return res.read(CAP+1)
    except urllib.error.HTTPError as exc:
        if exc.code in (401,403,404):
            raise SourceError("R109_A1_FIRSTPARTY_SOURCE_HTTP_"+str(exc.code)) from exc
        raise SourceError("R109_A1_FIRSTPARTY_SOURCE_HTTP_ERROR") from exc

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=pathlib.Path,required=True)
    args=ap.parse_args()
    try:
        exact_meta(META)
        meta_req=urllib.request.Request(META,headers={"User-Agent":"Psychohistory-R109-Firstparty-Official-Article-Metadata/1.0","Accept":"application/json"})
        with urllib.request.build_opener(NoMetadataRedirect()).open(meta_req,timeout=45) as res:
            exact_meta(res.geturl())
            rawmeta=res.read(262145)
        if len(rawmeta)>262144:raise SourceError("R109_A1_PUBLISHER_FILE_METADATA_TOO_LARGE")
        official_metadata_accept(json.loads(rawmeta.decode("utf-8")))
        result=two_authenticated_originals(get_author_original(),get_author_original())
    except (ValueError,OSError,TypeError,KeyError,UnicodeError,csv.Error) as e:
        result={"research_id":"R109","phase":"A1",
                "status":"R109_A1_GENUINE_ORIGINAL_PUBLISHED_SOURCE_FAIL_CLOSED",
                "safe_failure":str(e) if isinstance(e,SourceError) else "R109_A1_FIRSTPARTY_ORIGINAL_SOURCE_UNVERIFIED",
                "real_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R109_A1_TRUE_2016_FIGSHARE_ORIGINAL_PUBLISHED_MD5_DOUBLE_SHA_E1_HEADER_ONLY":
        raise SystemExit(1)
if __name__=="__main__":main()
