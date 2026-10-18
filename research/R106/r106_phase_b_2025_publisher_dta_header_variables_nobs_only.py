#!/usr/bin/env python3
"""R106 Phase B: Stata variable names/types/nobs only from MD5-verified publisher bytes.

StataReader._ensure_open() reads the Stata HEADER, not any original person row.
Never invoke StataReader.read(), get_chunk() or iterate its data.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import io
import json
import pathlib
import re
import urllib.request

from r106_phase_a_2025_drouvelis_pearce_zenodo_original_dta_md5_only import (
    URL, CAP, OFFICIAL_MD5, ExactRedirect, SourceError, validate_url, verify_only,
)

PINNED_SHA256="1cc9a4f68a51992808d966b118226bb5a66ee3ee6054843a132157df8eeb1985"
PINNED_BYTES=1514315
SAFE_NAME=re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,80}")

def type_class(s):
    # pandas StataReader._typlist uses b/h/l (byte/int/long),
    # f/d (float/double), and integer fixed-string widths.
    if type(s) is int and 1<=s<=2045:return "string"
    s=str(s).lower()
    if s in ("b","h","l","byte","int","long","int8","int16","int32","int64"):return "numeric_integer"
    if s in ("f","d","float","double","float32","float64"):return "numeric_float"
    if s=="q" or s.startswith("str") or s.startswith("string"):return "string"
    return "other"

def metadata_only(raw):
    source=verify_only(raw)
    if len(raw)!=PINNED_BYTES or source["study_computed_original_SHA256"]!=PINNED_SHA256:
        raise SourceError("R106_B_ORIGINAL_DTA_SOURCE_BYTES_SHA_NOT_PINNED")
    try:
        # Deliberate header-only interface: never call read() or get_chunk().
        from pandas.io.stata import StataReader
        with StataReader(io.BytesIO(raw), convert_categoricals=False) as stata:
            stata._ensure_open()  # pandas 2.2.3: _read_header only, no data.
            names=list(stata._varlist)
            types=list(stata._typlist)
            nobs=int(stata._nobs)
    except (ValueError,TypeError,AttributeError,OverflowError,NotImplementedError,UnicodeError,OSError) as e:
        raise SourceError("R106_B_STATA_HEADER_SCHEMA_COULD_NOT_BE_VERIFIED") from e
    if not 1<=len(names)<=300 or len(names)!=len(set(names)) or len(types)!=len(names) or not 0<=nobs<=5000000:
        raise SourceError("R106_B_STATA_HEADER_VARIABLE_OR_ROW_UNIVERSE_UNSAFE")
    if any(not isinstance(n,str) or SAFE_NAME.fullmatch(n) is None for n in names):
        raise SourceError("R106_B_STATA_VARIABLE_NAME_NOT_SAFE_ASCII")
    families=Counter(type_class(t) for t in types)
    return {
        "research_id":"R106",
        "phase":"B",
        "status":"R106_B_ORIGINAL_DTA_VERIFIED_HEADER_VARIABLE_TYPES_AND_NOBS_ONLY",
        "original_dataset_DOI":"10.5281/zenodo.15462528",
        "original_source_MD5_publisher_matched":OFFICIAL_MD5,
        "original_source_study_SHA256":PINNED_SHA256,
        "original_source_file_bytes":len(raw),
        "Stata_header_variable_count":len(names),
        "Stata_header_observation_count_unverified_human_rows":nobs,
        "Stata_header_allowlisted_variable_names":names,
        "Stata_header_type_family_counts":dict(sorted(families.items())),
        "original_human_cohort_recruited_independently_according_to_paper":True,
        "actual_dataset_contains_260_new_humans_verified":False,
        "original_paired_opponent_identity_verified":False,
        "actual_original_human_record_cells_read":0,
        "actual_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=pathlib.Path,required=True)
    args=ap.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R106-B-Stata-Header-Only-No-Original-Records/1.0"})
        with urllib.request.build_opener(ExactRedirect()).open(req,timeout=65) as resp:
            validate_url(resp.geturl())
            raw=resp.read(CAP+1)
        result=metadata_only(raw)
    except (ValueError,TypeError,OSError,KeyError,ImportError) as e:
        result={
            "research_id":"R106","phase":"B",
            "status":"R106_B_ORIGINAL_STATA_METADATA_FAIL_CLOSED",
            "safe_failure":str(e) if isinstance(e,SourceError) else "R106_B_ORIGINAL_STATA_METADATA_NOT_VERIFIED",
            "actual_human_model_scores":0,
            "PESEN_v0_1":"FROZEN",
        }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R106_B_ORIGINAL_DTA_VERIFIED_HEADER_VARIABLE_TYPES_AND_NOBS_ONLY":
        raise SystemExit(1)

if __name__=="__main__":
    main()
