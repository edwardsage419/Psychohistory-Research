#!/usr/bin/env python3
"""Strict original239 v7.0 single-item R120 attribution and 163 pending queue."""
from __future__ import annotations

import copy
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.9_2026-10-24.json"
NEW = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.0_2026-10-24.json"
QUEUE = "docs/ORIGINAL_239_PENDING_163_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
TARGET = "04-003"
ACCEPTANCE = "docs/ORIGINAL239_04-003_R120_E1_REATTRIBUTION_ACCEPTANCE.json"
RAW_SHA = "189a7a857cfa59e318e254c88ec3c7edb1d89f6caf6d197945ac1c3d00ad4fea"


def git_blob(body):
    return hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()


def verify(old, new, root):
    assert len(old["rows"]) == len(new["rows"]) == 239, "COUNT"
    identity = lambda obj: [(r["catalogue_id"], r["catalogue_name_en"],
                             r["original_priority"]) for r in obj["rows"]]
    assert identity(old) == identity(new), "IDENTITY_CHANGED"
    assert new["base_v6_9_path"] == OLD
    assert new["base_v6_9_git_blob_sha1"] == git_blob((root / OLD).read_bytes()), "BASE_BLOB_CHANGED"
    assert new["counts"] == old["counts"] == {
        "primary_R": 236, "shared_bounded_math": 3,
        "older_scoped_only": 0, "no_link_in_checked_sets": 0,
        "pending_primary_R": 0}, "PRIMARY_R_MAPPING_CHANGED"
    assert [b["catalogue_id"] for a, b in zip(old["rows"], new["rows"])
            if a != b] == [TARGET], "UNEXPECTED_ROW_EDIT"
    assert new["provisional_itemwise_audit_open_count"] == 163
    assert new["status_counts"]["PROVISIONAL_PRIMARY_README_LINK"] == 163
    assert new["status_counts"]["DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"] == 10
    assert sum(new["status_counts"].values()) == 239
    assert new["changed_original_IDs"] == old["changed_original_IDs"] + [TARGET]
    row = next(r for r in new["rows"] if r["catalogue_id"] == TARGET)
    assert row["proposed_primary_research_id"] == "R120"
    assert row["link_status"] == "DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"
    assert row["method_specific_E1_acceptance"] == ACCEPTANCE
    assert row["readme_git_blob_sha1"] == git_blob((root / row["readme_path"]).read_bytes())
    assert row["source_csv_file_count"] == 1
    assert row["P1_scoped_review_addendum"]["CI_run_id"] == 40083392282
    assert row["P1_scoped_review_addendum"]["new_human_E2_scores"] == 0
    assert row["P1_scoped_review_addendum"]["new_historical_E3_scores"] == 0
    receipt = json.loads((root / ACCEPTANCE).read_text(encoding="utf-8"))
    assert receipt["catalogue_id"] == TARGET and receipt["primary_R"] == "R120"
    assert receipt["scientific_grade"] == "PASS_BOUNDED_INTERNAL_THIRD_METHOD_EXACT_E1"
    assert receipt["successful_CI_run_id"] == 40083392282
    assert receipt["first_failed_CI_run_id"] == 40083352028
    assert receipt["freeze_commit"] == "5be1c64271e6ef1152e4b2e3059f307b211d5bfc"
    assert receipt["successful_python_versions"] == ["3.11", "3.12"]
    assert receipt["graph_seed_cases"] if "graph_seed_cases" in receipt else True
    assert receipt["independent_graph_seed_cases"] == 530
    assert receipt["independent_terminal_distribution_rows"] == 590
    assert receipt["new_human_E2"] == receipt["new_historical_E3"] == 0
    assert receipt["external_independent_replication"] is False
    assert (root / receipt["scientific_report"]).is_file()
    assert (root / receipt["source_path"]).is_file()
    raw = (root / receipt["raw_data_path"]).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == receipt["raw_data_sha256"] == RAW_SHA, "RAW_DATA_HASH"
    with (root / receipt["raw_data_path"]).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 590
    assert all(int(row["count"]) > 0 and int(row["total"]) > 0 for row in rows)
    with (root / QUEUE).open(newline="", encoding="utf-8") as f:
        queue = list(csv.DictReader(f))
    expected = [r["catalogue_id"] for r in new["rows"]
                if r["link_status"] == "PROVISIONAL_PRIMARY_README_LINK"]
    assert len(queue) == 163 and [r["catalogue_id"] for r in queue] == expected, "QUEUE"
    assert queue[0]["catalogue_id"] == "04-004"
    return {"result": "PASS_BOUNDED_ORIGINAL239_R120_E1_REATTRIBUTION",
            "catalogue": 239, "primary_R": 236, "shared_math": 3,
            "changed": [TARGET], "pending": 163, "data_rows": 590,
            "human_E2_new": 0, "historical_E3_new": 0}


def main():
    old = json.loads((ROOT / OLD).read_text(encoding="utf-8"))
    new = json.loads((ROOT / NEW).read_text(encoding="utf-8"))
    result = verify(old, new, ROOT)
    tamper_rejected = 0
    for case in range(3):
        bad = copy.deepcopy(new)
        if case == 0:
            bad["rows"][0]["catalogue_name_en"] = "TAMPER"
        elif case == 1:
            next(r for r in bad["rows"] if r["catalogue_id"] == TARGET)["proposed_primary_research_id"] = "R999"
        else:
            bad["provisional_itemwise_audit_open_count"] = 164
        try:
            verify(old, bad, ROOT)
        except AssertionError:
            tamper_rejected += 1
    assert tamper_rejected == 3
    result["tamper_rejections"] = tamper_rejected
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
