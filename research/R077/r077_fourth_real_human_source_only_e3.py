#!/usr/bin/env python3
"""R077 true fourth original human experiment: fixed R073 source numerical transfer.

The only training labels are the R073 source 18,424 original decisions. R077
raw participants are temporary in CI only and held out from all fitting.
The genuine fourth sample was not scored by our previous R073-R076 pipeline.
"""
from __future__ import annotations
import argparse,csv,hashlib,json
from collections import Counter,defaultdict
from pathlib import Path
from urllib.request import Request,urlopen
import sys

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"R076"))
sys.path.insert(0,str(HERE.parent/"R073"))
from r076_source_only_cross_study_transfer import (
    build_source_donors,verify_r073_blob,R073_BLOB_SHA1
)
from r073_human_ipd_memory_loso import (
    MODEL_NAMES,read_original_csv,predict,brier,logloss,ALPHA,NOISE
)
from r077_zenodo_fourth_human_partner_time_audit import summarize

R077_SHA="1cc9a4f68a51992808d966b118226bb5a66ee3ee6054843a132157df8eeb1985"
R077_MD5="4cce04ea68b7a0492c242b206efebe53"
R077_DTA_BYTES=1514315
EXPECTED_ROWS=3620
EXPECTED_ORIGINAL_SESSIONS=15
EXPECTED_PEOPLE=260
EXPECTED_PAIR_ROUNDS=1810
EXPECTED_RISK_EVENTS=1040
FROZEN_PROTOCOL="protocols/R077_PRE_FIRST_TARGET_MODEL_SCORE_SOURCE_SEMANTICS_AMENDMENT_REV002_2026-10-17.md"
PAIRS=(
 ("M3_JOINT_LAST","M1_OWN_LAST"),
 ("M4_JOINT_TWO_LAGS","M3_JOINT_LAST"),
 ("M1_OWN_LAST","M0_TREATMENT_PREVALENCE"),
 ("M2_OPPONENT_LAST","M0_TREATMENT_PREVALENCE"),
 ("M5_TFT_NOISY","M0_TREATMENT_PREVALENCE"),
 ("M6_WSLS_NOISY","M0_TREATMENT_PREVALENCE"),
)
SOURCE_DONOR="R073_ALL_12_POOLED"

def read_author_r077_stata(p):
    raw=Path(p).read_bytes()
    if (len(raw)!=R077_DTA_BYTES or hashlib.sha256(raw).hexdigest()!=R077_SHA
        or hashlib.md5(raw).hexdigest()!=R077_MD5):
        raise ValueError("R077_TRUE_FOURTH_AUTHOR_ZENODO_STATA_SHA_OR_MD5_MISMATCH")
    import pandas as pd
    return pd.read_stata(p,convert_categoricals=False)

