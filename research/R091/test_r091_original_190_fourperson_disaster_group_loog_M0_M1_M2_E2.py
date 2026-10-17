#!/usr/bin/env python3
"""R091 original-source model family transfer: strictly synthetic action tests."""
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r091_original_190_fourperson_disaster_group_loog_M0_M1_M2_E2 import (
 ARMS,COUNTRIES,TREATMENTS,MODELS,contribution,source_groups,evaluate_group_loo)
SMALL={c:{t:2 for t in TREATMENTS} for c in COUNTRIES}

def synthrows():
 out=[]
 for country,ts in SMALL.items():
  for treatment,n in ts.items():
   for g in range(n):
    for rnd in range(1,21):
     for i in range(4):
      out.append((f"PRIVATE_ACTOR_{country}_{treatment}_{g}_{i}",
          f"PRIVATE_GROUP_{country}_{treatment}_{g}",
          (2 if g==0 else 16),rnd,
          "Phils" if country=="Philippines" else "Sweden",
          {"Control":"Control","10P":"10Prob","40P":"40Prob","Impact":"40Impact","Level":"40Level"}[treatment]))
 return out

def make_fake_groups(kind="stable"):
 out={}
 for country in COUNTRIES:
  for t in TREATMENTS:
   out[(country,t)]={
    f"PRIVATE_{country}_{t}_a":[0.2 if kind=="stable" else (0.2 if i%2==0 else 0.8) for i in range(20)],
    f"PRIVATE_{country}_{t}_b":[0.8 if kind=="stable" else (0.2 if i%2==0 else 0.8) for i in range(20)]}
 return out

class ActionEligibility(unittest.TestCase):
 def test_zero_allowed(self):self.assertEqual(contribution(0),0)
 def test_max_20_allowed(self):self.assertEqual(contribution(20.0),20)
 def test_integer_mid(self):self.assertEqual(contribution(7),7)
 def test_bool_denied(self):
  with self.assertRaises(ValueError):contribution(True)
 def test_missing_denied(self):
  with self.assertRaises(ValueError):contribution(None)
 def test_string_denied(self):
  with self.assertRaises(ValueError):contribution("4")
 def test_negative_denied(self):
  with self.assertRaises(ValueError):contribution(-1)
 def test_over_20_denied(self):
  with self.assertRaises(ValueError):contribution(21)
 def test_fractional_denied(self):
  with self.assertRaises(ValueError):contribution(4.5)
 def test_nan_denied(self):
  with self.assertRaises(ValueError):contribution(float("nan"))
 def test_inf_denied(self):
  with self.assertRaises(ValueError):contribution(float("inf"))
 def test_fixed_three_candidates(self):self.assertEqual(len(MODELS),3)
 def test_frozen_source_groups_per_stratum(self):
  self.assertEqual(sum(sum(x.values()) for x in ARMS.values()),190)

class WholeOriginalGroup(unittest.TestCase):
 def test_syn_source_20_group_or_4_players_every_round(self):
  rows=synthrows();g=source_groups(rows,len(rows),SMALL)
  self.assertEqual(sum(len(x) for x in g.values()),20)
  self.assertAlmostEqual(list(g[("Sweden","Control")].values())[0][0],0.1)
 def test_syn_source_actor_behavior_is_0_20_fraction(self):
  g=source_groups(synthrows(),len(synthrows()),SMALL)
  a=sorted(g[("Sweden","Control")].values(),key=lambda z:z[0])
  self.assertAlmostEqual(a[0][0],0.1)
  self.assertAlmostEqual(a[1][0],0.8)
 def test_syn_source_all_IDs_never_in_scoring_report(self):
  g=source_groups(synthrows(),len(synthrows()),SMALL)
  r=evaluate_group_loo(g,SMALL,20*19)
  self.assertNotIn("PRIVATE_",str(r))
  self.assertFalse(r["group_or_actor_IDs_or_hashed_source_features_in_output"])
 def test_phaseB_country_treatment_map_kept(self):
  g=source_groups(synthrows(),len(synthrows()),SMALL)
  self.assertEqual(len(g[("Philippines","40P")]),2)
 def test_source_original_denominator_15200_default_gate(self):
  with self.assertRaises(ValueError):source_groups(synthrows())
 def test_drop_original_actor_at_last_round_fails(self):
  rows=synthrows()[:-1]
  with self.assertRaises(ValueError):source_groups(rows,len(rows),SMALL)
 def test_duplicate_source_actor_round_fails(self):
  rows=synthrows();rows[1]=rows[0]
  with self.assertRaises(ValueError):source_groups(rows,len(rows),SMALL)
 def test_wrong_original_country_fails(self):
  rows=synthrows();z=list(rows[0]);z[4]="Guessland";rows[0]=tuple(z)
  with self.assertRaises(ValueError):source_groups(rows,len(rows),SMALL)
 def test_wrong_original_treatment_fails(self):
  rows=synthrows();z=list(rows[0]);z[5]="99Prob";rows[0]=tuple(z)
  with self.assertRaises(ValueError):source_groups(rows,len(rows),SMALL)
 def test_missing_contribution_strict_fail(self):
  rows=synthrows();z=list(rows[0]);z[2]=None;rows[0]=tuple(z)
  with self.assertRaises(ValueError):source_groups(rows,len(rows),SMALL)
 def test_actual_source_four_contributions_combine_exact(self):
  g=source_groups(synthrows(),len(synthrows()),SMALL)
  self.assertEqual(len(g[("Sweden","Control")][next(iter(g[("Sweden","Control")]))]),20)

