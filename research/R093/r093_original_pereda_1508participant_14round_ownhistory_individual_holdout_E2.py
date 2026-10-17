#!/usr/bin/env python3
"""R093 Pereda et al. 2019 100/1000-person PGG, true original 14-round E2.

Per-treatment leave-one-PARTICIPANT-out contemporaneous others' mean M0;
target's last round M1; fixed half mix M2. This is not group heldout or
fully calendar-forward forecasting. Confidential author actor data in RAM only.
"""
from __future__ import annotations
import argparse,collections,csv,io,json,math,pathlib,urllib.request,urllib.error
from collections import Counter,defaultdict
from r093_2019_first_party_zenodo_14day_large_group_source_eligibility import (
 URL,MAX_BYTES,verify_url,identity,REQUIRED,SAFE_COL)
from r093_phase_b_author_csv_nonbehavior_actor_missing_and_labels import anonymous_original_metadata

FROZEN_SHA256="4eb3380a5eacdef5466709b343af391b27b48a35b5b82f355a4d85d5172644bc"
EXPECTED_PERSONS={
 "PGG100":100,"PGG1000":1004,"PGG_H":101,"PGG_H2":101,
 "PGG_HM":101,"PGG_HM2":101}
EXPECTED_BLANK_ROWS=83
EXPECTED_SOURCE_TOTAL_ROWS=21195
EXPECTED_TREATMENT_SOURCE_ROWS={k:v*14 for k,v in EXPECTED_PERSONS.items()}
PROTOCOL="protocols/R093_PHASE_C_PEREDA_2019_1508_HUMAN_14ROUND_INDIVIDUAL_HOLDOUT_M012_BEHAVIOR_FREEZE_2026-10-17.md"

def source_choice(raw):
 # The 2019 original allows 0,2,4,6,8,10; automated substitutions
 # can include odd integer amounts and are not removed.
 if raw is None or not str(raw).strip():
  raise ValueError("R093C_MISSING_REGISTERED_SOURCE_ACTION")
 try:x=float(str(raw).strip())
 except (ValueError,OverflowError) as e:
  raise ValueError("R093C_NONNUMERIC_REGISTERED_SOURCE_ACTION") from e
 if not math.isfinite(x) or int(x)!=x or not 0<=x<=10:
  raise ValueError("R093C_ORIGINAL_SOURCE_REGISTERED_ACTION_OUTSIDE_INTEGER_0_10")
 return int(x)

