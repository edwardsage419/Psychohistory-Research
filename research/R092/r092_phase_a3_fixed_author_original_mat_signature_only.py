#!/usr/bin/env python3
"""R092 source-file-type signals only, never source header contents or actor arrays."""
from __future__ import annotations
import argparse,io,json,pathlib,urllib.request,urllib.error
from scipy.io import whosmat
from r092_original_2025_4player_threshold_mat_source_structure_only import (
 URL,source_identity,check_destination,MAX_BYTES)
HDF=b"\x89HDF\r\n\x1a\n"
OFFSETS=(0,512,1024,2048,4096,8192)

def binary_format_flags(b):
 if not isinstance(b,bytes) or not b:raise ValueError("R092A3_EMPTY_AUTHOR_SOURCE")
 hdf_positions=[i for i in OFFSETS if b[i:i+8]==HDF]
 alpha_count=sum(x in range(32,127) or x in (9,10,13) for x in b[:min(128,len(b))])
 fmt={
 "HDF5_known_safe_signature_offsets":hdf_positions,
 "MATLAB_5_header_prefix":b.startswith(b"MATLAB 5.0 MAT-file"),
 "MATLAB_7_3_header_prefix":b.startswith(b"MATLAB 7.3 MAT-file"),
 "ZIP_magic_prefix":b.startswith(b"PK\x03\x04"),
 "GZIP_magic_prefix":b.startswith(b"\x1f\x8b"),
 "CDF_netCDF_magic_prefix":b.startswith(b"CDF"),
 "top_128_byte_printable_fraction":alpha_count/min(128,len(b)),
 }
 try:
  z=whosmat(io.BytesIO(b))
  fmt["scipy_mat_whosmat_source_schema_status"]="ACCEPTED" if 0<len(z)<=40 else "EMPTY_OR_TOO_MANY"
  fmt["scipy_exception_class_if_denied"]=None
 except Exception as e:
  fmt["scipy_mat_whosmat_source_schema_status"]="DENIED"
  fmt["scipy_exception_class_if_denied"]=type(e).__name__ if type(e).__name__ in (
   "MatReadError","ValueError","TypeError","NotImplementedError",
   "OSError","IndexError","OverflowError","FileNotFoundError") else "OTHER_CLASS"
 fmt["author_original_values_or_ids_exported"]=False
 fmt["real_human_behavior_read"]=False
 return fmt

def fetch():
 with urllib.request.urlopen(urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R092-locked-binary-format-signature-only/1.0"}),timeout=60) as r:
  check_destination(r.geturl());raw=r.read(MAX_BYTES+1)
 ident=source_identity(raw)
 typ=binary_format_flags(raw)
 inferred=("MATLAB_5" if typ["MATLAB_5_header_prefix"] else
           "MATLAB_7_3" if typ["MATLAB_7_3_header_prefix"] else
           "HDF5" if typ["HDF5_known_safe_signature_offsets"] else
           "ZIP" if typ["ZIP_magic_prefix"] else
           "GZIP" if typ["GZIP_magic_prefix"] else
           "UNKNOWN_MAT_FILE_FORMAT_BLOCKED")
 return {"research_id":"R092",
  "phase":"A3_ORIGINAL_AUTHOR_FIXED_MD5_FORMAT_SIGNATURE_NO_ACTOR_ARRAY",
  "published_original_DOI":"10.5281/zenodo.16918146",
  "source_identity":ident,"original_author_source_format_flags":typ,
  "nonbehavioral_format_classification":inferred,
  "whosmat_and_HDF5_source_failures_preserved":True,
  "actual_original_human_behavioral_scores_computed":False,
  "R092_real_group_E2_evidence":"NOT_ESTABLISHED",
  "PESEN_v0.1":"FROZEN"}
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 try:r=fetch()
 except (ValueError,OSError,TypeError,urllib.error.URLError,urllib.error.HTTPError) as e:
  safe=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R092_") else "R092A3_SOURCE_AUTHENTICITY_OR_FORMAT_AUDIT_FAILED"
  r={"research_id":"R092","phase":"A3_FILE_FORMAT_SOURCE_FAIL_CLOSED",
   "safe_failure":safe,"original_actor_behavior_values_read":False,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(json.dumps(r,sort_keys=True))
if __name__=="__main__":main()
