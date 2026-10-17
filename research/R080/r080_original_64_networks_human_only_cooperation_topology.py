#!/usr/bin/env python3
"""R080 real author 64-network 30-round human/bot-separated descriptive E2.

Read all 64 exact publisher-SHA-verified human/agent experiment JSONs, verify
whole original network universe before computing any real outcome statistics,
aggregate equal-weight across original independent networks, never publish
game IDs, human IDs, node links, single-network scores or signed URLs.
"""
from __future__ import annotations
import argparse,hashlib,json,pathlib,statistics
from collections import Counter,defaultdict
from urllib.error import URLError,HTTPError
from r080_official_dataset_per_file_content_and_role_schema import (
    BASE,DOI,MAX_METADATA,MAX_ITEM,SHA256_RE,get,metadata_overview,safe_official_download_url,
)

STUDY_PROTOCOL="protocols/R080_REAL_64_HUMAN_NETWORKS_HUMAN_BOT_SPLIT_TOPOLOGY_BEFORE_SCORE_FREEZE_2026-10-17.md"
FILE_COUNT=70
NETWORK_COUNT=64
HUMANS_PER_NETWORK=16
BEHAVIOR_ROUNDS=30
NETWORK_SNAPSHOTS=31
TREATMENTS=(
 "no_bots","allc_bots","tft_bots","random_mgmt_bots",
 "engaged_mgmt_bots","disengaged_mgmt_bots",
 "disengaged_mgmt_visible_bots","single_mgmt_bot",
)
TREATMENT_NET_COUNT=8
MEASURES=("human_coop_first","human_coop_last","human_coop_delta",
          "human_coop_early15","human_coop_late15","human_coop_late_minus_early",
          "human_action_coverage_rate",
          "nodes_total","bot_nodes",
          "edges_first_all","edges_last_all",
          "edges_first_HH","edges_last_HH",
          "edges_first_HB","edges_last_HB",
          "edges_first_BB","edges_last_BB",
          "HH_density_first","HH_density_last",
          "added_edges_30_steps","removed_edges_30_steps",
          "changed_edges_30_steps")
def average(values):
 vals=list(values)
 if not vals:raise ValueError("R080_EMPTY_NETWORK_GROUP_AVERAGE")
 return sum(vals)/len(vals)

