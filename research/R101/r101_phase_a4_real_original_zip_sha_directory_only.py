#!/usr/bin/env python3
"""R101 A4: exact official raw ZIP twice, full SHA equality, central directory only.

No archive member content is opened, extracted, printed, or parsed.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import io
import json
import pathlib
import urllib.parse
import urllib.request
import zipfile

OFFICIAL_ID=383977
OFFICIAL_NAME="3. Raw data files.zip"
OFFICIAL_BYTES=2247187
URL=f"https://dataverse.nl/api/access/datafile/{OFFICIAL_ID}"
CAP=OFFICIAL_BYTES+1
MAX_MEMBERS=300
MAX_UNCOMPRESSED=64*1024*1024
MAX_ONE=32*1024*1024
ALLOWED_EXT={"csv","tsv","txt","json","zip","xls","xlsx","dta","sav","rds","rdata","dat","r","rmd","do","pdf","doc","docx","md","py","html","xml","png","jpg","jpeg","other","none"}

class ArchiveGateError(ValueError):
    pass

def validate_source_url(url):
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or p.hostname!="dataverse.nl" or p.netloc!="dataverse.nl" or p.path!=f"/api/access/datafile/{OFFICIAL_ID}" or p.query or p.fragment:
        raise ArchiveGateError("R101_A4_OFFICIAL_FILE_ENDPOINT_NOT_PINNED")

class RejectExternalRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_source_url(newurl)
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def verified_identity(b):
    if type(b) is not bytes or len(b)!=OFFICIAL_BYTES:
        raise ArchiveGateError("R101_A4_FILE_BYTE_LENGTH_DIFFERS_FROM_OFFICIAL")
    if not zipfile.is_zipfile(io.BytesIO(b)):
        raise ArchiveGateError("R101_A4_ORIGINAL_BYTES_NOT_ZIP")
    return hashlib.sha256(b).hexdigest()

def directory_only(b):
    verified_identity(b)
    try:
        with zipfile.ZipFile(io.BytesIO(b),"r") as z:
            infos=z.infolist()
            if not 1<=len(infos)<=MAX_MEMBERS:
                raise ArchiveGateError("R101_A4_ZIP_MEMBER_COUNT_INVALID")
            ext=Counter()
            total=0
            paths=set()
            roots=set()
            for item in infos:
                n=item.filename
                segments=n.split("/")
                is_dir=item.is_dir()
                parts=segments[:-1] if is_dir else segments
                if (not n or n.startswith("/") or "\\" in n or "\x00" in n
                    or any(x in ("",".","..") for x in parts)
                    or (is_dir and not n.endswith("/"))
                    or (not is_dir and not segments[-1])
                    or len(n)>240 or n in paths):
                    raise ArchiveGateError("R101_A4_UNSAFE_OR_DUPLICATE_ZIP_PATH")
                paths.add(n)
                if item.flag_bits & 0x1 or (item.external_attr >> 16)&0o170000 == 0o120000:
                    raise ArchiveGateError("R101_A4_ENCRYPTED_OR_SYMLINK_MEMBER")
                if item.compress_type not in (zipfile.ZIP_STORED,zipfile.ZIP_DEFLATED):
                    raise ArchiveGateError("R101_A4_UNSUPPORTED_COMPRESSION")
                if item.file_size>MAX_ONE or item.compress_size>OFFICIAL_BYTES or item.file_size<0:
                    raise ArchiveGateError("R101_A4_MEMBER_SIZE_LIMIT")
                if item.file_size>0 and (item.compress_size==0 or item.file_size>1000*item.compress_size):
                    raise ArchiveGateError("R101_A4_ZIP_EXPANSION_RATIO_LIMIT")
                total+=item.file_size
                if total>MAX_UNCOMPRESSED:
                    raise ArchiveGateError("R101_A4_UNCOMPRESSED_ARCHIVE_LIMIT")
                roots.add(parts[0])
                if not is_dir:
                    last=parts[-1]
                    suffix=last.rsplit(".",1)[-1].lower() if "." in last else "none"
                    if suffix not in ALLOWED_EXT:
                        suffix="other"
                    ext[suffix]+=1
            return {
                "zip_central_directory_members":len(infos),
                "anonymous_member_extension_counts":dict(sorted(ext.items())),
                "zip_declared_uncompressed_bytes":total,
                "anonymous_top_level_segment_count":len(roots),
                "candidate_csv_tsv_txt_member_count":sum(ext[x] for x in ("csv","tsv","txt")),
                "any_archive_member_content_read":False,
                "original_human_actions_accessed":False,
                "original_human_scores":0,
            }
    except (zipfile.BadZipFile,RuntimeError,EOFError) as exc:
        raise ArchiveGateError("R101_A4_ZIP_CENTRAL_DIRECTORY_UNREADABLE") from exc

def compare_two_source_copies(first,second):
    a=verified_identity(first)
    b=verified_identity(second)
    if a!=b:
        raise ArchiveGateError("R101_A4_INDEPENDENT_SOURCE_FETCH_SHA_MISMATCH")
    summary=directory_only(first)
    return {
        "research_id":"R101","phase":"A4",
        "status":"R101_ACTUAL_RAW_ZIP_FULL_BYTES_DOUBLE_SHA_AND_DIRECTORY_ONLY",
        "official_dataset_DOI":"10.34894/EYFM5L",
        "official_public_original_filename":OFFICIAL_NAME,
        "official_datafile_ID":OFFICIAL_ID,
        "official_reported_and_actual_byte_size":OFFICIAL_BYTES,
        "project_computed_full_original_SHA256":a,
        "independent_source_download_SHA256_identical":True,
        "official_publisher_file_MD5_unavailable":True,
        **summary,
        "PESEN_v0_1":"FROZEN",
    }

def original_fetch():
    validate_source_url(URL)
    req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R101-A4-Original-ZIP-Full-SHA-Directory-Only/1.0","Accept":"application/octet-stream"})
    with urllib.request.build_opener(RejectExternalRedirect()).open(req,timeout=55) as response:
        validate_source_url(response.geturl())
        if response.status!=200:
            raise ArchiveGateError("R101_A4_SOURCE_HTTP_STATUS_NOT_200")
        return response.read(CAP)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=pathlib.Path)
    x=p.parse_args()
    try:
        result=compare_two_source_copies(original_fetch(),original_fetch())
    except (ValueError,TypeError,OSError,KeyError,zipfile.BadZipFile) as exc:
        result={"research_id":"R101","phase":"A4",
                "status":"R101_A4_OFFICIAL_ZIP_SOURCE_BLOCKED",
                "safe_failure":str(exc) if isinstance(exc,ArchiveGateError) else "R101_A4_OFFICIAL_ARCHIVE_BYTES_NOT_VERIFIED",
                "original_human_scores":0,"PESEN_v0_1":"FROZEN"}
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R101_ACTUAL_RAW_ZIP_FULL_BYTES_DOUBLE_SHA_AND_DIRECTORY_ONLY":
        raise SystemExit(1)

if __name__=="__main__":
    main()
