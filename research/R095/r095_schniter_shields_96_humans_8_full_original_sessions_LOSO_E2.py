#!/usr/bin/env python3
"""R095 96 real Chapman PD choices, eight original FULL LAB SESSION holdouts.

M0 leave all 12 actors of test session completely out of round2 training;
M1 target's own round1; M2 half. Binary Brier on ALL 96 original t2 choices.
No source IDs, partner traces, demographic fields or session codes in output.
Original published Fields.csv source MD5 and full SHA rechecked every run.
"""
from __future__ import annotations
import argparse,collections,csv,io,json,pathlib,urllib.request,urllib.error
from collections import Counter,defaultdict
from r095_schniter_shields_2020_original_session_roster_no_actions import (
 URL,MAX_FILE,check_source_url,verify_source_bytes,decode_original_metadata,EXPECTED_KEYS)

SHA256="0678cc3d565d3a02e4766fedff211cc37b2e0e9d373e41c391466c6f84a56f4c"
PROTOCOL="protocols/R095_PHASE_C_SCHNITER_SHIELDS_8_REAL_2020_LAB_SESSIONS_96_BINARY_ROUND2_LOSO_M012_FREEZE_2026-10-17.md"

def cooperation(source):
 val=str(source or "").strip().lower()
 if val=="split":return 1
 if val=="take all":return 0
 raise ValueError("R095C_ORIGINAL_SOURCE_BINARY_ACTION_UNRECOGNIZED")

def partner_choice_bit(source):
 val=str(source or "").strip()
 if val in ("0","1"):return int(val)
 raise ValueError("R095C_ORIGINAL_SOURCE_PARTNER_ACTION_NOT_BINARY")

