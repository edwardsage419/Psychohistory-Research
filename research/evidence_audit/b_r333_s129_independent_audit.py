#!/usr/bin/env python3
"""Independent nonblind exact Boolean audit of R333 S129 and R333 legacy bytes."""
import csv
import hashlib
import io
import json
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / 'validation'
CSV_NAME = 'R333_S129_ALL_320_TIMED_TRIADIC_STATES.csv'
JSON_NAME = 'R333_S129_EXACT_64_TIMED_TRIADIC_WORLDS.json'
FIELDS = ('mechanism','initial_p','initial_b','initial_e','do_b','intervention_time','time','p','b','e')


def path_states(mechanism, p, b, e, intervention, tau):
    path = [(p,b,e)]
    for time in range(1,5):
        next_p = p ^ e
        next_e = (b ^ e) if mechanism == 'cyclic' else e
        next_b = intervention if time == tau else (p ^ b)
        p,b,e = next_p,next_b,next_e
        path.append((p,b,e))
    return path


def generated():
    rows, worlds = [], []
    for mechanism in ('cyclic','feedforward'):
        for p,b,e in product((0,1), repeat=3):
            for intervention in (0,1):
                for tau in (1,2):
                    states = path_states(mechanism,p,b,e,intervention,tau)
                    for time,(P,B,E) in enumerate(states):
                        rows.append(dict(zip(FIELDS,map(str,(mechanism,p,b,e,intervention,tau,time,P,B,E)))))
                    worlds.append(dict(mechanism=mechanism,initial_p=p,initial_b=b,initial_e=e,do_b=intervention,intervention_time=tau,final_p=states[4][0],final_b=states[4][1],final_e=states[4][2]))
    return rows,worlds


def audit(csv_text,json_text):
    reader = csv.DictReader(io.StringIO(csv_text))
    if tuple(reader.fieldnames or ()) != FIELDS:
        raise ValueError('field mismatch')
    actual = list(reader)
    if len(actual) != 320:
        raise ValueError('row count')
    data = json.loads(json_text)
    if set(data) != {'model','source_row_count','world_count','worlds'} or data['model'] != 'R333_S129_TIMED_INTERVENTION_E1' or data['source_row_count'] != 320 or data['world_count'] != 64:
        raise ValueError('identity or evidence tier')
    if len(data['worlds']) != 64:
        raise ValueError('world count')
    rows, worlds = generated()
    if actual != rows:
        raise ValueError('row values/order')
    if data['worlds'] != worlds:
        raise ValueError('world values/order')
    return worlds


def controls(csv_text,json_text):
    lines = csv_text.splitlines(keepends=True)
    variants = [('deleted_row',''.join(lines[:2]+lines[3:]),json_text),('duplicate_row',''.join(lines[:2]+[lines[1]]+lines[2:]),json_text)]
    variants.append(('wrong_timing',csv_text.replace('cyclic,0,0,0,0,1,1,0,0,0','cyclic,0,0,0,0,2,1,0,0,0',1),json_text))
    variants.append(('state_flip',csv_text.replace('cyclic,0,0,0,1,1,1,0,1,0','cyclic,0,0,0,1,1,1,0,0,0',1),json_text))
    data=json.loads(json_text);data['worlds'][0]['final_e']^=1
    variants.append(('world_flip',csv_text,json.dumps(data)))
    data=json.loads(json_text);data['model']='E2_HUMAN'
    variants.append(('evidence_upgrade',csv_text,json.dumps(data)))
    for name,csv_v,json_v in variants:
        if csv_v==csv_text and json_v==json_text:
            raise ValueError('no-op mutation: '+name)
        try:
            audit(csv_v,json_v)
        except (ValueError,KeyError,TypeError):
            continue
        raise ValueError('mutation accepted: '+name)
    return len(variants)


def legacy_byte_identity():
    # Original R333's t=1 source serialization uses CRLF CSV and pretty JSON.
    legacy_rows,legacy_worlds=[],[]
    for mechanism in ('cyclic','feedforward'):
        for p,b,e in product((0,1),repeat=3):
            for intervention in (0,1):
                seq=path_states(mechanism,p,b,e,intervention,1)
                for time,(P,B,E) in enumerate(seq):
                    legacy_rows.append([mechanism,p,b,e,intervention,time,P,B,E])
                legacy_worlds.append(dict(mechanism=mechanism,initial_p=p,initial_b=b,initial_e=e,do_b1=intervention,final_p=seq[4][0],final_b=seq[4][1],final_e=seq[4][2]))
    checks=dict(equal_b1=0,different_p2=0,different_b3=0,cyclic_e2_do=0,feedforward_e2_do=0)
    for p,b,e in product((0,1),repeat=3):
        c0=path_states('cyclic',p,b,e,0,1);c1=path_states('cyclic',p,b,e,1,1)
        f0=path_states('feedforward',p,b,e,0,1);f1=path_states('feedforward',p,b,e,1,1)
        checks['cyclic_e2_do']+=c0[2][2]!=c1[2][2]
        checks['feedforward_e2_do']+=f0[2][2]!=f1[2][2]
        for c,f in ((c0,f0),(c1,f1)):
            checks['equal_b1']+=c[1][1]==f[1][1]
            checks['different_p2']+=c[2][0]!=f[2][0]
            checks['different_b3']+=c[3][1]!=f[3][1]
    s=io.StringIO(newline='');w=csv.writer(s,lineterminator='\r\n');w.writerow(['mechanism','initial_p','initial_b','initial_e','do_b1','time','p','b','e']);w.writerows(legacy_rows)
    c=s.getvalue().encode()
    j=(json.dumps(dict(schema='R333_frozen_triads_v1',worlds=legacy_worlds,checks=checks),indent=2,ensure_ascii=False)+'\n').encode()
    def blob(x):return hashlib.sha1(b'blob '+str(len(x)).encode()+b'\0'+x).hexdigest()
    if blob(c)!='8a202f773badb8833992ff0df25c3c90f60b3680' or blob(j)!='dd82e1f616528742622ebafc844ec66adadf18b5':
        raise ValueError('legacy byte identity')


if __name__=='__main__':
    csv_text=(ROOT/CSV_NAME).read_text(encoding='utf-8')
    json_text=(ROOT/JSON_NAME).read_text(encoding='utf-8')
    worlds=audit(csv_text,json_text)
    n=controls(csv_text,json_text)
    legacy_byte_identity()
    print(f'PASS_NONBLIND_INTERNAL_E1: {len(worlds)} worlds, 320 rows, {n} mutations rejected, legacy R333 byte identities PASS')
