#!/usr/bin/env python3
"""Fail-closed identity and independent finite-E1 semantics for frozen R336/R340.

Usage: python r336_r340_strict_receipt_gate_20261101.py R336 /path/to/R336
Only standard-library dependencies. This program does not import audited sources.
"""
import argparse
import csv
import hashlib
import io
import json
from fractions import Fraction
from pathlib import Path

PINNED = {
    'R336': {
        'r336_inoculation.py': 'bcbf7b40c1f8ba86d5478d57509a437b5ba0279f',
        'R336_ALL_96_ARTIFICIAL_ATTACK_ATOMS.csv': 'efa20e7d6432a1a6c7bd0abd53384b36e23422e5',
        'R336_EXACT_48_CONDITIONS.json': '2704b6066a7f3842c2273c8262d9fd41e2483d73',
    },
    'R340': {
        'r340_sis_generator.py': '7bd287300825266be1a13fc12229b8c48b01e7a7',
        'R340_ALL_48_ARTIFICIAL_GENERATOR_ATOMS.csv': '36ae0a9a11d2f27dacd8948f9617122eade0c40c',
        'R340_EXACT_3_GENERATORS.json': 'e5615c6d99bd79acac5501bda60976b3f7d3cad2',
    },
}

def blob_sha(raw):
    return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()

def unique_json(raw):
    def no_duplicates(pairs):
        d = {}
        for k, v in pairs:
            if k in d:
                raise ValueError('duplicate JSON key: ' + k)
            d[k] = v
        return d
    return json.loads(raw, object_pairs_hook=no_duplicates)

def check_r336(csv_bytes, json_bytes):
    obj = unique_json(json_bytes)
    if obj.get('schema') != 'R336_frozen_inoculation_transfer_v1':
        raise ValueError('R336 schema mismatch')
    conditions = obj['conditions']
    rows = list(csv.DictReader(io.StringIO(csv_bytes.decode('utf-8'))))
    if len(conditions) != 48 or len(rows) != 96:
        raise ValueError('R336 incomplete universe')
    expected = []
    for m in range(3):
        for w in (0,1):
            for r in (0,1):
                for s in (0,1):
                    for a in (1,2):
                        d = 0 if (m == 0 or w == 0 or r == 0) else ((2 if m == 1 else 3) if s else (1 if m == 1 else 2))
                        c = d if s else 0
                        baseline = 6 - 2*a
                        transfer = 6 - max(0, 2*a-d)
                        support = 6 - max(0, 2*a-c)
                        expected.append((m,w,r,s,a,baseline,transfer,support,d,c))
    keys = ['mode','weak','refutation','same_topic','attack_intensity','baseline_post','transfer_post','support_post','transfer_defense','support_defense']
    observed = [tuple(x[k] for k in keys) for x in conditions]
    if observed != expected:
        raise ValueError('R336 condition semantics mismatch')
    for i, vals in enumerate(expected):
        m,w,r,s,a,base,t,u,d,c = vals
        for j, (policy, defense, post) in enumerate((('INOCULATION_TRANSFER',d,t),('TOPIC_SPECIFIC_SUPPORT',c,u))):
            row = rows[2*i+j]
            expected_row = dict(mode=str(m),weak=str(w),refutation=str(r),same_topic=str(s),attack_intensity=str(a),policy=policy,defense=str(defense),baseline_post=str(base),post_belief=str(post),retained_gain=str(post-base))
            if row != expected_row:
                raise ValueError('R336 row semantics mismatch')
    checks = obj['checks']
    expected_checks = {'worlds':48,'rows':96,'same_topic_agreement':24,'novel_transfer_advantage':4,'no_weak_equal_baseline':24,'no_refutation_equal_baseline':24}
    if checks != expected_checks:
        raise ValueError('R336 check totals mismatch')

def check_r340(csv_bytes, json_bytes):
    obj = unique_json(json_bytes)
    if obj.get('schema') != 'R340_frozen_two_node_sis_generator_v1':
        raise ValueError('R340 schema mismatch')
    rows = list(csv.DictReader(io.StringIO(csv_bytes.decode('utf-8'))))
    worlds = obj['worlds']
    if len(rows) != 48 or len(worlds) != 3:
        raise ValueError('R340 incomplete universe')
    states = ('00','01','10','11')
    for k, beta_text in enumerate(('1/2','1','2')):
        beta = Fraction(beta_text)
        matrix = []
        for state in states:
            row = []
            for target in states:
                if target == state:
                    rate = -sum((Fraction(1) if state[bit] == '1' else beta if state[1-bit] == '1' else 0) for bit in range(2))
                else:
                    changed = [i for i in range(2) if state[i] != target[i]]
                    rate = Fraction(0)
                    if len(changed) == 1:
                        bit = changed[0]
                        if state[bit] == '1' and target[bit] == '0':
                            rate = Fraction(1)
                        elif state[bit] == '0' and target[bit] == '1' and state[1-bit] == '1':
                            rate = beta
                row.append(str(rate))
            matrix.append(row)
        world = worlds[k]
        expected_world = dict(beta=beta_text,matrix=matrix,first_event_infection=str(beta/(1+beta)),first_event_recovery=str(Fraction(1)/(1+beta)))
        if world != expected_world:
            raise ValueError('R340 matrix semantics mismatch')
        for i, origin in enumerate(states):
            for j, destination in enumerate(states):
                expected_row = dict(beta=beta_text,origin=origin,destination=destination,rate=matrix[i][j])
                if rows[16*k+4*i+j] != expected_row:
                    raise ValueError('R340 CSV matrix mismatch')
    expected_checks = dict(worlds=3,source_rows=48,absorbing_worlds=3,zero_sum_rows=12,nonnegative_offdiagonal_entries=36,correct_01_10_transitions=6,correct_11_recoveries=3)
    if obj['checks'] != expected_checks:
        raise ValueError('R340 check totals mismatch')

def verify(model, directory):
    pinned = PINNED[model]
    content = {}
    for name, expected_sha in pinned.items():
        data = (directory / name).read_bytes()
        actual = blob_sha(data)
        if actual != expected_sha:
            raise ValueError(f'{model} identity mismatch {name}: {actual}')
        content[name] = data
    csv_name, json_name = list(pinned)[1:]
    if model == 'R336':
        check_r336(content[csv_name], content[json_name])
    else:
        check_r340(content[csv_name], content[json_name])
    return True

def main():
    p = argparse.ArgumentParser()
    p.add_argument('model', choices=PINNED)
    p.add_argument('directory', type=Path)
    a = p.parse_args()
    try:
        verify(a.model, a.directory)
    except (OSError, ValueError, KeyError, TypeError, UnicodeError, json.JSONDecodeError) as exc:
        p.exit(1, f'STRICT_GATE_FAIL: {type(exc).__name__}: {exc}\n')
    print('STRICT_GATE_PASS ' + a.model)

if __name__ == '__main__':
    main()
