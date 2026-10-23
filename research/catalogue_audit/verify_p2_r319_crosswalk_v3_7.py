#!/usr/bin/env python3
"""Original239 v3.7 candidate-only provenance and R319 source hash audit."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
P=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.6_2026-10-24.json"
N=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.7_2026-10-24.json"
Q0=DOC/"ORIGINAL_239_PENDING_26_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
Q1=DOC/"ORIGINAL_239_PENDING_25_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def gitblob(p):
    data=p.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\\0"+data).hexdigest()

def audit():
    before=json.loads(P.read_text(encoding="utf-8"))
    now=json.loads(N.read_text(encoding="utf-8"))
    assert now["base_v3_6_path"]==str(P.relative_to(ROOT))
    assert now["base_v3_6_git_blob_sha1"]==gitblob(P)
    assert len(before["rows"])==len(now["rows"])==239
    assert now["changed_original_IDs"]==before["changed_original_IDs"]+["01-007"]
    assert now["E1_new_research"]==before["E1_new_research"]+["R319"]
    assert now["counts"]=={"primary_R":211,"shared_bounded_math":3,
                           "older_scoped_only":0,"no_link_in_checked_sets":25,
                           "pending_primary_R":25}
    assert sum(now["counts"][k] for k in ("primary_R","shared_bounded_math",
                "older_scoped_only","no_link_in_checked_sets"))==239
    assert now["status_counts"]["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==25
    assert now["status_counts"]["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==2
    assert sum(now["status_counts"].values())==239
    changed=[]
    for a,b in zip(before["rows"],now["rows"]):
        for key in ("catalogue_id","catalogue_name_en","original_priority","catalogue_category"):
            assert a[key]==b[key]
        if a!=b: changed.append(a["catalogue_id"])
    assert changed==["01-007"]
    row=next(x for x in now["rows"] if x["catalogue_id"]=="01-007")
    assert row["catalogue_name_en"]=="Mixed Logit" and row["original_priority"]=="P2"
    assert row["proposed_primary_research_id"]=="R319"
    assert row["readme_git_blob_sha1"]==gitblob(ROOT/row["readme_path"])
    assert (ROOT/row["scientific_report_filenames"][0]).is_file()
    acceptance=json.loads((ROOT/row["method_specific_E1_acceptance"]).read_text(encoding="utf-8"))
    assert acceptance["research_id"]=="R319" and acceptance["status"]=="PASS_BOUNDED_E1_ONLY"
    assert acceptance["CI_run_id"]==40005442471 and acceptance["three_jobs_success"] is True
    assert acceptance["source_atoms"]==84 and acceptance["choice_worlds"]==15
    assert acceptance["real_human_E2"]=="NOT_ESTABLISHED"
    receipt=json.loads((ROOT/"research/R319/R319_MACHINE_RECEIPT.json").read_text(encoding="utf-8"))
    assert receipt["protocol_commit"]==acceptance["protocol_commit"]
    assert gitblob(ROOT/receipt["protocol_path"])==receipt["protocol_blob_sha1"]
    assert receipt["verification"]["CI_run_id"]==40005442471
    assert len(receipt["verification"]["jobs"])==3
    assert all(x["conclusion"]=="success" for x in receipt["verification"]["jobs"])
    for f in receipt["verified_source_artifacts"]:
        assert gitblob(ROOT/f["path"])==f["git_blob_sha1"],f["path"]
    with Q0.open(encoding="utf-8",newline="") as f:oldq=list(csv.DictReader(f))
    with Q1.open(encoding="utf-8",newline="") as f:newq=list(csv.DictReader(f))
    assert len(oldq)==26 and len(newq)==25
    assert newq==[x for x in oldq if x["original_catalogue_id"]!="01-007"]
    assert Counter(x["priority"] for x in newq)=={"P2":25}
    assert newq[0]["original_catalogue_id"]=="01-009"
    unmatched={x["catalogue_id"] for x in now["rows"]
               if x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"}
    assert {x["original_catalogue_id"] for x in newq}==unmatched
    print("PASS original239 v3.7 one R319 01-007 only, 211 primary, 25 pending, 84 exact sources")

if __name__=="__main__":
    audit()
