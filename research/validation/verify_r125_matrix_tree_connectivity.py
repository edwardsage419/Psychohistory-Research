#!/usr/bin/env python3
"""R125 frozen third-method matrix-tree exact audit; constructed E1 only."""
from __future__ import annotations
import argparse
import csv
import hashlib
import io
import itertools
import json
import sys
from collections import defaultdict
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORIGINAL = ROOT / "research/R125/r125_erdos_renyi_gnm_gilbert_gnp_exact.py"
TEST = ROOT / "research/R125/test_r125_erdos_renyi_gnm_gilbert_gnp_exact.py"
REPORT = ROOT / "research/R125/R125_ERDOS_RENYI_GNM_GILBERT_GNP_FIRSTPARTY_FINITE_EXACT_SCIENTIFIC_REPORT_2026-10-20.md"
PINNED = {
    ORIGINAL: "01bf0a45879dc156ad1dcfcaa23624dc44f86ae5",
    TEST: "34276d7f9719967712ecd2525c1ab378e05f9440",
    REPORT: "6f2f28dd62b7a01e784603f0edae90e7196fbb16",
}
HEADER = ("n", "edge_mask", "edge_count", "spanning_tree_count",
          "matrix_tree_connected", "original_dfs_connected")

def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()

def verify_pins(pins=PINNED):
    for path, expected in pins.items():
        actual = git_blob_sha(path.read_bytes())
        if actual != expected:
            raise AssertionError(f"ORIGINAL_SOURCE_IDENTITY_MISMATCH {path.name} {actual}")

def edges_from_mask(n: int, mask: int):
    pairs = list(itertools.combinations(range(n), 2))
    return [e for bit, e in enumerate(pairs) if (mask >> bit) & 1]

def leibniz_det(matrix):
    size = len(matrix)
    if size == 0:
        return 1
    total = 0
    for perm in itertools.permutations(range(size)):
        inversions = sum(perm[i] > perm[j] for i in range(size)
                         for j in range(i + 1, size))
        prod = 1
        for i, j in enumerate(perm):
            prod *= matrix[i][j]
        total += (-1 if inversions % 2 else 1) * prod
    return total

def spanning_trees(n: int, edges):
    laplacian = [[0] * n for _ in range(n)]
    for a, b in edges:
        laplacian[a][a] += 1
        laplacian[b][b] += 1
        laplacian[a][b] -= 1
        laplacian[b][a] -= 1
    return leibniz_det([row[:-1] for row in laplacian[:-1]])

def original_module():
    sys.path.insert(0, str(ORIGINAL.parent))
    import r125_erdos_renyi_gnm_gilbert_gnp_exact as original
    return original

def generate_rows(original):
    for n in range(1, 6):
        for mask in range(1 << (n * (n - 1) // 2)):
            edges = edges_from_mask(n, mask)
            trees = spanning_trees(n, edges)
            assert trees >= 0
            independent = int(trees > 0)
            original_connected = int(original.graph_properties(n, tuple(edges))["connected"])
            assert independent == original_connected, (n, mask, trees)
            yield (n, mask, len(edges), trees, independent, original_connected)

def serialize(rows):
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(rows)
    return buffer.getvalue().encode("utf-8")

def audit(rows, original):
    assert len(rows) == 1099
    assert {n: sum(row[0] == n for row in rows) for n in range(1, 6)} == {
        1: 1, 2: 2, 3: 8, 4: 64, 5: 1024}
    look = {(r[0], r[1]): r[3] for r in rows}
    controls = {(1, 0): 1, (2, 0): 0, (4, 41): 1,
                (4, 45): 4, (4, 63): 16, (4, 33): 0}
    for key, value in controls.items():
        assert look[key] == value, (key, look[key], value)
    buckets = defaultdict(lambda: [0, 0])
    for n, mask, m, trees, connected, dfs in rows:
        bucket = buckets[(n, m)]
        bucket[0] += 1
        bucket[1] += connected
    assert len(buckets) == 25
    assert buckets[(4, 3)] == [20, 16]
    assert sum(r[4] for r in rows if r[0] == 4) == 38
    for n in range(1, 6):
        K = n * (n - 1) // 2
        for p in (Fraction(0), Fraction(1, 3), Fraction(1, 2), Fraction(1)):
            total = sum((p ** m) * ((1-p) ** (K-m)) * connected
                        for nn, mask, m, trees, connected, dfs in rows if nn == n)
            expected = original.independent_gilbert1959_connected_recurrence(n, p)
            assert total == expected, (n, p, total, expected)
            if p == 0:
                assert total == (1 if n == 1 else 0)
            if p == 1:
                assert total == 1
    return {
        "rows": len(rows), "fixed_m_buckets": len(buckets),
        "n4_m3_connected": buckets[(4, 3)][1],
        "n4_m3_total": buckets[(4, 3)][0],
        "n4_p_half_connected": 38,
        "n4_p_half_total": 64,
        "original_sources_git_blobs": {p.name: sha for p, sha in PINNED.items()},
        "real_human_E2": 0, "historical_E3": 0,
        "acceptance_ceiling": "PASS_BOUNDED_INTERNAL_MATRIX_TREE_CONNECTIVITY_E1"
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--verify", action="store_true")
    args = parser.parse_args()
    verify_pins()
    original = original_module()
    rows = list(generate_rows(original))
    payload = serialize(rows)
    receipt = audit(rows, original)
    if args.verify:
        assert args.output.read_bytes() == payload, "RAW_CSV_MUTATION_OR_ROW_MISMATCH"
        changed = bytearray(payload)
        changed[-2] = 49 if changed[-2] != 49 else 48
        assert bytes(changed) != payload
        assert bytes(changed) != args.output.read_bytes(), "TAMPER_NEGATIVE_CONTROL_FAILED"
        try:
            verify_pins({ORIGINAL: "0" * 40})
        except AssertionError:
            pass
        else:
            raise AssertionError("WRONG_SOURCE_SHA_NEGATIVE_CONTROL_FAILED")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_bytes(payload)
    receipt["raw_csv_sha256"] = hashlib.sha256(payload).hexdigest()
    print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=2))

if __name__ == "__main__":
    main()