def prepare_fourth_real_sessions(data):
    structural=summarize(data)
    a=structural
    if (a["rows"]!=EXPECTED_ROWS or a["observed_session_keys"]!=15
        or a["session_and_treatment_combinations"]!=15
        or a["source_human_session_participant_keys"]!=EXPECTED_PEOPLE
        or a["id_keys"]!=EXPECTED_PEOPLE
        or a["Period_duplicate_within_subject"]!=0
        or a["game+practiceperiod_duplicate_within_subject"]!=0
        or a["left_missing"]!=0 or a["otherleft_missing"]!=0
        or a["left_binary_domain"]!={"0":2175,"1":1445}
        or a["otherleft_binary_domain"]!={"0":2175,"1":1445}):
        raise ValueError("R077_TRUE_AUTHOR_HUMAN_SOURCE_UNIVERSE_CHANGED")
    pair=a["pair_key_Session,treatment,Period,Group"]
    if (pair["two_person_groups"]!=EXPECTED_PAIR_ROUNDS
        or pair["two_person_exact_opponent_action_reciprocity"]!=EXPECTED_PAIR_ROUNDS
        or pair["size_histogram"]!={"2":EXPECTED_PAIR_ROUNDS}):
        raise ValueError("R077_REAL_HUMAN_PAIR_RECIPROCITY_FAIL_CLOSED")
    if any(int(z)!=2 for z in data["part"]):
        raise ValueError("R077_ONLY_GENUINE_HUMAN_EXPERIMENT_PART2_ALLOWED")
    if set(int(z) for z in data["treatment"])!={0,1}:
        raise ValueError("R077_EXPERIMENT_TREATMENT_UNEXPECTED")
    session_treatment={}
    events=defaultdict(list)
    game_count=0
    for (sess,subject,game),group in data.groupby(
        ["Session","Subject","game"],sort=False,dropna=False,observed=True):
        game_count+=1
        # Rev-001 fail-closed identified genuine group reassignments (130
        # row transitions in treatment 1). Rev-002 frozen BEFORE any true
        # score uses previous realized counterpart behavior regardless of
        # partner identity, as original author's lagged-other action analysis.
        # The 1810 dyads themselves were all verified reciprocal above.
        if len(set(int(x) for x in group["treatment"]))!=1:
            raise ValueError("R077_TREATMENT_CHANGED_WITHIN_PERSON_GAME")
        tr=int(group["treatment"].iloc[0])
        if sess in session_treatment and session_treatment[sess]!=tr:
            raise ValueError("R077_SESSION_HAS_MULTIPLE_TREATMENTS")
        session_treatment[sess]=tr
        series=group.sort_values("practiceperiod")
        timesteps=[int(t) for t in series["practiceperiod"]]
        if len(timesteps)!=len(set(timesteps)):
            raise ValueError("R077_DUPLICATE_PERSON_GAME_LOCAL_PERIOD")
        if any(t<1 for t in timesteps):
            raise ValueError("R077_INVALID_LOCAL_GAME_PERIOD")
        timeline={int(row["practiceperiod"]):row
                  for _,row in series.iterrows()}
        # Rev-002: 80 original person-games are not fully observed from
        # t=1; refuse imputation and score only exact observed t,t-1,t-2.
        for t in sorted(timeline):
            if t<3 or t-1 not in timeline or t-2 not in timeline:
                continue
            row=timeline[t]
            previous=timeline[t-1]
            previous2=timeline[t-2]
            event=(int(previous["left"]),int(previous["otherleft"]),
                   int(previous2["left"]),int(previous2["otherleft"]),int(row["left"]))
            if any(z not in (0,1) for z in event):
                raise ValueError("R077_ORIGINAL_FOURTH_ACTION_NOT_BINARY")
            events[sess].append(event)
    if game_count!=1440:
        raise ValueError("R077_ORIGINAL_PERSON_GAME_COUNT_CHANGED")
    if len(session_treatment)!=EXPECTED_ORIGINAL_SESSIONS:
        raise ValueError("R077_ORIGINAL_SESSION_UNIVERSE_INCOMPLETE")
    if set(events)!=set(session_treatment):
        raise ValueError("R077_SOME_ORIGINAL_SESSION_HAS_NO_T3_EVENTS")
    if sum(len(v) for v in events.values())!=EXPECTED_RISK_EVENTS:
        raise ValueError("R077_ORIGINAL_T3_RISK_SET_CHANGED")
    out={sess:{"treatment":session_treatment[sess],"events":v}
         for sess,v in events.items()}
    return out, {
        "original_source_person_decisions":len(data),
        "true_independent_original_sessions":len(session_treatment),
        "distinct_session_person_keys":EXPECTED_PEOPLE,
        "genuine_two_person_game_rounds":EXPECTED_PAIR_ROUNDS,
        "person_supergames":game_count,
        "t3_scorable_within_game_events":sum(len(x) for x in events.values()),
        "treatment_session_counts":{str(k):int(v) for k,v in sorted(Counter(session_treatment.values()).items())},
        "individual_ids_or_actions_exported":False
    }

