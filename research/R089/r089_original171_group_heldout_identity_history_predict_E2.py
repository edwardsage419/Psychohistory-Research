#!/usr/bin/env python3
"""R089 frozen group heldout prediction: 5 folds, 3 arms, sharp unknown actions.

Outcome is fraction of six global contributors next round. Original group and
actor IDs never printed or serialized. Both within-group history and initial
(pre-round1) DIFI are available at prediction time, not future DIFI.
"""
from __future__ import annotations
import argparse,collections,hashlib,json,math,pathlib,urllib.request,urllib.error
from collections import defaultdict
from r088_original_171_groups_multilevel_global_cooperation_E2 import (
 author_bytes,parse_csv,CSV_FILE,CSV_BLOB,CSV_BYTES,
 EXCLUDE_FILE,EXCLUDE_BLOB,ANALYSIS_FILE,ANALYSIS_BLOB,
 CONDITIONS,COMMIT)
from r088_phase_c_original171_missing_sharp_bounds_E2 import boundary_group

ID_AUTHOR_FILES={
 "analysis/analysis_initial_identity.R":"c67bbdd50dbf4fe9efcfca8fe303ae418d0dd6a1",
 "analysis/anlaysis_trends_identity.R":"027fab69c27af7155d673469bdb32d6cbafa1080",
}
ID_FIELD="survey.1.player.DIFI_big_group_distance"
INITIAL_RANGE=(-175.7,125.0)
FOLD_SALT="R089_GROUP_HOLDOUT_V1_2026_10_17|"
MODEL_NAMES=("M0_CONDITION_ROUND","M1_LAST_GROUP_ROUND","M2_FIXED_HALF_BLEND","M3_PREGAME_GLOBAL_IDENTITY")
PROTOCOL="protocols/R089_171_GROUP_COMPLETE_HOLDOUT_HISTORY_AND_BASELINE_IDENTITY_PREDICTION_FREEZE_2026-10-17.md"

def git_sha(raw):
 return hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()

def pinned_identity_doc(name,digest):
 if name not in ID_AUTHOR_FILES or ID_AUTHOR_FILES[name]!=digest:
  raise ValueError("R089_UNFROZEN_AUTHOR_IDENTITY_SCRIPT")
 url=f"https://raw.githubusercontent.com/chasmani/PUBLIC_social_identity_and_cooperation/{COMMIT}/{name}"
 req=urllib.request.Request(url,headers={"User-Agent":"PsychologicalHistory-R089-author-identity-document/1.0"})
 with urllib.request.urlopen(req,timeout=50) as r:
  if r.geturl()!=url:raise ValueError("R089_UNFROZEN_AUTHOR_SOURCE_REDIRECT")
  body=r.read(26000)
 if git_sha(body)!=digest:raise ValueError("R089_AUTHOR_IDENTITY_DOCUMENT_HASH_MISMATCH")
 return body

def before_round_identity(raw):
 if raw is None or not isinstance(raw,str) or not raw.strip():
  return None
 try:v=float(raw)
 except ValueError:return None
 if not math.isfinite(v) or not INITIAL_RANGE[0]<=v<=INITIAL_RANGE[1]:
  return None
 return (v+175.7)/300.7

def group_five_folds(group_ids):
 return {gid:k%5 for k,gid in enumerate(sorted(group_ids,
   key=lambda g:hashlib.sha256((FOLD_SALT+g).encode("utf-8")).hexdigest()))}

