#!/usr/bin/env python3
"""R286 backfill and two shared mathematical studies: verify 239-row v0.2.

Retains original 239 catalogue untouched. Readme links and existing scientific
reports do not warrant a global 239 original-science completion claim.
"""
from __future__ import annotations
import argparse,hashlib,json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
SRC0=ROOT/"docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.1_2026-10-23.json"
SRC1=ROOT/"docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.2_2026-10-23.json"
SCAN=ROOT/"docs/ORIGINAL_239_P0_EARLY_74_ZIP_CONTENT_SCAN_RESULTS.json"
SNAP=ROOT/"docs/ORIGINAL_239_P0_EARLY_ZIP_SCAN_SHA256_RECEIPT.json"
ORIG=ROOT/"docs/MODEL_CANDIDATE_CATALOG_v0.1.json"
R111=ROOT/"research/R111/R111_PHASE_A_SYNTHETIC_MATH_CI_ACCEPTANCE_STATUS.json"
R118=ROOT/"research/R118/R118_FINAL_ACCEPTANCE_STATUS.json"
R286=ROOT/"research/R286/R286_FINAL_ACCEPTANCE_STATUS.json"
ZERO=SRC0
OLD=json.loads(SRC0.read_text(encoding="utf-8"))
NEW=json.loads(SRC1.read_text(encoding="utf-8"))
ROWS=NEW["rows"]
OLDS=OLD["rows"]
IDS={r["catalogue_id"] for r in ROWS}
def blob_sha(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data).hexdigest()
def verify_row(i):
    n,o=ROWS[i],OLDS[i]
    assert n["catalogue_id"]==o["catalogue_id"]
    assert n["catalogue_name_en"]==o["catalogue_name_en"]
    assert n["original_priority"]==o["original_priority"]
    assert n["catalogue_category"]==o["catalogue_category"]
    assert n["original_v0_1_link_status"]==o["link_status"]
    for field in ("older_2026_10_18_scoped_evidence_paths",
                  "older_scoped_paths_present","old_overlay_scope_note"):
        assert n[field]==o[field]
    for field in ("proposed_primary_research_id","evidence_basis","readme_path",
                  "readme_git_blob_sha1","readme_first_token_offset",
                  "formal_acceptance_filename_candidates","scientific_report_filenames",
                  "source_csv_file_count","python_source_file_count",
                  "scientific_evidence_grade","manual_primary_mapping_and_acceptance_review"):
        if n["catalogue_id"]!="02-002":
            if field not in ("scientific_evidence_grade","manual_primary_mapping_and_acceptance_review"):
                assert n[field]==o[field],(i,field)
            elif n["catalogue_id"] not in ("01-008","04-001"):assert n[field]==o[field]
    if n["catalogue_id"] not in ("01-008","02-002","04-001"):
        assert n["link_status"]==o["link_status"]
        assert n["shared_substantive_R_relation"] is None
        assert n["method_specific_E1_acceptance"] is None
        assert n["method_specific_scope_review"] is None
    return True
def audit():
    assert len(OLDS)==len(ROWS)==239
    assert len(IDS)==239
    assert [r["catalogue_id"] for r in ROWS]==[r["id"] for r in json.loads(ORIG.read_text())["models"]]
    for i in range(239):verify_row(i)
    byid={r["catalogue_id"]:r for r in ROWS}
    a,b,c=byid["01-008"],byid["02-002"],byid["04-001"]
    assert a["shared_substantive_R_relation"]["source_R"]=="R111"
    assert c["shared_substantive_R_relation"]["source_R"]=="R118"
    assert a["proposed_primary_research_id"] is None
    assert c["proposed_primary_research_id"] is None
    assert b["proposed_primary_research_id"]=="R286"
    assert b["scientific_evidence_grade"]=="E1_SYNTHETIC_TD0_EXACT_HELDOUT_ONLY"
    assert b["readme_path"]=="research/R286/README.md"
    assert blob_sha((ROOT/b["readme_path"]).read_bytes())==b["readme_git_blob_sha1"]
    assert NEW["source_v0_1_blob_sha"]==blob_sha(SRC0.read_bytes())
    assert NEW["source_zip_scan_blob_sha"]==blob_sha(SCAN.read_bytes())
    assert NEW["source_R286_readme_git_blob_sha"]==blob_sha((ROOT/b["readme_path"]).read_bytes())
    assert json.loads(R111.read_text())["catalogue_item"]=="01-005"
    assert json.loads(R111.read_text())["synthetic_unittest_cases_passed"]==18
    assert json.loads(R118.read_text())["original_knowledge_catalogue_item"]=="03-019"
    assert json.loads(R118.read_text())["first_party_related_prior_catalogue_id"]=="04-001"
    r286=json.loads(R286.read_text())
    assert r286["catalogue_original_id"]=="02-002"
    assert r286["ci_conclusion"]=="success" and r286["green_jobs"]==3
    assert r286["actual_python3_11_unittests"]==r286["actual_python3_12_unittests"]==93
    assert r286["new_real_human_E2"]==r286["new_historical_E3"]==0
    for v in (a,c):
        rel=v["shared_substantive_R_relation"]
        for field in ("report","acceptance"):
            assert (ROOT/rel[field]).is_file()
    scan=json.loads(SCAN.read_text())
    receipt=json.loads(SNAP.read_text())
    assert scan["original_archive_count"]==74
    assert scan["counts"]["total_archive_members"]==840
    assert scan["counts"]["scanned_text_members"]==799
    assert scan["all_original_zip_binary_sha256_gitblob_crc_member_counts_verified"]
    assert receipt["all_74_zip_bytes_crc_sha_and_member_counts_checked"]
    assert hashlib.sha256(SCAN.read_bytes()).hexdigest()==receipt["result_sha256"]
    statuses={}
    for x in ROWS:statuses[x["link_status"]]=statuses.get(x["link_status"],0)+1
    assert statuses=={
        "PROVISIONAL_PRIMARY_README_LINK":173,
        "DIRECT_NEW_P0_PRIMARY_R286_E1_BOUNDED":1,
        "SHARED_CORE_FORMULA_E1_NO_SEPARATE_PRIMARY_R":1,
        "SHARED_ORIGINAL_GRANOVETTER_1978_E1_NO_SEPARATE_PRIMARY_R":1,
        "PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY":5,
        "NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS":58}
    assert NEW["counts"]==dict(direct_primary_R=174,
       shared_substantive_R_evidence=2,older_scoped_only=5,
       not_linked_in_checked_sets=58,pending_including_old_scoped=63)
    assert len(set(r["proposed_primary_research_id"] for r in ROWS if r["proposed_primary_research_id"]))==174
    return {"original_catalogue_count":239,
      "direct_readme_primary_R_links":174,
      "shared_substantive_evidence_links_without_independent_R":2,
      "previous_only_scoped_related_research":5,
      "no_verified_link_in_two_checked_sets":58,
      "still_pending_primary_R_links":63,
      "P0_first_pass_evidence_reconciled":3,
      "R286_TD0_new_real_human_E2":0,
      "R286_TD0_new_real_historical_E3":0,
      "scientific_acceptance_of_all_239_certified":False}
