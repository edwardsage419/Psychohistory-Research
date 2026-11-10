"""Invented source statistics and target events only; no human scoring."""
import copy
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import product
from pathlib import Path
import math
import sys
import unittest

import score_oracle as gate

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/R077"))
from r077_fourth_real_human_source_only_e3 import score_with_frozen_source

MODELS = ("M0_TREATMENT_PREVALENCE", "M1_OWN_LAST", "M2_OPPONENT_LAST",
          "M3_JOINT_LAST", "M4_JOINT_TWO_LAGS", "M5_TFT_NOISY", "M6_WSLS_NOISY")


def synthetic_fit(offset=1):
    # For each of 16 history states: 4 fictional source rows, with
    # offset+own1+opp2 positive outcomes. 64 rows; p0=(offset+1)/4.
    return {
        "train_only_prevalence": (offset+1)/4,
        "state_counts": {
            "M1_OWN_LAST": {(a,): (8*offset+4+8*a, 32) for a in (0, 1)},
            "M2_OPPONENT_LAST": {(a,): (8*offset+8, 32) for a in (0, 1)},
            "M3_JOINT_LAST": {(a, b): (4*offset+2+4*a, 16) for a, b in product((0, 1), repeat=2)},
            "M4_JOINT_TWO_LAGS": {h: (offset+h[0]+h[3], 4) for h in product((0, 1), repeat=4)},
        },
        "source_sessions": 2, "train_target_count": 64,
    }


def synthetic_targets(flipped=False):
    rows = list(product((0, 1), repeat=5))
    sessions = {
        "ARTIFICIAL_A": {"treatment": 0, "events": rows},
        "ARTIFICIAL_B": {"treatment": 1, "events": [rows[i] for i in (0, 3, 31)]},
        "ARTIFICIAL_C": {"treatment": 1, "events": [rows[i] for i in (4, 6, 8, 10, 12)]},
        "ARTIFICIAL_D": {"treatment": 0, "events": [rows[i] for i in (17, 19)]},
    }
    if flipped:
        for info in sessions.values():
            info["events"] = [e[:4] + (1-e[4],) for e in info["events"]]
    return sessions


def run_contract(scorer):
    checks = calls = 0
    for offset in (0, 1):
        fit = synthetic_fit(offset)
        for flipped in (False, True):
            checks += gate.check_scorer(scorer, fit, synthetic_targets(flipped))
            calls += 1
        # All history states and both outcomes, using two artificial sessions
        # so both original treatment groups are represented in every call.
        for event in product((0, 1), repeat=5):
            sessions = {f"ARTIFICIAL_{tr}": {"treatment": tr, "events": [event]} for tr in (0, 1)}
            checks += gate.check_scorer(scorer, fit, sessions)
            calls += 1
    return {"score_calls": calls, "output_leaf_comparisons": checks}


