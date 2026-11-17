"""B-owned fixed PR30/31 source qualification; no mathematical scoring runs."""
import argparse
import ast
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[4]
OWN='research/codex_b/2026-11-11-r077-scientific-readiness'
ADAPTER='research/codex_a/r077_integration/preflight.py'
MAIN='d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c'
OLD31='03cf49d8970f273bb58ef0bfd125252166482dce'
PR30='8005fcb75e9e20545adb245edd45d72dbc374632'
A35='9ae4eb923b7d1cbc78fdc0c81cddee591efc68ef'
CAPTURE='import importlib.util,json,sys;s=importlib.util.spec_from_file_location("capture_only",sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(json.dumps(m.capture(),sort_keys=True))'


def need(ok,why):
    if not ok:raise ValueError(why)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def identity(raw):
    return {'git_blob':hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),'bytes':len(raw),'sha256':sha(raw)}


def verify(output):
    output.mkdir(parents=True,exist_ok=False)
    def git(repo,*args):return subprocess.check_output(['git','-C',str(repo),*args],stderr=subprocess.PIPE)
    def raw(ref,path):return git(ROOT,'show',ref+':'+path)
    changes=set(git(ROOT,'diff','--name-only',MAIN+'...'+PR30).decode().splitlines())
    need(changes=={ADAPTER,'research/codex_a/r077_integration/artifact_hashes.json',
                   'research/codex_a/r077_integration/deployment_metadata_20261111.json'},'UNEXPECTED_PR30_FILE_SCOPE')
    old_adapter,new_adapter=raw(MAIN,ADAPTER),raw(PR30,ADAPTER)
    replacements={b'PASS_ARTIFICIAL_SHADOW_ONLY_UNMERGED_CANDIDATE':b'PASS_ARTIFICIAL_SHADOW_ONLY_PINNED_CANDIDATE',
                  b'Opt in to fixed unmerged PR28 synthetic shadow; never enables production.':b'Opt in to pinned PR28 synthetic shadow; never enables production.'}
    expected=old_adapter
    for a,b in replacements.items():need(expected.count(a)==1,'LITERAL_PREIMAGE');expected=expected.replace(a,b)
    need(expected==new_adapter,'UNEXPECTED_A30_IMPLEMENTATION_CHANGE')
    # Reject AST changes other than the same two whitelisted literal values.
    old_ast=ast.parse(old_adapter);new_ast=ast.parse(new_adapter)
    reverse={v.decode():k.decode() for k,v in replacements.items()}
    for node in ast.walk(new_ast):
        if isinstance(node,ast.Constant) and type(node.value) is str:node.value=reverse.get(node.value,node.value)
    need(ast.dump(old_ast)==ast.dump(new_ast),'NON_LITERAL_AST_CHANGE')
    old_pins=raw(OLD31,OWN+'/pins.json');pins=json.loads(old_pins);pins[ADAPTER]=identity(new_adapter)
    expected_pins=(json.dumps(pins,indent=2)+'\n').encode()
    current=(ROOT/OWN/'pins.json').read_bytes();need(current==expected_pins,'CURRENT_PIN_NOT_REQUALIFIED')
    patch=raw(A35,'research/codex_a/r127_acceptance_20261112/pr31-pr30-pin-refresh.patch')
    need(patch==(ROOT/OWN/'evidence/pin-refresh-20261112/approved-A35.patch').read_bytes(),'A35_PATCH_DRIFT')
    need(old_pins==(ROOT/OWN/'evidence/pin-refresh-20261112/pins-before.json').read_bytes(),'OLD_SNAPSHOT_DRIFT')
    # All original mathematical programs and historical evidence are preserved.
    old_files=git(ROOT,'ls-tree','-r','--name-only',OLD31,OWN).decode().splitlines()
    for path in old_files:
        if path!=OWN+'/pins.json':need((ROOT/path).read_bytes()==raw(OLD31,path),'EXTRA_B31_CHANGE:'+path)
    commands=[]
    with tempfile.TemporaryDirectory(prefix='b31-pin-qualification-') as td:
        work=Path(td)/'repo'
        subprocess.run(['git','clone','--shared','--no-checkout',str(ROOT),str(work)],check=True,capture_output=True)
        git(work,'checkout','--detach',MAIN);git(work,'config','user.name','B source qualification fixture');git(work,'config','user.email','fixture@example.invalid')
        def apply(data):
            subprocess.run(['git','apply','--check','-'],input=data,cwd=work,check=True,capture_output=True)
            subprocess.run(['git','apply','-'],input=data,cwd=work,check=True,capture_output=True)
        def commit(label):git(work,'add','-A');git(work,'commit','-qm',label+' [skip ci]')
        def execute(tag,args,exit_code):
            child=subprocess.run(list(map(str,args)),cwd=work,capture_output=True,timeout=60);streams={}
            for kind,data in (('stdout',child.stdout),('stderr',child.stderr)):
                filename=tag+'.'+kind
                if data:(output/filename).write_bytes(data)
                streams[kind]={'file':filename if data else None,'bytes':len(data),'sha256':sha(data)}
            commands.append({'tag':tag,'argv':list(map(str,args)),'cwd':str(work),'exit_code':child.returncode,'expected_exit':exit_code,'streams':streams})
            (output/'commands.json').write_text(json.dumps(commands,indent=2)+'\n')
            need(child.returncode==exit_code,'WRONG_EXIT:'+tag);return child
        apply(git(ROOT,'diff','--binary',MAIN+'...'+PR30));apply(git(ROOT,'diff','--binary',MAIN+'...'+OLD31))
        commit('Fixed PR30 and original PR31 combination')
        prefixes={mode:[sys.executable,'-B']+(['-O'] if mode=='optimized' else []) for mode in ('normal','optimized')}
        for mode,prefix in prefixes.items():
            child=execute('old-pins-red-'+mode,prefix+['-c',CAPTURE,work/OWN/'run_audit.py'],1)
            need(('SOURCE_BLOB:'+ADAPTER).encode() in child.stderr,'WRONG_RED_REASON')
        apply(patch);need((work/OWN/'pins.json').read_bytes()==current,'PATCH_NOT_MINIMAL_EQUIVALENT');commit('B approved pin-only requalification')
        green={}
        for mode,prefix in prefixes.items():
            child=execute('new-pins-green-'+mode,prefix+['-c',CAPTURE,work/OWN/'run_audit.py'],0)
            captured=json.loads(child.stdout);need(len(captured)==22,'SOURCE_CAPTURE_COUNT')
            old_sources=json.loads(raw(OLD31,OWN+'/evidence/normal/summary.json'))['sources']
            changed={p for p in captured if captured[p]!=old_sources[p]}
            need(changed=={ADAPTER,OWN+'/pins.json'},'UNEXPECTED_SOURCE_DELTA')
            green[mode]={'count':22,'changed_fingerprint_records':sorted(changed)}
            regression="import importlib.util,json,sys,tarfile;s=importlib.util.spec_from_file_location('preflight',sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);t=tarfile.open(sys.argv[2],'r:gz');d=json.loads(t.extractfile('normal-shadow.stdout').read());base=m.classify(d['diagnostic']);shadow=m.validate_shadow(d['candidate_shadow']['data'],d['diagnostic']);m.require(base['exit_code']==2 and base['production_ready']is False and base['original_failure_cases']==11,'VETO');m.require(shadow['status']=='PASS_ARTIFICIAL_SHADOW_ONLY_PINNED_CANDIDATE' and shadow['corrected_orders']==35 and shadow['production_ready']is False,'METADATA');d['candidate_shadow']['data']['tiny']['candidate_worse_sessions']=0;rejected=False\ntry:m.validate_shadow(d['candidate_shadow']['data'],d['diagnostic'])\nexcept ValueError:rejected=True\nm.require(rejected,'REGRESSION_REJECTION');print(json.dumps({'production_ready':False,'original_failures_retained':11,'retained_corrected_cases':35,'corrupt_retained_shadow_rejected':True,'mathematical_programs_rerun':False}))"
            execute('retained-validator-regression-'+mode,prefix+['-c',regression,work/ADAPTER,work/'research/codex_a/r077_integration/shadow_evidence.tar.gz'],0)
        # Unexpected B candidate bytes must still fail before any calculation.
        target=work/'research/codex_b/2026-11-10-r077-exact-score-candidate/candidate.py';saved=target.read_bytes();target.write_bytes(saved+b'\n')
        for mode,prefix in prefixes.items():
            child=execute('unexpected-source-rejected-'+mode,prefix+['-c',CAPTURE,work/OWN/'run_audit.py'],1)
            need(b'SOURCE_BLOB:research/codex_b/2026-11-10-r077-exact-score-candidate/candidate.py' in child.stderr,'WRONG_REJECTION_REASON')
        target.write_bytes(saved)
        help_result=execute('native-help',[sys.executable,'-B',work/ADAPTER,'--help'],0)
        need(b'Opt in to pinned PR28' in help_result.stdout,'HELP_METADATA')
    result={'status':'COMPLETE_B31_PIN_REQUALIFICATION','main':MAIN,'old_PR31':OLD31,'PR30':PR30,'A35':A35,
        'old_adapter':identity(old_adapter),'new_adapter':identity(new_adapter),'new_pin_manifest':identity(current),
        'approved_patch_sha256':sha(patch),'helper_sha256':sha(Path(__file__).read_bytes()),'green':green,
        'original_files_preserved_except_pin_manifest':len(old_files)-1,'standalone_without_PR30':'EXPECTED_SOURCE_BLOB_REJECTION',
        'mathematical_programs_rerun':False,'human_scoring':'NOT_RUN','production_ready':False,'CI':'NOT_RUN',
        'real_A_files_modified':False,'fixture_remote_operations':'NONE_LOCAL_CLONE_ONLY'}
    (output/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True);verify(p.parse_args().output.resolve())
