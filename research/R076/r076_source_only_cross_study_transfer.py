#!/usr/bin/env python3
"""R076 retrospective zero-shot source-fitted numerical transfer, no target fitting.

All three genuine author sources are SHA-pinned and checked by earlier parsers.
Source-only R073 M0..M4 fits are frozen once, then unchanged across each entire
R074 and R075 target study. Human records/session identifiers never exported.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
for name in ("R073","R074","R075"):
    sys.path.insert(0,str(ROOT/name))
from r073_human_ipd_memory_loso import (
    MODEL_NAMES,CONDITIONAL_MODELS,read_original_csv,records_for_session,
    state_for,predict,brier,logloss,ALPHA,NOISE
)
from r074_dalbo_external_human_e3 import (
    prepare_external_sessions as prepare_r074_sessions,
    SOURCE_SHA256 as R074_SOURCE_SHA256,
)
from r075_coauthor_real_human_e3 import (
    prepare_original_sessions as prepare_r075_sessions,
    ORIGINAL_SHA256 as R075_SOURCE_SHA256,
)
R073_BLOB_SHA1="c8a0b47fd27bf05e7be5b87419a0824355fc911a"
DONORS=("R073_ALL_12_POOLED","R073_FIXED_6_ONLY","R073_SHUFFLED_6_ONLY")
TARGETS=("R074","R075")
EXPECTED_MODEL_NAMES=(
    "M0_TREATMENT_PREVALENCE","M1_OWN_LAST","M2_OPPONENT_LAST",
    "M3_JOINT_LAST","M4_JOINT_TWO_LAGS","M5_TFT_NOISY","M6_WSLS_NOISY",
)
PAIRS=(
    ("M3_JOINT_LAST","M1_OWN_LAST"),
    ("M4_JOINT_TWO_LAGS","M3_JOINT_LAST"),
    ("M1_OWN_LAST","M0_TREATMENT_PREVALENCE"),
    ("M2_OPPONENT_LAST","M0_TREATMENT_PREVALENCE"),
    ("M5_TFT_NOISY","M0_TREATMENT_PREVALENCE"),
    ("M6_WSLS_NOISY","M0_TREATMENT_PREVALENCE")
)
TARGET_SESSIONS=18
EXPECTED_TARGET_COUNTS={"R074":15338,"R075":26116}

def verify_r073_blob():
    path=ROOT/"R073"/"r073_human_ipd_memory_loso.py"
    raw=path.read_bytes()
    git_sha=hashlib.sha1(b"blob "+str(len(raw)).encode("ascii")+b"\0"+raw).hexdigest()
    if git_sha!=R073_BLOB_SHA1 or MODEL_NAMES!=EXPECTED_MODEL_NAMES:
        raise ValueError("R076_FROZEN_SOURCE_MODEL_IDENTITY_FAILED")
    if ALPHA!=20.0 or NOISE!=0.05:
        raise ValueError("R076_FROZEN_SOURCE_MODEL_PARAMETERS_FAILED")

def build_source_donors(source_sessions):
    if len(source_sessions)!=12:
        raise ValueError("R073_SOURCE_SESSION_COUNT_INVALID")
    records={}
    for name,condition in (
        (DONORS[0],lambda s:True),
        (DONORS[1],lambda s:s[0]=="fix"),
        (DONORS[2],lambda s:s[0]=="rand")
    ):
        matching=sorted(k for k in source_sessions if condition(k))
        if len(matching)!=(12 if name==DONORS[0] else 6):
            raise ValueError("R076_DONOR_TREATMENT_SESSION_UNIVERSE_INVALID")
        events=[rec for session in matching
                for rec in records_for_session(source_sessions[session])]
        required=18424 if name==DONORS[0] else (92*98 if name==DONORS[1] else 96*98)
        if len(events)!=required:
            raise ValueError("R076_DONOR_RISK_SET_INVALID")
        p0=sum(x[4] for x in events)/len(events)
        if not 0<p0<1:
            raise ValueError("R076_DEGENERATE_DONOR_PREVALENCE")
        counts={}
        for model in CONDITIONAL_MODELS:
            hist=defaultdict(lambda:[0,0])
            for ev in events:
                state=state_for(model,ev)
                hist[state][0]+=ev[4]
                hist[state][1]+=1
            counts[model]={state:tuple(vals) for state,vals in hist.items()}
        records[name]={
            "train_only_prevalence":p0,
            "state_counts":counts,
            "source_sessions":len(matching),
            "train_target_count":len(events),
        }
    return records

def check_targets(sessions,target):
    if len(sessions)!=TARGET_SESSIONS:
        raise ValueError("R076_TARGET_SESSION_UNIVERSE_INVALID")
    actual=sum(len(x["events"]) for x in sessions.values())
    if actual!=EXPECTED_TARGET_COUNTS[target]:
        raise ValueError("R076_TARGET_EVENT_UNIVERSE_INVALID")
    groups=Counter(x["treatment"] for x in sessions.values())
    if len(groups)!=6:
        raise ValueError("R076_TARGET_TREATMENT_UNIVERSE_INVALID")
    if target=="R074" and sorted(groups.values())!=[3]*6:
        raise ValueError("R074_TARGET_SESSION_STRATA_INVALID")
    if target=="R075" and sorted(groups.values())!=[2,3,3,3,3,4]:
        raise ValueError("R075_TARGET_SESSION_STRATA_INVALID")
    for item in sessions.values():
        if not item["events"]:
            raise ValueError("R076_EMPTY_TARGET_SESSION")
        if any(len(x)!=5 or any(type(z) is not int or z not in (0,1) for z in x)
               for x in item["events"]):
            raise ValueError("R076_INVALID_BINARY_TARGET_HISTORY")
    return groups

def transfer_predict_all(source_fits,target_sessions,target,donors=DONORS):
    """Never accepts a target fit, and never calls target training functions."""
    groups=check_targets(target_sessions,target)
    ordered=sorted(target_sessions)
    def avg(items):
        return sum(items)/len(items)
    def treatment_label(x):
        if target=="R074":
            return "R"+str(x[0])+"_DELTA"+x[1].replace(".","p")
        return "BC"+x[0].replace(".","p")+"_ERROR"+x[1].replace(".","p")
    results={}
    for donor in donors:
        fit=source_fits[donor]
        if not 0<fit["train_only_prevalence"]<1:
            raise ValueError("R076_DONOR_P0_INVALID")
        per_session={}
        for sid in ordered:
            events=target_sessions[sid]["events"]
            per_model={}
            for model in MODEL_NAMES:
                sb=sl=0.0
                for e in events:
                    p=predict(model,e,fit)
                    sb+=brier(e[4],p)
                    sl+=logloss(e[4],p)
                per_model[model]=(sb/len(events),sl/len(events))
            per_session[sid]=per_model
        macro={}
        for model in MODEL_NAMES:
            strata={}
            for tr in sorted(groups):
                candidates=[s for s in ordered if target_sessions[s]["treatment"]==tr]
                strata[treatment_label(tr)]={
                    "sessions":len(candidates),
                    "Brier":avg([per_session[s][model][0] for s in candidates]),
                    "log_loss":avg([per_session[s][model][1] for s in candidates])
                }
            macro[model]={
                "all_18_sessions_equal_weight_Brier":avg([per_session[s][model][0] for s in ordered]),
                "all_18_sessions_equal_weight_log_loss":avg([per_session[s][model][1] for s in ordered]),
                "per_treatment_session_equal":strata
            }
        comparisons={}
        for model,baseline in PAIRS:
            diffs=[per_session[s][model][0]-per_session[s][baseline][0] for s in ordered]
            strata={}
            for tr in sorted(groups):
                cases=[s for s in ordered if target_sessions[s]["treatment"]==tr]
                delta=[per_session[s][model][0]-per_session[s][baseline][0] for s in cases]
                strata[treatment_label(tr)]={
                    "sessions":len(cases),
                    "Brier_delta":avg(delta),
                    "sessions_better":sum(v<0 for v in delta),
                    "sessions_equal":sum(v==0 for v in delta),
                    "sessions_worse":sum(v>0 for v in delta)
                }
            comparisons[model+"_VS_"+baseline]={
                "all_18_sessions_equal_weight_Brier_delta":avg(diffs),
                "sessions_better":sum(v<0 for v in diffs),
                "sessions_equal":sum(v==0 for v in diffs),
                "sessions_worse":sum(v>0 for v in diffs),
                "sessions":len(ordered),
                "per_treatment":strata
            }
        results[donor]={
            "source_training_sessions":fit["source_sessions"],
            "source_training_target_events":fit["train_target_count"],
            "source_only_C_rate":fit["train_only_prevalence"],
            "models":macro,
            "comparisons":comparisons,
            "derived_M3_minus_M0_Brier":macro["M3_JOINT_LAST"]["all_18_sessions_equal_weight_Brier"]-
                macro["M0_TREATMENT_PREVALENCE"]["all_18_sessions_equal_weight_Brier"],
            "derived_M4_minus_M0_Brier":macro["M4_JOINT_TWO_LAGS"]["all_18_sessions_equal_weight_Brier"]-
                macro["M0_TREATMENT_PREVALENCE"]["all_18_sessions_equal_weight_Brier"]
        }
    # Source-free TFT and WSLS must yield the same scores across all donors.
    if len(donors)==3:
        for model in ("M5_TFT_NOISY","M6_WSLS_NOISY"):
            vals=[results[d]["models"][model]["all_18_sessions_equal_weight_Brier"] for d in DONORS]
            if vals[0]!=vals[1] or vals[0]!=vals[2]:
                raise ValueError("THEORETICAL_DONOR_FREE_BASELINE_INCONSISTENT")
    return results

def run(source_path,target_74_path,target_75_path):
    verify_r073_blob()
    source_sessions,_=read_original_csv(source_path)
    donors=build_source_donors(source_sessions)
    # These functions are parsers+audits, not training. Never fit to target.
    sessions74,_=prepare_r074_sessions(target_74_path.read_bytes())
    sessions75,_=prepare_r075_sessions(target_75_path.read_bytes())
    results={}
    for target,sessions in (("R074",sessions74),("R075",sessions75)):
        results[target]={
            "sessions":len(sessions),
            "scored_actions":sum(len(s["events"]) for s in sessions.values()),
            "donors":transfer_predict_all(donors,sessions,target)
        }
    return {
        "research_id":"R076",
        "status":"RETROSPECTIVE_R073_SOURCE_ONLY_NUMERICAL_ZERO_SHOT_TRANSFER_COMPUTED",
        "evidence_level":"RETROSPECTIVE_CROSS_STUDY_NUMERICAL_TRANSFER_ON_PREVIOUSLY_SEEN_DATA_NOT_NEW_E3",
        "protocol":"protocols/R076_RETROSPECTIVE_SOURCE_ONLY_ZERO_SHOT_CROSS_STUDY_TRANSFER_FREEZE_2026-10-17.md",
        "source_original_R073_submission_git_blobs":{
            "fix.csv":"3bf78bf85f6642afee18d6f1965dca7272582f40",
            "rand.csv":"f5a86cd033b739da45d3fc7c5019068f612146a2",
        },
        "original_target_SHA256":{"R074":R074_SOURCE_SHA256,"R075":R075_SOURCE_SHA256},
        "frozen_model_git_blob":R073_BLOB_SHA1,
        "source_12_sessions":12,"source_12_session_scorable_events":18424,
        "source_donor_splits":list(DONORS),
        "fixed_alpha":ALPHA,"fixed_theoretical_noise":NOISE,
        "target_label_records_used_for_any_fitting":0,
        "no_target_recalibration":True,
        "target_data_previously_seen_by_researchers":True,
        "individual_rows_session_ids_and_state_tables_exported":False,
        "results":results,
        "causal_memory": "NOT_IDENTIFIED",
        "prospectively_unseen_fourth_study": "NOT_TESTED",
        "PESEN_v0.1":"FROZEN"
    }

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--r073-source-dir",type=Path,required=True)
    ap.add_argument("--r074-source",type=Path,required=True)
    ap.add_argument("--r075-source",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    try:
        out=run(args.r073_source_dir,args.r074_source,args.r075_source)
    except (OSError,ValueError,UnicodeError) as e:
        out={"research_id":"R076","status":"R076_CROSS_STUDY_SOURCE_OR_FIT_FAIL_CLOSED",
             "error_class":type(e).__name__,
             "reason":str(e)[:105] if isinstance(e,ValueError) else "SOURCE_READ_FAILURE",
             "individual_rows_exported":False,"PESEN_v0.1":"FROZEN"}
    args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":out["status"],
        "source_train_targets":out.get("source_12_session_scorable_events"),
        "target_summary":{
            target:{
                "targets":study["scored_actions"],"sessions":study["sessions"],
                "donors":{
                    donor:{
                        "Brier":{k:v["all_18_sessions_equal_weight_Brier"] for k,v in v["models"].items()},
                        "primary":{k:q["all_18_sessions_equal_weight_Brier_delta"]
                            for k,q in v["comparisons"].items()
                            if k.startswith("M3_") or k.startswith("M4_")}
                    } for donor,v in study["donors"].items()
                }
            }for target,study in out.get("results",{}).items()
        }
    },sort_keys=True))
    if out["status"]!="RETROSPECTIVE_R073_SOURCE_ONLY_NUMERICAL_ZERO_SHOT_TRANSFER_COMPUTED":
        raise RuntimeError("R076_REAL_ZERO_SHOT_SCORE_FAIL_CLOSED")

if __name__=="__main__":
    main()
