#!/usr/bin/env python3
"""R269 S65 exact E1 postselection risk, standard library only.
Frozen protocol: protocols/R269_S65_POSTSELECTION_NEW_GROUP_BRIER_PRESCORE_FREEZE_2026-10-29.md
"""
import argparse
import itertools
import json
from collections import Counter
from fractions import Fraction as F
from math import comb

PS = (F(1,4), F(1,2), F(3,4))
MODELS = ('GROUP_ID_MEMORIZER', 'GLOBAL_LAPLACE', 'CONSTANT_HALF')
POLICIES = ('LOOR', 'LOGO')


def brier(q, y):
    return (q-y)**2


def predict(model, training, group):
    if model == MODELS[0]:
        matches = [y for g,y in training if g==group]
        return F(matches[0]) if matches else F(1,2)
    if model == MODELS[1]:
        return F(sum(y for _,y in training)+1, len(training)+2)
    if model == MODELS[2]:
        return F(1,2)
    raise ValueError(model)


def cv_score(z, model, policy):
    rows = [(g,z[g]) for g in range(6) for _ in range(2)]
    loss=F(0)
    for j,(g,y) in enumerate(rows):
        if policy == 'LOOR':
            train = rows[:j]+rows[j+1:]
        elif policy == 'LOGO':
            train = [row for row in rows if row[0]!=g]
        else:
            raise ValueError(policy)
        loss+=brier(predict(model,train,g), y)
    return loss/12


def new_group_risk(z, model, p):
    rows = [(g,z[g]) for g in range(6) for _ in range(2)]
    q=predict(model,rows,6)
    return (1-p)*brier(q,0)+p*brier(q,1)


def source_weight(z,p):
    k=sum(z)
    return p**k*(1-p)**(6-k)


def fstr(x):
    return str(x)


def calculate_direct():
    result={}
    for p in PS:
        rows={policy: {'risk':F(0),'cv':F(0),'counts':Counter(),'ties':F(0)} for policy in POLICIES}
        fixed={model:F(0) for model in MODELS}
        mass=F(0)
        for z in itertools.product((0,1), repeat=6):
            w=source_weight(z,p)
            mass+=w
            for model in MODELS:
                fixed[model]+=w*new_group_risk(z,model,p)
            for policy in POLICIES:
                scores={m:cv_score(z,m,policy) for m in MODELS}
                best=min(scores.values())
                winners=[m for m in MODELS if scores[m]==best]
                chosen=winners[0]
                rows[policy]['risk']+=w*new_group_risk(z,chosen,p)
                rows[policy]['cv']+=w*best
                rows[policy]['counts'][chosen]+=w
                if len(winners)>1:
                    rows[policy]['ties']+=w
        assert mass==1
        r={}
        for policy in POLICIES:
            d=rows[policy]
            r[policy]={'expected_new_group_brier':fstr(d['risk']), 'expected_selected_cv_brier':fstr(d['cv']),
                       'cv_minus_new_group':fstr(d['cv']-d['risk']),
                       'selection_mass':{m:fstr(d['counts'][m]) for m in MODELS},
                       'tie_mass':fstr(d['ties'])}
        r['LOGO_minus_LOOR_future_risk']=fstr(rows['LOGO']['risk']-rows['LOOR']['risk'])
        r['fixed_model_new_group_risk']={m:fstr(fixed[m]) for m in MODELS}
        result[fstr(p)]=r
    return {'research':'R269_S65','evidence':'E1_ARTIFICIAL','protocol':'R269_S65_POSTSELECTION_NEW_GROUP_BRIER_PRESCORE_FREEZE_2026-10-29.md','worlds':result}


def calculate_analytic():
    """Independent K-distribution and closed-form CV route; no fold reconstruction."""
    out={}
    for p in PS:
        data={v:{'risk':F(0),'cv':F(0),'counts':Counter(),'ties':F(0)} for v in POLICIES}
        fixed={m:F(0) for m in MODELS}
        for k in range(7):
            w=F(comb(6,k))*p**k*(1-p)**(6-k)
            # Group symmetry: average of the six possible target groups.
            lap_logo = F(0)
            lap_loor = F(0)
            for b,n in ((0,6-k),(1,k)):
                if not n: continue
                s=k-b
                lap_logo+=F(n,6)*(F(1-b)*(F(2*s+1,12)-b)**2+F(b)*(F(2*s+1,12)-b)**2)
                lap_loor+=F(n,6)*(F(2*s+b+1,13)-b)**2
            scores={'LOOR':(F(0),lap_loor,F(1,4)),'LOGO':(F(1,4),lap_logo,F(1,4))}
            q=F(2*k+1,14)
            risks=(F(1,4),(1-p)*q*q+p*(1-q)**2,F(1,4))
            for i,m in enumerate(MODELS):
                fixed[m]+=w*risks[i]
            for pol in POLICIES:
                v=scores[pol]
                best=min(v)
                winners=[i for i in range(3) if v[i]==best]
                chosen=winners[0]
                d=data[pol]
                d['risk']+=w*risks[chosen]
                d['cv']+=w*best
                d['counts'][MODELS[chosen]]+=w
                if len(winners)>1: d['ties']+=w
        r={}
        for pol in POLICIES:
            d=data[pol]
            r[pol]={'expected_new_group_brier':fstr(d['risk']), 'expected_selected_cv_brier':fstr(d['cv']),
                    'cv_minus_new_group':fstr(d['cv']-d['risk']),
                    'selection_mass':{m:fstr(d['counts'][m]) for m in MODELS},
                    'tie_mass':fstr(d['ties'])}
        r['LOGO_minus_LOOR_future_risk']=fstr(data['LOGO']['risk']-data['LOOR']['risk'])
        r['fixed_model_new_group_risk']={m:fstr(fixed[m]) for m in MODELS}
        out[fstr(p)]=r
    return {'research':'R269_S65','evidence':'E1_ARTIFICIAL','protocol':'R269_S65_POSTSELECTION_NEW_GROUP_BRIER_PRESCORE_FREEZE_2026-10-29.md','worlds':out}


