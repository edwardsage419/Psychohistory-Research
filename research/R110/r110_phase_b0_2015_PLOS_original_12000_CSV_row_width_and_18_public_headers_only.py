#!/usr/bin/env python3
"""R110 B0 PLOS original 12000x18 rows: public source COLUMN LABELS, widths only."""
from __future__ import annotations
import argparse,collections,csv,io,json,pathlib,re
import r110_phase_a1_2015_PLOS_S1_verified_google_storage_original_doubleSHA_header_only as a

PINNED_SHA="ea70b0f3d98075f9d3e4401becfcdec8f6bdb5cae00c4dad63a697f9b61d7b5f"
EXPECTED_BYTES=1023128
LABEL=re.compile(r"[A-Za-z_][A-Za-z0-9_ .()/-]{0,59}",flags=re.ASCII)

def original_public_source_headers_and_widths(raw):
    verified=a.authenticate_header_and_whole_SHA(raw)
    if (verified["project_computed_whole_original_SHA256"]!=PINNED_SHA
        or len(raw)!=EXPECTED_BYTES):
        raise a.SourceError("R110_B0_ORIGINAL_2015_PLOS_WHOLEFILE_SHA_SIZE_NOT_PINNED")
    rd=csv.reader(io.StringIO(raw.decode("utf-8-sig"),newline=""),strict=True)
    head=None
    counts=collections.Counter()
    n=0
    first=[]
    last=[]
    prior=None
    transitions=0
    try:
        for row in rd:
            if head is None:
                if (len(row)!=18 or len(set(row))!=18
                    or any(LABEL.fullmatch(label) is None for label in row)):
                    raise a.SourceError("R110_B0_SOURCE_PUBLIC_18_FIELDS_NOT_SAFE_TO_PUBLISH")
                head=list(row)
                continue
            # Reader decoded row cells, but no source cell value dereference.
            k=len(row)
            if not 1<=k<=500:
                raise a.SourceError("R110_B0_ORIGINAL_CSV_LOGICAL_ROW_WIDTH_INVALID")
            n+=1
            counts[k]+=1
            if len(first)<8:first.append(k)
            last.append(k)
            if len(last)>8:last.pop(0)
            if prior is not None and prior!=k:transitions+=1
            prior=k
    except (csv.Error,UnicodeError) as ex:
        raise a.SourceError("R110_B0_TRUE_ORIGINAL_CSV_ROW_DELIMITERS_UNVERIFIED") from ex
    if head is None or n<1:
        raise a.SourceError("R110_B0_MISSING_ORIGINAL_CSV_LOGICAL_ROW_UNIVERSE")
    return {
        "research_id":"R110","phase":"B0",
        "status":"R110_B0_2015_PLOS_GENUINE_12000_LOGICAL_ROW_PUBLIC_HEADER_ONLY_E1",
        "original_source_SHA256":PINNED_SHA,
        "original_source_full_bytes":len(raw),
        "original_publisher_S1_DOI":"10.1371/journal.pone.0117183.s001",
        "author_original_public_field_names_only":head,
        "original_header_column_count":len(head),
        "original_physical_data_lines":verified["source_physical_CSV_data_lines_no_behavior_values_read"],
        "original_logical_CSV_data_rows":n,
        "source_anonymous_row_width_histogram":dict(sorted((str(k),v) for k,v in counts.items())),
        "all_source_rows_12000x18_structurally":n==12000 and counts=={18:12000},
        "source_first_eight_anonymous_row_widths":first,
        "source_last_eight_anonymous_row_widths":last,
        "source_row_width_transition_count":transitions,
        "original_individual_behavior_or_person_ID_values_read":False,
        "real_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:r=original_public_source_headers_and_widths(a.actual_official_source())
    except (OSError,ValueError,TypeError,UnicodeError,csv.Error) as e:
        r={"research_id":"R110","phase":"B0",
           "status":"R110_B0_ORIGINAL_CSV_PUBLIC_CODEBOOK_FAIL_CLOSED",
           "safe_failure":str(e) if isinstance(e,a.SourceError) else "R110_B0_AUTHENTIC_ORIGINAL_CSV_ROW_SCHEMA_UNVERIFIED",
           "real_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(r,sort_keys=True))
    if r["status"]!="R110_B0_2015_PLOS_GENUINE_12000_LOGICAL_ROW_PUBLIC_HEADER_ONLY_E1":
        raise SystemExit(1)
if __name__=="__main__":main()
