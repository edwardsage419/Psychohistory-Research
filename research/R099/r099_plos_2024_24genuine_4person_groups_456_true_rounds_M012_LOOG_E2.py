#!/usr/bin/env python3
"""R099 original 2024 PLOS 96 human 24 x four-person 20round group-heldout E2.

Freeze BEFORE original stage2 contribution values examined; user source privacy:
no actor/session/group IDs or original contribution individual traces published.
M0 other 11 groups within same DF treatment at target t; M1 heldout group t-1
mean; M2 exact 50:50; target sum original 4 values /80, t2..20, group MSE.
"""
from __future__ import annotations
import argparse,csv,io,json,math,pathlib,urllib.request,urllib.error
from collections import defaultdict,Counter
from r099_liu_2024_plos_official_original_S1_CSV_publisher_metadata_only import (
 URL,MAX_CSV,check_publisher_url,verify_bytes,source_safe_columns)
from r099_phase_b_plos_2024_fixed4p_nonbehavior_group_roster_only import (
 REAL_SHA,EXPECTED_HEADER,N,cohort_metadata)
PROTOCOL="protocols/R099_PHASE_C_FIRST_PARTY_PLOS_24_TRUE_FIXED_4PERSON_GROUPS_20ROUND_LOOG_M0_M1_M2_PRESCORE_FREEZE_2026-10-17.md"

def contribution(v):
 text=str(v).strip()
 try:f=float(text)
 except (ValueError,TypeError) as e:
  raise ValueError("R099C_ORIGINAL_CONTRIBUTION_NONNUMERIC_OR_MISSING") from e
 if not math.isfinite(f) or f<0 or f>20 or f!=int(f):
  raise ValueError("R099C_ORIGINAL_CONTRIBUTION_NOT_INTEGER_0_TO_20")
 return int(f)

def original_group_actions(b,group_count=24,people_count=96,row_count=1920,groups_per_treat=12):
 rdr=csv.DictReader(io.StringIO(b.decode("utf-8-sig"),newline=""))
 if rdr.fieldnames!=EXPECTED_HEADER:raise ValueError("R099C_AUTHOR_ORIGINAL_COLUMNS_CHANGED")
 actions=defaultdict(dict);person_group={};group_people=defaultdict(set);group_df=defaultdict(set)
 pair_seen=set();source_count=0;actor_ids=set()
 for row in rdr:
  if None in row:raise ValueError("R099C_AUTHOR_CSV_ROW_WIDTH_CHANGED")
  # Only original Contribution is numerical target. Current OtherContri and
  # first-stage Type are NOT read, ever.
  actor=str(row["subject"]).strip();otheractor=str(row["id"]).strip()
  g=str(row["group"]).strip();t_raw=str(row["Period"]).strip();df=str(row["DF"]).strip()
  if not all((actor,otheractor,g,t_raw,df)) or not t_raw.isascii() or not t_raw.isdigit():
   raise ValueError("R099C_ORIGINAL_ACTOR_GROUP_TREATMENT_PERIOD_INVALID")
  t=int(t_raw);value=contribution(row["Contribution"])
  if not 1<=t<=20:raise ValueError("R099C_ORIGINAL_ROUND_OUTSIDE_1_TO_20")
  key=(actor,t)
  if key in pair_seen:raise ValueError("R099C_DUPLICATE_ORIGINAL_ACTOR_ROUND")
  pair_seen.add(key);source_count+=1;actor_ids.add(actor)
  group_people[g].add(actor);group_df[g].add(df)
  if actor in person_group and person_group[actor]!=g:raise ValueError("R099C_REAL_ORIGINAL_PERSON_MULTIPLE_STABLE_GROUPS")
  person_group[actor]=g
  if t not in actions[g]:actions[g][t]=[]
  actions[g][t].append(value)
 if len(actor_ids)!=people_count or source_count!=row_count or len(actions)!=group_count:
  raise ValueError("R099C_ORIGINAL_FULL_SOURCE_TOTALS_CHANGED")
 treatments=defaultdict(list);fractions={}
 for g,rounds in actions.items():
  if len(group_people[g])!=4 or len(group_df[g])!=1 or set(rounds)!=set(range(1,21)) or any(len(v)!=4 for v in rounds.values()):
   raise ValueError("R099C_ORIGINAL_FIXED_4PERSON_20ROUND_GROUP_INCOMPLETE")
  d=next(iter(group_df[g]));treatments[d].append(g)
  fractions[g]={t:sum(vals)/80.0 for t,vals in rounds.items()}
 if len(treatments)!=2 or any(len(v)!=groups_per_treat for v in treatments.values()):
  raise ValueError("R099C_ORIGINAL_SF_DF_GROUP_COUNTS_NOT_EQUAL_12")
 # additional original per actor each 20 rounds, source-only pre-validation
 if len(pair_seen)!=people_count*20:
  raise ValueError("R099C_SOURCE_ORIGINAL_ACTOR_HISTORY_NOT_20_ROUNDS")
 return fractions,treatments,{
  "original_real_human_actor_count":len(actor_ids),
  "original_real_fixed_four_person_groups":len(group_people),
  "original_first_party_action_cells":source_count,
  "original_each_individual_contribution_integer_between_0_and_20":True,
  "original_each_group_all4_actors_and20_rounds":True,
  "original_source_OtherContri_or_Type_fields_ever_read_or_used":False,
  "original_participant_and_group_identifiers_or_actions_republished":False}

