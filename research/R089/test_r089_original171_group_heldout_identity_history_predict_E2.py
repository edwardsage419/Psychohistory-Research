#!/usr/bin/env python3
"""R089 pure synthetic group holdout and missing-action discrete sharp score tests."""
import hashlib,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r089_original171_group_heldout_identity_history_predict_E2 import (
 MODEL_NAMES,FOLD_SALT,ID_FIELD,ID_AUTHOR_FILES,COMMIT,
 before_round_identity,group_five_folds,group_data,clamp,
 sharp_bounded_squared_loss,shared_target_improvement,evaluate_holdout)
from r088_original_171_groups_multilevel_global_cooperation_E2 import CONDITIONS,PERIODS

def fake_source(size=57,with_identity=True):
 out=[]
 for cond in CONDITIONS:
  for group_index in range(size):
   for human in range(6):
    r={"group_id":f"synthetic-group-{cond}-{group_index:03d}",
       "subgroup_id":f"synthetic-group-{cond}-{group_index:03d}-{'A' if human<3 else 'B'}",
       "condition":cond,ID_FIELD:("-25.7" if with_identity else "")}
    r["game.20.player.DIFI_big_group_distance"]="sensitive-future-should-not-access-999"
    for t in PERIODS:
     r[f"game.{t}.player.contribution"]="global" if human<(2+(group_index%3)) else "self"
    out.append(r)
 return out

class FrozenScientificProtocol(unittest.TestCase):
 def test_complete_model_family(self):self.assertEqual(len(MODEL_NAMES),4)
 def test_original_commit(self):self.assertEqual(COMMIT,"8ce2c0cac4784485232aa96295f48ff147290b05")
 def test_non_future_identity(self):self.assertEqual(ID_FIELD,"survey.1.player.DIFI_big_group_distance")
 def test_two_original_author_scripts(self):self.assertEqual(len(ID_AUTHOR_FILES),2)
 def test_deterministic_fold_key(self):
  ids=[f"g{i}" for i in range(57)]
  self.assertEqual(group_five_folds(ids),group_five_folds(ids[::-1]))
 def test_each_condition_split_count(self):
  out=group_five_folds([f"group{i}" for i in range(57)])
  self.assertEqual(sorted([list(out.values()).count(i) for i in range(5)]),[11,11,11,12,12])
 def test_group_has_single_fold(self):
  out=group_five_folds([f"group{i}" for i in range(57)])
  self.assertEqual(len(out),57)
 def test_seed_frozen(self):self.assertEqual(FOLD_SALT,"R089_GROUP_HOLDOUT_V1_2026_10_17|")

class PregameIdentityNotFutureLeakage(unittest.TestCase):
 def test_lower_bound_pre_identity(self):self.assertAlmostEqual(before_round_identity("-175.7"),0)
 def test_upper_bound_pre_identity(self):self.assertAlmostEqual(before_round_identity("125"),1)
 def test_source_middle(self):self.assertAlmostEqual(before_round_identity("-25.35"),0.5)
 def test_missing_identity(self):self.assertIsNone(before_round_identity(""))
 def test_outside_original_range(self):self.assertIsNone(before_round_identity("126"))
 def test_nonfinite_no_original_score(self):self.assertIsNone(before_round_identity("nan"))
 def test_no_person_level_identity_in_group_result(self):
  g,elig=group_data(fake_source(3),expected_arms=3,expected_missing=0)
  self.assertTrue(elig["all_pregame_identity_rows_in_three_arms_eligible"])
  self.assertNotIn("sensitive-future-should-not-access",str(g))
 def test_missing_identity_gates_M3_but_not_M0(self):
  g,elig=group_data(fake_source(3,False),3,0)
  self.assertFalse(elig["all_pregame_identity_rows_in_three_arms_eligible"])
  self.assertEqual(elig["complete_sixperson_group_identity_failures"],9)
 def test_6_person_identity_group_mean(self):
  g,elig=group_data(fake_source(3),3,0)
  v=list(g["GlobalOnly"].values())[0]
  self.assertAlmostEqual(v["identity"],150/300.7)

