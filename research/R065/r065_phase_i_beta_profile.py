#!/usr/bin/env python3
"""R065 I: copy-last Model3 beta robustness from aggregate choice counts.

Source-equivalent -log(p + 1e-10) likelihood, beta range [0,30].
Input count summaries are not primary raw-source evidence; when source-dir is
provided, upstream raw Git SHA identities are enforced via the Phase H parser.
"""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
from typing import Iterable

AUTHOR = (23,45,67,89,111)
BLOCK = (18,35,52,69,86,103,120)
PROFILE = (0,0.5,1,2,3,5,10,20,30)
COUNT_KEYS = ('match','mismatch','uniform','play')
MAX_BETA = 30.0
EPS = 1e-10


def validate_counts(c: dict) -> None:
    if not isinstance(c,dict) or any(type(c.get(k)) is not int or c[k] < 0 for k in COUNT_KEYS):
        raise ValueError('invalid integer choice counts')
    if c['play'] <= 0 or c['match'] + c['mismatch'] + c['uniform'] != c['play']:
        raise ValueError('inconsistent choice counts')


def counts_for(trials: Iterable[dict], reset_days: tuple[int,...]) -> dict:
    """Reconstruct the author Model 3's exact observe/play reset timing."""
    c = dict.fromkeys(COUNT_KEYS,0)
    previous = None
    for x in trials:
        if x['day'] in reset_days:
            previous = None
        if x['type'] == 'observe':
            previous = x['chosen']
        elif x['type'] == 'play':
            c['play'] += 1
            if previous is None or previous not in x['available']:
                c['uniform'] += 1
            elif previous == x['chosen']:
                c['match'] += 1
            else:
                c['mismatch'] += 1
        else:
            raise ValueError('not an observe or play trial')
    validate_counts(c)
    return c


def combine(parts: Iterable[dict]) -> dict:
    out = dict.fromkeys(COUNT_KEYS,0)
    found = False
    for c in parts:
        validate_counts(c)
        for key in COUNT_KEYS:
            out[key] += c[key]
        found = True
    if not found:
        raise ValueError('no participants')
    return out


def subtract(all_count:dict, held_out:dict)->dict:
    validate_counts(all_count);validate_counts(held_out)
    out={k:all_count[k]-held_out[k] for k in COUNT_KEYS}
    validate_counts(out)
    return out


def nll(c:dict,beta:float)->float:
    validate_counts(c)
    if not math.isfinite(beta) or not 0 <= beta <= MAX_BETA:
        raise ValueError('beta must be in [0,30]')
    p_match=1/(1+math.exp(-beta))
    p_mismatch=1/(1+math.exp(beta))
    return (-c['match']*math.log(p_match+EPS)
            -c['mismatch']*math.log(p_mismatch+EPS)
            -c['uniform']*math.log(.5+EPS))


def fit_beta(c:dict)->dict:
    validate_counts(c)
    # Unperturbed logistic MLE cross-check; exact code objective includes EPS.
    if c['match']==0:
        analytic=0.
    elif c['mismatch']==0:
        analytic=MAX_BETA
    else:
        analytic=max(0.,min(MAX_BETA,math.log(c['match']/c['mismatch'])))
    left,right=0.,MAX_BETA
    invphi=(math.sqrt(5)-1)/2
    a=right-invphi*(right-left)
    b=left+invphi*(right-left)
    fa,fb=nll(c,a),nll(c,b)
    for _ in range(150):
        if fa<fb:
            right,b,fb=b,a,fa
            a=right-invphi*(right-left)
            fa=nll(c,a)
        else:
            left,a,fa=a,b,fb
            b=left+invphi*(right-left)
            fb=nll(c,b)
    mid=(left+right)/2
    candidates=[(v,nll(c,v)) for v in (0.,mid,MAX_BETA)]
    beta,loss=min(candidates,key=lambda x:x[1])
    if abs(beta-analytic)>5e-5:
        raise ValueError('optimizer and analytic MLE disagree')
    return {'beta':beta,'total_nll':loss,'analytic_beta_check':analytic,
            'beta_at_boundary':beta in (0.,MAX_BETA)}


def profile(c:dict)->dict:
    validate_counts(c)
    return {'counts':c,'beta_grid':[{'beta':beta,'mean_nll':nll(c,beta)/c['play']}
                                   for beta in PROFILE],
            'pooled_fit':fit_beta(c)}


def lopo(per_subject:list[dict])->dict:
    if len(per_subject)<2:
        raise ValueError('need at least two participants')
    all_count=combine(per_subject)
    total=0.; betas=[]
    for heldout in per_subject:
        training=subtract(all_count,heldout)
        selected=fit_beta(training)['beta']
        betas.append(selected)
        total+=nll(heldout,selected)
    return {'total_nll':total,'mean_nll':total/all_count['play'],
            'min_beta':min(betas),'max_beta':max(betas),
            'zero_boundary_folds':sum(x==0 for x in betas),
            'folds':len(per_subject)}


def summary_from_raw(source_dir:Path)->dict:
    from r065_phase_h_model3_reset import SAMPLE_BLOBS,source_trials
    all_trials=[source_trials((source_dir/name).read_bytes(),sha) for name,sha in SAMPLE_BLOBS.items()]
    data={}
    for key,resets in (('author',AUTHOR),('block',BLOCK)):
        parts=[counts_for(trials,resets) for trials in all_trials]
        c=combine(parts)
        data[key]={**profile(c),'lopo':lopo(parts)}
    return {'scope':'UPSTREAM_RAW_FILES_GIT_BLOB_VERIFIED_SOURCE_EQUIVALENT_PORT',
            'subjects':len(all_trials),'models':data}


def summary_from_aggregate(obj:dict)->dict:
    if obj.get('study')!='R065_PHASE_I' or obj.get('subjects')!=10:
        raise ValueError('wrong aggregate artifact')
    data={}
    for name in ('author','block'):
        expected_reset=AUTHOR if name=='author' else BLOCK
        value=obj['models'][name]
        if value['reset_days']!=list(expected_reset):
            raise ValueError('reset days mismatch')
        data[name]=profile(value['counts'])
    return {'scope':'AGGREGATE_COUNTS_ONLY_NO_INDIVIDUAL_HOLDOUT_REPLAY',
            'subjects':10,'models':data}


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    group=ap.add_mutually_exclusive_group(required=True)
    group.add_argument('--aggregate-input',type=Path)
    group.add_argument('--source-dir',type=Path)
    ap.add_argument('--output',type=Path)
    args=ap.parse_args()
    result=(summary_from_raw(args.source_dir) if args.source_dir
            else summary_from_aggregate(json.loads(args.aggregate_input.read_text(encoding='utf-8'))))
    rendered=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
    if args.output:args.output.write_text(rendered,encoding='utf-8')
    print(rendered,end='')
if __name__=='__main__':main()
