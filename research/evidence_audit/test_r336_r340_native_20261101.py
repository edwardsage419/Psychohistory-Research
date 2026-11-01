#!/usr/bin/env python3
"""Native original-vs-strict negative controls, isolated temporary copies."""
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

BASE=pathlib.Path(__file__).resolve().parent
GATE=BASE/'r336_r340_strict_receipt_gate_20261101.py'
MODELS={
 'R336': ('r336_inoculation.py','R336_ALL_96_ARTIFICIAL_ATTACK_ATOMS.csv','R336_EXACT_48_CONDITIONS.json'),
 'R340': ('r340_sis_generator.py','R340_ALL_48_ARTIFICIAL_GENERATOR_ATOMS.csv','R340_EXACT_3_GENERATORS.json'),
}
CASES=('valid','csv_corrupt','json_corrupt','missing_both','source_mutation')

def invoke(args):
    p=subprocess.run(args,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=30,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    return {'exit_code':p.returncode,'pass_token':('PRODUCTION_REPLAY_PASS' in p.stdout or 'PRODUCTION_BYTE_REPLAY=PASS' in p.stdout or 'STRICT_GATE_PASS' in p.stdout),'last_stdout':p.stdout.strip().splitlines()[-1:] ,'last_stderr':p.stderr.strip().splitlines()[-1:]}

def main():
    output={'python':sys.version.split()[0],'models':{},'cases':{},'source':'exact original Git blobs reconstructed from GitHub connector; archived receipts generated locally and matched remote blob SHA','evidence':'nonblind internal E1 program integrity only'}
    for model, files in MODELS.items():
        output['models'][model]={}
        for case in CASES:
            with tempfile.TemporaryDirectory(prefix='psy_p0_') as tmp:
                directory=pathlib.Path(tmp)
                for name in files:
                    shutil.copyfile(BASE/model/name,directory/name)
                source,csv_name,json_name=files
                if case=='csv_corrupt':
                    p=directory/csv_name;p.write_bytes(p.read_bytes()+b'\n')
                elif case=='json_corrupt':
                    p=directory/json_name;p.write_bytes(p.read_bytes()+b'\n')
                elif case=='missing_both':
                    (directory/csv_name).unlink();(directory/json_name).unlink()
                elif case=='source_mutation':
                    p=directory/source;p.write_bytes(p.read_bytes()+b'\n# benign source-only mutation\n')
                for opt in (False,True):
                    mode='optimized' if opt else 'normal'
                    cmd=[sys.executable]+(['-O'] if opt else [])
                    original=invoke(cmd+[str(directory/source),'--test','--audit'])
                    strict=invoke(cmd+[str(GATE),model,str(directory)])
                    output['models'][model][case+'_'+mode]={'original':original,'strict':strict}
                    expected_original=(case in ('valid','source_mutation') or opt)
                    expected_strict=(case=='valid')
                    if (original['exit_code']==0)!=expected_original or (strict['exit_code']==0)!=expected_strict:
                        raise AssertionError(f'Unexpected result: {model} {case} {mode} {original} {strict}')
    output['counts']={'models':2,'cases_per_model':5,'modes':2,'original_runs':20,'strict_runs':20,'original_false_accept_optimized':6,'source_mutation_original_accept':4,'strict_negative_rejections':16}
    output['status']='PASS_BOUNDED_NATIVE_P0'
    path=BASE/'R336_R340_P0_NATIVE_EXECUTION_2026-11-01.json'
    path.write_text(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'status':output['status'],'counts':output['counts'],'artifact':str(path)},ensure_ascii=False))

if __name__=='__main__':
    main()
