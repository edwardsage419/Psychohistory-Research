#!/usr/bin/env python3
"""Test the fixed PR32 publisher against temporary LOCAL remotes, never GitHub."""
import argparse
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import tempfile

OWN = 'research/codex_a/r127_workflow_candidate'


def check(repo, python, bundle, receipt, output):
    repo, bundle, receipt, output = map(lambda p: Path(p).resolve(), (repo,bundle,receipt,output))
    output.mkdir(parents=True,exist_ok=False)
    data = json.loads(receipt.read_bytes());tested = data['execution']['tested_checkout_sha']
    ctx = data['context']
    relative = OWN+'/receipts/'+ctx['run_id']+'-'+ctx['attempt']+'-'+ctx['job_key']+'.json'
    def git(root,*args):
        return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.PIPE).decode().strip()
    records=[]
    with tempfile.TemporaryDirectory(prefix='r127-deploy-failures-') as td:
        temp=Path(td)
        for case in ('commit_rejected','remote_advanced_during_commit','push_rejected'):
            work,remote=temp/case,temp/(case+'.git')
            subprocess.run(['git','clone','--shared','--no-checkout',str(repo),str(work)],check=True,capture_output=True)
            git(work,'fetch',str(bundle),'HEAD');git(work,'checkout','--detach',tested)
            git(work,'config','user.name','Local failure fixture');git(work,'config','user.email','fixture@example.invalid')
            subprocess.run(['git','clone','--bare','--shared',str(work),str(remote)],check=True,capture_output=True)
            git(work,'remote','set-url','origin',str(remote))
            subprocess.run(['git','--git-dir',str(remote),'update-ref','refs/heads/main',tested],check=True,capture_output=True)
            if git(work,'remote','get-url','origin')!=str(remote) or not remote.is_relative_to(temp):
                raise ValueError('LOCAL_REMOTE_REQUIRED')
            target=work/relative;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(receipt.read_bytes())
            if case=='commit_rejected':
                hook=work/'.git/hooks/pre-commit';hook.write_text('#!/bin/sh\nexit 1\n');hook.chmod(0o755)
            elif case=='push_rejected':
                hook=remote/'hooks/pre-receive';hook.write_text('#!/bin/sh\nexit 1\n');hook.chmod(0o755)
            else:
                competing=git(work,'-c','user.name=Fixture','-c','user.email=fixture@example.invalid',
                              'commit-tree',git(work,'rev-parse','HEAD^{tree}'),'-p',tested,'-m','Local competing update')
                hook=work/'.git/hooks/pre-commit'
                hook.write_text('#!/bin/sh\ngit --git-dir '+shlex.quote(str(remote))+
                                ' update-ref refs/heads/main '+shlex.quote(competing)+'\n')
                hook.chmod(0o755)
            args=[str(python),'-B',OWN+'/publish.py','.', '--receipt',relative,
                  '--expected-head',tested,'--remote','origin','--allow-push']
            child=subprocess.run(args,cwd=work,capture_output=True,timeout=30)
            for name,raw in [('stdout',child.stdout),('stderr',child.stderr)]:
                (output/(case+'.'+name)).write_bytes(raw)
            outcome=json.loads(child.stdout)
            expected_reason={'commit_rejected':'GIT_OPERATION_FAILED:commit',
                             'push_rejected':'GIT_OPERATION_FAILED:push',
                             'remote_advanced_during_commit':'REMOTE_MAIN_ADVANCED_AFTER_COMMIT'}[case]
            if child.returncode!=1 or outcome.get('status')!='BLOCKED' or expected_reason not in outcome['reason']:
                raise ValueError('FALSE_SUCCESS_OR_WRONG_FAILURE:'+case)
            remote_after=git(work,'ls-remote','origin','refs/heads/main').split()[0]
            local_after=git(work,'rev-parse','HEAD')
            if remote_after!=(competing if case=='remote_advanced_during_commit' else tested):
                raise ValueError('REMOTE_OVERWRITTEN:'+case)
            if (local_after==tested)!=(case=='commit_rejected'):
                raise ValueError('WRONG_LOCAL_COMMIT_STATE:'+case)
            if case!='commit_rejected' and git(work,'diff','--name-only',tested,local_after)!=relative:
                raise ValueError('UNRELATED_PATH_COMMITTED')
            records.append({'case':case,'argv':args,'cwd':str(work),'exit':child.returncode,
                            'reason':outcome['reason'],'local_result_commit_remains':local_after!=tested,
                            'remote_expected_object_preserved':True,'remote_kind':'TEMP_LOCAL_BARE_ONLY',
                            'streams':{name:{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
                                       for name,raw in [('stdout',child.stdout),('stderr',child.stderr)]}})
    result={'status':'COMPLETE_EXPECTED_FAILURES','tested_fixture':tested,
            'bundle_sha256':hashlib.sha256(bundle.read_bytes()).hexdigest(),'cases':records,
            'CI':'NOT_RUN','production_deployed':False,'mathematical_programs_rerun':False}
    (output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('repo','python','bundle','receipt','output'):p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();print(json.dumps(check(a.repo,a.python,a.bundle,a.receipt,a.output),indent=2))
