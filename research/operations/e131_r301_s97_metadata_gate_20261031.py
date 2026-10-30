#!/usr/bin/env python3
"""Supplementary R301 S97 metadata gate. Leaves the original B checker unchanged.
Synthetic mutation tests are independent of archived files; --folder checks actual files.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path

FREEZE = 'b18d1cd4e149a60ebfe3732f38f09f1cb6d94e7a'
EXPECTED = {
    'research_id': 'R301', 'extension': 'S97', 'freeze_commit': FREEZE,
    'external_team_replication': False, 'history_length': 4,
    'heldout_length': 1, 'source_atoms': 288, 'distinct_true_atoms': 96,
}
NAMES = ('R301_S97_ALL_288_HELDOUT_ATOMS.csv', 'R301_S97_EXACT_HELDOUT_RESULTS.json')


def metadata_gate(results, receipt):
    for key, expected in EXPECTED.items():
        if key not in results or type(results[key]) is not type(expected) or results[key] != expected:
            raise ValueError('result metadata: ' + key)
    if receipt.get('freeze_commit') != FREEZE:
        raise ValueError('receipt freeze_commit')
    if set(receipt.get('files', {})) != set(NAMES):
        raise ValueError('receipt file universe')
    for name in NAMES:
        item = receipt['files'][name]
        if not isinstance(item.get('bytes'), int) or item['bytes'] < 0:
            raise ValueError('receipt bytes')
        if not isinstance(item.get('sha256'), str) or len(item['sha256']) != 64:
            raise ValueError('receipt SHA')
    return True


def check_folder(folder):
    folder = Path(folder)
    results = json.loads((folder / NAMES[1]).read_text(encoding='utf8'))
    receipt = json.loads((folder / 'R301_S97_RECEIPT.json').read_text(encoding='utf8'))
    metadata_gate(results, receipt)
    for name in NAMES:
        data = (folder / name).read_bytes()
        if len(data) != receipt['files'][name]['bytes']:
            raise ValueError('byte mismatch: ' + name)
        if hashlib.sha256(data).hexdigest() != receipt['files'][name]['sha256']:
            raise ValueError('SHA mismatch: ' + name)
    return True


def test():
    results = copy.deepcopy(EXPECTED)
    receipt = {'freeze_commit': FREEZE,
               'files': {name: {'bytes': 1, 'sha256': '0'*64} for name in NAMES}}
    assert metadata_gate(results, receipt)
    rejected = 0
    for key in EXPECTED:
        for mode in ('delete', 'mutate'):
            r = copy.deepcopy(results)
            if mode == 'delete':
                del r[key]
            else:
                r[key] = 'tampered' if isinstance(r[key], str) else (not r[key] if isinstance(r[key], bool) else r[key] + 1)
            try:
                metadata_gate(r, receipt)
            except ValueError:
                rejected += 1
            else:
                raise AssertionError('metadata mutation accepted: ' + key + ':' + mode)
    for mode in ('delete', 'mutate'):
        rc = copy.deepcopy(receipt)
        if mode == 'delete':
            del rc['freeze_commit']
        else:
            rc['freeze_commit'] = 'wrong'
        try:
            metadata_gate(results, rc)
        except ValueError:
            rejected += 1
        else:
            raise AssertionError('receipt freeze mutation accepted')
    assert rejected == 18
    return {'positive': 1, 'negative_rejected': rejected, 'assertions': 20,
            'scope': 'synthetic_metadata_only'}


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--folder')
    p.add_argument('--test', action='store_true')
    args = p.parse_args()
    if args.test:
        print(json.dumps(test(), indent=2))
    elif args.folder:
        print(json.dumps({'metadata_and_sha': 'PASS' if check_folder(args.folder) else 'FAIL'}))
    else:
        p.error('use --test or --folder')
