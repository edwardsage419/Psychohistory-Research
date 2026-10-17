#!/usr/bin/env python3
import csv,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r093_phase_b_author_csv_nonbehavior_actor_missing_and_labels import (
 author_code,field_kind,round_kind,anonymous_original_metadata)
FIELDS=["participant_id","player_alive","group_avg_contribution","player_contribution","round_number","treatment","gender","age"]
def fake(rows=None):
 if rows is None:
  rows=[
   ["SECRET-ACTOR-A","1","9999999","8888888","1","PGG100","GENDER","35"],
   ["","0","9999999","8888888","2","PGG100","GENDER","35"],
   ["SECRET-ACTOR-A","1","9999999","8888888","2","PGG100","GENDER","35"]]
 f=io.StringIO();w=csv.writer(f);w.writerow(FIELDS);w.writerows(rows);return f.getvalue().encode()
class SourceCodebook(unittest.TestCase):
 def test_safe_treatment(self):self.assertEqual(author_code("PGG1000"),"PGG1000")
 def test_unexpected_email_redacted(self):self.assertEqual(author_code("private@example.com"),"REDACTED_UNRECOGNIZED_TREATMENT")
 def test_empty_treatment(self):self.assertEqual(author_code(""),"MISSING_TREATMENT")
 def test_alive_1(self):self.assertEqual(field_kind("1"),"1")
 def test_alive_missing(self):self.assertEqual(field_kind(""),"EMPTY")
 def test_alive_unknown_sanitized(self):self.assertEqual(field_kind("10"),"OTHER_NONBINARY")
 def test_round1(self):self.assertEqual(round_kind("1"),"1")
 def test_round14(self):self.assertEqual(round_kind("14"),"14")
 def test_round15_redacted(self):self.assertEqual(round_kind("15"),"OUTSIDE_1_TO_14_OR_EMPTY")
 def test_source_missing_person_reported(self):
  a=anonymous_original_metadata(fake())
  self.assertEqual(a["source_missing_individual_ID_rows_by_publisher_treatment"]["PGG100"],1)
 def test_source_rows_complete_denominator(self):
  a=anonymous_original_metadata(fake());self.assertEqual(a["source_original_person_round_rows"],3)
 def test_person_and_contribution_private(self):
  s=str(anonymous_original_metadata(fake()))
  for token in ("SECRET-ACTOR","9999999","8888888","GENDER"):self.assertNotIn(token,s)
 def test_action_never_examined(self):self.assertFalse(anonymous_original_metadata(fake())["contribution_column_numeric_values_examined"])
 def test_treatment_frequencies(self):self.assertEqual(anonymous_original_metadata(fake())["safe_publisher_treatment_label_row_counts"]["PGG100"],3)
 def test_duplicate_original_key_audited(self):
  rows=[
   ["PERSON-X","1","777","555","1","PGG100","g","10"],
   ["PERSON-X","1","777","555","1","PGG100","g","10"]]
  self.assertEqual(anonymous_original_metadata(fake(rows))["source_fully_sanitized_duplicate_person_round_keys"],1)
 def test_invalid_header(self):
  with self.assertRaises(ValueError):anonymous_original_metadata(fake().replace(b"participant_id",b"invalid column",1))
 def test_invalid_rowwidth(self):
  with self.assertRaises(ValueError):anonymous_original_metadata(fake()+b"hi,there\n")
if __name__=="__main__":unittest.main()