def validate(receipt):
    if type(receipt) is not dict or set(receipt)!={'research','evidence','protocol','worlds'}:
        raise ValueError('top level identity')
    if receipt['research']!='R269_S65' or receipt['evidence']!='E1_ARTIFICIAL' or receipt['protocol']!='R269_S65_POSTSELECTION_NEW_GROUP_BRIER_PRESCORE_FREEZE_2026-10-29.md':
        raise ValueError('identity or evidence')
    if type(receipt['worlds']) is not dict or set(receipt['worlds'])!={str(p) for p in PS}:
        raise ValueError('world coverage')
    for p,d in receipt['worlds'].items():
        if type(d) is not dict or set(d)!={'LOOR','LOGO','LOGO_minus_LOOR_future_risk','fixed_model_new_group_risk'}:
            raise ValueError('world fields')
        for policy in POLICIES:
            v=d[policy]
            if type(v) is not dict or set(v)!={'expected_new_group_brier','expected_selected_cv_brier','cv_minus_new_group','selection_mass','tie_mass'}:
                raise ValueError('policy fields')
            for k in ('expected_new_group_brier','expected_selected_cv_brier','cv_minus_new_group','tie_mass'):
                if type(v[k]) is not str: raise ValueError('fraction type')
                F(v[k])
            if type(v['selection_mass']) is not dict or set(v['selection_mass'])!=set(MODELS):
                raise ValueError('selection coverage')
            if any(type(v['selection_mass'][m]) is not str for m in MODELS): raise ValueError('selection types')
            if sum((F(v['selection_mass'][m]) for m in MODELS),F(0))!=1:
                raise ValueError('selection normalization')
            if F(v['cv_minus_new_group'])!=F(v['expected_selected_cv_brier'])-F(v['expected_new_group_brier']):
                raise ValueError('optimism identity')
        if type(d['LOGO_minus_LOOR_future_risk']) is not str: raise ValueError('paired type')
        if F(d['LOGO_minus_LOOR_future_risk'])!=F(d['LOGO']['expected_new_group_brier'])-F(d['LOOR']['expected_new_group_brier']):
            raise ValueError('paired identity')
        if type(d['fixed_model_new_group_risk']) is not dict or set(d['fixed_model_new_group_risk'])!=set(MODELS):
            raise ValueError('fixed coverage')
        if any(type(d['fixed_model_new_group_risk'][m]) is not str for m in MODELS): raise ValueError('fixed types')
    if receipt!=calculate_analytic(): raise ValueError('independent exact oracle mismatch')
    return True


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--emit',metavar='PATH')
    ap.add_argument('--check',metavar='PATH')
    ap.add_argument('--selftest',action='store_true')
    args=ap.parse_args()
    if args.selftest:
        a=calculate_direct();b=calculate_analytic()
        assert a==b, (a,b)
        assert validate(a)
        import copy
        mutations=[]
        x=copy.deepcopy(a);x['worlds']['1/4']['LOGO']['expected_new_group_brier']='999';mutations.append(x)
        x=copy.deepcopy(a);x['worlds']['1/2']['LOGO']['selection_mass']['CONSTANT_HALF']='999';mutations.append(x)
        x=copy.deepcopy(a);del x['worlds']['3/4'];mutations.append(x)
        x=copy.deepcopy(a);x['evidence']='E2_HUMAN';mutations.append(x)
        x=copy.deepcopy(a);x['worlds']['1/4']['LOGO']['tie_mass']=False;mutations.append(x)
        for i,x in enumerate(mutations):
            try: validate(x)
            except (ValueError,TypeError,ZeroDivisionError): continue
            raise AssertionError(f'mutation {i} accepted')
        print('PASS: 3 p worlds, 2 policies, direct 64-source vs binomial oracle, 5 mutation controls')
    if args.emit:
        with open(args.emit,'w',encoding='utf8') as f: json.dump(calculate_direct(),f,indent=2,ensure_ascii=False);f.write('\n')
    if args.check:
        with open(args.check,encoding='utf8') as f: data=json.load(f)
        assert validate(data)
        print('PASS: persisted receipt matches independent exact binomial oracle')

if __name__=='__main__': main()
