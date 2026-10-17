#!/usr/bin/env python3
"""R096: source-original research team 12 session IDs x 100 rounds metadata.

Do NOT access action_player or action_opponent or payoffs, decision times,
source person/session/partner values in any output. Only 4 frozen metadata cols.
"""
from __future__ import annotations
import argparse,collections,csv,io,json,pathlib,urllib.request,urllib.error
from collections import Counter,defaultdict
from r096_phase_b_montero_author_git_tag_pinned_original_FP_SP_CSV_source import (
 FILES,CAP,raw_url,validate_raw_url,verify_author_blob,safe_original_csv_schema)

SOURCE_SHA={
 "fix.csv":"c2adc0d68dbc15c4f5ec5f0eb9a05a988cc049a9c086b82f796521a642b6eae9",
 "rand.csv":"bc2999d6ad44c60f2b93361eb46b75614b1f600967ae061c76ae51184a80848a"}
EXPECTED_ROWS={"fix.csv":9200,"rand.csv":9600}
EXPECTED_PEOPLE={"fix.csv":92,"rand.csv":96}

def real_anon_session_universe(source,name,rows=None,persons=None):
 if name not in FILES:raise ValueError("R096C_UNPINNED_AUTHOR_TREATMENT")
 if rows is None:rows=EXPECTED_ROWS[name]
 if persons is None:persons=EXPECTED_PEOPLE[name]
 txt=source.decode("utf-8-sig")
 reader=csv.DictReader(io.StringIO(txt,newline=""))
 if not reader.fieldnames or not {"round","player","session","opponent"}.issubset(reader.fieldnames):
  raise ValueError("R096C_REQUIRED_ACTOR_SESSION_ROUND_PAIR_FIELDS_MISSING")
 roster=defaultdict(set);opp=defaultdict(set);sess_people=defaultdict(set)
 rowcount=0;dups=0;seen=set();allrounds=Counter()
 for obj in reader:
  if None in obj:raise ValueError("R096C_ORIGINAL_CSV_SOURCE_ROW_WIDTH_UNEXPECTED")
  # Only access four frozen nonbehavioral columns.
  ss=str(obj["session"] or "").strip()
  person=str(obj["player"] or "").strip()
  target=str(obj["opponent"] or "").strip()
  t=str(obj["round"] or "").strip()
  if not ss or not person or not target or not t.isascii() or not t.isdigit():
   raise ValueError("R096C_ORIGINAL_SOURCE_SESSION_PERSON_OPPONENT_ROUND_MISSING")
  rnd=int(t)
  if not 0<=rnd<=100:raise ValueError("R096C_SOURCE_ROUND_NOT_0_TO_100")
  pid=(ss,person);key=(ss,person,rnd)
  if key in seen:dups+=1
  seen.add(key);roster[pid].add(rnd);opp[pid].add(target)
  sess_people[ss].add(person);allrounds[rnd]+=1
  rowcount+=1
 if rowcount!=rows or dups:
  raise ValueError("R096C_SOURCE_ORIGINAL_ROW_COUNT_OR_DUPLICATE_ACTOR_ROUND")
 if len(sess_people)!=6 or len(roster)!=persons:
  raise ValueError("R096C_SOURCE_TRUE_SIX_SESSIONS_OR_PERSONS_NOT_CONFIRMED")
 lengths=[len(v) for v in sess_people.values()]
 if min(lengths)<4 or any(n%2 for n in lengths):
  raise ValueError("R096C_EXPERIMENT_SOURCE_SESSION_NOT_EVEN_OR_TOO_SMALL")
 allroundsets=[v for v in roster.values()]
 if any(len(x)!=100 for x in allroundsets):
  raise ValueError("R096C_ORIGINAL_SOURCE_PERSON_NOT_100_SEPARATE_ROUNDS")
 rset=set(range(1,101))
 if all(x==rset for x in allroundsets):convention="1_THROUGH_100"
 elif all(x==set(range(100)) for x in allroundsets):convention="0_THROUGH_99"
 else:raise ValueError("R096C_UNVERIFIED_OR_MIXED_ROUND_INDEX_CONVENTIONS")
 changers=sum(len(x)>1 for x in opp.values())
 if name=="fix.csv" and changers:
  raise ValueError("R096C_FIXED_PARTNER_ORIGINAL_OPPONENT_CHANGES")
 if name=="rand.csv" and not changers:
  raise ValueError("R096C_SHUFFLED_PARTNERS_NOT_SHUFFLED")
 return {"source_treatment_filename":name,
  "true_original_source_experiment_sessions":len(sess_people),
  "true_source_distinct_actor_IDs_within_original_session":len(roster),
  "true_source_original_actor_round_rows":rowcount,
  "original_six_true_session_person_counts_sorted":sorted(lengths),
  "source_round_convention":convention,
  "all_original_persons_exactly_100_distinct_rounds":True,
  "source_distinct_persons_with_partner_changes_over_100_rounds":changers,
  "original_all_actor_round_unique_without_duplicates":True,
  "source_original_cooperation_action_or_payoff_values_examined":False,
  "source_person_session_opponent_codes_or_hashes_republished":False}

