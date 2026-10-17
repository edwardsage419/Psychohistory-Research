#!/usr/bin/env python3
"""R096 publisher Dryad original FP/SP CSV source identity & shape ONLY.

No personal identifiers, round values, choices, partner actions, payoffs, actor
or lab session data are ever extracted or exported. Fail-closed if source
unavailable, CSV invalid or official file URL not verifiably first-party.
"""
from __future__ import annotations
import argparse,csv,hashlib,io,json,pathlib,re,urllib.parse,urllib.request,urllib.error
ORIGINAL_DOI="10.5061/dryad.37pvmcvmk"
FILES={"fix.csv":1514373,"rand.csv":1514372,"README.txt":1514376}
CAP={"fix.csv":2000000,"rand.csv":2000000,"README.txt":10000}
NAME=re.compile(r"^[A-Za-z][A-Za-z0-9_. -]{0,60}$")
def official_urls(name):
 fid=FILES[name]
 return [f"https://datadryad.org/downloads/file_stream/{fid}",
         f"https://datadryad.org/api/v2/files/{fid}/download"]

def validate_published_url(name,url):
 p=urllib.parse.urlsplit(url)
 if p.scheme!="https" or p.netloc!="datadryad.org" or url not in official_urls(name):
  raise ValueError("R096_UNPINNED_ORIGIN_OR_ORIGINAL_FILE")
 return True

def original_csv_metadata(blob):
 try:text=blob.decode("utf-8-sig")
 except UnicodeError as e:raise ValueError("R096_PUBLISHER_CSV_ENCODING_UNREADABLE") from e
 it=csv.reader(io.StringIO(text,newline=""))
 head=next(it,None)
 if (head is None or not 3<=len(head)<=60 or len(head)!=len(set(head))
     or any(not NAME.fullmatch(n) for n in head)):
  raise ValueError("R096_ORIGINAL_CSV_HEADER_UNQUALIFIED")
 count=0
 for row in it:
  if len(row)!=len(head):raise ValueError("R096_ORIGINAL_CSV_ROW_WIDTH_INCONSISTENT")
  count+=1
 if count<100:raise ValueError("R096_ORIGINAL_SOURCE_TOO_FEW_ROWS")
 return {"safe_original_source_column_names":head,"total_original_csv_data_rows":count,
         "original_number_of_columns":len(head),
         "all_original_human_actions_outcomes_and_actor_or_session_values_unread":True,
         "original_microdata_republished":False}

def source_identity(b,name):
 if not isinstance(b,bytes) or not 1<=len(b)<=CAP[name]:
  raise ValueError("R096_ORIGINAL_SOURCE_BYTES_UNAVAILABLE_OR_EXCESS")
 return {"published_first_party_original_filename":name,
         "published_Dryad_source_file_id":FILES[name],
         "first_party_actual_raw_bytes":len(b),
         "first_party_actual_whole_file_SHA256":hashlib.sha256(b).hexdigest()}

def safe_redirect(original,final):
 p=urllib.parse.urlsplit(final)
 if p.scheme!="https" or p.hostname is None or p.username or p.password:
  raise ValueError("R096_ORIGINAL_PUBLISHER_REDIRECT_INSECURE")
 host=p.hostname.lower()
 if host not in ("datadryad.org","www.datadryad.org") and not (
   host.endswith(".amazonaws.com") or host.endswith(".cloudfront.net")
   or host.endswith(".datadryad.org")):
  raise ValueError("R096_ORIGINAL_PUBLISHER_REDIRECT_HOST_UNVERIFIED")
 return True

def fetch_one(name):
 attempts=[]
 for u in official_urls(name):
  validate_published_url(name,u)
  try:
   req=urllib.request.Request(u,headers={
     "User-Agent":"Psychohistory-R096-original-Dryad-2022-source-metadata-only/1.0",
     "Accept":"text/plain,text/csv,application/octet-stream,*/*"})
   with urllib.request.urlopen(req,timeout=24) as r:
    safe_redirect(u,r.geturl())
    b=r.read(CAP[name]+1)
   identity=source_identity(b,name)
   if name=="README.txt":
    # Only content identity; do not parse README actor-data examples.
    return {"status":"OFFICIAL_README_BYTES_VERIFIED_ONLY","identity":identity,
     "original_readme_content_republished":False,
     "source_attempts_prior_to_success":attempts}
   return {"status":"ORIGINAL_PUBLISHED_CSV_SCHEMA_ACCEPTED",
           "identity":identity,"source_schema":original_csv_metadata(b),
           "source_attempts_prior_to_success":attempts}
  except urllib.error.HTTPError as e:
   attempts.append({"endpoint":"file_stream" if "file_stream" in u else "official_api",
                    "safe_error":"HTTP_"+str(int(e.code))})
  except (urllib.error.URLError,OSError,TimeoutError,ValueError,UnicodeError,TypeError) as e:
   msg=str(e)
   attempts.append({"endpoint":"file_stream" if "file_stream" in u else "official_api",
     "safe_error":msg if isinstance(e,ValueError) and msg.startswith("R096_") else "DOWNLOAD_OR_FORMAT_FAIL_CLOSED"})
 return {"status":"ORIGINAL_DRYAD_SOURCE_ACCESS_OR_FORMAT_BLOCKED",
         "publisher_file":name,
         "safe_first_party_attempts":attempts,
         "human_experiment_actions_scored":0}

def run():
 r={k:fetch_one(k) for k in ("README.txt","fix.csv","rand.csv")}
 eligible=all(r[k]["status"]=="ORIGINAL_PUBLISHED_CSV_SCHEMA_ACCEPTED" for k in ("fix.csv","rand.csv"))
 return {"research_id":"R096","phase":"A_ORIGINAL_2022_DRYAD_100ROUND_SOURCE_BYTE_AND_SCHEMA_ONLY",
  "publisher_dataset_DOI":ORIGINAL_DOI,
  "published_study_12_sessions_188_people_not_independently_checked":True,
  "published_fixed_FP_6_sessions_92_people_not_independently_checked":True,
  "published_shuffled_SP_6_sessions_96_people_not_independently_checked":True,
  "official_first_party_source_files":r,
  "R096_first_party_original_FP_and_SP_CSV_both_eligible_for_next_roster_gate":eligible,
  "real_original_binary_human_cooperation_scoring_performed":False,
  "real_original_session_identity_verified_from_source":False,
  "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",required=True,type=pathlib.Path)
 a=p.parse_args()
 r=run()
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(r,sort_keys=True,indent=2)+"\n",encoding="utf8")
 print(json.dumps(r,sort_keys=True))
 if not r["R096_first_party_original_FP_and_SP_CSV_both_eligible_for_next_roster_gate"]:
  raise SystemExit(1)
if __name__=="__main__":main()
