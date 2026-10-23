#!/usr/bin/env python3
"""Source-level *metadata* verifier for all 239 catalogue-to-R evidence links.

No model validity or original-paper replication is inferred from filenames,
README mentions, source hashes, or the existence of any prior report.
"""
import argparse
import csv
import hashlib
import json
import re
import unittest
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
CROSS="docs/ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.1_2026-10-23.json"
CAT="docs/MODEL_CANDIDATE_CATALOG_v0.1.json"
EARLY="manifests/RECOVERY_STATUS_R001_R064.csv"
PATTERN=re.compile(r"\b(?:0[1-9]|1[012])-\d{3}\b")
CROSS_OBJ=json.loads((ROOT/CROSS).read_text(encoding="utf-8"))
CAT_OBJ=json.loads((ROOT/CAT).read_text(encoding="utf-8"))
ROWS=CROSS_OBJ["rows"]
CAT_ROWS=CAT_OBJ["models"]
ORIGINAL={x["id"]:x for x in CAT_ROWS}
STATUSES=("PROVISIONAL_PRIMARY_README_LINK",
          "PREVIOUS_SCOPED_EVIDENCE_LINK_ONLY",
          "NO_ITEMWISE_RESEARCH_LINK_FOUND_IN_THIS_PASS")

def git_blob_sha(data):
    return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\x00"+data).hexdigest()

def eligible_research_ids():
    return {"R"+str(x).zfill(3) for x in range(111,286)}-{"R208","R209"}

def validate_row(r,i):
    assert r["catalogue_id"]==CAT_ROWS[i]["id"]
    old=ORIGINAL[r["catalogue_id"]]
    assert r["catalogue_name_en"]==old["name_en"]
    assert r["catalogue_category"]==old["category"]
    assert r["original_priority"]==old["priority"]
    assert r["scientific_evidence_grade"]=="UNDETERMINED_BY_FILENAME_AND_README_TOKEN_SCAN"
    assert r["manual_primary_mapping_and_acceptance_review"]=="PENDING"
    status=r["link_status"]
    assert status in STATUSES
    source=r["proposed_primary_research_id"]
    if source is not None:
        assert status==STATUSES[0]
        assert source in eligible_research_ids()
        assert r["readme_path"]==f"research/{source}/README.md"
        raw=(ROOT/r["readme_path"]).read_bytes()
        assert git_blob_sha(raw)==r["readme_git_blob_sha1"],r["readme_path"]
        text=raw.decode("utf-8")
        matches=list(PATTERN.finditer(text))
        assert matches
        assert r["readme_first_token_offset"]==matches[0].start()
        if source=="R173":
            assert r["catalogue_id"]=="07-015"
            assert matches[0].group()=="07-016"
            report=(ROOT/"research/R173/R173_SCIENTIFIC_REPORT_2026-10-21.md").read_text(encoding="utf-8")
            assert "07-015" in report
            assert r["evidence_basis"]=="EXPLICIT_R173_SCIENTIFIC_REPORT_OVERRIDE"
        else:
            assert r["catalogue_id"]==matches[0].group()
            assert r["evidence_basis"]=="FIRST_ORIGINAL_CATALOGUE_ID_MENTION_IN_README"
        for p in r["formal_acceptance_filename_candidates"]:
            assert p.startswith("research/"+source+"/")
            assert (ROOT/p).is_file()
        for p in r["scientific_report_filenames"]:
            assert p.startswith("research/"+source+"/")
            assert (ROOT/p).is_file()
    else:
        assert r["readme_path"] is None
        assert r["readme_git_blob_sha1"] is None
        assert r["evidence_basis"] is None
        assert r["formal_acceptance_filename_candidates"]==[]
        assert r["scientific_report_filenames"]==[]
        assert r["source_csv_file_count"]==r["python_source_file_count"]==0
        if r["older_2026_10_18_scoped_evidence_paths"]:
            assert status==STATUSES[1]
        else:
            assert status==STATUSES[2]
    for p in r["older_scoped_paths_present"]:
        assert p in r["older_2026_10_18_scoped_evidence_paths"]
        assert (ROOT/p).exists()
    return True

def early_zip_archive():
    with (ROOT/EARLY).open(encoding="utf-8",newline="") as f:
        data=list(csv.DictReader(f))
    assert len(data)==64
    assert {r["round"] for r in data}=={"R"+str(i).zfill(3) for i in range(1,65)}
    assert all(r["zip_integrity"]=="PASS" for r in data)
    assert all(int(r["library_zip_count"])>=1 for r in data)
    return len(data),sum(int(r["library_zip_count"]) for r in data)

