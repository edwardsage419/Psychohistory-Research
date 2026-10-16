"""R072 REV005 privacy contracts use purely synthetic groups, no real subject rows."""
from __future__ import annotations
import hashlib,unittest
from unittest.mock import patch
from r072_plos_s8_profile_block_parity_rev005 import make_receipt,PUB_GROUP_SORTED
import r072_plos_s8_profile_block_parity_rev005 as m
from test_r072_plos_s8_column_domains_rev004 import workbook


def synthetic_groups(sizes=None,annotations=0,invalid_col2=False):
    sizes=sizes or PUB_GROUP_SORTED
    rows={}
    rid=2
    for group_ix,size in enumerate(sizes,1):
        if annotations and group_ix<=annotations:
            rows[rid]={1:"TEST_SECTION_TITLE_NOT_A_PERSON"}
            rid+=1
        for j in range(size):
            rows[rid]={1:group_ix,2:j%2}
            if invalid_col2 and group_ix==1 and j==0:
                rows[rid][2]="NOT_NUMERIC"
            rid+=1
    if annotations>len(sizes):
        for _ in range(annotations-len(sizes)):
            rows[rid]={1:"TEST_SECTION_TITLE_NOT_A_PERSON"}
            rid+=1
    return workbook(rows,header=("Synthetic Group Code","Synthetic Binary","Artificial Note"))


def scan(blob):
    with patch.object(m,"EXPECTED_S8_SHA",hashlib.sha256(blob).hexdigest()):
        return make_receipt(blob)


class AnonymousProfileGroupTests(unittest.TestCase):
    def test_published_size_multiset_not_identity(self):
        q=scan(synthetic_groups(annotations=9))
        self.assertEqual(q["candidate_rows_by_numeric_col1_and_col2"],189)
        self.assertEqual(q["noncandidate_annotation_format_rows"],9)
        self.assertEqual(q["anonymous_col1_group_sizes_sorted_suppressed_if_any_less10"],PUB_GROUP_SORTED)
        self.assertTrue(q["source_structural_189_x_8group_parity"])

    def test_198_nonheader_rows_keep_annotations_not_deleted(self):
        x=scan(synthetic_groups(annotations=9))
        self.assertEqual(x["total_nonheader_physical_rows"],198)
        self.assertEqual(x["noncandidate_annotation_format_rows"],9)

    def test_candidate_condition_uses_types_not_response_values(self):
        x=scan(synthetic_groups(annotations=9,invalid_col2=True))
        self.assertEqual(x["candidate_rows_by_numeric_col1_and_col2"],188)
        self.assertFalse(x["candidate_request_count_matches_published_189"])

    def test_188_is_not_force_tuned_to_published_189(self):
        x=scan(synthetic_groups(sizes=[19,19,19,19,25,28,30,29]))
        self.assertFalse(x["source_structural_189_x_8group_parity"])

    def test_publish_8_anonymous_size_multiset_without_code_keys(self):
        q=scan(synthetic_groups())
        self.assertNotIn('"anonymous_col1_code_values"',str(q))
        self.assertFalse(q["participant_codes_names_values_released"])
        self.assertFalse(q["individual_human_response_rows_released"])

    def test_bin_sums_cannot_be_misinterpreted_as_treatment(self):
        q=scan(synthetic_groups())
        self.assertIsNotNone(q["binary_second_column_code_counts_not_a_treatment_mapping"])
        self.assertEqual(q["author_serving_vs_neutral_profile_label_mapping"],"NOT_RECOVERED")

    def test_binary_outcome_not_automatically_named_yes(self):
        q=scan(synthetic_groups())
        self.assertEqual(q["author_yes_maybe_no_reply_semantics"],"NOT_RECOVERED")
        self.assertEqual(q["published_response_analysis_replication"],"NOT_PERFORMED")

    def test_synthetic_rare_group_less10_refused(self):
        with self.assertRaisesRegex(ValueError,"SMALL_CODE_GROUPS"):
            scan(synthetic_groups(sizes=[3,19,19,19,25,28,30,30]))

    def test_one_group_mismatched_size_even_if_189_cannot_pass(self):
        # Rebalance two groups, keeping 189 and 8 categories.
        q=scan(synthetic_groups(sizes=[20,18,19,19,25,28,30,30]))
        self.assertFalse(q["eight_anonymous_group_multiset_matches_table3"])
        self.assertTrue(q["candidate_request_count_matches_published_189"])
        self.assertFalse(q["source_structural_189_x_8group_parity"])

    def test_wrong_publisher_sha_cannot_pass(self):
        with self.assertRaisesRegex(ValueError,"SOURCE_SHA"):
            make_receipt(synthetic_groups())

    def test_no_private_record_contents_exported(self):
        q=scan(synthetic_groups(annotations=9))
        self.assertNotIn("TEST_SECTION_TITLE_NOT_A_PERSON",str(q))
        self.assertNotIn("Synthetic Group Code",str(q))

    def test_bare_url_or_metadata_does_not_pass_as_xlsx(self):
        with self.assertRaisesRegex(ValueError,"SOURCE_SHA"):
            make_receipt(b"https://example.org/filename.xlsx")

    def test_group_counts_do_not_claim_causal_identification(self):
        q=scan(synthetic_groups())
        self.assertEqual(q["treatment_randomization_replication"],"NOT_PERFORMED")
        self.assertEqual(q["human_image_standing_stern_reputation_model"],"NOT_TESTED")

    def test_segment_lengths_not_released_if_any_short(self):
        q=scan(synthetic_groups(sizes=PUB_GROUP_SORTED,annotations=9))
        self.assertIsNone(q["candidate_data_runs_orderless_sorted_if_min_ge10"])

    def test_outcomes_not_used_as_filters(self):
        # Only two first cells, not third outcome candidate, determine row eligibility.
        x=scan(synthetic_groups(annotations=9))
        self.assertEqual(x["candidate_rows_by_numeric_col1_and_col2"],189)
        self.assertEqual(x["anonymous_col1_unique_numeric_codes"],8)


if __name__=="__main__":unittest.main()
