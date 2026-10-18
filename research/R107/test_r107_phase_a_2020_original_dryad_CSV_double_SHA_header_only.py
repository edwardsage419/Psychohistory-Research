"""R107 A pure original Dryad 296893 URL, double SHA and header-only checks."""
import unittest
import r107_phase_a_2020_original_dryad_CSV_double_SHA_header_only as r

def mock_csv(unclosed=False, header="session,person,round,action"):
    out=(header+"\n")+("PRIVATE_SESSION,PRIVATE_PERSON,PRIVATE_ROUND,PRIVATE_ACTION\n"*45)
    return (out[:-1] if unclosed else out).encode("utf-8")

class R107SourceOnlySynthetic(unittest.TestCase):
    def test_exact_official_url(self):r.validate_url(r.URL)
    def test_external_hostname_denied(self):
        self.assertRaises(r.SourceError,r.validate_url,r.URL.replace("datadryad.org","hostile.example"))
    def test_http_denied(self):
        self.assertRaises(r.SourceError,r.validate_url,r.URL.replace("https","http",1))
    def test_wrong_id_denied(self):
        self.assertRaises(r.SourceError,r.validate_url,r.URL.replace("296893","296894"))
    def test_query_denied(self):
        self.assertRaises(r.SourceError,r.validate_url,r.URL+"?redirect=elsewhere")
    def test_single_realistic_synthetic_csv_header(self):
        x=r.validate_complete_csv_header_only(mock_csv())
        self.assertEqual(x["original_csv_field_count"],4)
        self.assertEqual(x["original_physical_data_lines_without_parsing"],45)
        self.assertFalse(x["any_original_human_action_or_person_or_session_value_accessed"])
        self.assertNotIn("PRIVATE_PERSON",repr(x))
    def test_two_identical_complete_origin_sources(self):
        b=mock_csv()
        x=r.double_source(b,b)
        self.assertTrue(x["two_independent_full_original_official_downloads_bytes_equal"])
        self.assertEqual(x["human_model_scores"],0)
    def test_two_origin_content_mismatch_fails(self):
        self.assertRaises(r.SourceError,r.double_source,mock_csv(),mock_csv().replace(b"PRIVATE_ACTION",b"PRIVATE_OTHER"))
    def test_duplicate_header_fails(self):
        self.assertRaises(r.SourceError,r.validate_complete_csv_header_only,mock_csv(header="person,person,round,action"))
    def test_untrusted_header_path_fails(self):
        self.assertRaises(r.SourceError,r.validate_complete_csv_header_only,mock_csv(header="../secret,person,round,action"))
    def test_html_payload_denied(self):
        self.assertRaises(r.SourceError,r.validate_complete_csv_header_only,(b"<html>Error</html>\n"*100))
    def test_json_payload_denied(self):
        self.assertRaises(r.SourceError,r.validate_complete_csv_header_only,(b'{"error":"auth"}\n'*100))
    def test_nul_binary_payload_denied(self):
        self.assertRaises(r.SourceError,r.validate_complete_csv_header_only,mock_csv()+b"\x00")
    def test_unterminated_final_record(self):
        x=r.validate_complete_csv_header_only(mock_csv(unclosed=True))
        self.assertEqual(x["original_physical_data_lines_without_parsing"],45)
    def test_oversize_cap(self):
        self.assertRaises(r.SourceError,r.validate_complete_csv_header_only,b"x"*(r.CAP+1))
    def test_truncated_low_size(self):
        self.assertRaises(r.SourceError,r.validate_complete_csv_header_only,b"person,action\nX,1\n")

if __name__=="__main__":
    unittest.main()
