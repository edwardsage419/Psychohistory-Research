#!/usr/bin/env python3
"""R099: genuine PLOS ONE 2024 author S1 Data CSV first-party ONLY.

Read source full bytes, derive SHA256 and safe CSV column names and row count.
Never examine/print any cell values, human IDs, actual contributions or sessions.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,pathlib,re,urllib.parse,urllib.request,urllib.error
URL="https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0299196.s002&type=supplementary"
ARTICLE_DOI="10.1371/journal.pone.0299196"
DATA_DOI=ARTICLE_DOI+".s002"
MAX_CSV=250000
SAFE=re.compile(r"^[A-Za-z_][A-Za-z0-9_ .()/:#-]{0,90}$")
def check_publisher_url(url):
 p=urllib.parse.urlsplit(url)
 if p.scheme!="https" or p.netloc!="journals.plos.org" or p.path!="/plosone/article/file" or p.query not in ("id=10.1371/journal.pone.0299196.s002&type=supplementary","type=supplementary&id=10.1371/journal.pone.0299196.s002"):
  raise ValueError("R099_PLOS_ORIGINAL_S1_CSV_PUBLISHER_FILE_URL_NOT_PINNED")
 return True
def verify_bytes(b):
 if not isinstance(b,bytes) or not 100<=len(b)<=MAX_CSV:
  raise ValueError("R099_ORIGINAL_PLOS_S1_CSV_SIZE_INVALID_OR_UNAVAILABLE")
 return {"publisher_original_file_URL":URL,
         "exact_original_CSV_bytes":len(b),
         "original_first_party_fullfile_SHA256":hashlib.sha256(b).hexdigest(),
         "publisher_original_has_independent_reported_official_MD5":False,
         "original_source_human_action_data_unavailable_in_public_GitHub":True}
def source_safe_columns(b):
 try:text=b.decode("utf-8-sig")
 except UnicodeError as e:raise ValueError("R099_ORIGINAL_PLOS_CSV_NOT_UTF8") from e
 rdr=csv.reader(io.StringIO(text,newline=""))
 cols=next(rdr,None)
 if not cols or not 3<=len(cols)<=120 or len(cols)!=len(set(cols)) or any(not SAFE.fullmatch(k) for k in cols):
  raise ValueError("R099_ORIGINAL_PLOS_CSV_SOURCE_HEADER_NOT_SAFE")
 n=0
 for row in rdr:
  if len(row)!=len(cols):
   raise ValueError("R099_ORIGINAL_PLOS_CSV_ROW_WIDTH_NOT_CONSISTENT")
  n+=1
 if n<96:
  raise ValueError("R099_ORIGINAL_PLOS_CSV_ROW_COUNT_TOO_SMALL")
 return {"original_source_columns_only":cols,
         "original_source_rows_NOT_YET_VERIFIED_AS_REPEATED_PLAYER_ACTIONS":n,
         "column_count":len(cols),
         "original_human_contribution_values_examined":False,
         "original_player_session_group_ID_values_examined":False,
         "original_microdata_redistributed":False}
def original():
 check_publisher_url(URL)
 with urllib.request.urlopen(urllib.request.Request(URL,headers={
  "User-Agent":"Psychohistory-R099-first-party-2024-PLOS-original-CSV-schema-NO-HUMAN-ROWS/1.0",
  "Accept":"text/csv,application/octet-stream,*/*"}),timeout=40) as r:
  check_publisher_url(r.geturl())
  b=r.read(MAX_CSV+1)
 fileid=verify_bytes(b);shape=source_safe_columns(b)
 return {"research_id":"R099","phase":"A_ORIGINAL_2024_PLOS_CSV_SCHEMA_AND_SOURCE_BYTE_ONLY",
  "status":"R099_PLOS_FIRST_PARTY_ORIGINAL_S1_CSV_SOURCE_IDENTITY_AND_COLUMNS_VERIFIED",
  "article_DOI":ARTICLE_DOI,"publisher_S1_data_DOI":DATA_DOI,
  "original_source":fileid,"anonymous_source_metadata":shape,
  "eight_independent_2024_recruited_sessions_from_paper_not_source_yet":True,
  "first_party_original_real_human_contribution_models_scored":0,
  "PESEN_v0.1":"FROZEN"}
def main():
 ap=argparse.ArgumentParser();ap.add_argument("--output",type=pathlib.Path,required=True);a=ap.parse_args()
 try:z=original()
 except (ValueError,UnicodeError,OSError,TypeError,urllib.error.URLError,urllib.error.HTTPError) as e:
  err=(str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R099_") else
       "R099_PLOS_FIRST_PARTY_ORIGINAL_SOURCE_ACCESS_OR_STRUCTURE_BLOCKED")
  z={"research_id":"R099","status":"R099_ORIGINAL_S1_CSV_NOT_YET_VERIFIED",
     "phase":"A_ORIGINAL_SOURCE_FAIL_CLOSED","safe_error":err,
     "original_human_behavioral_model_scores":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n")
 print(json.dumps(z,sort_keys=True))
 if z["status"]!="R099_PLOS_FIRST_PARTY_ORIGINAL_S1_CSV_SOURCE_IDENTITY_AND_COLUMNS_VERIFIED":
  raise SystemExit(1)
if __name__=="__main__":main()
