#!/usr/bin/env python3
"""R255 S51 exact finite E1 connectivity inference from opinion prefixes.

Reconstructs the two pre-frozen R255 p=1/2 artificial worlds from their
six edge bits and three seed bits. Does not claim a full original CSV audit.
"""
import csv
import hashlib
import itertools
import json
import sys
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path

WORLDS = ('ER_TRIANGLE_P_HALF', 'STATIC_EMPTY_TRUE_GRAPH_OBS_REPORT_HALF')
EDGES = ((0, 1), (0, 2), (1, 2))

def fstr(v):
    return str(v)

def evolve(bits, seed):
    edge = tuple(int(2 * bits[2*i] + bits[2*i+1] < 2) for i in range(3))
    a = [[Q(0) for _ in range(3)] for _ in range(3)]
    for opened, (i, j) in zip(edge, EDGES):
        if opened:
            a[i][j] = a[j][i] = Q(1, 4)
    for i in range(3):
        a[i][i] = 1 - sum(a[i][j] for j in range(3) if i != j)
    x = tuple(Q(v) for v in seed)
    path = [x]
    for _ in range(3):
        x = tuple(sum((a[i][j] * x[j] for j in range(3)), Q(0)) for i in range(3))
        path.append(x)
    return edge, tuple(path)

def calc(rows, world):
    out = {}
    group_details = {}
    for horizon in range(4):
        groups = defaultdict(lambda: [0, 0])
        for row in rows:
            key = tuple(v for state in row['states'][:horizon+1] for v in state)
            groups[key][0] += 1
            groups[key][1] += row['targets'][world]
        assert sum(n for n, s in groups.values()) == 512
        risk = sum((Q(s*(n-s), n) for n, s in groups.values()), Q(0)) / 512
        out[f'F{horizon}'] = fstr(risk)
        group_details[f'F{horizon}'] = {'groups':len(groups), 'mixed_label_groups':sum(0<s<n for n,s in groups.values()), 'max_group_size':max(n for n,s in groups.values()), 'risk':fstr(risk)}
    risk = [Q(out[f'F{i}']) for i in range(4)]
    assert all(risk[i] >= risk[i+1] for i in range(3))
    assert (risk[0] == Q(1,4)) if world == WORLDS[0] else (all(v == 0 for v in risk))
    out['improvements'] = [fstr(risk[i]-risk[i+1]) for i in range(3)]
    out['group_details'] = group_details
    out['leak_target_risk'] = '0'
    return out

def main():
    output = Path(sys.argv[1]) if len(sys.argv)>1 else Path('.')
    output.mkdir(parents=True, exist_ok=True)
    rows=[]
    for bits in itertools.product((0,1),repeat=6):
        for seed in itertools.product((0,1),repeat=3):
            edge,states = evolve(bits,seed)
            rows.append({'bits':bits,'seed':seed,'edge':edge,'states':states,
                         'targets':{WORLDS[0]:int(sum(edge)>=2),WORLDS[1]:0}})
    assert len(rows)==512 and len({(r['bits'],r['seed']) for r in rows})==512
    assert sum(r['targets'][WORLDS[0]] for r in rows)==256
    receipt={'study':'R255_S51','scope':'FINITE_ARTIFICIAL_E1','frozen_worlds':list(WORLDS),
             'source_combinations_per_world':512,'source_mass_per_world':'1',
             'source_reconstruction':'FROZEN_SIX_BITS_SEEDS_ONLY_NOT_FULL_ORIGINAL_CSV',
             'risk_by_world':{w:calc(rows,w) for w in WORLDS},
             'observed_paths_equal_across_worlds':True,
             'real_connected_positive_count':256,'alias_true_connected_positive_count':0,
             'E2_human':0,'E3_historical':0,'external_replication':0,
             'R073':'FROZEN','PESEN_v0_1':'FROZEN'}
    p=output/'R255_S51_SOURCE_RECONSTRUCTION_2026-10-29.csv'
    cols=['edge_bits','seed_bits','reported_edge_mask','x0','x1','x2','x3','ER_observed_connected','ALIAS_true_connected','mass']
    with p.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=cols,lineterminator='\n');writer.writeheader()
        for r in rows:
            writer.writerow({'edge_bits':''.join(map(str,r['bits'])),'seed_bits':''.join(map(str,r['seed'])),
                             'reported_edge_mask':''.join(map(str,r['edge'])),
                             **{f'x{i}':';'.join(map(str,r['states'][i])) for i in range(4)},
                             'ER_observed_connected':r['targets'][WORLDS[0]],
                             'ALIAS_true_connected':0,'mass':'1/512'})
    receipt['reconstructed_csv_sha256']=hashlib.sha256(p.read_bytes()).hexdigest()
    q=output/'R255_S51_EXACT_RECEIPT_2026-10-29.json'
    q.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print(json.dumps({'receipt':str(q),'csv':str(p),'csv_sha256':receipt['reconstructed_csv_sha256'],
                      'ER_risks':{k:v for k,v in receipt['risk_by_world'][WORLDS[0]].items() if k.startswith('F')},
                      'ALIAS_risks':{k:v for k,v in receipt['risk_by_world'][WORLDS[1]].items() if k.startswith('F')}}))

if __name__=='__main__':main()
