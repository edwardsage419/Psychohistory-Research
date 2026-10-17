#!/usr/bin/env python3
"""R099 first-party S1 source 1920 rows: NO contribution or opponent-value access.

This script deliberately touches ONLY identifiers and Period, DF, Type strings.
Its group output is aggregate counts and candidate-key eligibility, not IDs.
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,io,json,pathlib,urllib.request,urllib.error
from collections import Counter,defaultdict
from r099_liu_2024_plos_official_original_S1_CSV_publisher_metadata_only import (
 URL,MAX_CSV,check_publisher_url,verify_bytes,source_safe_columns)
REAL_SHA="75dc8ae8b63a6b3ea728df9acab9d27944b82ec4feb5c6055e26751ca9cc4a6e"
EXPECTED_HEADER=["subject","id","Period","group","DF","Contribution","OtherContri","Type"]
N=1920

def cohort_metadata(raw,expected=N):
 reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""))
 if reader.fieldnames!=EXPECTED_HEADER:raise ValueError("R099B_ORIGINAL_SOURCE_EIGHT_COLUMNS_CHANGED")
 distinct=defaultdict(set); persons_a=defaultdict(list);persons_b=defaultdict(list)
 pairs=defaultdict(list);observations=[]
 for row in reader:
  if None in row:raise ValueError("R099B_ORIGINAL_CSV_ROW_WIDTH_CHANGED")
  # Only these six nonbehavior columns. NEVER access Contribution or OtherContri.
  a=str(row["subject"]).strip();b=str(row["id"]).strip()
  t=str(row["Period"]).strip();g=str(row["group"]).strip()
  condition=str(row["DF"]).strip();kind=str(row["Type"]).strip()
  if any(not x for x in (a,b,t,g,condition,kind)) or not t.isascii() or not t.isdigit():
   raise ValueError("R099B_ORIGINAL_SOURCE_ACTOR_GROUP_ROUND_TREATMENT_NONBEHAVIOR_MISSING")
  r=int(t)
  if not 1<=r<=20:raise ValueError("R099B_ORIGINAL_PERIOD_OUTSIDE_1_20")
  observations.append((a,b,r,g,condition))
  for k,v in (("subject",a),("id",b),("Period",t),("group",g),("DF",condition),("Type",kind)):
   distinct[k].add(v)
  persons_a[a].append(r);persons_b[b].append(r)
  pairs[(a,b)].append(r)
 if len(observations)!=expected:raise ValueError("R099B_ORIGINAL_ROW_COUNT_NOT_1920")
 def cohort(keys,actor_index):
  groups=defaultdict(list);actor_groups=defaultdict(set)
  for a,b,t,g,d in observations:
   fields={"subject":a,"id":b,"DF":d,"group":g}
   k=tuple(fields[x] for x in keys)
   person=a if actor_index=="subject" else b if actor_index=="id" else (a,b)
   groups[k].append((person,t))
   actor_groups[person].add(k)
  sizes=[];dupes=0;complete=0;count20=0
  for records in groups.values():
   people={p for p,_ in records}
   sizes.append(len(people))
   if len(records)==80 and len(people)==4 and len(set(records))==80 and {t for _,t in records}==set(range(1,21)):
    complete+=1
   dupes+=len(records)-len(set(records))
   if len(records)==80:count20+=1
  return {
   "original_candidate_group_key":"+".join(keys),
   "candidate_actor_key":actor_index,
   "anonymous_distinct_group_keys":len(groups),
   "anonymous_sizes_of_distinct_actors_per_group_sorted":sorted(sizes),
   "candidate_groups_each_exactly_4_people_20_rounds":complete,
   "groups_with_80_source_actor_round_rows":count20,
   "duplicate_source_actor_round_records":dupes,
   "individuals_found_in_multiple_group_keys":sum(len(v)>1 for v in actor_groups.values()),
   "is_exact_complete_24_fourperson_group_roster":complete==24 and len(groups)==24 and dupes==0
  }
 cand=[cohort(fields,actor) for fields in (
   ("group",),("DF","group"),("id","group"),("DF","id","group"),
   ("subject","group"),("DF","subject","group")) for actor in ("subject","id","subject+id")]
 a={k:len(v) for k,v in distinct.items()}
 return {"original_source_1920_rows":len(observations),
  "raw_metadata_field_distinct_label_counts_no_original_values":dict(sorted(a.items())),
  "raw_subject_IDs_with_20_original_round_records":sum(len(x)==20 and set(x)==set(range(1,21)) for x in persons_a.values()),
  "raw_id_IDs_with_20_original_round_records":sum(len(x)==20 and set(x)==set(range(1,21)) for x in persons_b.values()),
  "source_subject_id_pairs_count":len(pairs),
  "subject_id_pairs_with_20_unique_rounds":sum(len(x)==20 and set(x)==set(range(1,21)) for x in pairs.values()),
  "source_period_all_1_through_20":{r for _,_,r,_,_ in observations}==set(range(1,21)),
  "anonymous_candidate_group_key_structures":cand,
  "source_Contribution_or_OtherContri_action_values_accessed":False,
  "original_actors_groups_period_values_or_Type_category_labels_exported":False,
  "original_author_lab_session_field_directly_in_CSV":False}

def fetch_real():
 check_publisher_url(URL)
 with urllib.request.urlopen(urllib.request.Request(URL,headers={
   "User-Agent":"Psychohistory-R099-PLOS-2024-real-nonbehavior-actor-group-roster-only/1.0"}),timeout=50) as r:
  check_publisher_url(r.geturl());b=r.read(MAX_CSV+1)
 z=verify_bytes(b)
 if z["original_first_party_fullfile_SHA256"]!=REAL_SHA or z["exact_original_CSV_bytes"]!=43467:
  raise ValueError("R099B_ORIGINAL_FIRST_PARTY_CSV_SHA_OR_BYTES_CHANGED")
 shape=source_safe_columns(b)
 if shape["original_source_columns_only"]!=EXPECTED_HEADER or shape["original_source_rows_NOT_YET_VERIFIED_AS_REPEATED_PLAYER_ACTIONS"]!=N:
  raise ValueError("R099B_FIRST_PARTY_SOURCE_SHAPE_CHANGED")
 return {"research_id":"R099","phase":"B_REAL_PLOS_SOURCE_4P_GROUP_METADATA_NO_ACTIONS",
  "status":"R099_PLOS_ORIGINAL_METADATA_ROSTER_CANDIDATES_VERIFIED",
  "original_SHA256":REAL_SHA,
  "source_cohort_safe_metadata_only":cohort_metadata(b),
  "source_true_8_independent_laboratory_session_codes_proven":False,
  "real_original_human_contribution_model_scores":0,"PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 try:z=fetch_real()
 except (ValueError,KeyError,UnicodeError,OSError,TypeError,urllib.error.HTTPError,urllib.error.URLError) as e:
  why=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R099B_") else "R099B_ORIGINAL_PUBLISHER_GROUP_SOURCE_FAIL_CLOSED"
  z={"research_id":"R099","status":"R099B_SOURCE_GROUP_METADATA_BLOCKED","safe_failure":why,"real_human_scores":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(z,sort_keys=True,indent=2)+"\n")
 print(json.dumps(z,sort_keys=True))
 if z["status"]!="R099_PLOS_ORIGINAL_METADATA_ROSTER_CANDIDATES_VERIFIED":raise SystemExit(1)
if __name__=="__main__":main()
