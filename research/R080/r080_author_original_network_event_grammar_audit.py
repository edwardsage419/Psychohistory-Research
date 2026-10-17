#!/usr/bin/env python3
"""R080 frozen-data-compatible per-author-file network grammar metadata gate.
No human choice values or edge lists exported; source R lines are author code.
"""
from __future__ import annotations
import pathlib,argparse,json,hashlib,re
from collections import Counter
from r080_official_dataset_per_file_content_and_role_schema import (
 BASE,DOI,MAX_METADATA,MAX_ITEM,SHA256_RE,get,metadata_overview,safe_official_download_url
)
NAMES=("players","is_bot","result_behaviors","result_networks","cooperation",
"rewiring","network","treatment","game_id","round")
LINE_RE=re.compile(r"result_networks|result_behaviors|is_bot|rewiring|cooperation|players|network|bot|treat",re.I)
TOP_RE=re.compile(r"^[A-Za-z][A-Za-z0-9_]{0,35}$")
def safe_tree(obj,depth=0):
 if isinstance(obj,dict):
  keys=[str(k) for k in obj if isinstance(k,str) and TOP_RE.fullmatch(k)]
  keys=[k for k in keys if not re.search(r"(?:user|player|id)[0-9]{2,}",k,re.I)][:30]
  return {"type":"object","length":len(obj),"properties":{k:safe_tree(obj[k],depth+1)
         if depth<4 else {"type":type(obj[k]).__name__} for k in keys[:20]}}
 if isinstance(obj,list):
  return {"type":"array","length":len(obj),
          "first_element_type":safe_tree(obj[0],depth+1) if obj and depth<5 else "redacted"}
 return {"type":type(obj).__name__}
def safe_author_R_statements(raw):
 lines=raw.decode("utf-8-sig",errors="replace").splitlines()
 hits=[]
 for i,s in enumerate(lines,1):
  line=s.strip()
  if (LINE_RE.search(line) and len(line)<=170 and
      not re.search(r"(?i)(https?://|bearer |secret|token|password|authorization)",line)):
   hits.append({"line_number":i,"author_R_code_line":line})
 return {"source_code_lines":len(lines),"relevant_author_statements":hits[:25]}
def run():
 raw,_=get(BASE)
 md=json.loads(raw)
 overview=metadata_overview(md)
 files=md["files"]
 targets_r=[f for f in files if f["filename"].lower().endswith(".r")]
 jsons=[f for f in files if f["filename"].lower().endswith(".json")]
 targets_j=[]
 folders=set()
 for f in sorted(jsons,key=lambda f:int(f.get("size") or 0)):
  fold=f.get("folder_id")
  if fold not in folders:
   targets_j.append(f);folders.add(fold)
  if len(targets_j)>=2:break
 records=[]
 for f in targets_r+targets_j:
  c=f.get("content_details") or {}
  link=c.get("download_url")
  if not safe_official_download_url(link):
   raise ValueError("R080_AUTHOR_FILE_SIGNED_DOWNLOAD_UNAVAILABLE")
  size=int(f.get("size") or 0)
  if size<1 or size>MAX_ITEM:
   raise ValueError("R080_AUTHOR_FILE_BYTES_ABOVE_GATE")
  data,_=get(link,min(MAX_ITEM,size+4096))
  h=c.get("sha256_hash")
  if len(data)!=size or not isinstance(h,str) or not SHA256_RE.fullmatch(h) or hashlib.sha256(data).hexdigest()!=h.lower():
   raise ValueError("R080_AUTHOR_FILE_PUBLISHER_SHA256_MISMATCH")
  rec={"source_file_type":"R" if f["filename"].lower().endswith(".r") else "JSON",
       "author_official_SHA256":h,"verified_bytes":size}
  if rec["source_file_type"]=="R":rec["author_script_semantics"]=safe_author_R_statements(data)
  else:
   rec["original_immutable_source_structure"]=safe_tree(json.loads(data))
  records.append(rec)
 return {"research_id":"R080","phase":"ORIGINAL_NETWORKS_64_JSON_AUTHOR_GRAMMAR_BEFORE_METRICS",
         "publisher_DOI":DOI,"publisher_metadata_file_count":overview["original_file_count"],
         "exact_publisher_sha256_verified_selected_source_files":len(records),
         "independent_original_human_networks_scored":0,
         "selected_author_real_files_source_code_and_schema_only":records,
         "real_human_64_networks_reconstructed":False,"PESEN_v0.1":"FROZEN"}
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args()
 result=run()
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
 print(json.dumps(result,sort_keys=True))
if __name__=="__main__":main()
