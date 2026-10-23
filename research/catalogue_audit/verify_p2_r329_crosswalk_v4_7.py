#!/usr/bin/env python3
"""Original239 v4.7 exact itemwise R329 metadata, source identity and queue audit."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.6_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.7_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_15_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def read(p): return (ROOT/p).read_bytes()
def blob(p):
    b=read(p)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\\0".replace(b"\\0",b"\0")+b).hexdigest()
def run():
    old=json.loads(read(OLD));new=json.loads(read(NEW))
    assert blob(OLD)=="7e61af15ecd6c0560cb5a71dbef0197a0ea010bc"
    assert new["base_v4_6_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [r["catalogue_id"] for r in old["rows"]]==[r["catalogue_id"] for r in new["rows"]]
    assert len(set(r["catalogue_id"] for r in new["rows"]))==239
    for a,b in zip(old["rows"],new["rows"]):
        if a["catalogue_id"]!="02-011": assert a==b,a["catalogue_id"]
        else:
            assert a["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert b["catalogue_name_en"]=="Active Inference" and b["original_priority"]=="P2"
            assert b["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert b["proposed_primary_research_id"]=="R329"
            assert blob(b["readme_path"])==b["readme_git_blob_sha1"]=="e116d7aa8a1cd2a10860047d629e4d2e0662759f"
    assert new["counts"]==dict(primary_R=221,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=15,pending_primary_R=15)
    counts=Counter(r["link_status"] for r in new["rows"])
    assert sum(counts.values())==239 and counts["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert counts["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==12
    assert counts["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==15
    assert all(new["status_counts"][k]==v for k,v in counts.items())
    queue=list(csv.DictReader(read(QUEUE).decode().splitlines()))
    assert len(queue)==15 and queue[0]["original_catalogue_id"]=="02-013"
    assert [r["original_catalogue_id"] for r in queue]==[r["catalogue_id"] for r in new["rows"] if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for path,sha in [
        ("protocols/R329_ACTIVE_INFERENCE_144_JOINT_ATOMS_18_WORLDS_PRESCORE_FREEZE_2026-10-24.md","a142b1a9a830ea0070a8c7e6991766cf49347d25"),
        ("research/R329/r329_active_inference.py","63c7e7c5ed1d7d390a7f6093073d5d62e23b91f1"),
        ("research/R329/R329_ALL_144_ARTIFICIAL_JOINT_ATOMS.csv","7308a1e34a24915d06f6b26f2cba47566d0c6c97"),
        ("research/R329/R329_EXACT_18_EFE_WORLDS.json","19218910a5b59e222f2b7f4ae64b7fc88f4b2eb8"),
        ("research/catalogue_audit/independent_r329_active_inference_audit.py","53b4b8cb32c335273e3b22103fe4bf44026ce208")
    ]: assert blob(path)==sha,(path,blob(path))
    receipt=json.loads(read("research/R329/R329_MACHINE_RECEIPT.json"))
    acceptance=json.loads(read("research/R329/R329_FINAL_ACCEPTANCE_STATUS.json"))
    assert receipt["protocol_commit"]=="15cb8ddaf57295ea3a2b6ad16f20cab4483187cb"
    assert receipt["verification"]["CI_run_id"]==acceptance["CI_run_id"]==40035516146
    assert all(j["conclusion"]=="success" for j in receipt["verification"]["jobs"])
    assert acceptance["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_BINARY_EFE_ONLY"
    assert acceptance["real_human_E2"]==acceptance["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="02-011" and new["E1_new_research"][-1]=="R329"
    print("ORIGINAL239_V47_PASS 239 original 221 primary 3 shared 15 pending 173 provisional R329 144 artificial atoms")
if __name__=="__main__":run()
