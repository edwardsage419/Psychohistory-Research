#!/usr/bin/env python3
"""R084 official OSF original-source METADATA ONLY eligibility probe.

Does NOT download original human rows, link-level records, or file bodies.
"""
from __future__ import annotations
import argparse,json,pathlib,re,urllib.parse,urllib.request,urllib.error
from collections import Counter

OSF_NODE="tyxfm"
OSF_COMPONENT="r7y9n"
OSF_FILE="fjyg3"
EXPECTED_UTRECHT_SHA256="f85367e8fff52c29384e51b48baa2b4efed4014c2ef08c00c9ec4549e6d65f3d"
# Both capability links are already disclosed in the authors' public 2023 article.
# NEVER include tokens in any written receipt, traceback, console logs or result.
PUBLISHED_TOKENS=("604fe6ace95d4e52b89ec8556c4fb304","5f560d5d570241eaa460b094aed074b4")
ALLOWED_HOSTS=frozenset({"api.osf.io","osf.io","share.osf.io"})
MAX_RESPONSE=1300000
MAX_FILES_PER_PAGE=100

def allow_public_original_https(url):
 u=urllib.parse.urlsplit(url)
 if u.scheme!="https" or u.hostname not in ALLOWED_HOSTS or u.username or u.password or u.port or u.fragment:
  raise ValueError("R084_OFFICIAL_HTTPS_HOST_REQUIRED")
 if not (u.path.startswith("/v2/nodes/") or u.path.startswith("/v2/files/")
         or (u.hostname=="osf.io" and u.path=="/tyxfm/")
         or (u.hostname=="share.osf.io" and u.path.startswith("/trove/index-card/"))):
  raise ValueError("R084_UNEXPECTED_OSF_OFFICIAL_METADATA_PATH")
 return True

def official_url(api_path, token):
 if token not in PUBLISHED_TOKENS:raise ValueError("R084_NON_PUBLISHED_ACCESS_CAPABILITY")
 if not api_path.startswith("/v2/"):raise ValueError("R084_UNEXPECTED_API_PATH")
 url="https://api.osf.io"+api_path+"?"+urllib.parse.urlencode({"view_only":token})
 allow_public_original_https(url)
 return url

def sanitized_error(error):
 if isinstance(error,urllib.error.HTTPError):return {"http_status":error.code,"metadata_json":False,"source_gate":"HTTP_REJECTED"}
 if isinstance(error,(urllib.error.URLError,TimeoutError,OSError)):
  return {"http_status":None,"metadata_json":False,"source_gate":"NETWORK_OR_TRANSPORT_UNREACHABLE"}
 if isinstance(error,(UnicodeDecodeError,ValueError,TypeError,json.JSONDecodeError)):
  return {"http_status":None,"metadata_json":False,"source_gate":"INVALID_JSON_OR_OSF_SCHEMA"}
 return {"http_status":None,"metadata_json":False,"source_gate":"UNKNOWN_FAILURE"}

def request_json(url):
 allow_public_original_https(url)
 request=urllib.request.Request(url,headers={
  "User-Agent":"Psychohistory-R084-source-metadata-only/1.0",
  "Accept":"application/vnd.api+json, application/json"})
 try:
  with urllib.request.urlopen(request,timeout=8) as res:
   stat=res.status
   content_type=res.headers.get("Content-Type","").split(";")[0].lower()
   data=res.read(MAX_RESPONSE+1)
   final_url=res.url
  # urllib follows redirects, disallow even if redirect was to a non-OSF host.
  if not allow_public_original_https(final_url):
   raise ValueError("R084_REDIRECT_TO_UNTRUSTED_DOMAIN")
  if len(data)>MAX_RESPONSE:raise ValueError("R084_OVERSIZE_METADATA_RESPONSE")
  if content_type not in ("application/json","application/vnd.api+json") and not content_type.endswith("+json"):
   return {"http_status":stat,"metadata_json":False,"source_gate":"NON_JSON_RESPONSE"},None
  obj=json.loads(data)
  if not isinstance(obj,dict) or "data" not in obj:
   raise ValueError("R084_OSF_JSON_ROOT_NO_DATA")
  return {"http_status":stat,"metadata_json":True,"source_gate":"JSON_RECEIVED"},obj
 except (urllib.error.HTTPError,urllib.error.URLError,TimeoutError,OSError,
         ValueError,UnicodeDecodeError,TypeError) as e:
  return sanitized_error(e),None

def metadata_summary(expected_id, response, obj):
 receipt=dict(response)
 receipt["original_id_match"]=False
 if obj is None:return receipt
 data=obj.get("data")
 if not isinstance(data,dict):
  receipt["source_gate"]="NO_SINGLE_OBJECT"
  return receipt
 if data.get("id")!=expected_id:
  receipt["source_gate"]="SOURCE_ID_MISMATCH"
  return receipt
 receipt["original_id_match"]=True
 attr=data.get("attributes") or {}
 receipt["original_resource_type"]=str(data.get("type",""))[:40]
 receipt["has_original_record_hashes"]=bool(attr.get("hashes"))
 receipt["has_original_schema_structure"]=bool(data.get("relationships"))
 if expected_id==OSF_FILE:
  receipt["official_filename_matches_index"]=attr.get("name")=="Utrecht_sbj.csv"
  hashes=attr.get("hashes") or {}
  receipt["indexed_file_sha256_matches"]=hashes.get("sha256")==EXPECTED_UTRECHT_SHA256
  receipt["original_file_size"]=attr.get("size") if isinstance(attr.get("size"),int) else None
  receipt["original_file_version"]=attr.get("version") if isinstance(attr.get("version"),int) else None
 # no private participant columns, IDs or raw metadata dict exported
 return receipt

