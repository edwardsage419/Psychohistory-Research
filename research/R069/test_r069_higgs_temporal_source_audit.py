"""Synthetic-only SNAP Higgs source, temporal precedence and graph privacy gates."""
import gzip
import io
import unittest
import r069_higgs_temporal_source_audit as m


def compress(lines):
    return gzip.compress(("\n".join(lines)+"\n").encode("utf-8"),mtime=0)


ACT=[
    "# SRC ACTIVITY A B UNIX_TIME ACTION",
    "0 1 1341100801 RT",
    "1 2 1341100801 RT",
    "3 1 1341100802 MT",
    "1 4 1341100803 RT",
    "2 1 1341100802 RT",
]
NET=["# a b weight","0 1 1","1 2 2","1 4 1","2 1 1"]


class SNAPHiggsSourceTests(unittest.TestCase):
    def test_timed_activity_types_and_zero_id_valid(self):
        x=m.audit_activity(compress(ACT))
        self.assertEqual(x["interaction_rows"],5)
        self.assertEqual(x["activity_types"],{"RT":4,"MT":1,"RE":0})
        self.assertEqual(x["rows_outside_official_2012_07_01_to_07_07_week"],0)
        self.assertFalse(x["original_user_ids_redistributed"])

    def test_strictly_earlier_activity_but_not_same_second(self):
        # Actor B at t=first time has NOT preceded the other actor.
        x=m.audit_activity(compress(ACT))
        self.assertEqual(x["RT_event_rows_with_target_prior_RT"],1)
        self.assertEqual(x["RT_event_rows_with_target_prior_any_activity"],1)

    def test_input_order_does_not_change_earliest_temporal_claim(self):
        x=m.audit_activity(compress(ACT))
        y=m.audit_activity(compress(ACT[:1]+list(reversed(ACT[1:]))))
        self.assertEqual(x,y)

    def test_timestamp_tie_is_not_prior_appearance(self):
        x=m.audit_activity(compress(["0 1 1341100801 RT","1 0 1341100801 RT"]))
        self.assertEqual(x["RT_event_rows_with_target_prior_RT"],0)

    def test_activity_directed_semantics_not_inverse_adoption(self):
        x=m.audit({"activity":compress(ACT),
                   "retweet_network":compress(NET)})
        self.assertIn("actor A retweets B",x["retweet_direction"])
        self.assertFalse(x["external_follow_network_loaded"])
        self.assertEqual(x["real_causal_threshold_or_IC_parameters"],"NOT_IDENTIFIED")

    def test_network_positive_weights(self):
        x=m.audit_aggregated_retweet_graph(compress(NET))
        self.assertEqual(x["retweet_network_edge_rows"],4)
        self.assertEqual(x["weight_sum"],5)
        self.assertEqual(x["unique_directed_weighted_edge_pairs"],4)

    def test_duplicate_aggregated_edge_kept_as_bad_measurement(self):
        x=m.audit_aggregated_retweet_graph(compress(NET+["0 1 1"]))
        self.assertEqual(x["duplicate_directed_edge_rows"],1)

    def test_unknown_event_type_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"INTERACTION_TYPE"):
            m.audit_activity(compress(["1 2 1341100801 LIKE"]))

    def test_negative_user_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"USER_ID"):
            m.audit_activity(compress(["-1 2 1341100801 RT"]))

    def test_invalid_timestamp_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"TIME"):
            m.audit_activity(compress(["0 2 0 RT"]))

    def test_bad_event_column_count_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"FOUR_FIELDS"):
            m.audit_activity(compress(["0 2 1341100801"]))

    def test_gzip_crc_failure_not_silently_parsed(self):
        data=bytearray(compress(["0 2 1341100801 RT"]))
        data[-8]^=2
        with self.assertRaises((OSError,EOFError,gzip.BadGzipFile)):
            m.audit_activity(bytes(data))

    def test_large_source_line_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"ROW_TOO_LONG"):
            m.audit_activity(compress(["0 "*250+"RT"]))

    def test_source_which_is_not_gzip_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"NOT_GZIP"):
            m.audit_activity(b"0 1 1341100801 RT")

    def test_negative_network_weight_fails_closed(self):
        with self.assertRaisesRegex(ValueError,"WEIGHT"):
            m.audit_aggregated_retweet_graph(compress(["1 2 -3"]))

    def test_no_source_event_fail_closed(self):
        with self.assertRaisesRegex(ValueError,"NO_SOURCE_RETWEETS"):
            m.audit_activity(compress(["# only comment"]))

    def test_missing_original_file_rejected(self):
        with self.assertRaisesRegex(ValueError,"EXACT_TWO"):
            m.audit({"activity":compress(ACT)})

    def test_discrete_out_of_week_count_without_filter(self):
        out=m.audit_activity(compress(["0 1 1341100801 RT","2 1 1341000000 RE"]))
        self.assertEqual(out["interaction_rows"],2)
        self.assertEqual(out["rows_outside_official_2012_07_01_to_07_07_week"],1)


if __name__=="__main__":
    unittest.main()
