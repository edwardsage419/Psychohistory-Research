#!/usr/bin/env python3
"""R132 independent exhaustive exact 2x2 replicator phase portrait audit.

Taylor & Jonker (1978) continuous Eq2 only. E1 artificial integer payoff grid.
Requires only Python standard library. When run in the repository, verifies
and executes the frozen original R132 Python source independently.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
from collections import Counter
from fractions import Fraction as F
from itertools import product
from pathlib import Path

ORIGINAL_REL = "research/R132/r132_replicator_1978_exact_invariants_and_trajectories.py"
ORIGINAL_BLOB = "850c01c0a4be95f7884d29e1b9d5ebe15de5f5b8"
X_GRID = (F(0), F(1, 10), F(1, 4), F(1, 2), F(3, 4), F(9, 10), F(1))
PAYOFFS = (-2, -1, 0, 1, 2)


def classify(beta: int, gamma: int) -> str:
    if beta == gamma == 0:
        return "neutral_continuum"
    if beta >= 0 and gamma >= 0:
        return "A_monotone"
    if beta <= 0 and gamma <= 0:
        return "B_monotone"
    if beta < 0 < gamma:
        return "bistable_threshold"
    if gamma < 0 < beta:
        return "stable_coexistence"
    raise AssertionError("phase portrait partition incomplete")


def bernstein_field(beta: int, gamma: int, x: F) -> F:
    return x * (1 - x) * ((1 - x) * beta + x * gamma)


def independent_direct_field(a: int, b: int, c: int, d: int, x: F) -> F:
    fa = a * x + b * (1 - x)
    fb = c * x + d * (1 - x)
    mean = x * fa + (1 - x) * fb
    return x * (fa - mean)


def original_module(repo_root: Path):
    path = repo_root / ORIGINAL_REL
    if not path.is_file():
        return None
    raw = path.read_bytes()
    actual = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if actual != ORIGINAL_BLOB:
        raise AssertionError(f"original R132 source blob changed: {actual}")
    spec = importlib.util.spec_from_file_location("r132_frozen_original", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def audit(repo_root: Path, csv_path: Path | None = None) -> dict:
    original = original_module(repo_root)
    counts = Counter()
    records = []
    original_checks = 0
    fixed_checks = 0
    for a, b, c, d in product(PAYOFFS, repeat=4):
        beta, gamma = b - d, a - c
        category = classify(beta, gamma)
        counts[category] += 1
        xstar = F(-beta, gamma - beta) if category in ("bistable_threshold", "stable_coexistence") else None
        for x in X_GRID:
            value = bernstein_field(beta, gamma, x)
            direct = independent_direct_field(a, b, c, d, x)
            assert value == direct, (a, b, c, d, x, value, direct)
            if original is not None:
                A = ((F(a), F(b)), (F(c), F(d)))
                source = original.source_original_eq2_exact_field(A, (x, 1 - x))
                assert source == (value, -value), (a, b, c, d, x, source, value)
                original_checks += 1
            fixed_checks += 1
        if xstar is not None:
            assert F(0) < xstar < F(1)
            assert bernstein_field(beta, gamma, xstar) == 0
            left = bernstein_field(beta, gamma, xstar / 2)
            right = bernstein_field(beta, gamma, (xstar + 1) / 2)
            if category == "stable_coexistence":
                assert left > 0 and right < 0
            else:
                assert left < 0 and right > 0
        else:
            for x in (F(1, 1000), F(1, 3), F(999, 1000)):
                f = bernstein_field(beta, gamma, x)
                if category == "A_monotone":
                    assert f > 0
                elif category == "B_monotone":
                    assert f < 0
                else:
                    assert f == 0
        records.append((a, b, c, d, beta, gamma, category, str(xstar) if xstar is not None else ""))
    assert fixed_checks == 4375 and len(records) == 625
    assert len(counts) == 5
    # Deliberately wrong competing models must fail at a fixed nondegenerate point.
    truth = bernstein_field(1, 1, F(1, 2))
    assert truth == F(1, 4)
    assert -truth != truth  # inverted selection direction
    assert F(0) != truth  # using own fitness instead of population mean
    if csv_path is not None:
        csv_path.parent.mkdir(parents=True, exist_ok=True)
        with csv_path.open("w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(("a", "b", "c", "d", "beta", "gamma", "phase_class", "interior_fixed_point"))
            w.writerows(records)
    return {
        "matrix_cases": len(records),
        "exact_field_comparisons": fixed_checks,
        "original_unchanged_source_executed": original is not None,
        "original_source_exact_matches": original_checks,
        "class_counts": dict(sorted(counts.items())),
        "negative_controls_rejected": 2,
        "evidence": "E1 synthetic exact mathematics only",
        "new_E2": 0,
        "new_E3": 0,
    }


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    result = audit(root, Path(__file__).with_name("R132_EXHAUSTIVE_625_TWO_STRATEGY_PHASE_PORTRAITS_2026-10-25.csv"))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
