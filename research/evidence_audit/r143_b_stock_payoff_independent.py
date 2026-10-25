#!/usr/bin/env python3
"""B independent R143 audit: full stock counts and direct Arthur Table 1 payoffs."""
import argparse
import itertools
import json
from collections import defaultdict
from fractions import Fraction as F
from pathlib import Path

GRID = (F(1, 4), F(1, 2), F(3, 4))
TIES = (F(0), F(1, 2), F(1))


def choose_a_probability(a_payoff, b_payoff, tie_a):
    if a_payoff > b_payoff:
        return F(1)
    if a_payoff < b_payoff:
        return F(0)
    return tie_a


def stock_forward(p_r, tie_a, horizon=12):
    states = {(0, 0, 'none'): F(1)}
    mass_check = []
    for _ in range(horizon):
        next_states = defaultdict(F)
        for (n_a, n_b, lock), mass in states.items():
            # R payoffs: (2+nA, nB). S payoffs: (nA, 2+nB).
            r_a = choose_a_probability(2 + n_a, n_b, tie_a)
            s_a = choose_a_probability(n_a, 2 + n_b, tie_a)
            pa = p_r * r_a + (1 - p_r) * s_a
            for move_a, prob in ((True, pa), (False, 1 - pa)):
                if not prob:
                    continue
                new_a = n_a + int(move_a)
                new_b = n_b + int(not move_a)
                new_lock = lock
                if new_lock == 'none' and new_a - new_b >= 3:
                    new_lock = 'A'
                if new_lock == 'none' and new_b - new_a >= 3:
                    new_lock = 'B'
                next_states[(new_a, new_b, new_lock)] += mass * prob
        states = dict(next_states)
        total = sum(states.values(), F(0))
        assert total == 1
        mass_check.append(str(total))
    results = {label: sum((v for (_, _, lock), v in states.items() if lock == label), F(0))
               for label in ('A', 'B', 'none')}
    assert sum(results.values()) == 1
    return {label: str(v) for label, v in results.items()}, len(states), mass_check


def audit(reference):
    output = []
    for p, a in itertools.product(GRID, TIES):
        res, nstates, mass_check = stock_forward(p, a)
        output.append({'p_R': str(p), 'tie_A': str(a), 'horizon12': res,
                       'final_stock_states': nstates, 'round_masses': mass_check})
    if reference:
        ref = json.loads(Path(reference).read_text(encoding='utf-8'))
        expected = {(x['p_R'], x['tie_A']): x['horizon12'] for x in ref['worlds']}
        assert len(expected) == len(output) == 9
        for row in output:
            actual = row['horizon12']
            assert actual['A'] == expected[(row['p_R'], row['tie_A'])]['A']
            assert actual['B'] == expected[(row['p_R'], row['tie_A'])]['B']
            assert actual['none'] == expected[(row['p_R'], row['tie_A'])]['not_locked']
    base = next(x for x in output if x['p_R'] == '1/2' and x['tie_A'] == '1/2')
    assert base['horizon12'] == {'A': '29643/65536', 'B': '29643/65536', 'none': '3125/32768'}
    # Direct two-round probability mass at |d|=2 is 1/2, but no lock is possible by t=2.
    two, _, _ = stock_forward(F(1, 2), F(1, 2), horizon=2)
    assert two == {'A': '0', 'B': '0', 'none': '1'}
    return {'research_id': 'R143', 'evidence': 'E1', 'method': 'direct_stock_payoff_Fraction',
            'world_count': 9, 'comparison_count': 27 if reference else 0,
            'wrong_d2_lock_control_rejected': True, 'worlds': output,
            'new_E2': 0, 'new_E3': 0, 'external_replication': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--reference', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = audit(args.reference)
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(payload, encoding='utf-8')
    else:
        print(payload)
    print('PASS B R143 direct stock payoff 9 worlds; 27 independent exact comparisons' if args.reference else 'PASS B R143 9 worlds')


if __name__ == '__main__':
    main()
