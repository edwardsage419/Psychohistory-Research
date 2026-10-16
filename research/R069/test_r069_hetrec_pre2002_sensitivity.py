import unittest
from r069_hetrec_pre2002_sensitivity import sensitivity, CUTOFF_UTC_MILLISECONDS

T=CUTOFF_UTC_MILLISECONDS

class TimestampSensitivityTests(unittest.TestCase):
    def test_synthetic_pre2002_row_not_mistaken_for_real_peer_exposure(self):
        events=[(1,5,1,T-10),(2,5,1,T+10),(3,5,1,T+20)]
        graph={1:{2},2:{1,3},3:{2}}
        z=sensitivity(events,graph)
        self.assertEqual(z["positive_timestamp_tag_event_rows_before_2002"],1)
        self.assertEqual(z["first_observed_user_artist_pairs_before_2002"],1)
        self.assertEqual(z["rev002_all_positive_source_proxy"]["with_strictly_prior_snapshot_friend_tag"],2)
        self.assertEqual(z["exclusion_sensitivity_proxy"]["with_strictly_prior_snapshot_friend_tag"],1)
        self.assertFalse(z["before_2002_exclusion_applied_to_original_source"])

    def test_no_anomaly_yields_equal_proxy_counts(self):
        events=[(1,5,1,T+1),(2,5,1,T+2)]
        graph={1:{2},2:{1}}
        z=sensitivity(events,graph)
        self.assertEqual(z["positive_timestamp_tag_event_rows_before_2002"],0)
        self.assertEqual(z["rev002_all_positive_source_proxy"],
                         z["exclusion_sensitivity_proxy"])

    def test_equal_timestamp_not_a_prior_event(self):
        events=[(1,5,1,T+1),(2,5,1,T+1)]
        graph={1:{2},2:{1}}
        z=sensitivity(events,graph)
        self.assertEqual(z["exclusion_sensitivity_proxy"]["with_strictly_prior_snapshot_friend_tag"],0)

    def test_source_rows_outside_cutoff_remain_in_source(self):
        events=[(1,6,1,T-1),(1,6,2,T+20)]
        z=sensitivity(events,{1:set()})
        self.assertEqual(z["valid_positive_original_tag_event_rows"],2)
        self.assertEqual(z["sensitivity_tag_event_rows_at_or_after_2002"],1)

    def test_cutoff_must_be_valid_integer(self):
        with self.assertRaises(ValueError):
            sensitivity([],{},cutoff=-1)

    def test_noncausal_boundary_is_explicit(self):
        z=sensitivity([(1,5,1,T+1)],{1:set()})
        self.assertEqual(z["causal_adoption_or_exposure_result"],"NONE")

if __name__=="__main__":
    unittest.main()
