#!/usr/bin/env python3
"""R119 third-method finite graph reachability audit, internal constructed E1."""
from collections import deque
import csv
from fractions import Fraction as F
import hashlib
import importlib.util
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "research/R119/r119_watts_2002_fraction_neighbor_cascade.py"
TESTS = ROOT / "research/R119/test_r119_watts_2002_fraction_neighbor_cascade.py"
DATA = ROOT / "research/validation/R119_GRAPH_REACHABILITY_687_CONSTRUCTED_WORLDS_2026-10-24.csv"
BLOBS = {
    SOURCE: "91d1853638fe5f3b3fe241d5fc952cceaee882a4",
    TESTS: "2e2209cddb0bd8f6654390c6ceee7cecc3354a27",
}
PALETTE = (F(1, 3), F(1, 2), F(2, 3))
FIELDS = ("n", "graph_mask", "threshold_codes", "seed", "reachable_state_count",
          "terminal_mask", "terminal_count", "transition_edges", "final_participants")


def git_blob(path):
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def reachable_graph(n, edges, thresholds, seed):
    """All reachable one-node entry orders, independent of R119 solvers."""
    if len(thresholds) != n or not 1 <= n <= 6 or not 0 <= seed < n:
        raise ValueError("BAD_FINITE_INPUT")
    neighbors = [0] * n
    for a, b in edges:
        if a == b or not 0 <= a < n or not 0 <= b < n:
            raise ValueError("BAD_EDGE")
        neighbors[a] |= 1 << b
        neighbors[b] |= 1 << a
    seen = {1 << seed}
    todo = deque([1 << seed])
    terminal = set()
    edges_count = 0
    while todo:
        state = todo.popleft()
        successors = []
        for v in range(n):
            if state & (1 << v):
                continue
            degree = neighbors[v].bit_count()
            if degree == 0:
                continue
            active_neighbors = (neighbors[v] & state).bit_count()
            if F(active_neighbors, degree) >= thresholds[v]:
                nxt = state | (1 << v)
                if (nxt & state) != state or nxt.bit_count() != state.bit_count() + 1:
                    raise AssertionError("NON_MONOTONE")
                successors.append(nxt)
        edges_count += len(successors)
        if not successors:
            terminal.add(state)
        for nxt in successors:
            if nxt not in seen:
                seen.add(nxt)
                todo.append(nxt)
    if len(terminal) != 1:
        raise AssertionError(("NONUNIQUE_TERMINAL", n, edges, thresholds, seed))
    last = next(iter(terminal))
    return len(seen), last, len(terminal), edges_count, last.bit_count()


def construct_rows():
    rows = []
    counts = {}
    for n in range(1, 4):
        pairs = tuple(combinations(range(n), 2))
        count = 0
        for graph_mask in range(1 << len(pairs)):
            edges = tuple(e for j, e in enumerate(pairs) if graph_mask & (1 << j))
            for codes in product(range(3), repeat=n):
                thresholds = tuple(PALETTE[c] for c in codes)
                for seed in range(n):
                    states, terminal, terminals, arcs, final = reachable_graph(n, edges, thresholds, seed)
                    rows.append(dict(zip(FIELDS, map(str, (
                        n, graph_mask, ":".join(map(str, codes)), seed, states,
                        terminal, terminals, arcs, final,
                    )))))
                    count += 1
        counts[str(n)] = count
    if counts != {"1": 3, "2": 36, "3": 648} or len(rows) != 687:
        raise AssertionError("FINITE_CENSUS_MISMATCH")
    return rows, counts


def load_original():
    for path, sha in BLOBS.items():
        if git_blob(path) != sha:
            raise AssertionError(("SOURCE_BLOB_IDENTITY_CHANGED", str(path)))
    spec = importlib.util.spec_from_file_location("r119_original", SOURCE)
    if spec is None or spec.loader is None:
        raise AssertionError("IMPORT_FAILURE")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def branch_ratio(pk, rho):
    z = sum((F(k) * p for k, p in enumerate(pk)), F(0))
    return sum((F(k * (k - 1)) * p * rho[k] for k, p in enumerate(pk)), F(0)) / z


