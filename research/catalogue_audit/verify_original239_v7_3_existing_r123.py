#!/usr/bin/env python3
"""Original239 v7.3: strict R123 E1 provenance and 160-item queue verifier."""
import copy
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.2_2026-10-24.json"
NEW = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.3_2026-10-24.json"
QUEUE = "docs/ORIGINAL_239_PENDING_160_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
TARGET = "04-009"
ACCEPTANCE = "docs/ORIGINAL239_04-009_R123_E1_REATTRIBUTION_ACCEPTANCE.json"


def blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify(old, new):
    identity = lambda x: [(r["catalogue_id"], r["catalogue_name_en"],
                           r["original_priority"]) for r in x["rows"]]
    assert len(new["rows"]) == len(old["rows"]) == 239
    assert identity(old) == identity(new), "CATALOGUE_IDENTITY_DRIFT"
    assert new["base_v7_2_path"] == OLD
    assert new["base_v7_2_git_blob_sha1"] == blob_sha((ROOT / OLD).read_bytes())
    assert new["counts"] == old["counts"]
    assert [b["catalogue_id"] for a, b in zip(old["rows"], new["rows"])
            if a != b] == [TARGET], "UNAUTHORIZED_ROW_EDIT"
    assert new["changed_original_IDs"] == old["changed_original_IDs"] + [TARGET]
    assert new["provisional_itemwise_audit_open_count"] == 160
    assert new["status_counts"]["PROVISIONAL_PRIMARY_README_LINK"] == 160
    assert new["status_counts"]["DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"] == 13
    assert sum(new["status_counts"].values()) == 239
    row = next(r for r in new["rows"] if r["catalogue_id"] == TARGET)
    assert row["proposed_primary_research_id"] == "R123"
    assert row["link_status"] == "DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"
    assert row["method_specific_E1_acceptance"] == ACCEPTANCE
    assert row["readme_git_blob_sha1"] == blob_sha((ROOT / row["readme_path"]).read_bytes())
    assert row["source_csv_file_count"] == 1 and row["python_source_file_count"] == 3
    assert row["P1_scoped_review_addendum"]["CI_run_id"] == 40090970105
    assert row["P1_scoped_review_addendum"]["new_human_E2_scores"] == 0
    assert row["P1_scoped_review_addendum"]["new_historical_E3_scores"] == 0
    receipt = json.loads((ROOT / ACCEPTANCE).read_text(encoding="utf-8"))
    assert receipt["catalogue_id"] == TARGET and receipt["primary_R"] == "R123"
    assert receipt["grade"] == "PASS_BOUNDED_INTERNAL_FINITE_POWER_BASIS_E1"
    assert receipt["ci"]["run_id"] == 40090970105
    assert receipt["ci"]["conclusion"] == "success"
    assert receipt["constructed_matrix_count"] == 226
    assert receipt["new_human_E2_scores"] == receipt["new_historical_E3_scores"] == 0
    assert receipt["external_independent_reproduction"] is False
    assert (ROOT / receipt["scientific_report"]).is_file()
    raw = (ROOT / receipt["raw_csv"]).read_bytes()
    assert blob_sha(raw) == receipt["raw_csv_git_blob"]
    assert hashlib.sha256(raw).hexdigest() == receipt["raw_csv_sha256"]
    with (ROOT / receipt["raw_csv"]).open(newline="", encoding="utf-8") as f:
        data = list(csv.DictReader(f))
    assert len(data) == 226
    assert sum(int(x["structural_consensus"]) for x in data) == 176
    assert all(x["finite_horizon_consensus"] == x["structural_consensus"] ==
               x["original_classifier"] for x in data)
    with (ROOT / QUEUE).open(newline="", encoding="utf-8") as f:
        queue = list(csv.DictReader(f))
    pending = [r["catalogue_id"] for r in new["rows"]
               if r["link_status"] == "PROVISIONAL_PRIMARY_README_LINK"]
    assert len(queue) == 160 and [r["catalogue_id"] for r in queue] == pending
    assert queue[0]["catalogue_id"] == "04-015"
    return {"status": "PASS_BOUNDED_ORIGINAL239_R123_E1_REATTRIBUTION",
            "candidates": 239, "primary_R": 236, "shared_math": 3,
            "changed": [TARGET], "pending": 160, "raw_rows": 226,
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
            bad["provisional_itemwise_audit_open_count"] = 161
        try:
            verify(old, bad)
        except AssertionError:
            rejected += 1
    assert rejected == 3
    result["tamper_rejections"] = rejected
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
