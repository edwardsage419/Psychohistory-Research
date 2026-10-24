#!/usr/bin/env python3
"""Original239 v5.2 exact R334 provenance and candidate queue checks."""
import csv, hashlib, json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.1_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.2_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_10_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def data(p):return (ROOT/p).read_bytes()
def blob(p):
    b=data(p)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def main():
    old=json.loads(data(OLD)); new=json.loads(data(NEW))
    assert blob(OLD)=="a0cb53261bc2b4fd607e475cfacbfbb36a43fcd2"
    assert new["base_v5_1_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [r["catalogue_id"] for r in old["rows"]]==[r["catalogue_id"] for r in new["rows"]]
    assert len(set(r["catalogue_id"] for r in new["rows"]))==239
    for a,b in zip(old["rows"],new["rows"]):
        if a["catalogue_id"]!="03-011":
            assert a==b,a["catalogue_id"]
        else:
            assert a["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert b["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert b["proposed_primary_research_id"]=="R334"
            assert blob(b["readme_path"])==b["readme_git_blob_sha1"]=="aae0126a561f03748eb989a97be632e5a3c5e3a4"
            assert b["method_specific_E1_acceptance"]=="research/R334/R334_FINAL_ACCEPTANCE_STATUS.json"
    assert new["counts"]==dict(primary_R=226,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=10,pending_primary_R=10)
    statuses=Counter(r["link_status"] for r in new["rows"])
    assert sum(statuses.values())==239
    assert statuses["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert statuses["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==17
    assert statuses["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==10
    assert dict(statuses)=={k:v for k,v in new["status_counts"].items() if v>0}
    q=list(csv.DictReader(data(QUEUE).decode().splitlines()))
    assert len(q)==10 and q[0]["original_catalogue_id"]=="03-013"
    assert [x["original_catalogue_id"] for x in q]==[r["catalogue_id"] for r in new["rows"] if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for p,sha in [
      ("protocols/R334_COGNITIVE_DISSONANCE_48_ARTIFICIAL_CONTRAST_PRESCORE_FREEZE_2026-10-24.md","08153771bd8d7db10c267135aa25503a40d4fffd"),
      ("research/R334/r334_dissonance.py","7d232a07d9d2979c2fcc8a407dd8bda18cd8ab93"),
      ("research/R334/R334_ALL_48_ARTIFICIAL_CONTRAST_ATOMS.csv","6e3bdcc5ca07d1321a651c29b899798a32f7fb72"),
      ("research/R334/R334_EXACT_16_CONDITIONS.json","02883b6b9cfc22b3b855d8a7cbaa5e5ddf6bd86c"),
      ("research/catalogue_audit/independent_r334_dissonance_audit.py","cc92d9c89e450deb032af3453e6fcaa719561db3"),
      ("research/R334/R334_FINAL_ACCEPTANCE_STATUS.json","ecaf06f19437b4e13940b5db8858f2f0920d1096"),
      ("research/R334/R334_MACHINE_RECEIPT.json","70c90c39ddcfe79140497dd0997444c50fcd7fdc")
    ]:assert blob(p)==sha,(p,blob(p))
    a=json.loads(data("research/R334/R334_FINAL_ACCEPTANCE_STATUS.json"))
    receipt=json.loads(data("research/R334/R334_MACHINE_RECEIPT.json"))
    assert a["protocol_commit"]==receipt["protocol_commit"]=="7ec583e77d7e4a937b552601dcca5409483cc59b"
    assert a["CI_run_id"]==receipt["verification"]["run_id"]==40051279908
    assert a["three_jobs_success"] and a["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_INDUCED_COMPLIANCE_ONLY"
    assert a["real_human_E2"]==a["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="03-011" and new["E1_new_research"][-1]=="R334"
    print("ORIGINAL239_V52_PASS 239 original 226 primary 3 shared 10 pending 173 provisional R334 48 artificial atoms")
if __name__=="__main__":main()
