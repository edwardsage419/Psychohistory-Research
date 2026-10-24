#!/usr/bin/env python3
"""Original239 v5.9 R342 link, source identity and 2-item queue audit."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.8_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.9_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_2_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"

def raw(p):return (ROOT/p).read_bytes()
def blob(p):
    b=raw(p)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def main():
    old,new=json.loads(raw(OLD)),json.loads(raw(NEW))
    assert blob(OLD)=="0b874f31c34216f763039d62c038a1ff38e0a9ce"
    assert new["base_v5_8_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [r["catalogue_id"] for r in old["rows"]]==[r["catalogue_id"] for r in new["rows"]]
    for before,after in zip(old["rows"],new["rows"]):
        if before["catalogue_id"]!="04-021":
            assert before==after,before["catalogue_id"]
        else:
            assert before["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert after["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert after["proposed_primary_research_id"]=="R342"
            assert blob(after["readme_path"])==after["readme_git_blob_sha1"]=="2e1ece2a16085006589b7b3c959e272a4c668156"
    status=json.loads(raw("research/R342/R342_FINAL_ACCEPTANCE_STATUS.json"))
    receipt=json.loads(raw("research/R342/R342_MACHINE_RECEIPT.json"))
    assert status["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_THREE_ACTOR_LOCAL_CHOICE_ONLY"
    assert status["protocol_commit"]==receipt["protocol_commit"]=="a18daa73d3fc2db9f01b2a50ef70a7094bdb6e9f"
    assert status["source_commit"]==receipt["source_commit"]=="e3b94a895e16a578dbcedeaf21b4a0806a25518f"
    assert status["CI_run_id"]==receipt["verification"]["run_id"]==40063626962
    assert status["three_jobs_success"] and status["CI_conclusion"]=="success"
    assert status["real_human_E2"]==status["historical_E3"]=="NOT_ESTABLISHED"
    for p,sha in [
      ("protocols/R342_SAOM_THREE_ACTOR_1152_ARTIFICIAL_CHOICE_ATOMS_PRESCORE_FREEZE_2026-10-24.md",receipt["protocol_blob_sha1"]),
      ("research/R342/R342_ALL_1152_ARTIFICIAL_ACTOR_CHOICE_ATOMS.csv",receipt["artificial_source_blob_sha1"]),
      ("research/R342/R342_EXACT_384_LOCAL_DECISIONS.json",receipt["results_blob_sha1"]),
      ("research/R342/r342_actor_choice.py",receipt["production_python_blob_sha1"]),
      ("research/catalogue_audit/independent_r342_saom_audit.py",receipt["independent_auditor_blob_sha1"])
    ]:assert blob(p)==sha,p
    assert new["counts"]==dict(primary_R=234,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=2,pending_primary_R=2)
    counts=Counter(r["link_status"] for r in new["rows"])
    assert counts["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert counts["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==25
    assert counts["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==2
    assert dict(counts)=={k:v for k,v in new["status_counts"].items() if v>0}
    pending=[r["catalogue_id"] for r in new["rows"] if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    queue=list(csv.DictReader(raw(QUEUE).decode().splitlines()))
    assert [r["original_catalogue_id"] for r in queue]==pending==["04-023","04-024"]
    assert new["changed_original_IDs"][-1]=="04-021" and new["E1_new_research"][-1]=="R342"
    print("ORIGINAL239_V59_PASS 239 candidates 234 primary 3 shared 2 pending 173 provisional R342 E1 only")

if __name__=="__main__":main()
