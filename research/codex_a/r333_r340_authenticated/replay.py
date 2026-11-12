#!/usr/bin/env python3
"""Authenticate and replay the EXISTING eight-model composite on one snapshot.

Reuses adopted S53 byte identity functions and the original R333..R340 gates.
No new math, network, Git mutation, workflow change or scientific acceptance.
The caller must trust this entrypoint's delivery commit before invoking Python -I.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import types

BASE='d4740c2cd999b8da06a25b0ef407aeaf8a56ab6c'
HELPER='research/codex_a/r257_s53_authenticated/authenticate.py'
HELPER_SHA256='42c8a198ac54c33b80fc69088a1edee58ff596e3d0369d750b229ad00bb01596'
AUDIT='research/evidence_audit/'
COMPOSITE=AUDIT+'r333_r340_composite_acceptance_20261101.py'
GATES=(COMPOSITE,AUDIT+'r333_r340_acceptance_entry_20261101.py',
       AUDIT+'r333_r340_claim_receipt_gate_20261101.js',
       AUDIT+'r333_r337_r338_r339_strict_gate_20261101.py',AUDIT+'r334_strict_receipt_gate_20261101.py',
       AUDIT+'r335_strict_receipt_gate_20261101.py',AUDIT+'r336_r340_strict_receipt_gate_20261101.py')
MODELS=['R'+str(i)for i in range(333,341)]
EXPECTED={'status':'PASS_COMPOSITE_CANDIDATE_E1_ONLY','models':MODELS,'claim_files_checked':16,
          'math_entry_runs':2,'math_child_checks_claimed':32,'evidence':'E1_ARTIFICIAL_ONLY',
          'production_adoption':'NOT_ESTABLISHED','independent_data_validation':'NOT_RUN',
          'external_team_replication':'NOT_RUN'}


def git(root,*args):
    environment=os.environ.copy()
    for name in ('GIT_DIR','GIT_WORK_TREE','GIT_COMMON_DIR','GIT_INDEX_FILE','GIT_OBJECT_DIRECTORY',
                 'GIT_ALTERNATE_OBJECT_DIRECTORIES','GIT_REPLACE_REF_BASE','GIT_SHALLOW_FILE','GIT_NAMESPACE'):
        environment.pop(name,None)
    try:return subprocess.check_output(['git','--no-replace-objects','-C',str(root),*args],
                                       stderr=subprocess.PIPE,env=environment)
    except subprocess.CalledProcessError as exc:raise ValueError('GIT_INPUT_UNAVAILABLE')from exc


def capture(root):
    root=Path(root).resolve()
    # Load an already adopted identity implementation from immutable Git bytes;
    # never execute a possibly changed worktree helper to authenticate itself.
    common=types.ModuleType('existing_s53_identity')
    helper=git(root,'show',BASE+':'+HELPER)
    if hashlib.sha256(helper).hexdigest()!=HELPER_SHA256:raise ValueError('IDENTITY_HELPER_SHA256')
    exec(compile(helper,BASE+':'+HELPER,'exec'),common.__dict__)
    head=git(root,'rev-parse','HEAD^{commit}').decode().strip()
    model_paths=git(root,'ls-tree','-r','--name-only',BASE,'--',
                    *('research/'+model for model in MODELS)).decode().splitlines()
    model_paths=[p for p in model_paths if p.endswith(('.py','.csv','.json'))]
    protocols=git(root,'ls-tree','-r','--name-only',BASE,'--','protocols').decode().splitlines()
    protocols=[p for p in protocols if any(p.startswith('protocols/'+model+'_')for model in MODELS)
               and p.endswith('_PRESCORE_FREEZE_2026-10-24.md')]
    if len(model_paths)!=40 or len(protocols)!=8:raise ValueError('SOURCE_UNIVERSE')
    raw={};ids={}
    for name in sorted(model_paths+protocols+list(GATES)+[HELPER]):
        path=root/name
        if path.is_symlink()or any(p.is_symlink()for p in path.parents if p!=root and p.is_relative_to(root)):
            raise ValueError('LINKED_SOURCE:'+name)
        expected=common.identity(git(root,'show',BASE+':'+name))
        value=common.authenticated(path,expected)
        if git(root,'rev-parse',head+':'+name).decode().strip()!=expected['git_blob']:
            raise ValueError('CHECKOUT_IDENTITY:'+name)
        raw[name]=value;ids[name]=expected
    return head,raw,ids,common


def verify(root,node='node'):
    own=Path(__file__).read_bytes()
    head,raw,ids,common=capture(root)
    node_path=shutil.which(node)
    if node_path is None:raise ValueError('NODE_EXECUTABLE_UNAVAILABLE')
    environment=os.environ.copy()
    for name in tuple(environment):
        if name.startswith('PYTHON')or name=='NODE_OPTIONS':environment.pop(name)
    environment['PYTHONNOUSERSITE']='1'
    with tempfile.TemporaryDirectory(prefix='r333-authenticated-')as td:
        snapshot=Path(td)
        for name,value in raw.items():
            p=snapshot/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(value)
        command=[sys.executable,'-I','-B']+(['-O']if sys.flags.optimize else[])
        command += [str(snapshot/COMPOSITE),'--repo-root',str(snapshot),'--node',node_path]
        child=subprocess.run(command,cwd=snapshot,env=environment,capture_output=True,timeout=120)
        if child.returncode!=0 or child.stderr:
            raise ValueError('COMPOSITE_CHILD_EXIT:'+str(child.returncode)+':'+child.stderr.decode(errors='replace')[:400])
        receipt=json.loads(child.stdout,object_pairs_hook=common.unique_object)
        if json.dumps(receipt,sort_keys=True)!=json.dumps(EXPECTED,sort_keys=True):
            raise ValueError('COMPOSITE_RECEIPT_MISMATCH')
        if any((snapshot/name).read_bytes()!=value for name,value in raw.items()):
            raise ValueError('SNAPSHOT_SOURCE_CHANGED')
    if Path(__file__).read_bytes()!=own:raise ValueError('ENTRYPOINT_CHANGED_DURING_REPLAY')
    return {'status':'COMPLETE_AUTHENTICATED_LOCAL_COMPOSITION','source_commit':BASE,
            'tested_checkout_sha':head,'sources':ids,'entrypoint_identity':common.identity(own),
            'command':command,'child_exit':child.returncode,'streams':{
                name:{'bytes':len(value),**common.identity(value),'text':value.decode()}
                for name,value in [('stdout',child.stdout),('stderr',child.stderr)]},
            'composite_receipt':receipt,'python':sys.version,'optimized':bool(sys.flags.optimize),
            'node_executable':node_path,'production_ready':False,'workflow_adopted':False,
            'scientific_acceptance':'NOT_RUN','historical_CI_authentication':'NOT_ESTABLISHED',
            'new_E2_E3':0,'human_rescoring':'NOT_RUN','CI':'NOT_RUN'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('repo',type=Path);p.add_argument('--node',default='node')
    a=p.parse_args()
    try:result=verify(a.repo,node=a.node)
    except (OSError,ValueError,KeyError,TypeError,UnicodeError,subprocess.SubprocessError)as exc:
        print(json.dumps({'status':'BLOCKED','production_ready':False,'reason':str(exc)[:500]}));return 1
    print(json.dumps(result,indent=2));return 0


if __name__=='__main__':sys.exit(main())
