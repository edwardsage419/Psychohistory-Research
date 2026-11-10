"""All records here are invented, never human observations."""
import copy
from fractions import Fraction
import importlib
import math
from pathlib import Path
import sys
import unittest

import fit_oracle as gate

ROOT = Path(__file__).resolve().parents[3]
for study in ("R074", "R075"):
    sys.path.insert(0, str(ROOT / "research" / study))

TRAINERS = (
    importlib.import_module("r074_dalbo_external_human_e3"),
    importlib.import_module("r075_coauthor_real_human_e3"),
)


def fictional_sessions(equal_size=False):
    rows = [
        [(1, 1, 1, 1, 1), (0, 0, 0, 0, 0),
         (1, 0, 0, 1, 0), (0, 1, 0, 1, 1)],
        [(0, 0, 0, 0, 0), (1, 0, 1, 0, 1), (1, 1, 0, 1, 0)],
        [(0, 1, 1, 0, 1), (0, 1, 1, 0, 0), (1, 0, 0, 1, 0),
         (1, 1, 1, 1, 1), (0, 0, 1, 1, 0)],
    ]
    if equal_size:
        rows[1].append((0, 0, 1, 0, 0))
        rows[2] = rows[2][:4]
    sessions = {}
    for treatment in ("A", "B"):
        for i, events in enumerate(rows):
            # The second treatment has reversed labels, not copied outcomes.
            events = list(events) if treatment == "A" else [e[:4] + (1-e[4],) for e in events]
            sessions[f"FICTIONAL_{treatment}_{i}"] = {"treatment": treatment, "events": events}
    return sessions


