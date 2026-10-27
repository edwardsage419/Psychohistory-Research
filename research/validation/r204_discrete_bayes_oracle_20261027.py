#!/usr/bin/env python3
"""R204 third method: finite discrete-source Bayes risk, Python standard library.
Usage: python r204_discrete_bayes_oracle_20261027.py [--test] [--emit PATH]
"""
import argparse,itertools,json,math
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path
K=('IID','CONSTANT','ALTERNATING','LINEAR')
S={'EXTRAPOLATION':((0,1,2),(3,4)),'INTERPOLATION':((0,2,4),(1,3)),'GAP':((0,1,4),(2,3))}
P={'IID':tuple(tuple(int(i==j) for i in range(5)) for j in range(5)),'CONSTANT':((1,1,1,1,1),),'ALTERNATING':((1,-1,1,-1,1),),'LINEAR':((-2,-1,0,1,2),)}
ORIGINAL={
'EXTRAPOLATION':{'IID':('127/72','1','1'),'CONSTANT':('499/288','1/4','1'),'ALTERNATING':('289/288','1/4','1'),'LINEAR':('587/288','5/12','5/2')},
'INTERPOLATION':{'IID':('14065/10368','1','1'),'CONSTANT':('17/32','1/4','1'),'ALTERNATING':('89/32','1/4','1'),'LINEAR':('1/9','1/9','1')},
'GAP':{'IID':('1191/800','1','1'),'CONSTANT':('17/32','1/4','1'),'ALTERNATING':('25/32','1/4','1'),'LINEAR':('1/20','1/20','1/2')}}
def inv(a):
 n=len(a);b=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(a)]
 for i in range(n):
  p=next(j for j in range(i,n) if b[j][i]);b[i],b[p]=b[p],b[i]
  d=b[i][i];b[i]=[z/d for z in b[i]]
  for j in range(n):
   if j!=i:
    d=b[j][i];b[j]=[b[j][h]-d*b[i][h] for h in range(2*n)]
 return [row[n:] for row in b]
def det3(a):
 return a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])-a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])+a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0])
def work(k,train,test):
 c=[[F(sum(v[i]*v[j] for v in P[k])+int(i==j)) for j in train] for i in train]
 a=inv(c)
 b=[[sum((F(sum(v[t]*v[i] for v in P[k]))*a[h][j] for h,t in enumerate(train)),F(0)) for j in range(3)] for i in test]
 return c,a,b
def mv(a,y):return tuple(sum((z*t for z,t in zip(row,y)),F(0)) for row in a)
def loss(x,y):return sum(((a-b)**2 for a,b in zip(x,y)),F(0))/2
def choose(pre,y):
 scores=[]
 for k in K:
  c,a,_=pre[k]
  q=sum((y[i]*sum((a[i][j]*y[j] for j in range(3)),F(0)) for i in range(3)),F(0))
  scores.append(math.log(float(det3(c)))+float(q))
 m=min(scores);return K[next(i for i,z in enumerate(scores) if z<=m+2e-12)]
def atoms(k,train,test):
 for factor in itertools.product((-1,1),repeat=len(P[k])):
  f=tuple(sum((v[i]*factor[j] for j,v in enumerate(P[k])),0) for i in range(5))
  for noise in itertools.product((-1,1),repeat=3):
   yield tuple(f[i]+noise[j] for j,i in enumerate(train)),tuple(f[i] for i in test)
def compute():
 worlds=[];total=0
 for split,(train,test) in S.items():
  pre={k:work(k,train,test) for k in K}
  for source in K:
   rows=list(atoms(source,train,test));n=len(rows);total+=n
   groups=defaultdict(list)
   for y,f in rows:groups[y].append(f)
   means={y:tuple(sum((f[j] for f in fs),F(0))/len(fs) for j in range(2)) for y,fs in groups.items()}
   risk={k:F(0) for k in ('bayes','gp_true','gp_selected','zero')}
   excess={k:F(0) for k in ('gp_true','gp_selected','zero')}
   for y,f in rows:
    pred={'bayes':means[y],'gp_true':mv(pre[source][2],y),'gp_selected':mv(pre[choose(pre,y)][2],y),'zero':(F(0),F(0))}
    for k,v in pred.items():risk[k]+=loss(v,f)/n
    for k in excess:excess[k]+=loss(pred[k],pred['bayes'])/n
   moment=sum((F(len(fs),n)*sum((sum((f[j]**2 for f in fs),F(0))/len(fs)-means[y][j]**2 for j in range(2)),F(0))/2 for y,fs in groups.items()),F(0))
   assert moment==risk['bayes']
   assert all(risk[k]-risk['bayes']==excess[k] for k in excess)
   assert all(sum((f[j]-means[y][j] for f in fs),F(0))==0 for y,fs in groups.items() for j in range(2))
   assert tuple(risk[k] for k in ('gp_selected','gp_true','zero'))==tuple(map(F,ORIGINAL[split][source]))
   worlds.append({'split':split,'true_kernel':source,'source_atoms':n,'distinct_observed_y':len(groups),'risk_exact':{k:str(v) for k,v in risk.items()},'excess_over_discrete_bayes_exact':{k:str(v) for k,v in excess.items()},'independent_conditional_moment_bayes_risk_exact':str(moment),'original_R204_GP_risk_regression':'PASS','orthogonality_identity':'PASS'})
 assert total==912 and len(worlds)==12
 summary={'total_source_atoms':total,'worlds':12,'source':'R204 frozen four discrete Rademacher kernels and three splits','evidence':'E1_ARTIFICIAL'}
 for k in ('gp_true','gp_selected','zero'):summary[k+'_strictly_worse_than_discrete_bayes']=sum(F(w['excess_over_discrete_bayes_exact'][k])>0 for w in worlds)
 return {'research_id':'R204','protocol':'protocols/R204_DISCRETE_BAYES_ORACLE_THIRD_METHOD_PRESCORE_FREEZE_2026-10-27.md','status':'INTERNAL_E1_THIRD_METHOD_NOT_FORMAL_NEW_ACCEPTANCE','summary':summary,'worlds':worlds,'evidence_limits':{'new_E2':0,'new_E3':0,'external_independent_replications':0,'R073_frozen':True,'PESEN_v0_1_frozen':True}}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--test',action='store_true');p.add_argument('--emit');a=p.parse_args();j=compute()
 if a.test:print('PASS 12 worlds, 912 atoms, exact R204 regressions and Bayes identities')
 if a.emit:Path(a.emit).write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 if not a.test and not a.emit:print(json.dumps(j['summary'],indent=2))
