#!/usr/bin/env python3
"""R085 original Zenodo 16918146 two first-party four-human PGG MAT sources.

PHASE A is source identity/structural inspection ONLY. No human scores.
"""
from __future__ import annotations
import argparse,hashlib,io,json,pathlib,urllib.parse,urllib.request,urllib.error
from scipy.io import whosmat

DOI="10.5281/zenodo.16918146"
RECORD=16918146
SOURCES={
 "four_person_linear":{"filename":"LinearPGG_4P_ExperimentalData.mat",
                       "author_published_md5":"42153952f8e6614d09c2d903fd97af62",
                       "participants_by_arm_published":{"FE":100,"AI":104,"MI":108}},
 "four_person_threshold":{"filename":"ThresholdPGG_4P_ExperimentalData.mat",
                          "author_published_md5":"6036f73c2f758ab3aeed6dcf4f74585b",
                          "participants_by_arm_published":{"FE":76,"AI":100,"MI":100}}}
MAX_BYTES=200_000
ALLOWED=frozenset(("zenodo.org","www.zenodo.org"))

def source_url(name):
 if name not in {x["filename"] for x in SOURCES.values()}:
  raise ValueError("R085_NOT_AUTHOR_FROZEN_FILE")
 return f"https://zenodo.org/records/{RECORD}/files/"+urllib.parse.quote(name)+"?download=1"

def validate_canonical_url(value):
 parsed=urllib.parse.urlsplit(value)
 if parsed.scheme!="https" or parsed.hostname not in ALLOWED or parsed.username or parsed.password or parsed.port or parsed.fragment:
  raise ValueError("R085_NOT_OFFICIAL_ZENODO_HOST")
 if not parsed.path.startswith(f"/records/{RECORD}/files/"):
  raise ValueError("R085_NOT_FROZEN_RECORD_PATH")
 if ".." in urllib.parse.unquote(parsed.path).split("/"):
  raise ValueError("R085_TRAVERSAL_ATTEMPT")
 if urllib.parse.unquote(parsed.path.rsplit("/",1)[-1]) not in (x["filename"] for x in SOURCES.values()):
  raise ValueError("R085_NOT_ONE_OF_TWO_FROZEN_MAT_FILES")
 return True

def diagnostic(ex):
 if isinstance(ex,urllib.error.HTTPError):
  return f"AUTHOR_HOST_HTTP_{ex.code}"
 if isinstance(ex,urllib.error.URLError):return "SOURCE_NETWORK_UNREACHABLE"
 if isinstance(ex,(TimeoutError,OSError)):return "SOURCE_NETWORK_OR_FILE_IO"
 if isinstance(ex,ValueError):return str(ex)[:85] if str(ex).startswith("R085_") else "SOURCE_OR_MAT_VALIDATION_FAILED"
 return "SOURCE_UNEXPECTED_FAILURE"

def inspect_publisher_mat(source:bytes, expected_md5:str):
 if not isinstance(source,bytes) or not 1<=len(source)<=MAX_BYTES:
  raise ValueError("R085_SOURCE_FILE_EMPTY_OVERSIZED_OR_NONBINARY")
 md5=hashlib.md5(source).hexdigest()
 if md5!=expected_md5:raise ValueError("R085_ZENODO_AUTHOR_MD5_MISMATCH")
 try:variables=whosmat(io.BytesIO(source))
 except (ValueError,OSError,TypeError,IndexError,EOFError,NotImplementedError) as e:
  raise ValueError("R085_SCIPY_MAT_SCHEMA_OR_VERSION_UNSUPPORTED") from e
 if not variables:raise ValueError("R085_NO_MATLAB_VARIABLES")
 if len(variables)>100:raise ValueError("R085_TOO_MANY_MAT_VARIABLES")
 listing=[]
 for name,shape,kind in variables:
  if len(shape)>7 or any(not isinstance(n,int) or n<0 or n>200000 for n in shape):
   raise ValueError("R085_MAT_UNREASONABLE_VARIABLE_DIMENSIONS")
  listing.append({"variable_name":name[:100],"shape":list(shape),"mat_class":kind[:40]})
 return {"author_published_md5_match":True,
         "original_mat_bytes":len(source),
         "whole_original_file_sha256_computed":hashlib.sha256(source).hexdigest(),
         "mat_header_schema_valid":True,
         "original_variable_count":len(variables),
         "original_mat_variable_shapes_without_data":listing}