def parse_network_source(doc:dict):
 """Never output human IDs or outcomes; local validations return normalized private structure."""
 if not isinstance(doc,dict):
  raise ValueError("R080_ORIGINAL_NETWORK_JSON_NOT_OBJECT")
 expected={"game_id","treatment","players","result_behaviors","result_networks"}
 if not expected.issubset(doc):
  raise ValueError("R080_ORIGINAL_NETWORK_TOP_LEVEL_SOURCE_MISSING")
 game=doc["game_id"]
 tr=doc["treatment"]
 if not isinstance(game,str) or not game or tr not in TREATMENTS:
  raise ValueError("R080_ORIGINAL_GAME_ID_OR_TREATMENT_INVALID")
 players=doc["players"]
 if not isinstance(players,list) or len(players)<HUMANS_PER_NETWORK:
  raise ValueError("R080_MISSING_ORIGINAL_PLAYERS")
 actor_types={}
 for rec in players:
  if not isinstance(rec,dict) or not isinstance(rec.get("player"),str) or not rec["player"] or type(rec.get("is_bot")) is not bool:
   raise ValueError("R080_ACTOR_ID_OR_BOT_BOOL_SCHEMA_INVALID")
  if rec["player"] in actor_types:raise ValueError("R080_DUPLICATE_PLAYER_IN_ORIGINAL_NETWORK")
  actor_types[rec["player"]]=rec["is_bot"]
 human={person for person,is_bot in actor_types.items() if not is_bot}
 if len(human)!=HUMANS_PER_NETWORK:
  raise ValueError("R080_EXPECTED_16_EXACT_REAL_HUMANS_PER_NETWORK")
 behaviors=doc["result_behaviors"]
 networks=doc["result_networks"]
 if (not isinstance(behaviors,list) or len(behaviors)!=BEHAVIOR_ROUNDS
   or not isinstance(networks,list) or len(networks)!=NETWORK_SNAPSHOTS):
  raise ValueError("R080_THIRTY_ACTION_ROUNDS_THIRTY_ONE_NETWORK_SNAPSHOTS_INCOMPLETE")
 rounds_b=[]
 human_rates=[]
 human_n=human_observed=0
 for b in behaviors:
  if not isinstance(b,dict) or not all(k in b for k in ("round","cooperation","rewiring")):
   raise ValueError("R080_ACTION_ROUND_FIELDS_MISSING")
  rd=b["round"]
  if type(rd) is not int:raise ValueError("R080_ORIGINAL_BEHAVIOR_ROUND_NUMBER_TYPE_INVALID")
  rounds_b.append(rd)
  actions=b["cooperation"]; rew=b["rewiring"]
  if not isinstance(actions,list) or not isinstance(rew,list):
   raise ValueError("R080_ORIGINAL_BEHAVIOR_LIST_SCHEMA_INVALID")
  observed=set();human_actions=[]
  for a in actions:
   if not isinstance(a,dict):
    raise ValueError("R080_COOPERATION_BEHAVIOR_NOT_OBJECT")
   person=a.get("player"); act=a.get("action")
   if person not in actor_types or person in observed:
    raise ValueError("R080_UNKNOWN_OR_DUPLICATE_REALIZED_ACTOR")
   if act not in ("C","D"):
    raise ValueError("R080_NON_C_D_ORIGINAL_ACTION_NO_SILENT_DEFECTOR_MAPPING")
   observed.add(person)
   if person in human:human_actions.append(int(act=="C"))
  if not human_actions:raise ValueError("R080_NO_REAL_HUMAN_CHOICES_IN_ORIGINAL_ROUND")
  human_n+=len(human);human_observed+=len(human_actions)
  human_rates.append(sum(human_actions)/len(human_actions))
  for e in rew:
   if not isinstance(e,dict) or not all(k in e for k in ("sender","receiver","action")):
    raise ValueError("R080_ORIGINAL_REWIRING_EVENT_SCHEMA_INVALID")
   if e["sender"] not in actor_types or e["receiver"] not in actor_types:
    raise ValueError("R080_REWIRING_ACTOR_NOT_IN_NETWORK")
 if any(rounds_b[i]>=rounds_b[i+1] for i in range(len(rounds_b)-1)):
  raise ValueError("R080_BEHAVIOR_ROUNDS_NOT_STRICT_INCREASING")
 rounds_n=[];snapshots=[];snap_class=[]
 for snap in networks:
  if not isinstance(snap,dict) or "round" not in snap or "network" not in snap:
   raise ValueError("R080_NETWORK_SNAPSHOT_FIELDS_MISSING")
  rd=snap["round"]
  if type(rd) is not int:raise ValueError("R080_NETWORK_ROUND_NUMBER_INVALID")
  rounds_n.append(rd)
  network=snap["network"]
  if not isinstance(network,dict) or network.get("directed") is not False or network.get("multigraph") is not False:
   raise ValueError("R080_NETWORK_MUST_BE_SIMPLE_UNDIRECTED")
  nodes=network.get("nodes");links=network.get("links")
  if not isinstance(nodes,list) or not isinstance(links,list):
   raise ValueError("R080_NETWORK_NODES_LINKS_NOT_LIST")
  ids=[n.get("id") for n in nodes if isinstance(n,dict)]
  if len(ids)!=len(nodes) or len(set(ids))!=len(ids) or set(ids)!=set(actor_types):
   raise ValueError("R080_NETWORK_SNAPSHOT_NODES_NOT_EQUAL_REAL_ACTORS")
  edges=set();kinds=Counter()
  for link in links:
   if not isinstance(link,dict):raise ValueError("R080_EDGE_NOT_OBJECT")
   a=link.get("source");b=link.get("target")
   if a not in actor_types or b not in actor_types or a==b:
    raise ValueError("R080_EDGE_UNKNOWN_ACTOR_OR_SELF_LOOP")
   edge=frozenset((a,b))
   if edge in edges:raise ValueError("R080_DUPLICATE_UNDIRECTED_EDGE")
   edges.add(edge)
   is_bot_pair=(int(actor_types[a])+int(actor_types[b]))
   kinds[("HH","HB","BB")[is_bot_pair]]+=1
  snapshots.append(edges);snap_class.append(kinds)
 if any(rounds_n[i]>=rounds_n[i+1] for i in range(len(rounds_n)-1)):
  raise ValueError("R080_NETWORK_ROUNDS_NOT_STRICT_INCREASING")
 if len(networks)!=len(behaviors)+1:
  raise ValueError("R080_NETWORK_BEHAVIOR_TEMPORAL_SEQUENCE_LENGTH_MISMATCH")
 return {"game_id":game,"treatment":tr,
  "actor_types_private":actor_types,
  "human_rates_private":human_rates,
  "human_observed_actions":human_observed,
  "human_possible_actions":human_n,
  "snapshots_private":snapshots,
  "edge_types_private":snap_class,
  "human_nodes":len(human),"bot_nodes":len(actor_types)-len(human)}

