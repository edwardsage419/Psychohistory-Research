#!/usr/bin/env python3
"""MKT083 exact synthetic feasibility checks for pinned pymoo tie constraints.
Standard library only. Optional source paths check Git blob identity and expressions.
No network calls, user data, or full pymoo execution.
"""
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

PIN_BLOB = "207726ffba920eca75f739b2d0cccaf0c23d92b8"
VF_BLOB = "f34c003203d01545ccfbf6b18a4b8f48fc25be3f"

def git_blob(text):
    data = text.encode("utf-8")
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()

def check_source(path, expected, phrases):
    source = Path(path).read_text(encoding="utf-8")
    assert git_blob(source) == expected, f"Unexpected source blob: {path}"
    for phrase in phrases:
        assert phrase in source, f"Missing expression: {phrase}"
    return len(phrases) + 1

def feasible(weights, epsilon, ranks):
    points = [(Q(0), Q(-2)), (Q(-1), Q(-1)), (Q(-2), Q(0))]
    values = [sum(a * b for a, b in zip(p, weights)) for p in points]
    delta = Q(1, 10)
    if sum(weights) != 1 or any(w < 0 or w > 1 for w in weights):
        return False
    for i in range(2):
        diff = values[i] - values[i + 1]
        g = abs(diff) - delta * epsilon if ranks[i] == ranks[i + 1] else -diff + epsilon
        if g > 0:
            return False
    return True

def main():
    checks = 0
    if len(sys.argv) == 3:
        checks += check_source(sys.argv[1], PIN_BLOB, [
            "if len(set(rank)) == 0:",
            "self.v2 = self.vf_res.vf(eta_F[dm_ranks[1] - 1] * -1).item()",
        ])
        checks += check_source(sys.argv[2], VF_BLOB, [
            "g[tie] = np.abs(diff[tie]) - delta * ep",
            "g = -diff + ep",
            "return -ep",
        ])
    elif len(sys.argv) != 1:
        raise SystemExit("Usage: python script.py [pinned_pinsga2.py pinned_value_functions.py]")
    tied = (1, 1, 1)
    strict = (1, 2, 3)
    high, zero, strict_high = 0, 0, 0
    for k in range(101):
        weights = (Q(k, 100), Q(100 - k, 100))
        high += feasible(weights, Q(1000), tied)
        zero += feasible(weights, Q(0), tied)
        strict_high += feasible(weights, Q(1000), strict)
        checks += 3
    assert high == 101 and zero == 1 and strict_high == 0
    checks += 3
    print(json.dumps({
        "status": "PASS", "checks": checks,
        "all_tie_epsilon_1000_feasible_weights": high,
        "all_tie_epsilon_0_feasible_weights": zero,
        "strict_ranking_epsilon_1000_feasible_weights": strict_high,
        "grid": "w0 = k/100, w1 = 1 - w0, k=0..100",
        "scope": "Exact synthetic constraint feasibility; no full optimizer run",
    }, indent=2))

if __name__ == "__main__":
    main()
