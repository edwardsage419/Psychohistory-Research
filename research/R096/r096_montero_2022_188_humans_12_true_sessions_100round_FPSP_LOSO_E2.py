#!/usr/bin/env python3
"""R096: first-party original-author 2022 12 REAL lab sessions x 100 rounds.

Two treatments fixed/shuffled opponent. Full original SESSION heldout:
M0 same-treatment OTHER 5 whole sessions' same-round source 1 fraction;
M1 own prior original 0/1 action; M2 fixed half; Brier. Original numeric
source 1 category is NOT labeled 'cooperation' without a source codebook.
No original person/session/partner IDs or source individual rows output.
"""
from __future__ import annotations
import argparse,collections,csv,io,json,pathlib,urllib.request,urllib.error
from collections import Counter,defaultdict
from r096_phase_b_montero_author_git_tag_pinned_original_FP_SP_CSV_source import (
 FILES,CAP,raw_url,validate_raw_url,verify_author_blob,safe_original_csv_schema)
from r096_phase_c_original_2022_author_fp_sp_six_true_sessions_roster import (
 SOURCE_SHA,EXPECTED_ROWS,EXPECTED_PEOPLE,real_anon_session_universe)

PROTOCOL="protocols/R096_PHASE_D_2022_MONTERO_12_TRUE_SESSIONS_188_HUMANS_100_ROUND_BINARY_SESSION_LOSO_M012_SCORE_FREEZE_2026-10-17.md"
PERIODS={"EARLY_2_25":range(2,26),"LATER_26_100":range(26,101),
 "P1_2_25":range(2,26),"P2_26_50":range(26,51),
 "P3_51_75":range(51,76),"P4_76_100":range(76,101)}
EXPERIMENTS=("fix.csv","rand.csv")

def original_binary(x):
 v=str(x or "").strip()
 if v in ("0","0.0"):return 0
 if v in ("1","1.0"):return 1
 raise ValueError("R096D_AUTHORIGINAL_ACTION_NOT_EXACT_BINARY_0_1")

def read_original_actions(blob,name,people_count=None,original_rows=None,require_opponent_consistency=True):
 if name not in EXPERIMENTS:raise ValueError("R096D_UNFROZEN_ORIGINAL_TREATMENT")
 if people_count is None:people_count=EXPECTED_PEOPLE[name]
 if original_rows is None:original_rows=EXPECTED_ROWS[name]
 rdr=csv.DictReader(io.StringIO(blob.decode("utf-8-sig"),newline=""))
 keys={"session","player","opponent","round","action_player","action_opponent"}
 if rdr.fieldnames is None or not keys.issubset(rdr.fieldnames):
  raise ValueError("R096D_REQUIRED_ORIGINAL_AUTHOR_ACTION_FIELDS_MISSING")
 actor_records=defaultdict(dict);by_round={}
 value1=0;opp1=0;total=0
 for d in rdr:
  if None in d:raise ValueError("R096D_ORIGINAL_SOURCE_ROW_WIDTH_CHANGED")
  # Do not use author postprocessed history/context labels or demographic data.
  ss=str(d["session"] or "").strip();actor=str(d["player"] or "").strip()
  peer=str(d["opponent"] or "").strip()
  r=str(d["round"] or "").strip()
  if not ss or not actor or not peer or not r.isascii() or not r.isdigit() or not 1<=int(r)<=100:
   raise ValueError("R096D_REAL_ORIGINAL_SESSION_PLAYER_OR_ROUND_INVALID")
  t=int(r);a=original_binary(d["action_player"]);b=original_binary(d["action_opponent"])
  uid=(ss,actor);key=(ss,actor,t)
  if key in by_round:raise ValueError("R096D_REAL_ORIGINAL_DUPLICATE_ACTOR_ROUND")
  by_round[key]=(a,b,peer)
  actor_records[uid][t]=a
  value1+=a;opp1+=b;total+=1
 if total!=original_rows or len(actor_records)!=people_count:
  raise ValueError("R096D_SOURCE_ACTION_ROSTER_COUNT_CHANGED")
 for actions in actor_records.values():
  if set(actions)!=set(range(1,101)):
   raise ValueError("R096D_SOURCE_FIRST_PARTY_PERSON_NOT_ALL_100_ROUNDS")
 if require_opponent_consistency:
  for (ss,actor,t),(a,b,peer) in by_round.items():
   z=by_round.get((ss,peer,t))
   if z is None or z[2]!=actor or z[0]!=b or z[1]!=a or actor==peer:
    raise ValueError("R096D_ORIGINAL_AUTHOR_DYAD_OPPONENT_SOURCE_INCONSISTENT")
 return actor_records,{
  "source_anonymous_action_behavioral_row_count":total,
  "source_distinct_original_participants":len(actor_records),
  "original_source_binary_action_code_1_rows_NO_COOP_MAPPING":value1,
  "source_original_opponent_binary_code_1_rows_NO_COOP_MAPPING":opp1,
  "original_source_partner_0_1_identity_and_action_consistency":require_opponent_consistency,
  "original_person_round_actions_republished":False,
  "original_person_session_and_partner_identifiers_republished":False}

