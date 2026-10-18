#!/usr/bin/env python3
"""R109 B0 true original 2016 Figshare source CSV ROW WIDTHS ONLY, no cells."""
from __future__ import annotations
import argparse,collections,csv,io,json,pathlib
import r109_phase_a1_2016_true_Guelph_Figshare_5611125_publisher_MD5_double_SHA_header_only as a

PINNED_SHA="31c989e9a2a8c3228e37effa0b3a850bbe69e3a9b15cd36dc317a3696e604bb6"

def original_widths(raw):
    original=a.source_header_only(raw)
    if original["computed_complete_original_SHA256"]!=PINNED_SHA:
        raise a.SourceError("R109_B0_FULL_ORIGINAL_CSV_SHA_NOT_PINNED")
    widths=[]
    try:
        for row in csv.reader(io.StringIO(raw.decode("utf-8-sig"),newline=""),strict=True):
            # Source row cells NEVER dereferenced; read len only.
            width=len(row)
            if not 1<=width<=300:
                raise a.SourceError("R109_B0_ORIGINAL_SOURCE_ROW_WIDTH_UNSAFE")
            widths.append(width)
    except (UnicodeError,csv.Error) as exc:
        raise a.SourceError("R109_B0_ORIGINAL_DATA_DELIMITERS_NOT_VERIFIED") from exc
    if len(widths)<2 or widths[0]!=18:
        raise a.SourceError("R109_B0_ORIGINAL_FIRST_SOURCE_ROW_NOT_18_COLUMNS")
    body=widths[1:]
    counts=collections.Counter(body)
    return {
        "research_id":"R109","phase":"B0",
        "status":"R109_B0_GENUINE_2016_MD5_BOUND_ORIGINAL_CSV_ANONYMOUS_ROW_WIDTH_ONLY",
        "original_publisher_md5_verified":original["publisher_MD5_full_original_verified"],
        "original_complete_SHA256":PINNED_SHA,
        "original_source_full_bytes":len(raw),
        "source_CSV_header_column_count":widths[0],
        "original_physical_data_line_count":original["CSV_physical_data_lines_unparsed"],
        "original_CSV_logical_body_row_count":len(body),
        "anonymous_source_body_row_width_counts":dict(sorted((str(k),v) for k,v in counts.items())),
        "all_original_CSV_body_rows_width_18":all(x==18 for x in body),
        "source_anonymous_first_8_data_row_widths":body[:8],
        "source_anonymous_last_8_data_row_widths":body[-8:],
        "original_body_row_width_transition_count":sum(body[i]!=body[i-1] for i in range(1,len(body))),
        "actual_human_source_data_cell_values_accessed":False,
        "source_independent_original_lab_session_ID_verified":False,
        "source_person_opponent_round_mapping_verified":False,
        "actual_human_model_scores":0,"PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        req=a.urllib.request.Request(a.META,headers={"User-Agent":"Psychohistory-R109-B0-Frozen-Firstparty-Catalog/1.0","Accept":"application/json"})
        with a.urllib.request.build_opener(a.NoMetadataRedirect()).open(req,timeout=40) as response:
            if response.status!=200:raise a.SourceError("R109_B0_FIRSTPARTY_SOURCE_META_HTTP_NOT_200")
            cat=response.read(262145)
        if len(cat)>262144:raise a.SourceError("R109_B0_PUBLISHER_META_TOO_LARGE")
        a.official_metadata_accept(json.loads(cat.decode("utf-8")))
        result=original_widths(a.get_author_original())
    except (ValueError,OSError,KeyError,TypeError,UnicodeError,csv.Error) as e:
        result={"research_id":"R109","phase":"B0",
                "status":"R109_B0_ORIGINAL_SOURCE_ROW_WIDTH_FAIL_CLOSED",
                "safe_failure":str(e) if isinstance(e,a.SourceError) else "R109_B0_ORIGINAL_SOURCE_UNVERIFIED",
                "actual_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R109_B0_GENUINE_2016_MD5_BOUND_ORIGINAL_CSV_ANONYMOUS_ROW_WIDTH_ONLY":
        raise SystemExit(1)
if __name__=="__main__":main()
