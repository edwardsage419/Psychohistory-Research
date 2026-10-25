#!/usr/bin/env python3
"""R143 frozen nine-world E1 audit: permutation Cramer and unmerged path tree.

Standard library only. Run:
  python r143_arrival_tie_bias_cramer_path_enum.py --self-test
  python r143_arrival_tie_bias_cramer_path_enum.py --output results.json
"""
import argparse
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

STATES = tuple(range(-2, 3))
GRID = (F(1, 4), F(1, 2), F(3, 4))
TIES = (F(0), F(1, 2), F(1))
HORIZON = 12


def fmt(x):
    return str(x)


def q_a(d, p, a):
    if d <= -3:
        return F(0)
    if d >= 3:
        return F(1)
    if d == -2:
        return p * a
    if d == 2:
        return p + (1 - p) * a
    return p


def det_permutation(matrix):
    """Exact Leibniz determinant; no Gaussian elimination or library solver."""
    n = len(matrix)
    result = F(0)
    for perm in itertools.permutations(range(n)):
        parity = sum(perm[i] > perm[j] for i in range(n) for j in range(i + 1, n))
        term = F(-1 if parity % 2 else 1)
        for i, j in enumerate(perm):
            term *= matrix[i][j]
        result += term
    return result


def cramer(matrix, rhs):
    denominator = det_permutation(matrix)
    assert denominator != 0, 'singular transient system'
    result = []
    for column in range(len(rhs)):
        repl = [[rhs[i] if j == column else matrix[i][j]
                 for j in range(len(rhs))] for i in range(len(rhs))]
        result.append(det_permutation(repl) / denominator)
    return result, denominator


def matrix_solution(p, a):
    matrix = [[F(int(i == j)) for j in range(5)] for i in range(5)]
    rhs_a = [F(0)] * 5
    for i, d in enumerate(STATES):
        qa = q_a(d, p, a)
        for step, prob in ((1, qa), (-1, 1 - qa)):
            d2 = d + step
            if d2 == 3:
                rhs_a[i] += prob
            elif d2 != -3:
                matrix[i][STATES.index(d2)] -= prob
    u, determinant = cramer(matrix, rhs_a)
    t, determinant2 = cramer(matrix, [F(1)] * 5)
    assert determinant == determinant2 != 0
    for i in range(5):
        assert sum(matrix[i][j] * u[j] for j in range(5)) == rhs_a[i]
        assert sum(matrix[i][j] * t[j] for j in range(5)) == 1
        assert 0 <= u[i] <= 1 and t[i] > 0
    return {'det': determinant, 'u': u, 't': t}


def unmerged_paths(p, a, horizon=HORIZON):
    """No merging of transient paths; absorbed branches retain exact mass."""
    leaves = []
    def walk(d, step, mass, absorbed, first_time):
        if step == horizon or absorbed:
            leaves.append((absorbed, mass, first_time))
            return
        qa = q_a(d, p, a)
        for move, prob in ((1, qa), (-1, 1 - qa)):
            if prob == 0:
                continue
            nxt = d + move
            lock = 'A' if nxt >= 3 else 'B' if nxt <= -3 else None
            walk(nxt, step + 1, mass * prob, lock, step + 1 if lock else None)
    walk(0, 0, F(1), None, None)
    totals = {k: sum((m for label, m, _ in leaves if label == k), F(0))
              for k in ('A', 'B', None)}
    passage = {t: sum((m for label, m, first in leaves if first == t), F(0))
               for t in range(1, horizon + 1)}
    assert sum(totals.values()) == 1
    return totals, passage, len(leaves)


def matrix_forward(p, a, horizon=HORIZON):
    live = {d: F(int(d == 0)) for d in STATES}
    locked = {'A': F(0), 'B': F(0)}
    passage = {}
    for step in range(1, horizon + 1):
        nxt = {d: F(0) for d in STATES}
        first = F(0)
        for d, mass in live.items():
            for move, prob in ((1, q_a(d, p, a)), (-1, 1 - q_a(d, p, a))):
                d2 = d + move
                delta = mass * prob
                if d2 >= 3:
                    locked['A'] += delta
                    first += delta
                elif d2 <= -3:
                    locked['B'] += delta
                    first += delta
                else:
                    nxt[d2] += delta
        live = nxt
        passage[step] = first
        assert sum(live.values()) + sum(locked.values()) == 1
    return {'A': locked['A'], 'B': locked['B'], None: sum(live.values())}, passage


