"""Synthetic-data test suite. These tests do not replace raw-CSV replay."""
import unittest
from r065_order_audit import order_audit


def fixture(n=12):
    data = []
    for p in range(n):
        high_first = p % 2 == 0
        for i, day in enumerate((4, 21, 38, 55, 72, 89, 106, 123)):
            stake = "high" if (i % 2 == 0) == high_first else "low"
            copy = int(i < 2)
            data.append({"participant_id": str(p), "day": str(day),
                         "stakes": stake, "copied": str(copy),
                         "accurate": "1", "critical": "1",
                         "counterbalance": str(int(high_first)),
                         "comprehension_check_repetitions": "0"})
    return data


class OrderAuditTests(unittest.TestCase):
    def test_known_decline_and_balanced_patterns(self):
        r = order_audit(fixture(), draws=20)
        self.assertEqual(r["n"], 12)
        self.assertEqual(r["sequence_counts"], {"HLHLHLHL": 6, "LHLHLHLH": 6})
        self.assertEqual(r["observed"]["early_minus_late"], 1)
        self.assertEqual(r["critical_copying_by_block"], [1, 1, 0, 0, 0, 0, 0, 0])

    def test_deterministic(self):
        x = order_audit(fixture(), draws=20)
        y = order_audit(fixture(), draws=20)
        self.assertEqual(x["bootstrap"], y["bootstrap"])

    def test_wrong_counterbalance_rejected(self):
        v = fixture()
        v[0]["counterbalance"] = "0"
        with self.assertRaisesRegex(ValueError, "Counterbalance mismatch"):
            order_audit(v, draws=1)

    def test_non_alternating_stakes_rejected(self):
        v = fixture()
        v[0]["stakes"] = "low"
        with self.assertRaisesRegex(ValueError, "alternate"):
            order_audit(v, draws=1)

    def test_bad_day_rejected(self):
        v = fixture()
        v[0]["day"] = "999"
        with self.assertRaisesRegex(ValueError, "incomplete"):
            order_audit(v, draws=1)

    def test_full_history_exclusion_before_critical(self):
        v = fixture()
        for row in v:
            if row["participant_id"] == "0":
                row["comprehension_check_repetitions"] = "3"
        r = order_audit(v, draws=1)
        self.assertEqual(r["n"], 11)


if __name__ == "__main__":
    unittest.main()
