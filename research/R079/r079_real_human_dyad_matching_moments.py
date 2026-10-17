#!/usr/bin/env python3
"""R079: Real original human dyad moment decomposition (descriptive E2 only).

Exact finite-population matching baseline, no intervention identification.
Original rows remain local in CI. Publish ONLY session-equal aggregate moments.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json
from collections import Counter,defaultdict
from fractions import Fraction as F
from pathlib import Path

ORIGINAL_GITHUB_COMMIT="979abf87b5d3cfb7aa8be13b81ef233076c3bb75"
SOURCE_REL="data/csv/subjects.csv"
SOURCE_BYTES=425701
SOURCE_GIT_BLOB="bd4c1550002621bee7dfb50e0d15d317764d1ea9"
PROTOCOL="protocols/R079_INDEPENDENT_HUMAN_DYAD_COVARIANCE_RANDOM_MATCHING_REFERENCE_FREEZE_2026-10-17.md"
REQUIRED=("treatment","session","period","subject","group","action","opp","opp_action","first_player")
TREATMENTS=("NoCondInfo","CondInfo")
ACTION_LEVELS={0,50,100}
MEASURES=("mu","pop_var","pair_cross","random_match_cross","excess_cross","pair_mean_var","random_match_pair_mean_var")
def mean_f(seq):
    a=list(seq)
    if not a:raise ValueError("EMPTY_MOMENT_AGGREGATION")
    return sum(a,F(0))/len(a)
def git_blob(data:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def parse_author_csv(content:bytes, *, verify_source=True):
    if verify_source and (len(content)!=SOURCE_BYTES or git_blob(content)!=SOURCE_GIT_BLOB):
        raise ValueError("R079_AUTHOR_EXACT_GIT_BLOB_SIZE_MISMATCH")
    try:
        reader=csv.DictReader(io.StringIO(content.decode("utf-8-sig"),newline=""))
        cols=reader.fieldnames or []
        if len(set(cols))!=len(cols) or any(x not in cols for x in REQUIRED):
            raise ValueError("R079_REQUIRED_AUTHOR_COLUMN_IDENTITY_FAIL")
        rows=[]
        for r in reader:
            if None in r or any(r.get(x) in ("","NA",None) for x in REQUIRED):
                raise ValueError("R079_REQUIRED_AUTHOR_HUMAN_VALUE_MISSING")
            tr=r["treatment"]
            if tr not in TREATMENTS:
                raise ValueError("R079_UNEXPECTED_TREATMENT_VALUE")
            try:
                session=int(r["session"]);period=int(r["period"])
                subj=int(r["subject"]);group=int(r["group"]);opp=int(r["opp"])
                action=int(r["action"]);opp_action=int(r["opp_action"])
                first_player=str(r["first_player"]).strip().upper()
            except (TypeError,ValueError):
                raise ValueError("R079_NONINTEGER_AUTHOR_SOURCE_PLAYER_OR_ACTION") from None
            if (session<=0 or period<=0 or subj<=0 or group<=0 or opp<=0
                or subj==opp or action not in ACTION_LEVELS
                or opp_action not in ACTION_LEVELS or first_player not in ("0","1","TRUE","FALSE")):
                raise ValueError("R079_REALIZED_DYAD_ACTION_OR_ID_INVALID")
            rows.append({
                "tr":tr,"sess":session,"period":period,"subj":subj,"group":group,
                "opp":opp,"action":action,"opp_action":opp_action,
                "first_player":first_player in ("1","TRUE"),
            })
        if not rows:raise ValueError("R079_EMPTY_AUTHOR_DATA")
        return rows
    except UnicodeError:
        raise ValueError("R079_ORIGINAL_CSV_ENCODING_INVALID") from None

def validate_real_pair_graph(rows):
    """Fails before any score if reciprocal pair/period or cohort keys are wrong."""
    by_stratum=defaultdict(list)
    by_sid=defaultdict(set)
    by_subject=defaultdict(set)
    for r in rows:
        by_stratum[(r["tr"],r["sess"],r["period"])].append(r)
        by_sid[r["sess"]].add(r["tr"])
        by_subject[(r["tr"],r["sess"],r["subj"])].add(r["period"])
    if any(len(conditions)!=1 for conditions in by_sid.values()):
        raise ValueError("R079_SESSION_TREATMENT_NOT_UNIQUE")
    if len(by_sid)<2 or set(tr for tr,_,_ in by_stratum)!=set(TREATMENTS):
        raise ValueError("R079_REQUIRED_TWO_TREATMENTS_MULTIPLE_SESSIONS")
    result={}
    for (tr,sess,period),participants in by_stratum.items():
        n=len(participants)
        if n<2 or n%2!=0:
            raise ValueError("R079_ORIGINAL_SESSION_PERIOD_HAS_ODD_OR_SMALL_HUMAN_UNIVERSE")
        ids=[r["subj"] for r in participants]
        if len(set(ids))!=n:
            raise ValueError("R079_DUPLICATE_SUBJECT_WITHIN_EXPERIMENT_ROUND")
        pairs=defaultdict(list)
        for r in participants:pairs[r["group"]].append(r)
        if len(pairs)*2!=n:
            raise ValueError("R079_GROUP_PAIR_COUNT_INVALID")
        actual_pair_list=[]
        for grp,people in pairs.items():
            if len(people)!=2:
                raise ValueError("R079_TRUE_REAL_HUMAN_DYAD_NOT_TWO_PEOPLE")
            a,b=people
            if (a["opp"]!=b["subj"] or b["opp"]!=a["subj"] or
                a["opp_action"]!=b["action"] or b["opp_action"]!=a["action"]):
                raise ValueError("R079_PARTNER_IDENTITY_OR_REALIZED_ACTION_NOT_RECIPROCAL")
            # First-mover might be assigned within pair; don't require it
            # if original study has a different survey sequencing representation.
            actual_pair_list.append((F(a["action"],100),F(b["action"],100)))
        result[(tr,sess,period)]=actual_pair_list
    sessions=sorted(by_sid)
    by_session_periods=defaultdict(set)
    for (_,sid,t) in by_stratum:by_session_periods[sid].add(t)
    common=sorted({t for (_,_,t) in by_stratum})
    if common!=list(range(1,max(common)+1)) or len(common)!=10:
        raise ValueError("R079_OFFICIAL_TEN_NONPRACTICE_PERIODS_NOT_RECOVERED")
    if any(ts!=set(range(1,11)) for ts in by_session_periods.values()):
        raise ValueError("R079_NOT_ALL_ORIGINAL_SESSIONS_COMPLETE_TEN_PERIODS")
    for key,pers in by_subject.items():
        if pers!=set(range(1,11)):
            raise ValueError("R079_PERSON_WITHIN_SESSION_PERIOD_UNIVERSE_NOT_COMPLETE")
    return result,{
        "source_original_rows":len(rows),
        "original_source_sessions":len(by_sid),
        "treatment_original_session_counts":dict(Counter(next(iter(v)) for v in by_sid.values())),
        "original_experimental_periods":len(common),
        "person_in_source_sessions":len(by_subject),
        "source_session_period_cohorts":len(by_stratum),
        "actual_realized_two_person_dyads":sum(len(v) for v in result.values()),
        "unique_session_period_group_keys":sum(len(v) for v in result.values()),
        "all_dyad_partner_and_action_reciprocals_verified":True,
        "raw_human_rows_exported":False,
    }

def moments_exact(real_pairs):
    n=2*len(real_pairs)
    if n<2:raise ValueError("MOMENT_REQUIRES_AT_LEAST_TWO_HUMANS")
    z=[y for pair in real_pairs for y in pair]
    mu=mean_f(z)
    pv=mean_f((x-mu)**2 for x in z)
    cross=mean_f((a-mu)*(b-mu) for a,b in real_pairs)
    random_ref=-pv/(n-1)
    excess=cross-random_ref
    mvar=mean_f((((a+b)/2)-mu)**2 for a,b in real_pairs)
    random_pair=(pv+random_ref)/2
    if mvar!=(pv+cross)/2 or mvar-random_pair!=excess/2:
        raise ValueError("EXACT_FINITE_MATCHING_VARIANCE_IDENTITY_BROKEN")
    return dict(zip(MEASURES,(mu,pv,cross,random_ref,excess,mvar,random_pair)))

def score_aggregate(rows):
    dyads,universe=validate_real_pair_graph(rows)
    per_session=defaultdict(list)
    per_treat=defaultdict(list)
    session_period_means=defaultdict(dict)
    strata_info=defaultdict(list)
    for (tr,sid,t),pairs in sorted(dyads.items()):
        vals=moments_exact(pairs)
        per_session[(tr,sid)].append(vals)
        session_period_means[(tr,sid)][t]=vals["mu"]
        strata_info[tr].append(len(pairs))
    session_means={}
    for key,per_period in per_session.items():
        if len(per_period)!=10:raise ValueError("R079_SESSION_PERIOD_COUNT_WRONG")
        session_means[key]={m:mean_f(d[m] for d in per_period) for m in MEASURES}
        session_means[key]["early_mu"]=mean_f(session_period_means[key][t] for t in range(1,6))
        session_means[key]["late_mu"]=mean_f(session_period_means[key][t] for t in range(6,11))
        session_means[key]["late_minus_early"]=session_means[key]["late_mu"]-session_means[key]["early_mu"]
        per_treat[key[0]].append(key)
    if set(per_treat)!=set(TREATMENTS):
        raise ValueError("R079_TREATMENT_COVERAGE_CHANGED")
    def summary(keys):
        ret={}
        for m in list(MEASURES)+["early_mu","late_mu","late_minus_early"]:
            ret[m]=float(mean_f(session_means[k][m] for k in keys))
        ret["original_sessions"]=len(keys)
        ret["excess_positive_sessions"]=sum(session_means[k]["excess_cross"]>0 for k in keys)
        ret["excess_equal_sessions"]=sum(session_means[k]["excess_cross"]==0 for k in keys)
        ret["excess_negative_sessions"]=sum(session_means[k]["excess_cross"]<0 for k in keys)
        if ret["excess_positive_sessions"]+ret["excess_equal_sessions"]+ret["excess_negative_sessions"]!=len(keys):
            raise ValueError("R079_SESSION_SIGN_ACCOUNTING_BROKEN")
        if abs(ret["pair_mean_var"]-(ret["pop_var"]+ret["pair_cross"])/2)>1e-12:
            raise ValueError("R079_AGGREGATED_GROUP_VAR_IDENTITY_BROKEN")
        if abs(ret["pair_mean_var"]-ret["random_match_pair_mean_var"]-ret["excess_cross"]/2)>1e-12:
            raise ValueError("R079_AGGREGATED_EXCESS_IDENTITY_BROKEN")
        return ret
    all_keys=list(session_means)
    return {
        "research_id":"R079",
        "status":"R079_REAL_AUTHOR_HUMAN_DYAD_MOMENTS_COMPUTED_DESCRIPTIVE_E2",
        "evidence_grade":"E2_ORIGINAL_AUTHOR_CLEANED_HUMAN_DATA_DESCRIPTIVE_NOT_CAUSAL_NOT_E3",
        "frozen_before_real_pair_moments":PROTOCOL,
        "original_git_commit":ORIGINAL_GITHUB_COMMIT,
        "original_source_csv_git_blob":SOURCE_GIT_BLOB,
        "original_source_csv_bytes":SOURCE_BYTES,
        "original_dataset_license":"CC BY 4.0",
        "model_formulas":"exact population dyad cross and finite perfect matching counterfactual index; NOT do(partner)",
        "normalized_realized_action":"action / 100, actualized 0/50/100 three-level contribution",
        "realization_timing":"contemporaneous completed dyad, NOT predetermined partner historical feedback",
        "privacy":"No original participant ID, group ID, source rows, single-session or single-period scores exported",
        "source_universe":universe,
        "all_original_sessions_equal_weight":summary(all_keys),
        "treatments_session_equal_weight":{
            t:{**summary(k),"dyad_count_per_session_period_distribution":{
                str(size):strata_info[t].count(size) for size in sorted(set(strata_info[t]))
            }} for t,k in sorted(per_treat.items())
        },
        "causal_peer_influence":"NOT_IDENTIFIED",
        "comparison_to_R078_n10_model":"NOT_APPLICABLE, actual groups have n=2; R078 Brier/causal numbers artificial",
        "network_level_longitudinal_identification":"NOT_ESTABLISHED",
        "PESEN_v0.1":"FROZEN",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    try:
        rows=parse_author_csv(args.source.read_bytes())
        result=score_aggregate(rows)
    except (ValueError,OSError) as e:
        result={"research_id":"R079","status":"R079_PAIR_SOURCE_FAIL_CLOSED",
            "failure_class":type(e).__name__,
            "reason":str(e)[:128] if isinstance(e,ValueError) else "IO_ERROR",
            "human_raw_rows_exported":False,"PESEN_v0.1":"FROZEN"}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "failure_reason":result.get("reason"),
        "universe":result.get("source_universe"),
        "group_summary":result.get("all_original_sessions_equal_weight"),
        "treatments":result.get("treatments_session_equal_weight"),
    },sort_keys=True))
    if result["status"]!="R079_REAL_AUTHOR_HUMAN_DYAD_MOMENTS_COMPUTED_DESCRIPTIVE_E2":
        raise RuntimeError("R079_REAL_HUMAN_DYAD_FAIL_CLOSED")
if __name__=="__main__":
    main()
