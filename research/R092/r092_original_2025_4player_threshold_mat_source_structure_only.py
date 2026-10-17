#!/usr/bin/env python3
"""R092 source-only original Wang/Hilbe/Zhang 2025 thresholdPGG MATLAB audit.

Source MAT original data are NEVER loaded into application memory as arrays:
scipy.io.whosmat reads variable names, numeric types, and shapes only. No
individual action, actor ID, group ID, session or contribution values output.
"""
from __future__ import annotations
import argparse,hashlib,io,json,pathlib,re,urllib.request,urllib.parse,urllib.error
from scipy.io import whosmat
from scipy.io.matlab import MatReadError
ZENODO="https://zenodo.org"
RECORD="16918146"
FILE="ThresholdPGG_4P_ExperimentalData.mat"
URL=f"{ZENODO}/records/{RECORD}/files/{FILE}?download=1"
MD5="6036f73c2f758ab3aeed6dcf4f74585b"
MAX_BYTES=150000
SAFE_NAME=re.compile(r"^[A-Za-z][A-Za-z_0-9]{0,40}$")
SAFE_TYPES={"double","single","int8","int16","int32","int64",
 "uint8","uint16","uint32","uint64","logical","struct","cell","char","sparse"}

def check_destination(url):
 p=urllib.parse.urlparse(url)
 if p.scheme!="https" or p.hostname!="zenodo.org" or p.port is not None:
  raise ValueError("R092_AUTHOR_DOWNLOAD_UNTRUSTED_HOST")
 if p.path not in (f"/records/{RECORD}/files/{FILE}",
                   f"/api/records/{RECORD}/files/{FILE}/content"):
  raise ValueError("R092_UNPINNED_AUTHOR_FILE_URL")
 return True

def source_identity(data,md5=MD5):
 if not isinstance(data,bytes) or not 1<=len(data)<=MAX_BYTES:
  raise ValueError("R092_AUTHOR_ORIGINAL_BYTES_UNAVAILABLE_OR_OVERSIZE")
 actual=hashlib.md5(data).hexdigest()
 if actual!=md5:raise ValueError("R092_FIRST_PARTY_ORIGINAL_MD5_MISMATCH")
 return {"fixed_original_Zenodo_record":int(RECORD),"published_original_file":FILE,
   "original_author_MD5_exact":actual,
   "original_source_bytes":len(data),
   "original_whole_file_SHA256":hashlib.sha256(data).hexdigest()}

def anonymous_whosmat(data):
 try:raw=whosmat(io.BytesIO(data))
 except (ValueError,TypeError,NotImplementedError,OverflowError,OSError,IndexError,MatReadError) as e:
  raise ValueError("R092_UNSUPPORTED_ORIGINAL_MAT_STRUCTURE") from e
 if not raw or len(raw)>40:raise ValueError("R092_MAT_VARIABLE_COUNT_MISSING_OR_EXCESS")
 output=[]
 for name,shape,kind in raw:
  if not SAFE_NAME.fullmatch(name) or kind not in SAFE_TYPES:
   raise ValueError("R092_UNSAFE_MAT_VARIABLE_METADATA")
  if not isinstance(shape,tuple) or len(shape)>8 or any(not isinstance(n,int) or n<0 or n>5000000 for n in shape):
   raise ValueError("R092_UNEXPECTED_MAT_VARIABLE_DIMENSIONS")
  output.append({"variable_name":name,"shape":list(shape),"mat_variable_class":kind})
 return {"source_only_MAT_variables":output,
   "source_MAT_variable_count":len(output),
   "original_actor_values_or_group_ids_examined":False,
   "original_behavior_contributions_scored":False,
   "original_MAT_raw_values_republished":False}

def run_original():
 check_destination(URL)
 req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R092-first-party-2025-thresholdPGG-md5-shape-only/1.0"})
 with urllib.request.urlopen(req,timeout=60) as resp:
  check_destination(resp.geturl())
  b=resp.read(MAX_BYTES+1)
 ident=source_identity(b)
 return {"research_id":"R092",
  "phase":"A_ORIGINAL_AUTHOR_2025_FOURPLAYER_THRESHOLD_MAT_ONLY",
  "paper_data_DOI":"10.5281/zenodo.16918146",
  "first_party_original_source":ident,
  "original_source_structure":anonymous_whosmat(b),
  "author_stated_distinct_original_humans":276,
  "author_stated_4player_group_sessions_treatments":["FE","AI","MI"],
  "same_humans_repeated_in_two_sessions":True,
  "real_original_contribution_score_rows":0,
  "R092_experimental_repeated_group_transfer_E2":"NOT_YET_EVALUATED",
  "R091_experiment_positive_and_R090_negative_unchanged":True,
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 try:r=run_original()
 except (ValueError,OSError,TypeError,urllib.error.URLError,urllib.error.HTTPError) as e:
  safe=str(e)[:105] if isinstance(e,ValueError) and str(e).startswith("R092_") else "R092_AUTHOR_SOURCE_OR_MAT_STRUCTURE_FAIL_CLOSED"
  r={"research_id":"R092","phase":"A_ORIGINAL_AUTHOR_SOURCE_FORMAT_FAIL_CLOSED",
   "safe_failure":safe,"original_behavioral_scores":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n")
 print(json.dumps(r,sort_keys=True))
if __name__=="__main__":main()
