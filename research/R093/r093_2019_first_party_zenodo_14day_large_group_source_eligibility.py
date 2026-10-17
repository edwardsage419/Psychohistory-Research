#!/usr/bin/env python3
"""R093: published Pereda et al. raw 14-day large-group PGG source metadata only.

Author Zenodo full MD5 verified first. Never inspect, evaluate or export
player_contribution / group_avg_contribution contents, IDs, or personal info.
"""
from __future__ import annotations
import argparse,collections,csv,hashlib,io,json,pathlib,re,urllib.parse,urllib.request,urllib.error
from collections import Counter,defaultdict
RECORD="2590686"
FILE="2017A2ECOCOOPANSA01ONL0000ESPMAD.csv"
URL=f"https://zenodo.org/records/{RECORD}/files/{FILE}?download=1"
PUBLISHER_MD5="626c61c2c18a114a5b92a7d2b7e46558"
MAX_BYTES=1200000
SAFE_COL=re.compile(r"^[a-z][a-z0-9_]{0,48}$")
SAFE_LABEL=re.compile(r"^[A-Za-z0-9_ .-]{1,20}$")
REQUIRED={"participant_id","player_alive","group_avg_contribution",
          "player_contribution","round_number","treatment"}
def verify_url(url):
 p=urllib.parse.urlsplit(url)
 if p.scheme!="https" or p.netloc!="zenodo.org" or p.path!=f"/records/{RECORD}/files/{FILE}":
  raise ValueError("R093_NONORIGINAL_OR_REDIRECTED_FIRST_PARTY_SOURCE")
 return True

def identity(original,expected_md5=PUBLISHER_MD5):
 if not isinstance(original,bytes) or not 1<=len(original)<=MAX_BYTES:
  raise ValueError("R093_UNAVAILABLE_OR_OVERSIZE_ORIGINAL_BYTES")
 if hashlib.md5(original).hexdigest()!=expected_md5:
  raise ValueError("R093_PUBLISHED_AUTHOR_SOURCE_MD5_MISMATCH")
 return {"original_publisher_record":int(RECORD),"original_first_party_file":FILE,
         "original_publisher_MD5_verified":True,"actual_first_party_MD5":expected_md5,
         "original_source_bytes":len(original),
         "original_full_file_SHA256":hashlib.sha256(original).hexdigest()}
def source_round(value):
 t=str(value).strip()
 if not t.isascii() or not t.isdigit() or not 1<=int(t)<=14:
  raise ValueError("R093_ORIGINAL_SOURCE_ROUND_OUTSIDE_1_14")
 return int(t)
def source_alive(value):
 if value not in ("0","1"):
  raise ValueError("R093_ORIGINAL_SOURCE_PLAYER_ALIVE_UNEXPECTED")
 return value

def structured_roster(original):
 try:text=original.decode("utf-8-sig")
 except UnicodeDecodeError as e:raise ValueError("R093_PUBLISHED_SOURCE_ENCODING_NOT_UTF8") from e
 src=csv.reader(io.StringIO(text,newline=""))
 try:header=next(src)
 except StopIteration:raise ValueError("R093_EMPTY_AUTHOR_CSV")
 if (not 6<=len(header)<=30 or len(header)!=len(set(header)) or
     any(not SAFE_COL.fullmatch(x) for x in header) or
     not REQUIRED.issubset(header)):
  raise ValueError("R093_FIRST_PARTY_SOURCE_HEADER_SCHEMA_INCOMPATIBLE")
 loc={h:i for i,h in enumerate(header)}
 counts=Counter();alive=Counter();rounds=Counter();ids=defaultdict(set)
 seen=set();duplicates=0;total=0
 for row in src:
  if len(row)!=len(header):raise ValueError("R093_ORIGINAL_CSV_ROW_WIDTH_MISMATCH")
  tr=row[loc["treatment"]].strip();player=row[loc["participant_id"]].strip()
  if not SAFE_LABEL.fullmatch(tr) or not player:
   raise ValueError("R093_EXPERIMENT_CODE_OR_PARTICIPANT_EMPTY")
  if len(tr)>20:raise ValueError("R093_EXPERIMENT_CODE_TOO_LONG")
  t=source_round(row[loc["round_number"]])
  alivecode=source_alive(row[loc["player_alive"]].strip())
  key=(tr,player,t)
  if key in seen:duplicates+=1
  seen.add(key)
  ids[tr].add(player)
  counts[tr]+=1;rounds[t]+=1;alive[(tr,alivecode)]+=1
  total+=1
 if not total or len(counts)>15:raise ValueError("R093_EMPTY_OR_TOO_MANY_AUTHOR_EXPERIMENTS")
 return {
  "original_verified_CSV_columns":header,
  "original_source_actor_round_rows":total,
  "source_distinct_treatment_experiments":len(counts),
  "source_rounds_observed_and_row_counts":{str(k):v for k,v in sorted(rounds.items())},
  "source_anonymized_experiment_metadata":{
     t:{"actor_round_source_rows":counts[t],
        "distinct_original_source_person_id_codes":len(ids[t]),
        "source_alive_1_rows":alive[(t,"1")],
        "source_alive_0_rows":alive[(t,"0")]} for t in sorted(counts)},
  "duplicate_original_treatment_person_round_keys":duplicates,
  "source_individual_IDs_or_original_actor_rows_exported":False,
  "source_contribution_or_original_group_mean_values_examined":False,
  "real_original_cooperation_model_scoring_performed":False}

def actual_original():
 verify_url(URL)
 req=urllib.request.Request(URL,headers={"User-Agent":"Psychohistory-R093-Pereda-published-source-md5-only/1.0"})
 with urllib.request.urlopen(req,timeout=60) as resp:
  verify_url(resp.geturl());b=resp.read(MAX_BYTES+1)
 ident=identity(b)
 roster=structured_roster(b)
 return {"research_id":"R093","phase":"A_PEREDA_2019_ZENODO_AUTHOR_MD5_SOURCE_STRUCTURE_ONLY",
 "scientific_article_DOI":"10.1038/s41598-019-50964-w",
 "author_data_DOI":"10.5281/zenodo.2590686",
 "first_party_identity":ident,"source_nonbehavioral_roster":roster,
 "R089_R090_R091_group_holdout_direct_transfer_eligible":False,
 "R093_individual_heldout_hypothesis":"NOT_YET_FROZEN_FOR_REAL_SCORES",
 "automatic_imputation_identified_from_player_alive_flag":False,
 "E2_true_real_human_model_scores":"NOT_YET_EXECUTED",
 "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args()
 try:z=actual_original()
 except (ValueError,OSError,TypeError,urllib.error.URLError,urllib.error.HTTPError,UnicodeError) as e:
  msg=str(e)[:105] if isinstance(e,ValueError) and str(e).startswith("R093_") else "R093_PUBLISHED_FIRST_PARTY_SOURCE_READ_FAILED"
  z={"research_id":"R093","phase":"A_ORIGINAL_PUBLISHED_SOURCE_FAIL_CLOSED",
     "safe_failure":msg,"original_human_behavioral_scores":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(z,sort_keys=True,indent=2)+"\n")
 print(json.dumps(z,sort_keys=True))
if __name__=="__main__":main()
