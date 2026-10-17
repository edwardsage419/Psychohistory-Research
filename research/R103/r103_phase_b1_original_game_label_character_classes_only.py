#!/usr/bin/env python3
"""R103 B1 original source game label codepoint classes only; NEVER player actions."""
from __future__ import annotations
import argparse
from collections import Counter
import csv
import io
import json
import pathlib
import urllib.request

from r103_phase_a_2016_drbrain_original_md5_header_only import (
    URL,CAP,ExactOfficialRedirect,SourceError,validate_url,audit_firstparty_bytes_header_only
)
from r103_phase_b_2016_original_dyadic_actor_opponent_reciprocity_only import (
    PINNED_SOURCE_SHA,PINNED_LINES
)

def classify_label(c):
    if "a"<=c<="z":return "ascii_lower"
    if "A"<=c<="Z":return "ascii_upper"
    if "0"<=c<="9":return "ascii_digit"
    if c in (" ","\t"):return "ascii_whitespace"
    if 33<=ord(c)<=126:return "ascii_punctuation"
    return "nonascii_or_control"

def label_format_only(raw):
    valid=audit_firstparty_bytes_header_only(raw)
    if valid["original_project_computed_SHA256"]!=PINNED_SOURCE_SHA or valid["source_physical_data_lines_without_parsing"]!=PINNED_LINES:
        raise SourceError("R103_B1_OFFICIAL_SOURCE_SHA_OR_ROWS_CHANGED")
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""))
    classes=Counter()
    sizes=Counter()
    punctuation=set()
    unique=set()
    count=0
    for row in reader:
        # Exactly one non-behavioral, non-personal column read.
        name=row["Game"]
        if not isinstance(name,str) or len(name)>100:
            raise SourceError("R103_B1_ORIGINAL_GAME_LABEL_FORMAT_INVALID")
        count+=1
        unique.add(name)
        sizes[len(name)]+=1
        for c in name:
            k=classify_label(c)
            classes[k]+=1
            if k=="ascii_punctuation":
                punctuation.add(ord(c))
    if count!=PINNED_LINES:
        raise SourceError("R103_B1_REAL_GAME_COLUMN_ROW_COUNT_CHANGED")
    return {
        "research_id":"R103","phase":"B1",
        "status":"R103_B1_AUTHENTIC_SOURCE_GAME_LABEL_CHARACTER_CLASSES_ONLY",
        "official_original_full_SHA256":PINNED_SOURCE_SHA,
        "original_source_rows":count,
        "distinct_original_game_labels_count":len(unique),
        "anonymous_original_game_label_lengths_histogram":dict(sorted(sizes.items())),
        "anonymous_game_label_character_class_count":dict(sorted(classes.items())),
        "ascii_punctuation_unicode_decimal_codepoints_only":sorted(punctuation),
        "any_original_Game_text_exported":False,
        "any_original_Action_or_Opponent_Action_values_accessed":False,
        "any_original_person_or_experiment_ID_accessed":False,
        "real_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    x=p.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R103-B1-Only-Game-Label-Char-Classes/1.0"})
        with urllib.request.build_opener(ExactOfficialRedirect()).open(req,timeout=55) as response:
            validate_url(response.geturl())
            raw=response.read(CAP+1)
        result=label_format_only(raw)
    except (ValueError,OSError,TypeError,KeyError,csv.Error,UnicodeError) as exc:
        result={"research_id":"R103","phase":"B1",
                "status":"R103_B1_SOURCE_GAME_METADATA_FAIL_CLOSED",
                "safe_failure":str(exc) if isinstance(exc,SourceError) else "R103_B1_OFFICIAL_GAME_METADATA_UNVERIFIED",
                "real_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R103_B1_AUTHENTIC_SOURCE_GAME_LABEL_CHARACTER_CLASSES_ONLY":
        raise SystemExit(1)

if __name__=="__main__":
    main()
