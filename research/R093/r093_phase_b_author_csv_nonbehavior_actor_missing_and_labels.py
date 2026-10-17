#!/usr/bin/env python3
"""R093 original Pereda file codebook/missing actor audit; no contribution scores."""
import argparse,collections,csv,io,json,pathlib,urllib.request,urllib.error
from collections import Counter,defaultdict
from r093_2019_first_party_zenodo_14day_large_group_source_eligibility import (
 URL,MAX_BYTES,verify_url,identity,SAFE_COL,SAFE_LABEL,REQUIRED)
def author_code(value):
 v=str(value or "").strip()
 if not v:return "MISSING_TREATMENT"
 return v if SAFE_LABEL.fullmatch(v) else "REDACTED_UNRECOGNIZED_TREATMENT"
def field_kind(value):
 s=str(value or "").strip()
 return s if s in ("0","1") else "EMPTY" if not s else "OTHER_NONBINARY"
def round_kind(value):
 s=str(value or "").strip()
 if s.isascii() and s.isdigit() and 1<=int(s)<=14:return str(int(s))
 return "OUTSIDE_1_TO_14_OR_EMPTY"
def anonymous_original_metadata(original):
 source=csv.reader(io.StringIO(original.decode("utf-8-sig"),newline=""))
 header=next(source,None)
 if header is None or not 6<=len(header)<=30 or not REQUIRED.issubset(header) or len(set(header))!=len(header) or any(not SAFE_COL.fullmatch(x) for x in header):
  raise ValueError("R093B_FIRST_PARTY_SCHEMA_HEADER_INVALID")
 loc={h:i for i,h in enumerate(header)}
 codes=Counter();missing_id=Counter();alive=defaultdict(Counter);rd=Counter();seen=set()
 dup=0;rows=0;missing_treatment=0
 for vals in source:
  if len(vals)!=len(header):raise ValueError("R093B_INCONSISTENT_ORIGINAL_CSV_ROW_WIDTH")
  label=author_code(vals[loc["treatment"]])
  person=vals[loc["participant_id"]].strip()
  t=round_kind(vals[loc["round_number"]])
  codes[label]+=1
  missing_id[label]+=int(not person)
  alive[label][field_kind(vals[loc["player_alive"]])]+=1
  rd[t]+=1
  missing_treatment+=int(label=="MISSING_TREATMENT")
  if person and label not in ("MISSING_TREATMENT","REDACTED_UNRECOGNIZED_TREATMENT") and t!="OUTSIDE_1_TO_14_OR_EMPTY":
   key=(label,person,t)
   if key in seen:dup+=1
   seen.add(key)
  rows+=1
 if not rows or len(codes)>20:raise ValueError("R093B_EMPTY_OR_TOO_MANY_SOURCE_LABELS")
 return {"source_original_column_names":header,"source_original_person_round_rows":rows,
  "safe_publisher_treatment_label_row_counts":dict(sorted(codes.items())),
  "source_missing_individual_ID_rows_by_publisher_treatment":dict(sorted(missing_id.items())),
  "source_player_alive_label_counts":{
    k:dict(sorted(v.items())) for k,v in sorted(alive.items())},
  "source_round_code_row_counts":dict(sorted(rd.items())),
  "source_fully_sanitized_duplicate_person_round_keys":dup,
  "source_missing_treatment_label_rows":missing_treatment,
  "contribution_column_numeric_values_examined":False,
  "original_person_source_ID_or_hashed_ID_exported":False}
def original():
 with urllib.request.urlopen(urllib.request.Request(URL,headers={
  "User-Agent":"Psychohistory-R093-original-Pereda-source-labels-and-missing-only/1.0"}),timeout=60) as r:
  verify_url(r.geturl());b=r.read(MAX_BYTES+1)
 ident=identity(b)
 return {"research_id":"R093","phase":"B_ORIGINAL_PUBLISHED_NONBEHAVIOR_MISSING_IDS_AND_EXPERIMENT_CODES",
  "original_first_party_MD5_SHA_identity":ident,
  "anonymized_source_fields_and_missingness":anonymous_original_metadata(b),
  "original_actor_contribution_values_computed":0,
  "prior_real_source_missing_actor_failure_retained":True,
  "R093_new_real_human_E2":"AWAITING_SEPARATE_ROSTER_AND_OUTCOME_PROTOCOL",
  "PESEN_v0.1":"FROZEN"}
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args()
 try:z=original()
 except (ValueError,OSError,UnicodeError,TypeError,urllib.error.URLError,urllib.error.HTTPError) as e:
  msg=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R093B_") else "R093B_AUTHOR_SOURCE_OR_NONBEHAVIOR_SCHEMA_FAIL_CLOSED"
  z={"research_id":"R093","phase":"B_ORIGINAL_SOURCE_METADATA_FAIL_CLOSED",
   "safe_failure":msg,"original_contribution_scores":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(z,indent=2,sort_keys=True)+"\n")
 print(json.dumps(z,sort_keys=True))
if __name__=="__main__":main()
