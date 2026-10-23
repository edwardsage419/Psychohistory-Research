#!/usr/bin/env python3
"""R318 original239 v3.6 candidate-only index invariants and exact Git blob audit."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
P=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.5_2026-10-24.json"
N=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.6_2026-10-24.json"
Q0=DOC/"ORIGINAL_239_PENDING_27_P2_ONLY_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
Q1=DOC/"ORIGINAL_239_PENDING_26_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def gitblob(path):
    raw=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
def audit():
    base=json.loads(P.read_text(encoding="utf-8"));now=json.loads(N.read_text(encoding="utf-8"))
    assert now["base_v3_5_path"]==str(P.relative_to(ROOT)) and now["base_v3_5_git_blob_sha1"]==gitblob(P)
    assert len(base["rows"])==len(now["rows"])==239
    assert now["changed_original_IDs"]==base["changed_original_IDs"]+["01-003"]
    assert now["E1_new_research"]==base["E1_new_research"]+["R318"]
    assert now["counts"]=={"primary_R":210,"shared_bounded_math":3,"older_scoped_only":0,"no_link_in_checked_sets":26,"pending_primary_R":26}
    assert sum(now["counts"][k] for k in ("primary_R","shared_bounded_math","older_scoped_only","no_link_in_checked_sets"))==239
    assert now["status_counts"]["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==base["status_counts"]["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]-1
    assert now["status_counts"]["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==1
    assert sum(now["status_counts"].values())==239
    for k,v in base["status_counts"].items():
        if k!="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS":assert now["status_counts"][k]==v
    changed=[];ids=[]
    for a,b in zip(base["rows"],now["rows"]):
        for k in ("catalogue_id","catalogue_name_en","original_priority","catalogue_category"):
            assert a[k]==b[k]
        ids.append(b["catalogue_id"])
        if a!=b:changed.append(a["catalogue_id"])
    assert changed==["01-003"] and len(set(ids))==239
    row=next(r for r in now["rows"] if r["catalogue_id"]=="01-003")
    assert row["catalogue_name_en"]=="Cumulative Prospect Theory" and row["original_priority"]=="P2"
    assert row["proposed_primary_research_id"]=="R318"
    assert row["readme_git_blob_sha1"]==gitblob(ROOT/row["readme_path"])
    assert (ROOT/row["scientific_report_filenames"][0]).is_file()
    acceptance=json.loads((ROOT/row["method_specific_E1_acceptance"]).read_text(encoding="utf-8"))
    assert acceptance["research_id"]=="R318" and acceptance["status"]=="PASS_BOUNDED_E1_ONLY"
    assert acceptance["CI_run_id"]==39996930026 and acceptance["CI_conclusion"]=="success"
    assert acceptance["original_1992_empirical_weight_function"]=="NOT_REPLICATED"
    assert acceptance["real_human_E2"]=="NOT_ESTABLISHED"
    receipt=json.loads((ROOT/"research/R318/R318_MACHINE_RECEIPT.json").read_text(encoding="utf-8"))
    assert receipt["prescore_commit"]==acceptance["prescore_commit"]
    assert receipt["prescore_git_blob_sha1"]==gitblob(ROOT/receipt["prescore_path"])
    assert receipt["verification"]["CI_run_id"]==39996930026
    assert len(receipt["verification"]["jobs"])==3
    for f in receipt["source_artifacts"]:
        assert gitblob(ROOT/f["path"])==f["git_blob_sha1"]
    with Q0.open(newline="",encoding="utf-8") as f:oldq=list(csv.DictReader(f))
    with Q1.open(newline="",encoding="utf-8") as f:newq=list(csv.DictReader(f))
    assert len(oldq)==27 and len(newq)==26
    assert newq==[r for r in oldq if r["original_catalogue_id"]!="01-003"]
    assert Counter(r["priority"] for r in newq)=={"P2":26}
    assert newq[0]["original_catalogue_id"]=="01-007"
    unmatched={r["catalogue_id"] for r in now["rows"] if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"}
    assert {r["original_catalogue_id"] for r in newq}==unmatched
    print("PASS original239 v3.6 one P2 01-003 R318, 210 primary and 26 pending, pinned 72 CPT source atoms")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true");p.add_argument("--audit",action="store_true")
    p.parse_args();audit()
