#!/usr/bin/env python3
"""Conservative static guard for the unadopted R272 workflow proposal.

Requires existing PyYAML (tested 6.0.3); no CI or network activity.
This is a proposal lint, not a substitute for native workflow execution.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import yaml

ZIP_HASH = 'f23b04706b60ac70bdbee6f051a74551779fb9d9a9b9af08c96cda345b055151'
REQUIRED_PATHS = {
    'research/R272/**',
    'protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md',
    'research/validation/R272_P0_FAILCLOSED_CANDIDATE_20261102.zip',
    'research/validation/r272_preimage_first_readonly_gate_20261102.py',
    'research/validation/r272_pinned_native_replay_and_preimage_negative_20261102.py',
    '.github/workflows/r272-exact-train-test-oos-e1.yml',
}


def require(ok: bool, why: str) -> None:
    if not ok:
        raise ValueError(why)


def check(raw: str) -> dict:
    doc = yaml.safe_load(raw)
    require(isinstance(doc, dict), 'YAML root must be mapping')
    # YAML 1.1 PyYAML resolves the bare key "on" to Boolean True.
    events = doc.get('on', doc.get(True))
    require(isinstance(events, dict) and 'workflow_dispatch' in events, 'missing events')
    push = events.get('push')
    require(isinstance(push, dict), 'missing push trigger')
    paths = push.get('paths')
    require(isinstance(paths, list) and REQUIRED_PATHS <= set(paths), 'missing watched input')
    require(doc.get('permissions') == {'contents': 'read'}, 'workflow must be read only')
    jobs = doc.get('jobs')
    require(isinstance(jobs, dict), 'jobs missing')
    require(set(jobs) == {'preimage-first', 'dual-python-tests', 'independent-sources-and-archive'},
            'expected three mandatory jobs')
    pre = jobs['preimage-first']
    dual = jobs['dual-python-tests']
    third = jobs['independent-sources-and-archive']
    require(dual.get('needs') == 'preimage-first', 'original tests lack mandatory prerequisite')
    require(set(third.get('needs', [])) == {'preimage-first', 'dual-python-tests'},
            'archive check lacks mandatory prerequisites')
    require(set(pre['strategy']['matrix']['python-version']) == {'3.11', '3.12'},
            'missing dual Python coverage')
    for job in jobs.values():
        require(not job.get('continue-on-error'), 'job failure can be ignored')
        for step in job.get('steps', []):
            require(not step.get('continue-on-error'), 'step failure can be ignored')
            run = step.get('run', '')
            for bad in ('git push', 'git add ', 'git commit', '|| true', 'set +e', 'assert '):
                require(bad not in run, 'unsafe workflow command: ' + bad)
    first = '\n'.join(step.get('run', '') for step in pre['steps'])
    last = '\n'.join(step.get('run', '') for step in third['steps'])
    require(first.count(ZIP_HASH) >= 1 and last.count(ZIP_HASH) >= 1,
            'ZIP source identity missing in a mandatory path')
    require(first.index(ZIP_HASH) < first.index('r272_preimage_first_readonly_gate_20261102.py'),
            'preimage gate occurs before ZIP identity')
    require('--regenerate' in first and '--regenerate' in last,
            'missing isolated regeneration')
    require('python -O research/validation/r272_preimage_first_readonly_gate_20261102.py' in first,
            'optimized mode missing')
    require('python -OO research/validation/r272_preimage_first_readonly_gate_20261102.py' in first,
            'double optimized mode missing')
    require('r272_pinned_native_replay_and_preimage_negative_20261102.py' in first,
            'negative native regression not mandatory')
    require('--emit' not in first + last, 'mutable original emit in acceptance path')
    require('r272_preimage_first_readonly_gate_20261102.py' in last,
            'third job must validate checkout independently')
    return {'status': 'PASS', 'jobs': len(jobs), 'mandatory_paths': len(REQUIRED_PATHS),
            'python_versions': 2, 'optimized_modes': 2, 'read_only': True}


def self_test(raw: str) -> dict:
    check(raw)
    mutants = {
        'remove_original_path': raw.replace("      - 'research/R272/**'", "      - 'research/R272/README.md'", 1),
        'write_permission': raw.replace('contents: read', 'contents: write', 1),
        'skip_preimage_dependency': raw.replace('needs: preimage-first', 'needs: []', 1),
        'skip_third_dependency': raw.replace('needs: [preimage-first, dual-python-tests]', 'needs: [dual-python-tests]', 1),
        'remove_optimized': raw.replace('          python -O research/validation/r272_preimage_first_readonly_gate_20261102.py', '          echo skipped -O', 1),
        'remove_double_optimized': raw.replace('          python -OO research/validation/r272_preimage_first_readonly_gate_20261102.py', '          echo skipped -OO', 1),
        'disable_failure': raw.replace('      - name: Mandatory pinned preimage audit and isolated regeneration',
                                       '      - continue-on-error: true\n        name: Mandatory pinned preimage audit and isolated regeneration', 1),
        'reintroduce_emit': raw.replace('          python research/validation/r272_preimage_first_readonly_gate_20261102.py --root .',
                                        '          python research/R272/r272_exact_train_test_prediction.py --emit\n          python research/validation/r272_preimage_first_readonly_gate_20261102.py --root .', 1),
        'remove_zip_hash': raw.replace(ZIP_HASH, '0'*64),
        'remove_negative': raw.replace('          python research/validation/r272_pinned_native_replay_and_preimage_negative_20261102.py',
                                       '          echo skip regression', 1),
    }
    require(all(v != raw for v in mutants.values()), 'a mutation did not apply')
    rejected = []
    for name, candidate in mutants.items():
        try:
            check(candidate)
        except (ValueError, yaml.YAMLError):
            rejected.append(name)
    require(len(rejected) == len(mutants), 'undetected mutants: ' + repr(set(mutants)-set(rejected)))
    return {'status': 'PASS', 'negative_mutations_rejected': len(rejected),
            'cases': rejected, 'scope': 'STATIC_CANDIDATE_ONLY'}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('workflow', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    raw = args.workflow.read_text(encoding='utf-8')
    import json
    print(json.dumps(self_test(raw) if args.self_test else check(raw), sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, yaml.YAMLError) as exc:
        raise SystemExit('FAIL: ' + str(exc)) from exc
