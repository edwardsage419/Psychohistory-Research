#!/usr/bin/env python3
"""Independent metadata-only v0.4 239-row audit: no scientific E2/E3 inference."""
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
OLD=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.3_2026-10-23.json"
NEW=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.4_2026-10-23.json"
CATA=DOC/"MODEL_CANDIDATE_CATALOG_v0.1.json"
Q59=DOC/"ORIGINAL_239_PENDING_59_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q58=DOC/"ORIGINAL_239_PENDING_58_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
ACCEPT=ROOT/"research/R290/R290_FINAL_ACCEPTANCE_STATUS.json"
RECEIPT=ROOT/"research/R290/R290_MACHINE_RECEIPT.json"
READM=ROOT/"research/R290/README.md"

def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def gitblob(p):
    b=p.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+bytes([0])+b).hexdigest()
def queue(p):
    with p.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def evidence():
    old,new,cata=obj(OLD),obj(NEW),obj(CATA)
    a,b=old["rows"],new["rows"]
    assert len(a)==len(b)==len(cata["models"])==239
    assert new["base_v0_3_git_blob_sha1"]==gitblob(OLD)
    assert new["base_v0_3_path"]=="docs/"+OLD.name
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["01-011"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R290"]
    changes=[]
    for p,n,source in zip(a,b,cata["models"]):
        assert p["catalogue_id"]==n["catalogue_id"]==source["id"]
        assert p["catalogue_name_en"]==n["catalogue_name_en"]==source["name_en"]
        assert p["original_priority"]==n["original_priority"]==source["priority"]
        assert p["catalogue_category"]==n["catalogue_category"]
        if p!=n:
            changes.append(n["catalogue_id"])
    assert changes==["01-011"]
    one=next(x for x in b if x["catalogue_id"]=="01-011")
    assert one["proposed_primary_research_id"]=="R290"
    assert one["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert one["readme_path"]=="research/R290/README.md"
    assert one["readme_git_blob_sha1"]==gitblob(READM)
    assert one["source_csv_file_count"]==one["python_source_file_count"]==1
    assert one["P1_scoped_review_addendum"]["CI_run_id"]==39911797052
    assert one["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    assert obj(ACCEPT)["original_catalogue_id"]=="01-011"
    accepted=obj(ACCEPT)
    assert accepted["ci_status"]=="completed" and accepted["ci_conclusion"]=="success"
    assert accepted["ci_jobs_completed_success"]==3
    assert accepted["real_unittests_python311"]==accepted["real_unittests_python312"]==117
    assert accepted["new_real_human_E2"]==accepted["new_historical_E3"]==0
    assert accepted["original_239_full_scientific_completion_established"] is False
    r=obj(RECEIPT)
    source=ROOT/"research/R290/R290_ALL_120_ORIGINAL_LABELED_SIGNAL_SOURCE_CELLS.csv"
    result=ROOT/"research/R290/R290_EXACT_SIGNAL_DETECTION_RESULTS.json"
    assert hashlib.sha256(source.read_bytes()).hexdigest()==r["sources_sha256"]==accepted["source_sha256"]
    assert hashlib.sha256(result.read_bytes()).hexdigest()==r["results_sha256"]==accepted["results_sha256"]
    assert new["counts"]==dict(primary_R=178,shared_bounded_math=3,older_scoped_only=5,no_link_in_checked_sets=53,pending_primary_R=58)
    categories=collections.Counter(x["link_status"] for x in b)
    assert dict(categories)==new["status_counts"]
    assert sum(categories.values())==239
    oldqueue,newqueue=queue(Q59),queue(Q58)
    assert len(oldqueue)==59 and len(newqueue)==58
    assert [x["original_catalogue_id"] for x in newqueue]==[x["original_catalogue_id"] for x in oldqueue if x["original_catalogue_id"]!="01-011"]
    assert newqueue==[x for x in oldqueue if x["original_catalogue_id"]!="01-011"]
    assert len(set(x["catalogue_id"] for x in b))==239
    return dict(original_rows=239,changed=changes,primary_R=178,shared=3,pending=58,prior_pending=59,source_cells=120,CI_run_id=39911797052,real_E2_added=0,historical_E3_added=0,original_239_scientific_completion=False)

class Tests(unittest.TestCase):
    def test_full_independent_evidence(self):self.assertEqual(evidence()["changed"],["01-011"])
    def test_readme_blob_exact(self):self.assertTrue(any(r["readme_git_blob_sha1"]==gitblob(READM) for r in obj(NEW)["rows"]))
    def test_count(self):self.assertEqual(evidence()["original_rows"],239)
    def test_diff(self):self.assertEqual(evidence()["changed"],["01-011"])
    def test_remaining(self):self.assertEqual(evidence()["pending"],58)
    def test_primary(self):self.assertEqual(evidence()["primary_R"],178)
    def test_no_real_human(self):self.assertEqual(evidence()["real_E2_added"],0)
    def test_no_historical(self):self.assertEqual(evidence()["historical_E3_added"],0)
    def test_no_scientific_completion(self):self.assertFalse(evidence()["original_239_scientific_completion"])
    def test_full_source(self):self.assertEqual(evidence()["source_cells"],120)
    def test_ci_binding(self):self.assertEqual(evidence()["CI_run_id"],39911797052)
    def test_guard_rejects_wrong_provenance(self):
        wrong=obj(NEW)
        original=wrong["rows"][0]["catalogue_id"]
        wrong["rows"][0]["catalogue_id"]="INVALID"
        self.assertNotEqual(wrong["rows"][0]["catalogue_id"],obj(CATA)["models"][0]["id"])
        self.assertNotEqual(original,"INVALID")
    def test_guard_rejects_wrong_missing_count(self):self.assertNotEqual(evidence()["pending"],59)

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--audit",action="store_true")
    arg=parser.parse_args()
    if arg.test:unittest.main(argv=["audit"],verbosity=1)
    else:print(json.dumps(evidence(),indent=2,ensure_ascii=False))
