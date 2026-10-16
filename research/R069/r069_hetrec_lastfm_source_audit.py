#!/usr/bin/env python3
"""R069: byte-pinned non-commercial HetRec Last.fm source and historical proxy.

Not a propagation model; graph ties are a snapshot, not timestamped exposure.
No user/artist/tag IDs or individual event sequences may be serialized.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import io
import json
import os
from collections import Counter, defaultdict
from itertools import groupby
from pathlib import Path
from urllib import error, request
import zipfile

SOURCE_URL="https://files.grouplens.org/datasets/hetrec2011/hetrec2011-lastfm-2k.zip"
EXPECTED_MD5="296d61afe4e8632b173fc2dd3be20ce2"
MAX_ZIP=15_000_000
MAX_MEMBER=30_000_000
MAX_TOTAL=60_000_000
REQUIRED=("readme.txt","user_friends.dat","user_taggedartists-timestamps.dat")
EXPECTED_COUNTS={"friends":25434,"tag_events":186479}


def fetch_source():
    req=request.Request(SOURCE_URL,headers={"User-Agent":"Psychohistory-R069-HetRec-noncommercial-source-audit/1.0"})
    with request.urlopen(req,timeout=35) as resp:
        raw=resp.read(MAX_ZIP+1)
    if len(raw)>MAX_ZIP:
        raise ValueError("ZIP_TOO_LARGE")
    return raw


def safe_archive(raw,expected_md5=EXPECTED_MD5):
    if hashlib.md5(raw).hexdigest()!=expected_md5:
        raise ValueError("ZIP_MD5_MISMATCH")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        members=z.infolist()
        if len(members)>20 or sum(m.file_size for m in members)>MAX_TOTAL:
            raise ValueError("ZIP_UNPACK_BUDGET_EXCEEDED")
        found={}
        for entry in members:
            path=entry.filename
            if (path.startswith("/") or "\\" in path or
                ".." in path.split("/") or entry.file_size>MAX_MEMBER):
                raise ValueError("ZIP_MEMBER_PATH_OR_SIZE_UNSAFE")
            if entry.is_dir():
                continue
            basename=path.rsplit("/",1)[-1].lower()
            if basename in REQUIRED:
                if basename in found:
                    raise ValueError("ZIP_DUPLICATE_REQUIRED_MEMBER")
                found[basename]=z.read(entry)
        if set(found)!=set(REQUIRED):
            raise ValueError("ZIP_REQUIRED_FILES_MISSING")
    return found


def parse_tab(raw,expected_header):
    with io.StringIO(raw.decode("utf-8-sig"),newline="") as source:
        reader=csv.reader(source,delimiter="\t")
        try:
            header=next(reader)
        except StopIteration:
            raise ValueError("SOURCE_EMPTY_TSV") from None
        if header!=list(expected_header):
            raise ValueError("SOURCE_UNEXPECTED_COLUMNS")
        rows=[]
        for idx,line in enumerate(reader,1):
            if idx>300000 or len(line)!=len(expected_header):
                raise ValueError("SOURCE_TSV_SHAPE_OR_ROW_BUDGET")
            try:
                values=tuple(int(x.strip()) for x in line)
            except ValueError:
                raise ValueError("SOURCE_FIELD_NOT_INTEGER") from None
            if any(x<=0 for x in values):
                raise ValueError("SOURCE_NONPOSITIVE_IDENTIFIERS_OR_TIMESTAMP")
            rows.append(values)
    return rows


def proxy_early_friend_tag(events,neighbors):
    """First observed tag per user-artist, using strictly prior OTHER user tags.

    All observations with the exact same timestamp are evaluated BEFORE any of
    them update the peer adopter set. Thus row order and ties cannot leak.
    """
    first={}
    duplicate_user_artist_events=0
    for user,artist,tag,timestamp in events:
        key=(artist,user)
        if key in first:
            duplicate_user_artist_events+=1
            if timestamp<first[key]:
                first[key]=timestamp
        else:
            first[key]=timestamp
    by_artist=defaultdict(list)
    for (artist,user),timestamp in first.items():
        by_artist[artist].append((timestamp,user))
    proxy_positive=0
    eligible_with_friends=0
    for tuples in by_artist.values():
        already=set()
        for t,same_time in groupby(sorted(tuples),key=lambda tup:tup[0]):
            users=[user for _,user in same_time]
            for user in users:
                friend_ids=neighbors.get(user,set())
                if friend_ids:
                    eligible_with_friends+=1
                if any(friend in already for friend in friend_ids):
                    proxy_positive+=1
            already.update(users)
    return {
        "unique_first_tag_user_artist_pairs":len(first),
        "tag_events_after_first_same_artist_repetition":duplicate_user_artist_events,
        "first_tag_pairs_with_at_least_one_recorded_friend":eligible_with_friends,
        "first_tag_pairs_with_strictly_earlier_friend_tag_same_artist":proxy_positive,
        "first_tag_pairs_without_earlier_friend_tag_same_artist":len(first)-proxy_positive,
        "proxy_semantics":"a friend in undated friend snapshot tagged same artist strictly before first observed user tag; NOT observed exposure or adoption",
    }


def audit_raw_zip(raw,md5=EXPECTED_MD5,expected_counts=EXPECTED_COUNTS):
    files=safe_archive(raw,expected_md5=md5)
    friends=parse_tab(files["user_friends.dat"],("userID","friendID"))
    tags=parse_tab(files["user_taggedartists-timestamps.dat"],
                   ("userID","artistID","tagID","timestamp"))
    if len(friends)!=expected_counts["friends"] or len(tags)!=expected_counts["tag_events"]:
        raise ValueError("SOURCE_BASELINE_ROW_UNIVERSE_DRIFT")
    graph=set(friends)
    if any(a==b for a,b in friends):
        raise ValueError("SOURCE_GRAPH_SELF_LOOP")
    users={u for e in graph for u in e}
    reciprocal=sum((b,a) in graph for a,b in graph)
    if len(graph)!=len(friends):
        raise ValueError("SOURCE_DUPLICATE_FRIEND_EDGE")
    neighbors=defaultdict(set)
    for a,b in graph:
        neighbors[a].add(b)
    # Original documentation expects every tie listed both ways.
    if reciprocal!=len(graph):
        raise ValueError("SOURCE_FRIEND_GRAPH_NOT_RECIPROCAL")
    tag_users={x[0] for x in tags}
    artists={x[1] for x in tags}
    tag_ids={x[2] for x in tags}
    times=[v[3] for v in tags]
    days=[]
    for t in (min(times),max(times)):
        try:
            days.append(dt.datetime.fromtimestamp(t/1000,dt.timezone.utc).strftime("%Y-%m-%d"))
        except (OverflowError,OSError,ValueError):
            raise ValueError("TIMESTAMP_OUTSIDE_UNIX_MILLISECONDS") from None
    precedents=proxy_early_friend_tag(tags,neighbors)
    return {
        "stage":"R069_E2_REAL_HETREC_LASTFM_NETWORK_TAG_SOURCE",
        "status":"E2_SOURCE_AND_RETROSPECTIVE_EXPOSURE_PROXY_PASS",
        "source_url":SOURCE_URL,
        "source_md5":hashlib.md5(raw).hexdigest(),
        "source_sha256":hashlib.sha256(raw).hexdigest(),
        "source_zip_bytes":len(raw),
        "publication":"HetRec 2011 / Universidad Autónoma de Madrid / GroupLens",
        "license_boundary":"NONCOMMERCIAL_USE_ONLY; no source data redistribution",
        "source_tables":{
            "user_friends.dat":{
                "rows_directed_listing":len(friends),
                "reciprocal_pairs_undirected":len(graph)//2,
                "distinct_graph_users":len(users),
                "all_directed_edges_have_reverse":reciprocal==len(graph)},
            "user_taggedartists-timestamps.dat":{
                "raw_tag_events":len(tags),
                "distinct_tagging_users":len(tag_users),
                "distinct_artist_ids":len(artists),
                "distinct_tag_ids":len(tag_ids),
                "earliest_tag_UTC_day":days[0],
                "latest_tag_UTC_day":days[1],
                "tagging_users_present_in_friend_graph":len(tag_users & users),
                **precedents}},
        "four_identification_limits":{
            "network_tie_formation_dates":"NOT_OBSERVED",
            "artist_listening_or_true_adoption_times":"NOT_OBSERVED",
            "peer_exposure_or_IC_single_attempt":"NOT_OBSERVED",
            "risk_set_including_never_taggers":"NOT_RECOVERED"},
        "causal_threshold_or_IC_fit_performed":False,
        "individual_records_redistributed":False,
        "pesen_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    try:
        report=audit_raw_zip(fetch_source())
    except (ValueError,OSError,UnicodeError,zipfile.BadZipFile,error.URLError) as exc:
        report={
            "stage":"R069_E2_REAL_HETREC_LASTFM_NETWORK_TAG_SOURCE",
            "status":"SOURCE_UNRESOLVED",
            "reason_type":type(exc).__name__,
            "reason_code":str(exc)[:90] if isinstance(exc,ValueError) else "SOURCE_FETCH_OR_UNPACK_BLOCKER",
            "source_data_verified":False,
            "pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "status":report["status"],
        "source_sha256":report.get("source_sha256"),
        "network_tag_totals":report.get("source_tables",{}),
        "blocker":report.get("reason_code")},sort_keys=True))
    if report["status"]!="E2_SOURCE_AND_RETROSPECTIVE_EXPOSURE_PROXY_PASS":
        raise RuntimeError("public Last.fm real source evidence not established")


if __name__=="__main__":
    main()