def group_data(source_rows,expected_arms=57,expected_missing=64):
 if not source_rows:raise ValueError("R089_EMPTY_AUTHOR_SAMPLE")
 group_map=defaultdict(list)
 for row in source_rows:
  gid=row.get("group_id")
  if not gid or not gid.strip():raise ValueError("R089_MISSING_ORIGINAL_GROUP_ID")
  group_map[gid].append(row)
 if len(group_map)!=3*expected_arms or len(source_rows)!=18*expected_arms:
  raise ValueError("R089_REAL_ORIGINAL_GROUP_UNIVERSE_NOT171x6")
 result=defaultdict(dict)
 missing=0
 identity_valid=True
 invalid_identity_groups=0
 for groupid,rows in group_map.items():
  condition,rawrounds=boundary_group(rows)
  acts=[]
  for r in rawrounds:
   g,m=r["confirmed_global"],r["unobserved_missing_action"]
   acts.append({"g":g,"m":m,"mid":(g+m/2)/6,"lower":g/6,"upper":(g+m)/6})
   missing+=m
  ident=[before_round_identity(row.get(ID_FIELD)) for row in rows]
  valid=all(z is not None for z in ident)
  if not valid:
   identity_valid=False;invalid_identity_groups+=1
  result[condition][groupid]={"rounds":acts,
    "identity":(sum(ident)/6 if valid else None)}
 if set(result)!=set(CONDITIONS) or any(len(result[c])!=expected_arms for c in CONDITIONS):
  raise ValueError("R089_ORIGINAL_3_ARMS_UNIVERSE_INVALID")
 if expected_missing is not None and missing!=expected_missing:
  raise ValueError("R089_ORIGINAL_MISSINGNESS_EXPECTED64_NOT_MET")
 if expected_missing==64:
  by={c:sum(r["m"] for z in result[c].values() for r in z["rounds"]) for c in CONDITIONS}
  if by!={"GlobalOnly":19,"Balanced":26,"GlobalBoost":19}:
   raise ValueError("R089_ORIGINAL_PER_CONDITION_MISSINGNESS_MISMATCH")
 return result,{"original_missing_action_slots":missing,
   "all_pregame_identity_rows_in_three_arms_eligible":identity_valid,
   "complete_sixperson_group_identity_failures":invalid_identity_groups}

def clamp(x):return min(1.0,max(0.0,float(x)))

def sharp_bounded_squared_loss(p,g,m):
 vals=[(p-k/6)**2 for k in range(g,g+m+1)]
 return (min(vals),max(vals))

def shared_target_improvement(p0,p1,g,m):
 d=[(p0-k/6)**2-(p1-k/6)**2 for k in range(g,g+m+1)]
 return (min(d),max(d))

def init_record():
 return {"raw_targets":0,"raw_groups":0,"missing_target_slots":0,
         "with_previous_round_missing":0,
         "models":{m:{"loss_lower_sum":0.0,"loss_upper_sum":0.0} for m in MODEL_NAMES},
         "improvement_vs_M0":{m:{"lower_sum":0.0,"upper_sum":0.0} for m in MODEL_NAMES[1:]}}

def add_model_metric(dest,preds,target):
 g,m=target["g"],target["m"]
 dest["raw_targets"]+=1
 dest["missing_target_slots"]+=m
 for k,p in preds.items():
  lo,hi=sharp_bounded_squared_loss(p,g,m)
  dest["models"][k]["loss_lower_sum"]+=lo
  dest["models"][k]["loss_upper_sum"]+=hi
 for k in MODEL_NAMES[1:]:
  if k not in preds:continue
  lo,hi=shared_target_improvement(preds[MODEL_NAMES[0]],preds[k],g,m)
  dest["improvement_vs_M0"][k]["lower_sum"]+=lo
  dest["improvement_vs_M0"][k]["upper_sum"]+=hi

def finish_record(x,identity_ok):
 n=x["raw_targets"]
 if not n:raise ValueError("R089_NO_HELDOUT_SCORES")
 models={}
 for k,v in x["models"].items():
  if k==MODEL_NAMES[3] and not identity_ok:continue
  models[k]={"score_sharp_lower":v["loss_lower_sum"]/n,
             "score_sharp_upper":v["loss_upper_sum"]/n}
 improves={}
 for k,v in x["improvement_vs_M0"].items():
  if k==MODEL_NAMES[3] and not identity_ok:continue
  lo,hi=v["lower_sum"]/n,v["upper_sum"]/n
  improves[k]={"score_gain_sharp_lower":lo,"score_gain_sharp_upper":hi,
    "robust_direction":("BETTER_THAN_M0" if lo>0 else "WORSE_THAN_M0" if hi<0
                        else "NOT_SIGN_IDENTIFIED")}
 return {"heldout_group_rounds":n,
   "unique_heldout_groups":x["raw_groups"],
   "original_missing_target_action_slots":x["missing_target_slots"],
   "heldout_history_lag_had_missing_slots":x["with_previous_round_missing"],
   "squared_group_share_error_sharp_bounds":models,
   "shared_unknown_target_paired_improvement_vs_M0":improves}

