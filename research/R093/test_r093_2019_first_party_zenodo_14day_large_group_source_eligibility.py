#!/usr/bin/env python3
"""R093 synthetic privacy, source MD5, official URL, age/role isolation."""
import csv,hashlib,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r093_2019_first_party_zenodo_14day_large_group_source_eligibility import (
 FILE,RECORD,PUBLISHER_MD5,MAX_BYTES,verify_url,identity,structured_roster,URL,source_round,source_alive)
COLS=["participant_id","player_alive","group_avg_contribution","player_contribution","round_number","treatment","gender","age"]
def mock_csv(n=3):
 f=io.StringIO();w=csv.writer(f);w.writerow(COLS)
 for i in range(n):
  w.writerow([f"PRIVATE_PERSON_{i}",1,99988777,99989999,i%14+1,"PGG100","SENSITIVE_GENDER",45])
 return f.getvalue().encode()
class SourceTests(unittest.TestCase):
 def test_official_record(self):self.assertEqual(RECORD,"2590686")
 def test_official_md5(self):self.assertEqual(PUBLISHER_MD5,"626c61c2c18a114a5b92a7d2b7e46558")
 def test_expected_source_file(self):self.assertEqual(FILE,"2017A2ECOCOOPANSA01ONL0000ESPMAD.csv")
 def test_official_url(self):self.assertTrue(verify_url(URL))
 def test_other_site_fails(self):
  with self.assertRaises(ValueError):verify_url(URL.replace("zenodo.org","zenodo.org.evil"))
 def test_http_fails(self):
  with self.assertRaises(ValueError):verify_url(URL.replace("https","http",1))
 def test_other_version_fails(self):
  with self.assertRaises(ValueError):verify_url(URL.replace(RECORD,"1"))
 def test_source_MD5_mismatch_fails(self):
  with self.assertRaises(ValueError):identity(mock_csv())
 def test_source_empty_fails(self):
  with self.assertRaises(ValueError):identity(b"",hashlib.md5(b"").hexdigest())
 def test_source_oversize_fails(self):
  with self.assertRaises(ValueError):identity(b"0"*(MAX_BYTES+1),hashlib.md5(b"0"*(MAX_BYTES+1)).hexdigest())
 def test_synthetic_MD5_sha(self):
  b=mock_csv();r=identity(b,hashlib.md5(b).hexdigest())
  self.assertEqual(r["original_full_file_SHA256"],hashlib.sha256(b).hexdigest())
 def test_round1(self):self.assertEqual(source_round("1"),1)
 def test_round14(self):self.assertEqual(source_round("14"),14)
 def test_round15_invalid(self):
  with self.assertRaises(ValueError):source_round("15")
 def test_round0_invalid(self):
  with self.assertRaises(ValueError):source_round("0")
 def test_alive1(self):self.assertEqual(source_alive("1"),"1")
 def test_alive0(self):self.assertEqual(source_alive("0"),"0")
 def test_invalid_alive_denied(self):
  with self.assertRaises(ValueError):source_alive("unknown")
 def test_source_roster_count(self):
  r=structured_roster(mock_csv())
  self.assertEqual(r["original_source_actor_round_rows"],3)
  self.assertEqual(r["source_anonymized_experiment_metadata"]["PGG100"]["distinct_original_source_person_id_codes"],3)
 def test_private_source_data_never_exported(self):
  r=str(structured_roster(mock_csv()))
  self.assertNotIn("PRIVATE_PERSON",r)
  self.assertNotIn("99988777",r)
  self.assertNotIn("99989999",r)
  self.assertNotIn("SENSITIVE_GENDER",r)
 def test_publisher_data_values_unexamined_flag(self):
  r=structured_roster(mock_csv())
  self.assertFalse(r["source_contribution_or_original_group_mean_values_examined"])
 def test_source_duplicate_person_time_count(self):
  f=io.StringIO();w=csv.writer(f);w.writerow(COLS)
  row=["PERSON-KEEP-PRIVATE","1","123","456","1","PGG100","x","25"]
  w.writerow(row);w.writerow(row)
  r=structured_roster(f.getvalue().encode())
  self.assertEqual(r["duplicate_original_treatment_person_round_keys"],1)
 def test_unexpected_column_denied(self):
  b=mock_csv().replace(b"participant_id",b"bad name",1)
  with self.assertRaises(ValueError):structured_roster(b)
 def test_malformed_utf8_denied(self):
  with self.assertRaises(ValueError):structured_roster(b"\xff\x80\x81")
 def test_malformed_rowwidth_denied(self):
  with self.assertRaises(ValueError):structured_roster(mock_csv()+b",,\n")
 def test_unknown_treatment_redacted_denied(self):
  b=mock_csv().replace(b"PGG100",b"somebody@example.com")
  with self.assertRaises(ValueError):structured_roster(b)
if __name__=="__main__":unittest.main()