def mean(values):
 if not values:raise ValueError("R096D_ZERO_ORIGINAL_SESSION_TEST_TARGETS")
 return sum(values)/len(values)

def aggregate(rows):
 if not rows:return {"eligible_targets":0}
 return {"eligible_targets":len(rows),
  "M0_other_5_whole_sessions_same_round_Brier":mean([x[0] for x in rows]),
  "M1_own_previous_round_binary_Brier":mean([x[1] for x in rows]),
  "M2_fixed_half_Brier":mean([x[2] for x in rows]),
  "M1_gain_M0_minus_M1":mean([x[3] for x in rows]),
  "M2_gain_M0_minus_M2":mean([x[4] for x in rows])}

def complete_original_session_LOSO(actors,expected_people):
 sessions=defaultdict(list)
 for (ss,actor),history in actors.items():
  if set(history)!=set(range(1,101)):
   raise ValueError("R096D_ORIGINAL_SESSION_ROUNDS_NOT_COMPLETE")
  sessions[ss].append(history)
 if len(sessions)!=6 or sum(map(len,sessions.values()))!=expected_people:
  raise ValueError("R096D_UNVERIFIED_SIX_ORIGINAL_TRUE_SESSIONS")
 scores=[];sess_scores=[];byperiod=defaultdict(list)
 for heldout_session,heldout in sessions.items():
  other={t:[h[t] for ss,ps in sessions.items() if ss!=heldout_session
                  for h in ps] for t in range(2,101)}
  if any(len(other[t])!=expected_people-len(heldout) for t in range(2,101)):
   raise ValueError("R096D_ORIGINAL_HELDOUT_WHOLE_SESSION_LEAKED")
  this=[]
  for h in heldout:
   for t in range(2,101):
    y=h[t];p0=mean(other[t]);p1=h[t-1];p2=(p0+p1)/2.
    z=((p0-y)**2,(p1-y)**2,(p2-y)**2,
       (p0-y)**2-(p1-y)**2,(p0-y)**2-(p2-y)**2)
    scores.append(z);this.append((t,z))
    for pn,rg in PERIODS.items():
     if t in rg:byperiod[pn].append(z)
  sess_scores.append(aggregate([z for _,z in this]))
 if len(scores)!=expected_people*99 or len(sess_scores)!=6:
  raise ValueError("R096D_ORIGINAL_VALID_TARGETS_NOT_EXPECTED")
 gains1=[s["M1_gain_M0_minus_M1"] for s in sess_scores]
 gains2=[s["M2_gain_M0_minus_M2"] for s in sess_scores]
 signs=lambda v:{"positive":sum(x>0 for x in v),"negative":sum(x<0 for x in v),
                  "exact_equal":sum(x==0 for x in v)}
 return {"original_real_session_holdout_unit":"ONE_ENTIRE_GENUINE_LAB_SESSION",
  "original_true_sessions_left_out_once":len(sessions),
  "source_original_distinct_participant_IDs_in_six_sessions":expected_people,
  "original_actor_round_t2_to_t100_prediction_pairs":len(scores),
  "pooled_real_original_target_Brier_comparison":aggregate(scores),
  "by_fixed_early_and_late_precommitted_periods":{
    name:aggregate(byperiod[name]) for name in PERIODS},
  "original_six_session_gain_M1_signs":signs(gains1),
  "original_six_session_gain_M2_signs":signs(gains2),
  "anonymized_sorted_six_session_M1_gains":[round(x,12) for x in sorted(gains1)],
  "anonymized_sorted_six_session_M2_gains":[round(x,12) for x in sorted(gains2)],
  "M0_excludes_all_original_heldout_session_humans_every_round":True,
  "M1_previous_round_only_M2_exact_fixed_half":True,
  "source_action_1_not_assumed_to_mean_cooperation":True,
  "original_source_actor_round_or_original_session_labels_exported":False}

