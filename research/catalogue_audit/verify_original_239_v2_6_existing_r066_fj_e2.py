#!/usr/bin/env python3
"""No-person-export source-only 239 candidate audit: existing R066 FJ real internal E2 scope."""
from __future__ import annotations
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/"docs"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.5_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.6_2026-10-23.json"
QOLD=D/"ORIGINAL_239_PENDING_37_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
QNEW=D/"ORIGINAL_239_PENDING_36_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
R=ROOT/"research/R066"
REPORT=D/"ORIGINAL239_04_010_EXISTING_R066_FJ_INTERNAL_REAL_E2_SCOPE_AUDIT_2026-10-23.md"
def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def gitblob(p):
    b=p.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\0"+b).hexdigest()
def rows(p):
    with p.open(newline="",encoding="utf-8") as f:return list(csv.DictReader(f))
def audit():
    canon=obj(CAT)["models"];old,new=obj(OLD),obj(NEW)
    before,after=old["rows"],new["rows"]
    assert len(canon)==len(before)==len(after)==239
    assert len({r["catalogue_id"] for r in after})==239
    assert new["base_v2_5_path"]=="docs/"+OLD.name
    assert new["base_v2_5_git_blob_sha1"]==gitblob(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["04-010"]
    assert new["E1_new_research"]==old["E1_new_research"]  # no new R model
    assert new["existing_R_primary_relinked_IDs"]==old["existing_R_primary_relinked_IDs"]+["04-010"]
    assert new["existing_R_primary_relinked_targets"]=={**old["existing_R_primary_relinked_targets"],"04-010":"R066"}
    changed=[]
    for x,a,b in zip(canon,before,after):
        assert x["id"]==a["catalogue_id"]==b["catalogue_id"]
        assert x["name_en"]==a["catalogue_name_en"]==b["catalogue_name_en"]
        assert x["priority"]==a["original_priority"]==b["original_priority"]
        assert x["category"]==a["catalogue_category"]==b["catalogue_category"]
        if a!=b:changed.append(x["id"])
    assert changed==["04-010"]
    oldrow=next(x for x in before if x["catalogue_id"]=="04-010")
    newrow=next(x for x in after if x["catalogue_id"]=="04-010")
    assert oldrow["link_status"]=="PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY"
    assert newrow["link_status"]=="DIRECT_P1_BOUNDED_E2_INTERNAL_CROSS_VILLAGE_EXISTING_PRIMARY_R_REATTRIBUTION"
    assert newrow["proposed_primary_research_id"]=="R066"
    assert newrow["readme_path"]=="research/R066/README.md"
    assert newrow["readme_git_blob_sha1"]==gitblob(R/"README.md")
    assert newrow["older_2026_10_18_scoped_evidence_paths"]==oldrow["older_2026_10_18_scoped_evidence_paths"]
    assert newrow["older_scoped_paths_present"]==oldrow["older_scoped_paths_present"]
    assert newrow["formal_acceptance_filename_candidates"]==["research/R066/R066_FINAL_ACCEPTANCE_STATUS.json"]
    assert newrow["source_csv_file_count"]==0
    scope=newrow["P1_scoped_review_addendum"]
    assert scope["primary_existing_research"]=="R066" and scope["new_R_model_generated"] is False
    assert scope["new_E1_or_E2_research_executed_in_this_audit"] is False
    assert scope["scope_report_git_blob_sha1"]==gitblob(REPORT)
    assert scope["audit_protocol_freeze_commit"]=="05764e0c19edc0fcf2daf6e805f540ccbfcee266"
    f,e1,e2=obj(R/"R066_FINAL_ACCEPTANCE_STATUS.json"),obj(R/"R066_E1_THREE_MODEL_RESULTS.json"),obj(R/"R066_E2_THREE_MODEL_LOVO_RESULTS.json")
    assert f["research_id"]=="R066" and f["closure"]=="CLOSED_BOUNDED"
    assert f["evidence_level"]=="E2_INTERNAL_CROSS_VILLAGE_CONDITIONAL_PREDICTION"
    assert f["source"]["dataset_doi"]=="10.7910/DVN/RAHSVM"
    assert f["source"]["households"]==2125 and f["source"]["villages"]==16
    assert f["source"]["paired_complete"]==1872
    assert f["source"]["union_edges"]==8659 and f["source"]["typed_edges"]==14767
    assert f["real_r_core_edge_parity"]["run_id"]==38865507356
    assert f["real_r_core_edge_parity"]["only_python"]==f["real_r_core_edge_parity"]["only_author_r"]==0
    assert e1["real_github_actions_run"]==38845611874 and e1["synthetic_tests_passed"]==25
    assert e1["run_conclusion"]=="success"
    assert any(x["doi"]=="10.1080/0022250X.1990.9990069" for x in e1["source_papers"])
    assert e2["status"]=="SOURCE_PINNED_16_VILLAGE_HELDOUT_COMPLETE"
    assert e2["protocol_commit"]=="85b8abb398f2e4cc060b6e4b36dc6880893455a1"
    assert e2["source"]=="doi:10.7910/DVN/RAHSVM" and e2["source_version"]=="1.0"
    assert e2["source_data_sha256"]=="10b3e31a6d160e003ff9edf96fc1f6e1a8549ea547b8b8b08aadab1f52b40cae"
    assert e2["dataset_universe"]["source_rows"]==2125
    assert e2["dataset_universe"]["villages"]==16
    assert e2["dataset_universe"]["baseline_endline_scored"]==1872
    assert e2["source_r_core_edge_parity_run"]==38865507356
    assert e2["workflow"]["run_id"]==38866210819 and e2["workflow"]["conclusion"]=="success"
    assert e2["workflow"]["synthetic_tests_passed"]==17
    assert e2["primary_metric"]=="equal-village-average heldout normalized attitude MSE"
    assert e2["model_selection"]=="grid and additive drift trained on 15 other villages each fold"
    assert "post-intervention immediate" in e2["forecast_origin"]
    assert e2["hk_network_semantics"]=="full village confidence peers, not observed social ties"
    required={"persistence":0.04227103404620483,"degroot":0.028614616600241692,
              "fj":0.0266149141842743,"hk":0.0265478188648263}
    for name,score in required.items():
        x=e2["classes"][name]
        assert x["heldout_village_count"]==16 and x["heldout_household_responses"]==1872
        assert x["primary_macro_village_mse"]==score
    fj=e2["classes"]["fj"]
    assert fj["secondary_household_weighted_mse"]==0.02822275983149589
    assert fj["secondary_household_weighted_mae"]==0.12901516753537692
    assert fj["variant_selected_in_training_fold_counts"]=={"alpha=0.75,steps=2":3,"alpha=0.75,steps=4":13}
    assert e2["scientific_interpretation"]=="retrospective internal 16-village conditional prediction; cannot identify causal opinion mechanism; HK uses different information structure"
    assert e2["e3_external_independent_cohort"]=="OPEN"
    assert f["unresolved"]["new_independent_cohort"]=="OPEN" and f["unresolved"]["historical_cross_scale_prediction"]=="UNSUPPORTED"
    assert new["counts"]=={"primary_R":200,"shared_bounded_math":3,"older_scoped_only":2,"no_link_in_checked_sets":34,"pending_primary_R":36}
    assert new["status_counts"]==dict(collections.Counter(x["link_status"] for x in after))
    assert sum(new["status_counts"].values())==239
    q0,q1=rows(QOLD),rows(QNEW)
    assert len(q0)==37 and len(q1)==36
    assert q1==[z for z in q0 if z["original_catalogue_id"]!="04-010"]
    assert q1[0]["original_catalogue_id"]=="04-011"
    assert sum(x["priority"]=="P1" for x in q1)==9
    assert sum(x["priority"]=="P2" for x in q1)==27
    assert next(z for z in after if z["catalogue_id"]=="04-012")["proposed_primary_research_id"] is None
    assert next(z for z in after if z["catalogue_id"]=="04-006")["proposed_primary_research_id"]=="R309"
    assert next(z for z in after if z["catalogue_id"]=="04-008")["proposed_primary_research_id"]=="R310"
    old072=next(z for z in after if z["catalogue_id"]=="03-010")
    assert old072["P1_scoped_review_addendum"]["latest_human_mechanism_E2"]=="NOT_IDENTIFIED"
    return {"original_candidates":239,"only_changed_original":"04-010","reused_existing_primary":"R066",
      "original_R066_real_internal_E2_paired_rows":1872,"original_R066_villages":16,
      "existing_FJ_real_village_heldout_MSE":0.0266149141842743,
      "existing_E2_external_cohort":"OPEN","new_science_or_data_executed_in_this_relink":False,
      "causal_opinion_mechanism_identification":"NOT_ESTABLISHED",
      "primary_R_links":200,"pending_sources":36,"pending_P1":9,"pending_P2":27,
      "next_original_id":"04-011","next_HK_04_012_not_prematurely_completed":True}
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed_original"],"04-010")
    def test_original(self):self.assertEqual(audit()["original_candidates"],239)
    def test_reused(self):self.assertEqual(audit()["reused_existing_primary"],"R066")
    def test_human_source(self):self.assertEqual(audit()["original_R066_real_internal_E2_paired_rows"],1872)
    def test_16_villages(self):self.assertEqual(audit()["original_R066_villages"],16)
    def test_MSE(self):self.assertEqual(audit()["existing_FJ_real_village_heldout_MSE"],0.0266149141842743)
    def test_no_new(self):self.assertFalse(audit()["new_science_or_data_executed_in_this_relink"])
    def test_external_unverified(self):self.assertEqual(audit()["existing_E2_external_cohort"],"OPEN")
    def test_not_causal(self):self.assertEqual(audit()["causal_opinion_mechanism_identification"],"NOT_ESTABLISHED")
    def test_primary(self):self.assertEqual(audit()["primary_R_links"],200)
    def test_pending(self):self.assertEqual(audit()["pending_sources"],36)
    def test_P1(self):self.assertEqual(audit()["pending_P1"],9)
    def test_P2(self):self.assertEqual(audit()["pending_P2"],27)
    def test_next(self):self.assertEqual(audit()["next_original_id"],"04-011")
    def test_no_HK_shortcut(self):self.assertTrue(audit()["next_HK_04_012_not_prematurely_completed"])
    def test_readme_blob(self):self.assertEqual(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="04-010")["readme_git_blob_sha1"],gitblob(R/"README.md"))
if __name__=="__main__":
    p=argparse.ArgumentParser()
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    args=p.parse_args()
    if args.test:unittest.main(argv=["R066 FJ provenance"],verbosity=1)
    else:print(json.dumps(audit(),ensure_ascii=False,indent=2))
