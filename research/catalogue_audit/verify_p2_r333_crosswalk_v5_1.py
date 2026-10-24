#!/usr/bin/env python3
"""Original239 v5.1: immutable 239 candidate identity and exact R333 provenance."""
import csv, hashlib, json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.0_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.1_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_11_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def read(p): return (ROOT/p).read_bytes()
def blob(p):
    data=read(p)
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def main():
    old=json.loads(read(OLD))
    new=json.loads(read(NEW))
    assert blob(OLD)=="65efda40694b4fc289e899295ae67a7706d5c9c5"
    assert new["base_v5_0_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert len({r["catalogue_id"] for r in new["rows"]})==239
    assert [r["catalogue_id"] for r in old["rows"]]==[r["catalogue_id"] for r in new["rows"]]
    for a,b in zip(old["rows"],new["rows"]):
        if a["catalogue_id"]!="03-002":
            assert a==b,a["catalogue_id"]
        else:
            assert a["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert b["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert b["proposed_primary_research_id"]=="R333"
            assert blob(b["readme_path"])==b["readme_git_blob_sha1"]=="cfd5f28c67155ae8a02f7194a6e86741a85845cd"
            assert b["method_specific_E1_acceptance"]=="research/R333/R333_FINAL_ACCEPTANCE_STATUS.json"
    assert new["counts"]==dict(primary_R=225,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=11,pending_primary_R=11)
    status=Counter(r["link_status"] for r in new["rows"])
    assert sum(status.values())==239
    assert status["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert status["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==16
    assert status["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==11
    assert dict(status)=={k:v for k,v in new["status_counts"].items() if v>0}
    q=list(csv.DictReader(read(QUEUE).decode().splitlines()))
    assert len(q)==11 and q[0]["original_catalogue_id"]=="03-011"
    assert [r["original_catalogue_id"] for r in q]==[r["catalogue_id"] for r in new["rows"] if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for path,sha in [
        ("protocols/R333_TRIADIC_RECIPROCAL_FEEDBACK_160_ARTIFICIAL_STATES_PRESCORE_FREEZE_2026-10-24.md","f66b8437f63bce079a7f10a0b8b82311dbdc64a4"),
        ("research/R333/r333_triadic_feedback.py","c28c82a6a18ababe8da14b0f48c846d940bf32b3"),
        ("research/R333/R333_ALL_160_ARTIFICIAL_TRIADIC_STATES.csv","8a202f773badb8833992ff0df25c3c90f60b3680"),
        ("research/R333/R333_EXACT_32_TRIADIC_WORLDS.json","dd82e1f616528742622ebafc844ec66adadf18b5"),
        ("research/catalogue_audit/independent_r333_triadic_audit.py","3d26317826130eed22380264af52c715ad8bf86e"),
        ("research/R333/R333_FINAL_ACCEPTANCE_STATUS.json","52ebada1e978179e624897715708854e41dd29f5"),
        ("research/R333/R333_MACHINE_RECEIPT.json","39c51ac7df3a208bbc884d90efeb9e213dcbfcc2")
    ]: assert blob(path)==sha,(path,blob(path))
    receipt=json.loads(read("research/R333/R333_MACHINE_RECEIPT.json"))
    acceptance=json.loads(read("research/R333/R333_FINAL_ACCEPTANCE_STATUS.json"))
    assert receipt["protocol_commit"]==acceptance["protocol_commit"]=="ebe035309977d3e5c5961a7091a17f0fe8222448"
    assert receipt["verification"]["CI_run_id"]==acceptance["CI_run_id"]==40047349488
    assert receipt["verification"]["three_jobs_success"] and acceptance["three_jobs_success"]
    assert acceptance["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_TRIADIC_BOOLEAN_FEEDBACK_ONLY"
    assert acceptance["real_human_E2"]==acceptance["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="03-002" and new["E1_new_research"][-1]=="R333"
    print("ORIGINAL239_V51_PASS 239 original 225 primary 3 shared 11 pending 173 provisional R333 160 artificial rows")
if __name__=="__main__": main()
