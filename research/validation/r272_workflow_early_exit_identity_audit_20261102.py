#!/usr/bin/env python3
"""Fail-closed R272 workflow identity and early-exit mutation audit.

Offline, nonblind engineering check. No CI dispatch.
Archived checker is imported only to measure its static sensitivity.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

CANDIDATE = 'research/validation/r272_mandatory_acceptance_proposal_20261102.yml'
ACTIVE = '.github/workflows/r272-exact-train-test-oos-e1.yml'
OLD_CHECKER = 'research/validation/r272_proposed_caller_structural_gate_20261102.py'
CANDIDATE_BLOB = 'fe7165cf0dfe1de12664ddfbcf4360b73c29a518'
ACTIVE_OLD_BLOB = '3132b08cf4ee64b55f5112d2249894ea0ec9d42d'
ANCHOR = ('          python research/validation/r272_preimage_first_readonly_gate_20261102.py '
          '--root . --gate research/validation/r272_failclosed_independent_receipt_gate_20261102.py '
          '--regenerate')


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def require(condition: bool, why: str) -> None:
    if not condition:
        raise ValueError(why)


def insert_exit(raw: str, occurrence: int) -> str:
    """Insert an unconditional successful shell exit ahead of a required audit."""
    positions = []
    start = 0
    while True:
        at = raw.find(ANCHOR, start)
        if at == -1:
            break
        positions.append(at)
        start = at + len(ANCHOR)
    require(len(positions) == 2, f'expected two mandatory audit anchors, got {len(positions)}')
    at = positions[occurrence]
    return raw[:at] + '          exit 0\n' + raw[at:]


def load_checker(path: Path):
    spec = importlib.util.spec_from_file_location('r272_archived_static_gate', path)
    require(spec is not None and spec.loader is not None, 'checker import unavailable')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def identity_check(candidate: bytes, installed: bytes | None = None) -> dict:
    require(git_blob(candidate) == CANDIDATE_BLOB, 'candidate bytes changed from reviewed Git blob')
    if installed is not None:
        require(installed == candidate, 'active workflow differs from reviewed candidate')
    return {'status': 'PASS', 'candidate_blob': CANDIDATE_BLOB,
            'adopted_workflow_exact_match': installed is not None}


def audit(root: Path) -> dict:
    root = root.resolve(strict=True)
    candidate_bytes = (root / CANDIDATE).read_bytes()
    old_bytes = (root / ACTIVE).read_bytes()
    checker_path = root / OLD_CHECKER
    require(git_blob(old_bytes) == ACTIVE_OLD_BLOB,
            'production workflow has changed; re-review latest workflow before conclusions')
    identity_check(candidate_bytes)
    candidate = candidate_bytes.decode('utf-8')
    old = load_checker(checker_path)
    old.check(candidate)
    cases = {
        'bypass_preimage_first_step': insert_exit(candidate, 0),
        'bypass_final_archive_step': insert_exit(candidate, 1),
    }
    cases['bypass_both_historical_preimage_paths'] = insert_exit(cases['bypass_preimage_first_step'], 1)
    findings = {}
    for label, changed in cases.items():
        require(changed != candidate, 'empty mutation')
        try:
            old.check(changed)
            old_accepted = True
        except ValueError:
            old_accepted = False
        try:
            identity_check(changed.encode('utf-8'))
            identity_rejected = False
        except ValueError:
            identity_rejected = True
        require(old_accepted and identity_rejected, 'mutation sensitivity mismatch: ' + label)
        findings[label] = {'archived_static_checker_accepted': old_accepted,
                           'pinned_identity_gate_rejected': identity_rejected}
    try:
        identity_check(candidate_bytes, old_bytes)
        adopted = True
    except ValueError:
        adopted = False
    require(not adopted, 'current production workflow unexpectedly matches proposal; re-review adoption')
    return {'status': 'PASS_BOUNDED_AUDIT', 'scope': 'STATIC_NONBLIND_CANDIDATE_ONLY',
            'candidate_git_blob': git_blob(candidate_bytes),
            'active_workflow_git_blob': git_blob(old_bytes),
            'mutations': findings, 'old_checker_false_acceptances': len(findings),
            'active_workflow_matches_reviewed_proposal': adopted,
            'historical_ci_or_native_workflow_executed': False,
            'scientific_acceptance': 'OPEN'}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path('.'))
    args = parser.parse_args()
    print(json.dumps(audit(args.root), sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, ImportError) as exc:
        sys.exit('FAIL: ' + str(exc))
