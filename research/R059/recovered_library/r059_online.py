#!/usr/bin/env python3
"""R059: per-person chronological prediction vs previous-reward condition.

Two execution tiers:
  (1) --derived-only verifies 26 source-linked connector summary rows and
      computes network-level contrasts without claiming local raw replication.
  (2) --raw-dir verifies each of the 26 actual Git blob SHA1s, recomputes
      R058 cells plus R059 online scores/previous reward identities, and
      checks connector-side references with tight numeric tolerance.

Prediction uses only past choices. Current Points, current partner_response,
DecisionType, and future trial rows are NEVER predictive inputs.
"""
from __future__ import annotations
import argparse, csv, io, json, math, random
from collections import defaultdict
from pathlib import Path
from r058_replay import read_counts, git_sha, recount_raw_bytes

ROOT=Path(__file__).resolve().parent
MISSING={'', 'nan','NaN','NA','None','null'}
MODES=('beta2','beta8','beta20','last5','ewma20','reward_condition4','reward_condition12')


def read_pipe(path, value_cols):
    lines=[l for l in Path(path).read_text(encoding='utf-8').splitlines() if l and not l.startswith('#')]
    rows=list(csv.DictReader(lines,delimiter='|'))
    if not rows or len({r['run'] for r in rows})!=len(rows): raise ValueError('duplicate/missing run')
    for row in rows:
        row['n']=int(row['n'])
        if 'rows' in row:row['rows']=int(row['rows'])
        for c in value_cols:row[c]=float(row[c])
        if row['n']<1:raise ValueError('empty evaluated run')
        if any(not math.isfinite(row[c]) or row[c]<0 for c in value_cols):raise ValueError('nonfinite loss')
    return {x['run']:x for x in rows}


def read_connector_online(path=ROOT/'R059_CONNECTOR_ONLINE.tsv'):
    return read_pipe(path,['beta2','beta8','beta20','last5','ewma20'])


def read_reward_conditional(path=ROOT/'R059_REWARD_CONDITIONAL.tsv'):
    return read_pipe(path,['personal_ewma20','reward_condition4','reward_condition12'])


def predict_person(history, ewma):
    n=len(history);s=sum(history);last=history[-5:]
    return {'beta2':(s+1)/(n+2),'beta8':(s+4)/(n+8),
            'beta20':(s+10)/(n+20),'last5':(sum(last)+1)/(len(last)+2),
            'ewma20':ewma}


def conditional_probability(ewma, group_stats, prev_reward, k):
    n,s=group_stats[prev_reward]
    return (s+k*ewma)/(n+k)


def loss(y,p):
    if y not in (0,1) or not(0<p<1):raise ValueError('invalid binary loss')
    return -y*math.log(p)-(1-y)*math.log1p(-p)


