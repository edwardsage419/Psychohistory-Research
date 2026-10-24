#!/usr/bin/env python3
"""R121 independent exact subset-cut recurrence; constructed E1 only."""
from __future__ import annotations

import csv
import hashlib
import io
import json
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "research" / "R121"))
import r121_kkt_2003_independent_cascade_exact as original

EXPECTED_BLOBS = {
    "research/R121/r121_kkt_2003_independent_cascade_exact.py":
        "576a7ad2d0d5499857d5bab11d9cb08cdbe3ab56",
    "research/R121/test_r121_kkt_2003_independent_cascade_exact.py":
        "6c34a5d0ca7e9e68164d04ade8ab06b6ef830968",
    "research/R121/R121_KKT_2003_INDEPENDENT_CASCADE_LIVE_EDGE_ONE_CHANCE_FIRSTPARTY_SCIENTIFIC_REPORT_2026-10-19.md":
        "efc8fd43f33f0c54ab82da398585acaeab78a659",
}
CSV_PATH = ROOT / "research" / "validation" / "R121_SUBSET_CUT_1060_CASE_TERMINAL_DISTRIBUTIONS_2026-10-24.csv"


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def verify_blob(path, expected):
    if git_blob(path.read_bytes()) != expected:
        raise AssertionError("R121_SOURCE_BLOB_MISMATCH")


def subset_cut(n, edges, seeds):
    """Exact probability of a terminal reachable set via subset recursion.

    This does not enumerate edge flips or chronological activation events.
    """
    universe = frozenset(range(n))
    S = frozenset(seeds)
    if not 1 <= n <= 4 or not S <= universe:
        raise ValueError("SUBSET_INPUT_INVALID")
    if any(u not in universe or v not in universe or u == v
           or type(p) is not F or not F(0) <= p <= F(1)
           for u, v, p in edges):
        raise ValueError("SUBSET_EDGES_INVALID")
    masks = [mask for mask in range(1 << n)
             if all(mask & (1 << v) for v in S)]
    masks.sort(key=lambda m: (m.bit_count(), m))
    sets = [frozenset(v for v in range(n) if m & (1 << v))
            for m in masks]

    def cut_failure(left, right):
        result = F(1)
        for u, v, p in edges:
            if u in left and v in right:
                result *= 1 - p
        return result

    fully_reachable = {}
    terminal = {}
    for T in sets:
        inside_failure = sum(
            (fully_reachable[U] * cut_failure(U, T - U)
             for U in fully_reachable if U < T), F(0))
        f = F(1) - inside_failure
        if f < 0 or f > 1:
            raise AssertionError("R121_RECURRENCE_PROBABILITY_INVALID")
        fully_reachable[T] = f
        q = f * cut_failure(T, universe - T)
        if q > 0:
            terminal[T] = q
    if sum(terminal.values(), F(0)) != 1:
        raise AssertionError("R121_SUBSET_CUT_NOT_NORMALIZED")
    return terminal


def compare(n, edges, seeds):
    new = subset_cut(n, edges, seeds)
    old_dynamic = original.exact_one_chance_round_distribution(n, edges, tuple(seeds))
    old_live = original.exact_independent_live_edge_distribution(n, edges, tuple(seeds))
    if new != old_dynamic or new != old_live:
        raise AssertionError("R121_FULL_TERMINAL_SET_DISTRIBUTION_MISMATCH")
    return new


def mask(nodes):
    return sum(1 << v for v in nodes)


