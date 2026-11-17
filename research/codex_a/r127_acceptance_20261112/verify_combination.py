#!/usr/bin/env python3
"""Fixed PR30–33 integration experiment; source captures only, no scoring/CI."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

MAIN='d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c'
HEADS={30:'8005fcb75e9e20545adb245edd45d72dbc374632',31:'03cf49d8970f273bb58ef0bfd125252166482dce',
       32:'16778c53b2e7a2c590ff65c854b1f7034169050d',33:'9d5041acdfc3f13a002e2cfbb6c33d4dfaed6af4'}
A='research/codex_a/r127_workflow_candidate'
B='research/codex_b/2026-11-11-r077-scientific-readiness'
ADAPTER='research/codex_a/r077_integration/preflight.py'
CAPTURE='import importlib.util,json,sys;s=importlib.util.spec_from_file_location("source_capture_only",sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(json.dumps(m.capture(),sort_keys=True))'


def need(ok,why):
    if not ok:raise ValueError(why)


def verify(repo,python,output):
    repo,output=Path(repo).resolve(),Path(output).resolve();output.mkdir(parents=True,exist_ok=False)
    def git(root,*args):return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.PIPE)
    def raw(ref,name):return git(repo,'show',ref+':'+name)
    files={n:set(git(repo,'diff','--name-only',MAIN+'...'+sha).decode().splitlines()) for n,sha in HEADS.items()}
    overlaps={str(a)+'/'+str(b):sorted(files[a]&files[b]) for a in HEADS for b in HEADS if a<b}
    need(not any(overlaps.values()),'PR_FILE_CONFLICT')
    old=raw(HEADS[31],B+'/pins.json');pins=json.loads(old);adapter=raw(HEADS[30],ADAPTER)
    pins[ADAPTER]={'git_blob':hashlib.sha1(b'blob '+str(len(adapter)).encode()+b'\0'+adapter).hexdigest(),
                   'bytes':len(adapter),'sha256':hashlib.sha256(adapter).hexdigest()}
    revised=(json.dumps(pins,indent=2)+'\n').encode()
    pin_patch=''.join(difflib.unified_diff(old.decode().splitlines(True),revised.decode().splitlines(True),
                                         fromfile='a/'+B+'/pins.json',tofile='b/'+B+'/pins.json')).encode()
    (output/'pr31-pr30-pin-refresh.patch').write_bytes(pin_patch)
    records=[]
    with tempfile.TemporaryDirectory(prefix='codex-a-integration-only-') as td:
        work=Path(td)/'repo'
        subprocess.run(['git','clone','--shared','--no-checkout',str(repo),str(work)],check=True,capture_output=True)
        git(work,'checkout','--detach',MAIN);git(work,'config','user.name','Local integration fixture');git(work,'config','user.email','fixture@example.invalid')
        def commit(label):
            git(work,'add','-A');git(work,'commit','-qm',label+' [skip ci]')
        def apply(patch):
            subprocess.run(['git','apply','--check','-'],input=patch,cwd=work,check=True,capture_output=True)
            subprocess.run(['git','apply','-'],input=patch,cwd=work,check=True,capture_output=True)
        def execute(tag,args,expected):
            child=subprocess.run(list(map(str,args)),cwd=work,capture_output=True,timeout=30)
            for name,value in [('stdout',child.stdout),('stderr',child.stderr)]: (output/(tag+'.'+name)).write_bytes(value)
            records.append({'tag':tag,'argv':list(map(str,args)),'cwd':str(work),'exit':child.returncode,'expected_exit':expected,
                            'streams':{name:{'bytes':len(value),'sha256':hashlib.sha256(value).hexdigest()}
                                       for name,value in [('stdout',child.stdout),('stderr',child.stderr)]}})
            need(child.returncode==expected,'UNEXPECTED_EXIT:'+tag)
            return child
        for n,sha in HEADS.items():apply(git(repo,'diff','--binary',MAIN+'...'+sha))
        commit('Local fixed PR30-33 fixture')
        for optimized,label in [(False,'normal'),(True,'optimized')]:
            cmd=[str(python),'-B']+(['-O']if optimized else[])+['-c',CAPTURE,str(work/B/'run_audit.py')]
            red=execute('pins-red-'+label,cmd,1)
            need(('SOURCE_BLOB:'+ADAPTER).encode() in red.stderr,'WRONG_SOURCE_FAILURE')
        apply(pin_patch);commit('Local B-owned candidate pin requalification')
        for optimized,label in [(False,'normal'),(True,'optimized')]:
            prefix=[str(python),'-B']+(['-O']if optimized else[])
            green=execute('pins-green-'+label,prefix+['-c',CAPTURE,str(work/B/'run_audit.py')],0)
            need(len(json.loads(green.stdout))==22,'SOURCE_CAPTURE_COVERAGE')
            checked=execute('checklist-'+label,prefix+['research/codex_a/r077_integration/mainline_checklist.py','.'],2)
            result=json.loads(checked.stdout)
            need(result['production_ready']is False and result['original_failure_cases']==11 and
                 result['candidate_correct_orders']==35 and result['mathematical_programs_rerun']is False,'PRODUCTION_VETO')
        # Only temp workflow/gate pin wiring is changed. No new mathematical run.
        generated=execute('generate-current-main-patch',[str(python),'-B',A+'/prepare.py','.'],0).stdout
        need(generated==raw(HEADS[32],A+'/candidate.patch'),'PATCH_DRIFT')
        manifest=json.loads(raw(HEADS[32],A+'/candidate_manifest.json'))
        original={name:(work/name).read_bytes() for name in manifest['targets']}
        apply(generated);commit('Local R-owned workflow candidate only')
        capture='import importlib.util,json,sys;s=importlib.util.spec_from_file_location("gate_capture",sys.argv[1]);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);raw,ids,head=m.capture(sys.argv[2]);print(json.dumps({"head":head,"sources":ids},sort_keys=True))'
        captured=execute('r127-current-main-source-capture',[str(python),'-B','-c',capture,
                         str(work/'research/codex_a/r127_local_gates/gate.py'),str(work)],0)
        need(len(json.loads(captured.stdout)['sources'])==5,'R127_SOURCE_COVERAGE')
        for name in json.loads(raw(MAIN,'research/codex_a/r127_local_gates/pins.json')):
            if name not in manifest['targets']:need((work/name).read_bytes()==raw(MAIN,name),'FROZEN_SOURCE_CHANGED')
        for options in (['--reverse','--check'],['--reverse']):
            subprocess.run(['git','apply',*options,'-'],input=generated,cwd=work,check=True,capture_output=True)
        need(all((work/name).read_bytes()==value for name,value in original.items()),'ROLLBACK_BYTES')
    result={'status':'COMPLETE_COMBINED_CAPTURE_ONLY','main':MAIN,'heads':HEADS,'file_overlaps':overlaps,
            'pr31_original_combination':'NEEDS_PIN_REFRESH','pr31_pin_patch_sha256':hashlib.sha256(pin_patch).hexdigest(),
            'source_capture_green_records':22,'R127_patch_sha256':hashlib.sha256(generated).hexdigest(),
            'R127_current_main_patch_and_reverse':'COMPLETE','R127_original_frozen_objects':'UNCHANGED',
            'commands':records,'mathematical_programs_rerun':False,'real_B_or_R_files_modified':False,
            'production_ready':False,'CI':'NOT_RUN','human_rescoring':'NOT_RUN'}
    (output/'result.json').write_text(json.dumps(result,indent=2)+'\n');return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for key in ('repo','python','output'):p.add_argument('--'+key,type=Path,required=True)
    a=p.parse_args();r=verify(a.repo,a.python,a.output);print(json.dumps({k:r[k] for k in ('status','main','pr31_original_combination','source_capture_green_records','production_ready')}))
