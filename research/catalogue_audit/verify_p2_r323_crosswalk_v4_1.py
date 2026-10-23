#!/usr/bin/env python3
"""Verify original239 v4.1 row identity, R323 source hashes and pending queue."""
import csv,hashlib,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):return (ROOT/p).read_bytes()
def blob(p):
    b=read(p);return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def run():
    oldp="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.0_2026-10-24.json"
    newp="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.1_2026-10-24.json"
    old=json.loads(read(oldp));new=json.loads(read(newp))
    assert blob(oldp)=="7277dcc00af0d10eaaa7007bd731d399addbde83"
    assert new["base_v4_0_git_blob_sha1"]==blob(oldp)
    assert len(old["rows"])==len(new["rows"])==239
    a={r["catalogue_id"]:r for r in old["rows"]}
    b={r["catalogue_id"]:r for r in new["rows"]}
    assert list(a)==list(b) and len(a)==239
    assert all(a[k]==b[k] for k in a if k!="01-015")
    target=b["01-015"]
    assert target["catalogue_name_en"]=="Value Belief Norm Theory"
    assert target["proposed_primary_research_id"]=="R323"
    assert target["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
    assert target["original_priority"]=="P2"
    assert blob(target["readme_path"])==target["readme_git_blob_sha1"]=="e24f162ce160a8ab31ea70bab48342a82a926963"
    assert new["counts"]["primary_R"]==215
    assert new["counts"]["shared_bounded_math"]==3
    assert new["counts"]["pending_primary_R"]==new["counts"]["no_link_in_checked_sets"]==21
    counts=Counter(x["link_status"] for x in new["rows"])
    assert sum(counts.values())==239
    assert counts["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==21
    assert counts["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==6
    assert counts["PROVISIONAL_PRIMARY_README_LINK"]==173
    for status,count in counts.items():assert new["status_counts"][status]==count
    pending=list(csv.DictReader(read("docs/ORIGINAL_239_PENDING_21_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv").decode().splitlines()))
    assert len(pending)==21 and pending[0]["original_catalogue_id"]=="01-017"
    assert [x["original_catalogue_id"] for x in pending]==[x["catalogue_id"] for x in new["rows"] if x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for path,sha in (
        ("protocols/R323_VALUE_BELIEF_NORM_MEDIATION_IDENTIFICATION_128_STATES_PRESCORE_FREEZE_2026-10-24.md","9130b0be7b1d7c5b9c47007822ff59bf4e281e41"),
        ("research/R323/r323_vbn.py","dd43f71ede4dcc5e7aeda90881aa74feee3d5ced"),
        ("research/R323/R323_ALL_128_ORIGINAL_VBN_STATES.csv","1b92efb314aae036e773be92e28793f8fcd60809"),
        ("research/R323/R323_EXACT_FOUR_VBN_WORLDS.json","c97770fe90390d9347f02e2d259c44fa30225c96"),
        ("research/catalogue_audit/independent_r323_vbn_audit.py","b4caf88b22025641b7d5b6738f59fdbcefc18626")):
        assert blob(path)==sha,(path,blob(path))
    receipt=json.loads(read("research/R323/R323_MACHINE_RECEIPT.json"))
    acceptance=json.loads(read("research/R323/R323_FINAL_ACCEPTANCE_STATUS.json"))
    assert receipt["protocol_commit"]=="54aee0ea3e5153396b167249ce7f75afa95a6756"
    assert receipt["original_source_commit"]=="0e560dc9be36534a65e8325dcc18d06adb12a341"
    assert receipt["verification"]["CI_run_id"]==40015028540
    assert all(x["conclusion"]=="success" for x in receipt["verification"]["jobs"])
    assert acceptance["status"]=="PASS_BOUNDED_E1_SCHEMATIC_VBN_MEDIATION_ONLY"
    assert acceptance["real_human_E2"]=="NOT_ESTABLISHED" and acceptance["historical_E3"]=="NOT_ESTABLISHED"
    assert "R323" in new["E1_new_research"] and new["changed_original_IDs"][-1]=="01-015"
    print("ORIGINAL239_V41_PASS 239 original rows 215 primary 3 shared 21 pending 173 provisional 128 E1 states")
if __name__=="__main__":run()
