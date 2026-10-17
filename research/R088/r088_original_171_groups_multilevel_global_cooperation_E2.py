#!/usr/bin/env python3
"""R088 immutable original author group-level human 6x20 multilevel PGG E2 audit.

Actual first-party de-identified original 'complete groups' subset only.
Exports condition-level aggregate counts, never subject, group or session IDs.
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,io,json,pathlib,urllib.request,urllib.error
from collections import Counter,defaultdict

REPO="chasmani/PUBLIC_social_identity_and_cooperation"
COMMIT="8ce2c0cac4784485232aa96295f48ff147290b05"
CSV_FILE="analysis/data/data_full_groups.csv"
CSV_BYTES=2270643
CSV_BLOB="f902865203bdb465a505869b593eca432831b2fa"
EXCLUDE_FILE="analysis/analysis_exclusions.R"
EXCLUDE_BLOB="5d7f6e65523df55a1f05bd69f48d60b9306783a9"
ANALYSIS_FILE="analysis/analysis_cooperation_rates.R"
ANALYSIS_BLOB="60793d82709a7807e86ceddd772fe2847733a6e2"
CONDITIONS=("GlobalOnly","Balanced","GlobalBoost")
ACTIONS=("global","local","other","self")
PERIODS=tuple(range(1,21))
N_PER_CONDITION=57
PUBLICATION="10.1038/s41598-025-30979-2"
PROTOCOL="protocols/R088_SIX_PERSON_MULTILEVEL_PUBLIC_GOODS_171_GROUP_ORIGINAL_SOURCE_E2_FREEZE_2026-10-17.md"

def blob_hash(b):
 if not isinstance(b,bytes):raise ValueError("R088_GIT_BLOB_BYTE_SOURCE_REQUIRED")
 return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def author_bytes(path,expected_blob,size_limit):
 if path not in (CSV_FILE,EXCLUDE_FILE,ANALYSIS_FILE):
  raise ValueError("R088_FROZEN_AUTHOR_PATH_UNKNOWN")
 url=f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/{path}"
 request=urllib.request.Request(url,headers={"User-Agent":"PsychologicalHistory-R088-original-sixperson-Git-blob-verification/1.0"})
 with urllib.request.urlopen(request,timeout=65) as response:
  if response.geturl()!=url:
   raise ValueError("R088_ORIGINAL_AUTHOR_SOURCE_REDIRECT_FORBIDDEN")
  raw=response.read(size_limit+1)
 if not 0<len(raw)<=size_limit:
  raise ValueError("R088_SOURCE_EMPTY_OR_OVERMAX")
 if blob_hash(raw)!=expected_blob:
  raise ValueError("R088_ORIGINAL_SOURCE_GIT_BLOB_UNEXPECTED")
 return raw

def parse_csv(raw):
 try:text=raw.decode("utf-8-sig")
 except UnicodeDecodeError as e:raise ValueError("R088_INVALID_ORIGINAL_AUTHOR_TEXT_ENCODING") from e
 reader=csv.DictReader(io.StringIO(text,newline=""))
 required=("group_id","subgroup_id","condition")+tuple(f"game.{i}.player.contribution" for i in PERIODS)
 if reader.fieldnames is None or not all(c in reader.fieldnames for c in required):
  raise ValueError("R088_ORIGINAL_AUTHOR_REQUIRED_COLS_ABSENT")
 if len(reader.fieldnames)!=len(set(reader.fieldnames)):
  raise ValueError("R088_DUPLICATED_AUTHOR_HEADER")
 return list(reader)

def one_group(group_rows):
 if len(group_rows)!=6:
  raise ValueError("R088_COMPLETE_AUTHOR_GROUP_NOT_SIX_PEOPLE")
 labels={r["condition"] for r in group_rows}
 if len(labels)!=1 or list(labels)[0] not in CONDITIONS:
  raise ValueError("R088_AUTHOR_GROUP_CONDITION_INCONSISTENT")
 cond=next(iter(labels))
 subgroups=Counter(r["subgroup_id"] for r in group_rows)
 if len(subgroups)!=2 or sorted(subgroups.values())!=[3,3] or any(not x for x in subgroups):
  raise ValueError("R088_ORIGINAL_GROUP_NOT_TWO_3_PERSON_SUBGROUPS")
 rounds=[]
 for period in PERIODS:
  field=f"game.{period}.player.contribution"
  choices=[r.get(field) for r in group_rows]
  if any(x not in ACTIONS for x in choices):
   raise ValueError("R088_HUMAN_ORIGINAL_ACTION_NULL_OR_UNEXPECTED")
  if cond=="GlobalOnly" and any(x not in ("global","self") for x in choices):
   raise ValueError("R088_GLOBALONLY_EXPERIMENT_HAS_UNAVAILABLE_LOCAL_OR_OTHER")
  cnt=Counter(choices)
  g=cnt["global"]
  if sum(cnt.values())!=6:raise ValueError("R088_PERSON_ROUND_ACTION_DENOMINATOR")
  rounds.append({"round":period,
    "global":g,"local":cnt["local"],"other":cnt["other"],"self":cnt["self"],
    "global_threshold_met":int(g>=4),
    "global_threshold_almost_met_at_3":int(g==3),
    "global_all_six":int(g==6),"global_zero":int(g==0)})
 return cond,rounds

def analyze_rows(rows,expected_groups_per_arm=57):
 if not rows:raise ValueError("R088_EMPTY_ORIGINAL_COMPLETE_GROUPS")
 group_sets=defaultdict(list)
 for r in rows:
  gid=r.get("group_id")
  if not gid or gid.isspace():
   raise ValueError("R088_GROUP_ID_MISSING")
  group_sets[gid].append(r)
 if len(group_sets)!=3*expected_groups_per_arm or len(rows)!=18*expected_groups_per_arm:
  raise ValueError("R088_AUTHOR_GROUP_UNIVERSE_171x6_NOT_VERIFIED")
 cond_groups=defaultdict(list)
 for members in group_sets.values():
  treatment,rounds=one_group(members)
  cond_groups[treatment].append(rounds)
 if {k:len(cond_groups[k]) for k in CONDITIONS}!={k:expected_groups_per_arm for k in CONDITIONS}:
  raise ValueError("R088_ORIGINAL_THREE_CONDITIONS_57_GROUPS_EACH_NOT_VERIFIED")
 result={}
 for treatment in CONDITIONS:
  groups=cond_groups[treatment]
  n=len(groups)
  perround=[]
  for t in range(20):
   gl=sum(g[t]["global"] for g in groups)
   local=sum(g[t]["local"] for g in groups)
   other=sum(g[t]["other"] for g in groups)
   kept=sum(g[t]["self"] for g in groups)
   met=sum(g[t]["global_threshold_met"] for g in groups)
   near=sum(g[t]["global_threshold_almost_met_at_3"] for g in groups)
   zero=sum(g[t]["global_zero"] for g in groups)
   alls=sum(g[t]["global_all_six"] for g in groups)
   if gl+local+other+kept!=6*n:
    raise ValueError("R088_CONDITION_PERSON_ROUND_ACTIONS_NOT_CONSERVED")
   perround.append({"round":t+1,"groups":n,
     "global_actions":gl,"local_actions":local,"other_local_group_actions":other,
     "self_actions":kept,
     "mean_fraction_investing_global":gl/(6*n),
     "mean_fraction_investing_local_either_group":(local+other)/(6*n),
     "mean_fraction_keeping":kept/(6*n),
     "global_threshold_met_groups":met,
     "global_threshold_met_rate":met/n,
     "global_threshold_just_missed_at_3_groups":near,
     "zero_global_investment_groups":zero,
     "all_six_global_investment_groups":alls})
  diffs=[(g[19]["global"]-g[0]["global"])/6 for g in groups]
  group_means=[sum(r["global"] for r in g)/120 for g in groups]
  result[treatment]={
   "original_complete_groups":n,
   "original_players_in_complete_groups":6*n,
   "original_group_rounds":20*n,
   "original_complete_players_action_rounds":120*n,
   "global_cooperation_group_equal_all20_mean":sum(group_means)/n,
   "global_cooperation_group_equal_first_round":perround[0]["mean_fraction_investing_global"],
   "global_cooperation_group_equal_last_round":perround[-1]["mean_fraction_investing_global"],
   "global_cooperation_first_last_group_equal_delta":sum(diffs)/n,
   "groups_more_global_first_to_last":sum(z>0 for z in diffs),
   "groups_less_global_first_to_last":sum(z<0 for z in diffs),
   "groups_same_global_first_to_last":sum(z==0 for z in diffs),
   "global_threshold_met_group_rounds_sum":sum(z["global_threshold_met_groups"] for z in perround),
   "global_threshold_met_rate_all20_group_rounds":sum(z["global_threshold_met_groups"] for z in perround)/(20*n),
   "global_threshold_met_groups_first_round":perround[0]["global_threshold_met_groups"],
   "global_threshold_met_groups_last_round":perround[-1]["global_threshold_met_groups"],
   "global_threshold_just_missed_at_three_group_rounds":sum(z["global_threshold_just_missed_at_3_groups"] for z in perround),
   "zero_global_group_rounds":sum(z["zero_global_investment_groups"] for z in perround),
   "mean_fraction_investing_local_either_group_all20":sum(z["mean_fraction_investing_local_either_group"] for z in perround)/20,
   "mean_fraction_self_all20":sum(z["mean_fraction_keeping"] for z in perround)/20,
   "original_twenty_rounds_complete_group_aggregate":perround,
   "group_observation_ids_exported":False}
 differences={}
 for left,right in (("GlobalOnly","Balanced"),("GlobalBoost","Balanced"),("GlobalBoost","GlobalOnly")):
  differences[f"{left}_minus_{right}"]=result[left]["global_cooperation_group_equal_all20_mean"]-result[right]["global_cooperation_group_equal_all20_mean"]
 return {"condition_aggregate":result,
   "frozen_source_group_mean_pair_contrasts":differences,
   "number_of_source_groups":len(group_sets),
   "source_human_participant_rows":len(rows),
   "group_rounds_scored":20*len(group_sets),
   "subject_round_actions_scored":20*len(rows)}

def original_full_replay():
 full=author_bytes(CSV_FILE,CSV_BLOB,2_500_000)
 if len(full)!=CSV_BYTES:raise ValueError("R088_AUTHOR_ORIGINAL_SIZE_NOT_FROZEN")
 exclude=author_bytes(EXCLUDE_FILE,EXCLUDE_BLOB,8_000)
 rates=author_bytes(ANALYSIS_FILE,ANALYSIS_BLOB,16_000)
 if b"data_full_groups.csv" not in exclude or b"global_group_contributions" not in rates:
  raise ValueError("R088_AUTHOR_GROUP_EXCLUSION_OR_MECHANISM_SCRIPT_NOT_RECOGNIZED")
 analysis=analyze_rows(parse_csv(full))
 return {"research_id":"R088",
  "status":"R088_TRUE_171_ORIGINAL_SIX_PERSON_GROUPS_ALL20_GROUP_LEVEL_E2_EXECUTED",
  "evidence_grade":"E2_RETROSPECTIVE_ORIGINAL_AUTHOR_COMPLETE_GROUPS_BEHAVIORAL_REANALYSIS",
  "source_paper_DOI":PUBLICATION,
  "original_source_commit":COMMIT,
  "original_full_group_CSV_git_blob":CSV_BLOB,
  "original_full_group_source_bytes":CSV_BYTES,
  "original_author_exclusions_R_git_blob":EXCLUDE_BLOB,
  "original_author_cooperation_rates_R_git_blob":ANALYSIS_BLOB,
  "protocol_frozen_before_original_human_scores":PROTOCOL,
  "original_group_behavior_results":analysis,
  "selection_scope":"ORIGINAL_AUTHOR_PRE_FILTERED_COMPLETE_SIX_PERSON_GROUPS_NOT_ALL_RECRUITED",
  "human_row_or_group_ID_exported":False,
  "raw_original_group_or_player_rows_exported":False,
  "cooperation_identity_questionnaire_causal_link":"NOT_IDENTIFIED",
  "intervention_random_effect":"NOT_IDENTIFIED_IN_THIS_DESCRIPTIVE_SCORE",
  "outside_lab_history_extrapolation":"NOT_ESTABLISHED",
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 args=p.parse_args()
 try:
  result=original_full_replay()
 except (ValueError,UnicodeDecodeError,OSError,KeyError,TypeError,urllib.error.HTTPError,urllib.error.URLError) as e:
  safe=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R088_") else "SOURCE_OR_SCHEMA_ERROR"
  result={"research_id":"R088","status":"R088_ORIGINAL_171_SIX_PLAYER_GROUP_E2_STRICT_FAIL_CLOSED",
    "safe_failure":safe,"human_or_group_scores_exported":0,"PESEN_v0.1":"FROZEN"}
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+"\n",encoding="utf-8")
 brief=result.get("original_group_behavior_results",{}).get("condition_aggregate",{})
 print(json.dumps({"status":result["status"],"safe_failure":result.get("safe_failure"),
  "groups":{k:{"original_complete_groups":v["original_complete_groups"],
    "global_mean":v["global_cooperation_group_equal_all20_mean"],
    "threshold_success_rate":v["global_threshold_met_rate_all20_group_rounds"],
    "first_round_global_share":v["global_cooperation_group_equal_first_round"],
    "last_round_global_share":v["global_cooperation_group_equal_last_round"],
    "groups_up":v["groups_more_global_first_to_last"],
    "groups_down":v["groups_less_global_first_to_last"],
    "groups_equal":v["groups_same_global_first_to_last"]}
    for k,v in brief.items()}},sort_keys=True))
 if result["status"]!="R088_TRUE_171_ORIGINAL_SIX_PERSON_GROUPS_ALL20_GROUP_LEVEL_E2_EXECUTED":
  raise RuntimeError("R088_ORIGINAL_COMPLETE_GROUPS_FAIL_CLOSED")
if __name__=="__main__":main()
