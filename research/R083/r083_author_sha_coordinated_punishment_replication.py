#!/usr/bin/env python3
"""R083 original-human independent paired conditional punishment main/replication E2.

Original author Stata file is held in-memory only, never stored in this project.
All output is anonymous cohort/subgroup aggregate paired binary counts.
"""
from __future__ import annotations
import argparse,hashlib,io,json,math,pathlib,urllib.request
from collections import Counter
import pandas as pd

AUTHOR_REPO="LucasMolleman/NHB_CoordinatedPunishment"
COMMIT="42cba97300910988b7b7386379fa32492d35d8aa"
DTA_GIT_BLOB="7989855cadae3dc70b83dd29bab572a1bc0d30fb"
DO_GIT_BLOB="981ca799943b97e9b6216053135e86db806eb0b5"
BASE=f"https://raw.githubusercontent.com/{AUTHOR_REPO}/{COMMIT}/"
PROTOCOL="protocols/R083_COORDINATED_PUNISHMENT_ORIGINAL_HUMAN_PAIRED_MAIN_REPLICATION_FREEZE_2026-10-17.md"
REQUIRED=("id","rerun","punisher","unconditional_punishment",
          "conditional_other_nopun","conditional_other_pun")
MAX_DTA=3_000_000;MAX_DO=250_000

def blob_sha(source:bytes)->str:
 if not isinstance(source,bytes):raise ValueError("R083_GIT_BLOB_SOURCE_NOT_BYTES")
 return hashlib.sha1(b"blob "+str(len(source)).encode()+b"\x00"+source).hexdigest()

def official_source_bytes(name,expected_sha,max_bytes):
 if name not in ("MKSG_Dataset.dta","MKSG_analysis.do"):
  raise ValueError("R083_NOT_FROZEN_AUTHOR_SOURCE_FILE")
 url=BASE+name
 req=urllib.request.Request(url,headers={"User-Agent":"Psychohistory-R083-real-original-2019-source-validation/1.0"})
 with urllib.request.urlopen(req,timeout=75) as response:
  data=response.read(max_bytes+1)
 if not 0<len(data)<=max_bytes:raise ValueError("R083_SOURCE_EMPTY_OR_OVERSIZED")
 if blob_sha(data)!=expected_sha:raise ValueError("R083_SOURCE_AUTHOR_COMMIT_BLOB_SHA_MISMATCH")
 return data

def exact_test_p(n01:int,n10:int)->float:
 if min(n01,n10)<0 or not isinstance(n01,int) or not isinstance(n10,int):
  raise ValueError("R083_NEGATIVE_OR_NON_INTEGER_SWITCH_COUNTS")
 total=n01+n10
 if not total:return 1.0
 lower=min(n01,n10)
 tail=sum(math.comb(total,k) for k in range(lower+1))
 return min(1.0,2*tail/(2**total))

def numeric_binary(v):
 if isinstance(v,bool):return int(v)
 if pd.isna(v):return None
 if isinstance(v,(float,int)) and v in (0,1):return int(v)
 raise ValueError("R083_BINARY_STRATEGY_INVALID_OR_UNMAPPED_LABEL")

def paired_stats(pairs:list[tuple[int,int]]):
 out=Counter()
 for a,b in pairs:
  if type(a) is not int or type(b) is not int or a not in (0,1) or b not in (0,1):
   raise ValueError("R083_NONBINARY_PAIRED_OUTCOME")
  out[(a,b)]+=1
 n=len(pairs);c00,c01,c10,c11=(out[(0,0)],out[(0,1)],out[(1,0)],out[(1,1)])
 if c00+c01+c10+c11!=n:raise ValueError("R083_PAIRED_SOURCE_COUNT_INCONSISTENCY")
 return {"n":n,"n00":c00,"n01_coordination_switch":c01,
         "n10_anti_coordination_switch":c10,"n11":c11,
         "punish_if_other_does_not":(c10+c11)/n if n else None,
         "punish_if_other_does":(c01+c11)/n if n else None,
         "paired_mean_difference":(c01-c10)/n if n else None,
         "conditional_McNemar_exact_two_sided_p":exact_test_p(c01,c10) if n else None,
         "discordant_pairs":c01+c10}

