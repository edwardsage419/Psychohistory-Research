#!/usr/bin/env python3
"""Independent R272 candidate workflow contract, offline and read-only.

Uses PyYAML if already installed. This gate is for the exact proposed workflow
and is not evidence of a production installation or a real CI run.
"""
import argparse
from pathlib import Path
import sys

try:
    import yaml
except ImportError as exc:
    raise SystemExit('NOT_RUN: PyYAML unavailable; no package installation authorized') from exc

CANDIDATE = 'research/validation/r272_single_entrypoint_caller_candidate_20261103.yml'
RUNNER = 'python research/validation/r272_single_entrypoint_failclosed_20261102.py --root .'
REQUIRED = {
    'research/R272/**',
    'protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md',
    'research/validation/R272_P0_FAILCLOSED_CANDIDATE_20261102.zip',
    'research/validation/r272_preimage_first_readonly_gate_20261102.py',
    'research/validation/r272_pinned_native_replay_and_preimage_negative_20261102.py',
    'research/validation/r272_single_entrypoint_failclosed_20261102.py',
    'research/validation/r272_single_entrypoint_workflow_contract_20261103.py',
    '.github/workflows/r272-exact-train-test-oos-e1.yml',
}

# PyYAML YAML 1.1 interprets 'on' as True; normalize that specific parser quirk.
def parse(raw):
    result = yaml.safe_load(raw)
    if isinstance(result, dict) and True in result and 'on' not in result:
        result['on'] = result.pop(True)
    return result


def verify(raw):
    d = parse(raw)
    if not isinstance(d, dict) or set(d) != {'name', 'on', 'permissions', 'jobs'}:
        raise ValueError('unexpected top-level keys')
    if d['permissions'] != {'contents': 'read'}:
        raise ValueError('permissions are not read-only')
    on = d['on']
    if not isinstance(on, dict) or set(on) != {'push', 'pull_request'}:
        raise ValueError('both automatic event types are required')
    for event in ('push', 'pull_request'):
        config = on[event]
        if not isinstance(config, dict) or set(config) != {'paths'}:
            raise ValueError('unexpected event config: ' + event)
        paths = config['paths']
        if not isinstance(paths, list) or len(paths) != len(REQUIRED) or set(paths) != REQUIRED:
            raise ValueError('required path trigger missing or added')
    jobs = d['jobs']
    if not isinstance(jobs, dict) or set(jobs) != {'r272-mandatory-acceptance'}:
        raise ValueError('unexpected jobs')
    job = jobs['r272-mandatory-acceptance']
    if set(job) != {'runs-on', 'timeout-minutes', 'strategy', 'steps'}:
        raise ValueError('unexpected job controls')
    if job['runs-on'] != 'ubuntu-latest' or job['timeout-minutes'] != 30:
        raise ValueError('runner or timeout changed')
    if job['strategy'] != {'matrix': {'python-version': ['3.11', '3.12']}}:
        raise ValueError('Python matrix changed')
    steps = job['steps']
    if not isinstance(steps, list) or len(steps) != 3:
        raise ValueError('unexpected steps')
    if steps[0] != {'uses': 'actions/checkout@v4'}:
        raise ValueError('checkout step changed')
    if steps[1] != {'uses': 'actions/setup-python@v5',
                    'with': {'python-version': '${{ matrix.python-version }}'}}:
        raise ValueError('setup-python step changed')
    if steps[2] != {'name': 'Mandatory authenticated preimage and native negative acceptance',
                    'run': RUNNER}:
        raise ValueError('mandatory single-command step changed')
    return True


def selftest(raw):
    if verify(raw) is not True:
        raise ValueError('baseline workflow rejected')
    mutations = {
        'skip_job': raw.replace('    runs-on: ubuntu-latest', '    if: false\n    runs-on: ubuntu-latest'),
        'skip_step': raw.replace('        run: ' + RUNNER, '        if: false\n        run: ' + RUNNER),
        'early_exit': raw.replace('        run: ' + RUNNER, '        run: exit 0'),
        'shell_override': raw.replace('        run: ' + RUNNER, '        shell: bash\n        run: ' + RUNNER),
        'continue_on_error': raw.replace('        run: ' + RUNNER, '        continue-on-error: true\n        run: ' + RUNNER),
        'selftest_only': raw.replace('--root .', '--selftest'),
        'write_token': raw.replace('contents: read', 'contents: write'),
        'missing_runner_trigger': raw.replace("      - 'research/validation/r272_single_entrypoint_failclosed_20261102.py'\n", ''),
        'missing_pull_request': raw.replace('  pull_request:', '  workflow_dispatch:'),
        'extra_job': raw + '\n  extra: {}\n',
        'remove_checkout': raw.replace('      - uses: actions/checkout@v4', '      - run: echo skipped'),
        'python_matrix': raw.replace("['3.11', '3.12']", "['3.11']"),
    }
    results = {}
    for name, mutant in mutations.items():
        if mutant == raw:
            raise AssertionError('mutation did not change source: ' + name)
        try:
            verify(mutant)
        except (ValueError, yaml.YAMLError, TypeError, KeyError):
            results[name] = 'REJECT'
        else:
            raise AssertionError('mutation falsely accepted: ' + name)
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('candidate', nargs='?', default=CANDIDATE)
    args = parser.parse_args()
    raw = Path(args.candidate).read_text(encoding='utf-8')
    results = selftest(raw)
    print('PASS: baseline and %d/%d mutations rejected' % (len(results), len(results)))
    print(', '.join(sorted(results)))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, yaml.YAMLError, TypeError, KeyError, AssertionError) as exc:
        raise SystemExit('FAIL: ' + str(exc)) from exc
