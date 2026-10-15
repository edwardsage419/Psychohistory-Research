#!/usr/bin/env python3
"""R060: network-group online context vs private online history, no future leakage.

26 network-level original CSVs are required for full source-replay with SHA1
Git blob authentication. Derived-only mode recomputes aggregation and intervals
from connector-computed per-run results; it is NOT a raw-byte replay.

Candidate algorithms were fixed before the source-backed R060 calculations:
 P0 individual EWMA(0.2) starting at 0.5, updated by individual's completed trials;
 P1 0.75*P0 + 0.25*network EWMA(0.2) of previously completed round self-repeat;
 P2 0.75*P0 + 0.25*network conditioned EWMA(0.2) by prior coordination
    reward, with each reward-state updated only on completed prior rounds.

All three predict exactly the same predeclared eligible sample: t >=3 with
Response, prev_response and partner_prev_response observed. Individual and
network histories can use t>=2 self-repeat when defined. Conditioned prior
history is updated only for eligible rows with observed previous reward.
Network EWMA update occurs only after processing all participant decisions
for one round. No present-round peer answers, Points or DecisionType enter.
"""
from __future__ import annotations
import argparse,csv,io,json,math,random
from collections import defaultdict
from pathlib import Path
from r058_replay import read_counts,git_sha,recount_raw_bytes
from r059_online import online_rows

ROOT=Path(__file__).resolve().parent
MISSING={'','nan','NaN','NA','None','null'}
ALPHA=.2
NETWORK_WEIGHT=.25
MODES=('self_ewma','online_network','online_network_reward')


def safe_response(row,k):
    v=row.get(k)
    return v is not None and v not in MISSING


def loss(y,p):
    if y not in (0,1) or not(0<p<1) or not math.isfinite(p):
        raise ValueError('invalid binary target/probability')
    return -math.log(p) if y else -math.log1p(-p)


def score_raw_rows(rows,details=False):
    req={'id','TrialNumber','Response','prev_response','partner_prev_response',
         'partner_response','Points'}
    if not rows or any(not req.issubset(x) for x in rows):
        raise ValueError('missing required raw fields')
    by_round=defaultdict(list); seen=set()
    for row in rows:
        t=int(row['TrialNumber']);k=(row['id'],t)
        if not 1<=t<=40:raise ValueError('trial outside 1..40')
        if k in seen:raise ValueError('duplicate participant-round')
        seen.add(k);by_round[t].append(row)
    personal=defaultdict(lambda:.5)
    group=.5;group_cond={0:.5,1:.5}
    totals={m:0. for m in MODES}; brier={m:0. for m in MODES}
    per_time=[];observations=[];n=0
    for t in range(1,41):
        updates=[];by_reward={0:[],1:[]}
        for z in by_round.get(t,[]):
            valid=t>=2 and safe_response(z,'Response') and safe_response(z,'prev_response')
            test=t>=3 and valid and safe_response(z,'partner_prev_response')
            if test:
                y=int(z['Response']==z['prev_response'])
                rew=int(z['prev_response']==z['partner_prev_response'])
                base=personal[z['id']]
                pp={'self_ewma':base,
                    'online_network':(1-NETWORK_WEIGHT)*base+NETWORK_WEIGHT*group,
                    'online_network_reward':(1-NETWORK_WEIGHT)*base+NETWORK_WEIGHT*group_cond[rew]}
                n+=1
                for key,p in pp.items():
                    totals[key]+=loss(y,p); brier[key]+=(y-p)**2
                by_reward[rew].append(y)
                if details:observations.append({'id':z['id'],'t':t,'y':y,'previous_reward':rew,**pp})
            if valid:
                updates.append((z['id'],int(z['Response']==z['prev_response'])))
        # Commit only after ALL predictions for this round have been scored.
        if updates:
            for uid,y in updates: personal[uid]=(1-ALPHA)*personal[uid]+ALPHA*y
            group=(1-ALPHA)*group+ALPHA*sum(y for _,y in updates)/len(updates)
        for reward in (0,1):
            a=by_reward[reward]
            if a:group_cond[reward]=(1-ALPHA)*group_cond[reward]+ALPHA*sum(a)/len(a)
        if details:per_time.append({'t':t,'n_current':len(by_round.get(t,[])),
                                    'group_updated':bool(updates),
                                    'group_mean_post':group})
    if n<=0:raise ValueError('no eligible observations')
    out={'n':n,'rows':len(rows),'logloss':{k:totals[k]/n for k in MODES},
         'brier':{k:brier[k]/n for k in MODES}}
    if details:out.update({'predictions':observations,'per_time':per_time})
    return out