def evaluate_holdout(groups,identity_ok):
 all_record=init_record()
 by_cond={c:init_record() for c in CONDITIONS}
 by_fold={str(i):init_record() for i in range(5)}
 positive_by_group={c:{k:{"guaranteed_gain":0,"guaranteed_loss":0,"ambiguous":0}
                       for k in MODEL_NAMES[1:] if k!=MODEL_NAMES[3] or identity_ok}
                    for c in CONDITIONS}
 fold_sizes={}
 fitted_beta_by_fold_and_condition={}
 for condition in CONDITIONS:
  ids=list(groups[condition])
  ranks=group_five_folds(ids)
  fold_sizes[condition]={str(f):sum(ranks[g]==f for g in ids) for f in range(5)}
  if sorted(fold_sizes[condition].values())!=[11,11,11,12,12] and len(ids)==57:
   raise ValueError("R089_FIVE_FOLDS_11_OR_12_GROUPS_NOT_BALANCED")
  for f in range(5):
   test=[g for g in ids if ranks[g]==f]
   train=[g for g in ids if ranks[g]!=f]
   if not test or not train or set(test)&set(train):
    raise ValueError("R089_HELDOUT_GROUP_LEAKAGE")
   baseline={}
   for t in range(1,20): # target t+1
    baseline[t]=sum(groups[condition][g]["rounds"][t]["mid"] for g in train)/len(train)
   beta=0.0
   mean_train_id=0.0
   if identity_ok:
    mean_train_id=sum(groups[condition][g]["identity"] for g in train)/len(train)
    numerator=denominator=0.0
    for g in train:
     data=groups[condition][g]
     dif=data["identity"]-mean_train_id
     avg_resid=sum(
       data["rounds"][t]["mid"]-(0.5*baseline[t]+0.5*data["rounds"][t-1]["mid"])
       for t in range(1,20))/19
     numerator+=dif*avg_resid
     denominator+=dif*dif
    beta=numerator/(denominator+1.0)
   fitted_beta_by_fold_and_condition[f"{condition}_fold{f}"]={
     "trained_groups":len(train),"heldout_groups":len(test),
     "identity_ridge_beta":beta if identity_ok else None}
   for gid in test:
    rows=groups[condition][gid]["rounds"]
    group_record=init_record()
    group_record["raw_groups"]+=1
    all_record["raw_groups"]+=1
    by_cond[condition]["raw_groups"]+=1
    by_fold[str(f)]["raw_groups"]+=1
    for t in range(1,20):
     last=rows[t-1]["mid"]
     base=baseline[t]
     blend=(base+last)/2
     predictions={MODEL_NAMES[0]:base,MODEL_NAMES[1]:last,MODEL_NAMES[2]:blend}
     if identity_ok:
      predictions[MODEL_NAMES[3]]=clamp(blend+beta*(groups[condition][gid]["identity"]-mean_train_id))
     for record in (all_record,by_cond[condition],by_fold[str(f)],group_record):
      add_model_metric(record,predictions,rows[t])
      record["with_previous_round_missing"]+=int(rows[t-1]["m"]>0)
    for challenger in positive_by_group[condition]:
     stat=group_record["improvement_vs_M0"][challenger]
     which=("guaranteed_gain" if stat["lower_sum"]>0 else
            "guaranteed_loss" if stat["upper_sum"]<0 else "ambiguous")
     positive_by_group[condition][challenger][which]+=1
 result={
  "model_not_hyperparameter_tuned_on_heldout_results":True,
  "fold_heldout_group_sizes_by_condition":fold_sizes,
  "training_only_identity_ridge_beta_no_actor_or_group_IDs":fitted_beta_by_fold_and_condition,
  "identity_source_eligible_for_M3":identity_ok,
  "overall":finish_record(all_record,identity_ok),
  "by_frozen_treatment":{c:finish_record(by_cond[c],identity_ok) for c in CONDITIONS},
  "by_outer_fold":{f:finish_record(by_fold[f],identity_ok) for f in by_fold},
  "groupwise_sign_of_paired_improvement_vs_M0":{
   c:positive_by_group[c] for c in CONDITIONS},
  "effective_sampling_unit":"ORIGINAL_FULL_SIX_PERSON_GROUP_NO_RANDOM_SESSION_EFFECTS_IDENTIFIED",
  "heldout_171_groups_x_19_future_rounds":all_record["raw_targets"]}
 if all_record["raw_groups"]!=171 or all_record["raw_targets"]!=3249:
  raise ValueError("R089_INDEPENDENT_GROUP_TARGETS_NOT_171x19")
 return result