def main():
    rows, counts = construct_rows()
    with DATA.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if tuple(reader.fieldnames or ()) != FIELDS or list(reader) != rows:
            raise AssertionError("CONSTRUCTED_DATA_REPLAY_MISMATCH")
    data_sha256 = hashlib.sha256(DATA.read_bytes()).hexdigest()
    original = load_original()
    for row in rows:
        n = int(row["n"])
        pairs = tuple(combinations(range(n), 2))
        graph_mask = int(row["graph_mask"])
        edges = tuple(e for j, e in enumerate(pairs) if graph_mask & (1 << j))
        thresholds = tuple(PALETTE[int(c)] for c in row["threshold_codes"].split(":"))
        seed = int(row["seed"])
        expected_mask = int(row["terminal_mask"])
        actual = original.synchronous_cascade(n, edges, thresholds, seed)["active"]
        async_result = original.independently_asynchronous_cascade(n, edges, thresholds, seed)
        if sum(1 << v for v in actual) != expected_mask or actual != async_result:
            raise AssertionError(("SOLVER_DISAGREEMENT", row))

    h = F(1, 2)
    cycle = tuple((i, i + 1) for i in range(5)) + ((5, 0),)
    triangles = ((0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5))
    cycle_final = reachable_graph(6, cycle, (h,) * 6, 0)[-1]
    triangle_final = reachable_graph(6, triangles, (h,) * 6, 0)[-1]
    diamond = ((0, 1), (0, 2), (1, 3), (2, 3))
    diamond_final = reachable_graph(4, diamond, (h, h, h, F(3, 4)), 0)[-1]
    isolated_final = reachable_graph(4, ((0, 1),), (h,) * 4, 0)[-1]
    if (cycle_final, triangle_final, diamond_final, isolated_final) != (6, 3, 4, 2):
        raise AssertionError("FROZEN_TOPOLOGY_COUNTEREXAMPLES")

    cases = (
        ((F(0), F(0), F(0), F(1)), (F(0), F(0), F(0), F(1)), F(2)),
        ((F(0), F(0), F(0), F(1)), (F(0), F(0), F(0), F(0)), F(0)),
        ((F(0), F(0), F(1)), (F(0), F(0), F(1)), F(1)),
    )
    for pk, rho, expected in cases:
        if branch_ratio(pk, rho) != expected:
            raise AssertionError("INDEPENDENT_BRANCHING_MATH")
        if original.branching_ratio(pk, rho)["branching_ratio"] != expected:
            raise AssertionError("ORIGINAL_BRANCHING_DISAGREEMENT")

    if cycle_final == 3 or cycle_final == triangle_final:
        raise AssertionError("TOPOLOGY_TAMPER_UNDETECTED")
    if diamond_final == 3:
        raise AssertionError("EXPECTED_SIZE_TAMPER_UNDETECTED")

    receipt = {
        "research_id": "R119", "catalogue_id": "04-002",
        "status": "PASS_BOUNDED_INTERNAL_INDEPENDENT_GRAPH_REACHABILITY_E1",
        "constructed_worlds": len(rows), "worlds_by_n": counts,
        "original_solver_comparisons": len(rows),
        "topology_final_sizes": {"cycle": cycle_final, "triangles": triangle_final,
                                 "diamond": diamond_final, "isolated": isolated_final},
        "independent_branching_ratios": [str(x[-1]) for x in cases],
        "tamper_controls_rejected": 2,
        "source_blob_sha1": {str(p.relative_to(ROOT)): git_blob(p) for p in BLOBS},
        "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in BLOBS},
        "constructed_csv_sha256": data_sha256,
        "new_human_E2": 0, "new_historical_E3": 0,
        "external_independent_replication": False,
        "R073": "FROZEN", "PESEN_v0_1": "FROZEN",
    }
    print(json.dumps(receipt, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
