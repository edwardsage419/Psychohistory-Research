#!/usr/bin/env python3
"""R206 exact exhaustive 2-means with 4-point artificial populations.

Training observations are i.i.d. (G,H), two independent Rademacher signs.
Coordinates are (a*G,b*H), and externally known G is the synthetic true
"population group". Clustering SSE uses X only; an optional supervised
post-fit cluster->G majority map uses TRAIN G only, never the future G.
The independent new sample is fully enumerated over all four genuine states.

python r206_exact_kmeans.py --test
python r206_exact_kmeans.py --emit
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
Z = F(0)
O = F(1)
SCALES = ((1, 1), (2, 1), (1, 2), (3, 1), (1, 3), (2, 2))
N_VALUES = (3, 4)
STATES = ((-1, -1), (-1, 1), (1, -1), (1, 1))
OUT = Path(__file__).resolve().parent


def validate_scale(a, b):
    if type(a) is not int or type(b) is not int or a <= 0 or b <= 0:
        raise ValueError("positive integer 2D scales only")


def observation(a, b, state):
    validate_scale(a, b)
    if state not in STATES:
        raise ValueError("unknown artificial source state")
    g, h = state
    return (F(a * g), F(b * h))


def squared(v, w):
    if len(v) != 2 or len(w) != 2:
        raise ValueError("two-dimensional only")
    return (v[0] - w[0]) ** 2 + (v[1] - w[1]) ** 2


def dot(v, w):
    return v[0] * w[0] + v[1] * w[1]


def centroid(points):
    if not points:
        raise ValueError("empty cluster prohibited")
    return (sum((p[0] for p in points), Z) / len(points),
            sum((p[1] for p in points), Z) / len(points))


def cluster_sse_two_routes(points, center):
    direct = sum((squared(p, center) for p in points), Z)
    # Σ||x||² − (||Σx||² / n). Independent of the direct residual loop.
    sx = sum((p[0] for p in points), Z)
    sy = sum((p[1] for p in points), Z)
    formula = sum((dot(p, p) for p in points), Z) - (sx ** 2 + sy ** 2) / len(points)
    if direct != formula:
        raise AssertionError("two exact SSE routes disagree")
    return direct


def partitions(n):
    if n not in N_VALUES:
        raise ValueError("only source n=3 or4 is precommitted")
    for mask in range(1, 1 << (n - 1)):
        labels = (0,) + tuple(1 if mask & (1 << (i - 1)) else 0
                              for i in range(1, n))
        if 0 not in labels or 1 not in labels:
            raise AssertionError("empty group")
        yield mask, labels


def all_candidate_partitions(xs):
    n = len(xs)
    if n not in N_VALUES:
        raise ValueError("observed training length must be 3 or 4")
    all_results = []
    for mask, labels in partitions(n):
        groups = {
            0: tuple(xs[i] for i in range(n) if labels[i] == 0),
            1: tuple(xs[i] for i in range(n) if labels[i] == 1),
        }
        centers = (centroid(groups[0]), centroid(groups[1]))
        sse = (cluster_sse_two_routes(groups[0], centers[0]) +
               cluster_sse_two_routes(groups[1], centers[1]))
        all_results.append((sse, mask, labels, centers))
    return tuple(all_results)


def fit_k2(xs):
    candidates = all_candidate_partitions(xs)
    # Exact Fraction SSE and numerical mask tie precedence.
    chosen = min(candidates, key=lambda item: (item[0], item[1]))
    sse, mask, assignments, centers = chosen
    one = centroid(xs)
    k1_sse = cluster_sse_two_routes(xs, one)
    if sse > k1_sse:
        raise AssertionError("optimal two-cluster SSE cannot exceed K1")
    if any(other[0] < sse for other in candidates):
        raise AssertionError("not global optimum among all partitions")
    return {
        "sse_k2_exact": sse,
        "sse_k1_exact": k1_sse,
        "partition_mask": mask,
        "assignments": assignments,
        "centers": centers,
        "center_k1": one,
        "partitions_considered": len(candidates),
    }


def map_clusters_to_training_groups(assignments, source_training_states):
    if len(assignments) != len(source_training_states):
        raise ValueError("train labels size mismatch")
    cluster_names = []
    for k in (0, 1):
        g_in_cluster = [source_training_states[i][0] for i in range(len(assignments))
                        if assignments[i] == k]
        if not g_in_cluster:
            raise ValueError("empty cluster")
        # Majority genuine labels, positive group breaks ties.
        cluster_names.append(1 if sum(g_in_cluster) >= 0 else -1)
    return tuple(cluster_names)


def nearest_cluster(x, centers):
    if len(centers) != 2:
        raise ValueError("two centroids required")
    d0, d1 = squared(x, centers[0]), squared(x, centers[1])
    return 0 if d0 <= d1 else 1


def posthoc_permutation_oracle_error(centers, a, b):
    """EVALUATION ONLY: future G is used to choose the better one-to-one mapping."""
    error_mapping_posneg = Z
    error_mapping_negpos = Z
    for state in STATES:
        g, _ = state
        assigned = nearest_cluster(observation(a, b, state), centers)
        prediction_posneg = 1 if assigned == 0 else -1
        prediction_negpos = -prediction_posneg
        error_mapping_posneg += F(int(prediction_posneg != g), 4)
        error_mapping_negpos += F(int(prediction_negpos != g), 4)
    return min(error_mapping_posneg, error_mapping_negpos)


def fixed_center_independent_future_scores(centers, k1_center, groups_train,
                                           a, b):
    """Use future 4-point source, never future observations in fitting."""
    if len(centers) != 2 or len(groups_train) != 2:
        raise ValueError("two clusters needed")
    source = []
    v_cells = {
        0: {"n": 0, "sx": Z, "sy": Z, "squared_norm": Z},
        1: {"n": 0, "sx": Z, "sy": Z, "squared_norm": Z},
    }
    total_two_sse = Z
    total_one_sse = Z
    total_group_error = Z
    for state in STATES:
        x = observation(a, b, state)
        actual_g = state[0]
        group = nearest_cluster(x, centers)
        c = centers[group]
        d2 = squared(x, c)
        d1 = squared(x, k1_center)
        err = F(int(groups_train[group] != actual_g))
        source.append((state, group, x, d2, d1, err))
        total_two_sse += d2 / 4
        total_one_sse += d1 / 4
        total_group_error += err / 4
        cell = v_cells[group]
        cell["n"] += 1
        cell["sx"] += x[0]
        cell["sy"] += x[1]
        cell["squared_norm"] += dot(x, x)
    # Entirely separate Voronoi-cell moment identity, exactly equal per-cell.
    from_sufficient_moments = Z
    for k in (0, 1):
        c, cell = centers[k], v_cells[k]
        from_sufficient_moments += (cell["squared_norm"]
                                   - 2 * (c[0] * cell["sx"] + c[1] * cell["sy"])
                                   + cell["n"] * dot(c, c)) / 4
    if total_two_sse != from_sufficient_moments:
        raise AssertionError("future independent two-means quantization mismatch")
    # Independent, zero-mean population X: E||X-c||² = a²+b²+||c||².
    one_moment = F(a * a + b * b) + dot(k1_center, k1_center)
    if total_one_sse != one_moment:
        raise AssertionError("future K1 original source and moment routes differ")
    return {
        "quantization_k2": total_two_sse,
        "quantization_k1": total_one_sse,
        "g_label_classification_error_with_train_majority_map": total_group_error,
        "posthoc_test_label_permutation_oracle_error": posthoc_permutation_oracle_error(centers, a, b),
        "all_four_original_future_samples": tuple(source),
    }


def compute():
    all_train = []
    all_train_future = []
    worlds = []
    for a, b in SCALES:
        for n in N_VALUES:
            source_weight = F(1, 4 ** n)
            ptotal = Z
            sum_train2 = Z
            sum_train1 = Z
            sum_future2 = Z
            sum_future1 = Z
            sum_error = Z
            sum_permutation_oracle = Z
            p_train_k2_sse_zero = Z
            p_future2_beats_k1 = Z
            for states in itertools.product(STATES, repeat=n):
                xs = tuple(observation(a, b, state) for state in states)
                fit = fit_k2(xs)
                maps = map_clusters_to_training_groups(fit["assignments"], states)
                future = fixed_center_independent_future_scores(
                    fit["centers"], fit["center_k1"], maps, a, b
                )
                ptotal += source_weight
                train2 = fit["sse_k2_exact"] / n
                train1 = fit["sse_k1_exact"] / n
                sum_train2 += source_weight * train2
                sum_train1 += source_weight * train1
                sum_future2 += source_weight * future["quantization_k2"]
                sum_future1 += source_weight * future["quantization_k1"]
                sum_error += source_weight * future["g_label_classification_error_with_train_majority_map"]
                sum_permutation_oracle += source_weight * future["posthoc_test_label_permutation_oracle_error"]
                if fit["sse_k2_exact"] == Z:
                    p_train_k2_sse_zero += source_weight
                if future["quantization_k2"] < future["quantization_k1"]:
                    p_future2_beats_k1 += source_weight
                record = {
                    "a": a,
                    "b": b,
                    "train_independent_samples_n": n,
                    "ordered_original_GH_source_states": "|".join(f"{g},{h}" for g, h in states),
                    "full_original_training_source_probability": str(source_weight),
                    "original_training_x": "|".join(f"{x[0]},{x[1]}" for x in xs),
                    "exact_partition_candidates": fit["partitions_considered"],
                    "chosen_partition_mask": fit["partition_mask"],
                    "chosen_training_cluster_ids": "|".join(map(str, fit["assignments"])),
                    "k2_centroid0": ",".join(map(str, fit["centers"][0])),
                    "k2_centroid1": ",".join(map(str, fit["centers"][1])),
                    "k1_centroid": ",".join(map(str, fit["center_k1"])),
                    "trained_cluster0_g_label": maps[0],
                    "trained_cluster1_g_label": maps[1],
                    "training_k2_sse_per_observation_exact": str(train2),
                    "training_k1_sse_per_observation_exact": str(train1),
                    "independent_new_k2_quantization_mse_exact": str(future["quantization_k2"]),
                    "independent_new_k1_quantization_mse_exact": str(future["quantization_k1"]),
                    "independent_new_train_mapped_G_classification_error_exact": str(
                        future["g_label_classification_error_with_train_majority_map"]),
                    "future_G_label_permutation_oracle_only_error_exact": str(
                        future["posthoc_test_label_permutation_oracle_error"]),
                }
                all_train.append(record)
                future_mean_sse = Z
                future_mean_class_error = Z
                for state, assigned, x, d2, d1, err in future["all_four_original_future_samples"]:
                    all_train_future.append({
                        "a": a,
                        "b": b,
                        "training_n": n,
                        "ordered_original_GH_source_states": record["ordered_original_GH_source_states"],
                        "independent_new_G": state[0],
                        "independent_new_H": state[1],
                        "independent_new_x1": str(x[0]),
                        "independent_new_x2": str(x[1]),
                        "joint_train_independent_new_state_probability": str(source_weight / 4),
                        "cluster_id_from_frozen_centers_only": assigned,
                        "mapped_group_prediction_from_train_only": maps[assigned],
                        "independent_new_k2_squared_quantization_error": str(d2),
                        "independent_new_k1_squared_quantization_error": str(d1),
                        "independent_new_G_prediction_zero_one_error": str(err),
                    })
                    future_mean_sse += d2 / 4
                    future_mean_class_error += err / 4
                if future_mean_sse != future["quantization_k2"]:
                    raise AssertionError("full future data differs from source moment")
                if future_mean_class_error != future["g_label_classification_error_with_train_majority_map"]:
                    raise AssertionError("full future group outcomes differ")
            if ptotal != O:
                raise AssertionError("incomplete world source probability")
            worlds.append({
                "true_scale_a": a,
                "n_independent_original_training_rows": n,
                "true_nuisance_scale_b": b,
                "ordered_complete_training_original_records": 4 ** n,
                "source_original_probability_sum": str(ptotal),
                "global_k2_partition_candidates_each_training": 2 ** (n - 1) - 1,
                "expected_training_k2_sse_per_row_exact": str(sum_train2),
                "expected_training_k1_sse_per_row_exact": str(sum_train1),
                "expected_independent_new_k2_quantization_mse_exact": str(sum_future2),
                "expected_independent_new_k1_quantization_mse_exact": str(sum_future1),
                "expected_independent_new_k2_quantization_mse": float(sum_future2),
                "expected_independent_new_k1_quantization_mse": float(sum_future1),
                "expected_independent_new_G_error_after_train_label_map_exact": str(sum_error),
                "expected_independent_new_G_error_after_train_label_map": float(sum_error),
                "expected_independent_new_permutation_oracle_G_error_exact": str(sum_permutation_oracle),
                "fixed_constant_G_plus_baseline_error_exact": "1/2",
                "target_aware_true_first_coordinate_sign_G_oracle_error_exact": "0",
                "probability_training_k2_sse_zero": str(p_train_k2_sse_zero),
                "probability_k2_independent_quantization_better_than_k1_per_train": str(
                    p_future2_beats_k1),
            })
    if (len(worlds), len(all_train), len(all_train_future)) != (12, 1920, 7680):
        raise AssertionError("not all original i.i.d. training and independent new events included")
    return {
        "research_id": "R206",
        "status": "ARTIFICIAL_E1_AWAIT_CI_ACCEPTANCE",
        "source_references": {
            "hartigan_wong_1979_doi": "10.2307/2346830",
            "sklearn_kmeans_doc": "https://scikit-learn.org/stable/modules/clustering.html#k-means",
        },
        "true_data_source": "i.i.d. four equiprobable G,H sign pairs, X=(a*G,b*H), G true synthetic group, H nuisance",
        "candidate_k": 2,
        "training_sizes": list(N_VALUES),
        "full_original_training_source_histories": len(all_train),
        "full_joint_train_independent_test_source_events": len(all_train_future),
        "full_worlds": len(worlds),
        "training_true_G_used_in_cluster_fit": False,
        "training_true_G_used_only_in_posthoc_majority_map": True,
        "independent_true_G_used_in_fit_or_majority_mapping": False,
        "posthoc_permutation_oracle_uses_future_labels_for_diagnostic_only": True,
        "new_real_human_E2": 0,
        "new_real_historical_E3": 0,
        "worlds": worlds,
        "limits": [
            "Exhaustive global K=2 partition optimum; no Lloyd/Hartigan-Wong algorithm equivalence",
            "Tiny samples n3/4, repeated points and exact tie handling",
            "True G artificially perfectly observed as first-coordinate sign; real psychological groups unknown",
            "Clustering inertia is distinct from heldout quantization or heldout group prediction",
        ],
    }, all_train, all_train_future


def emit():
    res, training, future = compute()
    paths = {
        "result": OUT / "R206_EXACT_RESULTS.json",
        "training": OUT / "R206_ALL_1920_ORIGINAL_KMEANS_TRAINING_HISTORIES.csv",
        "future": OUT / "R206_ALL_7680_INDEPENDENT_NEW_SAMPLE_PAIRS.csv",
    }
    paths["result"].write_text(
        json.dumps(res, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    for k, rows in (("training", training), ("future", future)):
        with paths[k].open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    a = {
        "model_id": "R206",
        "total_worlds": 12,
        "full_original_training_histories": 1920,
        "full_joint_train_independent_test_events": 7680,
        "global_training_partition_enumeration_and_two_fraction_SSE": True,
        "independent_new_moment_and_4_source_enumeration_exact": True,
        "no_future_G_used_to_make_training_prediction": True,
        "new_E2": 0,
        "new_E3": 0,
        **{k + "_sha256": hashlib.sha256(path.read_bytes()).hexdigest()
           for k, path in paths.items()},
    }
    (OUT / "R206_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(a, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(a, indent=2))


class Tests(unittest.TestCase):
    def test_6_scales(self):
        self.assertEqual(len(SCALES), 6)

    def test_training_3_and_4(self):
        self.assertEqual(N_VALUES, (3, 4))

    def test_four_source_states(self):
        self.assertEqual(len(STATES), 4)

    def test_1920_full_source_histories(self):
        self.assertEqual(len(SCALES) * sum(4 ** n for n in N_VALUES), 1920)

    def test_7680_full_train_future_pairs(self):
        self.assertEqual(len(SCALES) * sum(4 ** n for n in N_VALUES) * 4, 7680)

    def test_source_true_G_H_independent(self):
        self.assertEqual(sum((g * h for g, h in STATES), 0), 0)

    def test_source_true_G_balanced(self):
        self.assertEqual(sum(g for g, h in STATES), 0)

    def test_source_true_H_balanced(self):
        self.assertEqual(sum(h for g, h in STATES), 0)

    def test_four_points_coordinates(self):
        self.assertEqual(tuple(observation(2, 3, state) for state in STATES),
                         ((F(-2), F(-3)), (F(-2), F(3)), (F(2), F(-3)), (F(2), F(3))))

    def test_partition_count_n3(self):
        self.assertEqual(len(tuple(partitions(3))), 3)

    def test_partition_count_n4(self):
        self.assertEqual(len(tuple(partitions(4))), 7)

    def test_partition_first_observation_in_cluster0(self):
        for n in N_VALUES:
            self.assertTrue(all(labels[0] == 0 for _, labels in partitions(n)))

    def test_partitions_nonempty(self):
        for n in N_VALUES:
            for _, labels in partitions(n):
                self.assertEqual(set(labels), {0, 1})

    def test_partitions_no_duplicates(self):
        for n in N_VALUES:
            labels = [assignment for _, assignment in partitions(n)]
            self.assertEqual(len(labels), len(set(labels)))

    def test_centroid_rational(self):
        self.assertEqual(centroid(((O, Z), (Z, O))), (F(1, 2), F(1, 2)))

    def test_identical_duplicate_points_valid(self):
        xs = (observation(1, 1, (1, 1)),) * 4
        fit = fit_k2(xs)
        self.assertEqual(fit["sse_k2_exact"], Z)
        self.assertEqual(fit["centers"][0], fit["centers"][1])

    def test_nearest_equal_centers_ties_cluster0(self):
        self.assertEqual(nearest_cluster((Z, Z), ((Z, Z), (Z, Z))), 0)

    def test_centroid_formula_two_routes(self):
        xs = ((F(-3), F(2)), (F(1), F(-4)), (F(2), F(2)))
        self.assertGreaterEqual(cluster_sse_two_routes(xs, centroid(xs)), Z)

    def test_optimal_global_k2_sse_not_greater_than_k1(self):
        for a, b in SCALES:
            for n in N_VALUES:
                for states in itertools.product(STATES, repeat=n):
                    xs = tuple(observation(a, b, s) for s in states)
                    fit = fit_k2(xs)
                    self.assertLessEqual(fit["sse_k2_exact"], fit["sse_k1_exact"])

    def test_global_partition_exact_minimum(self):
        xs = tuple(observation(1, 3, s) for s in STATES)
        fit = fit_k2(xs)
        self.assertEqual(fit["sse_k2_exact"], min(c[0] for c in all_candidate_partitions(xs)))

    def test_balanced_nuisance_dominant_splits_nuisance(self):
        xs = tuple(observation(1, 3, s) for s in STATES)
        fit = fit_k2(xs)
        self.assertEqual(fit["sse_k2_exact"], F(4))
        self.assertEqual(fit["centers"], ((Z, F(-3)), (Z, F(3))))

    def test_balanced_true_group_dominant_splits_G(self):
        xs = tuple(observation(3, 1, s) for s in STATES)
        fit = fit_k2(xs)
        self.assertEqual(fit["sse_k2_exact"], F(4))
        self.assertEqual(fit["centers"], ((F(-3), Z), (F(3), Z)))

    def test_nuisance_split_permutation_oracle_group_half(self):
        xs = tuple(observation(1, 3, s) for s in STATES)
        fit = fit_k2(xs)
        self.assertEqual(posthoc_permutation_oracle_error(fit["centers"], 1, 3), F(1, 2))

    def test_G_split_permutation_oracle_zero(self):
        xs = tuple(observation(3, 1, s) for s in STATES)
        fit = fit_k2(xs)
        self.assertEqual(posthoc_permutation_oracle_error(fit["centers"], 3, 1), Z)

    def test_permuted_training_labels_do_not_affect_sse(self):
        xs = tuple(observation(2, 1, s) for s in STATES)
        fit = fit_k2(xs)
        labels = fit["assignments"]
        swapped = tuple(1-v for v in labels)
        group0 = tuple(xs[i] for i in range(4) if swapped[i] == 0)
        group1 = tuple(xs[i] for i in range(4) if swapped[i] == 1)
        sse = (cluster_sse_two_routes(group0, centroid(group0)) +
               cluster_sse_two_routes(group1, centroid(group1)))
        self.assertEqual(sse, fit["sse_k2_exact"])

    def test_label_majority_tie_plus(self):
        assignments = (0, 0, 1, 1)
        true = ((-1,-1), (1,-1), (-1,1), (1,1))
        self.assertEqual(map_clusters_to_training_groups(assignments, true), (1, 1))

    def test_train_majority_group_label_is_not_clustering_input(self):
        xs = tuple(observation(3, 1, s) for s in STATES)
        a = fit_k2(xs)
        self.assertEqual(a, fit_k2(xs))

    def test_four_source_independent_new_sse_two_routes(self):
        for a, b in SCALES:
            xs = tuple(observation(a, b, s) for s in STATES)
            fit = fit_k2(xs)
            groups = map_clusters_to_training_groups(fit["assignments"], STATES)
            scores = fixed_center_independent_future_scores(
                fit["centers"], fit["center_k1"], groups, a, b)
            self.assertGreaterEqual(scores["quantization_k2"], Z)

    def test_future_k1_analytic_formula(self):
        xs = tuple(observation(2, 3, s) for s in STATES)
        fit = fit_k2(xs)
        labels = map_clusters_to_training_groups(fit["assignments"], STATES)
        scores = fixed_center_independent_future_scores(
            fit["centers"], fit["center_k1"], labels, 2, 3)
        self.assertEqual(scores["quantization_k1"], F(13))

    def test_training_group_majority_future_error_bounded(self):
        for a, b in SCALES:
            xs = tuple(observation(a, b, s) for s in STATES)
            fit = fit_k2(xs)
            groups = map_clusters_to_training_groups(fit["assignments"], STATES)
            score = fixed_center_independent_future_scores(
                fit["centers"], fit["center_k1"], groups, a, b)
            self.assertTrue(Z <= score["g_label_classification_error_with_train_majority_map"] <= 1)

    def test_oracle_group_sign_known_first_coordinate(self):
        for a, b in SCALES:
            for state in STATES:
                x = observation(a, b, state)
                self.assertEqual(1 if x[0] > 0 else -1, state[0])

    def test_baseline_plus_new_group_error_half(self):
        self.assertEqual(F(sum(g != 1 for g, h in STATES), 4), F(1, 2))

    def test_invalid_scale_rejected(self):
        with self.assertRaises(ValueError):
            observation(0, 1, (-1,1))

    def test_invalid_state_rejected(self):
        with self.assertRaises(ValueError):
            observation(1, 1, (0, 1))

    def test_invalid_training_n_rejected(self):
        with self.assertRaises(ValueError):
            fit_k2(((Z,Z),(O,O)))

    def test_invalid_nearest_centers_rejected(self):
        with self.assertRaises(ValueError):
            nearest_cluster((O,O), ((Z,Z),))

    def test_compute_full_counts(self):
        r, train, paired = compute()
        self.assertEqual((len(r["worlds"]), len(train), len(paired)), (12, 1920, 7680))
        self.assertFalse(r["training_true_G_used_in_cluster_fit"])
        self.assertTrue(r["posthoc_permutation_oracle_uses_future_labels_for_diagnostic_only"])

    def test_complete_replay_deterministic(self):
        self.assertEqual(compute(), compute())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    if args.test:
        out = unittest.TextTestRunner(verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Tests))
        raise SystemExit(0 if out.wasSuccessful() else 1)
    if args.emit:
        emit()
    if not args.test and not args.emit:
        parser.print_help()
