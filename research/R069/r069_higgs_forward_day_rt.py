#!/usr/bin/env python3
"""R069 real-day forward RT behavior forecast, not IC/Watts contagion fit.

All features and training labels are from days strictly before each score day.
Source user identifiers never leave in-memory cohorts or appear in output.
"""
from __future__ import annotations
import argparse
from collections import Counter,defaultdict
import hashlib,json,math
from pathlib import Path
from r069_higgs_temporal_source_audit import (
    download,original_gzip_lines,require_unsigned_id,require_timestamp,
    MAX_ACTIVITY_ROWS,START,END,TYPES,
)

SHA="901b199716a23b0fc0371705e3ae9941b5c9493277aec65456abc4988674ad79"
COMPRESSED_BYTES=4169461
TOTAL_EVENTS=563069
EXPECTED_TYPES={"RT":354930,"MT":171237,"RE":36902}
DAY_SECONDS=86400
KAPPA=100.0
FAMILIES=("POOLED_GLOBAL","YESTERDAY_GLOBAL","ACTIVITY_HISTORY",
          "ACTIVITY_PLUS_TARGET_PROXY")
SCORE_DAYS=(3,4,5,6)  # July 4--7 (day zero is July 1)


def validate_source(raw):
    if len(raw)!=COMPRESSED_BYTES or hashlib.sha256(raw).hexdigest()!=SHA:
        raise ValueError("ORIGINAL_SNAP_HIGGS_ACTIVITIES_SHA_OR_LENGTH_CHANGED")
    by_day=[[] for _ in range(7)]
    types=Counter()
    for row in original_gzip_lines(raw,MAX_ACTIVITY_ROWS):
        if len(row)!=4:raise ValueError("ORIGINAL_ACTIVITY_COLUMNS_CHANGED")
        a,b=require_unsigned_id(row[0]),require_unsigned_id(row[1])
        ts=require_timestamp(row[2])
        kind=row[3]
        if kind not in TYPES:raise ValueError("ORIGINAL_ACTIVITY_TYPE_CHANGED")
        if not START<=ts<END:raise ValueError("SOURCE_EVENT_OUTSIDE_PUBLISHED_WEEK")
        by_day[(ts-START)//DAY_SECONDS].append((a,b,kind))
        types[kind]+=1
    if sum(types.values())!=TOTAL_EVENTS or dict(types)!=EXPECTED_TYPES:
        raise ValueError("ORIGINAL_563069_ROW_TYPE_COUNTS_CHANGED")
    if any(not events for events in by_day):
        raise ValueError("PUBLISHED_WEEK_DAY_WITHOUT_EVENTS")
    return by_day


def activity_bin(count):
    if type(count) is not int or count<1:
        raise ValueError("activity count must be positive integer")
    return 0 if count==1 else 1 if count<=4 else 2


def _add_bucket(table,key,y):
    if key not in table:table[key]=[0,0]
    table[key][0]+=1
    table[key][1]+=int(y)


def create_cohorts(by_day):
    if len(by_day)!=7:raise ValueError("EXACT_SEVEN_SOURCE_DAYS_REQUIRED")
    seen=set()
    counts=Counter()
    contacts=defaultdict(set)
    yesterday_any=set()
    yesterday_rt=set()
    cohort=[]
    for d,rows in enumerate(by_day):
        now_rt={a for a,b,kind in rows if kind=="RT"}
        if d>=1:
            if not seen:raise ValueError("EARLIER_DAY_RISK_SET_EMPTY")
            basic={}
            social={}
            social_true=0
            positives=0
            for u in seen:
                y=int(u in now_rt)
                recent_rt=int(u in yesterday_rt)
                recent_any=int(u in yesterday_any)
                base=(recent_rt,recent_any,activity_bin(counts[u]))
                peer=int(not contacts[u].isdisjoint(yesterday_rt))
                _add_bucket(basic,base,y)
                _add_bucket(social,base+(peer,),y)
                positives+=y
                social_true+=peer
            if sum(n for n,_ in basic.values())!=len(seen):
                raise ValueError("SCORE_RISK_COHORT_LOSS")
            cohort.append({
                "day_index":d,
                "risk_accounts":len(seen),
                "RT_accounts_in_at_risk_cohort":positives,
                "RT_accounts_first_appearing_today_excluded":len(now_rt-seen),
                "distinct_RT_accounts_today":len(now_rt),
                "peer_activity_proxy_true_risk_accounts":social_true,
                "total_event_rows_today":len(rows),
                "basic":basic,
                "social":social,
            })
        current_any=set()
        current_rt=set()
        for a,b,kind in rows:
            seen.add(a)
            counts[a]+=1
            contacts[a].add(b)
            current_any.add(a)
            if kind=="RT":current_rt.add(a)
        yesterday_any=current_any
        yesterday_rt=current_rt
    if len(cohort)!=6 or any(c["risk_accounts"]<=0 for c in cohort):
        raise ValueError("SIX_DAY_HISTORICAL_COHORT_REQUIREMENT_FAILED")
    return cohort


def pool_counts(training,key):
    pooled={}
    for day in training:
        for group,(n,y) in day[key].items():
            if group not in pooled:pooled[group]=[0,0]
            pooled[group][0]+=n
            pooled[group][1]+=y
    return pooled


def rate(pos,n):
    if type(pos) is not int or type(n) is not int or not 0<=pos<=n or n<=0:
        raise ValueError("illegal risk or positive count")
    z=(pos+1)/(n+2)
    if not 0<z<1:raise ValueError("probability outside open interval")
    return z


def shrink(group,group_counts,prior):
    n,pos=group_counts.get(group,(0,0))
    p=(pos+KAPPA*prior)/(n+KAPPA)
    if not 0<p<1:raise ValueError("invalid shrinkage probability")
    return p


def daily_prediction(cohorts,target_d):
    if target_d not in SCORE_DAYS:raise ValueError("target not in fixed test dates")
    history=[day for day in cohorts if day["day_index"]<target_d]
    train=[day for day in history if day["day_index"]>=1]
    today=next(day for day in cohorts if day["day_index"]==target_d)
    if len(train)!=target_d-1 or any(day["day_index"]>=target_d for day in train):
        raise ValueError("TRAINING_CONTAINS_FUTURE_OR_TEST_DAY")
    total_n=sum(z["risk_accounts"] for z in train)
    total_pos=sum(z["RT_accounts_in_at_risk_cohort"] for z in train)
    prior=rate(total_pos,total_n)
    yesterday=train[-1]
    yesterday_rate=rate(yesterday["RT_accounts_in_at_risk_cohort"],
                        yesterday["risk_accounts"])
    basic=pool_counts(train,"basic")
    social=pool_counts(train,"social")
    if sum(n for n,_ in basic.values())!=total_n or sum(n for n,_ in social.values())!=total_n:
        raise ValueError("TRAIN_HISTORY_BIN_TOTAL_DRIFT")
    scored={}
    for family in FAMILIES:
        sum_log=0.
        sum_brier=0.
        ntotal=0
        pos_total=0
        for key,(n,pos) in today["social"].items():
            if family=="POOLED_GLOBAL":
                p=prior
            elif family=="YESTERDAY_GLOBAL":
                p=yesterday_rate
            elif family=="ACTIVITY_HISTORY":
                p=shrink(key[:3],basic,prior)
            elif family=="ACTIVITY_PLUS_TARGET_PROXY":
                p=shrink(key,social,prior)
            else:
                raise ValueError("MODEL_NOT_PRE_REGISTERED")
            sum_log-=pos*math.log(p)+(n-pos)*math.log1p(-p)
            sum_brier+=pos*(1-p)**2+(n-pos)*p*p
            pos_total+=pos;ntotal+=n
        if ntotal!=today["risk_accounts"] or pos_total!=today["RT_accounts_in_at_risk_cohort"]:
            raise ValueError("HELDOUT_COHORT_NOT_SHARED_BETWEEN_MODELS")
        scored[family]={
            "average_binary_logloss_nats":sum_log/ntotal,
            "average_Brier_loss":sum_brier/ntotal,
            "scored_account_days":ntotal,
            "outcome_positive_account_days":pos_total,
        }
    return {
        "UTC_day":f"2012-07-{target_d+1:02d}",
        "training_labels_end_before_UTC_day":f"2012-07-{target_d+1:02d}",
        "training_days":target_d-1,
        "risk_accounts":today["risk_accounts"],
        "RT_accounts_in_at_risk_cohort":today["RT_accounts_in_at_risk_cohort"],
        "new_RT_accounts_excluded":today["RT_accounts_first_appearing_today_excluded"],
        "peer_activity_proxy_true_risk_accounts":today["peer_activity_proxy_true_risk_accounts"],
        "model_scores":scored,
    }


def evaluate_day_cohorts(cohorts):
    scores=[daily_prediction(cohorts,d) for d in SCORE_DAYS]
    if len(scores)!=4:raise ValueError("EXPECTED_FOUR_FORWARD_DAYS")
    results={}
    for model in FAMILIES:
        mean=lambda key:sum(day["model_scores"][model][key] for day in scores)/len(scores)
        total=sum(day["risk_accounts"] for day in scores)
        results[model]={
            "primary_four_UTC_days_equal_binary_logloss_nats":mean("average_binary_logloss_nats"),
            "secondary_all_scored_account_days_weighted_logloss_nats":
                sum(day["model_scores"][model]["average_binary_logloss_nats"]*day["risk_accounts"] for day in scores)/total,
            "primary_four_days_equal_Brier":mean("average_Brier_loss"),
            "secondary_all_scored_account_days_weighted_Brier":
                sum(day["model_scores"][model]["average_Brier_loss"]*day["risk_accounts"] for day in scores)/total,
            "test_day_count":4,
            "test_scored_account_days":total,
        }
    return {
        "scored_UTC_days":scores,
        "model_summary":results,
        "evaluated_days_are_sequential":"2012-07-04 through 2012-07-07",
        "source_person_ID_or_event_records_exported":False,
    }


def evaluate_real(raw):
    by_day=validate_source(raw)
    cohorts=create_cohorts(by_day)
    result=evaluate_day_cohorts(cohorts)
    return {
        "research_id":"R069",
        "stage":"E2_SNAP_HIGGS_TIME_FORWARD_RT_ACTIVITY",
        "status":"REAL_HIGGS_FORWARD_DAY_RT_PREDICTION_PASS_BOUNDED",
        "protocol":"protocols/R069_E2_HIGGS_FORWARD_DAY_RT_2026-10-16.md",
        "source_url":"https://snap.stanford.edu/data/higgs-activity_time.txt.gz",
        "source_sha256":SHA,
        "source_gzip_bytes":COMPRESSED_BYTES,
        "original_week_event_rows":TOTAL_EVENTS,
        "original_activity_event_types":EXPECTED_TYPES,
        "time_features":"only all prior days, no same-day RT labels or full-window RT graph",
        "at_risk_definition":"actor with a prior A-initiated RT/MT/RE action before UTC day starts",
        "prediction_target":"at least one observed RT from at-risk actor during current UTC day",
        "training_window":"2012-07-02 forward daily expanding, score July 04--07",
        "empirical_risk_group_prior_pseudocount":KAPPA,
        **result,
        "causal_diffusion_inference":"NOT_IDENTIFIED",
        "IC_attempt_or_failed_exposure_observed":False,
        "noncommercial_or_republication_license_assumed":False,
        "independent_E3":"OPEN",
        "pesen_v01":"FROZEN",
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    try:
        result=evaluate_real(download("activity"))
    except (ValueError,OSError,EOFError,UnicodeError) as exc:
        result={
            "research_id":"R069",
            "stage":"E2_SNAP_HIGGS_TIME_FORWARD_RT_ACTIVITY",
            "status":"SOURCE_OR_TIME_HOLDOUT_FAIL_CLOSED",
            "error_type":type(exc).__name__,
            "error_code":str(exc)[:120] if isinstance(exc,ValueError) else "ORIGINAL_DATA_RETRIEVAL_OR_GZIP_ERROR",
            "causal_diffusion_inference":"NOT_IDENTIFIED",
            "pesen_v01":"FROZEN",
        }
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "daily_base_population":[(x["UTC_day"],x["risk_accounts"],x["RT_accounts_in_at_risk_cohort"])
            for x in result.get("scored_UTC_days",[])],
        "models":{k:(v["primary_four_UTC_days_equal_binary_logloss_nats"],
                     v["primary_four_days_equal_Brier"])
                  for k,v in result.get("model_summary",{}).items()},
        "error":result.get("error_code"),
    },sort_keys=True))
    if result["status"]!="REAL_HIGGS_FORWARD_DAY_RT_PREDICTION_PASS_BOUNDED":
        raise RuntimeError("Real original SNAP Higgs forward-day heldout results not established")


if __name__=="__main__":main()
