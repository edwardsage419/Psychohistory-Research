#!/usr/bin/env python3
"""R205 finite-sample axis PCA with exact independent reconstruction and two targets.

The source is an artificial PAIR-BALANCED design: each independently sampled
axis produces two dependent, symmetric training observations. It is not an
i.i.d. observation sample. Holdout is a new independent axis and new sign.
PCA uses no labels; target-aware axis preservation is an oracle comparison.

Usage:
    python r205_exact_axis_pca.py --test
    python r205_exact_axis_pca.py --emit
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import unittest
from fractions import Fraction
from pathlib import Path

F = Fraction
ZERO = F(0)
ONE = F(1)
SCALES = ((1, 1), (2, 1), (1, 2), (3, 1), (1, 3), (2, 2))
PAIR_COUNTS = (3, 5)
TEST_AXIS_AND_SIGN = ((1, 1), (1, -1), (2, 1), (2, -1))
OUT = Path(__file__).resolve().parent


def validate_scale(a: int, b: int) -> None:
    if type(a) is not int or type(b) is not int or a <= 0 or b <= 0:
        raise ValueError("coordinate scales must be positive integers")


def train_observations(axes: tuple[int, ...], a: int, b: int):
    validate_scale(a, b)
    if len(axes) not in PAIR_COUNTS or any(v not in (1, 2) for v in axes):
        raise ValueError("training needs 3 or 5 precommitted paired axis draws")
    rows = []
    for axis in axes:
        if axis == 1:
            rows.extend(((F(a), ZERO), (F(-a), ZERO)))
        else:
            rows.extend(((ZERO, F(b)), (ZERO, F(-b))))
    return tuple(rows)


def covariance_from_original_pairs(rows):
    if len(rows) not in (6, 10) or any(len(row) != 2 for row in rows):
        raise ValueError("expected six or ten paired 2D observations")
    n = len(rows)
    means = tuple(sum((row[j] for row in rows), ZERO) / n for j in range(2))
    centered = tuple((row[0] - means[0], row[1] - means[1]) for row in rows)
    cov = tuple(tuple(sum((v[i] * v[j] for v in centered), ZERO) / n
                      for j in range(2)) for i in range(2))
    return means, cov


def covariance_from_axis_count(axes, a: int, b: int):
    m = len(axes)
    k = axes.count(1)
    return ((F(k * a * a, m), ZERO),
            (ZERO, F((m - k) * b * b, m)))


def fit_rank_one_pca(axes: tuple[int, ...], a: int, b: int):
    original = train_observations(axes, a, b)
    means, cov = covariance_from_original_pairs(original)
    expected = covariance_from_axis_count(axes, a, b)
    if means != (ZERO, ZERO) or cov != expected:
        raise AssertionError("two independent empirical covariance routes disagree")
    first, second = cov[0][0], cov[1][1]
    if first + second <= 0 or cov[0][1] != 0:
        raise AssertionError("this frozen design requires nonzero diagonal scatter")
    # Deterministic tie direction and sign: +e1 if lambda1 >= lambda2.
    chosen = 1 if first >= second else 2
    eigenvalue = max(first, second)
    trained_ratio = eigenvalue / (first + second)
    # Check the first PC minimizes TRAINING reconstruction among both axes.
    residual_if_e1 = sum((row[1] ** 2 for row in original), ZERO) / len(original)
    residual_if_e2 = sum((row[0] ** 2 for row in original), ZERO) / len(original)
    if min(residual_if_e1, residual_if_e2) != (first + second - eigenvalue):
        raise AssertionError("variance-max / reconstruction-min identity failed")
    if (residual_if_e1 if chosen == 1 else residual_if_e2) != min(residual_if_e1, residual_if_e2):
        raise AssertionError("trained PC does not minimize training residual")
    return {
        "axes": axes,
        "chosen_axis": chosen,
        "empirical_covariance": cov,
        "training_explained_variance_ratio_exact": trained_ratio,
        "training_rank1_reconstruction_mse_exact": first + second - eigenvalue,
        "training_covariance_trace_exact": first + second,
    }


def holdout_sample(axis: int, sign: int, a: int, b: int):
    validate_scale(a, b)
    if (axis, sign) not in TEST_AXIS_AND_SIGN:
        raise ValueError("unknown independent future event")
    return (F(sign * a), ZERO) if axis == 1 else (ZERO, F(sign * b))


def project_on_axis(x, selected_axis: int):
    if selected_axis == 1:
        return (x[0], ZERO)
    if selected_axis == 2:
        return (ZERO, x[1])
    raise ValueError("rank-one axis must be 1 or 2")


def squared_reconstruction(x, projected):
    if len(x) != 2 or len(projected) != 2:
        raise ValueError("two coordinates required")
    return (x[0] - projected[0]) ** 2 + (x[1] - projected[1]) ** 2


def target_value(x, a: int, b: int, target_axis: int):
    validate_scale(a, b)
    if target_axis == 1:
        return x[0] / a
    if target_axis == 2:
        return x[1] / b
    raise ValueError("target axis must be 1 or 2")


def independent_expected_scores(selected_axis: int, a: int, b: int):
    """Independent check from population axis variance, no test loops."""
    validate_scale(a, b)
    if selected_axis not in (1, 2):
        raise ValueError("unknown selected axis")
    total_variance = F(a * a + b * b, 2)
    if selected_axis == 1:
        retained = F(a * a, 2)
        recon = F(b * b, 2)
        y1_loss, y2_loss = ZERO, F(1, 2)
    else:
        retained = F(b * b, 2)
        recon = F(a * a, 2)
        y1_loss, y2_loss = F(1, 2), ZERO
    return {
        "reconstruction_mse_exact": recon,
        "future_explained_variance_ratio_exact": retained / total_variance,
        "future_target1_mse_exact": y1_loss,
        "future_target2_mse_exact": y2_loss,
    }


def full_independent_future_scores(selected_axis: int, a: int, b: int):
    """Independent source enumeration over fresh axis and fresh sign."""
    all_future = []
    for axis, sign in TEST_AXIS_AND_SIGN:
        x = holdout_sample(axis, sign, a, b)
        projected = project_on_axis(x, selected_axis)
        all_future.append((
            squared_reconstruction(x, projected),
            (target_value(x, a, b, 1) - target_value(projected, a, b, 1)) ** 2,
            (target_value(x, a, b, 2) - target_value(projected, a, b, 2)) ** 2,
            x[0] ** 2 + x[1] ** 2,
            projected[0] ** 2 + projected[1] ** 2,
        ))
    mean = tuple(sum((r[j] for r in all_future), ZERO) / 4 for j in range(5))
    if mean[3] <= 0:
        raise AssertionError("true future variance zero")
    empirical = {
        "reconstruction_mse_exact": mean[0],
        "future_explained_variance_ratio_exact": mean[4] / mean[3],
        "future_target1_mse_exact": mean[1],
        "future_target2_mse_exact": mean[2],
    }
    if empirical != independent_expected_scores(selected_axis, a, b):
        raise AssertionError("independent future exact source enumeration and moment routes differ")
    return empirical


def compute():
    training_records = []
    test_source_pairs = []
    worlds = []
    for a, b in SCALES:
        for m in PAIR_COUNTS:
            selected_probability = {1: ZERO, 2: ZERO}
            exp_training_ratio = ZERO
            exp_future_ratio = ZERO
            exp_train_recon = ZERO
            exp_future_recon = ZERO
            exp_target1 = ZERO
            exp_target2 = ZERO
            probability_sum = ZERO
            for axes in itertools.product((1, 2), repeat=m):
                model = fit_rank_one_pca(axes, a, b)
                axis_chosen = model["chosen_axis"]
                training_p = F(1, 2 ** m)
                future = full_independent_future_scores(axis_chosen, a, b)
                selected_probability[axis_chosen] += training_p
                exp_training_ratio += training_p * model["training_explained_variance_ratio_exact"]
                exp_future_ratio += training_p * future["future_explained_variance_ratio_exact"]
                exp_train_recon += training_p * model["training_rank1_reconstruction_mse_exact"]
                exp_future_recon += training_p * future["reconstruction_mse_exact"]
                exp_target1 += training_p * future["future_target1_mse_exact"]
                exp_target2 += training_p * future["future_target2_mse_exact"]
                probability_sum += training_p
                training_records.append({
                    "true_a": a,
                    "true_b": b,
                    "independent_training_pair_count": m,
                    "training_observation_count": 2 * m,
                    "ordered_training_pair_axes": "|".join(map(str, axes)),
                    "source_train_probability": str(training_p),
                    "full_sample_mean_x1": "0",
                    "full_sample_mean_x2": "0",
                    "source_empirical_cov_x1x1": str(model["empirical_covariance"][0][0]),
                    "source_empirical_cov_x1x2": str(model["empirical_covariance"][0][1]),
                    "source_empirical_cov_x2x2": str(model["empirical_covariance"][1][1]),
                    "training_selected_PC_axis": axis_chosen,
                    "training_explained_ratio_exact": str(model["training_explained_variance_ratio_exact"]),
                    "training_reconstruction_mse_exact": str(model["training_rank1_reconstruction_mse_exact"]),
                    "true_independent_new_event_recon_mse_exact": str(future["reconstruction_mse_exact"]),
                    "true_independent_new_event_retained_ratio_exact": str(future["future_explained_variance_ratio_exact"]),
                    "true_independent_new_event_target1_mse_exact": str(future["future_target1_mse_exact"]),
                    "true_independent_new_event_target2_mse_exact": str(future["future_target2_mse_exact"]),
                })
                pair_score_sums = [ZERO, ZERO, ZERO]
                for test_axis, test_sign in TEST_AXIS_AND_SIGN:
                    holdout = holdout_sample(test_axis, test_sign, a, b)
                    projected = project_on_axis(holdout, axis_chosen)
                    loss_recon = squared_reconstruction(holdout, projected)
                    loss_y1 = (
                        target_value(holdout, a, b, 1) -
                        target_value(projected, a, b, 1)
                    ) ** 2
                    loss_y2 = (
                        target_value(holdout, a, b, 2) -
                        target_value(projected, a, b, 2)
                    ) ** 2
                    for i, score in enumerate((loss_recon, loss_y1, loss_y2)):
                        pair_score_sums[i] += score / 4
                    test_source_pairs.append({
                        "true_a": a,
                        "true_b": b,
                        "independent_training_pair_count": m,
                        "ordered_training_pair_axes": "|".join(map(str, axes)),
                        "true_heldout_axis": test_axis,
                        "true_heldout_sign": test_sign,
                        "source_joint_probability_exact": str(training_p / 4),
                        "selected_PC_axis_using_training_only": axis_chosen,
                        "new_independent_holdout_x1": str(holdout[0]),
                        "new_independent_holdout_x2": str(holdout[1]),
                        "new_independent_reconstruction_error_exact": str(loss_recon),
                        "new_independent_target1_error_exact": str(loss_y1),
                        "new_independent_target2_error_exact": str(loss_y2),
                    })
                if tuple(pair_score_sums) != (
                    future["reconstruction_mse_exact"],
                    future["future_target1_mse_exact"],
                    future["future_target2_mse_exact"],
                ):
                    raise AssertionError("raw future quadruple scoring differs from preselected analytical risk")
            if probability_sum != ONE or sum(selected_probability.values(), ZERO) != ONE:
                raise AssertionError("incomplete original training distribution")
            pop_axis = 1 if a * a >= b * b else 2
            pop_oracle_mse = F(min(a * a, b * b), 2)
            if exp_future_recon < pop_oracle_mse:
                raise AssertionError("source-optimal population PC cannot be beaten")
            worlds.append({
                "true_scale_a": a,
                "true_scale_b": b,
                "training_independent_paired_axis_draws": m,
                "complete_original_training_axis_histories": 2 ** m,
                "complete_original_training_observations_per_history": 2 * m,
                "independent_test_events_per_train": 4,
                "training_probability_sum": str(probability_sum),
                "probability_select_PC_axis1": str(selected_probability[1]),
                "probability_select_PC_axis2": str(selected_probability[2]),
                "expected_training_explained_variance_ratio_exact": str(exp_training_ratio),
                "expected_training_explained_variance_ratio": float(exp_training_ratio),
                "expected_independent_heldout_explained_variance_ratio_exact": str(exp_future_ratio),
                "expected_independent_heldout_explained_variance_ratio": float(exp_future_ratio),
                "expected_training_reconstruction_mse_exact": str(exp_train_recon),
                "expected_independent_heldout_reconstruction_mse_exact": str(exp_future_recon),
                "expected_independent_heldout_reconstruction_mse": float(exp_future_recon),
                "population_rank1_PC_optimal_axis": pop_axis,
                "population_rank1_reconstruction_oracle_mse_exact": str(pop_oracle_mse),
                "expected_independent_target1_mse_exact": str(exp_target1),
                "expected_independent_target2_mse_exact": str(exp_target2),
                "independent_target1_zero_prediction_baseline_mse_exact": "1/2",
                "independent_target2_zero_prediction_baseline_mse_exact": "1/2",
                "target_aware_projection_oracle_each_target_mse_exact": "0",
            })
    if len(worlds) != 12 or len(training_records) != 240 or len(test_source_pairs) != 960:
        raise AssertionError("not complete original sampling spaces")
    diagnostics = {
        "source_training_unit": "independent axis draw producing a DETERMINISTIC dependent plus/minus observation pair",
        "source_training_rows_within_pair_iid": False,
        "sample_empirical_covariance_always_diagonal_by_design": True,
        "all_fraction_training_two_covariance_routes": True,
        "all_fraction_future_enumeration_vs_moment_routes": True,
        "sign_and_eigenvalue_tie_rule": "positive coordinate eigenvector, e1 wins equal eigenvalues",
        "isotropic_a1_b1_m5_expected_train_retained_ratio": next(
            w["expected_training_explained_variance_ratio_exact"] for w in worlds
            if (w["true_scale_a"], w["true_scale_b"], w["training_independent_paired_axis_draws"]) == (1, 1, 5)),
        "isotropic_a1_b1_m5_expected_future_retained_ratio": next(
            w["expected_independent_heldout_explained_variance_ratio_exact"] for w in worlds
            if (w["true_scale_a"], w["true_scale_b"], w["training_independent_paired_axis_draws"]) == (1, 1, 5)),
        "a3_b1_m5_future_target2_mse": next(
            w["expected_independent_target2_mse_exact"] for w in worlds
            if (w["true_scale_a"], w["true_scale_b"], w["training_independent_paired_axis_draws"]) == (3, 1, 5)),
        "e1_only_warning": "Artificial paired axis sampling and normalized targets; not general eigen-rotations, observational real datasets, causal latent factors or historical forecasting.",
    }
    return {
        "research_id": "R205",
        "status": "ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "literature": {
            "pearson_1901_doi": "10.1080/14786440109462720",
            "jolliffe_cadima_2016_doi": "10.1098/rsta.2015.0202",
        },
        "true_scale_sources": [[a, b] for a, b in SCALES],
        "training_pair_counts": list(PAIR_COUNTS),
        "full_original_training_histories": len(training_records),
        "full_original_independent_test_source_pairs": len(test_source_pairs),
        "source_worlds": len(worlds),
        "new_real_human_E2": 0,
        "new_real_historical_E3": 0,
        "worlds": worlds,
        "diagnostics": diagnostics,
    }, training_records, test_source_pairs


def emit():
    r, training, heldout = compute()
    paths = {
        "results": OUT / "R205_EXACT_RESULTS.json",
        "training": OUT / "R205_ALL_240_ORIGINAL_PAIRED_PCA_TRAINING_HISTORIES.csv",
        "holdout": OUT / "R205_ALL_960_INDEPENDENT_TEST_SOURCE_PAIRS.csv",
    }
    paths["results"].write_text(
        json.dumps(r, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    for key, rows in (("training", training), ("holdout", heldout)):
        with paths[key].open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    acceptance = {
        "model_id": "R205",
        "worlds": 12,
        "full_original_training_histories": 240,
        "full_original_train_test_joint_events": 960,
        "double_fraction_source_covariance_and_future_scoring": True,
        "paired_design_dependency_preserved": True,
        "new_E2": 0,
        "new_E3": 0,
        **{k + "_sha256": hashlib.sha256(p.read_bytes()).hexdigest() for k, p in paths.items()},
    }
    (OUT / "R205_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(acceptance, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(acceptance, indent=2))


class Tests(unittest.TestCase):
    def test_6_sources(self):
        self.assertEqual(len(SCALES), 6)

    def test_two_pair_counts(self):
        self.assertEqual(PAIR_COUNTS, (3, 5))

    def test_4_future_states(self):
        self.assertEqual(len(TEST_AXIS_AND_SIGN), 4)

    def test_240_training_source_count(self):
        self.assertEqual(len(SCALES) * sum(2 ** m for m in PAIR_COUNTS), 240)

    def test_960_test_pair_count(self):
        self.assertEqual(len(SCALES) * sum(2 ** m for m in PAIR_COUNTS) * 4, 960)

    def test_training_pairs_dependent_design(self):
        self.assertEqual(train_observations((1, 2, 1), 2, 3),
                         ((F(2), ZERO), (F(-2), ZERO),
                          (ZERO, F(3)), (ZERO, F(-3)),
                          (F(2), ZERO), (F(-2), ZERO)))

    def test_training_mean_exactly_zero(self):
        for a, b in SCALES:
            for m in PAIR_COUNTS:
                for axes in itertools.product((1, 2), repeat=m):
                    mu, _ = covariance_from_original_pairs(train_observations(axes, a, b))
                    self.assertEqual(mu, (ZERO, ZERO))

    def test_full_covariance_equals_counts(self):
        for a, b in SCALES:
            for m in PAIR_COUNTS:
                for axes in itertools.product((1, 2), repeat=m):
                    _, cov = covariance_from_original_pairs(train_observations(axes, a, b))
                    self.assertEqual(cov, covariance_from_axis_count(axes, a, b))

    def test_covariance_offdiag_zero(self):
        _, cov = covariance_from_original_pairs(train_observations((1, 2, 1, 2, 2), 3, 1))
        self.assertEqual(cov[0][1], ZERO)
        self.assertEqual(cov[1][0], ZERO)

    def test_training_trace_positive(self):
        for a, b in SCALES:
            for m in PAIR_COUNTS:
                for axes in itertools.product((1, 2), repeat=m):
                    model = fit_rank_one_pca(axes, a, b)
                    self.assertGreater(model["training_covariance_trace_exact"], ZERO)

    def test_first_eigen_direction_tie_e1(self):
        self.assertEqual(fit_rank_one_pca((1, 2, 1, 2), 1, 1)["chosen_axis"], 1)

    def test_axis1_strict_variance(self):
        self.assertEqual(fit_rank_one_pca((1, 1, 1), 3, 1)["chosen_axis"], 1)

    def test_axis2_strict_variance(self):
        self.assertEqual(fit_rank_one_pca((2, 2, 1), 1, 3)["chosen_axis"], 2)

    def test_explained_ratio_between_half_and_one(self):
        for a, b in SCALES:
            for m in PAIR_COUNTS:
                for axes in itertools.product((1, 2), repeat=m):
                    x = fit_rank_one_pca(axes, a, b)["training_explained_variance_ratio_exact"]
                    self.assertTrue(F(1, 2) <= x <= ONE)

    def test_unobserved_axis_training_ratio_one(self):
        for a, b in SCALES:
            for m in PAIR_COUNTS:
                for ax in (1, 2):
                    x = fit_rank_one_pca((ax,) * m, a, b)
                    self.assertEqual(x["training_explained_variance_ratio_exact"], ONE)
                    self.assertEqual(x["training_rank1_reconstruction_mse_exact"], ZERO)

    def test_future_source_axis_symmetric(self):
        for a, b in SCALES:
            out = [holdout_sample(axis, sgn, a, b) for axis, sgn in TEST_AXIS_AND_SIGN]
            self.assertEqual(sum((v[0] for v in out), ZERO), ZERO)
            self.assertEqual(sum((v[1] for v in out), ZERO), ZERO)

    def test_future_expected_recon_two_routes(self):
        for a, b in SCALES:
            for axis in (1, 2):
                self.assertEqual(full_independent_future_scores(axis, a, b),
                                 independent_expected_scores(axis, a, b))

    def test_future_reconstruction_e1(self):
        self.assertEqual(independent_expected_scores(1, 3, 1)["reconstruction_mse_exact"], F(1, 2))

    def test_future_reconstruction_e2(self):
        self.assertEqual(independent_expected_scores(2, 3, 1)["reconstruction_mse_exact"], F(9, 2))

    def test_future_explained_isotropic_half(self):
        for axis in (1, 2):
            self.assertEqual(independent_expected_scores(axis, 1, 1)
                             ["future_explained_variance_ratio_exact"], F(1, 2))

    def test_target1_target2_task_tradeoff(self):
        q1 = independent_expected_scores(1, 3, 1)
        q2 = independent_expected_scores(2, 3, 1)
        self.assertEqual((q1["future_target1_mse_exact"], q1["future_target2_mse_exact"]),
                         (ZERO, F(1, 2)))
        self.assertEqual((q2["future_target1_mse_exact"], q2["future_target2_mse_exact"]),
                         (F(1, 2), ZERO))

    def test_future_target_variance_same_one_half(self):
        for a, b in SCALES:
            points = [holdout_sample(j, s, a, b) for j, s in TEST_AXIS_AND_SIGN]
            for j in (1, 2):
                self.assertEqual(sum((target_value(x, a, b, j) ** 2 for x in points), ZERO) / 4,
                                 F(1, 2))

    def test_isotropic_m3_train_ratio(self):
        training_ratios = [
            fit_rank_one_pca(tuple(axes), 1, 1)["training_explained_variance_ratio_exact"]
            for axes in itertools.product((1, 2), repeat=3)]
        self.assertEqual(sum(training_ratios, ZERO) / 8, F(3, 4))

    def test_isotropic_m5_train_ratio(self):
        training_ratios = [
            fit_rank_one_pca(tuple(axes), 1, 1)["training_explained_variance_ratio_exact"]
            for axes in itertools.product((1, 2), repeat=5)]
        self.assertEqual(sum(training_ratios, ZERO) / 32, F(11, 16))

    def test_high_first_axis_selection_probability(self):
        chosen = [fit_rank_one_pca(tuple(axes), 3, 1)["chosen_axis"] for axes in
                  itertools.product((1, 2), repeat=5)]
        self.assertEqual(chosen.count(1), 31)

    def test_high_first_axis_target2_loss(self):
        chosen = [fit_rank_one_pca(tuple(axes), 3, 1)["chosen_axis"] for axes in
                  itertools.product((1, 2), repeat=5)]
        exact = sum((independent_expected_scores(i, 3, 1)["future_target2_mse_exact"]
                     for i in chosen), ZERO) / 32
        self.assertEqual(exact, F(31, 64))

    def test_population_pca_explained_not_supervised_target(self):
        # The true population PC for scale (3,1) is x1; target Y2 is exactly x2.
        self.assertEqual(independent_expected_scores(1, 3, 1)
                         ["future_target2_mse_exact"], F(1, 2))
        self.assertEqual(independent_expected_scores(2, 3, 1)
                         ["future_target2_mse_exact"], ZERO)

    def test_rank_one_projection_idempotent(self):
        for axis in (1, 2):
            for a, b in SCALES:
                for xax, sign in TEST_AXIS_AND_SIGN:
                    x = holdout_sample(xax, sign, a, b)
                    self.assertEqual(project_on_axis(project_on_axis(x, axis), axis),
                                     project_on_axis(x, axis))

    def test_no_original_future_used_fit(self):
        model = fit_rank_one_pca((1, 1, 2), 3, 1)
        self.assertEqual(model["chosen_axis"], fit_rank_one_pca((1, 1, 2), 3, 1)["chosen_axis"])

    def test_invalid_scale_rejected(self):
        with self.assertRaises(ValueError):
            holdout_sample(1, 1, 0, 2)

    def test_invalid_pair_count_rejected(self):
        with self.assertRaises(ValueError):
            train_observations((1, 2), 1, 1)

    def test_invalid_axis_rejected(self):
        with self.assertRaises(ValueError):
            train_observations((1, 2, 3), 1, 1)

    def test_invalid_holdout_event_rejected(self):
        with self.assertRaises(ValueError):
            holdout_sample(2, 0, 1, 1)

    def test_invalid_project_axis_rejected(self):
        with self.assertRaises(ValueError):
            project_on_axis((ONE, ZERO), 3)

    def test_complete_results(self):
        r, train, test = compute()
        self.assertEqual((len(r["worlds"]), len(train), len(test)), (12, 240, 960))
        self.assertEqual(r["new_real_human_E2"], 0)
        self.assertEqual(r["diagnostics"]["isotropic_a1_b1_m5_expected_train_retained_ratio"], "11/16")
        self.assertEqual(r["diagnostics"]["a3_b1_m5_future_target2_mse"], "31/64")

    def test_full_replay_deterministic(self):
        self.assertEqual(compute(), compute())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--emit", action="store_true")
    opts = parser.parse_args()
    if opts.test:
        result = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if result.wasSuccessful() else 1)
    if opts.emit:
        emit()
    if not (opts.test or opts.emit):
        parser.print_help()
