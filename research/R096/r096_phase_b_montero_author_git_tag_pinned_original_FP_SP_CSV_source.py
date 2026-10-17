#!/usr/bin/env python3
"""R096 first-party researcher-submission CSV full Git blob identity, schema only.

Never examine source action cells, subject/session labels, action counts or
original row values. Verifies pinned author commit AND exact original Git blob.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,pathlib,re,urllib.parse,urllib.request,urllib.error

AUTHOR="eladiomontero"
REPO="PairwiseStrategies"
COMMIT="4743f74d8a03a031b8f70aff64956f8ad5155182"
FILES={
 "fix.csv":{"bytes":988279,"blob":"3bf78bf85f6642afee18d6f1965dca7272582f40"},
 "rand.csv":{"bytes":1112614,"blob":"f5a86cd033b739da45d3fc7c5019068f612146a2"}}
CAP=1400000
SAFE_HEADER=re.compile(r"^[A-Za-z_][A-Za-z0-9_ .:()/-]{0,65}$")

def raw_url(name):
 if name not in FILES:raise ValueError("R096B_UNPINNED_ORIGINAL_AUTHOR_FILE")
 return f"https://raw.githubusercontent.com/{AUTHOR}/{REPO}/{COMMIT}/{name}"

def validate_raw_url(url,name):
 p=urllib.parse.urlparse(url)
 if p.scheme!="https" or p.netloc!="raw.githubusercontent.com" or p.query or p.fragment or url!=raw_url(name):
  raise ValueError("R096B_ORIGINAL_AUTHOR_FIXED_GIT_FILE_CHANGED")
 return True

def git_blob(data):
 return hashlib.sha1(b"blob "+str(len(data)).encode("ascii")+b"\0"+data).hexdigest()

def verify_author_blob(data,name):
 if not isinstance(data,bytes) or len(data)>CAP or len(data)!=FILES[name]["bytes"]:
  raise ValueError("R096B_ORIGINAL_AUTHOR_GIT_TREE_BYTE_LENGTH_MISMATCH")
 if git_blob(data)!=FILES[name]["blob"]:
  raise ValueError("R096B_ORIGINAL_AUTHOR_FIXED_COMMIT_GIT_BLOB_MISMATCH")
 return {"original_author_repository":f"{AUTHOR}/{REPO}",
  "fixed_author_submission_commit":COMMIT,"original_file":name,
  "whole_original_author_bytes":len(data),
  "original_git_blob_SHA1":git_blob(data),
  "full_original_whole_file_SHA256":hashlib.sha256(data).hexdigest(),
  "source_is_identical_to_Dryad_publication_file":False}

def safe_original_csv_schema(data):
 try:txt=data.decode("utf-8-sig")
 except UnicodeError as e:raise ValueError("R096B_ORIGINAL_AUTHOR_SOURCE_CSV_NOT_UTF8") from e
 r=csv.reader(io.StringIO(txt,newline=""))
 h=next(r,None)
 if (h is None or not 3<=len(h)<=80 or len(h)!=len(set(h)) or
     any(not SAFE_HEADER.fullmatch(v) for v in h)):
  raise ValueError("R096B_AUTHOR_SUBMISSION_CSV_COLUMN_NAMES_UNSAFE_OR_UNEXPECTED")
 count=0
 for row in r:
  if len(row)!=len(h):raise ValueError("R096B_AUTHOR_SUBMISSION_CSV_WIDTH_INCONSISTENT")
  count+=1
 if count<1000:raise ValueError("R096B_AUTHOR_SUBMISSION_TOO_FEW_SOURCE_ROWS")
 return {"original_author_published_CSV_safe_headers_only":h,
  "original_author_source_actor_action_row_count_NOT_YET_VALIDATED":count,
  "original_author_source_csv_columns":len(h),
  "original_human_action_values_or_round_person_session_values_ever_examined":False,
  "original_microdata_person_identifiers_republished":False}

def original():
 results={}
 for name in ("fix.csv","rand.csv"):
  url=raw_url(name);validate_raw_url(url,name)
  try:
   req=urllib.request.Request(url,headers={
    "User-Agent":"Psychohistory-R096-2022-author-fixed-git-blob-source-only/1.0"})
   with urllib.request.urlopen(req,timeout=55) as resp:
    validate_raw_url(resp.geturl(),name)
    b=resp.read(CAP+1)
   identity=verify_author_blob(b,name)
   shape=safe_original_csv_schema(b)
   results[name]={"status":"FIXED_AUTHOR_GIT_BLOB_SHA1_VERIFIED_SOURCE_SCHEMA_ONLY",
                  "source_identity":identity,"no_behavioral_source_schema":shape}
  except (ValueError,urllib.error.HTTPError,urllib.error.URLError,OSError,UnicodeError) as e:
   label=str(e)[:110] if isinstance(e,ValueError) and str(e).startswith("R096B_") else "R096B_PINNED_AUTHOR_SOURCE_UNAVAILABLE_FAIL_CLOSED"
   results[name]={"status":"PINNED_AUTHOR_FILE_SOURCE_OR_SCHEMA_BLOCKED",
                  "safe_error":label,"original_source_actions_scored":0}
 passed=all(results[n]["status"]=="FIXED_AUTHOR_GIT_BLOB_SHA1_VERIFIED_SOURCE_SCHEMA_ONLY" for n in FILES)
 return {"research_id":"R096","phase":"B_FIRST_PARTY_2022_RESEARCHER_SUBMISSION_PINNED_GIT_BLOB_SOURCE_SCHEMA",
  "source_not_identical_by_identity_to_Dryad_2022_published_files":True,
  "original_Dryad_access_403_and_401_prior_failure_preserved":True,
  "original_author_data_at_exact_commit":results,
  "both_original_author_source_CSVs_passed_full_fixed_Git_blob":passed,
  "full_session_loso_12_sessions_reconstructed":False,
  "original_repeated_game_real_human_behavior_model_scored":False,
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args();o=original()
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(o,sort_keys=True,indent=2)+"\n")
 print(json.dumps(o,sort_keys=True))
 if not o["both_original_author_source_CSVs_passed_full_fixed_Git_blob"]:
  raise SystemExit(1)
if __name__=="__main__":main()
