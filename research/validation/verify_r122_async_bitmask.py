#!/usr/bin/env python3
"""Independent R122 asynchronous reachability audit under frozen 2026-10-24 protocol.

Purely constructed E1 graph states. No human observations are used.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
from collections import deque
from itertools import combinations
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / 'research' / 'R122'
EXPECTED_BLOBS = {
    'r122_centola_macy_2007_distinct_neighbor_complex_contagion.py': 'bde1c39fc9b536aaa794209ceaf76c90407d0f16',
    'test_r122_centola_macy_2007_distinct_neighbor_complex_contagion.py': '6058f0f4ddb5f0fdcaf643e969374507f6a70063',
    'R122_CENTOLA_MACY_2007_COMPLEX_CONTAGION_BRIDGE_SCIENTIFIC_REPORT_2026-10-19.md': '7301d5a7b026feaa16ce7ac8e942d60a7ad1af63',
}
FIELDS = ['n', 'graph_mask', 'threshold_mask', 'seed_mask', 'terminal_mask', 'reachable_states']
COUNTS = {1: 2, 2: 32, 3: 512, 4: 16384}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def check_source_integrity(expected=EXPECTED_BLOBS):
    for name, sha in expected.items():
        actual = git_blob_sha((ORIGINAL / name).read_bytes())
        if actual != sha:
            raise AssertionError(f'SOURCE_SHA_MISMATCH {name} expected={sha} actual={actual}')


def adj_masks(n: int, graph_mask: int):
    adj = [0] * n
    pairs = tuple(combinations(range(n), 2))
    for i, (u, v) in enumerate(pairs):
        if graph_mask & (1 << i):
            adj[u] |= 1 << v
            adj[v] |= 1 << u
    return tuple(adj), tuple(p for i, p in enumerate(pairs) if graph_mask & (1 << i))


def independent_async_terminal(n: int, graph_mask: int, threshold_mask: int, seed_mask: int):
    """Enumerate all reachable single-node addition schedules without original solvers."""
    adj, _ = adj_masks(n, graph_mask)
    seen = {seed_mask}
    queue = deque([seed_mask])
    terminals = set()
    while queue:
        state = queue.popleft()
        next_states = []
        for node in range(n):
            bit = 1 << node
            if not state & bit and (adj[node] & state).bit_count() >= (1 + bool(threshold_mask & bit)):
                next_states.append(state | bit)
        if not next_states:
            terminals.add(state)
        for nxt in next_states:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    if len(terminals) != 1:
        raise AssertionError(f'NONCONFLUENT_TERMINALS {n} {graph_mask} {threshold_mask} {seed_mask}: {terminals}')
    return next(iter(terminals)), len(seen)


def original_reference(n, graph_mask, threshold_mask, seed_mask):
    sys.path.insert(0, str(ORIGINAL))
    import r122_centola_macy_2007_distinct_neighbor_complex_contagion as original
    _, edges = adj_masks(n, graph_mask)
    seeds = tuple(i for i in range(n) if seed_mask & (1 << i))
    t = tuple(1 + bool(threshold_mask & (1 << i)) for i in range(n))
    sync = original.synchronous_distinct_neighbor_cascade(n, edges, t, seeds)['final']
    closed = original.independent_least_closed_set(n, edges, t, seeds)
    if sync != closed:
        raise AssertionError('ORIGINAL_TWO_SOLVERS_DISAGREE')
    return sum(1 << i for i in sync)


def rows():
    counts = {n: 0 for n in COUNTS}
    for n in range(1, 5):
        for graph_mask in range(1 << (n * (n - 1) // 2)):
            for threshold_mask in range(1 << n) if n >= 2 else (0,):
                for seed_mask in range(1 << n):
                    terminal, states = independent_async_terminal(n, graph_mask, threshold_mask, seed_mask)
                    expected = original_reference(n, graph_mask, threshold_mask, seed_mask)
                    if terminal != expected:
                        raise AssertionError(f'THIRD_METHOD_DIVERGED {n} {graph_mask} {threshold_mask} {seed_mask}')
                    counts[n] += 1
                    yield [n, graph_mask, threshold_mask, seed_mask, terminal, states]
    if counts != COUNTS:
        raise AssertionError(f'CASE_COUNT_DRIFT {counts}')


def serialize_rows():
    buffer = io.StringIO(newline='')
    writer = csv.writer(buffer, lineterminator='\n')
    writer.writerow(FIELDS)
    count = 0
    for row in rows():
        writer.writerow(row)
        count += 1
    if count != 16930:
        raise AssertionError('TOTAL_CASE_COUNT_DRIFT')
    return buffer.getvalue().encode('utf-8'), count


def verify_csv(data: bytes, expected: bytes):
    if data != expected:
        raise AssertionError('CSV_BYTE_REPLAY_MISMATCH')
    return True


def negative_controls():
    # One repeated report from a single neighbor remains one distinct source.
    one, _ = independent_async_terminal(2, 1, 2, 1)
    if one != 1:
        raise AssertionError('SINGLE_NEIGHBOR_REPEATED_EXPOSURE_WRONGLY_COUNTS_TWICE')
    # Two disjoint triangles; 3 edges can be dispersed or reinforced.
    pairs = tuple(combinations(range(6), 2))
    internal = {(0,1),(0,2),(1,2),(3,4),(3,5),(4,5)}
    variants = {
        'narrow': {(2,3)},
        'dispersed': {(0,3),(1,4),(2,5)},
        'reinforced': {(1,3),(2,3),(2,4)},
    }
    for name, bridges in variants.items():
        graph_mask = sum(1 << i for i, edge in enumerate(pairs) if edge in internal | bridges)
        simple, _ = independent_async_terminal(6, graph_mask, 0, 7)
        complex_, _ = independent_async_terminal(6, graph_mask, 63, 7)
        if (simple, complex_) != (63, 63 if name == 'reinforced' else 7):
            raise AssertionError(f'BRIDGE_NEGATIVE_CONTROL_FAILED {name}')
    return 4


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--verify', action='store_true')
    args = parser.parse_args()
    check_source_integrity()
    controls = negative_controls()
    # Prove a deliberately false original blob identity fails closed.
    try:
        check_source_integrity({next(iter(EXPECTED_BLOBS)): '0' * 40})
    except AssertionError:
        pass
    else:
        raise AssertionError('WRONG_BLOB_SHA_NOT_REJECTED')
    expected, count = serialize_rows()
    if args.verify:
        verify_csv(args.output.read_bytes(), expected)
        altered = bytearray(expected)
        altered[-2] = 49 if altered[-2] != 49 else 50
        try:
            verify_csv(bytes(altered), expected)
        except AssertionError:
            pass
        else:
            raise AssertionError('ALTERED_CSV_NOT_REJECTED')
    else:
        if args.output.exists():
            raise FileExistsError('Refusing to overwrite an existing raw audit CSV')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(expected)
    print(f'R122_AUDIT_PASS cases={count} negative_controls={controls} source_blobs={len(EXPECTED_BLOBS)} '
          f'csv_sha256={hashlib.sha256(expected).hexdigest()} verify={args.verify}')


if __name__ == '__main__':
    main()
