#!/usr/bin/env python3
"""Original 239 evidence crosswalk v1.9 independent R305-only 03-004 and no-empirical-promotion verifier."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
DOCS=ROOT/"docs"
CAT=DOCS/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=DOCS/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.8_2026-10-23.json"
NEW=DOCS/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.9_2026-10-23.json"
P44=DOCS/"ORIGINAL_239_PENDING_44_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
P43=DOCS/"ORIGINAL_239_PENDING_43_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R305"

def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def gitblob(p):
    b=p.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def qrows(p):
    with p.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def audit():
    c=obj(CAT)["models"]
    old,new=obj(OLD),obj(NEW)
    before,after=old["rows"],new["rows"]
    assert len(c)==len(before)==len(after)==239
    assert len({x["catalogue_id"] for x in after})==239
    assert new["base_v1_8_path"]=="docs/"+OLD.name
    assert new["base_v1_8_git_blob_sha1"]==gitblob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["03-004"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R305"]
    changed=[]
    for canon,p,n in zip(c,before,after):
        assert canon["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert canon["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert canon["priority"]==p["original_priority"]==n["original_priority"]
        assert canon["category"]==p["catalogue_category"]==n["catalogue_category"]
        if p!=n:changed.append(canon["id"])
    assert changed==["03-004"]
    t=next(z for z in after if z["catalogue_id"]=="03-004")
    assert t["proposed_primary_research_id"]=="R305"
    assert t["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert t["readme_path"]=="research/R305/README.md" and t["readme_git_blob_sha1"]==gitblob(R/"README.md")
    assert t["formal_acceptance_filename_candidates"]==["research/R305/R305_FINAL_ACCEPTANCE_STATUS.json"]
    assert t["scientific_report_filenames"]==["research/R305/R305_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert t["source_csv_file_count"]==t["python_source_file_count"]==1
    assert t["P1_scoped_review_addendum"]["CI_run_id"]==39937267071
    assert t["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    assert t["P1_scoped_review_addendum"]["original_Turner_experimental_data_reused"] is False
    a,rec,res=obj(R/"R305_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R305_MACHINE_RECEIPT.json"),obj(R/"R305_EXACT_SCT_COMPARATIVE_FIT_RESULTS.json")
    assert a["research_id"]=="R305" and a["original_catalogue_id"]=="03-004"
    assert a["ci_status"]=="completed" and a["ci_conclusion"]=="success" and a["ci_jobs_completed_success"]==3
    assert a["model_unittests_python311"]==a["model_unittests_python312"]==1473
    assert a["independent_six_pair_audit_unittests_per_execution"]==18
    assert a["artificial_worlds"]==243 and a["complete_original_category_source_rows"]==486
    assert a["project_custom_score_rule_not_original_Turner_author_fitted_equation"] is True
    assert a["original_Turner_human_self_categorization_data_replicated"] is False
    assert a["self_categorization_full_theory_accepted"] is False
    assert a["R304_Tajfel_social_identity_allocation_study_independent_and_unchanged"] is True
    assert a["new_real_human_E2"]==a["new_real_animal_E2"]==a["new_historical_E3"]==0
    assert a["original_239_scientific_completion_established"] is False
    assert a["source_sha256"]==rec["source_sha256"]==hashlib.sha256((R/"R305_ALL_486_ORIGINAL_SELF_CATEGORIZATION_SOURCE_CELLS.csv").read_bytes()).hexdigest()
    assert a["results_sha256"]==rec["results_sha256"]==hashlib.sha256((R/"R305_EXACT_SCT_COMPARATIVE_FIT_RESULTS.json").read_bytes()).hexdigest()
    assert res["complete_labeled_original_source_rows"]==486 and res["artificial_worlds"]==243
    assert res["model_scoring_rule_project_invented_not_Turner_1985_author_equation"] is True
    assert res["frozen_reference"]["X_comparative_fit_P"]=="4"
    assert res["frozen_reference"]["Y_comparative_fit_Q"]=="4"
    assert new["counts"]=={"primary_R":193,"shared_bounded_math":3,"older_scoped_only":4,"no_link_in_checked_sets":39,"pending_primary_R":43}
    assert new["status_counts"]==dict(collections.Counter(x["link_status"] for x in after))
    assert sum(new["status_counts"].values())==239
    q0,q1=qrows(P44),qrows(P43)
    assert len(q0)==44 and len(q1)==43
    assert q1==[row for row in q0 if row["original_catalogue_id"]!="03-004"]
    assert q1[0]["original_catalogue_id"]=="03-010"
    assert sum(x["priority"]=="P1" for x in q1)==16
    assert sum(x["priority"]=="P2" for x in q1)==27
    assert next(x for x in after if x["catalogue_id"]=="03-003")["proposed_primary_research_id"]=="R304"
    assert next(x for x in after if x["catalogue_id"]=="03-001")["proposed_primary_research_id"]=="R303"
    r063=next(x for x in after if x["catalogue_id"]=="02-005")
    assert "research/R063/R063_EVIDENCE_AUDIT.md" in r063["older_scoped_paths_present"]
    return {"original_239":239,"only_changed_id":"03-004","primary_R_links":193,
      "old_scoped_only":4,"shared_math":3,"pending":43,"P1_pending":16,"P2_pending":27,
      "R305_full_artificial_sources":486,"next_original_id":"03-010",
      "prior_R063_R303_R304_still_independent":True,
      "new_empirical_E2":0,"new_historical_E3":0,
      "all_239_scientifically_accepted":False}
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed_id"],"03-004")
    def test_239(self):self.assertEqual(audit()["original_239"],239)
    def test_primary(self):self.assertEqual(audit()["primary_R_links"],193)
    def test_pending(self):self.assertEqual(audit()["pending"],43)
    def test_P1(self):self.assertEqual(audit()["P1_pending"],16)
    def test_P2(self):self.assertEqual(audit()["P2_pending"],27)
    def test_sources(self):self.assertEqual(audit()["R305_full_artificial_sources"],486)
    def test_next(self):self.assertEqual(audit()["next_original_id"],"03-010")
    def test_prior(self):self.assertTrue(audit()["prior_R063_R303_R304_still_independent"])
    def test_no_E2(self):self.assertEqual(audit()["new_empirical_E2"],0)
    def test_no_E3(self):self.assertEqual(audit()["new_historical_E3"],0)
    def test_science_not_full(self):self.assertFalse(audit()["all_239_scientifically_accepted"])
    def test_R304(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="03-003")["proposed_primary_research_id"],"R304")
    def test_git_blob(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="03-004")["readme_git_blob_sha1"],gitblob(R/"README.md"))
    def test_Turner_no_real_fit(self):self.assertFalse(obj(R/"R305_FINAL_ACCEPTANCE_STATUS.json")["original_Turner_human_self_categorization_data_replicated"])
    def test_not_full_theory(self):self.assertFalse(obj(R/"R305_FINAL_ACCEPTANCE_STATUS.json")["self_categorization_full_theory_accepted"])
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R305 catalogue"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
