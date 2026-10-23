#!/usr/bin/env python3
"""R314 original239 v3.1 one-row change proof plus live source hash checks."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
BASE=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.0_2026-10-24.json"
LATEST=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.1_2026-10-24.json"
OLDQUEUE=DOC/"ORIGINAL_239_PENDING_32_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
NEWQUEUE=DOC/"ORIGINAL_239_PENDING_31_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def sha1_blob(path):
    raw=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def audit():
    before=json.loads(BASE.read_text(encoding="utf-8"))
    after=json.loads(LATEST.read_text(encoding="utf-8"))
    assert after["base_v3_0_path"]==str(BASE.relative_to(ROOT))
    assert after["base_v3_0_git_blob_sha1"]==sha1_blob(BASE)
    assert len(before["rows"])==len(after["rows"])==239
    assert after["changed_original_IDs"]==before["changed_original_IDs"]+["04-016"]
    assert after["E1_new_research"]==before["E1_new_research"]+["R314"]
    assert after["counts"]=={"primary_R":205,"shared_bounded_math":3,"older_scoped_only":1,"no_link_in_checked_sets":30,"pending_primary_R":31}
    assert sum(after["counts"][k] for k in ("primary_R","shared_bounded_math","older_scoped_only","no_link_in_checked_sets"))==239
    assert after["status_counts"]["DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"]==before["status_counts"]["DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"]+1
    assert after["status_counts"]["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==before["status_counts"]["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]-1
    assert sum(after["status_counts"].values())==239
    for k in before["status_counts"]:
        if k not in {"DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R","NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"}:
            assert after["status_counts"][k]==before["status_counts"][k]
    changed=[]
    ids=[]
    for old,new in zip(before["rows"],after["rows"]):
        for key in ("catalogue_id","catalogue_name_en","original_priority","catalogue_category"):
            assert old[key]==new[key],(old["catalogue_id"],key)
        ids.append(new["catalogue_id"])
        if old!=new: changed.append(new["catalogue_id"])
    assert len(set(ids))==239
    assert changed==["04-016"]
    row=next(item for item in after["rows"] if item["catalogue_id"]=="04-016")
    assert row["catalogue_name_en"]=="Preferential Attachment Network"
    assert row["original_priority"]=="P1"
    assert row["proposed_primary_research_id"]=="R314"
    assert row["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert row["P1_scoped_review_addendum"]["CI_run_id"]==39994420445
    assert row["P1_scoped_review_addendum"]["original_full_artificial_target_atoms"]==54
    assert row["readme_git_blob_sha1"]==sha1_blob(ROOT/row["readme_path"])
    acceptance=json.loads((ROOT/row["method_specific_E1_acceptance"]).read_text(encoding="utf-8"))
    assert acceptance["research_id"]=="R314"
    assert acceptance["status"]=="PASS_BOUNDED_E1_ONLY"
    assert acceptance["run_id"]==39994420445 and acceptance["run_conclusion"]=="success"
    assert acceptance["human_E2"]=="NOT_ESTABLISHED" and acceptance["historical_E3"]=="NOT_ESTABLISHED"
    receipt=json.loads((ROOT/"research/R314/R314_MACHINE_RECEIPT.json").read_text(encoding="utf-8"))
    assert receipt["frozen_before_scoring_commit"]==acceptance["frozen_before_code_commit"]
    assert receipt["verification"]["CI_run_id"]==39994420445
    assert receipt["verification"]["conclusion"]=="success"
    assert len(receipt["verification"]["jobs"])==3
    for artifact in receipt["source_evidence"]:
        assert sha1_blob(ROOT/artifact["path"])==artifact["git_blob_sha1"], artifact["path"]
    with OLDQUEUE.open(encoding="utf-8",newline="") as h: q0=list(csv.DictReader(h))
    with NEWQUEUE.open(encoding="utf-8",newline="") as h: q1=list(csv.DictReader(h))
    assert len(q0)==32 and len(q1)==31
    assert q1==[x for x in q0 if x["original_catalogue_id"]!="04-016"]
    assert Counter(x["priority"] for x in q1)=={"P1":4,"P2":27}
    assert q1[0]["original_catalogue_id"]=="04-017"
    unassigned={x["catalogue_id"] for x in after["rows"] if x["link_status"] in ("NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS","PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY")}
    assert {x["original_catalogue_id"] for x in q1}==unassigned
    assert row["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    print("PASS: original239 v3.1 one changed 04-016; 205 primary, 31 pending (P1=4,P2=27); all R314 Git blob SHA1 verified")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test",action="store_true")
    parser.add_argument("--audit",action="store_true")
    parser.parse_args()
    audit()
