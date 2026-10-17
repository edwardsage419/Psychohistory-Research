#!/usr/bin/env python3
"""R093 36 synthetic source participation, real-human target leakage and negative tests."""
import csv,io,math,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r093_original_pereda_1508participant_14round_ownhistory_individual_holdout_E2 import (
 EXPECTED_PERSONS,EXPECTED_BLANK_ROWS,FROZEN_SHA256,source_choice,load_original_cohort,
 group_individual_heldout_score)
COLS=["participant_id","player_alive","group_avg_contribution","player_contribution","round_number","gender","age","treatment"]
SMALL={k:4 for k in EXPECTED_PERSONS}
def fake_original(kind="stable",blank=1,modified=None):
 f=io.StringIO();w=csv.writer(f);w.writerow(COLS)
 for tr in SMALL:
  for person in range(4):
   for t in range(1,15):
    amount=((0 if person==0 else 10) if kind=="stable"
         else (0 if t%2==1 else 10) if kind=="synchronous"
         else (person+t)%11)
    flag="1"
    if kind=="attrition" and tr=="PGG100" and person==0 and t>=8:flag="0"
    row=[f"SECRET_ORIGINAL_{tr}_{person}",flag,999999,amount,t,"PRIVATE_GENDER","PRIVATE_AGE",tr]
    if modified and modified(row,tr,person,t):pass
    w.writerow(row)
 for j in range(blank):w.writerow([""]*8)
 return f.getvalue().encode()
def sample(raw):return load_original_cohort(raw,SMALL,1,337)
class ContributionContract(unittest.TestCase):
 def test_zero(self):self.assertEqual(source_choice("0"),0)
 def test_ten(self):self.assertEqual(source_choice("10"),10)
 def test_even_four(self):self.assertEqual(source_choice("4"),4)
 def test_odd_auto_substitution_legitimate(self):self.assertEqual(source_choice("3"),3)
 def test_decimal_integer(self):self.assertEqual(source_choice("2.0"),2)
 def test_negative_denied(self):
  with self.assertRaises(ValueError):source_choice("-1")
 def test_oversize_denied(self):
  with self.assertRaises(ValueError):source_choice("11")
 def test_fraction_denied(self):
  with self.assertRaises(ValueError):source_choice("2.5")
 def test_missing_denied(self):
  with self.assertRaises(ValueError):source_choice("")
 def test_nonnumeric_denied(self):
  with self.assertRaises(ValueError):source_choice("broken")
 def test_nan_denied(self):
  with self.assertRaises(ValueError):source_choice("nan")
 def test_infinity_denied(self):
  with self.assertRaises(ValueError):source_choice("inf")
 def test_known_original_SHA_pinned(self):self.assertEqual(FROZEN_SHA256,"4eb3380a5eacdef5466709b343af391b27b48a35b5b82f355a4d85d5172644bc")
class OriginalUniverse(unittest.TestCase):
 def test_exact_1508_actor_sample_expected(self):self.assertEqual(sum(EXPECTED_PERSONS.values()),1508)
 def test_six_original_runs_frozen(self):self.assertEqual(len(EXPECTED_PERSONS),6)
 def test_unassigned_source_83_preserved(self):self.assertEqual(EXPECTED_BLANK_ROWS,83)
 def test_synthetic_six_run_full14(self):
  g,q=sample(fake_original())
  self.assertEqual(q["original_author_participant_codes_total"],24)
  self.assertEqual(q["registered_alive_1_actor_round_rows"],336)
 def test_source_private_human_IDs_never_reported(self):
  g,q=sample(fake_original())
  self.assertNotIn("SECRET_ORIGINAL",str(q))
  self.assertTrue(q["original_actor_or_contribution_row_values_exported"] is False)
 def test_wrong_83_count_denied(self):
  with self.assertRaises(ValueError):
   load_original_cohort(fake_original(blank=2),SMALL,1,338)
 def test_dropout_and_no_future_target(self):
  g,q=sample(fake_original("attrition"))
  self.assertEqual(q["registered_alive_1_actor_round_rows"],329)
  r=group_individual_heldout_score(g)
  self.assertLess(r["total_original_source_qualified_next_round_individual_targets"],312)
 def test_source_missing_alive_action_denied(self):
  def replace(row,tr,person,t):
   if tr=="PGG100" and person==0 and t==1:row[3]=""
  with self.assertRaises(ValueError):sample(fake_original(modified=replace))
 def test_empty_alive0_action_allowed(self):
  def replace(row,tr,person,t):
   if tr=="PGG100" and person==0 and t>=8:row[3]=""
  g,q=sample(fake_original("attrition",modified=replace))
  self.assertEqual(q["registered_alive_1_actor_round_rows"],329)
 def test_double_actor_round_denied(self):
  b=fake_original()
  rdr=list(csv.reader(io.StringIO(b.decode())))
  rdr[2][0]=rdr[1][0];rdr[2][4]=rdr[1][4]
  s=io.StringIO();w=csv.writer(s);w.writerows(rdr)
  with self.assertRaises(ValueError):sample(s.getvalue().encode())
 def test_player_different_label_changed_denied(self):
  def modified(row,tr,person,t):
   if tr=="PGG100" and person==0 and t==1:row[7]="UNKNOWN_RUN"
  with self.assertRaises(ValueError):sample(fake_original(modified=modified))
 def test_round14_boundary_denied(self):
  def modified(row,tr,person,t):
   if tr=="PGG100" and person==0 and t==14:row[4]="15"
  with self.assertRaises(ValueError):sample(fake_original(modified=modified))
 def test_reactivated_after_exit_denied(self):
  def modified(row,tr,person,t):
   if tr=="PGG100" and person==0 and t==8:row[1]="0"
  with self.assertRaises(ValueError):sample(fake_original(modified=modified))
 def test_bad_blank_row_if_identity_missing_other_present_denied(self):
  b=fake_original();r=list(csv.reader(io.StringIO(b.decode())))
  r[-1][7]="PGG100"
  s=io.StringIO();csv.writer(s).writerows(r)
  with self.assertRaises(ValueError):sample(s.getvalue().encode())