def network_moments_validated(z:dict):
 human_rates=z["human_rates_private"]
 snapshots=z["snapshots_private"]
 edge_types=z["edge_types_private"]
 changed_add=sum(len(snapshots[i+1]-snapshots[i]) for i in range(BEHAVIOR_ROUNDS))
 changed_drop=sum(len(snapshots[i]-snapshots[i+1]) for i in range(BEHAVIOR_ROUNDS))
 early=average(human_rates[:15]);late=average(human_rates[15:])
 edges_first=edge_types[0];edges_last=edge_types[-1]
 return {
  "human_coop_first":human_rates[0],
  "human_coop_last":human_rates[-1],
  "human_coop_delta":human_rates[-1]-human_rates[0],
  "human_coop_early15":early,
  "human_coop_late15":late,
  "human_coop_late_minus_early":late-early,
  "human_action_coverage_rate":z["human_observed_actions"]/z["human_possible_actions"],
  "nodes_total":z["human_nodes"]+z["bot_nodes"],
  "bot_nodes":z["bot_nodes"],
  "edges_first_all":len(snapshots[0]),"edges_last_all":len(snapshots[-1]),
  "edges_first_HH":edges_first["HH"],"edges_last_HH":edges_last["HH"],
  "edges_first_HB":edges_first["HB"],"edges_last_HB":edges_last["HB"],
  "edges_first_BB":edges_first["BB"],"edges_last_BB":edges_last["BB"],
  "HH_density_first":edges_first["HH"]/(HUMANS_PER_NETWORK*(HUMANS_PER_NETWORK-1)/2),
  "HH_density_last":edges_last["HH"]/(HUMANS_PER_NETWORK*(HUMANS_PER_NETWORK-1)/2),
  "added_edges_30_steps":changed_add,
  "removed_edges_30_steps":changed_drop,
  "changed_edges_30_steps":changed_add+changed_drop
 }