def load_original_cohort(raw,persons_expected=EXPECTED_PERSONS,blank_expected=83,
                         total_expected=21195):
 try:s=raw.decode("utf-8-sig")
 except UnicodeError as e:raise ValueError("R093C_ORIGINAL_SOURCE_CSV_ENCODING_FAIL") from e
 rd=csv.reader(io.StringIO(s,newline=""))
 header=next(rd,None)
 if (not header or not REQUIRED.issubset(header) or len(header)!=len(set(header)) or
     any(not SAFE_COL.fullmatch(h) for h in header)):
  raise ValueError("R093C_SOURCE_ORIGINAL_FIELD_SCHEMA_CHANGED")
 loc={h:i for i,h in enumerate(header)}
 participants=defaultdict(dict)
 present=Counter();allrows=Counter();blank_rows=0;count_rows=0
 for row in rd:
  count_rows+=1
  if len(row)!=len(header):raise ValueError("R093C_ORIGINAL_CSV_ROW_WIDTH_CHANGED")
  tr=row[loc["treatment"]].strip()
  actor=row[loc["participant_id"]].strip()
  rnd=row[loc["round_number"]].strip()
  alive=row[loc["player_alive"]].strip()
  if not tr and not actor and not rnd and not alive:
   blank_rows+=1
   continue
  if tr not in persons_expected or not actor or not rnd.isascii() or not rnd.isdigit() or not 1<=int(rnd)<=14:
   raise ValueError("R093C_SOURCE_ROSTER_UNKNOWN_RUN_PERSON_OR_ROUND")
  if alive not in ("0","1"):
   raise ValueError("R093C_ORIGINAL_SOURCE_ALIVE_FLAG_UNKNOWN")
  key=(tr,actor);t=int(rnd)
  if t in participants[key]:raise ValueError("R093C_ORIGINAL_PERSON_DUPLICATE_ROUND")
  amount=source_choice(row[loc["player_contribution"]]) if alive=="1" else None
  participants[key][t]=(alive=="1",amount)
  present[tr]+=int(alive=="1")
  allrows[tr]+=1
 if count_rows!=total_expected or blank_rows!=blank_expected:
  raise ValueError("R093C_ORIGINAL_ROWS_OR_83_UNASSIGNED_METADATA_ROWS_CHANGED")
 by_run=defaultdict(dict)
 for (tr,p),times in participants.items():
  if set(times)!=set(range(1,15)):
   raise ValueError("R093C_ORIGINAL_PERSON_NOT_ALL_14_TIME_KEYS")
  # No return from a game after being banned or first-day absent.
  had_inactive=False
  for t in range(1,15):
   active,_=times[t]
   if had_inactive and active:
    raise ValueError("R093C_ORIGINAL_ACTOR_REACTIVATED_AFTER_EXIT")
   if not active:had_inactive=True
  by_run[tr][p]=times
 for tr,count in persons_expected.items():
  if len(by_run[tr])!=count or allrows[tr]!=count*14:
   raise ValueError("R093C_SOURCE_PERSON_COUNTS_AND_FULL14_UNIVERSE_CHANGED")
 return by_run,{
  "original_csv_total_rows":count_rows,
  "original_unassigned_nonactor_rows_not_scored":blank_rows,
  "original_six_experiment_runs":len(persons_expected),
  "original_author_participant_codes_total":sum(map(len,by_run.values())),
  "registered_alive_1_actor_round_rows":sum(present.values()),
  "still_registered_actor_round_rows_by_experiment":dict(sorted(present.items())),
  "original_actor_or_contribution_row_values_exported":False}

def loss(p,y):return (p-y)**2
def mean(seq):
 if not seq:raise ValueError("R093C_ZERO_SCORED_SOURCE_DENOMINATOR")
 return sum(seq)/len(seq)