def probe_one(spec):
 result={"original_author_filename":spec["filename"],
         "original_author_published_md5":spec["author_published_md5"],
         "author_reported_participant_counts_not_recomputed":spec["participants_by_arm_published"],
         "source_identity_gate":"UNVERIFIED"}
 url=source_url(spec["filename"])
 validate_canonical_url(url)
 try:
  request=urllib.request.Request(url,headers={
   "User-Agent":"Psychohistory-R085-original-author-source-gate/1.0",
   "Accept":"application/octet-stream"})
  with urllib.request.urlopen(request,timeout=35) as response:
   status=response.status
   resolved=response.geturl()
   # Cross host CDN redirect forbidden until separately documented trust proof.
   validate_canonical_url(resolved)
   raw=response.read(MAX_BYTES+1)
  result["http_status"]=status
  result.update(inspect_publisher_mat(raw,spec["author_published_md5"]))
  result["source_identity_gate"]="AUTHOR_ORIGINAL_FILE_BYTES_MD5_VERIFIED_MAT_VARIABLES_INSPECTED"
 except (urllib.error.HTTPError,urllib.error.URLError,ValueError,TimeoutError,OSError,TypeError) as e:
  result["source_identity_gate"]="FAIL_CLOSED"
  result["source_failure_class"]=diagnostic(e)
  result["http_status"]=e.code if isinstance(e,urllib.error.HTTPError) else None
  result["original_raw_rows_or_values_exported"]=0
 return result

def run():
 files={k:probe_one(v) for k,v in SOURCES.items()}
 passed=all(x["source_identity_gate"]=="AUTHOR_ORIGINAL_FILE_BYTES_MD5_VERIFIED_MAT_VARIABLES_INSPECTED" for x in files.values())
 return {"research_id":"R085","phase":"A_PUBLISHER_ORIGINAL_FILE_ID_AND_MAT_SCHEMA_NO_REAL_BEHAVIOR_OUTCOME",
  "date":"2026-10-17",
  "source_DOI":DOI,"source_fixed_zenodo_record":RECORD,
  "publisher_source_gate":"PASS_TWO_AUTHOR_MD5_REAL_BYTES" if passed else "FAIL_CLOSED_NO_REAL_HUMAN_SCORE",
  "source_files":files,"original_behavior_row_values_computed":0,
  "original_human_action_metrics_computed":0,
  "source_metadata_class":"PUBLISHER_AUTHOR_PAPER_ORIGINAL_FILES",
  "evidence_grade":"E2_SOURCE_BYTES_ONLY_NO_BEHAVIORAL_ESTIMATE" if passed else "E0_AUTHOR_METADATA_E1_TESTS_SOURCE_BLOCKED",
  "original_person_ids_exported":False,"raw_matlab_files_exported":False,
  "research_design_causal_comparison":"NOT_IDENTIFIED",
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args()
 result=run()
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 print(json.dumps({"research_id":"R085","gate":result["publisher_source_gate"],
  "files":{k:{"source_identity_gate":v["source_identity_gate"],
               "source_failure_class":v.get("source_failure_class"),
               "original_mat_bytes":v.get("original_mat_bytes"),
               "whole_original_file_sha256_computed":v.get("whole_original_file_sha256_computed"),
               "original_mat_variable_shapes_without_data":v.get("original_mat_variable_shapes_without_data")}
           for k,v in result["source_files"].items()},
  "real_human_outcome_metrics_computed":0},sort_keys=True))
if __name__=="__main__":main()
