#!/usr/bin/env python3
"""R087 original author 134-human 10-period repeated conditional strategy audit E2.

Public first-party exact commit, git blob verification, session and individual
universe gating. Only treatment/group macro results; no actor/source rows.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,pathlib,urllib.request,urllib.error
from collections import Counter,defaultdict

ORIGINAL_REPO="seyhunsaral/stabilitycondcoop"
ORIGINAL_COMMIT="979abf87b5d3cfb7aa8be13b81ef233076c3bb75"
DATA_BLOB="bd4c1550002621bee7dfb50e0d15d317764d1ea9"
DATA_BYTES=425701
AUTHOR_PREPARATION_BLOB="522efd459f574ccaef3d9ce1dd2b086ffb70370e"
AUTHOR_PREPARATION_PATH="code/process_raw_data.R"
SOURCE_PATH="data/csv/subjects.csv"
SRC="https://raw.githubusercontent.com/"+ORIGINAL_REPO+"/"+ORIGINAL_COMMIT+"/"
REQUIRED=("treatment","session","period","subject","subject_unq","session_unq",
          "uc","ccL","ccM","ccH","action")
TREATMENTS=("CondInfo","NoCondInfo")
CATEGORIES=("D","F","C","O")
PROTOCOL="protocols/R087_AUTHOR_CONDITIONAL_COOPERATION_134_HUMANS_ORIGINAL_GIT_SOURCE_BEHAVIOR_FREEZE_2026-10-17.md"

def git_sha(content):
 if not isinstance(content,bytes):raise ValueError("R087_ORIGINAL_GIT_BLOB_NON_BYTES")
 return hashlib.sha1(b"blob "+str(len(content)).encode()+b"\0"+content).hexdigest()

def source_fetch(path,sha,maxbytes):
 if path not in (SOURCE_PATH,AUTHOR_PREPARATION_PATH):
  raise ValueError("R087_UNFROZEN_ORIGINAL_SOURCE_PATH")
 u=SRC+path
 request=urllib.request.Request(u,headers={
   "User-Agent":"Psychohistory-R087-2020-original-conditional-cooperation-source/1.0"})
 with urllib.request.urlopen(request,timeout=50) as response:
  if response.geturl()!=u:
   raise ValueError("R087_ORIGINAL_AUTHOR_SOURCE_REDIRECT_NOT_FROZEN")
  raw=response.read(maxbytes+1)
 if not 0<len(raw)<=maxbytes:
  raise ValueError("R087_SOURCE_EMPTY_OR_OVERSIZE")
 if git_sha(raw)!=sha:raise ValueError("R087_ORIGINAL_SOURCE_GIT_BLOB_HASH_MISMATCH")
 return raw

def ordinal_action(value):
 if value is None or not isinstance(value,str):
  raise ValueError("R087_MISSING_OR_NONSTRING_SOURCE_ACTION")
 try:v=float(value.strip())
 except ValueError as e:raise ValueError("R087_NONNUMERIC_ORIGINAL_THREE_LEVEL_CHOICE") from e
 if v not in (0.0,50.0,100.0):
  raise ValueError("R087_ACTION_OUTSIDE_0_50_100_AUTHOR_GAME")
 return int(v)

def strategy(a,b,c):
 if any(type(x) is not int or x not in (0,50,100) for x in (a,b,c)):
  raise ValueError("R087_WRONG_THREE_LEVEL_SCHEDULE")
 if a==b==c==0:return "D"
 if a==b==c:return "F"
 if a<=b<=c and c>a:return "C"
 return "O"

def parse_rows(text):
 if not isinstance(text,str):raise ValueError("R087_NON_UTF8_CSV_SOURCE")
 reader=csv.DictReader(io.StringIO(text))
 if reader.fieldnames is None or not all(k in reader.fieldnames for k in REQUIRED):
  raise ValueError("R087_AUTHOR_FIELDS_MISSING")
 if len(set(reader.fieldnames))!=len(reader.fieldnames):
  raise ValueError("R087_AUTHOR_DUPLICATE_FIELD_NAMES")
 return list(reader)

def by_person(records):
 if not records:raise ValueError("R087_EMPTY_AUTHOR_ROWS")
 people=defaultdict(dict)
 sessions=defaultdict(set)
 for row in records:
  if not all(k in row for k in REQUIRED):
   raise ValueError("R087_ORIGINAL_AUTHOR_FIELDS_CHANGED")
  treat=row["treatment"];p=row["period"]
  if treat not in TREATMENTS:raise ValueError("R087_AUTHOR_TREATMENT_UNKNOWN")
  if not p.isascii() or not p.isdigit() or int(p) not in range(1,11):
   raise ValueError("R087_AUTHOR_ONLY_1_TO_10_PAID_PERIODS")
  if not all(row.get(k,"").strip() for k in ("subject_unq","subject","session","session_unq")):
   raise ValueError("R087_AUTHOR_ID_SESSION_MISSING")
  who=row["subject_unq"]
  period=int(p)
  if period in people[who]:raise ValueError("R087_DUPLICATED_ORIGINAL_PERSON_PERIOD")
  choices={k:ordinal_action(row[k]) for k in ("uc","ccL","ccM","ccH","action")}
  people[who][period]=(treat,row["session"],row["session_unq"],row["subject"],choices)
  sessions[(treat,row["session_unq"])].add(who)
 if len(records)!=1340 or len(people)!=134 or len(sessions)!=6:
  raise ValueError("R087_ORIGINAL_134_PEOPLE_6_SESSIONS_1340_DECISIONS_MISMATCH")
 tr_session_counts=Counter(t for t,_ in sessions)
 if any(tr_session_counts[t]!=3 for t in TREATMENTS):
  raise ValueError("R087_ORIGINAL_3_SESSIONS_PER_TREATMENT_MISMATCH")
 cohort_people=Counter()
 for who,hist in people.items():
  if set(hist)!=set(range(1,11)):
   raise ValueError("R087_INCOMPLETE_ORIGINAL_PERSON_10_PERIODS")
  metas={(t,s,u,p) for t,s,u,p,_ in hist.values()}
  if len(metas)!=1:
   raise ValueError("R087_CROSS_PERIOD_PERSON_TREATMENT_SESSION_MISMATCH")
  treat=hist[1][0]
  cohort_people[treat]+=1
 if cohort_people["NoCondInfo"]!=68 or cohort_people["CondInfo"]!=66:
  raise ValueError("R087_2020_PUBLISHED_68_66_HUMANS_PARITY_FAILED")
 return people,sessions

def cohort_scores(person_histories):
 if not person_histories:raise ValueError("R087_EMPTY_TREATMENT")
 initial=Counter();final=Counter();cross=Counter()
 both_10_same=0;first_action=last_action=first_uc=last_uc=0
 slope_first=slope_last=0
 per_period={p:{"n":0,"classes":Counter(),"uc":0,"action":0,"cond_slope":0} for p in range(1,11)}
 for h in person_histories:
  if set(h)!=set(range(1,11)):raise ValueError("R087_SCORE_INCOMPLETE_PERSON")
  cats=[]
  for t in range(1,11):
   source=h[t][4]
   cat=strategy(source["ccL"],source["ccM"],source["ccH"])
   cats.append(cat)
   x=per_period[t];x["n"]+=1;x["classes"][cat]+=1
   x["uc"]+=source["uc"];x["action"]+=source["action"]
   x["cond_slope"]+=source["ccH"]-source["ccL"]
  initial[cats[0]]+=1;final[cats[-1]]+=1
  cross[(cats[0],cats[-1])]+=1
  if len(set(cats))==1:both_10_same+=1
  first,finalrow=h[1][4],h[10][4]
  first_action+=first["action"];last_action+=finalrow["action"]
  first_uc+=first["uc"];last_uc+=finalrow["uc"]
  slope_first+=first["ccH"]-first["ccL"]
  slope_last+=finalrow["ccH"]-finalrow["ccL"]
 n=len(person_histories)
 timeline=[]
 for t in range(1,11):
  c=per_period[t]
  if c["n"]!=n or sum(c["classes"].values())!=n:
   raise ValueError("R087_PERSON_PERIOD_DENOMINATOR_NOT_EXHAUSTIVE")
  timeline.append({"period":t,"people":n,
    "strategy_types":{k:c["classes"][k] for k in CATEGORIES},
    "mean_actualized_action":c["action"]/n,"mean_unconditional_choice":c["uc"]/n,
    "mean_conditional_H_minus_L":c["cond_slope"]/n})
 transition={a:{b:cross[(a,b)] for b in CATEGORIES} for a in CATEGORIES}
 if sum(sum(x.values()) for x in transition.values())!=n:
  raise ValueError("R087_FIRST_LAST_TRANSITION_UNIVERSE_NOT_COMPLETE")
 return {"participants":n,
  "first_strategy_classes":{k:initial[k] for k in CATEGORIES},
  "last_strategy_classes":{k:final[k] for k in CATEGORIES},
  "first_last_4_by_4_transition":transition,
  "initial_conditional_C_to_final_D":cross[("C","D")],
  "initial_unconditional_D_to_final_C":cross[("D","C")],
  "identical_strategy_class_all_10_periods":both_10_same,
  "first_mean_actualized_action":first_action/n,
  "final_mean_actualized_action":last_action/n,
  "mean_actualized_action_final_minus_first":(last_action-first_action)/n,
  "mean_unconditional_choice_final_minus_first":(last_uc-first_uc)/n,
  "first_mean_conditional_H_minus_L":slope_first/n,
  "final_mean_conditional_H_minus_L":slope_last/n,
  "mean_conditional_slope_final_minus_first":(slope_last-slope_first)/n,
  "all_ten_period_aggregate_timeline":timeline}

def original_aggregate(records):
 people,sessions=by_person(records)
 result={"all134":cohort_scores(list(people.values())),
  "by_original_information_treatment":{}}
 for treat in TREATMENTS:
  p=[v for v in people.values() if v[1][0]==treat]
  result["by_original_information_treatment"][treat]=cohort_scores(p)
 return {"research_id":"R087",
 "status":"R087_ORIGINAL_AUTHOR_FULL_134_HUMAN_10_PERIOD_STRATEGY_E2_EXECUTED",
 "source_fixed_commit":ORIGINAL_COMMIT,"source_CSV_git_blob":DATA_BLOB,
 "source_author_processing_R_git_blob":AUTHOR_PREPARATION_BLOB,
 "source_retroactivity":"PUBLISHED_2020_AUTHOR_E2_NOT_NEW_E3",
 "original_6_sessions_count":len(sessions),
 "original_134_humans_with_10_periods_each":134,
 "original_human_choice_period_rows":1340,
 "frozen_method_protocol":PROTOCOL,
 "original_human_aggregate":result,
 "actor_session_and_row_identifiers_exported":False,
 "original_person_decision_rows_exported":False,
 "model_mechanism_causal":"NOT_IDENTIFIED",
 "PESEN_v0.1":"FROZEN"}

def execute_original():
 data=source_fetch(SOURCE_PATH,DATA_BLOB,750000)
 if len(data)!=DATA_BYTES:raise ValueError("R087_AUTHOR_ORIGINAL_SUBJECTS_CSV_BYTES_MISMATCH")
 src=source_fetch(AUTHOR_PREPARATION_PATH,AUTHOR_PREPARATION_BLOB,35000)
 if b"subjects.csv" not in src:
  raise ValueError("R087_ORIGINAL_AUTHOR_SCRIPT_EXPECTED_CSV_GENERATOR_MISSING")
 return original_aggregate(parse_rows(data.decode("utf-8-sig")))

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args()
 try:r=execute_original()
 except (ValueError,OSError,UnicodeDecodeError,KeyError,TypeError,
         urllib.error.HTTPError,urllib.error.URLError) as e:
  reason=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R087_") else "STRICT_SOURCE_IO_OR_SCHEMA_FAILURE"
  r={"research_id":"R087","status":"R087_REAL_AUTHOR_SOURCE_OR_BEHAVIOR_ELIGIBILITY_FAIL_CLOSED",
     "safe_failure":reason,"real_human_scores_exported":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 print(json.dumps({"status":r["status"],
  "main_aggregate":r.get("original_human_aggregate",{}).get("all134"),
  "treatment_main":{
   k:{"participants":v["participants"],
      "action_delta":v["mean_actualized_action_final_minus_first"],
      "C_to_D":v["initial_conditional_C_to_final_D"],
      "D_to_C":v["initial_unconditional_D_to_final_C"]}
   for k,v in r.get("original_human_aggregate",{}).get("by_original_information_treatment",{}).items()},
  "safe_failure":r.get("safe_failure")},sort_keys=True))
 if r["status"]!="R087_ORIGINAL_AUTHOR_FULL_134_HUMAN_10_PERIOD_STRATEGY_E2_EXECUTED":
  raise RuntimeError("R087_SOURCE_OR_AUTHOR_RISK_SET_FAIL_CLOSED")
if __name__=="__main__":main()