def read_connector_scores(path=ROOT/'R060_CONNECTOR_SCORES.tsv'):
    lines=[line for line in Path(path).read_text(encoding='utf-8').splitlines() if line and not line.startswith('#')]
    if not lines:raise ValueError('empty results')
    out=list(csv.DictReader(lines,delimiter='|'))
    if any(set(['run','sha','rows','n',*MODES]) - set(z) for z in out):
        raise ValueError('missing results fields')
    if len(set(r['run'] for r in out))!=len(out):raise ValueError('duplicate network')
    for r in out:
        r['n']=int(r['n']);r['rows']=int(r['rows'])
        for m in MODES:r[m]=float(r[m])
        if r['n']<1 or any(not math.isfinite(r[k]) or r[k]<0 for k in MODES):
            raise ValueError('invalid numeric outcome')
    return out


def verify_registry(runs,derived,old):
    metadata={r['name']:r for r in runs}
    if len(metadata)!=26 or set(metadata)!=set(r['run'] for r in derived):
        raise ValueError('network registry mismatch')
    old_by={r['run']:r for r in old['per_network']}
    if set(old_by)!=set(metadata):raise ValueError('old online network mismatch')
    for row in derived:
        m=metadata[row['run']]
        if row['sha']!=m['sha'] or row['rows']!=m['raw_rows']:
            raise ValueError('source metadata mismatch '+row['run'])
        if row['n']!=old_by[row['run']]['n'] or row['n']!=sum(v[0] for v in m['cells'].values()):
            raise ValueError('eligible count mismatch '+row['run'])
        if abs(row['self_ewma']-old_by[row['run']]['ewma20'])>1e-10:
            raise ValueError('baseline mismatch '+row['run'])
    if sum(r['n'] for r in derived)!=36780 or sum(r['rows'] for r in derived)!=39619:
        raise ValueError('unexpected analysis population')


def verify_raw_network(raw_dir,derived,metadata):
    expected={r['run']:r for r in derived}
    for info in metadata:
        name=info['name'];path=Path(raw_dir)/f'{name}.csv'
        raw=path.read_bytes()
        if git_sha(raw)!=info['sha']:raise ValueError('GIT_BLOB_SHA_MISMATCH '+name)
        check=recount_raw_bytes(raw)
        if (check['rows'],check['ids'],check['cells'])!=(info['raw_rows'],info['ids'],info['cells']):
            raise ValueError('R058_RAW_RECOUNT_MISMATCH '+name)
        if check['checks']['self_mismatch'] or check['checks']['partner_mismatch']:
            raise ValueError('TIME_HISTORY_MISMATCH '+name)
        data=list(csv.DictReader(io.StringIO(raw.decode('utf-8-sig'),newline='')))
        output=score_raw_rows(data)
        if output['n']!=expected[name]['n']:raise ValueError('R060_ELIGIBLE_MISMATCH '+name)
        for k in MODES:
            if abs(output['logloss'][k]-expected[name][k])>1e-10:
                raise ValueError('R060_RAW_SCORE_MISMATCH '+name+' '+k)
        if abs(online_rows(data)['metrics']['ewma20']-output['logloss']['self_ewma'])>1e-10:
            raise ValueError('R059_BASELINE_REPLAY_MISMATCH '+name)
    return True


def summary(rows):
    n=sum(r['n'] for r in rows)
    out={'networks':len(rows),'eligible':n,
         'weighted_logloss':{m:sum(r['n']*r[m] for r in rows)/n for m in MODES},
         'networks_better_than_self':{m:sum(r[m]<r['self_ewma'] for r in rows) for m in MODES[1:]}}
    rng=random.Random(6001);draws=20000
    contrasts={}
    for mode in MODES[1:]:
        diffs=[]
        for _ in range(draws):
            a=rng.choices(rows,k=len(rows));N=sum(r['n'] for r in a)
            diffs.append(sum(r['n']*(r[mode]-r['self_ewma']) for r in a)/N)
        diffs.sort();contrasts[mode]={'delta_logloss':out['weighted_logloss'][mode]-out['weighted_logloss']['self_ewma'],
             'network_bootstrap95':[diffs[500],diffs[19500]],'draws':draws,'seed':6001}
    out['exploratory_contrasts']=contrasts
    return out


def main():
    pa=argparse.ArgumentParser();pa.add_argument('--raw-dir',type=Path)
    pa.add_argument('--source',type=Path,default=ROOT/'R060_CONNECTOR_SCORES.tsv');pa.add_argument('--out',type=Path)
    a=pa.parse_args();rows=read_connector_scores(a.source)
    registry=read_counts(ROOT/'R058_CONNECTOR_COUNTS.tsv')
    old=json.loads((ROOT/'R059_RESULTS.json').read_text())
    verify_registry(registry,rows,old)
    if a.raw_dir:verify_raw_network(a.raw_dir,rows,registry)
    result={'source_tier':'LOCAL_ORIGINAL_VERIFIED' if a.raw_dir else 'CONNECTOR_DERIVED_ONLY',
            'methods':{'target':'repeat own preceding response','sample':'t>=3, full history observed',
                'alpha':ALPHA,'network_weight':NETWORK_WEIGHT,
                'cross_network_training':False,'online_network_context':'earlier complete rounds only'},
            **summary(rows)}
    if a.out:a.out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()