def original_r089():
 src=author_bytes(CSV_FILE,CSV_BLOB,2500000)
 if len(src)!=CSV_BYTES:raise ValueError("R089_ORIGINAL_AUTHOR_CSV_SIZE_MISMATCH")
 a=author_bytes(EXCLUDE_FILE,EXCLUDE_BLOB,8000)
 b=author_bytes(ANALYSIS_FILE,ANALYSIS_BLOB,16000)
 if b"data_full_groups.csv" not in a or b"global_group_contributions" not in b:
  raise ValueError("R089_SOURCE_AUTHOR_ANALYSIS_CODE_NOT_RECOGNIZED")
 code=pinned_identity_doc("analysis/analysis_initial_identity.R",ID_AUTHOR_FILES["analysis/analysis_initial_identity.R"])
 trend=pinned_identity_doc("analysis/anlaysis_trends_identity.R",ID_AUTHOR_FILES["analysis/anlaysis_trends_identity.R"])
 if ID_FIELD.encode() not in code or b"game.20.player.DIFI_big_group_distance" not in trend:
  raise ValueError("R089_INITIAL_VERSUS_FUTURE_IDENTITY_DISTINCTION_NOT_VERIFIED")
 groups,source=group_data(parse_csv(src))
 return {"research_id":"R089",
  "status":"R089_REAL_ORIGINAL171_GROUP_COMPLETE_HOLDOUT_E2_PREDICTION_EXECUTED",
  "research_evidence":"E2_SAME_ORIGINAL_AUTHOR_171_GROUP_DATA_NEW_GROUP_HELDOUT_SCORE_NOT_NEW_E3",
  "frozen_protocol":PROTOCOL,
  "publisher_original_fixed_commit":COMMIT,
  "original_author_full_groups_blob":CSV_BLOB,
  "original_author_initial_identity_analysis_blob":ID_AUTHOR_FILES["analysis/analysis_initial_identity.R"],
  "original_author_identity_trends_blob":ID_AUTHOR_FILES["analysis/anlaysis_trends_identity.R"],
  "source_eligibility":source,
  "original_group_holdout_predictive_evaluation":evaluate_holdout(groups,source["all_pregame_identity_rows_in_three_arms_eligible"]),
  "future_round_identity_or_postsurvey_used_for_prediction":False,
  "source_actor_group_identity_or_actions_exported":False,
  "causal_identity_effect":"NOT_IDENTIFIED",
  "independent_external_lab_E3":"NOT_ESTABLISHED",
  "PESEN_v0.1":"FROZEN"}

def main():
 ap=argparse.ArgumentParser();ap.add_argument("--output",type=pathlib.Path,required=True)
 a=ap.parse_args()
 try:v=original_r089()
 except (ValueError,OSError,TypeError,KeyError,UnicodeError,urllib.error.HTTPError,urllib.error.URLError) as e:
  safe=str(e)[:100] if isinstance(e,ValueError) and str(e).startswith("R089_") else "R089_AUTHOR_SOURCE_OR_MODEL_GATE_ERROR"
  v={"research_id":"R089","status":"R089_ORIGINAL_SOURCE_OR_HELDOUT_MODEL_FAIL_CLOSED",
     "safe_failure":safe,"actual_group_heldout_scores_exported":0,"PESEN_v0.1":"FROZEN"}
 a.output.parent.mkdir(parents=True,exist_ok=True)
 a.output.write_text(json.dumps(v,indent=2,sort_keys=True)+"\n",encoding="utf-8")
 res=v.get("original_group_holdout_predictive_evaluation",{})
 print(json.dumps({"status":v["status"],"failure":v.get("safe_failure"),
   "identity_eligibility":v.get("source_eligibility"),
   "score_rows":res.get("heldout_171_groups_x_19_future_rounds"),
   "overall":res.get("overall"),
   "by_condition":res.get("by_frozen_treatment"),
   "groupwise_model_signs":res.get("groupwise_sign_of_paired_improvement_vs_M0")},sort_keys=True))
 if v["status"]!="R089_REAL_ORIGINAL171_GROUP_COMPLETE_HOLDOUT_E2_PREDICTION_EXECUTED":
  raise RuntimeError("R089_REAL_PREDICTION_FAIL_CLOSED")
if __name__=="__main__":main()
