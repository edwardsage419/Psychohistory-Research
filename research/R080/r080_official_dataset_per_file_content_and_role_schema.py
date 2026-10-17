#!/usr/bin/env python3
"""R080 official dataset per-file content SHA and human/bot network source grammar.

Prior to any human network outcome metric. Raw bytes only held on Github runner;
no signed URLs, filenames, IDs, edge lists or person actions written to reports.
"""
from __future__ import annotations
import argparse,hashlib,json,re,pathlib,urllib.parse
from collections import Counter,defaultdict
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError
BASE="https://data.mendeley.com/public-api/datasets/t963ktp6ft"
DOI="10.17632/t963ktp6ft.1"
MAX_METADATA=3_000_000
MAX_ITEM=6_000_000
EXTENSIONS=("json","r","csv","txt","md","rds","pdf","xlsx","zip")
SAFE_ID=re.compile(r"^[A-Za-z0-9-]{8,90}$")
SHA256_RE=re.compile(r"^[0-9a-fA-F]{64}$")
ALLOWED_SUFFIXES=(".amazonaws.com",".mendeley.com",".elsevier.com",".cloudfront.net",".mendeleyusercontent.com")
HINTS=("human","bot","network","edge","node","round","time","exp1","exp2","treatment","connection","choice","cooperation")

def get(url,max_size=MAX_METADATA):
 req=Request(url,headers={
  "User-Agent":"Psychohistory-R080-Shirado-original-file-source-grammar/1.0",
  "Accept":"application/json,application/octet-stream,*/*"})
 with urlopen(req,timeout=65) as r:
  b=r.read(max_size+1)
  if len(b)>max_size:raise ValueError("R080_SOURCE_RESPONSE_MAX_SIZE_EXCEEDED")
  return b,{"HTTP":r.status,"content_type":r.headers.get("Content-Type","").split(";")[0]}

def safe_official_download_url(url):
 if not isinstance(url,str) or not url.startswith("https://"):return False
 parsed=urllib.parse.urlparse(url)
 hostname=(parsed.hostname or "").lower()
 if parsed.username or parsed.password or parsed.port not in (None,443):return False
 return any(hostname.endswith(s) or hostname==s.lstrip(".") for s in ALLOWED_SUFFIXES)

def metadata_overview(md):
 if not isinstance(md,dict) or md.get("version")!=1:
  raise ValueError("R080_REQUIRED_MENDELEY_PUBLIC_V1_METADATA_MISSING")
 doi=md.get("doi")
 did=doi.get("id") if isinstance(doi,dict) else doi
 if did!=DOI or not isinstance(md.get("files"),list):
  raise ValueError("R080_REQUIRED_ORIGINAL_AUTHOR_DOI_AND_FILES_MISSING")
 files=md["files"]
 ext=Counter();folders=Counter();by_folder=defaultdict(Counter)
 hashes=0;urls=0;content_keys=set();names=set()
 for f in files:
  if not isinstance(f,dict):raise ValueError("R080_ORIGINAL_METADATA_FILE_NOT_DICT")
  fn=f.get("filename","")
  if not isinstance(fn,str) or not fn:raise ValueError("R080_ORIGINAL_FILENAME_INVALID")
  e=fn.lower().rsplit(".",1)[-1] if "." in fn else "OTHER"
  if e not in EXTENSIONS:e="OTHER"
  ext[e]+=1
  fold=f.get("folder_id")
  folders[str(bool(fold))]+=1
  by_folder[str(fold or "ROOT")][e]+=1
  if (fold,fn) in names:raise ValueError("R080_DUPLICATE_AUTHOR_FILENAME_IN_SAME_FOLDER")
  names.add((fold,fn))
  c=f.get("content_details") or {}
  if not isinstance(c,dict):raise ValueError("R080_FILE_CONTENT_DETAILS_NOT_DICT")
  content_keys.update(k for k in c if isinstance(k,str) and re.fullmatch(r"[a-z_]{1,45}",k))
  h=c.get("sha256_hash")
  hashes+=bool(isinstance(h,str) and SHA256_RE.fullmatch(h))
  urls+=bool(safe_official_download_url(c.get("download_url")))
 return {
  "dataset_DOI_verified":did==DOI,"dataset_version_verified":1,
  "original_file_count":len(files),
  "file_extensions":dict(sorted(ext.items())),
  "sha256_published_in_file_content_details_count":hashes,
  "official_downloadable_content_urls_present_count":urls,
  "folder_ids_present_count":folders.get("True",0),
  "distinct_nonempty_folder_ids":len({f.get("folder_id") for f in files if f.get("folder_id")}),
  "folder_partition_extension_counts_unnamed":[dict(sorted(v.items())) for v in by_folder.values()],
  "content_details_legal_metadata_key_names":sorted(content_keys)
 }

def safe_structure(raw):
 """Only variable names/types and group list cardinalities, never personal values."""
 try:doc=json.loads(raw)
 except (ValueError,UnicodeError):return {"valid_JSON":False}
 safe=re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,34}$")
 def shape(obj,depth=0):
  if isinstance(obj,dict):
   names=[x for x in obj.keys() if isinstance(x,str) and safe.fullmatch(x)][:45]
   # depth-2 keys do not imply participant ID as names; mask mostly UUID-like keys
   names=[x for x in names if not re.fullmatch(r"(?i)(user|subject|person|node)?[0-9]{2,}",x)]
   out={"shape":"dict","count":len(obj),"keys":names}
   if depth<2:
    out["fields"]={x:shape(obj[x],depth+1) for x in names[:25]}
   return out
  if isinstance(obj,list):
   a={"shape":"list","count":len(obj)}
   if obj and depth<2:a["first_item_structure"]=shape(obj[0],depth+1)
   return a
  return {"shape":type(obj).__name__}
 return {"valid_JSON":True,"root_structure":shape(doc)}

