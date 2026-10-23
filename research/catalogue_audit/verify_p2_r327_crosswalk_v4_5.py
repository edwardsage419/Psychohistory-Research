#!/usr/bin/env python3
"""Verify original239 v4.5 R327 E1 mapping and 17 pending identities."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.4_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.5_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_17_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def read(p):return (ROOT/p).read_bytes()
def blob(p):
    b=read(p)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def run():
    old=json.loads(read(OLD));new=json.loads(read(NEW))
    assert blob(OLD)=="9bbc7170d2f19862e9f49672e873ae6dfe9dd9e6"
    assert new["base_v4_4_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [x["catalogue_id"] for x in old["rows"]]==[x["catalogue_id"] for x in new["rows"]]
    assert len({x["catalogue_id"] for x in new["rows"]})==239
    for x,y in zip(old["rows"],new["rows"]):
        if x["catalogue_id"]!="02-009":
            assert x==y,x["catalogue_id"]
        else:
            assert x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert y["catalogue_name_en"]=="POMDP" and y["original_priority"]=="P2"
            assert y["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert y["proposed_primary_research_id"]=="R327"
            assert blob(y["readme_path"])==y["readme_git_blob_sha1"]=="9dd5d0dc922ef7af9e8a39104c73408d193be0b6"
    assert new["counts"]==dict(primary_R=219,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=17,pending_primary_R=17)
    c=Counter(x["link_status"] for x in new["rows"])
    assert sum(c.values())==239
    assert c["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert c["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==10
    assert c["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==17
    assert all(new["status_counts"][k]==v for k,v in c.items())
    queue=list(csv.DictReader(read(QUEUE).decode().splitlines()))
    assert len(queue)==17 and queue[0]["original_catalogue_id"]=="02-010"
    assert [r["original_catalogue_id"] for r in queue]==[r["catalogue_id"] for r in new["rows"] if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for path,sha in [
      ("protocols/R327_TWO_STATE_ONE_SENSE_POMDP_72_PATHS_PRESCORE_FREEZE_2026-10-24.md","df46cf75cf0e0ae9e0e1eb4f94313de9130c7b2f"),
      ("research/R327/r327_finite_pomdp.py","d62820c0e584cb0ba4d09f25964f4801b69fef46"),
      ("research/R327/R327_ALL_72_ARTIFICIAL_HIDDEN_OBSERVATION_PATHS.csv","e6cc4a03db826c6e8b8c9c13b98a0c832c51203b"),
      ("research/R327/R327_EXACT_18_BELIEF_WORLDS.json","71c696684555366c58140059ebd8947301300b48"),
      ("research/catalogue_audit/independent_r327_pomdp_audit.py","9f184f8d70ca6908a6c231db0eed08c5f69bee70")
    ]:assert blob(path)==sha,(path,blob(path))
    receipt=json.loads(read("research/R327/R327_MACHINE_RECEIPT.json"))
    acceptance=json.loads(read("research/R327/R327_FINAL_ACCEPTANCE_STATUS.json"))
    assert receipt["protocol_commit"]=="e40b9f4252afb2b31efc9977091057fa1480ff15"
    assert receipt["verification"]["CI_run_id"]==acceptance["CI_run_id"]==40029054228
    assert all(j["conclusion"]=="success" for j in receipt["verification"]["jobs"])
    assert acceptance["status"]=="PASS_BOUNDED_E1_FINITE_ONE_SENSE_POMDP_ONLY"
    assert acceptance["real_human_E2"]==acceptance["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="02-009" and new["E1_new_research"][-1]=="R327"
    print("ORIGINAL239_V45_PASS 239 original 219 primary 3 shared 17 pending 173 provisional R327 72 artificial paths")
if __name__=="__main__":run()
