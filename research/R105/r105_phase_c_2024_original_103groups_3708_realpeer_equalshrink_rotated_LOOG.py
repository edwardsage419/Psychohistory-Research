#!/usr/bin/env python3
"""R105 C original 2024 CPR exact 103 fixed-group LOOG, matched shrinkage controls.

This file is allowed to read real extraction only after frozen Phase C protocol.
Never export raw persons, group keys, action rows, treatment labels or demographics.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import csv
import io
import json
import math
import pathlib
import urllib.request

from r105_phase_a_original_2024_cpr_defaults_zenodo_md5_header_only import (
    SOURCE_URL,CAP,OnlyExactPublisherRedirect,SourceGateError,validate_url
)
from r105_phase_b_2024_original_cpr_actor_group_round_nonbehavior_roster import (
    ORIGINAL_SHA,identity,game_round,original_nonbehavior_roster
)

MODELS=("M0","M1","M2","M3","M4")
CONTRASTS=(
    ("M2","M3","M3_vs_M2_matched_shrinkage"),
    ("M4","M3","M3_vs_M4_rotated_group"),
    ("M1","M3","M3_vs_M1_own_only"),
    ("M0","M3","M3_vs_M0_external"),
    ("M0","M1","M1_vs_M0_external"),
)
TARGETS=3708
ROWS=4120

def normalized_extraction(x):
    try:
        f=float(x)
    except (ValueError,TypeError) as exc:
        raise SourceGateError("R105_C_ORIGINAL_EXTRACTION_NOT_NUMERIC") from exc
    if not math.isfinite(f) or not f.is_integer() or not (1<=f<=30):
        raise SourceGateError("R105_C_ORIGINAL_EXTRACTION_OUTSIDE_AUTHOR_INTEGER_1_TO_30")
    return f/30.0

def source_observations(raw):
    roster=original_nonbehavior_roster(raw)
    if (roster["original_actor_round_rows"]!=ROWS
        or roster["original_people_by_treatment_ID"]!=412
        or roster["original_fixed_group_identity_count"]!=103
        or roster["original_ten_round_group_combinations"]!=1030
        or roster["source_original_group_size_histogram"]!={4:103}):
        raise SourceGateError("R105_C_SOURCE_PERSON_GROUP_UNIVERSE_NOT_VERIFIED")
    reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""),strict=True)
    outcomes={}
    memberships=defaultdict(set)
    group_by_person={}
    treatment_groups=defaultdict(set)
    for row in reader:
        tr=identity(row["Treatment"])
        person=identity(row["player_id"])
        group=identity(row["group_id"])
        t=game_round(row["round"])
        source_group=(tr,group)
        k=(tr,person,t)
        if k in outcomes:
            raise SourceGateError("R105_C_DUPLICATE_PERSON_ROUND")
        outcomes[k]=normalized_extraction(row["extraction"])
        memberships[source_group].add(person)
        treatment_groups[tr].add(source_group)
        group_by_person[(tr,person)]=source_group
    if len(outcomes)!=ROWS or len(memberships)!=103:
        raise SourceGateError("R105_C_SOURCE_EXTRACTION_COHORT_UNIVERSE_INVALID")
    for g,persons in memberships.items():
        if len(persons)!=4 or any((g[0],p,t) not in outcomes for p in persons for t in range(1,11)):
            raise SourceGateError("R105_C_REAL_FOUR_PERSON_PREVIOUS_GROUP_INCOMPLETE")
    return outcomes,memberships,treatment_groups,roster

def summary(items):
    n=len(items)
    if not n:
        return {"target_count":0,"MSE":{k:None for k in MODELS},
                "gains":{label:None for _,_,label in CONTRASTS}}
    mse={name:math.fsum(x["loss"][name] for x in items)/n for name in MODELS}
    gains={label:mse[ref]-mse[candidate] for ref,candidate,label in CONTRASTS}
    return {"target_count":n,"MSE":mse,"gains":gains}

def source_score(raw):
    outcomes,groups,treatments,roster=source_observations(raw)
    label={tr:f"condition_{i+1}" for i,tr in enumerate(sorted(treatments))}
    allrows=[]
    group_reports=[]
    for tr in sorted(treatments):
        original_group_ids=sorted(treatments[tr])
        if len(original_group_ids)<2:
            raise SourceGateError("R105_C_EXTERNAL_SAME_CONDITION_GROUP_REFERENCES_MISSING")
        for j,g in enumerate(original_group_ids):
            donor=original_group_ids[(j+1)%len(original_group_ids)]
            if donor==g:
                raise SourceGateError("R105_C_ROTATED_CONTROL_SOURCE_GROUP_EQUALS_TARGET")
            source_peers=sorted(groups[g])
            external_groups=[other for other in original_group_ids if other!=g]
            for t in range(2,11):
                # All external source references deliberately exclude the held-out
                # group g in both previous and contemporaneous rounds.
                external_curr=math.fsum(outcomes[(tr,p,t)] for h in external_groups for p in sorted(groups[h]))/(4*len(external_groups))
                external_prev=math.fsum(outcomes[(tr,p,t-1)] for h in external_groups for p in sorted(groups[h]))/(4*len(external_groups))
                other_prev=math.fsum(outcomes[(tr,p,t-1)] for p in sorted(groups[donor]))/4
                for person in source_peers:
                    partner_history=math.fsum(outcomes[(tr,peer,t-1)] for peer in source_peers if peer!=person)/3
                    own_prev=outcomes[(tr,person,t-1)]
                    prediction={
                        "M0":external_curr,
                        "M1":own_prev,
                        "M2":0.5*own_prev+0.5*external_prev,
                        "M3":0.5*own_prev+0.5*partner_history,
                        "M4":0.5*own_prev+0.5*other_prev,
                    }
                    if any(not 0<=v<=1 for v in prediction.values()):
                        raise SourceGateError("R105_C_SOURCE_PREDICTION_OUTSIDE_NORMALIZED_DOMAIN")
                    y=outcomes[(tr,person,t)]
                    loss={name:(y-prediction[name])**2 for name in MODELS}
                    allrows.append({"group":g,"condition":label[tr],"t":t,"loss":loss})
    if len(allrows)!=TARGETS:
        raise SourceGateError("R105_C_TRUE_3708_IDENTICAL_OUTCOME_TARGETS_NOT_PRESENT")
    for tr in sorted(treatments):
        for g in sorted(treatments[tr]):
            rows=[x for x in allrows if x["group"]==g]
            if len(rows)!=36:
                raise SourceGateError("R105_C_SOURCE_GROUP_NOT_EXACTLY_36_TARGETS")
            group_reports.append({"condition":label[tr],"metrics":summary(rows)})
    all_summary=summary(allrows)
    treatment_summaries=[]
    for tr in sorted(treatments):
        cond=label[tr]
        row_subset=[x for x in allrows if x["condition"]==cond]
        group_subset=[g["metrics"] for g in group_reports if g["condition"]==cond]
        direction={
            name:{
               "positive_original_groups":sum(g["gains"][name]>0 for g in group_subset),
               "negative_original_groups":sum(g["gains"][name]<0 for g in group_subset),
               "zero_original_groups":sum(g["gains"][name]==0 for g in group_subset),
            } for _,_,name in CONTRASTS
        }
        treatment_summaries.append({
            "source_anonymous_treatment":cond,
            "original_group_count":len(group_subset),
            "scored_actor_round_targets":len(row_subset),
            "all_recorded":summary(row_subset),
            "source_original_group_effect_direction_counts":direction,
        })
    group_effects={}
    for _,_,name in CONTRASTS:
        vals=[g["metrics"]["gains"][name] for g in group_reports]
        group_effects[name]={
            "positive_groups":sum(v>0 for v in vals),
            "negative_groups":sum(v<0 for v in vals),
            "zero_groups":sum(v==0 for v in vals),
            "minimum_group_gain":min(vals),
            "median_group_gain":sorted(vals)[len(vals)//2],
            "maximum_group_gain":max(vals),
        }
    result={
        "research_id":"R105","phase":"C",
        "status":"R105_ACTUAL_HUMAN_103_ORIGINAL_FOURPERSON_GROUP_3708_LOOG_M01234_E2",
        "source_whole_publisher_MD5":"a3afbb4e52179a0e1d8b1b533f076cc9",
        "source_full_SHA256":ORIGINAL_SHA,
        "original_source_people":412,
        "original_source_complete_groups":103,
        "original_actor_round_source_rows":4120,
        "original_next_actor_round_targets_same_for_all_five_models":len(allrows),
        "model_contract":{
            "M0":"other groups same treatment target t contemporaneous mean retrospective benchmark",
            "M1":"focal person's own previous-round normalized extraction",
            "M2":"0.5 M1 + 0.5 mean of all other source groups same treatment t-1",
            "M3":"0.5 M1 + 0.5 actual previous three original partners' mean t-1",
            "M4":"0.5 M1 + 0.5 next cyclic group in same treatment prior t-1",
        },
        "MSE_smaller_is_better":True,
        "all_recorded_t2_to_t10":all_summary,
        "early_target_t2_to_t5":summary([x for x in allrows if 2<=x["t"]<=5]),
        "transition_target_t6":summary([x for x in allrows if x["t"]==6]),
        "late_target_t7_to_t10":summary([x for x in allrows if 7<=x["t"]<=10]),
        "anonymous_source_treatment_summaries":treatment_summaries,
        "original_source_group_gain_directions":group_effects,
        "whole_original_group_held_out":"one original four-person group at all ten rounds",
        "independent_original_lab_session_column_present":False,
        "raw_original_person_group_treatment_or_action_rows_exported":False,
        "equal_shrinkage_weight_in_M2_and_M3":0.5,
        "no_after_outcome_model_selection":True,
        "not_prospective_E3_or_causal_social_learning":True,
        "PESEN_v0_1":"FROZEN",
    }
    if (result["early_target_t2_to_t5"]["target_count"]!=1648
        or result["transition_target_t6"]["target_count"]!=412
        or result["late_target_t7_to_t10"]["target_count"]!=1648):
        raise SourceGateError("R105_C_PREDECLARED_DEFAULT_STAGE_WINDOWS_NOT_MATCHED")
    return result

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=pathlib.Path)
    x=p.parse_args()
    try:
        validate_url(SOURCE_URL)
        req=urllib.request.Request(SOURCE_URL,headers={"User-Agent":"Psychohistory-R105-C-FrozenEqualShrinkageTruePeerLOOG/1.0"})
        with urllib.request.build_opener(OnlyExactPublisherRedirect()).open(req,timeout=55) as response:
            validate_url(response.geturl())
            raw=response.read(CAP+1)
        result=source_score(raw)
    except (OSError,ValueError,TypeError,KeyError,UnicodeError,csv.Error) as exc:
        result={"research_id":"R105","phase":"C","status":"R105_C_ACTUAL_HUMAN_E2_FAIL_CLOSED",
                "safe_failure":str(exc) if isinstance(exc,SourceGateError) else "R105_C_ORIGINAL_HUMAN_SCORE_NOT_ESTABLISHED",
                "actual_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R105_ACTUAL_HUMAN_103_ORIGINAL_FOURPERSON_GROUP_3708_LOOG_M01234_E2":raise SystemExit(1)
if __name__=="__main__":main()
