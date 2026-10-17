#!/usr/bin/env python3
"""R082 first-party 64-network human observability patterns and graph degree audit."""
from __future__ import annotations
import argparse,hashlib,json,pathlib
from collections import Counter,defaultdict

SOURCE_FINGERPRINT="555e2127ac21f4532c33a2e0a08f2e081b5f970891bd772c9bac3155d1d53571"
PROTOCOL="protocols/R082_ORIGINAL64_HUMAN_NONRESPONSE_GRAPH_ISOLATION_AND_ALLOCATION_SOURCE_FREEZE_2026-10-17.md"
R080_DELTA=-0.11073225819319567
ARMS=("no_bots","allc_bots","tft_bots","random_mgmt_bots","engaged_mgmt_bots",
      "disengaged_mgmt_bots","disengaged_mgmt_visible_bots","single_mgmt_bot")
CATS=("full30_observed","never_observed","leading_only_missing",
      "trailing_only_missing","both_ends_missing_contiguous_middle","interior_gap_with_return")
ALIGN=("snapshot_before_index","snapshot_after_index")
EXPOSURES=("no_any_neighbor","no_human_neighbor")

def classify(seq):
 if len(seq)!=30 or any(type(x) is not bool for x in seq):
  raise ValueError("R082_OBSERVATION_VECTOR_NOT_30_BOOLS")
 if all(seq):return CATS[0]
 if not any(seq):return CATS[1]
 first=seq.index(True);last=max(i for i,x in enumerate(seq) if x)
 if not all(seq[first:last+1]):return CATS[5]
 if first>0 and last<29:return CATS[4]
 if first>0:return CATS[2]
 if last<29:return CATS[3]
 raise ValueError("R082_PATTERN_NOT_EXHAUSTIVE")

def one_original_doc(doc):
 """Caller must have validated every original graph with R080 before true scores."""
 types={v["player"]:v["is_bot"] for v in doc["players"]}
 human={p for p,bot in types.items() if bot is False}
 bots=set(types)-human
 if len(human)!=16 or len(doc["result_behaviors"])!=30 or len(doc["result_networks"])!=31:
  raise ValueError("R082_HUMAN_ROSTER_OR_ROUND_COUNT_INVALID")
 if doc["treatment"] not in ARMS:raise ValueError("R082_ARM_OUTSIDE_ORIGINAL_8")
 events={p:[False]*30 for p in human}
 for t,b in enumerate(doc["result_behaviors"]):
  seen=set()
  for a in b["cooperation"]:
   p=a["player"]
   if p not in types or p in seen or a["action"] not in ("C","D"):
    raise ValueError("R082_DUPLICATE_UNKNOWN_OR_NON_CD_ACTION")
   seen.add(p)
   if p in human:events[p][t]=True
 cats=Counter(classify(v) for v in events.values())
 missing=sum(v.count(False) for v in events.values())
 trailing_only=sum(v.count(False) for v in events.values() if classify(v)==CATS[3])
 suffix=sum(30-1-max(i for i,b in enumerate(v) if b) for v in events.values() if any(v))
 graph={a:{e:Counter() for e in EXPOSURES} for a in ALIGN}
 bot_HB_hist=Counter();bot_deg_hist=Counter();bot_anomalies=0
 for snapshot_index,s in enumerate(doc["result_networks"]):
  hh=Counter();hb=Counter();degree_bot=Counter();num_HB=0
  for edge in s["network"]["links"]:
   a,b=edge["source"],edge["target"]
   if a in human and b in human:
    hh[a]+=1;hh[b]+=1
   elif a in human and b in bots:
    hb[a]+=1;degree_bot[b]+=1;num_HB+=1
   elif b in human and a in bots:
    hb[b]+=1;degree_bot[a]+=1;num_HB+=1
  if doc["treatment"]=="single_mgmt_bot":
   if len(bots)!=5:raise ValueError("R082_SINGLE_MGMT_SOURCE_REQUIRES_FIVE_BOT_NODES")
   bot_HB_hist[num_HB]+=1
   for bot in bots:bot_deg_hist[degree_bot[bot]]+=1
   if num_HB!=5 or any(degree_bot[bot]!=1 for bot in bots):bot_anomalies+=1
  # snapshot index t maps to action t, index t+1 also maps to action t;
  # these two alignments are equally retained, never outcome-selected.
  for align,t in ((ALIGN[0],snapshot_index),(ALIGN[1],snapshot_index-1)):
   if not (0<=t<30):continue
   for p in human:
    outcome="observed" if events[p][t] else "missing"
    for exposure,zero in (("no_any_neighbor",hh[p]+hb[p]==0),
                          ("no_human_neighbor",hh[p]==0)):
     graph[align][exposure][("zero" if zero else "nonzero",outcome)]+=1
 if sum(cats.values())!=16:raise ValueError("R082_ACTOR_SEQUENCE_CLASS_UNIVERSE_FAILED")
 return {"arm":doc["treatment"],"cats":cats,"missing":missing,
   "trailing_only_missing_slots":trailing_only,"any_final_suffix_missing_slots":suffix,
   "graph":graph,"bot_HB_hist":bot_HB_hist,"bot_deg_hist":bot_deg_hist,"bot_anomalies":bot_anomalies}

