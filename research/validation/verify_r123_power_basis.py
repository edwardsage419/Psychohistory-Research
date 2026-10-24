#!/usr/bin/env python3
"""R123 DeGroot 1974 / Berger 1981 third-method finite E1 audit.

Frozen protocol: 226 row-stochastic matrices, exact Fraction W**256,
maximum basis-vector spread <= 2**-24. Synthetic mathematics only.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
from fractions import Fraction as F
from itertools import combinations, product
from math import gcd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'research' / 'R123'
BLOBS = {
    'r123_degroot_1974_berger_1981_exact_consensus.py': 'c4dfe0ba8b5778440676dd1bf3fa01bbc4bf440e',
    'test_r123_degroot_1974_berger_1981_exact_consensus.py': 'c34b9617ec569d5ef7f459dba347b85a70665074',
    'R123_DEGROOT_1974_BERGER_1981_ORIGINAL_CONSENSUS_AND_INFLUENCE_SCIENTIFIC_REPORT_2026-10-19.md': 'f2dfc14370fb437380ef7b10260f73dc5ede689d',
}
FIELDS = ('matrix_id', 'n', 'matrix_rows', 'basis_spreads', 'max_basis_spread',
          'finite_horizon_consensus', 'structural_consensus', 'original_classifier')
HORIZON = 256
TOL = F(1, 2**24)


def blob_sha(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def check_sources(expected):
    for name, sha in expected.items():
        found = blob_sha((SOURCE / name).read_bytes())
        if found != sha:
            raise AssertionError('SOURCE_BLOB_MISMATCH ' + name)


def row_options(n):
    rows = [tuple(F(int(j == i)) for j in range(n)) for i in range(n)]
    rows += [tuple(F(1, 2) if j in (a, b) else F(0) for j in range(n))
             for a, b in combinations(range(n), 2)]
    return rows


def structural_consensus(w):
    """Independent reachability and recurrent-class period test."""
    n = len(w)
    adj = [set(j for j, weight in enumerate(row) if weight) for row in w]
    reach = []
    for i in range(n):
        seen, queue = {i}, [i]
        for node in queue:
            for j in adj[node]:
                if j not in seen:
                    seen.add(j)
                    queue.append(j)
        reach.append(seen)
    remaining, closed = set(range(n)), []
    while remaining:
        root = min(remaining)
        group = {j for j in remaining if root in reach[j] and j in reach[root]}
        remaining -= group
        if all(adj[j] <= group for j in group):
            closed.append(group)
    if len(closed) != 1:
        return False
    group = closed[0]
    root = min(group)
    dist, queue = {root: 0}, [root]
    for node in queue:
        for j in adj[node]:
            if j in group and j not in dist:
                dist[j] = dist[node] + 1
                queue.append(j)
    period = 0
    for node in group:
        for j in adj[node]:
            period = gcd(period, abs(dist[node] + 1 - dist[j]))
    return period == 1


def power_basis_spreads(w):
    """Multiply exact Fraction matrices; no original R123 power routine."""
    n = len(w)
    current = tuple(tuple(F(int(i == j)) for j in range(n)) for i in range(n))
    for _ in range(HORIZON):
        current = tuple(tuple(sum((current[i][k] * w[k][j]
                                   for k in range(n)), F(0))
                              for j in range(n)) for i in range(n))
    spreads = tuple(max(current[i][j] for i in range(n)) -
                    min(current[i][j] for i in range(n)) for j in range(n))
    return spreads, current


def controls():
    swap = ((F(0), F(1)), (F(1), F(0)))
    identity = ((F(1), F(0)), (F(0), F(1)))
    leader = ((F(1), F(0)), (F(1, 2), F(1, 2)))
    original = ((F(1, 2), F(1, 2)), (F(1, 4), F(3, 4)))
    assert not structural_consensus(swap)
    assert max(power_basis_spreads(swap)[0]) > TOL
    assert tuple(sum((swap[i][j] * F(1, 2) for j in range(2)), F(0))
                 for i in range(2)) == (F(1, 2), F(1, 2))
    assert not structural_consensus(identity)
    assert power_basis_spreads(identity)[0] == (F(1), F(1))
    assert structural_consensus(leader)
    assert max(power_basis_spreads(leader)[0]) <= TOL
    assert structural_consensus(original)
    spreads, powered = power_basis_spreads(original)
    assert max(spreads) <= TOL
    assert abs(powered[0][1] - F(2, 3)) <= TOL
    assert F(1, 3) + F(2, 3) == 1
    return 4


def render(check_original=False):
    original = None
    if check_original:
        sys.path.insert(0, str(SOURCE))
        import r123_degroot_1974_berger_1981_exact_consensus as original
    out = io.StringIO(newline='')
    writer = csv.DictWriter(out, fieldnames=FIELDS, lineterminator='\n')
    writer.writeheader()
    totals = {1: 0, 2: 0, 3: 0}
    universals = 0
    for n in (1, 2, 3):
        for w in product(row_options(n), repeat=n):
            totals[n] += 1
            structural = structural_consensus(w)
            spreads, _ = power_basis_spreads(w)
            finite = max(spreads) <= TOL
            if original is not None:
                observed = original.support_structure(w)['all_initial_consensus_guaranteed']
                if observed != structural:
                    raise AssertionError(f'ORIGINAL_STRUCTURE_DISAGREEMENT n={n} matrix={w}')
            else:
                observed = structural
            if finite != observed:
                raise AssertionError(f'FROZEN_256_POWER_MISMATCH n={n} matrix={w} spread={max(spreads)}')
            universals += int(structural)
            writer.writerow({
                'matrix_id': f'n{n}_{totals[n]:03d}',
                'n': n,
                'matrix_rows': ';'.join(','.join(map(str, row)) for row in w),
                'basis_spreads': ';'.join(map(str, spreads)),
                'max_basis_spread': str(max(spreads)),
                'finite_horizon_consensus': int(finite),
                'structural_consensus': int(structural),
                'original_classifier': int(observed),
            })
    assert totals == {1: 1, 2: 9, 3: 216} and universals == 176
    return out.getvalue().encode('utf-8'), totals, universals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    if args.verify:
        check_sources(BLOBS)
    raw, totals, universals = render(check_original=args.verify)
    controls_count = controls()
    path = Path(args.output)
    if args.verify:
        assert path.read_bytes() == raw, 'RAW_CSV_BYTE_MISMATCH'
        assert path.read_bytes() + b'X' != raw, 'TAMPER_REJECTION_FAILED'
        false_blobs = dict(BLOBS)
        false_blobs['r123_degroot_1974_berger_1981_exact_consensus.py'] = '0' * 40
        try:
            check_sources(false_blobs)
        except AssertionError as exc:
            assert 'SOURCE_BLOB_MISMATCH' in str(exc)
        else:
            raise AssertionError('FALSE_BLOB_REJECTION_FAILED')
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    print(f'R123_AUDIT_PASS total={sum(totals.values())} universal={universals} '
          f'controls={controls_count} csv_sha256={hashlib.sha256(raw).hexdigest()} '
          f'verify={args.verify}')


if __name__ == '__main__':
    main()
