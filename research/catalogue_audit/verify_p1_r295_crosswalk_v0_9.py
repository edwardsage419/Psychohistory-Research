#!/usr/bin/env python3
"""Independent R295 v0.9 original 239 link+status audit, no E2 promotion."""
from __future__ import annotations
import argparse,csv,hashlib,json,collections,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
ORIGINAL=DOC/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.8_2026-10-23.json"
NEW=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.9_2026-10-23.json"
Q54=DOC/"ORIGINAL_239_PENDING_54_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q53=DOC/"ORIGINAL_239_PENDING_53_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R295"

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def blob(path):
    contents=path.read_bytes()
    return hashlib.sha1(("blob "+str(len(contents))).encode()+b"\x00"+contents).hexdigest()
def queue(path):
    with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def verify():
    original=obj(ORIGINAL)["models"]
    old,new=obj(OLD),obj(NEW)
    before,after=old["rows"],new["rows"]
    assert len(original)==len(before)==len(after)==239
    assert len(set(x["catalogue_id"] for x in after))==239
    assert new["base_v0_8_path"]=="docs/"+OLD.name
    assert new["base_v0_8_git_blob_sha1"]==blob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["01-019"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R295"]
    changed=[]
    for canonical,prior,now in zip(original,before,after):
        assert canonical["id"]==prior["catalogue_id"]==now["catalogue_id"]
        assert canonical["name_en"]==prior["catalogue_name_en"]==now["catalogue_name_en"]
        assert canonical["priority"]==prior["original_priority"]==now["original_priority"]
        assert canonical["category"]==prior["catalogue_category"]==now["catalogue_category"]
        if prior!=now:changed.append(canonical["id"])
    assert changed==["01-019"]
    row=next(z for z in after if z["catalogue_id"]=="01-019")
    assert row["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert row["proposed_primary_research_id"]=="R295"
    assert row["readme_path"]=="research/R295/README.md"
    assert row["readme_git_blob_sha1"]==blob(R/"README.md")
    assert row["formal_acceptance_filename_candidates"]==["research/R295/R295_FINAL_ACCEPTANCE_STATUS.json"]
    assert row["scientific_report_filenames"]==["research/R295/R295_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert row["source_csv_file_count"]==row["python_source_file_count"]==1
    assert row["P1_scoped_review_addendum"]["CI_run_id"]==39920355215
    assert row["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    acc,receipt,result=obj(R/"R295_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R295_MACHINE_RECEIPT.json"),obj(R/"R295_EXACT_HABIT_CUE_AND_DEVALUATION_RESULTS.json")
    assert acc["research_id"]=="R295" and acc["original_catalogue_id"]=="01-019"
    assert acc["ci_status"]=="completed" and acc["ci_conclusion"]=="success" and acc["ci_jobs_success"]==3
    assert acc["actual_main_unittests_python311"]==acc["actual_main_unittests_python312"]==731
    assert acc["new_real_human_E2"]==acc["new_historical_E3"]==0
    assert acc["original_239_scientific_completion_established"] is False
    assert acc["source_sha256"]==receipt["source_sha256"]==hashlib.sha256((R/"R295_ALL_180_ORIGINAL_HABIT_CUE_REVALUATION_STATES.csv").read_bytes()).hexdigest()
    assert acc["results_sha256"]==receipt["results_sha256"]==hashlib.sha256((R/"R295_EXACT_HABIT_CUE_AND_DEVALUATION_RESULTS.json").read_bytes()).hexdigest()
    assert result["fully_labeled_source_rows"]==180 and result["matched_devaluation_pairs"]==90
    assert result["original_catalogue_id"]=="01-019" and result["new_real_human_E2"]==result["new_historical_E3"]==0
    assert result["habit_share_group_sensitivity_counts"]=={
       "0":{"comparisons":30,"devaluation_sensitive":30},
       "1":{"comparisons":30,"devaluation_sensitive":0},
       "1/2":{"comparisons":30,"devaluation_sensitive":8}}
    assert new["counts"]=={"primary_R":183,"shared_bounded_math":3,"older_scoped_only":5,"no_link_in_checked_sets":48,"pending_primary_R":53}
    assert new["status_counts"]==dict(collections.Counter(z["link_status"] for z in after))
    assert sum(new["status_counts"].values())==239
    before_queue,after_queue=queue(Q54),queue(Q53)
    assert len(before_queue)==54 and len(after_queue)==53
    assert after_queue==[z for z in before_queue if z["original_catalogue_id"]!="01-019"]
    assert after_queue[0]["original_catalogue_id"]=="02-001"
    assert sum(z["priority"]=="P1" for z in after_queue)==26
    assert sum(z["priority"]=="P2" for z in after_queue)==27
    return {"original_candidates":239,"only_changed_original_id":"01-019",
        "confirmed_primary_provenance_links":183,"shared_bounded":3,"remaining":53,
        "P1_remaining":26,"P2_remaining":27,"synthetic_source_states":180,
        "synthetic_matched_pairs":90,"next_candidate":"02-001",
        "real_E2_added":0,"historical_E3_added":0,"all_239_scientifically_complete":False}

class Tests(unittest.TestCase):
    def test_full(self):self.assertEqual(verify()["only_changed_original_id"],"01-019")
    def test_239(self):self.assertEqual(verify()["original_candidates"],239)
    def test_primary(self):self.assertEqual(verify()["confirmed_primary_provenance_links"],183)
    def test_remaining(self):self.assertEqual(verify()["remaining"],53)
    def test_P1(self):self.assertEqual(verify()["P1_remaining"],26)
    def test_P2(self):self.assertEqual(verify()["P2_remaining"],27)
    def test_sources(self):self.assertEqual(verify()["synthetic_source_states"],180)
    def test_pairs(self):self.assertEqual(verify()["synthetic_matched_pairs"],90)
    def test_next(self):self.assertEqual(verify()["next_candidate"],"02-001")
    def test_E2(self):self.assertEqual(verify()["real_E2_added"],0)
    def test_E3(self):self.assertEqual(verify()["historical_E3_added"],0)
    def test_all_not_finished(self):self.assertFalse(verify()["all_239_scientifically_complete"])
    def test_readme_blob(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="01-019")["readme_git_blob_sha1"],blob(R/"README.md"))
    def test_earlier_R_unchanged(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="01-018")["proposed_primary_research_id"],"R294")

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R295metadata"],verbosity=1)
    else:print(json.dumps(verify(),indent=2,ensure_ascii=False))
