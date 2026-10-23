#!/usr/bin/env python3
"""Original239 v2.9 Deffuant R312 one-row-only model audit with original source SHA."""
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=ROOT/"docs";R=ROOT/"research/R312"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.8_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.9_2026-10-23.json"
Q34=D/"ORIGINAL_239_PENDING_34_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q33=D/"ORIGINAL_239_PENDING_33_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def blob(p):
    b=p.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\0"+b).hexdigest()
def queue(p):
    with p.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def audit():
    canon=obj(CAT)["models"];old,new=obj(OLD),obj(NEW)
    a,b=old["rows"],new["rows"]
    assert len(canon)==len(a)==len(b)==239
    assert len({z["catalogue_id"] for z in b})==239
    assert new["base_v2_8_path"]=="docs/"+OLD.name
    assert new["base_v2_8_git_blob_sha1"]==blob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["04-013"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R312"]
    assert new["existing_R_primary_relinked_IDs"]==old["existing_R_primary_relinked_IDs"]
    assert new["existing_R_primary_relinked_targets"]==old["existing_R_primary_relinked_targets"]
    changed=[]
    for c,p,n in zip(canon,a,b):
        assert c["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert c["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert c["category"]==p["catalogue_category"]==n["catalogue_category"]
        assert c["priority"]==p["original_priority"]==n["original_priority"]
        if p!=n:changed.append(c["id"])
    assert changed==["04-013"]
    x=next(z for z in b if z["catalogue_id"]=="04-013")
    assert x["proposed_primary_research_id"]=="R312"
    assert x["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert x["readme_path"]=="research/R312/README.md" and x["readme_git_blob_sha1"]==blob(R/"README.md")
    assert x["source_csv_file_count"]==x["python_source_file_count"]==1
    assert x["formal_acceptance_filename_candidates"]==["research/R312/R312_FINAL_ACCEPTANCE_STATUS.json"]
    assert x["scientific_report_filenames"]==["research/R312/R312_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert x["P1_scoped_review_addendum"]["CI_run_id"]==39957585074
    assert x["P1_scoped_review_addendum"]["original_human_subjects"]==0
    assert x["P1_scoped_review_addendum"]["prior_HK_R066_conditional_E2_not_reused_as_Deffuant_human_E2"] is True
    ac,receipt=obj(R/"R312_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R312_MACHINE_RECEIPT.json")
    assert ac["research_id"]=="R312" and ac["original_catalogue_id"]=="04-013"
    assert ac["ci_status"]=="completed" and ac["ci_conclusion"]=="success" and ac["ci_jobs_completed_success"]==3
    assert ac["model_unittests_python311"]==ac["model_unittests_python312"]==3469
    assert ac["independent_midpoint_pair_auditor_tests_per_execution"]==15
    assert ac["artificial_worlds"]==48 and ac["exact_pair_events"]==288 and ac["full_original_artificial_person_sources"]==1152
    assert ac["every_selected_dyad_event_conserves_group_mean"] is True
    assert ac["finite_two_step_contact_order_dependence"] is True
    assert ac["full_original_Deffuant_long_run_reproduced"] is False
    assert ac["new_real_human_E2"]==ac["new_real_animal_E2"]==ac["new_historical_E3"]==0
    assert ac["original_239_scientific_completion_established"] is False
    assert ac["source_sha256"]==receipt["source_sha256"]==hashlib.sha256((R/"R312_ALL_1152_ORIGINAL_DEFFUANT_PERSON_SOURCE_ROWS.csv").read_bytes()).hexdigest()
    assert ac["results_sha256"]==receipt["result_sha256"]==hashlib.sha256((R/"R312_EXACT_DEFFUANT_PAIR_EVENT_RESULTS.json").read_bytes()).hexdigest()
    assert new["counts"]=={"primary_R":203,"shared_bounded_math":3,"older_scoped_only":1,"no_link_in_checked_sets":32,"pending_primary_R":33}
    assert new["status_counts"]==dict(collections.Counter(z["link_status"] for z in b))
    assert sum(new["status_counts"].values())==239
    qa,qb=queue(Q34),queue(Q33)
    assert len(qa)==34 and len(qb)==33
    assert qb==[z for z in qa if z["original_catalogue_id"]!="04-013"]
    assert qb[0]["original_catalogue_id"]=="04-014"
    assert sum(z["priority"]=="P1" for z in qb)==6 and sum(z["priority"]=="P2" for z in qb)==27
    assert next(z for z in b if z["catalogue_id"]=="04-011")["proposed_primary_research_id"]=="R311"
    y=next(z for z in b if z["catalogue_id"]=="04-012")
    assert y["proposed_primary_research_id"]=="R066"
    assert y["P1_scoped_review_addendum"]["original_human_causal_HK_mechanism_identified"] is False
    assert next(z for z in b if z["catalogue_id"]=="04-010")["proposed_primary_research_id"]=="R066"
    return {"originals":239,"only_changed":"04-013","primary_R":203,"pending":33,
      "pending_P1":6,"pending_P2":27,"new_R312_original_sources":1152,
      "old_R066_HK_human_evidence_not_promoted":True,"new_real_E2":0,
      "new_historical_E3":0,"next":"04-014"}
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed"],"04-013")
    def test_originals(self):self.assertEqual(audit()["originals"],239)
    def test_primary(self):self.assertEqual(audit()["primary_R"],203)
    def test_pending(self):self.assertEqual(audit()["pending"],33)
    def test_p1(self):self.assertEqual(audit()["pending_P1"],6)
    def test_p2(self):self.assertEqual(audit()["pending_P2"],27)
    def test_sources(self):self.assertEqual(audit()["new_R312_original_sources"],1152)
    def test_next(self):self.assertEqual(audit()["next"],"04-014")
    def test_HK(self):self.assertTrue(audit()["old_R066_HK_human_evidence_not_promoted"])
    def test_noE2(self):self.assertEqual(audit()["new_real_E2"],0)
    def test_noE3(self):self.assertEqual(audit()["new_historical_E3"],0)
    def test_blob(self):self.assertEqual(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="04-013")["readme_git_blob_sha1"],blob(R/"README.md"))
    def test_HK_old(self):self.assertEqual(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="04-012")["proposed_primary_research_id"],"R066")
    def test_deffuant_not_empirical(self):self.assertFalse(obj(R/"R312_FINAL_ACCEPTANCE_STATUS.json")["full_original_Deffuant_long_run_reproduced"])
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["R312 index"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
