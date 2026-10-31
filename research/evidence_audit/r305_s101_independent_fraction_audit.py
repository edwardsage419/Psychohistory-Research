#!/usr/bin/env python3
"""Nonblind internal R305 S101 audit. Independent Fraction six-pair enumeration."""
from __future__ import annotations
import copy
import csv
import hashlib
import io
import itertools
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

LEVELS = (Q(0), Q(1, 2), Q(1))
THRESHOLDS = (Q(0), Q(1), Q(2))
LABELS = {"P": (0, 0, 1, 1), "Q": (0, 1, 0, 1)}
FIELDS = ("lambda", "features", "readiness", "norm_P", "norm_Q", "personal_threshold", "MC_P", "MC_Q", "score_P", "score_Q", "choice")


def metacontrast(k: int, category: str) -> Q:
    x = (Q(0), Q(1) + 3 * Q(k, 4), Q(4) - 3 * Q(k, 4), Q(5))
    labels = LABELS[category]
    inside, outside = [], []
    for i, j in itertools.combinations(range(4), 2):
        (inside if labels[i] == labels[j] else outside).append(abs(x[i] - x[j]))
    assert len(inside) == 2 and len(outside) == 4 and sum(inside) > 0
    return (sum(outside) / len(outside)) / (sum(inside) / len(inside))


def independent_expected():
    rows = []
    paths = []
    counts = {str(Q(k, 4)): {"P": 0, "Q": 0, "PERSONAL": 0} for k in range(5)}
    hist = {str(k): 0 for k in range(5)}
    for r, np, nq, t in itertools.product(LEVELS, LEVELS, LEVELS, THRESHOLDS):
        choices = []
        for k in range(5):
            mcp, mcq = metacontrast(k, "P"), metacontrast(k, "Q")
            sp, sq = r * np * mcp, r * nq * mcq
            choice = "P" if sp > max(sq, t) else ("Q" if sq > max(sp, t) else "PERSONAL")
            values = (Q(0), Q(1) + 3 * Q(k, 4), Q(4) - 3 * Q(k, 4), Q(5))
            row = (str(Q(k, 4)), ";".join(map(str, values)), str(r), str(np), str(nq), str(t), str(mcp), str(mcq), str(sp), str(sq), choice)
            rows.append(dict(zip(FIELDS, row)))
            counts[str(Q(k, 4))][choice] += 1
            choices.append(choice)
            if r == 0 or np == nq == 0:
                assert choice == "PERSONAL"
        switches = sum(a != b for a, b in zip(choices, choices[1:]))
        hist[str(switches)] += 1
        paths.append({"readiness": str(r), "norm_P": str(np), "norm_Q": str(nq), "personal_threshold": int(t), "path": choices, "adjacent_changes": switches})
    summary = {
        "research_id": "R305", "stage": "S101", "grade": "E1_SYNTHETIC_ONLY",
        "original_frozen_model_unchanged": True, "worlds": 405, "candidate_source_cells": 810,
        "configurations": 81, "adjacent_comparisons": 324,
        "metacontrast": [{"lambda": str(Q(k, 4)), "P": str(metacontrast(k, "P")), "Q": str(metacontrast(k, "Q"))} for k in range(5)],
        "choice_counts": {key: counts[key] for key in ("0", "1", "1/4", "1/2", "3/4")},
        "trajectory_change_histogram": hist,
        "total_adjacent_changes": sum(p["adjacent_changes"] for p in paths),
        "first_change_witness": next((p for p in paths if p["adjacent_changes"]), None),
        "all_trajectories": paths, "original_R305_endpoint_midpoint_parity": "CHECKED_EXTERNALLY",
        "human_E2": 0, "historical_E3": 0, "R073": "FROZEN", "PESEN_v0_1": "FROZEN",
        "scientific_acceptance": "PARTIAL"
    }
    assert len(rows) == 405 and len(paths) == 81
    return rows, summary


def audit(rows, summary):
    expected, expected_summary = independent_expected()
    assert len(rows) == 405, "complete world count"
    assert len({tuple(r[k] for k in FIELDS[:6]) for r in rows}) == 405, "unique world identity"
    for i, (actual, exp) in enumerate(zip(rows, expected)):
        assert actual == exp, f"row {i} mismatch"
    assert summary == expected_summary, "summary and trajectory mismatch"
    return True


def serialize(rows, summary):
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=FIELDS, lineterminator="\n", quoting=csv.QUOTE_ALL)
    buffer.write(",".join(FIELDS) + "\n")
    for row in rows:
        writer.writerow(row)
    return buffer.getvalue().encode(), (json.dumps(summary, indent=2, ensure_ascii=False) + "\n").encode()


def gitblob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def selftest():
    rows, summary = independent_expected()
    assert audit(rows, summary)
    mutations = []
    def mutate_row(index, key, value):
        a, b = copy.deepcopy(rows), copy.deepcopy(summary)
        a[index][key] = value
        return a, b
    mutations.append((rows[:-1], summary))
    mutations.append(([rows[0]] + rows[:-1], summary))
    mutations.append(mutate_row(0, "lambda", "1/3"))
    mutations.append(mutate_row(0, "features", "0;0;0;0"))
    mutations.append(mutate_row(0, "MC_P", "999"))
    mutations.append(mutate_row(0, "score_P", "999"))
    mutations.append(mutate_row(0, "choice", "Q"))
    a, b = copy.deepcopy(rows), copy.deepcopy(summary)
    b["total_adjacent_changes"] += 1
    mutations.append((a, b))
    a, b = copy.deepcopy(rows), copy.deepcopy(summary)
    b["grade"] = "E2_REAL_HUMAN"
    mutations.append((a, b))
    rejected = 0
    for a, b in mutations:
        try:
            audit(a, b)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError("mutation escaped")
    return rejected


if __name__ == "__main__":
    rows, summary = independent_expected()
    csv_bytes, json_bytes = serialize(rows, summary)
    print(json.dumps({"audit": audit(rows, summary), "mutations_rejected": selftest(),
                      "worlds": len(rows), "changes": summary["total_adjacent_changes"],
                      "hist": summary["trajectory_change_histogram"],
                      "csv_bytes": len(csv_bytes), "csv_blob": gitblob(csv_bytes),
                      "json_bytes": len(json_bytes), "json_blob": gitblob(json_bytes)}))
    if "--emit" in sys.argv:
        dest = Path(sys.argv[sys.argv.index("--emit") + 1])
        dest.mkdir(parents=True, exist_ok=True)
        (dest / "R305_S101_ALL_405_CONTEXT_WORLDS.csv").write_bytes(csv_bytes)
        (dest / "R305_S101_EXACT_RESULTS.json").write_bytes(json_bytes)
    if "--check" in sys.argv:
        index = sys.argv.index("--check")
        with open(sys.argv[index + 1], newline="") as f:
            actual = list(csv.DictReader(f))
        actual_summary = json.loads(Path(sys.argv[index + 2]).read_text())
        assert audit(actual, actual_summary)
