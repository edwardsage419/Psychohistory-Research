#!/usr/bin/env python3
"""R101 A5: no-follow official Dataverse redirect metadata preflight only."""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import urllib.error
import urllib.parse
import urllib.request

ORIGINAL="https://dataverse.nl/api/access/datafile/383977"
ALLOWED_CODES={301,302,303,307,308}
CAP_URL=8192
HOST_RE=re.compile(r"[A-Za-z0-9.-]{1,253}")

class RedirectGateError(ValueError):
    pass

def validate_original(url):
    p=urllib.parse.urlsplit(url)
    if p.scheme!="https" or p.netloc!="dataverse.nl" or p.path!="/api/access/datafile/383977" or p.query or p.fragment:
        raise RedirectGateError("R101_A5_ORIGINAL_ENDPOINT_NOT_PINNED")

def safe_destination(loc):
    if not isinstance(loc,str) or not loc or len(loc)>CAP_URL:
        raise RedirectGateError("R101_A5_DESTINATION_HEADER_MISSING_OR_OVERSIZED")
    full=urllib.parse.urljoin(ORIGINAL,loc)
    p=urllib.parse.urlsplit(full)
    if p.scheme!="https" or p.username or p.password or p.port is not None or not HOST_RE.fullmatch(p.hostname or "") or not p.path.startswith("/"):
        raise RedirectGateError("R101_A5_DESTINATION_URL_STRUCTURE_UNSAFE")
    segments=[x for x in p.path.split("/") if x]
    if len(segments)>30 or len(p.path)>4096:
        raise RedirectGateError("R101_A5_DESTINATION_PATH_STRUCTURE_UNSAFE")
    keys=[]
    if p.query:
        for k in urllib.parse.parse_qs(p.query,keep_blank_values=True).keys():
            keys.append(k if re.fullmatch(r"[A-Za-z0-9_-]{1,50}",k) else "other")
    keys=sorted(set(keys))
    return {
        "redirect_target_host":p.hostname.lower(),
        "redirect_target_path_first_segment_class":(
            segments[0] if segments and re.fullmatch(r"[a-zA-Z]{1,32}",segments[0]) else "opaque"
        ),
        "redirect_target_path_segment_count":len(segments),
        "redirect_target_last_segment_zip_suffix":bool(segments and segments[-1].lower().endswith(".zip")),
        "redirect_target_query_key_classes":keys,
        "full_redirect_URL_or_query_values_exported":False,
    }

class NeverFollow(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # Return None causes urllib to raise HTTPError to the caller.
        # No external request is made.
        return None

def preflight():
    validate_original(ORIGINAL)
    req=urllib.request.Request(ORIGINAL,headers={"User-Agent":"Psychohistory-R101-A5-NoFollow-Publisher-Redirect-Only/1.0"})
    opener=urllib.request.build_opener(NeverFollow())
    try:
        with opener.open(req,timeout=40) as response:
            code=response.status
            if code != 200:
                raise RedirectGateError("R101_A5_NONREDIRECT_UNEXPECTED_HTTP_STATUS")
            # Deliberately never read response entity bytes.
            return {
                "research_id":"R101","phase":"A5",
                "status":"R101_A5_OFFICIAL_ENDPOINT_DIRECT_HTTP200_NO_BODY_READ",
                "firstparty_http_status":200,
                "original_response_body_bytes_read":0,
                "original_human_scores":0,"PESEN_v0_1":"FROZEN",
            }
    except urllib.error.HTTPError as exc:
        if exc.code not in ALLOWED_CODES:
            return {
                "research_id":"R101","phase":"A5",
                "status":"R101_A5_SOURCE_HTTP_REJECTED_NO_BODY",
                "firstparty_http_status":int(exc.code),
                "original_response_body_bytes_read":0,
                "original_human_scores":0,"PESEN_v0_1":"FROZEN",
            }
        return {
            "research_id":"R101","phase":"A5",
            "status":"R101_A5_OFFICIAL_REDIRECT_TARGET_CLASS_VERIFIED_ONLY",
            "firstparty_http_status":int(exc.code),
            **safe_destination(exc.headers.get("Location")),
            "redirect_followed":False,
            "original_response_body_bytes_read":0,
            "original_human_scores":0,
            "PESEN_v0_1":"FROZEN",
        }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=pathlib.Path)
    x=p.parse_args()
    try:
        result=preflight()
    except (ValueError,TypeError,OSError,KeyError) as e:
        result={"research_id":"R101","phase":"A5",
                "status":"R101_A5_PREFLIGHT_FAIL_CLOSED",
                "safe_failure":str(e) if isinstance(e,RedirectGateError) else "R101_A5_ORIGINAL_RESPONSE_UNVERIFIED",
                "original_human_scores":0,"PESEN_v0_1":"FROZEN"}
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"] not in ("R101_A5_OFFICIAL_REDIRECT_TARGET_CLASS_VERIFIED_ONLY","R101_A5_OFFICIAL_ENDPOINT_DIRECT_HTTP200_NO_BODY_READ"):
        raise SystemExit(1)

if __name__=="__main__":
    main()
