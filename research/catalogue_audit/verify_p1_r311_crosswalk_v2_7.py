#!/usr/bin/env python3
"""Verify 239 original candidates preserved, only R311 confidence item04-011 linked."""
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=ROOT/"docs";R=ROOT/"research/R311"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.6_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.7_2026-10-23.json"
Q36=D/"ORIGINAL_239_PENDING_36_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q35=D/"ORIGINAL_239_PENDING_35_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def blob(p):
    b=p.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\0"+b).hexdigest()
def queue(p):
    with p.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def audit():
    original=obj(CAT)["models"];old,new=obj(OLD),obj(NEW)
    a,b=old["rows"],new["rows"]
    assert len(original)==len(a)==len(b)==239
    assert new["base_v2_6_path"]=="docs/"+OLD.name
    assert new["base_v2_6_git_blob_sha1"]==blob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["04-011"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R311"]
    changed=[]
    for c,p,n in zip(original,a,b):
        assert c["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert c["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert c["category"]==p["catalogue_category"]==n["catalogue_category"]
        assert c["priority"]==p["original_priority"]==n["original_priority"]
        if p!=n:changed.append(c["id"])
    assert changed==["04-011"]
    x=next(r for r in b if r["catalogue_id"]=="04-011")
    assert x["proposed_primary_research_id"]=="R311"
    assert x["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert x["readme_path"]=="research/R311/README.md" and x["readme_git_blob_sha1"]==blob(R/"README.md")
    assert x["source_csv_file_count"]==x["python_source_file_count"]==1
    assert x["formal_acceptance_filename_candidates"]==["research/R311/R311_FINAL_ACCEPTANCE_STATUS.json"]
    assert x["scientific_report_filenames"]==["research/R311/R311_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert x["P1_scoped_review_addendum"]["CI_run_id"]==39956812166
    assert x["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    assert x["P1_scoped_review_addendum"]["separate_HK_04_012_and_Deffuant_04_013_not_accepted_by_R311"] is True
    a,rec=obj(R/"R311_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R311_MACHINE_RECEIPT.json")
    assert a["ci_status"]=="completed" and a["ci_conclusion"]=="success" and a["ci_jobs_completed_success"]==3
    assert a["main_unittests_python311"]==a["main_unittests_python312"]==5845
    assert a["independent_union_find_auditor_tests_per_execution"]==12
    assert a["artificial_worlds"]==324 and a["fully_labeled_original_dyadic_source_rows"]==1944
    assert a["reference_epsilon_half_connected_not_fully_pairwise_confident"] is True
    assert a["reference_epsilon_half_nontransitive_confidence_relation"] is True
    assert a["HK_one_step_dynamics_replicated_in_R311"] is False
    assert a["Deffuant_async_dynamics_replicated_in_R311"] is False
    assert a["new_real_human_E2"]==a["new_real_animal_E2"]==a["new_historical_E3"]==0
    assert a["original_239_scientific_completion_established"] is False
    assert a["source_sha256"]==rec["source_sha256"]==hashlib.sha256((R/"R311_ALL_1944_ORIGINAL_CONFIDENCE_DYAD_SOURCES.csv").read_bytes()).hexdigest()
    assert a["results_sha256"]==rec["result_sha256"]==hashlib.sha256((R/"R311_EXACT_BOUNDED_CONFIDENCE_GRAPH_RESULTS.json").read_bytes()).hexdigest()
    assert new["counts"]=={"primary_R":201,"shared_bounded_math":3,"older_scoped_only":2,"no_link_in_checked_sets":33,"pending_primary_R":35}
    assert new["status_counts"]==dict(collections.Counter(r["link_status"] for r in b))
    assert sum(new["status_counts"].values())==239
    oldq,newq=queue(Q36),queue(Q35)
    assert len(oldq)==36 and len(newq)==35
    assert newq==[r for r in oldq if r["original_catalogue_id"]!="04-011"]
    assert newq[0]["original_catalogue_id"]=="04-012"
    assert sum(r["priority"]=="P1" for r in newq)==8
    assert sum(r["priority"]=="P2" for r in newq)==27
    assert next(r for r in b if r["catalogue_id"]=="04-012")["proposed_primary_research_id"] is None
    assert next(r for r in b if r["catalogue_id"]=="04-013")["proposed_primary_research_id"] is None
    assert next(r for r in b if r["catalogue_id"]=="04-010")["proposed_primary_research_id"]=="R066"
    return {"original_candidates":239,"only_changed":"04-011","primary_R":201,
     "pending":35,"P1":8,"P2":27,"R311_sources":1944,"next":"04-012",
     "R066_scope_unchanged":True,"new_human_E2":0,"new_historical_E3":0}
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed"],"04-011")
    def test_total(self):self.assertEqual(audit()["original_candidates"],239)
    def test_primary(self):self.assertEqual(audit()["primary_R"],201)
    def test_pending(self):self.assertEqual(audit()["pending"],35)
    def test_P1(self):self.assertEqual(audit()["P1"],8)
    def test_P2(self):self.assertEqual(audit()["P2"],27)
    def test_source(self):self.assertEqual(audit()["R311_sources"],1944)
    def test_next(self):self.assertEqual(audit()["next"],"04-012")
    def test_R066(self):self.assertTrue(audit()["R066_scope_unchanged"])
    def test_noE2(self):self.assertEqual(audit()["new_human_E2"],0)
    def test_noE3(self):self.assertEqual(audit()["new_historical_E3"],0)
    def test_readme(self):self.assertEqual(next(r for r in obj(NEW)["rows"] if r["catalogue_id"]=="04-011")["readme_git_blob_sha1"],blob(R/"README.md"))
    def test_HK_not_promoted(self):self.assertFalse(obj(R/"R311_FINAL_ACCEPTANCE_STATUS.json")["HK_one_step_dynamics_replicated_in_R311"])
    def test_Deffuant_not_promoted(self):self.assertFalse(obj(R/"R311_FINAL_ACCEPTANCE_STATUS.json")["Deffuant_async_dynamics_replicated_in_R311"])
    def test_R066_old(self):self.assertEqual(next(r for r in obj(NEW)["rows"] if r["catalogue_id"]=="04-010")["proposed_primary_research_id"],"R066")
if __name__=="__main__":
    p=argparse.ArgumentParser();m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true");m.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R311 index"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
