#!/usr/bin/env python3
"""B audit for R280 S76: independent binomial-count oracle and strict persisted receipt.

Usage: python b_r280_s76_count_and_receipt_audit_20261030.py CSV JSON
Standard library only; internal nonblind independent-method verification.
"""
import argparse
import copy
import csv
import json
from fractions import Fraction as F
from math import comb
from pathlib import Path

P = (F(1, 4), F(1, 2), F(3, 4))
Q = (F(1, 4), F(1, 2), F(3, 4))
PREF = {F(1, 2): 0, F(1, 4): 1, F(3, 4): 2}
FREEZE = '468ebb3006e864437fb8fc17cfcb39ed70b1bc1e'
COLS = ('true_p', 'train_bits', 'test_bits', 'source_mass', 'chosen_q',
        'train_score_q_1of4', 'train_score_q_1of2', 'train_score_q_3of4',
        'train_chosen_brier', 'train_oracle_brier', 'test_chosen_brier',
        'test_oracle_brier', 'test_regret', 'test_chosen_strictly_better',
        'test_chosen_tied')
KEYS = ('train_chosen', 'train_oracle', 'test_chosen', 'test_oracle',
        'train_regret', 'test_regret', 'test_minus_train', 'test_better',
        'test_tie', 'squared_bias')


def loss_count(k, q):
    return (F(k) * (1-q)**2 + F(4-k)*q*q)/4


def chosen_count(k):
    return min(Q, key=lambda q: (loss_count(k, q), PREF[q]))


def oracle_count():
    """Entirely count based: 25 (train count, test count) cells per true p."""
    result = {}
    for p in P:
        values = {key: F(0) for key in KEYS}
        choice = {q: F(0) for q in Q}
        mass_total = F(0)
        for k in range(5):
            q = chosen_count(k)
            pk = comb(4,k)*p**k*(1-p)**(4-k)
            for j in range(5):
                weight = pk*comb(4,j)*p**j*(1-p)**(4-j)
                mass_total += weight
                choice[q] += weight
                trainq, trainp = loss_count(k,q), loss_count(k,p)
                testq, testp = loss_count(j,q), loss_count(j,p)
                item = dict(train_chosen=trainq,train_oracle=trainp,
                    test_chosen=testq,test_oracle=testp,
                    train_regret=trainq-trainp,test_regret=testq-testp,
                    test_minus_train=testq-trainq,
                    test_better=F(int(testq<testp)),test_tie=F(int(testq==testp)),
                    squared_bias=(q-p)**2)
                for key in KEYS:
                    values[key] += weight*item[key]
        if mass_total != 1 or values['test_regret'] != values['squared_bias']:
            raise ValueError('independent oracle identity failure')
        result[str(p)] = {'source_types':256,'mass':'1',
            'chosen_probabilities':{str(q):str(choice[q]) for q in Q},
            'expectations':{k:str(values[k]) for k in KEYS}}
    return result


def require(condition, message):
    if not condition:
        raise ValueError(message)


