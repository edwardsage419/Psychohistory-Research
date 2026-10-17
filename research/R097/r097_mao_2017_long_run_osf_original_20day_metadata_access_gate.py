#!/usr/bin/env python3
"""R097: 2017 Mao et al *OSF file catalog only*, not an action-data reader.

Preserves original source access failures. The original group recruited same
people over 20 days; number of days is NOT independently assigned cohorts.
"""
from __future__ import annotations
import argparse,collections,json,pathlib,re,urllib.parse,urllib.request,urllib.error
from collections import Counter
NODE="64z8u"
BASE=f"https://api.osf.io/v2/nodes/{NODE}/"
LIST=BASE+"files/osfstorage/?page%5Bsize%5D=100"
MAX_JSON=1400000
EXTENSION_ALLOW={"csv","tsv","txt","json","rdata","rds","dta","sav","xlsx","xls","zip","gz","pdf","md","ipynb","r","py","js"}
def validate_catalog_url(url):
 p=urllib.parse.urlsplit(url)
 if p.scheme!="https" or p.hostname!="api.osf.io" or p.username or p.password:
  raise ValueError("R097_OSF_ORIGINAL_API_INVALID_URL_OR_HOST")
 if p.path not in (f"/v2/nodes/{NODE}/",f"/v2/nodes/{NODE}/files/osfstorage/"):
  raise ValueError("R097_OSF_ORIGINAL_PROJECT_NODE_SCOPE_MISMATCH")
 return True

def extension_group(name):
 n=str(name or "")
 if not n or n.startswith(".") or "/" in n or "\\" in n:return "UNSAFE_OR_FOLDER"
 ext=n.rsplit(".",1)[-1].lower() if "." in n else "NO_EXTENSION"
 return ext if ext in EXTENSION_ALLOW else "OTHER_FILE_TYPE"

def safe_project_metadata(j):
 if not isinstance(j,dict) or not isinstance(j.get("data"),dict):
  raise ValueError("R097_OSF_ORIGINAL_PROJECT_METADATA_NOT_JSONAPI")
 z=j["data"]
 if z.get("id")!=NODE or z.get("type")!="nodes":
  raise ValueError("R097_OSF_ORIGINAL_PROJECT_NODE_ID_NOT_MATCHED")
 attrs=z.get("attributes") or {}
 return {"source_project_ID":NODE,
  "original_OSF_public_project":attrs.get("public") is True,
  "original_study_title_not_exported_to_avoid_untrusted_text":True,
  "original_human_microdata_or_action_values_read":False}

def safe_file_catalog(j):
 if not isinstance(j,dict) or not isinstance(j.get("data"),list):
  raise ValueError("R097_OSF_ORIGINAL_FILE_INDEX_NOT_JSONAPI")
 kinds=Counter();extensions=Counter();published_hashes=0
 potential=0;bytes_sizes=[];count=0
 for o in j["data"]:
  if not isinstance(o,dict) or o.get("type")!="files":
   raise ValueError("R097_OSF_ORIGINAL_FILE_OBJECT_INVALID")
  attrs=o.get("attributes") or {}
  typ=str(attrs.get("kind") or "UNKNOWN").lower()
  if typ not in ("file","folder"):raise ValueError("R097_OSF_ORIGINAL_UNEXPECTED_FILE_KIND")
  kinds[typ]+=1;count+=1
  if typ=="file":
   ext=extension_group(attrs.get("name"))
   extensions[ext]+=1
   if ext in ("csv","tsv","txt","json","rdata","rds","dta","sav","xlsx","xls","zip","gz"):
    potential+=1
   size=attrs.get("size")
   if isinstance(size,int) and size>=0:bytes_sizes.append(size)
   extra=attrs.get("extra") or {}
   if isinstance(extra,dict) and isinstance(extra.get("hashes"),dict):
    h=extra["hashes"]
    if h.get("md5") or h.get("sha256"):published_hashes+=1
 next_page=(j.get("links") or {}).get("next")
 if next_page is not None:
  validate_catalog_url(str(next_page))
 return {"publisher_listing_file_objects":count,
  "publisher_file_extension_categories":dict(sorted(extensions.items())),
  "publisher_original_file_or_folder_counts":dict(sorted(kinds.items())),
  "publisher_tabular_or_archive_file_candidates":potential,
  "publisher_hashed_file_count":published_hashes,
  "publisher_total_size_of_files_with_reported_size":sum(bytes_sizes),
  "publisher_pagination_next":bool(next_page),
  "original_OSF_file_contents_downloaded_or_examined":False,
  "original_actor_subject_session_day_partner_labels_republished":False},next_page

