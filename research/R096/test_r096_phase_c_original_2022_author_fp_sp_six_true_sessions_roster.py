#!/usr/bin/env python3
"""R096 synthetic only: 6 real session metadata, 100 rounds fixed vs shuffled."""
import csv,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r096_phase_c_original_2022_author_fp_sp_six_true_sessions_roster import (
 SOURCE_SHA,EXPECTED_ROWS,EXPECTED_PEOPLE,real_anon_session_universe)
def fixture(name="fix.csv",weird=None):
 f=io.StringIO();w=csv.writer(f)
 w.writerow(["","round","session","player","opponent","action_player","action_opponent"])
 for sess in range(6):
  for person in range(4):
   for t in range(1,101):
    opp=person^1 if name=="fix.csv" else (person+(t%3)+1)%4
    if opp==person:opp=(person+1)%4
    row=["",str(t),f"SECRET_SESSION_{sess}",f"SECRET_PERSON_{person}",
         f"SECRET_PERSON_{opp}","PRIVATE_REAL_ACTION","PRIVATE_OPP_ACTION"]
    if weird and weird(sess,person,t,row):pass
    w.writerow(row)
 return f.getvalue().encode()
class SyntheticOriginalSessionRoster(unittest.TestCase):
 def test_source_full_SHA_pins(self):
  self.assertEqual(SOURCE_SHA["fix.csv"],"c2adc0d68dbc15c4f5ec5f0eb9a05a988cc049a9c086b82f796521a642b6eae9")
  self.assertEqual(SOURCE_SHA["rand.csv"],"bc2999d6ad44c60f2b93361eb46b75614b1f600967ae061c76ae51184a80848a")
 def test_expected_main_source_real_persons(self):self.assertEqual(sum(EXPECTED_PEOPLE.values()),188)
 def test_expected_author_rows(self):self.assertEqual(sum(EXPECTED_ROWS.values()),18800)
 def test_6_sessions_24participants_fixed(self):
  r=real_anon_session_universe(fixture("fix.csv"),"fix.csv",2400,24)
  self.assertEqual(r["true_original_source_experiment_sessions"],6)
  self.assertEqual(r["true_source_distinct_actor_IDs_within_original_session"],24)
 def test_stable_fixed_peers_zero_changers(self):
  r=real_anon_session_universe(fixture("fix.csv"),"fix.csv",2400,24)
  self.assertEqual(r["source_distinct_persons_with_partner_changes_over_100_rounds"],0)
 def test_random_peers_change(self):
  r=real_anon_session_universe(fixture("rand.csv"),"rand.csv",2400,24)
  self.assertGreater(r["source_distinct_persons_with_partner_changes_over_100_rounds"],0)
 def test_sorted_real_session_size(self):
  r=real_anon_session_universe(fixture("fix.csv"),"fix.csv",2400,24)
  self.assertEqual(r["original_six_true_session_person_counts_sorted"],[4]*6)
 def test_no_private_identifier_print(self):
  s=str(real_anon_session_universe(fixture("fix.csv"),"fix.csv",2400,24))
  for x in ("SECRET_SESSION","SECRET_PERSON","PRIVATE_REAL_ACTION"):self.assertNotIn(x,s)
 def test_100_actual_rounds(self):
  r=real_anon_session_universe(fixture("fix.csv"),"fix.csv",2400,24)
  self.assertTrue(r["all_original_persons_exactly_100_distinct_rounds"])
 def test_no_cooperation_values_examined(self):
  r=real_anon_session_universe(fixture("fix.csv"),"fix.csv",2400,24)
  self.assertFalse(r["source_original_cooperation_action_or_payoff_values_examined"])
 def test_invalid_session_blank(self):
  def alter(s,p,t,r):
   if s==0 and p==0 and t==1:r[2]=""
  with self.assertRaises(ValueError):real_anon_session_universe(fixture(weird=alter),"fix.csv",2400,24)
 def test_invalid_player_blank(self):
  def alter(s,p,t,r):
   if s==0 and p==0 and t==1:r[3]=""
  with self.assertRaises(ValueError):real_anon_session_universe(fixture(weird=alter),"fix.csv",2400,24)
 def test_round_out_of_range(self):
  def alter(s,p,t,r):
   if s==0 and p==0 and t==1:r[1]="200"
  with self.assertRaises(ValueError):real_anon_session_universe(fixture(weird=alter),"fix.csv",2400,24)
 def test_round_duplicate(self):
  def alter(s,p,t,r):
   if s==0 and p==0 and t==2:r[1]="1"
  with self.assertRaises(ValueError):real_anon_session_universe(fixture(weird=alter),"fix.csv",2400,24)
 def test_missing_round(self):
  def alter(s,p,t,r):
   if s==0 and p==0 and t==2:r[1]=""
  with self.assertRaises(ValueError):real_anon_session_universe(fixture(weird=alter),"fix.csv",2400,24)
 def test_bad_opponent_blank(self):
  def alter(s,p,t,r):
   if s==0 and p==0 and t==2:r[4]=""
  with self.assertRaises(ValueError):real_anon_session_universe(fixture(weird=alter),"fix.csv",2400,24)
 def test_changed_fp_peer_fails(self):
  def alter(s,p,t,r):
   if s==0 and p==0 and t==2:r[4]="SECRET_PERSON_2"
  with self.assertRaises(ValueError):real_anon_session_universe(fixture(weird=alter),"fix.csv",2400,24)
 def test_unshuffled_SP_fails(self):
  with self.assertRaises(ValueError):real_anon_session_universe(fixture("fix.csv"),"rand.csv",2400,24)
 def test_wrong_actor_count_fails(self):
  with self.assertRaises(ValueError):real_anon_session_universe(fixture("fix.csv"),"fix.csv",2400,92)
 def test_wrong_row_denominator_fails(self):
  with self.assertRaises(ValueError):real_anon_session_universe(fixture("fix.csv"),"fix.csv",9200,24)
 def test_nonaccepted_source_file(self):
  with self.assertRaises(ValueError):real_anon_session_universe(fixture(),"external.csv",2400,24)
if __name__=="__main__":unittest.main()
