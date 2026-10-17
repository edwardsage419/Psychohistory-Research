#!/usr/bin/env python3
import io,pathlib,sys,unittest
import numpy as np
from scipy.io import savemat
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r092_phase_a3_fixed_author_original_mat_signature_only import binary_format_flags,HDF
def sample():
 b=io.BytesIO();savemat(b,{"RealSourceContribution":np.array([1,98765432])});return b.getvalue()
class SyntheticSourceFileType(unittest.TestCase):
 def test_MAT5_header(self):self.assertTrue(binary_format_flags(sample())["MATLAB_5_header_prefix"])
 def test_MAT5_Scipy_success(self):self.assertEqual(binary_format_flags(sample())["scipy_mat_whosmat_source_schema_status"],"ACCEPTED")
 def test_HDF5_magic_offset512(self):
  z=b"x"*512+HDF+b"z"*20
  self.assertEqual(binary_format_flags(z)["HDF5_known_safe_signature_offsets"],[512])
 def test_HDF5_magic_offset1024(self):
  z=b"x"*1024+HDF+b"z"*20
  self.assertEqual(binary_format_flags(z)["HDF5_known_safe_signature_offsets"],[1024])
 def test_truncated_source_denied_no_content(self):
  z=str(binary_format_flags(b"garbage"))
  self.assertNotIn("garbage",z)
 def test_empty_denied(self):
  with self.assertRaises(ValueError):binary_format_flags(b"")
 def test_zip_magic(self):self.assertTrue(binary_format_flags(b"PK\x03\x04payload")["ZIP_magic_prefix"])
 def test_gzip_magic(self):self.assertTrue(binary_format_flags(b"\x1f\x8bpayload")["GZIP_magic_prefix"])
 def test_netCDF_magic(self):self.assertTrue(binary_format_flags(b"CDF\x01payload")["CDF_netCDF_magic_prefix"])
 def test_no_source_actor_values_exported(self):
  v=str(binary_format_flags(sample()))
  self.assertNotIn("98765432",v)
 def test_disallowed_private_source_header_not_echoed(self):
  z=str(binary_format_flags(b"PRIVATE_ACTOR_1234567890"*10))
  self.assertNotIn("PRIVATE",z)
 def test_invalid_return_has_safe_exception_only(self):
  z=binary_format_flags(b"garbage")
  self.assertEqual(z["scipy_mat_whosmat_source_schema_status"],"DENIED")
 def test_no_real_behaviour_read_flag(self):
  self.assertFalse(binary_format_flags(sample())["real_human_behavior_read"])
if __name__=="__main__":unittest.main()
