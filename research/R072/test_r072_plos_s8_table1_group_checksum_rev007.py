"""REV007: invented anonymized rows only; empirical values locked to published Table 1."""
import hashlib,unittest
from unittest.mock import patch
import r072_plos_s8_table1_group_checksum_rev007 as m
from test_r072_plos_s8_column_domains_rev004 import workbook

PUBLISHED=[(30,16),(30,6),(28,14),(25,11),(19,11),(19,12),(19,10),(19,9)]


def fake_published_dataset(pairs=PUBLISHED,footer=9):
    rows={}
    r=2
    for group,(size,ones) in enumerate(pairs,1):
        for index in range(size):
            # These are mathematical flags, not any human responses.
            rows[r]={1:group,2:int(index<ones)}
            r+=1
    for j in range(footer):
        rows[r]={1:"FAKE_FOOTER_NO_HUMAN_RECORD"}
        r+=1
    return workbook(rows,header=("Artificial Code","Artificial Flag","NOT_REAL"))


def inspect(raw):
    with patch.object(m,"SOURCE_SHA",hashlib.sha256(raw).hexdigest()):
        return m.count_anonymous_pairs(raw)


class UnlabelledAggregateTable1ChecksumTests(unittest.TestCase):
    def test_published_reference_has_8_groups_189_89(self):
        self.assertEqual(len(m.PUBLISHED_UNLABELLED_PAIRS),8)
        self.assertEqual(sum(n for n,_ in PUBLISHED),189)
        self.assertEqual(sum(y for _,y in PUBLISHED),89)

    def test_complete_matching_pair_multiset_on_aggregates(self):
        z=inspect(fake_published_dataset())
        self.assertTrue(z["weak_totals_match_published_189_89"])
        self.assertTrue(z["strong_eight_paired_multiset_matches_published_table1"])

    def test_cannot_identify_serving_from_matching_pairs(self):
        z=inspect(fake_published_dataset())
        self.assertEqual(z["author_numerical_profile_to_serving_neutral_mapping"],
                         "NOT_RECOVERED")
        self.assertEqual(z["real_serving_neutral_effect_96_93"],"NOT_CALCULATED")

    def test_swapped_group_order_keeps_parity_without_releasing_code(self):
        z=inspect(fake_published_dataset(list(reversed(PUBLISHED))))
        self.assertTrue(z["strong_eight_paired_multiset_matches_published_table1"])
        self.assertNotIn("group_code",str(z))

    def test_preserves_nine_annotation_rows_not_delete(self):
        z=inspect(fake_published_dataset(footer=9))
        self.assertEqual(z["noncandidate_format_rows"],9)
        self.assertEqual(z["candidate_requests"],189)

    def test_aggregate_total_89_weak_check_can_hide_mismatched_group_pairs(self):
        changed=list(PUBLISHED)
        changed[0]=(30,15)
        changed[-1]=(19,10)
        z=inspect(fake_published_dataset(changed))
        self.assertTrue(z["weak_totals_match_published_189_89"])
        self.assertFalse(z["strong_eight_paired_multiset_matches_published_table1"])

    def test_second_col_flipped_100_cannot_match_response89(self):
        z=inspect(fake_published_dataset())
        self.assertFalse(z["flipped_second_column_total_would_match_published_89"])

    def test_no_response_fit_or_ess(self):
        z=inspect(fake_published_dataset())
        self.assertEqual(z["real_yes_maybe_no_effect"],"NOT_CALCULATED")
        self.assertEqual(z["R072_IMAGE_STANDING_STERN_E2"],"NOT_TESTED")

    def test_individual_rows_not_printed(self):
        z=inspect(fake_published_dataset())
        self.assertFalse(z["individual_records_group_IDs_or_codes_exported"])
        self.assertNotIn("FAKE_FOOTER_NO_HUMAN_RECORD",str(z))

    def test_source_sha_enforced(self):
        with self.assertRaisesRegex(ValueError,"SHA_MISMATCH"):
            m.count_anonymous_pairs(fake_published_dataset())

    def test_no_unverified_rare_group(self):
        p=list(PUBLISHED)
        p[0]=(9,5)
        with self.assertRaisesRegex(ValueError,"BELOW_PUBLIC"):
            inspect(fake_published_dataset(p))

    def test_reject_not_eight_groups(self):
        with self.assertRaisesRegex(ValueError,"NOT_EIGHT"):
            inspect(fake_published_dataset(PUBLISHED[:7]))

    def test_reject_nonbinary_second_col(self):
        raw=workbook({2:{1:1,2:7},3:{1:2,2:0}})
        with self.assertRaisesRegex(ValueError,"PREDEFINED_BINARY"):
            inspect(raw)

    def test_coding_as_one_not_redefined_after_output(self):
        z=inspect(fake_published_dataset())
        self.assertIn("CANDIDATE_ANY_RESPONSE_1",z["column_2_semantics"])
        self.assertNotIn("VERIFIED_AUTHOR_CODEBOOK",str(z))

    def test_mismatched_189_total_is_not_parity(self):
        ps=list(PUBLISHED)
        ps[-1]=(20,9)
        z=inspect(fake_published_dataset(ps))
        self.assertFalse(z["weak_totals_match_published_189_89"])
        self.assertFalse(z["strong_eight_paired_multiset_matches_published_table1"])

    def test_PESEN_remains_frozen(self):
        z=inspect(fake_published_dataset())
        self.assertEqual(z["pesen_v01"],"FROZEN")


if __name__=="__main__":
    unittest.main()
