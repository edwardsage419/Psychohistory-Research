#!/usr/bin/env python3
"""R066 metadata ONLY publication/access check for longitudinal network attitudes.

No original respondent data are downloaded. DOI and Dataverse API status checks
are explicitly separated from scientific identification and file-level access.
"""
from __future__ import annotations
import argparse
import json
import re
import socket
import ssl
from urllib import error, parse, request
from pathlib import Path

DATASETS = {
    "larson_lewis_2026": "doi:10.7910/DVN/RAHSVM",
    "klar_2016_control": "doi:10.7910/DVN/JIIICD",
}
API_BASE = "https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId="
MAX_FILE_META = 200
MAX_REPLY_BYTES = 3_000_000


def sanitize_public_filename(value: object) -> str:
    """Omit unusual or suspicious names that could embed private identities."""
    s = str(value)
    if (len(s) > 140 or not re.fullmatch(r"[A-Za-z0-9_.+\-() ]+", s)
        or s in ("", ".", "..") or "/" in s or "\\" in s):
        return "[redacted-nonstandard-filename]"
    return s


def citation_field(version: dict, name: str):
    blocks = version.get("metadataBlocks", {})
    if not isinstance(blocks, dict):
        return None
    fields = blocks.get("citation", {}).get("fields", [])
    if not isinstance(fields, list):
        return None
    return next((v.get("value") for v in fields if isinstance(v, dict)
                 and v.get("typeName") == name), None)


def parse_dataset_api(http_code: int, payload: object, intended_doi: str) -> dict:
    """Strict classification: status and explicit metadata prove publication."""
    if http_code == 404 and isinstance(payload, dict) and payload.get("status") == "ERROR":
        return {"status": "NOT_FOUND_OR_UNREGISTERED", "http_status": 404,
                "dataset_doi": intended_doi}
    if http_code in (401, 403):
        return {"status": "DRAFT_OR_RESTRICTED_METADATA", "http_status": http_code,
                "dataset_doi": intended_doi}
    if http_code == 429 or http_code >= 500:
        return {"status": "NETWORK_OR_UPSTREAM_UNRESOLVED", "http_status": http_code,
                "dataset_doi": intended_doi}
    if http_code != 200 or not isinstance(payload, dict):
        return {"status": "RESPONSE_SCHEMA_UNRESOLVED", "http_status": http_code,
                "dataset_doi": intended_doi}
    if payload.get("status") != "OK":
        return {"status": "RESPONSE_SCHEMA_UNRESOLVED", "http_status": http_code,
                "dataset_doi": intended_doi}
    data = payload.get("data")
    if not isinstance(data, dict):
        return {"status": "RESPONSE_SCHEMA_UNRESOLVED", "http_status": http_code,
                "dataset_doi": intended_doi}
    version = data.get("latestVersion")
    if not isinstance(version, dict):
        return {"status": "RESPONSE_SCHEMA_UNRESOLVED", "http_status": http_code,
                "dataset_doi": intended_doi}
    version_state = version.get("versionState")
    if version_state in ("DRAFT", "DEACCESSIONED"):
        return {"status": "DRAFT_OR_RESTRICTED_METADATA", "http_status": 200,
                "dataset_doi": intended_doi, "version_state": version_state}
    files = version.get("files")
    if (not isinstance(files, list) or
        not isinstance(version.get("versionNumber"), int) or
        not isinstance(version.get("versionMinorNumber"), int) or
        version_state != "RELEASED"):
        return {"status": "RESPONSE_SCHEMA_UNRESOLVED", "http_status": 200,
                "dataset_doi": intended_doi, "version_state": version_state}
    # Some Dataverse versions use latestVersion.versionState="RELEASED",
    # while others expose a separate latestPublishedVersion; do not assume.
    published_files = []
    for entry in files[:MAX_FILE_META]:
        if not isinstance(entry, dict):
            return {"status": "RESPONSE_SCHEMA_UNRESOLVED", "dataset_doi": intended_doi,
                    "http_status": 200}
        df = entry.get("dataFile", {})
        if not isinstance(df, dict):
            df = {}
        name = df.get("filename") or entry.get("label") or ""
        published_files.append({
            "filename": sanitize_public_filename(name),
            "size_bytes": df.get("filesize") if type(df.get("filesize")) is int else None,
            "content_type": str(df.get("contentType", ""))[:80],
            "restricted": bool(entry.get("restricted", False)),
            "file_metadata_id": df.get("id") if type(df.get("id")) is int else None,
        })
    title = citation_field(version, "title")
    license_value = version.get("license")
    if isinstance(license_value, dict):
        license_out = {"name": str(license_value.get("name", ""))[:120],
                       "uri": str(license_value.get("uri", ""))[:250]}
    else:
        license_out = {"name": str(license_value)[:120]} if license_value else None
    return {
        "status": "PUBLIC_PUBLISHED_METADATA_VERIFIED",
        "http_status": 200,
        "dataset_doi": intended_doi,
        "reported_dataset_identifier": str(data.get("persistentUrl", ""))[:250],
        "title": str(title)[:260] if title is not None else None,
        "version_major": version["versionNumber"],
        "version_minor": version["versionMinorNumber"],
        "version_state": version_state,
        "release_time": str(version.get("releaseTime", ""))[:50],
        "license": license_out,
        "file_count": len(files),
        "files": published_files,
        "file_metadata_truncated": len(files) > MAX_FILE_META,
        "warning": "METADATA ONLY: no file was retrieved; no schema or model evidence.",
    }


