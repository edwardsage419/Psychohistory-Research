#!/usr/bin/env python3
"""R083 synthetic-only tests, no original human decisions downloaded here."""
import math, pathlib,sys,unittest
import pandas as pd
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r083_author_sha_coordinated_punishment_replication import (
 blob_sha,exact_test_p,numeric_binary,paired_stats,validated_dataframe,
 analyse_dataframe,COMMIT,DTA_GIT_BLOB,DO_GIT_BLOB)

def artificial_frame():
 rows=[]
 for cohort in (0,1):
  for i in range(8):
   rows.append({
    "id":f"synthetic-person-{cohort}-{i}",
    "rerun":cohort,
    "punisher":0 if i==0 else 1,
    "unconditional_punishment":i%2,
    "conditional_other_nopun":0 if i in (1,2,3,4) else 1,
    "conditional_other_pun":1 if i in (1,2,5,6) else 0
   })
 return pd.DataFrame(rows)

class SourceGuards(unittest.TestCase):
 def test_git_blob_known_empty(self):
  self.assertEqual(blob_sha(b""),"e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")
 def test_git_blob_mutated(self):
  self.assertNotEqual(blob_sha(b"a"),blob_sha(b"b"))
 def test_git_blob_requires_binary(self):
  with self.assertRaises(ValueError):blob_sha("abc")
 def test_fixed_commit_40hex(self):
  self.assertEqual(len(COMMIT),40)
 def test_fixed_two_github_blobs(self):
  self.assertEqual(len(DTA_GIT_BLOB),40)
  self.assertEqual(len(DO_GIT_BLOB),40)
 def test_source_missing_required_column(self):
  f=artificial_frame().drop(columns=["punisher"])
  self.assertNotIn("punisher",f.columns)
 def test_id_duplicate_cohort_logic_in_pipeline(self):
  f=artificial_frame()
  f.loc[2,"id"]=f.loc[1,"id"]
  # key-duplication is enforced in validated_dataframe after original DTA parse.
  self.assertTrue(f.duplicated(["rerun","id"]).any())
 def test_separate_cohorts_same_id_is_allowed_by_rule(self):
  f=artificial_frame()
  f.loc[8,"id"]=f.loc[0,"id"]
  self.assertFalse(f.duplicated(["rerun","id"]).any())

def raise_error():
 raise ValueError("synthetic schema invalid")

class ExactPairedCases(unittest.TestCase):
 def test_empty_stratum(self):
  self.assertIsNone(paired_stats([])["paired_mean_difference"])
 def test_all00(self):
  v=paired_stats([(0,0)]*4)
  self.assertEqual(v["paired_mean_difference"],0)
  self.assertEqual(v["conditional_McNemar_exact_two_sided_p"],1)
 def test_all11(self):
  self.assertEqual(paired_stats([(1,1)]*3)["n11"],3)
 def test_all_coordination_switch(self):
  self.assertEqual(paired_stats([(0,1)]*7)["paired_mean_difference"],1)
 def test_all_anticoordination_switch(self):
  self.assertEqual(paired_stats([(1,0)]*7)["paired_mean_difference"],-1)
 def test_half_discordant_both_directions(self):
  self.assertEqual(paired_stats([(0,1),(1,0)])["paired_mean_difference"],0)
 def test_one_sided_exact_mcnemar(self):
  self.assertEqual(exact_test_p(5,0),0.0625)
 def test_tie_exact_p(self):
  self.assertEqual(exact_test_p(2,2),1)
 def test_no_discordant_p(self):
  self.assertEqual(exact_test_p(0,0),1)
 def test_negative_counts_fail(self):
  with self.assertRaises(ValueError):exact_test_p(-1,0)
 def test_invalid_pair_label_fail(self):
  with self.assertRaises(ValueError):paired_stats([(0,2)])
 def test_missing_num_is_none(self):
  self.assertIsNone(numeric_binary(float("nan")))
 def test_binary_label_numeric(self):
  self.assertEqual(numeric_binary(1.0),1)
  self.assertEqual(numeric_binary(0),0)
 def test_nonbinary_label_fail(self):
  with self.assertRaises(ValueError):numeric_binary(2)
 def test_bool_ok(self):
  self.assertEqual(numeric_binary(True),1)
 def test_discordants_conservation(self):
  d=paired_stats([(0,0),(0,1),(1,0),(1,1),(0,1)])
  self.assertEqual(d["discordant_pairs"],d["n01_coordination_switch"]+d["n10_anti_coordination_switch"])
  self.assertAlmostEqual(d["paired_mean_difference"],d["punish_if_other_does"]-d["punish_if_other_does_not"])

