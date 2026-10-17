#!/usr/bin/env python3
"""R075: independent third experiment E3, original coauthor ZIP 18 full sessions.

Use unmodified R073 conditional model primitives, same seven families and scoring.
Current label is intended C/D, lagged features are actually implemented actions.
All session/person identifiers and action histories remain transient in memory.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math,sys
from collections import Counter,defaultdict
from pathlib import Path

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/"R073"))
from r073_human_ipd_memory_loso import (
    MODEL_NAMES, CONDITIONAL_MODELS, state_for, predict, brier, logloss, ALPHA, NOISE
)
from r075_coauthor_original_session_structure import (
    ORIGINAL_SHA256,ORIGINAL_ZIP_BYTES,ORIGINAL_TEXT_ROWS,original_text_from_verified_zip
)
from r075_coauthor_original_feedback_audit import analyze

MODEL_BLOB_SHA1="c8a0b47fd27bf05e7be5b87419a0824355fc911a"
ORIGINAL_TEXT_SHA256="ff552ba21a92c254e2d867670910f908f5ea8e3aa34b4fa6c05443a020fa56b7"
EXPECTED_SCORED=26116
EXPECTED_SESSIONS=18
EXPECTED_PARTICIPANT_SLOTS=384
EXPECTED_TREATMENT_SESSION_COUNT={
    ("1.5","0.125"):3,
    ("2","0.125"):2,
    ("2.5","0.125"):3,
    ("4","0"):3,
    ("4","0.0625"):3,
    ("4","0.125"):4,
}
EXPECTED_MODEL_NAMES=(
    "M0_TREATMENT_PREVALENCE","M1_OWN_LAST","M2_OPPONENT_LAST",
    "M3_JOINT_LAST","M4_JOINT_TWO_LAGS","M5_TFT_NOISY","M6_WSLS_NOISY"
)
PAIRS=(
    ("M3_JOINT_LAST","M1_OWN_LAST"),
    ("M4_JOINT_TWO_LAGS","M3_JOINT_LAST"),
    ("M1_OWN_LAST","M0_TREATMENT_PREVALENCE"),
    ("M2_OPPONENT_LAST","M0_TREATMENT_PREVALENCE"),
    ("M5_TFT_NOISY","M0_TREATMENT_PREVALENCE"),
    ("M6_WSLS_NOISY","M0_TREATMENT_PREVALENCE"),
)

def verify_frozen_r073():
    path=HERE.parent/"R073"/"r073_human_ipd_memory_loso.py"
    b=path.read_bytes()
    digest=hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
    if digest!=MODEL_BLOB_SHA1:raise ValueError("FROZEN_R073_CODE_BLOB_NOT_MATCHED")
    if MODEL_NAMES!=EXPECTED_MODEL_NAMES or ALPHA!=20.0 or NOISE!=.05:
        raise ValueError("FROZEN_MODEL_FAMILY_OR_PARAMETER_CHANGED")


def prepare_original_sessions(archive:bytes):
    source=original_text_from_verified_zip(archive)
    if hashlib.sha256(source).hexdigest()!=ORIGINAL_TEXT_SHA256:
        raise ValueError("ORIGINAL_PUBLISHED_TXT_HASH_CHANGED")
    summary=analyze(source)
    if (summary["original_source_text_actions"]!=ORIGINAL_TEXT_ROWS or
        summary["sessions"]!=EXPECTED_SESSIONS or
        summary["session_person_slots"]!=EXPECTED_PARTICIPANT_SLOTS or
        summary["paired_rounds"]!=17223 or
        summary["distinct_person_interactions"]!=4176 or
        summary["fully_observed_t3_candidate_targets"]!=EXPECTED_SCORED or
        summary["integrity_failures"] or
        summary["partner_switch_inside_same_interaction_rows"]!=0):
        raise ValueError("ORIGINAL_TRUE_HUMAN_UNIVERSE_PARITY_FAILURE")
    records=csv.DictReader(io.StringIO(source.decode("utf-8-sig")),delimiter="\t")
    histories=defaultdict(dict)
    treatments={}
    for r in records:
        file=r["file"]
        treatment=(r["bc"],r["error"])
        if file in treatments and treatments[file]!=treatment:
            raise ValueError("SESSION_HAS_MULTIPLE_TREATMENTS")
        treatments[file]=treatment
        person=(file,r["subject"],r["interaction"])
        t=int(r["period"])
        if t in histories[person]:raise ValueError("PERSON_INTERACTION_ROUND_DUPLICATE")
        if r["decision"] not in ("0","1"):
            raise ValueError("INTENDED_C_D_INVALID")
        histories[person][t]=r
    session_events=defaultdict(list)
    for (file,person,interaction),h in histories.items():
        ts=sorted(h)
        if ts!=list(range(1,len(ts)+1)):
            raise ValueError("GAPPED_PERSON_INTERACTION")
        # t=1,2 are used exclusively for prior information.
        for t in range(3,len(ts)+1):
            row=h[t]
            try:
                own1,opp1,own2,opp2=(
                    int(row["you_p_1"]),int(row["other_p_1"]),
                    int(row["you_p_2"]),int(row["other_p_2"])
                )
            except (ValueError,TypeError) as exc:
                raise ValueError("R075_LAGGED_OBSERVED_ACTION_NOT_BINARY") from exc
            if any(x not in (0,1) for x in (own1,opp1,own2,opp2)):
                raise ValueError("R075_LAGGED_OBSERVED_ACTION_NOT_BINARY")
            event=(own1,opp1,own2,opp2,int(row["decision"]))
            session_events[file].append(event)
    if set(session_events)!=set(treatments):
        raise ValueError("ALL_SESSIONS_MUST_HAVE_SCORABLE_TARGETS")
    if sum(len(events) for events in session_events.values())!=EXPECTED_SCORED:
        raise ValueError("TEST_RISK_SET_EXPECTED_26116")
    session_count=Counter(treatments.values())
    if dict(session_count)!=EXPECTED_TREATMENT_SESSION_COUNT:
        raise ValueError("SIX_TREATMENT_OR_SESSION_COUNTS_DIFFER")
    return {file:{"treatment":treatments[file],"events":session_events[file]}
            for file in sorted(treatments)},summary


def fit_other_sessions(sessions,heldout):
    if heldout not in sessions:raise ValueError("HELDOUT_SESSION_NOT_IN_UNIVERSE")
    treatment=sessions[heldout]["treatment"]
    training=[s for s in sessions if s!=heldout and sessions[s]["treatment"]==treatment]
    if not training:raise ValueError("NO_OTHER_TREATMENT_SESSIONS")
    events=[event for s in training for event in sessions[s]["events"]]
    if not events:raise ValueError("NO_REAL_TRAINING_EVENTS")
    p0=sum(e[4] for e in events)/len(events)
    if not 0<p0<1:raise ValueError("DEGENERATE_TREATMENT_TRAIN_PREVALENCE")
    tab={}
    for model in CONDITIONAL_MODELS:
        counts=defaultdict(lambda:[0,0])
        for e in events:
            t=counts[state_for(model,e)]
            t[0]+=e[4]
            t[1]+=1
        tab[model]={k:tuple(v) for k,v in counts.items()}
    return {"train_only_prevalence":p0,
            "state_counts":tab,"train_target_count":len(events),
            "trained_from_other_sessions_same_treatment":len(training)}


def evaluate_external(sessions):
    if not sessions:raise ValueError("EMPTY_EXTERNAL_UNIVERSE")
    by_treatment=defaultdict(list)
    for session,info in sessions.items():
        if not info["events"]:raise ValueError("HELDOUT_SESSION_EMPTY")
        if any(len(e)!=5 or any(type(x)!=int or x not in (0,1) for x in e)
               for e in info["events"]):
            raise ValueError("INVALID_EXTERNAL_EVENT_BINARY_OR_TIME")
        by_treatment[info["treatment"]].append(session)
    if any(len(group)<2 for group in by_treatment.values()):
        raise ValueError("NO_EXCLUSIVE_OTHER_SESSION_FOR_TRAINING")
    scores={}
    for session in sorted(sessions):
        fitted=fit_other_sessions(sessions,session)
        es=sessions[session]["events"]
        scores[session]={}
        for model in MODEL_NAMES:
            b=l=0.0
            for e in es:
                p=predict(model,e,fitted)
                b+=brier(e[4],p)
                l+=logloss(e[4],p)
            scores[session][model]=(b/len(es),l/len(es))
    def mean(vals):
        return sum(vals)/len(vals)
    all_sessions=sorted(sessions)
    def treatment_name(key):
        return "BC"+key[0].replace(".","p")+"_ERROR"+key[1].replace(".","p")
    aggregate={}
    for model in MODEL_NAMES:
        aggregate[model]={
            "all_18_sessions_equal_weight_Brier":mean([scores[s][model][0] for s in all_sessions]),
            "all_18_sessions_equal_weight_log_loss":mean([scores[s][model][1] for s in all_sessions]),
            "per_treatment_session_equal":{
                treatment_name(key):{
                    "sessions":len(group),
                    "Brier":mean([scores[s][model][0] for s in group]),
                    "log_loss":mean([scores[s][model][1] for s in group])
                }
                for key,group in sorted(by_treatment.items())
            }
        }
    paired={}
    for model,ref in PAIRS:
        per={}
        for treatment,group in sorted(by_treatment.items()):
            d=[scores[s][model][0]-scores[s][ref][0] for s in group]
            per[treatment_name(treatment)]={
                "Brier_delta":mean(d),
                "sessions_better":sum(x<0 for x in d),
                "sessions_equal":sum(x==0 for x in d),
                "sessions_worse":sum(x>0 for x in d),
                "sessions":len(d)
            }
        ds=[scores[s][model][0]-scores[s][ref][0] for s in all_sessions]
        paired[model+"_VS_"+ref]={
            "Brier_delta_all_sessions_equal_weight":mean(ds),
            "sessions_better":sum(x<0 for x in ds),
            "sessions_equal":sum(x==0 for x in ds),
            "sessions_worse":sum(x>0 for x in ds),
            "sessions":len(ds),
            "per_treatment":per
        }
    return {
        "model_macro":aggregate,
        "paired_comparisons":paired,
        "test_sessions":len(sessions),
        "treatments":len(by_treatment),
        "individual_test_targets":sum(len(x["events"]) for x in sessions.values()),
        "session_rows_exported":False
    }


def run(original_zip:bytes):
    verify_frozen_r073()
    sessions,source=prepare_original_sessions(original_zip)
    out=evaluate_external(sessions)
    return {
        "research_id":"R075",
        "status":"R075_TRUE_THIRD_HUMAN_EXPERIMENT_18_SESSION_FROZEN_E3_EXECUTED",
        "stage":"THIRD_INDEPENDENT_AUTHOR_HUMAN_NOISY_IPD_E3_SESSION_LOSO",
        "protocol":"protocols/R075_COAUTHOR_ORIGINAL_HUMAN_18_SESSION_E3_TRANSFER_FREEZE_2026-10-17.md",
        "original_author_paper_DOI":"10.1257/aer.102.2.720",
        "original_coauthor_source":"https://davidrand-cooperation.com/s/slow-to-anger-and-fast-to-forgive-data-and-code.zip",
        "original_source_SHA256":ORIGINAL_SHA256,
        "original_source_bytes":ORIGINAL_ZIP_BYTES,
        "original_text_SHA256":ORIGINAL_TEXT_SHA256,
        "source_human_actions":ORIGINAL_TEXT_ROWS,
        "true_source_sessions":EXPECTED_SESSIONS,
        "human_session_person_slots":EXPECTED_PARTICIPANT_SLOTS,
        "source_paired_rounds":17223,
        "scored_targets":EXPECTED_SCORED,
        "frozen_models":list(MODEL_NAMES),
        "frozen_alpha":ALPHA,"frozen_TFT_WSLS_noise":NOISE,
        "R073_frozen_implementation_git_blob":MODEL_BLOB_SHA1,
        "training":"other real complete original file sessions of same bc and implementation-error treatment; 1/2/3 other sessions according to original treatment",
        "target":"intended human cooperation C=1 D=0, conditional on own and partner's previously executed actual actions",
        "scoring":"teacher-forced within interaction t>=3, test each original session then 18 equal-weight sessions",
        "results":out,
        "numerical_parameter_zero_shot_transfer":"NOT_TESTED",
        "human_memory_causality":"NOT_IDENTIFIED",
        "cross_session_physical_reenrolment":"UNKNOWN; original within-session numeric subject codes repeat",
        "not_equivalent_to_AEA_deposited_archive":"BYTE_PARITY_UNKNOWN",
        "human_rows_or_session_ids_exported":False,
        "PESEN_v0.1":"FROZEN"
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--zip",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    try:
        result=run(args.zip.read_bytes())
    except (OSError,ValueError,UnicodeError) as e:
        result={"research_id":"R075","status":"R075_REAL_E3_FAIL_CLOSED",
                "error_type":type(e).__name__,
                "reason":str(e)[:100] if isinstance(e,ValueError) else "SOURCE_IO",
                "human_rows_exported":False,"PESEN_v0.1":"FROZEN"}
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n")
    print(json.dumps({
        "status":result["status"],
        "sessions":result.get("results",{}).get("test_sessions"),
        "targets":result.get("results",{}).get("individual_test_targets"),
        "Brier":{k:v["all_18_sessions_equal_weight_Brier"]
                 for k,v in result.get("results",{}).get("model_macro",{}).items()},
        "primary":{k:{t:v[t] for t in ("Brier_delta_all_sessions_equal_weight",
                    "sessions_better","sessions_worse","sessions_equal")}
                   for k,v in result.get("results",{}).get("paired_comparisons",{}).items()
                   if k.startswith(("M3_JOINT_LAST","M4_JOINT_TWO_LAGS"))}
    },sort_keys=True))
    if result["status"]!="R075_TRUE_THIRD_HUMAN_EXPERIMENT_18_SESSION_FROZEN_E3_EXECUTED":
        raise RuntimeError("REAL_EXTERNAL_HUMAN_E3_SOURCE_OR_MODEL_FAIL_CLOSED")

if __name__=="__main__":
    main()
