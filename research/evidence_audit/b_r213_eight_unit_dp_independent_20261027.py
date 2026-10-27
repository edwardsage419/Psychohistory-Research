#!/usr/bin/env python3
"""Independent finite-state polynomial DP audit of frozen R213 CSV and R third-method receipt.
Run: python research/evidence_audit/b_r213_eight_unit_dp_independent_20261027.py
"""
import csv
import hashlib
import json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT/'research/R213/R213_ALL_128_ORIGINAL_INSTRUMENT_SOURCE_ATOMS.csv'
RECEIPT = ROOT/'research/validation/R213_FINITE_ASSIGNMENT_8_WORLD_REPLAY_MATCHED_RECEIPT_V2_2026-10-27.json'
FIELDS = ('empty_arm','zero_sample_first_stage','defined')


def read_source():
    data = defaultdict(dict)
    with SOURCE.open(newline='', encoding='utf-8') as f:
        for r in csv.DictReader(f):
            w = r['world']; i = int(r['latent_source_person_i']); z = int(r['instrument_assignment_Z'])
            assert 0 <= i < 8 and z in (0,1) and (i,z) not in data[w]
            data[w][(i,z)] = (int(r['observed_actual_D']), F(r['observed_actual_Y_exact']),
                              F(r['person_specific_instrument_propensity_exact']),
                              F(r['joint_source_probability_exact']))
    assert len(data)==8 and all(len(d)==16 for d in data.values())
    for w, d in data.items():
        assert sum((x[3] for x in d.values()), F(0)) == 1
        for i in range(8):
            assert d[(i,0)][2]==d[(i,1)][2]
            assert d[(i,0)][3] + d[(i,1)][3] == F(1,8)
    return data


def dp_summary(d, late_text):
    # State: treated-arm count, D1 sum, D0 sum, Y1 sum, Y0 sum.
    # Each state carries number of assignments and exact probability mass.
    states = {(0,0,0,F(0),F(0)): (1,F(1))}
    for i in range(8):
        new = defaultdict(lambda: (0,F(0)))
        for state,(count,mass) in states.items():
            for z in (0,1):
                di,yi,q,_ = d[(i,z)]
                n1,ds1,ds0,ys1,ys0 = state
                next_state = (n1+z, ds1+di if z else ds1,
                              ds0+di if not z else ds0,
                              ys1+yi if z else ys1,
                              ys0+yi if not z else ys0)
                prev_count,prev_mass = new[next_state]
                new[next_state] = (prev_count+count,prev_mass+mass*(q if z else 1-q))
        states = dict(new)
    tally = {k: [0,F(0)] for k in FIELDS}
    tail10=gap2=wald_sum=max_abs=F(0)
    late = None if late_text=='UNDEFINED_NO_COMPLIERS' else F(late_text)
    for (n1,d1,d0,y1,y0),(count,mass) in states.items():
        n0=8-n1
        if n1==0 or n0==0: status='empty_arm'
        elif F(d1,n1)-F(d0,n0)==0: status='zero_sample_first_stage'
        else:
            status='defined'
            wald=(y1/n1-y0/n0)/(F(d1,n1)-F(d0,n0))
            wald_sum += mass*wald
            max_abs=max(max_abs,abs(wald))
            if abs(wald)>=10: tail10 += mass
            if late is not None and abs(wald-late)>=2: gap2 += mass
        tally[status][0]+=count
        tally[status][1]+=mass
    assert sum(x[0] for x in tally.values())==256
    assert sum((x[1] for x in tally.values()),F(0))==1
    defined=tally['defined'][1]
    return {'assignment_count':256, 'assignment_probability_sum_exact':'1',
            'empty_arm_count':tally['empty_arm'][0],
            'empty_arm_probability_exact':str(tally['empty_arm'][1]),
            'zero_sample_first_stage_count':tally['zero_sample_first_stage'][0],
            'zero_sample_first_stage_probability_exact':str(tally['zero_sample_first_stage'][1]),
            'defined_count':tally['defined'][0],
            'defined_probability_exact':str(defined),
            'wald_mean_conditional_defined_exact':str(wald_sum/defined) if defined else 'UNDEFINED_NO_DEFINED_ASSIGNMENT',
            'max_absolute_defined_wald_exact':str(max_abs) if defined else 'UNDEFINED',
            'absolute_wald_at_least_10_unconditional_probability_exact':str(tail10),
            'absolute_wald_at_least_10_conditional_defined_probability_exact':str(tail10/defined) if defined else 'UNDEFINED',
            'absolute_wald_minus_late_at_least_2_unconditional_probability_exact':str(gap2) if late is not None else 'NOT_APPLICABLE_NO_COMPLIERS',
            'absolute_wald_minus_late_at_least_2_conditional_defined_probability_exact':str(gap2/defined) if late is not None and defined else 'NOT_APPLICABLE'}


def compute():
    data = read_source()
    receipt = json.loads(RECEIPT.read_text(encoding='utf-8'))
    assert receipt['world_count']==8 and receipt['assignment_vectors_total']==2048
    checks=0
    independent=[]
    for w in receipt['summary_worlds']:
        world=w['world']
        actual=dp_summary(data[world],w['population_complier_LATE_exact'])
        for key, value in actual.items():
            assert w[key]==value, (world,key,w[key],value)
            checks+=1
        independent.append({'world':world,**actual})
    assert checks==8*len(actual)
    # Negative controls are checked against an unchanged frozen R receipt.
    mutant={key:tuple(value) for key,value in data['FULL_COMPLY'].items()}
    d,y,q,p=mutant[(0,1)]
    mutant[(0,1)]=(d,y+1,q,p)
    mutated=dp_summary(mutant,'5/2')
    assert mutated['wald_mean_conditional_defined_exact'] != receipt['summary_worlds'][0]['wald_mean_conditional_defined_exact']
    assert any(x['zero_sample_first_stage_count']>0 for x in independent)
    assert all(x['empty_arm_count']==2 for x in independent)
    return {'audit':'B_R213_FINITE_ASSIGNMENT_INDEPENDENT_STATE_DP',
            'evidence':'E1_INTERNAL_INDEPENDENT_ALGORITHM',
            'source_csv_sha256':hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            'R_receipt_sha256':hashlib.sha256(RECEIPT.read_bytes()).hexdigest(),
            'worlds':8, 'assignment_vectors':2048, 'exact_cross_method_fields_passed':checks,
            'mutation_Y_detected':True,'zero_sample_first_stage_undefined_guard':True,
            'empty_arm_guard':True,'failed':0,
            'external_replication':False,'E2':0,'E3':0,
            'independent_worlds':independent}


if __name__=='__main__':
    print(json.dumps(compute(),indent=2,sort_keys=True,ensure_ascii=False))
