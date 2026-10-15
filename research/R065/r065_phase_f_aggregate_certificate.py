#!/usr/bin/env python3
"""R065 Phase F: reproducibility certificate for Phase E summary statistics.

Given only (n eligible persons, k day-89 copy events), deterministically derive
cross-person leave-one-out scoring and exact conditional paired-bootstrap
quantiles. No participant records, third-party packages or network required.
This cannot verify that the original source actually contained (n, k).
"""
import argparse
import json
import math


def certificate(n: int = 226, k: int = 73, pseudo: float = 4.0) -> dict:
    if type(n) is not int or type(k) is not int or n < 2 or not 0 <= k <= n:
        raise ValueError("require integer n>=2 and 0<=k<=n")
    if not math.isfinite(pseudo) or pseudo <= 0:
        raise ValueError("require positive finite Beta symmetric pseudocount")
    # Exactly one held-out observation per person. Training uses n-1 others.
    p_if_1 = (k - 1 + pseudo) / (n - 1 + 2 * pseudo) if k else None
    p_if_0 = (k + pseudo) / (n - 1 + 2 * pseudo) if k < n else None
    gain_1 = math.log(2) + math.log(p_if_1) if k else None
    gain_0 = math.log(2) + math.log1p(-p_if_0) if k < n else None
    brier_gain_1 = 0.25 - (1-p_if_1)**2 if k else None
    brier_gain_0 = 0.25 - p_if_0**2 if k < n else None

    def mixture(one, zero, successes):
        return (successes * (one if one is not None else 0.0)
                + (n-successes) * (zero if zero is not None else 0.0)) / n

    log_gain = mixture(gain_1, gain_0, k)
    brier_gain = mixture(brier_gain_1, brier_gain_0, k)

    # Conditional bootstrap: resample from observed n binary labels.
    # Number of copies in each n-person resample ~ Binomial(n, k/n).
    # Stable recurrence starting from its binomial modal mass, normalized.
    p = k / n
    if p == 0:
        masses = [1.0] + [0.0]*n
    elif p == 1:
        masses = [0.0]*n + [1.0]
    else:
        m = min(n, int((n+1)*p))
        masses = [0.0] * (n+1)
        masses[m] = 1.0
        for j in range(m-1, -1, -1):
            masses[j] = masses[j+1] * (j+1)/(n-j) * (1-p)/p
        for j in range(m+1, n+1):
            masses[j] = masses[j-1] * (n-j+1)/j * p/(1-p)
        norm = sum(masses)
        masses = [v/norm for v in masses]
    cdf = []
    cumulative = 0.0
    for mass in masses:
        cumulative += mass
        cdf.append(cumulative)

    def resample_quantile(q, one, zero):
        # For negative monotonicity: score grows as #successful copy falls.
        if one is None:
            one = zero
        if zero is None:
            zero = one
        indices = list(range(n+1))
        if one < zero:
            indices.reverse()
        running = 0.0
        for j in indices:
            running += masses[j]
            if running + 1e-14 >= q:
                return mixture(one, zero, j)
        return mixture(one, zero, indices[-1])

    return {
        "kind": "RETROSPECTIVE_AGGREGATE_SUFFICIENT_STATISTIC_AUDIT",
        "n": n, "copied": k, "pseudo_each_beta_side": pseudo,
        "probability_training_loo_when_copy": p_if_1,
        "probability_training_loo_when_not_copy": p_if_0,
        "uniform_logloss": math.log(2), "uniform_brier": 0.25,
        "loo_logloss": math.log(2)-log_gain,
        "loo_brier": 0.25-brier_gain,
        "uniform_minus_loo_mean_logloss": log_gain,
        "uniform_minus_loo_mean_brier": brier_gain,
        "conditional_exact_bootstrap_percentile_95": {
            "logloss": [resample_quantile(.025, gain_1, gain_0),
                        resample_quantile(.975, gain_1, gain_0)],
            "brier": [resample_quantile(.025, brier_gain_1, brier_gain_0),
                      resample_quantile(.975, brier_gain_1, brier_gain_0)]
        },
        "scope": "Conditional bootstrap of fixed per-person losses; source count and raw-file identity not verified."
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n", type=int, default=226)
    parser.add_argument("--copied", type=int, default=73)
    parser.add_argument("--pseudo", type=float, default=4.0)
    parser.add_argument("--output", type=str)
    args = parser.parse_args()
    result = certificate(args.n, args.copied, args.pseudo)
    contents = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        from pathlib import Path
        Path(args.output).write_text(contents, encoding="utf-8")
    print(contents, end="")


if __name__ == "__main__":
    main()
