#!/usr/bin/env python3
"""R106 C: genuine original 2025 Stata nonbehavior session-person-pair-period census.

pandas may internally decode source row records, but application selects ONLY
whitelisted nonbehavior columns. No original 'left', 'otherleft', 'p2otherleft'.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import io
import json
import math
import pathlib
import urllib.request

from r106_phase_a_2025_drouvelis_pearce_zenodo_original_dta_md5_only import (
    URL,CAP,SourceError,ExactRedirect,validate_url
)
from r106_phase_b_2025_publisher_dta_header_variables_nobs_only import (
    PINNED_SHA256,metadata_only
)

WHITELIST=(
    "Session","Subject","ID","sessionid","Group","Period",
    "part","game","practiceperiod","realround","realperiod","practiceround"
)
EXPECTED_NOBS=3620
EXPECTED_VARS=148

def as_id(v):
    try:
        x=float(v)
    except (ValueError,TypeError,OverflowError):
        return None
    if not math.isfinite(x) or x<0 or x>1000000000 or not x.is_integer():
        return None
    return int(x)

def source_roster_only(raw):
    metadata=metadata_only(raw)
    if (metadata["Stata_header_variable_count"]!=EXPECTED_VARS or
        metadata["Stata_header_observation_count_unverified_human_rows"]!=EXPECTED_NOBS or
        not set(WHITELIST).issubset(metadata["Stata_header_allowlisted_variable_names"])):
        raise SourceError("R106_C_FROZEN_ORIGINAL_HEADER_ID_COLUMN_UNIVERSE_MISMATCH")
    from pandas.io.stata import StataReader
    try:
        with StataReader(io.BytesIO(raw),convert_categoricals=False) as r:
            # StataReader.read internally decodes records, but the returned table
            # is constrained to nonbehavior source identity columns only.
            frame=r.read(columns=list(WHITELIST),convert_categoricals=False,convert_dates=False)
    except (ValueError,TypeError,IndexError,OverflowError,UnicodeError,OSError) as exc:
        raise SourceError("R106_C_STATA_NONBEHAVIOR_IDENTITY_DECODER_FAILED") from exc
    if len(frame)!=EXPECTED_NOBS or set(frame.columns)!=set(WHITELIST):
        raise SourceError("R106_C_STATA_SELECTED_SOURCE_ROWS_OR_ID_COLUMN_MISMATCH")
    sessions=defaultdict(set)
    part2_sessions=defaultdict(set)
    seen=Counter()
    id_to_session=defaultdict(set)
    observed_pairs=defaultdict(list)
    part2_pairs=defaultdict(list)
    partcounts=Counter()
    invalid_match=0
    invalid_person=0
    anonymous_game_ids=set()
    technical_round_presence=Counter()
    for row in frame.itertuples(index=False,name=None):
        v=dict(zip(WHITELIST,row))
        ids={k:as_id(v[k]) for k in WHITELIST}
        s,p,g,t,part=ids["Session"],ids["Subject"],ids["Group"],ids["Period"],ids["part"]
        partcounts[str(part) if part is not None and part<=20 else "missing_or_other"]+=1
        game=ids["game"]
        if game is not None:
            anonymous_game_ids.add(game)
        technical_round_presence["practiceperiod_present" if ids["practiceperiod"] is not None else "practiceperiod_missing"]+=1
        technical_round_presence["realperiod_present" if ids["realperiod"] is not None else "realperiod_missing"]+=1
        if s is not None and p is not None:
            sessions[s].add(p)
            seen[(s,p)]+=1
            if part==2:
                part2_sessions[s].add(p)
        else:
            invalid_person+=1
        id_val=ids["ID"]
        if s is not None and id_val is not None:
            id_to_session[id_val].add(s)
        if None in (s,p,g,t):
            invalid_match+=1
        else:
            key=(s,g,t)
            observed_pairs[key].append(p)
            if part==2:
                part2_pairs[key].append(p)
    def pair_census(mapping):
        hist=Counter(len(x) for x in mapping.values())
        complete=sum(len(x) for x in mapping.values() if len(x)==2 and len(set(x))==2)
        complete_groups=sum(1 for x in mapping.values() if len(x)==2 and len(set(x))==2)
        repeat=sum(1 for x in mapping.values() if len(x)!=len(set(x)))
        return {
            "anonymized_pair_source_key_count":len(mapping),
            "group_record_count_histogram":dict(sorted((str(k),v) for k,v in hist.items())),
            "exact_two_distinct_person_pair_keys":complete_groups,
            "source_actor_rows_in_exact_two_person_pairs":complete,
            "source_keys_with_repeated_person":repeat,
        }
    total_part2=partcounts["2"]
    all_census=pair_census(observed_pairs)
    part2_census=pair_census(part2_pairs)
    return {
        "research_id":"R106","phase":"C",
        "status":"R106_C_ORIGINAL_STATA_NONBEHAVIOR_2025_SESSION_DYAD_ROSTER_CENSUS_ONLY",
        "original_source_DOI":"10.5281/zenodo.15462528",
        "original_full_source_SHA256":PINNED_SHA256,
        "original_data_frame_rows_header_verified":len(frame),
        "original_stata_column_count":EXPECTED_VARS,
        "original_source_distinct_session_labels":len(sessions),
        "original_distinct_source_session_subject_pairs":len(seen),
        "original_distinct_source_session_subject_pairs_part2":sum(len(v) for v in part2_sessions.values()),
        "source_persons_per_session_histogram":dict(sorted(Counter(map(len,sessions.values())).items())),
        "source_session_person_pairs_with_multiple_rows":sum(v>1 for v in seen.values()),
        "source_ID_codes_reused_across_source_sessions":sum(len(v)>1 for v in id_to_session.values()),
        "source_part_category_row_counts":dict(sorted(partcounts.items())),
        "source_distinct_game_code_count_only":len(anonymous_game_ids),
        "source_missing_session_or_subject_source_rows":invalid_person,
        "source_rows_not_eligible_for_group_period_pair_key":invalid_match,
        "source_technical_round_field_completeness_counts":dict(sorted(technical_round_presence.items())),
        "all_part_source_pair_coverage":all_census,
        "part2_only_source_pair_coverage":part2_census,
        "part2_source_actor_rows":total_part2,
        "part2_original_source_pair_eligible_actor_fraction":(
            part2_census["source_actor_rows_in_exact_two_person_pairs"]/total_part2 if total_part2 else None
        ),
        "article_reported_26_lab_sessions_260_new_people_not_yet_source_reconciled":True,
        "Stata_library_internally_decodes_rows_but_application_retrieves_only_whitelisted_nonbehavior_fields":True,
        "original_choice_own_partner_or_prior_partner_columns_application_accessed":False,
        "source_raw_person_session_group_identifiers_exported":False,
        "original_human_model_scores":0,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=pathlib.Path)
    args=p.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R106-C-2025-Original-Stata-NonBehavior-RosterOnly/1.0"})
        with urllib.request.build_opener(ExactRedirect()).open(req,timeout=65) as response:
            validate_url(response.geturl())
            raw=response.read(CAP+1)
        out=source_roster_only(raw)
    except (ValueError,TypeError,OSError,KeyError,ImportError) as e:
        out={
            "research_id":"R106","phase":"C",
            "status":"R106_C_ORIGINAL_STATA_NONBEHAVIOR_ROSTER_FAIL_CLOSED",
            "safe_failure":str(e) if isinstance(e,SourceError) else "R106_C_ORIGINAL_SOURCE_SESSION_DYAD_UNVERIFIED",
            "original_human_model_scores":0,
            "PESEN_v0_1":"FROZEN",
        }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(out,sort_keys=True))
    if out["status"]!="R106_C_ORIGINAL_STATA_NONBEHAVIOR_2025_SESSION_DYAD_ROSTER_CENSUS_ONLY":
        raise SystemExit(1)
if __name__=="__main__":
    main()
