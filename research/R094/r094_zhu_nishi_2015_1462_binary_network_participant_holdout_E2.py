#!/usr/bin/env python3
"""R094: 2015 original Nishi human network PGG, 2026 Zhu curated binary E2.

Full source-ID heldout from M0 cross-person/visibility/round average.
M1 own last observed 0/1; M2 fixed half. NO session-level evaluation and
never read secondary future feature 'decision_lead'. Only macro outputs.
"""
from __future__ import annotations
import argparse,collections,csv,io,json,math,pathlib,urllib.request,urllib.error
from collections import Counter,defaultdict
from r094_zhu_nishi_2015_binary_network_original_sessions_secondary_source_gate import (
 URL,LIMIT,source_url_valid,full_publisher_source_identity,schema_without_any_values)
from r094_phase_b_nishi_2015_2026_binary_network_person_round_visibility_only import (
 FROZEN_SHA256,anon_roster)

EXPECTED_ROWS=14620
EXPECTED_PERSONS=1462
PROTOCOL="protocols/R094_PHASE_C_NISHI_ZHU_BINARY_NETWORK_1462_PARTICIPANT_LOO_M012_PRESCORE_FREEZE_2026-10-17.md"

def observed_binary(x):
 s=str(x or "").strip().lower()
 if s in ("","na","nan","null","none"):return None
 if s in ("0","0.0"):return 0
 if s in ("1","1.0"):return 1
 raise ValueError("R094C_UNSUPPORTED_ORIGINAL_BINARY_COOPERATION_CODE")

def read_complete_source(rows,expected_rows=EXPECTED_ROWS,expected_subjects=EXPECTED_PERSONS):
 if len(rows)!=expected_rows:raise ValueError("R094C_SOURCE_ROUND_ROW_COUNT_CHANGED")
 participants=defaultdict(dict);vis_by_id={};missing=observed=0
 vis_counts=Counter();rnd_counts=Counter()
 for row in rows:
  if set(row)!={"node_id","round","visibility","decision"}:
   raise ValueError("R094C_UNEXPECTED_SOURCE_EXTRACTED_COLUMNS")
  uid=str(row["node_id"] or "").strip()
  if not uid:raise ValueError("R094C_ORIGINAL_SOURCE_PERSON_ID_MISSING")
  t=str(row["round"] or "").strip()
  if not t.isascii() or not t.isdigit() or not 1<=int(t)<=10:
   raise ValueError("R094C_ORIGINAL_ROUND_NOT_1_TO_10")
  t=int(t)
  vis=str(row["visibility"] or "").strip()
  if vis not in ("0","1"):raise ValueError("R094C_UNEXPECTED_VISIBILITY_CODE")
  if uid in vis_by_id and vis_by_id[uid]!=vis:
   raise ValueError("R094C_SOURCE_PERSON_VISIBILITY_CHANGED")
  vis_by_id[uid]=vis
  if t in participants[uid]:
   raise ValueError("R094C_SOURCE_DUPLICATE_PERSON_ROUND")
  y=observed_binary(row["decision"])
  participants[uid][t]=y
  missing+=int(y is None);observed+=int(y is not None)
  vis_counts[vis]+=1;rnd_counts[t]+=1
 if len(participants)!=expected_subjects or observed+missing!=expected_rows:
  raise ValueError("R094C_ORIGINAL_SOURCE_SUBJECT_COUNT_CHANGED")
 for pid,times in participants.items():
  if set(times)!=set(range(1,11)):
   raise ValueError("R094C_ORIGINAL_SOURCE_NODE_ROUND_INCOMPLETE")
 return participants,vis_by_id,{
  "source_original_secondary_rows":expected_rows,
  "source_unique_original_node_IDs":len(participants),
  "source_observed_original_binary_decisions":observed,
  "source_missing_binary_decision_codes":missing,
  "source_visibility_source_row_denominator":dict(sorted(vis_counts.items())),
  "original_time_rounds_1_to_10_all_actor_ids":True,
  "source_original_session_information_available":False,
  "any_source_actor_ID_or_raw_binary_choice_trace_serialized":False}

def avg(seq):
 if not seq:raise ValueError("R094C_NO_ELIGIBLE_SCORING_TARGETS")
 return sum(seq)/len(seq)