def parse_script_semantics(text):
 lines=text.decode("utf-8",errors="replace").splitlines()
 hints=Counter()
 for line in lines:
  low=line.lower()
  for w in HINTS:
   if w in low:hints[w]+=1
 return {"original_R_code_line_count":len(lines),
  "keyword_source_statement_occurrences":dict(sorted(hints.items()))}

def file_source_gate():
 raw,_=get(BASE)
 data=json.loads(raw)
 overview=metadata_overview(data)
 allfiles=data["files"]
 candidates=[]
 for f in allfiles:
  ext=f["filename"].lower().rsplit(".",1)[-1] if "." in f["filename"] else ""
  if ext not in ("r","json"):continue
  n=int(f.get("size") or (f.get("content_details") or {}).get("size") or 0)
  if n>MAX_ITEM or n<1:continue
  candidates.append((f,ext,n))
 # Select source R script up to 6, and first JSON from each anonymous folder,
 # then at most three additional JSONs from differing sizes; nothing outcome-scored.
 selected=[];folder_done=set();r_count=0;json_count=0
 for f,ext,n in sorted(candidates,key=lambda z:(0 if z[1]=="r" else 1,z[2])):
  if ext=="r" and r_count<6:
   selected.append((f,ext,n));r_count+=1
  elif ext=="json" and json_count<6:
   fold=f.get("folder_id")
   if fold not in folder_done or json_count<2:
    selected.append((f,ext,n));json_count+=1;folder_done.add(fold)
 selected_files=[]
 summary_attempts=Counter()
 for f,ext,expected_bytes in selected:
  c=f.get("content_details") or {}
  link=c.get("download_url")
  download_method="embedded_official_metadata"
  if not safe_official_download_url(link):
   fid=f.get("id")
   if not isinstance(fid,str) or not SAFE_ID.fullmatch(fid):
    summary_attempts["missing_safe_file_id"]+=1
    continue
   # file is inside the already verified genuine author dataset.
   try:
    detail_bytes,_=get(BASE+"/files/"+fid+"?version=1",MAX_METADATA)
    detail=json.loads(detail_bytes)
    if isinstance(detail,dict):
     link=(detail.get("content_details") or {}).get("download_url")
     download_method="official_dataset_file_details"
   except (ValueError,HTTPError,URLError):
    summary_attempts["official_individual_file_metadata_unavailable"]+=1
    continue
  if not safe_official_download_url(link):
   summary_attempts["official_signed_file_download_url_missing"]+=1
   continue
  try:
   body,_=get(link,min(MAX_ITEM,expected_bytes+1024))
   if len(body)!=expected_bytes:
    summary_attempts["file_size_not_equal_official_metadata"]+=1
    continue
   sha=hashlib.sha256(body).hexdigest()
   official_hash=c.get("sha256_hash")
   if isinstance(official_hash,str) and SHA256_RE.fullmatch(official_hash):
    if official_hash.lower()!=sha:
     summary_attempts["published_SHA256_disagrees_with_actual_bytes"]+=1
     continue
    author_sha_verified=True
   else:author_sha_verified=False
   item={"type":ext,"original_bytes":len(body),
      "first_party_file_SHA256":sha,
      "official_publisher_SHA256_verified":author_sha_verified,
      "which_download_method":download_method,
      # only anonymous folder ordinal *not original ID*.
      "file_came_from_distinct_original_folder":bool(f.get("folder_id")),
     }
   if ext=="r":item["source_code_schema_hints"]=parse_script_semantics(body)
   else:item["JSON_schema_no_values"]=safe_structure(body)
   selected_files.append(item)
   summary_attempts["successful_original_files"]+=1
  except (ValueError,HTTPError,URLError,OSError) as e:
   summary_attempts["public_original_file_bytes_unavailable"]+=1
 return {"research_id":"R080",
    "status":"R080_ORIGINAL_AUTHOR_PUBLISHED_SOURCE_FILE_ID_AND_METADATA_RETRIEVAL_GATE",
    "official_dataset":BASE,"official_DOI":DOI,
    "first_party_metadata_snapshot":overview,
    "file_download_selection_policy":"At most six R scripts and six JSONs across distinct original folders; zero target scores",
    "file_download_attempts":dict(sorted(summary_attempts.items())),
    "downloaded_author_source_digests_and_safe_shapes":selected_files,
    "all_64_real_networks_reconstructed":False,
    "human_bot_roles_identified":False,
    "human_network_rows_scored":0,
    "intervention_or_group_level_effect":"NOT_RUN",
    "PESEN_v0.1":"FROZEN"}

def main():
 p=argparse.ArgumentParser()
 p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args()
 try:result=file_source_gate()
 except (ValueError,HTTPError,URLError,UnicodeError,TimeoutError) as e:
  result={"research_id":"R080","status":"R080_OFFICIAL_PER_FILE_SOURCE_FAIL_CLOSED",
    "failure_class":type(e).__name__,
    "failure_reason":str(e)[:100] if isinstance(e,ValueError) else "PUBLIC_SOURCE_NETWORK_UNAVAILABLE",
    "human_network_rows_scored":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 print(json.dumps({
  "status":result["status"],
  "metadata":result.get("first_party_metadata_snapshot"),
  "download_attempts":result.get("file_download_attempts"),
  "file_structures":result.get("downloaded_author_source_digests_and_safe_shapes"),
  "human_network_rows_scored":0,
  "failed_reason":result.get("failure_reason"),
 },sort_keys=True))
if __name__=="__main__":main()
