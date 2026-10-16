#!/usr/bin/env python3
"""R066 E2 internal held-out 16-village original source opinion model comparison.

Uses pre-interim baseline + observed immediate response, source-pinned author
household networks, equal-village leave-one-village-out selection and scoring.
This is NOT randomized assignment to network structure, E3 replication, or
causal validation of any of the three mechanisms.
"""
from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from r066_author_r_edge_parity import python_edge_sets, read_author_rows
from r066_author_household_audit import sort_hhnum
from r066_larson_lewis_join_gate import ITEMS,parse_response,clean_id

STEPS=(1,2,4)
ALPHAS=(0.25,0.5,0.75,1.0)
EPSILONS=(0.05,0.15,0.30,0.50,1.0)
BASELINE_SCORE_ROWS=1872
EXPECTED_VILLAGES=16
EXPECTED_GRAPH_UNION_EDGES=8659
EXPECTED_HOUSEHOLDS=2125
EXPECTED_TYPOLOGY_EDGES=14767
CLASSES=("persistence","degroot","fj","hk")


def response_index(row, suffix):
    vals=[parse_response(row[item+suffix]) for item in ITEMS]
    if not all(k=="within_1_5" for k,v in vals):
        return None
    result=(math.fsum(value for k,value in vals)-6.0)/24.0
    if not math.isfinite(result) or not 0<=result<=1:
        raise ValueError("invalid six-item attitude index")
    return result


def create_villages(rows):
    if len(rows)!=EXPECTED_HOUSEHOLDS:
        raise ValueError("must use exactly original 2125 source rows")
    by_village=defaultdict(list)
    for row in rows:
        village=clean_id(row["village_number"])
        if village is None:
            raise ValueError("source village missing")
        by_village[village].append(row)
    if len(by_village)!=EXPECTED_VILLAGES:
        raise ValueError("exactly 16 source villages required")
    typed_edges=python_edge_sets(rows)
    if len(typed_edges)!=EXPECTED_TYPOLOGY_EDGES:
        raise ValueError("author-parity typed edge universe drift")
    union_edges={(v,a,b) for v,category,a,b in typed_edges}
    if len(union_edges)!=EXPECTED_GRAPH_UNION_EDGES:
        raise ValueError("author-parity unique undirected network universe drift")
    neighbors=defaultdict(list)
    for village,a,b in union_edges:
        neighbors[village,a].append(b-1)
        neighbors[village,b].append(a-1)
    groups={}
    total_score=0
    immediate_count=0
    imputed_count=0
    for village,orig in by_village.items():
        records=sorted(orig,key=lambda row:sort_hhnum(row["hhnum"]))
        n=len(records)
        original_x=[response_index(row,"1") for row in records]
        immediate_x=[response_index(row,"2") for row in records]
        endline_y=[response_index(row,"_e") for row in records]
        valid_baseline=[z for z in original_x if z is not None]
        if not valid_baseline:
            raise ValueError("village lacks any usable pre-interim baseline")
        impute=sum(valid_baseline)/len(valid_baseline)
        initial=np.array([
            immediate if immediate is not None else
            (base if base is not None else impute)
            for immediate,base in zip(immediate_x,original_x)
        ],dtype=np.float64)
        observed=np.array([v if v is not None else math.nan
                           for v in endline_y],dtype=np.float64)
        mask=np.array([base is not None and endline is not None
                       for base,endline in zip(original_x,endline_y)],
                      dtype=bool)
        if not np.any(mask):
            raise ValueError("village no complete baseline/endline cases")
        adj=tuple(tuple(sorted(set(neighbors.get((village,i+1),()))))
                  for i in range(n))
        total_score+=int(mask.sum())
        immediate_count+=sum(q is not None for q in immediate_x)
        imputed_count+=sum(a is None and b is None
                           for a,b in zip(original_x,immediate_x))
        groups[village]={
            "xstart":initial,"endline":observed,"mask":mask,
            "neighbors":adj,"participants":n,
            "scored":int(mask.sum()),
        }
    if total_score!=BASELINE_SCORE_ROWS:
        raise ValueError("baseline/endline denominator drift")
    return groups,{
        "source_rows":len(rows),"villages":len(groups),
        "baseline_endline_scored":total_score,
        "household_union_edges":len(union_edges),
        "household_typed_edges":len(typed_edges),
        "observed_immediate_six_item_values":immediate_count,
        "imputed_baseline_and_immediate_absent":imputed_count,
    }