def aggregate_all_64_source_files(metadata,documents):
 """documents: list original SHA verified JSON dicts; no human target model."""
 overview=metadata_overview(metadata)
 if (overview["original_file_count"]!=FILE_COUNT
    or overview["file_extensions"]!={"csv":3,"json":64,"r":3}
    or overview["sha256_published_in_file_content_details_count"]!=70):
  raise ValueError("R080_70_OFFICIAL_AUTHOR_FILES_MANIFEST_CHANGED")
 if len(documents)!=NETWORK_COUNT:raise ValueError("R080_EXACT_64_NETWORK_ORIGINAL_SOURCE_MISSING")
 # Mandatory full all-source validation before *any* outcome aggregation.
 validated=[parse_network_source(x) for x in documents]
 games=[z["game_id"] for z in validated]
 if len(set(games))!=NETWORK_COUNT:
  raise ValueError("R080_DUPLICATE_NETWORK_EXPERIMENT_ID")
 tr=Counter(z["treatment"] for z in validated)
 if set(tr)!=set(TREATMENTS) or any(tr[t]!=TREATMENT_NET_COUNT for t in TREATMENTS):
  raise ValueError("R080_8_GROUPS_TIMES_8_ORIGINAL_NETWORKS_UNIVERSE_MISMATCH")
 # All original 64 network and 1024 real human slots passed.
 metrics_by_treat=defaultdict(list)
 for z in validated:
  m=network_moments_validated(z)
  metrics_by_treat[z["treatment"]].append(m)
 def summarize(ms):
  result={"networks":len(ms)}
  for k in MEASURES:
   result[k]=average(m[k] for m in ms)
  result["network_cooperation_end_greater"]=sum(m["human_coop_delta"]>0 for m in ms)
  result["network_cooperation_end_equal"]=sum(m["human_coop_delta"]==0 for m in ms)
  result["network_cooperation_end_lower"]=sum(m["human_coop_delta"]<0 for m in ms)
  result["bot_nodes_min"]=min(m["bot_nodes"] for m in ms)
  result["bot_nodes_max"]=max(m["bot_nodes"] for m in ms)
  if result["network_cooperation_end_greater"]+result["network_cooperation_end_equal"]+result["network_cooperation_end_lower"]!=len(ms):
   raise ValueError("R080_NETWORK_POS_NEG_SIGN_ACCOUNTING_ERROR")
  if abs(result["human_coop_delta"]-(result["human_coop_last"]-result["human_coop_first"]))>1e-12:
   raise ValueError("R080_GLOBAL_HUMAN_ONLY_RATE_CHANGE_IDENTITY_ERROR")
  for side in ("first","last"):
   if abs(result[f"edges_{side}_all"]-sum(result[f"edges_{side}_{t}"] for t in ("HH","HB","BB")))>1e-12:
    raise ValueError("R080_HUMAN_BOT_EDGE_TYPE_PARTITION_ERROR")
  return result
 combined=[m for v in metrics_by_treat.values() for m in v]
 return {"research_id":"R080",
   "status":"R080_FIRST_PARTY_AUTHOR_64_NETWORK_HUMAN_ONLY_TOPOLOGY_E2_EXECUTED",
   "evidence_grade":"E2_PUBLISHED_AUTHOR_ORIGINAL_EXPERIMENT_JSON_OBSERVATIONAL_DESCRIPTIVE",
   "frozen_before_any_network_real_scores":STUDY_PROTOCOL,
   "original_authors":"Hirokazu Shirado and Nicholas A. Christakis",
   "doi":"10.17632/t963ktp6ft.1",
   "original_source":{"dataset_version":1,
       "publisher_file_count":70,"original_JSON_network_files":64,
       "publisher_file_sha256_all_64_strict":True,
       "verified_networks":64,
       "original_human_participant_network_slots":64*HUMANS_PER_NETWORK,
       "human_action_rounds_possible":64*HUMANS_PER_NETWORK*BEHAVIOR_ROUNDS,
       "original_behavior_rounds":64*BEHAVIOR_ROUNDS,
       "original_network_snapshots":64*NETWORK_SNAPSHOTS,
       "original_experimental_treatments":dict(sorted(tr.items())),
       "human_bot_classification":"strict bool players.is_bot from each original json",
       "all_network_edges_source_target_valid_and_simple":True,
       "all_raw_original_human_rows_exported":False},
   "main_outcome":"human C/(human observed C or D) per network per round; bots never contribute to human numerator or denominator",
   "network_topology":"undirected original node and edge snapshots, HH/HB/BB by strict original is_bot",
   "treatment_equal_network_aggregate":{t:summarize(v) for t,v in sorted(metrics_by_treat.items())},
   "all_64_networks_equal_weight_aggregate":summarize(combined),
   "noncausal_research_note":"Published in 2020; no new randomized assignment identification; short 30-round behavioral and edge descriptions, not institutional or historic causal effect.",
   "causal_human_social_effect":"NOT_IDENTIFIED",
   "robot_intervention_causal_effect":"NOT_IDENTIFIED",
   "PESEN_v0.1":"FROZEN"}

