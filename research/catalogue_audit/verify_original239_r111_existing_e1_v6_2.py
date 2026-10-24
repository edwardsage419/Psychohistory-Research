#!/usr/bin/env python3
"""Original239 v6.2 first provisional item R111 strict existing E1 scope audit."""
import hashlib
import json
from collections import Counter
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.1_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v6.2_2026-10-24.json"
ACCEPT="docs/ORIGINAL239_01-005_R111_E1_REATTRIBUTION_ACCEPTANCE.json"
RECEIPT="docs/ORIGINAL239_01-005_R111_E1_AUDIT_RECEIPT.json"

def raw(p):return (ROOT/p).read_bytes()
def blob(p):
    b=raw(p)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()

def main():
    old,new=json.loads(raw(OLD)),json.loads(raw(NEW))
    assert blob(OLD)=="2df6de5cc79b230e7958cb7acb55f06ebd1a2c12"
    assert new["base_v6_1_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [r["catalogue_id"] for r in old["rows"]]==[r["catalogue_id"] for r in new["rows"]]
    for a,b in zip(old["rows"],new["rows"]):
        if a["catalogue_id"]!="01-005":assert a==b,a["catalogue_id"]
        else:
            assert a["link_status"]=="PROVISIONAL_PRIMARY_README_LINK"
            assert b["link_status"]=="DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"
            assert b["proposed_primary_research_id"]=="R111"
            assert b["method_specific_E1_acceptance"]==ACCEPT
            assert blob(b["readme_path"])==b["readme_git_blob_sha1"]=="116580b2cc10323a93a737526c69bb8db5c9b8d2"
    a=json.loads(raw(ACCEPT))
    receipt=json.loads(raw(RECEIPT))
    assert a["status"]==receipt["evidence_grade"]=="PASS_EXISTING_BOUNDED_E1_IID_EV1_CONDITIONAL_LOGIT_ONLY"
    assert a["new_audit_CI_run_id"]==receipt["new_audit_CI_run"]==40064119855
    assert a["new_three_jobs_success"] and a["new_audit_CI_conclusion"]=="success"
    assert a["real_human_E2"]==a["historical_E3"]=="NOT_ESTABLISHED"
    assert new["counts"]==old["counts"]==dict(primary_R=236,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=0,pending_primary_R=0)
    counts=Counter(r["link_status"] for r in new["rows"])
    assert counts["PROVISIONAL_PRIMARY_README_LINK"]==new["provisional_itemwise_audit_open_count"]==172
    assert counts["DIRECT_P0_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"]==1
    assert counts["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==27
    assert dict(counts)=={k:v for k,v in new["status_counts"].items() if v>0}
    assert new["changed_original_IDs"][-1]=="01-005"
    assert new["existing_R_primary_relinked_targets"]["01-005"]=="R111"
    print("ORIGINAL239_V62_PASS 239 linked 236 primary 3 shared 0 unlinked 172 provisional R111 existing E1 bounded")

if __name__=="__main__":main()
