"""R108 B2 pure synthetics, original-signed source six 300-block audit only."""
import hashlib,unittest
from unittest.mock import patch

import r108_phase_a1_original_2017_Leicester_fixed_pair_CSV_MD5_double_SHA_header_only as a
import r108_phase_b2_2017_true_original_6x300_candidate_condition_block_source_only as d

def fixture(wrong_round=False,changed_group=False):
    lines=["header,,,,","text1,,,,","text2,,,,",",,,,","section,,,,"]
    for block in range(6):
        group=block//3+1
        condition=block%3+1
        for t in range(1,301):
            q=301 if wrong_round and block==2 and t==150 else t
            g=2 if changed_group and block==0 and t==20 else group
            lines.append(f"{q},{g},{condition},0.2500,1.5000")
    return ("\n".join(lines)+"\n").encode()

def audited(raw):
    with patch.object(a,"EXPECTED_MD5",hashlib.md5(raw).hexdigest()),\
         patch.object(a,"EXPECTED_SIZE",len(raw)),\
         patch.object(d,"PINNED_SHA",hashlib.sha256(raw).hexdigest()):
        return d.real_source_block_schema_only(raw)

class SourceSixBlock(unittest.TestCase):
    def test_positive_six_blocks_only_condition_not_people(self):
        x=audited(fixture())
        self.assertTrue(x["source_exact_two_by_three_condition_series_structure"])
        self.assertTrue(x["six_300_sequential_first_slot_ordinal_blocks_exact"])
        self.assertEqual(x["candidate_numeric_source_rows"],1800)
        self.assertEqual(x["total_original_logical_data_rows"],1804)
        self.assertFalse(x["actor_round_E2_eligible_with_current_source_codebook"])
        self.assertEqual(x["original_human_model_scores"],0)
    def test_wrong_round_does_not_conjure_source_block(self):
        x=audited(fixture(wrong_round=True))
        self.assertFalse(x["six_300_sequential_first_slot_ordinal_blocks_exact"])
        self.assertFalse(x["source_exact_two_by_three_condition_series_structure"])
    def test_changed_group_inside_block_rejected(self):
        x=audited(fixture(changed_group=True))
        self.assertFalse(x["source_exact_two_by_three_condition_series_structure"])
    def test_true_six_group_pair_distinct(self):
        x=audited(fixture())
        self.assertTrue(x["source_six_slot1_slot2_code_pairs_all_distinct"])
        self.assertEqual(x["slot0_slot1_slot2_distinct_undecoded_numeric_code_counts"],[300,2,3])
    def test_aggregate_numeric_decimal_vs_nonbinary(self):
        x=audited(fixture())
        self.assertEqual(x["slot3_4_numeric_value_range_class_aggregate"]["slot3"]["BETWEEN_ZERO_ONE"],1800)
        self.assertEqual(x["slot3_4_numeric_value_range_class_aggregate"]["slot4"]["GREATER_THAN_ONE"],1800)
    def test_raw_source_codes_values_not_exported(self):
        x=audited(fixture())
        self.assertNotIn("0.2500",repr(x))
        self.assertNotIn("1.5000",repr(x))
        self.assertFalse(x["original_CSV_person_gender_partner_action_values_exported"])
    def test_MD5_requires_true_original_full_bytes(self):
        self.assertRaises(a.SourceError,d.real_source_block_schema_only,fixture())
    def test_full_SHA_independently_frozen(self):
        raw=fixture()
        with patch.object(a,"EXPECTED_MD5",hashlib.md5(raw).hexdigest()),\
             patch.object(a,"EXPECTED_SIZE",len(raw)):
            self.assertRaisesRegex(a.SourceError,"SOURCE_SHA_NOT_PINNED",d.real_source_block_schema_only,raw)
    def test_wrong_body_universe_fails(self):
        raw=fixture().rsplit(b"\n",2)[0]+b"\n"
        with patch.object(a,"EXPECTED_MD5",hashlib.md5(raw).hexdigest()),\
             patch.object(a,"EXPECTED_SIZE",len(raw)),\
             patch.object(d,"PINNED_SHA",hashlib.sha256(raw).hexdigest()):
            self.assertRaises(a.SourceError,d.real_source_block_schema_only,raw)
    def test_posinteger_nonbinary(self):
        self.assertIsNone(d.posinteger("PRIVATE_PERSON"))
        self.assertIsNone(d.posinteger("0"))
        self.assertEqual(d.posinteger("0003"),3)
    def test_positive_decimal_classes(self):
        self.assertEqual(d.valclass("0.5"),"BETWEEN_ZERO_ONE")
        self.assertEqual(d.valclass("2"),"GREATER_THAN_ONE")
        self.assertEqual(d.valclass("1"),"ONE")
        self.assertEqual(d.valclass("-1"),"NEGATIVE")
        self.assertEqual(d.valclass("NA"),"NONNUMERIC")
    def test_no_real_action_model_scoring_even_if_block_structure_true(self):
        x=audited(fixture())
        self.assertFalse(x["real_focal_partner_identity_from_source_established"])
        self.assertFalse(x["real_independent_original_lab_session_from_source_established"])
        self.assertFalse(x["individual_human_identity_from_source_established"])
        self.assertTrue(x["original_data_cells_accessed_for_bounded_structural_audit"])

if __name__=="__main__":unittest.main()
