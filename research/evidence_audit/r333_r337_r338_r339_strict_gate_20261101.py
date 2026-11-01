#!/usr/bin/env python3
"""Independent, fail-closed finite E1 receipt gate for frozen R333/R337/R338/R339.

Usage: python r333_r337_r338_r339_strict_gate_20261101.py R333 /path/to/R333
No audited implementation is imported. All checks remain active with python -O.
"""
import argparse
import csv
import hashlib
import io
import itertools
import json
from pathlib import Path

PINNED = {
 'R333': {
  'r333_triadic_feedback.py':'c28c82a6a18ababe8da14b0f48c846d940bf32b3',
  'R333_ALL_160_ARTIFICIAL_TRIADIC_STATES.csv':'8a202f773badb8833992ff0df25c3c90f60b3680',
  'R333_EXACT_32_TRIADIC_WORLDS.json':'dd82e1f616528742622ebafc844ec66adadf18b5'},
 'R337': {
  'r337_elm.py':'96e9e2be1b7d7ac0ac7b3cfcf05c7c81e938090d',
  'R337_ALL_64_ARTIFICIAL_ARGUMENT_CUE_ATOMS.csv':'e711da9e296693037e5a87def3604b3fe53025e8',
  'R337_EXACT_32_CONDITIONS.json':'5061ce0d74a9703e9a11ef2180395066a99aca1f'},
 'R338': {
  'r338_relative_deprivation.py':'1ee4cff348278f208628358b626174fd5fcb5524',
  'R338_ALL_128_ARTIFICIAL_COMPARISON_ATOMS.csv':'c434463b5a3c1e4dc4da068dfd6e720466e68ce3',
  'R338_EXACT_64_CONDITIONS.json':'7f428ceaa0ff89ac359437e4e99768ebe06e4776'},
 'R339': {
  'r339_social_comparison.py':'ed769df49658f345e78859f2be733b5b43322791',
  'R339_ALL_100_ARTIFICIAL_TARGET_ATOMS.csv':'fe06c06c7f158ab174251f1a14d184a4317b3371',
  'R339_EXACT_50_CONDITIONS.json':'817389e331f07dda90ae291daef9b20df1f65363'},
}

def git_blob(data):
 return hashlib.sha1(b'blob '+str(len(data)).encode('ascii')+b'\0'+data).hexdigest()

def no_duplicate_json(data):
 def unique(pairs):
  out={}
  for key,value in pairs:
   if key in out: raise ValueError('duplicate JSON key '+key)
   out[key]=value
  return out
 return json.loads(data,object_pairs_hook=unique)

def exact_csv(raw, expected):
 text=raw.decode('utf-8')
 rows=list(csv.reader(io.StringIO(text,newline='')))
 if rows!=expected: raise ValueError('CSV semantic rows or order mismatch')

def check_r333(raw_csv,raw_json):
 rows=[['mechanism','initial_p','initial_b','initial_e','do_b1','time','p','b','e']]
 worlds=[]; seq={}
 for model,p,b,e,d in itertools.product(('cyclic','feedforward'),(0,1),(0,1),(0,1),(0,1)):
  history=[(p,b,e)]
  for t in range(1,5):
   lastp,lastb,laste=history[-1]
   history.append((lastp^laste, d if t==1 else lastp^lastb, (lastb^laste) if model=='cyclic' else laste))
  seq[model,p,b,e,d]=history
  for t,(pp,bb,ee) in enumerate(history):
   rows.append(list(map(str,[model,p,b,e,d,t,pp,bb,ee])))
  pp,bb,ee=history[-1]
  worlds.append(dict(mechanism=model,initial_p=p,initial_b=b,initial_e=e,do_b1=d,final_p=pp,final_b=bb,final_e=ee))
 checks=dict(equal_b1=0,different_p2=0,different_b3=0,cyclic_e2_do=0,feedforward_e2_do=0)
 for p,b,e in itertools.product((0,1),repeat=3):
  c0,c1=(seq['cyclic',p,b,e,d] for d in (0,1))
  f0,f1=(seq['feedforward',p,b,e,d] for d in (0,1))
  checks['cyclic_e2_do']+=c0[2][2]!=c1[2][2]
  checks['feedforward_e2_do']+=f0[2][2]!=f1[2][2]
  for c,f in ((c0,f0),(c1,f1)):
   checks['equal_b1']+=c[1][1]==f[1][1]
   checks['different_p2']+=c[2][0]!=f[2][0]
   checks['different_b3']+=c[3][1]!=f[3][1]
 if checks!=dict(equal_b1=16,different_p2=8,different_b3=8,cyclic_e2_do=8,feedforward_e2_do=0): raise ValueError('R333 falsifier failure')
 exact_csv(raw_csv,rows)
 if no_duplicate_json(raw_json)!=dict(schema='R333_frozen_triads_v1',worlds=worlds,checks=checks): raise ValueError('R333 JSON semantics')

