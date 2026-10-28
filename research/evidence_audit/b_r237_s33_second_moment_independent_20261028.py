#!/usr/bin/env python3
"""Independent R237 S33 E1 risk audit, Python standard library only.

Usage: python3 research/evidence_audit/b_r237_s33_second_moment_independent_20261028.py
Input: frozen R237 exact observable joint and S33 machine receipt.
Uses conditional second moments, never calls the R-track enumerator.
"""
import json
from fractions import Fraction as F
from pathlib import Path

SOURCE = Path("research/R237/R237_EXACT_RESULTS.json")
RECEIPT = Path("research/validation/R237_S33_PREFIX_BRIER_EXACT_RECEIPT_2026-10-28.json")


def audit(source, receipt):
    worlds = source["world_results"]
    expected = {w["world"]: w for w in receipt["worlds"]}
    assert len(worlds) == len(expected) == 9
    checked = 0
    for world in worlds:
        name = world["world"]
        joint = {k: F(v) for k, v in world["exact_observable_three_position_word_joint"].items()}
        assert len(joint) == 27 and sum(joint.values()) == 1
        by_prefix = {}
        unigram = [F(0), F(0), F(0)]
        for a in range(3):
            for b in range(3):
                prefix = str(a) + str(b)
                vals = [joint[prefix + str(k)] for k in range(3)]
                by_prefix[prefix] = vals
                for k in range(3):
                    unigram[k] += vals[k]
        # Bayes risk is 1 - E[sum_k P(Y=k|X)^2].
        # This is algebraically independent of the one-hot squared-error enumeration.
        conditional_second = F(0)
        regret_unigram = F(0)
        regret_uniform = F(0)
        for vals in by_prefix.values():
            mass = sum(vals)
            assert mass > 0
            q = [v / mass for v in vals]
            conditional_second += sum(v * v / mass for v in vals)
            regret_unigram += mass * sum((q[k] - unigram[k]) ** 2 for k in range(3))
            regret_uniform += mass * sum((v - F(1, 3)) ** 2 for v in q)
            checked += 5
        risk = {
            "ORACLE_PREFIX": 1 - conditional_second,
            "UNIGRAM": 1 - sum(v * v for v in unigram),
            "UNIFORM": F(2, 3),
        }
        regrets = {"UNIGRAM": regret_unigram, "UNIFORM": regret_uniform}
        assert risk["UNIGRAM"] - risk["ORACLE_PREFIX"] == regret_unigram
        assert risk["UNIFORM"] - risk["ORACLE_PREFIX"] == regret_uniform
        checked += 2
        for key, val in risk.items():
            assert str(val) == expected[name]["risks"][key], (name, key)
            checked += 1
        for key, val in regrets.items():
            assert str(val) == expected[name]["regrets"][key], (name, key)
            checked += 1
    # A deliberate corrupted receipt must be rejected by the same independent routine.
    bad = json.loads(json.dumps(receipt))
    bad["worlds"][0]["risks"]["ORACLE_PREFIX"] = "999"
    return checked, bad


def main():
    source = json.loads(SOURCE.read_text(encoding="utf8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf8"))
    checks, bad = audit(source, receipt)
    try:
        audit(source, bad)
    except AssertionError:
        mutation_detected = True
    else:
        raise AssertionError("corrupted oracle risk went undetected")
    print(json.dumps({"status": "PASS", "independent_exact_comparisons": checks,
                      "corrupted_receipt_detected": mutation_detected,
                      "scope": "INTERNAL_ALTERNATE_FORMULA_E1_ONLY",
                      "external_independent_replication": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
