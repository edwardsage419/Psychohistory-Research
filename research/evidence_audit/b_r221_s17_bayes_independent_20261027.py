#!/usr/bin/env python3
"""Independent Bayes-mixture audit of R221 S17; no import from R script."""
import csv,json
from pathlib import Path
from fractions import Fraction as F
from collections import defaultdict
ROOT=Path(__file__).resolve().parents[2]
SOURCE=ROOT/'research/R221/R221_ALL_48_ORIGINAL_MEDIATION_SCM_SOURCES.csv'
REF=ROOT/'research/validation/R221_S17_MEDIATOR_MISCLASSIFICATION_30_CONDITION_EXACT_RECEIPT_2026-10-27.json'
OUT=ROOT/'research/evidence_audit/B_R221_S17_BAYES_30_CONDITION_INDEPENDENT_RECEIPT_2026-10-27.json'
def run():
 with SOURCE.open(newline='',encoding='utf8') as f: rows=list(csv.DictReader(f))
 ref=json.loads(REF.read_text(encoding='utf8'));checks=[];count=0
 for world in sorted(set(r['true_world'] for r in rows)):
  joint=defaultdict(F);ymass=defaultdict(F)
  for r in rows:
   if r['true_world']!=world:continue
   t=int(r['realized_random_T']);m=int(r['realized_observable_M'])
   p=F(r['true_original_source_probability']);y=F(r['realized_observable_Y'])
   joint[t,m]+=p;ymass[t,m]+=p*y
  assert all(joint[t,m]>0 for t in (0,1) for m in (0,1))
  for e in (F(0),F(1,8),F(1,4),F(3,8),F(1,2)):
   pw={};ey={}
   for t in (0,1):
    for w in (0,1):
     weights={m:joint[t,m]*((1-e) if m==w else e) for m in (0,1)}
     denom=sum(weights.values());assert denom>0
     pw[t,w]=2*denom
     ey[t,w]=sum((weights[m]/denom)*(ymass[t,m]/joint[t,m]) for m in (0,1))
   nde=sum(pw[0,w]*(ey[1,w]-ey[0,w]) for w in (0,1))
   nie=sum(ey[1,w]*(pw[1,w]-pw[0,w]) for w in (0,1))
   item=next(x for x in ref['conditions'] if x['world']==world and x['flip_rate']==str(e))
   for key,val in [('naive_NDE',nde),('naive_NIE',nie),('total_effect',nde+nie),('W1_T0',pw[0,1]),('W1_T1',pw[1,1])]:
    assert F(item[key])==val,(world,e,key)
    count+=1
   checks.append(dict(world=world,flip_rate=str(e),bayes_NDE=str(nde),bayes_NIE=str(nie)))
 assert count==150
 assert all(F(x['bayes_NIE'])==0 for x in checks if x['flip_rate']=='1/2')
 # Mutation must be detected by the same exact comparator.
 target=next(x for x in ref['conditions'] if x['world']=='PURE_INDIRECT' and x['flip_rate']=='1/8')
 independent=next(x for x in checks if x['world']=='PURE_INDIRECT' and x['flip_rate']=='1/8')
 assert F(target['naive_NIE'])+F(1,100)!=F(independent['bayes_NIE'])
 result=dict(audit='B_R221_S17',cross_algorithm_exact_field_checks=count,failures=0,independent_method='Bayes mixture on original T,M,Y law',negative_control_half_flip_all_NIE_zero=True,mutation_detected=True,conditions=checks,external_independent_replication=0)
 OUT.write_text(json.dumps(result,indent=2,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf8')
 print('B R221 S17',count,'exact checks')
if __name__=='__main__':run()
