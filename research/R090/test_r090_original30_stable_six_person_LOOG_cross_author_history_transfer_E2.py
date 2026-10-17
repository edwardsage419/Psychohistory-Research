#!/usr/bin/env python3
"""R090 28+ purely synthetic transfer scoring and eligibility tests."""
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r090_original30_stable_six_person_LOOG_cross_author_history_transfer_E2 import (
 bounded_float,indicator_meta,parse_author_group_rounds,score_loo,AUTHOR_EXPECTED_GROUPS,
 TRAIN_MODELS)
from r090_independent_climate_clubs_original_roster_source_gate import TREATMENTS

def fake_humans():
 out=[]
 for treatment,n in AUTHOR_EXPECTED_GROUPS.items():
  for group in range(n):
   for t in range(1,16):
    for person in range(6):
     endowment=20 if person<2 else 10
     relative=(group+person+t)%11/10
     x={"session.code":f"synthetic-session-{treatment}",
       "group.id_in_subsession":str(group+1),
       "participant.code":f"{treatment}-g{group}-p{person}",
       "treatment":treatment,"subsession.round_number":str(t),
       "participant._round_number":"15",
       "player.contribution":str(endowment*relative),
       "player.endowment":str(endowment),
       "player.automatic_decision":"0",
       "player.timeout_contr":"0"}
     out.append(x)
 return out

def fake_groups(n=2):
 return {t:{f"private-{t}-g{i}":[(i+0.25)/3 +0.05*(j%3) for j in range(15)]
             for i in range(n)} for t in TREATMENTS}

class NumericElig(unittest.TestCase):
 def test_allow_numeric_zero_contribution(self):self.assertEqual(bounded_float("0","contribution"),0)
 def test_allow_decimal(self):self.assertEqual(bounded_float("5.5","contribution"),5.5)
 def test_allow_positive_endowment(self):self.assertEqual(bounded_float("0.1","endowment",True),0.1)
 def test_reject_zero_endowment(self):
  with self.assertRaises(ValueError):bounded_float("0","endowment",True)
 def test_reject_negative(self):
  with self.assertRaises(ValueError):bounded_float("-1","contribution")
 def test_reject_empty(self):
  with self.assertRaises(ValueError):bounded_float("","contribution")
 def test_reject_NA(self):
  with self.assertRaises(ValueError):bounded_float("NA","contribution")
 def test_reject_nan(self):
  with self.assertRaises(ValueError):bounded_float("nan","contribution")
 def test_reject_inf(self):
  with self.assertRaises(ValueError):bounded_float("inf","contribution")
 def test_source_auto_indicator_flags(self):self.assertEqual(indicator_meta("1"),"1")
 def test_auto_unknown(self):self.assertEqual(indicator_meta("NA"),"unknown")
 def test_auto_invalid_fails(self):
  with self.assertRaises(ValueError):indicator_meta("YES")

class SixPlayerRoster(unittest.TestCase):
 def test_30_groups_450_group_rounds_2700_human_decisions(self):
  group,info=parse_author_group_rounds(fake_humans())
  self.assertEqual(sum(map(len,group.values())),30)
  self.assertEqual(info["original_450_group_round_contribution_shares"],450)
  self.assertEqual(info["original_2700_actor_round_contributions_read"],2700)
 def test_exact_original_T1_T2_T3_T4_cohort_sizes(self):
  groups,_=parse_author_group_rounds(fake_humans())
  self.assertEqual({k:len(v) for k,v in groups.items()},AUTHOR_EXPECTED_GROUPS)
 def test_endowment_weighted_group_contribution(self):
  groups,_=parse_author_group_rounds(fake_humans())
  self.assertTrue(0<=list(groups["T1"].values())[0][0]<=1)
 def test_no_real_id_in_cohort_quality_receipt(self):
  groups,info=parse_author_group_rounds(fake_humans())
  self.assertNotIn("synthetic-session-",str(info))
  self.assertFalse(info["any_original_actor_or_group_IDs_exported"])
 def test_reject_source_membership_movement(self):
  source=fake_humans()
  source[0]["participant.code"]="made-up-new-actor"
  with self.assertRaises(ValueError):parse_author_group_rounds(source)
 def test_reject_contribution_greater_than_endowment(self):
  source=fake_humans();source[0]["player.contribution"]="50"
  with self.assertRaisesRegex(ValueError,"EXCEEDS_ENDOWMENT"):parse_author_group_rounds(source)
 def test_reject_empty_endowment(self):
  source=fake_humans();source[0]["player.endowment"]=""
  with self.assertRaises(ValueError):parse_author_group_rounds(source)
 def test_reject_bad_original_period(self):
  source=fake_humans();source[0]["subsession.round_number"]="16"
  with self.assertRaises(ValueError):parse_author_group_rounds(source)
 def test_reject_otree_technical_as_real_clock(self):
  source=fake_humans();source[0]["participant._round_number"]="1"
  with self.assertRaises(ValueError):parse_author_group_rounds(source)
 def test_reject_duplicate_person_round(self):
  source=fake_humans();source[1]["participant.code"]=source[0]["participant.code"]
  with self.assertRaises(ValueError):parse_author_group_rounds(source)
 def test_auto_flags_only_reported(self):
  source=fake_humans();source[0]["player.automatic_decision"]="1"
  groups,info=parse_author_group_rounds(source)
  self.assertEqual(info["auto_decision_observed_counts_by_treatment"]["T1"]["one"],1)
 def test_timeout_flags_only_reported(self):
  source=fake_humans();source[0]["player.timeout_contr"]="1"
  groups,info=parse_author_group_rounds(source)
  self.assertEqual(info["contribution_timeouts_by_treatment"]["T1"]["one"],1)
 def test_actor_choice_values_not_exported(self):
  groups,info=parse_author_group_rounds(fake_humans())
  self.assertNotIn("player.contribution",str(info))
  self.assertNotIn("participant.code",str(info))
 def test_no_missing_actor_drop(self):
  source=fake_humans()[:-1]
  with self.assertRaises(ValueError):parse_author_group_rounds(source)

