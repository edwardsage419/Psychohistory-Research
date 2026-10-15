#!/usr/bin/env python3
"""R054: deterministic sequential history baselines for De Geest & Kingsley.

Research type: post-hoc retrospective benchmark; this program does not establish
causal identification, preregistration, or cross-study validity.

Run: python r054_history_bench.py --csv /path/to/author/data.csv --out results.json

The supplied CSV must match author's Git blob and has to be separately obtained
from https://github.com/lrdegeest/InequalityCPR/blob/master/data/data.csv.
"""
from __future__ import annotations
import argparse
from collections import defaultdict
from pathlib import Path
import hashlib
import json
import numpy as np

from r053_holdout import git_blob_sha, parse_raw_csv, build_transitions, evaluate

HISTORY_MODES = ('persistence','mean3','mean5','meanAll','ewmaHalf','priorGroupMean')


def _mean(v):
    if not v:
        raise ValueError('Empty history cannot predict')
    return sum(v)/len(v)


def history_forecast(rows: list[dict], strict: bool=True):
    """Return row predictions using information from strictly earlier rounds.

    No population-level training; each individual is predicted sequentially.
    Round 1 is practice and never used as history. Group mean is lagged by 1.
    """
    by_subject = defaultdict(list)
    by_cell = defaultdict(list)
    for row in rows:
        for key in ('ProfileID','RoundID','Invest','Session','GameID','Token'):
            if key not in row or row[key] is None:
                raise ValueError(f'Missing required field {key}')
        by_subject[int(row['ProfileID'])].append(row)
        group = (int(row['Session']), int(row['GameID']), int(row['RoundID']))
        by_cell[group].append(row)
    for members in by_cell.values():
        if strict and len(members)!=4:
            raise ValueError('Each group-period should have 4 observations')
        ids=[int(o['ProfileID']) for o in members]
        if len(set(ids))!=len(ids):
            raise ValueError('Duplicate subject in group-period')
    out=[]
    for sid,arr in sorted(by_subject.items()):
        arr.sort(key=lambda x:int(x['RoundID']))
        rounds=[int(x['RoundID']) for x in arr]
        if len(set(rounds))!=len(rounds):
            raise ValueError('Duplicate rounds within participant')
        if strict and rounds!=list(range(1,17)):
            raise ValueError('Nonconsecutive full experiment history')
        for j in range(2,len(arr)):
            current=arr[j]
            if int(current['RoundID'])<3:
                continue
            previous=arr[j-1]
            if int(current['RoundID']) != int(previous['RoundID'])+1:
                raise ValueError('Cross-period prediction leakage')
            if (current['Session'],current['GameID']) != (previous['Session'],previous['GameID']):
                raise ValueError('Changed group without resetting history')
            if int(current['Token']) != int(previous['Token']):
                raise ValueError('Changed resource cap within participant')
            hist=[float(z['Invest']) for z in arr[1:j]]
            if not hist:
                raise ValueError('Missing observed formal history')
            past_group=by_cell[(int(current['Session']),int(current['GameID']),int(current['RoundID'])-1)]
            if not past_group:
                raise ValueError('Missing prior group observations')
            ema=hist[0]
            for v in hist[1:]:
                ema=0.5*v+0.5*ema
            candidate={
                'persistence': hist[-1],
                'mean3': _mean(hist[-3:]),
                'mean5': _mean(hist[-5:]),
                'meanAll': _mean(hist),
                'ewmaHalf': ema,
                'priorGroupMean': _mean([float(z['Invest']) for z in past_group]),
            }
            cap=float(current['Token'])
            if any(not (0<=x<=cap) for x in [float(current['Invest']),*candidate.values()]):
                raise ValueError('Outcome or prediction out of range')
            out.append({'session':int(current['Session']), 'subject':sid,
                'round':int(current['RoundID']), 'FF':int(current.get('FF',0)),
                'y':float(current['Invest']), 'pred':candidate})
    if strict and (len(out)!=1792 or len(by_subject)!=128 or len(by_cell)!=512):
        raise ValueError('Unexpected official sample structure')
    return out


def score_prediction_rows(pred_rows):
    folds=[]
    for session in sorted({o['session'] for o in pred_rows}):
        arr=[o for o in pred_rows if o['session']==session]
        if not arr:
            raise ValueError('Empty fold')
        by_mode={}
        for m in HISTORY_MODES:
            errors=np.array([o['y']-o['pred'][m] for o in arr],dtype=float)
            by_mode[m]={'mse':float(np.mean(errors*errors)),
                        'mae':float(np.mean(np.abs(errors)))}
        folds.append({'session':session,'n':len(arr),'models':by_mode})
    n=sum(f['n'] for f in folds)
    overall={m:{metric:sum(f['n']*f['models'][m][metric] for f in folds)/n
                for metric in ('mse','mae')} for m in HISTORY_MODES}
    return {'n':n,'folds':folds,'overall':overall}


def compare_to_r053(history, r053_results):
    folds=r053_results['heldout_folds_rounded_4_decimals']
    if len(folds)!=8 or len(history['folds'])!=8:
        raise ValueError('Expected eight sessions in comparison')
    by_session={x['session']:x for x in history['folds']}
    d=np.asarray([float(f['M1'])-by_session[f['session']]['models']['meanAll']['mse'] for f in folds])
    rng=np.random.default_rng(20261015)
    draws=rng.integers(0, len(d), size=(20000,len(d)))
    boot=d[draws].mean(axis=1)
    import itertools
    perms=np.asarray(list(itertools.product([-1,1],repeat=len(d))),dtype=float)
    p=float(np.mean(np.abs((perms*d).mean(axis=1))>=abs(d.mean())-1e-12))
    return {'contrast':'R053 M1 MSE minus individual meanAll MSE',
        'mean_difference':float(d.mean()),'m1_better_sessions':int(sum(d<0)),
        'session_differences':list(map(float,d)),
        'session_bootstrap_95':list(map(float,np.quantile(boot,[.025,.975]))),
        'sign_flip_p_exploratory':p,'disclaimer':'R053 M1 folds had only 4-digit printed precision'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--csv',required=True,type=Path)
    p.add_argument('--out',required=True,type=Path)
    p.add_argument('--r053-json',default=None,type=Path)
    a=p.parse_args()
    raw=a.csv.read_bytes()
    rows=parse_raw_csv(raw,source_check=True)
    hist=score_prediction_rows(history_forecast(rows,strict=True))
    results={'study':'De Geest & Kingsley InequalityCPR',
             'source_git_blob_sha1':git_blob_sha(raw),
             'source_sha256':hashlib.sha256(raw).hexdigest(),
             'analysis':'exploratory post-hoc historical baseline comparison',
             'history_scores':hist}
    # Existing R053 historical benchmark can be re-evaluated only after source access
    transitions,source_audit=build_transitions(rows,strict=True)
    results['source_audit']=source_audit
    results['r053_replayed']=evaluate(transitions)
    if a.r053_json:
        results['crosscheck_against_previous_summary']=compare_to_r053(hist,json.loads(a.r053_json.read_text()))
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(results,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'source_verified':True,'history_mse':{m:hist['overall'][m]['mse'] for m in HISTORY_MODES},
                      'r053_mse':results['r053_replayed']['overall']['mse']},ensure_ascii=False))

if __name__=='__main__':
    main()