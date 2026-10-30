#!/usr/bin/env python3
"""Nonblind synthetic fixture against original archived B checker. Run in repository root."""
import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
from fractions import Fraction as Q
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'research/evidence_audit/b_r290_s86_independent_binomial_oracle_20261030.py'
spec = importlib.util.spec_from_file_location('archived_b_s86', SRC)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

rows = []
for name in mod.DISTRIBUTIONS:
    for pi in (Q(1,2), Q(3,4)):
        for fp,fn in ((1,1),(1,3)):
            for m in (1,2):
                risk=mod.expected_risk(name,pi,fp,fn,m)
                rows.append(dict(world=f'{name}_PI{pi.numerator}of{pi.denominator}_FP{fp}_FN{fn}',
                    m=m,sources=5**(2*m),training_mass='1',expected_heldout_risk=str(risk),
                    oracle_risk=str(risk),regret='0'))
base=dict(evidence='E1_ARTIFICIAL_ONLY',new_E2=0,new_E3=0,R073='FROZEN',PESEN='FROZEN',results=rows)
assert mod.verify(base)==24

def verdict(doc,optimized):
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'fixture.json'
        path.write_text(json.dumps(doc),encoding='utf-8')
        code="import importlib.util,json,sys; s=importlib.util.spec_from_file_location('b',sys.argv[1]); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); m.verify(json.load(open(sys.argv[2])))"
        cp=subprocess.run([sys.executable]+(['-O'] if optimized else [])+
            ['-c',code,str(SRC),str(path)],capture_output=True,text=True)
        return cp.returncode==0

cases={}
for label,edit in (
    ('evidence_E2',lambda d:d.__setitem__('evidence','E2_HUMAN')),
    ('new_E2_1',lambda d:d.__setitem__('new_E2',1)),
    ('R073_unfrozen',lambda d:d.__setitem__('R073','UNFROZEN')),
    ('PESEN_unfrozen',lambda d:d.__setitem__('PESEN','UNFROZEN')),
):
    d=copy.deepcopy(base);edit(d)
    cases[label]={'normal_accept':verdict(d,False),'optimized_accept':verdict(d,True)}
    assert cases[label]=={'normal_accept':False,'optimized_accept':True}

d=copy.deepcopy(base)
d['results'][0]['oracle_risk']='0'
d['results'][0]['regret']=d['results'][0]['expected_heldout_risk']
cases['oracle_and_regret_joint_tamper']={'normal_accept':verdict(d,False)}
assert cases['oracle_and_regret_joint_tamper']['normal_accept']

d=copy.deepcopy(base)
pi=Q(1,3);m=1;r=mod.expected_risk('MONOTONE',pi,1,1,m)
d['results'][0]=dict(world='MONOTONE_PI1of3_FP1_FN1',m=m,sources=25,training_mass='1',
    expected_heldout_risk=str(r),oracle_risk=str(r),regret='0')
cases['noncanonical_world_replaces_canonical']={'normal_accept':verdict(d,False)}
assert cases['noncanonical_world_replaces_canonical']['normal_accept']
print(json.dumps({'status':'PASS','original_B_blob':'5f1cf8e8299cfff0276b2bbee3d3af69ef0eb869',
    'fixture':'synthetic 24 rows, NOT persisted S86','assertions':12,'cases':cases},indent=2))
