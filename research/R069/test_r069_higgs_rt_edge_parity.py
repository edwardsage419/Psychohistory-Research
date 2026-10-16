"""Synthetic-only original Higgs RT event vs aggregated directed edge invariants."""
import gzip
import unittest
from unittest.mock import patch
import r069_higgs_rt_edge_parity as m
from r069_higgs_temporal_source_audit import TYPES


def gz(lines):return gzip.compress(("\n".join(lines)+"\n").encode(),mtime=0)
def pair(a,b):
    return m.edge_multisets(gz(a),gz(b))


class RTParityTests(unittest.TestCase):
    def test_exact_original_direction_aggregation(self):
        d=pair(["0 1 1341100800 RT","0 1 1341100801 RT",
                "1 2 1341100802 RT","3 1 1341100803 MT"],
               ["0 1 2","1 2 1"])
        self.assertEqual(d["status"],"DIRECTIONAL_RT_MULTISET_EXACT_PASS")
        self.assertEqual(d["activity_RTs"],3)
        self.assertEqual(d["activity_MT_events_excluded"],1)
        self.assertFalse(d["parity_is_independent_second_human_dataset"])

    def test_one_weight_difference_failed(self):
        d=pair(["0 1 1341100800 RT","0 1 1341100801 RT"],["0 1 1"])
        self.assertEqual(d["common_directed_pairs_weight_mismatches"],1)
        self.assertEqual(d["status"],"RT_MULTISET_PARITY_MISMATCH")

    def test_swapped_direction_failed(self):
        d=pair(["0 1 1341100800 RT"],["1 0 1"])
        self.assertEqual(d["unique_pairs_only_in_activity"],1)
        self.assertEqual(d["unique_pairs_only_in_aggregate"],1)

    def test_reverse_reference_is_not_default(self):
        d=pair(["0 1 1341100800 RT"],["0 1 1"])
        self.assertEqual(d["reversed_direction_symmetric_difference_pairs"],2)

    def test_RT_duplicates_correctly_counted(self):
        d=pair(["0 1 1341100800 RT","0 1 1341100802 RT","0 1 1341100803 RT"],["0 1 3"])
        self.assertEqual(d["activity_unique_directed_RT_pairs"],1)
        self.assertEqual(d["status"],"DIRECTIONAL_RT_MULTISET_EXACT_PASS")

    def test_reply_and_mention_not_in_RT_edges(self):
        d=pair(["0 1 1341100800 RT","0 2 1341100801 MT","1 3 1341100802 RE"],["0 1 1"])
        self.assertEqual(d["activity_MT_events_excluded"],1)
        self.assertEqual(d["activity_RE_events_excluded"],1)
        self.assertEqual(d["status"],"DIRECTIONAL_RT_MULTISET_EXACT_PASS")

    def test_duplicated_aggregate_row_never_accepted(self):
        d=pair(["0 1 1341100800 RT","0 1 1341100801 RT"],["0 1 1","0 1 1"])
        self.assertEqual(d["aggregate_duplicate_directed_edges"],1)
        self.assertEqual(d["status"],"RT_MULTISET_PARITY_MISMATCH")

    def test_invalid_aggregate_weight_rejected(self):
        with self.assertRaises(ValueError):
            pair(["0 1 1341100800 RT"],["0 1 0"])

    def test_source_hash_mismatch_rejected(self):
        with self.assertRaisesRegex(ValueError,"SHA_MISMATCH"):
            m.check_source("activity",gz(["0 1 1341100800 RT"]))

    def test_exact_two_source_files_required(self):
        with self.assertRaisesRegex(ValueError,"EXACT_TWO"):
            m.evaluate({"activity":gz(["0 1 1341100800 RT"])})

    def test_missing_RT_fails(self):
        d=pair(["0 2 1341100801 MT"],["0 2 1"])
        self.assertEqual(d["status"],"RT_MULTISET_PARITY_MISMATCH")

    def test_invalid_gzip_not_forgiven(self):
        with self.assertRaises(ValueError):
            m.edge_multisets(b"plain",gz(["0 1 1"]))

    def test_no_edge_ids_in_result(self):
        d=pair(["654321 999999 1341100800 RT"],["654321 999999 1"])
        self.assertNotIn("654321",str(d))
        self.assertNotIn("999999",str(d))
        self.assertFalse(d["individual_edge_rows_or_ids_exported"])

if __name__=="__main__":
    unittest.main()
