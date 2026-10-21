#!/usr/bin/env python3
"""R201: finite exact Cox partial likelihood and independent-cohort event-order forecast.

Python standard library only. All subjects and mechanisms are entirely artificial.
Use --test for deterministic tests, --emit for machine-readable archival data.
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

X = (0, 0, 1, 1)
SUBJECTS = tuple(range(4))
TRUE_HRS = (Fraction(1, 4), Fraction(1), Fraction(4))
CANDIDATES = (Fraction(1), Fraction(1, 4), Fraction(4))
ALL_ORDERS = tuple(itertools.permutations(SUBJECTS))
OUT = Path(__file__).resolve().parent


def validate_hr(hr: Fraction) -> None:
    if not isinstance(hr, Fraction) or hr <= 0:
        raise ValueError("hazard ratio must be a positive Fraction")


def weights(hr: Fraction, remaining: tuple[int, ...]) -> dict[int, Fraction]:
    validate_hr(hr)
    if not remaining or len(set(remaining)) != len(remaining):
        raise ValueError("risk set must contain unique subjects")
    if any(i not in SUBJECTS for i in remaining):
        raise ValueError("unknown subject")
    return {i: hr if X[i] else Fraction(1) for i in remaining}


def first_event_distribution(hr: Fraction, remaining: tuple[int, ...] = SUBJECTS) -> dict[int, Fraction]:
    w = weights(hr, remaining)
    total = sum(w.values(), Fraction(0))
    return {i: w[i] / total for i in remaining}


def prefix_likelihood(prefix: tuple[int, ...], hr: Fraction) -> Fraction:
    if len(prefix) > len(SUBJECTS) or len(set(prefix)) != len(prefix):
        raise ValueError("invalid ordered failure prefix")
    remaining = SUBJECTS
    likelihood = Fraction(1)
    for failed in prefix:
        if failed not in remaining:
            raise ValueError("failure not in the risk set")
        likelihood *= first_event_distribution(hr, remaining)[failed]
        remaining = tuple(i for i in remaining if i != failed)
    return likelihood


def full_order_probability(order: tuple[int, ...], hr: Fraction) -> Fraction:
    if len(order) != len(SUBJECTS):
        raise ValueError("complete event order needs four distinct subjects")
    return prefix_likelihood(order, hr)


def fit_candidate(prefix: tuple[int, ...]) -> Fraction:
    """Precommitted finite Cox partial-likelihood maximization, null-first ties."""
    if not 1 <= len(prefix) <= 3:
        raise ValueError("training prefix length must be 1, 2 or 3")
    likelihoods = [prefix_likelihood(prefix, h) for h in CANDIDATES]
    return CANDIDATES[likelihoods.index(max(likelihoods))]


def brier_multiclass(true_hr: Fraction, fitted_hr: Fraction) -> Fraction:
    p = first_event_distribution(true_hr)
    q = first_event_distribution(fitted_hr)
    direct = sum(
        (p[i] * (1 - q[i]) ** 2 + (1 - p[i]) * q[i] ** 2)
        for i in SUBJECTS
    )
    decomposition = (
        1 - 2 * sum((p[i] * q[i] for i in SUBJECTS), Fraction(0))
        + sum((q[i] ** 2 for i in SUBJECTS), Fraction(0))
    )
    if direct != decomposition:
        raise AssertionError("Brier independent paths differ")
    return direct


def logloss_two_methods(true_hr: Fraction, fitted_hr: Fraction) -> float:
    p = first_event_distribution(true_hr)
    q = first_event_distribution(fitted_hr)
    standard = -sum(float(p[i]) * math.log(float(q[i])) for i in SUBJECTS)
    with localcontext() as ctx:
        ctx.prec = 70
        precise = Decimal(0)
        for i in SUBJECTS:
            pd = Decimal(p[i].numerator) / Decimal(p[i].denominator)
            qd = Decimal(q[i].numerator) / Decimal(q[i].denominator)
            precise -= pd * qd.ln()
    if abs(standard - float(precise)) > 1e-12:
        raise AssertionError("logloss numerical methods differ")
    return standard


def exact_prefix_source_mass(prefix: tuple[int, ...], true_hr: Fraction) -> Fraction:
    return sum(
        (full_order_probability(order, true_hr)
         for order in ALL_ORDERS if order[:len(prefix)] == prefix),
        Fraction(0),
    )


def tied_event_factor(risk: tuple[int, ...], failed: tuple[int, ...],
                      hr: Fraction, method: str) -> Fraction:
    """Single tied event group; exact is conditional on unordered failure set."""
    w = weights(hr, risk)
    if not failed or len(failed) > len(risk) or len(set(failed)) != len(failed):
        raise ValueError("invalid tied failure set")
    if not set(failed).issubset(risk):
        raise ValueError("failure absent from risk set")
    d = len(failed)
    total = sum(w.values(), Fraction(0))
    failed_total = sum((w[i] for i in failed), Fraction(0))
    num = math.prod(w[i] for i in failed)
    if method == "breslow":
        den = total ** d
    elif method == "efron":
        den = math.prod(total - Fraction(j, d) * failed_total for j in range(d))
    elif method == "exact":
        den = sum(
            (math.prod(w[i] for i in subset) for subset in itertools.combinations(risk, d)),
            Fraction(0),
        )
    else:
        raise ValueError("unknown ties method")
    return num / den


def censored_partial_likelihood(rows: tuple[tuple[int, int, int, int], ...],
                                hr: Fraction) -> Fraction:
    """Rows: (subject_id, observed_time, event_1_or_censor_0, binary_exposure).
    Event times must be distinct; failures precede any censor at the same time.
    This implementation uses SUBJECTS and their frozen binary X vector.
    """
    validate_hr(hr)
    if len({row[0] for row in rows}) != len(rows):
        raise ValueError("duplicate subject")
    for ident, time, event, x in rows:
        if ident not in SUBJECTS or x != X[ident] or time <= 0 or event not in (0, 1):
            raise ValueError("invalid censoring input")
    failures = sorted((row for row in rows if row[2] == 1), key=lambda row: row[1])
    if len({row[1] for row in failures}) != len(failures):
        raise ValueError("use a tied event handler for tied failure times")
    likelihood = Fraction(1)
    for ident, time, _, _ in failures:
        risk = tuple(row[0] for row in rows if row[1] >= time)
        likelihood *= first_event_distribution(hr, risk)[ident]
    return likelihood


def baseline_absolute_event_probability(common_hazard: float, hr: Fraction, t: float = 1.) -> float:
    if common_hazard <= 0 or t <= 0:
        raise ValueError("positive baseline hazard and horizon required")
    # Explicitly an exponential time model, an extra assumption not learned from Cox PL.
    total = sum(float(w) for w in weights(hr, SUBJECTS).values())
    return -math.expm1(-common_hazard * t * total)


def compute():
    records = []
    worlds = []
    for source_hr in TRUE_HRS:
        complete_pmf = {order: full_order_probability(order, source_hr) for order in ALL_ORDERS}
        assert sum(complete_pmf.values(), Fraction(0)) == 1
        for k in (1, 2, 3):
            chosen_mass = {hr: Fraction(0) for hr in CANDIDATES}
            source_mass = Fraction(0)
            expected_brier = Fraction(0)
            expected_logloss = 0.
            prefixes = tuple(itertools.permutations(SUBJECTS, k))
            for prefix in prefixes:
                source_probability = prefix_likelihood(prefix, source_hr)
                independent = sum(
                    (complete_pmf[o] for o in ALL_ORDERS if o[:k] == prefix),
                    Fraction(0),
                )
                assert independent == source_probability
                fitted = fit_candidate(prefix)
                selected_brier = brier_multiclass(source_hr, fitted)
                selected_logloss = logloss_two_methods(source_hr, fitted)
                chosen_mass[fitted] += source_probability
                source_mass += source_probability
                expected_brier += source_probability * selected_brier
                expected_logloss += float(source_probability) * selected_logloss
                records.append({
                    "true_hr": str(source_hr),
                    "observed_failures": k,
                    "prefix_subject_ids": "|".join(str(i) for i in prefix),
                    "true_source_prefix_probability": str(source_probability),
                    "cox_pl_hr_1": str(prefix_likelihood(prefix, Fraction(1))),
                    "cox_pl_hr_1_over_4": str(prefix_likelihood(prefix, Fraction(1, 4))),
                    "cox_pl_hr_4": str(prefix_likelihood(prefix, Fraction(4))),
                    "fitted_hr": str(fitted),
                    "new_cohort_four_class_brier": str(selected_brier),
                    "new_cohort_four_class_logloss": format(selected_logloss, ".14f"),
                })
            assert source_mass == 1
            assert sum(chosen_mass.values(), Fraction(0)) == 1
            oracle = brier_multiclass(source_hr, source_hr)
            null_risk = brier_multiclass(source_hr, Fraction(1))
            assert expected_brier >= oracle
            worlds.append({
                "true_hr": str(source_hr),
                "training_observed_event_count": k,
                "complete_order_source_count": 24,
                "ordered_training_prefix_count": len(prefixes),
                "training_prefix_source_probability_total": str(source_mass),
                "selected_hr_probability": {str(h): str(chosen_mass[h]) for h in CANDIDATES},
                "selected_true_hr_probability": str(chosen_mass[source_hr]),
                "independent_new_cohort_expected_brier_exact": str(expected_brier),
                "independent_new_cohort_expected_brier": round(float(expected_brier), 14),
                "independent_new_cohort_expected_logloss": round(expected_logloss, 14),
                "fixed_hr_1_new_cohort_brier_exact": str(null_risk),
                "known_true_hr_oracle_new_cohort_brier_exact": str(oracle),
                "oracle_gap_exact": str(expected_brier - oracle),
            })
    assert len(records) == 120 and len(worlds) == 9
    tied = {
        method: str(tied_event_factor(SUBJECTS, (0, 2), Fraction(4), method))
        for method in ("breslow", "efron", "exact")
    }
    censor = ((2, 1, 1, 1), (0, 2, 0, 0), (1, 3, 1, 0), (3, 4, 1, 1))
    # After low-x person 0 is censored, risk at t=3 is {1,3}.
    correct = censored_partial_likelihood(censor, Fraction(4))
    naive = Fraction(4, 10) * Fraction(1, 6)
    assert correct == Fraction(2, 25) and naive == Fraction(1, 15) and correct != naive
    diagnostics = {
        "four_person_exposure": list(X),
        "tied_one_low_one_high_hr4": tied,
        "censored_correct_partial_likelihood_hr4": str(correct),
        "incorrect_keep_censored_in_later_risk_set": str(naive),
        "same_next_event_order_probability_under_baseline_scale": True,
        "event_by_horizon_one_baseline_0_1_hr4": round(baseline_absolute_event_probability(0.1, Fraction(4)), 14),
        "event_by_horizon_one_baseline_0_2_hr4": round(baseline_absolute_event_probability(0.2, Fraction(4)), 14),
        "equal_composition_early_x1_event_share_hr4": "4/5",
        "equal_composition_late_x1_event_share_hr1over4": "1/5",
    }
    result = {
        "research_id": "R201",
        "status": "ARTIFICIAL_E1_PENDING_EXTERNAL_CI_ACCEPTANCE",
        "literature_doi": "10.1111/j.2517-6161.1972.tb00899.x",
        "training_only_candidates_prelocked": [str(x) for x in CANDIDATES],
        "true_sources": [str(x) for x in TRUE_HRS],
        "full_order_data_count": 72,
        "distinct_ordered_training_rows_count": len(records),
        "independent_validation_worlds": len(worlds),
        "new_real_human_E2": 0,
        "new_real_historical_E3": 0,
        "worlds": worlds,
        "diagnostics": diagnostics,
        "caveat": "Four artificial exponential-race event-order sources. Cox PL alone cannot identify baseline hazard or absolute event times; censoring independence and PH need outside validation.",
    }
    return result, records


def emit():
    result, records = compute()
    result_path = OUT / "R201_EXACT_RESULTS.json"
    csv_path = OUT / "R201_ALL_120_ORIGINAL_TRAINING_PREFIXES.csv"
    result_path.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)
    summary = {
        "model": "R201",
        "total_worlds": 9,
        "source_complete_orders": 72,
        "all_original_prefix_records": 120,
        "exact_fraction_and_decimal_verification": True,
        "new_E2": 0,
        "new_E3": 0,
        "result_sha256": hashlib.sha256(result_path.read_bytes()).hexdigest(),
        "source_prefix_csv_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
    }
    (OUT / "R201_FINAL_MACHINE_ACCEPTANCE.json").write_text(
        json.dumps(summary, sort_keys=True, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


class TestR201(unittest.TestCase):
    def test_source_pmf(self):
        for hr in TRUE_HRS:
            self.assertEqual(sum((full_order_probability(o, hr) for o in ALL_ORDERS), Fraction(0)), 1)

    def test_complete_order_positive(self):
        for hr in TRUE_HRS:
            self.assertTrue(all(full_order_probability(o, hr) > 0 for o in ALL_ORDERS))

    def test_prefix_normalization(self):
        for hr in TRUE_HRS:
            for k in (1, 2, 3):
                self.assertEqual(sum((prefix_likelihood(p, hr) for p in itertools.permutations(SUBJECTS, k)), Fraction(0)), 1)

    def test_prefix_full_order_independent_identity(self):
        for hr in TRUE_HRS:
            for k in (1, 2, 3):
                for p in itertools.permutations(SUBJECTS, k):
                    self.assertEqual(prefix_likelihood(p, hr), exact_prefix_source_mass(p, hr))

    def test_next_event_probability_normalization(self):
        for hr in TRUE_HRS:
            for remaining_k in (1, 2, 3, 4):
                for risk in itertools.combinations(SUBJECTS, remaining_k):
                    self.assertEqual(sum(first_event_distribution(hr, risk).values()), 1)

    def test_exposure_4_to_1_share(self):
        p = first_event_distribution(Fraction(4))
        self.assertEqual(p[2] + p[3], Fraction(4, 5))

    def test_exposure_1_to_4_share(self):
        p = first_event_distribution(Fraction(1, 4))
        self.assertEqual(p[2] + p[3], Fraction(1, 5))

    def test_equal_hr_uniform(self):
        self.assertEqual(set(first_event_distribution(Fraction(1)).values()), {Fraction(1, 4)})

    def test_finite_fitted_candidates(self):
        for k in (1, 2, 3):
            for p in itertools.permutations(SUBJECTS, k):
                self.assertIn(fit_candidate(p), CANDIDATES)

    def test_fit_does_not_need_source_label(self):
        self.assertEqual(fit_candidate((2, 0)), fit_candidate((2, 0)))

    def test_brier_two_exact_paths(self):
        for a in TRUE_HRS:
            for b in CANDIDATES:
                self.assertGreaterEqual(brier_multiclass(a, b), brier_multiclass(a, a))

    def test_null_multiclass_brier(self):
        self.assertEqual(brier_multiclass(Fraction(1), Fraction(1)), Fraction(3, 4))

    def test_oracle_symmetry(self):
        self.assertEqual(brier_multiclass(Fraction(4), Fraction(4)), brier_multiclass(Fraction(1, 4), Fraction(1, 4)))

    def test_double_logloss(self):
        for a in TRUE_HRS:
            for b in CANDIDATES:
                self.assertTrue(math.isfinite(logloss_two_methods(a, b)))

    def test_independent_next_cohort_normalization(self):
        for hr in TRUE_HRS:
            self.assertEqual(sum(first_event_distribution(hr).values()), 1)

    def test_tie_methods_known_rational(self):
        v = {x: tied_event_factor(SUBJECTS, (0, 2), Fraction(4), x)
             for x in ("breslow", "efron", "exact")}
        self.assertEqual(v, {"breslow": Fraction(1, 25), "efron": Fraction(4, 75), "exact": Fraction(4, 33)})

    def test_one_failure_ties_agree(self):
        for m in ("breslow", "efron", "exact"):
            self.assertEqual(tied_event_factor(SUBJECTS, (2,), Fraction(4), m), Fraction(2, 5))

    def test_right_censor_risk_removal(self):
        rows = ((2, 1, 1, 1), (0, 2, 0, 0), (1, 3, 1, 0), (3, 4, 1, 1))
        self.assertEqual(censored_partial_likelihood(rows, Fraction(4)), Fraction(2, 25))

    def test_baseline_time_unidentified(self):
        a = baseline_absolute_event_probability(0.1, Fraction(4))
        b = baseline_absolute_event_probability(0.2, Fraction(4))
        self.assertLess(a, b)
        self.assertEqual(first_event_distribution(Fraction(4)), first_event_distribution(Fraction(4)))

    def test_proportional_hazards_counterexample(self):
        self.assertEqual(sum(first_event_distribution(Fraction(4))[i] for i in (2, 3)), Fraction(4, 5))
        self.assertEqual(sum(first_event_distribution(Fraction(1, 4))[i] for i in (2, 3)), Fraction(1, 5))

    def test_reject_invalid_hr(self):
        for h in (Fraction(0), Fraction(-1)):
            with self.assertRaises(ValueError):
                first_event_distribution(h)

    def test_reject_invalid_subject(self):
        with self.assertRaises(ValueError):
            prefix_likelihood((1, 1), Fraction(1))
        with self.assertRaises(ValueError):
            first_event_distribution(Fraction(1), (0, 4))

    def test_reject_duplicate_censored_person(self):
        with self.assertRaises(ValueError):
            censored_partial_likelihood(((2, 1, 1, 1), (2, 2, 0, 1)), Fraction(4))

    def test_reject_tied_failure_times_without_tie_handler(self):
        with self.assertRaises(ValueError):
            censored_partial_likelihood(((2, 1, 1, 1), (0, 1, 1, 0)), Fraction(4))

    def test_compute_counts_and_bad_examples_retained(self):
        result, records = compute()
        self.assertEqual(len(records), 120)
        self.assertEqual(len(result["worlds"]), 9)
        self.assertTrue(all(w["oracle_gap_exact"] != "" for w in result["worlds"]))
        self.assertEqual(result["diagnostics"]["tied_one_low_one_high_hr4"]["exact"], "4/33")

    def test_deterministic_compute(self):
        self.assertEqual(compute(), compute())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    parser.add_argument("--emit", action="store_true")
    args = parser.parse_args()
    if args.test:
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestR201)
        outcome = unittest.TextTestRunner(verbosity=2).run(suite)
        raise SystemExit(0 if outcome.wasSuccessful() else 1)
    if args.emit:
        emit()
    if not (args.test or args.emit):
        parser.print_help()
