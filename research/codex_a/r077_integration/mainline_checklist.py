#!/usr/bin/env python3
"""Authenticate adopted R077 code and retained synthetic evidence; never score data.

Exit 2 is the required production veto even when all engineering checks pass.
No network, Git mutations, human inputs, mathematical execution or approval flag.
"""
import argparse
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

import preflight as p

EVIDENCE_COMMIT = '714ec9a7e257fff98044f0f68391944d526ac1d1'
OWN = 'research/codex_a/r077_integration'
ADAPTER_SHA256 = {
    '101adc1271e7ccbcf10f02e62afc0916bccd96d80278e9258cc9bfae6f45baaf',
    '8e04095a1b984d47245563a363309f5a7e332326584e53f0a17545235cf8ef23',
}


def adopted(repo, head, commit, name):
    raw = p.git(repo, 'show', commit+':'+name)
    expected = p.identity(raw)
    p.require(p.identity((repo/name).read_bytes()) == expected and
              p.git(repo, 'rev-parse', head+':'+name).decode().strip() == expected['git_blob'],
              'ADOPTED_SOURCE_IDENTITY:'+name)
    return raw, expected


def retained(repo):
    # Immutable Git evidence, not arbitrary caller-supplied receipt files.
    raw = p.git(repo, 'show', EVIDENCE_COMMIT+':'+OWN+'/shadow_evidence.tar.gz')
    p.require(p.identity(raw)['sha256'] == 'ea6324c5e8dc07c74a319858f3d758e624f74172735dd8dbdccb1f2533d6527a',
              'RETAINED_ARCHIVE_IDENTITY')
    members = p.load_json(p.git(repo, 'show', EVIDENCE_COMMIT+':'+OWN+'/shadow_evidence_members.json'))
    with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as archive:
        names = archive.getnames()
        p.require(len(names) == len(set(names)) and set(names) == {row['path'] for row in members},
                  'RETAINED_ARCHIVE_MEMBERS')
        contents = {}
        for row in members:
            info = archive.getmember(row['path'])
            p.require(info.isfile(), 'RETAINED_NONREGULAR_MEMBER')
            value = archive.extractfile(info).read()
            p.require(len(value) == row['bytes'] and p.identity(value)['sha256'] == row['sha256'],
                      'RETAINED_MEMBER_IDENTITY')
            contents[row['path']] = value
    return p.load_json(contents['normal-shadow.stdout']), p.identity(raw)


def validate_evidence(data, sources, candidate_sources):
    result = p.classify(data['diagnostic'])
    shadow = p.validate_shadow(data['candidate_shadow']['data'], data['diagnostic'])
    p.require(data['production_ready'] is False and data['exit_code'] == 2 and
              data['original_failure_cases'] == result['original_failure_cases'] and
              data['candidate_shadow']['production_ready'] is False and
              data['candidate_shadow']['corrected_orders'] == shadow['corrected_orders'],
              'RETAINED_PRODUCTION_VETO_OR_COUNT')
    p.require(data['sources'] == sources and data['candidate_shadow']['sources'] == candidate_sources,
              'RETAINED_SOURCE_BINDING')
    return result, shadow


def verify(repo):
    repo = Path(repo).resolve()
    own_raw = Path(__file__).read_bytes()
    with tempfile.TemporaryDirectory(prefix='r077-checklist-') as directory:
        head, sources, manifest = p.capture(repo, Path(directory))
    adapter, adapter_id = adopted(repo, head, head, OWN+'/preflight.py')
    p.require(adapter_id['sha256'] in ADAPTER_SHA256, 'UNREVIEWED_ADAPTER_VERSION')
    pins_raw = p.git(repo, 'show', p.CANDIDATE_COMMIT+':'+p.CANDIDATE_DIR+'/pins.json')
    pins = p.load_json(pins_raw)
    p.require(type(pins) is dict and len(pins) == 14, 'CANDIDATE_INPUT_COVERAGE')
    candidate_sources = {}
    for name, blob in pins.items():
        _, identity = adopted(repo, head, p.CANDIDATE_COMMIT, name)
        p.require(identity['git_blob'] == blob, 'CANDIDATE_INPUT_PIN')
        candidate_sources[name] = identity
    for short in ('candidate.py', 'test_candidate.py', 'pins.json'):
        name = p.CANDIDATE_DIR+'/'+short
        _, candidate_sources[name] = adopted(repo, head, p.CANDIDATE_COMMIT, name)
    data, archive = retained(repo)
    result, shadow = validate_evidence(data, sources, candidate_sources)
    p.require(Path(__file__).read_bytes() == own_raw, 'CHECKLIST_CHANGED_DURING_EXECUTION')
    return {
        'status': 'COMPLETE_ENGINEERING_CHECKS_PRODUCTION_BLOCKED', 'exit_code': 2,
        'production_ready': False, 'tested_checkout_sha': head,
        'checks': {'B18_40_sources': 'COMPLETE', 'B28_14_inputs_and_3_program_files': 'COMPLETE',
                   'retained_13_member_archive': 'COMPLETE', 'retained_original_and_shadow': 'COMPLETE',
                   'frozen_scoring_adoption_approval': 'BLOCKED_NOT_AUTHORIZED',
                   'qualified_human_input_identity': 'NOT_ESTABLISHED',
                   'historical_human_impact': 'UNKNOWN_NOT_RECOMPUTED',
                   'production_hook': 'NOT_INSTALLED', 'scientific_reacceptance': 'NOT_RUN'},
        'original_failure_cases': result['original_failure_cases'],
        'candidate_correct_orders': shadow['corrected_orders'],
        'sources': sources, 'candidate_sources': candidate_sources,
        'manifest_identity': manifest, 'adapter_identity': adapter_id,
        'retained_archive': archive, 'retained_evidence_commit': EVIDENCE_COMMIT,
        'checklist_identity': p.identity(own_raw),
        'mathematical_programs_rerun': False, 'human_rescoring': 'NOT_RUN', 'CI': 'NOT_RUN',
        'next_commands_if_sources_change': [
            'python3 -B '+OWN+'/preflight.py . --artificial-preflight --candidate-shadow',
            'python3 -B '+OWN+'/preflight.py . --artificial-preflight'],
        'expected_command_exit': 2,
        'rollback': 'Omit --candidate-shadow or stop optional preflight; original scorer stays unchanged.',
        'limits': ['Retained synthetic results are revalidated, not a new mathematical run.',
                   'Git adoption is checked by bytes and HEAD objects, not stale PR status labels.',
                   'No human-data qualification, adoption authorization or production success is inferred.'],
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', type=Path)
    args = parser.parse_args()
    try:result = verify(args.repo)
    except (OSError, ValueError, KeyError, TypeError, tarfile.TarError, subprocess.SubprocessError) as exc:
        print(json.dumps({'status': 'BLOCKED_INVALID_CHECKLIST', 'production_ready': False,
                          'reason': str(exc)[:300]}));return 1
    print(json.dumps(result, indent=2));return 2


if __name__ == '__main__':sys.exit(main())
