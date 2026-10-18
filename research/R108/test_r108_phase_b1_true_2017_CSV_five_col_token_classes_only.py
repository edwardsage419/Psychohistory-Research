"""R108 B1 published-source whole MD5 pinned, limited cell syntax, no raw values."""
import hashlib
import unittest
from unittest.mock import patch

import r108_phase_a1_original_2017_Leicester_fixed_pair_CSV_MD5_double_SHA_header_only as a
import r108_phase_b1_true_2017_CSV_five_col_token_classes_only as b

def synthetic_rows():
    lines=["note,,,,"]
    cases=[
        ("PRIVATE_PERSON","0","1","21",""),
        ("PRIVATE_PERSON","1","0","-12","2.75"),
        ("PRIVATE_PERSON","5","11","male","label_001"),
        ("PRIVATE_PERSON","","","0.5","abcd"),
        ("PRIVATE_PERSON","42","-7","-", "OTHER$VALUE"),
    ]
    for i in range(1804):
        lines.append(",".join(cases[i%len(cases)]))
    return ("\n".join(lines)+"\n").encode("utf-8")

def audited(raw):
    with patch.object(a,"EXPECTED_MD5",hashlib.md5(raw).hexdigest()),\
         patch.object(a,"EXPECTED_SIZE",len(raw)),\
         patch.object(b,"PINNED_ORIGINAL_SHA",hashlib.sha256(raw).hexdigest()):
        return b.original_anonymous_token_classes(raw)

class R108TypeOnly(unittest.TestCase):
    def test_syntax_empty(self):self.assertEqual(b.classify_token("  "),"EMPTY")
    def test_syntax_zero_one(self):
        self.assertEqual(b.classify_token("0"),"BIT_0")
        self.assertEqual(b.classify_token("1"),"BIT_1")
    def test_positive_int(self):self.assertEqual(b.classify_token("005"),"UNSIGNED_INTEGER")
    def test_negative_int(self):self.assertEqual(b.classify_token("-2"),"SIGNED_INTEGER")
    def test_decimal(self):self.assertEqual(b.classify_token("-2.5"),"DECIMAL")
    def test_letters(self):self.assertEqual(b.classify_token("female"),"LETTER_ONLY")
    def test_alphanumeric(self):self.assertEqual(b.classify_token("group_01"),"ALPHANUMERIC")
    def test_other_printable(self):self.assertEqual(b.classify_token("value$"),"OTHER_PRINTABLE")
    def test_unicode(self):self.assertEqual(b.classify_token("私人"),"NONASCII_CONTROL_OR_LONG")
    def test_control(self):self.assertEqual(b.classify_token("\x00"),"NONASCII_CONTROL_OR_LONG")
    def test_genuine_source_sized_synthetic(self):
        v=audited(synthetic_rows())
        self.assertEqual(v["original_body_rows"],1804)
        self.assertEqual(set(v["original_anonymous_column_slot_type_histograms"]),set(str(i) for i in range(5)))
        self.assertEqual(sum(v["original_anonymous_column_slot_type_histograms"]["0"].values()),1804)
        self.assertTrue(v["original_data_cell_values_transiently_examined_for_syntax"])
        self.assertFalse(v["raw_original_human_person_gender_game_partner_action_values_exported"])
        self.assertEqual(v["original_human_model_scores"],0)
    def test_raw_private_tokens_never_in_receipt(self):
        s=str(audited(synthetic_rows()))
        for private in ("PRIVATE_PERSON","OTHER$VALUE","label_001"):
            self.assertNotIn(private,s)
    def test_first_last_only_anonymous_category_labels(self):
        v=audited(synthetic_rows())
        self.assertEqual(len(v["first_eight_rows_TYPE_LABELS_ONLY"]),8)
        self.assertEqual(len(v["last_eight_rows_TYPE_LABELS_ONLY"]),8)
        self.assertTrue(all(x in b.TOKENS for row in v["first_eight_rows_TYPE_LABELS_ONLY"] for x in row))
    def test_publisher_real_MD5_rejects_unpinned_synthetic(self):
        self.assertRaises(a.SourceError,b.original_anonymous_token_classes,synthetic_rows())
    def test_wrong_full_SHA_rejected_even_matching_publisher_MD5(self):
        raw=synthetic_rows()
        with patch.object(a,"EXPECTED_MD5",hashlib.md5(raw).hexdigest()),\
             patch.object(a,"EXPECTED_SIZE",len(raw)):
            self.assertRaisesRegex(a.SourceError,"FULL_SHA_NOT_PINNED",b.original_anonymous_token_classes,raw)
    def test_original_full_row_universe_enforced(self):
        raw=synthetic_rows().replace(b"PRIVATE_PERSON","PRIVATE_PERSON",1)
        with patch.object(a,"EXPECTED_MD5",hashlib.md5(raw).hexdigest()),\
             patch.object(a,"EXPECTED_SIZE",len(raw)),\
             patch.object(b,"PINNED_ORIGINAL_SHA",hashlib.sha256(raw).hexdigest()),\
             patch.object(b,"PINNED_DATA_ROWS",1805):
            self.assertRaises(a.SourceError,b.original_anonymous_token_classes,raw)
    def test_untrusted_nonfive_col_fails(self):
        raw=synthetic_rows().replace(b"PRIVATE_PERSON,0,1,21,\n",b"PRIVATE_PERSON,0,1,21\n",1)
        with patch.object(a,"EXPECTED_MD5",hashlib.md5(raw).hexdigest()),\
             patch.object(a,"EXPECTED_SIZE",len(raw)),\
             patch.object(b,"PINNED_ORIGINAL_SHA",hashlib.sha256(raw).hexdigest()):
            self.assertRaises(a.SourceError,b.original_anonymous_token_classes,raw)

if __name__=="__main__":unittest.main()
