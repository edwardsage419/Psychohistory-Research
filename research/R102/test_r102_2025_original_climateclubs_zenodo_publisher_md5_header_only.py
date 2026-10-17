"""R102 pure synthetic source URL, MD5/header/row gate tests; never real behavior."""
import hashlib
import unittest
from unittest.mock import patch
import r102_2025_original_climateclubs_zenodo_publisher_md5_header_only as m

def fake_source(rows=2700,header=None):
    title=",".join(header or m.EXPECTED_HEADER)+"\n"
    line=",".join(["NA"]*len(m.EXPECTED_HEADER))+"\n"
    return (title+line*rows).encode("utf-8")

class SyntheticOnly(unittest.TestCase):
    def test_pinned_url(self):m.validate_url(m.URL)
    def test_other_hostname_rejected(self):
        self.assertRaises(m.SourceError,m.validate_url,m.URL.replace("zenodo.org","bad.example"))
    def test_wrong_file_rejected(self):
        self.assertRaises(m.SourceError,m.validate_url,m.URL.replace("Climate_Clubs_data.csv","other.csv"))
    def test_token_query_rejected(self):
        self.assertRaises(m.SourceError,m.validate_url,m.URL+"&token=secret")
    def test_synthetic_full_header_rounds(self):
        b=fake_source()
        with patch.object(m,"PUBLISHER_MD5",hashlib.md5(b).hexdigest()):
            r=m.source_identity_header_only(b)
        self.assertEqual(r["physical_source_data_rows"],2700)
        self.assertEqual(r["original_CSV_header_column_count"],27)
        self.assertFalse(r["any_original_human_decision_value_dereferenced"])
        self.assertEqual(r["real_human_model_scores"],0)
    def test_fake_publisher_md5_fails(self):
        self.assertRaises(m.SourceError,m.source_identity_header_only,fake_source())
    def test_missing_required_header_fails(self):
        bad=list(m.EXPECTED_HEADER)
        bad[1]="wrong.column"
        b=fake_source(header=bad)
        with patch.object(m,"PUBLISHER_MD5",hashlib.md5(b).hexdigest()):
            self.assertRaises(m.SourceError,m.source_identity_header_only,b)
    def test_reduced_2699_rows_fails(self):
        b=fake_source(rows=2699)
        with patch.object(m,"PUBLISHER_MD5",hashlib.md5(b).hexdigest()):
            self.assertRaises(m.SourceError,m.source_identity_header_only,b)
    def test_no_final_newline_fails(self):
        b=fake_source()[:-1]
        with patch.object(m,"PUBLISHER_MD5",hashlib.md5(b).hexdigest()):
            self.assertRaises(m.SourceError,m.source_identity_header_only,b)
    def test_binary_zero_rejected(self):
        b=fake_source()+b"\x00"
        with patch.object(m,"PUBLISHER_MD5",hashlib.md5(b).hexdigest()):
            self.assertRaises(m.SourceError,m.source_identity_header_only,b)
    def test_oversized_rejected(self):
        self.assertRaises(m.SourceError,m.source_identity_header_only,b"x"*(m.CAP+1))
    def test_bom_publisher_header_only(self):
        b=b"\xef\xbb\xbf"+fake_source()
        with patch.object(m,"PUBLISHER_MD5",hashlib.md5(b).hexdigest()):
            self.assertEqual(m.source_identity_header_only(b)["physical_source_data_rows"],2700)

if __name__=="__main__":
    unittest.main()