def evolve(model,initial,adj,param):
    x=np.asarray(initial,dtype=np.float64)
    start=np.array(x,copy=True)
    if x.ndim!=1 or len(x)!=len(adj) or np.any(~np.isfinite(x)):
        raise ValueError("invalid simulation starting vector")
    if np.any((x<0)|(x>1)):
        raise ValueError("opinion out of [0,1]")
    if model=="persistence":
        return start
    if model not in ("degroot","fj","hk"):
        raise ValueError("unknown model")
    steps=int(param["steps"])
    if steps not in STEPS:
        raise ValueError("outside prespecified steps")
    if model=="fj" and float(param["alpha"]) not in ALPHAS:
        raise ValueError("FJ alpha out of frozen grid")
    if model=="hk" and float(param["epsilon"]) not in EPSILONS:
        raise ValueError("HK epsilon out of frozen grid")
    for _ in range(steps):
        if model=="hk":
            eps=param["epsilon"]
            included=np.abs(x[:,None]-x[None,:])<=eps+1e-12
            x=(included@x)/included.sum(axis=1)
        else:
            wx=np.empty_like(x)
            for i,links in enumerate(adj):
                wx[i]=float(np.mean(x[list(links)])) if links else x[i]
            if model=="degroot":
                x=wx
            else:
                a=param["alpha"]
                x=a*wx+(1-a)*start
        if np.any(~np.isfinite(x)) or np.any(x < -1e-12) or np.any(x > 1+1e-12):
            raise ValueError("opinion simulation diverged")
        x=np.clip(x,0,1)
    return x


def make_grid(model):
    if model=="persistence":
        return [("start",{})]
    if model=="degroot":
        return [(f"steps={step}",{"steps":step}) for step in STEPS]
    if model=="fj":
        return [(f"alpha={alpha},steps={step}",{"alpha":alpha,"steps":step})
                for alpha in ALPHAS for step in STEPS]
    if model=="hk":
        return [(f"eps={eps},steps={step}",{"epsilon":eps,"steps":step})
                for eps in EPSILONS for step in STEPS]
    raise ValueError("unsupported model")


def precompute(groups):
    cache={}
    for model in CLASSES:
        variants=make_grid(model)
        per_variant={}
        for label,param in variants:
            per_variant[label]={v:evolve(model,g["xstart"],g["neighbors"],param)
                                for v,g in groups.items()}
        cache[model]=per_variant
    return cache


def choose_training(groups, pred_by_variant, heldout):
    """No heldout y is read, including when computing common drift."""
    train=[v for v in sorted(groups) if v!=heldout]
    if not train:
        raise ValueError("requires independent training villages")
    options=[]
    for order,(name,pred_by_village) in enumerate(pred_by_variant.items()):
        if set(pred_by_village)!=set(groups):
            raise ValueError("predicted village universe mismatch")
        raw_offsets=[]
        for v in train:
            group=groups[v]; mask=group["mask"]
            raw_offsets.append(float(np.mean(
                group["endline"][mask]-pred_by_village[v][mask]
            )))
        delta=float(np.mean(raw_offsets))   # each training village equal
        train_losses=[]
        for v in train:
            group=groups[v]; mask=group["mask"]
            prediction=np.clip(pred_by_village[v][mask]+delta,0,1)
            train_losses.append(float(np.mean(
                (group["endline"][mask]-prediction)**2)))
        training_macro_mse=float(np.mean(train_losses))
        if not math.isfinite(training_macro_mse):
            raise ValueError("nonfinite training score")
        options.append((training_macro_mse,order,name,delta))
    best=min(options,key=lambda x:(x[0],x[1]))
    return {"training_macro_mse":best[0],"variant":best[2],
            "train_drift":best[3]}


