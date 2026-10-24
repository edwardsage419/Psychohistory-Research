#!/usr/bin/env python3
"""Original239 v5.6 strict itemwise R338 provenance and six-item queue audit."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OLD = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.5_2026-10-24.json"
NEW = "docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.6_2026-10-24.json"
QUEUE = "docs/ORIGINAL_239_PENDING_6_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def data(path):
    return (ROOT / path).read_bytes()

def blob(path):
    b = data(path)
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()

def main():
    old, new = json.loads(data(OLD)), json.loads(data(NEW))
    assert blob(OLD) == "f36f661474616a96054adb2ba552f122a933e425"
    assert new["base_v5_5_git_blob_sha1"] == blob(OLD)
    assert len(old["rows"]) == len(new["rows"]) == 239
    assert [r["catalogue_id"] for r in old["rows"]] == [r["catalogue_id"] for r in new["rows"]]
    assert len({r["catalogue_id"] for r in new["rows"]}) == 239
    for before, after in zip(old["rows"], new["rows"]):
        if before["catalogue_id"] != "03-017":
            assert before == after, before["catalogue_id"]
        else:
            assert before["link_status"] == "NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert after["link_status"] == "DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert after["proposed_primary_research_id"] == "R338"
            assert blob(after["readme_path"]) == after["readme_git_blob_sha1"] == "d13385293116b21e1c31ffb6615648c8e729c731"
            assert after["method_specific_E1_acceptance"] == "research/R338/R338_FINAL_ACCEPTANCE_STATUS.json"
    assert new["counts"] == dict(primary_R=230, shared_bounded_math=3, older_scoped_only=0,
                                 no_link_in_checked_sets=6, pending_primary_R=6)
    statuses = Counter(r["link_status"] for r in new["rows"])
    assert sum(statuses.values()) == 239
    assert statuses["PROVISIONAL_PRIMARY_README_LINK"] == 173
    assert statuses["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"] == 21
    assert statuses["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"] == 6
    assert dict(statuses) == {k:v for k,v in new["status_counts"].items() if v>0}
    pending = [r["catalogue_id"] for r in new["rows"] if r["link_status"] == "NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    q = list(csv.DictReader(data(QUEUE).decode().splitlines()))
    assert len(q) == 6 and q[0]["original_catalogue_id"] == "03-020"
    assert [r["original_catalogue_id"] for r in q] == pending
    for path, sha in [
        ("protocols/R338_RELATIVE_DEPRIVATION_128_ARTIFICIAL_COMPARISON_ATOMS_PRESCORE_FREEZE_2026-10-24.md","52607cc28f098603f2d0286b58a76f0d79691f93"),
        ("research/R338/r338_relative_deprivation.py","1ee4cff348278f208628358b626174fd5fcb5524"),
        ("research/R338/R338_ALL_128_ARTIFICIAL_COMPARISON_ATOMS.csv","c434463b5a3c1e4dc4da068dfd6e720466e68ce3"),
        ("research/R338/R338_EXACT_64_CONDITIONS.json","7f428ceaa0ff89ac359437e4e99768ebe06e4776"),
        ("research/catalogue_audit/independent_r338_relative_deprivation_audit.py","ce5dc79a9b9df2869a2989309129b50d0c3b4b43")
    ]:
        assert blob(path) == sha, (path, blob(path))
    a = json.loads(data("research/R338/R338_FINAL_ACCEPTANCE_STATUS.json"))
    receipt = json.loads(data("research/R338/R338_MACHINE_RECEIPT.json"))
    assert a["protocol_commit"] == receipt["protocol_commit"] == "6b843af069053eb73c7883ba700f918c5cb8288d"
    assert a["source_commit"] == receipt["source_commit"] == "f4d219fecb3f54a522d0ab86a26cb24b41ee0452"
    assert a["CI_run_id"] == receipt["verification"]["run_id"] == 40059210892
    assert a["three_jobs_success"] and a["status"] == "PASS_BOUNDED_E1_CONSTRUCTED_REFERENCE_GAP_AND_FOUR_GATES_ONLY"
    assert a["real_human_E2"] == a["historical_E3"] == "NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1] == "03-017" and new["E1_new_research"][-1] == "R338"
    print("ORIGINAL239_V56_PASS 239 original 230 primary 3 shared 6 pending 173 provisional R338 128 artificial atoms")

if __name__ == "__main__":
    main()
