#!/usr/bin/env python3
"""Independent exact Markov-chain-tree audit for R136 Press-Dyson memory-one games.

Only Python standard library is required. The method never invokes the
existing Gaussian elimination or determinant payoff solvers.
"""
import argparse
import csv
import hashlib
import io
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

STATES = ('CC', 'CD', 'DC', 'DD')
PAY_X = (3, 0, 5, 1)
PAY_Y = (3, 5, 0, 1)
Q_GRID = tuple(itertools.product((F(1, 4), F(1, 2), F(3, 4)), repeat=4))


def rooted_trees(root):
    """Enumerate every oriented in-tree: each non-root node points to parent."""
    others = tuple(i for i in range(4) if i != root)
    trees = []
    for parents in itertools.product(range(4), repeat=3):
        nxt = dict(zip(others, parents))
        if any(nxt[u] == u for u in others):
            continue
        valid = True
        for start in others:
            seen = set()
            cur = start
            while cur != root:
                if cur in seen:
                    valid = False
                    break
                seen.add(cur)
                cur = nxt[cur]
            if not valid:
                break
        if valid:
            trees.append(tuple((u, nxt[u]) for u in others))
    return tuple(trees)


TREES = tuple(rooted_trees(r) for r in range(4))
assert tuple(map(len, TREES)) == (16, 16, 16, 16)


def transition(p, q, swap=True):
    y = (q[0], q[2], q[1], q[3]) if swap else q
    return tuple(tuple((a*b, a*(1-b), (1-a)*b, (1-a)*(1-b)))
                 for a, b in zip(p, y))


def stationary_tree(P):
    tau = tuple(sum((__import__('functools').reduce(
        lambda acc, edge: acc * P[edge[0]][edge[1]], tree, F(1))
        for tree in TREES[root]), F(0)) for root in range(4))
    total = sum(tau)
    if total == 0:
        return None, tau
    v = tuple(x / total for x in tau)
    assert sum(v) == 1
    assert all(sum(v[i] * P[i][j] for i in range(4)) == v[j] for j in range(4))
    return v, tau


def payoffs(v):
    return (sum(v[i] * PAY_X[i] for i in range(4)),
            sum(v[i] * PAY_Y[i] for i in range(4)))


def extortion_strategy(chi, phi):
    return (1 - 2*phi*(chi-1), 1-phi*(4*chi+1), phi*(chi+4), F(0))


def check_source(path):
    if path is None:
        return 'NOT_SUPPLIED'
    data = Path(path).read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    expected = 'a1495bc01a71064e190116e2ec71580aa3e8e1f1'
    assert blob == expected, (blob, expected)
    obj = json.loads(data)
    assert obj['extortion']['exact_pairs'] == 1134
    assert obj['equalizer']['checked_opponents'] == 81
    return blob


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', help='Exact research/R136/R136_MATHEMATICAL_RESULTS.json')
    parser.add_argument('--output', help='Optional deterministic CSV file')
    args = parser.parse_args()
    source_blob = check_source(args.source)
    chis = (2, 3, 5, 7)
    phis = (F(1, 100), F(1, 50), F(1, 25), F(1, 20), F(1, 10))
    valid = [(chi, phi, extortion_strategy(chi, phi))
             for chi in chis for phi in phis
             if all(0 <= a <= 1 for a in extortion_strategy(chi, phi))]
    assert len(valid) == 14, len(valid)
    out = io.StringIO(newline='')
    writer = csv.writer(out, lineterminator='\n')
    writer.writerow(['class', 'chi', 'phi', 'q1', 'q2', 'q3', 'q4',
                     'tau_sum', 'v_CC', 'v_CD', 'v_DC', 'v_DD',
                     'pay_X', 'pay_Y', 'identity_residual'])
    counts = {'extortion': 0, 'equalizer': 0, 'stationary_nonunique': 0,
              'negative_control_q_order': 0, 'negative_control_normalization': 0,
              'posthoc_q_transition_difference': 0}
    for chi, phi, p in valid:
        for q in Q_GRID:
            P = transition(p, q)
            v, tau = stationary_tree(P)
            assert v is not None
            x, y = payoffs(v)
            residual = x - 1 - chi*(y-1)
            assert residual == 0, (chi, phi, q, residual)
            writer.writerow(['extortion', chi, str(phi), *map(str, q),
                             str(sum(tau)), *map(str, v), str(x), str(y), str(residual)])
            counts['extortion'] += 1
    eq_p = (F(9, 10), F(3, 4), F(1, 8), F(1, 20))
    for q in Q_GRID:
        P = transition(eq_p, q)
        v, tau = stationary_tree(P)
        assert v is not None
        x, y = payoffs(v)
        assert y == F(5, 3)
        writer.writerow(['equalizer', '', '', *map(str, q),
                         str(sum(tau)), *map(str, v), str(x), str(y), str(y-F(5, 3))])
        counts['equalizer'] += 1
    assert counts['extortion'] == 1134
    assert counts['equalizer'] == 81
    p = extortion_strategy(3, F(1, 20))
    for q in ((F(1), F(1), F(0), F(0)), (F(1), F(1), F(1), F(0))):
        v, tau = stationary_tree(transition(p, q))
        assert v is None and sum(tau) == 0
        counts['stationary_nonunique'] += 1
    # Pre-registered negative control is non-discriminating: the ZD payoff
    # identity is invariant to opponent strategies, including misordered q.
    for chi, phi, p in valid:
        for q in Q_GRID:
            if q[1] == q[2]:
                continue
            v, _ = stationary_tree(transition(p, q, swap=False))
            if v is not None:
                x, y = payoffs(v)
                if x - 1 - chi*(y-1) != 0:
                    counts['negative_control_q_order'] = 1
                    break
        if counts['negative_control_q_order']:
            break
    # Posthoc diagnostic is labelled separately from the frozen negative control.
    asymmetric_q = (F(1,4), F(1,2), F(3,4), F(1,4))
    counts['posthoc_q_transition_difference'] = int(
        transition(p, asymmetric_q, True) != transition(p, asymmetric_q, False))
    assert counts['posthoc_q_transition_difference'] == 1
    P = transition(valid[0][2], Q_GRID[0])
    v, tau = stationary_tree(P)
    assert sum(tau) != 1 and sum(tau) != 0
    assert sum(tau) != sum(v)
    counts['negative_control_normalization'] = 1
    raw = out.getvalue().encode('utf-8')
    if args.output:
        Path(args.output).write_bytes(raw)
    result = {'method': 'four_state_markov_chain_directed_tree_exact_fraction',
              'source_git_blob_sha1': source_blob,
              'rooted_tree_counts': list(map(len, TREES)),
              'valid_extortion_strategies': len(valid),
              'counts': counts, 'csv_rows': counts['extortion']+counts['equalizer'],
              'csv_sha256': hashlib.sha256(raw).hexdigest(),
              'csv_bytes': len(raw),
              'evidence': 'E1_INTERNAL_ONLY', 'E2': 0, 'E3': 0}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
