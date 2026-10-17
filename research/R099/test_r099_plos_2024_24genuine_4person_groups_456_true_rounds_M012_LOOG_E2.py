#!/usr/bin/env python3
"""R099 E2 synthetic 24 x4 stage2, 20 rounds, 456 group targets only."""
import csv,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r099_plos_2024_24genuine_4person_groups_456_true_rounds_M012_LOOG_E2 import (
 PROTOCOL,contribution,original_group_actions,score)
from r099_phase_b_plos_2024_fixed4p_nonbehavior_group_roster_only import EXPECTED_HEADER
def demo(pattern="stable",edit=None):
 s=io.StringIO();w=csv.writer(s);w.writerow(EXPECTED_HEADER)
 for g in range(24):
  for actor in range(4):
   for t in range(1,21):
    if pattern=="stable":c=20 if (g+actor)%2 else 0
    elif pattern=="switch":c=0 if t%2 else 20
    elif pattern=="groups":c=20 if g%2 else 0
    else:c=(g+actor+t)%21
    row=[str(g*4+actor),"PRIVATE_ID_"+str(g*4+actor),str(t),str(g),
         str(g//12),str(c),"PRIVATE_OTHER_CONTRI","PRIVATE_COOP_DISPOSITION"]
    if edit:edit(row,g,actor,t)
    w.writerow(row)
 return s.getvalue().encode()
def result(pattern="stable"):
 f,c,q=original_group_actions(demo(pattern))
 return score(f,c)
class SourceAction(unittest.TestCase):
 def test_protocol(self):self.assertIn("24_TRUE_FIXED_4PERSON_GROUPS",PROTOCOL)
 def test_integer_zero(self):self.assertEqual(contribution("0"),0)
 def test_integer_twenty(self):self.assertEqual(contribution("20"),20)
 def test_integer_decimal_twenty(self):self.assertEqual(contribution("20.0"),20)
 def test_integer_decimal_fraction_denied(self):
  with self.assertRaises(ValueError):contribution("20.5")
 def test_source_negative_denied(self):
  with self.assertRaises(ValueError):contribution("-1")
 def test_source_twentyone_denied(self):
  with self.assertRaises(ValueError):contribution("21")
 def test_source_nan_denied(self):
  with self.assertRaises(ValueError):contribution("NaN")
 def test_source_missing_denied(self):
  with self.assertRaises(ValueError):contribution("")
 def test_source_type_disposition_not_used(self):
  f,c,q=original_group_actions(demo())
  self.assertFalse(q["original_source_OtherContri_or_Type_fields_ever_read_or_used"])
 def test_source_all96_humans(self):
  f,c,q=original_group_actions(demo())
  self.assertEqual(q["original_real_human_actor_count"],96)
 def test_source_full1920_human_round_rows(self):
  f,c,q=original_group_actions(demo())
  self.assertEqual(q["original_first_party_action_cells"],1920)
 def test_source_24_fixed_four_person_groups(self):
  f,c,q=original_group_actions(demo())
  self.assertEqual(len(f),24)
  self.assertEqual(q["original_real_fixed_four_person_groups"],24)
 def test_source_each_all20(self):
  f,c,q=original_group_actions(demo())
  self.assertTrue(all(set(d)==set(range(1,21)) for d in f.values()))
 def test_source_12_groups_per_condition(self):
  f,c,q=original_group_actions(demo())
  self.assertEqual(sorted(map(len,c.values())),[12,12])
 def test_group_fraction_half_when_two_twenty_two_zero(self):
  f,c,q=original_group_actions(demo())
  self.assertAlmostEqual(f["0"][1],0.5)
 def test_contribution_out_of_bound_in_original_denied(self):
  def change(row,g,a,t):
   if g==0 and a==0 and t==1:row[5]="21"
  with self.assertRaises(ValueError):original_group_actions(demo(edit=change))
 def test_original_one_actor_round_duplicate_denied(self):
  def change(row,g,a,t):
   if g==0 and a==0 and t==2:row[2]="1"
  with self.assertRaises(ValueError):original_group_actions(demo(edit=change))
 def test_original_person_changed_group_denied(self):
  def change(row,g,a,t):
   if g==0 and a==0 and t==2:row[3]="1"
  with self.assertRaises(ValueError):original_group_actions(demo(edit=change))
 def test_original_group_changes_treatment_denied(self):
  def change(row,g,a,t):
   if g==0 and a==0 and t==2:row[4]="1"
  with self.assertRaises(ValueError):original_group_actions(demo(edit=change))
 def test_original_action_actor_micro_values_not_exported(self):
  f,c,q=original_group_actions(demo())
  z=str(q)
  for text in ("PRIVATE_ID","PRIVATE_OTHER","PRIVATE_COOP"):self.assertNotIn(text,z)
class HoldoutMSE(unittest.TestCase):
 def test_full456_original_target_groups(self):
  self.assertEqual(result()["original_real_next_round_group_share_predictions"],456)
 def test_only24_independent_group_units(self):
  self.assertEqual(result()["original_actual_whole_source_fixed_groups"],24)
 def test_no_true_session_id_fabrication(self):
  self.assertFalse(result()["source_true_independent_lab_session_labels_recovered"])
 def test_m0_all_heldout_group_excluded(self):
  self.assertTrue(result()["source_heldout_group_every_round_excluded_from_M0"])
 def test_228_targets_per_two_conditions(self):
  z=result()["by_original_FEEDBACK_treatment_hidden_literal_identity"]
  self.assertEqual([q["real_group_round_target_predictions"] for q in z.values()],[228,228])
 def test_12_original_groups_each_condition(self):
  z=result()["by_original_FEEDBACK_treatment_hidden_literal_identity"]
  self.assertEqual([q["source_groups_within_this_treatment"] for q in z.values()],[12,12])
 def test_early_four_target_rounds(self):
  z=result()["by_original_FEEDBACK_treatment_hidden_literal_identity"]
  self.assertEqual(next(iter(z.values()))["early_rounds_t2_5"]["targets"],48)
 def test_later_fifteen_target_rounds(self):
  z=result()["by_original_FEEDBACK_treatment_hidden_literal_identity"]
  self.assertEqual(next(iter(z.values()))["later_rounds_t6_20"]["targets"],180)
 def test_synthetic_stable_history_M1_superior(self):
  z=result("groups")["overall_same_target_original_group_share_MSE"]
  self.assertGreater(z["paired_gain_M0_minus_M1"],0)
  self.assertEqual(z["M1_heldout_group_own_previous_round_MSE"],0)
 def test_synthetic_switch_history_M1_inferior(self):
  z=result("switch")["overall_same_target_original_group_share_MSE"]
  self.assertLess(z["paired_gain_M0_minus_M1"],0)
  self.assertEqual(z["M0_other_source_groups_same_treatment_same_round_MSE"],0)
 def test_fixed_M2_is_exact_half(self):
  z=result("groups")["overall_same_target_original_group_share_MSE"]
  self.assertAlmostEqual(z["M2_fixed_half_MSE"],z["M0_other_source_groups_same_treatment_same_round_MSE"]/4)
 def test_original_group_M1_positive_negative_signs_reported(self):
  z=result("groups")["by_original_FEEDBACK_treatment_hidden_literal_identity"]
  self.assertEqual(sum(q["positive_vs_negative_12_real_group_M1_gain_counts"]["positive"] for q in z.values()),24)
 def test_negative_group_signs_preserved(self):
  z=result("switch")["by_original_FEEDBACK_treatment_hidden_literal_identity"]
  self.assertEqual(sum(q["positive_vs_negative_12_real_group_M1_gain_counts"]["negative"] for q in z.values()),24)
 def test_sorted_anonymous_group_losses_no_group_ids(self):
  z=str(result("groups"))
  self.assertNotIn("PRIVATE_ID",z)
 def test_original_456_person_round_not_independent_sessions(self):
  z=result()
  self.assertFalse(z["source_true_independent_lab_session_labels_recovered"])
 def test_source_unauthorized_wrong_group_count(self):
  f,c,q=original_group_actions(demo())
  f.pop("0")
  with self.assertRaises(ValueError):score(f,c)
if __name__=="__main__":unittest.main()
