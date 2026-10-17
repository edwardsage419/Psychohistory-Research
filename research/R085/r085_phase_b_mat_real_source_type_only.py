#!/usr/bin/env python3
"""Source-identical R085 Phase B format-only metadata inspection after MAT5 failure."""
from __future__ import annotations
import argparse,hashlib,io,json,pathlib,urllib.request,urllib.error
import h5py
from scipy.io import whosmat
from r085_zenodo_original_four_person_mat_source_gate import (
 SOURCES,source_url,validate_canonical_url,MAX_BYTES,diagnostic,DOI,RECORD)

def header_kind(data:bytes):
 if not isinstance(data,bytes) or len(data)<129:raise ValueError("R085_PHASE_B_ORIGINAL_BYTES_TOO_SHORT")
 if data[:7]==b"MATLAB ":
  if data[512:520]==b"\x89HDF\r\n\x1a\n":return "MATLAB_7_3_HDF5_512"
  return "MATLAB_5_HEADER"
 if data[:8]==b"\x89HDF\r\n\x1a\n" or data[512:520]==b"\x89HDF\r\n\x1a\n":
  return "HDF5_HEADER"
 if data[:2]==b"PK":return "ZIP_UNKNOWN_NOT_MAT"
 return "OTHER_SOURCE_FORMAT_UNKNOWN"

def h5_structure(data):
 try:
  out=[]
  with h5py.File(io.BytesIO(data),"r") as root:
   for name in sorted(root):
    v=root[name]
    if name.startswith("#") or name.startswith("_"):
     # Still include first-party private internal reference tree structure flag, not personal rows.
     out.append({"root_name":name[:80],"kind":"INTERNAL_MATLAB_REFERENCE_TREE"})
     continue
    part={"root_name":name[:80],
          "kind":"group" if isinstance(v,h5py.Group) else "dataset"}
    if isinstance(v,h5py.Dataset):
     part.update({"shape":list(v.shape),"dtype_kind":v.dtype.kind,"dtype_itemsize":v.dtype.itemsize})
    elif isinstance(v,h5py.Group):
     part["first_level_members"]=[]
     for key in sorted(v.keys())[:100]:
      sub=v[key]
      s={"name":key[:80],"kind":"group" if isinstance(sub,h5py.Group) else "dataset"}
      if isinstance(sub,h5py.Dataset):s.update({"shape":list(sub.shape),"dtype_kind":sub.dtype.kind})
      part["first_level_members"].append(s)
     part["first_level_member_count"]=len(v)
    out.append(part)
  if not out:raise ValueError("R085_EMPTY_HDF5_VARIABLE_TREE")
  return out
 except (OSError,ValueError,TypeError,RuntimeError) as e:
  raise ValueError("R085_HDF5_SOURCE_SCHEMA_READ_NOT_SUPPORTED") from e

def inspect_source_format(raw,expected_md5):
 if not 128<len(raw)<=MAX_BYTES:raise ValueError("R085_FILE_EMPTY_OR_TOO_LARGE")
 if hashlib.md5(raw).hexdigest()!=expected_md5:
  raise ValueError("R085_OFFICIAL_ZENODO_MD5_MISMATCH")
 meta={"publisher_MD5_exact_match":True,"full_original_bytes":len(raw),
       "whole_author_file_sha256":hashlib.sha256(raw).hexdigest()}
 category=header_kind(raw)
 meta["original_format_signature"]=category
 if category in ("MATLAB_7_3_HDF5_512","HDF5_HEADER"):
  meta["mat_source_metadata"]=h5_structure(raw)
 elif category=="MATLAB_5_HEADER":
  try:
   xs=whosmat(io.BytesIO(raw))
   meta["mat_source_metadata"]=[{"name":str(n)[:80],"shape":list(s),"matclass":str(k)[:40]} for n,s,k in xs]
  except (OSError,ValueError,TypeError,IndexError,NotImplementedError) as e:
   raise ValueError("R085_PUBLISHED_FILE_MAT5_WHOSMAT_FAILED") from e
 else:raise ValueError("R085_UNEXPECTED_AUTHOR_MAT_SOURCE_FORMAT")
 meta["source_parse_level"]="STRUCTURAL_METADATA_ONLY_NO_HUMAN_MATRIX_VALUES"
 return meta

def examine():
 receipt={}
 for kind,spec in SOURCES.items():
  r={"filename":spec["filename"],"original_published_md5":spec["author_published_md5"]}
  try:
   url=source_url(spec["filename"])
   req=urllib.request.Request(url,headers={
     "User-Agent":"PsychologicalHistory-R085-phaseB-original-MAT-type-audit/1.0"})
   with urllib.request.urlopen(req,timeout=35) as response:
    validate_canonical_url(response.geturl())
    raw=response.read(MAX_BYTES+1)
   r.update(inspect_source_format(raw,spec["author_published_md5"]))
   r["source_gate"]="ORIGINAL_MD5_AND_METADATA_VERIFIED"
  except (ValueError,OSError,TypeError,urllib.error.HTTPError,urllib.error.URLError,TimeoutError) as e:
   r["source_gate"]="FAIL_CLOSED"
   r["safe_error_class"]=diagnostic(e)
  receipt[kind]=r
 ok=all(z["source_gate"]=="ORIGINAL_MD5_AND_METADATA_VERIFIED" for z in receipt.values())
 return {"research_id":"R085","phase":"B_MAT_ORIGINAL_SOURCE_FORMAT_ONLY",
   "status":"R085_PHASE_B_ORIGINAL_TWO_MAT_FORMATS_AND_MD5_VALID" if ok else "R085_PHASE_B_FORMAT_OR_AUTHORITY_FAIL_CLOSED",
   "first_R085_phase_A_source_parser_failure_retained":True,
   "author_DOI":DOI,"zenodo_record":RECORD,
   "two_source_format_inspections":receipt,
   "original_subject_level_action_values_computed":0,
   "original_real_human_cooperation_effects_computed":0,
   "personal_actors_or_network_ids_exported":False,
   "raw_author_files_exported":False,
   "real_human_behavior_evidence":"NOT_YET_REPRODUCED",
   "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 args=p.parse_args()
 r=examine()
 args.output.parent.mkdir(parents=True,exist_ok=True)
 args.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(json.dumps(r,sort_keys=True))
if __name__=="__main__":main()
