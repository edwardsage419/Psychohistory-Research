#!/usr/bin/env python3
"""Independent Fraction Markov oracle for frozen R261 S57.

Reads only the persisted R S57 JSON when verifying; it never imports the R
source scorer or reads its original ten-bit CSV. This is a non-blind internal
mathematical recomputation, not independent external reproduction.
"""
import argparse
import copy
import json
from fractions import Fraction as F
from pathlib import Path

WORLDS = (
    'FINITE_NEUTRAL_IDIOSYNCRATIC',
    'FINITE_CONVEX_SQUARE',
    'FINITE_CONCAVE_CONFORMITY',
    'FINITE_CONTRARIAN',
    'INDEPENDENT_HALF',
    'UNANIMOUS_ONLY',
    'MAJORITY_TIE_UP',
    'COMMON_NOISE_NEUTRAL',
    'OBSERVED_COMMON_NOISE_TRUE_INDEPENDENT_SENSOR',
)
SHARED = frozenset(WORLDS[-2:])
FIELDS = (
    'world', 'initial_count_K0', 'source_rows',
    'y2_probability_given_K0', 'prefix_mean_field_q0',
    'deterministic_MF_y2_probability', 'y2_Brier_K0_oracle',
    'y2_Brier_K0_K1_prefix', 'y2_Brier_deterministic_MF',
    'y2_prefix_information_gain', 'y2_MF_excess_risk',
    'j1_true_joint_probability', 'j1_independent_naive_probability',
    'j1_Brier_correct', 'j1_Brier_naive_independence',
    'j1_naive_excess_risk',
)


def q(world, m):
    if world in (WORLDS[0], WORLDS[7], WORLDS[8]):
        return m
    if world == WORLDS[1]:
        return m ** 2
    if world == WORLDS[2]:
        return 2 * m - m ** 2
    if world == WORLDS[3]:
        return 1 - m
    if world == WORLDS[4]:
        return F(1, 2)
    if world == WORLDS[5]:
        return F(int(m == 1))
    if world == WORLDS[6]:
        return F(int(m >= F(1, 2)))
    raise ValueError('unrecognized frozen world')


def fmt(value):
    return str(value)


def expected():
    rows = []
    for world in WORLDS:
        for k0 in (0, 1, 2):
            first = q(world, F(k0, 2))
            # Independent mathematical route: three-state Markov kernel.
            transition = ((1 - first, F(0), first) if world in SHARED else
                          ((1 - first) ** 2, 2 * first * (1 - first), first ** 2))
            assert sum(transition) == 1
            conditional = [q(world, F(k1, 2)) for k1 in (0, 1, 2)]
            prior = sum((weight * p for weight, p in zip(transition, conditional)), F(0))
            mf = q(world, first)
            b0 = prior * (1 - prior)
            b1 = sum((weight * p * (1 - p) for weight, p in zip(transition, conditional)), F(0))
            bm = b0 + (mf - prior) ** 2
            information = sum((weight * (p - prior) ** 2 for weight, p in zip(transition, conditional)), F(0))
            assert b0 - b1 == information
            true_joint = first if world in SHARED else first ** 2
            naive_joint = first ** 2
            bj = true_joint * (1 - true_joint)
            extra = (naive_joint - true_joint) ** 2
            rows.append(dict(zip(FIELDS, (
                world, k0, 512 if k0 == 1 else 256,
                fmt(prior), fmt(first), fmt(mf), fmt(b0), fmt(b1), fmt(bm),
                fmt(information), fmt(bm - b0), fmt(true_joint),
                fmt(naive_joint), fmt(bj), fmt(bj + extra), fmt(extra),
            ))))
    return rows


def verify(obj):
    if not isinstance(obj, dict) or obj.get('research_id') != 'R261' or obj.get('stage') != 'S57':
        raise ValueError('wrong research/stage identity')
    if obj.get('evidence_class') != 'E1_ARTIFICIAL' or obj.get('new_human_E2') != 0 or obj.get('new_historical_E3') != 0:
        raise ValueError('evidence class or E2/E3 mismatch')
    if obj.get('R073') != 'FROZEN' or obj.get('PESEN_v0_1') != 'FROZEN':
        raise ValueError('frozen model status mismatch')
    if obj.get('original_source_git_blob') != '7aec6fe1bbce064b985168f72a3b9adbcb6ca521':
        raise ValueError('original source identity mismatch')
    if obj.get('all_original_source_rows') != 9216 or obj.get('conditional_initial_groups') != 27:
        raise ValueError('source universe size mismatch')
    rows = obj.get('exact_rows')
    if not isinstance(rows, list) or len(rows) != 27:
        raise ValueError('incomplete or expanded row universe')
    expected_rows = expected()
    seen = set()
    checks = 0
    for i, (actual, truth) in enumerate(zip(rows, expected_rows)):
        if not isinstance(actual, dict) or set(actual) != set(FIELDS):
            raise ValueError(f'row {i} fields differ')
        key = (actual['world'], actual['initial_count_K0'])
        if key in seen:
            raise ValueError('duplicate world/K0 key')
        seen.add(key)
        for field in FIELDS:
            if actual[field] != truth[field] or type(actual[field]) is not type(truth[field]):
                raise ValueError(f'row {i} mismatch {field}: {actual[field]} != {truth[field]}')
            checks += 1
    return checks


def selftest():
    base = dict(research_id='R261', stage='S57', evidence_class='E1_ARTIFICIAL',
                new_human_E2=0, new_historical_E3=0, R073='FROZEN',
                PESEN_v0_1='FROZEN', original_source_git_blob='7aec6fe1bbce064b985168f72a3b9adbcb6ca521',
                all_original_source_rows=9216, conditional_initial_groups=27, exact_rows=expected())
    assert verify(base) == 27 * len(FIELDS)
    variants = []
    a = copy.deepcopy(base); a['exact_rows'][0] = copy.deepcopy(a['exact_rows'][1]); variants.append(a)
    a = copy.deepcopy(base); a['exact_rows'].pop(); variants.append(a)
    a = copy.deepcopy(base); a['exact_rows'][4]['y2_Brier_K0_oracle'] = '999'; variants.append(a)
    a = copy.deepcopy(base); a['evidence_class'] = 'E2_HUMAN'; variants.append(a)
    a = copy.deepcopy(base); a['exact_rows'][0]['source_rows'] = 512; variants.append(a)
    for i, mutation in enumerate(variants):
        try:
            verify(mutation)
        except ValueError:
            continue
        raise AssertionError(f'negative control {i} was accepted')
    print(json.dumps({'independent_oracle_rows': 27, 'exact_field_comparisons': 27 * len(FIELDS),
                      'negative_controls_rejected': len(variants), 'status': 'PASS'}, sort_keys=True))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify', type=Path, help='Persisted R S57 JSON receipt')
    parser.add_argument('--selftest', action='store_true')
    args = parser.parse_args()
    if not args.verify and not args.selftest:
        parser.error('provide --verify or --selftest')
    if args.selftest:
        selftest()
    if args.verify:
        receipt = json.loads(args.verify.read_text(encoding='utf-8'))
        print(json.dumps({'persisted_receipt_verified': True,
                          'exact_field_comparisons': verify(receipt)}, sort_keys=True))


if __name__ == '__main__':
    main()
