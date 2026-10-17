#!/usr/bin/env python3
"""R080 post-failed-gate source-only snapshot node universe differential.

Does not calculate any action or network behavior outcome. Inspects structural
key presence and node membership aggregated by original treatment only.
"""
from __future__ import annotations
import argparse,json,pathlib,hashlib
from collections import Counter,defaultdict
from r080_official_dataset_per_file_content_and_role_schema import (
 BASE,MAX_ITEM,SHA256_RE,get,metadata_overview,safe_official_download_url
)
def inspect64():
 raw,_=get(BASE)
 md=json.loads(raw)
 src=metadata_overview(md)
 entries=[f for f in md["files"] if f["filename"].lower().endswith(".json")]
 if len(entries)!=64 or src["sha256_published_in_file_content_details_count"]!=70:
  raise ValueError("R080_STRUCTURAL_DIAGNOSTIC_PUBLISHER_SOURCE_UNIVERSE_CHANGED")
 by_treat=defaultdict(Counter)
 sumfiles=0
 for f in entries:
  c=f["content_details"]
  url=c.get("download_url")
  sha=c.get("sha256_hash")
  size=int(f.get("size") or 0)
  if not safe_official_download_url(url) or not isinstance(sha,str) or not SHA256_RE.fullmatch(sha):
   raise ValueError("R080_STRUCTURAL_DIAGNOSTIC_OFFICIAL_SHA_MISSING")
  raw,_=get(url,min(MAX_ITEM,size+4096))
  if len(raw)!=size or hashlib.sha256(raw).hexdigest()!=sha.lower():
   raise ValueError("R080_STRUCTURAL_DIAGNOSTIC_SOURCE_SHA_DRIFT")
  j=json.loads(raw)
  actors={p["player"]:p["is_bot"] for p in j["players"]}
  if len(actors)!=len(j["players"]) or not all(type(x) is bool for x in actors.values()):
   raise ValueError("R080_STRUCTURAL_DIAGNOSTIC_ORIGINAL_ACTORS_INVALID")
  tr=j["treatment"];s=by_treat[tr];s["networks"]+=1;sumfiles+=1
  if len(j["result_networks"])!=31:s["wrong_network_snapshot_length"]+=1
  if len(j["result_behaviors"])!=30:s["wrong_behavior_round_length"]+=1
  s["human_node_slots"]+=sum(not x for x in actors.values())
  s["bot_node_slots"]+=sum(x for x in actors.values())
  network_any_missing=False;network_any_extra=False
  for k,snap in enumerate(j["result_networks"]):
   s["snapshots"]+=1
   net=snap["network"]
   ids=[n.get("id") for n in net["nodes"]]
   node_set=set(ids)
   missing=set(actors)-node_set
   extra=node_set-set(actors)
   s["nodes_absent_from_snapshot_total"]+=len(missing)
   s["humans_absent_from_snapshot_total"]+=sum(not actors[x] for x in missing)
   s["bots_absent_from_snapshot_total"]+=sum(actors[x] for x in missing)
   s["extra_unknown_nodes_total"]+=len(extra)
   if missing:s["snapshots_with_absent_actors"]+=1;network_any_missing=True
   if extra:s["snapshots_with_extra_actors"]+=1;network_any_extra=True
   if len(ids)!=len(node_set):s["snapshots_with_duplicate_node_ids"]+=1
   if net.get("directed") is not False:s["snapshots_marked_directed"]+=1
   if net.get("multigraph") is not False:s["snapshots_marked_multigraph"]+=1
   for link in net["links"]:
    a=link.get("source");b=link.get("target")
    if a not in actors or b not in actors:s["edges_ref_unknown_actor"]+=1
    if a not in node_set or b not in node_set:s["edges_ref_actor_not_declared_in_snapshot"]+=1
  if network_any_missing:s["networks_with_any_omitted_actor_node"]+=1
  if network_any_extra:s["networks_with_any_extra_node"]+=1
 return {
  "research_id":"R080",
  "phase":"POST_REV001_FAIL_PRE_ANY_REAL_NETWORK_OUTCOME_STRUCTURAL_SOURCE_DIAGNOSTIC",
  "source_version1_DOI":"10.17632/t963ktp6ft.1",
  "official_JSON_files_sha256_verified":sumfiles,
  "by_treatment_source_aggregate_node_universe_differences":{
    k:dict(sorted(v.items())) for k,v in sorted(by_treat.items())},
  "real_human_cooperation_outcome_scores":"NOT_RUN",
  "real_network_topology_change_scores":"NOT_RUN",
  "source_node_ids_or_edges_exported":False,
  "prior_initial_score_gate_failure":"R080_NETWORK_SNAPSHOT_NODES_NOT_EQUAL_REAL_ACTORS",
  "PESEN_v0.1":"FROZEN"
 }

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args();d=inspect64()
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(d,sort_keys=True,indent=2)+"\n")
 print(json.dumps(d,sort_keys=True))
if __name__=="__main__":main()