class ExactFitOracleTests(unittest.TestCase):
    def test_empty_trainer_input_cannot_report_vacuous_success(self):
        with self.assertRaisesRegex(ValueError, "ORACLE_EMPTY_SESSIONS"):
            gate.check_trainer(None, None, {})

    def test_corrupt_predictor_is_rejected(self):
        for wrong in (True, 1, math.nan, math.inf, 0.0, 1.0, 0.5):
            with self.subTest(wrong=wrong):
                with self.assertRaisesRegex(ValueError, "PREDICTION_MISMATCH"):
                    gate.check_trainer(TRAINERS[0].fit_other_sessions,
                                       lambda *args: wrong, fictional_sessions())

    def test_hand_calculated_prevalence_and_joint_counts(self):
        oracle = gate.expected_fit(fictional_sessions(), "FICTIONAL_A_0")
        self.assertEqual(oracle["train_only_prevalence"], Fraction(3, 8))
        self.assertEqual(oracle["train_target_count"], 8)
        self.assertEqual(oracle["trained_from_other_sessions_same_treatment"], 2)
        self.assertEqual(oracle["state_counts"]["M1_OWN_LAST"], {(0,): (1, 4), (1,): (2, 4)})
        self.assertEqual(oracle["state_counts"]["M2_OPPONENT_LAST"], {(0,): (1, 4), (1,): (2, 4)})
        self.assertEqual(oracle["state_counts"]["M3_JOINT_LAST"], {
            (0, 0): (0, 2), (1, 0): (1, 2), (1, 1): (1, 2), (0, 1): (1, 2)})
        self.assertEqual(oracle["state_counts"]["M4_JOINT_TWO_LAGS"], {
            (0, 0, 0, 0): (0, 1), (1, 0, 1, 0): (1, 1),
            (1, 1, 0, 1): (0, 1), (0, 1, 1, 0): (1, 2),
            (1, 0, 0, 1): (0, 1), (1, 1, 1, 1): (1, 1), (0, 0, 1, 1): (0, 1)})

    def test_exact_smoothing_and_unseen_state(self):
        oracle = gate.expected_fit(fictional_sessions(), "FICTIONAL_A_0")
        self.assertEqual(gate.probability(oracle, "M1_OWN_LAST", (0, 0, 0, 0, 0)), Fraction(17, 48))
        self.assertEqual(gate.probability(oracle, "M4_JOINT_TWO_LAGS", (1, 1, 0, 0, 0)), Fraction(3, 8))
        self.assertEqual(gate.probability(oracle, "M5_TFT_NOISY", (1, 0, 1, 1, 0)), Fraction(1, 20))
        self.assertEqual(gate.probability(oracle, "M6_WSLS_NOISY", (0, 0, 1, 1, 0)), Fraction(19, 20))

    def test_original_trainers_all_folds_and_states(self):
        for equal_size in (False, True):
            for module in TRAINERS:
                with self.subTest(equal_size=equal_size, module=module.__name__):
                    n = gate.check_trainer(module.fit_other_sessions, module.predict, fictional_sessions(equal_size))
                    self.assertEqual(n, {"folds": 6, "prediction_comparisons": 1344})

    def test_oracle_heldout_and_foreign_treatment_invariance(self):
        sessions = fictional_sessions()
        before = gate.expected_fit(sessions, "FICTIONAL_A_0")
        for name, info in sessions.items():
            if name == "FICTIONAL_A_0" or info["treatment"] == "B":
                info["events"] = [e[:4] + (1-e[4],) for e in info["events"]] * 7
        self.assertEqual(before, gate.expected_fit(sessions, "FICTIONAL_A_0"))

    def test_permutation_invariance(self):
        sessions = fictional_sessions()
        before = gate.expected_fit(sessions, "FICTIONAL_A_0")
        sessions = dict(reversed(list(sessions.items())))
        for info in sessions.values():
            info["events"].reverse()
        self.assertEqual(before, gate.expected_fit(sessions, "FICTIONAL_A_0"))

    def test_repeated_donor_is_detectable_even_when_total_is_preserved(self):
        sessions = fictional_sessions(True)
        oracle = gate.expected_fit(sessions, "FICTIONAL_A_0")
        repeated = copy.deepcopy(sessions)
        repeated["FICTIONAL_A_2"]["events"] = list(repeated["FICTIONAL_A_1"]["events"])
        for module in TRAINERS:
            fitted = module.fit_other_sessions(repeated, "FICTIONAL_A_0")
            self.assertEqual(fitted["train_target_count"], oracle["train_target_count"])
            with self.assertRaisesRegex(ValueError, "FIT_MISMATCH"):
                gate.validate_fit(fitted, oracle)

    def test_corrupt_state_count_is_rejected(self):
        oracle = gate.expected_fit(fictional_sessions(), "FICTIONAL_A_0")
        for module in TRAINERS:
            fitted = module.fit_other_sessions(fictional_sessions(), "FICTIONAL_A_0")
            fitted["state_counts"]["M3_JOINT_LAST"][(0, 0)] = (1, 2)
            with self.assertRaisesRegex(ValueError, "FIT_MISMATCH"):
                gate.validate_fit(fitted, oracle)

    def test_missing_or_extra_fit_fields_are_rejected(self):
        oracle = gate.expected_fit(fictional_sessions(), "FICTIONAL_A_0")
        for field in ("state_counts", "train_target_count"):
            fitted = TRAINERS[0].fit_other_sessions(fictional_sessions(), "FICTIONAL_A_0")
            del fitted[field]
            with self.assertRaises(ValueError):
                gate.validate_fit(fitted, oracle)
        fitted = TRAINERS[0].fit_other_sessions(fictional_sessions(), "FICTIONAL_A_0")
        fitted["unexpected"] = 1
        with self.assertRaises(ValueError):
            gate.validate_fit(fitted, oracle)

    def test_bool_float_and_nonfinite_fit_values_are_rejected(self):
        oracle = gate.expected_fit(fictional_sessions(), "FICTIONAL_A_0")
        for bad in (True, 8.0, math.nan, math.inf):
            fitted = TRAINERS[0].fit_other_sessions(fictional_sessions(), "FICTIONAL_A_0")
            fitted["train_target_count"] = bad
            with self.assertRaises(ValueError):
                gate.validate_fit(fitted, oracle)
        for bad in (math.nan, math.inf, True):
            fitted = TRAINERS[0].fit_other_sessions(fictional_sessions(), "FICTIONAL_A_0")
            fitted["train_only_prevalence"] = bad
            with self.assertRaises(ValueError):
                gate.validate_fit(fitted, oracle)
        fitted = TRAINERS[0].fit_other_sessions(fictional_sessions(), "FICTIONAL_A_0")
        fitted["state_counts"]["M3_JOINT_LAST"][(0, 0)] = (False, 2.0)
        with self.assertRaises(ValueError):
            gate.validate_fit(fitted, oracle)

    def test_invalid_binary_or_missing_fold_is_rejected(self):
        for bad in (True, 1.0, 2, math.nan):
            sessions = fictional_sessions()
            sessions["FICTIONAL_A_1"]["events"][0] = (bad, 0, 0, 0, 0)
            with self.assertRaises(ValueError):
                gate.expected_fit(sessions, "FICTIONAL_A_0")
        with self.assertRaises(ValueError):
            gate.expected_fit(fictional_sessions(), "MISSING")


if __name__ == "__main__":
    unittest.main()