def group_individual_heldout_score(cohorts):
 all_scores=[];per_run={}
 for tr in EXPECTED_PERSONS:
  actors=cohorts.get(tr,{})
  if len(actors)<3:raise ValueError("R093C_EMPTY_OR_TOO_FEW_OTHER_PEOPLE")
  same_round={}
  for t in range(1,15):
   alive_values=[z[t][1]/10 for z in actors.values() if z[t][0]]
   same_round[t]=(len(alive_values),sum(alive_values))
  scores=[];person_plus=person_minus=person_zero=no_targets=0
  with_lag_zero=0
  per_round=defaultdict(list)
  for p,series in actors.items():
   gains=[]
   for t in range(2,15):
    active,amount=series[t];prev,pamount=series[t-1]
    if not(active and prev):continue
    if amount is None or pamount is None:
     raise ValueError("R093C_INELIGIBLE_ALIVE_SOURCE_ACTION_IN_SCORING")
    n,total=same_round[t]
    if n<3:raise ValueError("R093C_CONDITION_ROUND_BASELINE_HAS_NO_TRAIN_PEOPLE")
    actual=amount/10.0
    p0=(total-actual)/(n-1)
    p1=pamount/10.0
    p2=0.5*(p0+p1)
    if not all(0<=q<=1.0000000001 for q in (p0,p1,p2,actual)):
     raise ValueError("R093C_ORIGINAL_NORMALIZED_INDIVIDUAL_SHARE_NOT_UNIT")
    e0=loss(p0,actual);e1=loss(p1,actual);e2=loss(p2,actual)
    vals=(e0,e1,e2,e0-e1,e0-e2)
    scores.append(vals);all_scores.append(vals);per_round[t].append(vals)
    gains.append(vals[3])
    with_lag_zero+=int(pamount==0)
   if gains:
    gap=mean(gains)
    person_plus+=int(gap>0);person_minus+=int(gap<0);person_zero+=int(gap==0)
   else:no_targets+=1
  if not scores:raise ValueError("R093C_NO_ELIGIBLE_PERSON_NEXT_ROUND_SCORES")
  per_run[tr]={
   "original_source_person_IDs_in_run":len(actors),
   "original_source_still_registered_14round_sum":sum(v[0] for s in actors.values() for v in s.values()),
   "qualified_individual_next_round_target_pairs":len(scores),
   "original_subjects_without_any_qualified_next_round_pair":no_targets,
   "mean_MSE_M0_other_alive_same_run_same_round":mean([v[0] for v in scores]),
   "mean_MSE_M1_own_previous_round":mean([v[1] for v in scores]),
   "mean_MSE_M2_fixed_half":mean([v[2] for v in scores]),
   "paired_improvement_M0_minus_M1":mean([v[3] for v in scores]),
   "paired_improvement_M0_minus_M2":mean([v[4] for v in scores]),
   "full_heldout_source_people_M1_better":person_plus,
   "full_heldout_source_people_M1_worse":person_minus,
   "full_heldout_source_people_M1_equal":person_zero,
   "qualified_pair_own_prior_zero_contribution":with_lag_zero,
   "by_round_2_to_14_anonymous_forecast_counts":{
    str(t):len(per_round[t]) for t in range(2,15)}}
 return {
  "model_unit":"WITHIN_ONE_ORIGINAL_LARGE_GROUP_INDIVIDUAL_HELDOUT_NOT_GROUP_HELDOUT",
  "total_original_source_qualified_next_round_individual_targets":len(all_scores),
  "all_original_source_person_codes":sum(len(v) for v in cohorts.values()),
  "pooled_M0_other_alive_same_run_round_MSE":mean([v[0] for v in all_scores]),
  "pooled_M1_own_previous_round_MSE":mean([v[1] for v in all_scores]),
  "pooled_M2_fixed_half_MSE":mean([v[2] for v in all_scores]),
  "pooled_paired_gain_M0_minus_M1":mean([v[3] for v in all_scores]),
  "pooled_paired_gain_M0_minus_M2":mean([v[4] for v in all_scores]),
  "by_original_publisher_experiment":per_run,
  "unweighted_six_original_experiment_mean_M1_gain":mean(
    [x["paired_improvement_M0_minus_M1"] for x in per_run.values()]),
  "unweighted_six_original_experiment_mean_M2_gain":mean(
    [x["paired_improvement_M0_minus_M2"] for x in per_run.values()]),
  "six_runs_in_which_M1_improves_M0":sum(x["paired_improvement_M0_minus_M1"]>0 for x in per_run.values()),
  "six_runs_in_which_M2_improves_M0":sum(x["paired_improvement_M0_minus_M2"]>0 for x in per_run.values()),
  "all_source_person_IDs_excluded_from_same_round_M0_training":True,
  "source_original_person_IDs_actor_traces_or_raw_actions_exported":False,
  "independent_new_experiment_group_clustering_confidence_intervals_computed":False}

