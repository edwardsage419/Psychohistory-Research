#!/usr/bin/env python3
"""Original239 v2.4 one-row SIR E1 provenance and SHA audit; no imported producer."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.3_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.4_2026-10-23.json"
QOLD=D/"ORIGINAL_239_PENDING_39_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
QNEW=D/"ORIGINAL_239_PENDING_38_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R309"
def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def gitblob(p):
    b=p.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\0"+b).hexdigest()
def queue(p):
    with p.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def audit():
    canon=obj(CAT)["models"];old,new=obj(OLD),obj(NEW)
    before,after=old["rows"],new["rows"]
    assert len(canon)==len(before)==len(after)==239
    assert len({r["catalogue_id"] for r in after})==239
    assert new["base_v2_3_path"]=="docs/"+OLD.name
    assert new["base_v2_3_git_blob_sha1"]==gitblob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["04-006"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R309"]
    assert new["existing_R_primary_relinked_IDs"]==old["existing_R_primary_relinked_IDs"]
    assert new["existing_R_primary_relinked_targets"]==old["existing_R_primary_relinked_targets"]
    changes=[]
    for original,p,n in zip(canon,before,after):
        assert original["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert original["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert original["priority"]==p["original_priority"]==n["original_priority"]
        assert original["category"]==p["catalogue_category"]==n["catalogue_category"]
        if p!=n:changes.append(original["id"])
    assert changes==["04-006"]
    row=next(x for x in after if x["catalogue_id"]=="04-006")
    assert row["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert row["proposed_primary_research_id"]=="R309"
    assert row["readme_path"]=="research/R309/README.md"
    assert row["readme_git_blob_sha1"]==gitblob(R/"README.md")
    assert row["source_csv_file_count"]==row["python_source_file_count"]==1
    assert row["formal_acceptance_filename_candidates"]==["research/R309/R309_FINAL_ACCEPTANCE_STATUS.json"]
    assert row["scientific_report_filenames"]==["research/R309/R309_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert row["P1_scoped_review_addendum"]["CI_run_id"]==39955168677
    assert row["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    assert row["P1_scoped_review_addendum"]["original_1927_continuous_math_not_replicated"] is True
    a,rec,res=obj(R/"R309_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R309_MACHINE_RECEIPT.json"),obj(R/"R309_EXACT_FIVE_AGENT_SIR_RESULTS.json")
    assert a["research_id"]=="R309" and a["original_catalogue_id"]=="04-006"
    assert a["ci_status"]=="completed" and a["ci_conclusion"]=="success" and a["ci_jobs_completed_success"]==3
    assert a["model_unittests_python311"]==a["model_unittests_python312"]==3417
    assert a["independent_microstate_auditor_tests_per_execution"]==17
    assert a["synthetic_worlds"]==189 and a["complete_original_source_rows"]==1134
    assert a["elementary_independent_contact_recovery_mask_assignments"]==11664
    assert a["project_defined_discrete_binomial_model_not_original_1927_continuous_equations"] is True
    assert a["real_clinical_or_cultural_diffusion_validation"] is False
    assert a["new_real_human_E2"]==a["new_real_animal_E2"]==a["new_historical_E3"]==0
    assert a["original239_scientific_completion_established"] is False
    assert a["source_sha256"]==rec["source_sha256"]==hashlib.sha256((R/"R309_ALL_1134_ORIGINAL_SIR_TRANSITION_SOURCES.csv").read_bytes()).hexdigest()
    assert a["results_sha256"]==rec["results_sha256"]==hashlib.sha256((R/"R309_EXACT_FIVE_AGENT_SIR_RESULTS.json").read_bytes()).hexdigest()
    assert res["synthetic_worlds"]==189 and res["complete_original_transition_source_rows"]==1134
    assert res["project_discrete_independent_contact_assumption_not_exact_Kermack_McKendrick_1927_equation"] is True
    assert res["frozen_reference"]["S3_I2_p1_q1_simultaneous_next_state"]=="0,3,2"
    assert res["frozen_reference"]["sum_over_all_world_one_step_microstate_assignments_per_nine_parameters"]==11664
    assert new["counts"]=={"primary_R":198,"shared_bounded_math":3,"older_scoped_only":3,"no_link_in_checked_sets":35,"pending_primary_R":38}
    assert new["status_counts"]==dict(collections.Counter(z["link_status"] for z in after))
    assert sum(new["status_counts"].values())==239
    q0,q1=queue(QOLD),queue(QNEW)
    assert len(q0)==39 and len(q1)==38
    assert q1==[z for z in q0 if z["original_catalogue_id"]!="04-006"]
    assert q1[0]["original_catalogue_id"]=="04-008"
    assert sum(x["priority"]=="P1" for x in q1)==11
    assert sum(x["priority"]=="P2" for x in q1)==27
    assert next(z for z in after if z["catalogue_id"]=="03-016")["proposed_primary_research_id"]=="R307"
    assert next(z for z in after if z["catalogue_id"]=="03-018")["proposed_primary_research_id"]=="R308"
    old072=next(z for z in after if z["catalogue_id"]=="03-010")
    assert old072["proposed_primary_research_id"]=="R072"
    assert old072["P1_scoped_review_addendum"]["latest_human_mechanism_E2"]=="NOT_IDENTIFIED"
    return {"original_candidates":239,"only_changed_original":"04-006","primary_R_links":198,
      "pending":38,"pending_P1":11,"pending_P2":27,"R309_original_artificial_transition_rows":1134,
      "R309_independent_contact_and_recovery_microstates":11664,"next_candidate":"04-008",
      "R072_E2_blocker_and_R307_R308_preserved":True,
      "new_real_E2":0,"new_historical_E3":0,"whole_catalogue_scientific_completion":False}
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed_original"],"04-006")
    def test_original(self):self.assertEqual(audit()["original_candidates"],239)
    def test_primary(self):self.assertEqual(audit()["primary_R_links"],198)
    def test_pending(self):self.assertEqual(audit()["pending"],38)
    def test_P1(self):self.assertEqual(audit()["pending_P1"],11)
    def test_P2(self):self.assertEqual(audit()["pending_P2"],27)
    def test_sources(self):self.assertEqual(audit()["R309_original_artificial_transition_rows"],1134)
    def test_micro(self):self.assertEqual(audit()["R309_independent_contact_and_recovery_microstates"],11664)
    def test_next(self):self.assertEqual(audit()["next_candidate"],"04-008")
    def test_prior(self):self.assertTrue(audit()["R072_E2_blocker_and_R307_R308_preserved"])
    def test_e2(self):self.assertEqual(audit()["new_real_E2"],0)
    def test_e3(self):self.assertEqual(audit()["new_historical_E3"],0)
    def test_not_all(self):self.assertFalse(audit()["whole_catalogue_scientific_completion"])
    def test_source_sha(self):self.assertEqual(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="04-006")["readme_git_blob_sha1"],gitblob(R/"README.md"))
    def test_not_continuous_original(self):self.assertTrue(obj(R/"R309_FINAL_ACCEPTANCE_STATUS.json")["project_defined_discrete_binomial_model_not_original_1927_continuous_equations"])
    def test_existing_r072(self):self.assertEqual(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="03-010")["proposed_primary_research_id"],"R072")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R309 catalogue"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
