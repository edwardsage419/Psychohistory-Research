#!/usr/bin/env python3
"""Original239 v4.6 exact R328 source and itemwise metadata audit."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.5_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.6_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_16_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def read(p):return (ROOT/p).read_bytes()
def blob(p):
    b=read(p)
    return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def run():
    old=json.loads(read(OLD));new=json.loads(read(NEW))
    assert blob(OLD)=="b13cda310b68ad118c88bfe4763bbe528d30882a"
    assert new["base_v4_5_git_blob_sha1"]==blob(OLD)
    assert len(old["rows"])==len(new["rows"])==239
    assert [r["catalogue_id"] for r in old["rows"]]==[r["catalogue_id"] for r in new["rows"]]
    assert len({r["catalogue_id"] for r in new["rows"]})==239
    for x,y in zip(old["rows"],new["rows"]):
        if x["catalogue_id"]!="02-010":assert x==y,x["catalogue_id"]
        else:
            assert x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert y["catalogue_name_en"]=="Predictive Processing" and y["original_priority"]=="P2"
            assert y["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert y["proposed_primary_research_id"]=="R328"
            assert blob(y["readme_path"])==y["readme_git_blob_sha1"]=="e35c6667f5ba787943ddcce5eebe722fd81e191c"
    assert new["counts"]==dict(primary_R=220,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=16,pending_primary_R=16)
    c=Counter(r["link_status"] for r in new["rows"])
    assert sum(c.values())==239 and c["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert c["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==11
    assert c["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==16
    assert all(new["status_counts"][k]==v for k,v in c.items())
    q=list(csv.DictReader(read(QUEUE).decode().splitlines()))
    assert len(q)==16 and q[0]["original_catalogue_id"]=="02-011"
    assert [r["original_catalogue_id"] for r in q]==[r["catalogue_id"] for r in new["rows"] if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for path,sha in [
        ("protocols/R328_SCALAR_PRECISION_WEIGHTED_PREDICTIVE_ERROR_120_ROWS_PRESCORE_FREEZE_2026-10-24.md","8cd8dadb4d651907f3390cc757bd11197c847a42"),
        ("research/R328/r328_scalar_predictive_error.py","84dc8326ebfdc85746fa7abb3554780d4bbf8979"),
        ("research/R328/R328_ALL_120_ARTIFICIAL_PREDICTION_ERROR_STATES.csv","b699cf1100955e89ed2edee7757bee70083656b0"),
        ("research/R328/R328_EXACT_24_PRECISION_WORLDS.json","0ad1a1ea4e17bc27b7cd3bef961da5d9f3ccee4f"),
        ("research/catalogue_audit/independent_r328_predictive_error_audit.py","a703e313bbbc2e82a3379a36a5dc9906767198f3")
    ]:assert blob(path)==sha,(path,blob(path))
    receipt=json.loads(read("research/R328/R328_MACHINE_RECEIPT.json"))
    acceptance=json.loads(read("research/R328/R328_FINAL_ACCEPTANCE_STATUS.json"))
    assert receipt["protocol_commit"]=="cf240df27b0fa1391fb03be2e714e8d498ed83de"
    assert receipt["verification"]["CI_run_id"]==acceptance["CI_run_id"]==40029363018
    assert all(j["conclusion"]=="success" for j in receipt["verification"]["jobs"])
    assert acceptance["status"]=="PASS_BOUNDED_E1_SCALAR_PREDICTIVE_ERROR_ONLY"
    assert acceptance["real_human_E2"]==acceptance["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="02-010" and new["E1_new_research"][-1]=="R328"
    print("ORIGINAL239_V46_PASS 239 original 220 primary 3 shared 16 pending 173 provisional R328 120 artificial states")
if __name__=="__main__":run()
