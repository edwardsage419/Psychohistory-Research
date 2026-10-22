#!/usr/bin/env python3
"""R223: exact synthetic confounding, positivity and RR/E-value sensitivity."""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
import unittest
from collections import defaultdict
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ZERO=F(0)
ONE=F(1)
# (p(T=1|U0), p(T=1|U1), (Y0 success count U0,U1), (Y1 count U0,U1))
WORLDS={
 'NULL_CONFOUNDED': (F(1,4),F(3,4),(2,14),(2,14)),
 'CAUSAL_ALIAS': (F(1,2),F(1,2),(5,5),(11,11)),
 'UNCONFOUNDED_CAUSAL':(F(1,2),F(1,2),(2,8),(6,12)),
 'CONFOUNDED_CAUSAL':(F(1,4),F(3,4),(2,8),(6,12)),
 'CONFOUNDED_REVERSED':(F(1,4),F(3,4),(6,14),(2,10)),
 'WEAK_OVERLAP':(F(1,16),F(15,16),(2,8),(6,12)),
 'NO_POSITIVITY':(ZERO,ONE,(2,8),(6,12)),
}


def source_rows(name):
    if name not in WORLDS: raise ValueError('unknown world')
    p0,p1,c0,c1=WORLDS[name]
    rows=[]
    for u,p in enumerate((p0,p1)):
        for t in (0,1):
            pt=(p if t else ONE-p)
            for v in range(16):
                y0=int(v<c0[u]);y1=int(v<c1[u])
                rows.append(dict(world=name,U_oracle=u,observed_T=t,V_oracle=v,
                                 observed_Y=y1 if t else y0, oracle_Y0=y0,oracle_Y1=y1,
                                 source_probability=F(1,2)*pt/F(16),
                                 supported_assignment=int(pt>0)))
    assert len(rows)==64 and sum((r['source_probability'] for r in rows),ZERO)==ONE
    return tuple(rows)


def joint_observed(rows):
    d=defaultdict(F)
    for row in rows:
        d[(row['observed_T'],row['observed_Y'])]+=row['source_probability']
    return {f'T{t}Y{y}':d[t,y] for t in (0,1) for y in (0,1)}


def observed_risks(rows):
    d=joint_observed(rows)
    r={}
    for t in (0,1):
        den=d[f'T{t}Y0']+d[f'T{t}Y1']
        if den<=0: raise AssertionError('frozen two observed treatment classes unsupported')
        r[t]=d[f'T{t}Y1']/den
    if r[0]<=0 or r[1]<=0: raise AssertionError('frozen positive observed risk')
    return r[0],r[1]


def oracle_risks(rows):
    # Reweight over exogenous U,V without treatment assignment selection.
    types={}
    for u in (0,1):
        # Capture the 16 unique potential records via the t=0 structural rows,
        # including probabilities zero under natural assignment.
        a=[r for r in rows if r['U_oracle']==u and r['observed_T']==0]
        assert len(a)==16
        types[u]=(sum(r['oracle_Y0'] for r in a)/F(16),sum(r['oracle_Y1'] for r in a)/F(16))
    return ((types[0][0]+types[1][0])/2,(types[0][1]+types[1][1])/2)


def standardized_observed_risks(rows):
    d=defaultdict(F); n=defaultdict(F)
    for r in rows:
        k=(r['U_oracle'],r['observed_T'])
        d[k]+=r['source_probability'];n[k]+=r['source_probability']*r['observed_Y']
    if any(d[u,t]==0 for u in (0,1) for t in (0,1)):
        return None
    return tuple(sum((n[u,t]/d[u,t] for u in (0,1)),ZERO)/2 for t in (0,1))


def independent_closed_form(name):
    p0,p1,c0,c1=WORLDS[name]
    pt1=(p0+p1)/2
    pt0=1-pt1
    e1=(p0*F(c1[0],16)+p1*F(c1[1],16))/(p0+p1)
    e0=((1-p0)*F(c0[0],16)+(1-p1)*F(c0[1],16))/(2-p0-p1)
    causal=(F(c0[0]+c0[1],32),F(c1[0]+c1[1],32))
    return e0,e1,causal


