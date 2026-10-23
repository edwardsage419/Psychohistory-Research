#!/usr/bin/env python3
"""Independently verify v1.2 original 239 R298 known-model planning E1-only addition."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
ORIGINAL=DOC/"MODEL_CANDIDATE_CATALOG_v0.1.json"
PREVIOUS=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.1_2026-10-23.json"
CURRENT=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.2_2026-10-23.json"
QUEUE_OLD=DOC/"ORIGINAL_239_PENDING_51_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
QUEUE_NEW=DOC/"ORIGINAL_239_PENDING_50_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R298"

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def blob(path):
    raw=path.read_bytes()
    return hashlib.sha1(("blob "+str(len(raw))).encode()+b"\x00"+raw).hexdigest()
def queue(path):
    with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def verify():
    orig=obj(ORIGINAL)["models"]
    old,new=obj(PREVIOUS),obj(CURRENT)
    a,b=old["rows"],new["rows"]
    assert len(orig)==len(a)==len(b)==239
    assert len({x["catalogue_id"] for x in b})==239
    assert new["base_v1_1_path"]=="docs/"+PREVIOUS.name
    assert new["base_v1_1_git_blob_sha1"]==blob(PREVIOUS)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["02-004"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R298"]
    changed=[]
    for original,prior,now in zip(orig,a,b):
        assert original["id"]==prior["catalogue_id"]==now["catalogue_id"]
        assert original["name_en"]==prior["catalogue_name_en"]==now["catalogue_name_en"]
        assert original["priority"]==prior["original_priority"]==now["original_priority"]
        assert original["category"]==prior["catalogue_category"]==now["catalogue_category"]
        if prior!=now:changed.append(original["id"])
    assert changed==["02-004"]
    target=next(x for x in b if x["catalogue_id"]=="02-004")
    assert target["proposed_primary_research_id"]=="R298"
    assert target["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert target["readme_path"]=="research/R298/README.md"
    assert target["readme_git_blob_sha1"]==blob(R/"README.md")
    assert target["formal_acceptance_filename_candidates"]==["research/R298/R298_FINAL_ACCEPTANCE_STATUS.json"]
    assert target["scientific_report_filenames"]==["research/R298/R298_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert target["source_csv_file_count"]==target["python_source_file_count"]==1
    assert target["P1_scoped_review_addendum"]["CI_run_id"]==39925393352
    assert target["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    acceptance=obj(R/"R298_FINAL_ACCEPTANCE_STATUS.json")
    receipt=obj(R/"R298_MACHINE_RECEIPT.json")
    data=obj(R/"R298_EXACT_MODEL_BASED_REVALUATION_RESULTS.json")
    assert acceptance["research_id"]=="R298" and acceptance["original_catalogue_id"]=="02-004"
    assert acceptance["ci_status"]=="completed" and acceptance["ci_conclusion"]=="success"
    assert acceptance["ci_jobs_completed_success"]==3
    assert acceptance["actual_model_unittests_python311"]==acceptance["actual_model_unittests_python312"]==269
    assert acceptance["new_real_human_E2"]==acceptance["new_real_animal_E2"]==acceptance["new_historical_E3"]==0
    assert acceptance["transition_model_estimation_reproduced"] is False
    assert acceptance["complete_Sutton_1990_DynaQ_architecture_reproduced"] is False
    assert acceptance["original_239_scientific_completion_established"] is False
    assert acceptance["original_source_sha256"]==receipt["source_sha256"]==hashlib.sha256((R/"R298_ALL_64_ORIGINAL_REVALUATION_ACTION_SOURCES.csv").read_bytes()).hexdigest()
    assert acceptance["results_sha256"]==receipt["results_sha256"]==hashlib.sha256((R/"R298_EXACT_MODEL_BASED_REVALUATION_RESULTS.json").read_bytes()).hexdigest()
    assert data["synthetic_worlds"]==32 and data["original_full_labeled_action_sources"]==64
    assert data["oracle_agreement_count"]==20 and data["oracle_disagreement_count"]==12
    assert data["new_real_human_E2"]==data["new_real_animal_E2"]==data["new_historical_E3"]==0
    assert new["counts"]=={"primary_R":186,"shared_bounded_math":3,"older_scoped_only":5,"no_link_in_checked_sets":45,"pending_primary_R":50}
    assert new["status_counts"]==dict(collections.Counter(x["link_status"] for x in b))
    assert sum(new["status_counts"].values())==239
    qa,qb=queue(QUEUE_OLD),queue(QUEUE_NEW)
    assert len(qa)==51 and len(qb)==50
    assert qb==[x for x in qa if x["original_catalogue_id"]!="02-004"]
    assert qb[0]["original_catalogue_id"]=="02-005"
    assert sum(x["priority"]=="P1" for x in qb)==23
    assert sum(x["priority"]=="P2" for x in qb)==27
    prior=next(x for x in b if x["catalogue_id"]=="02-005")
    assert prior["link_status"]=="PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY"
    assert prior["proposed_primary_research_id"] is None
    assert "research/R063/R063_EVIDENCE_AUDIT.md" in prior["older_scoped_paths_present"]
    assert next(x for x in b if x["catalogue_id"]=="02-003")["proposed_primary_research_id"]=="R297"
    return {"original_catalogue":239,"only_changed":"02-004","primary_R_links":186,
      "shared_bounded":3,"older_scoped_only":5,"pending_primary":50,"P1_pending":23,"P2_pending":27,
      "R298_full_action_sources":64,"next_ID":"02-005","R063_old_scoped_evidence_preserved":True,
      "new_E2":0,"new_E3":0,"all_original_models_scientifically_complete":False}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(verify()["only_changed"],"02-004")
    def test_original(self):self.assertEqual(verify()["original_catalogue"],239)
    def test_primary(self):self.assertEqual(verify()["primary_R_links"],186)
    def test_pending(self):self.assertEqual(verify()["pending_primary"],50)
    def test_P1(self):self.assertEqual(verify()["P1_pending"],23)
    def test_P2(self):self.assertEqual(verify()["P2_pending"],27)
    def test_source_count(self):self.assertEqual(verify()["R298_full_action_sources"],64)
    def test_next(self):self.assertEqual(verify()["next_ID"],"02-005")
    def test_prior_r063(self):self.assertTrue(verify()["R063_old_scoped_evidence_preserved"])
    def test_E2(self):self.assertEqual(verify()["new_E2"],0)
    def test_E3(self):self.assertEqual(verify()["new_E3"],0)
    def test_incomplete(self):self.assertFalse(verify()["all_original_models_scientifically_complete"])
    def test_readme_sha(self):self.assertEqual(next(x for x in obj(CURRENT)["rows"] if x["catalogue_id"]=="02-004")["readme_git_blob_sha1"],blob(R/"README.md"))
    def test_adjacent_Q(self):self.assertEqual(next(x for x in obj(CURRENT)["rows"] if x["catalogue_id"]=="02-003")["proposed_primary_research_id"],"R297")
    def test_no_Dyna_claim(self):self.assertFalse(obj(R/"R298_FINAL_ACCEPTANCE_STATUS.json")["complete_Sutton_1990_DynaQ_architecture_reproduced"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R298metadata"],verbosity=1)
    else:print(json.dumps(verify(),ensure_ascii=False,indent=2))
