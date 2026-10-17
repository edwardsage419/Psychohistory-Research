#!/usr/bin/env python3
"""R074 independent 2011 first-party human IPD session-heldout replication.

The R073 frozen model implementation is imported and exact Git blob SHA checked.
Only anonymized aggregate model scores leave memory / the CI runner.
"""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
R073_PATH = HERE.parent / "R073" / "r073_human_ipd_memory_loso.py"
R073_GIT_BLOB = "c8a0b47fd27bf05e7be5b87419a0824355fc911a"
SOURCE_SHA256 = "357a12968546a8d9002c912c1f499e02e93d59113d2a0928de2dee48323a0ae6"
EXPECTED_SESSION_COUNT = 18
EXPECTED_HUMAN_ROWS = 37042
EXPECTED_SESSION_PERSON_SLOTS = 266
EXPECTED_EVENTS = 15338
SOURCE_URL = "https://gfrechette.com/data/Dal_Bo_2011a_data.txt"
TRANSFER_PROTOCOL = "protocols/R074_DALBO_AUTHOR_INDEPENDENT_HUMAN_E3_TRANSFER_FREEZE_2026-10-17.md"

from r074_dalbo_author_source_gate import audit, source_rows

sys.path.insert(0, str(R073_PATH.parent))
from r073_human_ipd_memory_loso import (
    MODEL_NAMES, CONDITIONAL_MODELS, state_for, predict, brier, logloss,
    ALPHA, NOISE,
)

PAIRS = (
    ("M3_JOINT_LAST", "M1_OWN_LAST"),
    ("M4_JOINT_TWO_LAGS", "M3_JOINT_LAST"),
    ("M1_OWN_LAST", "M0_TREATMENT_PREVALENCE"),
    ("M2_OPPONENT_LAST", "M0_TREATMENT_PREVALENCE"),
    ("M5_TFT_NOISY", "M0_TREATMENT_PREVALENCE"),
    ("M6_WSLS_NOISY", "M0_TREATMENT_PREVALENCE"),
)
EXPECTED_NAMES = (
    "M0_TREATMENT_PREVALENCE", "M1_OWN_LAST", "M2_OPPONENT_LAST",
    "M3_JOINT_LAST", "M4_JOINT_TWO_LAGS", "M5_TFT_NOISY", "M6_WSLS_NOISY",
)


def verify_frozen_code():
    content = R073_PATH.read_bytes()
    digest = hashlib.sha1(b"blob " + str(len(content)).encode("ascii") +
                          b"\0" + content).hexdigest()
    if digest != R073_GIT_BLOB or MODEL_NAMES != EXPECTED_NAMES:
        raise ValueError("R073_FROZEN_MODEL_CODE_CHANGED")
    if ALPHA != 20.0 or NOISE != .05:
        raise ValueError("R073_FROZEN_PARAMETERS_CHANGED")


def prepare_external_sessions(source: bytes):
    # Scope and structural checks happen before any human score computation.
    if hashlib.sha256(source).hexdigest() != SOURCE_SHA256:
        raise ValueError("FIRST_PARTY_AUTHOR_SOURCE_SHA256_MISMATCH")
    a = audit(source)
    if (a["source_rows"] != EXPECTED_HUMAN_ROWS or
        a["distinct_sessions"] != EXPECTED_SESSION_COUNT or
        a["session_person_slots"] != EXPECTED_SESSION_PERSON_SLOTS or
        a["candidate_t3_plus_actions"] != EXPECTED_EVENTS or
        len(a["treatments"]) != 6 or
        any(x["session_count"] != 3 for x in a["treatments"])):
        raise ValueError("FIRST_PARTY_AUTHOR_SOURCE_UNIVERSE_CHANGED")
    rows = source_rows(source)
    id_namespace = {}
    match_round_pair = defaultdict(list)
    treatment_for_session = {}
    for date, r, delta, match, rd, group, person, action in rows:
        # Within-session IDs are known to be stable. Reused numbers across
        # dates are an unresolved potential re-enrolment and stop scoring.
        prior = id_namespace.setdefault(person, date)
        if prior != date:
            raise ValueError("POSSIBLE_CROSS_SESSION_ID_REUSE")
        treatment_for_session[date] = (r, delta)
        match_round_pair[(date, match, rd, group)].append((person, action))
    histories = defaultdict(dict)
    for (date, match, rd, group), pair in match_round_pair.items():
        if len(pair) != 2 or pair[0][0] == pair[1][0]:
            raise ValueError("SOURCE_PAIR_INTEGRITY_BROKEN")
        (i, ai), (j, aj) = pair
        histories[(date, match, i)][rd] = (ai, aj)
        histories[(date, match, j)][rd] = (aj, ai)
    # Reconstruct t>=3 only within the same pair's match. No future action
    # may enter one-step conditional prediction features.
    grouped = defaultdict(list)
    for (date, match, person), hist in histories.items():
        rounds = sorted(hist)
        if rounds != list(range(1, len(hist)+1)):
            raise ValueError("EXTERNAL_MATCH_HISTORY_GAP")
        for t in range(3, len(hist)+1):
            own1, opp1 = hist[t-1]
            own2, opp2 = hist[t-2]
            y = hist[t][0]
            grouped[date].append((own1, opp1, own2, opp2, y))
    sessions = {
        date: {"treatment": treatment_for_session[date], "events": events}
        for date, events in grouped.items()
    }
    if set(treatment_for_session) != set(sessions):
        raise ValueError("SESSION_HAS_NO_SCORABLE_EVENTS")
    if sum(len(x["events"]) for x in sessions.values()) != EXPECTED_EVENTS:
        raise ValueError("EXTERNAL_SCORING_UNIVERSE_NOT_EQUAL_15338")
    return sessions, a