def validated_dataframe(raw):
 try:
  frame=pd.read_stata(io.BytesIO(raw),convert_categoricals=False)
 except (ValueError,TypeError,OSError,EOFError) as e:
  raise ValueError("R083_FROZEN_AUTHOR_STATA_READ_FAILURE") from e
 if frame.empty or len(frame)>100000:raise ValueError("R083_AUTHOR_DATASET_ROW_COUNT_GATE")
 if not all(x in frame.columns for x in REQUIRED):
  raise ValueError("R083_AUTHOR_REQUIRED_FIELDS_MISSING")
 for name in ("rerun","punisher","unconditional_punishment","conditional_other_nopun","conditional_other_pun"):
  frame[name]=pd.to_numeric(frame[name],errors="raise")
 if frame["id"].isna().any():raise ValueError("R083_ORIGINAL_HUMAN_ID_MISSING")
 if frame.duplicated(subset=["rerun","id"]).any():
  raise ValueError("R083_DUPLICATED_HUMAN_ID_WITHIN_AUTHOR_COHORT")
 if set(frame["rerun"].dropna().unique())!={0,1} or frame["rerun"].isna().any():
  raise ValueError("R083_AUTHOR_COHORT_MUST_BE_MAIN_AND_REPLICATION")
 if not set(frame["punisher"].dropna().unique()).issubset({0,1}):
  raise ValueError("R083_AUTHOR_PUNISHER_SELECTION_INVALID")
 if frame["punisher"].isna().any():
  raise ValueError("R083_AUTHOR_PUNISHER_SELECTION_MISSING")
 return frame

def analyse_dataframe(frame):
 cohort={}
 for rerun in (0,1):
  part=frame[frame["rerun"]==rerun]
  risk=part[part["punisher"]==1]
  other=part[part["punisher"]==0]
  valid_pairs=[]
  strata={0:[],1:[],"unknown":[]}
  invalid=0
  for _,row in risk.iterrows():
   a=numeric_binary(row["conditional_other_nopun"])
   b=numeric_binary(row["conditional_other_pun"])
   if a is None or b is None:
    invalid+=1
    continue
   uncond=numeric_binary(row["unconditional_punishment"])
   if uncond is None:uncond="unknown"
   valid_pairs.append((a,b))
   strata[uncond].append((a,b))
  if not valid_pairs:raise ValueError("R083_EMPTY_ELIGIBLE_RERUN_COHORT")
  overall=paired_stats(valid_pairs)
  subgroup={"unconditional_no":paired_stats(strata[0]),
            "unconditional_yes":paired_stats(strata[1]),
            "unconditional_unknown":paired_stats(strata["unknown"])}
  if sum(v["n"] for v in subgroup.values())!=overall["n"]:
   raise ValueError("R083_STRATA_DO_NOT_EXHAUST_RISK_SET")
  cohort["main" if rerun==0 else "replication"]={
   "author_cohort_code":rerun,
   "full_original_cohort_rows":len(part),
   "original_nonpunisher_excluded":len(other),
   "author_punisher_risk_set":len(risk),
   "eligible_paired_main_comparison":overall["n"],
   "punisher_pairs_excluded_due_to_missing_response":invalid,
   "main_paired_table":overall,
   "three_prespecified_unconditional_punishment_strata":subgroup}
 first=cohort["main"]["main_paired_table"]["paired_mean_difference"]
 second=cohort["replication"]["main_paired_table"]["paired_mean_difference"]
 pairs_pooled=[
  (sum(cohort[c]["main_paired_table"]["n00"] for c in ("main","replication")),
   sum(cohort[c]["main_paired_table"]["n01_coordination_switch"] for c in ("main","replication")),
   sum(cohort[c]["main_paired_table"]["n10_anti_coordination_switch"] for c in ("main","replication")),
   sum(cohort[c]["main_paired_table"]["n11"] for c in ("main","replication")))]
 overall_count=sum(pairs_pooled[0])
 return {"research_id":"R083",
  "status":"R083_REAL_AUTHOR_MAIN_AND_REPLICATION_PAIRED_STRATEGY_E2_EXECUTED",
  "grade":"E2_RETROSPECTIVE_ORIGINAL_AUTHOR_REAL_HUMAN_PAIRED_STRATEGY_METHOD",
  "freeze_protocol":PROTOCOL,
  "original_dataset_git_blob":DTA_GIT_BLOB,
  "original_analysis_script_git_blob":DO_GIT_BLOB,
  "original_commit":COMMIT,
  "author_original_rows":len(frame),
  "author_original_cohort_count":2,
  "stratum_effects_descriptive_only":True,
  "cohort_counts_and_paired_effects":cohort,
  "predeclared_two_cohort_directional_gate":"PASS_POSITIVE_IN_BOTH" if first>0 and second>0 else "NOT_SUPPORTED",
  "cohort_signs":{"main":("positive" if first>0 else "negative" if first<0 else "zero"),
                  "replication":("positive" if second>0 else "negative" if second<0 else "zero")},
  "pooled_supplementary_count_weighted_not_primary":{
   "n":overall_count,
   "n01":pairs_pooled[0][1],"n10":pairs_pooled[0][2],
   "paired_mean_difference":(pairs_pooled[0][1]-pairs_pooled[0][2])/overall_count},
  "human_id_exported":False,
  "human_source_rows_exported":False,
  "hypothetical_conditional_strategy_not_observed_peer_sanction_causing_actual_behavior":True,
  "original_cohort_independence_verified_from_source":False,
  "institutional_causal_policy_effect":"NOT_IDENTIFIED",
  "population_scale_predictive_transfer":"NOT_ESTABLISHED",
  "PESEN_v0.1":"FROZEN"}

