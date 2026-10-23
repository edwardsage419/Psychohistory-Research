#!/usr/bin/env python3
"""R301 independent original 239 candidate one-row BOCPD provenance and E1 source audit."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.4_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.5_2026-10-23.json"
Q48=D/"ORIGINAL_239_PENDING_48_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q47=D/"ORIGINAL_239_PENDING_47_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R301"

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def blob(path):
    b=path.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def queue(path):
    with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def verify():
    canon=obj(CAT)["models"]
    before,after=obj(OLD),obj(NEW)
    a,b=before["rows"],after["rows"]
    assert len(canon)==len(a)==len(b)==239
    assert len(set(x["catalogue_id"] for x in b))==239
    assert after["base_v1_4_path"]=="docs/"+OLD.name
    assert after["base_v1_4_git_blob_sha1"]==blob(OLD)
    assert after["changed_original_IDs"]==before["changed_original_IDs"]+["02-012"]
    assert after["E1_new_research"]==before["E1_new_research"]+["R301"]
    changed=[]
    for c,p,n in zip(canon,a,b):
        assert c["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert c["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert c["category"]==p["catalogue_category"]==n["catalogue_category"]
        assert c["priority"]==p["original_priority"]==n["original_priority"]
        if p!=n:changed.append(c["id"])
    assert changed==["02-012"]
    target=next(x for x in b if x["catalogue_id"]=="02-012")
    assert target["proposed_primary_research_id"]=="R301"
    assert target["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert target["readme_path"]=="research/R301/README.md"
    assert target["readme_git_blob_sha1"]==blob(R/"README.md")
    assert target["formal_acceptance_filename_candidates"]==["research/R301/R301_FINAL_ACCEPTANCE_STATUS.json"]
    assert target["scientific_report_filenames"]==["research/R301/R301_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert target["source_csv_file_count"]==target["python_source_file_count"]==1
    assert target["P1_scoped_review_addendum"]["CI_run_id"]==39930227033
    assert target["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    acc,receipt,res=obj(R/"R301_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R301_MACHINE_RECEIPT.json"),obj(R/"R301_EXACT_CHANGEPOINT_RUN_LENGTH_RESULTS.json")
    assert acc["research_id"]=="R301" and acc["original_catalogue_id"]=="02-012"
    assert acc["ci_status"]=="completed" and acc["ci_conclusion"]=="success" and acc["ci_jobs_completed_success"]==3
    assert acc["actual_model_unittests_python311"]==acc["actual_model_unittests_python312"]==588
    assert acc["independent_complete_segmentation_audit_tests_per_execution"]==16
    assert acc["synthetic_worlds"]==48 and acc["complete_labeled_original_prefix_sources"]==192
    assert acc["new_real_human_E2"]==acc["new_real_animal_E2"]==acc["new_historical_E3"]==0
    assert acc["hazard_rate_fitted_to_real_sequence"] is False
    assert acc["empirical_false_positive_rate_evaluated"] is False
    assert acc["original_239_scientific_completion_established"] is False
    assert acc["source_sha256"]==receipt["source_sha256"]==hashlib.sha256((R/"R301_ALL_192_ORIGINAL_BAYESIAN_CHANGEPOINT_PREFIX_SOURCES.csv").read_bytes()).hexdigest()
    assert acc["results_sha256"]==receipt["results_sha256"]==hashlib.sha256((R/"R301_EXACT_CHANGEPOINT_RUN_LENGTH_RESULTS.json").read_bytes()).hexdigest()
    assert res["original_full_source_rows"]==192 and res["synthetic_worlds"]==48
    assert res["reference_cases"]["h_quarter_0001_last_change"]=="135/323"
    assert res["reference_cases"]["h_quarter_0000_last_change"]=="135/757"
    assert res["reference_cases"]["h_zero_0001_predict_one"]=="1/3"
    assert after["counts"]=={"primary_R":189,"shared_bounded_math":3,"older_scoped_only":4,"no_link_in_checked_sets":43,"pending_primary_R":47}
    assert after["status_counts"]==dict(collections.Counter(r["link_status"] for r in b))
    assert sum(after["status_counts"].values())==239
    qold,qnew=queue(Q48),queue(Q47)
    assert len(qold)==48 and len(qnew)==47
    assert qnew==[x for x in qold if x["original_catalogue_id"]!="02-012"]
    assert qnew[0]["original_catalogue_id"]=="02-016"
    assert sum(x["priority"]=="P1" for x in qnew)==20
    assert sum(x["priority"]=="P2" for x in qnew)==27
    assert next(x for x in b if x["catalogue_id"]=="02-008")["proposed_primary_research_id"]=="R300"
    oldR063=next(x for x in b if x["catalogue_id"]=="02-005")
    assert oldR063["proposed_primary_research_id"]=="R299"
    assert "research/R063/R063_EVIDENCE_AUDIT.md" in oldR063["older_scoped_paths_present"]
    return {"original_candidates":239,"only_changed_original":"02-012",
      "primary_R_links":189,"shared_bounded_math":3,"older_scoped_only":4,
      "pending_main_links":47,"P1_pending":20,"P2_pending":27,
      "R301_original_artificial_source_rows":192,"next_candidate":"02-016",
      "R063_R299_R300_source_prior_scopes_preserved":True,
      "new_human_animal_E2":0,"new_historical_E3":0,"overall_scientific_completion":False}

class Tests(unittest.TestCase):
    def test_full(self):self.assertEqual(verify()["only_changed_original"],"02-012")
    def test_239(self):self.assertEqual(verify()["original_candidates"],239)
    def test_primary(self):self.assertEqual(verify()["primary_R_links"],189)
    def test_pending(self):self.assertEqual(verify()["pending_main_links"],47)
    def test_P1(self):self.assertEqual(verify()["P1_pending"],20)
    def test_P2(self):self.assertEqual(verify()["P2_pending"],27)
    def test_sources(self):self.assertEqual(verify()["R301_original_artificial_source_rows"],192)
    def test_next(self):self.assertEqual(verify()["next_candidate"],"02-016")
    def test_past_sources(self):self.assertTrue(verify()["R063_R299_R300_source_prior_scopes_preserved"])
    def test_E2(self):self.assertEqual(verify()["new_human_animal_E2"],0)
    def test_E3(self):self.assertEqual(verify()["new_historical_E3"],0)
    def test_unfinished(self):self.assertFalse(verify()["overall_scientific_completion"])
    def test_prior_R300(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="02-008")["proposed_primary_research_id"],"R300")
    def test_readme_blob(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="02-012")["readme_git_blob_sha1"],blob(R/"README.md"))
    def test_not_false_calibration(self):self.assertFalse(obj(R/"R301_FINAL_ACCEPTANCE_STATUS.json")["empirical_false_positive_rate_evaluated"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R301catalogue"],verbosity=1)
    else:print(json.dumps(verify(),ensure_ascii=False,indent=2))