def fetch_dataset(doi: str, opener=request.urlopen) -> dict:
    if doi not in DATASETS.values():
        raise ValueError("unapproved DOI")
    url = API_BASE + parse.quote(doi, safe="")
    req = request.Request(url, headers={"User-Agent": "R066-metadata-reproducibility-audit/1.0",
                                        "Accept": "application/json"})
    payload = None
    status = None
    for attempt in range(2):
        try:
            with opener(req, timeout=20) as response:
                status = response.status
                raw = response.read(MAX_REPLY_BYTES+1)
                if len(raw) > MAX_REPLY_BYTES:
                    return {"status":"RESPONSE_SCHEMA_UNRESOLVED","dataset_doi":doi,
                            "reason":"metadata response exceeded byte limit"}
                payload = json.loads(raw.decode("utf-8"))
                break
        except error.HTTPError as exc:
            status = exc.code
            try:
                raw = exc.read(MAX_REPLY_BYTES+1)
                payload = json.loads(raw.decode("utf-8")) if len(raw) <= MAX_REPLY_BYTES else None
            except (ValueError, UnicodeError):
                payload = None
            break
        except (error.URLError, socket.timeout, TimeoutError, ssl.SSLError, OSError) as exc:
            if attempt == 1:
                return {"status":"NETWORK_OR_UPSTREAM_UNRESOLVED",
                        "dataset_doi":doi,"error_type":type(exc).__name__}
        except (ValueError, UnicodeError):
            return {"status":"RESPONSE_SCHEMA_UNRESOLVED","dataset_doi":doi,
                    "reason":"API did not provide UTF8 JSON"}
    if status is None:
        return {"status":"NETWORK_OR_UPSTREAM_UNRESOLVED","dataset_doi":doi}
    return parse_dataset_api(status, payload, doi)


def run_probe() -> dict:
    res = {name: fetch_dataset(doi) for name, doi in DATASETS.items()}
    return {
        "study":"R066",
        "stage":"E2_DATAVERSE_CATALOG_PUBLICATION_DISCOVERY",
        "protocol":"protocols/R066_E2_DATAVERSE_CATALOG_AVAILABILITY_2026-10-16.md",
        "api_origin":"https://dataverse.harvard.edu",
        "datasets":res,
        "model_fit_performed":False,
        "file_contents_downloaded":False,
        "empirical_model_identification":"OPEN",
        "evidence_type":"REMOTE_CATALOG_METADATA_ONLY",
        "pesen_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    result=run_probe()
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"stage":result["stage"],
                      "status":{k:v["status"] for k,v in result["datasets"].items()},
                      "file_counts":{k:v.get("file_count") for k,v in result["datasets"].items()}},
                     sort_keys=True))


if __name__=="__main__":
    main()
