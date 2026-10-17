#!/usr/bin/env python3
"""R088 publisher-Git-original 171x6x20 six-human multi-level PGG sharp bounds.

A global choice is confirmed only if explicitly 'global'. Each absent action
is free to be global or another allowed option, without imputing anyone's
individual data. Group/session IDs are used in-memory and never serialized.
"""
from __future__ import annotations
import argparse,collections,json,pathlib,urllib.error
from collections import Counter,defaultdict
from r088_original_171_groups_multilevel_global_cooperation_E2 import (
 author_bytes,parse_csv,CSV_FILE,CSV_BYTES,CSV_BLOB,EXCLUDE_FILE,EXCLUDE_BLOB,
 ANALYSIS_FILE,ANALYSIS_BLOB,CONDITIONS,ACTIONS,PERIODS,COMMIT,PUBLICATION)
SOURCE_AUDIT="protocols/R088_PHASE_C_ORIGINAL171_MISSING_ACTION_SHARP_INTERVAL_SOURCE_FREEZE_2026-10-17.md"

def boundary_group(members):
 if len(members)!=6:raise ValueError("R088C_SIX_AUTHOR_PERSONS_REQUIRED_PER_GROUP")
 labels={x.get("condition") for x in members}
 if len(labels)!=1 or next(iter(labels)) not in CONDITIONS:
  raise ValueError("R088C_SOURCE_GROUP_CONDITION_CHANGED")
 cond=next(iter(labels))
 subgroup=Counter(x.get("subgroup_id") for x in members)
 if len(subgroup)!=2 or sorted(subgroup.values())!=[3,3] or any(not x for x in subgroup):
  raise ValueError("R088C_ORIGINAL_TWO_THREE_PERSON_SUBGROUPS_NOT_MET")
 rounds=[]
 for p in PERIODS:
  col=f"game.{p}.player.contribution"
  choices=[person.get(col) for person in members]
  if any(x is not None and not isinstance(x,str) for x in choices):
   raise ValueError("R088C_NONSTRING_ORIGINAL_ACTION")
  parsed=["__MISSING__" if x is None or not x.strip() else x for x in choices]
  if any(x not in ACTIONS and x!="__MISSING__" for x in parsed):
   raise ValueError("R088C_ACTION_NOT_MISSING_OR_ORIGINAL_FOUR_CHOICES")
  if cond=="GlobalOnly" and any(x in ("local","other") for x in parsed):
   raise ValueError("R088C_UNAVAILABLE_LOCAL_CHOICE_IN_GLOBALONLY")
  c=Counter(parsed)
  g,m=c["global"],c["__MISSING__"]
  if g+c["local"]+c["other"]+c["self"]+m!=6:raise ValueError("R088C_GROUP_AND_UNKNOWN_MASS_NOT_SIX")
  rounds.append({"round":p,
   "confirmed_global":g,"confirmed_local":c["local"],"confirmed_other":c["other"],
   "confirmed_self":c["self"],"unobserved_missing_action":m,
   "global_investor_count_lower":g,"global_investor_count_upper":g+m,
   "certain_global_threshold_success":int(g>=4),
   "possible_global_threshold_success":int(g+m>=4),
   "certain_global_investors_zero":int(g+m==0),
   "possible_global_investors_zero":int(g==0),
   "certain_six_global_investors":int(g==6),
   "possible_six_global_investors":int(g+m==6)})
 return cond,rounds

def effect_pair_bounds(a,b):
 return {"sharp_lower":a["global_cooperation_over_all20_lower"]-b["global_cooperation_over_all20_upper"],
         "sharp_upper":a["global_cooperation_over_all20_upper"]-b["global_cooperation_over_all20_lower"]}

