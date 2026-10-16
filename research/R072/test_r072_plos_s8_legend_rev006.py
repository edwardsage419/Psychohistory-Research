"""R072 REV006 uses only invented footer lines. Never real participant data."""
import hashlib,unittest
from unittest.mock import patch
import r072_plos_s8_legend_rev006 as m
from test_r072_plos_s8_column_domains_rev004 import workbook


def fixture(note="1=serving and 0=neutral",before=0,after=1,inside=0):
    rows={}
    rid=2
    for _ in range(before):
        rows[rid]={1:note};rid+=1
    for j in range(20):
        if inside and j==10:
            rows[rid]={1:note};rid+=1
        rows[rid]={1:j%2+1,2:j%2};rid+=1
    for _ in range(after):
        rows[rid]={1:note};rid+=1
    return workbook(rows)


def inspect(raw):
    with patch.object(m,"EXACT_SHA",hashlib.sha256(raw).hexdigest()):
        return m.read_note_profile(raw)


class SyntheticPrivacyLegendTests(unittest.TestCase):
    def test_strict_author_code_syntax_candidate_not_proof(self):
        z=inspect(fixture())
        self.assertTrue(z["strict_numeric_label_assignment_syntax_with_both_serving_and_neutral"])
        self.assertFalse(z["author_treatment_encoding_verified"])

    def test_no_codes_or_full_footer_exported(self):
        z=inspect(fixture("PRIVATE_PERSON_987 and 1=serving 0=neutral"))
        self.assertNotIn("PRIVATE_PERSON_987",str(z))
        self.assertFalse(z["individual_text_or_codes_exported"])

    def test_keyword_presence_only(self):
        z=inspect(fixture("Neutral label with Service History and Provider"))
        self.assertTrue(z["public_keyword_presence_across_all_noncase_lines_only"]["neutral"])
        self.assertTrue(z["public_keyword_presence_across_all_noncase_lines_only"]["service"])
        self.assertFalse(z["strict_numeric_label_assignment_syntax_with_both_serving_and_neutral"])

    def test_annotation_suffix(self):
        z=inspect(fixture(after=2))
        self.assertEqual(z["noncase_rows_after_numeric_block"],2)
        self.assertEqual(z["noncase_rows_inside_numeric_block"],0)

    def test_annotation_prefix(self):
        z=inspect(fixture(before=2,after=0))
        self.assertEqual(z["noncase_rows_before_numeric_block"],2)

    def test_annotation_between(self):
        z=inspect(fixture(inside=1,after=0))
        self.assertEqual(z["noncase_rows_inside_numeric_block"],1)

    def test_no_footer_codebook_for_nonsense(self):
        z=inspect(fixture("UNRELATED_OLDER_NOTE"))
        self.assertEqual(z["author_codebook_status"],"AUTHOR_CODEBOOK_STILL_NOT_RECOVERED")

    def test_serving_only_not_enough(self):
        z=inspect(fixture("1=serving"))
        self.assertFalse(z["strict_numeric_label_assignment_syntax_with_both_serving_and_neutral"])

    def test_both_words_but_no_assignments_not_enough(self):
        z=inspect(fixture("These are serving or neutral profiles"))
        self.assertFalse(z["strict_numeric_label_assignment_syntax_with_both_serving_and_neutral"])

    def test_true_code_never_mapped_from_emergent_presence(self):
        z=inspect(fixture())
        self.assertFalse(z["author_treatment_encoding_verified"])
        self.assertFalse(z["real_response_analysis_performed"])

    def test_fixed_source_SHA_rejects_fake_book(self):
        with self.assertRaisesRegex(ValueError,"SOURCE_SHA"):
            m.read_note_profile(fixture())

    def test_study_does_not_become_E3(self):
        z=inspect(fixture())
        self.assertEqual(z["independent_E3"],"OPEN")


if __name__=="__main__":unittest.main()
