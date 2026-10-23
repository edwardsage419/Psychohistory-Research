#!/usr/bin/env python3
"""R316 original239 v3.3 single-row source and coverage proof."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
OLD=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.2_2026-10-24.json"
NEW=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.3_2026-10-24.json"
Q0=DOC/"ORIGINAL_239_PENDING_30_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
Q1=DOC/"ORIGINAL_239_PENDING_29_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def gitblob(path):
    b=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def audit():
    before=json.loads(OLD.read_text(encoding="utf-8"))
    now=json.loads(NEW.read_text(encoding="utf-8"))
    assert len(before["rows"])==len(now["rows"])==239
    assert now["base_v3_2_path"]==str(OLD.relative_to(ROOT))
    assert now["base_v3_2_git_blob_sha1"]==gitblob(OLD)
    assert now["changed_original_IDs"]==before["changed_original_IDs"]+["04-019"]
    assert now["E1_new_research"]==before["E1_new_research"]+["R316"]
    assert now["counts"]=={"primary_R":207,"shared_bounded_math":3,"older_scoped_only":1,"no_link_in_checked_sets":28,"pending_primary_R":29}
    assert sum(now["counts"][k] for k in ("primary_R","shared_bounded_math","older_scoped_only","no_link_in_checked_sets"))==239
    assert sum(now["status_counts"].values())==239
    for key,v in before["status_counts"].items():
        change=1 if key=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R" else -1 if key=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS" else 0
        assert now["status_counts"][key]==v+change
    changed=[];ids=[]
    for a,b in zip(before["rows"],now["rows"]):
        for k in ("catalogue_id","catalogue_name_en","original_priority","catalogue_category"):
            assert a[k]==b[k]
        ids.append(b["catalogue_id"])
        if a!=b:changed.append(a["catalogue_id"])
    assert len(set(ids))==239 and changed==["04-019"]
    r=next(x for x in now["rows"] if x["catalogue_id"]=="04-019")
    assert r["catalogue_name_en"]=="Stochastic Block Model"
    assert r["proposed_primary_research_id"]=="R316"
    assert r["original_priority"]=="P1"
    assert r["readme_git_blob_sha1"]==gitblob(ROOT/r["readme_path"])
    assert (ROOT/r["scientific_report_filenames"][0]).is_file()
    accept=json.loads((ROOT/r["method_specific_E1_acceptance"]).read_text(encoding="utf-8"))
    assert accept["research_id"]=="R316" and accept["status"]=="PASS_BOUNDED_E1_ONLY"
    assert accept["actual_CI_run_id"]==39995863890 and accept["live_CI_conclusion"]=="success"
    assert accept["human_E2"]=="NOT_ESTABLISHED" and accept["historical_E3"]=="NOT_ESTABLISHED"
    receipt=json.loads((ROOT/"research/R316/R316_MACHINE_RECEIPT.json").read_text(encoding="utf-8"))
    assert receipt["prescore_commit"]==accept["prescore_commit"]
    assert receipt["prescore_blob_sha1"]==gitblob(ROOT/receipt["prescore_path"])
    assert receipt["verification"]["run_id"]==39995863890
    assert len(receipt["verification"]["jobs"])==3
    for artifact in receipt["artifacts"]:
        assert artifact["git_blob_sha1"]==gitblob(ROOT/artifact["path"]),artifact["path"]
    with Q0.open(newline="",encoding="utf-8") as f:prev=list(csv.DictReader(f))
    with Q1.open(newline="",encoding="utf-8") as f:nxt=list(csv.DictReader(f))
    assert len(prev)==30 and len(nxt)==29
    assert nxt==[x for x in prev if x["original_catalogue_id"]!="04-019"]
    assert Counter(x["priority"] for x in nxt)=={"P1":2,"P2":27}
    assert nxt[0]["original_catalogue_id"]=="04-022"
    no_main={x["catalogue_id"] for x in now["rows"] if x["link_status"] in ("NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS","PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY")}
    assert {x["original_catalogue_id"] for x in nxt}==no_main
    print("PASS original239 v3.3: single 04-019 source change, 207 main, 29 pending, all R316 source blobs verified")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true");p.add_argument("--audit",action="store_true")
    p.parse_args();audit()
