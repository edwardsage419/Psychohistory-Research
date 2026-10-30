#!/usr/bin/env python3
"""R286 S82: exact finite Markov reward risk; artificial E1 only.
Run: python r286_s82_markov_reward_exact_20261030.py --test
     python r286_s82_markov_reward_exact_20261030.py --emit DIR
"""
import argparse
import csv
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

STAYS = (F(1, 4), F(1, 2), F(3, 4))
POLICIES = ('TD0_ONLINE_CORRECT', 'MC_COMPLETE_RETURN', 'B_THEN_A_UPDATED_BOOTSTRAP')
COEFFS64 = {
    'TD0_ONLINE_CORRECT': (8, 12, 16, 16, 0),
    'MC_COMPLETE_RETURN': (2, 4, 8, 16, 32),
    'B_THEN_A_UPDATED_BOOTSTRAP': (5, 8, 12, 16, 16),
}
IID_HALF = dict(zip(POLICIES, (F(155, 512), F(683, 2048), F(2445, 8192))))
COLUMNS = ('stay_probability', 'rho', 'policy', 'source_6bits', 'training_5bits',
           'future_Y6', 'source_mass', 'VA5', 'heldout_Brier')

def learn(train, policy):
    assert len(train) == 5 and set(train) <= {0, 1}
    a = b = F(0)
    for y in train:
        if policy == POLICIES[0]:
            a = (a + b) / 2
            b = (b + y) / 2
        elif policy == POLICIES[1]:
            a = (a + y) / 2
            b = (b + y) / 2
        elif policy == POLICIES[2]:
            b = (b + y) / 2
            a = (a + b) / 2
        else:
            raise ValueError('unknown policy')
    return a

def mass(stay, bits):
    same = sum(a == b for a, b in zip(bits, bits[1:]))
    return F(1, 2) * stay ** same * (1 - stay) ** (5 - same)

def covariance_oracle(stay, policy):
    rho = 2 * stay - 1
    c = [F(x, 64) for x in COEFFS64[policy]]
    var = sum((c[i] * c[j] * rho ** abs(i-j)
               for i in range(5) for j in range(5)), F(0))
    cross = sum((c[i] * rho ** (5-i) for i in range(5)), F(0))
    return F(1, 4) + (1-sum(c)) ** 2 / 4 + var / 4 - cross / 2

def generate():
    rows, results = [], []
    for stay in STAYS:
        for policy in POLICIES:
            weighted = F(0)
            total_mass = F(0)
            seen = set()
            for bits in itertools.product((0, 1), repeat=6):
                source = ''.join(map(str, bits))
                weight = mass(stay, bits)
                value = learn(bits[:5], policy)
                loss = (bits[5] - value) ** 2
                seen.add(source)
                total_mass += weight
                weighted += weight * loss
                rows.append((str(stay), str(2*stay-1), policy, source, source[:5],
                             str(bits[5]), str(weight), str(value), str(loss)))
            assert len(seen) == 64 and total_mass == 1
            oracle = covariance_oracle(stay, policy)
            assert weighted == oracle, (stay, policy, weighted, oracle)
            if stay == F(1, 2):
                assert weighted == IID_HALF[policy]
            for i, expected in enumerate(COEFFS64[policy]):
                basis = [0] * 5
                basis[i] = 1
                assert learn(basis, policy) == F(expected, 64)
            results.append(dict(stay_probability=str(stay), rho=str(2*stay-1),
                policy=policy, complete_sources=64, source_mass='1',
                exact_heldout_Brier=str(weighted), independent_covariance_Brier=str(oracle),
                constant_half_baseline_Brier='1/4',
                delta_vs_constant_half=str(weighted-F(1,4)),
                frozen_original_coefficients=[str(F(x,64)) for x in COEFFS64[policy]]))
    assert len(rows) == 576 and len(results) == 9
    output = dict(research_id='R286_S82',
        freeze_protocol='research/validation/R286_S82_MARKOV_REWARD_DEPENDENCE_PRESCORE_FREEZE_2026-10-30.md',
        original_R286_status='UNCHANGED_CLOSED_BOUNDED_E1',
        scope='INTERNAL_NONBLIND_ARTIFICIAL_E1_MARKOV_REWARD_DEPENDENCE',
        stay_probabilities=['1/4','1/2','3/4'], model_labeled_complete_source_types=576,
        independent_analytic_agreement=True, original_R286_iid_baseline_agreement=True,
        R073='FROZEN', PESEN_v0_1='FROZEN', new_E2_predictions=0,
        new_E3_predictions=0, external_independent_replication='NOT_RUN', results=results)
    return rows, output

def emit(directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    rows, output = generate()
    with (directory/'R286_S82_ALL_576_MARKOV_REWARD_SOURCES.csv').open('w', newline='', encoding='utf-8') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(COLUMNS)
        w.writerows(rows)
    (directory/'R286_S82_EXACT_RESULTS.json').write_text(
        json.dumps(output, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    return output

if __name__ == '__main__':
    p = argparse.ArgumentParser()
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument('--test', action='store_true')
    g.add_argument('--emit')
    a = p.parse_args()
    if a.test:
        rows, out = generate()
        print(json.dumps({'pass': True, 'rows': len(rows), 'worlds': len(out['results'])}))
    else:
        out = emit(a.emit)
        print(json.dumps({'pass': True, 'rows': 576, 'worlds': len(out['results'])}))