def emit():
    result=audit()
    out=ROOT/"docs/ORIGINAL_239_P0_RECONCILIATION_MACHINE_RESULTS.json"
    out.write_text(json.dumps({"kind":"ORIGINAL_239_P0_SCOPE_RECONCILIATION_NOT_SCIENTIFIC_FULL_CLOSURE",
      "crosswalk_v0_2":"docs/"+SRC1.name,"summary":result},ensure_ascii=False,indent=2)+"\n")
    receipt={"kind":"239_P0_RECONCILIATION_PROVENANCE",
     "original_239_catalogue_sha256":hashlib.sha256(ORIG.read_bytes()).hexdigest(),
     "crosswalk_v0_1_sha256":hashlib.sha256(SRC0.read_bytes()).hexdigest(),
     "crosswalk_v0_2_sha256":hashlib.sha256(SRC1.read_bytes()).hexdigest(),
     "original_74_ZIP_member_scan_sha256":hashlib.sha256(SCAN.read_bytes()).hexdigest(),
     "R286_final_acceptance_sha256":hashlib.sha256(R286.read_bytes()).hexdigest(),
     "summary_sha256":hashlib.sha256(out.read_bytes()).hexdigest()}
    (ROOT/"docs/ORIGINAL_239_P0_RECONCILIATION_SHA256_RECEIPT.json").write_text(
      json.dumps(receipt,indent=2)+"\n")
    return receipt
class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(audit()["still_pending_primary_R_links"],63)
    def test_catalogue(self):self.assertEqual(len(ROWS),239)
    def test_reconciled(self):self.assertEqual(NEW["counts"]["direct_primary_R"],174)
    def test_unique(self):self.assertEqual(len(IDS),239)
    def test_r286(self):self.assertEqual(next(z for z in ROWS if z["catalogue_id"]=="02-002")["proposed_primary_research_id"],"R286")
    def test_R111_share(self):self.assertEqual(next(z for z in ROWS if z["catalogue_id"]=="01-008")["shared_substantive_R_relation"]["source_R"],"R111")
    def test_R118_share(self):self.assertEqual(next(z for z in ROWS if z["catalogue_id"]=="04-001")["shared_substantive_R_relation"]["source_R"],"R118")
    def test_no_total_science_claim(self):self.assertFalse(audit()["scientific_acceptance_of_all_239_certified"])
    def test_sources(self):self.assertEqual(json.loads(SCAN.read_text())["counts"]["scanned_text_members"],799)
    def test_R286_acceptance(self):self.assertEqual(json.loads(R286.read_text())["ci_conclusion"],"success")
for i in range(239):
    def make(j):
        def t(self):self.assertTrue(verify_row(j))
        return t
    setattr(Tests,"test_row_"+str(i+1).zfill(3),make(i))
if __name__=="__main__":
    a=argparse.ArgumentParser()
    b=a.add_mutually_exclusive_group(required=True)
    b.add_argument("--test",action="store_true")
    b.add_argument("--emit",action="store_true")
    cmd=a.parse_args()
    if cmd.test:unittest.main(argv=["p0_reconcile"],verbosity=1)
    else:print(json.dumps(emit(),ensure_ascii=False,indent=2))
