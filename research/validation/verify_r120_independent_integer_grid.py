#!/usr/bin/env python3
"""Third-method R120 audit: integer midpoint grid, exact terminal-set counts.

The independent solver below does not call the original R120 algorithms.
Original solvers are imported solely for comparison after independent results.
All data are constructed E1. No human participants or real networks.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import sys
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research" / "R120"))
import r120_kkt_2003_uniform_linear_threshold_exact as original

EXPECTED_BLOBS = {
    "research/R120/r120_kkt_2003_uniform_linear_threshold_exact.py":
        "7029a679174828a6a74fd6adf849157e50285cff",
    "research/R120/test_r120_kkt_2003_uniform_linear_threshold_exact.py":
        "bba10681deac84fe765e51061359baa140b534cf",
    "research/R120/R120_KKT_2003_LINEAR_THRESHOLD_LIVE_EDGE_DISTRIBUTION_EQUIVALENCE_SCIENTIFIC_REPORT_2026-10-19.md":
        "bdb7ae43f142189c0f4f72ea3623165c87b0383a",
}
CSV_PATH = ROOT / "research" / "validation" / "R120_INTEGER_GRID_530_CASE_TERMINAL_DISTRIBUTIONS_2026-10-24.csv"


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def verify_identity(path: Path, expected_sha: str) -> None:
    if blob_sha(path.read_bytes()) != expected_sha:
        raise AssertionError("R120_SOURCE_IDENTITY_MISMATCH: " + str(path))


def independent_grid(n: int, edges: tuple, seeds: frozenset[int]) -> dict[frozenset[int], F]:
    """Enumerate uniform threshold cells using only integer comparisons.

    Every possible inbound subset weight is a multiple of 1/L. The midpoint
    of each of L equal threshold cells therefore represents that whole cell.
    Threshold indices remain fixed for every diffusion round.
    """
    if not 1 <= n <= 4 or any(u == v for u, v, _ in edges):
        raise ValueError("GRID_GRAPH_INVALID")
    if any(type(w) is not F or w < 0 or w > 1 for _, _, w in edges):
        raise ValueError("GRID_EXACT_WEIGHTS_REQUIRED")
    if any(v not in range(n) for v in seeds):
        raise ValueError("GRID_SEEDS_INVALID")
    denominator = math.lcm(*(w.denominator for _, _, w in edges))
    if denominator ** n > 50000:
        raise ValueError("GRID_EXCESSIVE_STATE_SPACE")
    integer_edges = [(u, v, w.numerator * (denominator // w.denominator))
                     for u, v, w in edges]
    for target in range(n):
        if sum(w for _, v, w in integer_edges if v == target) > denominator:
            raise ValueError("GRID_INBOUND_WEIGHT_OVER_ONE")
    counts: Counter[frozenset[int]] = Counter()
    for indices in product(range(denominator), repeat=n):
        active = set(seeds)
        for _ in range(n):
            additions = set()
            for target in range(n):
                if target in active:
                    continue
                incoming = sum(w for u, v, w in integer_edges
                               if v == target and u in active)
                if 2 * incoming >= 2 * indices[target] + 1:
                    additions.add(target)
            if not additions:
                break
            active.update(additions)
        counts[frozenset(active)] += 1
    total = denominator ** n
    if sum(counts.values()) != total:
        raise AssertionError("GRID_TOTAL_COUNT_WRONG")
    return {state: F(count, total) for state, count in counts.items()}


def mask(nodes) -> int:
    return sum(1 << node for node in nodes)


def compare_all(n, edges, seeds):
    independent = independent_grid(n, edges, frozenset(seeds))
    old_threshold = original.exact_threshold_distribution(n, edges, tuple(seeds))
    old_live = original.exact_live_edge_distribution(n, edges, tuple(seeds))
    if independent != old_threshold or independent != old_live:
        raise AssertionError("R120_FULL_DISTRIBUTION_MISMATCH")
    if sum(independent.values(), F(0)) != 1:
        raise AssertionError("R120_DISTRIBUTION_NOT_NORMALIZED")
    return independent


def generate_rows():
    rows = []
    graph_count = 0
    case_count = 0
    for n in (1, 2, 3):
        possible = tuple((u, v) for u in range(n)
                         for v in range(n) if u != v)
        for graph_mask in range(1 << len(possible)):
            pairs = tuple(edge for i, edge in enumerate(possible)
                          if graph_mask & (1 << i))
            degree = {v: sum(1 for _, dest in pairs if dest == v)
                      for v in range(n)}
            edges = tuple((u, v, F(1, degree[v])) for u, v in pairs)
            graph_count += 1
            for seed_mask in range(1 << n):
                seeds = frozenset(v for v in range(n)
                                  if seed_mask & (1 << v))
                result = compare_all(n, edges, seeds)
                case_count += 1
                for terminal in sorted(result, key=mask):
                    probability = result[terminal]
                    rows.append((n, graph_mask, seed_mask, mask(terminal),
                                 probability.numerator, probability.denominator))
    if (graph_count, case_count) != (69, 530):
        raise AssertionError("R120_COVERAGE_MISMATCH")
    return rows, graph_count, case_count


def serialize(rows):
    out = io.StringIO(newline="")
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(("n", "graph_mask", "seed_mask", "terminal_mask", "count", "total"))
    writer.writerows(rows)
    return out.getvalue().encode("utf-8")


def verify_csv(actual: bytes, expected: bytes):
    if actual != expected:
        raise AssertionError("R120_CSV_BYTE_MISMATCH")


def check_fixtures():
    single = ((0, 2, F(1, 2)), (1, 2, F(1, 4)))
    for seeds, expected in [((0,), F(3, 2)), ((1,), F(5, 4)),
                            ((0, 1), F(11, 4))]:
        distribution = compare_all(3, single, seeds)
        actual = sum((len(s) * p for s, p in distribution.items()), F(0))
        if actual != expected:
            raise AssertionError("R120_SINGLE_FIXTURE_MISMATCH")
    chain = ((0, 1, F(1, 2)), (1, 2, F(2, 3)),
             (2, 3, F(3, 4)))
    ring = ((0, 1, F(1, 2)), (1, 2, F(1, 2)),
            (2, 0, F(1, 2)))
    for n, edges, expected in [(4, chain, F(25, 12)),
                                (3, ring, F(7, 4))]:
        distribution = compare_all(n, edges, (0,))
        actual = sum((len(s) * p for s, p in distribution.items()), F(0))
        if actual != expected:
            raise AssertionError("R120_CHAIN_OR_CYCLE_MISMATCH")
    correct = sum((p for active, p in compare_all(3, single, (0, 1)).items()
                   if 2 in active), F(0))
    incorrect_independent_inbound = 1 - (1 - F(1, 2)) * (1 - F(1, 4))
    if correct != F(3, 4) or incorrect_independent_inbound != F(5, 8):
        raise AssertionError("R120_NEGATIVE_CONTROL_FAILED")


def check_tamper(expected):
    tampered = bytearray(expected)
    first_data_line = expected.index(b"\n") + 1
    count_column_start = expected.find(b",", first_data_line)
    if count_column_start < 0:
        raise AssertionError("R120_BAD_CSV_FORMAT")
    tampered[first_data_line] = ord("9")
    try:
        verify_csv(bytes(tampered), expected)
    except AssertionError:
        pass
    else:
        raise AssertionError("R120_TAMPER_NOT_REJECTED")
    path, good = next(iter(EXPECTED_BLOBS.items()))
    try:
        verify_identity(ROOT / path, "0" * 40)
    except AssertionError:
        pass
    else:
        raise AssertionError("R120_WRONG_SHA_NOT_REJECTED")


def main():
    for path, expected_sha in EXPECTED_BLOBS.items():
        verify_identity(ROOT / path, expected_sha)
    check_fixtures()
    rows, graphs, cases = generate_rows()
    expected = serialize(rows)
    verify_csv(CSV_PATH.read_bytes(), expected)
    check_tamper(expected)
    print(json.dumps({
        "result": "PASS_BOUNDED_INTERNAL_THIRD_METHOD_EXACT_E1",
        "graph_count": graphs,
        "graph_seed_cases": cases,
        "distribution_rows": len(rows),
        "csv_sha256": hashlib.sha256(expected).hexdigest(),
        "source_identity_checks": len(EXPECTED_BLOBS),
        "nonuniform_fixture_checks": 5,
        "negative_controls": 1,
        "tamper_rejections": 2,
        "real_human_E2": 0,
        "historical_E3": 0,
        "external_independent_reproduction": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