def anonymous_real_actions(original,expected_sessions=8,persons_per_session=12,
                           expected_source_rows=204):
 # All metadata must be eligible before reading a single original action.
 nonbehavior=decode_original_metadata(original)
 if (nonbehavior["source_distinct_explicit_true_session_IDs"]!=expected_sessions
  or nonbehavior["source_unique_original_real_participants"]!=expected_sessions*persons_per_session
  or nonbehavior["source_total_original_actor_round_records"]!=expected_source_rows
  or any(n!=persons_per_session for n in nonbehavior["number_original_humans_per_true_session_sorted"])
  or nonbehavior["anonymous_original_round_1_2_3_actor_record_counts"]["1"]!=expected_sessions*persons_per_session
  or nonbehavior["anonymous_original_round_1_2_3_actor_record_counts"]["2"]!=expected_sessions*persons_per_session):
  raise ValueError("R095C_ORIGINAL_FROZEN_SESSION_ROSTER_CHANGED")
 rd=csv.reader(io.StringIO(original.decode("utf-8-sig"),newline=""))
 h=next(rd,None)
 if h is None or tuple(h[:6])!=EXPECTED_KEYS:
  raise ValueError("R095C_ORIGINAL_SOURCE_FIRST_SIX_COLUMNS_CHANGED")
 # Only fields 0..5 ever used; all original demographics and mood fields ignored.
 persons=defaultdict(dict);bygroup=defaultdict(dict)
 for row in rd:
  if len(row)!=len(h):raise ValueError("R095C_SOURCE_ORIGINAL_CSV_COLUMN_COUNT_CHANGED")
  uid,t,choice,session,group,other = row[:6]
  actor=uid.strip();ss=session.strip();gr=group.strip()
  if t not in ("1","2","3"):raise ValueError("R095C_SOURCE_ROUND_MALFORMED")
  if t=="3":continue # no behavior contents read or scored from extra session
  action=cooperation(choice)
  partner=partner_choice_bit(other)
  t=int(t)
  if (ss,gr,t,actor) in bygroup[(ss,gr,t)]:
   raise ValueError("R095C_DUPLICATE_SOURCE_ACTOR_GROUP_ROUND")
  persons[(ss,actor)][t]=action
  bygroup[(ss,gr,t)][actor]=(action,partner)
 if len(persons)!=expected_sessions*persons_per_session:
  raise ValueError("R095C_ORIGINAL_BINARY_MAIN_ROUND_SUBJECT_COUNT")
 for original_person,states in persons.items():
  if set(states)!={1,2}:raise ValueError("R095C_ORIGINAL_PERSON_SECOND_ROUND_ACTION_MISSING")
 if len(bygroup)!=expected_sessions*(persons_per_session//2)*2:
  raise ValueError("R095C_ORIGINAL_TWO_PLAYER_PAIR_ROUNDS_CHANGED")
 for group_round,states in bygroup.items():
  if len(states)!=2:raise ValueError("R095C_UNPAIRED_ORIGINAL_TWO_HUMAN_SOURCE")
  actors=list(states.values())
  if actors[0][1]!=actors[1][0] or actors[1][1]!=actors[0][0]:
   raise ValueError("R095C_ORIGINAL_OTHER_SPLIT_PARTNER_BEHAVIOR_INCONSISTENT")
 return persons,{
  "original_source_true_independent_lab_sessions":expected_sessions,
  "original_human_people":len(persons),
  "original_observed_first_round_binary_choices":len(persons),
  "original_observed_second_round_binary_choices":len(persons),
  "original_published_total_actor_round_rows_including_excluded_third_round":expected_source_rows,
  "second_round_original_partner_reports_consistent_with_actual_two_player_actions":True,
  "raw_original_person_pair_session_ids_and_source_microtraces_exported":False}

def mean(xs):
 if not xs:raise ValueError("R095C_ZERO_INDEPENDENT_SESSION_HOLDOUT_BASELINE")
 return sum(xs)/len(xs)

def evaluate_8_sessions(persons,expected_sessions=8,persons_per_session=12):
 sessions=defaultdict(list)
 for (s,person),ts in persons.items():
  if set(ts)!={1,2} or any(v not in (0,1) for v in ts.values()):
   raise ValueError("R095C_TARGET_PERSON_BINARY_ROUNDS_REQUIRED")
  sessions[s].append(ts)
 if len(sessions)!=expected_sessions or any(len(x)!=persons_per_session for x in sessions.values()):
  raise ValueError("R095C_FULL_ORIGINAL_SESSION_ROSTER_NOT_ELIGIBLE")
 all_pairs=[];heldout_session_gain_m1=[];heldout_session_gain_m2=[]
 session_sign=Counter()
 for target_session,actors in sessions.items():
  others=[ts[2] for other_session,other_people in sessions.items()
          if other_session!=target_session for ts in other_people]
  if len(others)!=(expected_sessions-1)*persons_per_session:
   raise ValueError("R095C_ORIGINAL_HELDOUT_LAB_SESSION_LEAKED_INTO_M0")
  p0=mean(others)
  per_session=[]
  for z in actors:
   y=z[2];p1=z[1];p2=0.5*(p0+p1)
   e0=(p0-y)**2;e1=(p1-y)**2;e2=(p2-y)**2
   rec=(e0,e1,e2,e0-e1,e0-e2)
   per_session.append(rec);all_pairs.append(rec)
  gain_m1=mean([v[3] for v in per_session])
  gain_m2=mean([v[4] for v in per_session])
  heldout_session_gain_m1.append(gain_m1)
  heldout_session_gain_m2.append(gain_m2)
  session_sign["M1_positive"]+=int(gain_m1>0)
  session_sign["M1_negative"]+=int(gain_m1<0)
  session_sign["M1_exact_equal"]+=int(gain_m1==0)
 if len(all_pairs)!=expected_sessions*persons_per_session:
  raise ValueError("R095C_TRUE_SESSION_HELDOUT_TEST_TARGETS_NOT_COMPLETE")
 return {
  "heldout_unit":"ENTIRE_ORIGINAL_INDEPENDENT_LAB_SESSION_OF_12_HUMANS",
  "true_original_independent_lab_sessions":expected_sessions,
  "entire_source_sessions_left_out_exactly_once":expected_sessions,
  "original_binary_round_2_predictions_all_subjects":len(all_pairs),
  "M0_seven_other_sessions_second_round_Brier_MSE":mean([x[0] for x in all_pairs]),
  "M1_own_first_round_binary_Brier_MSE":mean([x[1] for x in all_pairs]),
  "M2_fixed_halfblend_Brier_MSE":mean([x[2] for x in all_pairs]),
  "paired_gain_M0_minus_M1":mean([x[3] for x in all_pairs]),
  "paired_gain_M0_minus_M2":mean([x[4] for x in all_pairs]),
  "source_genuine_lab_session_signs_M1":dict(sorted(session_sign.items())),
  "anonymous_sorted_per_session_M1_gains":[round(q,12) for q in sorted(heldout_session_gain_m1)],
  "anonymous_sorted_per_session_M2_gains":[round(q,12) for q in sorted(heldout_session_gain_m2)],
  "source_own_t1_cooperation_fraction":mean([z[1] for x in sessions.values() for z in x]),
  "source_own_t2_cooperation_fraction":mean([z[2] for x in sessions.values() for z in x]),
  "training_all_12_holdout_people_excluded_from_M0":True,
  "first_round_own_behavior_legitimately_used_in_M1":True,
  "source_only_one_session_has_round3_not_scored":True,
  "raw_source_original_session_person_pair_group_labels_exported":False,
  "is_2026_blinded_prepublication_data_collection":False}

def actual_real_source():
 with urllib.request.urlopen(urllib.request.Request(URL,headers={
  "User-Agent":"Psychohistory-R095-original-2020-Chapman-real-eight-session-binary-M012/1.0"}),timeout=50) as r:
  check_source_url(r.geturl());b=r.read(MAX_FILE+1)
 ident=verify_source_bytes(b)
 if ident["original_full_file_SHA256"]!=SHA256:
  raise ValueError("R095C_FIRST_PARTY_ORIGINAL_SOURCE_SHA256_CHANGED")
 cohort,quality=anonymous_real_actions(b)
 result=evaluate_8_sessions(cohort)
 return {
  "research_id":"R095",
  "status":"R095_ORIGINAL_2020_CHAPMAN_8_TRUE_SESSIONS_96_BINARY_PEOPLE_LOSO_E2_EXECUTED",
  "evidence_grade":"E2_RETROSPECTIVE_FIRST_PARTY_TRUE_ORIGINAL_EXPERIMENT_SESSION_LOSO_BINARY_FRIEND_OR_FOE_ROUND2",
  "original_first_party_DOI":"10.5281/zenodo.4321821",
  "verified_publisher_MD5":ident["publisher_MD5"],
  "verified_original_full_source_SHA256":ident["original_full_file_SHA256"],
  "scoring_protocol_frozen_before_machine_result":PROTOCOL,
  "publisher_web_preview_of_some_original_actions_prior_to_scoring_freeze":True,
  "anonymous_original_source_roster_and_partner_consistency":quality,
  "original_lab_session_full_holdout_human_binary_prediction":result,
  "binary_Friend_or_Foe_is_identical_to_R089_global_PGG_vote":False,
  "fully_future_prospective_E3":False,
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 try:r=actual_real_source()
 except (ValueError,TypeError,OSError,UnicodeError,urllib.error.HTTPError,urllib.error.URLError) as e:
  msg=str(e)[:96] if isinstance(e,ValueError) and str(e).startswith("R095C_") else "R095C_REAL_FIRST_PARTY_SOURCE_ELIGIBILITY_OR_SCORING_FAIL_CLOSED"
  r={"research_id":"R095","status":"R095C_ORIGINAL_HUMAN_LAB_SESSION_SCORE_FAIL_CLOSED",
    "safe_failure":msg,"verified_real_behavioral_scores":0,"PESEN_v0.1":"FROZEN"}
 pth=a.parse_args().output
 pth.parent.mkdir(parents=True,exist_ok=True)
 pth.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf8")
 z=r.get("original_lab_session_full_holdout_human_binary_prediction",{})
 print(json.dumps({"status":r["status"],"safe_failure":r.get("safe_failure"),
  "session_score_macro":z},sort_keys=True))
 if r["status"]!="R095_ORIGINAL_2020_CHAPMAN_8_TRUE_SESSIONS_96_BINARY_PEOPLE_LOSO_E2_EXECUTED":
  raise SystemExit(1)
if __name__=="__main__":main()
