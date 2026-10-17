#!/usr/bin/env python3
import csv,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r096_phase_d2_original_author_action_codebook_classes_no_scores import safe_class,anonymous_action_codes
from r096_phase_c_original_2022_author_fp_sp_six_true_sessions_roster import EXPECTED_ROWS
def fake(n=9200):
 s=io.StringIO();w=csv.writer(s);w.writerow(["action_player","action_opponent","player","session"])
 for i in range(n):w.writerow(["C" if i%2 else "D","D" if i%2 else "C",f"SECRET_ACTOR_{i}",f"SECRET_SESSION_{i%6}"])
 return s.getvalue().encode()
class SourceLiteralTests(unittest.TestCase):
 def test_C_safe(self):self.assertEqual(safe_class("C"),"C")
 def test_D_safe(self):self.assertEqual(safe_class("D"),"D")
 def test_numeric_safe(self):self.assertEqual(safe_class("1"),"1")
 def test_empty_marker(self):self.assertEqual(safe_class(""),"EMPTY_SOURCE_ACTION")
 def test_unknown_personal_token_redacted(self):self.assertEqual(safe_class("PRIVATE_ACTOR_999"),"REDACTED_OTHER")
 def test_original_source_rows(self):self.assertEqual(anonymous_action_codes(fake(),"fix.csv")["original_source_rows"],9200)
 def test_two_source_classes(self):
  r=anonymous_action_codes(fake(),"fix.csv")
  self.assertEqual(r["literal_player_source_action_code_classes"]["C"],4600)
  self.assertEqual(r["literal_player_source_action_code_classes"]["D"],4600)
 def test_no_person_ID_leaks(self):
  z=str(anonymous_action_codes(fake(),"fix.csv"))
  self.assertNotIn("SECRET_ACTOR",z)
  self.assertNotIn("SECRET_SESSION",z)
 def test_no_models_scored(self):self.assertFalse(anonymous_action_codes(fake(),"fix.csv")["original_human_binary_models_scored"])
 def test_wrong_row_count_denied(self):
  with self.assertRaises(ValueError):anonymous_action_codes(fake(2),"fix.csv")
 def test_unexpected_column_denied(self):
  with self.assertRaises(ValueError):anonymous_action_codes(fake().replace(b"action_player",b"other",1),"fix.csv")
if __name__=="__main__":unittest.main()
