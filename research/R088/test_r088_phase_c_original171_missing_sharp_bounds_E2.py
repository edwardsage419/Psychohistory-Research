#!/usr/bin/env python3
"""R088 phase C fully synthetic missing-value sharp group bounds and group-level tests."""
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r088_phase_c_original171_missing_sharp_bounds_E2 import (
 boundary_group,bounded_group_experiment,effect_pair_bounds)
from r088_original_171_groups_multilevel_global_cooperation_E2 import PERIODS,CONDITIONS

def rows():
 result=[]
 for cond in CONDITIONS:
  for person in range(6):
   x={"group_id":f"synthetic-{cond}",
      "subgroup_id":f"synthetic-{cond}-{'A' if person<3 else 'B'}",
      "condition":cond}
   for i in PERIODS:
    x[f"game.{i}.player.contribution"]="global" if person<4 else "self"
   result.append(x)
 return result

class OriginalBounds(unittest.TestCase):
 def test_both_original_subgroups(self):
  treatment,r=boundary_group(rows()[:6])
  self.assertEqual(treatment,"GlobalOnly")
  self.assertEqual(len(r),20)
 def test_known_four_meets_threshold(self):
  _,r=boundary_group(rows()[:6])
  self.assertEqual(r[0]["certain_global_threshold_success"],1)
 def test_3_observed_one_missing_might_meet(self):
  data=rows()[:6]
  data[0]["game.1.player.contribution"]=""
  _,v=boundary_group(data)
  self.assertEqual(v[0]["confirmed_global"],3)
  self.assertEqual(v[0]["unobserved_missing_action"],1)
  self.assertEqual(v[0]["certain_global_threshold_success"],0)
  self.assertEqual(v[0]["possible_global_threshold_success"],1)
 def test_2_observed_one_missing_never_meets(self):
  data=rows()[:6]
  data[0]["game.1.player.contribution"]=""
  data[1]["game.1.player.contribution"]="self"
  _,v=boundary_group(data)
  self.assertEqual(v[0]["possible_global_threshold_success"],0)
 def test_whitespace_missing(self):
  data=rows()[:6];data[0]["game.1.player.contribution"]=" "
  _,v=boundary_group(data)
  self.assertEqual(v[0]["unobserved_missing_action"],1)
 def test_none_missing(self):
  data=rows()[:6];data[0]["game.1.player.contribution"]=None
  _,v=boundary_group(data)
  self.assertEqual(v[0]["unobserved_missing_action"],1)
 def test_unknown_action_still_fails(self):
  data=rows()[:6];data[0]["game.1.player.contribution"]="unk"
  with self.assertRaisesRegex(ValueError,"ACTION_NOT_MISSING"):boundary_group(data)
 def test_globalonly_local_still_fails(self):
  data=rows()[:6];data[0]["game.1.player.contribution"]="local"
  with self.assertRaisesRegex(ValueError,"UNAVAILABLE_LOCAL"):boundary_group(data)
 def test_all_six_action_conserved_with_missing(self):
  data=rows()[:6];data[0]["game.1.player.contribution"]=""
  _,v=boundary_group(data);x=v[0]
  self.assertEqual(x["confirmed_global"]+x["confirmed_local"]+x["confirmed_other"]+x["confirmed_self"]+x["unobserved_missing_action"],6)
 def test_different_condition_members_fails(self):
  data=rows()[:6];data[0]["condition"]="Balanced"
  with self.assertRaises(ValueError):boundary_group(data)
 def test_not_six_fails(self):
  with self.assertRaises(ValueError):boundary_group(rows()[:5])
 def test_wrong_subgroup_distribution_fails(self):
  data=rows()[:6];data[0]["subgroup_id"]="third"
  with self.assertRaises(ValueError):boundary_group(data)
 def test_no_missing_analytical_point_bounds(self):
  r=bounded_group_experiment(rows(),groups_per_treatment=1,required_missing=0)
  z=r["original_three_treatments_sharp_source_bounded_group_results"]["GlobalOnly"]
  self.assertAlmostEqual(z["global_cooperation_over_all20_lower"],4/6)
  self.assertAlmostEqual(z["global_cooperation_over_all20_upper"],4/6)
  self.assertEqual(z["global_threshold_success_certain_group_rounds"],20)
 def test_one_missing_one_20_round_sharp(self):
  data=rows()
  data[0]["game.1.player.contribution"]=""
  r=bounded_group_experiment(data,groups_per_treatment=1,required_missing=1)
  z=r["original_three_treatments_sharp_source_bounded_group_results"]["GlobalOnly"]
  self.assertAlmostEqual(z["global_cooperation_over_all20_upper"]-z["global_cooperation_over_all20_lower"],1/120)
  self.assertAlmostEqual(z["first_last_group_equal_delta_sharp_lower"],0)
  self.assertAlmostEqual(z["first_last_group_equal_delta_sharp_upper"],1/6)
 def test_globalonly_missing_local_bound_always_zero(self):
  data=rows();data[0]["game.1.player.contribution"]=""
  r=bounded_group_experiment(data,1,1)
  z=r["original_three_treatments_sharp_source_bounded_group_results"]["GlobalOnly"]["original_round_1_to_20_complete_group_sharp_intervals"][0]
  self.assertEqual(z["local_either_group_fraction_sharp_upper"],0.0)
 def test_threshold_uncertain_only_once(self):
  data=rows();data[0]["game.1.player.contribution"]=""
  r=bounded_group_experiment(data,1,1)
  self.assertEqual(r["original_three_treatments_sharp_source_bounded_group_results"]["GlobalOnly"]["global_threshold_undecidable_group_rounds"],1)
 def test_first_last_missing_in_last(self):
  data=rows();data[0]["game.20.player.contribution"]=""
  r=bounded_group_experiment(data,1,1)
  z=r["original_three_treatments_sharp_source_bounded_group_results"]["GlobalOnly"]
  self.assertAlmostEqual(z["first_last_group_equal_delta_sharp_lower"],-1/6)
  self.assertAlmostEqual(z["first_last_group_equal_delta_sharp_upper"],0)
 def test_sign_guaranteed_decrease(self):
  data=rows()
  for p in data[:4]:p["game.20.player.contribution"]="self"
  r=bounded_group_experiment(data,1,0)
  z=r["original_three_treatments_sharp_source_bounded_group_results"]["GlobalOnly"]
  self.assertEqual(z["groups_guaranteed_decreasing"],1)
 def test_sign_guaranteed_increase(self):
  data=rows()
  for p in data[:4]:p["game.1.player.contribution"]="self"
  r=bounded_group_experiment(data,1,0)
  z=r["original_three_treatments_sharp_source_bounded_group_results"]["GlobalOnly"]
  self.assertEqual(z["groups_guaranteed_increasing"],1)
 def test_missing_is_not_forced_stable(self):
  data=rows();data[0]["game.1.player.contribution"]=""
  r=bounded_group_experiment(data,1,1)
  z=r["original_three_treatments_sharp_source_bounded_group_results"]["GlobalOnly"]
  self.assertEqual(z["groups_guaranteed_unchanged"],0)
  self.assertEqual(z["groups_with_uncertain_missing_first_or_last"],1)
 def test_pair_difference_lower_and_upper(self):
  a={"global_cooperation_over_all20_lower":0.2,"global_cooperation_over_all20_upper":0.3}
  b={"global_cooperation_over_all20_lower":0.1,"global_cooperation_over_all20_upper":0.15}
  self.assertAlmostEqual(effect_pair_bounds(a,b)["sharp_lower"],0.05)
  self.assertAlmostEqual(effect_pair_bounds(a,b)["sharp_upper"],0.2)
 def test_three_pre_frozen_pairwise_comparisons(self):
  r=bounded_group_experiment(rows(),1,0)
  self.assertEqual(len(r["pre_frozen_three_treatment_global_group_mean_pair_bounds"]),3)
 def test_real_57_groups_per_treatment_mandatory_by_default(self):
  with self.assertRaisesRegex(ValueError,"UNIVERSE"):bounded_group_experiment(rows())
 def test_missing_source_count_gate(self):
  with self.assertRaisesRegex(ValueError,"64_ACTION_MISSINGNESS"):bounded_group_experiment(rows(),1)
 def test_identity_never_serialized(self):
  r=bounded_group_experiment(rows(),1,0)
  self.assertNotIn("synthetic-",str(r))
  self.assertFalse(r["source_treatment_action_identities_exported"])
 def test_whole_20_rounds_all_one(self):
  r=bounded_group_experiment(rows(),1,0)
  for s in r["original_three_treatments_sharp_source_bounded_group_results"].values():
   self.assertEqual(len(s["original_round_1_to_20_complete_group_sharp_intervals"]),20)
 def test_missing_record_nonnegative(self):
  data=rows();data[0]["game.1.player.contribution"]=None
  r=bounded_group_experiment(data,1,1)
  self.assertEqual(r["original_missing_human_action_slots"],1)
 def test_no_actor_level_person_statistical_claims(self):
  r=bounded_group_experiment(rows(),1,0)
  self.assertNotIn("individual_human",str(r))
 def test_invalid_group_id_fail_closed(self):
  data=rows();data[0]["group_id"]=""
  with self.assertRaises(ValueError):bounded_group_experiment(data,1,0)

if __name__=="__main__":unittest.main()
