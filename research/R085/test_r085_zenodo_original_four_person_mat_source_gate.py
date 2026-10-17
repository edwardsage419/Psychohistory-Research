#!/usr/bin/env python3
"""R085 synthetic-only Zenodo exact author MD5 and MATLAB schema tests."""
import hashlib,io,pathlib,sys,unittest
from scipy.io import savemat
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r085_zenodo_original_four_person_mat_source_gate import (
 DOI,RECORD,SOURCES,MAX_BYTES,source_url,validate_canonical_url,
 inspect_publisher_mat,diagnostic,urllib)

def synthetic_mat(x=None):
 b=io.BytesIO()
 savemat(b,{"synthetic_matrix":[[0,1,2],[3,4,5]] if x is None else x},do_compression=False)
 return b.getvalue()

class SourceManifestTests(unittest.TestCase):
 def test_DOI(self):self.assertEqual(DOI,"10.5281/zenodo.16918146")
 def test_record(self):self.assertEqual(RECORD,16918146)
 def test_two_original_files(self):self.assertEqual(len(SOURCES),2)
 def test_fixed_names_and_md5(self):
  self.assertEqual(SOURCES["four_person_linear"]["author_published_md5"],"42153952f8e6614d09c2d903fd97af62")
  self.assertEqual(SOURCES["four_person_threshold"]["author_published_md5"],"6036f73c2f758ab3aeed6dcf4f74585b")
 def test_origianl_two_roles_not_independent_sessions(self):
  self.assertEqual(sum(SOURCES["four_person_linear"]["participants_by_arm_published"].values()),312)
  self.assertEqual(sum(SOURCES["four_person_threshold"]["participants_by_arm_published"].values()),276)
 def test_source_url_only_frozen_original(self):
  for v in SOURCES.values():self.assertTrue(validate_canonical_url(source_url(v["filename"])))
 def test_unknown_file_rejected(self):
  with self.assertRaises(ValueError):source_url("researcher_survey_person_1.csv")
 def test_http_rejected(self):
  with self.assertRaises(ValueError):
   validate_canonical_url("http://zenodo.org/records/16918146/files/LinearPGG_4P_ExperimentalData.mat")
 def test_forged_host_rejected(self):
  with self.assertRaises(ValueError):
   validate_canonical_url("https://zenodo.org.evil.com/records/16918146/files/LinearPGG_4P_ExperimentalData.mat")
 def test_filename_substitution_rejected(self):
  with self.assertRaises(ValueError):
   validate_canonical_url("https://zenodo.org/records/16918146/files/Fraud.mat")
 def test_version_substitution_rejected(self):
  with self.assertRaises(ValueError):
   validate_canonical_url("https://zenodo.org/records/16918145/files/LinearPGG_4P_ExperimentalData.mat")
 def test_path_traversal_rejected(self):
  with self.assertRaises(ValueError):
   validate_canonical_url("https://zenodo.org/records/16918146/files/../LinearPGG_4P_ExperimentalData.mat")
 def test_fragment_rejected(self):
  with self.assertRaises(ValueError):
   validate_canonical_url("https://zenodo.org/records/16918146/files/LinearPGG_4P_ExperimentalData.mat#bad")
 def test_userinfo_rejected(self):
  with self.assertRaises(ValueError):
   validate_canonical_url("https://user@zenodo.org/records/16918146/files/LinearPGG_4P_ExperimentalData.mat")
 def test_port_rejected(self):
  with self.assertRaises(ValueError):
   validate_canonical_url("https://zenodo.org:443/records/16918146/files/LinearPGG_4P_ExperimentalData.mat")

class MATLABDataClassTests(unittest.TestCase):
 def test_synthetic_mat_schema_passes_with_own_expected_md5(self):
  b=synthetic_mat()
  d=inspect_publisher_mat(b,hashlib.md5(b).hexdigest())
  self.assertTrue(d["author_published_md5_match"])
  self.assertEqual(d["original_mat_variable_shapes_without_data"][0]["shape"],[2,3])
  self.assertEqual(d["original_variable_count"],1)
  self.assertEqual(d["whole_original_file_sha256_computed"],hashlib.sha256(b).hexdigest())
 def test_wrong_md5_fails_before_mat_read(self):
  with self.assertRaisesRegex(ValueError,"MD5_MISMATCH"):
   inspect_publisher_mat(synthetic_mat(),"0"*32)
 def test_zero_file_rejected(self):
  with self.assertRaisesRegex(ValueError,"EMPTY"):
   inspect_publisher_mat(b"",hashlib.md5(b"").hexdigest())
 def test_oversize_bytes_rejected(self):
  b=b"x"*(MAX_BYTES+1)
  with self.assertRaisesRegex(ValueError,"OVERSIZED"):
   inspect_publisher_mat(b,hashlib.md5(b).hexdigest())
 def test_mat_not_python_or_arbitrary_text(self):
  b=b"synthetic source that is not Matlab"
  with self.assertRaisesRegex(ValueError,"MAT_SCHEMA"):
   inspect_publisher_mat(b,hashlib.md5(b).hexdigest())
 def test_no_human_rows_emitted_in_source_schema(self):
  b=io.BytesIO()
  savemat(b,{"secret_id_subject":[[123456789]]})
  x=b.getvalue()
  r=inspect_publisher_mat(x,hashlib.md5(x).hexdigest())
  self.assertNotIn("123456789",str(r))
 def test_failed_http_status_classified(self):
  e=urllib.error.HTTPError("https://zenodo.org",503,"Service Unavailable",{},None)
  self.assertEqual(diagnostic(e),"AUTHOR_HOST_HTTP_503")
 def test_transport_error_redacts_secrets(self):
  e=urllib.error.URLError("private-subject-ID-999")
  self.assertNotIn("999",diagnostic(e))
 def test_io_error_sanitized(self):
  self.assertEqual(diagnostic(OSError("secret")),"SOURCE_NETWORK_OR_FILE_IO")

if __name__=="__main__":
 unittest.main()