def fit_other_sessions(sessions, heldout):
    treatment = sessions[heldout]["treatment"]
    other = [s for s, detail in sessions.items()
             if s != heldout and detail["treatment"] == treatment]
    if len(other) != 2:
        raise ValueError("REQUIRES_TWO_OTHER_SAME_TREATMENT_SESSIONS")
    events = [ev for s in other for ev in sessions[s]["events"]]
    if not events:
        raise ValueError("EMPTY_EXTERNAL_TRAINING_RISK_SET")
    p0 = sum(x[4] for x in events)/len(events)
    if not 0 < p0 < 1:
        raise ValueError("DEGENERATE_TRAIN_PREVALENCE")
    tables={}
    for model in CONDITIONAL_MODELS:
        counts=defaultdict(lambda:[0,0])
        for ev in events:
            key=state_for(model,ev)
            counts[key][0]+=ev[4]
            counts[key][1]+=1
        tables[model]={k:tuple(v) for k,v in counts.items()}
    return {
        "train_only_prevalence":p0,
        "trained_from_other_sessions_same_treatment":2,
        "train_target_count":len(events),
        "state_counts":tables,
    }


def evaluate_external(sessions):
    if not sessions:
        raise ValueError("NO_SESSIONS")
    treatments = defaultdict(list)
    for session, data in sessions.items():
        if not data["events"]:
            raise ValueError("NO_TEST_EVENTS_IN_SESSION")
        if any(len(rec) != 5 or any(type(x) is not int or x not in (0,1)
                                   for x in rec) for rec in data["events"]):
            raise ValueError("INVALID_EVENT_HISTORY")
        treatments[data["treatment"]].append(session)
    if any(len(v) < 2 for v in treatments.values()):
        raise ValueError("UNTRAINABLE_SINGLE_SESSION_TREATMENT")
    scores = {}
    for heldout, data in sessions.items():
        fit = fit_other_sessions(sessions, heldout)
        record = {}
        for model in MODEL_NAMES:
            total_b = total_l = 0.0
            for ev in data["events"]:
                p = predict(model,ev,fit)
                total_b += brier(ev[4],p)
                total_l += logloss(ev[4],p)
            record[model] = (total_b/len(data["events"]),
                             total_l/len(data["events"]))
        scores[heldout] = record
    def avg(nums):
        return sum(nums)/len(nums)
    ordered_sessions=sorted(sessions)
    ordered_treatments=sorted(treatments)
    def treatment_tag(tr):
        return "R"+str(tr[0])+"_DELTA"+tr[1].replace(".","p")
    output_models={}
    for model in MODEL_NAMES:
        output_models[model]={
            "all_sessions_equal_weight_Brier":avg([scores[s][model][0] for s in ordered_sessions]),
            "all_sessions_equal_weight_log_loss":avg([scores[s][model][1] for s in ordered_sessions]),
            "per_treatment_session_equal":{
                treatment_tag(tr):{
                    "sessions":len(treatments[tr]),
                    "Brier":avg([scores[s][model][0] for s in treatments[tr]]),
                    "log_loss":avg([scores[s][model][1] for s in treatments[tr]]),
                } for tr in ordered_treatments
            },
        }
    comparisons={}
    for a,b in PAIRS:
        key=a+"_VS_"+b
        by_group={}
        for tr in ordered_treatments:
            differences=[scores[s][a][0]-scores[s][b][0] for s in treatments[tr]]
            by_group[treatment_tag(tr)]={
                "Brier_delta":avg(differences),
                "sessions_better":sum(x<0 for x in differences),
                "sessions_equal":sum(x==0 for x in differences),
                "sessions_worse":sum(x>0 for x in differences),
                "sessions":len(differences),
            }
        all_diffs=[scores[s][a][0]-scores[s][b][0] for s in ordered_sessions]
        comparisons[key]={
            "all_sessions_equal_weight_Brier_delta":avg(all_diffs),
            "all_sessions_better":sum(x<0 for x in all_diffs),
            "all_sessions_equal":sum(x==0 for x in all_diffs),
            "all_sessions_worse":sum(x>0 for x in all_diffs),
            "all_sessions":len(ordered_sessions),
            "per_treatment":by_group,
        }
    return {"model_macro":output_models,"paired_comparisons":comparisons,
            "sessions_equal_weighted":len(sessions),
            "scored_decisions":sum(len(d["events"]) for d in sessions.values()),
            "treatment_count":len(treatments)}


