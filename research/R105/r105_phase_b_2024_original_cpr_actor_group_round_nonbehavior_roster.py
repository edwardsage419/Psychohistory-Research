#!/usr/bin/env python3
"""R105 Phase B authentic MD5/SHA original person/group/round ONLY; no extraction."""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv
import io
import json
import pathlib
import re
import urllib.request

from r105_phase_a_original_2024_cpr_defaults_zenodo_md5_header_only import (
    SOURCE_URL,CAP,OnlyExactPublisherRedirect,SourceGateError,validate_url,
    source_header_only
)
ORIGINAL_SHA="a7d959361075ae88dc2fc4945b8a7ecd3c8fe3a234ff25dc53b28b9c2c5cdeae"
SOURCE_ROWS=4120
ID=re.compile(r"[A-Za-z0-9_./() -]{1,128}")
IDENTITY_NAMES=("player_id","Treatment","group_id","round")
UNNAMED="__UNNAMED_ORIGINAL_SOURCE_COLUMN__"

def identity(value):
    if type(value) is not str or not ID.fullmatch(value) or value.strip()!=value or ".." in value or "/" in value or value in (".",".."):
        raise SourceGateError("R105_B_ORIGINAL_SOURCE_IDENTITY_OR_TREATMENT_UNSAFE")
    return value

def game_round(value):
    if type(value) is not str or not value.isascii() or not value.isdecimal():
        raise SourceGateError("R105_B_ORIGINAL_GAME_ROUND_NOT_INTEGER")
    t=int(value)
    if t<1 or t>10:
        raise SourceGateError("R105_B_ORIGINAL_ROUND_OUTSIDE_ONE_TO_TEN")
    return t

