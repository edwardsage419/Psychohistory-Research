#!/usr/bin/env python3
"""R094 source-only first published secondary-curated Nishi network PGG CSV gate.

Strict Zenodo publisher MD5 before CSV. No participant, decision time, choice,
network link, session or original row VALUES read, aggregated, or exported.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,pathlib,re,urllib.parse,urllib.request,urllib.error

RECORD="19544006"
FILE="individual_data.csv"
MD5="85db2536b5be1cd50266900e61590d5a"
URL=f"https://zenodo.org/records/{RECORD}/files/{FILE}?download=1"
LIMIT=1500000
SAFE_NAME=re.compile(r"^[A-Za-z_][A-Za-z_0-9.]{0,80}$")

def source_url_valid(url):
 p=urllib.parse.urlsplit(url)
 if p.scheme!="https" or p.hostname!="zenodo.org" or p.port is not None or p.username or p.password:
  raise ValueError("R094_SOURCE_NOT_ZENODO")
 if p.path!=f"/records/{RECORD}/files/{FILE}":
  raise ValueError("R094_UNPINNED_SECONDARY_SOURCE_FILE")
 return True

def full_publisher_source_identity(raw,md5=MD5):
 if not isinstance(raw,bytes) or not 1<=len(raw)<=LIMIT:
  raise ValueError("R094_FIXED_SOURCE_BYTES_OUT_OF_RANGE")
 if hashlib.md5(raw).hexdigest()!=md5:
  raise ValueError("R094_OFFICIAL_PUBLISHER_MD5_MISMATCH")
 return {"fixed_Zenodo_record":int(RECORD),"author_secondary_curated_source":FILE,
  "fixed_publisher_MD5":md5,
  "raw_author_source_bytes":len(raw),
  "independently_computed_raw_SHA256":hashlib.sha256(raw).hexdigest()}

def schema_without_any_values(raw):
 try:s=raw.decode("utf-8-sig")
 except UnicodeError as e:raise ValueError("R094_AUTHOR_SECONDARY_CSV_NOT_UTF8") from e
 r=csv.reader(io.StringIO(s,newline=""))
 h=next(r,None)
 if (h is None or not 3<=len(h)<=80 or len(h)!=len(set(h))
     or any(not SAFE_NAME.fullmatch(x) for x in h)):
  raise ValueError("R094_SOURCE_CSV_COLUMN_HEADER_SYNTAX_REJECTED")
 n=0
 for line in r:
  if len(line)!=len(h):
   raise ValueError("R094_SECONDARY_SOURCE_CSV_ROW_WIDTH_NOT_UNIFORM")
  # Deliberately do NOT visit line values.
  n+=1
 if n<100:raise ValueError("R094_SOURCE_TOO_FEW_OBSERVATIONS")
 return {"original_publisher_safe_column_names":h,
  "original_data_row_count":n,
  "total_source_columns":len(h),
  "original_actor_group_session_ID_values_or_hashes_exported":False,
  "original_action_cooperation_time_network_values_examined":False,
  "original_data_cells_read_for_any_model":False}

def real_source():
 source_url_valid(URL)
 with urllib.request.urlopen(urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R094-2026-secondary-PGG-publisher-MD5-only/1.0"}),timeout=60) as r:
  source_url_valid(r.geturl());raw=r.read(LIMIT+1)
 ident=full_publisher_source_identity(raw)
 schema=schema_without_any_values(raw)
 return {"research_id":"R094","phase":"A_OFFICIAL_SECONDARY_AUTHOR_NETWORK_BINARY_PGG_CSV_SCHEMA_ONLY",
  "original_experiment_first_published_Nishi_2015_DOI":"10.1038/nature15392",
  "secondary_analysis_2026_DOI":"10.1371/journal.pone.0347919",
  "source_secondary_curated_dataset_DOI":"10.5281/zenodo.19544006",
  "publisher_source_identity":ident,"source_schema_no_behavior":schema,
  "original_secondary_curated_instead_of_raw_original_2015_logs":True,
  "R089_R090_R091_group_history_results_unmodified":True,
  "real_original_human_session_history_E2":"NOT_YET_EXECUTED",
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 try:r=real_source()
 except (ValueError,OSError,TypeError,UnicodeError,urllib.error.URLError,urllib.error.HTTPError) as e:
  reason=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R094_") else "R094_SECONDARY_PUBLISHER_SOURCE_SCHEMA_FAIL_CLOSED"
  r={"research_id":"R094","phase":"A_SECONDARY_PUBLISHER_CSV_SCHEMA_FAIL_CLOSED",
    "safe_failure":reason,"real_original_human_scores":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 print(json.dumps(r,sort_keys=True))
if __name__=="__main__":main()
