#!/usr/bin/env python3
"""Original239 v4.8 exact R330 source and itemwise metadata audit."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.7_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.8_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_14_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def read(p):return (ROOT/p).read_bytes()
def blob(p):
    b=read(p)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def run():
    old=json.loads(read(OLD));new=json.loads(read(NEW))
    assert blob(OLD)=="72fe6717d489453212f23009fe01ad66c4b1c5e3"
    assert new["base_v4_7_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [r["catalogue_id"] for r in old["rows"]]==[r["catalogue_id"] for r in new["rows"]]
    assert len({r["catalogue_id"] for r in new["rows"]})==239
    for a,b in zip(old["rows"],new["rows"]):
        if a["catalogue_id"]!="02-013": assert a==b,a["catalogue_id"]
        else:
            assert a["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert b["catalogue_name_en"]=="Instance Based Learning" and b["original_priority"]=="P2"
            assert b["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert b["proposed_primary_research_id"]=="R330"
            assert blob(b["readme_path"])==b["readme_git_blob_sha1"]=="60d2a28daa0a8969da5c829db38b52f717ca91ff"
    assert new["counts"]==dict(primary_R=222,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=14,pending_primary_R=14)
    c=Counter(r["link_status"] for r in new["rows"])
    assert sum(c.values())==239 and c["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert c["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==13
    assert c["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==14
    assert all(new["status_counts"][k]==v for k,v in c.items())
    q=list(csv.DictReader(read(QUEUE).decode().splitlines()))
    assert len(q)==14 and q[0]["original_catalogue_id"]=="02-014"
    assert [r["original_catalogue_id"] for r in q]==[r["catalogue_id"] for r in new["rows"] if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for path,sha in [
        ("protocols/R330_FOUR_INSTANCE_CUE_RECENCY_256_ATOMS_PRESCORE_FREEZE_2026-10-24.md","fd73ccb03726c26b2db8a4b0e88b0258cb7c39f6"),
        ("research/R330/r330_instance_retrieval.py","a61f49f47f81ed12d89b856038e00f853d4156ce"),
        ("research/R330/R330_ALL_256_ARTIFICIAL_MEMORY_ATOMS.csv","209067b67e45b4cbf9976ffcfb1cd78800fe8655"),
        ("research/R330/R330_EXACT_64_RETRIEVAL_WORLDS.json","c0ede1e2bedbd914cf5005c678370e0c8916466a"),
        ("research/catalogue_audit/independent_r330_instance_retrieval_audit.py","3ee6bddcbf3c41e684119c26333bcb01a1cdd7a7")
    ]:assert blob(path)==sha,(path,blob(path))
    receipt=json.loads(read("research/R330/R330_MACHINE_RECEIPT.json"))
    acceptance=json.loads(read("research/R330/R330_FINAL_ACCEPTANCE_STATUS.json"))
    assert receipt["protocol_commit"]=="0d51148a63e16abdc9505e2c57fab0488e27e0b5"
    assert receipt["verification"]["CI_run_id"]==acceptance["CI_run_id"]==40035835578
    assert receipt["verification"]["three_jobs_success"]
    assert acceptance["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_FOUR_INSTANCE_RETRIEVAL_ONLY"
    assert acceptance["real_human_E2"]==acceptance["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="02-013" and new["E1_new_research"][-1]=="R330"
    print("ORIGINAL239_V48_PASS 239 original 222 primary 3 shared 14 pending 173 provisional R330 256 artificial atoms")
if __name__=="__main__":run()
