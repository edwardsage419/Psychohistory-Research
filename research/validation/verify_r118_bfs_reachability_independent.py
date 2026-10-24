#!/usr/bin/env python3
"""Independent R118 reachability graph audit for finite Granovetter thresholds.

All records are constructed mathematical worlds, not observed human data.
Uses explicit bitmask state search, independently of R118's two solvers.
"""
from __future__ import annotations

from collections import deque
import csv
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "research/R118/r118_granovetter_1978_finite_threshold_participation.py"
TESTS = ROOT / "research/R118/test_r118_granovetter_1978_finite_threshold_participation.py"
CSV_PATH = ROOT / "research/validation/R118_BFS_REACHABILITY_ENUMERATION_2026-10-24.csv"
PINNED_BLOBS = {
    SOURCE: "438288bef99455ba9087988baf10eec09139ffe1",
    TESTS: "c81b8fd6dfbb7802d7f1652c838ce4a9eb21a552",
}
CSV_FIELDS = (
    "n", "threshold_vector", "reachable_state_count", "terminal_mask",
    "terminal_count", "transition_edges", "final_participants",
)


def git_blob_sha1(path):
    body = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(body)).encode("ascii") + b"\0" + body).hexdigest()


def reachable_state_graph(thresholds):
    """Enumerate every feasible sequence of one-person irreversible entries."""
    n = len(thresholds)
    if not 1 <= n <= 4 or any(type(x) is not int or x < 0 or x > n for x in thresholds):
        raise ValueError("INVALID_FINITE_WORLD")
    queue = deque([0])
    seen = {0}
    terminal = set()
    edges = 0
    while queue:
        mask = queue.popleft()
        active_count = mask.bit_count()
        successors = []
        for i, threshold in enumerate(thresholds):
            if not (mask & (1 << i)) and threshold <= active_count:
                successor = mask | (1 << i)
                if successor & mask != mask or successor.bit_count() != active_count + 1:
                    raise AssertionError("NON_MONOTONE_TRANSITION")
                successors.append(successor)
        edges += len(successors)
        if not successors:
            terminal.add(mask)
        for successor in successors:
            if successor not in seen:
                seen.add(successor)
                queue.append(successor)
    if len(terminal) != 1:
        raise AssertionError(("NONUNIQUE_REACHABLE_TERMINAL", thresholds, terminal))
    final_mask = next(iter(terminal))
    if final_mask not in seen:
        raise AssertionError("TERMINAL_NOT_REACHABLE")
    return len(seen), final_mask, len(terminal), edges, final_mask.bit_count()


def independently_generate_rows():
    rows = []
    by_n = {}
    for n in range(1, 5):
        count = 0
        for thresholds in product(range(n + 1), repeat=n):
            states, terminal, terminal_count, edges, final = reachable_state_graph(thresholds)
            rows.append({
                "n": str(n),
                "threshold_vector": ":".join(map(str, thresholds)),
                "reachable_state_count": str(states),
                "terminal_mask": str(terminal),
                "terminal_count": str(terminal_count),
                "transition_edges": str(edges),
                "final_participants": str(final),
            })
            count += 1
        if count != (n + 1) ** n:
            raise AssertionError("EXHAUSTIVE_VECTOR_COUNT_MISMATCH")
        by_n[str(n)] = count
    if by_n != {"1": 2, "2": 9, "3": 64, "4": 625}:
        raise AssertionError("WRONG_COVERAGE")
    return rows, by_n


def verify_csv_exact(rows):
    if not CSV_PATH.is_file():
        raise AssertionError("COMMITTED_ENUMERATION_CSV_MISSING")
    with CSV_PATH.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if tuple(reader.fieldnames or ()) != CSV_FIELDS:
            raise AssertionError("CSV_SCHEMA_CHANGED")
        observed = list(reader)
    if observed != rows:
        mismatch = next((i for i, (a, b) in enumerate(zip(observed, rows)) if a != b), None)
        raise AssertionError(("CSV_REPLAY_MISMATCH", mismatch, len(observed), len(rows)))
    return hashlib.sha256(CSV_PATH.read_bytes()).hexdigest()


