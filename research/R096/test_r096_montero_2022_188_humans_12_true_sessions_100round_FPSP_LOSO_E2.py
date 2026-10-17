#!/usr/bin/env python3
"""R096 source-free synthetic 6 truly separate groups, 100 binary rounds LOSO."""
import csv,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r096_montero_2022_188_humans_12_true_sessions_100round_FPSP_LOSO_E2 import (
 PROTOCOL,PERIODS,EXPERIMENTS,original_binary,read_original_actions,
 complete_original_session_LOSO)
H=["","round","player","session","opponent","action_player","action_opponent","action_lead","age"]
def peer_for(name,p,t):
 if name=="fix.csv":return p^1
 if t%2:return p^1
 return {0:2,2:0,1:3,3:1}[p]
def gen(name="fix.csv",pattern="stable",change=None):
 f=io.StringIO();w=csv.writer(f);w.writerow(H)
 for ss in range(6):
  for t in range(1,101):
   actions={}
   for p in range(4):
    if pattern=="stable":a=p%2
    elif pattern=="switch":a=t%2
    elif pattern=="sessional":a=ss%2
    else:a=(ss+p+t)%2
    actions[p]=a
   for p in range(4):
    opp=peer_for(name,p,t)
    row=["",str(t),f"SECRET_PERSON_{p}",f"SECRET_SESSION_{ss}",
         f"SECRET_PERSON_{opp}",str(actions[p]),str(actions[opp]),
         "PRIVATE_FUTURE_CHOICE","PRIVATE_AGE"]
    if change:change(row,ss,p,t)
    w.writerow(row)
 return f.getvalue().encode()
def eval_gen(name="fix.csv",pattern="stable"):
 actor,q=read_original_actions(gen(name,pattern),name,24,2400)
 return complete_original_session_LOSO(actor,24)
class BinaryActionContract(unittest.TestCase):
 def test_protocol_frozen(self):self.assertIn("188_HUMANS_100_ROUND_BINARY",PROTOCOL)
 def test_only_author_source_two_conditions(self):self.assertEqual(set(EXPERIMENTS),{"fix.csv","rand.csv"})
 def test_binary_0(self):self.assertEqual(original_binary("0"),0)
 def test_binary_1(self):self.assertEqual(original_binary("1"),1)
 def test_numeric_float_0_1(self):
  self.assertEqual(original_binary("0.0"),0)
  self.assertEqual(original_binary("1.0"),1)
 def test_synthetic_unknown_action_unexpected_rejected(self):
  with self.assertRaises(ValueError):original_binary("UNKNOWN")
 def test_synthetic_2_unsupported(self):
  with self.assertRaises(ValueError):original_binary("2")
 def test_synthetic_missing_denied(self):
  with self.assertRaises(ValueError):original_binary("")
 def test_synthetic_null_denied(self):
  with self.assertRaises(ValueError):original_binary("NaN")
 def test_synthetic_source_persons_24(self):
  actor,q=read_original_actions(gen(), "fix.csv",24,2400)
  self.assertEqual(q["source_distinct_original_participants"],24)
 def test_100round_source(self):
  actor,q=read_original_actions(gen(),"fix.csv",24,2400)
  self.assertEqual(q["source_anonymous_action_behavioral_row_count"],2400)
 def test_partner_original_fix_consistent(self):
  actor,q=read_original_actions(gen(),"fix.csv",24,2400)
  self.assertTrue(q["original_source_partner_0_1_identity_and_action_consistency"])
 def test_partner_original_rand_consistent(self):
  actor,q=read_original_actions(gen("rand.csv"),"rand.csv",24,2400)
  self.assertTrue(q["original_source_partner_0_1_identity_and_action_consistency"])
 def test_partner_source_mismatch_fail_closed(self):
  def bad(r,s,p,t):
   if s==0 and p==0 and t==2:r[6]="1" if r[6]=="0" else "0"
  with self.assertRaises(ValueError):read_original_actions(gen(change=bad),"fix.csv",24,2400)
 def test_partner_source_ID_not_reciprocal(self):
  def bad(r,s,p,t):
   if s==0 and p==0 and t==2:r[4]="NONEXISTENT_PEER"
  with self.assertRaises(ValueError):read_original_actions(gen(change=bad),"fix.csv",24,2400)
 def test_binary_invalid_source_rejected(self):
  def bad(r,s,p,t):
   if s==0 and p==0 and t==2:r[5]="SENSITIVE_UNKNOWN_ACTION"
  with self.assertRaises(ValueError):read_original_actions(gen(change=bad),"fix.csv",24,2400)
 def test_binary_invalid_opponent_source_rejected(self):
  def bad(r,s,p,t):
   if s==0 and p==0 and t==2:r[6]="3"
  with self.assertRaises(ValueError):read_original_actions(gen(change=bad),"fix.csv",24,2400)
 def test_no_demographics_or_actor_ids_exported(self):
  actor,q=read_original_actions(gen(),"fix.csv",24,2400)
  qstr=str(q)
  for token in ("SECRET_PERSON","SECRET_SESSION","PRIVATE_FUTURE_CHOICE","PRIVATE_AGE"):self.assertNotIn(token,qstr)
 def test_strict_original_actor_count(self):
  with self.assertRaises(ValueError):read_original_actions(gen(),"fix.csv",92,2400)
 def test_strict_original_row_count(self):
  with self.assertRaises(ValueError):read_original_actions(gen(),"fix.csv",24,9200)