def original_author_run():
 source=official_source_bytes("MKSG_Dataset.dta",DTA_GIT_BLOB,MAX_DTA)
 script=official_source_bytes("MKSG_analysis.do",DO_GIT_BLOB,MAX_DO)
 if not all(term in script for term in (
    b'MKSG_Dataset.dta',b'conditional_other_nopun',
    b'conditional_other_pun',b'rerun==0',b'rerun==1')):
  raise ValueError("R083_AUTHOR_SOURCE_DO_SCRIPT_SEMANTICS_NOT_PRESENT")
 frame=validated_dataframe(source)
 result=analyse_dataframe(frame)
 result["source_authentication"]={
  "original_github_repository":AUTHOR_REPO,
  "immutable_author_commit":COMMIT,
  "dataset_bytes":len(source),"original_git_blob_verified":True,
  "author_analysis_bytes":len(script),"original_analysis_script_git_blob_verified":True}
 return result

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--output",type=pathlib.Path,required=True)
 args=ap.parse_args()
 try:result=original_author_run()
 except (ValueError,TypeError,KeyError,OverflowError,urllib.error.HTTPError,urllib.error.URLError,OSError) as e:
  result={"research_id":"R083","status":"R083_STRICT_ORIGINAL_SOURCE_OR_RISK_SET_FAIL_CLOSED",
    "error_type":type(e).__name__,
    "error_code":str(e)[:95] if type(e) is ValueError else "ORIGINAL_SOURCE_IO_OR_SCHEMA_FAILURE",
    "real_human_statistics_exported":0,"PESEN_v0.1":"FROZEN"}
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"status":result["status"],
   "source_authentication":result.get("source_authentication"),
   "cohort_counts_and_paired_effects":result.get("cohort_counts_and_paired_effects"),
   "directional_gate":result.get("predeclared_two_cohort_directional_gate"),
   "error_code":result.get("error_code")},sort_keys=True))
 if result["status"]!="R083_REAL_AUTHOR_MAIN_AND_REPLICATION_PAIRED_STRATEGY_E2_EXECUTED":
  raise RuntimeError("R083_REAL_ORIGINAL_SOURCE_FAIL_CLOSED")
if __name__=="__main__":main()