def score_with_frozen_source(fit,target_sessions):
    """No target-side probability fit is available to this function."""
    if not 0<fit["train_only_prevalence"]<1:
        raise ValueError("R077_SOURCE_ONLY_PREVALENCE_DEGENERATE")
    if not target_sessions:
        raise ValueError("R077_EMPTY_TARGET_SESSIONS")
    grouped=defaultdict(list)
    for session,records in target_sessions.items():
        if not records["events"]:
            raise ValueError("R077_EMPTY_ORIGINAL_HELDOUT_SESSION")
        tr=records["treatment"]
        if tr not in (0,1):
            raise ValueError("R077_TREATMENT_INVALID")
        grouped[tr].append(session)
        for e in records["events"]:
            if len(e)!=5 or any(type(z)!=int or z not in (0,1) for z in e):
                raise ValueError("R077_MODEL_RISK_EVENTS_INVALID")
    if set(grouped)!={0,1}:
        raise ValueError("R077_BOTH_ORIGINAL_TREATMENTS_REQUIRED")
    macro_session={}
    for sid,info in target_sessions.items():
        es=info["events"]
        macro_session[sid]={}
        for model in MODEL_NAMES:
            total_b=total_l=0.0
            for row in es:
                pred=predict(model,row,fit)
                total_b+=brier(row[-1],pred)
                total_l+=logloss(row[-1],pred)
            macro_session[sid][model]={
                "Brier":total_b/len(es),"log_loss":total_l/len(es)
            }
    def avg(v):
        return sum(v)/len(v)
    names=sorted(target_sessions)
    m={}
    for model in MODEL_NAMES:
        m[model]={
            "all_original_sessions_equal_Brier":avg([macro_session[k][model]["Brier"] for k in names]),
            "all_original_sessions_equal_log_loss":avg([macro_session[k][model]["log_loss"] for k in names]),
            "per_treatment_original_session_equal":{
                str(tr):{
                    "original_sessions":len(sids),
                    "Brier":avg([macro_session[k][model]["Brier"] for k in sids]),
                    "log_loss":avg([macro_session[k][model]["log_loss"] for k in sids]),
                }for tr,sids in sorted(grouped.items())
            }
        }
    comps={}
    for model,reference in PAIRS:
        values=[macro_session[k][model]["Brier"]-macro_session[k][reference]["Brier"] for k in names]
        comps[model+"_VS_"+reference]={
            "Brier_delta_all_original_sessions_equal":avg(values),
            "sessions_better":sum(x<0 for x in values),
            "sessions_equal":sum(x==0 for x in values),
            "sessions_worse":sum(x>0 for x in values),
            "sessions":len(names),
            "per_treatment":{
                str(tr):{
                    "sessions":len(sids),
                    "Brier_delta":avg([macro_session[k][model]["Brier"]-macro_session[k][reference]["Brier"] for k in sids]),
                    "better":sum(macro_session[k][model]["Brier"]<macro_session[k][reference]["Brier"] for k in sids),
                    "equal":sum(macro_session[k][model]["Brier"]==macro_session[k][reference]["Brier"] for k in sids),
                    "worse":sum(macro_session[k][model]["Brier"]>macro_session[k][reference]["Brier"] for k in sids)
                }for tr,sids in sorted(grouped.items())
            }
        }
    return {
        "models":m,"paired_differences":comps,
        "original_session_count":len(names),
        "scored_t3_human_events":sum(len(info["events"]) for info in target_sessions.values()),
        "target_labels_used_in_training":0,
        "all_raw_sessions_and_action_sequences_exported":False
    }