def verify(rows, receipt):
    require(len(rows)==768,'source count')
    require(set(receipt)=={'research_id','original_catalogue_id','freeze_commit',
        'freeze_path','evidence','world_count','source_types','source_types_per_world',
        'train_size','heldout_size','candidate_q','tie_priority','R073','PESEN_v0_1',
        'new_real_human_E2_prediction','new_real_historical_E3_prediction',
        'world_results'},'receipt schema')
    require(receipt['research_id']=='R280_S76' and receipt['original_catalogue_id']=='12-010','research identity')
    require(receipt['freeze_commit']==FREEZE,'freeze commit')
    require(receipt['freeze_path']=='research/validation/R280_S76_POSTSELECTION_HOLDOUT_BRIER_FREEZE_2026-10-30.md','freeze path')
    require(receipt['evidence']=='E1_ARTIFICIAL_EXPLORATORY_NONBLIND','evidence class')
    require((receipt['world_count'],receipt['source_types'],receipt['source_types_per_world'],receipt['train_size'],receipt['heldout_size'])==(3,768,256,4,4),'source metadata')
    require(receipt['candidate_q']==['1/4','1/2','3/4'] and receipt['tie_priority']==['1/2','1/4','3/4'],'candidate/tie freeze')
    require(receipt['R073']=='FROZEN' and receipt['PESEN_v0_1']=='FROZEN' and receipt['new_real_human_E2_prediction']==0 and receipt['new_real_historical_E3_prediction']==0,'evidence boundary')
    require(len(receipt['world_results'])==3,'three worlds')
    worlds={x['true_p']:x for x in receipt['world_results']}
    require(set(worlds)==set(map(str,P)),'world identities')
    independent=oracle_count()
    for p in P:
        w=worlds[str(p)]
        require(set(w)=={'true_p','source_types','mass','chosen_probabilities','expectations'},'world schema')
        require({k:w[k] for k in ('source_types','mass','chosen_probabilities','expectations')}==independent[str(p)],'independent binomial oracle mismatch')
    seen=set()
    mass_by_world={str(p):F(0) for p in P}
    choice_by_train={}
    for row in rows:
        require(set(row)==set(COLS),'row columns')
        p=F(row['true_p']);require(p in P,'true p')
        train,test=row['train_bits'],row['test_bits']
        require(len(train)==len(test)==4 and set(train+test)<=set('01'),'bit format')
        key=(str(p),train,test)
        require(key not in seen,'duplicate source')
        seen.add(key)
        k,j=train.count('1'),test.count('1')
        mass=p**(k+j)*(1-p)**(8-k-j)
        require(F(row['source_mass'])==mass,'source mass')
        mass_by_world[str(p)]+=mass
        q=chosen_count(k)
        require(F(row['chosen_q'])==q,'test label contaminated train selection or argmin wrong')
        tkey=(str(p),train)
        if tkey in choice_by_train:
            require(choice_by_train[tkey]==q,'test label changes chosen q')
        choice_by_train[tkey]=q
        expected=(loss_count(k,Q[0]),loss_count(k,Q[1]),loss_count(k,Q[2]),
            loss_count(k,q),loss_count(k,p),loss_count(j,q),loss_count(j,p),
            loss_count(j,q)-loss_count(j,p))
        actual=tuple(F(row[col]) for col in COLS[5:13])
        require(actual==expected,'per-source score or regret mismatch')
        require(row['test_chosen_strictly_better']==str(int(expected[5]<expected[6])) and row['test_chosen_tied']==str(int(expected[5]==expected[6])),'test win/tie flag mismatch')
    require(len(seen)==768 and all(v==1 for v in mass_by_world.values()),'source mass/coverage')
    require(len(choice_by_train)==48,'train/test cross-product coverage')
    return {'worlds':3,'count_cells':75,'source_rows':len(seen),'train_prefixes':len(choice_by_train)}


def mutation_controls(rows,receipt):
    cases=[]
    def check_bad(label,rr,jj):
        try:
            verify(rr,jj)
        except (ValueError,KeyError,TypeError,ZeroDivisionError):
            cases.append(label)
            return
        raise AssertionError('undetected mutation: '+label)
    check_bad('missing_atom',rows[:-1],receipt)
    check_bad('duplicate_atom',rows+[copy.deepcopy(rows[-1])],receipt)
    rr=copy.deepcopy(rows);rr[0]['source_mass']='1';check_bad('mass_corruption',rr,receipt)
    rr=copy.deepcopy(rows);rr[0]['test_chosen_brier']='99';check_bad('test_score_corruption',rr,receipt)
    rr=copy.deepcopy(rows);rr[0]['chosen_q']='3/4' if rr[0]['chosen_q']!='3/4' else '1/4';check_bad('future_leak_selection',rr,receipt)
    jj=copy.deepcopy(receipt);jj['new_real_human_E2_prediction']=1;check_bad('E1_to_E2_promotion',rows,jj)
    return cases


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('csv_file')
    parser.add_argument('json_file')
    args=parser.parse_args()
    with Path(args.csv_file).open(newline='',encoding='utf-8') as f:
        reader=csv.DictReader(f)
        require(tuple(reader.fieldnames)==COLS,'CSV header')
        rows=list(reader)
    receipt=json.loads(Path(args.json_file).read_text(encoding='utf-8'))
    status=verify(rows,receipt)
    mutations=mutation_controls(rows,receipt)
    print('PASS independent 75 binomial count cells and strict persisted 768 rows')
    print('status',status)
    print('negative_controls',len(mutations),mutations)
    for p,w in oracle_count().items():
        print(p,w['expectations'])

if __name__=='__main__':
    main()
