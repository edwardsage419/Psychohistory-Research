#!/usr/bin/env python3
"""Verify original239 v4.4 R326 bounded E1 mapping, original identities and pending queue."""
import csv
import hashlib
import json
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
OLD="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.3_2026-10-24.json"
NEW="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v4.4_2026-10-24.json"
QUEUE="docs/ORIGINAL_239_PENDING_18_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv"
def read(p):return (ROOT/p).read_bytes()
def blob(p):
    data=read(p)
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def run():
    old=json.loads(read(OLD));new=json.loads(read(NEW))
    assert blob(OLD)=="07904d007652ce6d3398fb1b03efd441d8bd12f6"
    assert new["base_v4_3_git_blob_sha1"]==blob(OLD)
    a=old["rows"];b=new["rows"]
    assert len(a)==len(b)==239
    assert [r["catalogue_id"] for r in a]==[r["catalogue_id"] for r in b]
    assert len({r["catalogue_id"] for r in b})==239
    for x,y in zip(a,b):
        if x["catalogue_id"]!="02-007":assert x==y,x["catalogue_id"]
        else:
            assert x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
            assert y["catalogue_name_en"]=="Hierarchical Bayesian Learning" and y["original_priority"]=="P2"
            assert y["link_status"]=="DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"
            assert y["proposed_primary_research_id"]=="R326"
            assert blob(y["readme_path"])==y["readme_git_blob_sha1"]=="d315d29fa345267d2d9a770dcc8facf42aafcc18"
    assert new["counts"]==dict(primary_R=218,shared_bounded_math=3,older_scoped_only=0,no_link_in_checked_sets=18,pending_primary_R=18)
    c=Counter(r["link_status"] for r in b)
    assert sum(c.values())==239 and c["PROVISIONAL_PRIMARY_README_LINK"]==173
    assert c["DIRECT_P2_BOUNDED_E1_NEW_PRIMARY_R"]==9
    assert c["NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]==18
    assert all(new["status_counts"][k]==v for k,v in c.items())
    q=list(csv.DictReader(read(QUEUE).decode().splitlines()))
    assert len(q)==18 and q[0]["original_catalogue_id"]=="02-009"
    assert [r["original_catalogue_id"] for r in q]==[r["catalogue_id"] for r in b if r["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"]
    for path,sha in [
        ("protocols/R326_HIERARCHICAL_BAYESIAN_THREE_GROUP_64_ARTIFICIAL_HISTORIES_PRESCORE_FREEZE_2026-10-24.md","63e4a70bb28f42d0a0b26b216699da2c91cd8ae9"),
        ("research/R326/r326_hier_bayes.py","bcb90969b832cea6ca778c90fa6fbdcf2a4cc9c9"),
        ("research/R326/R326_ALL_64_ARTIFICIAL_GROUP_HISTORIES.csv","3d2481365160c33fabbba7f8be6c3a9ff78e5121"),
        ("research/R326/R326_EXACT_HIERARCHICAL_PREDICTIONS.json","18f8f36c7ff0a402e53463323a90c0142dd5f340"),
        ("research/catalogue_audit/independent_r326_hier_bayes_audit.py","eeee4b3e158e149f7d4d677745a0e506acec6e68")
    ]:assert blob(path)==sha,(path,blob(path))
    receipt=json.loads(read("research/R326/R326_MACHINE_RECEIPT.json"))
    acceptance=json.loads(read("research/R326/R326_FINAL_ACCEPTANCE_STATUS.json"))
    assert receipt["protocol_commit"]=="5be3b4f7ba1035fb8a655fc8a4a0263e92154cad"
    assert receipt["verification"]["CI_run_id"]==acceptance["CI_run_id"]==40022140444
    assert all(j["conclusion"]=="success" for j in receipt["verification"]["jobs"])
    assert acceptance["status"]=="PASS_BOUNDED_E1_FINITE_HIERARCHICAL_BAYES_POOLING_ONLY"
    assert acceptance["real_human_E2"]==acceptance["historical_E3"]=="NOT_ESTABLISHED"
    assert new["changed_original_IDs"][-1]=="02-007" and new["E1_new_research"][-1]=="R326"
    print("ORIGINAL239_V44_PASS 239 original 218 primary 3 shared 18 pending 173 provisional 64 artificial R326 histories")
if __name__=="__main__":run()