class PredictiveFrozenTransfer(unittest.TestCase):
 def test_small_20_group_total_380_targets(self):
  r=evaluate_group_loo(make_fake_groups(),SMALL,380)
  self.assertEqual(r["original_independent_group_next_round_test_targets"],380)
  self.assertEqual(r["original_fourperson_groups_heldout"],20)
 def test_frozen_real_3610_group_target_count(self):
  with self.assertRaises(ValueError):evaluate_group_loo(make_fake_groups(),SMALL)
 def test_fixed_same_10_strata(self):
  r=evaluate_group_loo(make_fake_groups(),SMALL,380)
  self.assertEqual(len(r["by_original_country_and_treatment"]),10)
 def test_positive_when_group_habit_stable(self):
  r=evaluate_group_loo(make_fake_groups("stable"),SMALL,380)
  self.assertGreater(r["pooled_M0_M1_M2"]["paired_gain_M0_minus_M1"],0)
  self.assertEqual(r["all_source_groups_M1_gain_positive"],20)
 def test_negative_when_synchronous_switching(self):
  r=evaluate_group_loo(make_fake_groups("alternating"),SMALL,380)
  self.assertLess(r["pooled_M0_M1_M2"]["paired_gain_M0_minus_M1"],0)
  self.assertEqual(r["all_source_groups_M1_gain_negative"],20)
 def test_own_group_not_in_training(self):
  r=evaluate_group_loo(make_fake_groups("stable"),SMALL,380)
  self.assertAlmostEqual(r["pooled_M0_M1_M2"]["M1_MSE"],0)
  self.assertGreater(r["pooled_M0_M1_M2"]["M0_MSE"],0)
 def test_halfblend_immutable(self):
  r=evaluate_group_loo(make_fake_groups("stable"),SMALL,380)
  self.assertLess(r["pooled_M0_M1_M2"]["M2_MSE"],r["pooled_M0_M1_M2"]["M0_MSE"])
 def test_source_not_independent_participant_test_rows(self):
  r=evaluate_group_loo(make_fake_groups(),SMALL,380)
  self.assertEqual(r["original_4player_actor_round_contribution_slots"],1600)
 def test_all_test_rounds_2_to_20(self):
  r=evaluate_group_loo(make_fake_groups(),SMALL,380)
  for x in r["by_original_country_and_treatment"].values():
   self.assertEqual(len(x["author_heldout_group_next_round_cooperation_mean_by_round_2_to_20"]),19)
 def test_no_heldout_group_IDs_exported(self):
  r=evaluate_group_loo(make_fake_groups(),SMALL,380)
  self.assertNotIn("PRIVATE_",str(r))
 def test_full_190_real_cohort_required_by_default(self):
  with self.assertRaises(ValueError):evaluate_group_loo(make_fake_groups())
 def test_malformed_group_time_denied(self):
  s=make_fake_groups();s[("Sweden","Control")]["PRIVATE_Sweden_Control_a"]=[0.5]*19
  with self.assertRaises(ValueError):evaluate_group_loo(s,SMALL,380)
 def test_invalid_outcome_denied(self):
  s=make_fake_groups();s[("Sweden","Control")]["PRIVATE_Sweden_Control_a"][5]=2.
  with self.assertRaises(ValueError):evaluate_group_loo(s,SMALL,380)
if __name__=="__main__":unittest.main()