def list_summary(response,obj):
 receipt=dict(response)
 receipt.update({"original_file_listing_count":None,
                 "original_file_listing_first_page_only":True,
                 "any_original_file_sha256_metadata":False,
                 "observed_public_csv_filenames":[]})
 if obj is None:return receipt
 data=obj.get("data")
 if not isinstance(data,list) or len(data)>MAX_FILES_PER_PAGE:
  receipt["source_gate"]="BAD_OR_OVERSIZE_OSF_FILES_COLLECTION"
  return receipt
 receipt["original_file_listing_count"]=len(data)
 receipt["original_file_listing_first_page_only"]=bool((obj.get("links") or {}).get("next"))
 receipt["any_original_file_sha256_metadata"]=any(
  isinstance(x,dict) and bool((x.get("attributes") or {}).get("hashes")) for x in data)
 names=[(x.get("attributes") or {}).get("name") for x in data if isinstance(x,dict)]
 # no generic filenames with possible subject secrets, only seven intended lab names
 allowed=re.compile(r"^(Bologna|Nuremberg|Utrecht|Valencia|Zurich|Oxford|Warsaw)(?:_[A-Za-z0-9_.-]{1,30})?\.(csv|dta|sav|xlsx|RData|rds)$",re.I)
 receipt["observed_public_csv_filenames"]=sorted(
  {x for x in names if isinstance(x,str) and allowed.fullmatch(x)})[:20]
 return receipt

def run_source_gate():
 checks=[]
 for token_index,token in enumerate(PUBLISHED_TOKENS,1):
  # publish only 1/2 token-index, NEVER capability secret or URL.
  for resource_id,prefix in ((OSF_NODE,"nodes"),(OSF_COMPONENT,"nodes"),(OSF_FILE,"files")):
   response,obj=request_json(official_url(f"/v2/{prefix}/{resource_id}/",token))
   checks.append({"published_author_link_number":token_index,
                  "original_resource":("study_root" if resource_id==OSF_NODE
                       else "original_replication_component" if resource_id==OSF_COMPONENT
                       else "first_party_Utrecht_csv_file"),
                  **metadata_summary(resource_id,response,obj)})
  for node in (OSF_NODE,OSF_COMPONENT):
   response,obj=request_json(official_url(f"/v2/nodes/{node}/files/",token))
   checks.append({"published_author_link_number":token_index,
                  "original_resource":"study_root_files" if node==OSF_NODE else "replication_component_files",
                  **list_summary(response,obj)})
 working=[x for x in checks if x["http_status"]==200 and x["metadata_json"] and
          (x.get("original_id_match") or x.get("original_file_listing_count") is not None)]
 source_gate="OFFICIAL_OSF_METADATA_PARTIALLY_ACCESSIBLE" if working else "OFFICIAL_OSF_ORIGINAL_METADATA_SOURCE_BLOCKED"
 file_verified=any(x.get("indexed_file_sha256_matches") is True for x in checks)
 return {
  "research_id":"R084","phase":"PHASE_A_OFFICIAL_ORIGINAL_OSF_METADATA_ONLY",
  "status":source_gate,
  "original_published_author_paper":"10.1093/pnasnexus/pgad091",
  "original_repo_identifiers":{"project":OSF_NODE,"author_component":OSF_COMPONENT,"indexed_website_file_id":OSF_FILE},
  "indexed_author_Utrecht_csv_sha256_from_trove":EXPECTED_UTRECHT_SHA256,
  "indexed_metadata_WAS_SEEN_IN_OSF_PUBLIC_SEARCH_BEFORE_THIS_RUN":True,
  "official_OSF_file_metadata_sha256_independently_confirmed":file_verified,
  "safe_official_http_checks":checks,
  "original_paper_report_only":{
   "labs":7,"groups_per_lab":12,"original_humans_per_group":12,
   "total_humans_published":1008,"rounds_per_human":30,
   "success_labs_published_by_original_authors":5,
   "replication_weak_or_fail_labs_published":["Oxford","Warsaw"],
   "not_currently_recomputed_by_R084":True},
  "original_human_row_files_downloaded":0,"original_human_outcomes_computed":0,
  "real_human_scientific_grade":"NOT_E2",
  "between_institution_causal_effect":"NOT_IDENTIFIED",
  "PESEN_v0.1":"FROZEN"}

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("--output",type=pathlib.Path,required=True)
 args=parser.parse_args()
 r=run_source_gate()
 args.output.parent.mkdir(parents=True,exist_ok=True)
 raw=json.dumps(r,sort_keys=True,indent=2,ensure_ascii=False)+"\n"
 if any(token in raw for token in PUBLISHED_TOKENS):
  raise RuntimeError("R084_CAPABILITY_TOKEN_LEAK_BLOCKED")
 args.output.write_text(raw,encoding="utf-8")
 print(json.dumps({"status":r["status"],
                   "metadata_sha_independently_confirmed":r["official_OSF_file_metadata_sha256_independently_confirmed"],
                   "resource_http_statuses":[z["http_status"] for z in r["safe_official_http_checks"]],
                   "human_rows_downloaded":r["original_human_row_files_downloaded"],
                   "PESEN_v0.1":r["PESEN_v0.1"]},sort_keys=True))
if __name__=="__main__":main()
