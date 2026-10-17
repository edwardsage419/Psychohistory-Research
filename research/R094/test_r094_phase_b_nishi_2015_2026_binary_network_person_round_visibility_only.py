#!/usr/bin/env python3
"""Source-node rounds and source-blinded visibility, no cooperation read tests."""
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r094_phase_b_nishi_2015_2026_binary_network_person_round_visibility_only import (
 visibility_label,cohort_round,private_identity_format,anon_roster)
def fake(n=3):
 return [(f"PRIVATE_ACTOR-{p}",str(t),"1" if p%2 else "0") for p in range(n) for t in range(1,11)]
class NoBehavioralRoster(unittest.TestCase):
 def test_expected_round1(self):self.assertEqual(cohort_round("1"),1)
 def test_expected_round10(self):self.assertEqual(cohort_round("10"),10)
 def test_round0_denied(self):
  with self.assertRaises(ValueError):cohort_round("0")
 def test_round11_denied(self):
  with self.assertRaises(ValueError):cohort_round("11")
 def test_missing_round_denied(self):
  with self.assertRaises(ValueError):cohort_round("")
 def test_valid_visibility_0(self):self.assertEqual(visibility_label("0"),"0")
 def test_valid_visibility_1(self):self.assertEqual(visibility_label("1"),"1")
 def test_visibility_private_email_redacted(self):self.assertEqual(visibility_label("actor@example.com"),"REDACTED_VISIBILITY_CODE")
 def test_visibility_private_long_redacted(self):self.assertEqual(visibility_label("PRIVATE-1"*8),"REDACTED_VISIBILITY_CODE")
 def test_opaque_actor_privacy_classification(self):self.assertEqual(private_identity_format("PRIVATE_ACTOR-1"),"ASCII_MIXED_ALNUM_IDENTIFIER")
 def test_empty_original_actor_format(self):self.assertEqual(private_identity_format(""),"MISSING_SOURCE_NODE_ID")
 def test_30_synthetic_rows_3_actors(self):
  r=anon_roster(fake(),30)
  self.assertEqual(r["distinct_original_node_ID_codes"],3)
  self.assertEqual(r["number_of_node_IDs_with_exactly_10_unique_rounds_1_to_10"],3)
  self.assertEqual(r["duplicate_node_ID_round_combinations"],0)
 def test_treatment_visibility_counts(self):
  r=anon_roster(fake(),30)
  self.assertEqual(r["original_visibility_source_safe_code_counts"]["0"],20)
 def test_private_ID_not_printed(self):
  r=str(anon_roster(fake(),30))
  self.assertNotIn("PRIVATE_ACTOR",r)
 def test_no_human_decision_time_cooperation_values_examined(self):
  self.assertFalse(anon_roster(fake(),30)["any_human_decision_or_decision_time_or_neighbors_values_read"])
 def test_source_80_group_ID_not_faked(self):
  self.assertFalse(anon_roster(fake(),30)["independent_80_original_sessions_reconstructible_from_node_round_visibility_only"])
 def test_real_denominator_strict(self):
  with self.assertRaises(ValueError):anon_roster(fake())
 def test_duplicate_actor_round_tracked_not_hidden(self):
  r=anon_roster(fake()+[fake()[0]],31)
  self.assertEqual(r["duplicate_node_ID_round_combinations"],1)
 def test_source_missing_actor_count(self):
  rows=fake();rows[0]=("",rows[0][1],rows[0][2])
  r=anon_roster(rows,30)
  self.assertEqual(r["missing_node_ID_rows"],1)
 def test_changing_visibility_detected(self):
  rows=fake();rows[0]=(rows[0][0],rows[0][1],"1")
  r=anon_roster(rows,30)
  self.assertEqual(r["number_of_original_node_IDs_with_visibility_change_across_rounds"],1)
 def test_invalid_original_format_denied(self):
  with self.assertRaises(ValueError):anon_roster([("Private",1)],1)
if __name__=="__main__":unittest.main()