def run_original():
 result={}
 for name in ("fix.csv","rand.csv"):
  url=raw_url(name)
  validate_raw_url(url,name)
  with urllib.request.urlopen(urllib.request.Request(url,headers={
   "User-Agent":"Psychohistory-R096-2022-author-tag-original-12session100round-identity-only/1.0"}),timeout=50) as response:
   validate_raw_url(response.geturl(),name)
   b=response.read(CAP+1)
  ident=verify_author_blob(b,name)
  if ident["full_original_whole_file_SHA256"]!=SOURCE_SHA[name]:
   raise ValueError("R096C_AUTHOR_ORIGINAL_WHOLE_FILE_SHA256_MISMATCH")
  shape=safe_original_csv_schema(b)
  if shape["original_author_source_actor_action_row_count_NOT_YET_VALIDATED"]!=EXPECTED_ROWS[name]:
   raise ValueError("R096C_PREVIOUS_AUTHOR_SOURCE_HEADER_ROWS_CHANGED")
  result[name]={"verified_original_author_blob_sha256":ident["full_original_whole_file_SHA256"],
    "source_nonbehavioral_original_session_roster":real_anon_session_universe(b,name)}
 return {"research_id":"R096","phase":"C_REAL_ORIGINAL_2022_AUTHOR_12SESSION_188_PERSON_100ROUND_NONBEHAVIOR_METADATA_ONLY",
  "original_primary_author_git_submission_sha1_pinned":True,
  "original_authors_Scientific_Reports_2022_DOI":"10.1038/s41598-022-11654-2",
  "original_Dryad_2022_Download_HTTP403_API401":True,
  "real_original_fixed_and_shuffled_treatment_rosters":result,
  "real_original_independent_sessions_total":sum(z["source_nonbehavioral_original_session_roster"]["true_original_source_experiment_sessions"] for z in result.values()),
  "real_original_player_ID_codes_total":sum(z["source_nonbehavioral_original_session_roster"]["true_source_distinct_actor_IDs_within_original_session"] for z in result.values()),
  "real_original_human_action_or_payoff_values_examined":False,
  "E2_real_original_session_loso_binary_actions_scored":False,
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args()
 try:r=run_original()
 except (ValueError,KeyError,OSError,UnicodeError,urllib.error.URLError,urllib.error.HTTPError) as e:
  safe=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R096C_") else "R096C_TRUE_SOURCE_SESSION_ROSTER_UNAVAILABLE_FAIL_CLOSED"
  r={"research_id":"R096","phase":"C_SOURCE_ORIGINAL_SESSION_ROSTER_FAIL_CLOSED",
   "safe_failure":safe,"real_original_E2_models_scored":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(json.dumps(r,sort_keys=True))
 if r["phase"]!="C_REAL_ORIGINAL_2022_AUTHOR_12SESSION_188_PERSON_100ROUND_NONBEHAVIOR_METADATA_ONLY":
  raise SystemExit(1)
if __name__=="__main__":main()
