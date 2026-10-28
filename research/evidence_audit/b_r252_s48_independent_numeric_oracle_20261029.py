#!/usr/bin/env python3
"""Independent numeric oracle for R252 S48, Python 3.10+ standard library.
Usage: python b_r252_s48_independent_numeric_oracle.py --receipt path/to/receipt.json
Reconstructs all 576 frozen artificial source atoms from separate formulas.
"""
import argparse,itertools,json,math
from collections import Counter
from pathlib import Path

W=('INDEPENDENT_BITS','DIRECT_COPY','HIDDEN_COMMON_CAUSE_ALIAS','XOR_SYNERGY','ERASURE_HALF','BINARY_SYMMETRIC_QUARTER','COLLIDER_AND','XOR_MASK_REPARAM','CONSTANT_REPORTER')

def observation(w,bits):
    u,a,b,c,d,e=bits
    if w=='INDEPENDENT_BITS':return a,b,c
    if w in ('DIRECT_COPY','HIDDEN_COMMON_CAUSE_ALIAS'):return a,a,c
    if w=='XOR_SYNERGY':return a,b,a^b
    if w=='ERASURE_HALF':return a,(a if c else 2),c
    if w=='BINARY_SYMMETRIC_QUARTER':return a,a^(b&c),b
    if w=='COLLIDER_AND':return a,b,a&b
    if w=='XOR_MASK_REPARAM':return a,a^b,b
    if w=='CONSTANT_REPORTER':return a,0,c
    raise AssertionError('unfrozen world')

def order(rep):
    state=(0x51A80000+7919*rep)%4294967296
    idx=list(range(64))
    for k in reversed(range(1,64)):
        state^=(state<<13)&0xffffffff
        state^=(state>>17)
        state^=(state<<5)&0xffffffff
        state&=0xffffffff
        partner=state%(k+1)
        idx[k],idx[partner]=idx[partner],idx[k]
    return idx

def entropy(obs,axes):
    counts=Counter(tuple(x[k] for k in axes) for x in obs)
    n=len(obs)
    return -sum((c/n)*math.log2(c/n) for c in counts.values())

def values(obs):
    hx=entropy(obs,(0,));hy=entropy(obs,(1,));hz=entropy(obs,(2,))
    hxy=entropy(obs,(0,1));hxz=entropy(obs,(0,2));hyz=entropy(obs,(1,2));hxyz=entropy(obs,(0,1,2))
    return {'H_Y':hy,'I_XY':hx+hy-hxy,
            'I_XY_given_Z':hxz+hyz-hz-hxyz,'H_Y_given_XZ':hxyz-hxz}

def audit(receipt):
    r=json.loads(Path(receipt).read_text(encoding='utf8'))
    assert r['n_records']==288
    assert r['prescore_protocol_commit']=='c57653fe521b9c2bad4da8fce95fa794050e320a'
    rows={(z['world'],z['replicate'],z['n']):z for z in r['records']}
    assert len(rows)==288
    source_bits=list(itertools.product((0,1),repeat=6))
    comparisons=0
    for rep in range(8):
        idx=order(rep)
        for n in (8,16,32,64):
            for w in W:
                rec=rows[(w,rep,n)]
                assert rec['source_indices']==idx[:n]
                sample=[observation(w,source_bits[i]) for i in idx[:n]]
                counts={','.join(map(str,k)):v for k,v in Counter(sample).items()}
                assert counts==rec['xyz_integer_counts']
                for key,val in values(sample).items():
                    assert abs(val-rec['metrics'][key]['approx_bits'])<1e-10,(w,rep,n,key,val)
                    comparisons+=1
    mutant=json.loads(json.dumps(r))
    for item in mutant['records']:
        if item['world']=='INDEPENDENT_BITS' and item['n']==64:
            item['metrics']['I_XY']['approx_bits']=999
            break
    changed={(z['world'],z['replicate'],z['n']):z for z in mutant['records']}
    try:
        obs=[observation('INDEPENDENT_BITS',source_bits[i]) for i in order(0)]
        assert abs(values(obs)['I_XY']-changed[('INDEPENDENT_BITS',0,64)]['metrics']['I_XY']['approx_bits'])<1e-10
        raise RuntimeError('mutant accepted')
    except AssertionError:pass
    print(json.dumps({'audit':'B_R252_S48','records_checked':len(rows),
      'independent_numeric_metric_comparisons':comparisons,
      'integer_count_and_source_index_checks':len(rows)*2,
      'mutant_rejected':True,'external_independent_replication':False}))

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--receipt',required=True)
    audit(p.parse_args().receipt)
