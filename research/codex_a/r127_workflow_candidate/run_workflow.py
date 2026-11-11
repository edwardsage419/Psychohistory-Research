#!/usr/bin/env python3
"""Candidate CI entry: reuse gate26, write only a new immutable run sidecar."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys

OWN = 'research/codex_a/r127_workflow_candidate'
GATE_DIR = 'research/codex_a/r127_local_gates'
RUN_PATH = OWN+'/run_workflow.py'
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'r127_local_gates'))
import gate

EXEC_KEYS = {'tested_checkout_sha', 'sources', 'gate_identity', 'pin_manifest_sha256',
             'workflow_git_blob', 'unittest', 'stage2', 'commands', 'python', 'optimized',
             'new_real_person_level_E2_prediction_scores'}
LIMITS = {'scientific_acceptance': 'NOT_EVALUATED', 'catalogue_05_003_closure': 'NOT_EVALUATED',
          'historical_run_authentication': 'NOT_ESTABLISHED', 'new_E2_E3': 0,
          'R073': 'FROZEN_UNCHANGED', 'PESEN_v0_1': 'FROZEN_UNCHANGED'}


def context(run_id, attempt, job_key, provider):
    gate.require(type(run_id) is str and re.fullmatch(r'[1-9][0-9]{0,31}', run_id), 'RUN_ID')
    gate.require(type(attempt) is str and re.fullmatch(r'[1-9][0-9]{0,8}', attempt), 'RUN_ATTEMPT')
    gate.require(type(job_key) is str and re.fullmatch(r'[A-Za-z_][A-Za-z0-9_-]{0,119}', job_key), 'JOB_KEY')
    gate.require(provider in ('local', 'github-actions'), 'CONTEXT_PROVIDER')
    return {'run_id': run_id, 'attempt': attempt, 'job_key': job_key, 'provider': provider,
            'numeric_job_id': None, 'externally_attested': False}


def receipt_name(ctx):
    gate.same(ctx, context(ctx['run_id'], ctx['attempt'], ctx['job_key'], ctx['provider']))
    return OWN+'/receipts/'+ctx['run_id']+'-'+ctx['attempt']+'-'+ctx['job_key']+'.json'


def safe_path(root, ctx, create=False):
    root = Path(root).resolve()
    path = root/receipt_name(ctx)
    cursor = root
    for part in path.relative_to(root).parts[:-1]:
        cursor = cursor/part
        if cursor.is_symlink():raise ValueError('SYMLINK_RECEIPT_PARENT')
        if create:cursor.mkdir(exist_ok=True)
    return path


def store(root, ctx, raw):
    path = safe_path(root, ctx, create=True)
    try:
        info = path.lstat()
    except FileNotFoundError:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
        with os.fdopen(fd, 'wb') as target:target.write(raw)
        return path, 'CREATED'
    gate.require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, 'UNSAFE_RECEIPT_TARGET')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as target:
        current = os.fstat(target.fileno())
        gate.require(stat.S_ISREG(current.st_mode) and current.st_nlink == 1, 'UNSAFE_RECEIPT_TARGET')
        gate.require(target.read() == raw, 'IMMUTABLE_RECEIPT_CONFLICT')
    return path, 'UNCHANGED'


def git(root, *args):
    try:return subprocess.check_output(['git', '-C', str(root), *args], stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as exc:
        raise ValueError('GIT_OPERATION_FAILED:'+args[0]+':'+exc.stderr.decode(errors='replace')[:300]) from exc


def tracked(root, name):
    raw = (Path(root)/name).read_bytes()
    gate.require(gate.identity(raw)['git_blob'] == git(root, 'rev-parse', 'HEAD:'+name).decode().strip(),
                 'UNTRACKED_OR_CHANGED_EXECUTABLE:'+name)
    return raw


def validate_record(root, record):
    gate.require(type(record) is dict and set(record) == {'status', 'context', 'execution',
                 'entrypoint_identity', 'limits'}, 'SIDECAR_SCHEMA')
    gate.require(record['status'] == 'COMPLETE_R127_CANDIDATE_CHECKS', 'SIDECAR_STATUS')
    ctx = record['context']
    receipt_name(ctx)
    execution = record['execution']
    gate.require(type(execution) is dict and set(execution) == EXEC_KEYS, 'EXECUTION_SCHEMA')
    sha = execution['tested_checkout_sha']
    gate.require(type(sha) is str and re.fullmatch('[0-9a-f]{40}', sha), 'CHECKOUT_SHA')
    pin_raw = git(root, 'show', sha+':'+GATE_DIR+'/pins.json')
    pins = gate.load_json(pin_raw)
    canonical = gate.load_json((gate.HERE/'pins.json').read_bytes())
    gate.require(set(pins) == set(canonical) and all(pins[k] == canonical[k] for k in pins if k != gate.WORKFLOW),
                 'FROZEN_SOURCE_PINS')
    identities = {}
    for name, pin in pins.items():
        identities[name] = gate.identity(git(root, 'show', sha+':'+name))
        gate.same(identities[name], pin, 'source.'+name)
    gate.same(execution['sources'], identities, 'sources')
    gate.require(execution['pin_manifest_sha256'] == hashlib.sha256(pin_raw).hexdigest() and
                 execution['workflow_git_blob'] == pins[gate.WORKFLOW]['git_blob'], 'WORKFLOW_PIN_BINDING')
    gate.same(execution['gate_identity'], gate.identity(git(root, 'show', sha+':'+GATE_DIR+'/gate.py')))
    gate.same(record['entrypoint_identity'], gate.identity(git(root, 'show', sha+':'+RUN_PATH)))
    commands = execution['commands']
    gate.require(type(commands) is list and len(commands) == 2, 'COMMAND_COVERAGE')
    for child in commands:
        gate.require(type(child) is dict and type(child.get('exit')) is int and child['exit'] == 0,
                     'CHILD_EXIT')
        gate.require(type(child.get('command')) is list and child['command'] and
                     all(type(v) is str for v in child['command']) and type(child.get('cwd')) is str, 'COMMAND_FIELDS')
        gate.require(type(child.get('streams')) is dict and set(child['streams']) == {'stdout','stderr'}, 'STREAM_COVERAGE')
        for stream in child['streams'].values():
            gate.require(type(stream) is dict and type(stream.get('text')) is str, 'STREAM_TEXT')
            raw = stream['text'].encode('utf-8')
            gate.same(stream, {'text':stream['text'], 'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()})
    gate.require(not commands[0]['streams']['stdout']['text'] and not commands[1]['streams']['stderr']['text'], 'UNEXPECTED_STREAM')
    parsed = gate.parse_test_log(commands[0]['streams']['stderr']['text'].encode(), commands[0]['exit'])
    gate.same(execution['unittest'], parsed, 'unittest')
    checked = gate.validate_stage2(gate.load_json(commands[1]['streams']['stdout']['text']),
                                  gate.load_json(git(root, 'show', sha+':'+gate.RECEIPT)))
    gate.same(execution['stage2'], checked, 'stage2')
    gate.same(execution['new_real_person_level_E2_prediction_scores'], checked['new_real_person_level_E2_prediction_scores'])
    gate.require(type(execution['python']) is str and type(execution['optimized']) is bool, 'RUNTIME_FIELDS')
    gate.same(record['limits'], LIMITS, 'limits')
    return ctx


def run(root, ctx):
    root = Path(root).resolve()
    own = tracked(root, RUN_PATH)
    tracked(root, GATE_DIR+'/gate.py')
    tracked(root, GATE_DIR+'/pins.json')
    execution = gate.verify(root)
    gate.require(execution['status'] == 'COMPLETE_LOCAL_R127_ENGINEERING_REPLAY', 'GATE_STATUS')
    record = {'status':'COMPLETE_R127_CANDIDATE_CHECKS', 'context':ctx,
              'execution':{key:execution[key] for key in EXEC_KEYS},
              'entrypoint_identity':gate.identity(own), 'limits':LIMITS}
    validate_record(root, record)
    gate.require(Path(__file__).read_bytes() == own, 'ENTRYPOINT_CHANGED_DURING_RUN')
    path, state = store(root, ctx, (json.dumps(record, sort_keys=True, indent=2)+'\n').encode())
    return {'status':'COMPLETE_R127_CANDIDATE_CHECKS','receipt':str(path.relative_to(root)),
            'write_state':state,'receipt_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'scientific_acceptance':'NOT_EVALUATED','context_externally_attested':False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--attempt', required=True)
    parser.add_argument('--job-key', required=True)
    parser.add_argument('--context', choices=('local','github-actions'), default='local')
    args = parser.parse_args()
    try:result = run(args.root, context(args.run_id,args.attempt,args.job_key,args.context))
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status':'BLOCKED','reason':str(exc)[:400]}));return 1
    print(json.dumps(result, indent=2));return 0


if __name__ == '__main__':sys.exit(main())
