#!/usr/bin/env python3
"""R090 independent climate clubs six-person group predictive transfer.

30 fixed groups ×15 rounds, leave-one-whole-group-out treatment comparison.
M0 other source groups same treatment round, M1 own prior group round, M2 half.
No actor, group, or session IDs or actor-level actions output.
"""
from __future__ import annotations
import argparse,collections,json,math,pathlib,urllib.request,urllib.error
from collections import defaultdict,Counter
from r090_independent_climate_clubs_original_roster_source_gate import (
 URL,MAX_BYTES,check_url,check_source_bytes,OFFICIAL_MD5,TREATMENTS)
from r090_phase_b_independent_original_otree_round_metadata_only import round_field_audit

FIRST_SOURCE_SHA256="ebc8831011a1a3b4893a80ae158d5129ed0f35e57a8092eba36c6a7b0cbd4282"
PROTOCOL="protocols/R090_PHASE_C_CROSS_AUTHOR_30_GROUP_15_ROUND_HISTORY_TRANSFER_FROZEN_SCORING_2026-10-17.md"
TRAIN_MODELS=("M0_OTHER_GROUPS_SAME_TREATMENT_ROUND",
 "M1_TARGET_GROUP_PRIOR_ROUND",
 "M2_FIXED_HALF_OTHER_HALF_HISTORY")
AUTHOR_EXPECTED_GROUPS={"T1":8,"T2":8,"T3":7,"T4":7}

def bounded_float(source,label,positive=False):
 if source is None or not isinstance(source,str) or not source.strip() or source.strip().upper() in ("NA","NAN","NULL"):
  raise ValueError("R090C_MISSING_CONTRIBUTION_OR_ENDOWMENT")
 try:v=float(source)
 except ValueError as e:raise ValueError("R090C_NONNUMERIC_CONTRIBUTION_OR_ENDOWMENT") from e
 if not math.isfinite(v) or v<0 or (positive and v<=0):
  raise ValueError("R090C_NONFINITE_NEGATIVE_OR_ZERO_ENDOWMENT")
 return v

def indicator_meta(source):
 if source in ("0","1"):return source
 if source in (None,"","NA","na"):return "unknown"
 raise ValueError("R090C_AUTHOR_AUTOMATIC_OR_TIMEOUT_SCHEMA_MISMATCH")

