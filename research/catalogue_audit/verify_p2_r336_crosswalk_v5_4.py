#!/usr/bin/env python3
"""Original239 v5.4 strict provenance and R336 finite evidence gates."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.3_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v5.4_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_8_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def data(path):return (ROOT/path).read_bytes()
def blob(path):
    b=data(path)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\\0"+b).hexdigest()
def main():
    old=json.loads(data(OLD)); new=json.loads(data(NEW))
    assert blob(OLD)=="d2a3933adfed40fdb3b534a0e835a5dcf6272cc3"
    assert new["base_v5_3_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [r["catalogue_id"] for r in old["rows"]]==[r["catalogue_id"] for r in new["rows"]]
    assert len(set(r["catalogue_id"] for r in new["rows"]))==239
    for a,b in zip(old["rows"],new["rows"]):
        if a["catalogue_id"]!="03-014":
            assert a==b,a["catalogue_id"]
        else:
            assert a["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert b["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert b["proposed_primary_research_id"]=="R336"
            assert blob(b["readme_path"])==b["readme_git_blob_sha1"]=="7d36050d5b3cb62eda7bd992e275dea627410122"
            assert b["method_specific_E1_acceptance"]=="research/R336/R336_FINAL_ACCEPTANCE_STATUS.json"
    assert new["counts"]==dict(primary_R=228,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=8,pending_primary_R=8)
    statuses=Counter(r["link_status"] for r in new["rows"])
    assert sum(statuses.values())==239
    assert statuses["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert statuses["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==19
    assert statuses["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==8
    assert dict(statuses)=={k:v for k,v in new["status_counts"].items() if v>0}
    q=list(csv.DictReader(data(QUEUE).decode().splitlines()))
    assert len(q)==8 and q[0]["original_catalogue_id"]=="03-015"
    assert [x["original_catalogue_id"] for x in q]==[r["catalogue_id"] for r in new["rows"] if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for p,sha in [
        ("protocols/R336_INOCULATION_96_ARTIFICIAL_ATTACK_ATOMS_PRESCORE_FREEZE_2026-10-24.md","cd0f7478a359fa64b4db4d0d7c8cfc527f868f2b"),
        ("research/R336/r336_inoculation.py","bcbf7b40c1f8ba86d5478d57509a437b5ba0279f"),
        ("research/R336/R336_ALL_96_ARTIFICIAL_ATTACK_ATOMS.csv","efa20e7d6432a1a6c7bd0abd53384b36e23422e5"),
        ("research/R336/R336_EXACT_48_CONDITIONS.json","2704b6066a7f3842c2273c8262d9fd41e2483d73"),
        ("research/catalogue_audit/independent_r336_inoculation_audit.py","62bd3085815f6977307d8c94bf8cba09f6b76b93")
    ]:assert blob(p)==sha,(p,blob(p))
    a=json.loads(data("research/R336/R336_FINAL_ACCEPTANCE_STATUS.json"))
    receipt=json.loads(data("research/R336/R336_MACHINE_RECEIPT.json"))
    assert a["protocol_commit"]==receipt["protocol_commit"]=="3f10d5a6c2c8b713d3b14abc61c768383de8c934"
    assert a["source_commit"]==receipt["source_commit"]=="1d580bed37891ca4516a5c3d338037bd3ba8c2d1"
    assert a["CI_run_id"]==receipt["verification"]["run_id"]==40055738338
    assert a["three_jobs_success"] and a["status"]=="PASS_BOUNDED_E1_CONSTRUCTED_INOCULATION_TRANSFER_CONTRAST_ONLY"
    assert a["real_human_E2"]==a["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="03-014" and new["E1_new_research"][-1]=="R336"
    print("ORIGINAL239_V54_PASS 239 original 228 primary 3 shared 8 pending 173 provisional R336 96 artificial atoms")
if __name__=="__main__":main()
