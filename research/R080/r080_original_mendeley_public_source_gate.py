#!/usr/bin/env python3
"""R080 Mendeley v1 genuine-network public source access gate (no human scoring).

NEVER downloads participant-level JSON or prints signed download URLs. This
phase verifies public metadata, file descriptors and official ZIP HEAD only.
"""
from __future__ import annotations
import argparse,json,hashlib,pathlib,re
from urllib.error import HTTPError,URLError
from urllib.parse import urlparse
from urllib.request import Request,build_opener,HTTPRedirectHandler
SOURCE_DOI="10.17632/t963ktp6ft.1"
SOURCE_ID="t963ktp6ft"
TARGET_VERSION=1
HTTP_LIMIT=1_000_000
PROBE_URLS={
 "official_page":"https://data.mendeley.com/datasets/t963ktp6ft/1",
 "public_api_snapshot":"https://api.data.mendeley.com/datasets/t963ktp6ft?version=1",
 "public_api_versions":"https://api.data.mendeley.com/datasets/t963ktp6ft/versions",
 "public_api_version_url":"https://api.data.mendeley.com/datasets/t963ktp6ft/versions/1",
 "mendeley_legacy_api":"https://api.mendeley.com/datasets/t963ktp6ft?version=1",
 "mendeley_data_public_api":"https://data.mendeley.com/public-api/datasets/t963ktp6ft/versions/1",
 "mendeley_data_public_api_base":"https://data.mendeley.com/public-api/datasets/t963ktp6ft",
 "mendeley_data_api":"https://data.mendeley.com/api/datasets/t963ktp6ft?version=1",
}
ZIP_PROBE_URLS={
 "data_zip_official":"https://api.data.mendeley.com/datasets/t963ktp6ft/zip/file_downloaded",
 "data_zip_public":"https://data.mendeley.com/datasets/t963ktp6ft/1/files/download.zip",
}
ALLOWED_HOSTS={"data.mendeley.com","api.data.mendeley.com","api.mendeley.com"}
class NoRedirect(HTTPRedirectHandler):
 def redirect_request(self,req,fp,code,msg,hdrs,newurl):return None
def request_public(url,method="GET"):
 host=urlparse(url).hostname or ""
 if host not in ALLOWED_HOSTS:raise ValueError("PUBLIC_METADATA_HOST_NOT_OFFICIAL")
 req=Request(url,headers={"User-Agent":"Psychohistory-R080-authors-source-v1-public-metadata-integrity/1.0",
    "Accept":"application/json,text/html;q=0.7,*/*;q=0.2"},method=method)
 try:
  with build_opener(NoRedirect).open(req,timeout=24) as resp:
   size=int(resp.headers.get("Content-Length","0") or 0)
   typ=resp.headers.get("Content-Type","").split(";")[0]
   raw=resp.read(HTTP_LIMIT+1) if method=="GET" else b""
   return {"http_status":resp.status,"content_type":typ,"content_length":size,
           "payload":raw,"response_truncated":len(raw)>HTTP_LIMIT}
 except HTTPError as e:
  return {"http_status":e.code,"content_type":e.headers.get("Content-Type","").split(";")[0],
          "content_length":int(e.headers.get("Content-Length","0") or 0),
          "redirect_location_present":bool(e.headers.get("Location")),
          "response_truncated":False,"payload":b""}
 except (URLError,OSError,TimeoutError) as e:
  return {"http_status":None,"network_error_type":type(e).__name__,"payload":b""}

def safe_file_descriptor(v:dict)->dict:
 """Only aggregate author-file structure, not raw subject identifiers."""
 if not isinstance(v,dict):raise ValueError("INVALID_OFFICIAL_FILE_DESCRIPTOR")
 desc={}
 name=next((v.get(k) for k in ("filename","file_name","name","path","relative_path","key","display_name") if isinstance(v.get(k),str)),"")
 low=name.lower()
 ext=low.rsplit(".",1)[-1] if "." in low else ""
 desc["extension"]=ext if ext in ("json","csv","r","rds","zip","txt","md","pdf","png","jpg","xlsx","xls","tar","gz") else "OTHER"
 desc["raw_json_candidate"]=(ext=="json")
 desc["exp1_path_indicator"]=bool(re.search(r"(^|[/_])exp1([/_]|$)",low))
 desc["exp2_path_indicator"]=bool(re.search(r"(^|[/_])exp2([/_]|$)",low))
 desc["raw_path_indicator"]=("/raw/" in low or low.startswith("raw/"))
 desc["R_analysis_candidate"]=(ext=="r")
 desc["byte_size"]=next((x for k in ("size","file_size","length") if isinstance((x:=v.get(k)),int) and x>=0),None)
 desc["published_hash_present"]=any(isinstance(v.get(k),str) and bool(v.get(k))
      for k in ("checksum","md5","sha256","sha1","hash"))
 return desc

