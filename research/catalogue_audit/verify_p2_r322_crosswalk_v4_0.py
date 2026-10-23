#!/usr/bin/env python3
"""Verify original239 v4.0 row identity, R322 source hashes and pending queue."""
import csv,hashlib,json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
def read(p):return (ROOT/p).read_bytes()
def blob(p):
    b=read(p);return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def run():
    oldp="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.9_2026-10-24.json"
    newp="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.0_2026-10-24.json"
    old=json.loads(read(oldp));new=json.loads(read(newp))
    assert blob(oldp)=="32845c8f514a2ded8d3b0cebbb4a653f8c96d17d"
    assert new["base_v3_9_git_blob_sha1"]==blob(oldp)
    assert len(old["rows"])==len(new["rows"])==239
    a={r["catalogue_id"]:r for r in old["rows"]}
    b={r["catalogue_id"]:r for r in new["rows"]}
    assert list(a)==list(b) and len(a)==239
    assert all(a[k]==b[k] for k in a if k!="01-012")
    target=b["01-012"]
    assert target["catalogue_name_en"]=="Dual Process Accounts"
    assert target["proposed_primary_research_id"]=="R322"
    assert target["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
    assert target["original_priority"]=="P2"
    assert blob(target["readme_path"])==target["readme_git_blob_sha1"]=="ed86f58108ae7cda663edbf9314ca9fd4a6fa6f9"
    assert new["counts"]["primary_R"]==214
    assert new["counts"]["shared_bounded_math"]==3
    assert new["counts"]["pending_primary_R"]==new["counts"]["no_link_in_checked_sets"]==22
    counts=Counter(x["link_status"] for x in new["rows"])
    assert sum(counts.values())==239
    assert counts["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==22
    assert counts["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==5
    assert counts["PROVISIONAL_PRIMARY_README_LINK"]==173
    for status,count in counts.items():assert new["status_counts"][status]==count
    pending=list(csv.DictReader(read("docs/ORIGINAL_239_PENDING_22_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv").decode().splitlines()))
    assert len(pending)==22 and pending[0]["original_catalogue_id"]=="01-015"
    assert [x["original_catalogue_id"] for x in pending]==[x["catalogue_id"] for x in new["rows"] if x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for path,sha in (
        ("protocols/R322_TYPE1_DEFAULT_TYPE2_INTERVENTION_256_STATES_PRESCORE_FREEZE_2026-10-24.md","685f637d5ad42351de50977f04249ffe30b443eb"),
        ("research/R322/r322_dual_process.py","af24e8656383515934ce51faef6ae2e3d5d7f156"),
        ("research/R322/R322_ALL_256_ORIGINAL_BINARY_STATES.csv","0cd38ecc22adc5941832c2b00e6928d48be8d896"),
        ("research/R322/R322_EXACT_FOUR_POLICY_WORLDS.json","9087e53b1abe11a8eb21c2ef44440f373ad57d53"),
        ("research/catalogue_audit/independent_r322_dual_process_audit.py","638c9d55054f596df697086d881e9ad9be4e3b69")):
        assert blob(path)==sha,(path,blob(path))
    receipt=json.loads(read("research/R322/R322_MACHINE_RECEIPT.json"))
    acceptance=json.loads(read("research/R322/R322_FINAL_ACCEPTANCE_STATUS.json"))
    assert receipt["protocol_commit"]=="98cd278861258cfa1697bca9a8eb122ebafbb74b"
    assert receipt["original_source_commit"]=="87ddd735890286f7117757b95b9a7b31277c674d"
    assert receipt["verification"]["CI_run_id"]==40014627376
    assert all(x["conclusion"]=="success" for x in receipt["verification"]["jobs"])
    assert acceptance["status"]=="PASS_BOUNDED_E1_SCHEMATIC_DEFAULT_INTERVENTION_IDENTIFICATION_ONLY"
    assert acceptance["real_human_E2"]=="NOT_ESTABLISHED" and acceptance["historical_E3"]=="NOT_ESTABLISHED"
    assert "R322" in new["E1_new_research"] and new["changed_original_IDs"][-1]=="01-012"
    print("ORIGINAL239_V40_PASS 239 original rows 214 primary 3 shared 22 pending 173 provisional 256 E1 states")
if __name__=="__main__":run()
