#!/usr/bin/env python3
"""Original239 existing R066 HK E1/conditional E2 scope-only 04-012 reattribution audit."""
import argparse,collections,csv,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];D=ROOT/"docs";R=ROOT/"research/R066"
OLD=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.7_2026-10-23.json"
NEW=D/"ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.8_2026-10-23.json"
CAT=D/"MODEL_CANDIDATE_CATALOG_v0.1.json"
Q35=D/"ORIGINAL_239_PENDING_35_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
Q34=D/"ORIGINAL_239_PENDING_34_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv"
SCOPE=D/"ORIGINAL239_04_012_EXISTING_R066_HK_E1_E2_CONDITIONAL_SCOPE_AUDIT_2026-10-23.md"
def obj(p):return json.loads(p.read_text(encoding="utf-8"))
def sha(p):
    b=p.read_bytes()
    return hashlib.sha1(("blob "+str(len(b))).encode()+b"\0"+b).hexdigest()
def queue(p):
    with p.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f))
def audit():
    canon=obj(CAT)["models"];old,new=obj(OLD),obj(NEW)
    a,b=old["rows"],new["rows"]
    assert len(canon)==len(a)==len(b)==239
    assert len(set(x["catalogue_id"] for x in b))==239
    assert new["base_v2_7_path"]=="docs/"+OLD.name
    assert new["base_v2_7_git_blob_sha1"]==sha(OLD)
    assert new["changed_original_IDs"]==old["changed_original_IDs"]+["04-012"]
    assert new["E1_new_research"]==old["E1_new_research"]  # reattribution only
    assert new["existing_R_primary_relinked_IDs"]==old["existing_R_primary_relinked_IDs"]+["04-012"]
    assert new["existing_R_primary_relinked_targets"]=={**old["existing_R_primary_relinked_targets"],"04-012":"R066"}
    changed=[]
    for c,x,y in zip(canon,a,b):
        assert c["id"]==x["catalogue_id"]==y["catalogue_id"]
        assert c["name_en"]==x["catalogue_name_en"]==y["catalogue_name_en"]
        assert c["priority"]==x["original_priority"]==y["original_priority"]
        assert c["category"]==x["catalogue_category"]==y["catalogue_category"]
        if x!=y:changed.append(c["id"])
    assert changed==["04-012"]
    previous=next(x for x in a if x["catalogue_id"]=="04-012")
    x=next(x for x in b if x["catalogue_id"]=="04-012")
    assert previous["link_status"]=="PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY"
    assert x["link_status"]=="DIRECT_P1_BOUNDED_E2_INTERNAL_CROSS_VILLAGE_EXISTING_PRIMARY_R_REATTRIBUTION"
    assert x["proposed_primary_research_id"]=="R066"
    assert x["readme_path"]=="research/R066/README.md" and x["readme_git_blob_sha1"]==sha(R/"README.md")
    assert x["formal_acceptance_filename_candidates"]==["research/R066/R066_FINAL_ACCEPTANCE_STATUS.json"]
    assert x["older_scoped_paths_present"]==previous["older_scoped_paths_present"]
    assert x["older_2026_10_18_scoped_evidence_paths"]==previous["older_2026_10_18_scoped_evidence_paths"]
    ad=x["P1_scoped_review_addendum"]
    assert ad["new_R_model_generated"] is False and ad["new_E1_or_E2_research_executed_in_this_audit"] is False
    assert ad["R066_E1_original_CI_run"]==38845611874
    assert ad["R066_real_heldout_CI_run"]==38866210819
    assert ad["HK_uses_observed_family_network"] is False
    assert ad["original_human_causal_HK_mechanism_identified"] is False
    assert ad["extra_independent_cohort_E3"] is False
    assert ad["source_scope_report_git_blob_sha1"]==sha(SCOPE)
    assert ad["R066_original_E1_result_git_blob_sha1"]==sha(R/"R066_E1_THREE_MODEL_RESULTS.json")
    assert ad["R066_real_village_result_git_blob_sha1"]==sha(R/"R066_E2_THREE_MODEL_LOVO_RESULTS.json")
    m,real,final=obj(R/"R066_E1_THREE_MODEL_RESULTS.json"),obj(R/"R066_E2_THREE_MODEL_LOVO_RESULTS.json"),obj(R/"R066_FINAL_ACCEPTANCE_STATUS.json")
    assert m["run_conclusion"]=="success" and m["real_github_actions_run"]==38845611874 and m["synthetic_tests_passed"]==25
    assert m["input"]["HK_epsilon"]==0.25
    assert all(abs(u-v)<1e-10 for u,v in zip(m["first_step"]["HK"],[0.1,0.1,1]))
    assert final["closure"]=="CLOSED_BOUNDED"
    assert final["evidence_level"]=="E2_INTERNAL_CROSS_VILLAGE_CONDITIONAL_PREDICTION"
    assert final["source"]["dataset_doi"]=="10.7910/DVN/RAHSVM"
    assert final["source"]["villages"]==16 and final["source"]["paired_complete"]==1872
    assert final["source"]["union_edges"]==8659 and final["source"]["typed_edges"]==14767
    assert final["heldout"]["run_id"]==38866210819 and final["heldout"]["status"]=="PASS_BOUNDED"
    assert final["heldout"]["hk_uses_actual_household_network"] is False
    assert final["heldout"]["model_mechanism_causality"]=="NOT_ESTABLISHED"
    assert final["heldout"]["external_cohort"] is False
    assert real["source_data_sha256"]=="10b3e31a6d160e003ff9edf96fc1f6e1a8549ea547b8b8b08aadab1f52b40cae"
    assert real["dataset_universe"]["baseline_endline_scored"]==1872
    assert real["hk_network_semantics"]=="full village confidence peers, not observed social ties"
    assert "post-intervention" in real["forecast_origin"]
    assert real["workflow"]["conclusion"]=="success" and real["workflow"]["run_id"]==38866210819
    assert real["classes"]["hk"]["variant_selected_in_training_fold_counts"]=={"eps=0.5,steps=1":16}
    assert real["classes"]["hk"]["primary_macro_village_mse"]==final["heldout"]["hk"]==ad["HK_heldout_macro_MSE"]==0.0265478188648263
    assert real["classes"]["fj"]["primary_macro_village_mse"]==final["heldout"]["fj"]==ad["FJ_heldout_macro_MSE"]==0.0266149141842743
    assert abs(real["classes"]["fj"]["primary_macro_village_mse"]-real["classes"]["hk"]["primary_macro_village_mse"])<0.0001
    assert new["counts"]=={"primary_R":202,"shared_bounded_math":3,"older_scoped_only":1,"no_link_in_checked_sets":33,"pending_primary_R":34}
    assert new["status_counts"]==dict(collections.Counter(z["link_status"] for z in b))
    assert sum(new["status_counts"].values())==239
    before,after=queue(Q35),queue(Q34)
    assert len(before)==35 and len(after)==34
    assert after==[z for z in before if z["original_catalogue_id"]!="04-012"]
    assert after[0]["original_catalogue_id"]=="04-013"
    assert sum(z["priority"]=="P1" for z in after)==7 and sum(z["priority"]=="P2" for z in after)==27
    assert next(z for z in b if z["catalogue_id"]=="04-010")["proposed_primary_research_id"]=="R066"
    assert next(z for z in b if z["catalogue_id"]=="04-011")["proposed_primary_research_id"]=="R311"
    assert next(z for z in b if z["catalogue_id"]=="04-013")["proposed_primary_research_id"] is None
    return {"only_changed":"04-012","primary":202,"pending":34,"P1":7,"P2":27,
      "existing_R066_HK_E1":"PASS","real_16_village_internal_E2":"PASS_BOUNDED",
      "HK_uses_real_household_network":False,
      "mechanism_causality":"NOT_ESTABLISHED",
      "new_E1_or_E2":0,"historical_E3":0,"next":"04-013"}
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["only_changed"],"04-012")
    def test_primary(self):self.assertEqual(audit()["primary"],202)
    def test_pending(self):self.assertEqual(audit()["pending"],34)
    def test_P1(self):self.assertEqual(audit()["P1"],7)
    def test_P2(self):self.assertEqual(audit()["P2"],27)
    def test_existingE1(self):self.assertEqual(audit()["existing_R066_HK_E1"],"PASS")
    def test_conditionalE2(self):self.assertEqual(audit()["real_16_village_internal_E2"],"PASS_BOUNDED")
    def test_not_real_network(self):self.assertFalse(audit()["HK_uses_real_household_network"])
    def test_not_causal(self):self.assertEqual(audit()["mechanism_causality"],"NOT_ESTABLISHED")
    def test_no_new(self):self.assertEqual(audit()["new_E1_or_E2"],0)
    def test_no_E3(self):self.assertEqual(audit()["historical_E3"],0)
    def test_next(self):self.assertEqual(audit()["next"],"04-013")
    def test_readme_blob(self):self.assertEqual(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="04-012")["readme_git_blob_sha1"],sha(R/"README.md"))
    def test_no_Deffuant(self):self.assertIsNone(next(z for z in obj(NEW)["rows"] if z["catalogue_id"]=="04-013")["proposed_primary_research_id"])
if __name__=="__main__":
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true");g.add_argument("--audit",action="store_true")
    v=p.parse_args()
    if v.test:unittest.main(argv=["original HK provenance"],verbosity=1)
    else:print(json.dumps(audit(),indent=2))
