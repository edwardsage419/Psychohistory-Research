#!/usr/bin/env python3
"""R096 full original file source identity gate tests -- SYNTHETIC ONLY."""
import csv,hashlib,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r096_montero_2022_original_dryad_100round_FP_SP_source_gate import (
  FILES,CAP,ORIGINAL_DOI,official_urls,validate_published_url,source_identity,
  original_csv_metadata,safe_redirect)
def fake(n=101):
 f=io.StringIO();w=csv.writer(f);w.writerow(["session","player","round","action","opponent"])
 for i in range(n):w.writerow(["PRIVATE_SESSION_000","PRIVATE_ACTOR_999",i,"PRIVATE_0_OR_1","PRIVATE_PEER"])
 return f.getvalue().encode()
class SourceOnly(unittest.TestCase):
 def test_doi(self):self.assertEqual(ORIGINAL_DOI,"10.5061/dryad.37pvmcvmk")
 def test_fixed_file_id(self):self.assertEqual(FILES["fix.csv"],1514373)
 def test_rand_file_id(self):self.assertEqual(FILES["rand.csv"],1514372)
 def test_readme_id(self):self.assertEqual(FILES["README.txt"],1514376)
 def test_valid_original_urls(self):
  for k in FILES:
   for u in official_urls(k):self.assertTrue(validate_published_url(k,u))
 def test_unsafe_host(self):
  with self.assertRaises(ValueError):validate_published_url("fix.csv",official_urls("fix.csv")[0].replace("datadryad.org","datadryad.org.evil"))
 def test_other_file_id(self):
  with self.assertRaises(ValueError):validate_published_url("fix.csv",official_urls("rand.csv")[0])
 def test_http_unpinned(self):
  with self.assertRaises(ValueError):validate_published_url("fix.csv",official_urls("fix.csv")[0].replace("https","http",1))
 def test_unsafe_manual_mirror(self):
  with self.assertRaises(ValueError):validate_published_url("fix.csv","https://github.com/attacker/fix.csv")
 def test_reject_http_redirect(self):
  with self.assertRaises(ValueError):safe_redirect("https://datadryad.org","http://s3.amazonaws.com/x")
 def test_reject_redirect_private(self):
  with self.assertRaises(ValueError):safe_redirect("https://datadryad.org","https://127.0.0.1/x")
 def test_allow_publisher_storage_redirect(self):
  self.assertTrue(safe_redirect("https://datadryad.org","https://example.s3.amazonaws.com/original"))
 def test_synthetic_raw_sha(self):
  b=fake();q=source_identity(b,"fix.csv")
  self.assertEqual(q["first_party_actual_whole_file_SHA256"],hashlib.sha256(b).hexdigest())
 def test_reject_oversize(self):
  with self.assertRaises(ValueError):source_identity(b"x"*(CAP["fix.csv"]+1),"fix.csv")
 def test_empty_original_denied(self):
  with self.assertRaises(ValueError):source_identity(b"","fix.csv")
 def test_safe_fields(self):
  self.assertEqual(original_csv_metadata(fake())["total_original_csv_data_rows"],101)
 def test_microdata_not_exported(self):
  r=str(original_csv_metadata(fake()))
  for secret in ("PRIVATE_SESSION_000","PRIVATE_ACTOR_999","PRIVATE_0_OR_1","PRIVATE_PEER"):self.assertNotIn(secret,r)
 def test_no_original_observations_read(self):
  self.assertTrue(original_csv_metadata(fake())["all_original_human_actions_outcomes_and_actor_or_session_values_unread"])
 def test_unknown_header_denied(self):
  with self.assertRaises(ValueError):original_csv_metadata(fake().replace(b"player",b"weird name@",1))
 def test_duplicate_header_denied(self):
  with self.assertRaises(ValueError):original_csv_metadata(fake().replace(b"opponent",b"action",1))
 def test_invalid_encoding_denied(self):
  with self.assertRaises(ValueError):original_csv_metadata(b"\xff\xfe")
 def test_few_rows_denied(self):
  with self.assertRaises(ValueError):original_csv_metadata(fake(5))
 def test_rowwidth_mismatch_denied(self):
  with self.assertRaises(ValueError):original_csv_metadata(fake()+b"only,one\n")
if __name__=="__main__":unittest.main()
