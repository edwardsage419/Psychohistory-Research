#!/usr/bin/env python3
"""R106 D: frozen original 26-session UK dyadic PD source Brier M0..M4.

True original human actions are accessed only after R106 A/B/C2 and D
prescore protocols were committed. No identifiers or human action rows output.
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
    URL,CAP,ExactRedirect,SourceError,validate_url
)
from r106_phase_b_2025_publisher_dta_header_variables_nobs_only import PINNED_SHA256
from r106_phase_c2_2025_original_sessionid_global_ID_person_partner_roster import (
    source_true_roster,pos_int
)

BEHAVIOR_FIELDS=("sessionid","ID","Group","Period","part","game",
                 "practiceperiod","left","otherleft","p2otherleft")
MODELS=("M0","M1","M2","M3","M4")
CONTRASTS=(("M2","M3","M3_vs_M2_peer_specific"),
           ("M4","M3","M3_vs_M4_donor_sham"),
           ("M1","M3","M3_vs_M1_own_only"),
           ("M1","M2","M2_vs_M1_shrink_only"),
           ("M0","M3","M3_vs_M0_external"))

def binary(x):
    # Missing and categorical/string encodings must not be silently coerced.
    if type(x) in (int,float) and math.isfinite(x) and x in (0,1):
        return int(x)
    raise SourceError("R106_D_ORIGINAL_BINARY_LEFT_OR_OTHERLEFT_CODE_NOT_0_1")

def optional_binary(x):
    if type(x) in (int,float) and math.isfinite(x) and x in (0,1):
        return int(x)
    return None

def phase2_rows(data):
    """Decode only pre-declared original behavioral and structural fields."""
    from pandas.io.stata import StataReader
    with StataReader(io.BytesIO(data),convert_categoricals=False) as r:
        frame=r.read(columns=list(BEHAVIOR_FIELDS),
                     convert_categoricals=False,convert_dates=False)
    if len(frame)!=3620 or tuple(frame.columns)!=BEHAVIOR_FIELDS:
        raise SourceError("R106_D_ORIGINAL_ACTION_COLUMN_OR_3620_ROW_UNIVERSE_DIFFERS")
    out=[]
    for source_record in frame.itertuples(index=False,name=None):
        rec=dict(zip(BEHAVIOR_FIELDS,source_record))
        sid=pos_int(rec["sessionid"])
        pid=pos_int(rec["ID"])
        group=pos_int(rec["Group"])
        t=pos_int(rec["Period"])
        part=pos_int(rec["part"])
        game=pos_int(rec["game"])
        k=pos_int(rec["practiceperiod"])
        if None in (sid,pid,group,t,part,game,k) or part!=2:
            raise SourceError("R106_D_INVALID_ORIGINAL_STAGE2_EVENT_IDENTITIES")
        act=binary(rec["left"])
        reported_partner=binary(rec["otherleft"])
        out.append({
            "s":sid,"p":pid,"g":group,"t":t,"part":part,"game":game,"k":k,
            "a":act,"reported_peer":reported_partner,
            "reported_previous_peer":optional_binary(rec["p2otherleft"]),
        })
    return out

def estimate(ones,n):
    # Fixed Laplace pseudocount specified before any outcome access.
    return (1+ones)/(2+n)

def loss(rows, predicate=None):
    rs=rows if predicate is None else [r for r in rows if predicate(r)]
    if not rs:
        return {"target_count":0,"MSE":{m:None for m in MODELS},
                "gains":{name:None for _,_,name in CONTRASTS}}
    mse={m:math.fsum(z["l"][m] for z in rs)/len(rs) for m in MODELS}
    return {"target_count":len(rs),
            "MSE":mse,
            "gains":{name:mse[a]-mse[b] for a,b,name in CONTRASTS}}

def evaluate(rows,*,enforce_real_universe=True):
    if enforce_real_universe and len(rows)!=3620:
        raise SourceError("R106_D_ORIGINAL_SOURCE_ACTION_TOTAL_NOT_3620")
    people=defaultdict(set)
    unique={}
    pairs=defaultdict(list)
    period_k_counts=defaultdict(lambda:[0,0])
    for r in rows:
        sid,p,t,g,k,game=r["s"],r["p"],r["t"],r["g"],r["k"],r["game"]
        key=(sid,p,t)
        if key in unique:
            raise SourceError("R106_D_ACTOR_PERIOD_DUPLICATED")
        unique[key]=r
        people[sid].add(p)
        pairs[(sid,g,t)].append(r)
        cnt=period_k_counts[(sid,k)]
        cnt[0]+=r["a"]
        cnt[1]+=1
    if enforce_real_universe and (len(people)!=26 or len(set((s,p) for s,ids in people.items() for p in ids))!=260
                                 or any(len(ps)!=10 for ps in people.values())
                                 or sum(len(v) for v in pairs.values())!=3620):
        raise SourceError("R106_D_REAL_26SESSION_260PERSON_SOURCE_SET_CHANGED")
    for dyad in pairs.values():
        if len(dyad)!=2 or dyad[0]["p"]==dyad[1]["p"]:
            raise SourceError("R106_D_SOURCE_DYAD_NEEDS_EXACT_TWO_DISTINCT_IDS")
        a,b=dyad
        if a["game"]!=b["game"] or a["k"]!=b["k"]:
            raise SourceError("R106_D_PAIR_GAME_OR_STAGE_PERIOD_MISMATCH")
        if a["reported_peer"]!=b["a"] or b["reported_peer"]!=a["a"]:
            raise SourceError("R106_D_ORIGINAL_CURRENT_COUNTERPART_ACTION_NOT_RECIPROCAL")
    sessions=sorted(people)
    scored=[]
    session_details=[]
    eligible_sessions=0
    structurally_eligible=0
    excluded=Counter()
    for sid in sessions:
        per_session=[]
        donor=sessions[(sessions.index(sid)+1)%len(sessions)]
        for person in sorted(people[sid]):
            obs=[x for (s,p,t),x in unique.items() if s==sid and p==person]
            for now in sorted(obs,key=lambda x:x["t"]):
                if now["k"]<=1:
                    excluded["first_stage_period"]+=1
                    continue
                prev=unique.get((sid,person,now["t"]-1))
                if prev is None:
                    excluded["missing_own_previous_round"]+=1
                    continue
                prev_pair=pairs.get((sid,prev["g"],prev["t"]))
                current_pair=pairs.get((sid,now["g"],now["t"]))
                if not prev_pair or not current_pair:
                    raise SourceError("R106_D_ORIGINAL_PAIR_SOURCE_EVENT_MISSING")
                prev_ids={z["p"] for z in prev_pair}
                curr_ids={z["p"] for z in current_pair}
                if (prev["g"]!=now["g"] or prev["game"]!=now["game"] or
                    now["k"]!=prev["k"]+1 or prev_ids!=curr_ids):
                    excluded["rematch_or_noncontiguous_previous_source_pair"]+=1
                    continue
                structurally_eligible+=1
                previous_peer=[z for z in prev_pair if z["p"]!=person]
                if len(previous_peer)!=1:
                    raise SourceError("R106_D_PREVIOUS_PARTNER_ID_NOT_UNIQUE")
                peer_lag=previous_peer[0]["a"]
                if now["reported_previous_peer"] is None or now["reported_previous_peer"]!=peer_lag:
                    raise SourceError("R106_D_AUTHOR_PREVIOUS_COUNTERPART_LAG_NOT_MATCHED")
                k=now["k"]
                if k<2:
                    raise SourceError("R106_D_SOURCE_STAGE_PERIOD_INVALID")
                # Fixed baseline excludes *entire* target original session, not
                # just the current actor/group.
                other_ones=0;other_n=0
                for s in sessions:
                    if s!=sid:
                        vals=period_k_counts.get((s,k))
                        if vals:
                            other_ones+=vals[0];other_n+=vals[1]
                q_current=estimate(other_ones,other_n)
                other_prev_ones=0;other_prev_n=0
                for s in sessions:
                    if s!=sid:
                        vals=period_k_counts.get((s,k-1))
                        if vals:
                            other_prev_ones+=vals[0];other_prev_n+=vals[1]
                q_prev=estimate(other_prev_ones,other_prev_n)
                donor_prev=period_k_counts.get((donor,k-1),[0,0])
                q_sham=estimate(donor_prev[0],donor_prev[1])
                own=prev["a"]
                target=now["a"]
                preds={
                    "M0":q_current,
                    "M1":float(own),
                    "M2":0.5*own+0.5*q_prev,
                    "M3":0.5*own+0.5*peer_lag,
                    "M4":0.5*own+0.5*q_sham,
                }
                if any(not math.isfinite(p) or not 0<=p<=1 for p in preds.values()):
                    raise SourceError("R106_D_INVALID_PRESCORE_FORECAST_PROBABILITY")
                per_session.append({
                    "k":k,
                    "l":{model:(target-pred)**2 for model,pred in preds.items()},
                })
        if per_session:
            eligible_sessions+=1
        scored.extend(per_session)
        session_details.append({
            "anonymous_original_lab_session_slot":sessions.index(sid)+1,
            "source_people_in_lab_session":len(people[sid]),
            "all_recorded":loss(per_session),
            "early_k2_to_k3":loss(per_session,lambda x:x["k"]<=3),
            "late_k4_plus":loss(per_session,lambda x:x["k"]>=4),
        })
    if len(scored)!=structurally_eligible:
        raise SourceError("R106_D_ELIGIBLE_TARGET_UNIVERSE_COUNT_MISMATCH")
    if enforce_real_universe and (len(scored)<800 or eligible_sessions<24 or sum(excluded.values())+len(scored)!=3620):
        raise SourceError("R106_D_PRE_FROZEN_800_AND_24SESSION_TARGET_GATE_NOT_MET")
    directions={}
    for _,_,name in CONTRASTS:
        arr=[z["all_recorded"]["gains"][name] for z in session_details
             if z["all_recorded"]["gains"][name] is not None]
        directions[name]={
            "positive_original_lab_sessions":sum(v>0 for v in arr),
            "negative_original_lab_sessions":sum(v<0 for v in arr),
            "zero_original_lab_sessions":sum(v==0 for v in arr),
        }
    return {
        "research_id":"R106","phase":"D",
        "status":"R106_D_REAL_2025_UK_LAB_26SESSION_DYADIC_EQUAL_SHRINK_E2",
        "original_source_SHA256":PINNED_SHA256,
        "source_all_stage2_original_person_round_rows":len(rows),
        "source_true_original_lab_sessions":len(people),
        "source_true_distinct_session_persons":sum(map(len,people.values())),
        "source_original_pair_rounds":len(pairs),
        "source_structurally_eligible_target_count":structurally_eligible,
        "source_frozen_excluded_target_counts":dict(sorted(excluded.items())),
        "source_all_eligible_target_count":len(scored),
        "source_sessions_with_at_least_one_eligible_target":eligible_sessions,
        "true_otherleft_current_partner_action_disagreements":0,
        "true_p2otherleft_previous_partner_action_disagreements":0,
        "M0_M4_model_definitions":{
            "M0":"other 25 original source sessions same practiceperiod k, fixed Laplace pseudo 1/2",
            "M1":"focal human own observed previous action",
            "M2":"0.5 own prior action + 0.5 other 25 sessions practiceperiod k-1 mean Laplace",
            "M3":"0.5 own prior action + 0.5 exact same previous partner action",
            "M4":"0.5 own prior action + 0.5 sorted cyclic donor session practiceperiod k-1 mean Laplace",
        },
        "primary_target":"source left current binary 0/1 (cooperation semantics not claimed)",
        "primary_loss":"Brier score lower better",
        "overall_all_eligible":loss(scored),
        "early_practiceperiod_k2_to_k3":loss(scored,lambda x:x["k"]<=3),
        "late_practiceperiod_k4_plus":loss(scored,lambda x:x["k"]>=4),
        "anonymous_original_lab_session_results":session_details,
        "original_lab_session_contrast_directions":directions,
        "original_human_ID_or_action_rows_exported":False,
        "not_R073_exact_frozen_dyadic_score_protocol":True,
        "not_calendar_prospective":True,
        "not_causal_opponent_social_learning":True,
        "PESEN_v0_1":"FROZEN",
    }

def score_original(raw):
    roster=source_true_roster(raw)
    if roster["status"]!="R106_C2_GENUINE_2025_RECRUITED_26SESSION_260_ID_SOURCE_DYADS_ELIGIBLE":
        raise SourceError("R106_D_PREVIOUS_NONBEHAVIOR_ORIGINAL_DYAD_GATE_NOT_MET")
    return evaluate(phase2_rows(raw),enforce_real_universe=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=pathlib.Path,required=True)
    args=p.parse_args()
    try:
        validate_url(URL)
        req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R106-D-FROZEN-26-Session-2025-True-Dyad-Equal-Shrink-E2/1.0"})
        with urllib.request.build_opener(ExactRedirect()).open(req,timeout=65) as response:
            validate_url(response.geturl())
            raw=response.read(CAP+1)
        result=score_original(raw)
    except (ValueError,OSError,TypeError,KeyError,ImportError,IndexError) as e:
        result={
            "research_id":"R106","phase":"D",
            "status":"R106_D_ORIGINAL_BEHAVIOR_GATE_FAIL_CLOSED",
            "safe_failure":str(e) if isinstance(e,SourceError) else "R106_D_REAL_SOURCE_MODEL_NOT_VALIDATED",
            "real_human_model_scores":0,
            "PESEN_v0_1":"FROZEN",
        }
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps(result,sort_keys=True))
    if result["status"]!="R106_D_REAL_2025_UK_LAB_26SESSION_DYADIC_EQUAL_SHRINK_E2":
        raise SystemExit(1)

if __name__=="__main__":
    main()
