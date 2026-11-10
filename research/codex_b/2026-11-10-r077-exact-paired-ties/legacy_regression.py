"""Intentionally fails on original R077, exercising a new exact-tie regression.

Kept separate from test discovery. replay.py requires its assertion failure,
preserving the historical defect rather than claiming the original is repaired.
All source and target rows here are fictional.
"""
from pathlib import Path
import sys
import unittest

from case import legacy_fit, target_cases

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT/"research/R077"))
from r077_fourth_real_human_source_only_e3 import score_with_frozen_source


class OriginalExactTieRegression(unittest.TestCase):
    def test_same_exact_tie_for_every_record_permutation(self):
        for positions, sessions in target_cases():
            with self.subTest(positive_positions=positions):
                result = score_with_frozen_source(legacy_fit(), sessions)
                pair = result["paired_differences"]["M3_JOINT_LAST_VS_M1_OWN_LAST"]
                self.assertEqual((pair["sessions_better"], pair["sessions_equal"], pair["sessions_worse"]),
                                 (0, 2, 0))


if __name__ == "__main__": unittest.main(verbosity=2)
