"""Synthetic program tests only; do not treat as an empirical replay."""
import unittest

from r065_critical_replay import CRITICAL_DAYS, summarize, parse_verified


def fixture(n_subjects=12):
    rows = []
    for participant in range(n_subjects):
        for idx, day in enumerate(CRITICAL_DAYS):
            stake = "high" if idx % 2 == 0 else "low"
            copied = int((idx + participant) % 3 == 0)
            rows.append({"participant_id": str(participant), "stakes": stake,
                         "copied": str(copied), "accurate": str(1-copied),
                         "critical": "1.0", "day": str(day),
                         "comprehension_check_repetitions": "0"})
        rows.append({"participant_id": str(participant), "stakes": "high",
                     "copied": "1", "accurate": "1", "critical": "0",
                     "day": "6", "comprehension_check_repetitions": "0"})
    return rows


class R065Tests(unittest.TestCase):
    def test_valid_fixture(self):
        out = summarize(fixture(), draws=30)
        self.assertEqual(out["participants"], 12)
        self.assertEqual(out["critical_rows"], 96)
        self.assertEqual(out["raw_rows"], 108)
        self.assertEqual(out["critical_stakes"]["high"]["n"], 48)
        self.assertEqual(out["participant_bootstrap"]["draws"], 30)

    def test_seed_reproducible(self):
        x = summarize(fixture(), draws=30)
        y = summarize(fixture(), draws=30)
        self.assertEqual(x["participant_bootstrap"], y["participant_bootstrap"])

    def test_bad_source_digest_rejected(self):
        with self.assertRaisesRegex(ValueError, "SHA1"):
            parse_verified(b"participant_id,critical\n1,1\n")

    def test_missing_day_rejected(self):
        a = fixture()
        a[0]["critical"] = "0"
        with self.assertRaisesRegex(ValueError, "schedule"):
            summarize(a, draws=4)

    def test_bad_stake_balance_rejected(self):
        a = fixture()
        a[0]["stakes"] = "low"
        with self.assertRaisesRegex(ValueError, "4/4"):
            summarize(a, draws=4)

    def test_diagnostic_copy_accuracy_rejected(self):
        a = fixture()
        a[0]["accurate"] = a[0]["copied"]
        with self.assertRaisesRegex(ValueError, "complement"):
            summarize(a, draws=4)

    def test_invalid_schema_rejected(self):
        a = fixture()
        a[0]["critical"] = "2"
        with self.assertRaisesRegex(ValueError, "Invalid"):
            summarize(a, draws=4)

    def test_author_exclusion_applies_before_critical_filter(self):
        a = fixture()
        for row in a:
            if row["participant_id"] == "0":
                row["comprehension_check_repetitions"] = "3"
        out = summarize(a, draws=4)
        self.assertEqual(out["exclusion"]["comprehension"], 1)
        self.assertEqual(out["participants"], 11)

    def test_fewer_than_minimum_fails(self):
        with self.assertRaisesRegex(ValueError, "Insufficient"):
            summarize(fixture(4), draws=4)


if __name__ == "__main__":
    unittest.main()
