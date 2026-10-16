#!/usr/bin/env python3
"""R073: genuine author submission C/D histories, 12-session LOSO human E2.

Only conditional individual next C (t>=3), not open-loop/IPD HMM/causal
identification. No player IDs, session IDs, row level time series exported.
"""
from __future__ import annotations
import argparse,csv,io,json,math,sys
from collections import Counter,defaultdict
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"R067"))
from r067_author_ipd_submission_audit import FILES,SUBMISSION_COMMIT,audit_csv_bytes

ALPHA=20.0
NOISE=.05
SESSION_COUNT=12
TRAIN_SESSIONS_PER_TREATMENT=5
TOTAL_PEOPLE=188
SCORED_ROUNDS_PER_PERSON=98
TOTAL_SCORED=TOTAL_PEOPLE*SCORED_ROUNDS_PER_PERSON
MODEL_NAMES=(
 "M0_TREATMENT_PREVALENCE",
 "M1_OWN_LAST",
 "M2_OPPONENT_LAST",
 "M3_JOINT_LAST",
 "M4_JOINT_TWO_LAGS",
 "M5_TFT_NOISY",
 "M6_WSLS_NOISY",
)
CONDITIONAL_MODELS=MODEL_NAMES[1:5]


def encode_action(raw):
    if raw=="C":return 1
    if raw=="D":return 0
    raise ValueError("INVALID_ORIGINAL_C_D_ACTION")


def event_from_history(history,t):
    """history maps exact integer round to (own C/D, previous opponent C/D)."""
    if t<3 or not all(k in history for k in (t-2,t-1,t)):
        raise ValueError("NO_COMPLETE_PREVIOUS_TWO_ROUNDS")
    own1,opp1=history[t-1]
    own2,opp2=history[t-2]
    y=history[t][0]
    return (own1,opp1,own2,opp2,y)


def validate_experiment(sessions):
    if len(sessions)!=SESSION_COUNT:
        raise ValueError("REQUIRES_EXACTLY_TWELVE_SESSIONS")
    for treatment in ("fix","rand"):
        if sum(k[0]==treatment for k in sessions)!=6:
            raise ValueError("REQUIRES_SIX_INDEPENDENT_SESSIONS_PER_TREATMENT")
    participants=0
    scored=0
    for key,players in sessions.items():
        if key[0] not in ("fix","rand") or len(players)<2:
            raise ValueError("EXPERIMENT_TREATMENT_SESSION_INVALID")
        participants+=len(players)
        for history in players.values():
            if set(history)!=set(range(1,101)):
                raise ValueError("ORIGINAL_PERSON_ROUNDS_NOT_ONE_TO_HUNDRED")
            if any(type(value) is not int or value not in (0,1)
                   for entry in history.values() for value in entry):
                raise ValueError("INVALID_BINARY_ACTION")
            scored+=98
    if participants!=TOTAL_PEOPLE or scored!=TOTAL_SCORED:
        raise ValueError("SOURCE_188_PERSON_UNIVERSE_MISMATCH")
    return {"sessions":len(sessions),"humans":participants,
            "individual_source_decisions":participants*100,
            "individual_scorable_outcomes":scored,"score_rounds_from":3,
            "score_rounds_through":100,
            "fixed_sessions":6,"shuffled_sessions":6,
            "individual_record_or_ID_exported":False}


def read_original_csv(folder):
    sessions=defaultdict(dict)
    for name,(bytes_n,sha) in FILES.items():
        source=(folder/name).read_bytes()
        audited=audit_csv_bytes(name,source)
        if (audited["actions_player_other_or_missing"] or
            audited["actions_opponent_other_or_missing"] or
            audited["invalid_round_values"] or
            audited["session_player_round_repeat_rows"] or
            audited["missing_session_or_player_rows"] or
            audited["records_who_played_other_or_missing"] or
            audited["records_treatment_other_or_missing"]):
            raise ValueError("PINNED_ORIGINAL_HUMAN_SOURCE_INTEGRITY_FAILURE")
        tr="fix" if name=="fix.csv" else "rand"
        rdr=csv.DictReader(io.StringIO(source.decode("utf-8-sig"),newline=""))
        for row in rdr:
            if row["treatment"]!=tr or row["who_played"]!="user":
                raise ValueError("SOURCE_TREATMENT_OR_WHO_PLAYED_INVALID")
            rd_float=float(row["round"])
            if not rd_float.is_integer() or not 1<=rd_float<=100:
                raise ValueError("SOURCE_ROUND_EXCEEDS_ORIGINAL_HORIZON")
            rd=int(rd_float)
            key=(tr,row["session"])
            person=row["player"]
            if person not in sessions[key]:sessions[key][person]={}
            if rd in sessions[key][person]:
                raise ValueError("DUPLICATE_PERSON_ROUND")
            sessions[key][person][rd]=(encode_action(row["action_player"]),
                                       encode_action(row["action_opponent"]))
    result=dict(sessions)
    return result,validate_experiment(result)


