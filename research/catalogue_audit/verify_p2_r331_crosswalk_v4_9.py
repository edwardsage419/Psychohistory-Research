#!/usr/bin/env python3
"""Original239 v4.9 itemwise R331 crosswalk, queue and scientific provenance audit."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.8_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.9_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_13_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def read(p):return (ROOT/p).read_bytes()
def blob(p):
    v=read(p)
    return hashlib.sha1(b"blob "+str(len(v)).encode()+b"\0"+v).hexdigest()
def run():
    old=json.loads(read(OLD))
    new=json.loads(read(NEW))
    assert blob(OLD)=="347ea8393ab2308dacbd40f2e13cc4e6352db1c9"
    assert new["base_v4_8_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [x["catalogue_id"] for x in old["rows"]]==[x["catalogue_id"] for x in new["rows"]]
    assert len({x["catalogue_id"] for x in new["rows"]})==239
    for a,b in zip(old["rows"],new["rows"]):
        if a["catalogue_id"]!="02-014":
            assert a==b,a["catalogue_id"]
        else:
            assert a["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert b["catalogue_name_en"]=="Memory Decay Models"
            assert b["original_priority"]=="P2"
            assert b["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert b["proposed_primary_research_id"]=="R331"
            assert blob(b["readme_path"])==b["readme_git_blob_sha1"]=="dfc94db20ae17898e8bed30c3a7205441957c14e"
    assert new["counts"]==dict(primary_R=223,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=13,pending_primary_R=13)
    c=Counter(x["link_status"] for x in new["rows"])
    assert sum(c.values())==239 and c["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert c["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==14
    assert c["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==13
    assert all(new["status_counts"][k]==v for k,v in c.items())
    q=list(csv.DictReader(read(QUEUE).decode().splitlines()))
    assert len(q)==13 and q[0]["original_catalogue_id"]=="02-015"
    assert [x["original_catalogue_id"] for x in q]==[x["catalogue_id"] for x in new["rows"] if x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for path,sha in [
        ("protocols/R331_HETEROGENEOUS_RETENTION_81_ATOMS_PRESCORE_FREEZE_2026-10-24.md","f25b23480d40e6bf2334777ddbe7a4b493331534"),
        ("research/R331/r331_retention_mixture.py","ff6e3feb06c554236b6531be118b8ddbaf3fa4d4"),
        ("research/R331/R331_ALL_81_ARTIFICIAL_RETENTION_ATOMS.csv","7abe55e5454b9d76e8032224455470d5610d87cf"),
        ("research/R331/R331_EXACT_9_RETENTION_WORLDS.json","30317b2e16269d89286c8a75cedb3c483b72c725"),
        ("research/catalogue_audit/independent_r331_retention_audit.py","4845cf83da4cbbf615da6507a82642923269c31f"),
        ("research/R331/R331_FINAL_ACCEPTANCE_STATUS.json","dd74cca8f210a8a6ad9d65b030ae225098a87ebb")
    ]:assert blob(path)==sha,(path,blob(path))
    receipt=json.loads(read("research/R331/R331_MACHINE_RECEIPT.json"))
    acceptance=json.loads(read("research/R331/R331_FINAL_ACCEPTANCE_STATUS.json"))
    assert receipt["protocol_commit"]==acceptance["protocol_commit"]=="fce59316d07acb73a2df5f1c6c60d7266faee4cc"
    assert receipt["verification"]["CI_run_id"]==acceptance["CI_run_id"]==40041261725
    assert receipt["verification"]["three_jobs_success"]
    assert acceptance["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_HETEROGENEOUS_RETENTION_ONLY"
    assert acceptance["real_human_E2"]==acceptance["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="02-014" and new["E1_new_research"][-1]=="R331"
    print("ORIGINAL239_V49_PASS 239 original 223 primary 3 shared 13 pending 173 provisional R331 81 artificial atoms")
if __name__=="__main__":run()
