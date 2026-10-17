#!/usr/bin/env python3
"""R094 strict synthetic checksum, original secondary source privacy tests."""
import csv,hashlib,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r094_zhu_nishi_2015_binary_network_original_sessions_secondary_source_gate import (
 MD5,RECORD,FILE,URL,LIMIT,source_url_valid,full_publisher_source_identity,schema_without_any_values)
def fake(n=102):
 buf=io.StringIO();writer=csv.writer(buf)
 writer.writerow(["SESSION_ID","subject_id","round","binary_cooperate","decision_time"])
 for t in range(n):
  writer.writerow([f"PRIVATE_SESSION_{t}",f"PRIVATE_ID_{t}",1,999999,777777])
 return buf.getvalue().encode("utf-8")
class OnlySourceSchema(unittest.TestCase):
 def test_original_2026_record(self):self.assertEqual(RECORD,"19544006")
 def test_author_MD5_web_publisher(self):self.assertEqual(MD5,"85db2536b5be1cd50266900e61590d5a")
 def test_filename(self):self.assertEqual(FILE,"individual_data.csv")
 def test_Zenodo_official_link_allowed(self):self.assertTrue(source_url_valid(URL))
 def test_source_http_denied(self):
  with self.assertRaises(ValueError):source_url_valid(URL.replace("https","http",1))
 def test_source_wrong_host_denied(self):
  with self.assertRaises(ValueError):source_url_valid(URL.replace("zenodo.org","zenodo.org.evil"))
 def test_source_wrong_file_denied(self):
  with self.assertRaises(ValueError):source_url_valid(URL.replace(FILE,"different.csv"))
 def test_source_wrong_record_denied(self):
  with self.assertRaises(ValueError):source_url_valid(URL.replace(RECORD,"100"))
 def test_source_empty_rejected(self):
  with self.assertRaises(ValueError):full_publisher_source_identity(b"",hashlib.md5(b"").hexdigest())
 def test_source_author_MD5_mismatch_rejected(self):
  with self.assertRaises(ValueError):full_publisher_source_identity(fake())
 def test_source_oversize_rejected(self):
  z=b"a"*(LIMIT+1)
  with self.assertRaises(ValueError):full_publisher_source_identity(z,hashlib.md5(z).hexdigest())
 def test_synthetic_entire_SHA(self):
  b=fake();z=full_publisher_source_identity(b,hashlib.md5(b).hexdigest())
  self.assertEqual(z["independently_computed_raw_SHA256"],hashlib.sha256(b).hexdigest())
 def test_102_safe_rows(self):
  z=schema_without_any_values(fake());self.assertEqual(z["original_data_row_count"],102)
 def test_safe_col_headers(self):
  z=schema_without_any_values(fake());self.assertIn("SESSION_ID",z["original_publisher_safe_column_names"])
 def test_never_export_private_actor(self):
  z=str(schema_without_any_values(fake()))
  for v in ("PRIVATE_SESSION","PRIVATE_ID","999999","777777"):self.assertNotIn(v,z)
 def test_no_original_coop_decision_data_examined(self):
  self.assertFalse(schema_without_any_values(fake())["original_action_cooperation_time_network_values_examined"])
 def test_reject_duplicate_headers(self):
  b=fake().replace(b"subject_id",b"SESSION_ID",1)
  with self.assertRaises(ValueError):schema_without_any_values(b)
 def test_reject_unsafe_headers(self):
  b=fake().replace(b"subject_id",b"private actor@home",1)
  with self.assertRaises(ValueError):schema_without_any_values(b)
 def test_invalid_UTF8_strict_reject(self):
  with self.assertRaises(ValueError):schema_without_any_values(b"\xff\x80")
 def test_missing_source_row_width_fails(self):
  with self.assertRaises(ValueError):schema_without_any_values(fake()+b"bad,short\n")
 def test_too_few_source_rows(self):
  with self.assertRaises(ValueError):schema_without_any_values(fake(5))
if __name__=="__main__":unittest.main()
