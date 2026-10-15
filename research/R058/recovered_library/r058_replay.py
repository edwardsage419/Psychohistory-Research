#!/usr/bin/env python3
"""R058 network-run held-out audit. Uses anonymized counts verified from Priniski et al GitHub source.

Never treats grouping labels, DecisionType, current-round Points or partner_response as predictive inputs.
On-disk raw CSV reproduction requires all 26 files; performs git blob SHA verification.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, math, re
from collections import defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent
MISSING={'', 'nan', 'NA', 'NaN', 'None', 'null'}


def read_counts(path=ROOT/'R058_CONNECTOR_COUNTS.tsv'):
    runs=[]
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        if not line or line.startswith('#'): continue
        cols=line.split('|')
        if len(cols)!=8: raise ValueError('bad column count')
        name,sha,nrows,nids,*phases=cols
        match=re.fullmatch(r'([fh])(20|50|100)([hs])(\d+)',name)
        if not match or len(sha)!=40 or not re.fullmatch('[a-f0-9]{40}',sha): raise ValueError('bad run metadata')
        if len(phases)!=4: raise ValueError('four phases required')
        cells={}
        for phase,entry in enumerate(phases):
            parts=entry.split(';')
            if len(parts)!=2: raise ValueError('two agreement states required')
            for agree,part in enumerate(parts):
                n,self_count,copy_count=map(int,part.split(','))
                if min(n,self_count,copy_count)<0 or max(self_count,copy_count)>n: raise ValueError('invalid counts')
                if agree and self_count!=copy_count: raise ValueError('identical lag responses must have identical match counts')
                if not agree and self_count+copy_count>n: raise ValueError('exclusive events exceed N')
                cells[(phase,agree)]=(n,self_count,copy_count)
        r={'name':name,'sha':sha,'raw_rows':int(nrows),'ids':int(nids),
           'content':'face' if match[1]=='f' else 'hashtag',
           'size':int(match[2]), 'structure':'homogeneous' if match[3]=='h' else 'spatial','cells':cells}
        eligible=sum(z[0] for z in cells.values())
        if not (0<=eligible<=r['raw_rows']<=r['size']*40): raise ValueError('invalid run row count')
        if not(0<r['ids']<=r['size']):raise ValueError('invalid id count')
        runs.append(r)
    if len({r['name'] for r in runs})!=len(runs):raise ValueError('duplicate run')
    return runs


def git_sha(blob:bytes)->str:
    return hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()


def recount_raw_bytes(raw:bytes):
    import io
    reader=csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline=''))
    required={'id','TrialNumber','Response','prev_response','partner_prev_response','partner_response'}
    if not required.issubset(reader.fieldnames or []): raise ValueError('missing required raw columns')
    rows=list(reader)
    lookup={}
    for row in rows:
        key=(row['id'],int(row['TrialNumber']))
        if key in lookup:raise ValueError('duplicate subject-round key')
        lookup[key]=row
    cells=defaultdict(lambda:[0,0,0])
    checks={'self_compared':0,'self_mismatch':0,'partner_compared':0,'partner_mismatch':0}
    for row in rows:
        t=int(row['TrialNumber'])
        if t<3:continue
        y,prev,peer=row['Response'],row['prev_response'],row['partner_prev_response']
        if any(z in MISSING for z in (y,prev,peer)):continue
        parent=lookup.get((row['id'],t-1))
        if parent is not None:
            if parent['Response'] not in MISSING:
                checks['self_compared']+=1
                if parent['Response']!=prev: checks['self_mismatch']+=1
            if parent['partner_response'] not in MISSING:
                checks['partner_compared']+=1
                if parent['partner_response']!=peer:checks['partner_mismatch']+=1
        phase=min(3,(t-1)//10)
        agree=int(prev==peer)
        a=cells[(phase,agree)]
        a[0]+=1;a[1]+=int(y==prev);a[2]+=int(y==peer)
    return {'rows':len(rows),'ids':len({z['id'] for z in rows}),
            'cells':{(i,j):tuple(cells[(i,j)]) for i in range(4) for j in range(2)},'checks':checks}


def verify_raw(runs, raw_dir):
    dirpath=Path(raw_dir)
    for run in runs:
        p=dirpath/f"{run['name']}.csv"
        if not p.exists():raise FileNotFoundError(p)
        b=p.read_bytes()
        if git_sha(b)!=run['sha']:raise ValueError(f"GIT_BLOB_MISMATCH {run['name']}")
        x=recount_raw_bytes(b)
        if x['rows']!=run['raw_rows'] or x['ids']!=run['ids'] or x['cells']!=run['cells']:
            raise ValueError(f"COUNT_MISMATCH {run['name']}")
        if x['checks']['self_mismatch'] or x['checks']['partner_mismatch']:
            raise ValueError(f"TIMING_MISMATCH {run['name']}")
    return True


def cell_sum(runs, pred):
    n=s=0
    for run in runs:
        for (phase,agree),(k,yes,_copy) in run['cells'].items():
            if pred(run,phase,agree): n+=k;s+=yes
    return n,s


def shrink(n,s,prior,strength):
    return (s+strength*prior)/(n+strength)


def probs(train,run,phase,agree):
    total,success=cell_sum(train,lambda r,p,a:True)
    p0=(success+1)/(total+2)
    n1,s1=cell_sum(train,lambda r,p,a:r['content']==run['content'] and p==phase)
    p1=shrink(n1,s1,p0,40)
    n2,s2=cell_sum(train,lambda r,p,a:r['content']==run['content'] and r['structure']==run['structure'] and p==phase)
    p2=shrink(n2,s2,p1,30)
    n3,s3=cell_sum(train,lambda r,p,a:r['content']==run['content'] and r['structure']==run['structure'] and p==phase and a==agree)
    p3=shrink(n3,s3,p2,20)
    return (p0,p1,p2,p3)


def run_cv(runs):
    if len(runs)<3:raise ValueError('at least 3 runs required')
    results=[]
    for held in runs:
        train=[r for r in runs if r['name']!=held['name']]
        output={'run':held['name'],'content':held['content'],'structure':held['structure'],'size':held['size'],'n':0}
        for key in ['logloss','brier']:
            for m in range(4):output[f'm{m}_{key}']=0.0
        for (phase,agree),(n,s,copy) in held['cells'].items():
            if not n:continue
            pp=probs(train,held,phase,agree)
            output['n']+=n
            for j,p in enumerate(pp):
                output[f'm{j}_logloss']+= -s*math.log(p)-(n-s)*math.log1p(-p)
                output[f'm{j}_brier']+=s*(1-p)**2+(n-s)*p*p
        for k in list(output):
            if k.startswith('m') and '_' in k:output[k]/=output['n']
        results.append(output)
    return results


def aggregate_cv(results):
    n=sum(r['n'] for r in results)
    out={'n':n,'runs':len(results)}
    for measure in ['logloss','brier']:
        for m in range(4):
            key=f'm{m}_{measure}'
            out[key]=sum(r['n']*r[key] for r in results)/n
    return out


def bootstrap_diff(results,compare='m3',baseline='m2',repetitions=20000,seed=5801):
    import random
    rng=random.Random(seed)
    observed=(sum(r['n']*(r[f'{compare}_logloss']-r[f'{baseline}_logloss']) for r in results)/sum(r['n'] for r in results))
    arr=[]
    for i in range(repetitions):
        sel=rng.choices(results,k=len(results)); num=sum(r['n']*(r[f'{compare}_logloss']-r[f'{baseline}_logloss']) for r in sel);den=sum(r['n'] for r in sel);arr.append(num/den)
    arr.sort()
    return {'contrast':observed,'bootstrap95':[arr[int(repetitions*.025)],arr[int(repetitions*.975)]],
            'improved_runs':sum(r[f'{compare}_logloss']<r[f'{baseline}_logloss'] for r in results),
            'runs':len(results),'draws':repetitions,'seed':seed}


def source_summary(runs):
    eligible=sum(sum(c[0] for c in r['cells'].values()) for r in runs)
    disagree=sum(sum(c[0] for (ph,a),c in r['cells'].items() if a==0) for r in runs)
    copy=sum(sum(c[2] for (ph,a),c in r['cells'].items() if a==0) for r in runs)
    self_rep=sum(sum(c[1] for c in r['cells'].values()) for r in runs)
    by={}
    for condition in ('face_homogeneous','face_spatial','hashtag_homogeneous','hashtag_spatial'):
        content,structure=condition.split('_');rr=[x for x in runs if x['content']==content and x['structure']==structure]
        n=sum(sum(c[0] for c in r['cells'].values()) for r in rr)
        d=sum(sum(c[0] for (phase,a),c in r['cells'].items() if a==0) for r in rr)
        cp=sum(sum(c[2] for (phase,a),c in r['cells'].items() if a==0) for r in rr)
        by[condition]={'runs':len(rr),'n':n,'disagreements':d,'copy_disagreement':cp,'copy_rate_disagreement':cp/d}
    return {'networks':len(runs),'source_rows':sum(r['raw_rows'] for r in runs),'actors_observed_per_network_sum':sum(r['ids'] for r in runs),'eligible':eligible,'self_repeat':self_rep,'self_repeat_rate':self_rep/eligible,'disagreement':disagree,'partner_copy_disagreement':copy,'partner_copy_rate_disagreement':copy/disagree,'conditions':by}


def run_main(counts,raw_dir=None):
    runs=read_counts(counts)
    if raw_dir:verify_raw(runs,raw_dir)
    cv=run_cv(runs)
    return {'reproduction':{'counts_verified':'CONNECTOR_DERIVED','local_raw_verified':bool(raw_dir)},
            'source':source_summary(runs),'cv':aggregate_cv(cv),
            'bootstrap_m3_vs_m2':bootstrap_diff(cv,'m3','m2'),
            'bootstrap_m2_vs_m1':bootstrap_diff(cv,'m2','m1'),
            'per_run':cv}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--counts',type=Path,default=ROOT/'R058_CONNECTOR_COUNTS.tsv')
    parser.add_argument('--raw-dir',type=Path,default=None)
    parser.add_argument('--json-out',type=Path,default=ROOT/'R058_RESULTS.json')
    args=parser.parse_args()
    result=run_main(args.counts,args.raw_dir)
    args.json_out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='per_run'},ensure_ascii=False,indent=2))