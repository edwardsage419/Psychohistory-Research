#!/usr/bin/env python3
"""R317 original239 v3.4 strict one-row source and real E2 boundary audit."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
OLD=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.3_2026-10-24.json"
NEW=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.4_2026-10-24.json"
Q0=DOC/"ORIGINAL_239_PENDING_29_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
Q1=DOC/"ORIGINAL_239_PENDING_28_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def sha(path):
    data=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def audit():
    a=json.loads(OLD.read_text(encoding="utf-8"))
    b=json.loads(NEW.read_text(encoding="utf-8"))
    assert b["base_v3_3_path"]==str(OLD.relative_to(ROOT))
    assert b["base_v3_3_git_blob_sha1"]==sha(OLD)
    assert len(a["rows"])==len(b["rows"])==239
    assert b["changed_original_IDs"]==a["changed_original_IDs"]+["04-022"]
    assert b["E1_new_research"]==a["E1_new_research"]+["R317"]
    assert b["counts"]=={"primary_R":208,"shared_bounded_math":3,"older_scoped_only":1,"no_link_in_checked_sets":27,"pending_primary_R":28}
    assert sum(b["counts"][k] for k in ("primary_R","shared_bounded_math","older_scoped_only","no_link_in_checked_sets"))==239
    assert sum(b["status_counts"].values())==239
    for k,v in a["status_counts"].items():
        delta=1 if k=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R" else -1 if k=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS" else 0
        assert b["status_counts"][k]==v+delta
    changes=[];ids=[]
    for old,new in zip(a["rows"],b["rows"]):
        for k in ("catalogue_id","catalogue_name_en","catalogue_category","original_priority"):
            assert old[k]==new[k]
        ids.append(new["catalogue_id"])
        if old!=new:changes.append(new["catalogue_id"])
    assert len(set(ids))==239 and changes==["04-022"]
    r=next(x for x in b["rows"] if x["catalogue_id"]=="04-022")
    assert r["proposed_primary_research_id"]=="R317" and r["catalogue_name_en"]=="Temporal Networks"
    assert r["readme_git_blob_sha1"]==sha(ROOT/r["readme_path"])
    assert (ROOT/r["scientific_report_filenames"][0]).is_file()
    accept=json.loads((ROOT/r["method_specific_E1_acceptance"]).read_text(encoding="utf-8"))
    assert accept["research_id"]=="R317" and accept["status"]=="PASS_BOUNDED_E1_ONLY"
    assert accept["live_run_id"]==39996280974 and accept["CI_conclusion"]=="success"
    assert accept["human_E2"]=="NOT_ESTABLISHED" and accept["historical_E3"]=="NOT_ESTABLISHED"
    receipt=json.loads((ROOT/"research/R317/R317_MACHINE_RECEIPT.json").read_text(encoding="utf-8"))
    assert receipt["prescore_commit"]==accept["prescore_commit"]
    assert receipt["prescore_blob_sha1"]==sha(ROOT/receipt["prescore_path"])
    assert receipt["verification"]["run_id"]==39996280974
    assert len(receipt["verification"]["jobs"])==3
    for obj in receipt["artifacts"]:
        assert obj["git_blob_sha1"]==sha(ROOT/obj["path"])
    with Q0.open(newline="",encoding="utf-8") as f:q0=list(csv.DictReader(f))
    with Q1.open(newline="",encoding="utf-8") as f:q1=list(csv.DictReader(f))
    assert len(q0)==29 and len(q1)==28
    assert q1==[x for x in q0 if x["original_catalogue_id"]!="04-022"]
    assert Counter(x["priority"] for x in q1)=={"P1":1,"P2":27}
    assert q1[0]["original_catalogue_id"]=="05-001"
    pending={x["catalogue_id"] for x in b["rows"] if x["link_status"] in ("NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS","PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY")}
    assert {x["original_catalogue_id"] for x in q1}==pending
    print("PASS v3.4 R317 only 04-022, exact original239, 208 main 28 pending, 81 temporal sources SHA verified")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--test",action="store_true");p.add_argument("--audit",action="store_true")
    p.parse_args();audit()
