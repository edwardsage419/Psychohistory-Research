#!/usr/bin/env python3
"""Offline R272 enforcement audit. Takes only recorded public GitHub metadata.

No network calls, CI dispatch, repository edits or third-party dependencies.
The result describes one recorded snapshot, never future GitHub state.
"""
import argparse
import copy
import json
from pathlib import Path

PATHS = (
    'research/R272/R272_MACHINE_RECEIPT.json',
    'research/R272/R272_EXACT_RESULTS.json',
    'protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md',
    'research/validation/r272_single_entrypoint_failclosed_20261102.py',
    'research/R272/r272_exact_train_test_prediction.py',
    '.github/workflows/r272-exact-train-test-oos-e1.yml',
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def matched(path, patterns):
    return any(path == p or (p.endswith('/**') and path.startswith(p[:-2]))
               for p in patterns)


def evaluate(snapshot):
    branch = snapshot['branch']
    checks = branch['required_status_checks']
    if snapshot['rulesets']:
        rule_status = 'UNDETERMINED_NONEMPTY_RULESETS'
    else:
        rule_status = 'NONE_RETURNED'
    enforced = (branch['protected'] is True
                and checks['enforcement_level'] != 'off'
                and bool(checks['contexts'] or checks['checks']))
    matrix = []
    for path in PATHS:
        matrix.append({'path': path,
                       'production_push': matched(path, snapshot['production']['push_paths']),
                       'candidate_push': matched(path, snapshot['candidate']['push_paths']),
                       'candidate_pr': matched(path, snapshot['candidate']['pull_request_paths'])})
    return {'main_head': snapshot['main_head'],
            'branch_protected': branch['protected'],
            'branch_required_status_checks_enforced': enforced,
            'rulesets': rule_status,
            'production_pull_request_event': 'pull_request' in snapshot['production']['events'],
            'candidate_pull_request_event': 'pull_request' in snapshot['candidate']['events'],
            'production_job_count': len(snapshot['production']['jobs']),
            'candidate_job_count': len(snapshot['candidate']['jobs']),
            'frozen_three_job_requirement': snapshot['freeze']['three_jobs'],
            'path_matrix': matrix}


def selftest(snapshot):
    base = evaluate(snapshot)
    require(base['branch_protected'] is False, 'observed branch unexpectedly protected')
    require(base['branch_required_status_checks_enforced'] is False, 'unexpected branch checks')
    require(base['rulesets'] == 'NONE_RETURNED', 'rulesets present')
    require(base['production_pull_request_event'] is False, 'production PR event differs')
    require(base['candidate_pull_request_event'] is True, 'candidate PR event missing')
    require(sum(x['production_push'] for x in base['path_matrix']) == 2, 'production trigger coverage differs')
    require(sum(x['candidate_push'] for x in base['path_matrix']) == 6, 'candidate trigger coverage differs')
    changed = copy.deepcopy(snapshot)
    changed['branch']['protected'] = True
    require(evaluate(changed)['branch_required_status_checks_enforced'] is False, 'protected without checks accepted')
    changed['branch']['required_status_checks'] = {
        'enforcement_level': 'non_admins', 'contexts': ['r272-mandatory-acceptance'], 'checks': []}
    require(evaluate(changed)['branch_required_status_checks_enforced'] is True, 'positive check not detected')
    changed['rulesets'] = [{'id': 1}]
    require(evaluate(changed)['rulesets'] == 'UNDETERMINED_NONEMPTY_RULESETS', 'unknown rulesets ignored')
    return {'status': 'PASS', 'checks': 10, 'scope': 'OFFLINE_METADATA_AND_TRIGGER_PATTERN'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('snapshot', type=Path)
    args = parser.parse_args()
    data = json.loads(args.snapshot.read_text(encoding='utf-8'))
    print(json.dumps({'evaluation': evaluate(data), 'selftest': selftest(data)},
                     ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
