#!/usr/bin/env python3
"""Strict original239 v7.2 R122 scope, source identity, and 161-item queue audit."""
import copy
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.1_2026-10-24.json"
NEW = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.2_2026-10-24.json"
QUEUE = "docs/ORIGINAL_239_PENDING_161_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
TARGET = "04-005"
ACCEPTANCE = "docs/ORIGINAL239_04-005_R122_E1_REATTRIBUTION_ACCEPTANCE.json"


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify(old, new):
    identity = lambda x: [(r["catalogue_id"], r["catalogue_name_en"],
                           r["original_priority"]) for r in x["rows"]]
    assert len(new["rows"]) == len(old["rows"]) == 239
    assert identity(old) == identity(new), "IDENTITY_DRIFT"
    assert new["base_v7_1_path"] == OLD
    assert new["base_v7_1_git_blob_sha1"] == git_blob((ROOT / OLD).read_bytes())
    assert new["counts"] == old["counts"]
    assert [b["catalogue_id"] for a, b in zip(old["rows"], new["rows"])
            if a != b] == [TARGET], "UNAUTHORIZED_ROW_EDIT"
    assert new["changed_original_IDs"] == old["changed_original_IDs"] + [TARGET]
    assert new["provisional_itemwise_audit_open_count"] == 161
    assert new["status_counts"]["PROVISIONAL_PRIMARY_README_LINK"] == 161
    assert new["status_counts"]["DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"] == 12
    assert sum(new["status_counts"].values()) == 239
    row = next(r for r in new["rows"] if r["catalogue_id"] == TARGET)
    assert row["proposed_primary_research_id"] == "R122"
    assert row["link_status"] == "DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"
    assert row["method_specific_E1_acceptance"] == ACCEPTANCE
    assert row["readme_git_blob_sha1"] == git_blob((ROOT / row["readme_path"]).read_bytes())
    assert row["source_csv_file_count"] == 1
    assert row["P1_scoped_review_addendum"]["CI_run_id"] == 40087355161
    assert row["P1_scoped_review_addendum"]["new_human_E2_scores"] == 0
    assert row["P1_scoped_review_addendum"]["new_historical_E3_scores"] == 0
    receipt = json.loads((ROOT / ACCEPTANCE).read_text(encoding="utf-8"))
    assert receipt["catalogue_id"] == TARGET and receipt["research_id"] == "R122"
    assert receipt["status"] == "PASS_BOUNDED_INTERNAL_ASYNC_REACHABILITY_E1"
    assert receipt["ci_run_id"] == 40087355161 and receipt["ci_conclusion"] == "success"
    assert {x["python"] for x in receipt["ci_jobs"]} == {"3.11", "3.12"}
    assert receipt["total_cases"] == 16930
    assert receipt["new_human_E2"] == receipt["new_historical_E3"] == 0
    assert receipt["external_team_replication"] is False
    assert (ROOT / receipt["scientific_report"]).is_file()
    assert git_blob((ROOT / receipt["third_method_script"]).read_bytes()) == receipt["third_method_script_git_blob_sha1"]
    raw = (ROOT / receipt["raw_csv"]).read_bytes()
    assert git_blob(raw) == receipt["raw_csv_git_blob_sha1"]
    assert hashlib.sha256(raw).hexdigest() == receipt["raw_csv_sha256"]
    with (ROOT / receipt["raw_csv"]).open(newline="", encoding="utf-8") as f:
        data = list(csv.DictReader(f))
    assert len(data) == 16930
    assert all(int(x["reachable_states"]) >= 1 for x in data)
    with (ROOT / QUEUE).open(newline="", encoding="utf-8") as f:
        queue = list(csv.DictReader(f))
    pending = [r["catalogue_id"] for r in new["rows"]
               if r["link_status"] == "PROVISIONAL_PRIMARY_README_LINK"]
    assert len(queue) == 161 and [r["catalogue_id"] for r in queue] == pending
    assert queue[0]["catalogue_id"] == "04-009"
    return {"status": "PASS_BOUNDED_ORIGINAL239_R122_E1_REATTRIBUTION",
            "original_candidates": 239, "primary_R": 236, "shared_math": 3,
            "changed": [TARGET], "pending": 161, "raw_rows": 16930,
            "new_human_E2": 0, "new_historical_E3": 0}


def main():
    old = json.loads((ROOT / OLD).read_text(encoding="utf-8"))
    new = json.loads((ROOT / NEW).read_text(encoding="utf-8"))
    result = verify(old, new)
    rejected = 0
    for i in range(3):
        bad = copy.deepcopy(new)
        if i == 0:
            bad["rows"][0]["catalogue_name_en"] = "TAMPER"
        elif i == 1:
            next(r for r in bad["rows"] if r["catalogue_id"] == TARGET)["proposed_primary_research_id"] = "R999"
        else:
            bad["provisional_itemwise_audit_open_count"] = 162
        try:
            verify(old, bad)
        except AssertionError:
            rejected += 1
    assert rejected == 3
    result["tamper_rejections"] = rejected
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
