#!/usr/bin/env python3
"""R292 original 239-row catalogue metadata audit, no empirical completion implied."""
from __future__ import annotations
import argparse,csv,json,hashlib,collections,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
ORIG=DOC/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.5_2026-10-23.json"
NEW=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.6_2026-10-23.json"
Q57=DOC/"ORIGINAL_239_PENDING_57_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q56=DOC/"ORIGINAL_239_PENDING_56_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R292"
READM=R/"README.md"

def data(path):return json.loads(path.read_text(encoding="utf-8"))
def blob(path):
    b=path.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+bytes([0])+b).hexdigest()
def records(path):
    with path.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def audit():
    cat=data(ORIG)["models"]
    prev,now=data(OLD),data(NEW)
    a,b=prev["rows"],now["rows"]
    assert len(cat)==len(a)==len(b)==239
    assert len(set(x["catalogue_id"] for x in b))==239
    assert now["base_v0_5_path"]=="docs/"+OLD.name and now["base_v0_5_git_blob_sha1"]==blob(OLD)
    assert now["changed_original_IDs"]==prev["changed_original_IDs"]+["01-014"]
    assert now["E1_new_research"]==prev["E1_new_research"]+["R292"]
    changed=[]
    for origin,old,new in zip(cat,a,b):
        assert origin["id"]==old["catalogue_id"]==new["catalogue_id"]
        assert origin["priority"]==old["original_priority"]==new["original_priority"]
        assert origin["name_en"]==old["catalogue_name_en"]==new["catalogue_name_en"]
        assert origin["category"]==old["catalogue_category"]==new["catalogue_category"]
        if old!=new:changed.append(origin["id"])
    assert changed==["01-014"]
    r=next(x for x in b if x["catalogue_id"]=="01-014")
    assert r["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert r["proposed_primary_research_id"]=="R292"
    assert r["readme_path"]=="research/R292/README.md"
    assert r["readme_git_blob_sha1"]==blob(READM)
    assert r["source_csv_file_count"]==r["python_source_file_count"]==1
    assert r["formal_acceptance_filename_candidates"]==["research/R292/R292_FINAL_ACCEPTANCE_STATUS.json"]
    assert r["scientific_report_filenames"]==["research/R292/R292_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert r["P1_scoped_review_addendum"]["CI_run_id"]==39912808354
    assert r["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    acc=data(R/"R292_FINAL_ACCEPTANCE_STATUS.json")
    receipt=data(R/"R292_MACHINE_RECEIPT.json")
    results=data(R/"R292_EXACT_CONTROL_RESULTS.json")
    assert acc["original_catalogue_id"]=="01-014" and acc["ci_status"]=="completed"
    assert acc["ci_conclusion"]=="success" and acc["ci_jobs_completed_success"]==3
    assert acc["actual_model_unittests_python311"]==acc["actual_model_unittests_python312"]==106
    assert acc["new_real_human_E2"]==acc["new_historical_E3"]==0
    assert acc["original_239_scientific_completion_established"] is False
    assert acc["original_source_sha256"]==receipt["sources_sha256"]==hashlib.sha256((R/"R292_ALL_256_ORIGINAL_TPB_CONTROL_FEASIBILITY_SOURCES.csv").read_bytes()).hexdigest()
    assert acc["source_results_sha256"]==receipt["results_sha256"]==hashlib.sha256((R/"R292_EXACT_CONTROL_RESULTS.json").read_bytes()).hexdigest()
    assert results["original_positive_source_cells"]==256 and results["original_catalogue_id"]=="01-014"
    assert now["counts"]=={"primary_R":180,"shared_bounded_math":3,"older_scoped_only":5,"no_link_in_checked_sets":51,"pending_primary_R":56}
    assert now["status_counts"]==dict(collections.Counter(x["link_status"] for x in b))
    assert sum(now["status_counts"].values())==239
    earlier,current=records(Q57),records(Q56)
    assert len(earlier)==57 and len(current)==56
    assert current==[x for x in earlier if x["original_catalogue_id"]!="01-014"]
    nextid=next(x for x in b if x["catalogue_id"]=="01-016")
    assert nextid["proposed_primary_research_id"] is None
    assert nextid["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
    return {"catalogue_rows":239,"exact_changed":["01-014"],"primary":180,"shared":3,
      "remaining_primary_link_gaps":56,"P1_remaining":29,"P2_remaining":27,
      "full_source_cells":256,"original_239_scientific_completion":False,
      "E2_new":0,"E3_new":0,"ci_run_id":39912808354}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["exact_changed"],["01-014"])
    def test_original_239(self):self.assertEqual(audit()["catalogue_rows"],239)
    def test_180_primary(self):self.assertEqual(audit()["primary"],180)
    def test_56_gaps(self):self.assertEqual(audit()["remaining_primary_link_gaps"],56)
    def test_source_256(self):self.assertEqual(audit()["full_source_cells"],256)
    def test_P1_29(self):self.assertEqual(len([x for x in records(Q56) if x["priority"]=="P1"]),29)
    def test_P2_27(self):self.assertEqual(len([x for x in records(Q56) if x["priority"]=="P2"]),27)
    def test_next_id(self):self.assertEqual(records(Q56)[0]["original_catalogue_id"],"01-016")
    def test_ci(self):self.assertEqual(audit()["ci_run_id"],39912808354)
    def test_no_E2(self):self.assertEqual(audit()["E2_new"],0)
    def test_no_E3(self):self.assertEqual(audit()["E3_new"],0)
    def test_scientific_completion(self):self.assertFalse(audit()["original_239_scientific_completion"])
    def test_readme_blob(self):self.assertEqual(next(x for x in data(NEW)["rows"] if x["catalogue_id"]=="01-014")["readme_git_blob_sha1"],blob(READM))
    def test_separate_tra(self):self.assertEqual(next(x for x in data(NEW)["rows"] if x["catalogue_id"]=="01-013")["proposed_primary_research_id"],"R291")

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    x=parser.parse_args()
    if x.test:unittest.main(argv=["R292metadata"],verbosity=1)
    else:print(json.dumps(audit(),indent=2,ensure_ascii=False))