class FrozenTransfer(unittest.TestCase):
 def test_three_frozen_model_names(self):self.assertEqual(len(TRAIN_MODELS),3)
 def test_small_all_arm_no_private_ids_exported(self):
  results=score_loo(fake_groups(),{t:2 for t in TREATMENTS},112)
  self.assertNotIn("private-",str(results))
 def test_small_all_arm_112_heldout_rounds(self):
  results=score_loo(fake_groups(),{t:2 for t in TREATMENTS},112)
  self.assertEqual(results["source_independent_author_heldout_forecast_targets"],112)
 def test_two_models_predictive_gain_can_be_negative(self):
  scores=score_loo(fake_groups(),{t:2 for t in TREATMENTS},112)
  self.assertIsInstance(scores["M1_history_pooled_shared_target_gain_over_M0"],float)
 def test_frozen_30_full_group_dataset_420_targets(self):
  g,source=parse_author_group_rounds(fake_humans())
  a=score_loo(g)
  self.assertEqual(a["source_independent_author_heldout_forecast_targets"],420)
  self.assertEqual(a["source_independent_groups_heldout"],30)
 def test_each_group_has_one_holdout_and_14_forecasts(self):
  g,source=parse_author_group_rounds(fake_humans())
  scores=score_loo(g)
  self.assertEqual(scores["by_original_author_treatment"]["T1"]["heldout_original_group_round_scores"],112)
  self.assertEqual(scores["by_original_author_treatment"]["T3"]["heldout_original_group_round_scores"],98)
 def test_false_positive_fail_when_not_enough_train_groups(self):
  s={t:{"one":[0.5]*15} for t in TREATMENTS}
  with self.assertRaises(ValueError):score_loo(s,{t:1 for t in TREATMENTS},56)
 def test_wrong_15_rounds_fails(self):
  s=fake_groups();s["T1"]["private-T1-g0"]=[0.1]*14
  with self.assertRaises(ValueError):score_loo(s,{t:2 for t in TREATMENTS},112)
 def test_wrong_condition_count_rejected(self):
  with self.assertRaises(ValueError):score_loo(fake_groups())
 def test_group_by_round_true_prediction_improves_when_stable(self):
  s={t:{f"g{i}":[0.1 if i==0 else 0.9]*15 for i in range(2)} for t in TREATMENTS}
  result=score_loo(s,{t:2 for t in TREATMENTS},112)
  self.assertGreater(result["M1_history_pooled_shared_target_gain_over_M0"],0)
 def test_group_by_round_history_worse_when_alternating(self):
  s={t:{f"g{i}":[0.1 if t0%2==0 else 0.9 for t0 in range(15)]
        for i in range(2)} for t in TREATMENTS}
  result=score_loo(s,{t:2 for t in TREATMENTS},112)
  self.assertLess(result["M1_history_pooled_shared_target_gain_over_M0"],0)
if __name__=="__main__":unittest.main()
