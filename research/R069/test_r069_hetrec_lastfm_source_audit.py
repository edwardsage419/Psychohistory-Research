"""R069 synthetic tests only: source corruption, tie ordering, proxy interpretation."""
import io
import hashlib
import unittest
import zipfile
from unittest.mock import patch
import r069_hetrec_lastfm_source_audit as m


FRIENDS=b"userID\tfriendID\n1\t2\n2\t1\n2\t3\n3\t2\n"
TAGS=(b"userID\tartistID\ttagID\ttimestamp\n"
      b"1\t5\t1\t1000\n"
      b"2\t5\t2\t2000\n"
      b"3\t5\t3\t2000\n"
      b"3\t5\t3\t3000\n"
      b"2\t6\t1\t1000\n")
README=b"Non-commercial synthetic research data only\n"


def zip_data(friends=FRIENDS,tags=TAGS,readme=README,member="../../danger" if False else None):
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w",compression=zipfile.ZIP_DEFLATED) as z:
        if member:
            z.writestr(member,friends)
        else:
            z.writestr("sample/readme.txt",readme)
            z.writestr("sample/user_friends.dat",friends)
            z.writestr("sample/user_taggedartists-timestamps.dat",tags)
    return buf.getvalue()


def run(raw):
    return m.audit_raw_zip(raw,hashlib.md5(raw).hexdigest(),
                            expected_counts={"friends":4,"tag_events":5})


class SourceTests(unittest.TestCase):
    def test_positive_source_and_precursor_counts(self):
        x=run(zip_data())
        self.assertEqual(x["status"],"E2_SOURCE_AND_RETROSPECTIVE_EXPOSURE_PROXY_PASS")
        self.assertEqual(x["source_tables"]["user_friends.dat"]["reciprocal_pairs_undirected"],2)
        y=x["source_tables"]["user_taggedartists-timestamps.dat"]
        self.assertEqual(y["unique_first_tag_user_artist_pairs"],4)
        self.assertEqual(y["first_tag_pairs_with_strictly_earlier_friend_tag_same_artist"],1)
        self.assertEqual(y["tag_events_after_first_same_artist_repetition"],1)
        self.assertFalse(x["causal_threshold_or_IC_fit_performed"])

    def test_late_friend_at_equal_timestamp_cannot_count(self):
        neighbors={1:{2},2:{1}}
        result=m.proxy_early_friend_tag([(1,5,1,2000),(2,5,2,2000)],neighbors)
        self.assertEqual(result["first_tag_pairs_with_strictly_earlier_friend_tag_same_artist"],0)

    def test_input_order_does_not_change_retrospective_peer_precedent(self):
        a=[(1,5,1,3000),(2,5,1,1000),(1,5,2,4000)]
        graph={1:{2},2:{1}}
        x=m.proxy_early_friend_tag(a,graph)
        y=m.proxy_early_friend_tag(list(reversed(a)),graph)
        self.assertEqual(x,y)
        self.assertEqual(x["first_tag_pairs_with_strictly_earlier_friend_tag_same_artist"],1)

    def test_source_md5_bitflip_fail_closed(self):
        a=zip_data()
        with self.assertRaisesRegex(ValueError,"MD5"):
            m.safe_archive(a+b"x",hashlib.md5(a).hexdigest())

    def test_zip_traversal_rejected(self):
        a=zip_data(member="../user_friends.dat")
        with self.assertRaisesRegex(ValueError,"MEMBER_PATH"):
            m.safe_archive(a,hashlib.md5(a).hexdigest())

    def test_source_requires_all_files(self):
        a=zip_data(member="only/user_friends.dat")
        with self.assertRaises(ValueError):
            m.safe_archive(a,hashlib.md5(a).hexdigest())

    def test_tsv_field_parse_strict(self):
        with self.assertRaisesRegex(ValueError,"FIELD_NOT_INTEGER"):
            m.parse_tab(b"a\tb\n1\tONE\n",("a","b"))

    def test_tsv_unexpected_header(self):
        with self.assertRaisesRegex(ValueError,"UNEXPECTED_COLUMNS"):
            m.parse_tab(b"a\tc\n1\t2\n",("a","b"))

    def test_nonreciprocal_graph_rejected(self):
        bad=b"userID\tfriendID\n1\t2\n2\t1\n2\t3\n3\t5\n"
        with self.assertRaisesRegex(ValueError,"GRAPH_NOT_RECIPROCAL"):
            run(zip_data(friends=bad))

    def test_invalid_self_loop_rejected(self):
        bad=b"userID\tfriendID\n1\t1\n2\t1\n2\t3\n3\t2\n"
        with self.assertRaisesRegex(ValueError,"GRAPH_SELF_LOOP"):
            run(zip_data(friends=bad))

    def test_wrong_expected_row_count_fail_closed(self):
        a=zip_data()
        with self.assertRaisesRegex(ValueError,"ROW_UNIVERSE_DRIFT"):
            m.audit_raw_zip(a,hashlib.md5(a).hexdigest(),
                            {"friends":25434,"tag_events":186479})

    def test_source_contains_no_ids_or_per_artist_timelines(self):
        x=run(zip_data())
        self.assertNotIn("tagged_artist_id",str(x))
        self.assertFalse(x["individual_records_redistributed"])
        self.assertEqual(x["four_identification_limits"]["network_tie_formation_dates"],
                         "NOT_OBSERVED")


if __name__=="__main__":
    unittest.main()