def run(source):
    verify_frozen_code()
    sessions, original = prepare_external_sessions(source)
    result = evaluate_external(sessions)
    return {
        "research_id":"R074",
        "status":"R074_INDEPENDENT_REAL_HUMAN_EXPERIMENT_SESSION_LOSO_EXECUTED",
        "evidence_level":"INDEPENDENT_AUTHOR_EXPERIMENT_WITHIN_SOURCE_SESSION_LOSO",
        "protocol_frozen_before_scores":TRANSFER_PROTOCOL,
        "original_publisher_DOI":"10.1257/aer.101.1.411",
        "original_author_url":SOURCE_URL,
        "original_author_source_sha256":SOURCE_SHA256,
        "original_author_source_bytes":len(source),
        "original_session_count":original["distinct_sessions"],
        "original_session_person_slots":original["session_person_slots"],
        "original_human_actions":original["source_rows"],
        "original_pair_match_rounds":original["paired_match_rounds"],
        "models":list(MODEL_NAMES),
        "train_rule":"other two complete original sessions within same treatment",
        "risk_set":"all t>=3 with own and previous counterpart histories inside original match",
        "scoring_rule":"teacher-forced one-step; each session then 18 sessions equal weight",
        "fixed_alpha":ALPHA,"fixed_TFT_WSLS_noise":NOISE,
        "frozen_R073_code_git_blob":R073_GIT_BLOB,
        "results":result,
        "R073_E2":"CLOSED_BOUNDED",
        "causal_memory_effect":"NOT_IDENTIFIED",
        "full_cross_session_physical_identity":"NOT_DOCUMENTED_BY_WITHIN_SESSION_IDS",
        "zero_shot_R073_parameter_transfer":"NOT_TESTED",
        "individual_records_exported":False,
        "individual_session_scores_exported":False,
        "PESEN_v0.1":"FROZEN",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        result=run(a.source.read_bytes())
    except (OSError,ValueError,UnicodeError) as exc:
        result={"research_id":"R074","status":"EXTERNAL_HUMAN_E3_FAIL_CLOSED",
                "reason":str(exc)[:110] if isinstance(exc,ValueError) else "SOURCE_IO",
                "individual_records_exported":False,"PESEN_v0.1":"FROZEN"}
    a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "sessions":result.get("results",{}).get("sessions_equal_weighted"),
        "targets":result.get("results",{}).get("scored_decisions"),
        "model_Brier":{m:r["all_sessions_equal_weight_Brier"]
                       for m,r in result.get("results",{}).get("model_macro",{}).items()},
        "paired_Brier":{k:v["all_sessions_equal_weight_Brier_delta"]
                        for k,v in result.get("results",{}).get("paired_comparisons",{}).items()
                        if k.startswith("M3_") or k.startswith("M4_")},
    },sort_keys=True))
    if result["status"] != "R074_INDEPENDENT_REAL_HUMAN_EXPERIMENT_SESSION_LOSO_EXECUTED":
        raise RuntimeError("E3_REAL_SESSION_HELDOUT_FAIL_CLOSED")


if __name__=="__main__":
    main()
