#!/usr/bin/env python3
"""R069 HetRec source Rev-002: retain, count and exclude four invalid times only.

Published original ZIP SHA and MD5 are immutable; initial fail remains valid.
Counts friend-before-tag *proxies*, not causal exposure or true adoption.
"""
from __future__ import annotations
import argparse,csv,datetime as dt,hashlib,io,json
from collections import defaultdict
from pathlib import Path
from r069_hetrec_lastfm_source_audit import (
    SOURCE_URL,EXPECTED_MD5,fetch_source,safe_archive,
    parse_tab,proxy_early_friend_tag,
)

EXPECTED_SHA="6738f48195667ff03caaab4d32ca9a3133d8cc026b7c3cdaf6ce1010e913c59c"
EXPECTED_FRIEND_ROWS=25434
EXPECTED_TAG_ROWS=186479
EXPECTED_INVALID_TIMES=4


def tagged_valid_rows(raw, expected_all=EXPECTED_TAG_ROWS, expected_invalid=EXPECTED_INVALID_TIMES):
    rd=csv.reader(io.StringIO(raw.decode("utf-8-sig"),newline=""),delimiter="\t")
    try:header=next(rd)
    except StopIteration:raise ValueError("EMPTY_ORIGINAL_TAG_CSV") from None
    if header!=["userID","artistID","tagID","timestamp"]:
        raise ValueError("TAG_COLUMNS_CHANGED")
    valid=[];invalid=0;all_rows=0
    for row in rd:
        all_rows+=1
        if len(row)!=4:
            raise ValueError("TAG_ROW_SHAPE_INVALID")
        try:values=tuple(int(x.strip()) for x in row)
        except ValueError:
            raise ValueError("TAG_INTEGER_INVALID") from None
        if any(x<=0 for x in values[:3]):
            raise ValueError("TAG_PERSON_ARTIST_OR_TAG_ID_INVALID")
        t=values[3]
        if t==0:
            raise ValueError("ZERO_TIMESTAMP_NOT_AUTHORIZED")
        if t<0:
            invalid+=1
            continue
        valid.append(values)
    if all_rows!=expected_all or invalid!=expected_invalid:
        raise ValueError("TAG_SOURCE_COUNT_OR_INVALID_TIME_UNIVERSE_DRIFT")
    return valid,{"raw_tag_rows":all_rows,
                  "original_negative_timestamp_rows":invalid,
                  "timestamp_order_valid_rows":len(valid)}


def evaluate_zip(raw,checksum=EXPECTED_SHA,md5=EXPECTED_MD5,
                 expected_friend=EXPECTED_FRIEND_ROWS,
                 expected_tag=EXPECTED_TAG_ROWS,
                 invalid=EXPECTED_INVALID_TIMES):
    if hashlib.sha256(raw).hexdigest()!=checksum:
        raise ValueError("SOURCE_ZIP_SHA256_DRIFT")
    files=safe_archive(raw,expected_md5=md5)
    friends=parse_tab(files["user_friends.dat"],("userID","friendID"))
    tags,counts=tagged_valid_rows(files["user_taggedartists-timestamps.dat"],
                                   expected_all=expected_tag,expected_invalid=invalid)
    if len(friends)!=expected_friend:
        raise ValueError("FRIEND_SOURCE_ROW_UNIVERSE_DRIFT")
    if any(a==b for a,b in friends) or len(set(friends))!=len(friends):
        raise ValueError("FRIEND_DUPLICATES_OR_SELF_LOOPS")
    graph=set(friends)
    if any((b,a) not in graph for a,b in graph):
        raise ValueError("FRIENDS_ARE_NOT_RECIPROCAL")
    neighbors=defaultdict(set)
    for a,b in graph:
        neighbors[a].add(b)
    user_tagger={row[0] for row in tags}
    graph_users=set(neighbors)
    proxy=proxy_early_friend_tag(tags,neighbors)
    timestamp_min=min(row[3] for row in tags)
    timestamp_max=max(row[3] for row in tags)
    utc=lambda t:dt.datetime.fromtimestamp(t/1000,dt.timezone.utc).date().isoformat()
    return {
        "research":"R069",
        "stage":"E2_HETREC_ORIGINAL_SOURCE_REV002",
        "status":"E2_SOURCE_AND_RETROSPECTIVE_EXPOSURE_PROXY_PASS_BOUNDED",
        "protocol":"protocols/R069_E2_HETREC_TIMESTAMP_SENTINEL_REV2_2026-10-16.md",
        "original_archive":{
            "publication":"GroupLens / UAM HetRec 2011 Last.fm 2K",
            "url":SOURCE_URL,
            "raw_zip_sha256":checksum,
            "raw_zip_md5":md5,
            "raw_zip_bytes":len(raw),
            "license_boundary":"non-commercial research use only; no raw source republished"},
        "network":{
            "directed_friend_listing_rows":len(friends),
            "unique_undirected_reciprocal_friend_pairs":len(graph)//2,
            "distinct_network_users":len(graph_users),
            "network_tie_formation_times":"NOT_OBSERVED"},
        "user_tag_events":{
            **counts,
            "distinct_tagged_user_ids":len(user_tagger),
            "distinct_artist_ids":len({row[1] for row in tags}),
            "distinct_tag_codes":len({row[2] for row in tags}),
            "source_tag_time_earliest_UTC":utc(timestamp_min),
            "source_tag_time_latest_UTC":utc(timestamp_max),
            "tagged_users_with_friend_graph_node":len(user_tagger&graph_users),
            **proxy},
        "initial_fail_workflow":38874370089,
        "diagnostic_workflow":38874509818,
        "true_initial_adoption_time":"UNOBSERVED_LISTENING_TIME_NOT_IN_TAG_RECORD",
        "prior_exposure_to_friend_tag":"NOT_PROVEN_UNTIMESTAMPED_FRIEND_EDGES",
        "true_independent_cascade_or_threshold_inference":"NOT_ESTABLISHED",
        "individual_source_events_or_ids_exported":False,
        "pesen_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    try:
        result=evaluate_zip(fetch_source())
    except (ValueError,OSError,UnicodeError,OverflowError) as exc:
        result={"research":"R069",
                "stage":"E2_HETREC_ORIGINAL_SOURCE_REV002",
                "status":"SOURCE_UNRESOLVED",
                "reason_type":type(exc).__name__,
                "reason":str(exc)[:90] if isinstance(exc,ValueError) else "SOURCE_IO_OR_TIMESTAMP_FAILURE",
                "pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":result["status"],
                      "network":result.get("network"),
                      "tags":result.get("user_tag_events"),
                      "source":result.get("original_archive",{}).get("raw_zip_sha256")},sort_keys=True))
    if result["status"]!="E2_SOURCE_AND_RETROSPECTIVE_EXPOSURE_PROXY_PASS_BOUNDED":
        raise RuntimeError("Rev-002 real source and temporal proxy did not pass")


if __name__=="__main__":
    main()
