#!/usr/bin/env python3
"""R099 first-party PLOS S1 original CSV source-only pure synthetic tests."""
import csv,hashlib,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r099_liu_2024_plos_official_original_S1_CSV_publisher_metadata_only import (
 URL,ARTICLE_DOI,DATA_DOI,MAX_CSV,check_publisher_url,verify_bytes,source_safe_columns)
def b(n=97):
 s=io.StringIO();w=csv.writer(s)
 w.writerow(["session","group","player","period","contribution"])
 for i in range(n):w.writerow(["PRIVATE_SESSION","PRIVATE_GROUP","PRIVATE_PERSON",i,"PRIVATE_CONTRIBUTION"])
 return s.getvalue().encode()
class PublicationSource(unittest.TestCase):
 def test_article_doi(self):self.assertEqual(ARTICLE_DOI,"10.1371/journal.pone.0299196")
 def test_original_data_doi(self):self.assertEqual(DATA_DOI,"10.1371/journal.pone.0299196.s002")
 def test_official_url(self):self.assertTrue(check_publisher_url(URL))
 def test_untrusted_host(self):
  with self.assertRaises(ValueError):check_publisher_url(URL.replace("journals.plos.org","journals.plos.org.example"))
 def test_bad_S1_file_id(self):
  with self.assertRaises(ValueError):check_publisher_url(URL.replace("s002","s003"))
 def test_http_forbidden(self):
  with self.assertRaises(ValueError):check_publisher_url(URL.replace("https","http",1))
 def test_unpinned_query_forbidden(self):
  with self.assertRaises(ValueError):check_publisher_url(URL+"&token=SECRET")
 def test_100_bytes_valid(self):
  q=verify_bytes(b());self.assertGreaterEqual(q["exact_original_CSV_bytes"],100)
 def test_empty_forbidden(self):
  with self.assertRaises(ValueError):verify_bytes(b"")
 def test_large_forbidden(self):
  with self.assertRaises(ValueError):verify_bytes(b"x"*(MAX_CSV+1))
 def test_checksum_real_formula(self):
  x=b();self.assertEqual(verify_bytes(x)["original_first_party_fullfile_SHA256"],hashlib.sha256(x).hexdigest())
 def test_exact_synthetic_csv_header(self):
  self.assertEqual(source_safe_columns(b())["column_count"],5)
 def test_synthetic_line_count(self):
  self.assertEqual(source_safe_columns(b())["original_source_rows_NOT_YET_VERIFIED_AS_REPEATED_PLAYER_ACTIONS"],97)
 def test_no_original_contribution_values(self):
  self.assertNotIn("PRIVATE_CONTRIBUTION",str(source_safe_columns(b())))
 def test_no_actual_source_actor(self):
  self.assertNotIn("PRIVATE_PERSON",str(source_safe_columns(b())))
 def test_no_source_session_ID(self):
  self.assertNotIn("PRIVATE_SESSION",str(source_safe_columns(b())))
 def test_contributions_not_examined(self):
  self.assertFalse(source_safe_columns(b())["original_human_contribution_values_examined"])
 def test_actor_id_values_not_examined(self):
  self.assertFalse(source_safe_columns(b())["original_player_session_group_ID_values_examined"])
 def test_no_microdata_redistributed(self):
  self.assertFalse(source_safe_columns(b())["original_microdata_redistributed"])
 def test_little_data_rejected(self):
  with self.assertRaises(ValueError):source_safe_columns(b(2))
 def test_width_changed_rejected(self):
  with self.assertRaises(ValueError):source_safe_columns(b()+b"only,two\n")
 def test_duplicate_columns_rejected(self):
  with self.assertRaises(ValueError):source_safe_columns(b().replace(b"period",b"player",1))
 def test_unsafe_csv_name_rejected(self):
  with self.assertRaises(ValueError):source_safe_columns(b().replace(b"contribution",b"<injection>",1))
 def test_invalid_utf8_rejected(self):
  with self.assertRaises(ValueError):source_safe_columns(b"\xff\xfe")
 def test_shows_only_publisher_computed_SHA_not_fake_official_MD5(self):
  self.assertFalse(verify_bytes(b())["publisher_original_has_independent_reported_official_MD5"])
if __name__=="__main__":unittest.main()