def run_original():
 with urllib.request.urlopen(urllib.request.Request(URL,headers={
  "User-Agent":"Psychohistory-R093-2019-Pereda-original-14day-individual-history-reanalysis/1.0"}),timeout=60) as r:
  verify_url(r.geturl());raw=r.read(MAX_BYTES+1)
 ident=identity(raw)
 if ident["original_full_file_SHA256"]!=FROZEN_SHA256:
  raise ValueError("R093C_ORIGINAL_MD5_VALID_BUT_SOURCE_SHA_CHANGED")
 # Stage B eligibility reread: safely require identical published code universe.
 check=anonymous_original_metadata(raw)
 if check["source_original_person_round_rows"]!=21195:
  raise ValueError("R093C_PREVIOUSLY_FROZEN_SOURCE_ROW_COUNT_CHANGED")
 if check["source_missing_treatment_label_rows"]!=EXPECTED_BLANK_ROWS:
  raise ValueError("R093C_PREVIOUSLY_FROZEN_UNKNOWN_SOURCE_LINES_CHANGED")
 if check["source_fully_sanitized_duplicate_person_round_keys"]!=0:
  raise ValueError("R093C_PREVIOUSLY_FROZEN_SOURCE_DUPLICATE_KEYS")
 for tr,n in EXPECTED_TREATMENT_SOURCE_ROWS.items():
  if check["safe_publisher_treatment_label_row_counts"].get(tr)!=n:
   raise ValueError("R093C_SOURCE_AUTHOR_TREATMENT_ROW_COUNTS_CHANGED")
 groups,quality=load_original_cohort(raw)
 result=group_individual_heldout_score(groups)
 return {"research_id":"R093",
  "status":"R093_TRUE_ORIGINAL_PEREDA_2019_1508_PERSON_14ROUND_INDIVIDUAL_HOLDOUT_E2_EXECUTED",
  "evidence_grade":"E2_PUBLISHED_REAL_HUMAN_EXPERIMENT_REGISTERED_PLAY_RECORDED_CHOICE_INDIVIDUAL_HELDOUT",
  "original_publisher_DOI":"10.5281/zenodo.2590686",
  "original_scientific_article_DOI":"10.1038/s41598-019-50964-w",
  "original_author_full_csv_sha256":ident["original_full_file_SHA256"],
  "original_author_MD5":ident["actual_first_party_MD5"],
  "frozen_before_behavior_model_protocol":PROTOCOL,
  "source_nonbehavioral_universe":quality,
  "real_author_original_individual_history_scores":result,
  "author_original_replacement_of_missing_decisions_possible":True,
  "original_player_alive_1_proves_independent_manual_action":False,
  "source_original_auto_replacement_flag_present_in_CSV":False,
  "same_run_other_person_same_target_round_M0_is_truly_out_of_calendar_time":False,
  "this_directly_replications_R089_R091_entire_group_LOOG":False,
  "real_new_external_prospective_human_E3":"NOT_ESTABLISHED",
  "new_causal_social_learning_mechanism":"NOT_IDENTIFIED",
  "original_person_or_group_ID_or_actions_redistributed":False,
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 try:z=run_original()
 except (ValueError,OSError,TypeError,KeyError,UnicodeError,urllib.error.URLError,urllib.error.HTTPError) as e:
  safe=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R093C_") else "R093C_AUTHOR_ORIGINAL_REAL_BEHAVIORAL_MODEL_FAIL_CLOSED"
  z={"research_id":"R093","status":"R093C_REAL_ORIGINAL_HUMAN_ELIGIBILITY_OR_PREDICTION_BLOCKED",
     "safe_failure":safe,"real_original_model_scores_exported":0,
     "R089_R090_R091_real_human_studies":"UNCHANGED","PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(z,sort_keys=True,indent=2)+"\n")
 result=z.get("real_author_original_individual_history_scores",{})
 print(json.dumps({"status":z["status"],"safe_failure":z.get("safe_failure"),
  "source_eligibility":z.get("source_nonbehavioral_universe"),
  "original_scored_target_rows":result.get("total_original_source_qualified_next_round_individual_targets"),
  "pooled_M0_MSE":result.get("pooled_M0_other_alive_same_run_round_MSE"),
  "pooled_M1_MSE":result.get("pooled_M1_own_previous_round_MSE"),
  "pooled_M2_MSE":result.get("pooled_M2_fixed_half_MSE"),
  "pooled_paired_M1_gain":result.get("pooled_paired_gain_M0_minus_M1"),
  "by_source_run":result.get("by_original_publisher_experiment")},sort_keys=True))
 if z["status"]!="R093_TRUE_ORIGINAL_PEREDA_2019_1508_PERSON_14ROUND_INDIVIDUAL_HOLDOUT_E2_EXECUTED":
  raise RuntimeError("R093C_AUTHOR_ORIGINAL_REAL_HUMAN_MODEL_FAIL_CLOSED")
if __name__=="__main__":main()
