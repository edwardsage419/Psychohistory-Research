#!/usr/bin/env python3
"""R101 A6: double official Dataverse -> SURF signed-S3 delivery, raw ZIP directory only.

Never log ephemeral signed URLs, credentials, tokens, or ZIP member contents.
"""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import urllib.parse
import urllib.request

from r101_phase_a4_real_original_zip_sha_directory_only import (
    URL, CAP, OFFICIAL_BYTES, ArchiveGateError, compare_two_source_copies,
    validate_source_url,
)

TARGET="objectstore.surf.nl"
QUERY_KEYS={
    "X-Amz-Algorithm","X-Amz-Credential","X-Amz-Date","X-Amz-Expires",
    "X-Amz-Signature","X-Amz-SignedHeaders",
    "response-content-disposition","response-content-type",
}

def validate_signed_target(newurl):
    if not isinstance(newurl,str) or len(newurl)>8192:
        raise ArchiveGateError("R101_A6_SIGNED_URL_SIZE_INVALID")
    p=urllib.parse.urlsplit(newurl)
    if (p.scheme!="https" or p.netloc!=TARGET or p.username or p.password
        or p.port is not None or p.fragment):
        raise ArchiveGateError("R101_A6_OFFICIAL_SURF_HOST_NOT_PINNED")
    segments=p.path.split("/")
    if len(segments)!=5 or segments[0]!="" or segments[1]!="store" or any(not x or x in (".","..") for x in segments[1:]):
        raise ArchiveGateError("R101_A6_SURF_OBJECT_PATH_SHAPE_UNVERIFIED")
    if "\\" in p.path or "\x00" in p.path or len(p.path)>2048:
        raise ArchiveGateError("R101_A6_SURF_OBJECT_PATH_UNSAFE")
    try:
        vals=urllib.parse.parse_qs(p.query,keep_blank_values=True,strict_parsing=True,max_num_fields=16)
    except ValueError as exc:
        raise ArchiveGateError("R101_A6_SIGNED_QUERY_PARSE_FAILED") from exc
    if set(vals)!=QUERY_KEYS or any(len(z)!=1 for z in vals.values()):
        raise ArchiveGateError("R101_A6_SIGNED_QUERY_KEYS_NOT_WHITELISTED")
    if vals["X-Amz-Algorithm"][0]!="AWS4-HMAC-SHA256":
        raise ArchiveGateError("R101_A6_SIGNED_ALGORITHM_NOT_VERIFIED")
    if not re.fullmatch(r"[A-Fa-f0-9]{64}",vals["X-Amz-Signature"][0]):
        raise ArchiveGateError("R101_A6_SIGNATURE_SHAPE_INVALID")
    if not re.fullmatch(r"[0-9]{8}T[0-9]{6}Z",vals["X-Amz-Date"][0]):
        raise ArchiveGateError("R101_A6_DATE_SHAPE_INVALID")
    expiry=vals["X-Amz-Expires"][0]
    if not expiry.isascii() or not expiry.isdecimal() or not 1<=int(expiry)<=604800:
        raise ArchiveGateError("R101_A6_SIGNED_EXPIRATION_INVALID")
    if not 1<=len(vals["X-Amz-Credential"][0])<=400:
        raise ArchiveGateError("R101_A6_SIGNED_CREDENTIAL_FORMAT_INVALID")
    return True

class OneExactPublisherRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self):
        super().__init__()
        self.count=0

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if req.full_url != URL or self.count != 0 or code != 303:
            raise ArchiveGateError("R101_A6_MULTIPLE_OR_NONPUBLISHER_REDIRECT_REJECTED")
        validate_signed_target(newurl)
        self.count+=1
        return super().redirect_request(req,fp,code,msg,headers,newurl)

def original_signed_fetch():
    validate_source_url(URL)
    req=urllib.request.Request(URL,headers={
        "User-Agent":"Psychohistory-R101-A6-DataverseNL-SURF-Exact-2MB-Original-ZIP-SHA/1.0",
        "Accept":"application/octet-stream",
    })
    opener=urllib.request.build_opener(OneExactPublisherRedirect())
    with opener.open(req,timeout=65) as response:
        if response.status!=200 or urllib.parse.urlsplit(response.geturl()).hostname != TARGET:
            raise ArchiveGateError("R101_A6_ORIGINAL_SURF_PAYLOAD_FINAL_HOST_NOT_VERIFIED")
        b=response.read(CAP)
    if len(b)!=OFFICIAL_BYTES:
        raise ArchiveGateError("R101_A6_OFFICIAL_ZIP_BYTE_SIZE_MISMATCH")
    return b

def audit():
    return compare_two_source_copies(original_signed_fetch(),original_signed_fetch())

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    x=p.parse_args()
    try:
        result=audit()
        result["phase"]="A6"
        result["status"]="R101_A6_REAL_ORIGINAL_SURF_DELIVERED_RAW_ZIP_DOUBLE_SHA_DIRECTORY_ONLY"
        result["publisher_delivery_verified"]="DataverseNL_HTTP303_to_SURF_S3"
        result["ephemeral_signed_URL_or_signature_saved"]=False
    except (ValueError,TypeError,OSError,KeyError) as exc:
        result={
            "research_id":"R101","phase":"A6",
            "status":"R101_A6_DELIVERY_SOURCE_BLOCKED",
            "safe_failure":str(exc) if isinstance(exc,ArchiveGateError) else "R101_A6_ORIGINAL_DELIVERY_UNVERIFIED",
            "original_human_scores":0,"PESEN_v0_1":"FROZEN",
        }
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R101_A6_REAL_ORIGINAL_SURF_DELIVERED_RAW_ZIP_DOUBLE_SHA_DIRECTORY_ONLY":
        raise SystemExit(1)

if __name__=="__main__":
    main()
