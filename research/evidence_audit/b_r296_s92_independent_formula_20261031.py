#!/usr/bin/env python3
"""Independent nonblind exact rational source auditor for R296 S92."""
import csv,json,sys
from pathlib import Path
from fractions import Fraction as F
from itertools import product
D=Path(sys.argv[1]) if len(sys.argv)>1 else Path('.')
with (D/'R296_S92_ALL_180_STATES.csv').open(newline='') as f: rows=list(csv.DictReader(f))
worlds=json.loads((D/'R296_S92_EXACT_RESULTS.json').read_text())['worlds']
R=(F(1,4),F(1,2),F(3,4))
def audit(rs,ws):
 keys=set()
 for r in rs:
  a,b,n,L,m=F(r['alpha_A']),F(r['alpha_B']),int(r['pretraining']),int(r['reward']),int(r['stage']);key=(a,b,n,L,m)
  if key in keys:raise ValueError('duplicate')
  keys.add(key);p=1-(1-a)**n;q=1-a-b
  if (F(r['A']),F(r['B']),F(r['error']),F(r['independent_B']))!=(p+a/(a+b)*(L-p)*(1-q**m),b/(a+b)*(L-p)*(1-q**m),(L-p)*q**m,L*(1-(1-b)**m)):raise ValueError('formula')
 if keys!={(a,b,n,L,m) for a,b,n,L,m in product(R,R,(0,8),(1,2),range(5))}:raise ValueError('missing')
 if len(ws)!=36:raise ValueError('world count')
 world_keys=set()
 for w in ws:
  a,b,n,L=F(w['alpha_A']),F(w['alpha_B']),int(w['pretraining']),int(w['reward']);key=(a,b,n,L)
  if key in world_keys:raise ValueError('duplicate world')
  world_keys.add(key);p=1-(1-a)**n;q=1-a-b
  if (F(w['B4']),F(w['error1']),w['overshoot1'],w['alternating'])!=((L-p)*b/(a+b)*(1-q**4),(L-p)*q,q<0,q<0):raise ValueError('world formula')
 if world_keys!={(a,b,n,L) for a,b,n,L in product(R,R,(0,8),(1,2))}:raise ValueError('missing world')
 return True
audit(rows,worlds)
for kind in ('duplicate','missing','A','B','error','independent_B','summary','flag'):
 r=[dict(x) for x in rows];w=[dict(x) for x in worlds]
 if kind=='duplicate':r[-1]=dict(r[0])
 elif kind=='missing':r.pop()
 elif kind in ('A','B','error','independent_B'):r[0][kind]='123/17'
 elif kind=='summary':w[0]['B4']='123/17'
 else:w[0]['overshoot1']=not w[0]['overshoot1']
 try:audit(r,w)
 except ValueError:continue
 raise AssertionError('mutation accepted '+kind)
print('INDEPENDENT_PASS 180 rows 36 worlds 8/8 mutations rejected')
