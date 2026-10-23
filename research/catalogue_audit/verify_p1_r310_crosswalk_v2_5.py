#!/usr/bin/env python3
"""Independent original239 one-row R310 voter provenance and first-then-corrected CI acceptance."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.4_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.5_2026-10-23.json"
Q38=D/"ORIGINAL_239_PENDING_38_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q37=D/"ORIGINAL_239_PENDING_37_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R310"
def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def blob(p):
    b=p.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def queue(p):
    with p.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def audit():
    canon=obj(CAT)["models"];old,new=obj(OLD),obj(NEW)
    before,after=old["rows"],new["rows"]
    assert len(canon)==len(before)==len(after)==239
    assert len({r["catalogue_id"] for r in after})==239
    assert new["base_v2_4_path"]=="docs/"+OLD.name
    assert new["base_v2_4_git_blob_sha1"]==blob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["04-008"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R310"]
    assert new["existing_R_primary_relinked_IDs"]==old["existing_R_primary_relinked_IDs"]
    assert new["existing_R_primary_relinked_targets"]==old["existing_R_primary_relinked_targets"]
    changed=[]
    for c,p,n in zip(canon,before,after):
        assert c["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert c["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert c["priority"]==p["original_priority"]==n["original_priority"]
        assert c["category"]==p["catalogue_category"]==n["catalogue_category"]
        if p!=n:changed.append(c["id"])
    assert changed==["04-008"]
    row=next(x for x in after if x["catalogue_id"]=="04-008")
    assert row["proposed_primary_research_id"]=="R310" and row["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert row["readme_path"]=="research/R310/README.md" and row["readme_git_blob_sha1"]==blob(R/"README.md")
    assert row["formal_acceptance_filename_candidates"]==["research/R310/R310_FINAL_ACCEPTANCE_STATUS.json"]
    assert row["scientific_report_filenames"]==["research/R310/R310_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert row["source_csv_file_count"]==row["python_source_file_count"]==1
    extra=row["P1_scoped_review_addendum"]
    assert extra["CI_first_failed_run_id"]==39955723523 and extra["CI_success_run_id"]==39955796344
    assert extra["independent_audit_fix_commit"]=="17a14103c9f01f1b774883de77df831f759c7792"
    assert extra["original_real_human_or_historical_rows"]==0
    a,receipt,j=obj(R/"R310_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R310_MACHINE_RECEIPT.json"),obj(R/"R310_EXACT_NETWORK_VOTER_MODEL_RESULTS.json")
    assert a["research_id"]=="R310" and a["original_catalogue_id"]=="04-008"
    assert a["ci_status"]=="completed" and a["ci_conclusion"]=="success" and a["ci_jobs_completed_success"]==3
    assert a["first_failed_ci_run_id"]==39955723523 and a["first_failed_ci_did_not_pass_independent_source_audit"] is True
    assert a["successful_ci_run_id"]==39955796344
    assert a["model_unittests_python311"]==a["model_unittests_python312"]==1262
    assert a["independent_graph_source_auditor_tests_per_execution"]==17
    assert a["artificial_worlds"]==48 and a["complete_original_directed_event_sources"]==416
    assert a["degree_weighted_binary_density_one_step_expected_martingale_all_worlds"] is True
    assert a["irregular_path_plain_binary_density_martingale"] is False
    assert (a["path_1000_original_plain"],a["path_1000_expected_next_plain"])==("1/4","7/32")
    assert a["new_real_human_E2"]==a["new_real_animal_E2"]==a["new_historical_E3"]==0
    assert a["original239_scientific_completion_established"] is False
    assert a["source_sha256"]==receipt["source_sha256"]==hashlib.sha256((R/"R310_ALL_416_ORIGINAL_VOTER_DIRECTED_UPDATE_SOURCES.csv").read_bytes()).hexdigest()
    assert a["results_sha256"]==receipt["results_sha256"]==hashlib.sha256((R/"R310_EXACT_NETWORK_VOTER_MODEL_RESULTS.json").read_bytes()).hexdigest()
    assert j["synthetic_worlds"]==48 and j["full_original_directed_update_rows"]==416
    assert j["frozen_reference"]["PATH4_1000_expected_plain"]=="7/32"
    assert j["frozen_reference"]["all_48_degree_weighted_expectation_conserved"] is True
    assert new["counts"]=={"primary_R":199,"shared_bounded_math":3,"older_scoped_only":3,"no_link_in_checked_sets":34,"pending_primary_R":37}
    assert new["status_counts"]==dict(collections.Counter(z["link_status"] for z in after))
    assert sum(new["status_counts"].values())==239
    q0,q1=queue(Q38),queue(Q37)
    assert len(q0)==38 and len(q1)==37
    assert q1==[z for z in q0 if z["original_catalogue_id"]!="04-008"]
    assert q1[0]["original_catalogue_id"]=="04-010"
    assert sum(z["priority"]=="P1" for z in q1)==10
    assert sum(z["priority"]=="P2" for z in q1)==27
    assert next(x for x in after if x["catalogue_id"]=="04-006")["proposed_primary_research_id"]=="R309"
    assert next(x for x in after if x["catalogue_id"]=="03-016")["proposed_primary_research_id"]=="R307"
    assert next(x for x in after if x["catalogue_id"]=="03-018")["proposed_primary_research_id"]=="R308"
    r072=next(x for x in after if x["catalogue_id"]=="03-010")
    assert r072["proposed_primary_research_id"]=="R072"
    assert r072["P1_scoped_review_addendum"]["latest_human_mechanism_E2"]=="NOT_IDENTIFIED"
    return {"original_candidates":239,"only_changed_id":"04-008",
       "primary_links":199,"pending":37,"pending_P1":10,"pending_P2":27,
       "R310_full_artificial_sources":416,"next_original_id":"04-010",
       "failed_then_corrected_CI_provenance_retained":True,
       "R309_R307_R308_R072_scope_preserved":True,
       "new_real_E2":0,"new_historical_E3":0,"whole_239_scientific_completion":False}
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed_id"],"04-008")
    def test_239(self):self.assertEqual(audit()["original_candidates"],239)
    def test_primary(self):self.assertEqual(audit()["primary_links"],199)
    def test_pending(self):self.assertEqual(audit()["pending"],37)
    def test_P1(self):self.assertEqual(audit()["pending_P1"],10)
    def test_P2(self):self.assertEqual(audit()["pending_P2"],27)
    def test_sources(self):self.assertEqual(audit()["R310_full_artificial_sources"],416)
    def test_next(self):self.assertEqual(audit()["next_original_id"],"04-010")
    def test_failed_visible(self):self.assertTrue(audit()["failed_then_corrected_CI_provenance_retained"])
    def test_prior(self):self.assertTrue(audit()["R309_R307_R308_R072_scope_preserved"])
    def test_E2(self):self.assertEqual(audit()["new_real_E2"],0)
    def test_E3(self):self.assertEqual(audit()["new_historical_E3"],0)
    def test_not_complete(self):self.assertFalse(audit()["whole_239_scientific_completion"])
    def test_readme_git_blob(self):self.assertEqual(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="04-008")["readme_git_blob_sha1"],blob(R/"README.md"))
    def test_R309_preserved(self):self.assertEqual(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="04-006")["proposed_primary_research_id"],"R309")
    def test_voter_not_real_politics(self):self.assertFalse(obj(R/"R310_FINAL_ACCEPTANCE_STATUS.json")["human_political_voting_data_analyzed"])
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    x=p.parse_args()
    if x.test:unittest.main(argv=["R310 original239"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
