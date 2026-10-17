#!/usr/bin/env python3
"""R095 first-party original Chapman repeated Friend/Foe PD session source gate.

Only original ID, round, session and group source metadata are evaluated, never
human option, partner action, mood, age, sex or language. Real original MD5
must pass before CSV parse; original row values never exported.
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,io,json,pathlib,re,urllib.request,urllib.error
from collections import Counter,defaultdict

REC="4321821"
FILENAME="Fields.csv"
URL=f"https://zenodo.org/records/{REC}/files/{FILENAME}?download=1"
PUBLISHER_MD5="4c30ac1861e12f46e0b9847c9d1857a7"
MAX_FILE=100000
EXPECTED_KEYS=("ID","round","option","session","group","other_split")
ASCII_HEADER=re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,55}$")

def check_source_url(s):
 p=urllib.parse.urlparse(s)
 if p.scheme!="https" or p.netloc!="zenodo.org" or p.path!=f"/records/{REC}/files/{FILENAME}":
  raise ValueError("R095_SOURCE_NOT_PINNED_PUBLISHED_ZENODO_FILE")
 return True

def verify_source_bytes(b,md5=PUBLISHER_MD5):
 if not isinstance(b,bytes) or len(b)==0 or len(b)>MAX_FILE:
  raise ValueError("R095_INVALID_ORIGINAL_SOURCE_SIZE")
 if hashlib.md5(b).hexdigest()!=md5:
  raise ValueError("R095_AUTHOR_PUBLISHED_ORIGINAL_MD5_MISMATCH")
 return {"zenodo_original_fixed_record":int(REC),
         "original_file":FILENAME,"publisher_MD5":md5,
         "original_actual_byte_length":len(b),
         "original_full_file_SHA256":hashlib.sha256(b).hexdigest()}

def decode_original_metadata(b):
 try:s=b.decode("utf-8-sig")
 except UnicodeError as e:raise ValueError("R095_ORIGINAL_SOURCE_NOT_UTF8") from e
 src=csv.reader(io.StringIO(s,newline=""))
 h=next(src,None)
 if (not h or not 6<=len(h)<=60 or tuple(h[:6])!=EXPECTED_KEYS or
     len(h)!=len(set(h)) or any(not ASCII_HEADER.fullmatch(x) for x in h)):
  raise ValueError("R095_PUBLISHER_CODEBOOK_SOURCE_HEADER_CHANGED")
 # Only first 2 identifier columns + two group labels; never read behavior.
 ids=defaultdict(dict)
 pairs=defaultdict(set)
 group_rows=Counter()
 allrows=0
 for row in src:
  if len(row)!=len(h):raise ValueError("R095_SOURCE_PERSON_ROW_WIDTH_CHANGED")
  actor=str(row[0]).strip();t=str(row[1]).strip()
  session=str(row[3]).strip();group=str(row[4]).strip()
  if not actor or not session or not group or not t.isascii() or t not in ("1","2","3"):
   raise ValueError("R095_INVALID_ORIGINAL_ACTOR_SESSION_PAIR_OR_ROUND")
  t=int(t)
  if t in ids[actor]:raise ValueError("R095_DUPLICATE_PERSON_ROUND")
  ids[actor][t]=(session,group)
  pairs[(session,group)].add(actor)
  group_rows[(session,group,t)]+=1
  allrows+=1
 if not ids:raise ValueError("R095_SOURCE_HAS_NO_REAL_PARTICIPANTS")
 sessions=defaultdict(set)
 for actor,ts in ids.items():
  if not {1,2}.issubset(ts):raise ValueError("R095_SOURCE_LACKS_FIRST_OR_SECOND_ROUND")
  if set(ts)-{1,2,3}:raise ValueError("R095_SOURCE_ROUND_UNEXPECTED")
  if len(set(ts.values()))!=1:raise ValueError("R095_ORIGINAL_PERSON_SESSION_PAIR_CHANGES")
  ss,gr=ts[1]
  sessions[ss].add(actor)
 for (ss,gr),pp in pairs.items():
  if len(pp)!=2:raise ValueError("R095_ORIGINAL_PAIR_NOT_EXACT_TWO_HUMANS")
  for t in (1,2):
   if group_rows[(ss,gr,t)]!=2:raise ValueError("R095_MATCHED_TWO_PLAYER_PAIR_ROUND1_2_INCOMPLETE")
  if group_rows[(ss,gr,3)] not in (0,2):
   raise ValueError("R095_OPTIONAL_THIRD_ROUND_NOT_COMPLETE_PAIR")
 if len(sessions)<3:raise ValueError("R095_NOT_ENOUGH_INDEPENDENT_SESSIONS")
 if any(len(grouppeople)<4 for grouppeople in sessions.values()):
  raise ValueError("R095_ORIGINAL_LAB_SESSION_FEWER_THAN_FOUR")
 rows_by_round=Counter()
 for ts in ids.values():
  for t in ts:rows_by_round[t]+=1
 return {
  "source_total_original_actor_round_records":allrows,
  "source_unique_original_real_participants":len(ids),
  "source_distinct_explicit_true_session_IDs":len(sessions),
  "source_matched_original_two_person_pairs":len(pairs),
  "number_original_humans_per_true_session_sorted":[len(s) for s in sorted(sessions.values(),key=len)],
  "anonymous_original_round_1_2_3_actor_record_counts":{str(t):rows_by_round[t] for t in (1,2,3)},
  "original_person_id_has_all_rounds_1_and_2":True,
  "all_two_player_pairs_fixed_within_source_sessions":True,
  "no_original_private_session_person_pair_IDs_or_hashes_exported":True,
  "no_original_actor_option_or_partner_action_values_inspected":True,
  "no_original_age_sex_survey_or_video_information_inspected":True}

def source_metadata_reacquire():
 check_source_url(URL)
 with urllib.request.urlopen(urllib.request.Request(URL,headers={
  "User-Agent":"Psychohistory-R095-2020-Schniter-Shields-original-Fields-privacy-MD5-roster/1.0"}),timeout=50) as resp:
  check_source_url(resp.geturl());b=resp.read(MAX_FILE+1)
 return {
  "research_id":"R095","phase":"A_FIRST_PARTY_ORIGINAL_2020_SESSION_GROUP_ROSTER_NO_BEHAVIOR",
  "source_DOI":"10.5281/zenodo.4321821",
  "authentic_original_csv_byte_identity":verify_source_bytes(b),
  "safe_source_actual_original_session_roster":decode_original_metadata(b),
  "original_Zenodo_preview_exposed_some_action_values_prior_to_protocol":True,
  "real_human_prediction_scores":0,
  "PESEN_v0.1":"FROZEN"}

def main():
 a=argparse.ArgumentParser();a.add_argument("--output",type=pathlib.Path,required=True)
 opts=a.parse_args()
 try:r=source_metadata_reacquire()
 except (ValueError,OSError,TypeError,UnicodeError,urllib.error.HTTPError,urllib.error.URLError) as e:
  safe=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R095_") else "R095_OFFICIAL_ORIGINAL_SESSION_SOURCE_FAIL_CLOSED"
  r={"research_id":"R095","phase":"A_ORIGINAL_AUTHOR_SESSION_ROSTER_FAIL_CLOSED",
     "safe_failure":safe,"original_human_prediction_scores":0,"PESEN_v0.1":"FROZEN"}
 opts.output.parent.mkdir(parents=True,exist_ok=True)
 opts.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf8")
 print(json.dumps(r,sort_keys=True))
 if r["phase"]!="A_FIRST_PARTY_ORIGINAL_2020_SESSION_GROUP_ROSTER_NO_BEHAVIOR":
  raise SystemExit(1)
if __name__=="__main__":main()
