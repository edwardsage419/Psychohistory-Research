#!/usr/bin/env python3
"""R069: original SNAP Higgs timestamped interaction + aggregate RT source audit.

No opinion contagion, knowledge adoption, or failed exposure inferred.
IDs never leave process: only aggregate statistics and source SHA in output.
"""
from __future__ import annotations
import argparse
from collections import Counter
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
import urllib.error
import urllib.request
from pathlib import Path

FILES={
    "activity":"https://snap.stanford.edu/data/higgs-activity_time.txt.gz",
    "retweet_network":"https://snap.stanford.edu/data/higgs-retweet_network.edgelist.gz",
}
MAX_COMPRESSED=80_000_000
MAX_ACTIVITY_ROWS=5_000_000
MAX_NETWORK_ROWS=2_000_000
MAX_LINE=220
START=1341100800  # 2012-07-01 00:00 UTC
END=1341705600    # 2012-07-08 00:00 UTC
TYPES=("RT","MT","RE")


def download(name):
    req=urllib.request.Request(FILES[name],headers={"User-Agent":"Psychohistory-R069-SNAP-Higgs-source-fingerprint/1.0"})
    with urllib.request.urlopen(req,timeout=35) as response:
        payload=response.read(MAX_COMPRESSED+1)
    if len(payload)>MAX_COMPRESSED:
        raise ValueError("ORIGINAL_GZIP_EXCEEDS_BUDGET")
    return payload


def original_gzip_lines(raw,limit):
    if not raw.startswith(b"\x1f\x8b"):
        raise ValueError("ORIGINAL_SOURCE_NOT_GZIP")
    with gzip.GzipFile(fileobj=io.BytesIO(raw),mode="rb") as g:
        nonempty=0
        while True:
            line=g.readline(MAX_LINE+1)
            if not line:break
            if len(line)>MAX_LINE:
                raise ValueError("EXPANDED_GZIP_ROW_TOO_LONG")
            try:
                text=line.decode("utf-8").strip()
            except UnicodeError:
                raise ValueError("SOURCE_NOT_UTF8") from None
            if not text or text.startswith("#"):
                continue
            nonempty+=1
            if nonempty>limit:
                raise ValueError("ORIGINAL_SOURCE_ROW_BUDGET")
            yield text.split()


def require_unsigned_id(val):
    try:
        z=int(val)
    except (ValueError,TypeError):
        raise ValueError("SOURCE_USER_ID_NOT_INTEGER") from None
    if z<0 or z>2**63-1:
        raise ValueError("SOURCE_USER_ID_OUTSIDE_UNSIGNED_RANGE")
    return z


def require_timestamp(val):
    try:
        z=int(val)
    except ValueError:
        raise ValueError("SOURCE_TIMESTAMP_NOT_INTEGER") from None
    if z<=0 or z>2**40:
        raise ValueError("SOURCE_TIME_OUTSIDE_POSSIBLE_EPOCH_SECONDS")
    return z


def audit_activity(raw):
    actors=set()
    targets=set()
    any_first={}
    rt_first={}
    events=Counter()
    seconds=Counter()
    self_event=0
    out_of_week=0
    rt_records=[]
    earliest=None
    latest=None
    for row in original_gzip_lines(raw,MAX_ACTIVITY_ROWS):
        if len(row)!=4:
            raise ValueError("ACTIVITY_NOT_FOUR_FIELDS")
        a,b,t,action=row
        a,b=require_unsigned_id(a),require_unsigned_id(b)
        tm=require_timestamp(t)
        if action not in TYPES:
            raise ValueError("UNKNOWN_INTERACTION_TYPE")
        events[action]+=1
        actors.add(a);targets.add(b)
        seconds[tm]+=1
        if a==b:self_event+=1
        if not START<=tm<END:out_of_week+=1
        earliest=tm if earliest is None else min(earliest,tm)
        latest=tm if latest is None else max(latest,tm)
        if a not in any_first or tm<any_first[a]:
            any_first[a]=tm
        if action=="RT":
            rt_records.append((a,b,tm))
            if a not in rt_first or tm<rt_first[a]:
                rt_first[a]=tm
    if not events or events["RT"]==0:
        raise ValueError("NO_SOURCE_RETWEETS")
    before_any=0
    before_rt=0
    first_actor_rt_records=0
    first_actor_before_any=0
    first_actor_before_rt=0
    for a,b,t in rt_records:
        p_any=(b in any_first and any_first[b]<t)
        p_rt=(b in rt_first and rt_first[b]<t)
        before_any+=int(p_any)
        before_rt+=int(p_rt)
        if rt_first[a]==t:
            first_actor_rt_records+=1
            first_actor_before_any+=int(p_any)
            first_actor_before_rt+=int(p_rt)
    return {
        "interaction_rows":sum(events.values()),
        "activity_types":{z:events[z] for z in TYPES},
        "distinct_active_users":len(actors),
        "distinct_target_users":len(targets),
        "actor_target_union_nodes":len(actors|targets),
        "earliest_interaction_UTC":datetime.fromtimestamp(earliest,timezone.utc).isoformat(),
        "latest_interaction_UTC":datetime.fromtimestamp(latest,timezone.utc).isoformat(),
        "rows_outside_official_2012_07_01_to_07_07_week":out_of_week,
        "self_interaction_rows":self_event,
        "same_second_excess_event_rows":sum(z-1 for z in seconds.values() if z>1),
        "distinct_event_seconds":len(seconds),
        "distinct_users_with_observed_RT":len(rt_first),
        "RT_event_rows_with_target_prior_any_activity":before_any,
        "RT_event_rows_with_target_prior_RT":before_rt,
        "RT_event_rows_at_actor_first_observed_RT_timestamp":first_actor_rt_records,
        "first_observed_RT_timestamp_rows_with_target_prior_any_activity":first_actor_before_any,
        "first_observed_RT_timestamp_rows_with_target_prior_RT":first_actor_before_rt,
        "row_semantics":"A RT B at t is a directed observable action; earlier B activity not guaranteed to be original exposure or tweet ancestry",
        "original_user_ids_redistributed":False,
    }


