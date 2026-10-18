"""R108 A4 synthetic full-publisher-MD5 source with anonymized header-only classes."""
import hashlib,unittest
from unittest.mock import patch
import r108_phase_a4_verified_full_original_MD5_header_class_only as a
import r108_phase_a1_original_2017_Leicester_fixed_pair_CSV_MD5_double_SHA_header_only as b

def fixture(head="Actor (ID),Round #,Action"):
    return (head+"\n"+("SYNTH_PERSON,1,PRIVATE_HUMAN_ACTION\n"*70)).encode()

def audit(raw):
    with patch.object(b,"EXPECTED_SIZE",len(raw)),patch.object(b,"EXPECTED_MD5",hashlib.md5(raw).hexdigest()):
        return a.class_only(raw)

class ClassesOnly(unittest.TestCase):
    def test_unsafe_original_ASCII_names_counted(self):
        x=audit(fixture())
        self.assertEqual(x["source_csv_header_column_count"],3)
        self.assertGreaterEqual(x["anonymous_source_header_strict_ASCII_identifier_violation_count"],1)
        self.assertIn(ord("#"),x["anonymous_header_ASCII_punctuation_decimal_codepoints_only"])
        self.assertEqual(x["source_physical_data_lines_unparsed"],70)
        self.assertFalse(x["source_human_person_pair_action_body_cells_accessed"])
        self.assertNotIn("SYNTH_PERSON",repr(x))
    def test_unicode_anonymized_never_printed(self):
        x=audit(fixture(head="Ø field,Other,Action"))
        self.assertEqual(x["anonymous_source_header_nonASCII_or_control_field_count"],1)
        self.assertNotIn("Ø",repr(x))
    def test_duplicate_name_counted(self):
        x=audit(fixture(head="Actor,Actor,Choice"))
        self.assertEqual(x["anonymous_source_header_duplicate_name_count"],1)
    def test_blank_name_counted(self):
        x=audit(fixture(head="Actor,,Choice"))
        self.assertEqual(x["anonymous_source_header_empty_name_count"],1)
    def test_author_MD5_still_required(self):
        self.assertRaises(b.SourceError,a.class_only,fixture())
    def test_no_header_line_fails(self):
        raw=b"x"*1200
        with patch.object(b,"EXPECTED_SIZE",len(raw)),patch.object(b,"EXPECTED_MD5",hashlib.md5(raw).hexdigest()):
            self.assertRaises(b.SourceError,a.class_only,raw)
    def test_html_source_fails(self):
        self.assertRaises(b.SourceError,audit,(b"<html>Unauthorized</html>\n"*60))
    def test_nul_source_fails(self):
        self.assertRaises(b.SourceError,audit,fixture()+b"\x00")
    def test_two_full_source_replay(self):
        blob=fixture()
        with patch.object(b,"EXPECTED_SIZE",len(blob)),patch.object(b,"EXPECTED_MD5",hashlib.md5(blob).hexdigest()):
            r=a.double_source(blob,blob)
        self.assertTrue(r["two_independent_exact_official_publisher_sources_byte_identical"])
        self.assertEqual(r["original_human_model_scores"],0)
    def test_different_source_replay_fails(self):
        blob=fixture();other=blob.replace(b"PRIVATE_HUMAN_ACTION",b"PRIVATE_HUMAN_OTHER0")
        with patch.object(b,"EXPECTED_SIZE",len(blob)),patch.object(b,"EXPECTED_MD5",hashlib.md5(blob).hexdigest()):
            self.assertRaises(b.SourceError,a.double_source,blob,other)
if __name__=="__main__":unittest.main()
