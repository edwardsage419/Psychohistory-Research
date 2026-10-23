#!/usr/bin/env python3
"""R315 original239 v3.2 invariant audit with Git blob source identity."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
OLD=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.1_2026-10-24.json"
NEW=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.2_2026-10-24.json"
Q0=DOC/"ORIGINAL_239_PENDING_31_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
Q1=DOC/"ORIGINAL_239_PENDING_30_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def gitblob(path):
    raw=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def audit():
    a=json.loads(OLD.read_text(encoding="utf-8"))
    b=json.loads(NEW.read_text(encoding="utf-8"))
    assert b["base_v3_1_path"]==str(OLD.relative_to(ROOT))
    assert b["base_v3_1_git_blob_sha1"]==gitblob(OLD)
    assert len(a["rows"])==len(b["rows"])==239
    assert b["changed_original_IDs"]==a["changed_original_IDs"]+["04-017"]
    assert b["E1_new_research"]==a["E1_new_research"]+["R315"]
    assert b["counts"]=={"primary_R":206,"shared_bounded_math":3,"older_scoped_only":1,"no_link_in_checked_sets":29,"pending_primary_R":30}
    assert sum(b["counts"][x] for x in ("primary_R","shared_bounded_math","older_scoped_only","no_link_in_checked_sets"))==239
    assert sum(b["status_counts"].values())==239
    for k,v in a["status_counts"].items():
        increment=1 if k=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R" else -1 if k=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS" else 0
        assert b["status_counts"][k]==v+increment
    changed=[]
    ids=[]
    for x,y in zip(a["rows"],b["rows"]):
        for key in ("catalogue_id","catalogue_name_en","original_priority","catalogue_category"):
            assert x[key]==y[key]
        ids.append(y["catalogue_id"])
        if x!=y:changed.append(y["catalogue_id"])
    assert len(set(ids))==239 and changed==["04-017"]
    r=next(y for y in b["rows"] if y["catalogue_id"]=="04-017")
    assert r["catalogue_name_en"]=="Watts Strogatz Small World"
    assert r["original_priority"]=="P1" and r["proposed_primary_research_id"]=="R315"
    assert r["readme_git_blob_sha1"]==gitblob(ROOT/r["readme_path"])
    assert (ROOT/r["scientific_report_filenames"][0]).is_file()
    accept=json.loads((ROOT/r["method_specific_E1_acceptance"]).read_text(encoding="utf-8"))
    assert accept["research_id"]=="R315" and accept["status"]=="PASS_BOUNDED_E1_ONLY"
    assert accept["live_CI_run_id"]==39995420565 and accept["CI_conclusion"]=="success"
    assert accept["human_E2"]=="NOT_ESTABLISHED" and accept["history_E3"]=="NOT_ESTABLISHED"
    receipt=json.loads((ROOT/"research/R315/R315_MACHINE_RECEIPT.json").read_text(encoding="utf-8"))
    assert receipt["freeze_commit_sha"]==accept["freeze_commit_sha"]
    assert receipt["freeze_protocol_blob_sha1"]==gitblob(ROOT/receipt["freeze_protocol_path"])
    assert receipt["verification"]["CI_run_id"]==39995420565
    for x in receipt["artifacts"]:
        assert gitblob(ROOT/x["path"])==x["git_blob_sha1"],x["path"]
    with Q0.open(newline="",encoding="utf-8") as f:oldq=list(csv.DictReader(f))
    with Q1.open(newline="",encoding="utf-8") as f:newq=list(csv.DictReader(f))
    assert len(oldq)==31 and len(newq)==30
    assert newq==[x for x in oldq if x["original_catalogue_id"]!="04-017"]
    assert Counter(x["priority"] for x in newq)=={"P1":3,"P2":27}
    assert newq[0]["original_catalogue_id"]=="04-019"
    pending={x["catalogue_id"] for x in b["rows"] if x["link_status"] in ("NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS","PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY")}
    assert {x["original_catalogue_id"] for x in newq}==pending
    print("PASS 239 original candidate invariants, one R315 04-017 change, 206 primary 30 pending, source blobs match")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--test",action="store_true");parser.add_argument("--audit",action="store_true")
    parser.parse_args();audit()