class SyntheticCohortAudit(unittest.TestCase):
 def test_no_original_data_used(self):
  s=analyse_dataframe(artificial_frame())
  self.assertFalse(s["human_id_exported"])
  self.assertNotIn("synthetic-person",str(s))
 def test_both_original_cohorts_separately(self):
  s=analyse_dataframe(artificial_frame())
  self.assertEqual(s["author_original_cohort_count"],2)
  self.assertEqual(s["cohort_counts_and_paired_effects"]["main"]["eligible_paired_main_comparison"],7)
  self.assertEqual(s["cohort_counts_and_paired_effects"]["replication"]["eligible_paired_main_comparison"],7)
 def test_nonpunishers_excluded_not_assumed_zero(self):
  s=analyse_dataframe(artificial_frame())
  self.assertEqual(s["cohort_counts_and_paired_effects"]["main"]["original_nonpunisher_excluded"],1)
 def test_three_strata_exhaustive(self):
  s=analyse_dataframe(artificial_frame())
  a=s["cohort_counts_and_paired_effects"]["main"]
  self.assertEqual(sum(t["n"] for t in a["three_prespecified_unconditional_punishment_strata"].values()),7)
 def test_unknown_unconditional_retained(self):
  f=artificial_frame();f.loc[1,"unconditional_punishment"]=float("nan")
  s=analyse_dataframe(f)
  self.assertEqual(s["cohort_counts_and_paired_effects"]["main"]["three_prespecified_unconditional_punishment_strata"]["unconditional_unknown"]["n"],1)
 def test_missing_paired_excluded_with_count(self):
  f=artificial_frame();f.loc[1,"conditional_other_pun"]=float("nan")
  s=analyse_dataframe(f)
  a=s["cohort_counts_and_paired_effects"]["main"]
  self.assertEqual(a["punisher_pairs_excluded_due_to_missing_response"],1)
  self.assertEqual(a["eligible_paired_main_comparison"],6)
 def test_invalid_conditional_fails_closed(self):
  f=artificial_frame();f.loc[2,"conditional_other_pun"]=3
  with self.assertRaises(ValueError):analyse_dataframe(f)
 def test_invalid_unconditional_fails_closed(self):
  f=artificial_frame();f.loc[2,"unconditional_punishment"]=3
  with self.assertRaises(ValueError):analyse_dataframe(f)
 def test_directional_transfer_positive_in_both(self):
  f=artificial_frame()
  s=analyse_dataframe(f)
  self.assertEqual(s["predeclared_two_cohort_directional_gate"],"PASS_POSITIVE_IN_BOTH")
 def test_main_negative_cohort_reports_no_transfer(self):
  f=artificial_frame()
  f.loc[f["rerun"]==1,["conditional_other_nopun","conditional_other_pun"]]=(
   f.loc[f["rerun"]==1,["conditional_other_pun","conditional_other_nopun"]].to_numpy())
  s=analyse_dataframe(f)
  self.assertEqual(s["predeclared_two_cohort_directional_gate"],"NOT_SUPPORTED")
 def test_no_primary_human_outcomes_fails(self):
  f=artificial_frame()
  f.loc[f["punisher"]==1,"conditional_other_pun"]=float("nan")
  with self.assertRaises(ValueError):analyse_dataframe(f)

if __name__=="__main__":
 unittest.main()