def evaluate_official_all64():
 b,_=get(BASE)
 md=json.loads(b)
 metadata_overview(md)
 files=md.get("files",[])
 original_JSON=[f for f in files if isinstance(f,dict) and str(f.get("filename","")).lower().endswith(".json")]
 if len(original_JSON)!=NETWORK_COUNT:
  raise ValueError("R080_ORIGINAL_SOURCE_JSON_64_COUNT_MISMATCH")
 records=[];sha_list=[]
 # All 64 official source files must be byte checked or the final result fails.
 for f in original_JSON:
  c=f.get("content_details") or {}
  url=c.get("download_url")
  size=int(f.get("size") or 0)
  sourcehash=c.get("sha256_hash")
  if not safe_official_download_url(url) or size<1 or size>MAX_ITEM or not isinstance(sourcehash,str) or not SHA256_RE.fullmatch(sourcehash):
   raise ValueError("R080_ORIGINAL_PUBLISHER_JSON_FILE_METADATA_SHA_MISSING")
  raw,_=get(url,min(MAX_ITEM,size+4096))
  if len(raw)!=size or hashlib.sha256(raw).hexdigest()!=sourcehash.lower():
   raise ValueError("R080_ONE_OR_MORE_REAL_ORIGINAL_JSON_SOURCE_SHA_MISMATCH")
  try:records.append(json.loads(raw))
  except (ValueError,UnicodeError):
   raise ValueError("R080_ORIGINAL_NETWORK_JSON_BYTES_INVALID")
  sha_list.append(sourcehash.lower())
 report=aggregate_all_64_source_files(md,records)
 report["original_source"]["aggregate_original_64_file_SHA256_set_fingerprint"]=hashlib.sha256(
  "\n".join(sorted(sha_list)).encode()).hexdigest()
 report["original_source"]["all_original_64_file_content_SHA256_verified"]=True
 return report

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args()
 try:report=evaluate_official_all64()
 except (ValueError,OSError,URLError,HTTPError,UnicodeError) as e:
  report={"research_id":"R080","status":"R080_FULL_ORIGINAL_HUMAN_NETWORK_SOURCE_OR_STRUCTURE_FAIL_CLOSED",
   "failure_class":type(e).__name__,
   "failure_reason":str(e)[:110] if isinstance(e,ValueError) else "SOURCE_IO_ERROR",
   "true_human_network_scores_exported":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
 print(json.dumps({
  "status":report["status"],"failure_reason":report.get("failure_reason"),
  "original_source":report.get("original_source"),
  "all_64_networks":report.get("all_64_networks_equal_weight_aggregate"),
  "per_treatment":report.get("treatment_equal_network_aggregate"),
  "human_id_and_network_edge_lists_exported":False,
 },sort_keys=True))
 if report["status"]!="R080_FIRST_PARTY_AUTHOR_64_NETWORK_HUMAN_ONLY_TOPOLOGY_E2_EXECUTED":
  raise RuntimeError("R080_64_NETWORK_ORIGINAL_SOURCE_STRICT_FAIL_CLOSED")
if __name__=="__main__":main()