def avg(v):
 if not v:raise ValueError("R099C_EMPTY_HOLDOUT_GROUP_BASELINE")
 return sum(v)/len(v)

def pack(data):
 if not data:return {"targets":0}
 return {"targets":len(data),
  "M0_other_source_groups_same_treatment_same_round_MSE":avg([x[0] for x in data]),
  "M1_heldout_group_own_previous_round_MSE":avg([x[1] for x in data]),
  "M2_fixed_half_MSE":avg([x[2] for x in data]),
  "paired_gain_M0_minus_M1":avg([x[3] for x in data]),
  "paired_gain_M0_minus_M2":avg([x[4] for x in data])}

def score(fractions,treatments,group_count=24,groups_per_treat=12):
 if len(fractions)!=group_count or len(treatments)!=2 or any(len(x)!=groups_per_treat for x in treatments.values()):
  raise ValueError("R099C_SOURCE_INELIGIBLE_ORIGINAL_GROUP_STRUCTURE")
 allresults=[];treat_result={}
 names=sorted(treatments.keys())
 for condid,condition in enumerate(names):
  members=treatments[condition];items=[];byearly=[];bylate=[];sess1=[];sess2=[]
  for heldout in members:
   h=fractions[heldout]
   if set(h)!=set(range(1,21)):
    raise ValueError("R099C_HELDOUT_ORIGINAL_GROUP_MISSING_SOURCE_ROUND")
   grouprows=[]
   for t in range(2,21):
    other=[fractions[k][t] for k in members if k!=heldout]
    if len(other)!=groups_per_treat-1:raise ValueError("R099C_ACTUAL_GROUP_M0_HELDOUT_LEAK")
    y=h[t];p0=avg(other);p1=h[t-1];p2=(p0+p1)/2
    values=((p0-y)**2,(p1-y)**2,(p2-y)**2,
            (p0-y)**2-(p1-y)**2,(p0-y)**2-(p2-y)**2)
    grouprows.append(values);items.append(values);allresults.append(values)
    if t<=5:byearly.append(values)
    else:bylate.append(values)
   gg=pack(grouprows)
   sess1.append(gg["paired_gain_M0_minus_M1"])
   sess2.append(gg["paired_gain_M0_minus_M2"])
  def signs(vals):
   return {"positive":sum(v>0 for v in vals),
    "negative":sum(v<0 for v in vals),
    "exact_tie":sum(v==0 for v in vals)}
  treat_result["ANONYMOUS_TREATMENT_"+("A" if condid==0 else "B")]={
   "source_study_treatment_label_is_anonymized":True,
   "source_groups_within_this_treatment":len(members),
   "real_group_round_target_predictions":len(items),
   "pooled_real_group_share_MSE":pack(items),
   "early_rounds_t2_5":pack(byearly),
   "later_rounds_t6_20":pack(bylate),
   "positive_vs_negative_12_real_group_M1_gain_counts":signs(sess1),
   "positive_vs_negative_12_real_group_M2_gain_counts":signs(sess2),
   "anonymous_sorted_M1_original_group_gain_values":[round(v,12) for v in sorted(sess1)],
   "anonymous_sorted_M2_original_group_gain_values":[round(v,12) for v in sorted(sess2)]
  }
 if len(allresults)!=group_count*19:
  raise ValueError("R099C_EXPECTED_ALL_456_GROUP_ROUND_TARGETS_NOT_MET")
 return {"original_actual_whole_source_fixed_groups":group_count,
  "source_true_independent_lab_session_labels_recovered":False,
  "original_real_next_round_group_share_predictions":len(allresults),
  "overall_same_target_original_group_share_MSE":pack(allresults),
  "by_original_FEEDBACK_treatment_hidden_literal_identity":treat_result,
  "source_heldout_group_every_round_excluded_from_M0":True,
  "source_actual_subject_group_IDs_or_original_action_sequences_republished":False}

