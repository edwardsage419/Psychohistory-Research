#!/usr/bin/env python3
"""R088 synthetic group roster, threshold, all-round result and Git source tests."""
import csv,hashlib,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r088_original_171_groups_multilevel_global_cooperation_E2 import (
 blob_hash,parse_csv,one_group,analyze_rows,ACTIONS,PERIODS,CONDITIONS,
 CSV_BLOB,EXCLUDE_BLOB,ANALYSIS_BLOB,COMMIT)

def fake_records():
 rows=[]
 for cond in CONDITIONS:
  for p in range(6):
   r={"group_id":f"synthetic-{cond}","subgroup_id":f"synthetic-{cond}-{'a' if p<3 else 'b'}",
      "condition":cond}
   for t in PERIODS:
    decision=("global" if p<4 else "self") if cond=="GlobalOnly" else (
      "global" if p<3 else "local" if p==3 else "other" if p==4 else "self")
    r[f"game.{t}.player.contribution"]=decision
   rows.append(r)
 return rows

def encoded(rows):
 s=io.StringIO();w=csv.DictWriter(s,fieldnames=list(rows[0]))
 w.writeheader();w.writerows(rows)
 return s.getvalue().encode("utf-8")

class TestSource(unittest.TestCase):
 def test_original_sha_40hex(self):
  for x in (CSV_BLOB,EXCLUDE_BLOB,ANALYSIS_BLOB,COMMIT):self.assertEqual(len(x),40)
 def test_empty_git_blob_known(self):
  self.assertEqual(blob_hash(b""),"e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")
 def test_changed_one_byte_changes_blob(self):
  self.assertNotEqual(blob_hash(b"source"),blob_hash(b"sourcE"))
 def test_blob_not_string(self):
  with self.assertRaises(ValueError):blob_hash("bytes")
 def test_parse_author_schema(self):
  self.assertEqual(len(parse_csv(encoded(fake_records()))),18)
 def test_csv_header_missing(self):
  with self.assertRaisesRegex(ValueError,"REQUIRED_COLS"):parse_csv(b"group_id,condition\nid,GlobalOnly\n")
 def test_20_round_columns(self):
  x=fake_records()[0];self.assertTrue(all(f"game.{t}.player.contribution" in x for t in PERIODS))
 def test_all_expected_actions(self):
  self.assertEqual(set(ACTIONS),{"global","local","other","self"})

class TestOneCompleteHumanGroup(unittest.TestCase):
 def test_six_players_and_two_subgroups(self):
  cond,rs=one_group(fake_records()[:6])
  self.assertEqual(cond,"GlobalOnly");self.assertEqual(len(rs),20)
 def test_threshold_four_pass(self):
  _,r=one_group(fake_records()[:6]);self.assertEqual(r[0]["global"],4)
  self.assertEqual(r[0]["global_threshold_met"],1)
 def test_threshold_three_fails(self):
  rows=fake_records()[:6]
  rows[3]["game.1.player.contribution"]="self"
  _,r=one_group(rows)
  self.assertEqual(r[0]["global_threshold_met"],0)
  self.assertEqual(r[0]["global_threshold_almost_met_at_3"],1)
 def test_zero_global(self):
  rows=fake_records()[:6]
  for x in rows:x["game.1.player.contribution"]="self"
  _,r=one_group(rows);self.assertEqual(r[0]["global_zero"],1)
 def test_all_global(self):
  rows=fake_records()[:6]
  for x in rows:x["game.1.player.contribution"]="global"
  _,r=one_group(rows);self.assertEqual(r[0]["global_all_six"],1)
 def test_local_in_globalonly_not_permitted(self):
  rows=fake_records()[:6]
  rows[0]["game.2.player.contribution"]="local"
  with self.assertRaisesRegex(ValueError,"UNAVAILABLE_LOCAL"):one_group(rows)
 def test_missing_action_fails(self):
  rows=fake_records()[:6];rows[0]["game.20.player.contribution"]=""
  with self.assertRaisesRegex(ValueError,"ACTION_NULL"):one_group(rows)
 def test_missing_subgroup_fails(self):
  rows=fake_records()[:6];rows[0]["subgroup_id"]=""
  with self.assertRaisesRegex(ValueError,"SUBGROUPS"):one_group(rows)
 def test_improper_subgroup_split_fails(self):
  rows=fake_records()[:6];rows[0]["subgroup_id"]="new-one"
  with self.assertRaisesRegex(ValueError,"SUBGROUPS"):one_group(rows)
 def test_short_group_fails(self):
  with self.assertRaisesRegex(ValueError,"NOT_SIX"):one_group(fake_records()[:5])
 def test_mixed_condition_in_one_group(self):
  rows=fake_records()[:6];rows[0]["condition"]="Balanced"
  with self.assertRaisesRegex(ValueError,"INCONSISTENT"):one_group(rows)
 def test_local_other_distinct(self):
  _,rows=one_group(fake_records()[6:12])
  self.assertEqual(rows[0]["global"],3)
  self.assertEqual(rows[0]["local"],1)
  self.assertEqual(rows[0]["other"],1)
  self.assertEqual(rows[0]["self"],1)

