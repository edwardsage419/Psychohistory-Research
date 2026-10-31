#!/usr/bin/env python3
"""Frozen R313 S109 finite three-step Axelrod kernel. Python stdlib only."""
from fractions import Fraction as F
from collections import defaultdict
from pathlib import Path
import json

N=64
DIRECTED=((0,1,F(1,3)),(1,0,F(1,6)),(1,2,F(1,6)),(2,1,F(1,3)))

def bits(w): return tuple((w>>(5-i))&1 for i in range(6))
def encode(b): return sum(v<<(5-i) for i,v in enumerate(b))
def edge_overlap(b,a,c): return sum(b[2*a+k]==b[2*c+k] for k in (0,1))
def active_edges(w):
 b=bits(w)
 return sum(edge_overlap(b,a,c)==1 for a,c in ((0,1),(1,2)))
def kernel(w):
 b=bits(w); out=defaultdict(F); out[w]=F(1)
 for a,c,weight in DIRECTED:
  m=edge_overlap(b,a,c)
  if m!=1: continue
  k=next(k for k in (0,1) if b[2*a+k]!=b[2*c+k]); new=list(b)
  new[2*a+k]=b[2*c+k]
  p=weight*F(1,2)
  out[w]-=p; out[encode(new)]+=p
 return {k:v for k,v in out.items() if v}

def flip(w,k):
 b=list(bits(w))
 for a in range(3): b[2*a+k]^=1
 return encode(b)
def reverse(w):
 b=bits(w);return encode(b[4:6]+b[2:4]+b[0:2])

def calculate():
 P=[kernel(w) for w in range(N)]
 paths={w:{w:F(1)} for w in range(N)}
 data=[];summary=[]
 for t in range(4):
  for w in range(N):
   p=paths[w]
   assert sum(p.values())==1 and all(x>=0 for x in p.values())
   a=sum(x for j,x in p.items() if active_edges(j)==0)
   e=sum(x*active_edges(j) for j,x in p.items())
   data.append({'initial_world':w,'step':t,'probabilities':[[j,str(p.get(j,F(0)))] for j in range(N) if p.get(j,0)],'absorbed_probability':str(a),'expected_active_edges':str(e)})
   summary.append((w,t,a,e))
  if t==3:break
  new={}
  for w in range(N):
   q=defaultdict(F)
   for j,p in paths[w].items():
    for k,v in P[j].items():q[k]+=p*v
   new[w]={k:v for k,v in q.items() if v}
  paths=new
 assert len(data)==256
 for w in range(N):
  for t in range(3):
   assert summary[64*t+w][2]<=summary[64*(t+1)+w][2]
 for t in (1,2,3):
  for f in (lambda w:flip(w,0),lambda w:flip(w,1),reverse):
   for w in range(N):
    p=dict((int(j),F(v)) for j,v in data[64*t+w]['probabilities'])
    q=dict((int(j),F(v)) for j,v in data[64*t+f(w)]['probabilities'])
    assert all(p.get(j,0)==q.get(f(j),0) for j in range(N))
 assert sum(active_edges(w)==0 for w in range(N))==16
 def changes(t,col):
  pairs=[(summary[64*t+w][col],summary[64*(t+1)+w][col]) for w in range(N)]
  return {'increase':sum(b>a for a,b in pairs),'decrease':sum(b<a for a,b in pairs),'equal':sum(b==a for a,b in pairs)}
 return {'schema':'R313_S109_exact_three_step_e1_v1','original_R313_one_step_blob':'b05bd67ee362bfcbb77726ab9262c807c93236cd','world_count':64,'step_count':4,'absorbing_worlds':16,'full_probability_cells_checked':64*64*3,'nonzero_probabilities_by_step':{str(t):sum(len(data[64*t+w]['probabilities']) for w in range(N)) for t in range(4)},'absorbed_changes':{'1_to_2':changes(1,2),'2_to_3':changes(2,2)},'active_edge_expectation_changes':{'0_to_1':changes(0,3),'1_to_2':changes(1,3),'2_to_3':changes(2,3)},'world1':[data[64*t+1] for t in range(4)],'worlds':data}

if __name__=='__main__':
 r=calculate()
 (Path(__file__).resolve().parent/'R313_S109_FULL_256_WORLD_STEP_DISTRIBUTIONS.json').write_text(json.dumps(r,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 print(json.dumps({k:v for k,v in r.items() if k not in ('worlds',)},ensure_ascii=False,indent=2))