def run_all():
    worlds = []
    for p, a in itertools.product(GRID, TIES):
        solution = matrix_solution(p, a)
        tree, passage, leaves = unmerged_paths(p, a)
        forward, fpassage = matrix_forward(p, a)
        assert tree == forward and passage == fpassage
        assert tree['A'] <= solution['u'][2]
        assert tree['B'] <= 1 - solution['u'][2]
        worlds.append({'p_R': fmt(p), 'tie_A': fmt(a),
                       'determinant': fmt(solution['det']),
                       'eventual_A_by_d': {str(d): fmt(solution['u'][i]) for i, d in enumerate(STATES)},
                       'expected_lock_steps_by_d': {str(d): fmt(solution['t'][i]) for i, d in enumerate(STATES)},
                       'horizon12': {'A': fmt(tree['A']), 'B': fmt(tree['B']), 'not_locked': fmt(tree[None])},
                       'first_passage': {str(k): fmt(v) for k, v in passage.items() if v},
                       'unmerged_terminal_branches': leaves})
    lookup = {(F(w['p_R']), F(w['tie_A'])): F(w['eventual_A_by_d']['0']) for w in worlds}
    for a in TIES:
        assert lookup[(GRID[0], a)] <= lookup[(GRID[1], a)] <= lookup[(GRID[2], a)]
    for p in GRID:
        assert lookup[(p, TIES[0])] <= lookup[(p, TIES[1])] <= lookup[(p, TIES[2])]
    baseline = next(w for w in worlds if w['p_R'] == '1/2' and w['tie_A'] == '1/2')
    assert baseline['eventual_A_by_d']['0'] == '1/2'
    assert baseline['expected_lock_steps_by_d']['0'] == '19/3'
    assert baseline['horizon12']['A'] == '29643/65536'
    assert baseline['horizon12']['B'] == '29643/65536'
    assert baseline['horizon12']['not_locked'] == '3125/32768'
    for j in range(5):
        assert F(baseline['first_passage'][str(3 + 2*j)]) == F(3, 8) * F(5, 8)**j
    assert all(int(t) % 2 == 1 and int(t) >= 3 for t in baseline['first_passage'])
    # Frozen negative controls: each wrong assertion must be rejected.
    negative = {}
    wrong_t2_lock = sum((q_a(d1, F(1, 2), F(1, 2)) * mass if d1 == 1 else
                         (1 - q_a(d1, F(1, 2), F(1, 2))) * mass)
                        for d1, mass in ((1, F(1, 2)), (-1, F(1, 2))))
    true_t2, _, _ = unmerged_paths(F(1, 2), F(1, 2), horizon=2)
    negative['incorrect_absorb_at_d2'] = wrong_t2_lock == F(1, 2) and true_t2['A'] == true_t2['B'] == 0
    bad_matrix = [[F(int(i == j)) for j in range(5)] for i in range(5)]
    bad_rhs = [F(0)] * 5
    for i, d in enumerate(STATES):
        qa = F(1, 2) if d == -2 else q_a(d, F(1, 2), F(1, 2))
        for move, prob in ((1, qa), (-1, 1 - qa)):
            dest = d + move
            if dest == 3:
                bad_rhs[i] += prob
            elif dest != -3:
                bad_matrix[i][STATES.index(dest)] -= prob
    bad_u, _ = cramer(bad_matrix, bad_rhs)
    negative['incorrect_q_minus2'] = bad_u[2] != F(1, 2)
    negative['incorrect_universal_half'] = lookup[(F(3, 4), F(1, 2))] != F(1, 2)
    assert all(negative.values()), negative
    return {'research_id': 'R143', 'evidence': 'E1', 'horizon': HORIZON,
            'world_count': len(worlds), 'starting_d': 0,
            'negative_controls': negative, 'worlds': worlds,
            'E2_new': 0, 'E3_new': 0, 'external_replication': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--self-test', action='store_true')
    args = parser.parse_args()
    result = run_all()
    payload = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + '\n'
    if args.output:
        args.output.write_text(payload, encoding='utf-8')
    if args.self_test:
        print('PASS R143 9 worlds Cramer exact and unmerged path tree, 3 negative controls')
    elif not args.output:
        print(payload, end='')


if __name__ == '__main__':
    main()
