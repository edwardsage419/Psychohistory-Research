#!/usr/bin/env python3
"""Original 239 candidate crosswalk v1.3 independent provenance and bounded R063/R299 science check."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
ORIGINAL=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.2_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.3_2026-10-23.json"
QUEUE50=D/"ORIGINAL_239_PENDING_50_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
QUEUE49=D/"ORIGINAL_239_PENDING_49_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R299"
OLD_R063=ROOT/"research/R063/R063_EVIDENCE_AUDIT.md"

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def blob(path):
    b=path.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def queue(path):
    with path.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def audit():
    catalogue=obj(ORIGINAL)["models"]
    old,new=obj(OLD),obj(NEW)
    oldrows,newrows=old["rows"],new["rows"]
    assert len(catalogue)==len(oldrows)==len(newrows)==239
    assert len({x["catalogue_id"] for x in newrows})==239
    assert new["base_v1_2_path"]=="docs/"+OLD.name
    assert new["base_v1_2_git_blob_sha1"]==blob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["02-005"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R299"]
    changed=[]
    for c,p,n in zip(catalogue,oldrows,newrows):
        assert c["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert c["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert c["priority"]==p["original_priority"]==n["original_priority"]
        assert c["category"]==p["catalogue_category"]==n["catalogue_category"]
        if p!=n:changed.append(c["id"])
    assert changed==["02-005"]
    o=next(x for x in oldrows if x["catalogue_id"]=="02-005")
    n=next(x for x in newrows if x["catalogue_id"]=="02-005")
    assert o["link_status"]=="PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY"
    assert o["proposed_primary_research_id"] is None
    assert n["proposed_primary_research_id"]=="R299"
    assert n["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert n["readme_path"]=="research/R299/README.md"
    assert n["readme_git_blob_sha1"]==blob(R/"README.md")
    assert n["source_csv_file_count"]==n["python_source_file_count"]==1
    assert n["formal_acceptance_filename_candidates"]==["research/R299/R299_FINAL_ACCEPTANCE_STATUS.json"]
    assert n["scientific_report_filenames"]==["research/R299/R299_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert n["P1_scoped_review_addendum"]["CI_run_id"]==39927231561
    assert n["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    assert n["older_2026_10_18_scoped_evidence_paths"]==o["older_2026_10_18_scoped_evidence_paths"]
    assert n["older_scoped_paths_present"]==o["older_scoped_paths_present"]
    assert "research/R063/R063_EVIDENCE_AUDIT.md" in n["older_scoped_paths_present"]
    assert OLD_R063.is_file()
    assert "Najar" in OLD_R063.read_text(encoding="utf-8")
    accept,receipt,result=obj(R/"R299_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R299_MACHINE_RECEIPT.json"),obj(R/"R299_EXACT_MODEL_FREE_TD_MC_RESULTS.json")
    assert accept["original_catalogue_id"]=="02-005" and accept["research_id"]=="R299"
    assert accept["ci_status"]=="completed" and accept["ci_conclusion"]=="success" and accept["ci_jobs_completed_success"]==3
    assert accept["actual_model_unittests_python311"]==accept["actual_model_unittests_python312"]==492
    assert accept["independent_auditor_tests_per_execution"]==16
    assert accept["synthetic_worlds"]==24 and accept["fully_labeled_source_states"]==120
    assert accept["R063_Najar2020_previous_scope_preserved"] is True
    assert accept["R063_real_data_not_new_R299_E2"] is True
    assert accept["new_real_human_E2"]==accept["new_real_animal_E2"]==accept["new_historical_E3"]==0
    assert accept["original_239_scientific_completion_established"] is False
    assert accept["source_sha256"]==receipt["source_sha256"]==hashlib.sha256((R/"R299_ALL_120_ORIGINAL_MODEL_FREE_TD_MC_STATES.csv").read_bytes()).hexdigest()
    assert accept["results_sha256"]==receipt["results_sha256"]==hashlib.sha256((R/"R299_EXACT_MODEL_FREE_TD_MC_RESULTS.json").read_bytes()).hexdigest()
    assert result["original_catalogue_id"]=="02-005" and result["synthetic_worlds"]==24 and result["original_exact_source_rows"]==120
    assert result["reference_reward2_gamma_half_alpha_half_epoch4"]=={"TD0_S0":"11/16","MC_S0":"15/16","common_S1":"15/8","oracle_S0":"1"}
    assert result["real_human_E2_added"]==result["real_animal_E2_added"]==result["historical_E3_added"]==0
    assert result["existing_R063_human_metadata_cannot_be_reused_as_new_R299_E2"] is True
    assert new["counts"]=={"primary_R":187,"shared_bounded_math":3,"older_scoped_only":4,"no_link_in_checked_sets":45,"pending_primary_R":49}
    assert new["status_counts"]==dict(collections.Counter(x["link_status"] for x in newrows))
    assert sum(new["status_counts"].values())==239
    oldqueue,newqueue=queue(QUEUE50),queue(QUEUE49)
    assert len(oldqueue)==50 and len(newqueue)==49
    assert newqueue==[z for z in oldqueue if z["original_catalogue_id"]!="02-005"]
    assert newqueue[0]["original_catalogue_id"]=="02-008"
    assert sum(z["priority"]=="P1" for z in newqueue)==22
    assert sum(z["priority"]=="P2" for z in newqueue)==27
    assert next(z for z in newrows if z["catalogue_id"]=="02-003")["proposed_primary_research_id"]=="R297"
    assert next(z for z in newrows if z["catalogue_id"]=="02-004")["proposed_primary_research_id"]=="R298"
    return {"original_candidate_count":239,"changed_original_id":"02-005",
       "original_R063_prior_scoped_evidence_preserved":True,"main_R_links":187,
       "shared_bounded_math":3,"older_scoped_only":4,"pending_main_links":49,
       "pending_P1":22,"pending_P2":27,"next_candidate":"02-008",
       "R299_complete_artificial_sources":120,"new_real_E2":0,
       "new_historical_E3":0,"all_239_scientifically_complete":False}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["changed_original_id"],"02-005")
    def test_canonical_count(self):self.assertEqual(audit()["original_candidate_count"],239)
    def test_primary(self):self.assertEqual(audit()["main_R_links"],187)
    def test_pending(self):self.assertEqual(audit()["pending_main_links"],49)
    def test_P1(self):self.assertEqual(audit()["pending_P1"],22)
    def test_P2(self):self.assertEqual(audit()["pending_P2"],27)
    def test_old_R063(self):self.assertTrue(audit()["original_R063_prior_scoped_evidence_preserved"])
    def test_src(self):self.assertEqual(audit()["R299_complete_artificial_sources"],120)
    def test_next(self):self.assertEqual(audit()["next_candidate"],"02-008")
    def test_E2(self):self.assertEqual(audit()["new_real_E2"],0)
    def test_E3(self):self.assertEqual(audit()["new_historical_E3"],0)
    def test_science(self):self.assertFalse(audit()["all_239_scientifically_complete"])
    def test_prior_scope_remaining(self):self.assertEqual(audit()["older_scoped_only"],4)
    def test_readme_sha(self):self.assertEqual(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="02-005")["readme_git_blob_sha1"],blob(R/"README.md"))
    def test_R297_preserved(self):self.assertEqual(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="02-003")["proposed_primary_research_id"],"R297")
    def test_R298_preserved(self):self.assertEqual(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="02-004")["proposed_primary_research_id"],"R298")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R299catalogue"],verbosity=1)
    else:print(json.dumps(audit(),indent=2,ensure_ascii=False))
