"""R100 B1c pure synthetic masked filename structure and role grammar tests."""
import re
import unittest
import r100_phase_b1c_original_workbook_anonymized_sheet_name_diagnostic as m


class B1cSynthetic(unittest.TestCase):
    def test_mask_nonrecoverable_short(self):
        self.assertEqual(m.name_mask("FE-Type 1"), "UUhUlll s9")
    def test_type_1_author_illustration(self):
        self.assertIsNotNone(re.fullmatch(m.ROLE_RULES[0], "FE_Type 1"))
    def test_type1_no_space(self):
        self.assertIsNotNone(re.fullmatch(m.ROLE_RULES[1], "FE_Type1"))
    def test_type_lower_case_rule(self):
        self.assertIsNotNone(re.fullmatch(m.ROLE_RULES[2], "FE-type 2", re.I))
    def test_T1_abbreviation(self):
        self.assertIsNotNone(re.fullmatch(m.ROLE_RULES[3], "FE_T1", re.I))
    def test_delimited_1(self):
        self.assertIsNotNone(re.fullmatch(m.ROLE_RULES[4], "FE_1"))
    def test_parenthesized_role(self):
        self.assertIsNotNone(re.fullmatch(m.ROLE_RULES[5], "FE(2)"))
    def test_player_role(self):
        self.assertIsNotNone(re.fullmatch(m.ROLE_RULES[6], "FE_Player1",re.I))
    def test_type_plain_suffix(self):
        self.assertIsNotNone(re.fullmatch(m.ROLE_RULES[7], "FEType2",re.I))
    def test_untrusted_unknown_char_mask(self):
        self.assertEqual(m.name_mask("a_1/"),"l_9p")
    def test_limit_name_size(self):
        with self.assertRaises(m.SourceError):m.name_mask("x"*80)
    def test_original_fake_rejected(self):
        with self.assertRaises(m.SourceError):m.masked_source_workbook_names(b"FAKE_SOURCE")

if __name__=="__main__":
    unittest.main()
