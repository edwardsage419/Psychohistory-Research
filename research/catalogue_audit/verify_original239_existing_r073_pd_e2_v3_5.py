#!/usr/bin/env python3
"""Original239 v3.5 PD reattribution: verify existing evidence, no new score."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
OLD=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.4_2026-10-24.json"
NEW=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.5_2026-10-24.json"
Q0=DOC/"ORIGINAL_239_PENDING_28_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
Q1=DOC/"ORIGINAL_239_PENDING_27_P2_ONLY_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
E73=ROOT/"research/R073/R073_FINAL_ACCEPTANCE_STATUS.json"
E106=ROOT/"research/R106/R106_FINAL_ACCEPTANCE_STATUS.json"
E110=ROOT/"research/R110/R110_PHASE_C0_LIVE_CI_2015_UCL_ACTOR_PEER_SIGNAL_MATCHED_SHRINK_SHAM_E2_OR_BOUNDED_FAILURE.json"
def sha(path):
    v=path.read_bytes()
    return hashlib.sha1(b"blob "+str(len(v)).encode()+b"\0"+v).hexdigest()
def audit():
    base=json.loads(OLD.read_text(encoding="utf-8"))
    now=json.loads(NEW.read_text(encoding="utf-8"))
    assert now["base_v3_4_path"]==str(OLD.relative_to(ROOT))
    assert now["base_v3_4_git_blob_sha1"]==sha(OLD)
    assert len(base["rows"])==len(now["rows"])==239
    assert now["changed_original_IDs"]==base["changed_original_IDs"]+["05-001"]
    assert now["E1_new_research"]==base["E1_new_research"] # no new models
    assert now["existing_R_primary_relinked_IDs"]==base["existing_R_primary_relinked_IDs"]+["05-001"]
    for k in base["existing_R_primary_relinked_targets"]:
        assert now["existing_R_primary_relinked_targets"][k]==base["existing_R_primary_relinked_targets"][k]
    assert now["existing_R_primary_relinked_targets"]["05-001"]=="R073"
    assert now["counts"]=={"primary_R":209,"shared_bounded_math":3,"older_scoped_only":0,"no_link_in_checked_sets":27,"pending_primary_R":27}
    assert sum(now["counts"][k] for k in ("primary_R","shared_bounded_math","older_scoped_only","no_link_in_checked_sets"))==239
    assert sum(now["status_counts"].values())==239
    for k,v in base["status_counts"].items():
        assert now["status_counts"][k]==(0 if k=="PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY" else v)
    assert now["status_counts"]["DIRECT_P1_BOUNDED_E2_REAL_HUMAN_REPEATED_PD_EXISTING_R073_REATTRIBUTION"]==1
    changed=[];seen=set()
    for x,y in zip(base["rows"],now["rows"]):
        for k in ("catalogue_id","catalogue_name_en","catalogue_category","original_priority"):
            assert x[k]==y[k]
        assert y["catalogue_id"] not in seen;seen.add(y["catalogue_id"])
        if x!=y:changed.append(x["catalogue_id"])
    assert changed==["05-001"]
    row=next(x for x in now["rows"] if x["catalogue_id"]=="05-001")
    assert row["proposed_primary_research_id"]=="R073" and row["original_priority"]=="P1"
    assert row["readme_git_blob_sha1"]==sha(ROOT/row["readme_path"])=="88ca2775873d02e6c408ffb667bd44e3623bd5de"
    assert sha(E73)=="4dcd30a7b47cc0f81ff186541d791474a3e2e0e9"
    assert sha(E106)=="ad7b328a7a2fb7a3a5aa2cd9eb33fd4bd7dc68ad"
    assert sha(E110)=="f142b5b7917986fee9c2da1e585d4e8d23f7bea4"
    x=json.loads(E73.read_text(encoding="utf-8"))
    assert x["research_id"]=="R073" and x["research_status"]=="CLOSED_BOUNDED"
    assert x["study_type"]=="REAL_HUMAN_OBSERVATIONAL_HELDOUT_CONDITIONAL_PREDICTION_E2"
    assert x["experiment"]["sessions"]==12 and x["experiment"]["humans"]==188
    assert x["experiment"]["scored_human_t3_to_t100"]==18424
    assert x["execution"]["true_human_workflow_run"]==38931506064
    assert x["execution"]["independent_full_original_replay_workflow_run"]==38931698718
    assert x["source"]["source_vs_final_Dryad"]=="UNKNOWN"
    assert x["limitations"]["causal_effect_of_opponent_behavior"]=="NOT_IDENTIFIED"
    y=json.loads(E106.read_text(encoding="utf-8"))
    assert y["R073_exact_frozen_model_replication"] is False
    z=json.loads(E110.read_text(encoding="utf-8"))
    assert z["real_human_model_scores"]==0 and "FAIL_CLOSED" in z["status"]
    assert row["P1_scoped_review_addendum"]["new_E2_subjects"]==0
    assert row["P1_scoped_review_addendum"]["new_E3"]==0
    with Q0.open(newline="",encoding="utf-8") as f:a=list(csv.DictReader(f))
    with Q1.open(newline="",encoding="utf-8") as f:b=list(csv.DictReader(f))
    assert len(a)==28 and len(b)==27
    assert b==[r for r in a if r["original_catalogue_id"]!="05-001"]
    assert Counter(r["priority"] for r in b)=={"P2":27}
    assert b[0]["original_catalogue_id"]=="01-003"
    pending={r["catalogue_id"] for r in now["rows"] if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"}
    assert {r["original_catalogue_id"] for r in b}==pending
    print("PASS original239 v3.5 only 05-001 existing R073 E2, R106 distinct, R110 fail closed, 209 main 27 P2 pending; zero new E2")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    p.add_argument("--audit",action="store_true");p.add_argument("--test",action="store_true")
    p.parse_args();audit()
