#!/usr/bin/env python3
"""R108 B0 authentic original CSV row WIDTH only: NO source cell dereferences."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import io
import json
import pathlib

import r108_phase_a1_original_2017_Leicester_fixed_pair_CSV_MD5_double_SHA_header_only as a
import r108_phase_a3_verified_Figshare_publisher_S3_delegate_MD5_double_source as s
import r108_phase_a4_verified_full_original_MD5_header_class_only as b

def width_only(raw):
    e1=b.class_only(raw)
    reader=csv.reader(io.StringIO(raw.decode("utf-8-sig"),newline=""),strict=True)
    widths=[]
    try:
        for row in reader:
            # Never access an original row's cells, not even first/last value.
            width=len(row)
            if not 1<=width<=500:
                raise a.SourceError("R108_B0_ORIGINAL_CSV_ROW_WIDTH_OUT_OF_BOUNDS")
            widths.append(width)
    except (UnicodeError,csv.Error) as exc:
        raise a.SourceError("R108_B0_ORIGINAL_CSV_ROW_FORMAT_NOT_VALID") from exc
    if len(widths)<2 or widths[0]!=e1["source_csv_header_column_count"]:
        raise a.SourceError("R108_B0_ORIGINAL_HEADER_OR_BODY_ROWS_UNVERIFIED")
    data=widths[1:]
    transitions=[i+1 for i in range(1,len(data)) if data[i]!=data[i-1]]
    counts=Counter(data)
    return {
        "research_id":"R108","phase":"B0",
        "status":"R108_B0_GENUINE_2017_ORIGINAL_CSV_ANONYMOUS_ROW_WIDTH_ONLY_E1",
        "original_source_SHA256":e1["project_original_complete_SHA256"],
        "publisher_MD5_verified":e1["publisher_original_MD5_whole_file_matched"],
        "original_file_bytes":e1["genuine_original_whole_file_bytes"],
        "true_original_csv_header_column_count":widths[0],
        "original_CSV_logical_data_row_count_no_cells_read":len(data),
        "original_CSV_physical_data_line_count":e1["source_physical_data_lines_unparsed"],
        "source_body_row_width_histogram":dict(sorted((str(k),v) for k,v in counts.items())),
        "anonymous_first_ten_data_row_widths_only":data[:10],
        "anonymous_last_ten_data_row_widths_only":data[-10:],
        "original_row_width_transition_count":len(transitions),
        "anonymous_first_thirty_row_width_transition_ordinals_only":transitions[:30],
        "original_CSV_cell_values_application_dereferenced":False,
        "raw_person_round_partner_acts_exported":False,
        "original_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=pathlib.Path,required=True)
    arg=parser.parse_args()
    try:
        m=a.get_url(a.METADATA,"metadata",262144)
        a.validate_article_original_file_catalog(json.loads(m.decode("utf-8")))
        result=width_only(s.real_publisher_download())
    except (ValueError,OSError,TypeError,KeyError,UnicodeError,csv.Error) as exc:
        result={"research_id":"R108","phase":"B0",
                "status":"R108_B0_ORIGINAL_CSV_ROW_WIDTH_FAIL_CLOSED",
                "safe_failure":str(exc) if isinstance(exc,a.SourceError) else "R108_B0_ORIGINAL_SOURCE_NOT_VERIFIED",
                "original_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    arg.output.parent.mkdir(parents=True,exist_ok=True)
    arg.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R108_B0_GENUINE_2017_ORIGINAL_CSV_ANONYMOUS_ROW_WIDTH_ONLY_E1":
        raise SystemExit(1)
if __name__=="__main__":main()
