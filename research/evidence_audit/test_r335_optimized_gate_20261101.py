"""Pinned R335 native false acceptance and independent strict-gate regression.

Only temporary copies are changed. Run from a checkout with the frozen R335
source and both receipts, or use --source to point to that exact source.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SOURCE_BLOB='9c005079716fe38eb4cb6d99730884a55e2795a3'
CSV_BLOB='f5987d4d9da8ef7532a3615b5f7fb6efbd4701cb'
JSON_BLOB='4ab8f69cbd483099dd2a1be28cb052e1e3bdb279'
CSV_NAME='R335_ALL_384_ARTIFICIAL_GROUP_ATOMS.csv'
JSON_NAME='R335_EXACT_128_CONDITIONS.json'


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def run(args: list[str]) -> dict:
    result=subprocess.run(args,capture_output=True,text=True,timeout=30)
    return {'exit':result.returncode,
            'pass_claim':'R335 PRODUCTION_REPLAY_PASS' in result.stdout,
            'strict_claim':'PASS_BOUNDED_E1_RECEIPT' in result.stdout,
            'unit_ok':'\nOK\n' in result.stderr}


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,default=Path(__file__).resolve().parents[1]/'R335'/'r335_groupthink.py')
    args=parser.parse_args()
    source=args.source
    gate=Path(__file__).with_name('r335_strict_receipt_gate_20261101.py')
    if git_blob(source.read_bytes())!=SOURCE_BLOB:
        raise ValueError('R335 source blob mismatch')
    spec=importlib.util.spec_from_file_location('pinned_r335',source)
    mod=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    cb,jb=mod.render()
    if git_blob(cb)!=CSV_BLOB or git_blob(jb)!=JSON_BLOB:
        raise ValueError('R335 original renderer failed to reproduce pinned receipt blobs')
    output={'python':sys.version.split()[0], 'source_git_blob':SOURCE_BLOB,
            'csv_git_blob':CSV_BLOB,'json_git_blob':JSON_BLOB,'cases':{}}
    with tempfile.TemporaryDirectory(prefix='r335-native-negative-') as temp:
        root=Path(temp)
        for case in ('clean','csv_corrupt','json_corrupt','both_missing','source_corrupt'):
            shutil.copyfile(source,root/source.name)
            (root/CSV_NAME).write_bytes(cb)
            (root/JSON_NAME).write_bytes(jb)
            if case=='csv_corrupt':
                (root/CSV_NAME).write_bytes(cb.replace(b'OPEN',b'FAKE',1))
            if case=='json_corrupt':
                (root/JSON_NAME).write_bytes(jb.replace(b'R335_frozen_public_unanimity_v1',b'FORGED_SCHEMA',1))
            if case=='both_missing':
                (root/CSV_NAME).unlink()
                (root/JSON_NAME).unlink()
            if case=='source_corrupt':
                (root/source.name).write_bytes(source.read_bytes()+b'\n')
            output['cases'][case]={}
            for mode,flags in [('normal',[]),('optimized',['-O'])]:
                original=run([sys.executable,*flags,str(root/source.name),'--test','--audit'])
                strict=run([sys.executable,*flags,str(gate),'--root',str(root)])
                output['cases'][case][mode]={'original':original,'strict':strict}
                if case=='clean':
                    if original['exit']!=0 or strict['exit']!=0:
                        raise ValueError(('clean failure',mode,original,strict))
                else:
                    if strict['exit']!=1 or strict['strict_claim']:
                        raise ValueError(('strict false acceptance',case,mode,strict))
                    if case=='source_corrupt':
                        if original['exit']!=0:
                            raise ValueError(('original source-only behavior',mode,original))
                    elif mode=='normal':
                        if original['exit']==0:
                            raise ValueError(('original normal false acceptance',case))
                    elif original['exit']!=0 or not original['pass_claim'] or not original['unit_ok']:
                        raise ValueError(('original optimized unexpectedly rejected',case,original))
    print(json.dumps(output,indent=2,sort_keys=True))


if __name__=='__main__':
    main()
