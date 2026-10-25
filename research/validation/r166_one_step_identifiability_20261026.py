"""R166 frozen third-method exact single-generation count identifiability, E1 only.
Uses Python standard library; no original-author EMG model or human data.
Run from repository root:
python research/validation/r166_one_step_identifiability_20261026.py > /tmp/r166_third_method.json
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
ORIGINAL = ROOT / "R166" / "R166_EXACT_RESULTS.json"
N_GRID = (4, 8)
REGIMES = ("neutral", "toward_A", "toward_B")
MECHANISMS = ("selection", "transformation")


def success_probability(n, k, regime, mechanism):
    p = F(k, n)
    if regime == "neutral":
        return p
    if regime == "toward_A":
        return F(2) * p / (1 + p) if mechanism == "selection" else (1 + 2 * p) / 3
    if regime == "toward_B":
        return p / (2 - p) if mechanism == "selection" else 2 * p / 3
    raise ValueError("unknown regime")


def binomial_count_distribution(n, q):
    row = tuple(F(comb(n, j)) * q**j * (1 - q)**(n - j) for j in range(n + 1))
    assert sum(row) == 1 and all(x >= 0 for x in row)
    return row


def tv_distance(a, b):
    assert len(a) == len(b) and sum(a) == sum(b) == 1
    return sum((abs(x - y) for x, y in zip(a, b)), F(0)) / 2


def main():
    original = json.loads(ORIGINAL.read_text(encoding="utf-8"))
    old = {(x["N"], x["regime"], x["mechanism"]): x["rows"] for x in original["kernels"]}
    assert len(old) == 12
    kernel_rows_verified = 0
    for n in N_GRID:
        for regime in REGIMES:
            for mechanism in MECHANISMS:
                expected = [[str(x) for x in binomial_count_distribution(
                    n, success_probability(n, k, regime, mechanism))]
                    for k in range(n + 1)]
                assert old[(n, regime, mechanism)] == expected
                kernel_rows_verified += n + 1
    assert kernel_rows_verified == 84

    records = []
    neutral_equal = 0
    for n in N_GRID:
        for regime in REGIMES:
            for k in range(n + 1):
                a = binomial_count_distribution(n, success_probability(n, k, regime, "selection"))
                b = binomial_count_distribution(n, success_probability(n, k, regime, "transformation"))
                tv = tv_distance(a, b)
                if regime == "neutral":
                    assert tv == 0
                    neutral_equal += 1
                    continue
                records.append({
                    "N": n, "k": k, "p": str(F(k, n)), "regime": regime,
                    "q_selection": str(success_probability(n, k, regime, "selection")),
                    "q_transformation": str(success_probability(n, k, regime, "transformation")),
                    "TV": str(tv), "equal_prior_Bayes_error": str((1 - tv) / 2),
                    "distribution_equal": a == b
                })
    assert len(records) == 56 and neutral_equal == 14
    equal = sum(x["distribution_equal"] for x in records)
    assert equal == 8
    assert sum(not x["distribution_equal"] for x in records) == 48

    # Prespecified mutation: B->A conversion 1/4 rather than 1/3.
    p = F(1, 2)
    mutant_q = p + (1 - p) * F(1, 4)
    mutant_tv = tv_distance(
        binomial_count_distribution(4, F(2, 3)),
        binomial_count_distribution(4, mutant_q))
    assert mutant_q == F(5, 8) and mutant_tv > 0

    # Exact symbolic discriminability equalities for the frozen nonneutral rules:
    # toward_A q_sel-q_trf = (1-p)(2p-1)/(3(1+p))
    # toward_B q_sel-q_trf = p(2p-1)/(3(2-p))
    for n in N_GRID:
        for k in range(n + 1):
            p = F(k, n)
            assert success_probability(n,k,"toward_A","selection") - success_probability(n,k,"toward_A","transformation") == (1-p)*(2*p-1)/(3*(1+p))
            assert success_probability(n,k,"toward_B","selection") - success_probability(n,k,"toward_B","transformation") == p*(2*p-1)/(3*(2-p))

    return {
        "research_id": "R166", "date": "2026-10-26", "evidence": "E1_SYNTHETIC_ONLY",
        "source": "research/R166/R166_EXACT_RESULTS.json",
        "prescore_protocol": "protocols/R166_ONE_STEP_COUNT_IDENTIFIABILITY_THIRD_METHOD_FREEZE_2026-10-26.md",
        "kernel_count": len(old), "kernel_rows_exact_verified": kernel_rows_verified,
        "nonneutral_conditions": len(records), "neutral_conditions": neutral_equal,
        "equal_nonneutral": equal, "different_nonneutral": len(records)-equal,
        "mutation_control": {"mutant_q": str(mutant_q), "TV": str(mutant_tv), "detected": mutant_tv > 0},
        "by_group": [{
            "N": n, "regime": regime,
            "min_TV": str(min(F(x["TV"]) for x in records if x["N"] == n and x["regime"] == regime)),
            "max_TV": str(max(F(x["TV"]) for x in records if x["N"] == n and x["regime"] == regime))
        } for n in N_GRID for regime in REGIMES[1:]],
        "records": records,
        "author_EMG_reproduced": False, "E2_new": 0, "E3_new": 0,
        "external_independent_replication": False
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False, sort_keys=True))
