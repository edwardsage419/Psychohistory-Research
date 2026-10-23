#!/usr/bin/env python3
"""R313 original239 v3.0 crosswalk: exact, minimal one-row source audit."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
P=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.9_2026-10-23.json"
C=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.0_2026-10-24.json"
Q0=DOC/"ORIGINAL_239_PENDING_33_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q1=DOC/"ORIGINAL_239_PENDING_32_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def git_blob_sha(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\\0"+data).hexdigest()

def audit():
    prior=json.loads(P.read_text(encoding="utf-8"))
    now=json.loads(C.read_text(encoding="utf-8"))
    assert len(prior["rows"])==len(now["rows"])==239
    assert now["base_v2_9_path"]==str(P.relative_to(ROOT))
    assert now["base_v2_9_git_blob_sha1"]==git_blob_sha(P)
    assert now["changed_original_IDs"]==prior["changed_original_IDs"]+["04-014"]
    assert now["E1_new_research"]==prior["E1_new_research"]+["R313"]
    assert now["counts"]=={"primary_R":204,"shared_bounded_math":3,"older_scoped_only":1,"no_link_in_checked_sets":31,"pending_primary_R":32}
    assert sum(now["counts"][k] for k in ("primary_R","shared_bounded_math","older_scoped_only","no_link_in_checked_sets"))==239
    assert now["status_counts"]["DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"]==prior["status_counts"]["DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"]+1
    assert now["status_counts"]["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==prior["status_counts"]["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]-1
    assert sum(now["status_counts"].values())==239
    for k in prior["status_counts"]:
        if k not in {"DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R","NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"}:
            assert now["status_counts"][k]==prior["status_counts"][k]
    ids=[x["catalogue_id"] for x in now["rows"]]
    assert len(ids)==len(set(ids))==239
    assert ids==[x["catalogue_id"] for x in prior["rows"]]
    changed=[]
    for old,new in zip(prior["rows"],now["rows"]):
        if old!=new: changed.append(old["catalogue_id"])
        assert (old["catalogue_id"],old["catalogue_name_en"],old["original_priority"],old["catalogue_category"]) == (new["catalogue_id"],new["catalogue_name_en"],new["original_priority"],new["catalogue_category"])
    assert changed==["04-014"]
    row=next(x for x in now["rows"] if x["catalogue_id"]=="04-014")
    assert row["catalogue_name_en"]=="Axelrod Cultural Dissemination"
    assert row["original_priority"]=="P1"
    assert row["proposed_primary_research_id"]=="R313"
    assert row["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert row["P1_scoped_review_addendum"]["CI_run_id"]==39993794818
    assert row["P1_scoped_review_addendum"]["original_full_artificial_feature_atoms"]==512
    assert row["method_specific_E1_acceptance"]=="research/R313/R313_FINAL_ACCEPTANCE_STATUS.json"
    assert row["readme_git_blob_sha1"]==git_blob_sha(ROOT/row["readme_path"])
    assert (ROOT/row["scientific_report_filenames"][0]).is_file()
    acceptance=json.loads((ROOT/row["method_specific_E1_acceptance"]).read_text(encoding="utf-8"))
    assert acceptance["research_id"]=="R313" and acceptance["status"]=="PASS_BOUNDED_E1_ONLY"
    assert acceptance["live_run_id"]==39993794818 and acceptance["live_run_conclusion"]=="success"
    assert acceptance["real_human_E2"]=="NOT_ESTABLISHED" and acceptance["historical_E3"]=="NOT_ESTABLISHED"
    receipt=json.loads((ROOT/"research/R313/R313_MACHINE_RECEIPT.json").read_text(encoding="utf-8"))
    assert receipt["freeze_protocol_commit_sha"]==acceptance["frozen_before_scoring_commit"]
    for artifact in receipt["artifacts"]:
        assert git_blob_sha(ROOT/artifact["path"])==artifact["git_blob_sha1"], artifact["path"]
    with Q0.open(newline="",encoding="utf-8") as h: oldq=list(csv.DictReader(h))
    with Q1.open(newline="",encoding="utf-8") as h: newq=list(csv.DictReader(h))
    assert len(oldq)==33 and len(newq)==32
    assert newq==[r for r in oldq if r["original_catalogue_id"]!="04-014"]
    assert Counter(r["priority"] for r in newq)=={"P1":5,"P2":27}
    assert newq[0]["original_catalogue_id"]=="04-016"
    assert {r["original_catalogue_id"] for r in newq}=={r["catalogue_id"] for r in now["rows"] if r["link_status"] in ("NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS","PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY")}
    assert row["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    print("PASS: v3.0, 239 immutable candidate IDs/names/priorities, one changed 04-014, 204 main, 32 pending (5 P1/27 P2); R313 source blobs match")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--audit",action="store_true");p.add_argument("--test",action="store_true")
    p.parse_args()
    audit()
