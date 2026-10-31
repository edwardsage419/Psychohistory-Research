#!/usr/bin/env python3
"""Nonblind original R301 S97 B-checker mutation audit using synthetic fixtures.
Requires the unmodified upstream B checker alongside this file. No personal data.
"""
import csv
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
from copy import deepcopy
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORIGINAL = ((HERE / 'b_r301_s97_independent_segmentation.py')
            if (HERE / 'b_r301_s97_independent_segmentation.py').exists()
            else (HERE.parent / 'evidence_audit' / 'b_r301_s97_independent_segmentation.py'))
EXPECTED_BLOB = '527193aa8cb747696a11b204c066bc07f22511b6'
FREEZE = 'b18d1cd4e149a60ebfe3732f38f09f1cb6d94e7a'
FIELDS = {'research_id':'R301','extension':'S97','freeze_commit':FREEZE,
          'external_team_replication':False,'history_length':4,'heldout_length':1,
          'source_atoms':288,'distinct_true_atoms':96}
CSV_NAME = 'R301_S97_ALL_288_HELDOUT_ATOMS.csv'
JSON_NAME = 'R301_S97_EXACT_HELDOUT_RESULTS.json'
RECEIPT_NAME = 'R301_S97_RECEIPT.json'

def git_blob_sha(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def load_original():
    data = ORIGINAL.read_bytes()
    assert git_blob_sha(data) == EXPECTED_BLOB, 'Original B source identity mismatch'
    spec = importlib.util.spec_from_file_location('original_b_r301_s97', ORIGINAL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def fixtures(b):
    rows=[]
    risks={(t,a):F(0) for t in b.H for a in b.H}
    for t in b.H:
        for a in b.H:
            for s in b.S:
                mass,p=b.oracle(t,s)
                _,q=b.oracle(a,s)
                for y in (0,1):
                    joint=mass*(p if y else 1-p)
                    loss=(q-y)**2
                    rows.append(dict(zip(b.COLS,map(str,(t,a,s,y,mass,p,q,joint,loss,joint*loss)))))
                    risks[t,a]+=joint*loss
    pairs=[]
    for t in b.H:
        for a in b.H:
            excess=sum((b.oracle(t,s)[0]*(b.oracle(a,s)[1]-b.oracle(t,s)[1])**2 for s in b.S),F(0))
            pairs.append(dict(true_hazard=str(t),assumed_hazard=str(a),risk=str(risks[t,a]),
                              oracle_risk=str(risks[t,t]),excess_risk=str(excess),
                              constant_half_baseline='1/4'))
    result={**FIELDS,'evidence':'E1_SYNTHETIC_ONLY','real_E2':0,'historical_E3':0,
            'pairs':pairs,'R073':'FROZEN','PESEN_v0_1':'FROZEN'}
    assert b.check(rows,result)
    return rows,result

def save(folder,rows,results,receipt_override=None):
    folder.mkdir(exist_ok=True,parents=True)
    with (folder/CSV_NAME).open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    (folder/JSON_NAME).write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    files={}
    for name in (CSV_NAME,JSON_NAME):
        data=(folder/name).read_bytes()
        files[name]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
    receipt={'freeze_commit':FREEZE,'files':files}
    if receipt_override:
        receipt_override(receipt)
    (folder/RECEIPT_NAME).write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf8')

def native_check(folder):
    p=subprocess.run([sys.executable,str(ORIGINAL),'--folder',str(folder)],
                     capture_output=True,text=True,timeout=45)
    return p.returncode,p.stdout.strip(),p.stderr.strip()

def main():
    b=load_original()
    rows,result=fixtures(b)
    observed={'original_checker_blob':EXPECTED_BLOB,'fixture_rows':len(rows),
              'fixture_pairs':len(result['pairs']),'baseline':None,'false_accept':[],
              'correct_reject':[]}
    with tempfile.TemporaryDirectory() as temp:
        folder=Path(temp)
        save(folder,rows,result)
        code,out,err=native_check(folder)
        assert code==0 and '"audit": "PASS"' in out, (code,out,err)
        observed['baseline']='PASS'
        for key,value in FIELDS.items():
            for mode in ('delete','mutate'):
                altered=deepcopy(result)
                if mode=='delete':del altered[key]
                else:altered[key]='wrong' if isinstance(value,str) else (not value if isinstance(value,bool) else value+1)
                save(folder,rows,altered)
                code,out,err=native_check(folder)
                assert code==0 and '"audit": "PASS"' in out, (key,mode,code,err)
                observed['false_accept'].append(f'results.{key}:{mode}')
        for mode in ('delete','mutate'):
            def alter_receipt(rec):
                if mode=='delete':del rec['freeze_commit']
                else:rec['freeze_commit']='wrong'
            save(folder,rows,result,alter_receipt)
            code,out,err=native_check(folder)
            assert code==0 and '"audit": "PASS"' in out, (mode,code,err)
            observed['false_accept'].append('receipt.freeze_commit:'+mode)
        for name in (CSV_NAME,JSON_NAME):
            def omit(rec):del rec['files'][name]
            save(folder,rows,result,omit)
            code,out,err=native_check(folder)
            assert code==0 and '"audit": "PASS"' in out, (name,code,err)
            observed['false_accept'].append('receipt.files.omit:'+name)
        for key,value in (('real_E2',1),('evidence','E2_REAL')):
            altered=deepcopy(result);altered[key]=value
            save(folder,rows,altered)
            code,out,err=native_check(folder)
            assert code!=0,(key,code,out)
            observed['correct_reject'].append(key)
        altered=deepcopy(rows)
        altered[0]['joint_mass']='0'
        save(folder,altered,result)
        code,out,err=native_check(folder)
        assert code!=0,(code,out)
        observed['correct_reject'].append('row.joint_mass')
    observed['native_runs']=1+len(observed['false_accept'])+len(observed['correct_reject'])
    print(json.dumps(observed,ensure_ascii=False,indent=2))
    assert observed['native_runs']==24
    assert len(observed['false_accept'])==20
    assert len(observed['correct_reject'])==3

if __name__=='__main__':main()
