#!/usr/bin/env python3
"""R091 source-only six-col actor-group-time roster synthetic regression."""
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r091_phase_b_main_sheet_group_time_roster_only import (
 qualify_rows,country_tag,condition_tag,time_round,CONDITIONS)
def synthetic(groups=2):
 out=[]
 for g in range(groups):
  country="Sweden" if g%2==0 else "Philippines"
  for t in range(1,21):
   for player in range(4):
    out.append((f"PRIVATE_ACTOR_{g}_{player}",f"PRIVATE_GROUP_{g}",
        f"PRIVATE_CONTRIBUTION_NEVER_TOUCH_99999",t,country,"Control"))
 return out

class SourceOnlyRosterTests(unittest.TestCase):
 def test_valid_country_sweden(self):self.assertEqual(country_tag("Sweden"),"Sweden")
 def test_valid_country_philippines(self):self.assertEqual(country_tag("Philippines"),"Philippines")
 def test_valid_country_shortcode(self):self.assertEqual(country_tag("PH"),"Philippines")
 def test_unknown_country_not_guessed(self):self.assertIsNone(country_tag("other"))
 def test_known_paper_treatments(self):self.assertEqual(CONDITIONS,("Control","10P","40P","Impact","Level"))
 def test_treatment_case_insensitive(self):self.assertEqual(condition_tag("control"),"Control")
 def test_treatment_unmapped(self):self.assertIsNone(condition_tag("70P"))
 def test_real_round_1(self):self.assertEqual(time_round(1),1)
 def test_real_round_20(self):self.assertEqual(time_round(20),20)
 def test_real_round_zero_denied(self):
  with self.assertRaises(ValueError):time_round(0)
 def test_real_round_21_denied(self):
  with self.assertRaises(ValueError):time_round(21)
 def test_main_two_groups_actor4_round20(self):
  v=qualify_rows(synthetic(),160,2)
  self.assertEqual(v["verified_4_member_20_round_source_group_count"],2)
  self.assertEqual(v["verified_complete_original_source_group_rounds"],40)
  self.assertEqual(v["roster_person_identifier_evidence_counts"]["first_column_stable_within_original_group"],2)
 def test_raw_private_actor_and_contribution_never_leak(self):
  v=str(qualify_rows(synthetic(),160,2))
  self.assertNotIn("PRIVATE_",v)
  self.assertNotIn("99999",v)
 def test_exact_full_source_rows_gate(self):
  with self.assertRaises(ValueError):qualify_rows(synthetic())
 def test_exact_group_count_gate(self):
  with self.assertRaises(ValueError):qualify_rows(synthetic(),160,190)
 def test_missing_original_person_round_fails(self):
  with self.assertRaises(ValueError):qualify_rows(synthetic()[:-1],159,2)
 def test_repeated_group_round_more_than_four_fails(self):
  rows=synthetic();rows[0]=(rows[0][0],rows[0][1],rows[0][2],2,rows[0][4],rows[0][5])
  with self.assertRaises(ValueError):qualify_rows(rows,160,2)
 def test_changing_person_id_is_flagged_not_faked_stable(self):
  rows=synthetic()
  a=list(rows[0]);a[0]="SYNTH_OTHER_ACTOR";rows[0]=tuple(a)
  v=qualify_rows(rows,160,2)
  self.assertEqual(v["roster_person_identifier_evidence_counts"]["first_column_not_proven_stable_as_actor_ID"],1)
 def test_actor_ids_absent_cannot_be_qualified(self):
  rows=synthetic();rows[0]=("",)+rows[0][1:]
  v=qualify_rows(rows,160,2)
  self.assertEqual(v["source_first_column_actor_identifier_empty_cells"],1)
  self.assertEqual(v["roster_person_identifier_evidence_counts"]["first_column_not_proven_stable_as_actor_ID"],1)
 def test_alternate_countries_group_code_not_falsely_joined(self):
  v=qualify_rows(synthetic(),160,2)
  self.assertEqual(v["source_unique_country_condition_arms"],2)
 def test_noncountry_record_fails(self):
  rows=synthetic();x=list(rows[0]);x[4]="NEVER_GUESS";rows[0]=tuple(x)
  with self.assertRaises(ValueError):qualify_rows(rows,160,2)
 def test_duplicate_second_sheet_not_appended(self):
  v=qualify_rows(synthetic(),160,2)
  self.assertTrue(v["original_diffprob_sheet_not_appended_due_possible_overlap"])
if __name__=="__main__":unittest.main()