def sensitivity_parameters(rows):
    d=defaultdict(F); y=defaultdict(F)
    for r in rows:
        k=(r['U_oracle'],r['observed_T'])
        d[k]+=r['source_probability']
        y[k]+=r['source_probability']*r['observed_Y']
    if any(d[u,t]==0 for u in (0,1) for t in (0,1)):
        return None
    ptr={t:sum(d[u,t] for u in (0,1)) for t in (0,1)}
    rr_eu=max((d[u,1]/ptr[1])/(d[u,0]/ptr[0]) for u in (0,1))
    rr_ud=max(max(y[u,t]/d[u,t] for u in (0,1))/min(y[u,t]/d[u,t] for u in (0,1)) for t in (0,1))
    bf=rr_eu*rr_ud/(rr_eu+rr_ud-1)
    return rr_eu,rr_ud,bf


def decimal_e_value(rr):
    if rr<=0: raise ValueError('RR must be positive')
    q=max(rr,ONE/rr)
    with localcontext() as ctx:
        ctx.prec=50
        d=Decimal(q.numerator)/Decimal(q.denominator)
        x=d+(d*(d-1)).sqrt()
        assert abs(x*x/(2*x-1)-d)<Decimal('1e-44')
        return str(x)


def world_result(name):
    rows=source_rows(name)
    r0,r1=observed_risks(rows)
    true0,true1=oracle_risks(rows)
    e0,e1,closed=independent_closed_form(name)
    if (r0,r1)!=(e0,e1) or (true0,true1)!=closed:
        raise AssertionError('exact source and independent analytic formulas diverge')
    standardized=standardized_observed_risks(rows)
    if standardized is not None and standardized!=(true0,true1):
        raise AssertionError('observed U adjustment must recover oracle under positivity')
    params=sensitivity_parameters(rows)
    obs_rr=r1/r0;true_rr=true1/true0
    if params is not None:
        rreu,rrud,bf=params
        if true_rr<obs_rr/bf: raise AssertionError('bounding factor lower inequality failure')
    else: rreu=rrud=bf=None
    return dict(world=name,source_structural_atoms=64,
                positive_probability_atoms=sum(r['source_probability']>0 for r in rows),
                observed_joint_TY={k:str(v) for k,v in joint_observed(rows).items()},
                observed_risk_T0=str(r0),observed_risk_T1=str(r1),
                observed_RR=str(obs_rr),
                true_intervention_risk_T0=str(true0),true_intervention_risk_T1=str(true1),
                true_causal_RR=str(true_rr),
                observed_U_standardized_risk=None if standardized is None else [str(x) for x in standardized],
                standardized_status='UNIDENTIFIED_NO_POSITIVITY' if standardized is None else 'EXACT_UNDER_OBSERVED_U_AND_POSITIVITY',
                oracle_sensitivity_RR_EU=None if rreu is None else str(rreu),
                oracle_sensitivity_RR_UD=None if rrud is None else str(rrud),
                oracle_bias_factor=None if bf is None else str(bf),
                oracle_bounded_RR_lower=None if bf is None else str(obs_rr/bf),
                association_E_value_point_50digit=decimal_e_value(obs_rr))