class IndividualHistoryFrozen(unittest.TestCase):
 def test_6x3x13_targets_312(self):
  g,q=sample(fake_original())
  z=group_individual_heldout_score(g)
  self.assertEqual(z["total_original_source_qualified_next_round_individual_targets"],312)
 def test_one_original_run52_targets(self):
  g,q=sample(fake_original())
  z=group_individual_heldout_score(g)
  self.assertEqual(z["by_original_publisher_experiment"]["PGG100"]["qualified_individual_next_round_target_pairs"],52)
 def test_first_round_unscored(self):
  g,q=sample(fake_original())
  r=group_individual_heldout_score(g)
  self.assertNotIn("1",r["by_original_publisher_experiment"]["PGG100"]["by_round_2_to_14_anonymous_forecast_counts"])
 def test_13_test_rounds_for_14(self):
  g,q=sample(fake_original())
  r=group_individual_heldout_score(g)
  self.assertEqual(len(r["by_original_publisher_experiment"]["PGG100"]["by_round_2_to_14_anonymous_forecast_counts"]),13)
 def test_model_history_positive_stable_individual(self):
  g,q=sample(fake_original())
  r=group_individual_heldout_score(g)
  self.assertGreater(r["pooled_paired_gain_M0_minus_M1"],0)
  self.assertAlmostEqual(r["pooled_M1_own_previous_round_MSE"],0)
 def test_model_negative_synchronous_alternation(self):
  g,q=sample(fake_original("synchronous"))
  r=group_individual_heldout_score(g)
  self.assertLess(r["pooled_paired_gain_M0_minus_M1"],0)
  self.assertAlmostEqual(r["pooled_M0_other_alive_same_run_round_MSE"],0)
 def test_self_excluded_from_other_same_round_mean(self):
  g,q=sample(fake_original())
  r=group_individual_heldout_score(g)
  self.assertGreater(r["pooled_M0_other_alive_same_run_round_MSE"],0)
 def test_model_exact_half_blend_lowers_stable_baseline_error(self):
  g,q=sample(fake_original())
  r=group_individual_heldout_score(g)
  self.assertLess(r["pooled_M2_fixed_half_MSE"],r["pooled_M0_other_alive_same_run_round_MSE"])
 def test_no_person_identifier_output(self):
  g,q=sample(fake_original())
  z=str(group_individual_heldout_score(g))
  self.assertNotIn("SECRET_ORIGINAL",z)
  self.assertTrue(group_individual_heldout_score(g)["source_original_person_IDs_actor_traces_or_raw_actions_exported"] is False)
 def test_6_original_run_mean_reported(self):
  g,q=sample(fake_original())
  z=group_individual_heldout_score(g)
  self.assertEqual(z["six_runs_in_which_M1_improves_M0"],6)
 def test_dropout_data_not_falsely_scored_as_human(self):
  g,q=sample(fake_original("attrition"))
  z=group_individual_heldout_score(g)
  self.assertEqual(z["total_original_source_qualified_next_round_individual_targets"],305)
 def test_no_cluster_CI_fabricated(self):
  g,q=sample(fake_original())
  r=group_individual_heldout_score(g)
  self.assertFalse(r["independent_new_experiment_group_clustering_confidence_intervals_computed"])
if __name__=="__main__":unittest.main()
