#!/usr/bin/env python3
"""Original239 v5.0 R332 exact catalogue provenance and queue audit."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.9_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.0_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_12_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def read(p):return (ROOT/p).read_bytes()
def blob(p):
    v=read(p)
    return hashlib.sha1(b"blob "+str(len(v)).encode()+b"\0"+v).hexdigest()
def run():
    old=json.loads(read(OLD));new=json.loads(read(NEW))
    assert blob(OLD)=="cadb1f579efd27e741bc1ac024233328371be721"
    assert new["base_v4_9_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [x["catalogue_id"] for x in old["rows"]]==[x["catalogue_id"] for x in new["rows"]]
    assert len({x["catalogue_id"] for x in new["rows"]})==239
    for a,b in zip(old["rows"],new["rows"]):
        if a["catalogue_id"]!="02-015":assert a==b,a["catalogue_id"]
        else:
            assert a["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert b["catalogue_name_en"]=="Cognitive Resource Constraints" and b["original_priority"]=="P2"
            assert b["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert b["proposed_primary_research_id"]=="R332"
            assert blob(b["readme_path"])==b["readme_git_blob_sha1"]=="a2fa62ce2c5310072d9d2af90d4bfe576d36d245"
    assert new["counts"]==dict(primary_R=224,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=12,pending_primary_R=12)
    c=Counter(x["link_status"] for x in new["rows"])
    assert sum(c.values())==239 and c["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert c["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==15
    assert c["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==12
    assert all(new["status_counts"][k]==v for k,v in c.items())
    q=list(csv.DictReader(read(QUEUE).decode().splitlines()))
    assert len(q)==12 and q[0]["original_catalogue_id"]=="03-002"
    assert [x["original_catalogue_id"] for x in q]==[x["catalogue_id"] for x in new["rows"] if x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for path,sha in [
        ("protocols/R332_THREE_TASK_COGNITIVE_RESOURCE_112_ATOMS_PRESCORE_FREEZE_2026-10-24.md","17d2022bece9d78a011796e61b581bf172b0c04a"),
        ("research/R332/r332_resource_allocation.py","fd468b3177c98c59a4612ac9ce5b719ad11398d4"),
        ("research/R332/R332_ALL_112_ARTIFICIAL_RESOURCE_SUBSETS.csv","d311966233bc608ba78eadcd696ae6c369c0674a"),
        ("research/R332/R332_EXACT_14_RESOURCE_WORLDS.json","5d7c162c968171f0bb45320ffde835035ed46486"),
        ("research/catalogue_audit/independent_r332_resource_audit.py","3fb9bf8c78b0a70fcd0f59b268ccf128e64fd246"),
        ("research/R332/R332_FINAL_ACCEPTANCE_STATUS.json","036e1819ab72ceba9a39b659c8b47ece7e121513")
    ]:assert blob(path)==sha,(path,blob(path))
    receipt=json.loads(read("research/R332/R332_MACHINE_RECEIPT.json"))
    acceptance=json.loads(read("research/R332/R332_FINAL_ACCEPTANCE_STATUS.json"))
    assert receipt["protocol_commit"]==acceptance["protocol_commit"]=="5dde3f2dab6bf09d51542de57e58fc962d02fd56"
    assert receipt["verification"]["CI_run_id"]==acceptance["CI_run_id"]==40041585075
    assert receipt["verification"]["three_jobs_success"]
    assert acceptance["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_THREE_TASK_RESOURCE_ALLOCATION_ONLY"
    assert acceptance["real_human_E2"]==acceptance["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="02-015" and new["E1_new_research"][-1]=="R332"
    print("ORIGINAL239_V50_PASS 239 original 224 primary 3 shared 12 pending 173 provisional R332 112 artificial subsets")
if __name__=="__main__":run()
