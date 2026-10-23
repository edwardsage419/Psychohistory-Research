#!/usr/bin/env python3
"""Independently verify exactly one R291 TRA catalogue amendment, NOT empirical closure."""
from __future__ import annotations
import argparse
import collections
import csv
import hashlib
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
ORIGINAL=DOC/"MODEL_CANDIDATE_CATALOG_v0.1.json"
PREV=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.4_2026-10-23.json"
LATEST=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.5_2026-10-23.json"
Q58=DOC/"ORIGINAL_239_PENDING_58_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q57=DOC/"ORIGINAL_239_PENDING_57_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
TRA=ROOT/"research/R291"
README=TRA/"README.md"

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def gitblob(path):
    b=path.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+bytes([0])+b).hexdigest()
def queue(path):
    with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def verify():
    original=obj(ORIGINAL)["models"]
    old,new=obj(PREV),obj(LATEST)
    a,b=old["rows"],new["rows"]
    assert len(original)==len(a)==len(b)==239
    assert len({x["catalogue_id"] for x in b})==239
    assert new["base_v0_4_path"]=="docs/"+PREV.name
    assert new["base_v0_4_git_blob_sha1"]==gitblob(PREV)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["01-013"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R291"]
    changed=[]
    for k,p,n in zip(original,a,b):
        assert k["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert k["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert k["priority"]==p["original_priority"]==n["original_priority"]
        assert k["category"]==p["catalogue_category"]==n["catalogue_category"]
        if p!=n:changed.append(k["id"])
    assert changed==["01-013"]
    target=next(z for z in b if z["catalogue_id"]=="01-013")
    assert target["proposed_primary_research_id"]=="R291"
    assert target["readme_path"]=="research/R291/README.md"
    assert target["readme_git_blob_sha1"]==gitblob(README)
    assert target["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert target["source_csv_file_count"]==target["python_source_file_count"]==1
    assert target["formal_acceptance_filename_candidates"]==["research/R291/R291_FINAL_ACCEPTANCE_STATUS.json"]
    assert target["scientific_report_filenames"]==["research/R291/R291_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert target["P1_scoped_review_addendum"]["CI_run_id"]==39912378382
    assert target["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    acc=obj(TRA/"R291_FINAL_ACCEPTANCE_STATUS.json")
    receipt=obj(TRA/"R291_MACHINE_RECEIPT.json")
    assert acc["original_catalogue_id"]=="01-013" and acc["ci_conclusion"]=="success"
    assert acc["ci_status"]=="completed" and acc["ci_jobs_successful"]==3
    assert acc["actual_model_tests_python311"]==acc["actual_model_tests_python312"]==106
    assert acc["new_real_human_E2"]==acc["new_historical_E3"]==0
    assert not acc["original_239_model_scientific_completion_established"]
    assert acc["source_sha256"]==receipt["sources_sha256"]==hashlib.sha256((TRA/"R291_ALL_128_ORIGINAL_TRA_LABELED_JOINT_SOURCES.csv").read_bytes()).hexdigest()
    assert acc["result_sha256"]==receipt["results_sha256"]==hashlib.sha256((TRA/"R291_EXACT_TRA_RESULTS.json").read_bytes()).hexdigest()
    assert obj(TRA/"R291_EXACT_TRA_RESULTS.json")["fully_labeled_joint_source_cells"]==128
    categories=dict(collections.Counter(z["link_status"] for z in b))
    assert new["status_counts"]==categories
    assert sum(categories.values())==239
    assert new["counts"]=={"primary_R":179,"shared_bounded_math":3,"older_scoped_only":5,"no_link_in_checked_sets":52,"pending_primary_R":57}
    q1,q2=queue(Q58),queue(Q57)
    assert len(q1)==58 and len(q2)==57
    assert q2==[z for z in q1 if z["original_catalogue_id"]!="01-013"]
    assert all(z["original_catalogue_id"]!="01-013" for z in q2)
    tp=next(z for z in b if z["catalogue_id"]=="01-014")
    assert tp["proposed_primary_research_id"] is None
    assert tp["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
    return {"original_catalogue_rows":239,"only_changed_original_id":"01-013","primary_R":179,"scoped_shared":3,"pending":57,"TPB_still_pending":"01-014","source_cells":128,"CI_run":39912378382,"E2_added":0,"E3_added":0,"overall_scientific_completion":False}

class Tests(unittest.TestCase):
    def test_full(self):self.assertEqual(verify()["only_changed_original_id"],"01-013")
    def test_count(self):self.assertEqual(verify()["original_catalogue_rows"],239)
    def test_primary(self):self.assertEqual(verify()["primary_R"],179)
    def test_pending(self):self.assertEqual(verify()["pending"],57)
    def test_tpbdistinct(self):self.assertEqual(verify()["TPB_still_pending"],"01-014")
    def test_source_count(self):self.assertEqual(verify()["source_cells"],128)
    def test_e2(self):self.assertEqual(verify()["E2_added"],0)
    def test_e3(self):self.assertEqual(verify()["E3_added"],0)
    def test_completed_false(self):self.assertFalse(verify()["overall_scientific_completion"])
    def test_github_ci(self):self.assertEqual(verify()["CI_run"],39912378382)
    def test_readme_hash(self):self.assertEqual(next(z for z in obj(LATEST)["rows"] if z["catalogue_id"]=="01-013")["readme_git_blob_sha1"],gitblob(README))
    def test_queue_exact(self):self.assertEqual(queue(Q57),[z for z in queue(Q58) if z["original_catalogue_id"]!="01-013"])
    def test_reject_catalogue_shift(self):
        rows=list(obj(LATEST)["rows"])
        rows[0]=dict(rows[0])
        rows[0]["catalogue_id"]="WRONG"
        self.assertNotEqual(rows[0]["catalogue_id"],obj(ORIGINAL)["models"][0]["id"])
    def test_reject_historical_reinterpretation(self):
        self.assertFalse(obj(TRA/"R291_FINAL_ACCEPTANCE_STATUS.json")["original_paper_human_experiment_reproduced"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R291crosswalk"],verbosity=1)
    else:print(json.dumps(verify(),indent=2))
