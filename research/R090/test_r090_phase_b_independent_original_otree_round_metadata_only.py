#!/usr/bin/env python3
"""R090 phase B 17 metadata-only synthetic tests, no human contributions."""
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r090_phase_b_independent_original_otree_round_metadata_only import round_field_audit
from test_r090_independent_climate_clubs_original_roster_source_gate import sample

def novel():
 rows=sample(participants=6,rounds=5)
 for r in rows:r["participant._round_number"]="1"
 return rows

class OtreeMetadata(unittest.TestCase):
 def test_round_mismatch_24_of_30(self):
  v=round_field_audit(novel(),30)
  self.assertEqual(v["nonmatching_two_round_fields_rows"],24)
 def test_participant_technical_round_all_one(self):
  v=round_field_audit(novel(),30)
  self.assertEqual(v["participant_technical_round_histogram"],{"1":30})
 def test_subsession_round_distribution(self):
  v=round_field_audit(novel(),30)
  self.assertEqual(v["subsession_experimental_round_histogram"],{"1":6,"2":6,"3":6,"4":6,"5":6})
 def test_original_sample_equal_rounds(self):
  self.assertEqual(round_field_audit(sample(),30)["nonmatching_two_round_fields_rows"],0)
 def test_technical_round_duplicates(self):
  self.assertEqual(round_field_audit(novel(),30)["persons_with_duplicate_participant_technical_rounds"],6)
 def test_subsession_round_unique(self):
  self.assertEqual(round_field_audit(novel(),30)["persons_with_duplicate_subsession_rounds"],0)
 def test_group_membership_stable(self):
  v=round_field_audit(novel(),30)
  self.assertEqual(v["subsession_group_membership_stability_histogram"]["multi_round_stable"],1)
 def test_diagnostic_no_original_action(self):
  s=str(round_field_audit(novel(),30))
  self.assertNotIn("99999",s)
  self.assertNotIn("secret",s)
 def test_no_ids_hashed_or_exported(self):
  self.assertFalse(round_field_audit(novel(),30)["actor_or_group_identifiers_exported"])
 def test_other_treatment_denied(self):
  r=novel();r[0]["treatment"]="T10"
  with self.assertRaises(ValueError):round_field_audit(r,30)
 def test_group_mixed_treatment_denied(self):
  r=novel();r[0]["treatment"]="T2"
  with self.assertRaises(ValueError):round_field_audit(r,30)
 def test_empty_person_denied(self):
  r=novel();r[0]["participant.code"]=""
  with self.assertRaises(ValueError):round_field_audit(r,30)
 def test_inconsistent_round_syntax_denied(self):
  r=novel();r[0]["subsession.round_number"]="x"
  with self.assertRaises(ValueError):round_field_audit(r,30)
 def test_expected2700_gate(self):
  with self.assertRaises(ValueError):round_field_audit(novel())
 def test_group_roster_change_detected(self):
  r=novel()
  r[0]["group.id_in_subsession"]="2"
  v=round_field_audit(r,30)
  self.assertEqual(v["subsession_group_membership_stability_histogram"]["multi_round_changed"],1)
 def test_two_or_more_subsession_rounds(self):
  self.assertTrue(round_field_audit(novel(),30)["subsession_at_least_2_distinct_round_values"])
 def test_one_subsession_round_no_dynamic_prediction(self):
  rows=[r for r in novel() if r["subsession.round_number"]=="1"]
  v=round_field_audit(rows,6)
  self.assertFalse(v["subsession_at_least_2_distinct_round_values"])
if __name__=="__main__":unittest.main()