def online_rows(rows, with_predictions=False):
    """Raw dictionaries, returns diagnostics and per-network mean log losses.

    Exact eligible definition is R058: t>=3 and Response, prev_response,
    partner_prev_response nonmissing. History may include t=2 choice even
    though previous-partner information is missing there (legal prior input).
    """
    required={'id','TrialNumber','Response','prev_response','partner_prev_response',
              'partner_response','Points'}
    if not rows or any(not required.issubset(r) for r in rows):raise ValueError('missing fields')
    by_person=defaultdict(list); lookup={}
    for row in rows:
        t=int(row['TrialNumber']);key=(row['id'],t)
        if key in lookup:raise ValueError('duplicate person-round')
        lookup[key]=row;by_person[row['id']].append(row)
    sums=dict.fromkeys(MODES,0.0); brier=dict.fromkeys(MODES,0.0)
    diag={'rows':len(rows),'ids':len(by_person),'eligible':0,'earlier_updates':0,
          'reward_compared':0,'reward_mismatch':0,
          'self_compared':0,'self_mismatch':0,
          'peer_compared':0,'peer_mismatch':0}
    detail=[]
    for user,series in by_person.items():
        series.sort(key=lambda r:int(r['TrialNumber']))
        history=[];ewma=.5;group_stats={0:[0,0],1:[0,0]}
        for z in series:
            t=int(z['TrialNumber']);can_update=t>=2 and z['Response'] not in MISSING and z['prev_response'] not in MISSING
            eligible=t>=3 and can_update and z['partner_prev_response'] not in MISSING
            if eligible:
                y=int(z['Response']==z['prev_response'])
                prev_reward=int(z['prev_response']==z['partner_prev_response'])
                pp=predict_person(history,ewma)
                pp['reward_condition4']=conditional_probability(ewma,group_stats,prev_reward,4)
                pp['reward_condition12']=conditional_probability(ewma,group_stats,prev_reward,12)
                for key,p in pp.items():
                    sums[key]+=loss(y,p)
                    brier[key]+=(y-p)**2
                diag['eligible']+=1
                prev=lookup.get((user,t-1))
                if prev is not None and prev['Response'] not in MISSING:
                    diag['self_compared']+=1
                    diag['self_mismatch']+=int(prev['Response']!=z['prev_response'])
                if prev is not None and prev['partner_response'] not in MISSING:
                    diag['peer_compared']+=1
                    diag['peer_mismatch']+=int(prev['partner_response']!=z['partner_prev_response'])
                if prev is not None and prev['Points'] not in MISSING:
                    point=float(prev['Points'])
                    if point not in (0,1):raise ValueError('unexpected point value')
                    diag['reward_compared']+=1
                    diag['reward_mismatch']+=int((point==1)!=(prev_reward==1))
                if with_predictions:detail.append({'user':user,'t':t,'y':y,'previous_reward':prev_reward,**pp})
                group_stats[prev_reward][0]+=1;group_stats[prev_reward][1]+=y
            if can_update:
                yy=int(z['Response']==z['prev_response'])
                history.append(yy);ewma=.8*ewma+.2*yy
                diag['earlier_updates']+=1
    n=diag['eligible']
    if not n:raise ValueError('no eligible data')
    out={'metrics':{key:sums[key]/n for key in MODES},
         'brier':{key:brier[key]/n for key in MODES},'checks':diag}
    if with_predictions:out['predictions']=detail
    return out


def raw_file(path):
    return list(csv.DictReader(io.StringIO(Path(path).read_bytes().decode('utf-8-sig'),newline='')))


def verify_raw_file(path, metadata, legacy, online, conditional):
    raw=Path(path).read_bytes()
    if git_sha(raw)!=metadata['sha']:raise ValueError('Git blob mismatch: '+metadata['name'])
    recount=recount_raw_bytes(raw)
    if (recount['rows'],recount['ids'],recount['cells'])!=(metadata['raw_rows'],metadata['ids'],metadata['cells']):
        raise ValueError('R058 cell mismatch: '+metadata['name'])
    out=online_rows(raw_file(path))
    d=out['checks'];n=metadata['name']
    if d['eligible']!=online[n]['n'] or d['rows']!=online[n]['rows']:
        raise ValueError('R059 rows mismatch '+n)
    if any(d[k]!=0 for k in ('self_mismatch','peer_mismatch','reward_mismatch')):
        raise ValueError('timing or reward mismatch '+n)
    if d['reward_compared']!=d['eligible']:
        raise ValueError('not all rewards could be verified '+n)
    for key in ('beta2','beta8','beta20','last5','ewma20'):
        if abs(out['metrics'][key]-online[n][key])>1e-10:
            raise ValueError('R059 personal score mismatch '+n+' '+key)
    for key in ('reward_condition4','reward_condition12'):
        if abs(out['metrics'][key]-conditional[n][key])>1e-10:
            raise ValueError('R059 reward score mismatch '+n+' '+key)
    return out


def weighted_mean(rows,key):
    return sum(r['n']*r[key] for r in rows)/sum(r['n'] for r in rows)