def actual():
 check_publisher_url(URL)
 with urllib.request.urlopen(urllib.request.Request(URL,headers={
  "User-Agent":"Psychohistory-R099-2024-first-party-PLOS-original-24-fourperson-stage2-LOOG-E2/1.0"}),timeout=50) as r:
  check_publisher_url(r.geturl());b=r.read(MAX_CSV+1)
 i=verify_bytes(b)
 if i["exact_original_CSV_bytes"]!=43467 or i["original_first_party_fullfile_SHA256"]!=REAL_SHA:
  raise ValueError("R099C_FIRST_PARTY_PLOS_SOURCE_SHA256_OR_LENGTH_CHANGED")
 nonbehavior=cohort_metadata(b)
 candidate=[x for x in nonbehavior["anonymous_candidate_group_key_structures"]
            if x["original_candidate_group_key"]=="group" and x["candidate_actor_key"]=="subject"]
 if not candidate or not candidate[0]["is_exact_complete_24_fourperson_group_roster"]:
  raise ValueError("R099C_PREVIOUS_NONBEHAVIOR_AUTHOR_GROUP_ROSTER_NOT_ELIGIBLE")
 fractions,treat,quality=original_group_actions(b)
 z=score(fractions,treat)
 return {"research_id":"R099",
  "status":"R099_2024_PLOS_FIRST_PARTY_96_HUMAN_24_TRUE_GROUPS_20ROUND_LOOG_456_E2_SCORED",
  "evidence_grade":"E2_RETROSPECTIVE_INDEPENDENT_2024_AUTHOR_HUMAN_FIXED_GROUP_HELDOUT_NOT_ORIGINAL_LAB_SESSION_LOSO",
  "article_DOI":"10.1371/journal.pone.0299196",
  "published_original_S1_data_DOI":"10.1371/journal.pone.0299196.s002",
  "original_full_source_bytes":43467,"source_full_SHA256":REAL_SHA,
  "pre_real_score_frozen_protocol":PROTOCOL,
  "source_qualification_group_actor_treatment":quality,
  "actual_real_20round_group_holdout_scores":z,
  "real_original_new_human_E3_prospective_experiment":False,
  "original_eight_lab_session_IDs_observed_in_published_CSV":False,
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",required=True,type=pathlib.Path);a=p.parse_args()
 try:r=actual()
 except (ValueError,TypeError,OSError,KeyError,UnicodeError,urllib.error.HTTPError,urllib.error.URLError) as e:
  safe=str(e)[:110] if isinstance(e,ValueError) and str(e).startswith("R099C_") else "R099C_FIRST_PARTY_HUMAN_GROUP_SCORE_FAIL_CLOSED"
  r={"research_id":"R099","status":"R099C_PUBLISHED_HUMAN_SCORE_BLOCKED","safe_error":safe,
     "genuine_original_human_predictions_scored":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(json.dumps({"status":r["status"],"safe_error":r.get("safe_error"),
                   "score":r.get("actual_real_20round_group_holdout_scores")},sort_keys=True))
 if r["status"]!="R099_2024_PLOS_FIRST_PARTY_96_HUMAN_24_TRUE_GROUPS_20ROUND_LOOG_456_E2_SCORED":
  raise SystemExit(1)
if __name__=="__main__":main()
