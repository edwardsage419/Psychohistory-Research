#!/usr/bin/env python3
"""R072 REV002 only: publisher-delegated exact PLOS S8 XLSX byte provenance.

The official PLOS endpoint redirects to a signed storage.googleapis.com
/plos-corpus-prod/.../pone.0152076.s008.xlsx. Trust that *one* published
object only if issuer is already verified PLOS; never expose signed query.
No cell contents, person-level rows, or named subjects are extracted.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from urllib import request,parse,error
from r072_plos_s8_original_source_identity import (
    audit_bytes, allowed_official_url, MAX_BYTES
)

INITIAL_URL=("https://journals.plos.org/plosone/article/file"
             "?id=10.1371/journal.pone.0152076.s008&type=supplementary")
SIGNED_HOST="storage.googleapis.com"
OBJECT_PATH_RE=re.compile(
    r"^/plos-corpus-prod/10[.]1371/journal[.]pone[.]0152076/[0-9]+/pone[.]0152076[.]s008[.]xlsx$")
SIGNED_KEYS=("X-Goog-Algorithm","X-Goog-Credential","X-Goog-Date",
             "X-Goog-Expires","X-Goog-Signature")


def valid_delegated_target(url):
    p=parse.urlsplit(url)
    if (p.scheme!="https" or p.hostname!=SIGNED_HOST or
        p.username is not None or p.password is not None or p.port is not None or
        not OBJECT_PATH_RE.fullmatch(p.path) or p.fragment):
        return False
    try:
        pairs=parse.parse_qsl(p.query,keep_blank_values=True,strict_parsing=True)
    except ValueError:
        return False
    kv={}
    for k,v in pairs:
        if k in kv:
            return False
        kv[k]=v
    if (kv.get("X-Goog-Algorithm")!="GOOG4-RSA-SHA256" or
        any(not kv.get(key) for key in SIGNED_KEYS)):
        return False
    if (not re.fullmatch(r"[0-9]{8}T[0-9]{6}Z",kv["X-Goog-Date"])
        or not re.fullmatch(r"[A-Za-z0-9+/=._%-]+",kv["X-Goog-Signature"])
        or not re.fullmatch(r"[0-9]+",kv["X-Goog-Expires"])):
        return False
    expire=int(kv["X-Goog-Expires"])
    return 1<=expire<=86400 and "plos" in kv["X-Goog-Credential"].lower()


def permitted_redirect(issuer,target):
    if not allowed_official_url(issuer):
        return False
    return allowed_official_url(target) or valid_delegated_target(target)


class NarrowPublisherRedirect(request.HTTPRedirectHandler):
    def __init__(self):
        super().__init__()
        self.redirects=0
        self.used_delegated=False

    def redirect_request(self,req,fp,code,msg,headers,newurl):
        self.redirects+=1
        if self.redirects>5 or not permitted_redirect(req.full_url,newurl):
            raise ValueError("R072_S8_REJECTED_REDIRECT_NOT_PUBLISHER_AUTHENTICATED")
        if valid_delegated_target(newurl):
            self.used_delegated=True
        return super().redirect_request(req,fp,code,msg,headers,newurl)


def retrieve():
    handler=NarrowPublisherRedirect()
    opener=request.build_opener(handler)
    req=request.Request(INITIAL_URL,headers={
        "User-Agent":"Psychohistory-Research/1.0 academic-archive-provenance",
        "Accept":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream,*/*"})
    with opener.open(req,timeout=30) as resp:
        if not (allowed_official_url(resp.url) or
                (handler.used_delegated and valid_delegated_target(resp.url))):
            raise ValueError("R072_S8_FINAL_SOURCE_NOT_ORIGINAL")
        raw=resp.read(MAX_BYTES+1)
        if len(raw)>MAX_BYTES:
            raise ValueError("R072_S8_SOURCE_FILE_EXCEEDS_BYTE_BUDGET")
    return raw,("PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT"
                if handler.used_delegated else "PLOS_DIRECT_PUBLISHER")


def audit(raw,source_mode):
    if source_mode not in ("PLOS_DIRECT_PUBLISHER","PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT"):
        raise ValueError("INVALID_PUBLISHER_SOURCE_MODE")
    result=audit_bytes(raw,INITIAL_URL)
    result.update({
        "stage":"E2_PLOS_S8_SIGNED_REDIRECT_REV002",
        "status":"E2_PLOS_S8_SOURCE_BYTES_VERIFIED",
        "source_chain_category":source_mode,
        "new_protocol":"protocols/R072_E2_PLOS_SIGNED_ORIGIN_REDIRECT_RECOVERY_2026-10-16.md",
        "original_previous_run_38921163855":"HISTORIC_SOURCE_UNRESOLVED_NOT_REWRITTEN",
        "published_research_uses_real_human_participants":True,
        "real_workbook_cells_read":False,
        "real_human_behavior_model_e2":"BLOCKED_EXPERIMENT_RULE_AND_DATA_DICTIONARY",
        "R072_closure_unchanged":"CLOSED_BOUNDED",
    })
    # Old source URL remains publisher-only; never emit signed query tokens.
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    try:
        data,mode=retrieve()
        result=audit(data,mode)
    except (ValueError,OSError,error.URLError) as exc:
        result={
            "research_id":"R072",
            "stage":"E2_PLOS_S8_SIGNED_REDIRECT_REV002",
            "status":"SOURCE_UNRESOLVED",
            "cause_type":type(exc).__name__,
            "cause_code":str(exc)[:100] if isinstance(exc,ValueError) else "HTTP_OR_NETWORK_FAILURE",
            "original_bytes_sha256":None,
            "human_rows_read":False,
            "signed_redirect_secret_disclosed":False,
            "prior_failed_workflow_retained":38921163855,
            "pesen_v01":"FROZEN",
        }
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "sha256":result.get("raw_publisher_file_sha256"),
        "bytes":result.get("raw_original_bytes"),
        "source_mode":result.get("source_chain_category"),
        "failure_code":result.get("cause_code"),
    },sort_keys=True))
    if result["status"]!="E2_PLOS_S8_SOURCE_BYTES_VERIFIED":
        raise RuntimeError("Publisher-delegated R072 S8 original source not validated")


if __name__=="__main__":
    main()
