#!/usr/bin/env python3
"""R066: source-pinned aggregate ONLY opinion-measurement feasibility audit.

No username, user identifier, post, user-level trajectory, edge or source data
is printed/persisted. E2 source verification != E2 validated opinion mechanism.
"""
from __future__ import annotations

import argparse
import bz2
import collections
import csv
import hashlib
import io
import json
import math
from pathlib import Path

MONTI_COMMIT = "5d31ba59e716e5bde85e4c56b9cdacc3920aaaf6"
OKAWA_COMMIT = "32441421a9a012acc64b206f73a2b6525580e3ce"
A_SOURCES = {
    "edges_user.tsv.bz2": ("e2e261b123963b257ed126a66b101fbaef6f937d", 321422, ("yearmonth", "parent", "author", "count")),
    "edges_feature.tsv.bz2": ("12b6d3f407697e593bc368b9cd65fca1bfd7ce2d", 490710, ("yearmonth", "author", "subreddit", "count")),
    "feature_scores.tsv.bz2": ("6c7d8a9e63d9860541d24b1c25c45d1cc2b8c565", 776604, None),
    "interaction_scores.tsv.bz2": ("18e367869399850fb4a1f28659a4b375e2ed43a1", 1922336, None),
}
B_FILENAME = "posts_final_sample_twitter_Abortion.tsv"
B_BLOB = "2a88788f32496a8ebe45293ecf95eaf516876df6"
B_EXPECTED_BYTES = 279372
MAX_EXPANDED_BYTES = 250_000_000
MAX_ROWS = 5_000_000
MAX_COLUMN_CHARS = 100_000


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def verify_blob(path: Path, expected_hash: str, expected_size: int) -> bytes:
    data = path.read_bytes()
    if len(data) != expected_size or git_blob_sha1(data) != expected_hash:
        raise ValueError("FAIL CLOSED: source byte size or Git blob SHA mismatch")
    return data


def _consume_rows(reader, expected_ncols: int | None = None):
    n = 0
    nbytes = 0
    for row in reader:
        n += 1
        if n > MAX_ROWS:
            raise ValueError("expanded row limit exceeded")
        nbytes += sum(len(value.encode("utf-8")) for value in row)
        if nbytes > MAX_EXPANDED_BYTES:
            raise ValueError("expanded byte limit exceeded")
        if expected_ncols is not None and len(row) != expected_ncols:
            raise ValueError("FAIL CLOSED: TSV number of columns differs")
        yield row
    if n == 0:
        raise ValueError("empty source table")


def audit_reddit_file(path: Path, sha: str, size: int,
                      declared: tuple[str, ...] | None):
    data = verify_blob(path, sha, size)
    csv.field_size_limit(MAX_COLUMN_CHARS)
    with bz2.BZ2File(io.BytesIO(data), mode="rb") as raw:
        with io.TextIOWrapper(raw, encoding="utf-8", newline="") as decoded:
            reader = csv.reader(decoded, delimiter="\t")
            if declared is None:
                try:
                    header = next(reader)
                except StopIteration:
                    raise ValueError("FAIL CLOSED: absent data header") from None
                if not 2 <= len(header) <= 20 or any(not name.strip() for name in header):
                    raise ValueError("FAIL CLOSED: invalid scores header")
                schema = tuple(header)
                has_header = True
            else:
                schema = declared
                has_header = False
            num_rows = 0
            months = set()
            positive_weight_sum = 0
            for row in _consume_rows(reader, expected_ncols=len(schema)):
                num_rows += 1
                if declared is not None:
                    if not row[0].strip() or any(not x.strip() for x in row[1:]):
                        raise ValueError("invalid nonempty edge field")
                    try:
                        count = int(row[3])
                    except ValueError:
                        raise ValueError("noninteger edge weight") from None
                    if count <= 0:
                        raise ValueError("nonpositive edge weight")
                    positive_weight_sum += count
                    months.add(row[0])
            if num_rows == 0:
                raise ValueError("empty source after header")
    return {
        "name": path.name, "git_blob_sha1": sha, "compressed_bytes": size,
        "rows": num_rows, "header_exists": has_header, "columns": list(schema),
        "distinct_months": len(months) if declared is not None else None,
        "min_month": min(months) if months else None,
        "max_month": max(months) if months else None,
        "aggregate_edge_weight": positive_weight_sum if declared is not None else None,
        "source_integrity": "PASS",
    }