def generate():
    res=[world_result(w) for w in WORLDS]
    a,b=res[0],res[1]
    assert a['observed_joint_TY']==b['observed_joint_TY']
    assert (a['true_causal_RR'],b['true_causal_RR'])==('1','11/5')
    results=dict(research_id='R223',catalogue_id='09-014',scientific_scope='FINITE_ARTIFICIAL_E1',
                 protocol_commit='1fec84f11e180f4dcd409f42318d8585d2787374',
                 all_structural_atoms=448,positive_probability_atoms=416,
                 new_real_human_E2=0,new_real_historical_E3=0,worlds=res)
    src=HERE/'R223_ALL_448_ORIGINAL_CONFOUNDING_STRUCTURAL_ATOMS.csv'
    columns=('world','U_oracle','observed_T','V_oracle','observed_Y','oracle_Y0','oracle_Y1','source_probability','supported_assignment')
    with src.open('w',newline='',encoding='utf-8') as f:
        wr=csv.DictWriter(f,fieldnames=columns,lineterminator='\n');wr.writeheader()
        for w in WORLDS:
            for row in source_rows(w): wr.writerow({k:str(row[k]) for k in columns})
    out=HERE/'R223_EXACT_RESULTS.json'
    out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    receipt=dict(research_id='R223',original_catalogue='09-014',worlds=7,
                 full_structural_atom_rows=448,positive_source_atom_rows=416,
                 original_source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
                 exact_results_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
                 new_real_human_E2=0,new_real_historical_E3=0)
    (HERE/'R223_FINAL_MACHINE_ACCEPTANCE.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    return receipt


class Tests(unittest.TestCase):
    def test_world_count(self): self.assertEqual(len(WORLDS),7)
    def test_all_original_states(self): self.assertEqual(sum(len(source_rows(w)) for w in WORLDS),448)
    def test_positive_count(self): self.assertEqual(sum(sum(r['source_probability']>0 for r in source_rows(w)) for w in WORLDS),416)
    def test_null_alias_actual_distribution(self): self.assertEqual(joint_observed(source_rows('NULL_CONFOUNDED')),joint_observed(source_rows('CAUSAL_ALIAS')))
    def test_null_alias_true_differs(self):
        a=world_result('NULL_CONFOUNDED');b=world_result('CAUSAL_ALIAS')
        self.assertEqual((a['true_causal_RR'],b['true_causal_RR']),('1','11/5'))
    def test_null_obs_rr(self): self.assertEqual(world_result('NULL_CONFOUNDED')['observed_RR'],'11/5')
    def test_confounded_causes_obs_rr(self): self.assertEqual(world_result('CONFOUNDED_CAUSAL')['observed_RR'],'3')
    def test_reversed_effect(self):
        a=world_result('CONFOUNDED_REVERSED')
        self.assertEqual((a['observed_RR'],a['true_causal_RR']),('1','3/5'))
    def test_no_positivity(self): self.assertEqual(world_result('NO_POSITIVITY')['standardized_status'],'UNIDENTIFIED_NO_POSITIVITY')
    def test_null_bf(self): self.assertEqual(world_result('NULL_CONFOUNDED')['oracle_bias_factor'],'7/3')
    def test_evalue_one(self): self.assertEqual(decimal_e_value(ONE),'1')
    def test_evalue_reciprocal(self): self.assertEqual(decimal_e_value(F(2)),decimal_e_value(F(1,2)))
    def test_bad_world(self):
        with self.assertRaises(ValueError): source_rows('UNKNOWN')


def _world_test(world,kind):
    def t(self):
        src=source_rows(world)
        if kind=='normalization': self.assertEqual(sum((r['source_probability'] for r in src),ZERO),1)
        elif kind=='binary': self.assertTrue(all(r['observed_Y'] in (0,1) for r in src))
        elif kind=='oracle': self.assertEqual(len([r for r in src if r['U_oracle']==0]),32)
        elif kind=='analytic':
            x,y,z=independent_closed_form(world)
            self.assertEqual(observed_risks(src),(x,y))
            self.assertEqual(oracle_risks(src),z)
        elif kind=='full': self.assertEqual(world_result(world)['source_structural_atoms'],64)
        else: raise ValueError('bad test')
    return t
for _world in WORLDS:
    for _kind in ('normalization','binary','oracle','analytic','full'):
        setattr(Tests,'test_'+_world.lower()+'_'+_kind,_world_test(_world,_kind))

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    flags=parser.add_mutually_exclusive_group(required=True)
    flags.add_argument('--test',action='store_true');flags.add_argument('--emit',action='store_true')
    args=parser.parse_args()
    if args.test:unittest.main(argv=['r223'],verbosity=2)
    else: print(json.dumps(generate(),indent=2))
