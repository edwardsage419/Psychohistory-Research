#!/usr/bin/env python3
"""R098 2025 Wang/Hilbe/Zhang original MAT publisher authentication — NO behavior.

Only header metadata from scipy.io.whosmat after exact v2 Zenodo publisher
MD5. Never scipy.io.loadmat, access contribution values, or actor identifiers.
"""
from __future__ import annotations
import argparse,hashlib,io,json,pathlib,urllib.parse,urllib.request,urllib.error
RECORD="16918146"
NAME="LinearPGG_4P_ExperimentalData.mat"
URL=f"https://zenodo.org/records/{RECORD}/files/{NAME}?download=1"
OFFICIAL_MD5="42153952f8e6614d09c2d903fd97af62"
CAP=100000
SAFE_NAME=__import__("re").compile(r"^[A-Za-z_][A-Za-z0-9_]{0,70}$")

def validate_url(u):
 p=urllib.parse.urlsplit(u)
 if p.scheme!="https" or p.netloc!="zenodo.org" or p.path!=f"/records/{RECORD}/files/{NAME}" or p.query not in ("","download=1"):
  raise ValueError("R098_ZENODO_PUBLISHER_ORIGINAL_V2_URL_NOT_PINNED")
 return True

def verify_original_bytes(b,official=OFFICIAL_MD5):
 if not isinstance(b,bytes) or not 1<=len(b)<=CAP:
  raise ValueError("R098_ORIGINAL_PUBLISHED_MAT_SIZE_INVALID")
 if hashlib.md5(b).hexdigest()!=official:
  raise ValueError("R098_PUBLISHER_ORIGINAL_FULL_MD5_MISMATCH")
 return {"source_original_publisher_record_ID":RECORD,
         "original_first_party_filename":NAME,
         "publisher_published_MD5":OFFICIAL_MD5,
         "full_original_source_bytes":len(b),
         "original_fullfile_computed_SHA256":hashlib.sha256(b).hexdigest()}

def mat_container_type(b):
 # Static fingerprint only, never expose user-supplied file header bytes.
 h=b"\x89HDF\r\n\x1a\n"
 if b.startswith(b"MATLAB 7.3 MAT-file") or any(b[k:k+8]==h for k in (0,512,1024)):
  return "MATLAB_7_3_OR_HDF5"
 if b.startswith(b"MATLAB "):return "MATLAB_LEGACY_V5"
 if len(b)>=20 and (b[:4] in (b"\x00\x00\x00\x00",b"\x00\x00\x07\xe8")):
  return "UNKNOWN_LEGACY_MAT"
 return "UNKNOWN_CONTAINER"

def mat_metadata(b):
 typ=mat_container_type(b)
 if typ=="MATLAB_7_3_OR_HDF5":
  import h5py
  try:
   # HDF5 keys, group and dataset shapes ONLY. NEVER dereference data arrays.
   with h5py.File(io.BytesIO(b),"r") as file:
    variables=[]
    for key in file.keys():
     if key=="#refs#":
      variables.append(("MATLAB_INTERNAL_REFS",(),"internal_group"))
      continue
     obj=file[key]
     if isinstance(obj,h5py.Group):
      variables.append((key,(),"group"))
     else:
      variables.append((key,tuple(int(x) for x in obj.shape),"hdf5_dataset_"+str(obj.dtype.kind)))
  except (ValueError,TypeError,KeyError,OSError,RuntimeError) as e:
   raise ValueError("R098_PUBLISHED_HDF5_MAT_DIRECTORY_NOT_SUPPORTED") from e
 else:
  # scipy whosmat enumerates MATLAB directories, not behavior matrices.
  from scipy.io import whosmat
  from scipy.io.matlab import MatReadError
  try:
   variables=whosmat(io.BytesIO(b))
  except (ValueError,TypeError,IndexError,NotImplementedError,MatReadError) as e:
   raise ValueError("R098_PUBLISHED_MAT_HEADER_NOT_SUPPORTED_"+typ+"_CLASS_"+(type(e).__name__ if type(e).__name__ in ("MatReadError","ValueError","NotImplementedError","TypeError","IndexError") else "OTHER")) from e
 if not 1<=len(variables)<=40:
  raise ValueError("R098_MAT_VARIABLE_COUNT_UNEXPECTED")
 safe=[]
 for name,shape,clazz in variables:
  if not SAFE_NAME.fullmatch(name) or not isinstance(shape,tuple) or len(shape)>5 or any((not isinstance(i,int) or i<0) for i in shape):
   raise ValueError("R098_MAT_ORIGINAL_VARIABLE_METADATA_UNSAFE")
  if not SAFE_NAME.fullmatch(clazz):
   raise ValueError("R098_MAT_ORIGINAL_VARIABLE_CLASS_UNSAFE")
  safe.append({"MAT_original_top_level_variable_name":name,
               "shape_dimensions":list(shape),
               "MAT_variable_container_class":clazz})
 return {"source_publisher_original_MAT_container_kind":typ,
         "source_metadata_only_variables":safe,
         "number_top_level_original_MAT_variables":len(safe),
         "actual_human_contribution_values_or_actor_group_codes_inspected":False,
         "individual_source_human_record_rows_republished":False,
         "MAT_full_data_arrays_loaded":False}