def get_json(url):
 validate_catalog_url(url)
 req=urllib.request.Request(url,headers={
  "User-Agent":"Psychohistory-R097-2017-Mao-OSF-original-files-metadata-no-human-choice/1.0",
  "Accept":"application/vnd.api+json,application/json"})
 with urllib.request.urlopen(req,timeout=28) as resp:
  validate_catalog_url(resp.geturl())
  b=resp.read(MAX_JSON+1)
 if len(b)>MAX_JSON:raise ValueError("R097_OSF_SOURCE_METADATA_RESPONSE_OVER_CAP")
 return json.loads(b.decode("utf-8"))

def failclass(e):
 if isinstance(e,urllib.error.HTTPError):return "HTTP_"+str(int(e.code))
 if isinstance(e,ValueError) and str(e).startswith("R097_"):return str(e)[:110]
 return "SOURCE_OSF_METADATA_ACCESS_FAILED_CLOSED"

def original_metadata():
 receipts=[]
 try:root=safe_project_metadata(get_json(BASE))
 except (OSError,urllib.error.URLError,urllib.error.HTTPError,ValueError,TypeError,KeyError) as e:
  receipts.append({"endpoint":"project_node","safe_failure":failclass(e)})
  root=None
 catalogs=[];page=LIST
 try:
  for _ in range(5):
   j=get_json(page)
   a,next_page=safe_file_catalog(j)
   catalogs.append(a)
   if not next_page:break
   page=str(next_page)
  else:
   raise ValueError("R097_OSF_PAGINATION_OVER_FIVE_PAGES_LIMIT")
 except (OSError,urllib.error.URLError,urllib.error.HTTPError,ValueError,TypeError,KeyError) as e:
  receipts.append({"endpoint":"public_osfstorage_listing","safe_failure":failclass(e)})
 status=("R097_ORIGINAL_2017_OSF_METADATA_CATALOG_VERIFIED"
         if root is not None and catalogs else "R097_ORIGINAL_2017_OSF_SOURCE_CATALOG_NOT_VERIFIED")
 return {"research_id":"R097","phase":"A_ORIGINAL_2017_MAO_LONG_RUN_PD_OSF_FILE_LISTING_NO_HUMAN_ACTIONS",
   "status":status,"publisher_PAPER_DOI":"10.1038/ncomms13800",
   "official_publisher_data_OSF_project":NODE,
   "original_published_project_metadata":root,
   "publisher_public_file_catalog_pages":catalogs,
   "public_source_discovery_failure_receipts":receipts,
   "source_original_human_repeated_cohort":"SAME_PEOPLE_OVER_MULTIPLE_DAYS_NOT_NEW_INDEPENDENT_POPULATION",
   "original_human_action_records_read_or_scored":0,
   "true_independent_person_or_session_LOSO_established":False,
   "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True);a=p.parse_args()
 z=original_metadata();a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(z,sort_keys=True,indent=2)+"\n")
 print(json.dumps(z,sort_keys=True))
 if z["status"]!="R097_ORIGINAL_2017_OSF_METADATA_CATALOG_VERIFIED":
  raise SystemExit(1)
if __name__=="__main__":main()