def summarize_official_json(data):
 if not isinstance(data,(dict,list)):raise ValueError("OFFICIAL_METADATA_NOT_CONTAINER")
 if isinstance(data,list):
  return {"json_type":"list","outer_count":len(data),
          "file_descriptors": [safe_file_descriptor(v) for v in data[:80] if isinstance(v,dict)]}
 safe={
   "json_type":"dict",
   "top_level_keys":[k for k in data.keys() if isinstance(k,str) and
      re.fullmatch(r"[a-zA-Z_]{1,45}",k)][:40],
   "id_matches":str(data.get("id",data.get("short_id",""))) in (SOURCE_ID,""),
   "version_field":data.get("version") if type(data.get("version")) in (int,str) else None,
   "doi_exact_match":SOURCE_DOI in str(data.get("doi",""))[:180],
   "title_matches":any(s in str(data.get(key,"")).lower() for key in ("title","name")
          for s in ("bot cooperation","cooperation experiment")),
 }
 candidates=[]
 for key in ("files","file_list","file_metadata","datafiles","data_files"):
  v=data.get(key)
  if isinstance(v,list):candidates.extend(v)
  if isinstance(v,dict):
   for nested in ("items","results","files","data"):
    if isinstance(v.get(nested),list):candidates.extend(v[nested])
 safe["file_descriptors"]=[safe_file_descriptor(x) for x in candidates[:120] if isinstance(x,dict)]
 safe["file_descriptors_total"]=len(candidates)
 safe["first_file_metadata_field_keys"]=[k for k in candidates[0] if isinstance(k,str) and re.fullmatch(r"[a-zA-Z_]{1,45}",k)][:45] if candidates and isinstance(candidates[0],dict) else []
 return safe

def metadata_gate_report(probes):
 outcomes={}
 official_readable=[]
 for label,p in probes.items():
  output={k:v for k,v in p.items() if k not in ("payload","response_truncated")}
  output["response_truncated"]=p.get("response_truncated",False)
  raw=p.get("payload",b"")
  if p.get("http_status")==200 and raw and not p.get("response_truncated",False):
   try:
    j=json.loads(raw)
    output["safe_official_json"]=summarize_official_json(j)
    official_readable.append(label)
   except (ValueError,UnicodeError):
    output["not_json_or_invalid_json"]=True
  outcomes[label]=output
 descriptors=[d for label in official_readable
                  for d in outcomes[label].get("safe_official_json",{}).get("file_descriptors",[])]
 return {
  "research_id":"R080","phase":"PUBLIC_ORIGINAL_MENDELEY_NETWORK_SOURCE_ACCESS_ONLY",
  "dataset_DOI":SOURCE_DOI,"official_dataset_v1":"https://data.mendeley.com/datasets/t963ktp6ft/1",
  "original_author":"Hirokazu Shirado",
  "journal_DOI":"10.1016/j.isci.2020.101438",
  "dataset_publisher_license":"CC BY 4.0",
  "official_description_stated_humans":1024,
  "official_description_stated_networks":64,
  "claims_above_verified_from_real_human_rows":False,
  "exact_full_original_network_JSON_bytes_verified":False,
  "human_vs_bot_node_classification_verified":False,
  "network_edges_time_series_verified":False,
  "official_json_metadata_success_labels":official_readable,
  "metadata_file_descriptors_total":len(descriptors),
  "descriptors_json_files":sum(x.get("raw_json_candidate",False) for x in descriptors),
  "descriptors_exp1_files":sum(x.get("exp1_path_indicator",False) for x in descriptors),
  "descriptors_exp2_files":sum(x.get("exp2_path_indicator",False) for x in descriptors),
  "official_access_checks":outcomes,
  "R080_real_network_E2":"OPEN_UNTIL_ORIGINAL_BYTES_AND_HUMAN_BOT_ROLE_GATE",
  "R080_real_behavior_model_scores":"NOT_RUN",
  "human_person_rows_exported":0,
  "PESEN_v0.1":"FROZEN"
 }

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args()
 probes={label:request_public(url) for label,url in PROBE_URLS.items()}
 probes.update({label:request_public(url,method="HEAD") for label,url in ZIP_PROBE_URLS.items()})
 report=metadata_gate_report(probes)
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 print(json.dumps({
  "research_id":"R080","metadata_access":report["official_json_metadata_success_labels"],
  "metadata_source_structures":{k:{"keys":v.get("safe_official_json",{}).get("top_level_keys"),
   "version":v.get("safe_official_json",{}).get("version_field"),
   "DOI_matches":v.get("safe_official_json",{}).get("doi_exact_match"),
   "file_count":v.get("safe_official_json",{}).get("file_descriptors_total"),
   "file_fields":v.get("safe_official_json",{}).get("first_file_metadata_field_keys"),
   "first_descriptors":v.get("safe_official_json",{}).get("file_descriptors",[])[:3]}
   for k,v in report["official_access_checks"].items() if k in report["official_json_metadata_success_labels"]},
  "file_descriptors":report["metadata_file_descriptors_total"],
  "HTTP":{k:v.get("http_status") for k,v in report["official_access_checks"].items()},
  "R080_real_network_E2":report["R080_real_network_E2"],
  "human_rows_scored":0,
 },sort_keys=True))
if __name__=="__main__":main()
