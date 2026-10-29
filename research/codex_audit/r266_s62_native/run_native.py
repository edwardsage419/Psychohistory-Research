#!/usr/bin/env python3
"""Pinned R266 S62 original CLIs, byte reconstruction and source-row audit.
Use a fresh --output directory for each evidentiary run; existing logs are replaced.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from source_audit import audit

R='research/validation/r266_s62_score_coverage.js'
B='research/evidence_audit/r266_s62_independent_convolution_gate.js'
REBUILD='research/evidence_audit/r266_s62_original_source_sha_rebuild.py'
CSV='research/R266/R266_ALL_5328_FINITE_MONTE_CARLO_ORIGINAL_SOURCES.csv'
BASE='research/R266/R266_EXACT_FINITE_MC_RESULTS.json'
RECEIPT='research/validation/R266_S62_EXACT_SCORE_COVERAGE_RECEIPT_2026-10-29.json'
PINS={R:'07b0ddeabe02415a2545af289ac29678e616f53e',B:'136b87413c779eb40236e4a5048d400f1120059e',
      REBUILD:'1596c5b9763090ec9edd2fb430fd4a207eb40d85',CSV:'53a808994300f85826a18723146fdb2fea7c6db2',
      BASE:'ec307a45a361d202cae074a45cea5406b2a8e28e',RECEIPT:'9c7f64d593ac3f9f06472a5f62f19f09fb4582fb'}

def require(ok,message):
    if not ok:raise ValueError(message)

def identity(root):
    out={}
    for path,pin in PINS.items():
        raw=(root/path).read_bytes();blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        require(blob==pin,'source identity '+path)
        out[path]={'bytes':len(raw),'git_blob':blob,'sha256':hashlib.sha256(raw).hexdigest()}
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    root,out=a.root.resolve(),a.output.resolve();labels=('r_native','b_persisted','rebuild_native','rebuild_bytes_adapter','b_replayed')
    targets=[out/'execution.json']+[out/(label+suffix) for label in labels for suffix in ('.stdout','.stderr')]
    protected=[root/path for path in PINS]+[Path(__file__).resolve(),Path(__file__).with_name('source_audit.py').resolve()]
    require(not any(t==s.resolve() or (t.exists() and s.exists() and t.samefile(s)) for t in targets for s in protected),'output aliases input')
    out.mkdir(parents=True,exist_ok=True);(out/'execution.json').unlink(missing_ok=True)
    before=identity(root);commands=[]
    def run(label,cmd):
        r=subprocess.run(cmd,cwd=root,capture_output=True,timeout=60)
        (out/(label+'.stdout')).write_bytes(r.stdout);(out/(label+'.stderr')).write_bytes(r.stderr)
        commands.append({'label':label,'command':cmd,'cwd':str(root),'exit_code':r.returncode,'stdout_file':label+'.stdout','stderr_file':label+'.stderr'})
        require(r.returncode==0,'CLI failed '+label)
        return r.stdout
    r_raw=run('r_native',['node',str(root/R)]);archived=(root/RECEIPT).read_bytes()
    require(r_raw==archived,'R full receipt bytes mismatch')
    b=json.loads(run('b_persisted',['node',str(root/B),str(root/RECEIPT)]))
    require(b.get('status')=='PASS' and b.get('fields_compared')==180 and b.get('negative_controls_rejected')==5,'B coverage')
    rebuild=run('rebuild_native',[sys.executable,'-B',str(root/REBUILD)])
    require(rebuild.startswith(b'PASS rows=5328 bytes=419791 sha256=5e0aac41c960ee21b54d3266064793a7e9a2454dbb4493ae8e4451591d48587a'),'rebuild CLI summary')
    with tempfile.TemporaryDirectory(prefix='s62-native-') as tmp:
        tmp=Path(tmp);regenerated=tmp/'regenerated.csv';replayed=tmp/'r-replayed.json';replayed.write_bytes(r_raw)
        # Preserve original CLI semantics above; this separate adapter exposes
        # regenerate() bytes without modifying original source or republishing CSV.
        code="import runpy,sys,json;from pathlib import Path;raw,n=runpy.run_path(sys.argv[1])['regenerate']();Path(sys.argv[2]).write_bytes(raw);print(json.dumps({'rows':n,'bytes':len(raw)}))"
        adapter=json.loads(run('rebuild_bytes_adapter',[sys.executable,'-B','-c',code,str(root/REBUILD),str(regenerated)]))
        require(adapter=={'rows':5328,'bytes':419791} and regenerated.read_bytes()==(root/CSV).read_bytes(),'rebuilt full CSV bytes mismatch')
        require(json.loads(run('b_replayed',['node',str(root/B),str(replayed)]))==b,'replayed B differs')
    source=audit((root/CSV).read_text(),json.loads((root/BASE).read_text()),json.loads(archived))
    require(before==identity(root),'original files changed')
    result={'status':'COMPLETE','pinned_source_baseline':'3d5349f5505679492ee324f8b47d028476b1fc7b',
            'python':sys.version,'node':subprocess.check_output(['node','--version'],text=True).strip(),'platform':platform.platform(),
            'seed':'N/A; exhaustive finite enumeration','source_identity':before,'source_unchanged':True,
            'positive_original_cli_invocations':4,'additional_byte_adapter_invocations':1,
            'R_receipt_byte_equal':True,'reconstructed_CSV_byte_equal':True,'B_persisted':b,'source_audit':source,
            'commands':commands,'evidence':'NONBLIND_INTERNAL_ARTIFICIAL_E1','new_E2':0,'new_E3':0,'external_team_replications':0,
            'original_R266_136_test_suites':'NOT_RUN','full_repo_tests':'NOT_RUN','ci':'NOT_RUN',
            'code_sha256':{n:hashlib.sha256(Path(__file__).with_name(n).read_bytes()).hexdigest() for n in ('run_native.py','source_audit.py')}}
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=out,delete=False) as f:
        staged=Path(f.name);f.write(json.dumps(result,indent=2)+'\n')
    staged.replace(out/'execution.json')
    print(json.dumps({'status':'COMPLETE','source_rows':5328,'metric_fields':180,'R_and_rebuilt_CSV_bytes_equal':True,'original_positive_clis':4,'byte_adapters':1}))

if __name__=='__main__':main()