def bootstrap(rows,a,b='m3',draws=20000,seed=5901):
    rng=random.Random(seed)
    obs=weighted_mean(rows,a)-weighted_mean(rows,b)
    vals=[]
    for _ in range(draws):
        rr=rng.choices(rows,k=len(rows))
        vals.append(weighted_mean(rr,a)-weighted_mean(rr,b))
    vals.sort();return{'difference':obs,'bootstrap_95':[vals[int(.025*draws)],vals[int(.975*draws)]],
                        'networks_improved':sum(r[a]<r[b] for r in rows),'networks':len(rows),
                        'bootstrap_seed':seed,'bootstrap_draws':draws}


def run_main(raw_dir=None,personal_path=ROOT/'R059_CONNECTOR_ONLINE.tsv',
             conditional_path=ROOT/'R059_REWARD_CONDITIONAL.tsv'):
    metadata=read_counts(ROOT/'R058_CONNECTOR_COUNTS.tsv')
    if len(metadata)!=26:raise ValueError('expected all 26 original networks')
    expected={z['name'] for z in metadata}
    online=read_connector_online(personal_path);conditional=read_reward_conditional(conditional_path)
    if set(online)!=expected or set(conditional)!=expected:raise ValueError('network identity mismatch')
    old=json.loads((ROOT/'R058_RESULTS.json').read_text(encoding='utf-8'))
    prev={r['run']:r for r in old['per_run']}
    if set(prev)!=expected:raise ValueError('R058 reference identity mismatch')
    rows=[]
    for r in metadata:
        name=r['name'];a=online[name];b=conditional[name]
        expected_n=sum(z[0] for z in r['cells'].values())
        if a['n']!=b['n'] or a['n']!=prev[name]['n'] or a['n']!=expected_n:
            raise ValueError('network sample mismatch '+name)
        if a['rows']!=r['raw_rows'] or abs(a['ewma20']-b['personal_ewma20'])>1e-12:
            raise ValueError('source count or score mismatch '+name)
        item={'run':name,'sha':r['sha'],'n':a['n'],'raw_rows':a['rows'],
              'm3':prev[name]['m3_logloss'],**{m:a[m] for m in ('beta2','beta8','beta20','last5','ewma20')},
              **{m:b[m] for m in ('reward_condition4','reward_condition12')}}
        if raw_dir is not None:verify_raw_file(Path(raw_dir)/f'{name}.csv',r,prev[name],online,conditional)
        rows.append(item)
    if sum(r['n'] for r in rows)!=36780 or sum(r['raw_rows'] for r in rows)!=39619:
        raise ValueError('unexpected total samples')
    measures=('m3','beta2','beta8','beta20','last5','ewma20','reward_condition4','reward_condition12')
    return{'source_status':{'connector_original_verified':True,'local_original_bytes_verified':raw_dir is not None,
                             'networks':26,'raw_rows':39619,'eligible':36780,
                             'reward_agreement_mismatches_connector':0},
           'weighted_logloss':{m:weighted_mean(rows,m) for m in measures},
           'contrasts':{'ewma20_vs_m3':bootstrap(rows,'ewma20','m3'),
                        'last5_vs_m3':bootstrap(rows,'last5','m3'),
                        'reward4_vs_ewma':bootstrap(rows,'reward_condition4','ewma20'),
                        'reward12_vs_ewma':bootstrap(rows,'reward_condition12','ewma20')},
           'per_network':rows}

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--raw-dir',type=Path)
    p.add_argument('--personal',type=Path,default=ROOT/'R059_CONNECTOR_ONLINE.tsv')
    p.add_argument('--reward',type=Path,default=ROOT/'R059_REWARD_CONDITIONAL.tsv')
    p.add_argument('--out',type=Path,default=ROOT/'R059_RESULTS.json')
    args=p.parse_args()
    out=run_main(args.raw_dir,args.personal,args.reward)
    args.out.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'source_status':out['source_status'],'weighted_logloss':out['weighted_logloss'],
      'contrasts':out['contrasts']},ensure_ascii=False,indent=2))