#!/usr/bin/env python3
"""Independent 239-candidate 02-001 R296 one-row provenance audit, no E2 assumptions."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
ORIGINAL=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.9_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.0_2026-10-23.json"
Q53=D/"ORIGINAL_239_PENDING_53_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q52=D/"ORIGINAL_239_PENDING_52_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R296"

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def blob(path):
    b=path.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def queue(path):
    with path.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def verify():
    original=obj(ORIGINAL)["models"]
    previous,new=obj(OLD),obj(NEW)
    oldrows,newrows=previous["rows"],new["rows"]
    assert len(original)==len(oldrows)==len(newrows)==239
    assert len({r["catalogue_id"] for r in newrows})==239
    assert new["base_v0_9_path"]=="docs/"+OLD.name
    assert new["base_v0_9_git_blob_sha1"]==blob(OLD)
    assert new["changed_original_IDs"]==previous["changed_original_IDs"]+["02-001"]
    assert new["E1_new_research"]==previous["E1_new_research"]+["R296"]
    changes=[]
    for canonical,p,n in zip(original,oldrows,newrows):
        assert canonical["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert canonical["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert canonical["priority"]==p["original_priority"]==n["original_priority"]
        assert canonical["category"]==p["catalogue_category"]==n["catalogue_category"]
        if p!=n:changes.append(canonical["id"])
    assert changes==["02-001"]
    row=next(z for z in newrows if z["catalogue_id"]=="02-001")
    assert row["proposed_primary_research_id"]=="R296"
    assert row["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert row["readme_path"]=="research/R296/README.md"
    assert row["readme_git_blob_sha1"]==blob(R/"README.md")
    assert row["formal_acceptance_filename_candidates"]==["research/R296/R296_FINAL_ACCEPTANCE_STATUS.json"]
    assert row["scientific_report_filenames"]==["research/R296/R296_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert row["source_csv_file_count"]==row["python_source_file_count"]==1
    assert row["P1_scoped_review_addendum"]["CI_run_id"]==39920891647
    assert row["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    acc,rec,results=obj(R/"R296_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R296_MACHINE_RECEIPT.json"),obj(R/"R296_EXACT_BLOCKING_UNBLOCKING_RESULTS.json")
    assert acc["original_catalogue_id"]=="02-001" and acc["research_id"]=="R296"
    assert acc["ci_status"]=="completed" and acc["ci_conclusion"]=="success" and acc["ci_jobs_completed_success"]==3
    assert acc["actual_model_unittests_python311"]==acc["actual_model_unittests_python312"]==211
    assert acc["new_real_human_E2"]==acc["new_real_animal_E2"]==acc["new_historical_E3"]==0
    assert acc["original_239_scientific_completion_established"] is False
    assert acc["independent_source_sha256"]==rec["source_sha256"]==hashlib.sha256((R/"R296_ALL_40_ORIGINAL_RW_CUE_BLOCKING_STATES.csv").read_bytes()).hexdigest()
    assert acc["result_sha256"]==rec["results_sha256"]==hashlib.sha256((R/"R296_EXACT_BLOCKING_UNBLOCKING_RESULTS.json").read_bytes()).hexdigest()
    assert results["complete_artificial_source_rows"]==40 and results["world_count"]==8 and results["original_catalogue_id"]=="02-001"
    assert results["blocking_under_A_pretraining_for_both_alphas"] is True
    assert results["unblocking_under_reward_upshift_for_both_alphas"] is True
    assert new["counts"]=={"primary_R":184,"shared_bounded_math":3,"older_scoped_only":5,"no_link_in_checked_sets":47,"pending_primary_R":52}
    assert new["status_counts"]==dict(collections.Counter(r["link_status"] for r in newrows))
    assert sum(new["status_counts"].values())==239
    qold,qnew=queue(Q53),queue(Q52)
    assert len(qold)==53 and len(qnew)==52
    assert qnew==[x for x in qold if x["original_catalogue_id"]!="02-001"]
    assert qnew[0]["original_catalogue_id"]=="02-003"
    assert sum(z["priority"]=="P1" for z in qnew)==25
    assert sum(z["priority"]=="P2" for z in qnew)==27
    return {"original_catalogue_count":239,"only_updated_ID":"02-001","primary_links":184,
            "shared_bounded":3,"remaining_primary_gaps":52,"P1_remaining":25,"P2_remaining":27,
            "R296_full_source_rows":40,"next_original_ID":"02-003",
            "R296_E2":0,"R296_E3":0,"full_original239_scientific_acceptance":False}

class Tests(unittest.TestCase):
    def test_full(self):self.assertEqual(verify()["only_updated_ID"],"02-001")
    def test_original_count(self):self.assertEqual(verify()["original_catalogue_count"],239)
    def test_primary(self):self.assertEqual(verify()["primary_links"],184)
    def test_remaining(self):self.assertEqual(verify()["remaining_primary_gaps"],52)
    def test_P1(self):self.assertEqual(verify()["P1_remaining"],25)
    def test_P2(self):self.assertEqual(verify()["P2_remaining"],27)
    def test_source_count(self):self.assertEqual(verify()["R296_full_source_rows"],40)
    def test_next(self):self.assertEqual(verify()["next_original_ID"],"02-003")
    def test_E2(self):self.assertEqual(verify()["R296_E2"],0)
    def test_E3(self):self.assertEqual(verify()["R296_E3"],0)
    def test_science_incomplete(self):self.assertFalse(verify()["full_original239_scientific_acceptance"])
    def test_blob(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="02-001")["readme_git_blob_sha1"],blob(R/"README.md"))
    def test_preserve_R295(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="01-019")["proposed_primary_research_id"],"R295")
    def test_real_observations(self):self.assertFalse(obj(R/"R296_FINAL_ACCEPTANCE_STATUS.json")["source_author_animal_experimental_reproduction"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true")
    group.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R296 metadata"],verbosity=1)
    else:print(json.dumps(verify(),indent=2))
