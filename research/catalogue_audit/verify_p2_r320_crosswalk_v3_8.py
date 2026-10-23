#!/usr/bin/env python3
"""Original239 v3.8 one-row R320 provenance and exact Git blob audit."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
P=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.7_2026-10-24.json"
N=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.8_2026-10-24.json"
Q0=DOC/"ORIGINAL_239_PENDING_25_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
Q1=DOC/"ORIGINAL_239_PENDING_24_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def gitblob(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def audit():
    base=json.loads(P.read_text(encoding="utf-8"))
    now=json.loads(N.read_text(encoding="utf-8"))
    assert now["base_v3_7_path"]==str(P.relative_to(ROOT))
    assert now["base_v3_7_git_blob_sha1"]==gitblob(P)
    assert len(base["rows"])==len(now["rows"])==239
    assert now["changed_original_IDs"]==base["changed_original_IDs"]+["01-009"]
    assert now["E1_new_research"]==base["E1_new_research"]+["R320"]
    assert now["counts"]=={"primary_R":212,"shared_bounded_math":3,
                           "older_scoped_only":0,"no_link_in_checked_sets":24,
                           "pending_primary_R":24}
    assert sum(now["counts"][k] for k in ("primary_R","shared_bounded_math",
                 "older_scoped_only","no_link_in_checked_sets"))==239
    assert now["status_counts"]["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==24
    assert now["status_counts"]["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==3
    assert sum(now["status_counts"].values())==239
    changed=[]
    for a,b in zip(base["rows"],now["rows"]):
        for k in ("catalogue_id","catalogue_name_en","original_priority","catalogue_category"):
            assert a[k]==b[k]
        if a!=b:changed.append(a["catalogue_id"])
    assert changed==["01-009"]
    row=next(r for r in now["rows"] if r["catalogue_id"]=="01-009")
    assert row["catalogue_name_en"]=="Drift Diffusion Model" and row["original_priority"]=="P2"
    assert row["proposed_primary_research_id"]=="R320"
    assert row["readme_git_blob_sha1"]==gitblob(ROOT/row["readme_path"])
    assert (ROOT/row["scientific_report_filenames"][0]).is_file()
    acceptance=json.loads((ROOT/row["method_specific_E1_acceptance"]).read_text(encoding="utf-8"))
    assert acceptance["research_id"]=="R320"
    assert acceptance["status"]=="PASS_BOUNDED_E1_DISCRETE_ANALOGUE_ONLY"
    assert acceptance["CI_run_id"]==40006163876 and acceptance["three_jobs_success"] is True
    assert acceptance["original_path_source_rows"]==384 and acceptance["world_count"]==6
    assert acceptance["real_human_E2"]=="NOT_ESTABLISHED"
    receipt=json.loads((ROOT/"research/R320/R320_MACHINE_RECEIPT.json").read_text(encoding="utf-8"))
    assert receipt["protocol_commit"]==acceptance["protocol_commit"]
    assert gitblob(ROOT/receipt["protocol_path"])==receipt["protocol_blob_sha1"]
    assert receipt["verification"]["CI_run_id"]==40006163876
    assert len(receipt["verification"]["jobs"])==3
    assert all(j["conclusion"]=="success" for j in receipt["verification"]["jobs"])
    for f in receipt["verified_source_artifacts"]:
        assert gitblob(ROOT/f["path"])==f["git_blob_sha1"],f["path"]
    with Q0.open(encoding="utf-8",newline="") as f:oldq=list(csv.DictReader(f))
    with Q1.open(encoding="utf-8",newline="") as f:newq=list(csv.DictReader(f))
    assert len(oldq)==25 and len(newq)==24
    assert newq==[r for r in oldq if r["original_catalogue_id"]!="01-009"]
    assert Counter(r["priority"] for r in newq)=={"P2":24}
    assert newq[0]["original_catalogue_id"]=="01-010"
    unmatched={r["catalogue_id"] for r in now["rows"]
               if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"}
    assert {r["original_catalogue_id"] for r in newq}==unmatched
    print("PASS original239 v3.8 R320 01-009 only, 212 primary, 24 pending, 384 exact paths")

if __name__=="__main__":
    audit()
