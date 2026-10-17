#!/usr/bin/env python3
"""R099 only synthetic genuine four-person 20-round source actor-group roster."""
import csv,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r099_phase_b_plos_2024_fixed4p_nonbehavior_group_roster_only import (
 EXPECTED_HEADER,REAL_SHA,cohort_metadata)
def raw(n_groups=24,mutate=None):
 s=io.StringIO();w=csv.writer(s);w.writerow(EXPECTED_HEADER)
 for g in range(n_groups):
  for p in range(4):
   for t in range(1,21):
    r=[str(g*4+p),"LOCAL_"+str(g*4+p),str(t),str(g),str(g%2),
       "SECRET_CONTRIBUTION_NOT_TOUCHED","SECRET_PEER_CONTRIBUTION_NOT_TOUCHED","SECRET_PSYCH_TYPE"]
    if mutate:mutate(r,g,p,t)
    w.writerow(r)
 return s.getvalue().encode()
def scan(n_groups=24):return cohort_metadata(raw(n_groups),n_groups*80)
class StrictRoster(unittest.TestCase):
 def test_fixed_source_SHA(self):self.assertEqual(REAL_SHA,"75dc8ae8b63a6b3ea728df9acab9d27944b82ec4feb5c6055e26751ca9cc4a6e")
 def test_original_eight_columns(self):self.assertEqual(len(EXPECTED_HEADER),8)
 def test_full_1920(self):self.assertEqual(scan()["original_source_1920_rows"],1920)
 def test_96_distinct_original_subjects(self):self.assertEqual(scan()["raw_metadata_field_distinct_label_counts_no_original_values"]["subject"],96)
 def test_96_subjects_all20(self):self.assertEqual(scan()["raw_subject_IDs_with_20_original_round_records"],96)
 def test_24_original_groups(self):self.assertEqual(scan()["raw_metadata_field_distinct_label_counts_no_original_values"]["group"],24)
 def test_all_twenty_source_rounds(self):self.assertTrue(scan()["source_period_all_1_through_20"])
 def test_plain_original_group_candidate_eligible(self):
  z=scan()
  self.assertTrue(any(x["is_exact_complete_24_fourperson_group_roster"] and x["original_candidate_group_key"]=="group" and x["candidate_actor_key"]=="subject" for x in z["anonymous_candidate_group_key_structures"]))
 def test_source_cohort_24_groups_exact4persons(self):
  z=scan()["anonymous_candidate_group_key_structures"][0]
  self.assertEqual(z["anonymous_sizes_of_distinct_actors_per_group_sorted"],[4]*24)
 def test_no_real_source_actions_accessed(self):self.assertFalse(scan()["source_Contribution_or_OtherContri_action_values_accessed"])
 def test_no_actor_codes_exported(self):
  q=str(scan())
  self.assertNotIn("LOCAL_",q)
  self.assertNotIn("SECRET_",q)
 def test_field_id_20(self):self.assertEqual(scan()["raw_id_IDs_with_20_original_round_records"],96)
 def test_missing_group_denied(self):
  def change(r,g,p,t):
   if g==0 and p==0 and t==1:r[3]=""
  with self.assertRaises(ValueError):cohort_metadata(raw(24,change))
 def test_blank_subject_denied(self):
  def change(r,g,p,t):
   if g==0 and p==0 and t==1:r[0]=""
  with self.assertRaises(ValueError):cohort_metadata(raw(24,change))
 def test_blank_period_denied(self):
  def change(r,g,p,t):
   if g==0 and p==0 and t==1:r[2]=""
  with self.assertRaises(ValueError):cohort_metadata(raw(24,change))
 def test_outside_round_denied(self):
  def change(r,g,p,t):
   if g==0 and p==0 and t==1:r[2]="21"
  with self.assertRaises(ValueError):cohort_metadata(raw(24,change))
 def test_wrong_expected_rows_denied(self):
  with self.assertRaises(ValueError):cohort_metadata(raw(6))
 def test_24_group_record_sensitivity(self):
  def change(r,g,p,t):
   if g==0 and p==0 and t==1:r[3]="99"
  z=cohort_metadata(raw(24,change))
  self.assertFalse(z["anonymous_candidate_group_key_structures"][0]["is_exact_complete_24_fourperson_group_roster"])
 def test_no_contribution_even_when_malicious_cell(self):
  def change(r,g,p,t):
   r[5]="<SECRET_SOURCE_CONTRIBUTION>"
  z=cohort_metadata(raw(24,change))
  self.assertNotIn("SECRET_SOURCE_CONTRIBUTION",str(z))
 def test_no_other_contribution_even_malicious_cell(self):
  def change(r,g,p,t):r[6]="9999999"
  z=cohort_metadata(raw(24,change))
  self.assertNotIn("9999999",str(z))
 def test_no_type_disposition_exported(self):self.assertNotIn("SECRET_PSYCH_TYPE",str(scan()))
 def test_field_type_labels_not_exported(self):self.assertEqual(scan()["raw_metadata_field_distinct_label_counts_no_original_values"]["Type"],1)
 def test_unequal_rounds_not_eligible(self):
  def change(r,g,p,t):
   if g==0 and p==0 and t==2:r[2]="1"
  z=cohort_metadata(raw(24,change))
  self.assertFalse(z["anonymous_candidate_group_key_structures"][0]["is_exact_complete_24_fourperson_group_roster"])
 def test_no_true_session_code_improvised(self):self.assertFalse(scan()["original_author_lab_session_field_directly_in_CSV"])
if __name__=="__main__":unittest.main()