def actual_original():
 outcomes={};alltotals=[]
 for name in EXPERIMENTS:
  u=raw_url(name);validate_raw_url(u,name)
  req=urllib.request.Request(u,headers={
   "User-Agent":"Psychohistory-R096-2022-original-188humans-12true-lab-sessions-100rounds-binary-M012/1.0"})
  with urllib.request.urlopen(req,timeout=55) as r:
   validate_raw_url(r.geturl(),name);raw=r.read(CAP+1)
  ident=verify_author_blob(raw,name)
  if ident["full_original_whole_file_SHA256"]!=SOURCE_SHA[name]:
   raise ValueError("R096D_SOURCE_AUTHORIGINAL_SHA256_MISMATCH")
  structure=safe_original_csv_schema(raw)
  if structure["original_author_source_actor_action_row_count_NOT_YET_VALIDATED"]!=EXPECTED_ROWS[name]:
   raise ValueError("R096D_FIRST_PARTY_SOURCE_SHAPE_CHANGED")
  # Repeat complete original source nonbehavioral independent true-session audit.
  nonbehavior=real_anon_session_universe(raw,name)
  if nonbehavior["true_original_source_experiment_sessions"]!=6:
   raise ValueError("R096D_ORIGINAL_LAB_SESSION_COHORT_WRONG")
  cohort,eligibility=read_original_actions(raw,name)
  scoring=complete_original_session_LOSO(cohort,EXPECTED_PEOPLE[name])
  outcomes[name]={"original_author_fixed_blob_sha1":ident["original_git_blob_SHA1"],
    "original_author_whole_source_SHA256":ident["full_original_whole_file_SHA256"],
    "original_source_binary_partner_eligibility":eligibility,
    "true_original_session_loso":scoring}
  alltotals.append(scoring)
 n0=sum(v["pooled_real_original_target_Brier_comparison"]["eligible_targets"] for v in alltotals)
 def pooled(key):
  return sum(v["pooled_real_original_target_Brier_comparison"]["eligible_targets"]*
   v["pooled_real_original_target_Brier_comparison"][key] for v in alltotals)/n0
 return {"research_id":"R096",
  "status":"R096_FIRST_PARTY_AUTHOR_GIT_2022_12_REAL_SESSIONS_188_HUMANS_100ROUND_TRUE_SESSION_LOSO_E2_EXECUTED",
  "evidence_grade":"E2_RETROSPECTIVE_FIRST_PARTY_AUTHOR_CODE_REPO_REPROCESSED_CSV_NOT_IDENTICAL_VERIFIED_DRYAD",
  "published_original_paper_DOI":"10.1038/s41598-022-11654-2",
  "original_author_git_submission_commit":"4743f74d8a03a031b8f70aff64956f8ad5155182",
  "pre_score_freeze":PROTOCOL,
  "original_Dryad_source_unavailable_403_401":True,
  "actual_real_treatment_sessions":outcomes,
  "original_real_true_independent_sessions_total":12,
  "original_real_participant_codes_total":188,
  "original_real_actor_round_binary_source_rows":18800,
  "original_real_next_round_binary_source_targets":n0,
  "pooled_real_original_12_session_LOSO_Brier":{
    "M0":pooled("M0_other_5_whole_sessions_same_round_Brier"),
    "M1":pooled("M1_own_previous_round_binary_Brier"),
    "M2":pooled("M2_fixed_half_Brier"),
    "M1_gain":pooled("M1_gain_M0_minus_M1"),
    "M2_gain":pooled("M2_gain_M0_minus_M2")},
  "action_code_label_is_definitively_confirmed_cooperation":False,
  "full_12_original_session_time_forward_prospective_E3":False,
  "source_all_original_actor_IDs_and_human_action_rows_redistributed":False,
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",required=True,type=pathlib.Path);a=p.parse_args()
 try:res=actual_original()
 except (ValueError,KeyError,TypeError,OSError,UnicodeError,urllib.error.URLError,urllib.error.HTTPError) as e:
  msg=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R096D_") else "R096D_ORIGINAL_2022_AUTHOR_FP_SP_SESSION_E2_FAILED_CLOSED"
  res={"research_id":"R096","status":"R096D_ORIGINAL_AUTHOR_ACTION_OR_SESSION_E2_BLOCKED",
    "safe_failure":msg,"original_binary_model_scores":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(res,sort_keys=True,indent=2)+"\n")
 brief={x:res[x] for x in ("status","safe_failure","pooled_real_original_12_session_LOSO_Brier") if x in res}
 print(json.dumps(brief,sort_keys=True))
 if res["status"]!="R096_FIRST_PARTY_AUTHOR_GIT_2022_12_REAL_SESSIONS_188_HUMANS_100ROUND_TRUE_SESSION_LOSO_E2_EXECUTED":
  raise SystemExit(1)
if __name__=="__main__":main()