def run(source_dir,r077_file):
    verify_r073_blob()
    donor_sessions,_=read_original_csv(source_dir)
    donor_fits=build_source_donors(donor_sessions)
    frozen_fit=donor_fits[SOURCE_DONOR]
    if frozen_fit["source_sessions"]!=12 or frozen_fit["train_target_count"]!=18424:
        raise ValueError("R073_FROZEN_SOURCE_DONOR_RISK_SET_CHANGED")
    true_frame=read_author_r077_stata(r077_file)
    sessions,source=prepare_fourth_real_sessions(true_frame)
    scored=score_with_frozen_source(frozen_fit,sessions)
    if scored["original_session_count"]!=EXPECTED_ORIGINAL_SESSIONS or scored["scored_t3_human_events"]!=EXPECTED_RISK_EVENTS:
        raise ValueError("R077_REAL_TARGET_SCORE_DENOMINATOR_INVALID")
    return {
        "research_id":"R077",
        "status":"R077_FOURTH_INDEPENDENT_AUTHOR_REAL_HUMAN_SOURCE_ONLY_NUMERICAL_E3_EXECUTED",
        "source_eligibility_protocol":"protocols/R077_FOURTH_INDEPENDENT_HUMAN_DATA_SOURCE_AND_BLIND_SCORE_GATE_2026-10-17.md",
        "frozen_before_fourth_model_scoring_protocol":FROZEN_PROTOCOL,
        "source_donor":"R073_ALL_12_POOLED",
        "source_donor_fitted_on":"R073-original 12 complete sessions, 18424 original human events only",
        "frozen_r073_model_git_blob":R073_BLOB_SHA1,
        "frozen_alpha":ALPHA,"frozen_TFT_WSLS_noise":NOISE,
        "target_author_original_DOI":"10.1016/j.euroecorev.2025.105075",
        "target_original_archive_DOI":"10.5281/zenodo.15462528",
        "target_original_Stata_sha256":R077_SHA,
        "target_original_Stata_md5":R077_MD5,
        "target_original_Stata_bytes":R077_DTA_BYTES,
        "source_universe":source,
        "target":"human real cooperation C=1 / defection D=0 in new author original part2 experiment",
        "observed_history":"within subject + game: own and counterpart already executed C/D at t-1,t-2",
        "source_original_15_session_macro_scoring":"Each original Session mean then 15 sessions equal weight; no target model fit",
        "fourth_new_author_study_outcomes_not_previously_scored_with_our_seven_models":True,
        "paper_historical_aggregate_effects_already_public":True,
        "not_a_new_preregistered_human_data_collection":True,
        "causal_human_memory_effect":"NOT_IDENTIFIED",
        "human_records_or_session_scores_exported":False,
        "results":scored,"PESEN_v0.1":"FROZEN"
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--r073-source-dir",type=Path,required=True)
    p.add_argument("--r077-source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        result=run(a.r073_source_dir,a.r077_source)
    except (OSError,ValueError,UnicodeError) as e:
        result={"research_id":"R077","status":"R077_FIRST_FOURTH_HUMAN_E3_FAIL_CLOSED",
                "failure_class":type(e).__name__,
                "bounded_failure":str(e)[:130] if isinstance(e,ValueError) else "SOURCE_IO_ERROR",
                "human_rows_exported":False,"PESEN_v0.1":"FROZEN"}
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "failure_reason":result.get("bounded_failure"),
        "source":result.get("source_universe"),
        "model_Brier":{k:v["all_original_sessions_equal_Brier"]
                       for k,v in result.get("results",{}).get("models",{}).items()},
        "principal":{k:{"Brier_delta":v["Brier_delta_all_original_sessions_equal"],
            "better":v["sessions_better"],"worse":v["sessions_worse"]}
            for k,v in result.get("results",{}).get("paired_differences",{}).items()
            if k.startswith("M3_") or k.startswith("M4_")}
    },sort_keys=True))
    if result["status"]!="R077_FOURTH_INDEPENDENT_AUTHOR_REAL_HUMAN_SOURCE_ONLY_NUMERICAL_E3_EXECUTED":
        raise RuntimeError("R077_FOURTH_SOURCE_UNSEEN_E3_MODEL_SCORE_FAIL_CLOSED")

if __name__=="__main__":
    main()
