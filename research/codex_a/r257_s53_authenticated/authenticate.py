#!/usr/bin/env python3
"""Compose pinned existing S53 source-link and PR3 math CLIs, stdout only.

No network, historical-source changes, author signatures or scientific upgrade.
Each source is read once; both CLIs consume the same authenticated temp snapshot.
"""
import argparse
import hashlib
import json
from pathlib import Path
import platform
import subprocess
import sys
import tempfile

PINS = {'research/R257/R257_ALL_225_ORIGINAL_GRID_CANDIDATE_SOURCE_ATOMS.csv': {'git_blob': '63dc333cf4c4206fa466e0c0f33e3b079f4dc01b',
                                                                         'sha256': 'ac201d9b736f223e0a63b4d11d6a9891b4396f822c6a8b6eaba793a95f69cb5d'},
 'research/R257/R257_EXACT_RESULTS.json': {'git_blob': '55c00defa893ba3ed36cc5d3a6b0144953f16301',
                                           'sha256': 'ab9aefc5626451d1ea2d0419b38d7cfc7abe12f12e891b3904926a8a22f7b87e'},
 'research/validation/r257_s53_capacity_shadow_20261029.py': {'git_blob': '4026c2111eed6d64dd21d100ab9961c00a6fa71e',
                                                              'sha256': '3510b7bd26d910e18fae00e17d042a9a3a381435b4a3d3a4c1b85c35931ce47d'},
 'research/validation/R257_S53_EXACT_RECEIPT_2026-10-29.json': {'git_blob': '37f33083b45435e18c66641ef693c6f0c779a680',
                                                                'sha256': 'd4a33b47f4d818a8b4358a809b977c49aaad19c1656570e97947f0f3d30cd8e4'},
 'research/validation/r257_s53_original225_source_link_gate_20261102.js': {'git_blob': 'a4dfac449371aa259bcdabf4cc73c88e7e014135',
                                                                           'sha256': '84642c9b1db4ab306c5348d70a8d9380f58e85807766bb25604e13aa492555f8'},
 'protocols/R257_S53_CAPACITY_SHADOW_PRICE_PRESCORE_FREEZE_2026-10-29.md': {'git_blob': '2060b7423fed97dcd62f7a53aebea5220b969d2b',
                                                                            'sha256': 'fb659012041c2569ed8fb1a3f1dcb5ddab15fa2e5f674bb7f74da6e04efa4ade'},
 'research/evidence_audit/B_R257_S53_PROTOCOL_ORDER_DEVIATION_ADDENDUM_2026-10-29.md': {'git_blob': '154a06a9e9a3454818ff9e1b96aa298c6dc422cc',
                                                                                        'sha256': '630d751a5d490d89b69d2aff171a596ef3c3d05df5778dde90d4bdbf0185de69'}}
VALIDATOR_PIN = {
    'git_blob': '75c0870c49c26f175ab678a7600ae4d4b8a5c7f2',
    'sha256': '9850be7142765edc1620f557f937cf2215b5dd6275aaba8282b8188ea6ff6964',
}
SOURCE_GATE = 'research/validation/r257_s53_original225_source_link_gate_20261102.js'
RECEIPT = 'research/validation/R257_S53_EXACT_RECEIPT_2026-10-29.json'
SOURCE_EXPECTED = {
    'status': 'PASS_SOURCE_LINK_INTERNAL_E1_ONLY', 'original_rows': 225,
    'convex_rows': 200, 'nonconvex_rows_structure_only': 25,
    'feasible_grid_rows': 145, 'linked_worlds': 8, 'blind_order': 'FAIL',
    'formal_scientific_acceptance': 'PARTIAL',
}
MATH_EXPECTED = {
    'status': 'COMPLETE', 'scope': 'NONBLIND_E1_MATHEMATICAL_RECEIPT_CHECK',
    'capacity_certificates': 40, 'secants_checked': 32,
    'baseline_multipliers_checked': 8, 'blinded_prescore_order': 'FAIL',
    'full_scientific_acceptance': 'PARTIAL', 'source_authentication': 'NOT_RUN',
    'external_team_replications': 0, 'new_human_E2': 0, 'new_history_E3': 0,
}


def identity(raw):
    return {'git_blob': hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest(),
            'sha256': hashlib.sha256(raw).hexdigest()}


def authenticated(path, pin):
    raw = Path(path).read_bytes()
    if identity(raw) != pin:
        raise ValueError('identity mismatch: ' + str(path))
    return raw


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: ' + key)
        result[key] = value
    return result


def checked_child(command, expected):
    try:
        child = subprocess.run(command, capture_output=True, text=True, timeout=30)
    except subprocess.TimeoutExpired as exc:
        raise ValueError('child timeout: ' + command[0]) from exc
    if child.returncode != 0:
        raise ValueError('child exit ' + str(child.returncode) + ': ' + child.stderr[:500])
    result = json.loads(child.stdout, object_pairs_hook=unique_object)
    # Compare canonical JSON as well as values: Python True must not equal int 1.
    if (type(result) is not dict or
            json.dumps(result, sort_keys=True) != json.dumps(expected, sort_keys=True)):
        raise ValueError('summary mismatch: ' + command[0])
    return result


def verify(root, validator):
    root = Path(root)
    raw_sources = {path: authenticated(root / path, pin) for path, pin in PINS.items()}
    validator_raw = authenticated(validator, VALIDATOR_PIN)
    identities = {path: identity(raw) for path, raw in raw_sources.items()}
    identities['PR3_validator'] = identity(validator_raw)
    with tempfile.TemporaryDirectory(prefix='s53-authenticated-') as directory:
        snapshot = Path(directory)
        for path, raw in raw_sources.items():
            target = snapshot / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(raw)
        staged_validator = snapshot / 'PR3_validate_receipt.py'
        staged_validator.write_bytes(validator_raw)
        source_command = ['node', str(snapshot / SOURCE_GATE), '--repo-root', str(snapshot)]
        python_command = [sys.executable, '-B'] + (['-O'] if sys.flags.optimize else [])
        python_command += [str(staged_validator), str(snapshot / RECEIPT)]
        source = checked_child(source_command, SOURCE_EXPECTED)
        math = checked_child(python_command, MATH_EXPECTED)
    return {
        'status': 'COMPLETE_PINNED_COMPOSITION',
        'scope': 'NONBLIND_INTERNAL_E1_PINNED_BYTES_AND_EXISTING_GATES',
        'source_authentication': 'PINNED_INPUT_AND_EXECUTABLE_BYTES_VERIFIED',
        'source_link': source, 'mathematical_gate': math, 'identities': identities,
        'commands': [source_command, python_command],
        'python': platform.python_version(), 'optimized': bool(sys.flags.optimize),
        'blinded_prescore_order': 'FAIL', 'full_scientific_acceptance': 'PARTIAL',
        'historical_execution_time_authenticated': 'NOT_ESTABLISHED',
        'nonconvex_objective_recomputed': 'NOT_RUN',
        'new_E2': 0, 'new_E3': 0, 'external_team_replications': 0,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    parser.add_argument('--validator', required=True, type=Path)
    args = parser.parse_args()
    try:
        result = verify(args.root, args.validator)
    except (OSError, ValueError) as exc:
        print(json.dumps({'status': 'BLOCKED', 'reason': str(exc)}))
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == '__main__':
    sys.exit(main())
