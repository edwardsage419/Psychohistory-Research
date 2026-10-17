#!/usr/bin/env python3
"""R102 B original source session/person/group/round ONLY, no contribution values."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import csv
import io
import json
import pathlib
import re
import urllib.request

from r102_2025_original_climateclubs_zenodo_publisher_md5_header_only import (
    URL, CAP, EXPECTED_HEADER, SafeRedirect, SourceError,
    source_identity_header_only, validate_url
)

PINNED_SHA256="ebc8831011a1a3b4893a80ae158d5129ed0f35e57a8092eba36c6a7b0cbd4282"
LABEL=re.compile(r"[A-Za-z0-9_.-]{1,80}")
IDENTITY_COLS=("session.code","participant.code","participant.id_in_session",
               "participant._round_number","subsession.round_number",
               "group.id_in_subsession","group","player.id_in_group","treatment")

def require_tag(x):
    if not isinstance(x,str) or not LABEL.fullmatch(x):
        raise SourceError("R102_B_SOURCE_IDENTITY_TAG_INVALID")
    return x

def natural_int(x,maximum=100000):
    if not isinstance(x,str) or not x.isascii() or not x.isdecimal():
        raise SourceError("R102_B_SOURCE_INTEGER_ID_INVALID")
    number=int(x)
    if not 1<=number<=maximum:
        raise SourceError("R102_B_SOURCE_INTEGER_RANGE_INVALID")
    return number

def parse_nonbehavior_roster(raw):
    signed=source_identity_header_only(raw)
    if signed["actual_original_full_SHA256"]!=PINNED_SHA256:
        raise SourceError("R102_B_FROZEN_FULL_ORIGINAL_SHA256_MISMATCH")
    try:
        stream=io.StringIO(raw.decode("utf-8-sig"),newline="")
    except UnicodeError as exc:
        raise SourceError("R102_B_ORIGINAL_UTF8_INVALID") from exc
    reader=csv.DictReader(stream)
    if tuple(reader.fieldnames or [])!=EXPECTED_HEADER:
        raise SourceError("R102_B_ACTUAL_HEADER_CHANGED")
    # CSV parser allocates transient row values. Only nonbehavior fields
    # explicitly listed here are ever dereferenced, aggregated or retained.
    records=0
    session_treatment={}
    sess_people=defaultdict(dict)
    code_sessions=defaultdict(set)
    person_rounds=defaultdict(set)
    group_members=defaultdict(set)
    group_positions=defaultdict(set)
    seen_person_round=set()
    session_rounds=defaultdict(set)
    technical_round_mismatches=0
    for row in reader:
        records+=1
        if records>2700 or None in row:
            raise SourceError("R102_B_ACTUAL_ROW_STRUCTURE_INVALID")
        source={k:row[k] for k in IDENTITY_COLS}
        session=require_tag(source["session.code"])
        person=require_tag(source["participant.code"])
        group_name=require_tag(source["group"])
        tr=require_tag(source["treatment"])
        group_idx=natural_int(source["group.id_in_subsession"])
        pos=natural_int(source["player.id_in_group"])
        session_id=natural_int(source["participant.id_in_session"])
        roundnum=natural_int(source["subsession.round_number"],maximum=100)
        # oTree's participant._round_number may be a final participant snapshot.
        # The source subsession.round_number is the only behavioral round key.
        if natural_int(source["participant._round_number"],maximum=100)!=roundnum:
            technical_round_mismatches+=1
        if session in session_treatment and session_treatment[session]!=tr:
            raise SourceError("R102_B_TREATMENT_MIXED_WITHIN_ORIGINAL_SESSION")
        session_treatment[session]=tr
        per=(session,person)
        if (per,roundnum) in seen_person_round:
            raise SourceError("R102_B_ORIGINAL_PERSON_ROUND_DUPLICATE")
        seen_person_round.add((per,roundnum))
        old=sess_people[session].get(person)
        if old is not None and old!=session_id:
            raise SourceError("R102_B_PERSON_ID_IN_SESSION_CHANGED")
        sess_people[session][person]=session_id
        code_sessions[person].add(session)
        session_rounds[session].add(roundnum)
        person_rounds[per].add(roundnum)
        group_key=(session,roundnum,group_idx,group_name)
        if pos in group_positions[group_key]:
            raise SourceError("R102_B_PLAYER_POSITION_DUPLICATED_WITHIN_GROUP")
        group_positions[group_key].add(pos)
        if person in group_members[group_key]:
            raise SourceError("R102_B_PERSON_DUPLICATED_WITHIN_GROUP")
        group_members[group_key].add(person)
    if records!=2700:
        raise SourceError("R102_B_WRONG_ORIGINAL_ROWS")
    for session,members in sess_people.items():
        if len(set(members.values()))!=len(members):
            raise SourceError("R102_B_SOURCE_PERSON_NUMERIC_ID_REUSED_WITHIN_SESSION")
    group_sizes=Counter(len(members) for members in group_members.values())
    if any(n<2 for n in group_sizes):
        raise SourceError("R102_B_SINGLE_ACTOR_GROUP_INVALID_FOR_PEER_HISTORY")
    contiguous_person=sum(1 for rounds in person_rounds.values() if rounds==set(range(1,max(rounds)+1)))
    contiguous_session=sum(1 for rounds in session_rounds.values() if rounds==set(range(1,max(rounds)+1)))
    actor_count=len(person_rounds)
    treatment_sessions=Counter(session_treatment.values())
    source_identity_collisions=sum(len(sessions)-1 for sessions in code_sessions.values() if len(sessions)>1)
    return {
        "research_id":"R102","phase":"B",
        "status":"R102_FIRSTPARTY_REAL_SOURCE_SESSION_PERSON_GROUP_ROUND_ROSTER_AUDITED_ONLY",
        "official_whole_source_SHA256":PINNED_SHA256,
        "original_actual_person_round_rows":records,
        "original_session_count":len(session_treatment),
        "anonymous_source_person_per_session_count":actor_count,
        "source_distinct_participant_code_count":len(code_sessions),
        "original_participant_codes_reused_across_sessions_count":source_identity_collisions,
        "original_anonymous_treatment_session_counts":dict(sorted(treatment_sessions.items())),
        "original_session_round_count_histogram":dict(sorted(Counter(len(x) for x in session_rounds.values()).items())),
        "original_group_size_histogram":dict(sorted(group_sizes.items())),
        "original_distinct_session_round_group_keys":len(group_members),
        "technical_participant_round_disagrees_with_actual_subsession_round_rows":technical_round_mismatches,
        "all_people_have_contiguous_1_to_last_round":contiguous_person==actor_count,
        "number_people_with_contiguous_rounds":contiguous_person,
        "all_source_sessions_have_contiguous_rounds":contiguous_session==len(session_rounds),
        "all_source_groups_at_least_2_members":all(n>=2 for n in group_sizes),
        "real_human_contribution_values_dereferenced":0,
        "raw_person_group_session_IDs_exported":False,
        "actual_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",type=pathlib.Path,required=True)
    x=a.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R102-B-Source-Nonbehavior-Roster-Only/1.0"})
        with urllib.request.build_opener(SafeRedirect()).open(req,timeout=55) as response:
            validate_url(response.geturl())
            data=response.read(CAP+1)
        result=parse_nonbehavior_roster(data)
    except (OSError,ValueError,TypeError,KeyError,UnicodeError,csv.Error) as e:
        result={"research_id":"R102","phase":"B",
                "status":"R102_B_ORIGINAL_ROSTER_SOURCE_FAIL_CLOSED",
                "safe_failure":str(e) if isinstance(e,SourceError) else "R102_B_SOURCE_IDENTITY_UNVERIFIED",
                "actual_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R102_FIRSTPARTY_REAL_SOURCE_SESSION_PERSON_GROUP_ROUND_ROSTER_AUDITED_ONLY":
        raise SystemExit(1)

if __name__=="__main__":
    main()
