#!/usr/bin/env python3
"""R106 C1: publisher-authenticated seven nonbehavior Stata ID source type classes.

No literal actor/session/group identifiers, original choices or source rows printed.
"""
from __future__ import annotations
import argparse
from collections import Counter
import io
import json
import math
import pathlib
import urllib.request

from r106_phase_a_2025_drouvelis_pearce_zenodo_original_dta_md5_only import (
    URL,CAP,ExactRedirect,SourceError,validate_url
)
from r106_phase_b_2025_publisher_dta_header_variables_nobs_only import metadata_only,PINNED_SHA256

COLUMNS=("Session","Subject","Group","Period","ID","sessionid","ClientNumber")
SOURCE_ROWS=3620
SOURCE_VARS=148
CLASSES=(
    "numeric_positive_integer_bounded",
    "numeric_zero","numeric_negative_integer","numeric_positive_integer_above_original_1e9_ceiling",
    "numeric_fractional","missing_nan_or_blank","ascii_numeric_string","ascii_nonnumeric_string",
    "unicode_string","other"
)

def class_only(value):
    import pandas as pd
    try:
        if pd.isna(value):
            return "missing_nan_or_blank"
    except (TypeError,ValueError):
        pass
    if isinstance(value,str):
        z=value.strip()
        if not z:
            return "missing_nan_or_blank"
        if not z.isascii():
            return "unicode_string"
        try:
            n=float(z)
            if math.isfinite(n):
                return "ascii_numeric_string"
        except (ValueError,OverflowError):
            pass
        return "ascii_nonnumeric_string"
    try:
        n=float(value)
    except (ValueError,TypeError,OverflowError):
        return "other"
    if not math.isfinite(n):
        return "missing_nan_or_blank"
    if not n.is_integer():
        return "numeric_fractional"
    if n==0:
        return "numeric_zero"
    if n<0:
        return "numeric_negative_integer"
    if n>1000000000:
        return "numeric_positive_integer_above_original_1e9_ceiling"
    return "numeric_positive_integer_bounded"

def anonymous_id_types_only(raw):
    metadata=metadata_only(raw)
    if (metadata["Stata_header_observation_count_unverified_human_rows"]!=SOURCE_ROWS or
        metadata["Stata_header_variable_count"]!=SOURCE_VARS or
        not set(COLUMNS).issubset(metadata["Stata_header_allowlisted_variable_names"])):
        raise SourceError("R106_C1_TRUE_SOURCE_IDENTITY_HEADER_NOT_PINNED")
    from pandas.io.stata import StataReader
    try:
        with StataReader(io.BytesIO(raw),convert_categoricals=False) as s:
            selected=s.read(columns=list(COLUMNS),convert_categoricals=False,convert_dates=False)
    except (ValueError,TypeError,UnicodeError,OSError,IndexError) as e:
        raise SourceError("R106_C1_STATA_SOURCE_IDENTITY_ONLY_PARSE_FAILED") from e
    if len(selected)!=SOURCE_ROWS or set(selected.columns)!=set(COLUMNS):
        raise SourceError("R106_C1_SELECTED_SOURCE_IDENTITY_SCHEMA_CHANGED")
    selected=selected.loc[:,list(COLUMNS)]
    counts={}
    unique={}
    types={}
    for name in COLUMNS:
        x=selected[name]
        counts[name]={category:0 for category in CLASSES}
        for v in x:
            counts[name][class_only(v)]+=1
        if sum(counts[name].values())!=SOURCE_ROWS:
            raise SourceError("R106_C1_ANONYMOUS_ID_CLASS_COUNTS_NOT_CLOSED")
        try:
            unique[name]=int(x.nunique(dropna=True))
        except (TypeError,ValueError) as e:
            raise SourceError("R106_C1_UNIQUE_ID_SOURCE_CARDINALITY_UNVERIFIED") from e
        import pandas as pd
        types[name]=("numeric" if pd.api.types.is_numeric_dtype(x.dtype) else
                     "string" if pd.api.types.is_string_dtype(x.dtype) else "other")
    return {
        "research_id":"R106","phase":"C1",
        "status":"R106_C1_REAL_SOURCE_SEVEN_ID_FIELD_ANONYMOUS_TYPE_DIAGNOSTIC_ONLY",
        "original_source_SHA256":PINNED_SHA256,
        "original_source_row_count":SOURCE_ROWS,
        "original_Stata_header_variables":SOURCE_VARS,
        "anonymous_seven_ID_source_field_type_classes":counts,
        "anonymous_source_ID_field_distinct_nonmissing_counts":unique,
        "anonymous_source_ID_field_declared_dtype_class":types,
        "original_ID_field_literal_values_exported":False,
        "application_requested_only_seven_nonbehavior_fields":True,
        "pandas_decoder_internally_reads_records_but_no_behavior_column_requested":True,
        "original_left_otherleft_p2otherleft_application_accessed":False,
        "original_human_behavior_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R106-C1-2025-Stata-Nonbehavior-ID-Types-Only/1.0"})
        with urllib.request.build_opener(ExactRedirect()).open(req,timeout=65) as response:
            validate_url(response.geturl())
            raw=response.read(CAP+1)
        result=anonymous_id_types_only(raw)
    except (ValueError,TypeError,OSError,KeyError,ImportError) as exc:
        result={
            "research_id":"R106","phase":"C1",
            "status":"R106_C1_ORIGINAL_ID_FIELD_SYNTAX_FAIL_CLOSED",
            "safe_failure":str(exc) if isinstance(exc,SourceError) else "R106_C1_ORIGINAL_SOURCE_ID_TYPE_NOT_VERIFIED",
            "original_human_behavior_scores":0,
            "PESEN_v0_1":"FROZEN",
        }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R106_C1_REAL_SOURCE_SEVEN_ID_FIELD_ANONYMOUS_TYPE_DIAGNOSTIC_ONLY":
        raise SystemExit(1)

if __name__=="__main__":
    main()
