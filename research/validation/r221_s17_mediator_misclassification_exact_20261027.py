#!/usr/bin/env python3
"""R221 S17 exact mediator misclassification, standard library only."""
import csv,json
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'research/R221/R221_ALL_48_ORIGINAL_MEDIATION_SCM_SOURCES.csv'
OUT=ROOT/'research/validation/R221_S17_MEDIATOR_MISCLASSIFICATION_30_CONDITION_EXACT_RECEIPT_2026-10-27.json'
RATES=[F(0),F(1,8),F(1,4),F(3,8),F(1,2)]
def compute():
 with SOURCE.open(newline='',encoding='utf8') as f: rows=list(csv.DictReader(f))
 assert len(rows)==48 and all(F(r['true_original_source_probability'])==F(1,8) for r in rows)
 conditions=[];positive=0
 for world in sorted(set(r['true_world'] for r in rows)):
  rs=[r for r in rows if r['true_world']==world];assert len(rs)==8
  oracle=defaultdict(F)
  for r in rs:
   p=F(r['true_original_source_probability'])
   oracle['te']+=p*(F(r['nested_Y_1_M1_ORACLE_ONLY'])-F(r['nested_Y_0_M0_ORACLE_ONLY']))
   oracle['nde']+=p*(F(r['nested_Y_1_M0_ORACLE_ONLY'])-F(r['nested_Y_0_M0_ORACLE_ONLY']))
   oracle['nie']+=p*(F(r['nested_Y_1_M1_ORACLE_ONLY'])-F(r['nested_Y_1_M0_ORACLE_ONLY']))
  assert oracle['nde']+oracle['nie']==oracle['te']
  for e in RATES:
   mass=defaultdict(F);ymass=defaultdict(F);total=F(0)
   for r in rs:
    t=int(r['realized_random_T']);m=int(r['realized_observable_M'])
    y=F(r['realized_observable_Y']);p=F(r['true_original_source_probability'])
    for w in (0,1):
     q=1-e if w==m else e
     total+=p*q
     if p*q>0:positive+=1
     mass[t,w]+=p*q;ymass[t,w]+=p*q*y
   assert total==1 and all(mass[t,w]>0 for t in (0,1) for w in (0,1))
   pw={(t,w):2*mass[t,w] for t in (0,1) for w in (0,1)}
   ey={(t,w):ymass[t,w]/mass[t,w] for t in (0,1) for w in (0,1)}
   nde=sum((pw[0,w]*(ey[1,w]-ey[0,w]) for w in (0,1)),F(0))
   nie=sum((ey[1,w]*(pw[1,w]-pw[0,w]) for w in (0,1)),F(0))
   assert nde+nie==oracle['te']
   conditions.append(dict(world=world,flip_rate=str(e),naive_NDE=str(nde),naive_NIE=str(nie),total_effect=str(oracle['te']),oracle_NDE=str(oracle['nde']),oracle_NIE=str(oracle['nie']),NDE_bias=str(nde-oracle['nde']),NIE_bias=str(nie-oracle['nie']),W1_T0=str(pw[0,1]),W1_T1=str(pw[1,1])))
 assert len(conditions)==30 and positive==432
 for rate in RATES:
  a,b=[next(x for x in conditions if x['world']==w and x['flip_rate']==str(rate)) for w in ('PURE_INDIRECT','LATENT_COMMON_CAUSE_NO_MEDIATION')]
  assert (a['naive_NDE'],a['naive_NIE'],a['total_effect'])==(b['naive_NDE'],b['naive_NIE'],b['total_effect'])
  assert a['oracle_NIE']!=b['oracle_NIE']
 assert all(F(c['naive_NIE'])==0 for c in conditions if c['flip_rate']=='1/2')
 return dict(research_id='R221',supplement='S17',evidence='E1_ARTIFICIAL_ONLY',frozen_original_source_rows=48,source_slots=480,positive_source_slots=432,worlds=6,misclassification_rates=[str(e) for e in RATES],conditions=conditions,real_human_E2=0,real_historical_E3=0,external_replication=0)
if __name__=='__main__':
 result=compute()
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf8')
 print('R221 S17',len(result['conditions']),'conditions, 480 slots')