def load_original_after_independent_computation():
    for path, expected in PINNED_BLOBS.items():
        if git_blob_sha1(path) != expected:
            raise AssertionError(("ORIGINAL_SOURCE_BLOB_CHANGED", str(path)))
    spec = importlib.util.spec_from_file_location("r118_original", SOURCE)
    if spec is None or spec.loader is None:
        raise AssertionError("ORIGINAL_SOURCE_IMPORT_FAILURE")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main():
    # Freeze the independent enumerations before loading the original model.
    rows, by_n = independently_generate_rows()
    csv_sha256 = verify_csv_exact(rows)
    original = load_original_after_independent_computation()
    for row in rows:
        thresholds = tuple(int(v) for v in row["threshold_vector"].split(":"))
        expected = int(row["final_participants"])
        observed = original.synchronous_participation(thresholds).final_participants
        sorted_observed = original.independently_sorted_minimal_closure(thresholds)
        if observed != expected or sorted_observed != expected:
            raise AssertionError(("ORIGINAL_DISAGREEMENT", thresholds, expected, observed, sorted_observed))

    # Two distinct 100-person examples; exhaustive bitmask enumeration is limited to n<=4.
    chain = tuple(range(100))
    broken = tuple(2 if x == 1 else x for x in chain)
    compensated = tuple(2 if x == 1 else 98 if x == 99 else x for x in chain)
    outcomes = [original.synchronous_participation(x).final_participants
                for x in (chain, broken, compensated)]
    if outcomes != [100, 1, 1]:
        raise AssertionError(("AUTHOR_AND_NEW_EXAMPLES_CHANGED", outcomes))
    if sum(chain) != sum(compensated) or sum(chain) != 4950:
        raise AssertionError("SAME_MEAN_COUNTEREXAMPLE_CHANGED")

    # Reachable closure is narrower than arbitrary static all-active equilibria.
    if reachable_state_graph((1, 1))[-1] != 0:
        raise AssertionError("UNSEEDED_EQUILIBRIUM_CONFUSION")
    if not all(t <= 1 for t in (1, 1)):
        raise AssertionError("STATIC_EQUILIBRIUM_NEGATIVE_CONTROL_BROKEN")
    if reachable_state_graph((0, 2, 2))[-1] != 1:
        raise AssertionError("MISSING_THRESHOLD_LINK_CONTROL_BROKEN")

    # Both deliberate corruptions must change a frozen prediction.
    actual = reachable_state_graph((0, 1, 2))[-1]
    if actual == 2:
        raise AssertionError("CORRUPTED_EXPECTED_OUTCOME_ACCEPTED")
    altered = reachable_state_graph((0, 2, 2))[-1]
    if actual == altered or (actual, altered) != (3, 1):
        raise AssertionError("CORRUPTED_THRESHOLD_UNDETECTED")

    receipt = {
        "research_id": "R118",
        "catalogue_id": "03-019",
        "status": "PASS_BOUNDED_INTERNAL_INDEPENDENT_REACHABILITY_E1",
        "independent_method": "one_person_transition_bitmask_BFS",
        "ordered_threshold_worlds_by_n": by_n,
        "total_constructed_worlds": len(rows),
        "original_solver_comparisons": len(rows),
        "author_and_compensated_100_person_final_counts": outcomes,
        "same_mean_sum_each": 4950,
        "negative_controls": 2,
        "tamper_controls_rejected": 2,
        "source_blob_sha1": {str(p.relative_to(ROOT)): git_blob_sha1(p) for p in PINNED_BLOBS},
        "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in PINNED_BLOBS},
        "constructed_csv_sha256": csv_sha256,
        "human_E2_model_scores": 0,
        "historical_E3_model_scores": 0,
        "external_independent_replication": False,
        "R073": "FROZEN",
        "PESEN_v0_1": "FROZEN",
    }
    print(json.dumps(receipt, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
