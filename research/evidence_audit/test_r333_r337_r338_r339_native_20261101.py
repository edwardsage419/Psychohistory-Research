#!/usr/bin/env python3
"""Native subprocess negative controls for pinned R333/R337/R338/R339 scripts.

The original scripts are executed unchanged on positive/receipt-mutation cases.
Only the source-edit case appends a benign comment to a disposable copy.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parent
SOURCE_ROOT=ROOT.parent if (ROOT.parent/'R333').is_dir() else ROOT
MODELS={
 'R333':('r333_triadic_feedback.py','R333_ALL_160_ARTIFICIAL_TRIADIC_STATES.csv','R333_EXACT_32_TRIADIC_WORLDS.json'),
 'R337':('r337_elm.py','R337_ALL_64_ARTIFICIAL_ARGUMENT_CUE_ATOMS.csv','R337_EXACT_32_CONDITIONS.json'),
 'R338':('r338_relative_deprivation.py','R338_ALL_128_ARTIFICIAL_COMPARISON_ATOMS.csv','R338_EXACT_64_CONDITIONS.json'),
 'R339':('r339_social_comparison.py','R339_ALL_100_ARTIFICIAL_TARGET_ATOMS.csv','R339_EXACT_50_CONDITIONS.json')}
CASES=('valid','csv_corrupt','json_corrupt','both_missing','source_comment')

def run(cmd):
 result=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,timeout=30)
 return {'exit':result.returncode,'stdout_tail':result.stdout[-350:],'stderr_tail':result.stderr[-400:]}

def test():
 records=[]
 for model,(source,csv,json_name) in MODELS.items():
  for case in CASES:
   with tempfile.TemporaryDirectory(prefix='psy_p0_'+model+'_') as temp:
    folder=Path(temp)
    for name in (source,csv,json_name):shutil.copyfile(SOURCE_ROOT/model/name,folder/name)
    if case=='csv_corrupt':
     p=folder/csv; b=bytearray(p.read_bytes()); b[len(b)//2]^=1;p.write_bytes(b)
    elif case=='json_corrupt':
     p=folder/json_name;b=bytearray(p.read_bytes());b[len(b)//2]^=1;p.write_bytes(b)
    elif case=='both_missing':
     (folder/csv).unlink();(folder/json_name).unlink()
    elif case=='source_comment':
     with (folder/source).open('ab') as f:f.write(b'\n# isolated source identity mutation\n')
    for optimized in (False,True):
     flag=['-O'] if optimized else []
     original=run([sys.executable,*flag,str(folder/source),'--test','--audit'])
     strict=run([sys.executable,*flag,str(ROOT/'r333_r337_r338_r339_strict_gate_20261101.py'),model,str(folder)])
     orig_expect=(case=='valid' or case=='source_comment' or optimized)
     strict_expect=(case=='valid')
     original_ok=(original['exit']==0)==orig_expect
     strict_ok=(strict['exit']==0)==strict_expect
     if not (original_ok and strict_ok):
      raise RuntimeError(f'UNEXPECTED {model} {case} optimized={optimized}: {original} {strict}')
     records.append({'model':model,'case':case,'optimized':optimized,'original':original,'strict':strict,'expected_matched':True})
 summary={
  'environment':sys.version,
  'test_kind':'same_operator_nonblind_native_python_subprocess',
  'input_provenance':'original Python sources and regenerated receipts with exact upstream Git blob matches',
  'records':len(records),
  'original_executions':len(records),
  'strict_executions':len(records),
  'original_optimized_false_accepts':sum(1 for r in records if r['optimized'] and r['case'] in ('csv_corrupt','json_corrupt','both_missing') and r['original']['exit']==0),
  'strict_negative_rejections':sum(1 for r in records if r['case']!='valid' and r['strict']['exit']!=0),
  'all_expected_matched':all(r['expected_matched'] for r in records),
  'external_independent_reproduction':'NOT_RUN',
  'e2_e3':'NOT_RUN',
  'records_detail':records,
 }
 out=ROOT/'R333_R337_R338_R339_P0_NATIVE_MATRIX_2026-11-01.json'
 out.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in summary.items() if k!='records_detail'},ensure_ascii=False,indent=2))

if __name__=='__main__':test()
