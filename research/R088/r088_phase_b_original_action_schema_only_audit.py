#!/usr/bin/env python3
"""R088 Phase B: fixed-original-source action labels audit. No group-level scores."""
from __future__ import annotations
import argparse,collections,json,pathlib
from r088_original_171_groups_multilevel_global_cooperation_E2 import (
 author_bytes,parse_csv,CSV_FILE,CSV_BLOB,CSV_BYTES,EXCLUDE_FILE,EXCLUDE_BLOB,
 ANALYSIS_FILE,ANALYSIS_BLOB,CONDITIONS,PERIODS)

VALID=frozenset(("global","local","other","self"))
ALIASES=frozenset(("kept","keep","defect","nothing","0","1","2","3","na","n/a","none","null"))

def category(token):
 if token is None or not isinstance(token,str) or not token.strip():
  return "EMPTY_MISSING"
 if token in VALID:return "EXACT"
 lower=token.strip().lower()
 if lower in VALID:return "CASE_OR_SPACE_ONLY"
 if lower in ALIASES:return "DECLARED_COMMON_NON_EQUIVALENT"
 return "UNRECOGNIZED_OTHER"

def schema_counts(rows):
 if len(rows)!=1026:raise ValueError("R088_PHASEB_AUTHOR_COMPLETE_PLAYER_UNIVERSE_NOT_1026")
 counts=collections.Counter()
 by=collections.defaultdict(collections.Counter)
 raw_exact=collections.Counter()
 alias=collections.Counter()
 all_by_period=collections.defaultdict(collections.Counter)
 for row in rows:
  cond=row.get("condition")
  if cond not in CONDITIONS:
   raise ValueError("R088_PHASEB_UNEXPECTED_AUTHOR_CONDITION")
  for i in PERIODS:
   token=row.get(f"game.{i}.player.contribution")
   typ=category(token)
   counts[typ]+=1
   by[cond][typ]+=1
   all_by_period[i][typ]+=1
   if typ=="EXACT":
    raw_exact[token]+=1
   if typ=="CASE_OR_SPACE_ONLY":
    raw_exact[token.strip().lower()]+=1
   if typ=="DECLARED_COMMON_NON_EQUIVALENT":
    alias[token.strip().lower()]+=1
 result={
  "total_person_round_slots_seen":sum(counts.values()),
  "categories":{t:counts[t] for t in ("EXACT","CASE_OR_SPACE_ONLY","DECLARED_COMMON_NON_EQUIVALENT","EMPTY_MISSING","UNRECOGNIZED_OTHER")},
  "by_author_condition":{t:{k:by[t][k] for k in ("EXACT","CASE_OR_SPACE_ONLY","DECLARED_COMMON_NON_EQUIVALENT","EMPTY_MISSING","UNRECOGNIZED_OTHER")} for t in CONDITIONS},
  "safe_whitelisted_original_action_token_counts":{k:raw_exact[k] for k in sorted(VALID)},
  "safe_known_other_alias_counts":{k:alias[k] for k in sorted(alias)},
  "nonexact_occurrences_by_period_without_person_or_group":{str(p):sum(v for k,v in all_by_period[p].items() if k!="EXACT") for p in PERIODS},
  "safe_format_only_CI_repairable_case_or_space_without_any_other_error":
    (counts["CASE_OR_SPACE_ONLY"]>0 and counts["EMPTY_MISSING"]==0
     and counts["UNRECOGNIZED_OTHER"]==0
     and counts["DECLARED_COMMON_NON_EQUIVALENT"]==0),
  "all_actions_exact_frozen_schema":counts["EXACT"]==sum(counts.values())}
 if result["total_person_round_slots_seen"]!=20520:
  raise ValueError("R088_PHASEB_PERSON_ROUND_SOURCE_SLOTS_MISMATCH")
 return result

def evaluate():
 data=author_bytes(CSV_FILE,CSV_BLOB,2500000)
 if len(data)!=CSV_BYTES:raise ValueError("R088_PHASEB_ORIGINAL_AUTHOR_CSV_FILE_BYTE_MISMATCH")
 script=author_bytes(EXCLUDE_FILE,EXCLUDE_BLOB,8000)
 author_bytes(ANALYSIS_FILE,ANALYSIS_BLOB,16000)
 if b"data_full_groups.csv" not in script:
  raise ValueError("R088_PHASEB_AUTHOR_EXCLUSION_SCRIPT_IDENTITY_MISMATCH")
 fields=schema_counts(parse_csv(data))
 return {"research_id":"R088","phase":"B_FIXED_AUTHOR_ACTION_FIELD_METADATA_AUDIT",
  "source_SHA_blob_verified":True,"original_fixed_commit":"8ce2c0cac4784485232aa96295f48ff147290b05",
  "original_author_source_csv_blob":CSV_BLOB,
  "first_CI_R088_real_source_fail_retained":True,
  "schema_review":fields,
  "person_level_records_exported":False,"source_group_IDs_exported":False,
  "actual_global_cooperation_rate_recomputed":False,
  "actual_group_thresholds_recomputed":False,
  "real_human_group_E2":"BLOCKED_PENDING_AMENDED_SCHEMA_SOURCE_CONTRACT",
  "PESEN_v0.1":"FROZEN"}

def main():
 a=argparse.ArgumentParser();a.add_argument("--output",type=pathlib.Path,required=True)
 p=a.parse_args()
 try:result=evaluate()
 except (OSError,ValueError,TypeError,UnicodeError) as e:
  safe=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R088_") else "SOURCE_FETCH_OR_FIELD_FORMAT_FAILED"
  result={"research_id":"R088","phase":"B_ACTION_SOURCE_SCHEMA_FAIL_CLOSED",
    "status":safe,"real_human_group_E2":"NOT_COMPUTED",
    "real_human_group_scores_exported":0,"PESEN_v0.1":"FROZEN"}
 p.output.parent.mkdir(parents=True,exist_ok=True)
 p.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(result,sort_keys=True))
if __name__=="__main__":main()
