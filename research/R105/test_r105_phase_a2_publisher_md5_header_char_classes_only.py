"""R105 A2 pure synthetic header-class privacy plus full published MD5 gate."""
import hashlib
import unittest
from unittest.mock import patch
import r105_phase_a2_publisher_md5_header_char_classes_only as s

def sample(header="participant.id,round,total_extract,Contrib (units)"):
    return (header+"\n"+("PRIVATE_ID,1,10,20\n"*30)).encode()

def audited(b):
    with patch.object(s,"PUBLISHED_MD5",hashlib.md5(b).hexdigest()):
        return s.only_header_classes(b)

class HeaderOnly(unittest.TestCase):
    def test_actual_punctuation_ordinal_only(self):
        x=audited(sample())
        self.assertEqual(x["actual_header_field_count"],4)
        self.assertIn(40,x["ASCII_header_punctuation_ordinal_list_only"])
        self.assertIn(41,x["ASCII_header_punctuation_ordinal_list_only"])
        self.assertFalse(x["exact_header_names_or_person_values_exported"])
        self.assertFalse(x["any_original_human_behavior_or_identity_data_row_read"])
        self.assertNotIn("Contrib",str(x))
        self.assertNotIn("PRIVATE_ID",str(x))
    def test_initial_character_counts(self):
        self.assertEqual(audited(sample())["header_names_starting_safe_ASCII_count"],4)
    def test_duplicate_names_diagnostic(self):
        r=audited(sample(header="id,id,treatment"))
        self.assertEqual(r["duplicate_source_column_names_count"],1)
    def test_source_md5_mismatch_blocks(self):
        self.assertRaises(s.SourceGateError,s.only_header_classes,sample())
    def test_empty_header_value_class_aggregated(self):
        self.assertEqual(audited(sample(header="id,,treatment"))["anonymous_header_name_length_histogram"][0],1)
    def test_non_ascii_masked(self):
        x=audited(sample(header="id,β,decision"))
        self.assertEqual(x["anonymous_header_character_class_counts"]["nonascii_or_control"],1)
        self.assertNotIn("β",str(x))
    def test_too_few_columns_rejected(self):
        self.assertRaises(s.SourceGateError,audited,sample(header="id,round"))
    def test_oversize_rejected(self):
        self.assertRaises(s.SourceGateError,s.only_header_classes,b"x"*(s.CAP+1))
    def test_original_header_alias_no_data_row_scan(self):
        a=audited(sample())
        b=audited(sample().replace(b"PRIVATE_ID",b"PRIVATE_ZZ"))
        self.assertEqual(a["anonymous_header_character_class_counts"],b["anonymous_header_character_class_counts"])
        self.assertNotEqual(a["full_original_project_SHA256"],b["full_original_project_SHA256"])

if __name__=="__main__":unittest.main()
