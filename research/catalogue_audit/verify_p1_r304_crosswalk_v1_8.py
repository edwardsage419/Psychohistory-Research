#!/usr/bin/env python3
"""Independent original 239 candidate 03-003-only R304 social identity toy provenance audit."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.7_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.8_2026-10-23.json"
Q45=D/"ORIGINAL_239_PENDING_45_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q44=D/"ORIGINAL_239_PENDING_44_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R304"

def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def gitblob(p):
    b=p.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def queue(p):
    with p.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def audit():
    canon=obj(CAT)["models"]
    before,after=obj(OLD),obj(NEW)
    a,b=before["rows"],after["rows"]
    assert len(canon)==len(a)==len(b)==239
    assert len({x["catalogue_id"] for x in b})==239
    assert after["base_v1_7_path"]=="docs/"+OLD.name
    assert after["base_v1_7_git_blob_sha1"]==gitblob(OLD)
    assert after["changed_original_IDs"]==before["changed_original_IDs"]+["03-003"]
    assert after["E1_new_research"]==before["E1_new_research"]+["R304"]
    changed=[]
    for c,old,new in zip(canon,a,b):
        assert c["id"]==old["catalogue_id"]==new["catalogue_id"]
        assert c["name_en"]==old["catalogue_name_en"]==new["catalogue_name_en"]
        assert c["category"]==old["catalogue_category"]==new["catalogue_category"]
        assert c["priority"]==old["original_priority"]==new["original_priority"]
        if old!=new:changed.append(c["id"])
    assert changed==["03-003"]
    row=next(z for z in b if z["catalogue_id"]=="03-003")
    assert row["proposed_primary_research_id"]=="R304"
    assert row["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert row["readme_path"]=="research/R304/README.md"
    assert row["readme_git_blob_sha1"]==gitblob(R/"README.md")
    assert row["source_csv_file_count"]==row["python_source_file_count"]==1
    assert row["formal_acceptance_filename_candidates"]==["research/R304/R304_FINAL_ACCEPTANCE_STATUS.json"]
    assert row["scientific_report_filenames"]==["research/R304/R304_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert row["P1_scoped_review_addendum"]["CI_run_id"]==39934709217
    assert row["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    assert row["P1_scoped_review_addendum"]["author_Tajfel_original_quantitative_model_replicated"] is False
    acc,receipt,res=obj(R/"R304_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R304_MACHINE_RECEIPT.json"),obj(R/"R304_EXACT_SOCIAL_IDENTITY_ALLOCATION_RESULTS.json")
    assert acc["research_id"]=="R304" and acc["original_catalogue_id"]=="03-003"
    assert acc["ci_status"]=="completed" and acc["ci_conclusion"]=="success" and acc["ci_jobs_completed_success"]==3
    assert acc["model_unittests_python311"]==acc["model_unittests_python312"]==1310
    assert acc["independent_source_auditor_tests_per_execution"]==17
    assert acc["artificial_worlds"]==216 and acc["fully_labeled_original_option_sources"]==432
    assert acc["alternate_choice_artificial_worlds"]==12 and acc["lower_total_favoring_alternate_worlds"]==2
    assert acc["new_project_invented_utility_not_Tajfel_1971_author_equation"] is True
    assert acc["Tajfel_1971_original_human_allocation_data_reanalyzed"] is False
    assert acc["self_categorization_theory_03_004_accepted_by_this_study"] is False
    assert acc["new_real_human_E2"]==acc["new_real_animal_E2"]==acc["new_historical_E3"]==0
    assert acc["original_239_scientific_completion_established"] is False
    assert acc["original_source_sha256"]==receipt["source_sha256"]==hashlib.sha256((R/"R304_ALL_432_ORIGINAL_MINIMAL_GROUP_ALLOCATION_OPTIONS.csv").read_bytes()).hexdigest()
    assert acc["results_sha256"]==receipt["results_sha256"]==hashlib.sha256((R/"R304_EXACT_SOCIAL_IDENTITY_ALLOCATION_RESULTS.json").read_bytes()).hexdigest()
    assert res["synthetic_worlds"]==216 and res["complete_option_source_rows"]==432
    assert res["summary"]["artificial_alternative_chosen_worlds"]==12
    assert res["summary"]["lower_total_alternatives_chosen"]==2
    assert res["social_identity_model_utility_invented_by_project"] is True
    assert after["counts"]=={"primary_R":192,"shared_bounded_math":3,"older_scoped_only":4,"no_link_in_checked_sets":40,"pending_primary_R":44}
    assert after["status_counts"]==dict(collections.Counter(x["link_status"] for x in b))
    assert sum(after["status_counts"].values())==239
    qold,qnew=queue(Q45),queue(Q44)
    assert len(qold)==45 and len(qnew)==44
    assert qnew==[x for x in qold if x["original_catalogue_id"]!="03-003"]
    assert qnew[0]["original_catalogue_id"]=="03-004"
    assert sum(x["priority"]=="P1" for x in qnew)==17
    assert sum(x["priority"]=="P2" for x in qnew)==27
    assert next(x for x in b if x["catalogue_id"]=="03-004")["proposed_primary_research_id"] is None
    assert next(x for x in b if x["catalogue_id"]=="03-001")["proposed_primary_research_id"]=="R303"
    oldR063=next(x for x in b if x["catalogue_id"]=="02-005")
    assert "research/R063/R063_EVIDENCE_AUDIT.md" in oldR063["older_scoped_paths_present"]
    return {"original_239":239,"only_changed_original":"03-003",
       "primary_R_links":192,"shared_math":3,"old_scoped":4,
       "pending_primary":44,"pending_P1":17,"pending_P2":27,
       "R304_original_synthetic_sources":432,"next_original_candidate":"03-004",
       "R303_and_R063_prior_scope_preserved":True,
       "new_real_E2":0,"historical_E3":0,"239_scientific_completion":False}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed_original"],"03-003")
    def test_239(self):self.assertEqual(audit()["original_239"],239)
    def test_primary(self):self.assertEqual(audit()["primary_R_links"],192)
    def test_pending(self):self.assertEqual(audit()["pending_primary"],44)
    def test_P1(self):self.assertEqual(audit()["pending_P1"],17)
    def test_P2(self):self.assertEqual(audit()["pending_P2"],27)
    def test_sources(self):self.assertEqual(audit()["R304_original_synthetic_sources"],432)
    def test_next(self):self.assertEqual(audit()["next_original_candidate"],"03-004")
    def test_prior(self):self.assertTrue(audit()["R303_and_R063_prior_scope_preserved"])
    def test_E2(self):self.assertEqual(audit()["new_real_E2"],0)
    def test_E3(self):self.assertEqual(audit()["historical_E3"],0)
    def test_incomplete(self):self.assertFalse(audit()["239_scientific_completion"])
    def test_distinct_next(self):self.assertIsNone(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="03-004")["proposed_primary_research_id"])
    def test_readme_git_blob(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="03-003")["readme_git_blob_sha1"],gitblob(R/"README.md"))
    def test_Tajfel_no_original_fit(self):self.assertFalse(obj(R/"R304_FINAL_ACCEPTANCE_STATUS.json")["Tajfel_1971_original_human_allocation_data_reanalyzed"])
    def test_R303_preserved(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="03-001")["proposed_primary_research_id"],"R303")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R304 original239"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
