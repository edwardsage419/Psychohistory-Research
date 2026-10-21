#!/usr/bin/env python3
"""R202 finite artificial accelerated failure time model with administrative censoring.

Strict standard-library, exhaustive rational sample space, genuinely independent
new-subject time-threshold evaluation. --test / --emit.
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

BASE = (Fraction(1), Fraction(2), Fraction(4), Fraction(8))
TRUE_A = (Fraction(1, 2), Fraction(1), Fraction(2))
CANDIDATES = (Fraction(1), Fraction(1, 2), Fraction(2))
CUTOFFS = (Fraction(2), Fraction(4))
TARGET = Fraction(3)
ORIGINAL_PAIRS = tuple(itertools.product(BASE, repeat=2))
OUT = Path(__file__).resolve().parent


def check_a(a):
    if not isinstance(a, Fraction) or a <= 0:
        raise ValueError("AFT scale must be positive Fraction")


def exact_time(a: Fraction, x: int, baseline: Fraction) -> Fraction:
    check_a(a)
    if x not in (0, 1) or baseline not in BASE:
        raise ValueError("invalid exposure or baseline support")
    return baseline * (a if x else 1)


def observation(time: Fraction, cutoff: Fraction) -> tuple[Fraction, int]:
    if time <= 0 or cutoff not in CUTOFFS:
        raise ValueError("invalid time or censoring cutoff")
    # Event at the administrative cutoff is observed.
    return min(time, cutoff), int(time <= cutoff)


def observed_person_probability(a: Fraction, x: int,
                                obs: tuple[Fraction, int], cutoff: Fraction) -> Fraction:
    check_a(a)
    if x not in (0, 1) or cutoff not in CUTOFFS:
        raise ValueError("invalid exposure or cutoff")
    if len(obs) != 2 or obs[1] not in (0, 1):
        raise ValueError("invalid observed event flag")
    time, event = obs
    if time <= 0 or time > cutoff or (not event and time != cutoff):
        raise ValueError("inconsistent censoring record")
    # Sum exact latent baseline paths that produce the observed record.
    return Fraction(sum(observation(exact_time(a, x, b), cutoff) == obs for b in BASE), 4)


def source_observed_pair(a: Fraction, raw_pair: tuple[Fraction, Fraction],
                         cutoff: Fraction) -> tuple[tuple[Fraction, int], tuple[Fraction, int]]:
    if len(raw_pair) != 2:
        raise ValueError("two training people required")
    return (observation(exact_time(a, 0, raw_pair[0]), cutoff),
            observation(exact_time(a, 1, raw_pair[1]), cutoff))


def joint_observed_likelihood(a: Fraction, obs_pair, cutoff: Fraction) -> Fraction:
    return (observed_person_probability(a, 0, obs_pair[0], cutoff)
            * observed_person_probability(a, 1, obs_pair[1], cutoff))


def joint_likelihood_by_original_paths(a: Fraction, obs_pair, cutoff: Fraction) -> Fraction:
    return Fraction(sum(source_observed_pair(a, raw, cutoff) == obs_pair
                        for raw in ORIGINAL_PAIRS), len(ORIGINAL_PAIRS))


def fit(obs_pair, cutoff: Fraction) -> Fraction:
    likelihoods = [joint_observed_likelihood(a, obs_pair, cutoff) for a in CANDIDATES]
    if max(likelihoods) <= 0:
        raise ValueError("observation impossible under all candidates")
    return CANDIDATES[likelihoods.index(max(likelihoods))]


def future_probability(a: Fraction) -> Fraction:
    """Probability a new independent x=1 subject has event by horizon 3."""
    return Fraction(sum(exact_time(a, 1, b) <= TARGET for b in BASE), len(BASE))


def future_brier(source_a: Fraction, prediction_a: Fraction) -> Fraction:
    p, q = future_probability(source_a), future_probability(prediction_a)
    direct = p * (1 - q) ** 2 + (1 - p) * q ** 2
    decomposition = p * (1 - p) + (q - p) ** 2
    if direct != decomposition:
        raise AssertionError("Brier direct and decomposition differ")
    return direct


def future_logloss(source_a: Fraction, prediction_a: Fraction) -> float:
    p, q = future_probability(source_a), future_probability(prediction_a)
    ordinary = -float(p) * math.log(float(q)) - float(1 - p) * math.log(float(1 - q))
    with localcontext() as ctx:
        ctx.prec = 70
        pd = Decimal(p.numerator) / Decimal(p.denominator)
        qd = Decimal(q.numerator) / Decimal(q.denominator)
        high_precision = -(pd * qd.ln() + (1 - pd) * (1 - qd).ln())
    if abs(ordinary - float(high_precision)) > 1e-12:
        raise AssertionError("70-digit logloss confirmation failed")
    return ordinary


def discrete_hazard(times: tuple[Fraction, ...], t: Fraction) -> Fraction:
    at_risk = sum(v >= t for v in times)
    if at_risk == 0:
        raise ValueError("no one at risk")
    return Fraction(sum(v == t for v in times), at_risk)


def compute():
    original_records = []
    worlds = []
    for source_a in TRUE_A:
        for cutoff in CUTOFFS:
            selected = {a: Fraction(0) for a in CANDIDATES}
            brier_sum = Fraction(0)
            logloss_sum = 0.
            for raw_pair in ORIGINAL_PAIRS:
                visible = source_observed_pair(source_a, raw_pair, cutoff)
                candidate_likelihood = {
                    a: joint_observed_likelihood(a, visible, cutoff) for a in CANDIDATES
                }
                for a in CANDIDATES:
                    assert candidate_likelihood[a] == joint_likelihood_by_original_paths(a, visible, cutoff)
                chosen_a = fit(visible, cutoff)
                assert chosen_a in CANDIDATES
                true_source_mass = Fraction(1, 16)
                selected[chosen_a] += true_source_mass
                brier = future_brier(source_a, chosen_a)
                logloss = future_logloss(source_a, chosen_a)
                brier_sum += true_source_mass * brier
                logloss_sum += float(true_source_mass) * logloss
                original_records.append({
                    "true_time_scale_a": str(source_a),
                    "administrative_censor_time": str(cutoff),
                    "original_x0_baseline_T0": str(raw_pair[0]),
                    "original_x1_baseline_T0": str(raw_pair[1]),
                    "x0_visible_time": str(visible[0][0]),
                    "x0_event_flag": visible[0][1],
                    "x1_visible_time": str(visible[1][0]),
                    "x1_event_flag": visible[1][1],
                    "original_training_source_probability": "1/16",
                    "training_likelihood_a1": str(candidate_likelihood[Fraction(1)]),
                    "training_likelihood_a1over2": str(candidate_likelihood[Fraction(1, 2)]),
                    "training_likelihood_a2": str(candidate_likelihood[Fraction(2)]),
                    "selected_a": str(chosen_a),
                    "independent_new_x1_T_le_3_probability": str(future_probability(chosen_a)),
                    "independent_new_x1_expected_brier": str(brier),
                    "independent_new_x1_expected_logloss": format(logloss, ".14f"),
                })
            assert sum(selected.values(), Fraction(0)) == 1
            oracle = future_brier(source_a, source_a)
            assert brier_sum >= oracle
            worlds.append({
                "true_time_scale_a": str(source_a),
                "censor_cutoff": str(cutoff),
                "original_training_records": 16,
                "training_source_probability_sum": "1",
                "model_selection_probabilities": {str(a): str(selected[a]) for a in CANDIDATES},
                "selected_true_a_probability": str(selected[source_a]),
                "new_independent_person_true_target_probability": str(future_probability(source_a)),
                "new_independent_person_Brier_exact": str(brier_sum),
                "new_independent_person_Brier": round(float(brier_sum), 14),
                "new_independent_person_logloss": round(logloss_sum, 14),
                "fixed_a_1_Brier_exact": str(future_brier(source_a, Fraction(1))),
                "known_true_a_oracle_Brier_exact": str(oracle),
                "oracle_gap_exact": str(brier_sum - oracle),
            })
    assert len(original_records) == 96 and len(worlds) == 6
    reference = tuple(exact_time(Fraction(2), 0, b) for b in BASE)
    exposed = tuple(exact_time(Fraction(2), 1, b) for b in BASE)
    diagnostics = {
        "true_AFT_target_probabilities": {str(a): str(future_probability(a)) for a in TRUE_A},
        "x0_observation_likelihood_identical_across_all_time_scales": all(
            len({observed_person_probability(a, 0, observation(b, c), c)
                 for a in CANDIDATES}) == 1 for b in BASE for c in CUTOFFS
        ),
        "censor_at_cutoff_is_distinct_from_event_at_cutoff": [
            {"observation": ["2", 1], "source_a2_x1_probability": str(observed_person_probability(
                Fraction(2), 1, (Fraction(2), 1), Fraction(2)))},
            {"observation": ["2", 0], "source_a2_x1_probability": str(observed_person_probability(
                Fraction(2), 1, (Fraction(2), 0), Fraction(2)))},
        ],
        "a2_discrete_hazard_ratio_at_time2": str(
            discrete_hazard(exposed, Fraction(2)) / discrete_hazard(reference, Fraction(2))),
        "a2_discrete_hazard_ratio_at_time4": str(
            discrete_hazard(exposed, Fraction(4)) / discrete_hazard(reference, Fraction(4))),
        "scope": "Discrete four-point artificial base time; PH comparison conditional on discrete risk interpretation",
    }
    return ({
        "research_id": "R202",
        "status": "ARTIFICIAL_E1_PENDING_EXTERNAL_CI_ACCEPTANCE",
        "literature_doi": "10.1002/sim.4780111409",
        "all_source_worlds": 6,
        "full_original_training_records": 96,
        "training_base_pairs_per_world": 16,
        "independent_heldout_new_person_exposure": 1,
        "independent_heldout_event_threshold": "3",
        "candidate_a_tie_preference": [str(a) for a in CANDIDATES],
        "new_real_human_E2": 0,
        "new_real_historical_E3": 0,
        "worlds": worlds,
        "diagnostics": diagnostics,
    }, original_records)


def emit():
    result, records = compute()
    result_path = OUT / "R202_EXACT_RESULTS.json"
    csv_path = OUT / "R202_ALL_96_ORIGINAL_CENSORED_TRAINING_WORLDS.csv"
    result_path.write_text(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    acceptance = {
        "research_id": "R202",
        "total_worlds": 6,
        "total_original_train_source_records": 96,
        "all_fraction_source_and_brier_identities": True,
        "two_logloss_implementations": True,
        "new_E2": 0,
        "new_E3": 0,
        "result_sha256": hashlib.sha256(result_path.read_bytes()).hexdigest(),
        "original_source_csv_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
    }
    (OUT / "R202_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(acceptance, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(acceptance, indent=2))


class TestR202(unittest.TestCase):
    def test_time_scale_identity_reference(self):
        for a in TRUE_A:
            for b in BASE:
                self.assertEqual(exact_time(a, 0, b), b)

    def test_exposed_time_scales(self):
        for b in BASE:
            self.assertEqual(exact_time(Fraction(2), 1, b), 2 * b)

    def test_future_target_probs(self):
        self.assertEqual({str(a): str(future_probability(a)) for a in TRUE_A},
                         {"1/2": "3/4", "1": "1/2", "2": "1/4"})

    def test_event_exactly_at_censor_cutoff_is_observed(self):
        self.assertEqual(observation(Fraction(2), Fraction(2)), (Fraction(2), 1))

    def test_after_cutoff_is_censored(self):
        self.assertEqual(observation(Fraction(4), Fraction(2)), (Fraction(2), 0))

    def test_event_and_censor_same_recorded_time_are_distinct(self):
        self.assertEqual(observed_person_probability(Fraction(2), 1, (Fraction(2), 1), Fraction(2)), Fraction(1, 4))
        self.assertEqual(observed_person_probability(Fraction(2), 1, (Fraction(2), 0), Fraction(2)), Fraction(3, 4))

    def test_zero_exposure_independent_of_a(self):
        for c in CUTOFFS:
            for b in BASE:
                obs = observation(b, c)
                self.assertEqual(len({observed_person_probability(a, 0, obs, c) for a in TRUE_A}), 1)

    def test_exposure_event_distribution_normalizes(self):
        for a in TRUE_A:
            for c in CUTOFFS:
                outcomes = {observation(exact_time(a, 1, b), c) for b in BASE}
                self.assertEqual(sum((observed_person_probability(a, 1, ob, c) for ob in outcomes), Fraction(0)), 1)

    def test_reference_distribution_normalizes(self):
        for c in CUTOFFS:
            outcomes = {observation(b, c) for b in BASE}
            self.assertEqual(sum((observed_person_probability(Fraction(1), 0, ob, c) for ob in outcomes), Fraction(0)), 1)

    def test_joint_likelihood_two_routes_all_worlds(self):
        for a in TRUE_A:
            for c in CUTOFFS:
                for raw in ORIGINAL_PAIRS:
                    obs = source_observed_pair(a, raw, c)
                    for model_a in CANDIDATES:
                        self.assertEqual(joint_observed_likelihood(model_a, obs, c),
                                         joint_likelihood_by_original_paths(model_a, obs, c))

    def test_joint_source_distribution_normalizes(self):
        for a in TRUE_A:
            for c in CUTOFFS:
                visible_outcomes = {source_observed_pair(a, raw, c) for raw in ORIGINAL_PAIRS}
                self.assertEqual(sum((joint_observed_likelihood(a, ob, c) for ob in visible_outcomes), Fraction(0)), 1)

    def test_selected_candidate_has_positive_likelihood(self):
        for a in TRUE_A:
            for c in CUTOFFS:
                for raw in ORIGINAL_PAIRS:
                    ob = source_observed_pair(a, raw, c)
                    self.assertGreater(joint_observed_likelihood(fit(ob, c), ob, c), 0)

    def test_selection_in_locked_candidates(self):
        for a in TRUE_A:
            for c in CUTOFFS:
                for raw in ORIGINAL_PAIRS:
                    self.assertIn(fit(source_observed_pair(a, raw, c), c), CANDIDATES)

    def test_brier_identity_oracle(self):
        for a in TRUE_A:
            for selected in CANDIDATES:
                self.assertGreaterEqual(future_brier(a, selected), future_brier(a, a))

    def test_no_effect_oracle_brier(self):
        self.assertEqual(future_brier(Fraction(1), Fraction(1)), Fraction(1, 4))

    def test_aft_extremes_oracle_brier(self):
        self.assertEqual(future_brier(Fraction(2), Fraction(2)), Fraction(3, 16))
        self.assertEqual(future_brier(Fraction(1, 2), Fraction(1, 2)), Fraction(3, 16))

    def test_two_logloss_methods(self):
        for a in TRUE_A:
            for b in CANDIDATES:
                self.assertTrue(math.isfinite(future_logloss(a, b)))

    def test_discrete_hazard_non_proportional(self):
        ref = tuple(exact_time(Fraction(2), 0, b) for b in BASE)
        exp = tuple(exact_time(Fraction(2), 1, b) for b in BASE)
        self.assertEqual(discrete_hazard(exp, Fraction(2)) / discrete_hazard(ref, Fraction(2)), Fraction(3, 4))
        self.assertEqual(discrete_hazard(exp, Fraction(4)) / discrete_hazard(ref, Fraction(4)), Fraction(2, 3))

    def test_reject_nonpositive_scale(self):
        for a in (Fraction(0), Fraction(-1)):
            with self.assertRaises(ValueError):
                future_probability(a)

    def test_reject_invalid_exposure(self):
        with self.assertRaises(ValueError):
            exact_time(Fraction(1), 2, BASE[0])

    def test_reject_inconsistent_censor_record(self):
        with self.assertRaises(ValueError):
            observed_person_probability(Fraction(1), 1, (Fraction(1), 0), Fraction(2))

    def test_reject_bad_cutoff(self):
        with self.assertRaises(ValueError):
            observation(Fraction(1), Fraction(3))

    def test_full_record_counts(self):
        result, records = compute()
        self.assertEqual(len(records), 96)
        self.assertEqual(len(result["worlds"]), 6)
        self.assertTrue(all(w["original_training_records"] == 16 for w in result["worlds"]))

    def test_compute_reproducible(self):
        self.assertEqual(compute(), compute())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    if args.test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestR202)
        result = unittest.TextTestRunner(verbosity=2).run(suite)
        raise SystemExit(0 if result.wasSuccessful() else 1)
    if args.emit:
        emit()
    if not args.test and not args.emit:
        parser.print_help()
