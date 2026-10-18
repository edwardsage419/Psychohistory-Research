#!/usr/bin/env python3
"""R106 C2: origin-md5 2025 cohort roster by sessionid + global ID, before actions.

StataReader reads binary rows internally, while this application selects
nonbehavior columns only; never inspect left/otherleft/p2otherleft.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import io
import json
import math
import pathlib
import re
import urllib.request

from r106_phase_a_2025_drouvelis_pearce_zenodo_original_dta_md5_only import URL,CAP,ExactRedirect,SourceError,validate_url
from r106_phase_b_2025_publisher_dta_header_variables_nobs_only import metadata_only,PINNED_SHA256

FIELDS=("sessionid","ID","Subject","Group","Period","part","game","practiceperiod","Session")
NROWS=3620
NVARS=148

def pos_int(v):
    try:
        n=float(v)
    except (TypeError,ValueError,OverflowError):
        return None
    if not math.isfinite(n) or not 1<=n<=1000000000 or not n.is_integer():
        return None
    return int(n)

def session_alias(x):
    if not isinstance(x,str):
        return None
    x=x.strip()
    if not 1<=len(x)<=40 or not x.isascii() or re.fullmatch(r"[0-9]+(?:\.[0-9]+)?",x) is None:
        return None
    return x

def source_true_roster(raw):
    header=metadata_only(raw)
    if header["Stata_header_observation_count_unverified_human_rows"]!=NROWS or header["Stata_header_variable_count"]!=NVARS or not set(FIELDS).issubset(header["Stata_header_allowlisted_variable_names"]):
        raise SourceError("R106_C2_TRUE_ORIGINAL_SOURCE_ROSTER_COLUMNS_UNVERIFIED")
    from pandas.io.stata import StataReader
    try:
        with StataReader(io.BytesIO(raw),convert_categoricals=False) as reader:
            frame=reader.read(columns=list(FIELDS),convert_categoricals=False,convert_dates=False)
    except (ValueError,TypeError,UnicodeError,OSError,IndexError) as exc:
        raise SourceError("R106_C2_ACTUAL_STATA_SOURCE_ROW_SELECTION_FAILED") from exc
    if len(frame)!=NROWS or set(frame.columns)!=set(FIELDS):
        raise SourceError("R106_C2_SELECTED_SOURCE_SCHEME_OR_LENGTH_CHANGED")
    frame=frame.loc[:,list(FIELDS)]
    sessions=defaultdict(set)
    session_person_subject=defaultdict(set)
    session_subject_person=defaultdict(set)
    global_person_sessions=defaultdict(set)
    alias_per_session=defaultdict(set)
    sessions_per_alias=defaultdict(set)
    pairs=defaultdict(list)
    person_period_counts=Counter()
    session_person_round_count=Counter()
    stage_rows=Counter()
    rejected_rows=0
    rows_with_unavailable_alias=0
    for record in frame.itertuples(index=False,name=None):
        item=dict(zip(FIELDS,record))
        sid=pos_int(item["sessionid"])
        pid=pos_int(item["ID"])
        subject=pos_int(item["Subject"])
        group=pos_int(item["Group"])
        period=pos_int(item["Period"])
        stage=pos_int(item["part"])
        alias=session_alias(item["Session"])
        stage_rows[str(stage) if stage is not None and stage<=20 else "missing_or_other"]+=1
        if None in (sid,pid,subject,group,period,stage):
            rejected_rows+=1
            continue
        if alias is None:
            rows_with_unavailable_alias+=1
        else:
            alias_per_session[sid].add(alias)
            sessions_per_alias[alias].add(sid)
        sessions[sid].add(pid)
        session_person_subject[(sid,pid)].add(subject)
        session_subject_person[(sid,subject)].add(pid)
        global_person_sessions[pid].add(sid)
        person_period_counts[(sid,pid,period)]+=1
        session_person_round_count[(sid,pid)]+=1
        if stage==2:
            pairs[(sid,group,period)].append(pid)
    eligible_events=0
    eligible_source_rows=0
    pair_size=Counter()
    repeated_person_key=0
    for members in pairs.values():
        pair_size[len(members)]+=1
        if len(members)==2 and len(set(members))==2:
            eligible_events+=1
            eligible_source_rows+=2
        if len(set(members))!=len(members):
            repeated_person_key+=1
    per_session_people_counts=Counter(map(len,sessions.values()))
    participants=len(global_person_sessions)
    original_sessions=len(sessions)
    unique_src_part2=stage_rows["2"]
    collisions=sum(len(k)-1 for k in global_person_sessions.values() if len(k)>1)
    duplicate_actor_period=sum(n-1 for n in person_period_counts.values() if n>1)
    subject_mapping_conflicts=sum(len(x)>1 for x in session_person_subject.values())+sum(len(x)>1 for x in session_subject_person.values())
    pair_fraction=eligible_source_rows/unique_src_part2 if unique_src_part2 else 0.0
    min_sessions_with_pairs=len({k[0] for k,x in pairs.items() if len(x)==2 and len(set(x))==2})
    source_eligible=(
        original_sessions==26 and participants==260
        and per_session_people_counts==Counter({10:26})
        and collisions==0 and rejected_rows==0 and duplicate_actor_period==0
        and subject_mapping_conflicts==0 and pair_fraction>=0.95
        and min_sessions_with_pairs>=24
    )
    return {
        "research_id":"R106","phase":"C2",
        "status":("R106_C2_GENUINE_2025_RECRUITED_26SESSION_260_ID_SOURCE_DYADS_ELIGIBLE" if source_eligible
                  else "R106_C2_BOUNDED_2025_SOURCE_DYAD_ROSTER_INELIGIBLE"),
        "original_whole_study_SHA256":PINNED_SHA256,
        "original_full_source_rows":NROWS,
        "original_sessions_by_numeric_sessionid":original_sessions,
        "original_unique_global_ID_people":participants,
        "source_session_persons_count_histogram":dict(sorted((str(k),v) for k,v in per_session_people_counts.items())),
        "source_part_task_record_counts":dict(sorted(stage_rows.items())),
        "source_rows_with_missing_or_invalid_true_person_pair_fields":rejected_rows,
        "source_Session_string_alias_missing_or_unrecognized_rows":rows_with_unavailable_alias,
        "source_Session_string_aliases_shared_across_different_real_sessionid_count":sum(len(v)>1 for v in sessions_per_alias.values()),
        "source_real_sessionid_with_multiple_Session_string_alias_count":sum(len(v)>1 for v in alias_per_session.values()),
        "source_global_ID_codes_reused_between_sessions":collisions,
        "source_session_person_Subject_mapping_conflict_count":subject_mapping_conflicts,
        "original_person_period_key_duplicate_record_count":duplicate_actor_period,
        "source_distinct_paired_group_period_candidates":len(pairs),
        "source_group_period_row_size_histogram":dict(sorted((str(k),v) for k,v in pair_size.items())),
        "source_group_period_keys_with_same_ID_repeated":repeated_person_key,
        "candidate_true_two_distinct_person_group_period_events":eligible_events,
        "source_part2_actor_rows_in_true_candidate_pairs":eligible_source_rows,
        "source_part2_all_actor_rows":unique_src_part2,
        "candidate_source_part2_row_pair_coverage":pair_fraction,
        "source_sessions_with_any_exact_two_ID_candidate_pair":min_sessions_with_pairs,
        "source_identity_and_candidate_pair_gate_passed":source_eligible,
        "original_human_source_action_columns_application_accessed":False,
        "Stata_reader_internally_decodes_source_rows":True,
        "raw_person_session_pair_ID_values_exported":False,
        "real_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=pathlib.Path)
    args=p.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R106-C2-Author-2025-True26Session260Person-NoBehavior/1.0"})
        with urllib.request.build_opener(ExactRedirect()).open(req,timeout=65) as response:
            validate_url(response.geturl())
            raw=response.read(CAP+1)
        result=source_true_roster(raw)
    except (ValueError,TypeError,KeyError,OSError,ImportError) as e:
        result={"research_id":"R106","phase":"C2","status":"R106_C2_SOURCE_IDENTITY_FAIL_CLOSED",
                "safe_failure":str(e) if isinstance(e,SourceError) else "R106_C2_ORIGINAL_PERSON_GROUP_SESSION_SOURCE_NOT_VERIFIED",
                "real_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R106_C2_GENUINE_2025_RECRUITED_26SESSION_260_ID_SOURCE_DYADS_ELIGIBLE":
        raise SystemExit(1)

if __name__=="__main__":
    main()