def summarize(items):
 if not items:raise ValueError("R082_EMPTY_SOURCE_GROUP")
 n=len(items);missing=sum(z["missing"] for z in items)
 observed=n*480-missing
 classes=Counter();hb_hist=Counter();bot_degrees=Counter()
 grids={a:{e:Counter() for e in EXPOSURES} for a in ALIGN}
 for z in items:
  classes.update(z["cats"]);hb_hist.update(z["bot_HB_hist"]);bot_degrees.update(z["bot_deg_hist"])
  for a in ALIGN:
   for e in EXPOSURES:grids[a][e].update(z["graph"][a][e])
 if sum(classes.values())!=16*n:raise ValueError("R082_ACTOR_CLASS_TOTAL_MISMATCH")
 measures={}
 for a in ALIGN:
  measures[a]={}
  for exposure in EXPOSURES:
   cells=grids[a][exposure]
   zm,zo=cells[("zero","missing")],cells[("zero","observed")]
   nm,no=cells[("nonzero","missing")],cells[("nonzero","observed")]
   if zm+zo+nm+no != 480*n:raise ValueError("R082_EXPOSURE_TABLE_NOT_EXHAUSTIVE")
   rz=zm/(zm+zo) if zm+zo else None
   rn=nm/(nm+no) if nm+no else None
   measures[a][exposure]={
    "degree_zero_missing":zm,"degree_zero_observed":zo,
    "degree_nonzero_missing":nm,"degree_nonzero_observed":no,
    "missing_risk_degree_zero":rz,"missing_risk_degree_nonzero":rn,
    "risk_difference_zero_minus_nonzero":rz-rn if rz is not None and rn is not None else None,
    "causal":False}
 return {"original_networks":n,"human_slots":16*n,
  "possible_human_decision_slots":480*n,"observed_human_CD":observed,"missing_human_slots":missing,
  "six_disjoint_human_response_patterns":{k:classes[k] for k in CATS},
  "missing_slots_from_trailing_only_class":sum(z["trailing_only_missing_slots"] for z in items),
  "all_ever_observed_human_final_missing_suffix_slots":sum(z["any_final_suffix_missing_slots"] for z in items),
  "degree_missingness_associations_both_alignments":measures,
  "bot_marked_node_structure":{
   "snapshot_count":sum(hb_hist.values()),
   "HB_edge_count_histogram":{str(k):v for k,v in sorted(hb_hist.items())},
   "bot_node_HB_degree_histogram":{str(k):v for k,v in sorted(bot_degrees.items())},
   "five_tie_or_singleton_exception_snapshots":sum(z["bot_anomalies"] for z in items)
  } if hb_hist else None}

def audit_full64(docs):
 if len(docs)!=64 or len({d["game_id"] for d in docs})!=64:
  raise ValueError("R082_ALL64_DISTINCT_ORIGINAL_EXPERIMENT_NETWORKS_REQUIRED")
 grouped=defaultdict(list)
 for d in docs:grouped[d["treatment"]].append(one_original_doc(d))
 if set(grouped)!=set(ARMS) or any(len(grouped[k])!=8 for k in ARMS):
  raise ValueError("R082_EIGHT_ARMS_EIGHT_ORIGINAL_NETWORKS_EACH_REQUIRED")
 by_arm={arm:summarize(grouped[arm]) for arm in sorted(ARMS)}
 full=summarize([z for group in grouped.values() for z in group])
 if full["human_slots"]!=1024 or full["observed_human_CD"]!=27656:
  raise ValueError("R082_PRIOR_R081_TOTAL_OBSERVED_ACTIONS_SOURCE_PARITY_FAIL")
 if by_arm["single_mgmt_bot"]["bot_marked_node_structure"]["snapshot_count"]!=248:
  raise ValueError("R082_SINGLE_BOT_248_SNAPSHOTS_INCOMPLETE")
 return {"study":"R082","status":"R082_FULL64_SOURCE_VERIFIED_HUMAN_NONRESPONSE_GRAPH_ASSOCIATION_E2",
  "source":"Shirado-Christakis Mendeley Data v1 original network JSON",
  "protocol_before_R082_new_real_result":PROTOCOL,
  "R080_R081_results_previously_known":True,
  "source_fingerprint":SOURCE_FINGERPRINT,
  "original_publisher_SHA256_verified":64,
  "all64":full,"all_eight_author_treatments":by_arm,
  "source_design_main_article":{
   "Erdos_Renyi_initial_human_graph_randomized":True,
   "individual_rewiring_opportunity_randomized":True,
   "between_network_bot_treatment_randomization_independently_verified":False,
   "experiment2_single_logical_bot_strategy_chosen_after_experiment1_results":True},
  "single_logical_bot_vs_five_source_bot_nodes":"UNVERIFIED_IMPLEMENTATION_MAPPING",
  "original_action_nonresponse_reason":"UNKNOWN",
  "peer_effect_causal":"NOT_IDENTIFIED",
  "between_arm_robot_causal":"NOT_IDENTIFIED_BY_THIS_E2_AUDIT",
  "raw_actor_ids_or_edges_exported":False,"per_network_results_exported":False,
  "PESEN_v0.1":"FROZEN"}