def bounded_group_experiment(rows,groups_per_treatment=57,required_missing=64):
 if not rows:raise ValueError("R088C_EMPTY_AUTHOR_GROUP_UNIVERSE")
 sets=defaultdict(list)
 for r in rows:
  gid=r.get("group_id")
  if not isinstance(gid,str) or not gid.strip():
   raise ValueError("R088C_ORIGINAL_SOURCE_GROUP_ID_INVALID")
  sets[gid].append(r)
 if len(sets)!=3*groups_per_treatment or len(rows)!=18*groups_per_treatment:
  raise ValueError("R088C_COMPLETE_GROUP_171x6_ORIGINAL_UNIVERSE_MISMATCH")
 conds=defaultdict(list)
 for members in sets.values():
  cond,rounds=boundary_group(members);conds[cond].append(rounds)
 if {name:len(conds[name]) for name in CONDITIONS}!={name:groups_per_treatment for name in CONDITIONS}:
  raise ValueError("R088C_ORIGINAL_THREE_TREATMENT_UNIVERSE_MISMATCH")
 missing_counts={c:sum(r["unobserved_missing_action"] for g in conds[c] for r in g) for c in CONDITIONS}
 total_missing=sum(missing_counts.values())
 if required_missing is not None and total_missing!=required_missing:
  raise ValueError("R088C_FROZEN_ORIGINAL_64_ACTION_MISSINGNESS_NOT_VERIFIED")
 if required_missing==64 and missing_counts!={"GlobalOnly":19,"Balanced":26,"GlobalBoost":19}:
  raise ValueError("R088C_ORIGINAL_CONDITION_SPECIFIC_SOURCE_MISSINGNESS_NOT_VERIFIED")
 outputs={}
 for treatment in CONDITIONS:
  groups=conds[treatment];n=len(groups)
  ts=[]
  for time in range(20):
   period=[g[time] for g in groups]
   total_g=sum(x["confirmed_global"] for x in period)
   total_l=sum(x["confirmed_local"]+x["confirmed_other"] for x in period)
   total_self=sum(x["confirmed_self"] for x in period)
   missing=sum(x["unobserved_missing_action"] for x in period)
   definite=sum(x["certain_global_threshold_success"] for x in period)
   possible=sum(x["possible_global_threshold_success"] for x in period)
   if total_g+total_l+total_self+missing!=6*n:
    raise ValueError("R088C_ORIGINAL_SOURCE_ACTION_MASS_FAILED")
   ts.append({"round":time+1,"groups":n,"original_players":6*n,
    "observed_global_actions":total_g,"observed_local_or_other_actions":total_l,
    "observed_self_actions":total_self,"missing_actions":missing,
    "global_fraction_sharp_lower":total_g/(6*n),
    "global_fraction_sharp_upper":(total_g+missing)/(6*n),
    "local_either_group_fraction_sharp_lower":total_l/(6*n),
    "local_either_group_fraction_sharp_upper":0.0 if treatment=="GlobalOnly" else (total_l+missing)/(6*n),
    "self_fraction_sharp_lower":total_self/(6*n),
    "self_fraction_sharp_upper":(total_self+missing)/(6*n),
    "global_threshold_certain_groups":definite,
    "global_threshold_possible_groups":possible,
    "global_threshold_success_rate_lower":definite/n,
    "global_threshold_success_rate_upper":possible/n,
    "global_threshold_undecidable_group_rounds":possible-definite})
  # Each group enters exactly once. Missing first or last makes the individual group delta an interval.
  group_deltas=[((g[19]["confirmed_global"]-g[0]["confirmed_global"]-g[0]["unobserved_missing_action"])/6,
                 (g[19]["confirmed_global"]+g[19]["unobserved_missing_action"]-g[0]["confirmed_global"])/6)
                for g in groups]
  lower=sum(d[0] for d in group_deltas)/n
  upper=sum(d[1] for d in group_deltas)/n
  if lower>upper:raise ValueError("R088C_END_POINT_SHARP_INTERVAL_INVERTED")
  out={"original_complete_groups":n,
   "original_people_in_complete_groups":6*n,
   "original_actor_round_slots":6*n*20,
   "original_group_rounds":20*n,
   "missing_original_actor_action_slots":missing_counts[treatment],
   "observed_original_actor_actions":6*n*20-missing_counts[treatment],
   "global_cooperation_over_all20_lower":sum(x["global_fraction_sharp_lower"] for x in ts)/20,
   "global_cooperation_over_all20_upper":sum(x["global_fraction_sharp_upper"] for x in ts)/20,
   "global_threshold_success_over_all20_lower":sum(x["global_threshold_certain_groups"] for x in ts)/(20*n),
   "global_threshold_success_over_all20_upper":sum(x["global_threshold_possible_groups"] for x in ts)/(20*n),
   "global_threshold_success_certain_group_rounds":sum(x["global_threshold_certain_groups"] for x in ts),
   "global_threshold_success_possible_group_rounds":sum(x["global_threshold_possible_groups"] for x in ts),
   "global_threshold_undecidable_group_rounds":sum(x["global_threshold_undecidable_group_rounds"] for x in ts),
   "first_round_global_fraction_lower":ts[0]["global_fraction_sharp_lower"],
   "first_round_global_fraction_upper":ts[0]["global_fraction_sharp_upper"],
   "last_round_global_fraction_lower":ts[-1]["global_fraction_sharp_lower"],
   "last_round_global_fraction_upper":ts[-1]["global_fraction_sharp_upper"],
   "first_last_group_equal_delta_sharp_lower":lower,
   "first_last_group_equal_delta_sharp_upper":upper,
   "groups_guaranteed_increasing":sum(a>0 for a,b in group_deltas),
   "groups_guaranteed_decreasing":sum(b<0 for a,b in group_deltas),
   "groups_possible_increasing":sum(b>0 for a,b in group_deltas),
   "groups_possible_decreasing":sum(a<0 for a,b in group_deltas),
   "groups_guaranteed_unchanged":sum(a==b==0 for a,b in group_deltas),
   "groups_with_uncertain_missing_first_or_last":sum(a!=b for a,b in group_deltas),
   "original_round_1_to_20_complete_group_sharp_intervals":ts}
  if out["global_cooperation_over_all20_lower"]>out["global_cooperation_over_all20_upper"]:
   raise ValueError("R088C_GLOBAL_ALL20_INTERVAL_INVERTED")
  outputs[treatment]=out
 pairs={f"{x}_minus_{y}":effect_pair_bounds(outputs[x],outputs[y]) for x,y in (
  ("GlobalOnly","Balanced"),("GlobalBoost","Balanced"),("GlobalBoost","GlobalOnly"))}
 for label,z in pairs.items():
  z["missing_robust_sign"]=("POSITIVE" if z["sharp_lower"]>0
      else "NEGATIVE" if z["sharp_upper"]<0 else "ZERO_ONLY" if z["sharp_lower"]==z["sharp_upper"]==0
      else "UNIDENTIFIED_SIGN_DUE_TO_MISSING")
 return {"original_complete_six_person_groups":len(sets),
  "original_human_participants_in_complete_groups":len(rows),
  "original_20_round_group_rounds":len(sets)*20,
  "original_actor_round_action_opportunities":len(rows)*20,
  "original_missing_human_action_slots":total_missing,
  "original_observed_human_action_slots":len(rows)*20-total_missing,
  "original_three_treatments_sharp_source_bounded_group_results":outputs,
  "pre_frozen_three_treatment_global_group_mean_pair_bounds":pairs,
  "source_previous_strict_nonmissing_failure_retained":True,
  "source_treatment_action_identities_exported":False}

