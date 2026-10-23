#!/usr/bin/env python3
"""Original239 v2.0 independent itemwise archival audit: existing R072 ≠ new E1/E2. No data import."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.9_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.0_2026-10-23.json"
Q43=D/"ORIGINAL_239_PENDING_43_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q42=D/"ORIGINAL_239_PENDING_42_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R072"
REPORT=D/"ORIGINAL239_03_010_EXISTING_R072_E1_AND_REV008_CODEBOOK_SCOPE_AUDIT_2026-10-23.md"

def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def blob(p):
    b=p.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\x00"+b).hexdigest()
def qrows(p):
    with p.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))

def audit():
    canon=obj(CAT)["models"];old,new=obj(OLD),obj(NEW)
    before,after=old["rows"],new["rows"]
    assert len(canon)==len(before)==len(after)==239
    assert len({x["catalogue_id"] for x in after})==239
    assert new["base_v1_9_path"]=="docs/"+OLD.name
    assert new["base_v1_9_git_blob_sha1"]==blob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["03-010"]
    assert new["E1_new_research"]==old["E1_new_research"]  # no new study
    assert new["existing_R_primary_relinked_IDs"]==["03-010"]
    assert new["existing_R_primary_relinked_targets"]=={"03-010":"R072"}
    changed=[]
    for c,p,n in zip(canon,before,after):
        assert c["id"]==p["catalogue_id"]==n["catalogue_id"]
        assert c["name_en"]==p["catalogue_name_en"]==n["catalogue_name_en"]
        assert c["priority"]==p["original_priority"]==n["original_priority"]
        assert c["category"]==p["catalogue_category"]==n["catalogue_category"]
        if p!=n:changed.append(c["id"])
    assert changed==["03-010"]
    oldrow=next(x for x in before if x["catalogue_id"]=="03-010")
    newrow=next(x for x in after if x["catalogue_id"]=="03-010")
    assert oldrow["link_status"]=="PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY"
    assert oldrow["proposed_primary_research_id"] is None
    assert newrow["link_status"]=="DIRECT_P1_BOUNDED_E1_EXISTING_PRIMARY_R_REATTRIBUTION"
    assert newrow["proposed_primary_research_id"]=="R072"
    assert newrow["readme_path"]=="research/R072/README.md"
    assert newrow["readme_git_blob_sha1"]==blob(R/"README.md")
    assert newrow["older_2026_10_18_scoped_evidence_paths"]==oldrow["older_2026_10_18_scoped_evidence_paths"]
    assert newrow["older_scoped_paths_present"]==oldrow["older_scoped_paths_present"]
    assert newrow["formal_acceptance_filename_candidates"]==["research/R072/R072_FINAL_ACCEPTANCE_STATUS.json"]
    assert newrow["source_csv_file_count"]==0  # no human raw file uploaded, only E1 JSON.
    addon=newrow["P1_scoped_review_addendum"]
    assert addon["new_R_model_generated"] is False
    assert addon["itemwise_report_blob_sha1"]==blob(REPORT)
    assert addon["primary_existing_research"]=="R072"
    assert addon["audit_frozen_commit"]=="c8427f47cdbb0fe7edbda8de7cd7faf2b4737df1"
    assert addon["latest_human_mechanism_E2"]=="NOT_IDENTIFIED"
    e1,final,rev7,rev8=(
       obj(R/"R072_E1_FULL_11664_PUBLIC_REPUTATION_RESULTS.json"),
       obj(R/"R072_FINAL_ACCEPTANCE_STATUS.json"),
       obj(R/"R072_POSTCLOSURE_S8_REV007_GROUP_RESPONSE_PARITY_STATUS.json"),
       obj(R/"R072_POSTCLOSURE_S8_REV008_AUTHOR_CODEBOOK_GATE_STATUS.json"))
    assert e1["research_id"]==final["research_id"]=="R072"
    assert e1["synthetic_only"] is True
    assert e1["status"]=="E1_PUBLIC_REPUTATION_FULL_ENUMERATION_PASS"
    assert e1["complete_model_cases"]==final["E1"]["cases"]==11664
    assert e1["actual_decision_events"]==final["E1"]["decisions"]==279936
    assert e1["strategy_vectors"]==81 and e1["initial_reputation_vectors"]==16
    assert e1["schedule_size"]==24 and len(e1["norm_channel_results"])==3
    cells=[v for norm in e1["norm_channel_results"].values() for v in norm.values()]
    assert len(cells)==9 and all(c["cases"]==1296 and c["transactions"]==31104 for c in cells)
    assert sum(c["cases"] for c in cells)==11664
    assert sum(c["transactions"] for c in cells)==279936
    assert final["final_status"]=="CLOSED_BOUNDED"
    assert final["E1"]["executed_CI_run"]==38920131192
    assert final["E1"]["source_jar_archive_CI_run"]==38920307122
    assert final["E1"]["passed_unit_tests"]==30
    original_bytes=(R/"R072_E1_FULL_11664_PUBLIC_REPUTATION_RESULTS.json").read_bytes()
    assert len(original_bytes)==final["E1"]["bytes"]==45784
    assert hashlib.sha256(original_bytes).hexdigest()==final["E1"]["SHA256"]=="6137894586488cabcc684ae350e692ccd0c6c2a731d6e0787153197de3a8868a"
    assert e1["norm_channel_results"]["IMAGE_SCORING"]["VERIFIED"]["true_help_rate_all_scheduled_24_transactions"]==0.5
    assert e1["norm_channel_results"]["IMAGE_SCORING"]["FLIP_EVERY_FOURTH"]["true_help_rate_all_scheduled_24_transactions"]==0.5
    assert e1["paired_channel_counterfactuals"]["IMAGE_SCORING|FLIP_EVERY_FOURTH"]["different_true_help_cases"]==912
    assert e1["real_human_trust_signal_E2"]=="NOT_ESTABLISHED"
    assert e1["model_evolutionary_ESS"]=="NOT_CALCULATED"
    assert final["E2_PLOS_field"]["status"]=="SOURCE_UNRESOLVED" # original historical closure
    assert rev7["genuine_r072_observed"]["strong_published_eight_paired_aggregate_multiset_equal"] is True
    assert rev7["genuine_r072_observed"]["source_candidate_requests"]==189
    assert rev7["genuine_r072_observed"]["coded_second_column_one_total"]==89
    assert rev7["genuine_r072_observed"]["published_treatment_group_mapping_verified"] is False
    assert rev7["genuine_r072_observed"]["published_serving_neutral_effect_computed"] is False
    assert rev7["original_human_source"]["raw_byte_length"]==38647
    sha="5fed03458fc72be7425b3d38386dcc7a149c3f7a69c3c14ed9dbb6e269bc4e1b"
    assert rev7["original_human_source"]["raw_original_sha256"]==sha
    assert rev8["pinned_original_SHA256"]==sha
    assert rev8["archive_conclusion"]=="success"
    assert rev8["actual_source_outcome"]["source_verified"] is True
    assert rev8["actual_source_outcome"]["source_independent_complete_numeric_profile_to_treatment_map"] is False
    assert rev8["scientific_gates"]["AUTHOR_SERVING_NEUTRAL_NUMERIC_CODEBOOK"]=="BLOCKED_NO_UNAMBIGUOUS_SOURCE_CODEBOOK"
    assert rev8["scientific_gates"]["TRUE_SERVING_HISTORY_CAUSAL_EFFECT_ESTIMATION"]=="NOT_PERFORMED"
    assert rev8["scientific_gates"]["HUMAN_IMAGE_STANDING_STERN_R072"]=="NOT_IDENTIFIED"
    assert rev8["scientific_gates"]["INDEPENDENT_E3"]=="OPEN"
    assert new["counts"]=={"primary_R":194,"shared_bounded_math":3,"older_scoped_only":3,"no_link_in_checked_sets":39,"pending_primary_R":42}
    assert new["status_counts"]==dict(collections.Counter(x["link_status"] for x in after))
    assert sum(new["status_counts"].values())==239
    qold,qnew=qrows(Q43),qrows(Q42)
    assert len(qold)==43 and len(qnew)==42
    assert qnew==[x for x in qold if x["original_catalogue_id"]!="03-010"]
    assert qnew[0]["original_catalogue_id"]=="03-012"
    assert sum(x["priority"]=="P1" for x in qnew)==15
    assert sum(x["priority"]=="P2" for x in qnew)==27
    assert next(x for x in after if x["catalogue_id"]=="03-004")["proposed_primary_research_id"]=="R305"
    assert next(x for x in after if x["catalogue_id"]=="03-003")["proposed_primary_research_id"]=="R304"
    return {"original_candidates":239,"only_changed":"03-010",
       "preexisting_R_primary":"R072","preexisting_E1_synthetic_worlds":11664,
       "preexisting_artificial_decisions":279936,"new_E1_experiments":0,
       "original_S8_anonymous_descriptive_source":"VERIFIED_PARTIAL",
       "latest_author_treatment_codebook":"BLOCKED_NO_UNAMBIGUOUS_SOURCE_CODEBOOK",
       "real_human_reputation_mechanism_E2":"NOT_IDENTIFIED",
       "new_historical_E3":0,
       "primary_R_links":194,"pending_primary":42,"pending_P1":15,"pending_P2":27,
       "next_candidate":"03-012","R304_R305_original_sources_unchanged":True}
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed"],"03-010")
    def test_original_239(self):self.assertEqual(audit()["original_candidates"],239)
    def test_R072(self):self.assertEqual(audit()["preexisting_R_primary"],"R072")
    def test_E1_old(self):self.assertEqual(audit()["preexisting_E1_synthetic_worlds"],11664)
    def test_E1_events(self):self.assertEqual(audit()["preexisting_artificial_decisions"],279936)
    def test_no_new_E1(self):self.assertEqual(audit()["new_E1_experiments"],0)
    def test_original_S8(self):self.assertEqual(audit()["original_S8_anonymous_descriptive_source"],"VERIFIED_PARTIAL")
    def test_blocker(self):self.assertEqual(audit()["latest_author_treatment_codebook"],"BLOCKED_NO_UNAMBIGUOUS_SOURCE_CODEBOOK")
    def test_no_E2(self):self.assertEqual(audit()["real_human_reputation_mechanism_E2"],"NOT_IDENTIFIED")
    def test_no_E3(self):self.assertEqual(audit()["new_historical_E3"],0)
    def test_primary(self):self.assertEqual(audit()["primary_R_links"],194)
    def test_pending(self):self.assertEqual(audit()["pending_primary"],42)
    def test_P1(self):self.assertEqual(audit()["pending_P1"],15)
    def test_P2(self):self.assertEqual(audit()["pending_P2"],27)
    def test_next(self):self.assertEqual(audit()["next_candidate"],"03-012")
    def test_R305_unchanged(self):self.assertTrue(audit()["R304_R305_original_sources_unchanged"])
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    a=p.parse_args()
    if a.test:unittest.main(argv=["03-010 R072 existing"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
