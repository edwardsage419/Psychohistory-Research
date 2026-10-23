#!/usr/bin/env python3
"""Original 239 candidates, R294 exact time-choice model one-row v0.8 provenance audit."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.7_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.8_2026-10-23.json"
Q55=D/"ORIGINAL_239_PENDING_55_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q54=D/"ORIGINAL_239_PENDING_54_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R294"

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def blob(path):
    x=path.read_bytes()
    return hashlib.sha1(("blob "+str(len(x))).encode()+bytes([0])+x).hexdigest()
def rows(path):
    with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def audit():
    catalog=obj(CAT)["models"]
    old,new=obj(OLD),obj(NEW)
    before,after=old["rows"],new["rows"]
    assert len(catalog)==len(before)==len(after)==239
    assert len(set(x["catalogue_id"] for x in after))==239
    assert new["base_v0_7_path"]=="docs/"+OLD.name and new["base_v0_7_git_blob_sha1"]==blob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["01-018"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R294"]
    changed=[]
    for k,a,b in zip(catalog,before,after):
        assert k["id"]==a["catalogue_id"]==b["catalogue_id"]
        assert k["name_en"]==a["catalogue_name_en"]==b["catalogue_name_en"]
        assert k["priority"]==a["original_priority"]==b["original_priority"]
        assert k["category"]==a["catalogue_category"]==b["catalogue_category"]
        if a!=b:changed.append(k["id"])
    assert changed==["01-018"]
    r=next(z for z in after if z["catalogue_id"]=="01-018")
    assert r["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R" and r["proposed_primary_research_id"]=="R294"
    assert r["readme_git_blob_sha1"]==blob(R/"README.md")
    assert r["readme_path"]=="research/R294/README.md"
    assert r["source_csv_file_count"]==r["python_source_file_count"]==1
    assert r["formal_acceptance_filename_candidates"]==["research/R294/R294_FINAL_ACCEPTANCE_STATUS.json"]
    assert r["scientific_report_filenames"]==["research/R294/R294_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert r["P1_scoped_review_addendum"]["CI_run_id"]==39919476504
    assert r["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    acc,receipt,output=obj(R/"R294_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R294_MACHINE_RECEIPT.json"),obj(R/"R294_EXACT_DISCOUNT_REVERSALS.json")
    assert acc["ci_conclusion"]=="success" and acc["ci_status"]=="completed" and acc["ci_jobs_completed_success"]==3
    assert acc["actual_model_unittests_python311"]==acc["actual_model_unittests_python312"]==583
    assert acc["original_catalogue_id"]=="01-018" and acc["new_real_human_E2"]==acc["new_historical_E3"]==0
    assert acc["original_239_scientific_completion_established"] is False
    assert acc["original_source_sha256"]==receipt["source_sha256"]==hashlib.sha256((R/"R294_ALL_144_EXACT_INTERTEMPORAL_DECISION_SOURCES.csv").read_bytes()).hexdigest()
    assert acc["result_sha256"]==receipt["result_sha256"]==hashlib.sha256((R/"R294_EXACT_DISCOUNT_REVERSALS.json").read_bytes()).hexdigest()
    assert output["original_catalogue_id"]=="01-018" and output["artificial_worlds"]==72 and output["exact_decision_source_rows"]==144
    assert len(output["worlds"])==72
    counts=collections.Counter()
    for w in output["worlds"]:counts[w["family"]]+=int(w["reversal_B_to_A"])
    assert counts["HYPERBOLIC"]==8 and counts["EXPONENTIAL"]==0 and counts["QUASI_HYPERBOLIC_BETA_DELTA"]==7
    assert new["counts"]=={"primary_R":182,"shared_bounded_math":3,"older_scoped_only":5,"no_link_in_checked_sets":49,"pending_primary_R":54}
    assert new["status_counts"]==dict(collections.Counter(z["link_status"] for z in after))
    assert sum(new["status_counts"].values())==239
    oldq,newq=rows(Q55),rows(Q54)
    assert len(oldq)==55 and len(newq)==54
    assert newq==[x for x in oldq if x["original_catalogue_id"]!="01-018"]
    assert newq[0]["original_catalogue_id"]=="01-019"
    assert sum(x["priority"]=="P1" for x in newq)==27
    assert sum(x["priority"]=="P2" for x in newq)==27
    return {"original_catalogue_rows":239,"changed_only":["01-018"],"primary":182,
      "shared_scoped":3,"pending":54,"P1_remaining":27,"P2_remaining":27,
      "R294_decision_sources":144,"R294_worlds":72,"R294_hyper_reversals":8,
      "R294_quasi_reversals":7,"R294_exponential_reversals":0,
      "new_real_E2":0,"new_historical_E3":0,"overall_scientific_completion":False}

class Tests(unittest.TestCase):
    def test_full(self):self.assertEqual(audit()["changed_only"],["01-018"])
    def test_count(self):self.assertEqual(audit()["original_catalogue_rows"],239)
    def test_primary(self):self.assertEqual(audit()["primary"],182)
    def test_pending(self):self.assertEqual(audit()["pending"],54)
    def test_P1(self):self.assertEqual(audit()["P1_remaining"],27)
    def test_P2(self):self.assertEqual(audit()["P2_remaining"],27)
    def test_decision_sources(self):self.assertEqual(audit()["R294_decision_sources"],144)
    def test_worlds(self):self.assertEqual(audit()["R294_worlds"],72)
    def test_reversal_hyper(self):self.assertEqual(audit()["R294_hyper_reversals"],8)
    def test_reversal_quasi(self):self.assertEqual(audit()["R294_quasi_reversals"],7)
    def test_reversal_exponential(self):self.assertEqual(audit()["R294_exponential_reversals"],0)
    def test_E2(self):self.assertEqual(audit()["new_real_E2"],0)
    def test_E3(self):self.assertEqual(audit()["new_historical_E3"],0)
    def test_fullscientific(self):self.assertFalse(audit()["overall_scientific_completion"])
    def test_readme(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="01-018")["readme_git_blob_sha1"],blob(R/"README.md"))

if __name__=="__main__":
    p=argparse.ArgumentParser()
    m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true")
    m.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R294provenance"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