def records_for_session(players):
    """Anonymous records stay in memory; no IDs or sequences returned to JSON."""
    for history in players.values():
        for t in range(3,101):
            yield event_from_history(history,t)


def state_for(model,event):
    own1,opp1,own2,opp2,_=event
    if model=="M1_OWN_LAST":return (own1,)
    if model=="M2_OPPONENT_LAST":return (opp1,)
    if model=="M3_JOINT_LAST":return (own1,opp1)
    if model=="M4_JOINT_TWO_LAGS":return (own1,opp1,own2,opp2)
    raise ValueError("MODEL_HAS_NO_TRAINABLE_CONDITIONAL_STATE")


def train_only_other_sessions(sessions,heldout):
    same=[s for s in sessions if s[0]==heldout[0] and s!=heldout]
    if heldout not in sessions or len(same)!=TRAIN_SESSIONS_PER_TREATMENT:
        raise ValueError("TRAIN_AND_HELDOUT_SESSION_PARTITION_VIOLATED")
    rows=[rec for group in same for rec in records_for_session(sessions[group])]
    if not rows or any(len(rec)!=5 for rec in rows):
        raise ValueError("NO_TRAINING_ROWS")
    prevalence=sum(rec[4] for rec in rows)/len(rows)
    if not 0<prevalence<1:
        raise ValueError("DEGENERATE_TRAIN_ONLY_PREVALENCE")
    counts={}
    for model in CONDITIONAL_MODELS:
        table=defaultdict(lambda:[0,0])
        for rec in rows:
            slot=table[state_for(model,rec)]
            slot[0]+=rec[4]
            slot[1]+=1
        counts[model]={s:tuple(n) for s,n in table.items()}
    return {"train_only_prevalence":prevalence,
            "trained_from_other_sessions_same_treatment":5,
            "train_target_count":len(rows),
            "state_counts":counts}


def predict(model,rec,fit):
    if len(rec)!=5 or any(type(v) is not int or v not in (0,1) for v in rec):
        raise ValueError("ALL_RECORD_ACTIONS_MUST_BE_BINARY")
    p0=fit["train_only_prevalence"]
    if not 0<p0<1:raise ValueError("INVALID_TRAIN_PREVALENCE")
    if model=="M0_TREATMENT_PREVALENCE":p=p0
    elif model in CONDITIONAL_MODELS:
        c,n=fit["state_counts"][model].get(state_for(model,rec),(0,0))
        p=(c+ALPHA*p0)/(n+ALPHA)
    elif model=="M5_TFT_NOISY":
        p=1-NOISE if rec[1] else NOISE
    elif model=="M6_WSLS_NOISY":
        p=1-NOISE if rec[0]==rec[1] else NOISE
    else:
        raise ValueError("UNKNOWN_MODEL_FAMILY")
    if not 0<p<1 or not math.isfinite(p):
        raise ValueError("INVALID_CONDITIONAL_PROBABILITY")
    return p


def brier(y,p):
    if y not in (0,1) or not 0<p<1:
        raise ValueError("INVALID_PREDICTION_OR_OUTCOME")
    return (p-y)**2


def logloss(y,p):
    if y not in (0,1) or not 0<p<1:
        raise ValueError("INVALID_PREDICTION_OR_OUTCOME")
    return -(y*math.log(p)+(1-y)*math.log1p(-p))


