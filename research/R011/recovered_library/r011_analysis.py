#!/usr/bin/env python3
"""R011: Becker et al. 2019 cross-trial placebo-signal diagnostic.

Examine ONLY Experiment 1, positive finite three-wave complete cases.
Proxy signals: leave-one-out trial average; independent opposite-party matched-trial average.
Neither proxy is actual shown 4-neighbor information.

Usage: python r011_analysis.py path/to/author_data.csv --output r011_results.json
Standard library only. DOI: 10.1073/pnas.1817195116.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

SOURCE_REPOSITORY = 'https://github.com/joshua-a-becker/wisdom-of-partisan-crowds'
SOURCE_BLOB_SHA = '2fc18cefd211727e560b05d60c1289f1f4891969'


def blob_sha(data: bytes) -> str:
    """Compute Git's blob SHA-1, not raw-file SHA-1."""
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def read_cases(path: Path):
    data = path.read_bytes()
    text = data.decode('utf-8-sig')
    source_rows = list(csv.DictReader(text.splitlines()))
    cases=[]
    rejected=defaultdict(int)
    for row in source_rows:
        if row['experiment'] != '1':
            continue
        try:
            estimates=[float(row['response_'+str(t)]) for t in [1,2,3]]
            truth=float(row['truth'])
        except (ValueError,TypeError,KeyError):
            rejected['missing_or_non_numeric']+=1
            continue
        if truth<=0 or not math.isfinite(truth) or any(v<=0 or not math.isfinite(v) for v in estimates):
            rejected['non_positive_or_non_finite']+=1
            continue
        if row['party'] not in ('Dem','Repub') or row['network'] not in ('Social','Control'):
            rejected['bad_condition']+=1
            continue
        cases.append({
            'party':row['party'],'set':row['set'],'pair':str(row['pair_id']),
            'condition':row['network'],'question':row['q'],
            'x':[math.log(v) for v in estimates],
            'truth':math.log(truth),
        })
    return cases, dict(rejected), {'filename':path.name,'sha256':hashlib.sha256(data).hexdigest(),
                                  'git_blob_sha':blob_sha(data),'bytes':len(data),
                                  'raw_records':len(source_rows)}


def observations(cases):
    """All pairs matched across opposite-party, same set, trial index, arm and question."""
    groups=defaultdict(list)
    for c in cases:
        groups[(c['party'],c['set'],c['pair'],c['condition'],c['question'])].append(c)
    output=[]; unmatched=0
    for (party,set_,pair,arm,question),group in groups.items():
        other_party='Repub' if party=='Dem' else 'Dem'
        peer_group=groups.get((other_party,set_,pair,arm,question))
        if not peer_group or len(group)<3 or len(peer_group)<3:
            unmatched+=len(group)
            continue
        for t in (0,1):
            sum_log=sum(p['x'][t] for p in group)
            fake_mean=sum(p['x'][t] for p in peer_group)/len(peer_group)
            for p in group:
                initial=p['x'][t]
                output.append({
                    'arm':arm,'round':t+1,'pair_key':(set_,pair,arm),
                    'trial_key':(party,set_,pair,arm),
                    'y':p['x'][t+1]-initial,
                    'same':(sum_log-initial)/(len(group)-1)-initial,
                    'other':fake_mean-initial,
                })
    if not output:
        raise ValueError('No matched valid observations; inspect data and schemas')
    return output, unmatched


def slope(rows,key):
    d2=sum(x[key]*x[key] for x in rows)
    return sum(x[key]*x['y'] for x in rows)/d2 if d2>1e-10 else 0.0


def heldout_score(records, arm, key, t='both'):
    selected=[r for r in records if r['arm']==arm and (t=='both' or r['round']==t)]
    if not selected: raise ValueError('No data for condition')
    pair_ids=sorted({r['pair_key'] for r in selected})
    if len(pair_ids)<2: raise ValueError('Need >= 2 independent matched trial pairs')
    beta=slope(selected,key) if key else 0.0
    loss=0.0
    for pair_id in pair_ids:
        train=[x for x in selected if x['pair_key'] != pair_id]
        test=[x for x in selected if x['pair_key'] == pair_id]
        b=slope(train,key) if key else 0.0
        loss+=sum((x['y']-(b*x[key] if key else 0.0))**2 for x in test)
    return {'n_person_rounds':len(selected),'n_holdout_pairs':len(pair_ids),
            'full_sample_slope':round(beta,9), 'holdout_pair_mse':round(loss/len(selected),9)}


def analyze(cases):
    records,unmatched=observations(cases)
    comparisons={}
    for arm in ('Social','Control'):
        comparisons[arm]={}
        for t in (1,2,'both'):
            comparisons[arm][str(t)]={
                'M0_inertia':heldout_score(records,arm,None,t),
                'M_same_trial_mean_PROXY':heldout_score(records,arm,'same',t),
                'M_opposite_party_PLACEBO':heldout_score(records,arm,'other',t),
            }
    return {'n_valid_individual_question_rows':len(cases),
            'n_person_round_observations':len(records),
            'n_unmatched_rows':unmatched,'comparisons':comparisons}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('csv',type=Path,help='Exact unmodified authors CSV downloaded from GitHub')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    cases,excluded,source=read_cases(args.csv)
    results={'study':'R011','status':'REAL_AUTHOR_CSV_ANALYSIS',
             'source':{**source,'repository':SOURCE_REPOSITORY,'expected_git_blob_sha':SOURCE_BLOB_SHA},
             'rejected':excluded,'analysis':analyze(cases),
             'important_warning': 'Two constructed peer-mean PROXIES, not actually shown four-neighbor signals; placebo is not exposure. Descriptive, noncausal test.'}
    if source['git_blob_sha']!=SOURCE_BLOB_SHA:
        raise ValueError('Author source SHA differs from original revision: investigate; do not silently use revised dataset')
    out=json.dumps(results,indent=2,ensure_ascii=False)+'\n'
    if args.output:args.output.write_text(out,encoding='utf-8')
    else:print(out)

if __name__=='__main__':main()