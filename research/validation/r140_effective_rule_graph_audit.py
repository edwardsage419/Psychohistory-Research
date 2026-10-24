#!/usr/bin/env python3
"""Independent bounded R140 IAD game audit, Python standard library only.

All players and payoff numbers are artificial. The original R140 ZIP is not imported.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from collections import Counter
from pathlib import Path

AXES = (
    ("boundary", (2, 3)),
    ("position", ("all", "steward")),
    ("cap", (1, 2)),
    ("aggregation", ("independent", "quota4")),
    ("information", ("private", "public")),
    ("fee", (0, 2)),
    ("scope", (4, 6)),
)


def profiles(c):
    eligible = [i < c["boundary"] and not (i == 2 and c["position"] == "steward") for i in range(3)]
    choices = [range(c["cap"] + 1) if eligible[i] else (0,) for i in range(3)]
    return [p for p in itertools.product(*choices)
            if sum(p) <= c["scope"] and (c["aggregation"] == "independent" or sum(p) <= 4)]


def outcome(c, p):
    total = sum(p)
    fee_active = c["boundary"] == 3 and c["position"] == "steward" and c["information"] == "public" and c["fee"] == 2
    fines = tuple(2 * max(0, v - 1) if fee_active else 0 for v in p)
    utility = tuple(v * (8 - total) - fines[i] for i, v in enumerate(p))
    return utility, fines, total * (8 - total)


def audit(c, omit_first_edge=False):
    possible = profiles(c)
    pset = set(possible)
    rows = []
    deviations = 0
    edges = []
    ne = []
    best_g = max(outcome(c, p)[2] for p in possible)
    for p in possible:
        utility, fines, g = outcome(c, p)
        positive_regrets = []
        for i in range(3):
            for alternative in range(c["cap"] + 1):
                if alternative == p[i]:
                    continue
                q = p[:i] + (alternative,) + p[i+1:]
                if q not in pset:
                    continue
                alt_utility = outcome(c, q)[0][i]
                regret = alt_utility - utility[i]
                if omit_first_edge and not edges:
                    omit_first_edge = False
                    continue
                deviations += 1
                edges.append([list(p), i, list(q), regret])
                positive_regrets.append(regret)
        is_ne = not positive_regrets or max(positive_regrets) <= 0
        if is_ne:
            ne.append(p)
        rows.append([list(p), list(utility), int(is_ne)])
    canonical = json.dumps(rows, ensure_ascii=True, separators=(",", ":"))
    return {
        "configuration": c,
        "profiles": len(possible),
        "deviations": deviations,
        "edge_certificate_sha256": hashlib.sha256(json.dumps(edges, separators=(",", ":")).encode()).hexdigest(),
        "pure_ne": [list(p) for p in ne],
        "resource_optimum": best_g,
        "has_resource_optimal_ne": any(outcome(c, p)[2] == best_g for p in ne),
        "canonical_game_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "game_rows": rows,
    }


def check_controls(records):
    lookup = {tuple(x["configuration"][k] for k, _ in AXES): x for x in records}
    base = dict(boundary=3, position="all", cap=2, aggregation="independent", information="private", fee=0, scope=6)
    b = lookup[tuple(base[k] for k, _ in AXES)]
    assert b["pure_ne"] == [[2, 2, 2]] and b["resource_optimum"] == 16
    assert outcome(base, (2, 2, 2))[2] == 12
    q = dict(base, aggregation="quota4")
    s = dict(base, scope=4)
    assert lookup[tuple(q[k] for k, _ in AXES)]["canonical_game_sha256"] == lookup[tuple(s[k] for k, _ in AXES)]["canonical_game_sha256"]
    enforced = dict(boundary=3, position="steward", cap=2, aggregation="independent", information="public", fee=2, scope=6)
    unenforced = dict(enforced, fee=0)
    assert outcome(enforced, (2, 2, 0))[0] != outcome(unenforced, (2, 2, 0))[0]
    absent = dict(boundary=2, position="all", cap=2, aggregation="independent", information="public", fee=2, scope=6)
    assert outcome(absent, (2, 2, 0))[0] != (6, 6, 0)  # false positive penalty must be rejected
    assert outcome(absent, (2, 2, 0))[0] == (8, 8, 0)
    baseline = audit(base)
    deleted = audit(base, omit_first_edge=True)
    assert baseline["deviations"] == deleted["deviations"] + 1
    assert baseline["edge_certificate_sha256"] != deleted["edge_certificate_sha256"]
    return {"baseline_ne": True, "quota_scope_equivalence": True, "fee_disabled_detected": True,
            "false_fee_detected": True, "deleted_edge_count_detected": True}


def main():
    records = [audit(dict(zip((k for k, _ in AXES), values)))
               for values in itertools.product(*(values for _, values in AXES))]
    counts = Counter(x["canonical_game_sha256"] for x in records)
    summary = {
        "configurations": len(records),
        "feasible_profiles": sum(x["profiles"] for x in records),
        "unilateral_deviations": sum(x["deviations"] for x in records),
        "strict_signatures": len(counts),
        "strict_equivalent_unordered_pairs": sum(n * (n - 1) // 2 for n in counts.values()),
        "resource_optimal_ne_configs": sum(x["has_resource_optimal_ne"] for x in records),
        "signature_class_sizes": sorted(counts.values()),
        "negative_and_positive_controls": check_controls(records),
        "evidence": "E1_project_constructed_only",
    }
    expected = (128, 1136, 4584, 6, 2272, 124)
    actual = tuple(summary[k] for k in (
        "configurations", "feasible_profiles", "unilateral_deviations", "strict_signatures",
        "strict_equivalent_unordered_pairs", "resource_optimal_ne_configs"))
    if actual != expected:
        raise AssertionError(f"Frozen R140 count mismatch: {actual} != {expected}")
    payload = {"summary": summary, "records": records}
    path = Path(__file__).with_name("R140_EFFECTIVE_RULE_GRAPH_128_EXACT_RESULTS_2026-10-25.json")
    path.write_text(json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n")
    print(json.dumps(summary, sort_keys=True, ensure_ascii=True, indent=2))
    print("RESULT_JSON_SHA256", hashlib.sha256(path.read_bytes()).hexdigest())


if __name__ == "__main__":
    main()
