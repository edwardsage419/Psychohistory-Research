#!/usr/bin/env python3
"""R102 C: exact 8 original sessions LOSO, fixed M0/M1/M2/M3 contribution shares.

Outcome access is permitted only after source A2, roster B2 and separate C
prescore protocol have been archived. Never export raw actor/group/session IDs.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
import csv
import io
import json
import math
import pathlib
import urllib.request

from r102_2025_original_climateclubs_zenodo_publisher_md5_header_only import (
    URL,CAP,EXPECTED_HEADER,SafeRedirect,SourceError,validate_url
)
from r102_phase_b_original_climateclubs_person_session_round_group_roster_only import (
    PINNED_SHA256,parse_nonbehavior_roster,natural_int,require_tag
)

MODELS=("M0","M1","M2","M3")
DIFFS=(("M0","M1","M1_vs_M0"),("M0","M2","M2_vs_M0"),
       ("M1","M3","M3_vs_M1"),("M0","M3","M3_vs_M0"))

def read_fraction(value):
    try:
        n=float(value)
    except (TypeError,ValueError) as exc:
        raise SourceError("R102_C_NONNUMERIC_ENDOWMENT_OR_CONTRIBUTION") from exc
    if not math.isfinite(n):
        raise SourceError("R102_C_NONFINITE_ENDOWMENT_OR_CONTRIBUTION")
    return n

def bounded_human_observations(raw):
    # Source integrity, all-actor nonbehavior roster validated before choices.
    roster=parse_nonbehavior_roster(raw)
    if roster["original_actual_person_round_rows"]!=2700 or roster["original_session_count"]!=8 or roster["anonymous_source_person_per_session_count"]!=180 or roster["original_group_size_histogram"]!={6:450}:
        raise SourceError("R102_C_BOUNDED_ORIGINAL_ROSTER_UNIVERSE_NOT_ESTABLISHED")
    if roster["original_participant_codes_reused_across_sessions_count"]!=0:
        raise SourceError("R102_C_INDEPENDENT_SOURCE_PARTICIPANT_COLLISION")
    decoded=raw.decode("utf-8-sig")
    reader=csv.DictReader(io.StringIO(decoded,newline=""))
    if tuple(reader.fieldnames or [])!=EXPECTED_HEADER:
        raise SourceError("R102_C_SOURCE_SCHEMA_CHANGED")
    observations={}
    groups=defaultdict(list)
    sessions=defaultdict(set)
    treatments=defaultdict(set)
    for r in reader:
        sid=require_tag(r["session.code"])
        pid=require_tag(r["participant.code"])
        tr=require_tag(r["treatment"])
        t=natural_int(r["subsession.round_number"],100)
        group=(sid,t,natural_int(r["group.id_in_subsession"]),require_tag(r["group"]))
        g_pos=natural_int(r["player.id_in_group"])
        endowment=read_fraction(r["player.endowment"])
        contribution=read_fraction(r["player.contribution"])
        if endowment<=0 or not (0<=contribution<=endowment):
            raise SourceError("R102_C_ORIGINAL_CONTRIBUTION_ENDOWMENT_BOUNDS_FAIL_CLOSED")
        automatic=r["player.automatic_decision"]
        if automatic not in ("0","1"):
            raise SourceError("R102_C_AUTOMATIC_DECISION_CODEBOOK_INVALID")
        key=(sid,pid,t)
        if key in observations:
            raise SourceError("R102_C_DUPLICATE_ACTOR_ROUND")
        observations[key]={
            "treatment":tr,"group":group,"position":g_pos,
            "share":contribution/endowment,"auto":int(automatic)
        }
        groups[group].append((pid,g_pos))
        sessions[sid].add(pid)
        treatments[tr].add(sid)
    if len(observations)!=2700 or len(sessions)!=8 or len(treatments)!=4 or any(len(s)!=2 for s in treatments.values()):
        raise SourceError("R102_C_ORIGINAL_OBSERVATION_UNIVERSE_MISMATCH")
    for members in groups.values():
        if len(members)!=6 or len({p for p,_ in members})!=6 or len({pos for _,pos in members})!=6:
            raise SourceError("R102_C_INCOMPLETE_OR_DUPLICATE_SIX_PERSON_PEER_GROUP")
    return observations,groups,sessions,treatments,roster

def mean_loss(rows, selector=None):
    chosen=rows if selector is None else [r for r in rows if selector(r)]
    if not chosen:
        return {"target_count":0,"MSE":{k:None for k in MODELS},
                "gains":{name:None for _,_,name in DIFFS}}
    sums={k:math.fsum(r["loss"][k] for r in chosen) for k in MODELS}
    mse={k:sums[k]/len(chosen) for k in MODELS}
    gains={name:mse[base]-mse[alternative] for base,alternative,name in DIFFS}
    return {"target_count":len(chosen),"MSE":mse,"gains":gains}

def real_source_score(raw):
    observations,groups,sessions,treatments,roster=bounded_human_observations(raw)
    # Session identifiers are used internally for deterministic computation,
    # then replaced by anonymous treatment-local slots in all reports.
    anonymous_sessions={}
    for tr in sorted(treatments):
        for i,sid in enumerate(sorted(treatments[tr]),1):
            anonymous_sessions[sid]={"treatment":tr,"anonymous_session_slot_within_treatment":i}
    all_scores=[]
    session_records=[]
    for sid in sorted(sessions,key=lambda x:(anonymous_sessions[x]["treatment"],anonymous_sessions[x]["anonymous_session_slot_within_treatment"])):
        tr=anonymous_sessions[sid]["treatment"]
        training=[x for x in sorted(treatments[tr]) if x!=sid]
        if len(training)!=1:
            raise SourceError("R102_C_SAME_TREATMENT_ONE_OTHER_SOURCE_SESSION_REQUIRED")
        train=training[0]
        # Cross-session source baseline at same round: retrospective, never prospective.
        external={}
        for t in range(2,16):
            shares=[observations[(train,p,t)]["share"] for p in sorted(sessions[train])]
            if not shares:
                raise SourceError("R102_C_EMPTY_TREATMENT_EXTERNAL_REFERENCE")
            external[t]=math.fsum(shares)/len(shares)
        this=[]
        for person in sorted(sessions[sid]):
            for t in range(2,16):
                prev=observations.get((sid,person,t-1))
                now=observations.get((sid,person,t))
                if prev is None or now is None:
                    raise SourceError("R102_C_MISSING_PERSON_ROUND_HISTORY")
                previous_peer_list=groups[prev["group"]]
                peer_ids=sorted(p for p,_ in previous_peer_list if p!=person)
                if len(peer_ids)!=5:
                    raise SourceError("R102_C_PREVIOUS_SIX_PERSON_GROUP_PEER_UNIVERSE_MISSING")
                peer_history=math.fsum(observations[(sid,p,t-1)]["share"] for p in peer_ids)/5
                prior_self=prev["share"]
                preds={"M0":external[t],"M1":prior_self,"M2":peer_history,
                       "M3":0.5*prior_self+0.5*peer_history}
                target=now["share"]
                if any(not 0<=p<=1 for p in preds.values()) or not 0<=target<=1:
                    raise SourceError("R102_C_INVALID_SHARE_OR_PREDICTION_RANGE")
                this.append({"t":t,"manual":now["auto"]==0,
                             "loss":{k:(preds[k]-target)**2 for k in MODELS}})
        if len(this)!=14*len(sessions[sid]):
            raise SourceError("R102_C_ORIGINAL_SESSION_TARGET_COUNT_INVALID")
        all_scores.extend(this)
        session_records.append({
            **anonymous_sessions[sid],
            "source_persons_in_session":len(sessions[sid]),
            "all_recorded":mean_loss(this),
            "manual_target_only":mean_loss(this,lambda r:r["manual"]),
            "early_t2_to_t5":mean_loss(this,lambda r:r["t"]<=5),
            "later_t6_to_t15":mean_loss(this,lambda r:r["t"]>=6),
            "automatic_target_count":sum(not r["manual"] for r in this),
        })
    if len(all_scores)!=2520:
        raise SourceError("R102_C_FROZEN_2520_ORIGINAL_NEXT_ACTION_TARGETS_NOT_FOUND")
    treatment_summaries=[]
    for tr in sorted(treatments):
        # Metrics are rebuilt from session loss values only with explicit equal
        # participant-round count weights. Each source session is still one
        # independent replicate for effect-direction reporting.
        parts=[s for s in session_records if s["treatment"]==tr]
        treatment_summaries.append({
            "source_treatment":tr,
            "true_original_session_count":2,
            "sessions_positive_M3_vs_M1":sum(x["all_recorded"]["gains"]["M3_vs_M1"]>0 for x in parts),
            "sessions_negative_M3_vs_M1":sum(x["all_recorded"]["gains"]["M3_vs_M1"]<0 for x in parts),
            "sessions_positive_M1_vs_M0":sum(x["all_recorded"]["gains"]["M1_vs_M0"]>0 for x in parts),
        })
    counts={}
    for _,_,name in DIFFS:
        diffs=[s["all_recorded"]["gains"][name] for s in session_records]
        counts[name]={"positive_sessions":sum(v>0 for v in diffs),
                      "negative_sessions":sum(v<0 for v in diffs),
                      "zero_sessions":sum(v==0 for v in diffs)}
    return {
        "research_id":"R102","phase":"C",
        "status":"R102_REAL_ORIGINAL_8SESSION_2520_HELDOUT_M0_M1_M2_M3_E2",
        "original_full_sha256":PINNED_SHA256,
        "actual_original_person_round_rows":len(observations),
        "verified_true_original_sessions":len(sessions),
        "verified_source_people":len(set((sid,p) for sid,ps in sessions.items() for p in ps)),
        "source_group_size":6,
        "source_target_round_range":"t2..t15",
        "actual_same_target_original_next_actor_rounds":len(all_scores),
        "models":{"M0":"other original same-treatment session contemporaneous round mean",
                  "M1":"focal actor own immediately previous contribution/endowment",
                  "M2":"mean last-round shares of other 5 prior-group participants",
                  "M3":"fixed 0.5*M1+0.5*M2"},
        "loss":"mean squared error on original share contributed, lower better",
        "all_recorded":mean_loss(all_scores),
        "manual_target_only":mean_loss(all_scores,lambda r:r["manual"]),
        "early_t2_to_t5":mean_loss(all_scores,lambda r:r["t"]<=5),
        "later_t6_to_t15":mean_loss(all_scores,lambda r:r["t"]>=6),
        "original_automatic_target_count":sum(not r["manual"] for r in all_scores),
        "session_effect_direction_counts":counts,
        "anonymous_original_session_results":session_records,
        "original_treatment_session_direction_summaries":treatment_summaries,
        "independent_holdout_unit":"entire publisher original session.code",
        "external_baseline_uses_other_publisher_session_same_round":True,
        "original_human_ID_or_action_rows_exported":False,
        "not_prospective_E3":True,
        "not_R073_exact_dyadic_opponent_contract":True,
        "PESEN_v0_1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R102-2025-Frozen-C-Original-Session-LOSO-M0123/1.0"})
        with urllib.request.build_opener(SafeRedirect()).open(req,timeout=55) as res:
            validate_url(res.geturl())
            raw=res.read(CAP+1)
        result=real_source_score(raw)
    except (ValueError,OSError,TypeError,KeyError,UnicodeError,csv.Error) as exc:
        result={"research_id":"R102","phase":"C","status":"R102_C_ORIGINAL_ACTION_E2_FAIL_CLOSED",
                "safe_failure":str(exc) if isinstance(exc,SourceError) else "R102_C_ORIGINAL_HUMAN_SCORE_UNVERIFIED",
                "actual_human_model_scores":0,"PESEN_v0_1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R102_REAL_ORIGINAL_8SESSION_2520_HELDOUT_M0_M1_M2_M3_E2":
        raise SystemExit(1)

if __name__=="__main__":
    main()