def parse_author_group_rounds(rows,expected_n=2700):
 if len(rows)!=expected_n:
  raise ValueError("R090C_REAL_SOURCE_ROW_UNIVERSE_MISMATCH")
 by_group=defaultdict(list)
 by_group_time=defaultdict(list)
 treatments=defaultdict(set)
 peoples=defaultdict(set)
 technical_rounds=Counter()
 auto=Counter();timeouts=Counter()
 seen=set()
 for row in rows:
  sid=row.get("session.code");group=row.get("group.id_in_subsession")
  p=row.get("participant.code");tr=row.get("treatment")
  if not sid or not group or not p or tr not in TREATMENTS:
   raise ValueError("R090C_AUTHOR_ORIGINAL_PERSON_SESSION_TREATMENT_MISSING")
  rnd=row.get("subsession.round_number")
  if not isinstance(rnd,str) or not rnd.isascii() or not rnd.isdigit() or int(rnd) not in range(1,16):
   raise ValueError("R090C_AUTHOR_ORIGINAL_15_REAL_ROUNDS_CHANGED")
  t=int(rnd);tech=row.get("participant._round_number")
  if tech!="15":raise ValueError("R090C_AUTHOR_OTREE_TECHNICAL_ROUND_NOT15")
  technical_rounds[tech]+=1
  key=(sid,p,t)
  if key in seen:raise ValueError("R090C_REPEATED_ORIGINAL_ACTOR_AT_ROUND")
  seen.add(key)
  contrib=bounded_float(row.get("player.contribution"),"contribution")
  endowment=bounded_float(row.get("player.endowment"),"endowment",positive=True)
  if contrib>endowment+1e-10:
   raise ValueError("R090C_AUTHOR_CONTRIBUTION_EXCEEDS_ENDOWMENT")
  group_key=(sid,group)
  by_group[group_key].append((t,p,tr,contrib,endowment))
  by_group_time[(group_key,t)].append((p,tr,contrib,endowment))
  treatments[group_key].add(tr)
  peoples[group_key].add(p)
  auto[(tr,indicator_meta(row.get("player.automatic_decision")))]+=1
  timeouts[(tr,indicator_meta(row.get("player.timeout_contr")))]+=1
 if len(by_group)!=30 or len(by_group_time)!=450 or len(seen)!=2700:
  raise ValueError("R090C_ORIGINAL_30x15x6_GROUP_UNIVERSE_NOT_MET")
 modelgroups=defaultdict(dict)
 for key,records in by_group.items():
  trset=treatments[key];members=peoples[key]
  if len(trset)!=1 or len(members)!=6 or len(records)!=90:
   raise ValueError("R090C_ORIGINAL_SIX_STABLE_MEMBERS_PER_GROUP_NOT_MET")
  condition=next(iter(trset))
  times=[]
  for t in range(1,16):
   row=by_group_time[(key,t)]
   if len(row)!=6 or {x[0] for x in row}!=members or {x[1] for x in row}!={condition}:
    raise ValueError("R090C_ORIGINAL_GROUP_ROSTER_UNSTABLE_OR_ROUND_MISSING")
   value=sum(x[2] for x in row)/sum(x[3] for x in row)
   if not 0<=value<=1+1e-10:
    raise ValueError("R090C_AUTHOR_GROUP_CONTRIBUTION_FRACTION_OUTSIDE_UNIT")
   times.append(min(1.,value))
  modelgroups[condition][key]=times
 if {c:len(modelgroups[c]) for c in TREATMENTS}!=AUTHOR_EXPECTED_GROUPS:
  raise ValueError("R090C_AUTHOR_8_8_7_7_ORIGINAL_STABLE_GROUPS_CHANGED")
 return modelgroups,{
  "original_2700_actor_round_contributions_read":len(rows),
  "original_30_stable_six_person_groups_verified":len(by_group),
  "original_180_humans_with_15_periods":len(seen)//15,
  "original_15_rounds_with_30_groups_each":15,
  "original_450_group_round_contribution_shares":450,
  "original_four_treatment_group_counts":AUTHOR_EXPECTED_GROUPS,
  "auto_decision_observed_counts_by_treatment":{
    c:{"one":auto[(c,"1")],"zero":auto[(c,"0")],"unknown":auto[(c,"unknown")]} for c in TREATMENTS},
  "contribution_timeouts_by_treatment":{
    c:{"one":timeouts[(c,"1")],"zero":timeouts[(c,"0")],"unknown":timeouts[(c,"unknown")]} for c in TREATMENTS},
  "source_original_technical_round_field_is15_every_row":technical_rounds==Counter({"15":len(rows)}),
  "any_original_actor_or_group_IDs_exported":False}

def stats(values):return sum(values)/len(values) if values else 0.

