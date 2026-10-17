#!/usr/bin/env python3
"""R094 pure synthetic 2015 published binary network human actor histories M012."""
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r094_zhu_nishi_2015_1462_binary_network_participant_holdout_E2 import (
 observed_binary,read_complete_source,score_LOO,FROZEN_SHA256,EXPECTED_PERSONS)
def fake(behavior="stable"):
 rows=[]
 for v in ("0","1"):
  for p in range(3):
   for t in range(1,11):
    y=("0" if p==0 else "1") if behavior=="stable" else \
      ("1" if t%2 else "0") if behavior=="switch" else \
      ("1" if (t+p)%3 else "0")
    rows.append({"node_id":f"PRIVATE_ACTOR_{v}_{p}","round":str(t),
                 "visibility":v,"decision":y})
 return rows

def fake_scores(behavior="stable"):
 x=fake(behavior);ids,vis,q=read_complete_source(x,len(x),6)
 return score_LOO(ids,vis)
class OriginalBinaryValues(unittest.TestCase):
 def test_zero(self):self.assertEqual(observed_binary("0"),0)
 def test_one(self):self.assertEqual(observed_binary("1"),1)
 def test_zero_decimal(self):self.assertEqual(observed_binary("0.0"),0)
 def test_one_decimal(self):self.assertEqual(observed_binary("1.0"),1)
 def test_missing_empty(self):self.assertIsNone(observed_binary(""))
 def test_missing_NA(self):self.assertIsNone(observed_binary("NA"))
 def test_missing_nan(self):self.assertIsNone(observed_binary("NaN"))
 def test_missing_None(self):self.assertIsNone(observed_binary("None"))
 def test_bool_text_denied(self):
  with self.assertRaises(ValueError):observed_binary("true")
 def test_numeric_two_denied(self):
  with self.assertRaises(ValueError):observed_binary("2")
 def test_future_label_denied(self):
  with self.assertRaises(ValueError):observed_binary("Cooperate")
 def test_source_SHA_pin(self):self.assertEqual(FROZEN_SHA256,"b37fa71434dd46249a0e7f43f9b9e798b1d3cafcffea3c80bc6997b99b6dd0a5")
 def test_real_original_source_subject_count(self):self.assertEqual(EXPECTED_PERSONS,1462)
class OriginalSourceRoster(unittest.TestCase):
 def test_complete_10round_actor(self):
  ids,vis,q=read_complete_source(fake(),60,6)
  self.assertEqual(q["source_unique_original_node_IDs"],6)
  self.assertEqual(q["source_observed_original_binary_decisions"],60)
 def test_no_private_data_exported(self):
  ids,vis,q=read_complete_source(fake(),60,6)
  self.assertNotIn("PRIVATE_ACTOR",str(q))
 def test_missing_original_binary_count(self):
  rows=fake();rows[0]["decision"]="NA"
  ids,vis,q=read_complete_source(rows,60,6)
  self.assertEqual(q["source_missing_binary_decision_codes"],1)
 def test_different_actor_status_error(self):
  rows=fake();rows[0]["visibility"]="1"
  with self.assertRaises(ValueError):read_complete_source(rows,60,6)
 def test_duplicate_source_actor_round_error(self):
  rows=fake();rows[1]["round"]=rows[0]["round"]
  with self.assertRaises(ValueError):read_complete_source(rows,60,6)
 def test_missing_original_source_round_error(self):
  rows=fake();rows[1]["round"]="11"
  with self.assertRaises(ValueError):read_complete_source(rows,60,6)
 def test_missing_original_actor_identifier_error(self):
  rows=fake();rows[1]["node_id"]=""
  with self.assertRaises(ValueError):read_complete_source(rows,60,6)
 def test_strict_original_14620_source_rows(self):
  with self.assertRaises(ValueError):read_complete_source(fake())
 def test_wrong_original_subject_count_denied(self):
  with self.assertRaises(ValueError):read_complete_source(fake(),60,1462)
 def test_not_future_leakage_field_allowed(self):
  x=fake();x[0]["decision_lead"]="1"
  with self.assertRaises(ValueError):read_complete_source(x,60,6)
class FrozenBinaryPredictors(unittest.TestCase):
 def test_synthetic_6people_9score_rounds(self):
  r=fake_scores()
  self.assertEqual(r["next_round_current_and_previous_binary_source_action_targets"],54)
 def test_positive_own_last_stable_pattern(self):
  r=fake_scores("stable")
  self.assertGreater(r["all_original_binary_target_records"]["paired_gain_M0_minus_M1"],0)
  self.assertEqual(r["all_original_binary_target_records"]["M1_own_last_binary_action_Brier"],0)
 def test_negative_own_last_synchronized_reversal(self):
  r=fake_scores("switch")
  self.assertLess(r["all_original_binary_target_records"]["paired_gain_M0_minus_M1"],0)
  self.assertEqual(r["all_original_binary_target_records"]["M0_other_person_visibility_round_Brier"],0)
 def test_fixed_halfblend_stable(self):
  r=fake_scores("stable")["all_original_binary_target_records"]
  self.assertLess(r["M2_fixed_halfblend_Brier"],r["M0_other_person_visibility_round_Brier"])
 def test_each_visibility_reported(self):
  r=fake_scores()
  self.assertEqual(set(r["by_original_visible_or_invisible_condition"]),{"0","1"})
 def test_each_forecast_target_uses_2_to_10(self):
  r=fake_scores()
  self.assertEqual(len(r["source_observed_next_round_targets_by_period"]),9)
 def test_not_a_true_session_group_holdout(self):
  r=fake_scores()
  self.assertEqual(r["true_independent_original_session_count_reconstructed"],0)
 def test_does_not_serialize_private_actor_IDs(self):
  s=str(fake_scores());self.assertNotIn("PRIVATE_ACTOR",s)
 def test_missing_previous_choice_decreases_targets(self):
  x=fake();x[0]["decision"]=""
  ids,vis,q=read_complete_source(x,60,6)
  r=score_LOO(ids,vis)
  self.assertEqual(r["next_round_current_and_previous_binary_source_action_targets"],53)
 def test_missing_current_choice_decreases_targets(self):
  x=fake();x[11]["decision"]="NA"
  ids,vis,q=read_complete_source(x,60,6)
  r=score_LOO(ids,vis)
  self.assertEqual(r["next_round_current_and_previous_binary_source_action_targets"],52)
 def test_no_outgroup_other_people_wins_zero_out(self):
  x=fake();x=[z for z in x if not(z["node_id"]=="PRIVATE_ACTOR_1_1")]
  ids,vis,q=read_complete_source(x,len(x),5)
  with self.assertRaises(ValueError):score_LOO(ids,vis)
 def test_positive_sign_person_count(self):
  r=fake_scores("stable")
  self.assertEqual(r["source_complete_person_heldout_M1_gain_sign_counts"].get("M1_positive"),6)
 def test_all_participants_have_scored_targets(self):
  r=fake_scores()
  self.assertEqual(r["source_IDs_with_no_valid_adjacent_observed_actions"],0)
 def test_no_lead_feature_used(self):
  self.assertTrue(fake_scores()["source_decision_lead_future_information_excluded"])
 def test_2015_raw_not_group_linkable(self):
  self.assertEqual(fake_scores()["source_grouping_type"],"INDIVIDUAL_FULL_PERSON_HOLDOUT_NOT_2015_SESSION_HOLDOUT")
if __name__=="__main__":unittest.main()
