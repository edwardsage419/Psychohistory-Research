#!/usr/bin/env python3
"""Exercise candidate shells in disposable clones/local bare remotes; no Actions."""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap

import prepare

HERE = Path(__file__).resolve().parent
OWN = 'research/codex_a/r127_workflow_candidate'
JOB = 'firstparty-1990-minimum-effort-and-2x2-risk-selection'


def exercise(repo, output):
    repo, output = Path(repo).resolve(), Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    records = []

    def command(tag, args, cwd, expected=0, env=None):
        child = subprocess.run(list(map(str,args)), cwd=cwd, capture_output=True, env=env, timeout=180)
        for suffix, raw in (('stdout',child.stdout),('stderr',child.stderr)):
            (output/(tag+'.'+suffix)).write_bytes(raw)
        records.append({'tag':tag,'argv':list(map(str,args)),'cwd':str(cwd),'exit':child.returncode,
                        'expected_exit':expected,'streams':{
                            name:{'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
                            for name,raw in (('stdout',child.stdout),('stderr',child.stderr))}})
        (output/'commands.json').write_text(json.dumps(records,indent=2)+'\n')
        if child.returncode != expected:
            raise ValueError(tag+':'+str(child.returncode)+':'+child.stdout.decode(errors='replace')[-400:]+child.stderr.decode(errors='replace')[-400:])
        return child

    def git(root, *args):return subprocess.check_output(['git','-C',str(root),*args],stderr=subprocess.PIPE).decode().strip()
    def clone(source, target):
        subprocess.run(['git','clone','--shared','--no-checkout',str(source),str(target)],check=True,capture_output=True)
        subprocess.run(['git','checkout','--detach',prepare.BASE],cwd=target,check=True,capture_output=True)

    with tempfile.TemporaryDirectory(prefix='r127-workflow-local-') as directory:
        temporary = Path(directory)
        baseline = temporary/'candidate'
        clone(repo,baseline)
        shutil.copytree(HERE,baseline/OWN,dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('__pycache__','receipts','*.tar.gz'))
        patch, manifest = prepare.build(baseline)
        (output/'candidate.patch').write_text(patch)
        (output/'candidate_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
        subprocess.run(['git','apply','--check','-'],input=patch.encode(),cwd=baseline,check=True,capture_output=True)
        subprocess.run(['git','apply','-'],input=patch.encode(),cwd=baseline,check=True,capture_output=True)
        subprocess.run(['git','add','--',OWN,prepare.WORKFLOW,prepare.GATE,prepare.PINS],cwd=baseline,check=True,capture_output=True)
        subprocess.run(['git','-c','user.name=Fixture','-c','user.email=fixture@example.invalid','commit','-qm','local candidate only [skip ci]'],cwd=baseline,check=True,capture_output=True)
        tested = git(baseline,'rev-parse','HEAD')
        # Preserve the exact disposable tested commit, with public BASE as a
        # prerequisite; do not present a deleted temp commit as a GitHub commit.
        subprocess.run(['git','bundle','create',str(output/'candidate.bundle'),'HEAD','^'+prepare.BASE],
                       cwd=baseline,check=True,capture_output=True)
        shell_blocks = [textwrap.dedent(x) for x in re.findall(r'        run: \|\n((?:          .*\n)+)',(baseline/prepare.WORKFLOW).read_text())]
        if len(shell_blocks) != 2:raise ValueError('CANDIDATE_SHELL_COVERAGE')
        result = {'base':prepare.BASE,'local_candidate':tested,'candidate_tree':git(baseline,'rev-parse','HEAD^{tree}'),
                  'CI':'NOT_RUN_LOCAL_SHELL_SIMULATION_ONLY','publication_remote_kind':'TEMP_LOCAL_BARE_ONLY','modes':[]}
        for optimized,label in ((False,'normal'),(True,'optimized')):
            work, remote = temporary/label, temporary/(label+'.git')
            subprocess.run(['git','clone','--shared',str(baseline),str(work)],check=True,capture_output=True)
            subprocess.run(['git','clone','--bare','--shared',str(baseline),str(remote)],check=True,capture_output=True)
            if not remote.is_relative_to(temporary):raise ValueError('NONLOCAL_TEST_REMOTE')
            subprocess.run(['git','--git-dir',str(remote),'update-ref','refs/heads/main',tested],check=True,capture_output=True)
            git(work,'remote','set-url','origin',str(remote))
            if git(work,'remote','get-url','origin') != str(remote):raise ValueError('UNSAFE_TEST_ORIGIN')
            env = os.environ.copy()
            env['PYTHONOPTIMIZE'] = '1' if optimized else '0'
            env.update(GITHUB_RUN_ID='1002' if optimized else '1001',GITHUB_RUN_ATTEMPT='1',
                       GITHUB_JOB=JOB,GITHUB_SHA=tested,GITHUB_REF='refs/heads/main')
            # Exact shell bodies from the candidate YAML, not Actions runner emulation.
            command(label+'-workflow-run',['bash','-c',shell_blocks[0]],work,env=env)
            rel = OWN+'/receipts/'+env['GITHUB_RUN_ID']+'-1-'+JOB+'.json'
            raw = (work/rel).read_bytes(); data = json.loads(raw)
            if data['execution']['unittest']['tests'] != 60 or data['execution']['stage2']['checked_leaf_fields'] != 138:
                raise ValueError('NATIVE_COUNTS')
            (output/(label+'-sidecar.json')).write_bytes(raw)
            first = json.loads(command(label+'-publish',['bash','-c',shell_blocks[1]],work,env=env).stdout)
            published = git(work,'rev-parse','HEAD')
            again = json.loads(command(label+'-publish-noop',['bash','-c',shell_blocks[1]],work,env=env).stdout)
            if first['status'] != 'PUBLISHED_IMMUTABLE_SIDECAR' or again['status'] != 'UNCHANGED_NOOP' or git(work,'rev-parse','HEAD') != published:
                raise ValueError('PUBLICATION_IDEMPOTENCE')
            if git(work,'diff','--name-only',tested,published) != rel:raise ValueError('PUBLICATION_CHANGED_OTHER_PATH')
            def reject(tag, altered, reason):
                (work/rel).write_text(json.dumps(altered,sort_keys=True,indent=2)+'\n')
                child = command(label+'-'+tag,['bash','-c',shell_blocks[1]],work,expected=1,env=env)
                failure = json.loads(child.stdout)
                if failure['status'] != 'BLOCKED' or reason not in failure['reason']:raise ValueError('WRONG_REJECTION:'+tag)
                (work/rel).write_bytes(raw)
                if git(work,'rev-parse','HEAD') != published:raise ValueError('FAILED_PUBLICATION_COMMITTED')
            changed = copy.deepcopy(data);changed['execution']['unittest']['tests'] = 59
            reject('wrong-count',changed,'FIELD_VALUE')
            changed = copy.deepcopy(data)
            stream = changed['execution']['commands'][0]['streams']['stderr']
            stream['text'] = 'Ran 60 tests in 0.1s\nFAILED (failures=1)\nOK\n'
            stream['bytes'] = len(stream['text'].encode());stream['sha256'] = hashlib.sha256(stream['text'].encode()).hexdigest()
            reject('trailing-fake-ok',changed,'FAILURE_MARKER')
            for tag,section,key,value in [('masked-e2','original','new_real_human_E2_prediction_scores',7),
                                          ('wrong-aggregate','original','source_reported_human_participants_not_reanalyzed',108),
                                          ('wrong-enumeration','audit','all_exact_individual_candidate_deviations',75118)]:
                changed = copy.deepcopy(data);stream = changed['execution']['commands'][1]['streams']['stdout']
                source = json.loads(stream['text']);source[section][key] = value
                stream['text'] = json.dumps(source)+'\n';stream['bytes'] = len(stream['text'].encode());stream['sha256'] = hashlib.sha256(stream['text'].encode()).hexdigest()
                reject(tag,changed,key)
            changed = copy.deepcopy(data);changed['context']['provider'] = 'local'
            reject('immutable-tracked-conflict',changed,'IMMUTABLE_TRACKED_RECEIPT_CONFLICT')
            other = work/'unrelated.txt';other.write_text('disposable staged control\n');git(work,'add','unrelated.txt')
            bad = command(label+'-unrelated-staged',['bash','-c',shell_blocks[1]],work,expected=1,env=env)
            if 'UNRELATED_DIRTY_OR_STAGED_PATH' not in json.loads(bad.stdout)['reason']:raise ValueError('STAGED_CONTROL')
            git(work,'reset','-q','--','unrelated.txt');other.unlink()
            # Competing write to the LOCAL bare main. No actual origin or HTTP remote is used.
            git(work,'commit','--allow-empty','-m','local competing actor [skip ci]')
            concurrent = git(work,'rev-parse','HEAD');git(work,'push','origin','HEAD:refs/heads/main')
            git(work,'update-ref','HEAD',published)
            bad = command(label+'-remote-advanced',['bash','-c',shell_blocks[1]],work,expected=1,env=env)
            if 'REMOTE_MAIN_ADVANCED' not in json.loads(bad.stdout)['reason']:raise ValueError('CONCURRENT_CONTROL')
            if git(work,'ls-remote','origin','refs/heads/main').split()[0] != concurrent:raise ValueError('CONCURRENT_WRITE_OVERWRITTEN')
            # Old publisher's unchanged historical receipt produces commit exit1.
            historic = 'research/R127/R127_PHASE_A_1990_ORIGINAL_MIN_EFFORT_60_TEST_75117_DEVIATIONS_1296_2X2_CI_ACCEPTANCE.json'
            command(label+'-historical-unconditional-commit',['bash','-c','git add '+historic+'\ngit commit -m "old noop control"'],work,expected=1,env=env)
            # Original source corruption is confined to this disposable copy, before any new sidecar.
            module = work/'research/R127/r127_van_huyck_1990_min_effort_coordination_selection_exact.py'
            original = module.read_bytes();module.write_bytes(original+b'\n# disposable source corruption\n')
            bad_env = env.copy();bad_env['GITHUB_RUN_ID'] = '2002' if optimized else '2001'
            blocked = command(label+'-source-corruption',['bash','-c',shell_blocks[0]],work,expected=1,env=bad_env)
            if 'SOURCE_IDENTITY' not in json.loads(blocked.stdout)['reason']:raise ValueError('SOURCE_CONTROL')
            module.write_bytes(original)
            if (work/(OWN+'/receipts/'+bad_env['GITHUB_RUN_ID']+'-1-'+JOB+'.json')).exists():raise ValueError('FAILED_GATE_WROTE_SIDECAR')
            for path in json.loads((repo/'research/codex_a/r127_local_gates/pins.json').read_text()):
                if path == prepare.WORKFLOW:continue
                if git(work,'rev-parse','HEAD:'+path) != git(repo,'rev-parse',prepare.BASE+':'+path):raise ValueError('HISTORICAL_SOURCE_CHANGED')
            result['modes'].append({'optimized':optimized,'native_original_methods':60,'stage2_fields':138,
                                    'published_only':rel,'published_commit':published,'noop_commit_unchanged':True,
                                    'adversarial_rejections':9,'old_noop_commit_exit':1,
                                    'historical_receipt_unchanged':True,'context_ids':'SYNTHETIC_LOCAL_CLAIMS_NOT_GITHUB_RUNS'})
        result['all_expectations_match'] = True
        (output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
        return result


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('repo',type=Path);parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    print(json.dumps(exercise(args.repo,args.output),indent=2))
