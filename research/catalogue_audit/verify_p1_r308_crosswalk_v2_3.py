#!/usr/bin/env python3
"""Independent original 239 v2.3 R308-only collective efficacy E1 provenance plus R072 R307 scope."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.2_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.3_2026-10-23.json"
Q40=D/"ORIGINAL_239_PENDING_40_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q39=D/"ORIGINAL_239_PENDING_39_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R308"

def obj(path):return json.loads(path.read_text(encoding="utf-8"))
def gitblob(path):
    b=path.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def queue(path):
    with path.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def audit():
    catalog=obj(CAT)["models"]
    old,new=obj(OLD),obj(NEW)
    before,after=old["rows"],new["rows"]
    assert len(catalog)==len(before)==len(after)==239
    assert len({x["catalogue_id"] for x in after})==239
    assert new["base_v2_2_path"]=="docs/"+OLD.name
    assert new["base_v2_2_git_blob_sha1"]==gitblob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["03-018"]
    assert new["E1_new_research"]==old["E1_new_research"]+["R308"]
    assert new["existing_R_primary_relinked_IDs"]==old["existing_R_primary_relinked_IDs"]
    changed=[]
    for c,p,n in zip(catalog,before,after):
        assert c["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert c["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert c["category"]==p["catalogue_category"]==n["catalogue_category"]
        assert c["priority"]==p["original_priority"]==n["original_priority"]
        if p!=n:changed.append(c["id"])
    assert changed==["03-018"]
    row=next(x for x in after if x["catalogue_id"]=="03-018")
    assert row["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
    assert row["proposed_primary_research_id"]=="R308"
    assert row["readme_path"]=="research/R308/README.md"
    assert row["readme_git_blob_sha1"]==gitblob(R/"README.md")
    assert row["source_csv_file_count"]==row["python_source_file_count"]==1
    assert row["formal_acceptance_filename_candidates"]==["research/R308/R308_FINAL_ACCEPTANCE_STATUS.json"]
    assert row["scientific_report_filenames"]==["research/R308/R308_SCIENTIFIC_REPORT_2026-10-23.md"]
    assert row["P1_scoped_review_addendum"]["CI_run_id"]==39954221447
    assert row["P1_scoped_review_addendum"]["no_original_human_survey_reproduction"] is True
    assert row["P1_scoped_review_addendum"]["actual_subject_or_historical_data"]==0
    a,receipt,res=obj(R/"R308_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R308_MACHINE_RECEIPT.json"),obj(R/"R308_EXACT_COLLECTIVE_EFFICACY_RESULTS.json")
    assert a["research_id"]=="R308" and a["original_catalogue_id"]=="03-018"
    assert a["ci_status"]=="completed" and a["ci_conclusion"]=="success" and a["ci_jobs_completed_success"]==3
    assert a["model_unittests_py311"]==a["model_unittests_py312"]==2607
    assert a["independent_four_binary_gate_auditor_tests_per_execution"]==18
    assert a["synthetic_worlds"]==432 and a["complete_original_source_rows"]==864
    assert a["new_aggregation_and_intervention_equations_not_original_author_models"] is True
    assert a["real_Bandura_Sampson_Goddard_original_human_responses_reanalyzed"] is False
    assert a["real_neighborhood_crime_or_school_scores_predicted"] is False
    assert a["new_real_human_E2"]==a["new_real_animal_E2"]==a["new_historical_E3"]==0
    assert a["original_239_scientific_completion_established"] is False
    assert a["source_sha256"]==receipt["source_sha256"]==hashlib.sha256((R/"R308_ALL_864_ORIGINAL_COLLECTIVE_EFFICACY_CHANNEL_SOURCES.csv").read_bytes()).hexdigest()
    assert a["results_sha256"]==receipt["results_sha256"]==hashlib.sha256((R/"R308_EXACT_COLLECTIVE_EFFICACY_RESULTS.json").read_bytes()).hexdigest()
    assert res["synthetic_worlds"]==432 and res["original_source_rows"]==864
    assert res["project_invented_probability_aggregators_and_intervention_proxy"] is True
    assert res["frozen_reference"]["one_weak_link_mean"]=="2/3"
    assert res["frozen_reference"]["same_mean_no_zero_mean"]=="2/3"
    assert res["frozen_reference"]["one_weak_link_bottleneck_proxy"]=="0"
    assert res["frozen_reference"]["same_mean_no_zero_bottleneck_proxy"]=="1/2"
    assert new["counts"]=={"primary_R":197,"shared_bounded_math":3,"older_scoped_only":3,"no_link_in_checked_sets":36,"pending_primary_R":39}
    assert new["status_counts"]==dict(collections.Counter(x["link_status"] for x in after))
    assert sum(new["status_counts"].values())==239
    qold,qnew=queue(Q40),queue(Q39)
    assert len(qold)==40 and len(qnew)==39
    assert qnew==[row for row in qold if row["original_catalogue_id"]!="03-018"]
    assert qnew[0]["original_catalogue_id"]=="04-006"
    assert sum(x["priority"]=="P1" for x in qnew)==12
    assert sum(x["priority"]=="P2" for x in qnew)==27
    assert next(x for x in after if x["catalogue_id"]=="03-016")["proposed_primary_research_id"]=="R307"
    assert next(x for x in after if x["catalogue_id"]=="03-012")["proposed_primary_research_id"]=="R306"
    prior=next(x for x in after if x["catalogue_id"]=="03-010")
    assert prior["proposed_primary_research_id"]=="R072"
    assert prior["P1_scoped_review_addendum"]["latest_human_mechanism_E2"]=="NOT_IDENTIFIED"
    return {"canonical_original_candidates":239,"only_changed_original":"03-018",
       "primary_R_links":197,"pending":39,"P1_pending":12,"P2_pending":27,
       "R308_original_artificial_channels":864,"next_candidate":"04-006",
       "R072_REV008_and_R307_preserved":True,"new_real_E2":0,"new_E3":0,
       "all_original_candidates_scientifically_finished":False}

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed_original"],"03-018")
    def test_canonical(self):self.assertEqual(audit()["canonical_original_candidates"],239)
    def test_primary(self):self.assertEqual(audit()["primary_R_links"],197)
    def test_pending(self):self.assertEqual(audit()["pending"],39)
    def test_P1(self):self.assertEqual(audit()["P1_pending"],12)
    def test_P2(self):self.assertEqual(audit()["P2_pending"],27)
    def test_rows(self):self.assertEqual(audit()["R308_original_artificial_channels"],864)
    def test_next(self):self.assertEqual(audit()["next_candidate"],"04-006")
    def test_old(self):self.assertTrue(audit()["R072_REV008_and_R307_preserved"])
    def test_E2(self):self.assertEqual(audit()["new_real_E2"],0)
    def test_E3(self):self.assertEqual(audit()["new_E3"],0)
    def test_not_all(self):self.assertFalse(audit()["all_original_candidates_scientifically_finished"])
    def test_blob(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="03-018")["readme_git_blob_sha1"],gitblob(R/"README.md"))
    def test_no_crime_prediction(self):self.assertFalse(obj(R/"R308_FINAL_ACCEPTANCE_STATUS.json")["real_neighborhood_crime_or_school_scores_predicted"])
    def test_belief_is_not_action(self):self.assertEqual(obj(R/"R308_FINAL_ACCEPTANCE_STATUS.json")["all_high_belief_without_intervention_willingness_action_proxy"],"0")
    def test_R307(self):self.assertEqual(next(x for x in obj(NEW)["rows"] if x["catalogue_id"]=="03-016")["proposed_primary_research_id"],"R307")

if __name__=="__main__":
    p=argparse.ArgumentParser();m=p.add_mutually_exclusive_group(required=True)
    m.add_argument("--test",action="store_true");m.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R308 catalogue"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