class TestWholeExperiment(unittest.TestCase):
 def test_three_equal_conditions(self):
  r=analyze_rows(fake_records(),expected_groups_per_arm=1)
  self.assertEqual(r["number_of_source_groups"],3)
  self.assertEqual(r["source_human_participant_rows"],18)
  self.assertEqual(r["subject_round_actions_scored"],360)
 def test_globalonly_rate(self):
  r=analyze_rows(fake_records(),expected_groups_per_arm=1)
  self.assertAlmostEqual(r["condition_aggregate"]["GlobalOnly"]["global_cooperation_group_equal_all20_mean"],4/6)
 def test_balanced_has_local(self):
  r=analyze_rows(fake_records(),expected_groups_per_arm=1)
  self.assertAlmostEqual(r["condition_aggregate"]["Balanced"]["mean_fraction_investing_local_either_group_all20"],2/6)
 def test_group_threshold_all20(self):
  r=analyze_rows(fake_records(),expected_groups_per_arm=1)
  self.assertEqual(r["condition_aggregate"]["GlobalOnly"]["global_threshold_met_group_rounds_sum"],20)
  self.assertEqual(r["condition_aggregate"]["Balanced"]["global_threshold_met_group_rounds_sum"],0)
 def test_exact_20_rounds(self):
  r=analyze_rows(fake_records(),expected_groups_per_arm=1)
  self.assertEqual(len(r["condition_aggregate"]["GlobalBoost"]["original_twenty_rounds_complete_group_aggregate"]),20)
 def test_first_last_delta(self):
  rows=fake_records()
  for x in rows[:6]:
   if x["game.20.player.contribution"]=="self":x["game.20.player.contribution"]="global"
  r=analyze_rows(rows,expected_groups_per_arm=1)
  self.assertAlmostEqual(r["condition_aggregate"]["GlobalOnly"]["global_cooperation_first_last_group_equal_delta"],1/3)
 def test_zero_delta_groups(self):
  r=analyze_rows(fake_records(),expected_groups_per_arm=1)
  for x in r["condition_aggregate"].values():self.assertEqual(x["groups_same_global_first_to_last"],1)
 def test_group_up_down_zero_conservation(self):
  r=analyze_rows(fake_records(),expected_groups_per_arm=1)
  for x in r["condition_aggregate"].values():
   self.assertEqual(x["groups_more_global_first_to_last"]+x["groups_less_global_first_to_last"]+x["groups_same_global_first_to_last"],1)
 def test_fixed_pairwise_contrasts(self):
  r=analyze_rows(fake_records(),expected_groups_per_arm=1)
  self.assertEqual(set(r["frozen_source_group_mean_pair_contrasts"]),{
   "GlobalOnly_minus_Balanced","GlobalBoost_minus_Balanced","GlobalBoost_minus_GlobalOnly"})
 def test_real_57_per_arm_enforced_by_default(self):
  with self.assertRaisesRegex(ValueError,"GROUP_UNIVERSE"):analyze_rows(fake_records())
 def test_missing_one_player_does_not_silently_drop(self):
  with self.assertRaises(ValueError):analyze_rows(fake_records()[1:],expected_groups_per_arm=1)
 def test_group_id_missing(self):
  rows=fake_records();rows[0]["group_id"]=""
  with self.assertRaisesRegex(ValueError,"GROUP_ID_MISSING"):analyze_rows(rows,1)
 def test_group_ids_not_exported(self):
  r=analyze_rows(fake_records(),expected_groups_per_arm=1)
  self.assertNotIn("synthetic-",str(r))
 def test_no_person_record_in_results(self):
  r=analyze_rows(fake_records(),expected_groups_per_arm=1)
  self.assertNotIn("subgroup_id",str(r))
  self.assertNotIn("group_id",str(r))
 def test_no_late_round_data_loss(self):
  rows=fake_records();rows[0]["game.20.player.contribution"]="None"
  with self.assertRaisesRegex(ValueError,"ACTION_NULL"):analyze_rows(rows,1)

if __name__=="__main__":unittest.main()
