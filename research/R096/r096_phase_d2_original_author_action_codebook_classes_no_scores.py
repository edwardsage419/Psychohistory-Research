#!/usr/bin/env python3
"""R096 prescore publisher-author action codebook literals only. No human scores."""
from __future__ import annotations
import argparse,collections,csv,io,json,pathlib,urllib.request,urllib.error
from collections import Counter
from r096_phase_b_montero_author_git_tag_pinned_original_FP_SP_CSV_source import (
 FILES,CAP,raw_url,validate_raw_url,verify_author_blob)
from r096_phase_c_original_2022_author_fp_sp_six_true_sessions_roster import SOURCE_SHA,EXPECTED_ROWS
SAFE_LITERAL={"0","1","0.0","1.0","C","D","c","d",
 "Cooperate","Defect","cooperate","defect","True","False","None","NA","NaN",""}
def safe_class(v):
 x=str(v if v is not None else "")
 return ("EMPTY_SOURCE_ACTION" if x=="" else x) if x in SAFE_LITERAL else "REDACTED_OTHER"
def anonymous_action_codes(raw,name):
 reader=csv.DictReader(io.StringIO(raw.decode("utf-8-sig"),newline=""))
 if reader.fieldnames is None or not {"action_player","action_opponent"}.issubset(reader.fieldnames):
  raise ValueError("R096D2_AUTHOR_SOURCE_ACTION_COLUMNS_MISSING")
 player=Counter();opponent=Counter();n=0
 for r in reader:
  if None in r:raise ValueError("R096D2_ORIGINAL_AUTHOR_SOURCE_ROW_WIDTH_CHANGED")
  player[safe_class(r["action_player"])]+=1
  opponent[safe_class(r["action_opponent"])]+=1
  n+=1
 if n!=EXPECTED_ROWS[name]:
  raise ValueError("R096D2_ORIGINAL_AUTHOR_ACTION_SOURCE_ROWS_CHANGED")
 return {"published_author_file":name,"original_source_rows":n,
  "literal_player_source_action_code_classes":dict(sorted(player.items())),
  "literal_opponent_source_action_code_classes":dict(sorted(opponent.items())),
  "original_human_binary_models_scored":False,
  "actor_sessions_partners_actions_individual_rows_republished":False}
def real():
 output={}
 for name in ("fix.csv","rand.csv"):
  u=raw_url(name)
  with urllib.request.urlopen(urllib.request.Request(u,headers={
   "User-Agent":"Psychohistory-R096-author-exact-git-publisher-categorical-action-codes-pre-score/1.0"}),timeout=60) as r:
   validate_raw_url(r.geturl(),name);b=r.read(CAP+1)
  ident=verify_author_blob(b,name)
  if ident["full_original_whole_file_SHA256"]!=SOURCE_SHA[name]:
   raise ValueError("R096D2_SOURCE_WHOLE_FILE_SHA_CHANGED")
  output[name]=anonymous_action_codes(b,name)
 return {"research_id":"R096","phase":"D2_ORIGINAL_AUTHOR_PRESCORE_ACTION_CODE_LITERAL_CLASSES_ONLY",
  "original_source_fix_rand_git_blob_and_whole_sha_verified":True,
  "source_safe_class_counts":output,
  "prior_original_real_E2_action_code_rejection_preserved":True,
  "original_real_human_brier_prediction_scores":0,
  "PESEN_v0.1":"FROZEN"}
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=pathlib.Path,required=True)
 a=p.parse_args()
 try:z=real()
 except (ValueError,OSError,TypeError,KeyError,UnicodeError,urllib.error.URLError,urllib.error.HTTPError) as e:
  why=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R096D2_") else "R096D2_SOURCE_CODEBOOK_CLASSIFICATION_FAIL_CLOSED"
  z={"research_id":"R096","phase":"D2_AUTHORIGINAL_SOURCE_CODEBOOK_GATE_BLOCKED",
   "safe_error":why,"original_real_human_Brier_scores":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(z,sort_keys=True,indent=2)+"\n")
 print(json.dumps(z,sort_keys=True))
 if z["phase"]!="D2_ORIGINAL_AUTHOR_PRESCORE_ACTION_CODE_LITERAL_CLASSES_ONLY":
  raise SystemExit(1)
if __name__=="__main__":main()