class ActualSixSessionBrier(unittest.TestCase):
 def test_6_full_original_session_holdouts(self):
  r=eval_gen();self.assertEqual(r["original_true_sessions_left_out_once"],6)
 def test_24_people_times_99_targets(self):
  r=eval_gen();self.assertEqual(r["original_actor_round_t2_to_t100_prediction_pairs"],2376)
 def test_stable_individual_lag_positive(self):
  r=eval_gen()
  self.assertGreater(r["pooled_real_original_target_Brier_comparison"]["M1_gain_M0_minus_M1"],0)
  self.assertEqual(r["pooled_real_original_target_Brier_comparison"]["M1_own_previous_round_binary_Brier"],0)
 def test_synchronized_switch_negative(self):
  r=eval_gen(pattern="switch")
  self.assertLess(r["pooled_real_original_target_Brier_comparison"]["M1_gain_M0_minus_M1"],0)
  self.assertEqual(r["pooled_real_original_target_Brier_comparison"]["M0_other_5_whole_sessions_same_round_Brier"],0)
 def test_M2_fixed_half_helps_stable(self):
  r=eval_gen()
  x=r["pooled_real_original_target_Brier_comparison"]
  self.assertLess(x["M2_fixed_half_Brier"],x["M0_other_5_whole_sessions_same_round_Brier"])
 def test_all_6_sessions_both_signs_correct(self):
  self.assertEqual(eval_gen()["original_six_session_gain_M1_signs"]["positive"],6)
  self.assertEqual(eval_gen(pattern="switch")["original_six_session_gain_M1_signs"]["negative"],6)
 def test_rounds_early_24_late_75(self):
  r=eval_gen()["by_fixed_early_and_late_precommitted_periods"]
  self.assertEqual(r["EARLY_2_25"]["eligible_targets"],24*24)
  self.assertEqual(r["LATER_26_100"]["eligible_targets"],24*75)
 def test_four_disjoint_periods_sum99(self):
  r=eval_gen()["by_fixed_early_and_late_precommitted_periods"]
  n=sum(r[x]["eligible_targets"] for x in ("P1_2_25","P2_26_50","P3_51_75","P4_76_100"))
  self.assertEqual(n,24*99)
 def test_brier_invariant_when_binary_labels_inverted(self):
  actor,q=read_original_actions(gen(),"fix.csv",24,2400)
  x=complete_original_session_LOSO(actor,24)["pooled_real_original_target_Brier_comparison"]
  flipped={(s,p):{t:1-v for t,v in z.items()} for (s,p),z in actor.items()}
  y=complete_original_session_LOSO(flipped,24)["pooled_real_original_target_Brier_comparison"]
  for k in ("M0_other_5_whole_sessions_same_round_Brier","M1_own_previous_round_binary_Brier","M2_fixed_half_Brier","M1_gain_M0_minus_M1","M2_gain_M0_minus_M2"):
   self.assertAlmostEqual(x[k],y[k])
 def test_session_gain_anonymously_sorted(self):
  r=eval_gen()
  self.assertEqual(r["anonymized_sorted_six_session_M1_gains"],sorted(r["anonymized_sorted_six_session_M1_gains"]))
  self.assertNotIn("SECRET_",str(r))
 def test_early_omit_round1(self):
  r=eval_gen()
  self.assertNotIn("round1",str(r))
 def test_source_ID_belongs_to_exact_6_sessions(self):
  actor,q=read_original_actions(gen(),"fix.csv",24,2400)
  del actor[next(iter(actor))]
  with self.assertRaises(ValueError):complete_original_session_LOSO(actor,24)
 def test_0_or_1_binary_is_not_human_cooperation_mapping(self):
  self.assertTrue(eval_gen()["source_action_1_not_assumed_to_mean_cooperation"])
 def test_original_author_literal_C_maps_one(self):self.assertEqual(original_binary("C"),1)
 def test_original_author_literal_D_maps_zero(self):self.assertEqual(original_binary("D"),0)
 def test_original_author_lowercase_not_silently_accepted(self):
  with self.assertRaises(ValueError):original_binary("c")
 def test_source_exact_CD_code_only_when_frozen(self):
  def labels(r,s,p,t):
   r[5]="C" if r[5]=="1" else "D"
   r[6]="C" if r[6]=="1" else "D"
  cohort,q=read_original_actions(gen(change=labels),"fix.csv",24,2400,enforce_literal_C_D=True)
  self.assertEqual(q["source_distinct_original_participants"],24)
 def test_source_numeric0_1_requires_original_author_literality(self):
  with self.assertRaises(ValueError):read_original_actions(gen(),"fix.csv",24,2400,enforce_literal_C_D=True)
 def test_original_CD_recoding_same_Brier_as_synthetic_numeric(self):
  def labels(r,s,p,t):
   r[5]="C" if r[5]=="1" else "D"
   r[6]="C" if r[6]=="1" else "D"
  n,_=read_original_actions(gen(),"fix.csv",24,2400)
  d,_=read_original_actions(gen(change=labels),"fix.csv",24,2400,enforce_literal_C_D=True)
  x=complete_original_session_LOSO(n,24)["pooled_real_original_target_Brier_comparison"]
  y=complete_original_session_LOSO(d,24)["pooled_real_original_target_Brier_comparison"]
  self.assertAlmostEqual(x["M1_gain_M0_minus_M1"],y["M1_gain_M0_minus_M1"])
if __name__=="__main__":unittest.main()
