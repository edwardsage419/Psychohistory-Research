#!/usr/bin/env python3
"""Strict original239 v7.1 single-item R121 E1 attribution and 162-item queue."""
import copy
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.0_2026-10-24.json"
NEW = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v7.1_2026-10-24.json"
QUEUE = "docs/ORIGINAL_239_PENDING_162_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
TARGET = "04-004"
ACCEPTANCE = "docs/ORIGINAL239_04-004_R121_E1_REATTRIBUTION_ACCEPTANCE.json"
RAW_SHA = "60010a03972f41a091987e5d2be55d28347736c46af6cc28fc0bfab803c8efcb"


def git_blob(body):
    return hashlib.sha1(b"blob " + str(len(body)).encode() + b"\0" + body).hexdigest()


def verify(old, new):
    assert len(old["rows"]) == len(new["rows"]) == 239
    identities = lambda obj: [(r["catalogue_id"], r["catalogue_name_en"],
                               r["original_priority"]) for r in obj["rows"]]
    assert identities(old) == identities(new), "IDENTITY_DRIFT"
    assert new["base_v7_0_path"] == OLD
    assert new["base_v7_0_git_blob_sha1"] == git_blob((ROOT / OLD).read_bytes())
    assert new["counts"] == old["counts"]
    assert [b["catalogue_id"] for a, b in zip(old["rows"], new["rows"])
            if a != b] == [TARGET], "OTHER_ROWS_CHANGED"
    assert new["changed_original_IDs"] == old["changed_original_IDs"] + [TARGET]
    assert new["provisional_itemwise_audit_open_count"] == 162
    assert new["status_counts"]["PROVISIONAL_PRIMARY_README_LINK"] == 162
    assert new["status_counts"]["DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"] == 11
    assert sum(new["status_counts"].values()) == 239
    row = next(r for r in new["rows"] if r["catalogue_id"] == TARGET)
    assert row["proposed_primary_research_id"] == "R121"
    assert row["link_status"] == "DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"
    assert row["method_specific_E1_acceptance"] == ACCEPTANCE
    assert row["readme_git_blob_sha1"] == git_blob((ROOT / row["readme_path"]).read_bytes())
    assert row["source_csv_file_count"] == 1
    assert row["P1_scoped_review_addendum"]["CI_run_id"] == 40083743480
    assert row["P1_scoped_review_addendum"]["new_human_E2_scores"] == 0
    assert row["P1_scoped_review_addendum"]["new_historical_E3_scores"] == 0
    receipt = json.loads((ROOT / ACCEPTANCE).read_text(encoding="utf-8"))
    assert receipt["catalogue_id"] == TARGET and receipt["primary_R"] == "R121"
    assert receipt["scientific_grade"] == "PASS_BOUNDED_INTERNAL_SUBSET_CUT_RECURRENCE_E1"
    assert receipt["successful_CI_run_id"] == 40083743480
    assert receipt["freeze_commit"] == "22ce983ba369843e4dd5124b147ec14f8dbd7d45"
    assert receipt["successful_python_versions"] == ["3.11", "3.12"]
    assert receipt["independent_graph_seed_scheme_cases"] == 1060
    assert receipt["independent_terminal_distribution_rows"] == 1932
    assert receipt["new_human_E2"] == receipt["new_historical_E3"] == 0
    assert receipt["external_independent_replication"] is False
    assert (ROOT / receipt["scientific_report"]).is_file()
    assert (ROOT / receipt["source_path"]).is_file()
    raw = (ROOT / receipt["raw_data_path"]).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == receipt["raw_data_sha256"] == RAW_SHA
    with (ROOT / receipt["raw_data_path"]).open(newline="", encoding="utf-8") as stream:
        data = list(csv.DictReader(stream))
    assert len(data) == 1932
    assert all(int(x["numerator"]) > 0 and int(x["denominator"]) > 0 for x in data)
    with (ROOT / QUEUE).open(newline="", encoding="utf-8") as stream:
        queue = list(csv.DictReader(stream))
    pending = [r["catalogue_id"] for r in new["rows"]
               if r["link_status"] == "PROVISIONAL_PRIMARY_README_LINK"]
    assert len(queue) == 162 and [r["catalogue_id"] for r in queue] == pending
    assert queue[0]["catalogue_id"] == "04-005"
    return {"status": "PASS_BOUNDED_ORIGINAL239_R121_E1_REATTRIBUTION",
            "original_candidates": 239, "primary_R": 236, "shared_math": 3,
            "changed": [TARGET], "pending": 162, "raw_rows": 1932,
            "new_human_E2": 0, "new_historical_E3": 0}


def main():
    old = json.loads((ROOT / OLD).read_text(encoding="utf-8"))
    new = json.loads((ROOT / NEW).read_text(encoding="utf-8"))
    result = verify(old, new)
    rejected = 0
    for case in range(3):
        bad = copy.deepcopy(new)
        if case == 0:
            bad["rows"][0]["catalogue_name_en"] = "TAMPER"
        elif case == 1:
            next(r for r in bad["rows"] if r["catalogue_id"] == TARGET)["proposed_primary_research_id"] = "R999"
        else:
            bad["provisional_itemwise_audit_open_count"] = 163
        try:
            verify(old, bad)
        except AssertionError:
            rejected += 1
    assert rejected == 3
    result["tamper_rejections"] = rejected
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
