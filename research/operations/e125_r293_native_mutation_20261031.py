#!/usr/bin/env python3
"""E125: Native Python test of pinned original R293 S89 checker with synthetic fixtures.
Run in directory containing the exact archived B checker file. Standard library only.
No original persisted R293 files are modified or claimed replayed.
"""
from __future__ import annotations
import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from fractions import Fraction as Q

ROOT=Path(__file__).resolve().parent
CHECKER=ROOT/'b_r293_s89_independent_linear_audit_20261030.py'
EXPECTED_BLOB='691b93b2835477b140cbcea7258547b8c89ad736'

def main():
    import hashlib
    raw=CHECKER.read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert blob==EXPECTED_BLOB, (blob,EXPECTED_BLOB)
    spec=importlib.util.spec_from_file_location('r293_b_original',CHECKER)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    rows=[]
    for mode in mod.MODES:
        n=10 if mode=='INDEPENDENT' else 5
        for style in mod.STYLES:
            for k in range(2**n):
                bits=format(k,f'0{n}b')
                b=tuple(map(int,bits))
                latent=b if n==10 else b+tuple(1-x for x in b)
                shift=2*b[0] if style=='ANCHOR_PLUS' else 2*(1-b[0])
                raw_scores=tuple(x+shift for x in latent)
                centered=tuple(Q(x)-Q(sum(raw_scores),10) for x in raw_scores)
                rows.append(dict(zip(mod.FIELDS,(
                    mode,style,bits,str(Q(1,2**n)),str(shift),
                    ';'.join(map(str,latent)),
                    ';'.join(map(str,raw_scores)),
                    ';'.join(map(str,centered))))))
    worlds=[]
    for mode in mod.MODES:
        for style in mod.STYLES:
            worlds.append(dict(mode=mode,mechanism=style,source_rows=2**(10 if mode=='INDEPENDENT' else 5),source_mass='1',**mod.analytical(mode,style)))
    result=dict(research_id='R293',increment='S89',freeze_commit=mod.FREEZE,
                scope='SYNTHETIC_E1_ENDOGENOUS_SHARED_STYLE_NOT_HUMAN_ESS_PVQ21',
                original_R293_baseline='CLOSED_BOUNDED_E1_UNCHANGED',
                new_source_rows=2112,new_human_E2=0,new_historical_E3=0,
                empirical_circle_validated=False,R073='FROZEN',PESEN_v0_1='FROZEN',worlds=worlds)
    original=dict(worlds=[dict(mode=mode,centered_covariance=mod.analytical(mode,'ANCHOR_PLUS')['centered_covariance']) for mode in mod.MODES])
    assert mod.validate(rows,result,original)['covariance_entries_checked']==800
    def command(src,js,orig):
        return subprocess.run([sys.executable,str(CHECKER),'--check','--csv',str(src),'--json',str(js),'--original',str(orig)],capture_output=True,text=True)
    with tempfile.TemporaryDirectory() as d:
        d=Path(d)
        src,js,baseline=d/'source.csv',d/'result.json',d/'original.json'
        with src.open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=mod.FIELDS);writer.writeheader();writer.writerows(rows)
        js.write_text(json.dumps(result),encoding='utf-8')
        baseline.write_text(json.dumps(original),encoding='utf-8')
        good=command(src,js,baseline)
        assert good.returncode==0,good.stderr
        changed=dict(result,research_id='FALSE_R999',scope='FALSE_HUMAN_E2')
        js.write_text(json.dumps(changed),encoding='utf-8')
        metadata=command(src,js,baseline)
        assert metadata.returncode==0,metadata.stderr
        for field in ('research_id','scope'):
            mutated=dict(result);mutated.pop(field)
            js.write_text(json.dumps(mutated),encoding='utf-8')
            assert command(src,js,baseline).returncode==0,field
        js.write_text(json.dumps(result),encoding='utf-8')
        wrong=dict(original)
        wrong['worlds']=[dict(w) for w in original['worlds']]
        wrong['worlds'][0]['centered_covariance']=[list(r) for r in wrong['worlds'][0]['centered_covariance']]
        wrong['worlds'][0]['centered_covariance'][0][0]='999'
        baseline.write_text(json.dumps(wrong),encoding='utf-8')
        bad=command(src,js,baseline)
        assert bad.returncode!=0,bad.stdout
        absent=command(src,js,d/'does_not_exist.json')
        assert absent.returncode==0,absent.stderr
        inflated=dict(result,new_human_E2=1)
        js.write_text(json.dumps(inflated),encoding='utf-8')
        assert command(src,js,d/'does_not_exist.json').returncode!=0
        print(json.dumps({'source_blob_verified':blob,'fixture_origin':'generated_exact_2112_synthetic_rows_not_persisted_csv',
                          'normal_exit':good.returncode,'wrong_baseline_exit':bad.returncode,
                          'missing_baseline_exit':absent.returncode,
                          'wrong_two_metadata_exit':metadata.returncode,
                          'two_metadata_deletions_accepted':2,'inflated_E2_rejected':True,
                          'worlds':4,'source_rows':2112,'covariance_cells':800,
                          'native_subprocesses':7},indent=2))

if __name__=='__main__':main()
