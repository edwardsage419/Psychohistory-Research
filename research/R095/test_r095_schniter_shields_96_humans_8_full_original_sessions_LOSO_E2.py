#!/usr/bin/env python3
"""Synthetic only: strict 2020 original human lab-session Foe/Split binary choices."""
import csv,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r095_schniter_shields_96_humans_8_full_original_sessions_LOSO_E2 import (
 SHA256,PROTOCOL,cooperation,partner_choice_bit,anonymous_real_actions,evaluate_8_sessions)
HEADER=["ID","round","option","session","group","other_split","age","optionAfraid"]
def fixture(mode="stable", third=False,mutator=None):
 b=io.StringIO();w=csv.writer(b);w.writerow(HEADER)
 for sess in range(3):
  for pair in range(2):
   for t in (1,2,3) if third and sess==1 else (1,2):
    acts=[]
    for p in (0,1):
     if mode=="stable":act=(p+pair)%2
     elif mode=="reversal":act=0 if t==1 else 1
     elif mode=="notconstant":act=(p+t+sess)%2
     acts.append(act)
    for p in (0,1):
     row=[f"PRIVATE_PERSON_{sess}_{pair}_{p}",t,
          "split" if acts[p] else "take all",f"PRIVATE_LAB_{sess}",str(pair),str(acts[1-p]),"SECRET_AGE","SECRET_MOOD"]
     if mutator is not None:mutator(row,sess,pair,p,t)
     w.writerow(row)
 return b.getvalue().encode()
def evaluate_fake(mode="stable"):
 s,q=anonymous_real_actions(fixture(mode),3,4,24)
 return evaluate_8_sessions(s,3,4)
class StrictOutcomeSource(unittest.TestCase):
 def test_source_sha_lock(self):self.assertEqual(SHA256,"0678cc3d565d3a02e4766fedff211cc37b2e0e9d373e41c391466c6f84a56f4c")
 def test_frozen_protocol_name(self):self.assertIn("8_REAL_2020_LAB_SESSIONS",PROTOCOL)
 def test_split(self):self.assertEqual(cooperation(" SPLIT "),1)
 def test_take_all(self):self.assertEqual(cooperation("Take All"),0)
 def test_other_choice_zero(self):self.assertEqual(partner_choice_bit("0"),0)
 def test_other_choice_one(self):self.assertEqual(partner_choice_bit("1"),1)
 def test_unknown_action_rejected(self):
  with self.assertRaises(ValueError):cooperation("unknown")
 def test_missing_action_rejected(self):
  with self.assertRaises(ValueError):cooperation("")
 def test_unknown_other_flag_rejected(self):
  with self.assertRaises(ValueError):partner_choice_bit("0.5")
 def test_synthetic_3_sessions_12humans_full2round(self):
  ps,q=anonymous_real_actions(fixture(),3,4,24)
  self.assertEqual(q["original_human_people"],12)
  self.assertEqual(q["original_observed_second_round_binary_choices"],12)
 def test_synthetic_third_excluded(self):
  ps,q=anonymous_real_actions(fixture(third=True),3,4,28)
  self.assertEqual(q["original_human_people"],12)
  self.assertEqual(q["original_published_total_actor_round_rows_including_excluded_third_round"],28)
 def test_original_session_labels_not_exported(self):
  ps,q=anonymous_real_actions(fixture(),3,4,24)
  self.assertNotIn("PRIVATE_",str(q))
 def test_demographics_not_inspected(self):
  ps,q=anonymous_real_actions(fixture(),3,4,24)
  self.assertNotIn("SECRET_",str(q))
 def test_missing_actor_choice_denied(self):
  def f(r,s,g,p,t):
   if s==0 and g==0 and p==1 and t==1:r[2]=""
  with self.assertRaises(ValueError):anonymous_real_actions(fixture(mutator=f),3,4,24)
 def test_partner_report_mismatch_denied(self):
  def f(r,s,g,p,t):
   if s==0 and g==0 and p==1 and t==2:r[5]="1" if r[5]=="0" else "0"
  with self.assertRaises(ValueError):anonymous_real_actions(fixture(mutator=f),3,4,24)
 def test_wrong_original_actor_universe_denied(self):
  with self.assertRaises(ValueError):anonymous_real_actions(fixture(),8,12,204)
 def test_change_original_group_eligibility_denied(self):
  def f(r,s,g,p,t):
   if s==0 and g==0 and p==1 and t==2:r[4]="99"
  with self.assertRaises(ValueError):anonymous_real_actions(fixture(mutator=f),3,4,24)
class SessionHeldout(unittest.TestCase):
 def test_all_human_targets_one_round2(self):
  r=evaluate_fake()
  self.assertEqual(r["original_binary_round_2_predictions_all_subjects"],12)
 def test_all_three_real_sessions_excluded(self):
  r=evaluate_fake()
  self.assertEqual(r["entire_source_sessions_left_out_exactly_once"],3)
 def test_own_history_positive_when_stable(self):
  r=evaluate_fake("stable")
  self.assertGreater(r["paired_gain_M0_minus_M1"],0)
  self.assertAlmostEqual(r["M1_own_first_round_binary_Brier_MSE"],0)
 def test_own_history_negative_when_all_synchronize_reversal(self):
  r=evaluate_fake("reversal")
  self.assertLess(r["paired_gain_M0_minus_M1"],0)
  self.assertAlmostEqual(r["M0_seven_other_sessions_second_round_Brier_MSE"],0)
 def test_fixed_half_is_stable(self):
  r=evaluate_fake("stable")
  self.assertLess(r["M2_fixed_halfblend_Brier_MSE"],r["M0_seven_other_sessions_second_round_Brier_MSE"])
 def test_independent_session_signs_all8_or_test3(self):
  r=evaluate_fake("stable")
  self.assertEqual(sum(r["source_genuine_lab_session_signs_M1"].values()),3)
 def test_session_gain_sorted_no_original_group_labels(self):
  r=evaluate_fake("stable")
  self.assertEqual(r["anonymous_sorted_per_session_M1_gains"],sorted(r["anonymous_sorted_per_session_M1_gains"]))
  self.assertNotIn("PRIVATE_",str(r))
 def test_round3_only_one_session_not_score(self):
  x,q=anonymous_real_actions(fixture(third=True),3,4,28)
  z=evaluate_8_sessions(x,3,4)
  self.assertEqual(z["original_binary_round_2_predictions_all_subjects"],12)
 def test_holdout_never_original_person_id_output(self):
  r=evaluate_fake("notconstant")
  self.assertTrue(r["training_all_12_holdout_people_excluded_from_M0"])
  self.assertNotIn("PRIVATE_PERSON",str(r))
 def test_group_counts_unqualified_denied(self):
  ps,q=anonymous_real_actions(fixture(),3,4,24)
  with self.assertRaises(ValueError):evaluate_8_sessions(ps,8,12)
if __name__=="__main__":unittest.main()
