"""Constructed examples only: AST extraction, consistency, fail-closed policy."""
import tempfile
import unittest
from pathlib import Path
from r065_reset_alignment import (
    AUTHOR_BLOB, KNOWN_RESETS, audit_alignment, git_blob_sha1,
    inspect_source, inspect_verified_file, fresh_state_two_action_probabilities,
)


def fake_objectives(reset="[23, 45, 67, 89, 111]"):
    return "\n\n".join(
        f"def model_{k}_objective(params, data):\n"
        f"    for _, row in data.iterrows():\n"
        f"        if row ['day'] in {reset}:\n"
        f"            value = 0\n"
        f"    return value\n"
        for k in range(1, 8)
    )


class ResetAlignmentTests(unittest.TestCase):
    def test_extract_all_guards(self):
        models = inspect_source(fake_objectives())
        self.assertEqual(models, {k: KNOWN_RESETS for k in range(1, 8)})

    def test_off_block_source_resets(self):
        a = audit_alignment(inspect_source(fake_objectives()))
        self.assertEqual(a["observed_design"]["internal_block_starts"], [18, 35, 52, 69, 86, 103, 120])
        for m in a["models"].values():
            self.assertEqual(m["matched_block_start_days"], [])
            self.assertEqual(m["unexpected_resets"], list(KNOWN_RESETS))
            self.assertEqual(len(m["unreset_block_starts"]), 7)
            self.assertEqual(m["critical_days_reset_by_source"], [89])

    def test_cannot_assume_guards_without_source(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            inspect_source("def model_1_objective(params, data): pass")

    def test_unreadable_dynamic_guard_rejected(self):
        with self.assertRaisesRegex(ValueError, "exactly one"):
            inspect_source(fake_objectives(reset="list(range(23, 112, 22))"))

    def test_git_blob_formula(self):
        self.assertEqual(git_blob_sha1(b"test content\n"), "d670460b4b4aece5915caf5c68d12f560a9fe3e4")

    def test_tampered_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "objectives.py"
            p.write_text(fake_objectives(), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "SHA1 mismatch"):
                inspect_verified_file(p)

    def test_distinct_corrected_schedule_has_all_matches(self):
        expected = "[18, 35, 52, 69, 86, 103, 120]"
        a = audit_alignment(inspect_source(fake_objectives(reset=expected)))
        for m in a["models"].values():
            self.assertEqual(m["unexpected_resets"], [])
            self.assertEqual(m["unreset_block_starts"], [])
            self.assertEqual(len(m["matched_block_start_days"]), 7)

    def test_day89_fresh_state_uniform_for_seven_model_families(self):
        matrix = ((.8, .2, 0.), (0., .8, .2), (.2, 0., .8))
        for available in ((0, 1), (0, 2), (1, 2)):
            for beta in (0., 1., 30.):
                for weight in (0., .37, 1.):
                    q = fresh_state_two_action_probabilities(matrix, available, beta, weight)
                    for family in ("emulation", "imitation", "copy_last", "mixture"):
                        self.assertEqual(q[family], [0.5, 0.5])

    def test_uniform_claim_requires_normalized_source_transitions(self):
        bad = ((.9, .2, 0.), (0., .8, .2), (.2, 0., .8))
        with self.assertRaisesRegex(ValueError, "normalized"):
            fresh_state_two_action_probabilities(bad)

    def test_design_rejects_invalid_parameters(self):
        with self.assertRaises(ValueError):
            audit_alignment(inspect_source(fake_objectives()), blocks=1)


if __name__ == "__main__":
    unittest.main()
