#!/usr/bin/env python3
"""R262 S58: exact conditional Brier risks on 7-cell periodic elementary CA."""
import argparse,csv,hashlib,itertools,json
from collections import defaultdict
from fractions import Fraction as Q
from pathlib import Path
RULES={'ABSORB_ZERO':0,'ABSORB_ONE':255,'IDENTITY':204,'SHIFT_RIGHT':170,'SHIFT_LEFT':240,'XOR_NEIGHBORS':90,'XOR_THREE':150,'RULE30':30,'RULE110':110}
FEATURES=('F0','F1','F01','Ffull')
TARGETS=('Y_cell','Y_macro')
ORIGINAL_SHA='6bc81d5ae6aae67d8f0b271b6baa02240439a3bf87313a6b812a2e51bdae6adb'
FREEZE='9822be38814185583f63bfd42bca4d984741715f'
def step(state,rule):
    return tuple((rule >> (4*state[(i-1)%7]+2*state[i]+state[(i+1)%7]))&1 for i in range(7))
def samples(world):
    rule=RULES[world]
    for x0 in itertools.product((0,1),repeat=7):
        x1=step(x0,rule);x2=step(x1,rule)
        yield (x0,x1,x2)
def key(feature,x0,x1):
    if feature=='F0':return ()
    if feature=='F1':return (sum(x1),)
    if feature=='F01':return (sum(x0),sum(x1))
    if feature=='Ffull':return x1
    raise ValueError(feature)
def risk(rows,target,feature):
    groups=defaultdict(lambda:[0,0])
    for x0,x1,x2 in rows:
        y=x2[0] if target=='Y_cell' else int(sum(x2)>=4)
        g=groups[key(feature,x0,x1)];g[0]+=y;g[1]+=1
    return sum((Q(pos*(n-pos),128*n) for pos,n in groups.values()),Q(0)),len(groups)
def audit_original_csv(path):
    b=Path(path).read_bytes()
    if hashlib.sha256(b).hexdigest()!=ORIGINAL_SHA:raise ValueError('original CSV sha256 mismatch')
    seen=set();counts={w:0 for w in RULES}
    with Path(path).open(newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            w=row['world'];n=int(row['observed_time_index_n'])
            if w not in RULES or n not in range(5):raise ValueError('unknown world or time')
            x0=tuple(int(row[f'original_initial_cell_bit_{i}']) for i in range(7))
            if any(v not in (0,1) for v in x0):raise ValueError('invalid initial bit')
            identity=(w,x0,n)
            if identity in seen:raise ValueError('duplicate source')
            seen.add(identity);counts[w]+=1
            x=x0
            for _ in range(n):x=step(x,RULES[w])
            if int(row['frozen_Wolfram_rule_decimal'])!=RULES[w] or any(int(row[f'observed_cell_state_{i}_at_time'])!=x[i] for i in range(7)) or int(row['observed_number_cells_in_state_1'])!=sum(x) or int(row['observed_global_state_parity'])!=sum(x)%2 or row['original_complete_initial_and_time_design_mass']!='1/640':raise ValueError('source state mismatch')
    if len(seen)!=5760 or any(v!=640 for v in counts.values()):raise ValueError('incomplete original source')
    return {'rows_checked':5760,'cell_values_checked':40320,'source_sha256':ORIGINAL_SHA}
def compute():
    results=[]
    for w in RULES:
        rows=list(samples(w));assert len(rows)==128
        for target in TARGETS:
            vals=[]
            for feat in FEATURES:
                r,n=risk(rows,target,feat)
                results.append({'world':w,'target':target,'feature':feat,'risk':str(r),'groups':n})
                vals.append(r)
            if not(vals[0]>=vals[1]>=vals[2]>=vals[3]==0):raise AssertionError('nested Brier inequality')
    assert len(results)==72
    return {'research_id':'R262','supplement':'S58','freeze_commit':FREEZE,'evidence':'E1_ARTIFICIAL','original_initials_per_world':128,'targets':list(TARGETS),'features':list(FEATURES),'risk_rows':results,'new_E2':0,'new_E3':0,'external_independent_replications':0,'R073':'FROZEN','PESEN_v0_1':'FROZEN'}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--csv');ap.add_argument('--out');a=ap.parse_args()
    z=compute();z['original_csv_audit']=audit_original_csv(a.csv) if a.csv else {'status':'NOT_RUN','reason':'original CSV bytes unavailable locally'}
    data=json.dumps(z,ensure_ascii=False,indent=2)+'\n'
    if a.out:Path(a.out).write_text(data,encoding='utf-8')
    print('risk_rows=',len(z['risk_rows']),'original_csv_audit=',z['original_csv_audit'].get('status','PASS'))
