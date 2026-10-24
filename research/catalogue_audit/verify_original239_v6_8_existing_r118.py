#!/usr/bin/env python3
"""Strict original239 v6.8 R118 link attribution and 165-row queue verifier."""
import copy
import csv
import hashlib
import json
from pathlib import Path

OLD = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.7_2026-10-24.json"
NEW = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.8_2026-10-24.json"
QUEUE = "docs/ORIGINAL_239_PENDING_165_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
TARGET = "03-019"


def git_blob(body):
    return hashlib.sha1(b"blob " + str(len(body)).encode("ascii") + b"\0" + body).hexdigest()


def verify(old, new, root):
    assert len(old["rows"]) == len(new["rows"]) == 239, "CATALOGUE_CARDINALITY"
    identity = lambda j: [(x["catalogue_id"], x["catalogue_name_en"], x["original_priority"])
                          for x in j["rows"]]
    assert identity(old) == identity(new), "IDENTITY_OR_ORDER_CHANGED"
    assert new["base_v6_7_git_blob_sha1"] == git_blob((root / OLD).read_bytes()), "BASE_BLOB"
    assert new["counts"] == old["counts"], "PRIMARY_MAPPING_COUNT_CHANGED"
    assert [y["catalogue_id"] for x, y in zip(old["rows"], new["rows"]) if x != y] == [TARGET], "CHANGED_ROWS"
    assert new["provisional_itemwise_audit_open_count"] == 165, "PENDING_COUNT"
    assert new["status_counts"]["PROVISIONAL_PRIMARY_README_LINK"] == 165, "PROVISIONAL_STATUS_COUNT"
    assert new["status_counts"]["DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"] == 8
    assert sum(new["status_counts"].values()) == 239, "STATUS_SUM"
    row = next(x for x in new["rows"] if x["catalogue_id"] == TARGET)
    assert row["proposed_primary_research_id"] == "R118", "WRONG_PRIMARY_R"
    assert row["link_status"] == "DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"
    acceptance = json.loads((root / row["method_specific_E1_acceptance"]).read_text(encoding="utf-8"))
    receipt = json.loads((root / acceptance["independent_CI_receipt"]).read_text(encoding="utf-8"))
    assert acceptance["existing_primary_R"] == receipt["research_id"] == "R118"
    assert acceptance["protocol_freeze_commit"] == receipt["protocol_freeze_commit"]
    assert acceptance["independent_CI_run"] == receipt["run_id"] == 40079060024
    assert acceptance["independent_CI_conclusion"] == receipt["run_conclusion"] == "success"
    assert receipt["run_status"] == "completed"
    assert acceptance["new_human_E2_scores"] == acceptance["new_historical_E3_scores"] == 0
    assert receipt["constructed_worlds"] == 700 and receipt["tamper_controls_rejected"] == 2
    assert (root / acceptance["independent_report"]).is_file()
    assert (root / acceptance["independent_script"]).is_file()
    with (root / acceptance["independent_constructed_data"]).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    assert len(rows) == 700, "ARTIFICIAL_ROW_COUNT"
    assert hashlib.sha256((root / acceptance["independent_constructed_data"]).read_bytes()).hexdigest() == receipt["constructed_csv_sha256"], "ARTIFICIAL_CSV_IDENTITY"
    with (root / QUEUE).open(newline="", encoding="utf-8") as stream:
        queue = list(csv.DictReader(stream))
    expected = [x["catalogue_id"] for x in new["rows"]
                if x["link_status"] == "PROVISIONAL_PRIMARY_README_LINK"]
    assert [x["catalogue_id"] for x in queue] == expected, "QUEUE_NOT_EXACT"
    return {"catalogue_count": 239, "changed": [TARGET], "provisional_remaining": 165,
            "primary_R": 236, "shared_math": 3, "new_human_E2": 0, "new_historical_E3": 0,
            "status": "PASS_BOUNDED_ORIGINAL239_R118_E1_REATTRIBUTION"}


def main():
    root = Path(__file__).resolve().parents[2]
    old = json.loads((root / OLD).read_text(encoding="utf-8"))
    new = json.loads((root / NEW).read_text(encoding="utf-8"))
    result = verify(old, new, root)
    controls = 0
    bad = copy.deepcopy(new)
    bad["rows"][0]["catalogue_name_en"] = "TAMPERED"
    try:
        verify(old, bad, root)
    except AssertionError:
        controls += 1
    bad = copy.deepcopy(new)
    next(x for x in bad["rows"] if x["catalogue_id"] == TARGET)["proposed_primary_research_id"] = "R999"
    try:
        verify(old, bad, root)
    except AssertionError:
        controls += 1
    assert controls == 2, "NEGATIVE_CONTROLS"
    result["tamper_controls_rejected"] = controls
    print(json.dumps(result, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
