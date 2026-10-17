#!/usr/bin/env python3
"""R085 phase-B synthetic data format-only inspection tests. No real human rows."""
import hashlib,io,pathlib,sys,unittest
import h5py
from scipy.io import savemat
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r085_phase_b_mat_real_source_type_only import (
 header_kind,h5_structure,inspect_source_format)

class FileHeaderTests(unittest.TestCase):
 def test_unknown_magic_rejected(self):
  self.assertEqual(header_kind(b"X"*600),"OTHER_SOURCE_FORMAT_UNKNOWN")
 def test_too_short_rejected(self):
  with self.assertRaises(ValueError):header_kind(b"HDF")
 def test_detect_MAT5(self):
  self.assertEqual(header_kind(b"MATLAB 5.0"+b" " * 150),"MATLAB_5_HEADER")
 def test_detect_hdf5_root_magic(self):
  b=io.BytesIO()
  with h5py.File(b,"w") as f:f.create_dataset("synthetic",data=[1,2,3])
  self.assertEqual(header_kind(b.getvalue()),"HDF5_HEADER")
 def test_detect_hdf5_512(self):
  b=b"MATLAB 7.3 "+b" "*500+b"\x89HDF\r\n\x1a\n"+b"x"*300
  # This synthetic value intentionally has a non-512 placement.
  self.assertEqual(header_kind(b),"MATLAB_5_HEADER")
 def test_mat5_synthetic_structure_no_values(self):
  b=io.BytesIO()
  savemat(b,{"testvalue":[[11223344,5]]})
  s=b.getvalue();r=inspect_source_format(s,hashlib.md5(s).hexdigest())
  self.assertEqual(r["original_format_signature"],"MATLAB_5_HEADER")
  self.assertNotIn("11223344",str(r))
 def test_valid_hdf5_structure_keys_only(self):
  b=io.BytesIO()
  with h5py.File(b,"w") as f:
   f.create_dataset("experiment_data",data=[333333333,4,5])
  r=inspect_source_format(b.getvalue(),hashlib.md5(b.getvalue()).hexdigest())
  self.assertEqual(r["original_format_signature"],"HDF5_HEADER")
  self.assertNotIn("333333333",str(r))
 def test_invalid_md5_fails(self):
  b=io.BytesIO()
  with h5py.File(b,"w") as f:f.create_dataset("x",data=[1])
  with self.assertRaisesRegex(ValueError,"MD5_MISMATCH"):
   inspect_source_format(b.getvalue(),"0"*32)
 def test_zip_fails_even_if_md5_ok(self):
  s=b"PK"+b"x"*200
  with self.assertRaises(ValueError):inspect_source_format(s,hashlib.md5(s).hexdigest())
 def test_HDF5_internal_reference_tree_is_not_expanded(self):
  b=io.BytesIO()
  with h5py.File(b,"w") as f:f.create_group("#refs#").create_dataset("secret_table",data=[12345])
  d=h5_structure(b.getvalue())
  self.assertEqual(d[0]["kind"],"INTERNAL_MATLAB_REFERENCE_TREE")
  self.assertNotIn("12345",str(d))

if __name__=="__main__":unittest.main()