def evaluate(sessions):
    validate_experiment(sessions)
    scores={model:{"fix":[],"rand":[]} for model in MODEL_NAMES}
    for heldout in sorted(sessions):
        fit=train_only_other_sessions(sessions,heldout)
        group=list(records_for_session(sessions[heldout]))
        if len(group)!=98*len(sessions[heldout]):
            raise ValueError("TEST_RISK_SET_NOT_98_PER_PERSON")
        for model in MODEL_NAMES:
            total_b=total_l=0.0
            for rec in group:
                p=predict(model,rec,fit)
                total_b+=brier(rec[4],p)
                total_l+=logloss(rec[4],p)
            scores[model][heldout[0]].append(
                (total_b/len(group),total_l/len(group)))
    def mean(seq):return sum(seq)/len(seq)
    public={}
    for model in MODEL_NAMES:
        fixed=scores[model]["fix"];rand=scores[model]["rand"]
        if len(fixed)!=6 or len(rand)!=6:
            raise ValueError("LOSO_METRIC_DENOMINATOR_INCOMPLETE")
        public[model]={
            "all_12_sessions_equal_weight_Brier":mean([v[0] for v in fixed+rand]),
            "all_12_sessions_equal_weight_log_loss":mean([v[1] for v in fixed+rand]),
            "fixed_six_sessions_equal_weight_Brier":mean([v[0] for v in fixed]),
            "shuffled_six_sessions_equal_weight_Brier":mean([v[0] for v in rand]),
            "fixed_six_sessions_equal_weight_log_loss":mean([v[1] for v in fixed]),
            "shuffled_six_sessions_equal_weight_log_loss":mean([v[1] for v in rand]),
            "heldout_session_count":12,
            "individual_test_records":TOTAL_SCORED,
        }
    comparisons={}
    for a,b in (
        ("M3_JOINT_LAST","M1_OWN_LAST"),
        ("M4_JOINT_TWO_LAGS","M3_JOINT_LAST"),
        ("M1_OWN_LAST","M0_TREATMENT_PREVALENCE"),
        ("M2_OPPONENT_LAST","M0_TREATMENT_PREVALENCE"),
        ("M5_TFT_NOISY","M0_TREATMENT_PREVALENCE"),
        ("M6_WSLS_NOISY","M0_TREATMENT_PREVALENCE"),
    ):
        pair={}
        for tr in ("fix","rand"):
            differences=[x[0]-y[0] for x,y in zip(scores[a][tr],scores[b][tr])]
            pair[tr]={
                "Brier_delta_compared_to_reference":mean(differences),
                "sessions_better":sum(q<0 for q in differences),
                "sessions_equal":sum(q==0 for q in differences),
                "sessions_worse":sum(q>0 for q in differences),
                "sessions":6,
            }
        comparisons[a+"_VS_"+b]=pair
    return {"models":public,"paired_comparisons":comparisons}


def run(folder):
    sessions,source=read_original_csv(folder)
    output=evaluate(sessions)
    return {
        "research_id":"R073",
        "stage":"E2_HUMAN_IPD_INDIVIDUAL_NEXT_ACTION_MEMORY_LOSO",
        "status":"R073_REAL_HUMAN_12_SESSION_LOSO_COMPLETED",
        "protocol":"protocols/R073_HUMAN_IPD_LAGGED_SOCIAL_MEMORY_LOSO_2026-10-17.md",
        "publisher_paper_DOI":"10.1038/s41598-022-11654-2",
        "source_repository":"eladiomontero/PairwiseStrategies",
        "source_submission_commit":SUBMISSION_COMMIT,
        "source_git_blobs":{n:v[1] for n,v in FILES.items()},
        "source_universe":source,
        "training":"leave out one entire session; 5 other same-treatment sessions; no target labels in outer heldout",
        "heldout_test_rounds_per_person":"3..100 (98), real past own/opponent actions available at t-1 and t-2",
        "scoring":"one-step teacher-forced individual choice conditional on actual previous actions",
        "Brier_and_logloss_session_macro":output["models"],
        "session_equal_paired_Brier_comparisons":output["paired_comparisons"],
        "smoothing_alpha_fixed_before_results":ALPHA,
        "deterministic_reference_observation_flip":NOISE,
        "original_author_hmm_clusters":"NOT_REPRODUCED",
        "author_submission_equals_final_Dryad":"NOT_VERIFIED",
        "causal_psychological_memory_effect":"NOT_IDENTIFIED",
        "cross_society_historical_evolution":"NOT_STUDIED",
        "independent_E3":"OPEN",
        "individual_ids_or_rows_exported":False,
        "pesen_v01":"FROZEN",
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--source-dir",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    try:
        output=run(args.source_dir)
    except (OSError,ValueError,UnicodeError,csv.Error) as e:
        output={"research_id":"R073","status":"REAL_HUMAN_E2_FAIL_CLOSED",
                "error_type":type(e).__name__,
                "bounded_message":str(e)[:120] if isinstance(e,ValueError) else "SOURCE_IO_OR_CSV",
                "individual_records_exported":False,
                "pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(output,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":output["status"],
        "source_actions":output.get("source_universe",{}).get("individual_source_decisions"),
        "scored_targets":output.get("source_universe",{}).get("individual_scorable_outcomes"),
        "Brier_macro":{k:v["all_12_sessions_equal_weight_Brier"] for k,v in
                       output.get("Brier_and_logloss_session_macro",{}).items()},
        "primary_comparison":{k:v for k,v in
                              output.get("session_equal_paired_Brier_comparisons",{}).items()
                              if k.startswith("M3_") or k.startswith("M4_")},
    },sort_keys=True))
    if output["status"]!="R073_REAL_HUMAN_12_SESSION_LOSO_COMPLETED":
        raise RuntimeError("Real source-pinned R073 session holdout human study failed")


if __name__=="__main__":main()
