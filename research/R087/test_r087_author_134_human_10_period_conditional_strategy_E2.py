#!/usr/bin/env python3
"""28+ synthetic-only source and actor-strategy guards; never download real rows."""
import csv,hashlib,io,pathlib,sys,unittest
from collections import Counter
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r087_author_134_human_10_period_conditional_strategy_E2 import (
 git_sha,ordinal_action,strategy,parse_rows,by_person,cohort_scores,original_aggregate,
 ORIGINAL_COMMIT,DATA_BLOB,TREATMENTS,CATEGORIES)

def fake_rows():
 out=[];person=0
 for treatment,counts,st in (("NoCondInfo",[24,22,22],1),("CondInfo",[22,22,22],4)):
  for sesidx,size in enumerate(counts):
   session=st+sesidx
   for local in range(size):
    person+=1
    for period in range(1,11):
     r={"treatment":treatment,"session":str(session),
       "session_unq":str(session),"subject":str(local+1),
       "subject_unq":str(person),"period":str(period),
       "uc":"50","ccL":"0","ccM":"50","ccH":"100",
       "action":"50"}
     out.append(r)
 return out

def encode(rows):
 f=io.StringIO()
 w=csv.DictWriter(f,fieldnames=list(rows[0]))
 w.writeheader();w.writerows(rows)
 return f.getvalue()

class FixedSourceAndRoles(unittest.TestCase):
 def test_frozen_full_original_commit(self):self.assertEqual(len(ORIGINAL_COMMIT),40)
 def test_csv_git_blob_id(self):self.assertEqual(len(DATA_BLOB),40)
 def test_known_empty_gitblob_hash(self):self.assertEqual(git_sha(b""),"e69de29bb2d1d6434b8b29ae775ad8c2e48c5391")
 def test_gitblob_differs_after_single_byte(self):self.assertNotEqual(git_sha(b"x"),git_sha(b"y"))
 def test_nonbinary_source_denied(self):
  with self.assertRaises(ValueError):git_sha("x")
 def test_zero_action(self):self.assertEqual(ordinal_action("0"),0)
 def test_50_action(self):self.assertEqual(ordinal_action("50.0"),50)
 def test_100_action(self):self.assertEqual(ordinal_action("100"),100)
 def test_other_action_denied(self):
  with self.assertRaises(ValueError):ordinal_action("7")
 def test_missing_action_denied(self):
  with self.assertRaises(ValueError):ordinal_action("")
 def test_nonnum_action_denied(self):
  with self.assertRaises(ValueError):ordinal_action("C")
 def test_missing_header_denied(self):
  with self.assertRaises(ValueError):parse_rows("subject,period\n1,1\n")
 def test_csv_encodes_and_parses(self):
  self.assertEqual(len(parse_rows(encode(fake_rows()))),1340)

class FrozenClasses(unittest.TestCase):
 def test_full_zero_defector(self):self.assertEqual(strategy(0,0,0),"D")
 def test_flat_positive_50(self):self.assertEqual(strategy(50,50,50),"F")
 def test_flat_positive_100(self):self.assertEqual(strategy(100,100,100),"F")
 def test_strictly_conditional(self):self.assertEqual(strategy(0,50,100),"C")
 def test_non_strict_conditional(self):self.assertEqual(strategy(0,0,100),"C")
 def test_nonmonotone_other(self):self.assertEqual(strategy(100,0,100),"O")
 def test_anticoordination_other(self):self.assertEqual(strategy(100,50,0),"O")
 def test_negative_level_denied(self):
  with self.assertRaises(ValueError):strategy(-1,0,100)
 def test_float_type_denied(self):
  with self.assertRaises(ValueError):strategy(0.0,50,100)