def actual_immutable_author_source():
 original=author_bytes(CSV_FILE,CSV_BLOB,2_500_000)
 if len(original)!=CSV_BYTES:raise ValueError("R088C_AUTHOR_FIXED_CSV_LENGTH_NOT_MATCHED")
 exclude=author_bytes(EXCLUDE_FILE,EXCLUDE_BLOB,8_000)
 rates=author_bytes(ANALYSIS_FILE,ANALYSIS_BLOB,16_000)
 if b"data_full_groups.csv" not in exclude or b"global_group_contributions" not in rates:
  raise ValueError("R088C_ORIGINAL_AUTHOR_ANALYSIS_CODE_NOT_VERIFIED")
 return {"research_id":"R088",
  "status":"R088_ORIGINAL171_GROUP_MISSING_SHARP_INTERVAL_E2_EXECUTED",
  "evidence_grade":"E2_RETROSPECTIVE_AUTHOR_ORIGINAL_COMPLETE_GROUP_HUMAN_ACTION_SHARP_BOUNDS",
  "original_paper_DOI":PUBLICATION,
  "original_author_fixed_commit":COMMIT,
  "original_full_groups_CSV_git_blob":CSV_BLOB,
  "original_author_exclusion_script_git_blob":EXCLUDE_BLOB,
  "first_failed_complete_action_score_CI":39011042473,
  "second_original_action_format_diagnostic_CI":39011243425,
  "frozen_sharp_interval_source_score":SOURCE_AUDIT,
  "original_author_real_human_sharp_bounds":bounded_group_experiment(parse_csv(original)),
  "original_human_action_rows_or_group_IDs_exported":False,
  "original_source_raw_CSV_redistributed":False,
  "statistics_are_missingness_extremal_bounds_not_confidence_intervals":True,
  "original_author_post_exclusion_full_groups_not_all_recruited":True,
  "causal_policy_effect":"NOT_IDENTIFIED_BY_THIS_SCORE",
  "PESEN_v0.1":"FROZEN"}

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--output",type=pathlib.Path,required=True)
 a=ap.parse_args()
 try:r=actual_immutable_author_source()
 except (ValueError,OSError,KeyError,TypeError,UnicodeError,urllib.error.HTTPError,urllib.error.URLError) as e:
  reason=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R088C_") else "R088C_SOURCE_OR_MISSINGNESS_FORMAT_FAILURE"
  r={"research_id":"R088","status":"R088C_ORIGINAL_REAL_HUMAN_SHARP_INTERVAL_E2_FAIL_CLOSED",
    "safe_failure":reason,"actual_original_group_human_scores_exported":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 results=r.get("original_author_real_human_sharp_bounds",{})
 print(json.dumps({"status":r["status"],"safe_failure":r.get("safe_failure"),
  "author_original_171_group_three_arm_intervals":{
   k:{"n_group":v["original_complete_groups"],"missing":v["missing_original_actor_action_slots"],
      "global_share_bounds":[v["global_cooperation_over_all20_lower"],v["global_cooperation_over_all20_upper"]],
      "threshold_bounds":[v["global_threshold_success_over_all20_lower"],v["global_threshold_success_over_all20_upper"]],
      "global_first_last_delta_bounds":[v["first_last_group_equal_delta_sharp_lower"],v["first_last_group_equal_delta_sharp_upper"]],
      "uncertain_threshold_group_rounds":v["global_threshold_undecidable_group_rounds"]}
    for k,v in results.get("original_three_treatments_sharp_source_bounded_group_results",{}).items()},
  "source_cross_arm_bounded_contrasts":results.get("pre_frozen_three_treatment_global_group_mean_pair_bounds")},sort_keys=True))
 if r["status"]!="R088_ORIGINAL171_GROUP_MISSING_SHARP_INTERVAL_E2_EXECUTED":
  raise RuntimeError("R088C_ORIGINAL_AUTHOR_FULL_GROUPS_FAIL_CLOSED")
if __name__=="__main__":main()
