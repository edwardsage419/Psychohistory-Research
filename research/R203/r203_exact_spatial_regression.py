#!/usr/bin/env python3
"""R203 exact finite spatial lag/error mechanism audit.

Four-node ring, five fixed spatial candidates, three covariate patterns,
Rademacher innovations, complete independent heldout-area expected scoring.
All data are artificial. Python standard library only.

Usage: python r203_exact_spatial_regression.py --test
       python r203_exact_spatial_regression.py --emit
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import unittest
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

F = Fraction
N = 4
ZERO = F(0)
ONE = F(1)
R = F(1, 2)
PATTERNS = {
    "SMOOTH": (F(1), F(1), F(1), F(1)),
    "ALTERNATING": (F(1), F(-1), F(1), F(-1)),
    "MIXED": (F(1), F(0), F(0), F(-1)),
}
CANDIDATES = ("IID", "SAR_POS", "SEM_POS", "SAR_NEG", "SEM_NEG")
EPS = tuple(tuple(F(i) for i in seq) for seq in itertools.product((-1, 1), repeat=N))
OUT = Path(__file__).resolve().parent


def eye():
    return tuple(tuple(ONE if i == j else ZERO for j in range(N)) for i in range(N))


I = eye()
W = tuple(
    tuple(F(1, 2) if (i - j) % N in (1, N - 1) else ZERO for j in range(N))
    for i in range(N)
)


def mm(a, b):
    return tuple(tuple(sum((a[i][k] * b[k][j] for k in range(N)), ZERO)
                       for j in range(N)) for i in range(N))


def mv(a, v):
    return tuple(sum((a[i][j] * v[j] for j in range(N)), ZERO)
                 for i in range(N))


def mt(a):
    return tuple(tuple(a[j][i] for j in range(N)) for i in range(N))


def madd(a, b):
    return tuple(tuple(a[i][j] + b[i][j] for j in range(N)) for i in range(N))


def mscale(a, coefficient):
    return tuple(tuple(coefficient * a[i][j] for j in range(N)) for i in range(N))


def vadd(a, b):
    return tuple(a[i] + b[i] for i in range(N))


def vsub(a, b):
    return tuple(a[i] - b[i] for i in range(N))


def vdot(a, b):
    return sum((a[i] * b[i] for i in range(N)), ZERO)


def sqnorm(v):
    return vdot(v, v)


def mat_inverse_exact(a):
    """Independent exact Gauss-Jordan inversion."""
    rows = [[a[i][j] for j in range(N)] + [I[i][j] for j in range(N)]
            for i in range(N)]
    for col in range(N):
        pivot = next((r for r in range(col, N) if rows[r][col] != 0), None)
        if pivot is None:
            raise ValueError("singular matrix")
        rows[col], rows[pivot] = rows[pivot], rows[col]
        d = rows[col][col]
        rows[col] = [v / d for v in rows[col]]
        for j in range(N):
            if j != col:
                coef = rows[j][col]
                rows[j] = [rows[j][k] - coef * rows[col][k] for k in range(2 * N)]
    return tuple(tuple(rows[i][N:]) for i in range(N))


def spatial_A(rho):
    if abs(rho) >= 1:
        raise ValueError("spatial rho must satisfy abs(rho)<1")
    return madd(I, mscale(W, -rho))


def spatial_inverse_polynomial(rho):
    if abs(rho) >= 1:
        raise ValueError("spatial rho must satisfy abs(rho)<1")
    den = ONE - rho ** 2
    return madd(madd(I, mscale(W, rho / den)), mscale(mm(W, W), rho ** 2 / den))


def operator(rho):
    a = spatial_A(rho)
    s = spatial_inverse_polynomial(rho)
    if s != mat_inverse_exact(a) or mm(a, s) != I or mm(s, a) != I:
        raise AssertionError("independent exact spatial inverses disagree")
    return a, s


def model_rho(model):
    if model == "IID":
        return ZERO
    if model in ("SAR_POS", "SEM_POS"):
        return R
    if model in ("SAR_NEG", "SEM_NEG"):
        return -R
    raise ValueError("unknown candidate")


def mean_and_cov(model, x):
    if model not in CANDIDATES or len(x) != N:
        raise ValueError("unknown model or invalid x")
    _, s = operator(model_rho(model))
    mu = mv(s, x) if model.startswith("SAR") else x
    cov = mm(s, mt(s))
    return mu, cov


def sample_outcome(model, x, eps):
    if model not in CANDIDATES or len(eps) != N or any(v not in (-ONE, ONE) for v in eps):
        raise ValueError("invalid source / Rademacher shock")
    mu, _ = mean_and_cov(model, x)
    return vadd(mu, mv(operator(model_rho(model))[1], eps))


def precision_quadratic(model, v):
    a, _ = operator(model_rho(model))
    transformed = mv(a, v)
    route1 = sqnorm(transformed)
    precision = mm(mt(a), a)
    route2 = vdot(v, mv(precision, v))
    if route1 != route2:
        raise AssertionError("two exact precision quadratic forms differ")
    return route1


def constant_log_term(model):
    rho = model_rho(model)
    # Eigenvalues W: 1,-1,0,0; det(I-rho W) = 1-rho^2.
    det_a = ONE - rho ** 2
    if det_a <= 0:
        raise ValueError("invalid determinant")
    ordinary = N * math.log(2 * math.pi) - 2 * math.log(float(det_a))
    with localcontext() as ctx:
        ctx.prec = 70
        pi = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286")
        dd = Decimal(det_a.numerator) / Decimal(det_a.denominator)
        precise = Decimal(N) * (Decimal(2) * pi).ln() - Decimal(2) * dd.ln()
    if abs(ordinary - float(precise)) > 1e-11:
        raise AssertionError("ordinary and 70-digit constant differ")
    return ordinary


def gaussian_working_logscore(model, x, y):
    mu, _ = mean_and_cov(model, x)
    return 0.5 * (constant_log_term(model) + float(precision_quadratic(model, vsub(y, mu))))


def fit_candidate(x, observed_y):
    scores = [gaussian_working_logscore(model, x, observed_y) for model in CANDIDATES]
    m = min(scores)
    # Fixed model precedence and deterministic tolerances independent of true source.
    return CANDIDATES[next(i for i, s in enumerate(scores) if s <= m + 1e-12)]


def future_mse_exact(true_model, forecast_model, x):
    mu_true, sig_true = mean_and_cov(true_model, x)
    mu_q, _ = mean_and_cov(forecast_model, x)
    analytical = (sum((sig_true[i][i] for i in range(N)), ZERO)
                  + sqnorm(vsub(mu_true, mu_q))) / N
    independent_exhaustive = sum(
        (sqnorm(vsub(sample_outcome(true_model, x, e), mu_q)) / N for e in EPS),
        ZERO
    ) / len(EPS)
    if analytical != independent_exhaustive:
        raise AssertionError("heldout independent risk analytic/enumeration differ")
    return analytical


def future_gaussian_logscore_analytical(true_model, forecast_model, x):
    mu_true, sig_true = mean_and_cov(true_model, x)
    mu_q, _ = mean_and_cov(forecast_model, x)
    a, _ = operator(model_rho(forecast_model))
    transformed_sigma = mm(mm(a, sig_true), mt(a))
    tr = sum((transformed_sigma[i][i] for i in range(N)), ZERO)
    diff = vsub(mu_true, mu_q)
    quadratic = precision_quadratic(forecast_model, diff)
    analytical = 0.5 * (constant_log_term(forecast_model) + float(tr + quadratic))
    complete_new_region = sum(
        gaussian_working_logscore(forecast_model, x, sample_outcome(true_model, x, e))
        for e in EPS
    ) / len(EPS)
    if abs(analytical - complete_new_region) > 1e-10:
        raise AssertionError("independent Gaussian work logscore two routes mismatch")
    return analytical


def ols_moments_under_spatial_source(source_model, x):
    xx = vdot(x, x)
    if xx <= 0:
        raise ValueError("x must have positive norm")
    mu, cov = mean_and_cov(source_model, x)
    expectation = vdot(x, mu) / xx
    exact_var = vdot(x, mv(cov, x)) / (xx ** 2)
    iid_naive_var = ONE / xx
    # Independently enumerate the complete finite true data source, checking
    # both analytical mean and the true unconditional finite variance.
    slopes = [vdot(x, sample_outcome(source_model, x, e)) / xx for e in EPS]
    empirical_mean = sum(slopes, ZERO) / len(EPS)
    empirical_variance = sum(((b - empirical_mean) ** 2 for b in slopes), ZERO) / len(EPS)
    if expectation != empirical_mean or exact_var != empirical_variance:
        raise AssertionError("OLS source moments not exact")
    return {
        "true_beta": "1",
        "expected_beta_hat": str(expectation),
        "actual_beta_hat_variance": str(exact_var),
        "naive_iid_variance_with_known_unit_error_variance": str(iid_naive_var),
        "actual_to_naive_variance_ratio": str(exact_var / iid_naive_var),
    }


def compute():
    assert W == mt(W) and all(sum(row, ZERO) == 1 for row in W)
    assert all(W[i][i] == 0 for i in range(N))
    assert mm(mm(W, W), W) == W
    all_training_rows = []
    all_train_test_pairs = []
    all_worlds = []
    for pattern, x in PATTERNS.items():
        candidate_mu = {q: mean_and_cov(q, x)[0] for q in CANDIDATES}
        for source in CANDIDATES:
            selection_prob = {q: ZERO for q in CANDIDATES}
            mean_mse = ZERO
            mean_gaussian_logscore = 0.
            exact_risk_by_q = {q: future_mse_exact(source, q, x) for q in CANDIDATES}
            logscore_by_q = {
                q: future_gaussian_logscore_analytical(source, q, x) for q in CANDIDATES
            }
            for train_eps in EPS:
                train_y = sample_outcome(source, x, train_eps)
                selected = fit_candidate(x, train_y)
                selection_prob[selected] += F(1, 16)
                mse = exact_risk_by_q[selected]
                ll = logscore_by_q[selected]
                mean_mse += mse / 16
                mean_gaussian_logscore += ll / 16
                all_training_rows.append({
                    "covariate_pattern": pattern,
                    "true_source": source,
                    "source_training_shock": "|".join(str(i) for i in train_eps),
                    "source_observed_y": "|".join(str(i) for i in train_y),
                    "original_training_source_probability": "1/16",
                    "selected_candidate": selected,
                    "working_gaussian_nll_IID": format(gaussian_working_logscore("IID", x, train_y), ".14f"),
                    "working_gaussian_nll_SAR_POS": format(gaussian_working_logscore("SAR_POS", x, train_y), ".14f"),
                    "working_gaussian_nll_SEM_POS": format(gaussian_working_logscore("SEM_POS", x, train_y), ".14f"),
                    "working_gaussian_nll_SAR_NEG": format(gaussian_working_logscore("SAR_NEG", x, train_y), ".14f"),
                    "working_gaussian_nll_SEM_NEG": format(gaussian_working_logscore("SEM_NEG", x, train_y), ".14f"),
                    "independent_new_region_exact_MSE_per_node": str(mse),
                    "independent_new_region_gaussian_logscore": format(ll, ".14f"),
                })
                test_mse_average = ZERO
                test_logscore_average = 0.
                for test_eps in EPS:
                    test_y = sample_outcome(source, x, test_eps)
                    diff = vsub(test_y, candidate_mu[selected])
                    sqerr = sqnorm(diff) / N
                    gscore = gaussian_working_logscore(selected, x, test_y)
                    test_mse_average += sqerr / 16
                    test_logscore_average += gscore / 16
                    all_train_test_pairs.append({
                        "covariate_pattern": pattern,
                        "true_source": source,
                        "source_training_shock": "|".join(str(i) for i in train_eps),
                        "independent_test_shock": "|".join(str(i) for i in test_eps),
                        "source_independent_train_test_joint_probability": "1/256",
                        "selected_candidate_from_train_only": selected,
                        "new_region_mean_squared_error_per_node_exact": str(sqerr),
                        "new_region_gaussian_working_logscore": format(gscore, ".14f"),
                    })
                if test_mse_average != mse or abs(test_logscore_average - ll) > 1e-10:
                    raise AssertionError("train-specific exact future score mismatch")
            assert sum(selection_prob.values(), ZERO) == ONE
            oracle_risk = exact_risk_by_q[source]
            oracle_logscore = logscore_by_q[source]
            assert mean_mse >= min(exact_risk_by_q.values())
            all_worlds.append({
                "pattern": pattern,
                "true_source": source,
                "original_training_vectors": 16,
                "independent_test_vectors_per_training_vector": 16,
                "selected_candidate_probabilities_exact": {
                    q: str(selection_prob[q]) for q in CANDIDATES
                },
                "selected_true_source_probability_exact": str(selection_prob[source]),
                "expected_independent_new_region_MSE_exact": str(mean_mse),
                "expected_independent_new_region_MSE": round(float(mean_mse), 12),
                "expected_independent_new_region_gaussian_logscore": round(mean_gaussian_logscore, 12),
                "fixed_IID_new_region_MSE_exact": str(exact_risk_by_q["IID"]),
                "oracle_known_true_mechanism_new_region_MSE_exact": str(oracle_risk),
                "oracle_known_true_mechanism_new_region_gaussian_logscore": round(oracle_logscore, 12),
                "min_candidate_new_region_MSE_exact": str(min(exact_risk_by_q.values())),
                "source_probability_sum_exact": str(sum(selection_prob.values(), ZERO)),
            })
    assert len(all_training_rows) == 240
    assert len(all_train_test_pairs) == 3840
    assert len(all_worlds) == 15
    diagnostics = {
        "spatial_four_node_weight_matrix": [[str(i) for i in row] for row in W],
        "spatial_inverse_two_independent_exact_methods": True,
        "sigma_SAR_POS_equals_sigma_SEM_POS_for_same_W_and_rho": all(
            mean_and_cov("SAR_POS", x)[1] == mean_and_cov("SEM_POS", x)[1]
            for x in PATTERNS.values()
        ),
        "mean_SAR_POS_smooth_x": [str(i) for i in mean_and_cov("SAR_POS", PATTERNS["SMOOTH"])[0]],
        "mean_SEM_POS_smooth_x": [str(i) for i in mean_and_cov("SEM_POS", PATTERNS["SMOOTH"])[0]],
        "ols_unadjusted_under_SEM_POS": {
            name: ols_moments_under_spatial_source("SEM_POS", x)
            for name, x in PATTERNS.items()
        },
        "ols_under_SAR_POS_smooth": ols_moments_under_spatial_source(
            "SAR_POS", PATTERNS["SMOOTH"]
        ),
        "warning": "Fixed beta=1 and finite candidates; normal work likelihood is misspecified for discrete ±1 source innovations. No causal identification or realistic spatial prediction is established.",
    }
    return {
        "research_id": "R203",
        "status": "ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "training_true_sources": list(CANDIDATES),
        "prior_tie_preference": list(CANDIDATES),
        "original_training_samples": len(all_training_rows),
        "independent_train_test_pairs": len(all_train_test_pairs),
        "full_evaluation_worlds": len(all_worlds),
        "original_training_probability_each": "1/16",
        "independent_train_test_pair_probability_each": "1/256",
        "two_way_independent_future_mse_exact": True,
        "two_way_independent_future_work_logscore": True,
        "new_real_human_E2": 0,
        "new_real_historical_E3": 0,
        "worlds": all_worlds,
        "diagnostics": diagnostics,
    }, all_training_rows, all_train_test_pairs


def emit():
    result, training, pairs = compute()
    p_result = OUT / "R203_EXACT_RESULTS.json"
    p_train = OUT / "R203_ALL_240_ORIGINAL_SPATIAL_TRAINING_WORLDS.csv"
    p_pairs = OUT / "R203_ALL_3840_INDEPENDENT_TEST_SOURCE_PAIRS.csv"
    p_result.write_text(json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8")
    for path, records in ((p_train, training), (p_pairs, pairs)):
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)
    acceptance = {
        "model_id": "R203",
        "total_worlds": 15,
        "full_original_training_samples": 240,
        "full_independent_train_test_pair_records": 3840,
        "exact_Fraction_matrix_risk_and_complete_shock_enumeration": True,
        "normal_logscore_double_analytical_and_exhaustive_check": True,
        "new_E2": 0,
        "new_E3": 0,
        "results_sha256": hashlib.sha256(p_result.read_bytes()).hexdigest(),
        "training_source_sha256": hashlib.sha256(p_train.read_bytes()).hexdigest(),
        "independent_test_pairs_sha256": hashlib.sha256(p_pairs.read_bytes()).hexdigest(),
    }
    (OUT / "R203_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(acceptance, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(acceptance, indent=2))


class Tests(unittest.TestCase):
    def test_W_symmetric(self):
        self.assertEqual(W, mt(W))

    def test_W_row_normalized(self):
        self.assertTrue(all(sum(row, ZERO) == ONE for row in W))

    def test_W_diagonal_zero(self):
        self.assertTrue(all(W[i][i] == 0 for i in range(N)))

    def test_W_cubic(self):
        self.assertEqual(mm(mm(W, W), W), W)

    def test_W_not_identity(self):
        self.assertNotEqual(W, I)

    def test_two_inverse_positive(self):
        self.assertEqual(operator(R)[1], mat_inverse_exact(spatial_A(R)))

    def test_two_inverse_negative(self):
        self.assertEqual(operator(-R)[1], mat_inverse_exact(spatial_A(-R)))

    def test_zero_inverse(self):
        self.assertEqual(operator(ZERO), (I, I))

    def test_reject_singular_positive(self):
        with self.assertRaises(ValueError):
            operator(ONE)

    def test_reject_singular_negative(self):
        with self.assertRaises(ValueError):
            operator(-ONE)

    def test_five_model_names(self):
        self.assertEqual(len(CANDIDATES), 5)

    def test_three_patterns(self):
        self.assertEqual(len(PATTERNS), 3)

    def test_16_shocks(self):
        self.assertEqual(len(EPS), 16)

    def test_rademacher_zero_mean(self):
        for j in range(N):
            self.assertEqual(sum((e[j] for e in EPS), ZERO), 0)

    def test_rademacher_unit_variance(self):
        for j in range(N):
            self.assertEqual(sum((e[j]**2 for e in EPS), ZERO) / 16, 1)

    def test_rademacher_independent(self):
        for i in range(N):
            for j in range(N):
                self.assertEqual(sum((e[i]*e[j] for e in EPS), ZERO) / 16, int(i == j))

    def test_covariance_positive_trace(self):
        for model in CANDIDATES:
            for x in PATTERNS.values():
                _, s = mean_and_cov(model, x)
                self.assertTrue(all(s[i][i] > 0 for i in range(N)))

    def test_iid_mean_cov(self):
        for x in PATTERNS.values():
            self.assertEqual(mean_and_cov("IID", x), (x, I))

    def test_same_covariance_sar_sem_positive(self):
        for x in PATTERNS.values():
            self.assertEqual(mean_and_cov("SAR_POS", x)[1], mean_and_cov("SEM_POS", x)[1])

    def test_same_covariance_sar_sem_negative(self):
        for x in PATTERNS.values():
            self.assertEqual(mean_and_cov("SAR_NEG", x)[1], mean_and_cov("SEM_NEG", x)[1])

    def test_different_spatial_mean_smooth(self):
        x = PATTERNS["SMOOTH"]
        self.assertEqual(mean_and_cov("SAR_POS", x)[0], tuple(F(2) for _ in range(N)))
        self.assertEqual(mean_and_cov("SEM_POS", x)[0], x)

    def test_ols_variance_inflation_smooth(self):
        x = PATTERNS["SMOOTH"]
        self.assertEqual(ols_moments_under_spatial_source("SEM_POS", x)
                         ["actual_to_naive_variance_ratio"], "4")

    def test_ols_variance_deflation_alternating(self):
        x = PATTERNS["ALTERNATING"]
        self.assertEqual(ols_moments_under_spatial_source("SEM_POS", x)
                         ["actual_to_naive_variance_ratio"], "4/9")

    def test_sar_spatial_feedback_ols_bias_smooth(self):
        x = PATTERNS["SMOOTH"]
        self.assertEqual(ols_moments_under_spatial_source("SAR_POS", x)
                         ["expected_beta_hat"], "2")

    def test_sem_unbiased_ols_moments(self):
        for x in PATTERNS.values():
            self.assertEqual(ols_moments_under_spatial_source("SEM_POS", x)
                             ["expected_beta_hat"], "1")

    def test_gaussian_quadratic_two_routes(self):
        for model in CANDIDATES:
            self.assertGreaterEqual(precision_quadratic(model, (ONE, ZERO, ONE, ZERO)), 0)

    def test_working_logscore_finite(self):
        for model in CANDIDATES:
            self.assertTrue(math.isfinite(gaussian_working_logscore(model, PATTERNS["MIXED"],
                                                                    (ONE, ZERO, ZERO, ONE))))

    def test_training_fit_candidate_locked(self):
        for model in CANDIDATES:
            for x in PATTERNS.values():
                for e in EPS[:3]:
                    self.assertIn(fit_candidate(x, sample_outcome(model, x, e)), CANDIDATES)

    def test_future_mse_double_exact(self):
        for true in CANDIDATES:
            for guess in CANDIDATES:
                self.assertGreaterEqual(future_mse_exact(true, guess, PATTERNS["MIXED"]), 0)

    def test_future_gaussian_score_double(self):
        for true in CANDIDATES:
            for guess in CANDIDATES:
                self.assertTrue(math.isfinite(future_gaussian_logscore_analytical(
                    true, guess, PATTERNS["MIXED"])))

    def test_correct_gaussian_work_forecast_best_logscore(self):
        for pattern in PATTERNS.values():
            for true in CANDIDATES:
                scores = [future_gaussian_logscore_analytical(true, guess, pattern)
                          for guess in CANDIDATES]
                self.assertLessEqual(scores[CANDIDATES.index(true)], min(scores) + 1e-10)

    def test_true_mean_best_squared_error(self):
        for pattern in PATTERNS.values():
            for true in CANDIDATES:
                scores = [future_mse_exact(true, guess, pattern) for guess in CANDIDATES]
                self.assertLessEqual(scores[CANDIDATES.index(true)], min(scores))

    def test_unknown_model_rejected(self):
        with self.assertRaises(ValueError):
            model_rho("UNRECOGNIZED")

    def test_invalid_shock_rejected(self):
        with self.assertRaises(ValueError):
            sample_outcome("IID", PATTERNS["MIXED"], (ONE, ONE, ZERO, ONE))

    def test_complete_counts_and_moments(self):
        result, train, pairs = compute()
        self.assertEqual((len(result["worlds"]), len(train), len(pairs)), (15, 240, 3840))
        self.assertTrue(result["diagnostics"]["sigma_SAR_POS_equals_sigma_SEM_POS_for_same_W_and_rho"])
        self.assertEqual(result["new_real_human_E2"], 0)

    def test_full_computation_deterministic(self):
        self.assertEqual(compute(), compute())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    if args.test:
        outcome = unittest.TextTestRunner(
            verbosity=2
        ).run(unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if outcome.wasSuccessful() else 1)
    if args.emit:
        emit()
    if not (args.test or args.emit):
        parser.print_help()
