#!/usr/bin/env python3
"""Independent original239 v2.1 one-row R306 polarization E1 and prior R072 codebook-blocker audit."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.0_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.1_2026-10-23.json"
Q42=D/"ORIGINAL_239_PENDING_42_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q41=D/"ORIGINAL_239_PENDING_41_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R306"

def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def gitblob(p):
    b=p.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def qrows(p):
    with p.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def audit():
    catalog=obj(CAT)["models"]
    old,new=obj(OLD),obj(NEW)
    before,after=old["rows"],new["rows"]
    assert len(catalog)==len(before)==len(after)==239
    assert len({x["catalogue_id"] for x in after})==239
    assert new["base_v2_0_path"]=="docs/"+OLD.name
    assert new["base_v2_0_git_blob_sha1"]==gitblob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["03-012"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R306"]
    assert new["existing_R_primary_relinked_IDs"]==old["existing_R_primary_relinked_IDs"]
    assert new["existing_R_primary_relinked_targets"]==old["existing_R_primary_relinked_targets"]
    changed=[]
    for c,p,n in zip(catalog,before,after):
        assert c["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert c["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert c["category"]==p["catalogue_category"]==n["catalogue_category"]
        assert c["priority"]==p["original_priority"]==n["original_priority"]
        if p!=n:changed.append(c["id"])
    assert changed==["03-012"]
    row=next(x for x in after if x["catalogue_id"]=="03-012")
    assert row["proposed_primary_research_id"]=="R306"
    assert row["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert row["readme_path"]=="research/R306/README.md" and row["readme_git_blob_sha1"]==gitblob(R/"README.md")
    assert row["source_csv_file_count"]==row["python_source_file_count"]==1
    assert row["formal_acceptance_filename_candidates"]==["research/R306/R306_FINAL_ACCEPTANCE_STATUS.json"]
    assert row["scientific_report_filenames"]==["research/R306/R306_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert row["P1_scoped_review_addendum"]["CI_run_id"]==39938339913
    assert row["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    assert row["P1_scoped_review_addendum"]["original_human_data_replayed"] is False
    a,rec,res=obj(R/"R306_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R306_MACHINE_RECEIPT.json"),obj(R/"R306_EXACT_GROUP_POLARIZATION_RESULTS.json")
    assert a["research_id"]=="R306" and a["original_catalogue_id"]=="03-012"
    assert a["ci_status"]=="completed" and a["ci_conclusion"]=="success" and a["ci_jobs_completed_success"]==3
    assert a["model_unittests_python311"]==a["model_unittests_python312"]==1959
    assert a["independent_source_auditor_tests_per_execution"]==17
    assert a["synthetic_worlds"]==216 and a["fully_labeled_original_person_source_rows"]==648
    assert a["averaging_strict_polarization_count_per_argument_context"]==0
    assert a["social_comparison_strict_polarization_count_per_argument_context"]==18
    assert a["supportive_argument_strict_polarization_nonzero_start_count"]==20
    assert a["counterargument_direction_flips_nonzero_start_count"]==20
    assert a["new_project_equation_not_original_author_fitted_model"] is True
    assert a["original_human_1969_or_1976_raw_behavior_replicated"] is False
    assert a["new_real_human_E2"]==a["new_real_animal_E2"]==a["new_historical_E3"]==0
    assert a["original_239_scientific_completion_established"] is False
    assert a["source_sha256"]==rec["source_sha256"]==hashlib.sha256((R/"R306_ALL_648_ORIGINAL_POLARIZATION_PERSON_SOURCES.csv").read_bytes()).hexdigest()
    assert a["results_sha256"]==rec["results_sha256"]==hashlib.sha256((R/"R306_EXACT_GROUP_POLARIZATION_RESULTS.json").read_bytes()).hexdigest()
    assert res["synthetic_group_worlds"]==216 and res["all_original_source_person_rows"]==648
    assert res["new_project_mathematics_not_original_Moscovici_Myers_fitted_equation"] is True
    assert res["frozen_reference"]["heterogeneous_combined_support"]=="3/4"
    assert res["status_counts_by_policy_and_argument"]["CONSENSUS_AVERAGING"]["SUPPORT_PRE_DISCUSSION_DIRECTION"]["POLARIZED"]==0
    assert res["status_counts_by_policy_and_argument"]["PERSUASIVE_ARGUMENT_ONLY"]["COUNTER_PRE_DISCUSSION_DIRECTION"]["DIRECTION_FLIP"]==20
    assert new["counts"]=={"primary_R":195,"shared_bounded_math":3,"older_scoped_only":3,"no_link_in_checked_sets":38,"pending_primary_R":41}
    assert new["status_counts"]==dict(collections.Counter(x["link_status"] for x in after))
    assert sum(new["status_counts"].values())==239
    q0,q1=qrows(Q42),qrows(Q41)
    assert len(q0)==42 and len(q1)==41
    assert q1==[row for row in q0 if row["original_catalogue_id"]!="03-012"]
    assert q1[0]["original_catalogue_id"]=="03-016"
    assert sum(x["priority"]=="P1" for x in q1)==14
    assert sum(x["priority"]=="P2" for x in q1)==27
    oldR072=next(x for x in after if x["catalogue_id"]=="03-010")
    assert oldR072["proposed_primary_research_id"]=="R072"
    assert oldR072["P1_scoped_review_addendum"]["latest_human_mechanism_E2"]=="NOT_IDENTIFIED"
    assert next(x for x in after if x["catalogue_id"]=="03-004")["proposed_primary_research_id"]=="R305"
    return {"original_models":239,"only_changed_original_id":"03-012",
        "primary_R_sources":195,"pending_sources":41,"pending_P1":14,"pending_P2":27,
        "R306_full_original_artificial_rows":648,"next_ID":"03-016",
        "prior_existing_R072_E2_blocker_preserved":True,
        "new_real_E2":0,"new_historical_E3":0,"whole_239_scientific_completion":False}
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed_original_id"],"03-012")
    def test_original(self):self.assertEqual(audit()["original_models"],239)
    def test_primary(self):self.assertEqual(audit()["primary_R_sources"],195)
    def test_pending(self):self.assertEqual(audit()["pending_sources"],41)
    def test_P1(self):self.assertEqual(audit()["pending_P1"],14)
    def test_P2(self):self.assertEqual(audit()["pending_P2"],27)
    def test_source(self):self.assertEqual(audit()["R306_full_original_artificial_rows"],648)
    def test_next(self):self.assertEqual(audit()["next_ID"],"03-016")
    def test_reused_R072(self):self.assertTrue(audit()["prior_existing_R072_E2_blocker_preserved"])
    def test_E2(self):self.assertEqual(audit()["new_real_E2"],0)
    def test_E3(self):self.assertEqual(audit()["new_historical_E3"],0)
    def test_not_all(self):self.assertFalse(audit()["whole_239_scientific_completion"])
    def test_readme_sha(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="03-012")["readme_git_blob_sha1"],gitblob(R/"README.md"))
    def test_original_humans_not_replicated(self):self.assertFalse(obj(R/"R306_FINAL_ACCEPTANCE_STATUS.json")["original_human_1969_or_1976_raw_behavior_replicated"])
    def test_previous_R305(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="03-004")["proposed_primary_research_id"],"R305")
    def test_old_R072(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="03-010")["proposed_primary_research_id"],"R072")
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R306 catalogue"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
