#!/usr/bin/env python3
"""Verify original239 v4.3 R325 bounded E1 mapping and source identity."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.2_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.3_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_19_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def read(p):return (ROOT/p).read_bytes()
def blob(p):
    data=read(p)
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def run():
    old=json.loads(read(OLD));new=json.loads(read(NEW))
    assert blob(OLD)=="85ef4cf04e7233429e352e9c591a06743c7866a9"
    assert new["base_v4_2_git_blob_sha1"]==blob(OLD)
    a=old["rows"];b=new["rows"]
    assert len(a)==len(b)==239
    assert [r["catalogue_id"] for r in a]==[r["catalogue_id"] for r in b]
    assert len({r["catalogue_id"] for r in b})==239
    for x,y in zip(a,b):
        if x["catalogue_id"]!="01-020":assert x==y,x["catalogue_id"]
        else:
            assert x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert y["catalogue_name_en"]=="Regret Theory" and y["original_priority"]=="P2"
            assert y["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert y["proposed_primary_research_id"]=="R325"
            assert blob(y["readme_path"])==y["readme_git_blob_sha1"]=="bb9142491842615f5d9850d77144dc6f2299db8e"
    assert new["counts"]==dict(primary_R=217,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=19,pending_primary_R=19)
    c=Counter(r["link_status"] for r in b)
    assert sum(c.values())==239 and c["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert c["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==8
    assert c["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==19
    assert all(new["status_counts"][k]==v for k,v in c.items())
    q=list(csv.DictReader(read(QUEUE).decode().splitlines()))
    assert len(q)==19 and q[0]["original_catalogue_id"]=="02-007"
    assert [r["original_catalogue_id"] for r in q]==[r["catalogue_id"] for r in b if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for path,sha in [
        ("protocols/R325_REGRET_THEORY_1029_ARTIFICIAL_STATEWISE_DIFFERENCE_PRESCORE_FREEZE_2026-10-24.md","c9cca57618d2c1d5a4b3e391c865a50bac60c306"),
        ("research/R325/r325_regret.py","e1fd070d271fa9a5516515e162d9057a47e76f46"),
        ("research/R325/R325_ALL_1029_ARTIFICIAL_REGRET_STATES.csv","b4964ef88aded2c9bd2a70280c067176fedcd597"),
        ("research/R325/R325_EXACT_THREE_REGRET_WORLDS.json","05e0b2e1f582420ea4aa510aaa9ba9b56dcd57a9"),
        ("research/catalogue_audit/independent_r325_regret_audit.py","c798bd1ce671c559f41d5d634ce09ff45ece965b")
    ]:assert blob(path)==sha,(path,blob(path))
    receipt=json.loads(read("research/R325/R325_MACHINE_RECEIPT.json"))
    acceptance=json.loads(read("research/R325/R325_FINAL_ACCEPTANCE_STATUS.json"))
    assert receipt["protocol_commit"]=="2d4fec87becfc46b6f66da1db5187b557afdcb53"
    assert receipt["verification"]["CI_run_id"]==acceptance["CI_run_id"]==40021709853
    assert all(j["conclusion"]=="success" for j in receipt["verification"]["jobs"])
    assert acceptance["status"]=="PASS_BOUNDED_E1_PROJECT_CONSTRUCTED_CUBIC_REGRET_ONLY"
    assert acceptance["real_human_E2"]==acceptance["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="01-020" and new["E1_new_research"][-1]=="R325"
    print("ORIGINAL239_V43_PASS 239 original 217 primary 3 shared 19 pending 173 provisional 1029 artificial R325 rows")
if __name__=="__main__":run()