def original_nonbehavior_roster(raw):
    a=source_header_only(raw)
    if a["project_original_complete_SHA256"]!=ORIGINAL_SHA or a["physical_original_data_row_lines_unparsed"]!=SOURCE_ROWS:
        raise SourceGateError("R105_B_ORIGINAL_PUBLISHED_FULLFILE_SHA_OR_ROWS_MISMATCH")
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""),strict=True)
    safe=[name if name else UNNAMED for name in (reader.fieldnames or [])]
    if safe!=a["public_sanitized_original_header_field_names"] or any(k not in safe for k in IDENTITY_NAMES):
        raise SourceGateError("R105_B_ORIGINAL_NONBEHAVIOR_IDENTITY_FIELDS_UNVERIFIED")
    treatment_people=defaultdict(set)
    treatment_groups=defaultdict(set)
    people_groups={}
    person_rounds=defaultdict(set)
    group_round_roster=defaultdict(set)
    group_permanent_members=defaultdict(set)
    player_treatments=defaultdict(set)
    rows=0
    for row in reader:
        rows+=1
        if rows>SOURCE_ROWS or None in row or len(row)!=37:
            raise SourceGateError("R105_B_ORIGINAL_ROW_STRUCTURE_MALFORMED")
        # The only original cell values application-dereferenced in B:
        player=identity(row["player_id"])
        treatment=identity(row["Treatment"])
        group=identity(row["group_id"])
        t=game_round(row["round"])
        person=(treatment,player)
        g=(treatment,group)
        if t in person_rounds[person]:
            raise SourceGateError("R105_B_DUPLICATE_ORIGINAL_PLAYER_ROUND")
        person_rounds[person].add(t)
        if person in people_groups and people_groups[person]!=g:
            raise SourceGateError("R105_B_ORIGINAL_PERSON_MOVED_GROUPS")
        people_groups[person]=g
        player_treatments[player].add(treatment)
        treatment_people[treatment].add(person)
        treatment_groups[treatment].add(g)
        group_permanent_members[g].add(person)
        group_round_roster[(g,t)].add(person)
    if rows!=SOURCE_ROWS:
        raise SourceGateError("R105_B_SOURCE_ROW_UNIVERSE_CHANGED")
    expected_rounds=set(range(1,11))
    if any(rounds!=expected_rounds for rounds in person_rounds.values()):
        raise SourceGateError("R105_B_ORIGINAL_PERSON_TEN_CONTIGUOUS_ROUNDS_MISSING")
    if any(len(p)!=4 for p in group_permanent_members.values()):
        raise SourceGateError("R105_B_ORIGINAL_FOUR_PERSON_GROUP_MEMBER_COUNT_INVALID")
    for g,persons in group_permanent_members.items():
        for t in range(1,11):
            if group_round_roster.get((g,t))!=persons:
                raise SourceGateError("R105_B_SOURCE_FOUR_PERSON_FIXED_GROUP_ROUND_NOT_COMPLETE")
    if len(person_rounds)!=412 or len(group_permanent_members)!=103 or len(group_round_roster)!=1030:
        raise SourceGateError("R105_B_TRUE_ORIGINAL_412_PEOPLE_103_GROUPS_UNIVERSE_NOT_ESTABLISHED")
    labels={tr:f"condition_{i+1}" for i,tr in enumerate(sorted(treatment_people))}
    anonymized_treatments=[{
      "source_anonymous_condition":labels[tr],
      "original_individuals":len(treatment_people[tr]),
      "original_fixed_four_person_groups":len(treatment_groups[tr]),
      "source_actor_round_rows":len(treatment_people[tr])*10,
    } for tr in sorted(treatment_people)]
    return {
        "research_id":"R105","phase":"B",
        "status":"R105_ACTUAL_ORIGINAL_412_PERSON_103_FOURPERSON_FIXED_GROUP_TENROUND_ROSTER_ONLY",
        "full_original_publisher_md5_verified":True,
        "whole_original_SHA256":ORIGINAL_SHA,
        "original_actor_round_rows":rows,
        "original_people_by_treatment_ID":len(person_rounds),
        "original_fixed_group_identity_count":len(group_permanent_members),
        "original_ten_round_group_combinations":len(group_round_roster),
        "original_treatment_count":len(treatment_people),
        "anonymized_original_treatment_counts":anonymized_treatments,
        "source_original_group_size_histogram":dict(sorted(Counter(len(p) for p in group_permanent_members.values()).items())),
        "source_original_person_round_count_histogram":dict(sorted(Counter(len(x) for x in person_rounds.values()).items())),
        "repeated_player_id_string_across_treatments_count":sum(len(t)-1 for t in player_treatments.values() if len(t)>1),
        "independent_original_lab_session_column_present":False,
        "eligible_holdout_unit":"whole original fixed group only, not entire independent laboratory session",
        "raw_human_player_group_or_treatment_codes_exported":False,
        "any_original_extraction_payoff_or_demographic_cell_dereferenced":False,
        "actual_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",required=True,type=pathlib.Path)
    args=a.parse_args()
    try:
        validate_url(SOURCE_URL)
        req=urllib.request.Request(SOURCE_URL,headers={"User-Agent":"Psychohistory-R105-B-Zenodo-Only-Group-Person-Roster/1.0"})
        with urllib.request.build_opener(OnlyExactPublisherRedirect()).open(req,timeout=55) as resp:
            validate_url(resp.geturl())
            raw=resp.read(CAP+1)
        result=original_nonbehavior_roster(raw)
    except (OSError,ValueError,TypeError,KeyError,UnicodeError,csv.Error) as exc:
        result={"research_id":"R105","phase":"B",
                "status":"R105_B_ORIGINAL_NONBEHAVIOR_ROSTER_FAIL_CLOSED",
                "safe_failure":str(exc) if isinstance(exc,SourceGateError) else "R105_B_SOURCE_IDENTITY_UNVERIFIED",
                "actual_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R105_ACTUAL_ORIGINAL_412_PERSON_103_FOURPERSON_FIXED_GROUP_TENROUND_ROSTER_ONLY":
        raise SystemExit(1)
if __name__=="__main__":main()