def verify_all():
    assert len(CAT_ROWS)==len(ROWS)==239
    assert [r["catalogue_id"] for r in ROWS]==[r["id"] for r in CAT_ROWS]
    assert len({r["catalogue_id"] for r in ROWS})==239
    for i,row in enumerate(ROWS):validate_row(row,i)
    linked=[r for r in ROWS if r["proposed_primary_research_id"]]
    assert len(linked)==173
    assert len({r["proposed_primary_research_id"] for r in linked})==173
    assert {r["proposed_primary_research_id"] for r in linked}==eligible_research_ids()
    assert not any(r["proposed_primary_research_id"] in ("R208","R209") for r in ROWS)
    assert "08-032" not in ORIGINAL and "08-033" not in ORIGINAL
    oldonly=sum(r["link_status"]==STATUSES[1] for r in ROWS)
    unlinked=sum(r["link_status"]==STATUSES[2] for r in ROWS)
    assert (len(linked),oldonly,unlinked)==(173,7,59)
    assert CROSS_OBJ["summary"]==dict(direct=173,old_only=7,neither=59)
    categories=defaultdict(list)
    for r in ROWS:categories[r["catalogue_category"]].append(r)
    assert len(categories)==12
    for cat in CROSS_OBJ["category_counts"]:
        candidates=categories[cat["category"]]
        assert cat["total"]==len(candidates)
        assert cat["direct"]==sum(x["link_status"]==STATUSES[0] for x in candidates)
        assert cat["old_scoped_only"]==sum(x["link_status"]==STATUSES[1] for x in candidates)
        assert cat["not_linked"]==sum(x["link_status"]==STATUSES[2] for x in candidates)
    return dict(catalogue_count=239,primary_readme_links=173,
      older_scoped_links_without_primary=7,no_itemwise_link_in_this_scan=59,
      ambiguous_R173_primary_reconciled_to="07-015",
      R208_R209_supplementary_not_catalogue_entries=True,
      original_R001_R064_archive_rounds=early_zip_archive()[0],
      original_R001_R064_archive_zip_entries=early_zip_archive()[1],
      itemwise_scientific_E1_E2_E3_grade_validated=False,
      original_full_paper_reproduction_certified=False,
      full_239_scientific_completion_certified=False)

def emit():
    output=verify_all()
    path=ROOT/"docs/ORIGINAL_239_CROSSWALK_MACHINE_AUDIT_RESULTS.json"
    result=dict(research_kind="RETROSPECTIVE_REPOSITORY_METADATA_AUDIT_NOT_PRESCORE",
                source_crosswalk=CROSS,source_catalogue=CAT,source_early_archive=EARLY,
                provenance=output)
    path.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    receipt=dict(kind="239_CROSSWALK_METADATA_AUDIT",
                 catalogue_sha256=hashlib.sha256((ROOT/CAT).read_bytes()).hexdigest(),
                 crosswalk_sha256=hashlib.sha256((ROOT/CROSS).read_bytes()).hexdigest(),
                 early_archive_manifest_sha256=hashlib.sha256((ROOT/EARLY).read_bytes()).hexdigest(),
                 results_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    (ROOT/"docs/ORIGINAL_239_CROSSWALK_MACHINE_AUDIT_RECEIPT.json").write_text(
      json.dumps(receipt,indent=2)+"\n",encoding="utf-8")
    return receipt

class Tests(unittest.TestCase):
    def test_all(self):self.assertEqual(verify_all()["primary_readme_links"],173)
    def test_categories(self):self.assertEqual(len(CROSS_OBJ["category_counts"]),12)
    def test_catalogue_complete(self):self.assertEqual(len(CAT_ROWS),239)
    def test_source_order(self):self.assertEqual([r["id"] for r in CAT_ROWS],[r["catalogue_id"] for r in ROWS])
    def test_early_archive(self):self.assertEqual(early_zip_archive()[0],64)
    def test_supplements(self):self.assertTrue(all(r["proposed_primary_research_id"] not in ("R208","R209") for r in ROWS))
    def test_R173_correct(self):self.assertEqual(next(r for r in ROWS if r["proposed_primary_research_id"]=="R173")["catalogue_id"],"07-015")
    def test_unresolved(self):self.assertEqual(sum(r["link_status"]==STATUSES[2] for r in ROWS),59)
    def test_scoped_only(self):self.assertEqual(sum(r["link_status"]==STATUSES[1] for r in ROWS),7)
    def test_no_auto_scientific_upgrade(self):self.assertTrue(all(r["scientific_evidence_grade"]=="UNDETERMINED_BY_FILENAME_AND_README_TOKEN_SCAN" for r in ROWS))
    def test_first_P0_gap(self):
        p=[r for r in ROWS if r["original_priority"]=="P0" and not r["proposed_primary_research_id"]]
        self.assertEqual({r["catalogue_id"] for r in p},{"01-008","02-002","04-001"})

for i in range(239):
    def test_row(j):
        def single(self):self.assertTrue(validate_row(ROWS[j],j))
        return single
    setattr(Tests,"test_original_catalogue_row_"+str(i+1).zfill(3),test_row(i))

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    g=parser.add_mutually_exclusive_group(required=True)
    g.add_argument("--test",action="store_true")
    g.add_argument("--emit",action="store_true")
    cmd=parser.parse_args()
    if cmd.test:unittest.main(argv=["catalogue_audit"],verbosity=1)
    else:print(json.dumps(emit(),indent=2))