def score_loo(groups,expected_group_numbers=None,expected_total_forecasts=420):
 if expected_group_numbers is None:expected_group_numbers=AUTHOR_EXPECTED_GROUPS
 allrows=[]
 aggregated={}
 neg_group=[]
 for tr in TREATMENTS:
  mapping=groups.get(tr,{})
  if len(mapping)!=expected_group_numbers[tr]:
   raise ValueError("R090C_SOURCE_PER_TREATMENT_GROUPS_MISMATCH")
  scored=[]
  per_group_signs=Counter()
  by_round=defaultdict(list)
  for gid,vec in mapping.items():
   if len(vec)!=15 or any(not isinstance(y,(float,int)) or not math.isfinite(y) or not 0<=y<=1 for y in vec):
    raise ValueError("R090C_INVALID_GROUP_ROUND_FRACTION_INPUT")
   for t in range(15):by_round[t].append(vec[t])
   others=[other for other in mapping if other!=gid]
   if not others:raise ValueError("R090C_NO_OUT_OF_GROUP_TRAINING")
   gains=[]
   for t in range(1,15):
    target=vec[t]
    p0=stats([mapping[other][t] for other in others])
    p1=vec[t-1]
    p2=(p0+p1)/2
    e0=(p0-target)**2;e1=(p1-target)**2;e2=(p2-target)**2
    scored.append((e0,e1,e2,e0-e1,e0-e2,t+1))
    gains.append(e0-e1)
    allrows.append((tr,e0,e1,e2,e0-e1,e0-e2))
   delta=stats(gains)
   per_group_signs["gain_positive" if delta>0 else "gain_negative" if delta<0 else "gain_zero"]+=1
  if len(scored)!=len(mapping)*14:
   raise ValueError("R090C_ORIGINAL_HOLDOUT_FORECAST_TARGETS_MISMATCH")
  aggregated[tr]={
   "independent_original_heldout_groups":len(mapping),
   "heldout_original_group_round_scores":len(scored),
   "mean_group_endowment_weighted_contribution_ratio_by_round":[stats(by_round[t]) for t in range(15)],
   "model_mean_squared_losses":{
     TRAIN_MODELS[k]:stats([r[k] for r in scored]) for k in range(3)},
   "shared_target_m1_minus_m0_score_gain":stats([r[3] for r in scored]),
   "shared_target_m2_minus_m0_score_gain":stats([r[4] for r in scored]),
   "whole_heldout_group_M1_vs_M0_gain_signs":dict(per_group_signs)}
 if len(allrows)!=expected_total_forecasts:raise ValueError("R090C_TOTAL_HOLDOUT_GROUP_FORECASTS_NOT420")
 summary={
  "source_independent_groups_heldout":sum(v["independent_original_heldout_groups"] for v in aggregated.values()),
  "source_independent_author_heldout_forecast_targets":len(allrows),
  "three_frozen_models_pooled_group_round_mean_squared_loss":{
    TRAIN_MODELS[k]:stats([r[k+1] for r in allrows]) for k in range(3)},
  "M1_history_pooled_shared_target_gain_over_M0":stats([r[4] for r in allrows]),
  "M2_halfblend_pooled_shared_target_gain_over_M0":stats([r[5] for r in allrows]),
  "by_original_author_treatment":aggregated,
  "total_source_original_heldout_groups_M1_gain_positive":sum(x["whole_heldout_group_M1_vs_M0_gain_signs"].get("gain_positive",0) for x in aggregated.values()),
  "total_source_original_heldout_groups_M1_gain_negative":sum(x["whole_heldout_group_M1_vs_M0_gain_signs"].get("gain_negative",0) for x in aggregated.values()),
  "total_source_original_heldout_groups_M1_gain_zero":sum(x["whole_heldout_group_M1_vs_M0_gain_signs"].get("gain_zero",0) for x in aggregated.values()),
  "independent_author_mean_history_gain_direction":"REPLICATED_MEAN_POSITIVE" if stats([r[4] for r in allrows])>0 else "NOT_REPLICATED_MEAN_NONPOSITIVE",
  "original_four_treatments_all_positive":all(aggregated[t]["shared_target_m1_minus_m0_score_gain"]>0 for t in TREATMENTS),
  "group_ids_and_person_decision_rows_exported":False}
 return summary

