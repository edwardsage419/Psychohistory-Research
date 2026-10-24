#!/usr/bin/env python3
"""Original239 v6.0 R343 link, exact source and single pending item."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.9_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.0_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def raw(p):return (ROOT/p).read_bytes()
def blob(p):
    b=raw(p)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def main():
    old,new=json.loads(raw(OLD)),json.loads(raw(NEW))
    assert blob(OLD)=="fb137cf4c16fadc5179a7fa1a2d69d1ce7eb82ed"
    assert new["base_v5_9_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [x["catalogue_id"] for x in old["rows"]]==[x["catalogue_id"] for x in new["rows"]]
    for a,b in zip(old["rows"],new["rows"]):
        if a["catalogue_id"]!="04-023":assert a==b,a["catalogue_id"]
        else:
            assert a["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert b["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert b["proposed_primary_research_id"]=="R343"
            assert blob(b["readme_path"])==b["readme_git_blob_sha1"]=="efa8c6e212b611d6d8b46e3cd9f044f21e30113f"
    status=json.loads(raw("research/R343/R343_FINAL_ACCEPTANCE_STATUS.json"))
    receipt=json.loads(raw("research/R343/R343_MACHINE_RECEIPT.json"))
    assert status["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_TWO_LAYER_PROJECTION_ONLY"
    assert status["protocol_commit"]==receipt["protocol_commit"]=="85d72f14c9b386aa7ba5331d4497e6673f714773"
    assert status["source_commit"]==receipt["source_commit"]=="e9f696c084e22c5c715d8d46d3734b97e5485856"
    assert status["CI_run_id"]==receipt["verification"]["run_id"]==40063743843
    assert status["three_jobs_success"] and status["CI_conclusion"]=="success"
    assert status["real_human_E2"]==status["historical_E3"]=="NOT_ESTABLISHED"
    for p,sha in [
      ("protocols/R343_MULTIPLEX_TWO_LAYER_192_ARTIFICIAL_EDGE_ATOMS_PRESCORE_FREEZE_2026-10-24.md",receipt["protocol_blob_sha1"]),
      ("research/R343/R343_ALL_192_ARTIFICIAL_LAYER_EDGE_ATOMS.csv",receipt["artificial_source_blob_sha1"]),
      ("research/R343/R343_EXACT_64_LAYER_PAIRS.json",receipt["results_blob_sha1"]),
      ("research/R343/r343_multiplex_projection.py",receipt["production_python_blob_sha1"]),
      ("research/catalogue_audit/independent_r343_multiplex_audit.py",receipt["independent_auditor_blob_sha1"])
    ]:assert blob(p)==sha,p
    assert new["counts"]==dict(primary_R=235,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=1,pending_primary_R=1)
    counts=Counter(x["link_status"] for x in new["rows"])
    assert counts["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert counts["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==26
    assert counts["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==1
    assert dict(counts)=={k:v for k,v in new["status_counts"].items() if v>0}
    pending=[x["catalogue_id"] for x in new["rows"] if x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    queue=list(csv.DictReader(raw(QUEUE).decode().splitlines()))
    assert [x["original_catalogue_id"] for x in queue]==pending==["04-024"]
    assert new["changed_original_IDs"][-1]=="04-023" and new["E1_new_research"][-1]=="R343"
    print("ORIGINAL239_V60_PASS 239 candidates 235 primary 3 shared 1 pending 173 provisional R343 E1 only")

if __name__=="__main__":main()
