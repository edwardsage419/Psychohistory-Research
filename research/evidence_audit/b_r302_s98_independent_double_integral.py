#!/usr/bin/env python3
"""Nonblind independent R302 S98 audit, alternating-polynomial integral, stdlib."""
from __future__ import annotations
import argparse,csv,itertools,json,math
from fractions import Fraction as Q
from pathlib import Path

FIELDS=('world','A_success','A_failure','B_success','B_failure','posterior_mean_A','posterior_mean_B','thompson_prob_A','greedy_choice','greedy_reward','thompson_reward','uniform_reward','thompson_cost','uniform_cost')
WORLDS=set(itertools.product(range(3),repeat=4))
SUMMARY_FIELDS=('scope','worlds','mean_thompson_cost','mean_uniform_cost','positive_thompson_cost_worlds','zero_thompson_cost_worlds','max_thompson_cost','max_cost_worlds','posterior_mean_tie_worlds','R073','PESEN_v0_1','new_human_E2','new_historical_E3','external_independent_replication')

def exact_prob(a,b,c,d):
    # Double polynomial integration; does not import R Beta CDF.
    numerator=sum((Q((-1)**(j+k)*math.comb(b-1,j)*math.comb(d-1,k),(c+k)*(a+c+j+k))
                   for j in range(b) for k in range(d)),Q(0))
    beta_a=Q(math.factorial(a-1)*math.factorial(b-1),math.factorial(a+b-1))
    beta_b=Q(math.factorial(c-1)*math.factorial(d-1),math.factorial(c+d-1))
    return numerator/(beta_a*beta_b)

def check(rows,summary):
    if set(summary)!=set(SUMMARY_FIELDS):raise ValueError('summary schema')
    if summary['scope']!='E1_ARTIFICIAL_POSTERIOR_ONE_STEP_ONLY' or summary['new_human_E2']!=0 or summary['new_historical_E3']!=0 or summary['R073']!='FROZEN' or summary['PESEN_v0_1']!='FROZEN' or summary['external_independent_replication']!='NOT_RUN':raise ValueError('evidence label')
    if len(rows)!=81 or summary['worlds']!=81:raise ValueError('row count')
    seen=set();costs=[];uniforms=[];ties=0
    for row in rows:
        if set(row)!=set(FIELDS):raise ValueError('row schema')
        w=tuple(int(row[k]) for k in ('A_success','A_failure','B_success','B_failure'))
        if w not in WORLDS or w in seen:raise ValueError('coverage')
        seen.add(w)
        sa,fa,sb,fb=w;a,b,c,d=sa+1,fa+1,sb+1,fb+1
        if row['world']!=f'A={sa},{fa}|B={sb},{fb}':raise ValueError('world identity')
        ma,mb=Q(a,a+b),Q(c,c+d);p=exact_prob(a,b,c,d)
        g=max(ma,mb);ts=p*ma+(1-p)*mb;u=(ma+mb)/2
        expected={'posterior_mean_A':ma,'posterior_mean_B':mb,'thompson_prob_A':p,'greedy_reward':g,'thompson_reward':ts,'uniform_reward':u,'thompson_cost':g-ts,'uniform_cost':g-u}
        for k,v in expected.items():
            if Q(row[k])!=v:raise ValueError('arithmetic '+k)
        if row['greedy_choice']!=('A' if ma>=mb else 'B'):raise ValueError('greedy choice')
        costs.append(g-ts);uniforms.append(g-u);ties+=ma==mb
    if seen!=WORLDS:raise ValueError('coverage incomplete')
    maximum=max(costs)
    maxworlds=sorted(rows[i]['world'] for i,x in enumerate(costs) if x==maximum)
    expected={'mean_thompson_cost':str(sum(costs,Q(0))/81),'mean_uniform_cost':str(sum(uniforms,Q(0))/81),'positive_thompson_cost_worlds':sum(x>0 for x in costs),'zero_thompson_cost_worlds':sum(x==0 for x in costs),'max_thompson_cost':str(maximum),'max_cost_worlds':maxworlds,'posterior_mean_tie_worlds':ties}
    for k,v in expected.items():
        if summary[k]!=v:raise ValueError('summary '+k)
    return expected

def load(directory):
    with (directory/'R302_S98_ALL_81_POSTERIOR_ONE_STEP_WORLDS.csv').open(newline='',encoding='utf-8') as f:rows=list(csv.DictReader(f))
    summary=json.loads((directory/'R302_S98_EXACT_POSTERIOR_ONE_STEP_RESULTS.json').read_text(encoding='utf-8'))
    return rows,summary

def mutations(rows,summary):
    import copy
    rejected=[]
    def attempt(name,edit):
        a,b=copy.deepcopy(rows),copy.deepcopy(summary);edit(a,b)
        try:check(a,b)
        except (ValueError,AssertionError,ZeroDivisionError):rejected.append(name)
        else:raise AssertionError('accepted mutation '+name)
    attempt('duplicate',lambda a,b:a.__setitem__(1,a[0].copy()))
    attempt('omission',lambda a,b:a.pop())
    attempt('probability',lambda a,b:a[0].__setitem__('thompson_prob_A','1/3'))
    attempt('cost',lambda a,b:a[3].__setitem__('thompson_cost','0'))
    attempt('reward',lambda a,b:a[4].__setitem__('greedy_reward','0'))
    attempt('summary',lambda a,b:b.__setitem__('mean_thompson_cost','0'))
    attempt('evidence',lambda a,b:b.__setitem__('new_human_E2',1))
    attempt('coverage',lambda a,b:a[0].__setitem__('world','wrong'))
    return rejected

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);args=ap.parse_args()
    rows,summary=load(args.directory);out=check(rows,summary);mut=mutations(rows,summary)
    print(json.dumps({'result':'PASS','independent_method':'alternating_polynomial_double_integral','worlds':81,'mutation_rejections':mut,'summary':out},ensure_ascii=False,indent=2))