def actual_original_source():
 req=urllib.request.Request(URL,headers={"User-Agent":"PsychologicalHistory-R090-independent-climate-club-30group-source-SHA-transfer/1.0"})
 with urllib.request.urlopen(req,timeout=45) as resp:
  check_url(resp.geturl());raw=resp.read(MAX_BYTES+1)
 rows,identity=check_source_bytes(raw)
 if identity["full_source_SHA256"]!=FIRST_SOURCE_SHA256 or identity["original_source_bytes"]!=419189:
  raise ValueError("R090C_ORIGINAL_AUTHOR_SOURCE_WHOLE_SHA256_CHANGED")
 meta=round_field_audit(rows)
 if (meta["nonmatching_two_round_fields_rows"]!=2520 or
     meta["subsession_group_membership_stability_histogram"].get("multi_round_stable")!=30 or
     meta["distinct_author_sessions"]!=8):
  raise ValueError("R090C_AUTHOR_PRE_SCORING_ROSTER_DIAGNOSTIC_CHANGED")
 groups,quality=parse_author_group_rounds(rows)
 prediction=score_loo(groups)
 positive_automatic=sum(v["one"] for v in quality["auto_decision_observed_counts_by_treatment"].values())
 missing_automatic=sum(v["unknown"] for v in quality["auto_decision_observed_counts_by_treatment"].values())
 return {"research_id":"R090",
  "status":"R090_ORIGINAL_INDEPENDENT_AUTHOR_30GROUP_15ROUND_HISTORY_TRANSFER_E2_EXECUTED",
  "evidence_grade":"E2_RETROSPECTIVE_INDEPENDENT_AUTHOR_DATA_MODEL_FAMILY_TRANSFER",
  "original_publisher_DOI":"10.5281/zenodo.17610157",
  "original_fixed_Zenodo_record":17610157,
  "original_official_publisher_MD5":OFFICIAL_MD5,
  "original_full_source_SHA256":FIRST_SOURCE_SHA256,
  "frozen_before_outcome_protocol":PROTOCOL,
  "original_2700_row_real_human_behavior_source_eligibility":quality,
  "transfer_group_level_prediction_results":prediction,
  "scientific_scope_if_system_automatic_decisions":"MIXED_RECORDED_EXPERIMENT_ACTIONS_INCLUDES_AUTOMATIC" if positive_automatic or missing_automatic else "NO_AUTOMATIC_DECISIONS_FLAGGED_IN_SOURCE",
  "original_2025_author_results_not_new2026_recruitment":True,
  "target_variable_not_identical_to_R089_binary_global_action_fraction":True,
  "cross_author_transfer_uses_same_FROZEN_M0_M1_M2_PREDICTOR_STRUCTURES":True,
  "individual_actor_actions_or_group_ID_exported":False,
  "source_or_original_CSV_redistributed":False,
  "independent_external_prospective_E3":"NOT_ESTABLISHED",
  "causal_climate_club_effect":"NOT_IDENTIFIED",
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 try:r=actual_original_source()
 except (ValueError,OSError,TypeError,KeyError,urllib.error.HTTPError,urllib.error.URLError) as e:
  safe=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R090") else "R090C_SOURCE_OR_REAL_OUTCOME_CONTRACT_FAILED"
  r={"research_id":"R090","status":"R090C_ORIGINAL_INDEPENDENT_SOURCE_SCORING_STRICT_FAIL_CLOSED",
    "safe_failure":safe,"real_original_human_cross_transfer_metrics_exported":0,
    "R089_prior_scientific_evidence":"UNMODIFIED","PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n")
 print(json.dumps({"status":r["status"],"safe_failure":r.get("safe_failure"),
   "quality":r.get("original_2700_row_real_human_behavior_source_eligibility"),
   "prediction":r.get("transfer_group_level_prediction_results")},sort_keys=True))
 if r["status"]!="R090_ORIGINAL_INDEPENDENT_AUTHOR_30GROUP_15ROUND_HISTORY_TRANSFER_E2_EXECUTED":
  raise RuntimeError("R090C_REAL_GROUP_HELDOUT_SOURCE_OR_BEHAVIOR_FAILED")
if __name__=="__main__":main()
