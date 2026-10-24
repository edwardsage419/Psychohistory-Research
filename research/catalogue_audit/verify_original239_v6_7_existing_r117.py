#!/usr/bin/env python3
"""Strict original239 v6.7 R117 E1 reattribution and 166-row queue check."""
import copy
import csv
import hashlib
import json
from pathlib import Path

OLD = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.6_2026-10-24.json"
NEW = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.7_2026-10-24.json"
QUEUE = "docs/ORIGINAL_239_PENDING_166_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
TARGET = "03-009"


def git_blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def check(old, new, root):
    assert len(old["rows"]) == len(new["rows"]) == 239
    identity = lambda j: [(x["catalogue_id"], x["catalogue_name_en"], x["original_priority"])
                          for x in j["rows"]]
    assert identity(old) == identity(new), "CATALOGUE_IDENTITY"
    assert new["base_v6_6_git_blob_sha1"] == git_blob((root / OLD).read_bytes()), "BASE_IDENTITY"
    assert [b["catalogue_id"] for a, b in zip(old["rows"], new["rows"]) if a != b] == [TARGET]
    assert new["counts"] == old["counts"]
    assert new["provisional_itemwise_audit_open_count"] == 166
    assert sum(new["status_counts"].values()) == 239
    assert new["status_counts"]["PROVISIONAL_PRIMARY_README_LINK"] == 166
    assert new["status_counts"]["DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"] == 7
    row = next(x for x in new["rows"] if x["catalogue_id"] == TARGET)
    assert row["proposed_primary_research_id"] == "R117"
    assert row["link_status"] == "DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"
    receipt = json.loads((root / row["method_specific_E1_acceptance"]).read_text())
    assert receipt["existing_primary_R"] == "R117"
    assert receipt["independent_CI_run"] == 40075340202
    assert receipt["independent_CI_conclusion"] == "success"
    assert receipt["new_human_E2_scores"] == receipt["new_historical_E3_scores"] == 0
    assert (root / row["scientific_report_filenames"][0]).is_file()
    with (root / QUEUE).open(newline="", encoding="utf-8") as stream:
        queue = list(csv.DictReader(stream))
    expected = [x["catalogue_id"] for x in new["rows"]
                if x["link_status"] == "PROVISIONAL_PRIMARY_README_LINK"]
    assert [x["catalogue_id"] for x in queue] == expected
    return {"catalogue_count": 239, "changed": [TARGET], "provisional_remaining": 166,
            "primary_R": 236, "shared_math": 3, "new_E2": 0, "new_E3": 0,
            "status": "PASS_BOUNDED_ORIGINAL239_R117_E1_REATTRIBUTION"}


def main():
    root = Path(__file__).resolve().parents[2]
    old = json.loads((root / OLD).read_text(encoding="utf-8"))
    new = json.loads((root / NEW).read_text(encoding="utf-8"))
    result = check(old, new, root)
    controls = 0
    broken = copy.deepcopy(new)
    broken["rows"][0]["catalogue_name_en"] = "TAMPER"
    try:
        check(old, broken, root)
    except AssertionError:
        controls += 1
    broken = copy.deepcopy(new)
    next(x for x in broken["rows"] if x["catalogue_id"] == TARGET)["proposed_primary_research_id"] = "R999"
    try:
        check(old, broken, root)
    except AssertionError:
        controls += 1
    assert controls == 2, "NEGATIVE_CONTROLS"
    result["tamper_controls_rejected"] = controls
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
