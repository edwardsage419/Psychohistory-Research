#!/usr/bin/env python3
"""Synthetic MAT v5 only; no original 2025 human choice data."""
import io,hashlib,pathlib,sys,struct,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from scipy.io import savemat
from r098_phase_a5_mat5_tlv_metadata_only_parser import (
 REAL_SOURCE_SHA,tag,directory_only,parse_matrix_directory,compressed_block)
def mat(compressed=False,records=None):
 b=io.BytesIO()
 savemat(b,records if records is not None else
  {"FE":[[123456789,5],[2,3]],"AI":[[1.5,0],[2.1,4.0]],"MI":[[4]]},
  do_compression=compressed)
 return b.getvalue()
class SyntheticSourceMAT(unittest.TestCase):
 def test_fixed_author_publisher_sha(self):
  self.assertEqual(REAL_SOURCE_SHA,"dcdd23e709ce1c17fadddffb84d07b9cf2f37a0a206e4665317aed31fd4e790b")
 def test_original_header_length(self):self.assertEqual(len(mat()[:128]),128)
 def test_no_real_choice_first(self):
  z=directory_only(mat());self.assertFalse(z["reader_decoded_any_original_real_human_contribution_or_actor_value"])
 def test_no_real_value_ever_exported(self):
  self.assertNotIn("123456789",str(directory_only(mat())))
 def test_three_original_variable_names(self):
  z=directory_only(mat())
  self.assertEqual({x["original_MAT5_name_only"] for x in z["original_MAT5_top_level_variables_directory_ONLY"]},{"FE","AI","MI"})
 def test_scipy_legacy_no_compression(self):
  self.assertEqual(directory_only(mat())["original_top_level_variables"],3)
 def test_scipy_legacy_zlib_compression(self):
  self.assertEqual(directory_only(mat(True))["original_top_level_variables"],3)
 def test_original_type_only(self):
  x=directory_only(mat())["original_MAT5_top_level_variables_directory_ONLY"]
  self.assertTrue(all("original_MAT5_class_only" in v for v in x))
 def test_array_source_numeric_never_loaded(self):
  self.assertFalse(directory_only(mat())["reader_loaded_source_numeric_arrays"])
 def test_original_actor_ids_never_republished(self):
  self.assertTrue(not directory_only(mat())["publisher_original_bytes_redistributed"])
 def test_mat_version_mark(self):
  self.assertEqual(directory_only(mat())["MAT_byteorder_and_version_metadata_only"],"MAT5_0x0100_little_endian")
 def test_truncated_file_failure(self):
  with self.assertRaises(ValueError):directory_only(mat()[:-10])
 def test_not_mat_failure(self):
  with self.assertRaises(ValueError):directory_only(b"123")
 def test_wrong_endian_failure(self):
  b=bytearray(mat());b[126:128]=b"MI"
  with self.assertRaises(ValueError):directory_only(bytes(b))
 def test_wrong_version_failure(self):
  b=bytearray(mat());b[124:126]=b"\x01\x00"
  with self.assertRaises(ValueError):directory_only(bytes(b))
 def test_fake_TLV_type_denied(self):
  b=bytearray(mat());b[128:132]=struct.pack("<I",9)
  with self.assertRaises(ValueError):directory_only(bytes(b))
 def test_outer_invalid_large_length_denied(self):
  b=bytearray(mat());b[132:136]=struct.pack("<I",200000000)
  with self.assertRaises(ValueError):directory_only(bytes(b))
 def test_top_level_source_empty_denied(self):
  with self.assertRaises(ValueError):directory_only(mat()[:128])
 def test_padded_short_top_type(self):
  t,n,pos,nxt=tag(mat(),128,len(mat()))
  self.assertEqual(t,14);self.assertGreater(n,0);self.assertLess(nxt,len(mat())+1)
 def test_high_dim_shape(self):
  x=directory_only(mat(False,{"MATRIX":[[1,2,3]]}))
  self.assertEqual(x["original_MAT5_top_level_variables_directory_ONLY"][0]["shape_dimensions_only"],[1,3])
 def test_source_variable_int_mat(self):
  x=directory_only(mat(False,{"FOO":[[5,6],[7,8]]}))
  self.assertEqual(x["original_MAT5_top_level_variables_directory_ONLY"][0]["original_MAT5_name_only"],"FOO")
 def test_many_variable_data_values_never_printed(self):
  x=directory_only(mat(False,{"MI":[[987654321.01]]}))
  self.assertNotIn("987654321",str(x))
 def test_anonymous_source_meta_only(self):
  x=str(directory_only(mat()))
  self.assertNotIn("SECRET_ACTOR_0091",x)
 def test_no_source_numerical_output_cells(self):
  x=directory_only(mat())
  self.assertNotIn("actual_contribution",str(x))
 def test_compressed_material_source_numerical_output_never_loaded(self):
  x=directory_only(mat(True))
  self.assertFalse(x["reader_loaded_source_numeric_arrays"])
if __name__=="__main__":unittest.main()
