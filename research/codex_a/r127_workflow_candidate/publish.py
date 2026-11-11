#!/usr/bin/env python3
"""Candidate publisher: immutable sidecar only, no rebase/force/history rewrite."""
import argparse
import hashlib
import json
from pathlib import Path
import stat
import subprocess
import sys

import run_workflow as runner


def remote_head(root, remote):
    lines = runner.git(root, 'ls-remote', remote, 'refs/heads/main').decode().splitlines()
    runner.gate.require(len(lines) == 1, 'REMOTE_MAIN_UNAVAILABLE')
    return lines[0].split()[0]


def publish(root, receipt, expected, remote):
    root = Path(root).resolve()
    runner.tracked(root, runner.OWN+'/publish.py')
    runner.tracked(root, runner.RUN_PATH)
    runner.tracked(root, runner.GATE_DIR+'/gate.py')
    runner.tracked(root, runner.GATE_DIR+'/pins.json')
    path = root/receipt
    info = path.lstat()
    runner.gate.require(stat.S_ISREG(info.st_mode) and info.st_nlink == 1, 'UNSAFE_RECEIPT_TARGET')
    raw = path.read_bytes()
    data = runner.gate.load_json(raw)
    ctx = runner.validate_record(root, data)
    runner.gate.require(receipt == runner.receipt_name(ctx) and runner.safe_path(root,ctx) == path,
                        'RECEIPT_PATH_BINDING')
    runner.gate.require(data['execution']['tested_checkout_sha'] == expected, 'EXPECTED_CHECKOUT_BINDING')
    dirty = runner.git(root,'status','--porcelain','--untracked-files=all').decode().splitlines()
    runner.gate.require(all(line[3:] == receipt for line in dirty), 'UNRELATED_DIRTY_OR_STAGED_PATH')
    head = runner.git(root,'rev-parse','HEAD').decode().strip()
    exists = subprocess.run(['git','-C',str(root),'cat-file','-e','HEAD:'+receipt],capture_output=True).returncode == 0
    if exists:
        runner.gate.require(runner.git(root,'show','HEAD:'+receipt) == raw, 'IMMUTABLE_TRACKED_RECEIPT_CONFLICT')
        runner.gate.require(remote_head(root,remote) == head, 'REMOTE_MAIN_ADVANCED')
        return {'status':'UNCHANGED_NOOP','commit':head,'receipt_sha256':hashlib.sha256(raw).hexdigest()}
    runner.gate.require(head == expected and remote_head(root,remote) == expected, 'REMOTE_MAIN_ADVANCED')
    runner.git(root,'add','--',receipt)
    runner.git(root,'commit','-m','results(R127): immutable validated run sidecar [skip ci]')
    commit = runner.git(root,'rev-parse','HEAD').decode().strip()
    runner.gate.require(remote_head(root,remote) == expected, 'REMOTE_MAIN_ADVANCED_AFTER_COMMIT')
    runner.git(root,'push',remote,'HEAD:refs/heads/main')
    runner.gate.require(remote_head(root,remote) == commit, 'REMOTE_READBACK_MISMATCH')
    return {'status':'PUBLISHED_IMMUTABLE_SIDECAR','commit':commit,
            'tested_checkout':expected,'receipt_sha256':hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path)
    parser.add_argument('--receipt',required=True)
    parser.add_argument('--expected-head',required=True)
    parser.add_argument('--remote',required=True)
    parser.add_argument('--allow-push',action='store_true',required=True)
    args = parser.parse_args()
    try:result = publish(args.root,args.receipt,args.expected_head,args.remote)
    except (OSError,ValueError,KeyError,TypeError,subprocess.SubprocessError) as exc:
        print(json.dumps({'status':'BLOCKED','reason':str(exc)[:400]}));return 1
    print(json.dumps(result,indent=2));return 0


if __name__ == '__main__':sys.exit(main())