def score_lovo(groups,cache):
    keys=sorted(groups)
    if len(keys)!=EXPECTED_VILLAGES:
        raise ValueError("requires all sixteen source villages")
    outcomes={}
    for model in CLASSES:
        predictions=cache[model]
        mse_by_fold=[]
        mae_by_fold=[]
        total_error_sq=0.0
        total_error_abs=0.0
        total_count=0
        chosen=Counter()
        drifts=[]
        for village in keys:
            selection=choose_training(groups,predictions,village)
            chosen[selection["variant"]]+=1
            drifts.append(selection["train_drift"])
            g=groups[village]; mask=g["mask"]
            prediction=np.clip(
                predictions[selection["variant"]][village][mask]
                +selection["train_drift"],0,1)
            observed=g["endline"][mask]
            errors=prediction-observed
            mse=float(np.mean(errors**2))
            mae=float(np.mean(np.abs(errors)))
            n=int(mask.sum())
            mse_by_fold.append(mse)
            mae_by_fold.append(mae)
            total_error_sq+=mse*n
            total_error_abs+=mae*n
            total_count+=n
        if total_count!=BASELINE_SCORE_ROWS or len(mse_by_fold)!=EXPECTED_VILLAGES:
            raise ValueError("source scoring universe changed")
        outcomes[model]={
            "heldout_village_count":len(keys),
            "heldout_household_responses":total_count,
            "primary_macro_village_mse":float(np.mean(mse_by_fold)),
            "secondary_household_weighted_mse":total_error_sq/total_count,
            "secondary_household_weighted_mae":total_error_abs/total_count,
            "variant_selected_in_training_fold_counts":dict(sorted(chosen.items())),
            "train_fitted_drift_min":min(drifts),
            "train_fitted_drift_max":max(drifts),
            "village_label_level_detail_exported":False,
            "individual_prediction_exported":False,
        }
    return outcomes


def evaluate(source_dir:Path):
    groups,counts=create_villages(read_author_rows(source_dir))
    variants=precompute(groups)
    result=score_lovo(groups,variants)
    return {
        "stage":"R066_E2_THREE_OPINION_MODELS_LOVO",
        "status":"SOURCE_PINNED_16_VILLAGE_HELDOUT_COMPLETE",
        "protocol":"protocols/R066_E2_THREE_MODELS_LOVO_2026-10-16.md",
        "source":"doi:10.7910/DVN/RAHSVM",
        "source_version":"1.0",
        "dataset_universe":counts,
        "classes":result,
        "primary_metric":"equal-village-average heldout normalized attitude MSE",
        "secondary_metric":"household-weighted heldout normalized attitude MSE/MAE",
        "model_selection":"grid and additive drift trained on 15 other villages each fold",
        "forecast_origin":"post-intervention immediate score when available else baseline, prior to endline",
        "hk_network_semantics":"full village confidence peers, not observed social ties",
        "source_r_core_edge_parity_run":38865507356,
        "scientific_interpretation":"retrospective internal 16-village conditional prediction; cannot identify causal opinion mechanism",
        "e3_external_independent_cohort":"OPEN",
        "pesen_v01":"FROZEN",
    }


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-dir",type=Path,required=True)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    try:
        result=evaluate(args.source_dir)
    except (ValueError,OSError,UnicodeError) as exc:
        result={"stage":"R066_E2_THREE_OPINION_MODELS_LOVO",
                "status":"FAIL_CLOSED_OR_UNRESOLVED",
                "reason_type":type(exc).__name__,
                "reason":str(exc)[:250],
                "pesen_v01":"FROZEN"}
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
        "stage":result["stage"],
        "status":result["status"],
        "scores":{model:{
            "primary_macro_village_mse":row["primary_macro_village_mse"],
            "secondary_household_weighted_mse":row["secondary_household_weighted_mse"],
        } for model,row in result.get("classes",{}).items()},
    },sort_keys=True))
    if result["status"]!="SOURCE_PINNED_16_VILLAGE_HELDOUT_COMPLETE":
        raise RuntimeError("R066 real heldout gate did not pass")


if __name__=="__main__":
    main()
