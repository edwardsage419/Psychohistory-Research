"""Exact same Brier metric, fictional records only; no tolerance-based tie rule."""
from fractions import Fraction as F
import math
import unittest

import exact_pair as m
from case import source_events, legacy_fit, rational_probabilities, target_cases, exact_sessions, integer_witness


class ExactPairTests(unittest.TestCase):
    def test_hand_pair_risks_and_integer_witness(self):
        _, sessions = next(target_cases())
        result = m.summarize(exact_sessions(sessions))
        self.assertEqual(result["candidate_macro_Brier"], F(1, 4))
        self.assertEqual(result["reference_macro_Brier"], F(1, 4))
        self.assertEqual(result["paired"]["Brier_delta_all_original_sessions_equal"], F(0))
        proof = integer_witness([1, 1, 1, 0, 0, 0, 0])
        self.assertEqual(proof, {"integer_squared_sums": {"candidate": 343, "reference": 343},
                                 "denominator": 1372, "risks": {"candidate": "1/4", "reference": "1/4"}})

    def test_all_35_permutations_are_exact_ties(self):
        seen = 0
        for _, sessions in target_cases():
            result = m.summarize(exact_sessions(sessions))
            pair = result["paired"]
            self.assertEqual((pair["sessions_better"], pair["sessions_equal"], pair["sessions_worse"]), (0, 2, 0))
            self.assertEqual(integer_witness([e[4] for e in next(iter(sessions.values()))["events"]])["risks"],
                             {"candidate": "1/4", "reference": "1/4"})
            seen += 1
        self.assertEqual(seen, 35)

    def test_source_fixture_is_coherent_and_frozen_probabilities_match_hand(self):
        events, fit = source_events(), legacy_fit()
        self.assertEqual((len(events), sum(e[4] for e in events)), (32, 16))
        for model, mask in (("M1_OWN_LAST", (0,)), ("M2_OPPONENT_LAST", (1,)),
                            ("M3_JOINT_LAST", (0, 1)), ("M4_JOINT_TWO_LAGS", (0, 1, 2, 3))):
            for state, counts in fit["state_counts"][model].items():
                selected = [e for e in events if tuple(e[i] for i in mask) == state]
                self.assertEqual(counts, (sum(e[4] for e in selected), len(selected)))
        self.assertEqual(rational_probabilities(), (F(5, 14), F(1, 2)))

    def test_genuine_tiny_nonzero_delta_keeps_its_sign(self):
        denominator = 2**60
        records = [(0, F(1, 2)+F(1, denominator), F(1, 2))]
        result = m.session_risks(records)
        self.assertEqual(result["delta"], F(denominator+1, denominator**2))
        self.assertEqual(result["direction"], "worse")
        self.assertEqual(float(records[0][1]), float(records[0][2]))

    def test_equal_session_weight_differs_from_row_weight(self):
        sessions = {
            "A": {"treatment": 0, "records": [(0, F(1, 4), F(1, 2))]*3},
            "B": {"treatment": 1, "records": [(1, F(1, 4), F(1, 2))]},
        }
        result = m.summarize(sessions)
        self.assertEqual(result["candidate_macro_Brier"], F(5, 16))
        self.assertEqual(result["paired"]["Brier_delta_all_original_sessions_equal"], F(1, 16))
        self.assertEqual(m.session_risks(sessions["A"]["records"]+sessions["B"]["records"])["delta"], F(-1, 16))

    def test_within_session_duplication_does_not_change_macro_votes(self):
        _, sessions = next(target_cases())
        exact = exact_sessions(sessions)
        before = m.summarize(exact)
        exact["ARTIFICIAL_SESSION_0"]["records"] *= 9
        self.assertEqual(before, m.summarize(exact))

    def test_empty_inputs_fail_closed(self):
        with self.assertRaises(ValueError): m.session_risks([])
        with self.assertRaises(ValueError): m.summarize({})

    def test_nonrational_probabilities_and_invalid_outcomes_rejected(self):
        for bad in (.5, True, math.nan, math.inf, "1/2", 1):
            with self.assertRaises(ValueError): m.session_risks([(0, bad, F(1, 2))])
        for bad in (True, 0.0, 2, math.nan):
            with self.assertRaises(ValueError): m.session_risks([(bad, F(1, 2), F(1, 2))])
        for p in (F(0), F(1), F(-1, 2), F(3, 2)):
            with self.assertRaises(ValueError): m.session_risks([(0, p, F(1, 2))])

    def test_session_schema_and_treatment_types_rejected(self):
        for bad in (False, 0.0, 2, None):
            with self.assertRaises(ValueError):
                m.summarize({"A": {"treatment": bad, "records": [(0, F(1, 2), F(1, 2))]}})
        with self.assertRaises(ValueError): m.summarize({"A": {"records": []}})

    def test_legacy_false_improvement_is_rejected_despite_tiny_delta(self):
        _, sessions = next(target_cases())
        exact = m.summarize(exact_sessions(sessions))["paired"]
        legacy = m.as_float_pair(exact)
        m.validate_legacy_pair(legacy, exact)
        legacy["sessions_better"] = 2; legacy["sessions_equal"] = 0
        legacy["Brier_delta_all_original_sessions_equal"] = -2.7755575615628914e-17
        with self.assertRaisesRegex(ValueError, "PAIRED_DIRECTION_MISMATCH"):
            m.validate_legacy_pair(legacy, exact)

    def test_legacy_field_counts_and_nonfinite_numbers_rejected(self):
        _, sessions = next(target_cases())
        exact = m.summarize(exact_sessions(sessions))["paired"]
        for mode in ("missing", "extra", "bool", "nan"):
            actual = m.as_float_pair(exact)
            if mode == "missing": del actual["sessions_equal"]
            elif mode == "extra": actual["extra"] = 0
            elif mode == "bool": actual["sessions_better"] = False
            else: actual["Brier_delta_all_original_sessions_equal"] = math.nan
            with self.assertRaises(ValueError): m.validate_legacy_pair(actual, exact)

    def test_true_better_and_worse_counts(self):
        result = m.summarize({
            "A": {"treatment": 0, "records": [(0, F(1, 4), F(1, 2))]},
            "B": {"treatment": 1, "records": [(1, F(1, 4), F(1, 2))]},
        })
        pair = result["paired"]
        self.assertEqual((pair["sessions_better"], pair["sessions_equal"], pair["sessions_worse"]), (1, 0, 1))


if __name__ == "__main__": unittest.main()