def check_r337(raw_csv,raw_json):
 rows=[['involvement','ability','argument_quality','source_cue','cue_visible','policy','central_gate','score']]
 worlds=[]
 checks=dict(worlds=32,rows=64,central_worlds=8,other_worlds=24,low_no_cue_zero=12,quality_pairs_central=4,quality_pairs_low=12,cue_pairs_central=2,cue_pairs_low=6,agreement=2,disagreement=30)
 for i,b,q,e,c in itertools.product((0,1),(0,1),(-1,1),(-1,1),(0,1)):
  central=int(i==1 and b==1)
  gated=(2*q) if central else (e if c else 0)
  additive=q+c*e
  worlds.append(dict(involvement=i,ability=b,argument_quality=q,source_cue=e,cue_visible=c,central_gate=central,route_score=gated,fixed_score=additive))
  for policy,score in (('ROUTE_GATE',gated),('FIXED_ADDITIVE',additive)):
   rows.append(list(map(str,[i,b,q,e,c,policy,central,score])))
 exact_csv(raw_csv,rows)
 if no_duplicate_json(raw_json)!=dict(schema='R337_frozen_binary_route_gate_v1',conditions=worlds,checks=checks): raise ValueError('R337 JSON semantics')

def check_r338(raw_csv,raw_json):
 rows=[['own','reference','desire','entitlement','feasibility','external_attribution','policy','gap','grievance']]
 worlds=[]
 checks=dict(worlds=64,rows=128,gap_worlds=16,zero_gap_worlds=48,conjunctive_positive=1,gap_only_positive=16,agreement=49,disagreement=15,single_missing_gate_negative=4,zero_gap_both_zero=48)
 for x,r,d,e,f,a in itertools.product((0,1),repeat=6):
  gap=int(r>x)
  conj=int(gap==1 and d==1 and e==1 and f==1 and a==1)
  worlds.append(dict(own=x,reference=r,desire=d,entitlement=e,feasibility=f,external_attribution=a,gap=gap,conjunctive_grievance=conj,gap_only_grievance=gap))
  for policy,grievance in (('CONJUNCTIVE',conj),('GAP_ONLY',gap)):
   rows.append(list(map(str,[x,r,d,e,f,a,policy,gap,grievance])))
 exact_csv(raw_csv,rows)
 if no_duplicate_json(raw_json)!=dict(schema='R338_frozen_reference_comparison_four_gate_v1',conditions=worlds,checks=checks): raise ValueError('R338 JSON semantics')

def check_r339(raw_csv,raw_json):
 rows=[['objective_available','candidate_a','candidate_b','policy','target','estimate','absolute_error']]
 worlds=[]
 checks=dict(worlds=50,rows=100,objective_worlds=25,no_objective_worlds=25,objective_both_none=25,agreement=40,disagreement=10,similar_A=17,similar_B=8,high_A=15,high_B=10,similar_better=8,similar_equal=17,similar_worse=0)
 for objective,a,b in itertools.product((0,1),range(5),range(5)):
  near='NONE' if objective else ('A' if abs(a-2)<=abs(b-2) else 'B')
  high='NONE' if objective else ('A' if a>=b else 'B')
  ne=2 if objective else (a if near=='A' else b)
  he=2 if objective else (a if high=='A' else b)
  worlds.append(dict(objective_available=objective,candidate_a=a,candidate_b=b,similar_target=near,similar_estimate=ne,similar_error=abs(ne-2),high_target=high,high_estimate=he,high_error=abs(he-2)))
  rows.append([str(objective),str(a),str(b),'SIMILARITY',near,str(ne),str(abs(ne-2))])
  rows.append([str(objective),str(a),str(b),'HIGH_SCORE',high,str(he),str(abs(he-2))])
 exact_csv(raw_csv,rows)
 if no_duplicate_json(raw_json)!=dict(schema='R339_frozen_two_target_similarity_v1',conditions=worlds,checks=checks): raise ValueError('R339 JSON semantics')

CHECKS={'R333':check_r333,'R337':check_r337,'R338':check_r338,'R339':check_r339}

def verify(model, directory):
 pinned=PINNED[model]
 contents={}
 for name,expected in pinned.items():
  raw=(directory/name).read_bytes()
  if git_blob(raw)!=expected: raise ValueError('identity mismatch '+name)
  contents[name]=raw
 names=list(pinned)
 CHECKS[model](contents[names[1]],contents[names[2]])
 return True

def main():
 parser=argparse.ArgumentParser()
 parser.add_argument('model',choices=sorted(PINNED))
 parser.add_argument('directory',type=Path)
 args=parser.parse_args()
 try: verify(args.model,args.directory)
 except (OSError,ValueError,KeyError,TypeError,UnicodeError) as err:
  parser.exit(1,f'STRICT_GATE_FAIL: {type(err).__name__}: {err}\n')
 print('STRICT_GATE_PASS '+args.model)

if __name__=='__main__':main()
