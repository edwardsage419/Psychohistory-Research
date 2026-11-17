#!/usr/bin/env python3
"""Print an exact candidate patch; never applies it or edits protected files."""
import argparse
import difflib
import hashlib
import json
from pathlib import Path
import subprocess
import sys

BASE = 'ce6ae2dbf96f5346cf5062de3773b72c0ab90446'
HERE = Path(__file__).resolve().parent
WORKFLOW = '.github/workflows/r127-van-huyck-1990-coordination-source-table-60-tests.yml'
GATE = 'research/codex_a/r127_local_gates/gate.py'
PINS = 'research/codex_a/r127_local_gates/pins.json'


def identity(raw):
    return {'git_blob': hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),
            'sha256': hashlib.sha256(raw).hexdigest()}


def build(repo):
    repo = Path(repo)
    before = {name: subprocess.check_output(['git', '-C', str(repo), 'show', BASE+':'+name])
              for name in (WORKFLOW, GATE, PINS)}
    after = {WORKFLOW: (HERE/'workflow.template.yml').read_bytes()}
    pins = json.loads(before[PINS])
    pins[WORKFLOW] = identity(after[WORKFLOW])
    after[PINS] = (json.dumps(pins, indent=2)+'\n').encode()
    old = hashlib.sha256(before[PINS]).hexdigest()
    new = hashlib.sha256(after[PINS]).hexdigest()
    text = before[GATE].decode()
    needle = "PIN_MANIFEST_SHA256 = '"+old+"'"
    if text.count(needle) != 1:raise ValueError('BASE_GATE_PREIMAGE')
    after[GATE] = text.replace(needle, "PIN_MANIFEST_SHA256 = '"+new+"'").encode()
    observed = {name: (repo/name).read_bytes() for name in before}
    if observed == before:state = 'BASE_MATCHES'
    elif observed == after:state = 'ALREADY_APPLIED'
    else:raise ValueError('STALE_OR_PARTIAL_TARGET_REFUSE_OVERWRITE')
    patch = '' if state == 'ALREADY_APPLIED' else ''.join(
        ''.join(difflib.unified_diff(before[name].decode().splitlines(keepends=True),
                                    after[name].decode().splitlines(keepends=True),
                                    fromfile='a/'+name, tofile='b/'+name))
        for name in before)
    manifest = {'base': BASE, 'state': state, 'targets': {
        name: {'before': identity(before[name]), 'after': identity(after[name])} for name in before},
        'original_research_files_changed': False, 'production_applied': False,
        'scientific_acceptance': 'NOT_RUN', 'CI': 'NOT_RUN'}
    return patch, manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', type=Path)
    parser.add_argument('--manifest', action='store_true')
    args = parser.parse_args()
    try:patch, manifest = build(args.repo)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status': 'BLOCKED', 'reason': str(exc)[:240]}), file=sys.stderr)
        return 1
    print(json.dumps(manifest, indent=2) if args.manifest else patch, end='\n' if args.manifest else '')
    return 0


if __name__ == '__main__':sys.exit(main())
