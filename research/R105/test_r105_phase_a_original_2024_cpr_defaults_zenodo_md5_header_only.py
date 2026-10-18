"""R105 A3 exactly one unnamed original CSV header, pure synthetic no actions."""
import hashlib
import unittest
from unittest.mock import patch
import r105_phase_a_original_2024_cpr_defaults_zenodo_md5_header_only as s

def fields():
    return ["","participant_id","group","round_number","extraction"] + [f"safe_col_{i}" for i in range(32)]

def simulated_source(lines=50,ending=True,header=None):
    header=fields() if header is None else header
    raw=",".join(header)+"\n"+("SYNTHETIC_FAKE_ID,SYNTHETIC_FAKE_GROUP,1,20\n"*lines)
    return (raw if ending else raw[:-1]).encode("utf-8")
def audited(raw):
    with patch.object(s,"PUBLISHED_MD5",hashlib.md5(raw).hexdigest()):
        return s.source_header_only(raw)

class OneEmptyOriginalHeader(unittest.TestCase):
    def test_exact_author_zenodo_url(self):s.validate_url(s.SOURCE_URL)
    def test_other_zenodo_record_rejected(self):
        self.assertRaises(s.SourceGateError,s.validate_url,s.SOURCE_URL.replace("10818840","10228658"))
    def test_evil_host_rejected(self):
        self.assertRaises(s.SourceGateError,s.validate_url,s.SOURCE_URL.replace("zenodo.org","fake.example"))
    def test_token_query_rejected(self):
        self.assertRaises(s.SourceGateError,s.validate_url,s.SOURCE_URL+"&token=secret")
    def test_fake_original_MD5_blocked(self):
        self.assertRaises(s.SourceGateError,s.source_header_only,simulated_source())
    def test_37_columns_exact_one_unnamed_header_passes(self):
        r=audited(simulated_source())
        self.assertEqual(r["original_csv_header_field_count"],37)
        self.assertEqual(r["original_unnamed_column_count"],1)
        self.assertEqual(r["public_sanitized_original_header_field_names"][0],"__UNNAMED_ORIGINAL_SOURCE_COLUMN__")
        self.assertEqual(r["physical_original_data_row_lines_unparsed"],50)
        self.assertFalse(r["any_original_human_choice_value_read"])
        self.assertFalse(r["any_original_person_or_group_identifier_cell_read"])
        self.assertNotIn("SYNTHETIC_FAKE_ID",str(r))
    def test_exact_missing_final_newline_allowed(self):
        self.assertEqual(audited(simulated_source(ending=False))["physical_original_data_row_lines_unparsed"],50)
    def test_two_empty_headers_rejected(self):
        a=fields();a[2]=""
        self.assertRaises(s.SourceGateError,audited,simulated_source(header=a))
    def test_no_unnamed_header_rejected(self):
        a=fields();a[0]="new_name"
        self.assertRaises(s.SourceGateError,audited,simulated_source(header=a))
    def test_duplicate_original_named_header_rejected(self):
        a=fields();a[3]=a[2]
        self.assertRaises(s.SourceGateError,audited,simulated_source(header=a))
    def test_illegal_other_named_header_rejected(self):
        a=fields();a[4]="../notallowed"
        self.assertRaises(s.SourceGateError,audited,simulated_source(header=a))
    def test_null_byte_original_data_rejected(self):
        self.assertRaises(s.SourceGateError,audited,simulated_source()+b"\x00")
    def test_oversize_source_rejected(self):
        self.assertRaises(s.SourceGateError,s.source_header_only,b"x"*(s.CAP+1))

if __name__=="__main__":unittest.main()