def score_LOO(participants,vis_by_id):
 all_scores=[];by_vis=defaultdict(list);by_time=defaultdict(list)
 person_signs=Counter();no_pairs=0
 source_vis_actor_counts=Counter()
 for uid,v in vis_by_id.items():source_vis_actor_counts[v]+=1
 counts=defaultdict(lambda:[0,0])
 for uid,series in participants.items():
  v=vis_by_id[uid]
  if set(series)!=set(range(1,11)):raise ValueError("R094C_SCORES_MISSING_SOURCE_ROUND")
  for t,y in series.items():
   if y is not None:
    if y not in (0,1):raise ValueError("R094C_UNEXPECTED_NOT_BINARY_INPUT_FOR_SCORE")
    counts[(v,t)][0]+=1;counts[(v,t)][1]+=y
 for uid,series in participants.items():
  v=vis_by_id[uid];personal=[]
  for t in range(2,11):
   y=series[t];yp=series[t-1]
   if y is None or yp is None:continue
   n,total=counts[(v,t)]
   if n<3:raise ValueError("R094C_TWO_OTHER_ELIGIBLE_PLAYERS_REQUIRED")
   p0=(total-y)/(n-1)
   p1=yp
   p2=(p0+p1)/2.
   if not 0<=p0<=1:
    raise ValueError("R094C_SOURCE_UNEXPECTED_OUTGROUP_PROBABILITY")
   err0=(p0-y)**2;err1=(p1-y)**2;err2=(p2-y)**2
   z=(err0,err1,err2,err0-err1,err0-err2)
   personal.append(z);all_scores.append(z)
   by_vis[v].append(z);by_time[t].append(z)
  if not personal:no_pairs+=1
  else:
   m=avg([z[3] for z in personal])
   person_signs["M1_positive"]+=int(m>0)
   person_signs["M1_negative"]+=int(m<0)
   person_signs["M1_equal"]+=int(m==0)
 def aggregate(samples):
  return {"eligible_binary_next_round_targets":len(samples),
   "M0_other_person_visibility_round_Brier":avg([z[0] for z in samples]),
   "M1_own_last_binary_action_Brier":avg([z[1] for z in samples]),
   "M2_fixed_halfblend_Brier":avg([z[2] for z in samples]),
   "paired_gain_M0_minus_M1":avg([z[3] for z in samples]),
   "paired_gain_M0_minus_M2":avg([z[4] for z in samples])}
 if person_signs["M1_positive"]+person_signs["M1_negative"]+person_signs["M1_equal"]+no_pairs!=len(participants):
  raise ValueError("R094C_ORIGINAL_PERSON_SIGN_COUNT_INCOMPLETE")
 return {
  "source_grouping_type":"INDIVIDUAL_FULL_PERSON_HOLDOUT_NOT_2015_SESSION_HOLDOUT",
  "true_independent_original_session_count_reconstructed":0,
  "original_secondary_source_actors":len(participants),
  "next_round_current_and_previous_binary_source_action_targets":len(all_scores),
  "source_IDs_with_no_valid_adjacent_observed_actions":no_pairs,
  "source_complete_person_heldout_M1_gain_sign_counts":dict(person_signs),
  "source_actor_codes_by_visibility":dict(sorted(source_vis_actor_counts.items())),
  "all_original_binary_target_records":aggregate(all_scores),
  "by_original_visible_or_invisible_condition":{
   v:aggregate(by_vis[v]) for v in ("0","1")},
  "source_observed_next_round_targets_by_period":{
   str(t):len(by_time[t]) for t in range(2,11)},
  "full_test_subject_excluded_from_same_visibility_round_M0":True,
  "source_decision_lead_future_information_excluded":True,
  "participant_IDs_source_tenround_binary_traces_or_session_IDs_exported":False,
  "source_may_contain_unidentified_automatic_action_processes":True}

