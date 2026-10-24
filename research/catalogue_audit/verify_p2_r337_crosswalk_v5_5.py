#!/usr/bin/env python3
"""Original239 v5.5 strict itemwise R337 provenance and queue checks."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.4_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.5_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_7_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def data(path):return (ROOT/path).read_bytes()
def blob(path):
    b=data(path)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def main():
    old=json.loads(data(OLD)); new=json.loads(data(NEW))
    assert blob(OLD)=="fbfc9b4a45304f24638cfb264ecdc8894ae7a334"
    assert new["base_v5_4_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [x["catalogue_id"] for x in old["rows"]]==[x["catalogue_id"] for x in new["rows"]]
    assert len(set(x["catalogue_id"] for x in new["rows"]))==239
    for a,b in zip(old["rows"],new["rows"]):
        if a["catalogue_id"]!="03-015":assert a==b,a["catalogue_id"]
        else:
            assert a["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert b["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert b["proposed_primary_research_id"]=="R337"
            assert blob(b["readme_path"])==b["readme_git_blob_sha1"]=="b38f4e7f7e838bf8371bb4713de7365799b38edc"
            assert b["method_specific_E1_acceptance"]=="research/R337/R337_FINAL_ACCEPTANCE_STATUS.json"
    assert new["counts"]==dict(primary_R=229,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=7,pending_primary_R=7)
    statuses=Counter(x["link_status"] for x in new["rows"])
    assert sum(statuses.values())==239
    assert statuses["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert statuses["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==20
    assert statuses["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==7
    assert dict(statuses)=={k:v for k,v in new["status_counts"].items() if v>0}
    queue=list(csv.DictReader(data(QUEUE).decode().splitlines()))
    assert len(queue)==7 and queue[0]["original_catalogue_id"]=="03-017"
    assert [x["original_catalogue_id"] for x in queue]==[x["catalogue_id"] for x in new["rows"] if x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for p,sha in [
      ("protocols/R337_ELM_64_ARTIFICIAL_ARGUMENT_CUE_ATOMS_PRESCORE_FREEZE_2026-10-24.md","1f98d653400ec2661edc2675e6396be8593cf0a2"),
      ("research/R337/r337_elm.py","96e9e2be1b7d7ac0ac7b3cfcf05c7c81e938090d"),
      ("research/R337/R337_ALL_64_ARTIFICIAL_ARGUMENT_CUE_ATOMS.csv","e711da9e296693037e5a87def3604b3fe53025e8"),
      ("research/R337/R337_EXACT_32_CONDITIONS.json","5061ce0d74a9703e9a11ef2180395066a99aca1f"),
      ("research/catalogue_audit/independent_r337_elm_audit.py","db952978d4e71bc3cbba61915c44e96c3d629af7")
    ]:assert blob(p)==sha,(p,blob(p))
    a=json.loads(data("research/R337/R337_FINAL_ACCEPTANCE_STATUS.json"))
    receipt=json.loads(data("research/R337/R337_MACHINE_RECEIPT.json"))
    assert a["protocol_commit"]==receipt["protocol_commit"]=="c26ded95a844908d692f069c1a11ac1934b15487"
    assert a["source_commit"]==receipt["source_commit"]=="7f7a44f9596acb5d06ffe4d51677e59d75a5f357"
    assert a["CI_run_id"]==receipt["verification"]["run_id"]==40055959491
    assert a["three_jobs_success"] and a["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_BINARY_ELM_GATE_ONLY"
    assert a["real_human_E2"]==a["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="03-015" and new["E1_new_research"][-1]=="R337"
    print("ORIGINAL239_V55_PASS 239 original 229 primary 3 shared 7 pending 173 provisional R337 64 artificial atoms")
if __name__=="__main__":main()
