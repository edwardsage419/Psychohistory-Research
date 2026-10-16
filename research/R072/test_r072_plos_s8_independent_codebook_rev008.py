"""REV008 fictional-note only tests, never any actual participant data."""
import hashlib,unittest
from decimal import Decimal as D
from unittest.mock import patch
import r072_plos_s8_independent_codebook_rev008 as m
from test_r072_plos_s8_column_domains_rev004 import workbook


CODES=set(D(x) for x in range(1,9))


def test_notes():
    notes=[]
    for ix in range(1,9):
        label="serving profile" if ix<=4 else "neutral"
        notes.append({1:(f"{ix}: {label}","text")})
    notes.append({1:("Notes unrelated to treatment","text")})
    return notes


def synthetic_scan(raw):
    with patch.object(m,"EXACT_SHA",hashlib.sha256(raw).hexdigest()):
        return m.original_data_gate(raw)


class S8AuthorCodebookIndependentGate(unittest.TestCase):
    def test_complete_source_explicit_one_to_one(self):
        z=m.characterize_codebook(CODES,test_notes())
        self.assertTrue(z["candidate_full_eight_codebook_exists"])
        self.assertFalse(z["human_serving_effect_calculated"])

    def test_one_to_one_two_column_example(self):
        ns=[{1:(D(i),"numeric"),2:(("serving profile" if i<=4 else "neutral"),"text")}
            for i in range(1,9)]
        z=m.characterize_codebook(CODES,ns)
        self.assertTrue(z["candidate_unique_serving_neutral_four_each"])

    def test_service_without_history_not_assumed(self):
        ns=[{1:(f"{i}: service","text")} for i in range(1,9)]
        self.assertFalse(m.characterize_codebook(CODES,ns)["candidate_full_eight_codebook_exists"])

    def test_one_code_missing_never_infer_from_paper_totals(self):
        z=m.characterize_codebook(CODES,test_notes()[:7])
        self.assertFalse(z["candidate_full_eight_codebook_exists"])

    def test_no_numeric_code_no_author_binding(self):
        z=m.characterize_codebook(CODES,[{1:("service history neutral group","text")}])
        self.assertFalse(z["candidate_full_eight_codebook_exists"])

    def test_conflicting_service_neutral_single_row_rejected(self):
        ns=test_notes()+[{1:("2: neutral","text")}]
        z=m.characterize_codebook(CODES,ns)
        self.assertTrue(z["candidate_conflict_found"])
        self.assertFalse(z["candidate_full_eight_codebook_exists"])

    def test_numeric_code_not_existing_first_col_not_adopted(self):
        ns=[{1:(f"{ix+10}: serving profile","text")} for ix in range(1,9)]
        z=m.characterize_codebook(CODES,ns)
        self.assertFalse(z["candidate_full_eight_codebook_exists"])

    def test_partial_range_hint_never_adopted_as_codebook(self):
        z=m.characterize_codebook(CODES,[{1:("1-4 serving profile; 5-8 neutral","text")}])
        self.assertTrue(z["range_syntax_hint_present_not_adopted"])
        self.assertFalse(z["candidate_full_eight_codebook_exists"])

    def test_duplicate_code_with_same_label_not_create_two_codes(self):
        ns=test_notes()[:7]+[{1:("1 = serving profile","text")}]
        z=m.characterize_codebook(CODES,ns)
        self.assertFalse(z["candidate_full_eight_codebook_exists"])

    def test_publisher_response_rates_irrelevant_to_matching(self):
        z=m.characterize_codebook(CODES,test_notes())
        self.assertEqual(z["status"],"FULL_AUTHOR_CODEBOOK_CANDIDATE_REQUIRES_NEXT_STAGE_CONFIRMATION")
        self.assertNotIn("responses",str(z))

    def test_no_individual_header_or_profile_text_exported(self):
        notes=test_notes()+[{2:("SECRET_PERSON_ACCOUNT_NAME_78654","text")}]
        z=m.characterize_codebook(CODES,notes)
        self.assertNotIn("SECRET_PERSON_ACCOUNT_NAME_78654",str(z))
        self.assertFalse(z["raw_group_codes_notes_and_individual_responses_disclosed"])

    def test_source_sha_guard_before_any_source_analysis(self):
        fake=workbook({2:{1:1,2:0}})
        with self.assertRaisesRegex(ValueError,"SHA_MISMATCH"):
            m.original_data_gate(fake)

    def test_invalid_not_eight_groups_fails(self):
        with self.assertRaisesRegex(ValueError,"EIGHT_GROUP"):
            m.characterize_codebook(set(range(1,5)),test_notes())

    def test_ambiguous_number_cannot_be_inferred(self):
        ns=[{1:(D(1),"numeric"),2:(D(2),"numeric"),3:("serving profile","text")}]
        z=m.characterize_codebook(CODES,ns)
        self.assertTrue(z["candidate_conflict_found"])

    def test_nonlabel_yes_no_does_not_prove_treatment(self):
        z=m.characterize_codebook(CODES,[{1:("1: yes, 0: no","text")}])
        self.assertFalse(z["candidate_full_eight_codebook_exists"])


if __name__=="__main__":unittest.main()
