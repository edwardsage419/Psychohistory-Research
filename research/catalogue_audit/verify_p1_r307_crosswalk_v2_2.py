#!/usr/bin/env python3
"""Original 239 v2.2 independent R307-only 03-016 source and nonidentifiability gate audit."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.1_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.2_2026-10-23.json"
Q41=D/"ORIGINAL_239_PENDING_41_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q40=D/"ORIGINAL_239_PENDING_40_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R307"

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def blob(path):
    b=path.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def qrows(path):
    with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def audit():
    catalog=obj(CAT)["models"]
    old,new=obj(OLD),obj(NEW)
    before,after=old["rows"],new["rows"]
    assert len(catalog)==len(before)==len(after)==239
    assert len({r["catalogue_id"] for r in after})==239
    assert new["base_v2_1_path"]=="docs/"+OLD.name
    assert new["base_v2_1_git_blob_sha1"]==blob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["03-016"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R307"]
    assert new["existing_R_primary_relinked_IDs"]==old["existing_R_primary_relinked_IDs"]
    changed=[]
    for canonical,p,n in zip(catalog,before,after):
        assert canonical["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert canonical["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert canonical["priority"]==p["original_priority"]==n["original_priority"]
        assert canonical["category"]==p["catalogue_category"]==n["catalogue_category"]
        if p!=n:changed.append(canonical["id"])
    assert changed==["03-016"]
    row=next(r for r in after if r["catalogue_id"]=="03-016")
    assert row["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert row["proposed_primary_research_id"]=="R307"
    assert row["readme_path"]=="research/R307/README.md"
    assert row["readme_git_blob_sha1"]==blob(R/"README.md")
    assert row["source_csv_file_count"]==row["python_source_file_count"]==1
    assert row["formal_acceptance_filename_candidates"]==["research/R307/R307_FINAL_ACCEPTANCE_STATUS.json"]
    assert row["scientific_report_filenames"]==["research/R307/R307_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert row["P1_scoped_review_addendum"]["CI_run_id"]==39953705822
    assert row["P1_scoped_review_addendum"]["consistency_credibility_nonidentifiability_flag"] is True
    assert row["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    a,receipt,res=obj(R/"R307_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R307_MACHINE_RECEIPT.json"),obj(R/"R307_EXACT_MINORITY_INFLUENCE_RESULTS.json")
    assert a["research_id"]=="R307" and a["original_catalogue_id"]=="03-016"
    assert a["ci_status"]=="completed" and a["ci_conclusion"]=="success" and a["ci_jobs_completed_success"]==3
    assert a["actual_model_unittests_py311"]==a["actual_model_unittests_py312"]==2607
    assert a["independent_sequential_bayes_source_auditor_tests_per_execution"]==18
    assert a["artificial_worlds"]==432 and a["complete_original_source_rows"]==864
    assert a["consistency_credibility_individually_identified_from_final_response"] is False
    assert a["original_authors_human_data_or_1994_meta_replicated"] is False
    assert a["new_real_human_E2"]==a["new_real_animal_E2"]==a["new_historical_E3"]==0
    assert a["original239_scientific_completion_established"] is False
    assert a["source_sha256"]==receipt["source_sha256"]==hashlib.sha256((R/"R307_ALL_864_ORIGINAL_MINORITY_PRIVATE_PUBLIC_SOURCES.csv").read_bytes()).hexdigest()
    assert a["results_sha256"]==receipt["results_sha256"]==hashlib.sha256((R/"R307_EXACT_MINORITY_INFLUENCE_RESULTS.json").read_bytes()).hexdigest()
    assert res["synthetic_worlds"]==432 and res["all_labeled_original_source_rows"]==864
    assert res["project_custom_evidence_lr_and_public_suppression_not_original_authors_equations"] is True
    assert res["frozen_reference"]["prior_quarter_three_consistent_credible_private"]=="8/11"
    assert res["frozen_reference"]["same_world_one_norm_two_of_six_public"]=="9/22"
    assert res["frozen_reference"]["same_world_one_norm_one_of_six_public"]=="29/88"
    assert res["frozen_reference"]["half_consistency_full_credibility_private"]==res["frozen_reference"]["full_consistency_half_credibility_private"]=="9/17"
    assert new["counts"]=={"primary_R":196,"shared_bounded_math":3,"older_scoped_only":3,"no_link_in_checked_sets":37,"pending_primary_R":40}
    assert new["status_counts"]==dict(collections.Counter(z["link_status"] for z in after))
    assert sum(new["status_counts"].values())==239
    qold,qnew=qrows(Q41),qrows(Q40)
    assert len(qold)==41 and len(qnew)==40
    assert qnew==[z for z in qold if z["original_catalogue_id"]!="03-016"]
    assert qnew[0]["original_catalogue_id"]=="03-018"
    assert sum(z["priority"]=="P1" for z in qnew)==13
    assert sum(z["priority"]=="P2" for z in qnew)==27
    assert next(z for z in after if z["catalogue_id"]=="03-012")["proposed_primary_research_id"]=="R306"
    assert next(z for z in after if z["catalogue_id"]=="03-010")["proposed_primary_research_id"]=="R072"
    assert next(z for z in after if z["catalogue_id"]=="03-010")["P1_scoped_review_addendum"]["latest_human_mechanism_E2"]=="NOT_IDENTIFIED"
    return {"original_239":239,"only_changed_id":"03-016","primary_R":196,
      "pending":40,"P1_pending":13,"P2_pending":27,
      "R307_original_synthetic_rows":864,"next_ID":"03-018",
      "original_R072_R306_preserved":True,
      "real_human_E2":0,"historical_E3":0,"all_models_scientifically_accepted":False}

class Tests(unittest.TestCase):
    def test_main(self):self.assertEqual(audit()["only_changed_id"],"03-016")
    def test_total(self):self.assertEqual(audit()["original_239"],239)
    def test_primary(self):self.assertEqual(audit()["primary_R"],196)
    def test_pending(self):self.assertEqual(audit()["pending"],40)
    def test_P1(self):self.assertEqual(audit()["P1_pending"],13)
    def test_P2(self):self.assertEqual(audit()["P2_pending"],27)
    def test_sources(self):self.assertEqual(audit()["R307_original_synthetic_rows"],864)
    def test_next(self):self.assertEqual(audit()["next_ID"],"03-018")
    def test_prior(self):self.assertTrue(audit()["original_R072_R306_preserved"])
    def test_E2(self):self.assertEqual(audit()["real_human_E2"],0)
    def test_E3(self):self.assertEqual(audit()["historical_E3"],0)
    def test_not_full(self):self.assertFalse(audit()["all_models_scientifically_accepted"])
    def test_readme(self):self.assertEqual(next(r for r in obj(NEW)["rows"] if r["catalogue_id"]=="03-016")["readme_git_blob_sha1"],blob(R/"README.md"))
    def test_no_human(self):self.assertFalse(obj(R/"R307_FINAL_ACCEPTANCE_STATUS.json")["original_authors_human_data_or_1994_meta_replicated"])
    def test_not_identifiable(self):self.assertFalse(obj(R/"R307_FINAL_ACCEPTANCE_STATUS.json")["consistency_credibility_individually_identified_from_final_response"])
    def test_R306(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="03-012")["proposed_primary_research_id"],"R306")

if __name__=="__main__":
    p=argparse.ArgumentParser();m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true");m.add_argument("--audit",action="store_true")
    z=p.parse_args()
    if z.test:unittest.main(argv=["R307 catalogue"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
