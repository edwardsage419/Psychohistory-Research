#!/usr/bin/env python3
"""Check provenance of four bounded P1 catalogue updates in 239-row v0.3."""
import argparse,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FILES={
 "catalog":ROOT/"docs/MODEL_CANDIDATE_CATALOG_v0.1.json",
 "old":ROOT/"docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.2_2026-10-23.json",
 "new":ROOT/"docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.3_2026-10-23.json"}
CAT=json.loads(FILES["catalog"].read_text())["models"]
OLD=json.loads(FILES["old"].read_text())["rows"]
NEW=json.loads(FILES["new"].read_text())["rows"]
CHANGED={"01-001":"R287","01-002":"R288","01-004":"R289","01-006":None}
def blob(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest()
def row_verification(i):
    n,o,m=NEW[i],OLD[i],CAT[i]
    assert n["catalogue_id"]==o["catalogue_id"]==m["id"]
    assert n["catalogue_name_en"]==o["catalogue_name_en"]==m["name_en"]
    assert n["catalogue_category"]==o["catalogue_category"]==m["category"]
    assert n["original_priority"]==o["original_priority"]==m["priority"]
    assert n["prior_v0_2_status"]==o["link_status"]
    assert n["older_2026_10_18_scoped_evidence_paths"]==o["older_2026_10_18_scoped_evidence_paths"]
    if n["catalogue_id"] not in CHANGED:
        for key in o:assert n[key]==o[key],(n["catalogue_id"],key)
        assert n["P1_scoped_review_addendum"] is None
    else:
        assert o["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"
    return True
def run():
    assert len(CAT)==len(OLD)==len(NEW)==239
    assert len({m["id"] for m in CAT})==239
    assert blob(FILES["old"].read_bytes())==json.loads(FILES["new"].read_text())["base_v0_2_readme_blob_sha1"]
    for i in range(239):row_verification(i)
    new={x["catalogue_id"]:x for x in NEW}
    for cat,rname in CHANGED.items():
        a=new[cat]
        if rname:
            assert a["proposed_primary_research_id"]==rname
            assert a["link_status"]=="DIRECT_P1_BOUNDED_E1_NEW_PRIMARY_R"
            assert a["P1_scoped_review_addendum"]["CI_run_id"] in (39910069650,39910074038,39910079877)
            assert blob((ROOT/a["readme_path"]).read_bytes())==a["readme_git_blob_sha1"]
            accepted=json.loads((ROOT/f"research/{rname}/{rname}_FINAL_ACCEPTANCE_STATUS.json").read_text())
            assert accepted["original_catalogue_id"]==cat
            assert accepted["ci_conclusion"]=="success" and accepted["ci_jobs_completed_success"]==3
            assert accepted["new_real_human_E2"]==accepted["new_historical_E3"]==0
            assert accepted["independent_source_csv_formula_and_hash_audit"]
            assert len(a["formal_acceptance_filename_candidates"])==1
            assert len(a["scientific_report_filenames"])==1
            assert (ROOT/a["formal_acceptance_filename_candidates"][0]).is_file()
            assert (ROOT/a["scientific_report_filenames"][0]).is_file()
        else:
            assert cat=="01-006"
            assert a["proposed_primary_research_id"] is None
            assert a["shared_substantive_R_relation"]["source_R"]=="R111"
            assert a["shared_substantive_R_relation"]["source_primary_catalogue"]=="01-005"
            assert a["link_status"]=="SHARED_R111_MULTINOMIAL_LOGIT_FORMULA_NOT_SEPARATE_EMPIRICAL_ESTIMATION"
            assert blob((ROOT/a["shared_substantive_R_relation"]["executor"]).read_bytes())==a["P1_scoped_review_addendum"]["read_code_git_blob_sha1"]
            accepted_path=ROOT/a["shared_substantive_R_relation"]["acceptance"]
            assert blob(accepted_path.read_bytes())==a["P1_scoped_review_addendum"]["acceptance_json_git_blob_sha1"]
            assert json.loads(accepted_path.read_text())["synthetic_unittest_cases_passed"]==18
            assert json.loads(accepted_path.read_text())["catalogue_item"]=="01-005"
    assert sum(x["proposed_primary_research_id"] is not None for x in NEW)==177
    assert len({x["proposed_primary_research_id"] for x in NEW if x["proposed_primary_research_id"]})==177
    assert sum(x["shared_substantive_R_relation"] is not None for x in NEW)==3
    assert sum(x["link_status"]=="PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY" for x in NEW)==5
    assert sum(x["link_status"]=="NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS" for x in NEW)==54
    assert all(x["original_priority"]!="P0" for x in NEW if x["link_status"] in ("PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY","NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS"))
    return dict(catalogue=239,direct_primary_R=177,shared_substantive_without_double_counting=3,
      old_scoped_only=5,no_link_in_checked_sources=54,pending_primary=59,
      exact_original_239_completion_certified=False,new_human_E2=0,new_historical_E3=0)
def emit():
    results=run()
    out=ROOT/"docs/ORIGINAL_239_P1_R287_R289_CROSSWALK_MACHINE_RESULTS.json"
    out.write_text(json.dumps({"scope":"REPOSITORY_CROSSWALK_METADATA_NOT_ALL_239_SCIENTIFIC_VALIDATION",
       "results":results},indent=2)+"\n")
    receipt={k+"_sha256":hashlib.sha256(p.read_bytes()).hexdigest() for k,p in FILES.items()}
    receipt["results_sha256"]=hashlib.sha256(out.read_bytes()).hexdigest()
    for r in ("R287","R288","R289"):
        receipt[r+"_scientific_acceptance_sha256"]=hashlib.sha256((ROOT/f"research/{r}/{r}_FINAL_ACCEPTANCE_STATUS.json").read_bytes()).hexdigest()
    (ROOT/"docs/ORIGINAL_239_P1_R287_R289_CROSSWALK_SHA256_RECEIPT.json").write_text(
      json.dumps(receipt,indent=2)+"\n")
    return receipt
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(run()["pending_primary"],59)
    def test_cat(self):self.assertEqual(len(CAT),239)
    def test_old(self):self.assertEqual(len(OLD),239)
    def test_new(self):self.assertEqual(len(NEW),239)
    def test_three(self):self.assertEqual(len(CHANGED),4)
    def test_E2(self):self.assertEqual(run()["new_human_E2"],0)
    def test_E3(self):self.assertEqual(run()["new_historical_E3"],0)
    def test_model_01_006_share(self):self.assertEqual(next(z for z in NEW if z["catalogue_id"]=="01-006")["shared_substantive_R_relation"]["source_R"],"R111")
    def test_R287(self):self.assertEqual(next(z for z in NEW if z["catalogue_id"]=="01-001")["proposed_primary_research_id"],"R287")
    def test_R288(self):self.assertEqual(next(z for z in NEW if z["catalogue_id"]=="01-002")["proposed_primary_research_id"],"R288")
    def test_R289(self):self.assertEqual(next(z for z in NEW if z["catalogue_id"]=="01-004")["proposed_primary_research_id"],"R289")
for i in range(239):
    def test_at(j):
        def case(self):self.assertTrue(row_verification(j))
        return case
    setattr(Tests,"test_row_"+str(i+1).zfill(3),test_at(i))
if __name__=="__main__":
    parser=argparse.ArgumentParser()
    group=parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test",action="store_true");group.add_argument("--emit",action="store_true")
    cmd=parser.parse_args()
    if cmd.test:unittest.main(argv=["p1_crosswalk"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
