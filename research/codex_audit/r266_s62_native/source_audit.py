"""Nonblind exact source-row reconstruction; no original R/B imports.

Scope: primitive values and derived moments/score metrics, not full metadata.
The native runner authenticates all source and receipt metadata via blob pins.
"""
import csv
from fractions import Fraction as F
import io

WORLDS=tuple((f,n) for f in ('THRESHOLD_Q1','THRESHOLD_HALF','THRESHOLD_Q3') for n in (2,4))+tuple(('SYMMETRIC_EXTREMES',n) for n in (2,4,6))
HEADER='world,function,evaluations,design,primitive_independent_draws,original_source_tuple,exact_source_mass,event_success_count,estimate,true_integral,squared_error'

def require(ok,message):
    if not ok:raise ValueError(message)

def event(fn,u):
    return int(u==0) if fn=='THRESHOLD_Q1' else int(u<=1) if fn=='THRESHOLD_HALF' else int(u<=2) if fn=='THRESHOLD_Q3' else int(u in (0,3))

def audit(csv_text,baseline,receipt):
    known={f'{fn}_N{n}':(fn,n) for fn,n in WORLDS};groups={};rows=list(csv.reader(io.StringIO(csv_text)))
    require(rows and rows.pop(0)==HEADER.split(','),'CSV schema')
    for row in rows:
        require(len(row)==11 and row[0] in known and row[3] in ('IID','ANTITHETIC'),'source identity')
        world,design=row[0],row[3];fn,n=known[world];draws=n if design=='IID' else n//2
        parts=row[5].split(';');require(len(parts)==draws and all(x in ('0','1','2','3') for x in parts),'primitive tuple')
        origin=tuple(map(int,parts));hit=sum(event(fn,u)+(event(fn,3-u) if design=='ANTITHETIC' else 0) for u in origin)
        p=F(sum(event(fn,u) for u in range(4)),4);est=F(hit,n);mass=F(1,4**draws)
        expected=[world,fn,str(n),design,str(draws),row[5],str(mass),str(hit),str(est),str(p),str((est-p)**2)]
        require(row==expected,'derived primitive source mismatch')
        key=world,design
        if key not in groups:groups[key]={'seen':set(),'sum':F(),'sum2':F(),'plugin':F(),'covered':0,'mass':F()}
        g=groups[key];require(origin not in g['seen'],'duplicate primitive');g['seen'].add(origin)
        g['sum']+=mass*est;g['sum2']+=mass*est**2;g['plugin']+=mass*est*(1-est)/n;g['mass']+=mass
        if n*(est-p)**2<=4*p*(1-p):g['covered']+=1
    require(len(rows)==5328 and len(groups)==18,'source universe')
    require(type(baseline.get('worlds')) is list and len(baseline['worlds'])==9,'baseline worlds')
    refs={w['world']:w for w in baseline['worlds']};require(set(refs)==set(known),'baseline universe')
    require(type(receipt.get('results')) is list and len(receipt['results'])==18,'receipt rows')
    result=[]
    for fn,n in WORLDS:
        world=f'{fn}_N{n}';p=F(sum(event(fn,u) for u in range(4)),4)
        for design in ('IID','ANTITHETIC'):
            g=groups[world,design];count=4**(n if design=='IID' else n//2)
            require(len(g['seen'])==count and g['mass']==1,'source completeness')
            mean=g['sum'];variance=g['sum2']-mean**2;require(mean==p,'unbiasedness')
            ref=refs[world]['designs'][design]
            require(ref['exact_mean']==str(mean) and ref['exact_variance']==str(variance) and ref['source_atoms']==count,'baseline moments')
            coverage=F(g['covered'],count)
            result.append({'world':world,'design':design,'evaluations':n,'source_atoms':count,'covered_atoms':g['covered'],
                           'exact_score_z2_coverage':str(coverage),'exact_score_z2_miscoverage':str(1-coverage),
                           'expected_naive_IID_plugin_variance':str(g['plugin']),'actual_estimator_variance':str(variance),
                           'naive_plugin_over_actual_variance':None if variance==0 else str(g['plugin']/variance)})
    for row,want in zip(receipt['results'],result):
        require(type(row) is dict and set(row)==set(want),'receipt row schema')
        for key,value in want.items():require(type(row[key]) is type(value) and row[key]==value,'receipt metric '+key)
    counter=next(r for r in result if r['world']=='SYMMETRIC_EXTREMES_N6' and r['design']=='ANTITHETIC')
    return {'status':'COMPLETE','source_rows':5328,'source_fields_checked':5328*11,'metric_rows':18,'metric_fields':180,
            'baseline_moment_rows':18,'symmetric_N6_antithetic_coverage':counter['exact_score_z2_coverage'],
            'symmetric_N6_antithetic_variance_ratio':counter['naive_plugin_over_actual_variance'],
            'evidence':'NONBLIND_INTERNAL_ARTIFICIAL_E1','external_team_replications':0}
