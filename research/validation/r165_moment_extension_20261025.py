"""R165 E1 extension: exact diversity recurrence and stationary autocovariance.

Run: python r165_moment_extension_20261025.py > R165_MOMENT_EXTENSION_RECEIPT_2026-10-25.json
Only Python standard library. This script uses the preregistered algebraic
moment method, independently of the archived finite transition kernels.
"""
from fractions import Fraction as F
import json

NS = (4, 6, 8)
STARTS = ((0, 1, 2, 4), (0, 1, 3, 6), (0, 1, 4, 8))
MUS = (F(0), F(1, 16), F(1, 8), F(1, 4))
LAGS = (1, 2, 4)


def diversity(n, k):
    p = F(k, n)
    return 2 * p * (1 - p)


def coefficients(n, mu):
    c = F(n - 1, n)
    return c * (1 - mu) ** 2, c * mu * (1 - mu / 2)


def closed_diversity(n, k, mu, t):
    a, b = coefficients(n, mu)
    h0 = diversity(n, k)
    return a ** t * h0 + b * (1 - a ** t) / (1 - a)


def stationary_diversity(n, mu):
    if mu <= 0:
        raise ValueError("positive innovation required for unique stationary law")
    a, b = coefficients(n, mu)
    return b / (1 - a)


def stationary_covariance(n, mu, lag):
    h = stationary_diversity(n, mu)
    return (1 - mu) ** lag * (1 - 2 * h) / 4


def main():
    worlds = []
    pairs = 0
    points = 0
    omission_c_applicable = omission_c_detected = 0
    linear_mu_applicable = linear_mu_detected = 0
    mu0_decay_checks = 0
    for ni, n in enumerate(NS):
        for ki, k in enumerate(STARTS[ni]):
            for mi, mu in enumerate(MUS):
                h = diversity(n, k)
                h0 = h
                a, b = coefficients(n, mu)
                history = []
                for t in range(5):
                    assert h == closed_diversity(n, k, mu, t)
                    assert F(0) <= h <= F(1, 2)
                    history.append(str(h))
                    points += 1
                    if mu == 0:
                        assert h == h0 * F(n - 1, n) ** t
                        mu0_decay_checks += 1
                    if t == 4:
                        continue
                    correct = a * h + b
                    c = F(n - 1, n)
                    wrong_no_c = (1 - mu) ** 2 * h + mu * (1 - mu / 2)
                    wrong_linear = c * (1 - mu) * h + b
                    if correct != wrong_no_c:
                        omission_c_applicable += 1
                        omission_c_detected += int(correct != wrong_no_c)
                    if correct != wrong_linear:
                        linear_mu_applicable += 1
                        linear_mu_detected += int(correct != wrong_linear)
                    h = correct
                    pairs += 1
                worlds.append({"id": f"n{ni}_k{ki}_m{mi}", "N": n,
                               "k0": k, "mu": str(mu), "H_t": history})
    stationarity = []
    for n in NS:
        for mu in MUS[1:]:
            h = stationary_diversity(n, mu)
            a, b = coefficients(n, mu)
            assert 0 < h < F(1, 2)
            assert a * h + b == h
            stationarity.append({"N": n, "mu": str(mu), "H_star": str(h),
                                 "cov_lag": {str(s): str(stationary_covariance(n, mu, s))
                                             for s in LAGS}})
    assert len(worlds) == 48 and pairs == 192 and points == 240
    assert len(stationarity) == 9 and mu0_decay_checks == 60
    return {"research_id": "R165", "method": "exact_algebraic_moment_recursion",
            "evidence": "E1_SYNTHETIC_ONLY", "source": "R165 original frozen two-token model",
            "worlds": worlds, "stationary": stationarity,
            "checks": {"worlds": 48, "transitions": pairs, "timepoints": points,
                       "mu0_decay": mu0_decay_checks, "stationary_laws": 9,
                       "stationary_cov_lags": 27,
                       "mutant_omit_c_applicable": omission_c_applicable,
                       "mutant_omit_c_detected": omission_c_detected,
                       "mutant_linear_mu_applicable": linear_mu_applicable,
                       "mutant_linear_mu_detected": linear_mu_detected},
            "E2": 0, "E3": 0, "external_replication": 0}


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, sort_keys=True, ensure_ascii=False))
