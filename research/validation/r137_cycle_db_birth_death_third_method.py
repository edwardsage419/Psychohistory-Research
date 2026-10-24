#!/usr/bin/env python3
"""R137 independent contiguous-cluster birth/death chain weak-selection audit.

All arithmetic is exact. No R137 2^N state solver or derivative matrix is imported.
"""
import json
import hashlib
from fractions import Fraction as F
from pathlib import Path

EXPECTED = {5:F(6),6:F(4),7:F(10,3),8:F(3),9:F(14,5)}


def one_state(N,m,b,c=F(1)):
    state = [1 if i<m else 0 for i in range(N)]
    pay=[]
    for i in range(N):
        nc=state[(i-1)%N]+state[(i+1)%N]
        pay.append(b*nc-2*c*state[i])
    tp0=tm0=tp1=tm1=F(0)
    for dead in range(N):
        left,right=(dead-1)%N,(dead+1)%N
        neighbors=(left,right)
        cs=[i for i in neighbors if state[i]==1]
        ds=[i for i in neighbors if state[i]==0]
        if state[dead]==0:
            if len(cs)==2:
                tp0+=F(1,N)
            elif len(cs)==1:
                tp0+=F(1,2*N)
                tp1+=(pay[cs[0]]-pay[ds[0]])/F(4*N)
        else:
            if len(ds)==2:
                tm0+=F(1,N)
            elif len(ds)==1:
                tm0+=F(1,2*N)
                tm1+=(pay[ds[0]]-pay[cs[0]])/F(4*N)
    assert tp0==tm0==F(1,N),(N,m,tp0,tm0)
    return {'m':m,'plus0':tp0,'minus0':tm0,'plus_derivative':tp1,'minus_derivative':tm1,
            'ratio_derivative':N*(tm1-tp1)}


def gradient(N,b,c=F(1),swap_gradient=False):
    states=[one_state(N,m,b,c) for m in range(1,N)]
    rprime=[(-s['ratio_derivative'] if swap_gradient else s['ratio_derivative']) for s in states]
    derivative=-sum((N-m)*rprime[m-1] for m in range(1,N))/F(N*N)
    return derivative,states


def main():
    rows=[]
    for N,expected in EXPECTED.items():
        y0,s0=gradient(N,F(0))
        y1,s1=gradient(N,F(1))
        A=y1-y0
        assert A>0 and y0<0
        threshold=-y0/A
        assert threshold==expected,(N,threshold,expected)
        below,sbelow=gradient(N,threshold-1)
        above,sabove=gradient(N,threshold+1)
        assert below<0<above
        zero_cost,_=gradient(N,F(0),F(0))
        reversed_sign,_=gradient(N,F(0),swap_gradient=True)
        assert zero_cost==0 and y0<0
        assert reversed_sign==-y0 and reversed_sign>0
        rows.append({'graph':f'C{N}','N':N,'neutral_birth_death_each':str(F(1,N)),
                     'gradient_b0':str(y0),'gradient_b1':str(y1),'slope_b':str(A),
                     'threshold':str(threshold),'gradient_below':str(below),'gradient_above':str(above),
                     'zero_cost_b0_gradient':str(zero_cost),'reversed_event_b0_gradient':str(reversed_sign),
                     'state_gradients_b0':[{k:str(v) for k,v in s.items()} for s in s0],
                     'state_gradients_b1':[{k:str(v) for k,v in s.items()} for s in s1]})
    result={'method':'contiguous_cluster_birth_death_exact_first_derivative',
            'source':'R137 archived finite C5-C9 DB thresholds',
            'graphs':len(rows),'b_conditions_per_graph':4,
            'gradient_checks':20,'neutral_state_checks':sum(N-1 for N in EXPECTED),
            'zero_cost_negative_controls':5,'reversed_event_negative_controls':5,
            'results':rows,'status':'PASS_BOUNDED_LOCAL_E1_THIRD_METHOD',
            'E2':0,'E3':0,'external_replication':0,'new_ci':'NOT_RUN'}
    out=Path('/mnt/data/R137_CYCLE_DB_THIRD_METHOD_EXACT_RESULTS_2026-10-25.json')
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    print(json.dumps({'status':result['status'],'thresholds':{r['graph']:r['threshold'] for r in rows},
                      'gradients_b0':{r['graph']:r['gradient_b0'] for r in rows},
                      'file_sha256':hashlib.sha256(out.read_bytes()).hexdigest()},indent=2))

if __name__=='__main__':
    main()
