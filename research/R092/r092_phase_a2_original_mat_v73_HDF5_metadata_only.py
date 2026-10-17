#!/usr/bin/env python3
"""R092 author MATLAB v7.3 HDF5 structural gate only; NO source arrays read."""
from __future__ import annotations
import argparse,hashlib,io,json,pathlib,re,urllib.request,urllib.error
import h5py
from r092_original_2025_4player_threshold_mat_source_structure_only import (
 URL,MAX_BYTES,source_identity,check_destination)
NAMING=re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,45}$")
HDF=b"\x89HDF\r\n\x1a\n"
def signature_format(raw):
 if raw.startswith(HDF):return 0
 if len(raw)>520 and raw[512:520]==HDF:return 512
 raise ValueError("R092A2_NOT_SUPPORTED_PINNED_HDF5_OR_MAT_V73_FORMAT")
def safe_hdf_metadata(raw):
 signature_format(raw)
 try:
  with h5py.File(io.BytesIO(raw),"r") as f:
   if not f.keys():raise ValueError("R092A2_NO_HDF5_METADATA_ELEMENTS")
   if len(f.keys())>30:raise ValueError("R092A2_TOO_MANY_HDF5_TOPLEVEL_ELEMENTS")
   stats=[]
   for k in sorted(f.keys()):
    if k.startswith("#"):continue # MATLAB reference table, never read.
    if not NAMING.fullmatch(k):
     raise ValueError("R092A2_HDF5_NAME_NOT_SAFE_FOR_RESEARCH_OUTPUT")
    v=f[k]
    if isinstance(v,h5py.Dataset):
     dims=list(v.shape)
     if len(dims)>8 or any(int(x)>5000000 for x in dims):
      raise ValueError("R092A2_UNBOUNDED_HDF5_SHAPE")
     dtype_kind=v.dtype.kind
     if dtype_kind not in ("i","u","f","b","O","S","U","V"):
      raise ValueError("R092A2_UNSUPPORTED_SOURCE_HDF5_DATATYPE")
     stats.append({"source_variable":k,"object":"dataset","shape":dims,
        "dtype_kind":dtype_kind,"dtype_item_bytes":v.dtype.itemsize})
    elif isinstance(v,h5py.Group):
     if len(v.keys())>30:raise ValueError("R092A2_UNBOUNDED_ORIGINAL_GROUP_KEYS")
     kids=[]
     for name in sorted(v.keys()):
      if not NAMING.fullmatch(name):raise ValueError("R092A2_UNSAFE_NESTED_GROUP_NAME")
      child=v[name]
      if isinstance(child,h5py.Dataset):
       kids.append({"source_field":name,"shape":list(child.shape),
        "dtype_kind":child.dtype.kind})
      else:
       kids.append({"source_field":name,"object":"nested_group_not_explored"})
     stats.append({"source_variable":k,"object":"group",
       "safe_immediate_child_metadata":kids})
    else:raise ValueError("R092A2_UNSUPPORTED_HDF5_OBJECT")
 except (OSError,RuntimeError,KeyError,TypeError,ValueError) as e:
  if isinstance(e,ValueError) and str(e).startswith("R092A2_"):raise
  raise ValueError("R092A2_MAT_HDF5_METADATA_READ_FAILED") from e
 if not stats:raise ValueError("R092A2_NO_SAFE_VARIABLE_METADATA")
 return {"matlab_v73_HDF5_only_variable_shape_and_type":stats,
  "values_of_source_actor_group_contribution_arrays_read":False,
  "source_actor_values_or_identifiers_exported":False}
def original():
 check_destination(URL)
 with urllib.request.urlopen(urllib.request.Request(URL,headers={
  "User-Agent":"Psychohistory-R092-Wang-2025-fixed-hdf5-source-metadata/1.0"}),timeout=50) as r:
  check_destination(r.geturl());raw=r.read(MAX_BYTES+1)
 ident=source_identity(raw)
 return {"research_id":"R092","phase":"A2_AUTHOR_OFFICIAL_MATLAB_V73_HDF5_SOURCE_STRUCTURE_ONLY",
  "published_DOI":"10.5281/zenodo.16918146",
  "author_source_identity":ident,"source_mat_structure":safe_hdf_metadata(raw),
  "previous_whosmat_original_failure_retained":True,
  "source_real_actor_contribution_scores_computed":0,
  "same_human_subjects_in_two_session_sources":True,
  "R092_next_roster_protocol":"NOT_YET_FROZEN_PENDING_REAL_SOURCE_STRUCTURE",
  "PESEN_v0.1":"FROZEN"}
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 try:r=original()
 except (OSError,ValueError,RuntimeError,TypeError,urllib.error.URLError,urllib.error.HTTPError) as e:
  why=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R092A2_") else "R092A2_FIRST_PARTY_MAT_SOURCE_OR_HDF_FORMAT_FAILED"
  r={"research_id":"R092","phase":"A2_FIXED_SOURCE_FORMAT_FAIL_CLOSED","safe_failure":why,
    "human_contribution_scores":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(json.dumps(r,sort_keys=True))
if __name__=="__main__":main()
