#!/usr/bin/env python3
"""R300 independent original239 v1.4 HMM evidence-link and previous-R-source audit."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.3_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.4_2026-10-23.json"
Q49=D/"ORIGINAL_239_PENDING_49_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q48=D/"ORIGINAL_239_PENDING_48_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R300"

def data(path):return json.loads(path.read_text(encoding="utf-8"))
def blob(path):
    b=path.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def queue(path):
    with path.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def audit():
    catalogue=data(CAT)["models"]
    old,new=data(OLD),data(NEW)
    before,after=old["rows"],new["rows"]
    assert len(catalogue)==len(before)==len(after)==239
    assert len({r["catalogue_id"] for r in after})==239
    assert new["base_v1_3_path"]=="docs/"+OLD.name
    assert new["base_v1_3_git_blob_sha1"]==blob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["02-008"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R300"]
    changed=[]
    for c,p,n in zip(catalogue,before,after):
        assert c["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert c["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert c["priority"]==p["original_priority"]==n["original_priority"]
        assert c["category"]==p["catalogue_category"]==n["catalogue_category"]
        if p!=n:changed.append(c["id"])
    assert changed==["02-008"]
    x=next(x for x in after if x["catalogue_id"]=="02-008")
    assert x["proposed_primary_research_id"]=="R300"
    assert x["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert x["readme_path"]=="research/R300/README.md"
    assert x["readme_git_blob_sha1"]==blob(R/"README.md")
    assert x["formal_acceptance_filename_candidates"]==["research/R300/R300_FINAL_ACCEPTANCE_STATUS.json"]
    assert x["scientific_report_filenames"]==["research/R300/R300_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert x["source_csv_file_count"]==x["python_source_file_count"]==1
    assert x["P1_scoped_review_addendum"]["CI_run_id"]==39927762571
    assert x["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    a,r,results=data(R/"R300_FINAL_ACCEPTANCE_STATUS.json"),data(R/"R300_MACHINE_RECEIPT.json"),data(R/"R300_EXACT_HMM_FORWARD_RESULTS.json")
    assert a["research_id"]=="R300" and a["original_catalogue_id"]=="02-008"
    assert a["ci_status"]=="completed" and a["ci_conclusion"]=="success" and a["ci_jobs_completed_success"]==3
    assert a["actual_model_unittests_python311"]==a["actual_model_unittests_python312"]==394
    assert a["independent_hidden_path_auditor_unittests_per_execution"]==16
    assert a["complete_original_observation_prefix_sources"]==128
    assert a["new_real_human_E2"]==a["new_real_animal_E2"]==a["new_historical_E3"]==0
    assert a["Baum_Welch_parameter_estimation_performed"] is False
    assert a["Viterbi_decoding_performed"] is False
    assert a["original_239_scientific_completion_established"] is False
    assert a["original_source_sha256"]==r["source_sha256"]==hashlib.sha256((R/"R300_ALL_128_ORIGINAL_HMM_PREFIX_SOURCES.csv").read_bytes()).hexdigest()
    assert a["results_sha256"]==r["results_sha256"]==hashlib.sha256((R/"R300_EXACT_HMM_FORWARD_RESULTS.json").read_bytes()).hexdigest()
    assert results["complete_original_source_rows"]==128 and results["artificial_worlds"]==2
    assert results["original_catalogue_id"]=="02-008"
    assert results["history_effect_demo"]=={
      "persistent_1110_posterior_hidden1":"19/46",
      "persistent_0000_posterior_hidden1":"3/22",
      "persistent_1110_next_obs1":"11/23",
      "persistent_0000_next_obs1":"9/22",
      "iid_same_last_obs_posterior_hidden1":"1/4",
      "iid_next_observation1":"1/2"}
    assert new["counts"]=={"primary_R":188,"shared_bounded_math":3,"older_scoped_only":4,"no_link_in_checked_sets":44,"pending_primary_R":48}
    assert new["status_counts"]==dict(collections.Counter(z["link_status"] for z in after))
    assert sum(new["status_counts"].values())==239
    qold,qnew=queue(Q49),queue(Q48)
    assert len(qold)==49 and len(qnew)==48
    assert qnew==[r for r in qold if r["original_catalogue_id"]!="02-008"]
    assert qnew[0]["original_catalogue_id"]=="02-012"
    assert sum(r["priority"]=="P1" for r in qnew)==21
    assert sum(r["priority"]=="P2" for r in qnew)==27
    for catalogid,rid in (("02-003","R297"),("02-004","R298"),("02-005","R299")):
        assert next(z for z in after if z["catalogue_id"]==catalogid)["proposed_primary_research_id"]==rid
    prior=next(z for z in after if z["catalogue_id"]=="02-005")
    assert "research/R063/R063_EVIDENCE_AUDIT.md" in prior["older_scoped_paths_present"]
    return {"original_239_rows":239,"only_changed":"02-008",
      "primary_R_links":188,"shared_scope":3,"older_scoped_only":4,
      "pending_main_links":48,"pending_P1":21,"pending_P2":27,
      "R300_original_artificial_HMM_sources":128,"next_original_ID":"02-012",
      "R063_R297_R298_R299_prior_evidence_preserved":True,
      "human_or_animal_E2_added":0,"historical_E3_added":0,
      "overall_239_scientific_acceptance":False}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed"],"02-008")
    def test_original(self):self.assertEqual(audit()["original_239_rows"],239)
    def test_primary(self):self.assertEqual(audit()["primary_R_links"],188)
    def test_pending(self):self.assertEqual(audit()["pending_main_links"],48)
    def test_P1(self):self.assertEqual(audit()["pending_P1"],21)
    def test_P2(self):self.assertEqual(audit()["pending_P2"],27)
    def test_source(self):self.assertEqual(audit()["R300_original_artificial_HMM_sources"],128)
    def test_next(self):self.assertEqual(audit()["next_original_ID"],"02-012")
    def test_old_scope(self):self.assertTrue(audit()["R063_R297_R298_R299_prior_evidence_preserved"])
    def test_E2(self):self.assertEqual(audit()["human_or_animal_E2_added"],0)
    def test_E3(self):self.assertEqual(audit()["historical_E3_added"],0)
    def test_not_all(self):self.assertFalse(audit()["overall_239_scientific_acceptance"])
    def test_old_scoped_count(self):self.assertEqual(audit()["older_scoped_only"],4)
    def test_blob(self):self.assertEqual(next(z for z in data(NEW)["rows"] if z["catalogue_id"]=="02-008")["readme_git_blob_sha1"],blob(R/"README.md"))
    def test_unchanged_R299(self):self.assertEqual(next(z for z in data(NEW)["rows"] if z["catalogue_id"]=="02-005")["proposed_primary_research_id"],"R299")
    def test_finite_scope_only(self):self.assertFalse(data(R/"R300_FINAL_ACCEPTANCE_STATUS.json")["Rabiner_original_real_speech_recognition_reproduced"])

if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R300catalogue"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
