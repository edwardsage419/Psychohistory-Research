#!/usr/bin/env python3
"""Strict original239 v6.5 R113 E1 reattribution and queue check."""
import copy
import csv
import hashlib
import json
from pathlib import Path

OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.4_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.5_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_168_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def git_blob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()

def check(old,new,root):
    if len(old["rows"])!=239 or len(new["rows"])!=239:
        raise AssertionError("CATALOGUE_COUNT")
    identity=lambda j:[(x["catalogue_id"],x["catalogue_name_en"],x["original_priority"]) for x in j["rows"]]
    if identity(old)!=identity(new):
        raise AssertionError("CATALOGUE_IDENTITY_ORDER")
    if new["base_v6_4_git_blob_sha1"]!=git_blob((root/OLD).read_bytes()):
        raise AssertionError("BASE_BLOB_IDENTITY")
    changed=[b["catalogue_id"] for a,b in zip(old["rows"],new["rows"]) if a!=b]
    if changed!=["03-007"]:
        raise AssertionError("UNEXPECTED_CHANGED_ROWS")
    if new["counts"]!=old["counts"]:
        raise AssertionError("PRIMARY_COVERAGE_CHANGED")
    if new["provisional_itemwise_audit_open_count"]!=168:
        raise AssertionError("PENDING_COUNT")
    if sum(new["status_counts"].values())!=239:
        raise AssertionError("STATUS_SUM")
    if new["status_counts"]["PROVISIONAL_PRIMARY_README_LINK"]!=168:
        raise AssertionError("PENDING_STATUS")
    row=next(r for r in new["rows"] if r["catalogue_id"]=="03-007")
    if row["proposed_primary_research_id"]!="R113" or row["link_status"]!="DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION":
        raise AssertionError("R113_LINK")
    rec=json.loads((root/row["method_specific_E1_acceptance"]).read_text(encoding="utf-8"))
    if rec["existing_primary_R"]!="R113" or rec["independent_CI_run"]!=40072087441 or rec["independent_CI_conclusion"]!="success":
        raise AssertionError("R113_CI_RECEIPT")
    if rec["new_human_E2_scores"]!=0 or rec["new_historical_E3_scores"]!=0:
        raise AssertionError("E2_E3_ESCALATION")
    if not (root/row["scientific_report_filenames"][0]).is_file():
        raise AssertionError("MISSING_REPORT")
    with (root/QUEUE).open(encoding="utf-8",newline="") as stream:
        queue=list(csv.DictReader(stream))
    expected=[r["catalogue_id"] for r in new["rows"] if r["link_status"]=="PROVISIONAL_PRIMARY_README_LINK"]
    if [r["catalogue_id"] for r in queue]!=expected:
        raise AssertionError("QUEUE_IDENTITY_ORDER")
    return {"original_candidates":239,"changed":["03-007"],"provisional_remaining":168,
            "primary_R":236,"shared_math":3,"new_E2":0,"new_E3":0,
            "status":"PASS_BOUNDED_ORIGINAL239_R113_E1_REATTRIBUTION"}

def main():
    root=Path(__file__).resolve().parents[2]
    old=json.loads((root/OLD).read_text(encoding="utf-8"))
    new=json.loads((root/NEW).read_text(encoding="utf-8"))
    result=check(old,new,root)
    neg=0
    tampered=copy.deepcopy(new)
    tampered["rows"][0]["catalogue_name_en"]="CORRUPT"
    try:
        check(old,tampered,root)
    except AssertionError:
        neg+=1
    tampered=copy.deepcopy(new)
    row=next(r for r in tampered["rows"] if r["catalogue_id"]=="03-007")
    row["proposed_primary_research_id"]="R999"
    try:
        check(old,tampered,root)
    except AssertionError:
        neg+=1
    if neg!=2:
        raise AssertionError("NEGATIVE_CONTROLS")
    result["tamper_controls_rejected"]=neg
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