def audit_annotated_opinions(path: Path, sha: str, size: int):
    data = verify_blob(path, sha, size)
    text = data.decode("utf-8")
    csv.field_size_limit(MAX_COLUMN_CHARS)
    reader = csv.DictReader(io.StringIO(text, newline=""), delimiter="\t")
    if reader.fieldnames != ["user_id", "opinion", "time"]:
        raise ValueError("FAIL CLOSED: expected exactly three opinion columns")
    persons: dict[str, list[float]] = {}
    opinion_counts = collections.Counter()
    times = set()
    rows = 0
    min_time = math.inf
    max_time = -math.inf
    last_time = -math.inf
    for row in reader:
        rows += 1
        if rows > MAX_ROWS:
            raise ValueError("row cap exceeded")
        if None in row or any(value is None for value in row.values()):
            raise ValueError("incorrect TSV column count")
        pid = row["user_id"]
        if not pid or len(pid) > 256:
            raise ValueError("missing or invalid user identifier")
        try:
            val = float(row["opinion"])
            t = float(row["time"])
        except ValueError:
            raise ValueError("invalid opinion/time numeric value") from None
        if not math.isfinite(val) or not math.isfinite(t) or t < 0.0:
            raise ValueError("nonfinite or negative timeline")
        if t < last_time:
            raise ValueError("file rows not chronologically nondecreasing")
        last_time = t
        min_time = min(min_time, t)
        max_time = max(max_time, t)
        opinion_counts[str(val)] += 1
        persons.setdefault(pid, []).append(t)
        times.add(t)
    if rows == 0 or not persons:
        raise ValueError("empty opinion data")
    repeat_people = sum(len(values) >= 2 for values in persons.values())
    multi_time_people = sum(len(set(values)) >= 2 for values in persons.values())
    # No raw IDs or trajectories are emitted. Manual post labels are not a
    # validated interval-scale human latent opinion nor a social network.
    return {
        "name":path.name,"git_blob_sha1":sha,"bytes":size,
        "columns":["user_id","opinion","time"],
        "rows":rows,"distinct_users":len(persons),
        "participants_with_two_or_more_posts":repeat_people,
        "participants_with_two_or_more_distinct_times":multi_time_people,
        "distinct_timestamps":len(times),
        "time_min":min_time,"time_max":max_time,
        "opinion_label_counts":dict(sorted(opinion_counts.items())),
        "source_integrity":"PASS",
        "opinion_measurement":"MANUALLY_ANNOTATED_POST_CLASS_LABEL_NOT_PERSON_LATENT_CONTINUOUS_OPINION",
        "social_exposure_network":"NOT_INCLUDED_IN_THIS_PUBLIC_SAMPLE",
        "three_model_identification":"BLOCKED_MISSING_NETWORK_AND_LATENT_MEASUREMENT",
    }


def audit_all(reddit_dir: Path, opinion_path: Path) -> dict:
    a = [audit_reddit_file(reddit_dir/name, *params)
         for name, params in A_SOURCES.items()]
    b = audit_annotated_opinions(opinion_path, B_BLOB, B_EXPECTED_BYTES)
    return {
        "study":"R066", "stage":"E2_TWO_CANDIDATE_SOURCE_MEASUREMENT_AUDIT",
        "protocol":"protocols/R066_E2_TWO_DATASET_MEASUREMENT_AUDIT_2026-10-16.md",
        "reddit_author_commit":MONTI_COMMIT,
        "annotated_opinion_author_commit":OKAWA_COMMIT,
        "reddit_files":a,
        "reddit_direct_repeated_opinion":"NO",
        "reddit_three_model_empirical_discrimination":"BLOCKED_MEASUREMENT",
        "annotated_opinion":b,
        "annotated_opinion_direct_continuous_person_level_opinion":"NO",
        "annotated_opinion_social_edges":"NOT_INCLUDED",
        "combined_three_model_empirical_fit":"NOT_AUTHORIZED",
        "status":"SOURCE_INTEGRITY_PASS_MEASUREMENT_BLOCKED",
        "privacy":"ONLY_NONIDENTIFYING_AGGREGATES_RECORDED",
        "pesen_v01":"FROZEN",
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--reddit-dir", type=Path, required=True)
    ap.add_argument("--annotated-opinion", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args=ap.parse_args()
    result=audit_all(args.reddit_dir,args.annotated_opinion)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({"stage":result["stage"],"status":result["status"],
                      "reddit_rows":{x["name"]:x["rows"] for x in result["reddit_files"]},
                      "annotated_rows":result["annotated_opinion"]["rows"],
                      "annotated_users":result["annotated_opinion"]["distinct_users"],
                      "empirical_fit":result["combined_three_model_empirical_fit"]},
                     sort_keys=True))


if __name__ == "__main__":
    main()
