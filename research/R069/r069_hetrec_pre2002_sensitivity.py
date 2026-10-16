#!/usr/bin/env python3
"""R069: preregistered date plausibility sensitivity, not causal diffusion.

Original 1979 positive millisecond timestamp impossible as a Last.fm tag
created on that site (launched 2002); preserves all source anomaly categories.
"""
from __future__ import annotations
import argparse,hashlib,json
from collections import defaultdict
from pathlib import Path
from r069_hetrec_lastfm_source_audit import (
    fetch_source,safe_archive,parse_tab,proxy_early_friend_tag,EXPECTED_MD5,
)
from r069_hetrec_source_rev002 import (
    tagged_valid_rows,evaluate_zip,EXPECTED_SHA,
)

CUTOFF_UTC_MILLISECONDS=1009843200000  # 2002-01-01 00:00 UTC
PRESENTATION_DATE="2002-01-01"


def sensitivity(valid,neighbors,cutoff=CUTOFF_UTC_MILLISECONDS):
    if not isinstance(cutoff,int) or cutoff<=0:
        raise ValueError("invalid conservative 2002 cutoff")
    before=[v for v in valid if v[3]<cutoff]
    after=[v for v in valid if v[3]>=cutoff]
    originally_first={}
    for u,a,tag,t in valid:
        key=(u,a)
        if key not in originally_first or t<originally_first[key]:
            originally_first[key]=t
    base=proxy_early_friend_tag(valid,neighbors)
    revised=proxy_early_friend_tag(after,neighbors)
    return {
        "cutoff_UTC_day":PRESENTATION_DATE,
        "valid_positive_original_tag_event_rows":len(valid),
        "positive_timestamp_tag_event_rows_before_2002":len(before),
        "first_observed_user_artist_pairs_before_2002":sum(t<cutoff for t in originally_first.values()),
        "sensitivity_tag_event_rows_at_or_after_2002":len(after),
        "rev002_all_positive_source_proxy":{
            "first_user_artist_tag_pairs":base["unique_first_tag_user_artist_pairs"],
            "with_strictly_prior_snapshot_friend_tag":base["first_tag_pairs_with_strictly_earlier_friend_tag_same_artist"]},
        "exclusion_sensitivity_proxy":{
            "first_user_artist_tag_pairs":revised["unique_first_tag_user_artist_pairs"],
            "with_strictly_prior_snapshot_friend_tag":revised["first_tag_pairs_with_strictly_earlier_friend_tag_same_artist"]},
        "before_2002_exclusion_applied_to_original_source":False,
        "causal_adoption_or_exposure_result":"NONE",
    }


def evaluate_real(raw):
    # Require full previous source and network semantics before doing any
    # post-hoc historically plausible timestamp sensitivity.
    baseline=evaluate_zip(raw)
    if baseline["status"]!="E2_SOURCE_AND_RETROSPECTIVE_EXPOSURE_PROXY_PASS_BOUNDED":
        raise ValueError("original corrected source audit not passed")
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_SHA:
        raise ValueError("original ZIP pinned SHA mismatch")
    f=safe_archive(raw,EXPECTED_MD5)
    friends=parse_tab(f["user_friends.dat"],("userID","friendID"))
    valid,counts=tagged_valid_rows(f["user_taggedartists-timestamps.dat"])
    neighbors=defaultdict(set)
    for a,b in friends:
        neighbors[a].add(b)
    q=sensitivity(valid,neighbors)
    assert q["valid_positive_original_tag_event_rows"]==186475
    if (q["rev002_all_positive_source_proxy"]["first_user_artist_tag_pairs"]!=
          baseline["user_tag_events"]["unique_first_tag_user_artist_pairs"] or
        q["rev002_all_positive_source_proxy"]["with_strictly_prior_snapshot_friend_tag"]!=
          baseline["user_tag_events"]["first_tag_pairs_with_strictly_earlier_friend_tag_same_artist"]):
        raise ValueError("baseline Rev002 not reproduced")
    return {
        "research":"R069",
        "stage":"E2_HETREC_LASTFM_PRE2002_TEMPORAL_SENSITIVITY",
        "status":"SENSITIVITY_DESCRIPTIVE_COMPLETE",
        "protocol":"protocols/R069_E2_HETREC_PRE2002_DATE_SENSITIVITY_2026-10-16.md",
        "source_zip_sha256":EXPECTED_SHA,
        "source_zip_md5":EXPECTED_MD5,
        "original_negative_time_rows":counts["original_negative_timestamp_rows"],
        **q,
        "source_event_rows_exported":False,
        "network_edge_dates_observed":False,
        "real_diffusion_inference":"NOT_ESTABLISHED",
        "pesen_v01":"FROZEN",
    }


def main():
    a=argparse.ArgumentParser()
    a.add_argument("--output",type=Path,required=True)
    args=a.parse_args()
    try:
        outcome=evaluate_real(fetch_source())
    except (ValueError,OSError,UnicodeError,OverflowError) as e:
        outcome={"research":"R069","stage":"E2_HETREC_LASTFM_PRE2002_TEMPORAL_SENSITIVITY",
                 "status":"SOURCE_OR_SENSITIVITY_UNRESOLVED",
                 "reason_type":type(e).__name__,
                 "reason":str(e)[:95] if isinstance(e,ValueError) else "SOURCE_OR_TIME_ERROR",
                 "pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(outcome,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(outcome,sort_keys=True))
    if outcome["status"]!="SENSITIVITY_DESCRIPTIVE_COMPLETE":
        raise RuntimeError("real pre-2002 sensitivity did not complete")


if __name__=="__main__":main()
