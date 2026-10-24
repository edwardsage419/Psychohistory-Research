#!/usr/bin/env python3
"""Original239 v5.7 strict R339 itemwise link and five-item pending queue audit."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.6_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.7_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_5_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def data(path):return (ROOT/path).read_bytes()
def blob(path):
    b=data(path)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def main():
    old,new=json.loads(data(OLD)),json.loads(data(NEW))
    assert blob(OLD)=="5dd4b6612e0462d7d537844b497002e92d9504f0"
    assert new["base_v5_6_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [r["catalogue_id"] for r in old["rows"]]==[r["catalogue_id"] for r in new["rows"]]
    assert len({r["catalogue_id"] for r in new["rows"]})==239
    for a,b in zip(old["rows"],new["rows"]):
        if a["catalogue_id"]!="03-020":assert a==b,a["catalogue_id"]
        else:
            assert a["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert b["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert b["proposed_primary_research_id"]=="R339"
            assert blob(b["readme_path"])==b["readme_git_blob_sha1"]=="fd01ff50df0b0cc796d862290b6fdda846664c2b"
            assert b["method_specific_E1_acceptance"]=="research/R339/R339_FINAL_ACCEPTANCE_STATUS.json"
    assert new["counts"]==dict(primary_R=231,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=5,pending_primary_R=5)
    status=Counter(r["link_status"] for r in new["rows"])
    assert sum(status.values())==239
    assert status["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert status["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==22
    assert status["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==5
    assert dict(status)=={k:v for k,v in new["status_counts"].items() if v>0}
    pending=[r["catalogue_id"] for r in new["rows"] if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    queue=list(csv.DictReader(data(QUEUE).decode().splitlines()))
    assert len(queue)==5 and queue[0]["original_catalogue_id"]=="04-007"
    assert [r["original_catalogue_id"] for r in queue]==pending
    for path,sha in [
      ("protocols/R339_SOCIAL_COMPARISON_100_ARTIFICIAL_TARGET_ATOMS_PRESCORE_FREEZE_2026-10-24.md","18629c8708189fc6a196ebbadeb84bd06f7aed10"),
      ("research/R339/r339_social_comparison.py","ed769df49658f345e78859f2be733b5b43322791"),
      ("research/R339/R339_ALL_100_ARTIFICIAL_TARGET_ATOMS.csv","fe06c06c7f158ab174251f1a14d184a4317b3371"),
      ("research/R339/R339_EXACT_50_CONDITIONS.json","817389e331f07dda90ae291daef9b20df1f65363"),
      ("research/catalogue_audit/independent_r339_social_comparison_audit.py","dd0ea88f73bdc3d4a75ac9b53b1442a56b4dfe25")
    ]:assert blob(path)==sha,(path,blob(path))
    a=json.loads(data("research/R339/R339_FINAL_ACCEPTANCE_STATUS.json"))
    receipt=json.loads(data("research/R339/R339_MACHINE_RECEIPT.json"))
    assert a["protocol_commit"]==receipt["protocol_commit"]=="dba0ded506b85e7c938a2c97d9478c2cd1daf120"
    assert a["source_commit"]==receipt["source_commit"]=="9152132df26ecfb9a09aaa6ce09f12aedd3658e9"
    assert a["CI_run_id"]==receipt["verification"]["run_id"]==40059401269
    assert a["three_jobs_success"] and a["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_TWO_TARGET_SIMILARITY_ONLY"
    assert a["real_human_E2"]==a["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="03-020" and new["E1_new_research"][-1]=="R339"
    print("ORIGINAL239_V57_PASS 239 original 231 primary 3 shared 5 pending 173 provisional R339 100 artificial atoms")
if __name__=="__main__":main()
