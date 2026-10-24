#!/usr/bin/env python3
"""Strict v6.3 to v6.4 original239 evidence reattribution audit, standard library."""
from __future__ import annotations
import copy
import csv
import hashlib
import json
from pathlib import Path

BASE="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.3_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.4_2026-10-24.json"
EXPECTED={"03-005":("R116",40067493660),"03-006":("R115",40071792992)}

def gitblob(raw):
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+bytes([0])+raw).hexdigest()

def validate(old,new,root):
    if len(old["rows"])!=239 or len(new["rows"])!=239:
        raise AssertionError("ORIGINAL239_SIZE")
    identity=lambda j:[(x["catalogue_id"],x["catalogue_name_en"],x["original_priority"]) for x in j["rows"]]
    if identity(old)!=identity(new):
        raise AssertionError("ORIGINAL239_IDENTITY_ORDER")
    if new["base_v6_3_git_blob_sha1"]!=gitblob((root/BASE).read_bytes()):
        raise AssertionError("BASE_GIT_BLOB_MISMATCH")
    if new["provisional_itemwise_audit_open_count"]!=169:
        raise AssertionError("PROVISIONAL_COUNT")
    if new["status_counts"]["PROVISIONAL_PRIMARY_README_LINK"]!=169:
        raise AssertionError("PROVISIONAL_STATUS_COUNT")
    if sum(new["status_counts"].values())!=239:
        raise AssertionError("STATUS_TOTAL")
    if new["counts"]!=old["counts"]:
        raise AssertionError("PRIMARY_COVERAGE_CHANGED")
    queue_path=root/"docs/ORIGINAL_239_PENDING_169_ITEMWISE_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
    with queue_path.open(encoding="utf-8",newline="") as stream:
        queue=list(csv.DictReader(stream))
    expected_pending=[r["catalogue_id"] for r in new["rows"]
                      if r["link_status"]=="PROVISIONAL_PRIMARY_README_LINK"]
    if [r["catalogue_id"] for r in queue]!=expected_pending:
        raise AssertionError("PENDING_QUEUE_IDENTITY_OR_ORDER")
    if any(r["current_status"]!="PROVISIONAL_PRIMARY_README_LINK" for r in queue):
        raise AssertionError("PENDING_QUEUE_STATUS")
    changed=[]
    for a,b in zip(old["rows"],new["rows"]):
        if a!=b:
            changed.append(b["catalogue_id"])
    if set(changed)!=set(EXPECTED) or len(changed)!=2:
        raise AssertionError("UNEXPECTED_ROW_MUTATION")
    for id,(research,run) in EXPECTED.items():
        row=next(x for x in new["rows"] if x["catalogue_id"]==id)
        if row["proposed_primary_research_id"]!=research:
            raise AssertionError("RESEARCH_ID_MISMATCH")
        if row["link_status"]!="DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION":
            raise AssertionError("DIRECT_STATUS_MISMATCH")
        if row["P1_scoped_review_addendum"]["CI_run_id"]!=run:
            raise AssertionError("CI_RUN_MISMATCH")
        receipt=root/row["method_specific_E1_acceptance"]
        data=json.loads(receipt.read_text(encoding="utf-8"))
        if data["existing_primary_R"]!=research or data["independent_CI_run"]!=run:
            raise AssertionError("RECEIPT_IDENTITY_MISMATCH")
        if data["independent_CI_conclusion"]!="success":
            raise AssertionError("CI_NOT_SUCCESS")
        if data["new_human_E2"]!=0 or data["new_historical_E3"]!=0:
            raise AssertionError("E2_E3_GRADE_ESCALATION")
        if data["scientific_grade"]!="PASS_BOUNDED_INTERNAL_INDEPENDENT_METHOD_E1":
            raise AssertionError("E1_GRADE_MISMATCH")
        if not (root/row["scientific_report_filenames"][0]).is_file():
            raise AssertionError("MISSING_SCIENTIFIC_REPORT")
    return {"original_candidates":239,"changed_only":["03-005","03-006"],
            "provisional_remaining":169,"primary_R_links":236,
            "shared_bounded_math":3,"new_human_E2":0,"new_historical_E3":0,
            "acceptance":"PASS_BOUNDED_CROSSWALK_PROVENANCE_AND_E1_SCOPE"}

def main():
    root=Path(__file__).resolve().parents[2]
    old=json.loads((root/BASE).read_text(encoding="utf-8"))
    new=json.loads((root/NEW).read_text(encoding="utf-8"))
    result=validate(old,new,root)
    corrupt=copy.deepcopy(new)
    corrupt["rows"][0]["catalogue_name_en"]="CORRUPTED"
    rejected=0
    try:
        validate(old,corrupt,root)
    except AssertionError:
        rejected+=1
    corrupt=copy.deepcopy(new)
    row=next(x for x in corrupt["rows"] if x["catalogue_id"]=="03-006")
    row["P1_scoped_review_addendum"]["CI_run_id"]=0
    try:
        validate(old,corrupt,root)
    except AssertionError:
        rejected+=1
    if rejected!=2:
        raise AssertionError("NEGATIVE_CONTROLS_FAILED")
    result["tamper_controls_rejected"]=rejected
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=="__main__":
    main()
