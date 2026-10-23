#!/usr/bin/env python3
"""Original239 v4.2 itemwise immutable-identity, bounded R324 and pending queue audit."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.1_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.2_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_20_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def read(path):
    return (ROOT/path).read_bytes()

def blob(path):
    data=read(path)
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()

def run():
    old=json.loads(read(OLD));new=json.loads(read(NEW))
    assert blob(OLD)=="54df5f9a476e8a301a5f25a5fbea4f341de4b130"
    assert new["base_v4_1_git_blob_sha1"]==blob(OLD)
    a=old["rows"];b=new["rows"]
    assert len(a)==len(b)==239
    assert [r["catalogue_id"] for r in a]==[r["catalogue_id"] for r in b]
    assert len(set(r["catalogue_id"] for r in b))==239
    for x,y in zip(a,b):
        if x["catalogue_id"]!="01-017":assert x==y,x["catalogue_id"]
        else:
            assert x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert y["catalogue_name_en"]=="Psychometric Paradigm of Risk Perception"
            assert y["original_priority"]=="P2"
            assert y["proposed_primary_research_id"]=="R324"
            assert y["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert blob(y["readme_path"])==y["readme_git_blob_sha1"]=="fd91966fdc719b33085065d77b1c4558e76c3b26"
    assert new["counts"]==dict(primary_R=216,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=20,pending_primary_R=20)
    c=Counter(x["link_status"] for x in b)
    assert sum(c.values())==239 and c["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert c["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==7
    assert c["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==20
    assert all(new["status_counts"][k]==v for k,v in c.items())
    q=list(csv.DictReader(read(QUEUE).decode().splitlines()))
    assert len(q)==20 and q[0]["original_catalogue_id"]=="01-020"
    assert [x["original_catalogue_id"] for x in q]==[x["catalogue_id"] for x in b if x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for path,sha in [
        ("protocols/R324_PSYCHOMETRIC_RISK_TWO_DIMENSION_64_ARTIFICIAL_STATES_PRESCORE_FREEZE_2026-10-24.md","e98ae5e41bc9799a821b33125f33b6701d05e157"),
        ("research/R324/r324_risk.py","817b1177e2024f385b4080debcedede350d0bcf3"),
        ("research/R324/R324_ALL_64_ARTIFICIAL_RISK_STATES.csv","1b0062eeea020606a3d510d566da43db03ace8d9"),
        ("research/R324/R324_EXACT_FOUR_SCORING_WORLDS.json","97c506e487fd60dfdae76fc862031803aaf911de"),
        ("research/catalogue_audit/independent_r324_risk_audit.py","24e9b846e190e3ea72d82832e81f82815f35bf1e")
    ]:assert blob(path)==sha,(path,blob(path))
    acceptance=json.loads(read("research/R324/R324_FINAL_ACCEPTANCE_STATUS.json"))
    receipt=json.loads(read("research/R324/R324_MACHINE_RECEIPT.json"))
    assert acceptance["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_RISK_COMPOSITE_ONLY"
    assert acceptance["corrected_CI_run_id"]==receipt["verification"]["corrected_CI_run_id"]==40021287400
    assert receipt["verification"]["initial_CI_conclusion"]=="failure"
    assert all(x["conclusion"]=="success" for x in receipt["verification"]["jobs"])
    assert acceptance["real_human_E2"]==acceptance["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="01-017" and new["E1_new_research"][-1]=="R324"
    print("ORIGINAL239_V42_PASS 239 original 216 primary 3 shared 20 pending 173 provisional 64 artificial R324 rows")

if __name__=="__main__":
    run()