class FullSyntheticCohort(unittest.TestCase):
 def test_full134_parses_three_sessions_each(self):
  p,s=by_person(fake_rows());self.assertEqual(len(p),134);self.assertEqual(len(s),6)
 def test_aggregation_two_cohorts(self):
  v=original_aggregate(fake_rows())
  tr=v["original_human_aggregate"]["by_original_information_treatment"]
  self.assertEqual(tr["CondInfo"]["participants"],66)
  self.assertEqual(tr["NoCondInfo"]["participants"],68)
 def test_1340_all_conditional(self):
  v=original_aggregate(fake_rows())["original_human_aggregate"]["all134"]
  self.assertEqual(v["first_strategy_classes"]["C"],134)
  self.assertEqual(v["last_strategy_classes"]["C"],134)
  self.assertEqual(v["identical_strategy_class_all_10_periods"],134)
 def test_treatment_classes_and_time(self):
  v=original_aggregate(fake_rows())["original_human_aggregate"]["all134"]
  self.assertEqual(v["all_ten_period_aggregate_timeline"][0]["people"],134)
  self.assertEqual(len(v["all_ten_period_aggregate_timeline"]),10)
  self.assertEqual(v["mean_actualized_action_final_minus_first"],0)
 def test_direct_conditional_flip_C_to_D(self):
  rows=fake_rows()
  for r in rows:
   if r["subject_unq"]=="1" and r["period"]=="10":
    r["ccL"]=r["ccM"]=r["ccH"]="0"
  v=original_aggregate(rows)["original_human_aggregate"]["all134"]
  self.assertEqual(v["initial_conditional_C_to_final_D"],1)
  self.assertEqual(v["initial_unconditional_D_to_final_C"],0)
 def test_reverse_D_to_C_distinct(self):
  rows=fake_rows()
  for r in rows:
   if r["subject_unq"]=="1" and r["period"]=="1":
    r["ccL"]=r["ccM"]=r["ccH"]="0"
  v=original_aggregate(rows)["original_human_aggregate"]["all134"]
  self.assertEqual(v["initial_unconditional_D_to_final_C"],1)
 def test_action_and_strategy_deltas_are_different(self):
  rows=fake_rows()
  for r in rows:
   if r["period"]=="10":r["action"]="100"
  v=original_aggregate(rows)["original_human_aggregate"]["all134"]
  self.assertEqual(v["mean_actualized_action_final_minus_first"],50)
  self.assertEqual(v["mean_conditional_slope_final_minus_first"],0)
 def test_no_subject_ids_in_results(self):
  r=original_aggregate(fake_rows())
  self.assertNotIn('"subject_unq"',str(r))
  self.assertFalse(r["actor_session_and_row_identifiers_exported"])
 def test_one_period_missing_fails(self):
  rows=[r for r in fake_rows() if not(r["subject_unq"]=="1" and r["period"]=="2")]
  with self.assertRaises(ValueError):by_person(rows)
 def test_duplicate_person_period_fails(self):
  rows=fake_rows();rows.append(dict(rows[0]))
  with self.assertRaises(ValueError):by_person(rows)
 def test_wrong_treatment_fails(self):
  rows=fake_rows();rows[0]["treatment"]="UnknownControl"
  with self.assertRaises(ValueError):by_person(rows)
 def test_missing_actor_id_fails(self):
  rows=fake_rows();rows[0]["subject_unq"]=""
  with self.assertRaises(ValueError):by_person(rows)
 def test_cross_session_identity_reuse_fails(self):
  rows=fake_rows();rows[0]["session_unq"]="4"
  with self.assertRaises(ValueError):by_person(rows)
 def test_out_of_range_period_fails(self):
  rows=fake_rows();rows[0]["period"]="11"
  with self.assertRaises(ValueError):by_person(rows)
 def test_non_numeric_cc_field_denied(self):
  rows=fake_rows();rows[0]["ccM"]="unanswered"
  with self.assertRaises(ValueError):by_person(rows)
 def test_invalid_treatment_cohort_person_count_fails(self):
  rows=fake_rows()
  for r in rows:
   if r["subject_unq"]=="134":r["treatment"]="NoCondInfo"
  with self.assertRaises(ValueError):by_person(rows)

if __name__=="__main__":unittest.main()
