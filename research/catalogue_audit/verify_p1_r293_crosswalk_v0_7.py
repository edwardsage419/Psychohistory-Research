#!/usr/bin/env python3
"""Original 239-row R293 v0.7 provenance audit. Never promotes synthetic E1 to E2."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
DOC=ROOT/"docs"
CAT=DOC/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.6_2026-10-23.json"
NEW=DOC/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.7_2026-10-23.json"
Q56=DOC/"ORIGINAL_239_PENDING_56_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q55=DOC/"ORIGINAL_239_PENDING_55_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R293"
R013=DOC/"R293_R013_ORIGINAL_ZIP_MEMBERS_SCHWARTZ_EVIDENCE_AUDIT_2026-10-23.json"

def data(path):return json.loads(path.read_text(encoding="utf-8"))
def blob(path):
    b=path.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+bytes([0])+b).hexdigest()
def queue(path):
    with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))

def audit():
    original=data(CAT)["models"]
    old,new=data(OLD),data(NEW)
    before,after=old["rows"],new["rows"]
    assert len(original)==len(before)==len(after)==239
    assert len(set(x["catalogue_id"] for x in after))==239
    assert new["base_v0_6_path"]=="docs/"+OLD.name and new["base_v0_6_git_blob_sha1"]==blob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["01-016"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R293"]
    changed=[]
    for o,p,n in zip(original,before,after):
        assert o["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert o["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert o["priority"]==p["original_priority"]==n["original_priority"]
        assert o["category"]==p["catalogue_category"]==n["catalogue_category"]
        if p!=n:changed.append(o["id"])
    assert changed==["01-016"]
    row=next(x for x in after if x["catalogue_id"]=="01-016")
    assert row["proposed_primary_research_id"]=="R293"
    assert row["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert row["readme_path"]=="research/R293/README.md" and row["readme_git_blob_sha1"]==blob(R/"README.md")
    assert row["source_csv_file_count"]==row["python_source_file_count"]==1
    assert row["formal_acceptance_filename_candidates"]==["research/R293/R293_FINAL_ACCEPTANCE_STATUS.json"]
    assert row["scientific_report_filenames"]==["research/R293/R293_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert row["P1_scoped_review_addendum"]["CI_run_id"]==39918965106
    assert row["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    assert row["P1_scoped_review_addendum"]["historical_R013_theory_overlap_found"] is False
    receipt,acc,res=data(R/"R293_MACHINE_RECEIPT.json"),data(R/"R293_FINAL_ACCEPTANCE_STATUS.json"),data(R/"R293_EXACT_VALUE_CENTERING_RESULTS.json")
    assert acc["ci_conclusion"]=="success" and acc["ci_jobs_completed_success"]==3
    assert acc["actual_model_tests_python311"]==acc["actual_model_tests_python312"]==153
    assert acc["synthetic_original_labeled_sources"]==2112 and acc["original_catalogue_id"]=="01-016"
    assert acc["new_real_human_E2"]==acc["new_historical_E3"]==0
    assert acc["original_239_scientific_completion_established"] is False
    assert acc["original_source_sha256"]==receipt["source_sha256"]==hashlib.sha256((R/"R293_ALL_2112_ORIGINAL_TEN_VALUE_STYLE_SOURCES.csv").read_bytes()).hexdigest()
    assert acc["result_sha256"]==receipt["result_sha256"]==hashlib.sha256((R/"R293_EXACT_VALUE_CENTERING_RESULTS.json").read_bytes()).hexdigest()
    assert res["empirical_circle_validated"] is False and res["new_human_E2"]==res["new_historical_E3"]==0
    assert len(res["worlds"])==2 and res["original_source_rows"]==2112
    assert res["worlds"][0]["illustrative_pair_0_5_raw_correlation"]=="4/5"
    assert res["worlds"][0]["illustrative_pair_0_5_centered_correlation"]=="-1/9"
    archive=data(R013)
    assert archive["archive_sha256"]=="d18eaa9a721fe9850ba93590fd9c112be70ae7282e7cc7b1341ee53f2e265d8c"
    assert archive["member_count"]==7 and archive["zip_crc"]=="PASS"
    assert all(not any(term in member.get("hits",{}) for term in ("schwartz","基本价值","基本人类价值","human values","pvq")) for member in archive["member_scan"])
    assert new["counts"]=={"primary_R":181,"shared_bounded_math":3,"older_scoped_only":5,"no_link_in_checked_sets":50,"pending_primary_R":55}
    assert new["status_counts"]==dict(collections.Counter(r["link_status"] for r in after))
    assert sum(new["status_counts"].values())==239
    earlier,pending=queue(Q56),queue(Q55)
    assert len(earlier)==56 and len(pending)==55
    assert pending==[r for r in earlier if r["original_catalogue_id"]!="01-016"]
    assert pending[0]["original_catalogue_id"]=="01-018"
    assert sum(p["priority"]=="P1" for p in pending)==28
    assert sum(p["priority"]=="P2" for p in pending)==27
    return {"original_candidates":239,"only_v0_7_change":"01-016","primary_links":181,
            "shared_scoped":3,"unresolved_primary":55,"pending_P1":28,"pending_P2":27,
            "R013_complete_zip_members_scanned":7,"R293_complete_artificial_sources":2112,
            "new_E2":0,"new_E3":0,"scientific_full_239_completion":False}

class Tests(unittest.TestCase):
    def test_full(self):self.assertEqual(audit()["only_v0_7_change"],"01-016")
    def test_count(self):self.assertEqual(audit()["original_candidates"],239)
    def test_primary(self):self.assertEqual(audit()["primary_links"],181)
    def test_pending(self):self.assertEqual(audit()["unresolved_primary"],55)
    def test_P1(self):self.assertEqual(audit()["pending_P1"],28)
    def test_P2(self):self.assertEqual(audit()["pending_P2"],27)
    def test_zip_members(self):self.assertEqual(audit()["R013_complete_zip_members_scanned"],7)
    def test_source_rows(self):self.assertEqual(audit()["R293_complete_artificial_sources"],2112)
    def test_no_E2(self):self.assertEqual(audit()["new_E2"],0)
    def test_no_E3(self):self.assertEqual(audit()["new_E3"],0)
    def test_not_complete(self):self.assertFalse(audit()["scientific_full_239_completion"])
    def test_next(self):self.assertEqual(queue(Q55)[0]["original_catalogue_id"],"01-018")
    def test_readme_blob(self):self.assertEqual(next(x for x in data(NEW)["rows"] if x["catalogue_id"]=="01-016")["readme_git_blob_sha1"],blob(R/"README.md"))
    def test_R013_only_historical(self):self.assertFalse(next(x for x in data(NEW)["rows"] if x["catalogue_id"]=="01-016")["P1_scoped_review_addendum"]["historical_R013_theory_overlap_found"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true")
    m.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R293metadata"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
