"""Synthetic isolated proof: time-negative source rows are not valid temporal facts."""
import hashlib
import unittest
from unittest.mock import patch
import r069_hetrec_source_rev002 as v2
from test_r069_hetrec_lastfm_source_audit import zip_data


TAGS=(b"userID\tartistID\ttagID\ttimestamp\n"
      b"1\t5\t1\t1000\n"
      b"2\t5\t2\t2000\n"
      b"3\t5\t3\t2000\n"
      b"3\t5\t3\t-1\n"
      b"2\t6\t1\t1000\n")


def synthetic_run(data):
    return v2.evaluate_zip(data,
        checksum=hashlib.sha256(data).hexdigest(),
        md5=hashlib.md5(data).hexdigest(),
        expected_friend=4,expected_tag=5,invalid=1)


class Rev002Tests(unittest.TestCase):
    def test_one_invalid_timestamp_filtered_only(self):
        d=zip_data(tags=TAGS)
        result=synthetic_run(d)
        self.assertEqual(result["user_tag_events"]["original_negative_timestamp_rows"],1)
        self.assertEqual(result["user_tag_events"]["timestamp_order_valid_rows"],4)
        self.assertEqual(result["user_tag_events"]["first_tag_pairs_with_strictly_earlier_friend_tag_same_artist"],1)
        self.assertEqual(result["status"],
                         "E2_SOURCE_AND_RETROSPECTIVE_EXPOSURE_PROXY_PASS_BOUNDED")

    def test_negative_timestamp_unexpected_count_fails(self):
        d=zip_data(tags=TAGS)
        with self.assertRaisesRegex(ValueError,"UNIVERSE_DRIFT"):
            v2.evaluate_zip(d,hashlib.sha256(d).hexdigest(),
                 hashlib.md5(d).hexdigest(),4,5,2)

    def test_zero_timestamp_not_silently_filtered(self):
        d=TAGS.replace(b"\t-1\n",b"\t0\n")
        with self.assertRaisesRegex(ValueError,"ZERO_TIMESTAMP"):
            v2.tagged_valid_rows(d,5,1)

    def test_negative_identifiers_never_filtered(self):
        d=TAGS.replace(b"3\t5\t3\t-1",b"-3\t5\t3\t-1")
        with self.assertRaisesRegex(ValueError,"PERSON_ARTIST"):
            v2.tagged_valid_rows(d,5,1)

    def test_original_ZIP_SHA_change_rejected_before_rows(self):
        d=zip_data(tags=TAGS)
        with self.assertRaisesRegex(ValueError,"SOURCE_ZIP_SHA256_DRIFT"):
            v2.evaluate_zip(d,checksum="0"*64,md5=hashlib.md5(d).hexdigest(),
                            expected_friend=4,expected_tag=5,invalid=1)

    def test_same_time_friend_is_not_prior_in_corrected_input(self):
        d=TAGS.replace(b"1\t5\t1\t1000",b"1\t5\t1\t2000")
        events,_=v2.tagged_valid_rows(d,5,1)
        graph={1:{2},2:{1,3},3:{2}}
        res=v2.proxy_early_friend_tag(events,graph)
        self.assertEqual(res["first_tag_pairs_with_strictly_earlier_friend_tag_same_artist"],0)

    def test_prior_failed_run_remains_cited(self):
        d=zip_data(tags=TAGS)
        res=synthetic_run(d)
        self.assertEqual(res["initial_fail_workflow"],38874370089)
        self.assertEqual(res["true_independent_cascade_or_threshold_inference"],"NOT_ESTABLISHED")
        self.assertFalse(res["individual_source_events_or_ids_exported"])


if __name__=="__main__":
    unittest.main()
