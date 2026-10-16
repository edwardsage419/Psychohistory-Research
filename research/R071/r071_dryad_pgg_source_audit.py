#!/usr/bin/env python3
"""R071: first-source-byte and column-only Dryad real public-goods audit.

No participant events, IDs, group IDs or within-person trajectories emitted.
Human behavior parameter fits are out of scope.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json
from pathlib import Path
from urllib import request,error

SOURCE_DOI="10.5061/dryad.n02v6wx03"
URL="https://datadryad.org/downloads/file_stream/1283295"
MAX_BYTES=4_000_000
MAX_ROWS=100_000
MAX_COLUMNS=120
CATEGORIES={
 "cooperation":("contrib","invest"),
 "punishment":("punish","fine"),
 "group":("group",),
 "institution":("treat","noise"),
 "time":("round","period"),
 "agent":("player","participant"),
}


def fetch():
    req=request.Request(URL,headers={
        "User-Agent":"Psychohistory-R071-Dryad-open-scholarly-source-audit/1.0",
        "Accept":"text/csv,application/octet-stream,*/*"})
    with request.urlopen(req,timeout=30) as resp:
        blob=resp.read(MAX_BYTES+1)
    if len(blob)>MAX_BYTES:raise ValueError("HUMAN_CSV_SOURCE_BYTE_BUDGET_EXCEEDED")
    return blob


def audit_bytes(raw):
    if not isinstance(raw,bytes) or not raw or len(raw)>MAX_BYTES:
        raise ValueError("HUMAN_CSV_SOURCE_BYTE_BUDGET_OR_EMPTY")
    if raw.startswith(b"%PDF") or raw.startswith(b"PK\x03\x04") or raw.startswith(b"<!DOCTYPE") or raw.startswith(b"<html"):
        raise ValueError("SOURCE_NOT_A_CSV_FILE")
    try:source=raw.decode("utf-8-sig")
    except UnicodeError:raise ValueError("SOURCE_CSV_ENCODING_NOT_UTF8") from None
    rd=csv.reader(io.StringIO(source,newline=""),delimiter=",")
    try:header=next(rd)
    except StopIteration:raise ValueError("CSV_HEADER_MISSING") from None
    if (not 1<=len(header)<=MAX_COLUMNS or
        any(not x.strip() or len(x)>120 for x in header) or
        len({x.casefold().strip() for x in header})!=len(header)):
        raise ValueError("CSV_HEADER_UNIQUE_NONEMPTY_COLUMNS_FAILED")
    rows=0
    filled=0
    for row in rd:
        rows+=1
        if rows>MAX_ROWS or len(row)!=len(header):
            raise ValueError("CSV_ROW_LENGTH_OR_ROW_BUDGET_FAILED")
        filled+=sum(bool(x.strip()) for x in row)
    if rows==0:raise ValueError("CSV_DATA_ROWS_MISSING")
    tags={key:[name for name in header
               if any(substring in name.lower() for substring in patterns)]
          for key,patterns in CATEGORIES.items()}
    return {
        "study":"R071",
        "stage":"E2_DRYAD_NOISY_PUBLIC_GOODS_SOURCE_AND_SCHEMA",
        "status":"E2_REAL_DRYAD_SOURCE_AND_SCHEMA_CANDIDATE_PASS",
        "dataset_DOI":SOURCE_DOI,
        "publisher":"Dryad",
        "file_display_name":"noisy-PGG.csv",
        "original_file_stream_url":URL,
        "raw_sha256":hashlib.sha256(raw).hexdigest(),
        "raw_byte_length":len(raw),
        "parsed_header_column_count":len(header),
        "original_public_field_names":header,
        "parsed_data_rows":rows,
        "nonnull_cell_total":filled,
        "candidate_semantic_field_names_only":tags,
        "no_participant_or_group_identifiers_exported":True,
        "no_human_row_data_exported":True,
        "measurement_status":"CANDIDATE_HEADER_ONLY_NO_VALUE_SEMANTICS_OR_REGIME_PARITY",
        "five_person_binary_fixed_roles_exact_match":"NO_FOUR_PERSON_EXPERIMENT_AND_NO_PRECISE_ROLE_EQUIVALENCE",
        "causal_norm_or_punishment_model_fitted":False,
        "E2_full_human_model_fit":"BLOCKED_MODEL_CONTRACT",
        "E3_independent":"OPEN",
        "pesen_v01":"FROZEN",
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    try:
        report=audit_bytes(fetch())
    except (ValueError,UnicodeError,OSError,error.URLError) as exc:
        report={"study":"R071","stage":"E2_DRYAD_NOISY_PUBLIC_GOODS_SOURCE_AND_SCHEMA",
                "status":"SOURCE_UNRESOLVED",
                "error_type":type(exc).__name__,
                "error_code":str(exc)[:100] if isinstance(exc,ValueError) else "HTTP_NETWORK_OR_CSV_ERROR",
                "source_data_verified":False,
                "human_model_fit":"NOT_EXECUTED",
                "pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":report["status"],
        "bytes":report.get("raw_byte_length"),
        "sha":report.get("raw_sha256"),
        "row_count":report.get("parsed_data_rows"),
        "headers":report.get("original_public_field_names"),
        "reason":report.get("error_code")},ensure_ascii=False))
    if report["status"]!="E2_REAL_DRYAD_SOURCE_AND_SCHEMA_CANDIDATE_PASS":
        raise RuntimeError("R071 Dryad source data not established")


if __name__=="__main__":main()