def audit_aggregated_retweet_graph(raw):
    counts=Counter()
    nodes=set()
    edges=set()
    positive_weight_sum=0
    loops=0
    for row in original_gzip_lines(raw,MAX_NETWORK_ROWS):
        if len(row)!=3:
            raise ValueError("AGGREGATED_RT_GRAPH_NOT_THREE_COLUMNS")
        a,b=require_unsigned_id(row[0]),require_unsigned_id(row[1])
        try:w=int(row[2])
        except ValueError:raise ValueError("RT_NETWORK_WEIGHT_NOT_INTEGER") from None
        if w<=0:
            raise ValueError("RT_NETWORK_NONPOSITIVE_WEIGHT")
        counts["rows"]+=1
        nodes.add(a);nodes.add(b)
        if a==b:loops+=1
        if (a,b) in edges:
            counts["duplicate_directed_edge_rows"]+=1
        edges.add((a,b))
        positive_weight_sum+=w
    if not counts["rows"]:
        raise ValueError("AGGREGATED_NETWORK_EMPTY")
    return {
        "retweet_network_edge_rows":counts["rows"],
        "unique_directed_weighted_edge_pairs":len(edges),
        "duplicate_directed_edge_rows":counts["duplicate_directed_edge_rows"],
        "retweet_network_distinct_nodes":len(nodes),
        "weight_sum":positive_weight_sum,
        "self_loop_rows":loops,
        "is_derived_from_same_activity_not_preexisting_exposure_network":True,
        "no_raw_edges_redistributed":True,
    }


def audit(sources):
    if set(sources)!=set(FILES):
        raise ValueError("EXACT_TWO_ORIGINAL_SNAP_FILES_REQUIRED")
    fingerprints={key:{"official_url":FILES[key],"gzip_bytes":len(raw),
                       "sha256":hashlib.sha256(raw).hexdigest()}
                  for key,raw in sources.items()}
    activity=audit_activity(sources["activity"])
    network=audit_aggregated_retweet_graph(sources["retweet_network"])
    return {
        "research":"R069",
        "stage":"E2_SNAP_HIGGS_ACTIVITY_AND_DERIVED_RT_NETWORK",
        "status":"ORIGINAL_SNAP_TIMED_ACTION_SOURCE_PASS_BOUNDED",
        "protocol":"protocols/R069_E2_HIGGS_TEMPORAL_RETWEET_SOURCE_GATE_2026-10-16.md",
        "official_dataset":"SNAP Higgs Twitter Dataset (version posted March 31, 2015)",
        "original_gzip_fingerprints":fingerprints,
        "timed_interaction_evidence":activity,
        "retweet_aggregate_evidence":network,
        "retweet_direction":"RT actor A retweets B, not information transmission A to B",
        "external_follow_network_loaded":False,
        "exact_tweet_lineage_available":False,
        "failed_exposure_opportunities_available":False,
        "real_causal_threshold_or_IC_parameters":"NOT_IDENTIFIED",
        "true_information_belief_or_technology_adoption":"NOT_OBSERVED",
        "e3_new_population":"OPEN",
        "user_level_data_exported":False,
        "pesen_v01":"FROZEN",
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    try:
        result=audit({name:download(name) for name in FILES})
    except (ValueError,OSError,EOFError,UnicodeError,gzip.BadGzipFile,urllib.error.URLError) as exc:
        result={
            "research":"R069","stage":"E2_SNAP_HIGGS_ACTIVITY_AND_DERIVED_RT_NETWORK",
            "status":"SOURCE_UNRESOLVED",
            "error_type":type(exc).__name__,
            "error_code":str(exc)[:120] if isinstance(exc,ValueError) else "DOWNLOAD_OR_GZIP_READ_FAILED",
            "real_causal_threshold_or_IC_parameters":"NOT_IDENTIFIED",
            "pesen_v01":"FROZEN"}
    a.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":result["status"],
        "source_fingerprints":result.get("original_gzip_fingerprints"),
        "temporal_counts":result.get("timed_interaction_evidence"),
        "aggregate_RT_network":result.get("retweet_aggregate_evidence"),
        "error":result.get("error_code")},sort_keys=True))
    if result["status"]!="ORIGINAL_SNAP_TIMED_ACTION_SOURCE_PASS_BOUNDED":
        raise RuntimeError("Real SNAP Higgs source audit did not establish original-data integrity")


if __name__=="__main__":
    main()