class ActualFeasibleSixPersonSharpLoss(unittest.TestCase):
 def test_point_no_missing(self):
  self.assertEqual(sharp_bounded_squared_loss(0.5,3,0),(0,0))
 def test_missing_discrete_not_continuous_projection(self):
  lo,hi=sharp_bounded_squared_loss(0.58,3,1)
  self.assertGreater(lo,0)
  self.assertAlmostEqual(lo,min((.58-.5)**2,(.58-4/6)**2))
 def test_missing_extremal_score_bounds(self):
  lo,hi=sharp_bounded_squared_loss(0,2,3)
  self.assertAlmostEqual(lo,(2/6)**2)
  self.assertAlmostEqual(hi,(5/6)**2)
 def test_source_zero_to_six_legal(self):
  self.assertEqual(sharp_bounded_squared_loss(0,0,6)[0],0)
  self.assertEqual(sharp_bounded_squared_loss(0,0,6)[1],1)
 def test_shared_outcome_positive_gain(self):
  lo,hi=shared_target_improvement(.2,.6,4,0)
  self.assertGreater(lo,0);self.assertAlmostEqual(lo,hi)
 def test_shared_outcome_negative_gain(self):
  lo,hi=shared_target_improvement(.8,.1,4,0)
  self.assertLess(hi,0)
 def test_shared_outcome_missing_bound_spans_zero(self):
  lo,hi=shared_target_improvement(.2,.8,0,6)
  self.assertLess(lo,0);self.assertGreater(hi,0)
 def test_same_model_gain_exact_zero(self):
  self.assertEqual(shared_target_improvement(.5,.5,2,3),(0,0))
 def test_pairwise_gain_diff_not_independent_lower_minus_upper(self):
  lo,hi=shared_target_improvement(.4,.6,2,1)
  direct=[(.4-k/6)**2-(.6-k/6)**2 for k in (2,3)]
  self.assertAlmostEqual(lo,min(direct))
  self.assertAlmostEqual(hi,max(direct))
 def test_clip_bounds(self):self.assertEqual((clamp(-1),clamp(3)),(0,1))

class TrueGroupContractSynthetic(unittest.TestCase):
 def test_complete_171_groups(self):
  g,e=group_data(fake_source(),57,0)
  self.assertEqual({c:len(g[c]) for c in CONDITIONS},{c:57 for c in CONDITIONS})
 def test_eligible_20520_round_slots_in_staged_model(self):
  g,e=group_data(fake_source(),57,0)
  self.assertEqual(sum(len(v["rounds"])*6 for c in CONDITIONS for v in g[c].values()),20520)
 def test_one_missing_action_accepted_with_bound(self):
  data=fake_source(2)
  data[0]["game.1.player.contribution"]=""
  g,e=group_data(data,2,1)
  rr=list(g["GlobalOnly"].values())[0]["rounds"][0]
  self.assertEqual(rr["m"],1)
  self.assertEqual(rr["mid"],(rr["g"]+0.5)/6)
 def test_missing_count_freeze_rejects_actual_different_count(self):
  with self.assertRaisesRegex(ValueError,"MISSINGNESS"):group_data(fake_source())
 def test_unknown_action_fails(self):
  s=fake_source(2);s[0]["game.1.player.contribution"]="unknown-token"
  with self.assertRaises(ValueError):group_data(s,2,0)
 def test_wrong_group_roster_fails(self):
  with self.assertRaises(ValueError):group_data(fake_source(2)[:-1],2,0)
 def test_wrong_local_subgroup_distribution_fails(self):
  s=fake_source(2);s[0]["subgroup_id"]="synthetic-extra"
  with self.assertRaises(ValueError):group_data(s,2,0)
 def test_future_identity_column_never_used(self):
  s=fake_source(2)
  for row in s:row["game.5.player.DIFI_big_group_distance"]="no-access-123456789"
  g,e=group_data(s,2,0)
  self.assertNotIn("123456789",str(g))
 def test_train_holdout_round_scores_real_synthetic_171(self):
  g,e=group_data(fake_source(),57,0)
  result=evaluate_holdout(g,True)
  self.assertEqual(result["heldout_171_groups_x_19_future_rounds"],3249)
  self.assertEqual(result["overall"]["unique_heldout_groups"],171)
  self.assertEqual(result["by_frozen_treatment"]["Balanced"]["heldout_group_rounds"],1083)
 def test_no_ids_are_serialized_in_macro(self):
  g,e=group_data(fake_source(),57,0)
  result=evaluate_holdout(g,True)
  self.assertNotIn("synthetic-group",str(result))
 def test_identity_model_optional_while_first_three_still_score(self):
  g,e=group_data(fake_source(with_identity=False),57,0)
  result=evaluate_holdout(g,False)
  self.assertFalse(result["identity_source_eligible_for_M3"])
  self.assertNotIn(MODEL_NAMES[3],result["overall"]["squared_group_share_error_sharp_bounds"])
  self.assertIn(MODEL_NAMES[2],result["overall"]["squared_group_share_error_sharp_bounds"])
 def test_all_171_groups_complete_fold_heldout(self):
  g,e=group_data(fake_source(),57,0)
  result=evaluate_holdout(g,True)
  for d in result["fold_heldout_group_sizes_by_condition"].values():
   self.assertEqual(sorted(d.values()),[11,11,11,12,12])
 def test_no_ex_post_selector_heldout_results(self):
  g,e=group_data(fake_source(),57,0)
  result=evaluate_holdout(g,True)
  self.assertTrue(result["model_not_hyperparameter_tuned_on_heldout_results"])
if __name__=="__main__":unittest.main()
