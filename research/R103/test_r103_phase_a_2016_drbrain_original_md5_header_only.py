"""R103 pure synthetic full published-MD5 gate and true-dyadic header-only tests."""
import hashlib
import unittest
from unittest.mock import patch
import r103_phase_a_2016_drbrain_original_md5_header_only as s

def fakecsv(columns=s.MANDATORY_FIELDS,final_newline=True):
    data=",".join(columns)+"\n"+"1,1,1,2,3,PD,C,2,D\n"*30
    if not final_newline:data=data[:-1]
    return data.encode()

def audited(b):
    with patch.object(s,"OFFICIAL_MD5",hashlib.md5(b).hexdigest()):
        return s.audit_firstparty_bytes_header_only(b)

class A103SourceSynthetic(unittest.TestCase):
    def test_url_original(self):s.validate_url(s.URL)
    def test_http_refused(self):self.assertRaises(s.SourceError,s.validate_url,s.URL.replace("https","http",1))
    def test_host_refused(self):self.assertRaises(s.SourceError,s.validate_url,s.URL.replace("zenodo.org","evil.example"))
    def test_wrong_record_refused(self):self.assertRaises(s.SourceError,s.validate_url,s.URL.replace("1127154","0"))
    def test_wrong_csv_refused(self):self.assertRaises(s.SourceError,s.validate_url,s.URL.replace("decisions.csv","other.csv"))
    def test_additional_query_refused(self):self.assertRaises(s.SourceError,s.validate_url,s.URL+"&token=private")
    def test_official_fake_original_unverified(self):self.assertRaises(s.SourceError,s.audit_firstparty_bytes_header_only,fakecsv())
    def test_nine_declared_fields_pass(self):
        r=audited(fakecsv())
        self.assertEqual(r["original_csv_header_count"],9)
        self.assertEqual(r["source_physical_data_lines_without_parsing"],30)
        self.assertEqual(r["original_additional_csv_columns_count"],0)
        self.assertFalse(r["original_action_or_opponent_action_values_accessed"])
        self.assertEqual(r["real_human_model_scores"],0)
    def test_unterminated_last_line_pass(self):
        r=audited(fakecsv(final_newline=False))
        self.assertEqual(r["source_physical_data_lines_without_parsing"],30)
    def test_extra_declared_column_allowed(self):
        r=audited(fakecsv(columns=s.MANDATORY_FIELDS+("Metadata",)))
        self.assertEqual(r["original_additional_csv_columns_count"],1)
    def test_missing_opponent_action_header_blocked(self):
        b=fakecsv(columns=s.MANDATORY_FIELDS[:-1])
        self.assertRaises(s.SourceError,audited,b)
    def test_header_filename_private_rejected(self):
        b=fakecsv(columns=s.MANDATORY_FIELDS+("../x",))
        self.assertRaises(s.SourceError,audited,b)
    def test_duplicate_original_field_rejected(self):
        b=fakecsv(columns=s.MANDATORY_FIELDS+("Game",))
        self.assertRaises(s.SourceError,audited,b)
    def test_binary_null_fails(self):
        b=fakecsv()+b"\x00"
        self.assertRaises(s.SourceError,audited,b)
    def test_oversize_fails(self):
        self.assertRaises(s.SourceError,s.audit_firstparty_bytes_header_only,b"x"*(s.CAP+1))
    def test_bom_header(self):
        b=b"\xef\xbb\xbf"+fakecsv()
        self.assertEqual(audited(b)["original_csv_header_count"],9)

if __name__=="__main__":
    unittest.main()