def original_real():
 with urllib.request.urlopen(urllib.request.Request(URL,headers={
  "User-Agent":"Psychohistory-R094-2026-secondary-Nishi-original-binary-individual-holdout/1.0"}),timeout=60) as resp:
  source_url_valid(resp.geturl());raw=resp.read(LIMIT+1)
 ident=full_publisher_source_identity(raw)
 if ident["independently_computed_raw_SHA256"]!=FROZEN_SHA256:
  raise ValueError("R094C_SECONDARY_SOURCE_FULL_SHA256_CHANGED")
 h=schema_without_any_values(raw)
 if h["original_data_row_count"]!=EXPECTED_ROWS:
  raise ValueError("R094C_ORIGINAL_SOURCE_ROWS_UNEXPECTED")
 input=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""))
 required={"node_id","round","visibility","decision"}
 if not required.issubset(input.fieldnames):
  raise ValueError("R094C_ORIGINAL_SECONDARY_SOURCE_FIELDS_MISSING")
 rows=[{k:z[k] for k in required} for z in input]
 # First re-audit source ID/period/visibility using *no decision values*.
 metadata=anon_roster([(z["node_id"],z["round"],z["visibility"]) for z in rows])
 if (metadata["distinct_original_node_ID_codes"]!=EXPECTED_PERSONS or
     metadata["number_of_node_IDs_with_exactly_10_unique_rounds_1_to_10"]!=EXPECTED_PERSONS or
     metadata["duplicate_node_ID_round_combinations"]!=0 or
     metadata["number_of_node_IDs_with_visibility_change_across_rounds"]!=0):
  raise ValueError("R094C_ORIGINAL_SOURCE_METADATA_1462_ACTOR_COHORT_FAILED")
 cohort,vis,quality=read_complete_source(rows)
 scores=score_LOO(cohort,vis)
 return {"research_id":"R094",
  "status":"R094_SECONDARY_CURATED_ORIGINAL_2015_HUMAN_BINARY_NETWORK_1462_PERSON_E2_EXECUTED",
  "original_primary_experiment_DOI":"10.1038/nature15392",
  "curated_secondary_publication_DOI":"10.1371/journal.pone.0347919",
  "source_Zenodo_DOI":"10.5281/zenodo.19544006",
  "source_secondary_MD5":ident["fixed_publisher_MD5"],
  "source_secondary_fullfile_SHA256":ident["independently_computed_raw_SHA256"],
  "prescore_model_protocol":PROTOCOL,
  "source_metadata":quality,
  "binary_individual_full_person_heldout_evaluation":scores,
  "secondary_not_verified_unmodified_original_2015_log":True,
  "2015_original_80_sessions_heldout_for_testing":False,
  "R089_group_heldout_exact_reproduction":False,
  "no_prospective_E3_or_psychological_causality":True,
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 try:r=original_real()
 except (OSError,TypeError,ValueError,KeyError,urllib.error.HTTPError,urllib.error.URLError) as e:
  msg=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R094C_") else "R094C_ORIGINAL_2015_SECONDARY_BINARY_DATA_SOURCE_FAIL_CLOSED"
  errclass=type(e).__name__
  errclass=errclass if errclass in ("ValueError","KeyError","TypeError","OSError","IndexError","OverflowError","HTTPError","URLError") else "OTHER_ERROR_CLASS"
  r={"research_id":"R094","status":"R094C_PRESCORE_ORIGINAL_SECONDARY_SOURCE_BEHAVIOR_ELIGIBILITY_BLOCKED",
    "safe_failure":msg,"source_only_failure_class":errclass,
    "actual_human_E2_predictions_scored":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n",encoding="utf-8")
 brief=r.get("binary_individual_full_person_heldout_evaluation",{})
 print(json.dumps({"status":r["status"],"safe_failure":r.get("safe_failure"),
  "original_source":r.get("source_metadata"),
  "scoring":brief.get("all_original_binary_target_records"),
  "by_visibility":brief.get("by_original_visible_or_invisible_condition"),
  "person_signs":brief.get("source_complete_person_heldout_M1_gain_sign_counts")},sort_keys=True))
 if r["status"]!="R094_SECONDARY_CURATED_ORIGINAL_2015_HUMAN_BINARY_NETWORK_1462_PERSON_E2_EXECUTED":
  raise RuntimeError("R094C_REAL_SOURCE_BINARY_GAME_TEST_FAILED")
if __name__=="__main__":main()
