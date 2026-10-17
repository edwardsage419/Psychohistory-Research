#!/usr/bin/env python3
"""R094 original binary PGG secondary CSV *metadata only*, no behavior values.

Only node_id, round, visibility source fields are read; anonymous counts only.
No original session IDs exist in the secondary curated data.
"""
from __future__ import annotations
import argparse,collections,csv,io,json,pathlib,re,urllib.request,urllib.error
from collections import Counter,defaultdict
from r094_zhu_nishi_2015_binary_network_original_sessions_secondary_source_gate import (
 FILE,URL,LIMIT,source_url_valid,full_publisher_source_identity,schema_without_any_values)
FROZEN_SHA256="b37fa71434dd46249a0e7f43f9b9e798b1d3cafcffea3c80bc6997b99b6dd0a5"
EXPECTED_ROWS=14620
VIS_SAFE=re.compile(r"^[A-Za-z0-9_ -]{1,16}$")

def visibility_label(v):
 s=str(v or "").strip()
 return s if VIS_SAFE.fullmatch(s) else "REDACTED_VISIBILITY_CODE"

def cohort_round(v):
 x=str(v or "").strip()
 if not x.isascii() or not x.isdigit() or not 1<=int(x)<=10:
  raise ValueError("R094B_INVALID_SOURCE_NETWORK_ROUND")
 return int(x)

def private_identity_format(v):
 if not v:return "MISSING_SOURCE_NODE_ID"
 s=str(v).strip()
 if not s:return "MISSING_SOURCE_NODE_ID"
 if len(s)>128:return "REDACTED_LONG_ID"
 if s.isascii() and s.isdigit():return "ASCII_DECIMAL_IDENTIFIER"
 if s.isascii() and re.fullmatch(r"[A-Za-z0-9_-]+",s):return "ASCII_MIXED_ALNUM_IDENTIFIER"
 return "OTHER_OPAQUE_IDENTIFIER_FORMAT"

def anon_roster(rows,expected_rows=EXPECTED_ROWS):
 if len(rows)!=expected_rows:raise ValueError("R094B_SECONDARY_SOURCE_ROW_DENOMINATOR_MISMATCH")
 ids=defaultdict(set);id_vis=defaultdict(set);round_counts=Counter();vis_counts=Counter()
 id_formats=Counter();seen=set();duplicate=0;missing=0
 for row in rows:
  if len(row)!=3:raise ValueError("R094B_METADATA_READER_MUST_RECEIVE_ONLY_3_COLUMNS")
  ident,original_round,original_vis=row
  actor=str(ident or "").strip()
  id_formats[private_identity_format(actor)]+=1
  vis=visibility_label(original_vis)
  vis_counts[vis]+=1
  when=cohort_round(original_round)
  if not actor:
   missing+=1;continue
  key=(actor,when)
  if key in seen:duplicate+=1
  seen.add(key);ids[actor].add(when);id_vis[actor].add(vis)
  round_counts[when]+=1
 count_fulldecisions=sum(len(r)==10 and r==set(range(1,11)) for r in ids.values())
 wrong=sum(not(len(r)==10 and r==set(range(1,11))) for r in ids.values())
 changing_vis=sum(len(v)>1 for v in id_vis.values())
 return {"secondary_2026_original_binary_network_source_rows":len(rows),
  "distinct_original_node_ID_codes":len(ids),
  "number_of_node_IDs_with_exactly_10_unique_rounds_1_to_10":count_fulldecisions,
  "number_of_node_IDs_without_full_10_round_coverage":wrong,
  "duplicate_node_ID_round_combinations":duplicate,
  "missing_node_ID_rows":missing,
  "original_row_counts_by_round":{str(t):round_counts[t] for t in range(1,11)},
  "original_visibility_source_safe_code_counts":dict(sorted(vis_counts.items())),
  "number_of_original_node_IDs_with_visibility_change_across_rounds":changing_vis,
  "original_node_identifier_format_class_counts":dict(sorted(id_formats.items())),
  "raw_original_actor_node_IDs_or_hashes_exported":False,
  "any_human_decision_or_decision_time_or_neighbors_values_read":False,
  "original_experiment_session_ID_column_available":False,
  "independent_80_original_sessions_reconstructible_from_node_round_visibility_only":False}

def source_b():
 with urllib.request.urlopen(urllib.request.Request(URL,headers={
  "User-Agent":"Psychohistory-R094-source-no-human-choice-person-visibility-check/1.0"}),timeout=60) as resp:
  source_url_valid(resp.geturl());raw=resp.read(LIMIT+1)
 ident=full_publisher_source_identity(raw)
 if ident["independently_computed_raw_SHA256"]!=FROZEN_SHA256:
  raise ValueError("R094B_FULL_SOURCE_SHA256_NOT_PRE_FROZEN_IDENTITY")
 first=schema_without_any_values(raw)
 if first["original_data_row_count"]!=EXPECTED_ROWS:
  raise ValueError("R094B_OFFICIAL_HEADER_ROW_COUNT_CHANGED")
 reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""))
 if not {"node_id","round","visibility"}.issubset(reader.fieldnames):
  raise ValueError("R094B_SECONDARY_SOURCE_NO_NODE_ROUND_VISIBILITY")
 # Only ever extract the three specifically frozen metadata fields.
 records=[(z["node_id"],z["round"],z["visibility"]) for z in reader]
 r=anon_roster(records)
 return {"research_id":"R094","phase":"B_REAL_SECONDARY_NISHI_NETWORK_PERSON_ROUND_METADATA_ONLY",
  "original_secondary_publisher_MD5_verified":ident["fixed_publisher_MD5"],
  "original_secondary_full_SHA256_verified":ident["independently_computed_raw_SHA256"],
  "original_binary_network_source_roster":r,
  "2026_secondary_curated_not_original_2015_raw_log":True,
  "real_original_human_binary_decisions_examined":0,
  "human_history_model_predicted":False,
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 try:r=source_b()
 except (OSError,ValueError,TypeError,urllib.error.URLError,urllib.error.HTTPError) as e:
  safe=str(e)[:105] if isinstance(e,ValueError) and str(e).startswith("R094B_") else "R094B_SECONDARY_AUTHOR_SOURCE_ROSTER_FAIL_CLOSED"
  r={"research_id":"R094","phase":"B_NETWORK_SOURCE_ANON_ROSTER_FAIL_CLOSED",
     "safe_failure":safe,"human_cooperation_outcomes_scored":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(r,sort_keys=True))
if __name__=="__main__":main()