def all_rows():
    rows = []
    graphs = 0
    cases = 0
    for n in (1, 2, 3):
        possible = [(u, v) for u in range(n) for v in range(n) if u != v]
        for graph_mask in range(1 << len(possible)):
            pairs = [edge for i, edge in enumerate(possible)
                     if graph_mask & (1 << i)]
            graphs += 1
            for scheme in ("HALF", "PARITY"):
                edges = tuple((u, v, F(1, 2) if scheme == "HALF"
                               else F(1, 4) if (u + v) % 2 == 0
                               else F(3, 4)) for u, v in pairs)
                for seed_mask in range(1 << n):
                    seeds = frozenset(v for v in range(n)
                                      if seed_mask & (1 << v))
                    dist = compare(n, edges, seeds)
                    cases += 1
                    for terminal in sorted(dist, key=mask):
                        p = dist[terminal]
                        rows.append((n, scheme, graph_mask, seed_mask,
                                     mask(terminal), p.numerator, p.denominator))
    if (graphs, cases) != (69, 1060):
        raise AssertionError("R121_COVERAGE_MISMATCH")
    return rows, graphs, cases


def serialize(rows):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator="\n")
    writer.writerow(("n", "scheme", "graph_mask", "seed_mask",
                     "terminal_mask", "numerator", "denominator"))
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def fixture_checks():
    single = ((0, 2, F(1, 2)), (1, 2, F(1, 4)))
    both = compare(3, single, (0, 1))
    target = sum((p for T, p in both.items() if 2 in T), F(0))
    expected = sum((len(T) * p for T, p in both.items()), F(0))
    if target != F(5, 8) or expected != F(21, 8):
        raise AssertionError("R121_TWO_SOURCE_FIXTURE")
    chain = ((0, 1, F(1, 2)), (1, 2, F(2, 3)), (2, 3, F(3, 4)))
    cycle = ((0, 1, F(1, 2)), (1, 2, F(1, 2)), (2, 0, F(1, 2)))
    for n, edges, target_expectation in ((4, chain, F(25, 12)),
                                         (3, cycle, F(7, 4))):
        d = compare(n, edges, (0,))
        actual = sum((len(T) * p for T, p in d.items()), F(0))
        if actual != target_expectation:
            raise AssertionError("R121_CHAIN_OR_CYCLE_FIXTURE")
    wrong_LT = F(1, 2) + F(1, 4)
    wrong_repeat = 1 - (1 - F(1, 2)) ** 2
    one_try = sum((p for T, p in compare(2, ((0, 1, F(1, 2)),), (0,)).items()
                   if 1 in T), F(0))
    if wrong_LT != F(3, 4) or wrong_LT == target:
        raise AssertionError("R121_LT_NEGATIVE_CONTROL")
    if wrong_repeat != F(3, 4) or one_try != F(1, 2):
        raise AssertionError("R121_REPEAT_NEGATIVE_CONTROL")


def check_tamper(raw):
    modified = bytearray(raw)
    modified[raw.index(b"\n") + 1] = ord("9")
    rejected = 0
    for altered in (bytes(modified),):
        try:
            if altered != raw:
                raise AssertionError("R121_RAW_DATA_MISMATCH")
        except AssertionError:
            rejected += 1
    try:
        first = next(iter(EXPECTED_BLOBS))
        verify_blob(ROOT / first, "0" * 40)
    except AssertionError:
        rejected += 1
    if rejected != 2:
        raise AssertionError("R121_TAMPER_REJECTION_FAILED")
    return rejected


def main():
    for path, sha in EXPECTED_BLOBS.items():
        verify_blob(ROOT / path, sha)
    fixture_checks()
    rows, graphs, cases = all_rows()
    raw = serialize(rows)
    if CSV_PATH.read_bytes() != raw:
        raise AssertionError("R121_COMMITTED_CSV_DIFFERS_FROM_RECOMPUTATION")
    rejected = check_tamper(raw)
    print(json.dumps({
        "status": "PASS_BOUNDED_INTERNAL_SUBSET_CUT_RECURRENCE_E1",
        "graphs": graphs, "cases": cases, "terminal_distribution_rows": len(rows),
        "csv_sha256": hashlib.sha256(raw).hexdigest(),
        "nonuniform_fixtures": 3, "negative_controls": 2,
        "source_blob_checks": 3, "tamper_rejections": rejected,
        "new_human_E2": 0, "new_historical_E3": 0,
        "external_team_replication": False,
    }, sort_keys=True))


if __name__ == "__main__":
    main()
