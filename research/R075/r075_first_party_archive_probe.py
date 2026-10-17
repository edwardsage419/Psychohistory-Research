#!/usr/bin/env python3
"""R075 external original source reachability discovery, zero human model scores.

Public output contains URL reachability, content hashes, archive type and
aggregate file-type counts only. No raw human file, row or person identifier.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
import zipfile

LIMIT=30_000_000
CANDIDATES=[
  ("AUTHOR_RAND_PRIMARY_SOURCE_ZIP","https://davidrand-cooperation.com/s/slow-to-anger-and-fast-to-forgive-data-and-code.zip"),
  ("AEA_LEGACY_HTTPS","https://www.aeaweb.org/aer/data/april2012/20100629_data.zip"),
  ("AEA_LEGACY_FTP","https://ftp.aeaweb.org/aer/data/april2012/20100629_data.zip"),
  ("AEA_DATASET_PAGE","https://www.aeaweb.org/journals/dataset?id=10.1257%2Faer.102.2.720"),
  ("OPENICPSR_ARCHIVE_VIEW","https://www.openicpsr.org/openicpsr/project/112512/version/V1/view"),
  ("OPENICPSR_STUDY_DOWNLOAD","https://www.openicpsr.org/openicpsr/project/112512/version/V1/download"),
  ("MAO_2017_OSF_PUBLIC_FILES_API","https://api.osf.io/v2/nodes/64z8u/files/"),
  ("MAO_2017_OSF_PROJECT","https://osf.io/64z8u/"),
]

def summarize_archive(data):
    if not zipfile.is_zipfile(io.BytesIO(data)):
        return {"is_zip":False}
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        infos=z.infolist()
        if len(infos)>5000:
            raise ValueError("TOO_MANY_ARCHIVE_MEMBERS")
        if any(x.file_size>50_000_000 or x.flag_bits&1 for x in infos):
            raise ValueError("OVERSIZE_OR_ENCRYPTED_ZIP_MEMBER")
        if sum(x.file_size for x in infos)>120_000_000:
            raise ValueError("ZIP_BOMB_TOTAL_EXCEEDED")
        ext=Counter()
        for x in infos:
            if x.is_dir():continue
            name=x.filename.rsplit("/",1)[-1].lower()
            ext["."+name.rsplit(".",1)[-1] if "." in name else "<no_extension>"]+=1
        # The filenames themselves can carry participant or session codes;
        # only extension histogram and total anonymous dimensions are public.
        return {
            "is_zip":True, "members":len(infos),
            "uncompressed_bytes":sum(x.file_size for x in infos),
            "extension_counts":dict(sorted(ext.items())),
            "zip_testzip_bad_member_present": z.testzip() is not None,
        }


def official_data_links(body, base_url):
    """Recover public archive/navigation links from an official landing page only."""
    from html.parser import HTMLParser
    from urllib.parse import urljoin,urlparse,parse_qsl
    class Anchors(HTMLParser):
        def __init__(self):
            super().__init__()
            self.hrefs=[]
        def handle_starttag(self,tag,attrs):
            if tag not in ("a","form"):return
            d=dict(attrs)
            href=d.get("href") or d.get("action") or ""
            if href:self.hrefs.append(href)
    p=Anchors()
    p.feed(body.decode("utf-8","replace")[:1_000_000])
    allowed={"aeaweb.org","www.aeaweb.org","ftp.aeaweb.org",
             "openicpsr.org","www.openicpsr.org","icpsr.umich.edu","www.icpsr.umich.edu"}
    output=[]
    for relative in p.hrefs:
        full=urljoin(base_url,relative)
        url=urlparse(full)
        if url.scheme!="https" or url.hostname not in allowed:continue
        keys=[k.lower() for k,v in parse_qsl(url.query)]
        if any(any(secret in key for secret in ("token","auth","signature","secret","key","session"))
               for key in keys):continue
        searchable=(url.path+"?"+url.query).lower()
        if not any(v in searchable for v in ("download","dataset","20100629","112512","replication","content/file")):
            continue
        if full not in output:output.append(full)
    return output[:12]

def probe_one(label,url,reader=None):
    result={"candidate":label,"url":url,"source_kind":"official_or_original_archive_endpoint"}
    def perform():
        req=urllib.request.Request(url,headers={
            "User-Agent":"Psychohistory-R075-source-availability/1.0",
            "Accept":"application/zip,application/octet-stream,text/html,*/*"
        })
        with urllib.request.urlopen(req,timeout=18) as response:
            status=response.status
            ct=response.headers.get("Content-Type","").split(";")[0].lower()
            body=response.read(LIMIT+1)
            target=response.url
        return status,ct,body,target
    try:
        status,content_type,body,target=(reader or perform)()
        result.update({"http_status":status,"content_type":content_type,
                       "response_bytes":len(body),
                       "sha256":hashlib.sha256(body).hexdigest(),
                       "redirect_final_host":urllib.parse.urlparse(target).hostname})
        if len(body)>LIMIT:
            result.update({"status":"BLOCKED_RESPONSE_TOO_LARGE"})
        elif not body:
            result.update({"status":"EMPTY_RESPONSE"})
        else:
            summary=summarize_archive(body)
            result["archive"]=summary
            if summary["is_zip"] and not summary["zip_testzip_bad_member_present"]:
                result["status"]="ZIP_STRUCTURALLY_ACCESSIBLE_ORIGIN_BYTE_HASHED"
            elif "html" in content_type or body[:20].lower().find(b"<html")>=0:
                result["status"]="HTML_NOT_RAW_ARCHIVE"
                result["official_document_links"]=official_data_links(body,target)
            else:
                result["status"]="REACHABLE_NON_ARCHIVE"
    except urllib.error.HTTPError as e:
        result.update({"http_status":e.code,"status":"HTTP_FAILURE"})
    except urllib.error.URLError as e:
        result.update({"status":"NETWORK_FAILURE","error_type":type(e.reason).__name__})
    except (ValueError,zipfile.BadZipFile,RuntimeError) as e:
        result.update({"status":"ARCHIVE_VALIDATION_FAILURE",
                       "error_type":type(e).__name__})
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    observations=[probe_one(label,url) for label,url in CANDIDATES]
    result={
      "research_id":"R075",
      "stage":"THIRD_EXTERNAL_SOURCE_DISCOVERY_ONLY",
      "source_candidates":observations,
      "original_experiment_full_session_schema":"NOT_YET_VERIFIED",
      "original_intention_vs_realized_noise":"NOT_YET_VERIFIED",
      "real_human_model_scoring":"NOT_RUN",
      "individual_rows_exported":False,
      "R075_E3":"OPEN",
      "PESEN_v0.1":"FROZEN",
    }
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    # Reachability is best effort. Blocked access is a legitimate negative result.
if __name__=="__main__":
    main()
