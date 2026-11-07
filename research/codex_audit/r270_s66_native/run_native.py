#!/usr/bin/env python3
"""Replay exact pinned S66 sources; outputs must use a distinct directory per run."""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
from dp_oracle import calculate,verify

R='research/validation/r270_s66_exact_ppc_alarm.js'
B='research/evidence_audit/r270_s66_independent_run_composition_cli.py'
RECEIPT='research/validation/R270_S66_EXACT_PPC_ALARM_RECEIPT_2026-10-29.json'
PINS={R:'6408335f61e0638a7b0951a78034c13664f5133d',B:'b79636d2969d353954d997717cddbe7115e8e5cd',RECEIPT:'20fc7f616a3ce2e3b9d30714646f3173d1ffea08'}

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
    root,out=a.root.resolve(),a.output.resolve();labels=['r_original','b_original','r_emit','r_regenerated','b_regenerated']+[case+'_'+route for case in ('wrong_tail','reordered','float_count') for route in ('r','b')]
    targets=[out/'execution.json',out/'DP_full_receipt.json']+[out/(label+suffix) for label in labels for suffix in ('.stdout','.stderr')]
    protected=[root/path for path in PINS]+[Path(__file__).resolve(),Path(__file__).with_name('dp_oracle.py').resolve()]
    require(not any(t==s.resolve() or (t.exists() and s.exists() and t.samefile(s)) for t in targets for s in protected),'output aliases input')
    out.mkdir(parents=True,exist_ok=True);(out/'execution.json').unlink(missing_ok=True)
    before=identity(root);data=json.loads((root/RECEIPT).read_text());commands=[]
    def run(label,cmd,success=True):
        r=subprocess.run(cmd,cwd=root,capture_output=True,text=True,timeout=60)
        (out/(label+'.stdout')).write_text(r.stdout);(out/(label+'.stderr')).write_text(r.stderr)
        commands.append({'label':label,'command':cmd,'cwd':str(root),'exit_code':r.returncode,'stdout_file':label+'.stdout','stderr_file':label+'.stderr'})
        require((r.returncode==0)==success,'unexpected CLI outcome '+label)
        return r.stdout
    rs=run('r_original',['node',str(root/R),'--selftest','--check',str(root/RECEIPT)])
    rtest=json.loads(rs.splitlines()[0]);require(rtest=={'pass':True,'negative_controls_rejected':5,'exact_tails':192,'alarm_probabilities':27},'R selftest coverage')
    bs=run('b_original',[sys.executable,'-B',str(root/B),'--selftest','--check',str(root/RECEIPT)])
    require('5 negative controls' in bs and 'PASS: archived receipt' in bs,'B selftest coverage')
    dp=verify(data);dp_bytes=(json.dumps(calculate(),indent=2)+'\n').encode()
    require(dp_bytes==(root/RECEIPT).read_bytes(),'DP full bytes mismatch')
    (out/'DP_full_receipt.json').write_bytes(dp_bytes)
    controls=[]
    with tempfile.TemporaryDirectory(prefix='s66-native-') as tmp:
        tmp=Path(tmp);emitted=tmp/'R_emitted.json'
        run('r_emit',['node',str(root/R),'--emit',str(emitted)])
        require(emitted.read_bytes()==(root/RECEIPT).read_bytes(),'R emitted byte mismatch')
        run('r_regenerated',['node',str(root/R),'--check',str(emitted)])
        run('b_regenerated',[sys.executable,'-B',str(root/B),'--check',str(emitted)])
        for case in ('wrong_tail','reordered','float_count'):
            obj=json.loads(json.dumps(data))
            if case=='wrong_tail':obj['lower_tails']['1,1'][0]='999'
            elif case=='reordered':obj=dict(reversed(list(obj.items())))
            else:obj['alarms']['1,1|1/4|1/20']['alarm_sequence_count']=2.0
            path=tmp/(case+'.json');path.write_text(json.dumps(obj,indent=2)+'\n')
            r_accept=case=='float_count';b_accept=case!='wrong_tail'
            run(case+'_r',['node',str(root/R),'--check',str(path)],r_accept)
            run(case+'_b',[sys.executable,'-B',str(root/B),'--check',str(path)],b_accept)
            try:verify(obj)
            except ValueError:dp_accept=False
            else:dp_accept=True
            require(dp_accept==(case=='reordered'),'unexpected DP control '+case)
            controls.append({'case':case,'R_accepted':r_accept,'B_accepted':b_accept,'DP_accepted':dp_accept})
    require(before==identity(root),'original inputs changed')
    result={'status':'COMPLETE','pinned_source_baseline':'7c5d5650af12cfdd08e0f2d23b73a49e6f506d29',
            'python':sys.version,'node':subprocess.check_output(['node','--version'],text=True).strip(),'platform':platform.platform(),
            'seed':'N/A; exact finite arithmetic','source_identity':before,'source_unchanged':True,
            'positive_original_cli_invocations':5,'original_selftest_negative_controls_per_route':5,
            'R_emitted_byte_equal':True,'DP_byte_equal':True,'DP_receipt_sha256':hashlib.sha256(dp_bytes).hexdigest(),
            'DP_result':dp,'controls':controls,'commands':commands,
            'evidence':'NONBLIND_INTERNAL_ARTIFICIAL_E1','new_E2':0,'new_E3':0,'external_team_replications':0,
            'S66_scientific_status':'PARTIAL_BOUNDED_INTERNAL_EXACT','full_repo_tests':'NOT_RUN',
            'original_R270_83_test_suites':'NOT_RUN','legacy_nonportable_B_cli':'NOT_RUN','ci':'NOT_RUN',
            'code_sha256':{n:hashlib.sha256(Path(__file__).with_name(n).read_bytes()).hexdigest() for n in ('dp_oracle.py','run_native.py')}}
    with tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',dir=out,delete=False) as f:
        stage=Path(f.name);f.write(json.dumps(result,indent=2)+'\n')
    stage.replace(out/'execution.json')
    print(json.dumps({'status':'COMPLETE','tails':192,'alarms':27,'R_and_DP_byte_equal':True,'controls':controls}))

if __name__=='__main__':main()
