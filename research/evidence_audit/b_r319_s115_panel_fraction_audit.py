#!/usr/bin/env python3
"""Independent no-import exact audit of R319 S115 synthetic two-occasion panels."""
from __future__ import annotations
import argparse
import copy
import csv
import io
import json
from fractions import Fraction
from itertools import product
from pathlib import Path

SETS = ((0, 1), (0, 1, 2), (0, 1, 1), (0, 2, 1), (0, 2, 2))
MASSES = (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4))
FIELDS = ('world_id','choice_set_id','features','q_plus','mechanism','choice_t1','choice_t2','joint_probability')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def conditionals(xs, beta):
    # Independently construct a categorical distribution by normalizing weights.
    weights = [Fraction(2) ** (beta * x) for x in xs]
    total = sum(weights)
    return tuple(w / total for w in weights)


def expected():
    rows = {}
    worlds = {}
    for si, xs in enumerate(SETS):
        positive = conditionals(xs, 1)
        negative = conditionals(xs, -1)
        for qi, q in enumerate(MASSES):
            wid = 3 * si + qi
            marg = tuple(q * a + (1-q) * b for a,b in zip(positive, negative))
            persistent, redraw = {}, {}
            for j,k in product(range(len(xs)), repeat=2):
                # Independent latent-path enumeration: persistent beta_1=beta_2;
                # redraw sums over all four ordered latent-type pairs.
                persist = sum((weight * probs[j] * probs[k] for weight,probs in
                               ((q,positive),(1-q,negative))), Fraction(0))
                redraw_value = sum((w1*w2*p1[j]*p2[k] for (w1,p1),(w2,p2) in
                                    product(((q,positive),(1-q,negative)), repeat=2)), Fraction(0))
                persistent[(j,k)] = persist
                redraw[(j,k)] = redraw_value
                for mechanism, val in (('PERSISTENT',persist),('REDRAW',redraw_value)):
                    rows[(wid,mechanism,j,k)] = (f'S{si}','|'.join(map(str,xs)),str(q),str(val))
            tv = sum((abs(persistent[key]-redraw[key]) for key in persistent), Fraction(0))/2
            for j,k in persistent:
                delta = q*(1-q)*(positive[j]-negative[j])*(positive[k]-negative[k])
                require(persistent[(j,k)]-redraw[(j,k)]==delta, 'latent covariance identity')
            worlds[wid] = dict(world_id=wid,choice_set_id=f'S{si}',features=list(xs),q_plus=str(q),
                               marginal_probabilities=list(map(str,marg)),tv_distance=str(tv),
                               equal_prior_bayes_accuracy=str((1+tv)/2))
    return rows, worlds


def boundary_controls():
    count=0
    for xs in SETS:
        for q in (Fraction(0), Fraction(1)):
            pp,pm=conditionals(xs,1),conditionals(xs,-1)
            marg=tuple(q*a+(1-q)*b for a,b in zip(pp,pm))
            for j,k in product(range(len(xs)),repeat=2):
                p=q*pp[j]*pp[k]+(1-q)*pm[j]*pm[k]
                require(p==marg[j]*marg[k], 'boundary persistence mismatch')
            count+=1
    return count


def validate(csv_text, summary):
    expected_rows, expected_worlds = expected()
    require(boundary_controls()==10, 'boundary controls')
    require(set(summary) == {'schema','original_model','original_catalogue_id','synthetic_only','source_worlds','ordered_joint_cells','mechanisms','worlds'}, 'summary keys')
    require(summary['schema']=='r319_s115_two_occasion_persistence_e1_v1', 'schema')
    require(summary['original_model']=='R319' and summary['original_catalogue_id']=='01-007', 'model identity')
    require(summary['synthetic_only'] is True, 'evidence level')
    require(summary['source_worlds']==15 and summary['ordered_joint_cells']==240, 'summary universe')
    require(summary['mechanisms']==['PERSISTENT','REDRAW'], 'mechanism labels')
    require(len(summary['worlds'])==15, 'world length')
    require({w['world_id'] for w in summary['worlds']}==set(range(15)), 'world coverage')
    for w in summary['worlds']:
        require(w==expected_worlds[w['world_id']], 'world exact result mismatch')
    reader=csv.DictReader(io.StringIO(csv_text))
    require(tuple(reader.fieldnames or ())==FIELDS, 'csv header')
    observed={}
    for row in reader:
        require(None not in row and all(v is not None for v in row.values()), 'csv field count')
        key=(int(row['world_id']),row['mechanism'],int(row['choice_t1']),int(row['choice_t2']))
        require(key not in observed, 'duplicate outcome key')
        observed[key]=(row['choice_set_id'],row['features'],row['q_plus'],row['joint_probability'])
    require(len(observed)==240 and set(observed)==set(expected_rows), 'complete joint universe')
    for key,val in observed.items():
        require(val==expected_rows[key], 'exact source cell mismatch')
    return {'joint_cells':len(observed),'worlds':15,'boundary_controls':10,'mutations_checked':0,'status':'PASS'}


def mutation_tests(csv_text, summary):
    lines=csv_text.splitlines(keepends=True)
    require(len(lines)==241, 'expected input lines')
    tests={
        'delete_cell': (''.join(lines[:2]+lines[3:]),summary),
        'duplicate_cell': (''.join(lines[:2]+[lines[1]]+lines[2:]),summary),
        'probability_tamper': (csv_text.replace('1/4,PERSISTENT,0,0,', '1/4,PERSISTENT,0,0,999',1),summary),
        'mechanism_swap': (csv_text.replace(',PERSISTENT,0,0,', ',REDRAW,0,0,',1),summary),
        'alternative_index': (csv_text.replace(',PERSISTENT,0,0,', ',PERSISTENT,3,0,',1),summary),
        'mixing_mass': (csv_text.replace(',1/4,PERSISTENT,0,0,', ',1/3,PERSISTENT,0,0,',1),summary),
    }
    bad=copy.deepcopy(summary);bad['worlds'][1]['tv_distance']='1/2';tests['tv_summary_tamper']=(csv_text,bad)
    bad=copy.deepcopy(summary);bad['synthetic_only']=False;tests['false_evidence_promotion']=(csv_text,bad)
    rejected=[]
    for name,(csv_data,json_data) in tests.items():
        try:
            validate(csv_data,json_data)
        except (ValueError,TypeError,KeyError,IndexError):
            rejected.append(name)
        else:
            raise RuntimeError('MUTATION_ACCEPTED: '+name)
    require(len(rejected)==8, 'mutation coverage')
    return rejected


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--csv',type=Path,required=True)
    parser.add_argument('--summary',type=Path,required=True)
    parser.add_argument('--selftest',action='store_true')
    args=parser.parse_args()
    csv_data=args.csv.read_text(encoding='utf-8')
    summary=json.loads(args.summary.read_text(encoding='utf-8'))
    receipt=validate(csv_data,summary)
    if args.selftest:
        receipt['mutations_checked']=len(mutation_tests(csv_data,summary))
    print(json.dumps(receipt,sort_keys=True))

if __name__=='__main__':
    main()
