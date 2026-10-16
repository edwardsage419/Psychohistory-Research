#!/usr/bin/env python3
"""R072 PLOS 2016 indirect reciprocity S8 human-source envelope ONLY.

No spreadsheet cells, sheet names, participant data or demographic values
are read or redistributed, just source SHA256 and bounded ZIP validity.
"""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
from urllib import request,parse,error
from zipfile import ZipFile,BadZipFile

PAPER="10.1371/journal.pone.0152076"
SUPPLEMENT="10.1371/journal.pone.0152076.s008"
URLS=(
  "https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0152076.s008&type=supplementary",
  "https://doi.org/10.1371/journal.pone.0152076.s008",
)
MAX_BYTES=600_000
MAX_UNCOMPRESSED=3_000_000
MAX_MEMBERS=60


def allowed_official_url(url):
    u=parse.urlparse(url)
    host=(u.hostname or "").lower()
    return (u.scheme=="https" and
            (host=="doi.org" or host=="plos.org" or host.endswith(".plos.org")))


class PublisherRedirect(request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if not allowed_official_url(newurl):
            raise ValueError("REDIRECT_LEFT_VERIFIED_PUBLISHER_DOMAINS")
        return super().redirect_request(req,fp,code,msg,headers,newurl)


def fetch_from_publisher():
    errors=[]
    opener=request.build_opener(PublisherRedirect)
    for url in URLS:
        if not allowed_official_url(url):
            raise ValueError("SOURCE_URL_NOT_PUBLISHER")
        try:
            req=request.Request(url,headers={
                "User-Agent":"Mozilla/5.0 (compatible; Psychohistory-R072-Academic-source-check/1.0)",
                "Accept":"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/octet-stream,*/*",
            })
            with opener.open(req,timeout=30) as resp:
                if not allowed_official_url(resp.url):
                    raise ValueError("UNTRUSTED_FINAL_SOURCE_HOST")
                data=resp.read(MAX_BYTES+1)
                if len(data)>MAX_BYTES:
                    raise ValueError("PUBLISHER_S8_BYTE_LIMIT_EXCEEDED")
            return data,url
        except (error.URLError,OSError,ValueError) as exc:
            errors.append(type(exc).__name__)
    raise ValueError("PUBLISHER_S8_ORIGINAL_UNAVAILABLE_"+ "_".join(errors))


def audit_bytes(raw,source_url):
    if not allowed_official_url(source_url):
        raise ValueError("SOURCE_NOT_OFFICIAL_PLOS_OR_DOI")
    if type(raw) is not bytes or len(raw)<60 or len(raw)>MAX_BYTES:
        raise ValueError("S8_XLSX_TOO_SHORT_OR_OVER_BUDGET")
    if not raw.startswith(b"PK\x03\x04"):
        raise ValueError("S8_NOT_OPEN_XML_ZIP_CONTAINER")
    try:
        with ZipFile(io.BytesIO(raw)) as z:
            files=z.infolist()
            if not 1<=len(files)<=MAX_MEMBERS:
                raise ValueError("S8_ZIP_UNEXPECTED_MEMBER_COUNT")
            names={item.filename for item in files}
            if "[Content_Types].xml" not in names or "xl/workbook.xml" not in names:
                raise ValueError("S8_NOT_XLSX_WORKBOOK_ENVELOPE")
            for item in files:
                name=item.filename.lower()
                if ("vbaProject".lower() in name or
                    "externallink" in name or
                    "connections.xml" in name or
                    ".." in item.filename.split("/") or
                    item.is_dir() and name.startswith("../")):
                    raise ValueError("S8_POTENTIALLY_ACTIVE_OR_EXTERNAL_WORKBOOK_PART")
            if sum(item.file_size for item in files)>MAX_UNCOMPRESSED:
                raise ValueError("S8_EXCESS_UNCOMPRESSED_MEMBER_BYTES")
            if z.testzip() is not None:
                raise ValueError("S8_ARCHIVE_FAILED_CRC_VALIDATION")
    except BadZipFile:
        raise ValueError("S8_NOT_VALID_XLSX_ZIP") from None
    return {
      "research_id":"R072",
      "stage":"E2_PLOS_FIELD_S8_BYTE_PROVENANCE_ONLY",
      "status":"E2_PUBLISHED_HUMAN_SOURCE_BYTES_VERIFIED",
      "paper_DOI":PAPER,
      "supplement_DOI":SUPPLEMENT,
      "source_official_url":source_url,
      "raw_publisher_file_sha256":hashlib.sha256(raw).hexdigest(),
      "raw_original_bytes":len(raw),
      "zip_members_checked_for_integrity":len(files),
      "office_open_xml_envelope":True,
      "original_sheet_or_member_rows_read":False,
      "source_file_redistributed":False,
      "participant_rows_exported":False,
      "human_behavior_schema_verified":False,
      "true_visible_reputations_or_donation_costs_verified":False,
      "R072_four_agent_indirect_reciprocity_mechanism_fitted":False,
      "R072_human_E2_exact_mechanism":"BLOCKED_MEASUREMENT_AND_RULE_PARITY",
      "independent_E3":"OPEN",
      "pesen_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    try:
        data,official=fetch_from_publisher()
        result=audit_bytes(data,official)
    except (ValueError,OSError,error.URLError) as exc:
        result={
            "research_id":"R072","stage":"E2_PLOS_FIELD_S8_BYTE_PROVENANCE_ONLY",
            "status":"SOURCE_UNRESOLVED",
            "error_category":type(exc).__name__,
            "bounded_error_code":str(exc)[:130] if isinstance(exc,ValueError) else "NETWORK_UNAVAILABLE",
            "S8_original_byte_hash":None,
            "human_rows_read":False,
            "human_mechanism_fitted":False,
            "pesen_v01":"FROZEN",
        }
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],
                      "bytes":result.get("raw_original_bytes"),
                      "sha256":result.get("raw_publisher_file_sha256"),
                      "error":result.get("bounded_error_code")},sort_keys=True))
    if result["status"]!="E2_PUBLISHED_HUMAN_SOURCE_BYTES_VERIFIED":
        raise RuntimeError("Verified original PLOS S8 bytes not acquired")


if __name__=="__main__":
    main()
