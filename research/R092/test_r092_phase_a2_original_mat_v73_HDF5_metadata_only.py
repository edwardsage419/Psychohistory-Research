#!/usr/bin/env python3
"""R092 original 2025 HDF5 MAT structure-only tests; strictly synthetic values."""
import io,pathlib,sys,unittest
import h5py,numpy as np
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r092_phase_a2_original_mat_v73_HDF5_metadata_only import (
 HDF,signature_format,safe_hdf_metadata)

def fixture(keys=None):
 if keys is None:keys={"Contribution":np.array([[123456.789,345678.901]])}
 b=io.BytesIO()
 with h5py.File(b,"w") as h:
  for k,v in keys.items():h.create_dataset(k,data=v)
 return b.getvalue()
class StrictHDFSource(unittest.TestCase):
 def test_HDF_header_magic(self):self.assertEqual(signature_format(fixture()),0)
 def test_HDF_header_offset512(self):self.assertEqual(signature_format(b"x"*512+fixture()),512)
 def test_nonMAT_cannot_pass(self):
  with self.assertRaises(ValueError):signature_format(b"garbage"*60)
 def test_empty_data_not_HDF(self):
  with self.assertRaises(ValueError):safe_hdf_metadata(b"")
 def test_source_no_raw_contribution_values(self):
  s=str(safe_hdf_metadata(fixture()))
  self.assertNotIn("123456",s)
  self.assertNotIn("345678",s)
 def test_shape_without_values(self):
  r=safe_hdf_metadata(fixture())["matlab_v73_HDF5_only_variable_shape_and_type"][0]
  self.assertEqual(r["shape"],[1,2])
 def test_dtype_shape_report(self):
  r=safe_hdf_metadata(fixture())["matlab_v73_HDF5_only_variable_shape_and_type"][0]
  self.assertEqual(r["dtype_kind"],"f")
 def test_multiple_safe_dataset_names(self):
  r=safe_hdf_metadata(fixture({"Round":np.array([[2]]),"GroupID":np.array([[9999999]])}))
  self.assertEqual(len(r["matlab_v73_HDF5_only_variable_shape_and_type"]),2)
 def test_no_actor_values_read_flag(self):
  x=safe_hdf_metadata(fixture())
  self.assertFalse(x["values_of_source_actor_group_contribution_arrays_read"])
 def test_unsafe_private_name_denied(self):
  with self.assertRaises(ValueError):
   safe_hdf_metadata(fixture({"actor@gmail.com":np.array([1])}))
 def test_non_ascii_name_denied(self):
  with self.assertRaises(ValueError):
   safe_hdf_metadata(fixture({"私隐":np.array([1])}))
 def test_huge_dimensions_denied(self):
  b=io.BytesIO()
  with h5py.File(b,"w") as h:
   h.create_dataset("Contribution",shape=(5000001,),dtype="u1")
  with self.assertRaises(ValueError):safe_hdf_metadata(b.getvalue())
 def test_empty_group_no_output(self):
  b=io.BytesIO()
  with h5py.File(b,"w") as h:
   h.create_group("#refs#")
  with self.assertRaises(ValueError):safe_hdf_metadata(b.getvalue())
 def test_immediate_group_child_shapes_only(self):
  b=io.BytesIO()
  with h5py.File(b,"w") as h:
   g=h.create_group("Data");g.create_dataset("Round",data=np.array([42,10000000]))
  r=str(safe_hdf_metadata(b.getvalue()))
  self.assertIn("Round",r)
  self.assertNotIn("10000000",r)
 def test_truncated_HDF_fails_closed(self):
  with self.assertRaises(ValueError):safe_hdf_metadata(fixture()[:20])
if __name__=="__main__":unittest.main()
