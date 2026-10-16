#!/usr/bin/env python3
"""Exact RT event-to-weighted-graph directional multiset parity for SNAP Higgs.

Same underlying observations, NOT independent network diffusion evidence.
"""
from __future__ import annotations
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
from r069_higgs_temporal_source_audit import (
    download,original_gzip_lines,MAX_ACTIVITY_ROWS,MAX_NETWORK_ROWS,
    require_unsigned_id,require_timestamp,FILES,TYPES,
)

PINNED={
 "activity":(4169461,"901b199716a23b0fc0371705e3ae9941b5c9493277aec65456abc4988674ad79"),
 "retweet_network":(1957437,"4097edebd539043cfc62d9b4ba67676f79523f6dbe896d345fcc127dec3e936e"),
}


def check_source(name,data):
    count,sha=PINNED[name]
    if len(data)!=count or hashlib.sha256(data).hexdigest()!=sha:
        raise ValueError("OFFICIAL_HIGGS_SOURCE_SIZE_OR_SHA_MISMATCH")


def edge_multisets(activity,network):
    events=Counter()
    raw_RTs=0
    RT_self=0
    type_counts=Counter()
    for row in original_gzip_lines(activity,MAX_ACTIVITY_ROWS):
        if len(row)!=4:raise ValueError("ACTIVITY_FIELDS_DRIFT")
        a,b=require_unsigned_id(row[0]),require_unsigned_id(row[1])
        require_timestamp(row[2])
        kind=row[3]
        if kind not in TYPES:raise ValueError("ACTIVITY_KIND_INVALID")
        type_counts[kind]+=1
        if kind=="RT":
            events[(a,b)]+=1
            raw_RTs+=1
            RT_self+=int(a==b)
    derived={}
    aggregated_RT_rows=0
    duplicate_aggregate=0
    total_aggregated_weights=0
    for row in original_gzip_lines(network,MAX_NETWORK_ROWS):
        if len(row)!=3:raise ValueError("RT_GRAPH_ROW_SHAPE_CHANGED")
        a,b=require_unsigned_id(row[0]),require_unsigned_id(row[1])
        try:weight=int(row[2])
        except ValueError:raise ValueError("RT_GRAPH_WEIGHT_NOT_INTEGER") from None
        if weight<=0:raise ValueError("RT_GRAPH_WEIGHT_NOT_POSITIVE")
        pair=(a,b)
        if pair in derived:duplicate_aggregate+=1
        derived[pair]=weight
        aggregated_RT_rows+=1
        total_aggregated_weights+=weight
    source_keys=set(events)
    graph_keys=set(derived)
    same=source_keys&graph_keys
    only_source=source_keys-graph_keys
    only_agg=graph_keys-source_keys
    mismatched=sum(events[k]!=derived[k] for k in same)
    abs_error=sum(abs(events[k]-derived[k]) for k in same)
    reversed_graph={(b,a) for a,b in graph_keys}
    reverse_differences=len(source_keys-reversed_graph)+len(reversed_graph-source_keys)
    passed=(bool(events) and bool(derived) and
            not only_source and not only_agg and
            not mismatched and duplicate_aggregate==0 and
            raw_RTs==total_aggregated_weights)
    return {
        "status":"DIRECTIONAL_RT_MULTISET_EXACT_PASS" if passed else "RT_MULTISET_PARITY_MISMATCH",
        "activity_RTs":raw_RTs,
        "activity_MT_events_excluded":type_counts["MT"],
        "activity_RE_events_excluded":type_counts["RE"],
        "activity_unique_directed_RT_pairs":len(events),
        "activity_RT_self_events":RT_self,
        "aggregate_graph_rows":aggregated_RT_rows,
        "aggregate_graph_total_weight":total_aggregated_weights,
        "aggregate_duplicate_directed_edges":duplicate_aggregate,
        "unique_pairs_only_in_activity":len(only_source),
        "unique_pairs_only_in_aggregate":len(only_agg),
        "common_directed_pairs_weight_mismatches":mismatched,
        "sum_abs_common_pair_weight_differences":abs_error,
        "reversed_direction_symmetric_difference_pairs":reverse_differences,
        "parity_is_independent_second_human_dataset":False,
        "retweeted_item_lineage_reconstructed":False,
        "true_social_network_tie_formation_history_available":False,
        "individual_edge_rows_or_ids_exported":False,
    }


def evaluate(d):
    if set(d)!=set(PINNED):raise ValueError("EXACT_TWO_FILES_REQUIRED")
    for k in PINNED:check_source(k,d[k])
    probe=edge_multisets(d["activity"],d["retweet_network"])
    return {
        "research":"R069","stage":"E2_ORIGINAL_SNAP_HIGGS_EXACT_RT_EDGE_PARITY",
        "protocol":"protocols/R069_E2_HIGGS_ORIGINAL_RT_EXACT_PARITY_2026-10-16.md",
        "status":probe["status"],
        "source_sha256":{k:PINNED[k][1] for k in PINNED},
        "directional_edge_parity":probe,
        "causal_diffusion_model":"NOT_FITTED",
        "source_license":"NO_RIGHTS_ASSUMED_FOR_REPUBLICATION",
        "pesen_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    try:result=evaluate({name:download(name) for name in PINNED})
    except (ValueError,OSError,EOFError) as exc:
        result={"research":"R069","stage":"E2_ORIGINAL_SNAP_HIGGS_EXACT_RT_EDGE_PARITY",
                "status":"SOURCE_OR_GRAPH_UNRESOLVED",
                "reason_type":type(exc).__name__,
                "reason":str(exc)[:130] if isinstance(exc,ValueError) else "SOURCE_ACCESS_OR_DECODING",
                "pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],
                      "parity_counts":result.get("directional_edge_parity",{})},sort_keys=True))
    if result["status"]!="DIRECTIONAL_RT_MULTISET_EXACT_PASS":
        raise RuntimeError("SNAP Higgs RT graph was not exact edge-by-edge identical")


if __name__=="__main__":main()
