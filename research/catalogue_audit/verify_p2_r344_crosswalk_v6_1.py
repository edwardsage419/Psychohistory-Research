#!/usr/bin/env python3
"""Original239 v6.1 R344 linkage and zero-unlinked guard, 173 provisional open."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.0_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.1_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_0_UNLINKED_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def raw(p):return (ROOT/p).read_bytes()
def blob(p):
    b=raw(p)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def main():
    old,new=json.loads(raw(OLD)),json.loads(raw(NEW))
    assert blob(OLD)=="f3deeff8bd60fadc59dd30cf95e15567f783f4ac"
    assert new["base_v6_0_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [r["catalogue_id"] for r in old["rows"]]==[r["catalogue_id"] for r in new["rows"]]
    for a,b in zip(old["rows"],new["rows"]):
        if a["catalogue_id"]!="04-024":assert a==b,a["catalogue_id"]
        else:
            assert a["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert b["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert b["proposed_primary_research_id"]=="R344"
            assert blob(b["readme_path"])==b["readme_git_blob_sha1"]=="909eb74fd3d8f727fe0b9cdf4d224959a8aae236"
    status=json.loads(raw("research/R344/R344_FINAL_ACCEPTANCE_STATUS.json"))
    receipt=json.loads(raw("research/R344/R344_MACHINE_RECEIPT.json"))
    assert status["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_TWO_TYPE_METAPATH_SIMILARITY_ONLY"
    assert status["protocol_commit"]==receipt["protocol_commit"]=="000b70435a2e1f65a1826af3fe604862be1f0c60"
    assert status["source_commit"]==receipt["source_commit"]=="0eb0967f693a17c6bb29154f78042220692e5c5b"
    assert status["CI_run_id"]==receipt["verification"]["run_id"]==40063860148
    assert status["three_jobs_success"] and status["CI_conclusion"]=="success"
    assert status["real_human_E2"]==status["historical_E3"]=="NOT_ESTABLISHED"
    for p,sha in [
      ("protocols/R344_HETEROGENEOUS_METAPATH_64_ARTIFICIAL_PAIR_ATOMS_PRESCORE_FREEZE_2026-10-24.md",receipt["protocol_blob_sha1"]),
      ("research/R344/R344_ALL_64_ARTIFICIAL_TYPED_PATH_ATOMS.csv",receipt["artificial_source_blob_sha1"]),
      ("research/R344/R344_EXACT_16_TYPED_NETWORKS.json",receipt["results_blob_sha1"]),
      ("research/R344/r344_typed_pathsim.py",receipt["production_python_blob_sha1"]),
      ("research/catalogue_audit/independent_r344_heterogeneous_audit.py",receipt["independent_auditor_blob_sha1"])
    ]:assert blob(p)==sha,p
    assert new["counts"]==dict(primary_R=236,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=0,pending_primary_R=0)
    counts=Counter(x["link_status"] for x in new["rows"])
    assert counts["PROVISIONAL_PRIMARY_README_LINK"]==new["provisional_itemwise_audit_open_count"]==173
    assert counts["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==27
    assert counts["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==0
    assert dict(counts)=={k:v for k,v in new["status_counts"].items() if v>0}
    pending=[x["catalogue_id"] for x in new["rows"] if x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    queue=list(csv.DictReader(raw(QUEUE).decode().splitlines()))
    assert pending==[] and queue==[]
    assert new["changed_original_IDs"][-1]=="04-024" and new["E1_new_research"][-1]=="R344"
    assert new["rows"][0]["catalogue_id"]==old["rows"][0]["catalogue_id"]
    print("ORIGINAL239_V61_PASS 239 original 236 primary 3 shared 0 unlinked 173 provisional itemwise audits OPEN")

if __name__=="__main__":main()
