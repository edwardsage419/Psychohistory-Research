#!/usr/bin/env python3
"""R309 S105 frozen two-step artificial SIR exact transition calculation. No real data."""
from fractions import Fraction as F
from collections import defaultdict
from math import comb
import csv, json, hashlib
from pathlib import Path

HERE=Path(__file__).resolve().parent
ORIGINAL_SHA='9470c1e1c880f51da5c11377b6cc8be7f799542d0cebd1f82d4fc3539cabd134'
P=(F(0),F(1,2),F(1))
STATES=tuple((s,i,5-s-i) for s in range(6) for i in range(6-s))
WORLDS=tuple((s,i,r,p,q) for s,i,r in STATES for p in P for q in P)
COLUMNS=('world','S','I','R','contact_p','old_recovery_q','one_susceptible_attack_probability',
'newly_infected_susceptibles','recovered_old_infectives','next_S','next_I','next_R',
'joint_transition_probability','expected_next_S','expected_next_I','expected_next_R',
'next_population_total','is_positive_probability')

def fmt(x):return str(x)
def binom(n,k,p):return F(comb(n,k))*p**k*(1-p)**(n-k)
def worldid(s,i,r,p,q):return f'S={s}|I={i}|R={r}|contact_p={p}|recovery_q={q}'

def original_events(w):
    s,i,r,p,q=w
    a=1-(1-p)**i
    es=F(s)-s*a;ei=F(i)+s*a-i*q;er=F(r)+i*q
    for x in range(s+1):
        for y in range(i+1):
            prob=binom(s,x,a)*binom(i,y,q)
            ns,ni,nr=s-x,i+x-y,r+y
            yield dict(zip(COLUMNS,[worldid(*w),s,i,r,p,q,a,x,y,ns,ni,nr,prob,es,ei,er,5,prob>0]))

def reproduce_original_source():
    path=HERE/'R309_S105_RECONSTRUCTED_ORIGINAL_1134.csv'
    with path.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=COLUMNS,lineterminator='\n');writer.writeheader()
        for w in WORLDS:
            for row in original_events(w):writer.writerow({k:fmt(row[k]) for k in COLUMNS})
    digest=hashlib.sha256(path.read_bytes()).hexdigest()
    if digest!=ORIGINAL_SHA:raise RuntimeError(f'ORIGINAL_SOURCE_SHA_MISMATCH {digest} != {ORIGINAL_SHA}')
    return path,digest

def kernel(w):
    out=defaultdict(F)
    for e in original_events(w):
        out[(e['next_S'],e['next_I'],e['next_R'])]+=e['joint_transition_probability']
    if sum(out.values(),F())!=1:raise RuntimeError('non-normalized original kernel')
    return out

def run():
    source,digest=reproduce_original_source()
    kernels={w:kernel(w) for w in WORLDS}
    rows=[];summary=[];npaths=0
    for w in WORLDS:
        s,i,r,p,q=w
        k1=kernels[w];k2=defaultdict(F);new2=F()
        for mid,weight in k1.items():
            if weight==0:continue
            mid_w=(*mid,p,q)
            for fin,weight2 in kernels[mid_w].items():k2[fin]+=weight*weight2
            for e in original_events(mid_w):
                npaths+=1
                if e['newly_infected_susceptibles']>0:new2+=weight*e['joint_transition_probability']
        if sum(k2.values(),F())!=1:raise RuntimeError(f'bad mass {w}')
        extinction1=sum((v for u,v in k1.items() if u[1]==0),F())
        extinction2=sum((v for u,v in k2.items() if u[1]==0),F())
        es=sum((v*u[0] for u,v in k2.items()),F())
        ei=sum((v*u[1] for u,v in k2.items()),F())
        er=sum((v*u[2] for u,v in k2.items()),F())
        if es+ei+er!=5 or extinction2<extinction1:raise RuntimeError('failed invariants')
        if i==0 and (extinction1,extinction2,ei)!=(1,1,0):raise RuntimeError('absorption failure')
        if q==0 and i>0 and extinction2!=0:raise RuntimeError('no-recovery failure')
        if p==0 and q==1 and i>0 and extinction1!=1:raise RuntimeError('certain recovery failure')
        if w==(3,2,0,F(1),F(1)) and (k2[(0,0,5)],extinction2)!=(1,1):raise RuntimeError('new-infective timing failure')
        summary.append({'world':worldid(*w),'S':s,'I':i,'R':r,'p':str(p),'q':str(q),
           'one_step_extinction':str(extinction1),'two_step_extinction':str(extinction2),
           'second_step_extinction_increment':str(extinction2-extinction1),
           'second_step_any_new_infection':str(new2),
           'expected_S2':str(es),'expected_I2':str(ei),'expected_R2':str(er)})
        for u in STATES:
            if u[0]>s and k2[u]!=0:raise RuntimeError('S monotonicity')
            if u[2]<r and k2[u]!=0:raise RuntimeError('R monotonicity')
            rows.append({'world':worldid(*w),'S':s,'I':i,'R':r,'p':str(p),'q':str(q),
                'final_S':u[0],'final_I':u[1],'final_R':u[2],'two_step_probability':str(k2[u])})
    out=HERE/'R309_S105_ALL_3969_TWO_STEP_STATES.csv'
    with out.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');writer.writeheader();writer.writerows(rows)
    report={'study':'R309_S105','evidence':'E1_ARTIFICIAL_INTERNAL_NONBLIND','source_original_sha256':digest,
        'original_worlds':len(WORLDS),'original_one_step_events':1134,'two_step_state_cells':len(rows),
        'two_step_positive_cells':sum(F(r['two_step_probability'])>0 for r in rows),
        'nonzero_first_step_paths_second_event_evaluations':npaths,
        'original_example_one_step_extinction':'1/256',
        'worlds':summary,
        'frozen_R073':'FROZEN','frozen_PESEN_v0_1':'FROZEN','new_E2':0,'new_E3':0,
        'scientific_status':'PARTIAL_E1_ARTIFICIAL_TWO_STEP'}
    result=HERE/'R309_S105_TWO_STEP_SUMMARY.json';result.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'source_sha':digest,'csv_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),
       'summary_sha256':hashlib.sha256(result.read_bytes()).hexdigest(),
       'rows':len(rows),'positive_cells':report['two_step_positive_cells'],
       'sample_half':next(x for x in summary if x['world']==worldid(3,2,0,F(1,2),F(1,2))),
       'sample_certain':next(x for x in summary if x['world']==worldid(3,2,0,F(1),F(1))),
       'worlds_extinction_increases':sum(F(x['second_step_extinction_increment'])>0 for x in summary),
       'max_increment':str(max(F(x['second_step_extinction_increment']) for x in summary))},indent=2))
if __name__=='__main__':run()