def original_publisher_64():
 from r080_official_dataset_per_file_content_and_role_schema import (
  BASE,MAX_ITEM,SHA256_RE,get,metadata_overview,safe_official_download_url)
 from r080_original_64_networks_human_only_cooperation_topology import (
  parse_network_source,aggregate_all_64_source_files,exact_source_bytes_retry)
 metadata,_=get(BASE)
 md=json.loads(metadata)
 o=metadata_overview(md)
 if (o["original_file_count"]!=70 or
     o["file_extensions"]!={"csv":3,"json":64,"r":3} or
     o["sha256_published_in_file_content_details_count"]!=70):
  raise ValueError("R082_70_AUTHOR_FILES_OR_MANIFEST_CHANGED")
 files=[x for x in md["files"] if x["filename"].lower().endswith(".json")]
 if len(files)!=64:raise ValueError("R082_64_AUTHOR_JSON_SOURCE_FILES_MISSING")
 shas=sorted((x.get("content_details") or {}).get("sha256_hash","").lower() for x in files)
 if any(not SHA256_RE.fullmatch(s) for s in shas):
  raise ValueError("R082_ORIGINAL_PUBLISHER_SHA256_MISSING")
 if hashlib.sha256("\n".join(shas).encode()).hexdigest()!=SOURCE_FINGERPRINT:
  raise ValueError("R082_FROZEN_AUTHOR_SOURCE_FINGERPRINT_MISMATCH")
 docs=[]
 for f in files:
  c=f.get("content_details") or {}
  size=int(f.get("size") or 0)
  url=c.get("download_url")
  if not safe_official_download_url(url) or not 0<size<=MAX_ITEM:
   raise ValueError("R082_AUTHOR_FILE_DOWNLOAD_SOURCE_UNTRUSTED")
  body=exact_source_bytes_retry(f,c["sha256_hash"],size,url)
  docs.append(json.loads(body))
 # All 64 original source and full graph eligibility checks precede any R082 scores.
 for d in docs:parse_network_source(d)
 old=aggregate_all_64_source_files(md,docs)
 if abs(old["all_64_networks_equal_weight_aggregate"]["human_coop_delta"]-R080_DELTA)>1e-12:
  raise ValueError("R082_R080_64_NETWORK_PRIOR_MEASURE_PARITY_FAIL")
 result=audit_full64(docs)
 result["source_parity_R080_original_all64_delta"]=R080_DELTA
 return result

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args()
 try:r=original_publisher_64()
 except (ValueError,OSError,UnicodeError,KeyError,TypeError) as e:
  r={"study":"R082","status":"R082_STRICT_SOURCE_OR_SCHEMA_FAIL_CLOSED",
     "error_type":type(e).__name__,
     "reason":str(e)[:120] if isinstance(e,ValueError) else "SOURCE_IO_OR_GRAMMAR_ERROR",
     "real_human_tables_exported":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 print(json.dumps({"status":r["status"],"full64_summary":r.get("all64"),
                   "source_fingerprint":r.get("source_fingerprint"),
                   "reason":r.get("reason")},sort_keys=True))
 if r["status"]!="R082_FULL64_SOURCE_VERIFIED_HUMAN_NONRESPONSE_GRAPH_ASSOCIATION_E2":
  raise RuntimeError("R082_HUMAN_NETWORK_SOURCE_FAIL_CLOSED")
if __name__=="__main__":main()
