"""R065 Phase D synthetic tests only; real CSV requires strict Git SHA1."""
import math
import unittest
from r065_phase_d_loso import (
    SOURCE_BLOB, analyze, cell_name, loo_cell_probability, parse_source,
)


def fixture(count=12):
    rows = []
    for person in range(count):
        for i, day in enumerate((4, 21, 38, 55, 72, 89, 106, 123)):
            high = (i % 2 == 0) == (person % 2 == 0)
            copied = (i + person) % 3 == 0
            rows.append({
                "participant_id": str(person),
                "stakes": "high" if high else "low",
                "copied": str(int(copied)), "accurate": "1",
                "comprehension_check_repetitions": "0",
                "critical": "1", "day": str(day),
            })
    return rows


class PhaseDTests(unittest.TestCase):
    def test_blob_gate_rejects_constructed_data(self):
        with self.assertRaisesRegex(ValueError, "Git blob mismatch"):
            parse_source(b"participant_id,critical\nA,1\n")

    def test_whole_subject_out_cell(self):
        self.assertAlmostEqual(loo_cell_probability((16, 8), (8, 8)), 0.25)

    def test_one_row_removal_would_leak(self):
        correct = loo_cell_probability((16, 8), (8, 8))
        wrong = loo_cell_probability((16, 8), (1, 1))
        self.assertNotAlmostEqual(correct, wrong)

    def test_training_rejects_impossible_counts(self):
        with self.assertRaisesRegex(ValueError, "Inconsistent"):
            loo_cell_probability((8, 2), (9, 1))

    def test_cells_are_distinct(self):
        x = {"stake":"high", "block":3, "copy":1}
        self.assertEqual([cell_name(m,x) for m in ("M0","M1","M2","M3")],
                         ["*", "high", "3", "3|high"])

    def test_same_seed_reproduces_bootstrap(self):
        a = analyze(fixture(), draws=25)
        b = analyze(fixture(), draws=25)
        self.assertEqual(a["bootstrap_95"], b["bootstrap_95"])
        self.assertEqual(a["diagnostic_rows"], 96)
        self.assertEqual(a["eligible_participants"], 12)

    def test_no_held_out_outcome_exposed(self):
        # With exactly two people and opposite labels, each test person's
        # pooled training probability must reflect ONLY the other person.
        a = fixture(2)
        for row in a:
            row["copied"] = "1" if row["participant_id"] == "0" else "0"
        report = analyze(a, draws=3, min_subjects=2)
        self.assertAlmostEqual(report["models"]["M0"]["logloss"],
                               -math.log(0.25), places=10)

    def test_bad_critical_day_fails(self):
        a = fixture()
        a[0]["day"] = "999"
        with self.assertRaisesRegex(ValueError, "diagnostic-day"):
            analyze(a, draws=2)

    def test_bad_stakes_schedule_fails(self):
        a = fixture()
        a[0]["stakes"] = "low"
        with self.assertRaisesRegex(ValueError, "stake balance"):
            analyze(a, draws=2)

    def test_all_trial_exclusions(self):
        a = fixture()
        for row in a:
            if row["participant_id"] == "0":
                row["comprehension_check_repetitions"] = "3"
        report = analyze(a, draws=2)
        self.assertEqual(report["excluded"]["union"], 1)
        self.assertEqual(report["eligible_participants"], 11)


if __name__ == "__main__":
    unittest.main()