def original_source():
 validate_url(URL)
 req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R098-2025-original-4P-source-MD5-whosmat-no-human-choices/1.0"})
 with urllib.request.urlopen(req,timeout=55) as resp:
  validate_url(resp.geturl());b=resp.read(CAP+1)
 identity=verify_original_bytes(b)
 try:
  m=mat_metadata(b)
 except ValueError as e:
  return {"research_id":"R098",
    "phase":"A_AUTHENTIC_PUBLISHER_ORIGINAL_SOURCE_SCHEMA_INCOMPATIBLE",
    "status":"R098_PUBLISHER_SOURCE_MD5_SHA_VERIFIED_BUT_MAT_DIRECTORY_UNREADABLE",
    "safe_failure":str(e)[:140] if str(e).startswith("R098_") else "R098_UNSUPPORTED_MAT_METADATA",
    "original_author_dataset_DOI":"10.5281/zenodo.16918146",
    "original_source_byte_identity":identity,
    "MAT_publisher_header_128byte_SHA256":hashlib.sha256(b[:128]).hexdigest(),
    "MAT_container_version_bytes_hex":b[124:126].hex() if len(b)>=126 else "",
    "source_container_enum":mat_container_type(b),
    "actual_original_human_contributions_inspected":False,
    "real_human_contribution_model_scores":0,
    "PESEN_v0.1":"FROZEN"}
 return {"research_id":"R098","phase":"A_FIRST_PARTY_2025_ZENODO_4P_LINEARPGG_MAT_PUBLISHER_SOURCE_ONLY",
   "status":"R098_ORIGINAL_ZENODO_V2_FULL_MD5_AND_MAT_VARIABLE_DIRECTORY_VERIFIED",
   "original_author_dataset_DOI":"10.5281/zenodo.16918146",
   "original_source_byte_identity":identity,
   "original_nonbehavior_MAT_directory":m,
   "published_FE_AI_MI_people_per_treatment_reported_but_not_verified":[100,104,108],
   "two_original_sessions_same_human_subjects_so_not_independent_recruitment":True,
   "first_party_human_contribution_values_scored":0,
   "PESEN_v0.1":"FROZEN"}
def main():
 a=argparse.ArgumentParser();a.add_argument("--output",type=pathlib.Path,required=True);opts=a.parse_args()
 try:z=original_source()
 except (OSError,ValueError,KeyError,TypeError,urllib.error.URLError,urllib.error.HTTPError,ImportError) as e:
  msg=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R098_") else "R098_ORIGINAL_PUBLISHER_ZENODO_MAT_SOURCE_FAIL_CLOSED"
  z={"research_id":"R098","phase":"A_ORIGINAL_PUBLISHED_SOURCE_FAIL_CLOSED","status":"BLOCKED","safe_failure":msg,
     "real_human_contribution_model_scores":0,"PESEN_v0.1":"FROZEN"}
 opts.output.parent.mkdir(parents=True,exist_ok=True)
 opts.output.write_text(json.dumps(z,sort_keys=True,indent=2)+"\n")
 print(json.dumps(z,sort_keys=True))
 if z["status"] not in ("R098_ORIGINAL_ZENODO_V2_FULL_MD5_AND_MAT_VARIABLE_DIRECTORY_VERIFIED","R098_PUBLISHER_SOURCE_MD5_SHA_VERIFIED_BUT_MAT_DIRECTORY_UNREADABLE"):
  raise SystemExit(1)
if __name__=="__main__":main()
