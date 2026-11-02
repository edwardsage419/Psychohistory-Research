#!/usr/bin/env python3
"""R272 candidate caller bypass review. Read-only, no Actions dispatch.

Run from repository root with Python and an existing PyYAML installation.
The historical checker is loaded only to measure its structural sensitivity.
This review independently checks the execution controls it does not inspect.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import yaml

PROPOSAL = Path('research/validation/r272_mandatory_acceptance_proposal_20261102.yml')
OLD_CHECKER = Path('research/validation/r272_proposed_caller_structural_gate_20261102.py')


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def load_old_checker(path: Path):
    spec = importlib.util.spec_from_file_location('r272_existing_static_checker', path)
    require(spec is not None and spec.loader is not None, 'checker cannot be loaded')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def independent_execution_controls(raw: str) -> dict:
    document = yaml.safe_load(raw)
    require(isinstance(document, dict), 'invalid workflow')
    jobs = document.get('jobs')
    require(isinstance(jobs, dict) and len(jobs) == 3, 'three jobs required')
    steps_seen = 0
    for job_name, job in jobs.items():
        require(isinstance(job, dict), 'invalid job: ' + job_name)
        require('if' not in job, 'conditional job may skip mandatory acceptance: ' + job_name)
        require('continue-on-error' not in job, 'conditional job failure policy')
        steps = job.get('steps')
        require(isinstance(steps, list) and steps, 'missing steps: ' + job_name)
        for number, step in enumerate(steps):
            require(isinstance(step, dict), 'invalid step')
            require('if' not in step, f'conditional step may skip acceptance: {job_name}/{number}')
            require('continue-on-error' not in step, 'step may suppress failure')
            # A custom shell template can omit errexit and let an early failure
            # be masked by a later successful command in a multiline run.
            require('shell' not in step, f'unreviewed custom shell: {job_name}/{number}')
            steps_seen += 1
    return {'status': 'PASS', 'jobs': len(jobs), 'steps': steps_seen}


def replace_once(raw: str, old: str, new: str) -> str:
    require(raw.count(old) == 1, 'mutation anchor missing or ambiguous: ' + old)
    return raw.replace(old, new, 1)


def mutants(raw: str) -> dict[str, str]:
    false_if = 'if: ' + '$' + '{{ false }}'
    return {
        'skip_preimage_job': replace_once(raw, '  preimage-first:\n',
                                           '  preimage-first:\n    ' + false_if + '\n'),
        'skip_preimage_audit_step': replace_once(
            raw, '      - name: Mandatory pinned preimage audit and isolated regeneration',
            '      - ' + false_if + '\n        name: Mandatory pinned preimage audit and isolated regeneration'),
        'skip_original_tests_step': replace_once(
            raw, '      - name: Original 83 unit tests, with independent acceptance prerequisite',
            '      - ' + false_if + '\n        name: Original 83 unit tests, with independent acceptance prerequisite'),
        'skip_archive_job': replace_once(raw, '  independent-sources-and-archive:\n',
                                         '  independent-sources-and-archive:\n    ' + false_if + '\n'),
        'all_jobs_skipped': replace_once(
            replace_once(replace_once(raw, '  preimage-first:\n',
                                      '  preimage-first:\n    ' + false_if + '\n'),
                         '  dual-python-tests:\n',
                         '  dual-python-tests:\n    ' + false_if + '\n'),
            '  independent-sources-and-archive:\n',
            '  independent-sources-and-archive:\n    ' + false_if + '\n'),
        'disable_errexit': replace_once(
            raw, '      - name: Mandatory pinned preimage audit and isolated regeneration',
            '      - shell: bash {0}\n        name: Mandatory pinned preimage audit and isolated regeneration'),
    }


def audit(proposal: Path = PROPOSAL, checker: Path = OLD_CHECKER) -> dict:
    raw = proposal.read_text(encoding='utf-8')
    old = load_old_checker(checker)
    old.check(raw)
    independent_execution_controls(raw)
    cases = {}
    for name, modified in mutants(raw).items():
        require(modified != raw, 'empty mutation: ' + name)
        try:
            old.check(modified)
            old_accepted = True
        except (ValueError, yaml.YAMLError):
            old_accepted = False
        try:
            independent_execution_controls(modified)
            independent_rejected = False
        except (ValueError, yaml.YAMLError):
            independent_rejected = True
        require(independent_rejected, 'independent check missed mutation: ' + name)
        cases[name] = {'existing_checker_accepted': old_accepted,
                       'independent_control_rejected': independent_rejected}
    return {'status': 'PASS', 'scope': 'STATIC_NONBLIND_PROPOSAL_ONLY',
            'mutations': len(cases),
            'existing_checker_false_acceptances': sum(v['existing_checker_accepted'] for v in cases.values()),
            'cases': cases, 'actions_executed': False, 'scientific_E1_acceptance': False}


if __name__ == '__main__':
    try:
        print(json.dumps(audit(), sort_keys=True))
    except (ValueError, OSError, yaml.YAMLError) as exc:
        raise SystemExit('FAIL: ' + str(exc)) from exc
