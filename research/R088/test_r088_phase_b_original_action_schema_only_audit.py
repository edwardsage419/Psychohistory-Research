import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r088_phase_b_original_action_schema_only_audit import category,schema_counts
from r088_original_171_groups_multilevel_global_cooperation_E2 import CONDITIONS,PERIODS

def synthetic_source():
 out=[]
 for cond in CONDITIONS:
  for i in range(342):
   r={"condition":cond}
   for p in PERIODS:r[f"game.{p}.player.contribution"]="global"
   out.append(r)
 return out

class SourceSchemaOnly(unittest.TestCase):
 def test_valid_global(self):self.assertEqual(category("global"),"EXACT")
 def test_valid_local(self):self.assertEqual(category("local"),"EXACT")
 def test_valid_other(self):self.assertEqual(category("other"),"EXACT")
 def test_valid_self(self):self.assertEqual(category("self"),"EXACT")
 def test_space_trim_detect(self):self.assertEqual(category(" global "),"CASE_OR_SPACE_ONLY")
 def test_case_lower_detect(self):self.assertEqual(category("GLOBAL"),"CASE_OR_SPACE_ONLY")
 def test_blank_missing(self):self.assertEqual(category(""),"EMPTY_MISSING")
 def test_none_missing(self):self.assertEqual(category(None),"EMPTY_MISSING")
 def test_unknown_redacted(self):self.assertEqual(category("synthetic-private-ID999"),"UNRECOGNIZED_OTHER")
 def test_alias_kept_not_silently_self(self):self.assertEqual(category("kept"),"DECLARED_COMMON_NON_EQUIVALENT")
 def test_synthetic_complete1026x20(self):
  s=schema_counts(synthetic_source())
  self.assertEqual(s["total_person_round_slots_seen"],20520)
  self.assertTrue(s["all_actions_exact_frozen_schema"])
 def test_synthetic_one_dirty_action(self):
  rows=synthetic_source()
  rows[0]["game.1.player.contribution"]=" LOCAL "
  s=schema_counts(rows)
  self.assertTrue(s["safe_format_only_CI_repairable_case_or_space_without_any_other_error"])
  self.assertEqual(s["categories"]["CASE_OR_SPACE_ONLY"],1)
 def test_synthetic_unknown_does_not_echo_value(self):
  rows=synthetic_source()
  rows[0]["game.1.player.contribution"]="synthetic-private-ID999"
  s=schema_counts(rows)
  self.assertNotIn("999",str(s))
 def test_empty_not_repairable(self):
  rows=synthetic_source()
  rows[0]["game.1.player.contribution"]=""
  s=schema_counts(rows)
  self.assertFalse(s["safe_format_only_CI_repairable_case_or_space_without_any_other_error"])
  self.assertEqual(s["categories"]["EMPTY_MISSING"],1)
 def test_correct_per_cond_count(self):
  s=schema_counts(synthetic_source())
  for x in CONDITIONS:self.assertEqual(s["by_author_condition"][x]["EXACT"],6840)
 def test_source_missing_person_fails(self):
  with self.assertRaises(ValueError):schema_counts(synthetic_source()[:-1])
 def test_alias_safe_whitelist(self):
  rows=synthetic_source();rows[0]["game.1.player.contribution"]="kept"
  s=schema_counts(rows)
  self.assertEqual(s["safe_known_other_alias_counts"]["kept"],1)

if __name__=="__main__":unittest.main()
