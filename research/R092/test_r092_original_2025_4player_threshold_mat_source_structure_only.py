#!/usr/bin/env python3
"""Original MATLAB source gate synthetic-only immutable hash, name, and safe dimensions."""
import hashlib,io,pathlib,sys,unittest
import numpy as np
from scipy.io import savemat
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r092_original_2025_4player_threshold_mat_source_structure_only import (
 MD5,MAX_BYTES,URL,RECORD,FILE,source_identity,check_destination,anonymous_whosmat)

def mat_file(variables):
 buf=io.BytesIO();savemat(buf,variables);return buf.getvalue()
class OriginalSourceOnlyTests(unittest.TestCase):
 def test_original_MD5_pinned(self):self.assertEqual(MD5,"6036f73c2f758ab3aeed6dcf4f74585b")
 def test_record_pinned(self):self.assertEqual(RECORD,"16918146")
 def test_filename_is_threshold_four_person(self):self.assertEqual(FILE,"ThresholdPGG_4P_ExperimentalData.mat")
 def test_zenodo_original_url(self):self.assertTrue(check_destination(URL))
 def test_unknown_host_denied(self):
  with self.assertRaises(ValueError):check_destination(URL.replace("zenodo.org","zenodo.org.evil"))
 def test_other_record_denied(self):
  with self.assertRaises(ValueError):check_destination(URL.replace(RECORD,"2"))
 def test_http_not_https_denied(self):
  with self.assertRaises(ValueError):check_destination(URL.replace("https","http",1))
 def test_other_file_denied(self):
  with self.assertRaises(ValueError):check_destination(URL.replace(FILE,"OTHER.mat"))
 def test_source_empty_rejected(self):
  with self.assertRaises(ValueError):source_identity(b"",hashlib.md5(b"").hexdigest())
 def test_source_different_MD5_refused(self):
  with self.assertRaises(ValueError):source_identity(b"not source")
 def test_source_too_large_refused(self):
  with self.assertRaises(ValueError):source_identity(b"a"*(MAX_BYTES+1),hashlib.md5(b"a"*(MAX_BYTES+1)).hexdigest())
 def test_source_synthetic_complete_digest(self):
  b=mat_file({"Treatment":np.arange(4)})
  info=source_identity(b,hashlib.md5(b).hexdigest())
  self.assertEqual(info["original_source_bytes"],len(b))
  self.assertEqual(info["original_whole_file_SHA256"],hashlib.sha256(b).hexdigest())
 def test_whosmat_structure_safe_shape(self):
  x=anonymous_whosmat(mat_file({"Treatment":np.zeros((5,3))}))
  self.assertEqual(x["source_only_MAT_variables"][0]["shape"],[5,3])
 def test_whosmat_no_rows_dumped(self):
  v=str(anonymous_whosmat(mat_file({"GroupID":np.array([[98765432,12345678]])})))
  self.assertNotIn("98765432",v)
  self.assertNotIn("12345678",v)
 def test_whosmat_counts_classes_only(self):
  v=anonymous_whosmat(mat_file({"GroupID":np.arange(5),"Contribution":np.zeros((5,20))}))
  self.assertEqual(v["source_MAT_variable_count"],2)
  self.assertFalse(v["original_actor_values_or_group_ids_examined"])
 def test_unreadable_MAT_rejected(self):
  with self.assertRaises(ValueError):anonymous_whosmat(b"garbage")
 def test_MAT_variable_count_must_positive(self):
  with self.assertRaises(ValueError):anonymous_whosmat(mat_file({}))
 def test_name_header_field_data_only_never_read(self):
  v=str(anonymous_whosmat(mat_file({"Contribution":np.array([[123456.78]])})))
  self.assertNotIn("123456",v)
 def test_zipped_original_not_accepted_as_mat(self):
  with self.assertRaises(ValueError):anonymous_whosmat(b"PK"+b"x"*200)
if __name__=="__main__":unittest.main()
