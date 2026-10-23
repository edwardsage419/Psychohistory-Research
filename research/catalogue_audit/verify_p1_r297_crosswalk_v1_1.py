#!/usr/bin/env python3
"""Independent R297 original239 v1.1 one-row provenance and bounded E1 audit."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
ORIGINAL=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.0_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.1_2026-10-23.json"
Q52=D/"ORIGINAL_239_PENDING_52_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q51=D/"ORIGINAL_239_PENDING_51_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R297"

def data(path):return json.loads(path.read_text(encoding="utf-8"))
def blob(path):
    b=path.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def queue(path):
    with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def verify():
    original=data(ORIGINAL)["models"]
    old,new=data(OLD),data(NEW)
    before,after=old["rows"],new["rows"]
    assert len(original)==len(before)==len(after)==239
    assert len({x["catalogue_id"] for x in after})==239
    assert new["base_v1_0_path"]=="docs/"+OLD.name
    assert new["base_v1_0_git_blob_sha1"]==blob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["02-003"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R297"]
    changed=[]
    for ref,previous,current in zip(original,before,after):
        assert ref["id"]==previous["catalogue_id"]==current["catalogue_id"]
        assert ref["name_en"]==previous["catalogue_name_en"]==current["catalogue_name_en"]
        assert ref["priority"]==previous["original_priority"]==current["original_priority"]
        assert ref["category"]==previous["catalogue_category"]==current["catalogue_category"]
        if previous!=current:changed.append(ref["id"])
    assert changed==["02-003"]
    row=next(z for z in after if z["catalogue_id"]=="02-003")
    assert row["proposed_primary_research_id"]=="R297"
    assert row["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert row["readme_path"]=="research/R297/README.md"
    assert row["readme_git_blob_sha1"]==blob(R/"README.md")
    assert row["formal_acceptance_filename_candidates"]==["research/R297/R297_FINAL_ACCEPTANCE_STATUS.json"]
    assert row["scientific_report_filenames"]==["research/R297/R297_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert row["source_csv_file_count"]==row["python_source_file_count"]==1
    assert row["P1_scoped_review_addendum"]["CI_run_id"]==39924889538
    assert row["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    accept,receipt,results=data(R/"R297_FINAL_ACCEPTANCE_STATUS.json"),data(R/"R297_MACHINE_RECEIPT.json"),data(R/"R297_EXACT_Q_LEARNING_OFF_POLICY_RESULTS.json")
    assert accept["original_catalogue_id"]=="02-003" and accept["research_id"]=="R297"
    assert accept["ci_status"]=="completed" and accept["ci_conclusion"]=="success" and accept["ci_jobs_completed_success"]==3
    assert accept["model_unittests_python311"]==accept["model_unittests_python312"]==611
    assert accept["human_E2_added"]==accept["animal_E2_added"]==accept["historical_E3_added"]==0
    assert accept["original_1992_asymptotic_convergence_theorem_reproduced"] is False
    assert accept["original_239_scientific_completion_established"] is False
    assert accept["source_sha256"]==receipt["sources_sha256"]==hashlib.sha256((R/"R297_ALL_120_ORIGINAL_Q_LEARNING_Q_VECTOR_SOURCES.csv").read_bytes()).hexdigest()
    assert accept["results_sha256"]==receipt["results_sha256"]==hashlib.sha256((R/"R297_EXACT_Q_LEARNING_OFF_POLICY_RESULTS.json").read_bytes()).hexdigest()
    assert results["world_count"]==24 and results["full_original_Q_vector_source_rows"]==120
    assert results["original_catalogue_id"]=="02-003"
    assert results["epoch4_oracle_correct_worlds"]==results["epoch4_oracle_disagreement_worlds"]==12
    assert results["human_E2"]==results["real_animal_E2"]==results["historical_E3"]==0
    assert new["counts"]=={"primary_R":185,"shared_bounded_math":3,"older_scoped_only":5,"no_link_in_checked_sets":46,"pending_primary_R":51}
    assert new["status_counts"]==dict(collections.Counter(x["link_status"] for x in after))
    assert sum(new["status_counts"].values())==239
    oldq,newq=queue(Q52),queue(Q51)
    assert len(oldq)==52 and len(newq)==51
    assert newq==[z for z in oldq if z["original_catalogue_id"]!="02-003"]
    assert newq[0]["original_catalogue_id"]=="02-004"
    assert sum(r["priority"]=="P1" for r in newq)==24
    assert sum(r["priority"]=="P2" for r in newq)==27
    old_rl=next(x for x in after if x["catalogue_id"]=="02-005")
    assert old_rl["link_status"]=="PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY"
    assert old_rl["proposed_primary_research_id"] is None
    assert "research/R063/R063_EVIDENCE_AUDIT.md" in old_rl["older_scoped_paths_present"]
    assert next(x for x in after if x["catalogue_id"]=="02-004")["proposed_primary_research_id"] is None
    return {"original_catalogue_items":239,"only_changed_original_id":"02-003",
      "primary_R_links":185,"shared_scoped":3,"older_scoped_only":5,
      "pending":51,"pending_P1":24,"pending_P2":27,
      "R297_complete_artificial_Q_states":120,"next_ID":"02-004",
      "R063_social_learning_prior_scope_preserved":True,
      "human_E2":0,"animal_E2":0,"historical_E3":0,"overall_scientific_completion":False}

class Tests(unittest.TestCase):
    def test_entire_audit(self):self.assertEqual(verify()["only_changed_original_id"],"02-003")
    def test_full_239(self):self.assertEqual(verify()["original_catalogue_items"],239)
    def test_primary_links(self):self.assertEqual(verify()["primary_R_links"],185)
    def test_pending(self):self.assertEqual(verify()["pending"],51)
    def test_P1(self):self.assertEqual(verify()["pending_P1"],24)
    def test_P2(self):self.assertEqual(verify()["pending_P2"],27)
    def test_q_source_count(self):self.assertEqual(verify()["R297_complete_artificial_Q_states"],120)
    def test_next(self):self.assertEqual(verify()["next_ID"],"02-004")
    def test_prior_rl(self):self.assertTrue(verify()["R063_social_learning_prior_scope_preserved"])
    def test_human_e2(self):self.assertEqual(verify()["human_E2"],0)
    def test_animal_e2(self):self.assertEqual(verify()["animal_E2"],0)
    def test_historical_e3(self):self.assertEqual(verify()["historical_E3"],0)
    def test_not_239_complete(self):self.assertFalse(verify()["overall_scientific_completion"])
    def test_readme_git_blob(self):self.assertEqual(next(x for x in data(NEW)["rows"] if x["catalogue_id"]=="02-003")["readme_git_blob_sha1"],blob(R/"README.md"))
    def test_adjacent_category_preserved(self):self.assertEqual(next(x for x in data(NEW)["rows"] if x["catalogue_id"]=="02-001")["proposed_primary_research_id"],"R296")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    arg=parser.parse_args()
    if arg.test:unittest.main(argv=["R297metadata"],verbosity=1)
    else:print(json.dumps(verify(),ensure_ascii=False,indent=2))
