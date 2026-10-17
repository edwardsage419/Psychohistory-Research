#!/usr/bin/env python3
import hashlib,io,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from scipy.io import savemat
from r098_wang2025_4p_linear_zenodo_mat_publisher_MD5_structure_only import (
 URL,NAME,OFFICIAL_MD5,CAP,validate_url,verify_original_bytes,mat_metadata)
def synt():
 b=io.BytesIO();savemat(b,{"FE":[[1,2],[3,4]],"AI":[[0,0],[0,1]],"MI":[[1,0],[1,0]]})
 return b.getvalue()
class OriginalMatSourceOnly(unittest.TestCase):
 def test_url(self):self.assertTrue(validate_url(URL))
 def test_basename(self):self.assertEqual(NAME,"LinearPGG_4P_ExperimentalData.mat")
 def test_publisher_md5_pin(self):self.assertEqual(OFFICIAL_MD5,"42153952f8e6614d09c2d903fd97af62")
 def test_not_raw_root(self):
  with self.assertRaises(ValueError):validate_url("https://zenodo.org/records/16918146/files/ThresholdPGG_4P_ExperimentalData.mat")
 def test_wrong_record(self):
  with self.assertRaises(ValueError):validate_url(URL.replace("16918146","16918145"))
 def test_wrong_host(self):
  with self.assertRaises(ValueError):validate_url(URL.replace("zenodo.org","zenodo.org.evil"))
 def test_insecure_http(self):
  with self.assertRaises(ValueError):validate_url(URL.replace("https","http",1))
 def test_wrong_origin_suffix(self):
  with self.assertRaises(ValueError):validate_url(URL+"&actor=SECRET_PERSON")
 def test_synthetic_mat_header(self):
  m=mat_metadata(synt());self.assertEqual(m["number_top_level_original_MAT_variables"],3)
 def test_only_keys_and_shapes(self):
  m=mat_metadata(synt());names={v["MAT_original_top_level_variable_name"] for v in m["source_metadata_only_variables"]}
  self.assertEqual(names,{"FE","AI","MI"})
 def test_no_human_action_values_read(self):
  m=mat_metadata(synt());self.assertFalse(m["actual_human_contribution_values_or_actor_group_codes_inspected"])
 def test_full_MAT_array_never_loaded(self):self.assertFalse(mat_metadata(synt())["MAT_full_data_arrays_loaded"])
 def test_source_sha_correct(self):
  b=synt();r=verify_original_bytes(b,hashlib.md5(b).hexdigest())
  self.assertEqual(r["original_fullfile_computed_SHA256"],hashlib.sha256(b).hexdigest())
 def test_strict_public_md5(self):
  with self.assertRaises(ValueError):verify_original_bytes(synt())
 def test_empty_denied(self):
  with self.assertRaises(ValueError):verify_original_bytes(b"",hashlib.md5(b"").hexdigest())
 def test_file_over_cap_denied(self):
  with self.assertRaises(ValueError):verify_original_bytes(b"f"*(CAP+1),hashlib.md5(b"f"*(CAP+1)).hexdigest())
 def test_mat_header_not_mat_denied(self):
  with self.assertRaises(ValueError):mat_metadata(b"12345")
 def test_no_source_original_actor_filename(self):
  self.assertNotIn("PRIVATE",str(mat_metadata(synt())))
 def test_MAT_names_distinct(self):
  a=mat_metadata(synt())["source_metadata_only_variables"]
  self.assertEqual(len({v["MAT_original_top_level_variable_name"] for v in a}),3)
if __name__=="__main__":unittest.main()
