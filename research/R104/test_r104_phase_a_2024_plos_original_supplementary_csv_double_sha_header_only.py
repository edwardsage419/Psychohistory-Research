"""R104 A publisher source-only double SHA synthetic security and no human-value parsing."""
import unittest
import r104_phase_a_2024_plos_original_supplementary_csv_double_sha_header_only as s

def fake(rows=30,final=True):
    b=("session,actor,contribution\n"+("T,PRIVATE_PERSON,PRIVATE_ACTION\n"*rows)).encode()
    return b if final else b[:-1]

class Synthetic(unittest.TestCase):
    def test_original_url(self):s.validate_url(s.URL)
    def test_fake_host_rejected(self):
        self.assertRaises(s.SourceError,s.validate_url,s.URL.replace("journals.plos.org","bad.example"))
    def test_extra_query_rejected(self):
        self.assertRaises(s.SourceError,s.validate_url,s.URL+"&secret=token")
    def test_wrong_supplementary_rejected(self):
        self.assertRaises(s.SourceError,s.validate_url,s.URL.replace("s002","s001"))
    def test_exact_original_source_bytes_double(self):
        r=s.complete_double_source(fake(),fake())
        self.assertTrue(r["two_independent_publisher_downloads_byte_for_byte_equal"])
        self.assertEqual(r["original_csv_header_field_count"],3)
        self.assertFalse(r["any_original_human_behavior_or_identity_cells_accessed"])
        self.assertEqual(r["actual_human_model_scores"],0)
        self.assertNotIn("PRIVATE_PERSON",repr(r))
    def test_mismatched_full_original_rejected(self):
        a=fake()
        b=a.replace(b"PRIVATE_ACTION",b"PRIVATE_OTHER")
        self.assertRaises(s.SourceError,s.complete_double_source,a,b)
    def test_nonterminated_final_line_count(self):
        self.assertEqual(s.source_header_only(fake(final=False))["original_physical_data_lines_unparsed"],30)
    def test_bad_header_duplicate_rejected(self):
        b=fake().replace(b"session,actor,contribution",b"session,actor,actor")
        self.assertRaises(s.SourceError,s.source_header_only,b)
    def test_bad_header_path_rejected(self):
        b=fake().replace(b"contribution",b"../unsafe",1)
        self.assertRaises(s.SourceError,s.source_header_only,b)
    def test_html_rejected(self):
        b=b"<html><body>Forbidden</body></html>"*5
        self.assertRaises(s.SourceError,s.source_header_only,b)
    def test_zero_byte_rejected(self):
        self.assertRaises(s.SourceError,s.source_header_only,b"\x00"*500)
    def test_overlong_original_rejected(self):
        self.assertRaises(s.SourceError,s.source_header_only,b"x"*(s.CAP+1))

if __name__=="__main__":
    unittest.main()
