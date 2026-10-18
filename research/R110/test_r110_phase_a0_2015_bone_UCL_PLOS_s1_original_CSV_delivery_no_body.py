"""R110 A0 source-only published PLOS S1 first-party no-body link tests."""
import unittest
import r110_phase_a0_2015_bone_UCL_PLOS_s1_original_CSV_delivery_no_body as a
class PLOS(unittest.TestCase):
    def test_publisher_exact(self):self.assertTrue(a.origin(a.URL))
    def test_other_article(self):
        self.assertRaises(a.SourceError,a.origin,a.URL.replace("0117183","0117184"))
    def test_wrong_file(self):
        self.assertRaises(a.SourceError,a.origin,a.URL.replace(".s001",".s002"))
    def test_nonhttps(self):
        self.assertRaises(a.SourceError,a.origin,a.URL.replace("https:","http:"))
    def test_host_spoof(self):
        self.assertRaises(a.SourceError,a.origin,a.URL.replace("journals.plos.org","fake.plos.org"))
    def test_query_leak(self):
        self.assertRaises(a.SourceError,a.origin,a.URL+"&token=PRIVATE")
    def test_200_content_length_only(self):
        x=a.safe_header_result(200,None,"text/csv; charset=utf-8","999123")
        self.assertEqual(x["publisher_content_length_if_bounded"],999123)
        self.assertEqual(x["original_S1_body_bytes_read"],0)
        self.assertEqual(x["publisher_content_type_class"],"POSSIBLE_CSV_OR_BINARY")
    def test_cdn_redirect_host_no_path_or_query_export(self):
        x=a.safe_header_result(302,"https://static-content.springer.com/private/a?SIGNED_PRIVATE=token")
        self.assertEqual(x["PLOS_file_delivery_hostname_only"],"static-content.springer.com")
        self.assertNotIn("SIGNED_PRIVATE",str(x))
        self.assertFalse(x["whole_redirect_URL_path_query_exported"])
    def test_http_redirect_denied(self):
        self.assertRaises(a.SourceError,a.safe_header_result,302,"http://cdn.plos.org/object")
    def test_userinfo_redirect_denied(self):
        self.assertRaises(a.SourceError,a.safe_header_result,302,"https://pass:word@cdn.plos.org/file")
    def test_fragment_redirect_denied(self):
        self.assertRaises(a.SourceError,a.safe_header_result,302,"https://cdn.plos.org/file#secret")
    def test_port_redirect_denied(self):
        self.assertRaises(a.SourceError,a.safe_header_result,302,"https://cdn.plos.org:444/file")
    def test_403_no_source_content(self):
        x=a.safe_header_result(403,None)
        self.assertEqual(x["original_publisher_HTTP_code"],403)
        self.assertEqual(x["original_S1_body_bytes_read"],0)
        self.assertFalse(x["original_human_action_or_actor_source_values_accessed"])
if __name__=="__main__":unittest.main()
