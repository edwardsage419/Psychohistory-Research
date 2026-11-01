"""Nonblind, reproducible optimized-mode R334 regression and strict-gate controls.

The pinned original is read only. All mutations occur in a temporary directory.
Run from the repository: python research/evidence_audit/test_r334_optimized_gate_20261101.py
"""
from __future__ import annotations
import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SOURCE_NAME = 'r334_dissonance.py'
CSV_NAME = 'R334_ALL_48_ARTIFICIAL_CONTRAST_ATOMS.csv'
JSON_NAME = 'R334_EXACT_16_CONDITIONS.json'
EXPECTED = {'source': '7d232a07d9d2979c2fcc8a407dd8bda18cd8ab93',
            'csv': '6e3bdcc5ca07d1321a651c29b899798a32f7fb72',
            'json': '02883b6b9cfc22b3b855d8a7cbaa5e5ddf6bd86c'}

def git_blob(data: bytes) -> str:
    import hashlib
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def execute(args: list[str]) -> dict:
    result = subprocess.run(args, text=True, capture_output=True, timeout=20)
    return {'exit': result.returncode,
            'original_claims_pass': 'R334 PRODUCTION_REPLAY_PASS' in result.stdout,
            'strict_claims_pass': 'PASS_BOUNDED_E1_RECEIPT' in result.stdout,
            'unittest_reports_ok': '\nOK\n' in result.stderr}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,default=Path(__file__).resolve().parents[1]/'R334'/SOURCE_NAME)
    args=parser.parse_args()
    source=args.source
    gate=Path(__file__).with_name('r334_strict_receipt_gate_20261101.py')
    if git_blob(source.read_bytes()) != EXPECTED['source']:
        raise ValueError('original source Git blob identity mismatch')
    spec=importlib.util.spec_from_file_location('r334_pinned_source',source)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cb,jb=mod.render()
    if git_blob(cb)!=EXPECTED['csv'] or git_blob(jb)!=EXPECTED['json']:
        raise ValueError('generated original receipts differ from GitHub pinned blobs')
    out={'python':sys.version.split()[0], 'source_git_blob':EXPECTED['source'],
         'csv_git_blob':EXPECTED['csv'],'json_git_blob':EXPECTED['json'],
         'cases':{}}
    with tempfile.TemporaryDirectory(prefix='r334-optimized-gate-') as td:
        root=Path(td)
        script=root/SOURCE_NAME
        csv_file=root/CSV_NAME
        json_file=root/JSON_NAME
        for case in ('clean','csv_corrupt','json_corrupt','both_missing','source_corrupt'):
            shutil.copyfile(source,script)
            csv_file.write_bytes(cb)
            json_file.write_bytes(jb)
            if case=='csv_corrupt':
                csv_file.write_bytes(cb.replace(b'DISSONANCE',b'FAKE_DISSO',1))
            if case=='json_corrupt':
                json_file.write_bytes(jb.replace(b'R334_frozen_induced_compliance_v1',b'FORGED_schema_v1',1))
            if case=='both_missing':
                csv_file.unlink()
                json_file.unlink()
            if case=='source_corrupt':
                script.write_bytes(source.read_bytes()+b'\n')
            out['cases'][case]={}
            for mode,flags in [('normal',[]),('optimized',['-O'])]:
                orig=execute([sys.executable,*flags,str(script),'--test','--audit'])
                strict=execute([sys.executable,*flags,str(gate),'--root',str(root)])
                out['cases'][case][mode]={'original':orig,'strict':strict}
                if case=='clean':
                    if orig['exit']!=0 or strict['exit']!=0:
                        raise AssertionError((case,mode,orig,strict))
                else:
                    if strict['exit']!=1 or strict['strict_claims_pass']:
                        raise AssertionError(('strict false accept',case,mode,strict))
                    if case=='source_corrupt':
                        # Original CLI has no source identity gate; both modes may pass.
                        if orig['exit']!=0:
                            raise AssertionError((case,mode,orig))
                    elif mode=='normal':
                        if orig['exit']==0:
                            raise AssertionError(('original normal failed to reject',case))
                    elif orig['exit']!=0 or not orig['original_claims_pass'] or not orig['unittest_reports_ok']:
                        raise AssertionError(('original optimized unexpectedly rejected',case))
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':main()
