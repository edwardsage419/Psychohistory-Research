#!/usr/bin/env python3
"""Nonblind independent event-tree auditor for R313 S109; no import of R generator."""
import copy
import json
import sys
from pathlib import Path
from collections import defaultdict
from fractions import Fraction

SOURCE=str(Path(__file__).resolve().parent.parent/'validation'/'R313_S109_FULL_256_WORLD_STEP_DISTRIBUTIONS.json')

def split(w):
 return [list(map(int,f'{w:06b}'[2*i:2*i+2])) for i in range(3)]
def join(groups):
 return int(''.join(str(v) for pair in groups for v in pair),2)
def branches(w):
 groups=split(w)
 for agent in range(3):
  peers={0:(1,),1:(0,2),2:(1,)}[agent]
  for peer in peers:
   contact=Fraction(1,3*len(peers))
   differences=[j for j in range(2) if groups[agent][j]!=groups[peer][j]]
   if len(differences)!=1:
    yield w,contact
   else:
    copychance=Fraction(1,2)
    yield w,contact*(1-copychance)
    alternative=[pair[:] for pair in groups]
    alternative[agent][differences[0]]=groups[peer][differences[0]]
    yield join(alternative),contact*copychance

def active(w):
 g=split(w)
 return sum(sum(g[a][j]==g[b][j] for j in range(2))==1 for a,b in ((0,1),(1,2)))

def check(doc):
 def require(ok,message):
  if not ok: raise ValueError(message)
 require(doc.get('schema')=='R313_S109_exact_three_step_e1_v1','schema')
 require(doc.get('original_R313_one_step_blob')=='b05bd67ee362bfcbb77726ab9262c807c93236cd','source blob')
 require(doc.get('world_count')==64 and doc.get('step_count')==4 and doc.get('absorbing_worlds')==16,'metadata')
 require(doc.get('full_probability_cells_checked')==12288,'coverage')
 rows=doc.get('worlds')
 require(isinstance(rows,list) and len(rows)==256,'rows')
 expected={}
 for origin in range(64):
  dist={origin:Fraction(1)}
  for step in range(4):
   row=rows[step*64+origin]
   require(row.get('initial_world')==origin and row.get('step')==step,'row key')
   rec=row.get('probabilities')
   require(isinstance(rec,list) and len(rec)==len(dist),'support size')
   parsed={}
   for item in rec:
    require(isinstance(item,list) and len(item)==2,'cell shape')
    k,v=item
    require(type(k) is int and 0<=k<64 and k not in parsed,'duplicate or invalid target')
    require(isinstance(v,str),'probability type')
    parsed[k]=Fraction(v)
   require(parsed==dist,'full probability vector')
   require(Fraction(row['absorbed_probability'])==sum(p for k,p in dist.items() if active(k)==0),'absorbed')
   require(Fraction(row['expected_active_edges'])==sum(p*active(k) for k,p in dist.items()),'active edges')
   expected[(origin,step)]=dist
   nxt=defaultdict(Fraction)
   for state,p in dist.items():
    for dest,conditional in branches(state):nxt[dest]+=p*conditional
   dist={k:v for k,v in nxt.items() if v}
 require(doc['nonzero_probabilities_by_step']=={str(t):sum(len(expected[(w,t)]) for w in range(64)) for t in range(4)},'support summary')
 for field,idx in [('absorbed_changes','absorbed_probability'),('active_edge_expectation_changes','expected_active_edges')]:
  for key,steps in ([('1_to_2',(1,2)),('2_to_3',(2,3))] if field=='absorbed_changes' else [('0_to_1',(0,1)),('1_to_2',(1,2)),('2_to_3',(2,3))]):
   counts={'increase':0,'decrease':0,'equal':0}
   for w in range(64):
    a=Fraction(rows[steps[0]*64+w][idx]);b=Fraction(rows[steps[1]*64+w][idx])
    counts['increase' if b>a else 'decrease' if b<a else 'equal']+=1
   require(doc[field][key]==counts,'change counts')
 require(doc.get('world1')==[rows[t*64+1] for t in range(4)],'world1')
 return {'verified_world_step_rows':256,'verified_full_probability_cells':64*64*4,'verified_nonzero_cells':sum(len(x) for x in expected.values())}

def mutations(doc):
 tests=[]
 def test(name,edit):
  obj=copy.deepcopy(doc);edit(obj)
  if obj==doc:raise RuntimeError('no-op mutation '+name)
  try:check(obj)
  except (ValueError,KeyError,TypeError,ZeroDivisionError):tests.append(name);return
  raise RuntimeError('ACCEPTED MUTATION '+name)
 test('missing_row',lambda x:x['worlds'].pop())
 test('duplicate_world_step',lambda x:x['worlds'][1].update(initial_world=0))
 test('probability_tamper',lambda x:x['worlds'][64+1]['probabilities'][0].__setitem__(1,'1/2'))
 test('support_target_tamper',lambda x:x['worlds'][64+1]['probabilities'][0].__setitem__(0,63))
 test('absorbed_probability_tamper',lambda x:x['worlds'][64+1].update(absorbed_probability='1'))
 test('expected_active_edges_tamper',lambda x:x['worlds'][64+1].update(expected_active_edges='0'))
 test('support_summary_tamper',lambda x:x['nonzero_probabilities_by_step'].update({'3':999}))
 test('source_identity_tamper',lambda x:x.update(original_R313_one_step_blob='fake'))
 test('world1_summary_tamper',lambda x:x['world1'][1].update(step=2))
 return tests

if __name__=='__main__':
 with open(sys.argv[1] if len(sys.argv)>1 else SOURCE,encoding='utf-8') as f:doc=json.load(f)
 result=check(doc);result['mutations_rejected']=mutations(doc)
 print(json.dumps(result,ensure_ascii=False,indent=2))
