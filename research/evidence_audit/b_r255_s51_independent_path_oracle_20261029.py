#!/usr/bin/env python3
"""Independent exact R255 S51 oracle from 8 edge masks x 8 opinion seeds.

Uses walk expansion, never imports the R trajectory or matrix iteration code.
Checks the R reconstructed 512-row CSV and frozen receipt, plus mutation test.
"""
import csv
import hashlib
import itertools
import json
import sys
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

EDGES=((0,1),(0,2),(1,2))
WORLDS=('ER_TRIANGLE_P_HALF','STATIC_EMPTY_TRUE_GRAPH_OBS_REPORT_HALF')

def weights(mask):
    w={}
    for i in range(3):
        for j in range(3):
            if i==j:
                w[i,j]=Q(1)-Q(sum(mask[k] for k,(u,v) in enumerate(EDGES) if i in (u,v)),4)
            else:
                edge_index=EDGES.index((min(i,j),max(i,j)))
                w[i,j]=Q(mask[edge_index],4)
    return w

def path_opinion(mask,seed,n):
    w=weights(mask)
    result=[]
    for i in range(3):
        if n==0:
            result.append(Q(seed[i]));continue
        s=Q(0)
        for path in itertools.product(range(3),repeat=n):
            product=Q(1);prev=i
            for nxt in path:
                product*=w[prev,nxt];prev=nxt
            s+=product*seed[prev]
        result.append(s)
    return tuple(result)

def risk_group(rows,idx,alias):
    groups=defaultdict(lambda:[0,0])
    for mask,seed,states in rows:
        k=tuple(x for state in states[:idx+1] for x in state)
        groups[k][0]+=1
        groups[k][1]+=0 if alias else int(sum(mask)>=2)
    risk=sum((Q(s*(n-s),n) for n,s in groups.values()),Q(0))/len(rows)
    return str(risk),len(groups),sum(0<s<n for n,s in groups.values()),max(n for n,s in groups.values())

def main():
    folder=Path(sys.argv[1]) if len(sys.argv)>1 else Path('.')
    csvpath=folder/'R255_S51_SOURCE_RECONSTRUCTION_2026-10-29.csv'
    receipt=json.loads((folder/'R255_S51_EXACT_RECEIPT_2026-10-29.json').read_text())
    rows=[]
    for mask in itertools.product((0,1),repeat=3):
        for seed in itertools.product((0,1),repeat=3):
            rows.append((mask,seed,tuple(path_opinion(mask,seed,n) for n in range(4))))
    assert len(rows)==64
    by_key={(mask,seed):states for mask,seed,states in rows}
    with csvpath.open(newline='',encoding='utf-8') as f:
        source=list(csv.DictReader(f))
    assert len(source)==512
    keys=set()
    field_checks=0
    for row in source:
        bits=tuple(int(v) for v in row['edge_bits'])
        seed=tuple(int(v) for v in row['seed_bits'])
        mask=tuple(int(v) for v in row['reported_edge_mask'])
        assert len(bits)==6 and len(seed)==3 and len(mask)==3
        assert (bits,seed) not in keys
        keys.add((bits,seed))
        assert mask==tuple(1-bits[2*i] for i in range(3))
        assert row['mass']=='1/512'
        states=by_key[mask,seed]
        for n in range(4):
            actual=tuple(Q(v) for v in row[f'x{n}'].split(';'))
            assert actual==states[n]
            field_checks+=3
        assert int(row['ER_observed_connected'])==int(sum(mask)>=2)
        assert int(row['ALIAS_true_connected'])==0
    assert len(keys)==512
    assert receipt['reconstructed_csv_sha256']==hashlib.sha256(csvpath.read_bytes()).hexdigest()
    checks=0
    for world in WORLDS:
        alias=world==WORLDS[1]
        prev=None
        for n in range(4):
            risk,ngroups,mixed,maxsize=risk_group(rows,n,alias)
            entry=receipt['risk_by_world'][world]
            assert risk==entry[f'F{n}']
            details=entry['group_details'][f'F{n}']
            assert (ngroups,mixed,maxsize*8)==(details['groups'],details['mixed_label_groups'],details['max_group_size'])
            assert risk==details['risk']
            checks+=4
            if prev is not None:
                assert Q(prev)>=Q(risk)
            prev=risk
    assert receipt['risk_by_world'][WORLDS[0]]['F0']=='1/4'
    assert receipt['risk_by_world'][WORLDS[1]]['F3']=='0'
    assert receipt['risk_by_world'][WORLDS[0]]['leak_target_risk']=='0'
    mutated=json.loads(json.dumps(receipt))
    mutated['risk_by_world'][WORLDS[0]]['F2']='999'
    assert str(risk_group(rows,2,False)[0])!=mutated['risk_by_world'][WORLDS[0]]['F2']
    print(json.dumps({'status':'INTERNAL_INDEPENDENT_PATH_ORACLE_PASS','distinct_mask_seed_cases':64,
                      'source_rows_verified':512,'opinion_coordinates_verified':field_checks,
                      'risk_and_group_fields_verified':checks,'mutation_rejected':True,
                      'observed_connectivity_risks':[risk_group(rows,n,False)[0] for n in range(4)]}))

if __name__=='__main__':main()
