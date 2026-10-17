#!/usr/bin/env python3
"""R090 synthetic-only roster and publisher MD5 privacy tests."""
import csv,hashlib,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r090_independent_climate_clubs_original_roster_source_gate import (
 OFFICIAL_MD5,URL,RECORD,REQUIRED,TREATMENTS,check_url,check_source_bytes,
 original_source_roster, int_positive,bool_indicator)

def sample(participants=6,rounds=5):
 a=[]
 for t in range(1,rounds+1):
  for i in range(participants):
   d={k:"" for k in REQUIRED}
   d.update({"participant.id_in_session":str(i+1),
   "participant.code":f"opaque-private-actor{i}","participant._round_number":str(t),
   "player.id_in_group":str(i+1),"player.automatic_decision":"0",
   "player.contribution":"__PRIVATE_ACTION_NEVER_READ_OR_EXPORT_99999",
   "player.endowment":"__PRIVATE_ENDOWMENT_NEVER_READ_99999",
   "player.timeout_contr":"0","group.id_in_subsession":"1",
   "subsession.round_number":str(t),"session.code":"synthetic-private-session-secret",
   "group":"6A","treatment":"T1"})
   a.append(d)
 return a

def fake_csv(rows):
 f=io.StringIO()
 extra=[f"metadata_column_{i}" for i in range(27-len(REQUIRED))]
 names=list(REQUIRED)+extra
 w=csv.DictWriter(f,fieldnames=names)
 w.writeheader()
 for a in rows:w.writerow(a)
 return f.getvalue().encode()

class SourceChecks(unittest.TestCase):
 def test_publisher_original_md5(self):self.assertEqual(OFFICIAL_MD5,"56931608b717aea06105ad10a58ff937")
 def test_publisher_fixed_record(self):self.assertEqual(RECORD,17610157)
 def test_official_url(self):self.assertTrue(check_url(URL))
 def test_unofficial_domain(self):
  with self.assertRaises(ValueError):check_url(URL.replace("zenodo.org","zenodo.org.evil"))
 def test_other_record(self):
  with self.assertRaises(ValueError):check_url(URL.replace("17610157","1"))
 def test_http_not_allowed(self):
  with self.assertRaises(ValueError):check_url(URL.replace("https","http",1))
 def test_positive_round_1(self):self.assertEqual(int_positive("1","bad"),1)
 def test_period0_denied(self):
  with self.assertRaises(ValueError):int_positive("0","bad")
 def test_negative_round_denied(self):
  with self.assertRaises(ValueError):int_positive("-1","bad")
 def test_auto_1(self):self.assertEqual(bool_indicator("1"),1)
 def test_auto_0(self):self.assertEqual(bool_indicator("0"),0)
 def test_auto_NA(self):self.assertIsNone(bool_indicator("NA"))
 def test_auto_not_numeric(self):
  with self.assertRaises(ValueError):bool_indicator("private")
 def test_md5_mismatch_before_parsing(self):
  with self.assertRaisesRegex(ValueError,"MD5_MISMATCH"):check_source_bytes(fake_csv(sample()),OFFICIAL_MD5)
 def test_real_2700_row_gate(self):
  b=fake_csv(sample())
  with self.assertRaisesRegex(ValueError,"PUBLISHED_ROWS"):check_source_bytes(b,hashlib.md5(b).hexdigest())
 def test_short_blob_empty_gate(self):
  with self.assertRaises(ValueError):check_source_bytes(b"",hashlib.md5(b"").hexdigest())

class StructureChecks(unittest.TestCase):
 def test_synthetic_6_person_5_round_one_group(self):
  v=original_source_roster(sample(),False)
  self.assertEqual(v["original_unique_persons_within_session"],6)
  self.assertEqual(v["original_distinct_group_round_keys"],5)
  self.assertEqual(v["original_group_roster_stability_summary"]["stable_membership"],1)
 def test_group_size_six(self):
  s=original_source_roster(sample(),False)
  self.assertEqual(s["group_round_size_distribution"]["6"],5)
 def test_rounds_exact(self):
  s=original_source_roster(sample(),False)
  self.assertEqual(s["rounds_observed_sorted"],[1,2,3,4,5])
 def test_no_action_information_leak(self):
  s=original_source_roster(sample(),False)
  self.assertNotIn("99999",str(s))
  self.assertNotIn("secret",str(s))
  self.assertTrue(s["no_actor_or_group_id_values_exported"])
 def test_nonmatching_rounds_denied(self):
  r=sample();r[0]["subsession.round_number"]="4"
  with self.assertRaises(ValueError):original_source_roster(r,False)
 def test_duplicate_person_round_denied(self):
  r=sample();r.append(dict(r[0]))
  with self.assertRaisesRegex(ValueError,"DUPLICATE_PERSON"):original_source_roster(r,False)
 def test_group_treatment_conflict_denied(self):
  r=sample();r[0]["treatment"]="T2"
  with self.assertRaisesRegex(ValueError,"PERSON_CHANGES_TREATMENT"):original_source_roster(r,False)
 def test_missing_person_denied(self):
  r=sample();r[0]["participant.code"]=""
  with self.assertRaisesRegex(ValueError,"EMPTY_PERSON"):original_source_roster(r,False)
 def test_missing_group_denied(self):
  r=sample();r[0]["group.id_in_subsession"]=""
  with self.assertRaises(ValueError):original_source_roster(r,False)
 def test_member_migrates_source_marks_change(self):
  r=sample()
  for a in r:
   if a["participant.code"]=="opaque-private-actor0" and a["participant._round_number"]=="5":
    a["group.id_in_subsession"]="2"
  s=original_source_roster(r,False)
  self.assertEqual(s["original_group_roster_stability_summary"]["changed_membership"],1)
 def test_auto_flag_count_only(self):
  r=sample();r[0]["player.automatic_decision"]="1"
  s=original_source_roster(r,False)
  self.assertEqual(s["by_original_treatment"]["T1"]["automatic_decision_one"],1)
 def test_timeout_flag_count_only(self):
  r=sample();r[0]["player.timeout_contr"]="1"
  s=original_source_roster(r,False)
  self.assertEqual(s["by_original_treatment"]["T1"]["contribution_timeout_one"],1)
 def test_unknown_treatment_denied(self):
  r=sample();r[0]["treatment"]="Other"
  with self.assertRaises(ValueError):original_source_roster(r,False)
 def test_2700_strict_universe_gate(self):
  with self.assertRaises(ValueError):original_source_roster(sample())
if __name__=="__main__":unittest.main()
