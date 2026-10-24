#!/usr/bin/env python3
"""Original239 v5.3 exact R335 provenance and candidate queue checks."""
import csv, hashlib, json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.2_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.3_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_9_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def data(p):return (ROOT/p).read_bytes()
def blob(p):
    b=data(p)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def main():
    old=json.loads(data(OLD)); new=json.loads(data(NEW))
    assert blob(OLD)=="2e335c2829db6e458bdd62a59b94a4af5b6f0cca"
    assert new["base_v5_2_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [r["catalogue_id"] for r in old["rows"]]==[r["catalogue_id"] for r in new["rows"]]
    assert len(set(r["catalogue_id"] for r in new["rows"]))==239
    for a,b in zip(old["rows"],new["rows"]):
        if a["catalogue_id"]!="03-013":
            assert a==b,a["catalogue_id"]
        else:
            assert a["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert b["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert b["proposed_primary_research_id"]=="R335"
            assert blob(b["readme_path"])==b["readme_git_blob_sha1"]=="3d66ab32fd1704e71fb8c6a3811a916a1383c779"
            assert b["method_specific_E1_acceptance"]=="research/R335/R335_FINAL_ACCEPTANCE_STATUS.json"
    assert new["counts"]==dict(primary_R=227,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=9,pending_primary_R=9)
    statuses=Counter(r["link_status"] for r in new["rows"])
    assert sum(statuses.values())==239
    assert statuses["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert statuses["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==18
    assert statuses["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==9
    assert dict(statuses)=={k:v for k,v in new["status_counts"].items() if v>0}
    q=list(csv.DictReader(data(QUEUE).decode().splitlines()))
    assert len(q)==9 and q[0]["original_catalogue_id"]=="03-014"
    assert [x["original_catalogue_id"] for x in q]==[r["catalogue_id"] for r in new["rows"] if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for p,sha in [
      ("protocols/R335_GROUPTHINK_384_ARTIFICIAL_PUBLIC_UNANIMITY_PRESCORE_FREEZE_2026-10-24.md","3dd13dda234e702a2e809752e4a2d4e74cf89296"),
      ("research/R335/r335_groupthink.py","9c005079716fe38eb4cb6d99730884a55e2795a3"),
      ("research/R335/R335_ALL_384_ARTIFICIAL_GROUP_ATOMS.csv","f5987d4d9da8ef7532a3615b5f7fb6efbd4701cb"),
      ("research/R335/R335_EXACT_128_CONDITIONS.json","4ab8f69cbd483099dd2a1be28cb052e1e3bdb279"),
      ("research/catalogue_audit/independent_r335_groupthink_audit.py","ce9c97c5c2589d5b5f9e37c38bfa96ca501c143f"),
      ("research/R335/R335_FINAL_ACCEPTANCE_STATUS.json","507b781e2fb4a27d72c6cbd096f8dd14c6d4543d"),
      ("research/R335/R335_MACHINE_RECEIPT.json","3e71a2a448923a969df3b16aae607df6c3908942")
    ]:assert blob(p)==sha,(p,blob(p))
    a=json.loads(data("research/R335/R335_FINAL_ACCEPTANCE_STATUS.json"))
    receipt=json.loads(data("research/R335/R335_MACHINE_RECEIPT.json"))
    assert a["protocol_commit"]==receipt["protocol_commit"]=="0c553f662ae723adadaba9c7f4ce325d8964032e"
    assert a["CI_run_id"]==receipt["verification"]["run_id"]==40051490899
    assert a["three_jobs_success"] and a["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_PUBLIC_UNANIMITY_ORACLE_ONLY"
    assert a["real_human_E2"]==a["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="03-013" and new["E1_new_research"][-1]=="R335"
    print("ORIGINAL239_V53_PASS 239 original 227 primary 3 shared 9 pending 173 provisional R335 384 artificial atoms")
if __name__=="__main__":main()
