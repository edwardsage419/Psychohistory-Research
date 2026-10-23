#!/usr/bin/env python3
"""Original 239 v1.7 R303 independent one-row and Bandura/R063 scope audit."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.6_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.7_2026-10-23.json"
Q46=D/"ORIGINAL_239_PENDING_46_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q45=D/"ORIGINAL_239_PENDING_45_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R303"
R063=ROOT/"research/R063/R063_EVIDENCE_AUDIT.md"

def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def blob(p):
    b=p.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def queue(p):
    with p.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def audit():
    catalog=obj(CAT)["models"]
    old,new=obj(OLD),obj(NEW)
    before,after=old["rows"],new["rows"]
    assert len(catalog)==len(before)==len(after)==239
    assert len({r["catalogue_id"] for r in after})==239
    assert new["base_v1_6_path"]=="docs/"+OLD.name
    assert new["base_v1_6_git_blob_sha1"]==blob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["03-001"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R303"]
    differences=[]
    for c,p,n in zip(catalog,before,after):
        assert c["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert c["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert c["category"]==p["catalogue_category"]==n["catalogue_category"]
        assert c["priority"]==p["original_priority"]==n["original_priority"]
        if p!=n:differences.append(c["id"])
    assert differences==["03-001"]
    x=next(z for z in after if z["catalogue_id"]=="03-001")
    assert x["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert x["proposed_primary_research_id"]=="R303"
    assert x["readme_path"]=="research/R303/README.md"
    assert x["readme_git_blob_sha1"]==blob(R/"README.md")
    assert x["source_csv_file_count"]==x["python_source_file_count"]==1
    assert x["formal_acceptance_filename_candidates"]==["research/R303/R303_FINAL_ACCEPTANCE_STATUS.json"]
    assert x["scientific_report_filenames"]==["research/R303/R303_SCIENTIFIC_REPORT_2026-10-23.md"]
    extra=x["P1_scoped_review_addendum"]
    assert extra["CI_success_run_id"]==39934165046 and extra["CI_first_failed_run_id"]==39934080577
    assert extra["actual_subject_or_historical_data"]==0
    assert extra["project_new_probability_equation_not_bandura_original"] is True
    assert extra["related_but_not_same_original_author_or_mechanism"]=="research/R063/R063_EVIDENCE_AUDIT.md"
    a,receipt,res=obj(R/"R303_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R303_MACHINE_RECEIPT.json"),obj(R/"R303_EXACT_ACQUISITION_VS_EXPRESSION_RESULTS.json")
    assert a["research_id"]=="R303" and a["original_catalogue_id"]=="03-001"
    assert a["ci_status"]=="completed" and a["ci_conclusion"]=="success" and a["ci_jobs_completed_success"]==3
    assert a["first_failed_ci_run_id"]==39934080577
    assert a["first_failed_ci_did_not_pass_archive"] is True
    assert a["successful_ci_run_id"]==39934165046
    assert a["actual_model_unittests_python311"]==a["actual_model_unittests_python312"]==1473
    assert a["independent_five_binary_gate_auditor_tests_per_execution"]==17
    assert a["synthetic_worlds"]==243 and a["complete_original_phase_sources"]==486
    assert a["project_custom_gate_equation_not_in_Bandura_1965"] is True
    assert a["Bandura_original_human_experiment_replicated"] is False
    assert a["R063_Najar_original_human_studies_not_reused_as_R303_E2"] is True
    assert a["new_real_human_E2"]==a["new_real_animal_E2"]==a["new_historical_E3"]==0
    assert a["original_239_scientific_completion_established"] is False
    assert a["original_source_sha256"]==receipt["source_sha256"]==hashlib.sha256((R/"R303_ALL_486_ORIGINAL_OBSERVATIONAL_SOURCE_PHASES.csv").read_bytes()).hexdigest()
    assert a["results_sha256"]==receipt["results_sha256"]==hashlib.sha256((R/"R303_EXACT_ACQUISITION_VS_EXPRESSION_RESULTS.json").read_bytes()).hexdigest()
    assert res["original_phase_source_rows"]==486 and res["synthetic_worlds"]==243
    assert res["research_project_custom_multiplicative_probability_equations_not_bandura_original"] is True
    assert res["reference_case"]["fully_attending_retaining_producing_motivation_half_PUNISHED_spontaneous"]=="1/8"
    assert new["counts"]=={"primary_R":191,"shared_bounded_math":3,"older_scoped_only":4,"no_link_in_checked_sets":41,"pending_primary_R":45}
    assert new["status_counts"]==dict(collections.Counter(z["link_status"] for z in after))
    assert sum(new["status_counts"].values())==239
    a0,b0=queue(Q46),queue(Q45)
    assert len(a0)==46 and len(b0)==45
    assert b0==[row for row in a0 if row["original_catalogue_id"]!="03-001"]
    assert b0[0]["original_catalogue_id"]=="03-003"
    assert sum(x["priority"]=="P1" for x in b0)==18
    assert sum(x["priority"]=="P2" for x in b0)==27
    oldR063=next(z for z in after if z["catalogue_id"]=="02-005")
    assert "research/R063/R063_EVIDENCE_AUDIT.md" in oldR063["older_scoped_paths_present"]
    assert "Najar" in R063.read_text(encoding="utf-8")
    assert next(z for z in after if z["catalogue_id"]=="02-016")["proposed_primary_research_id"]=="R302"
    return {"original_candidates":239,"only_changed_original":"03-001",
       "primary_R_links":191,"shared_bounded":3,"old_scoped_only":4,
       "pending":45,"pending_P1":18,"pending_P2":27,
       "R303_original_artificial_phase_sources":486,"next_original_id":"03-003",
       "earlier_failed_run_reported":True,"original_R063_independent_scope_preserved":True,
       "real_human_or_animal_E2_added":0,"historical_E3_added":0,
       "full_scientific_239_acceptance_established":False}
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed_original"],"03-001")
    def test_239(self):self.assertEqual(audit()["original_candidates"],239)
    def test_primary(self):self.assertEqual(audit()["primary_R_links"],191)
    def test_pending(self):self.assertEqual(audit()["pending"],45)
    def test_P1(self):self.assertEqual(audit()["pending_P1"],18)
    def test_P2(self):self.assertEqual(audit()["pending_P2"],27)
    def test_486_sources(self):self.assertEqual(audit()["R303_original_artificial_phase_sources"],486)
    def test_next(self):self.assertEqual(audit()["next_original_id"],"03-003")
    def test_R063(self):self.assertTrue(audit()["original_R063_independent_scope_preserved"])
    def test_failed_attempt_visible(self):self.assertTrue(audit()["earlier_failed_run_reported"])
    def test_E2(self):self.assertEqual(audit()["real_human_or_animal_E2_added"],0)
    def test_E3(self):self.assertEqual(audit()["historical_E3_added"],0)
    def test_not_complete(self):self.assertFalse(audit()["full_scientific_239_acceptance_established"])
    def test_readme_sha(self):self.assertEqual(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="03-001")["readme_git_blob_sha1"],blob(R/"README.md"))
    def test_not_Bandura_original_equation(self):self.assertTrue(obj(R/"R303_FINAL_ACCEPTANCE_STATUS.json")["project_custom_gate_equation_not_in_Bandura_1965"])
    def test_prior_R302(self):self.assertEqual(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="02-016")["proposed_primary_research_id"],"R302")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R303 provenance"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