class ScoreOracleTests(unittest.TestCase):
    def test_hand_source_probabilities_and_unseen_state(self):
        fit = synthetic_fit(0)
        e = (0, 1, 0, 0, 1)
        self.assertEqual(gate.source_probability(fit, MODELS[0], e), Fraction(1, 4))
        self.assertEqual(gate.source_probability(fit, MODELS[1], e), Fraction(9, 52))
        self.assertEqual(gate.source_probability(fit, MODELS[3], e), Fraction(7, 36))
        self.assertEqual(gate.source_probability(fit, MODELS[4], e), Fraction(5, 24))
        fit["state_counts"][MODELS[4]].pop(e[:4])
        self.assertEqual(gate.source_probability(fit, MODELS[4], e), Fraction(1, 4))

    def test_hand_session_macro_brier_and_decimal_logloss(self):
        result = gate.expected_scores(synthetic_fit(0), synthetic_targets())
        m0 = result["models"][MODELS[0]]
        self.assertEqual(m0["all_original_sessions_equal_Brier"], Fraction(1, 3))
        with localcontext() as ctx:
            ctx.prec = 70
            want = -(Decimal(13)/24*Decimal("0.25").ln() + Decimal(11)/24*Decimal("0.75").ln())
            self.assertLess(abs(m0["all_original_sessions_equal_log_loss"]-want), Decimal("1e-65"))
        self.assertEqual(result["original_session_count"], 4)
        self.assertEqual(result["scored_t3_human_events"], 42)

    def test_original_full_contract_all_states_both_labels_and_priors(self):
        self.assertEqual(run_contract(score_with_frozen_source),
                         {"score_calls": 68, "output_leaf_comparisons": 10200})

    def test_label_pair_brier_identifies_fixed_prediction(self):
        fit = synthetic_fit(0)
        for history in product((0, 1), repeat=4):
            scores = []
            for y in (0, 1):
                sessions = {str(tr): {"treatment": tr, "events": [history+(y,)]} for tr in (0, 1)}
                scores.append(score_with_frozen_source(fit, sessions))
            for model in MODELS:
                b0 = scores[0]["models"][model]["all_original_sessions_equal_Brier"]
                b1 = scores[1]["models"][model]["all_original_sessions_equal_Brier"]
                recovered = (b0-b1+1)/2
                self.assertAlmostEqual(recovered, float(gate.source_probability(fit, model, history+(0,))), delta=1e-15)

    def test_permutation_and_within_session_repetition(self):
        fit = synthetic_fit(0)
        sessions = synthetic_targets()
        before = score_with_frozen_source(fit, sessions)
        changed = dict(reversed(list(sessions.items())))
        for info in changed.values():
            info["events"] = list(reversed(info["events"]))
        changed["ARTIFICIAL_B"]["events"] *= 7
        gate.check_scorer(score_with_frozen_source, fit, changed)
        after = score_with_frozen_source(fit, changed)
        for model in MODELS:
            self.assertAlmostEqual(before["models"][model]["all_original_sessions_equal_Brier"],
                                   after["models"][model]["all_original_sessions_equal_Brier"], delta=1e-15)

    def test_current_label_mixture_quarter_brier_is_rejected(self):
        fit, sessions = synthetic_fit(0), synthetic_targets()
        actual = score_with_frozen_source(fit, sessions)
        for model in actual["models"].values():
            model["all_original_sessions_equal_Brier"] /= 4
        with self.assertRaisesRegex(ValueError, "SCORE_MISMATCH"):
            gate.validate_scores(actual, gate.expected_scores(fit, sessions))

    def test_wrong_log_loss_is_rejected(self):
        fit, sessions = synthetic_fit(0), synthetic_targets()
        actual = score_with_frozen_source(fit, sessions)
        m0 = actual["models"][MODELS[0]]
        m0["all_original_sessions_equal_log_loss"] = m0["all_original_sessions_equal_Brier"]
        with self.assertRaisesRegex(ValueError, "SCORE_MISMATCH"):
            gate.validate_scores(actual, gate.expected_scores(fit, sessions))

    def test_result_requires_complete_field_set(self):
        fit, sessions = synthetic_fit(0), synthetic_targets()
        expected = gate.expected_scores(fit, sessions)
        for change in ("missing", "extra", "missing_model", "missing_treatment"):
            actual = score_with_frozen_source(fit, sessions)
            if change == "missing": del actual["target_labels_used_in_training"]
            elif change == "extra": actual["extra"] = 0
            elif change == "missing_model": del actual["models"][MODELS[1]]
            else: del actual["models"][MODELS[0]]["per_treatment_original_session_equal"]["1"]
            with self.assertRaises(ValueError): gate.validate_scores(actual, expected)

    def test_result_rejects_nonfinite_wrong_numeric_types_and_false_zero(self):
        fit, sessions = synthetic_fit(0), synthetic_targets()
        expected = gate.expected_scores(fit, sessions)
        for bad in (True, 0, math.nan, math.inf, "0.333333"):
            actual = score_with_frozen_source(fit, sessions)
            actual["models"][MODELS[0]]["all_original_sessions_equal_Brier"] = bad
            with self.assertRaises(ValueError): gate.validate_scores(actual, expected)
        for bad in (False, 0.0):
            actual = score_with_frozen_source(fit, sessions)
            actual["target_labels_used_in_training"] = bad
            with self.assertRaises(ValueError): gate.validate_scores(actual, expected)

    def test_paired_sign_counts_are_checked(self):
        fit, sessions = synthetic_fit(0), synthetic_targets()
        actual = score_with_frozen_source(fit, sessions)
        pair = next(iter(actual["paired_differences"].values()))
        pair["sessions_better"] += 1
        with self.assertRaises(ValueError): gate.validate_scores(actual, gate.expected_scores(fit, sessions))

    def test_empty_missing_treatment_and_bad_action_inputs_rejected(self):
        fit = synthetic_fit(0)
        for sessions in ({}, {"A": {"treatment": 0, "events": [(0, 0, 0, 0, 0)]}}):
            with self.assertRaises(ValueError): gate.expected_scores(fit, sessions)
        for bad in (True, 1.0, 2, math.nan):
            sessions = synthetic_targets()
            sessions["ARTIFICIAL_A"]["events"][0] = (bad, 0, 0, 0, 0)
            with self.assertRaises(ValueError): gate.expected_scores(fit, sessions)
        with self.assertRaises(ValueError): gate.check_scorer(None, fit, {})
        with self.assertRaises(ValueError): gate.validate_scores({}, {})

    def test_malformed_source_statistics_rejected(self):
        for counts in ((False, 32), (1, 32.0), (33, 32), (-1, 32)):
            fit = synthetic_fit(0)
            fit["state_counts"][MODELS[1]][(0,)] = counts
            with self.assertRaises(ValueError): gate.expected_scores(fit, synthetic_targets())
        for bad in (True, math.nan, math.inf, 0.0, 1.0):
            fit = synthetic_fit(0); fit["train_only_prevalence"] = bad
            with self.assertRaises(ValueError): gate.expected_scores(fit, synthetic_targets())


if __name__ == "__main__":
    unittest.main()
