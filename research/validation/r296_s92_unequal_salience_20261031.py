#!/usr/bin/env python3
"""R296 S92 frozen finite exact artificial shared-error source generator."""
import csv,json,sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path
D=Path(sys.argv[1]) if len(sys.argv)>1 else Path('.')
R=(F(1,4),F(1,2),F(3,4));rows=[];worlds=[]
for a,b,n,L in product(R,R,(0,8),(1,2)):
 p=1-(1-a)**n;A=p;B=F(0);I=F(0);rs=[]
 for m in range(5):
  e=L-A-B;z=dict(alpha_A=str(a),alpha_B=str(b),pretraining=n,reward=L,stage=m,A=str(A),B=str(B),error=str(e),independent_B=str(I));rows.append(z);rs.append(z)
  q=1-a-b
  assert B==b/(a+b)*(L-p)*(1-q**m) and e==(L-p)*q**m
  A+=a*e;B+=b*e;I+=b*(L-I)
 worlds.append(dict(alpha_A=str(a),alpha_B=str(b),pretraining=n,reward=L,rate_sum=str(a+b),B4=rs[4]['B'],error1=rs[1]['error'],overshoot1=F(rs[1]['error'])<0,alternating=all(F(rs[i]['error'])*F(rs[i+1]['error'])<0 for i in (1,2,3))))
assert len(rows)==180 and len(worlds)==36 and sum(w['overshoot1'] for w in worlds)==12
if '--check' in sys.argv:
 with (D/'R296_S92_ALL_180_STATES.csv').open(newline='') as f:got=list(csv.DictReader(f))
 for z in got:
  for k in ('pretraining','reward','stage'):z[k]=int(z[k])
 assert got==rows and json.loads((D/'R296_S92_EXACT_RESULTS.json').read_text())==dict(research_id='R296',substudy='S92',evidence='E1',rows=180,worlds=worlds)
 print('CHECK_PASS 180 source states 36 worlds')
else:
 D.mkdir(parents=True,exist_ok=True)
 with (D/'R296_S92_ALL_180_STATES.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=tuple(rows[0]));w.writeheader();w.writerows(rows)
 (D/'R296_S92_EXACT_RESULTS.json').write_text(json.dumps(dict(research_id='R296',substudy='S92',evidence='E1',rows=180,worlds=worlds),indent=2)+'\n')
 print('EMIT_PASS 180 source states 36 worlds')
