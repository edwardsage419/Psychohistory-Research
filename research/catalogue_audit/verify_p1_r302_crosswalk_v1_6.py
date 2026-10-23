#!/usr/bin/env python3
"""Independently verify R302 only modifies original catalogue 02-016 and remains exact artificial E1."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.5_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.6_2026-10-23.json"
QOLD=D/"ORIGINAL_239_PENDING_47_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
QNEW=D/"ORIGINAL_239_PENDING_46_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R302"

def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def gitblob(p):
    b=p.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def queue(p):
    with p.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def audit():
    catalog=obj(CAT)["models"]
    old,new=obj(OLD),obj(NEW)
    before,after=old["rows"],new["rows"]
    assert len(catalog)==len(before)==len(after)==239
    assert len(set(z["catalogue_id"] for z in after))==239
    assert new["base_v1_5_path"]=="docs/"+OLD.name
    assert new["base_v1_5_git_blob_sha1"]==gitblob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["02-016"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R302"]
    changed=[]
    for canonical,p,n in zip(catalog,before,after):
        assert canonical["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert canonical["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert canonical["priority"]==p["original_priority"]==n["original_priority"]
        assert canonical["category"]==p["catalogue_category"]==n["catalogue_category"]
        if p!=n:changed.append(canonical["id"])
    assert changed==["02-016"]
    target=next(x for x in after if x["catalogue_id"]=="02-016")
    assert target["proposed_primary_research_id"]=="R302" and target["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert target["readme_path"]=="research/R302/README.md" and target["readme_git_blob_sha1"]==gitblob(R/"README.md")
    assert target["formal_acceptance_filename_candidates"]==["research/R302/R302_FINAL_ACCEPTANCE_STATUS.json"]
    assert target["scientific_report_filenames"]==["research/R302/R302_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert target["source_csv_file_count"]==target["python_source_file_count"]==1
    assert target["P1_scoped_review_addendum"]["CI_run_id"]==39930778614
    assert target["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    acc,receipt,res=obj(R/"R302_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R302_MACHINE_RECEIPT.json"),obj(R/"R302_EXACT_BANDIT_THOMPSON_RESULTS.json")
    assert acc["research_id"]=="R302" and acc["original_catalogue_id"]=="02-016"
    assert acc["ci_status"]=="completed" and acc["ci_conclusion"]=="success" and acc["ci_jobs_completed_success"]==3
    assert acc["actual_model_unittests_python311"]==acc["actual_model_unittests_python312"]==660
    assert acc["independent_alternate_beta_integral_auditor_tests_per_execution"]==17
    assert acc["synthetic_count_worlds"]==81 and acc["complete_labeled_original_arm_sources"]==162
    assert acc["new_real_human_E2"]==acc["new_real_animal_E2"]==acc["new_historical_E3"]==0
    assert acc["empirical_bandit_regret_computed"] is False
    assert acc["UCB1_logarithmic_regret_theorem_reproduced"] is False
    assert acc["original_239_scientific_completion_established"] is False
    assert acc["source_sha256"]==receipt["source_sha256"]==hashlib.sha256((R/"R302_ALL_162_ORIGINAL_BETA_BANDIT_ARM_SOURCES.csv").read_bytes()).hexdigest()
    assert acc["results_sha256"]==receipt["results_sha256"]==hashlib.sha256((R/"R302_EXACT_BANDIT_THOMPSON_RESULTS.json").read_bytes()).hexdigest()
    assert res["synthetic_count_worlds"]==81 and res["original_labeled_source_rows"]==162
    assert res["reference_exact_cases"]["A_two_success_B_two_failure"]=="19/20"
    assert res["real_human_E2_added"]==res["real_animal_E2_added"]==res["historical_E3_added"]==0
    assert new["counts"]=={"primary_R":190,"shared_bounded_math":3,"older_scoped_only":4,"no_link_in_checked_sets":42,"pending_primary_R":46}
    assert new["status_counts"]==dict(collections.Counter(x["link_status"] for x in after))
    assert sum(new["status_counts"].values())==239
    q0,q1=queue(QOLD),queue(QNEW)
    assert len(q0)==47 and len(q1)==46
    assert q1==[x for x in q0 if x["original_catalogue_id"]!="02-016"]
    assert q1[0]["original_catalogue_id"]=="03-001"
    assert sum(x["priority"]=="P1" for x in q1)==19
    assert sum(x["priority"]=="P2" for x in q1)==27
    assert next(x for x in after if x["catalogue_id"]=="02-012")["proposed_primary_research_id"]=="R301"
    assert next(x for x in after if x["catalogue_id"]=="02-008")["proposed_primary_research_id"]=="R300"
    older=next(x for x in after if x["catalogue_id"]=="02-005")
    assert "research/R063/R063_EVIDENCE_AUDIT.md" in older["older_scoped_paths_present"]
    return {"original_candidates":239,"only_changed_id":"02-016","primary_R_links":190,
      "shared_bounded":3,"older_scoped_only":4,"pending":46,
      "pending_P1":19,"pending_P2":27,"R302_full_artificial_sources":162,
      "next_candidate":"03-001","prior_R063_R300_R301_preserved":True,
      "human_animal_E2":0,"historical_E3":0,"full_239_scientifically_complete":False}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed_id"],"02-016")
    def test_239(self):self.assertEqual(audit()["original_candidates"],239)
    def test_primary(self):self.assertEqual(audit()["primary_R_links"],190)
    def test_pending(self):self.assertEqual(audit()["pending"],46)
    def test_P1(self):self.assertEqual(audit()["pending_P1"],19)
    def test_P2(self):self.assertEqual(audit()["pending_P2"],27)
    def test_source(self):self.assertEqual(audit()["R302_full_artificial_sources"],162)
    def test_next(self):self.assertEqual(audit()["next_candidate"],"03-001")
    def test_prior(self):self.assertTrue(audit()["prior_R063_R300_R301_preserved"])
    def test_E2(self):self.assertEqual(audit()["human_animal_E2"],0)
    def test_E3(self):self.assertEqual(audit()["historical_E3"],0)
    def test_incomplete(self):self.assertFalse(audit()["full_239_scientifically_complete"])
    def test_readme_blob(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="02-016")["readme_git_blob_sha1"],gitblob(R/"README.md"))
    def test_R301_preserved(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="02-012")["proposed_primary_research_id"],"R301")
    def test_no_real_regret(self):self.assertFalse(obj(R/"R302_FINAL_ACCEPTANCE_STATUS.json")["empirical_bandit_regret_computed"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R302 catalogue"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
