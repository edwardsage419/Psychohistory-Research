"""R101 A5 pure synthetic nofollow redirect metadata tests."""
import unittest
import urllib.request
import r101_phase_a5_no_follow_official_redirect_metadata as m

class TestA5(unittest.TestCase):
    def test_exact_original(self):m.validate_original(m.ORIGINAL)
    def test_other_datafile_rejected(self):
        self.assertRaises(m.RedirectGateError,m.validate_original,m.ORIGINAL.replace("383977","383978"))
    def test_same_host_approved_relative(self):
        x=m.safe_destination("/api/access/datafile/383977?token=secret")
        self.assertEqual(x["redirect_target_host"],"dataverse.nl")
        self.assertEqual(x["redirect_target_query_key_classes"],["token"])
        self.assertNotIn("secret",repr(x))
    def test_external_https_classified_without_follow(self):
        x=m.safe_destination("https://storage.example.org/archive/opaque-file?X-Amz-Signature=SUPERPRIVATE")
        self.assertEqual(x["redirect_target_host"],"storage.example.org")
        self.assertFalse(x["full_redirect_URL_or_query_values_exported"])
        self.assertNotIn("SUPERPRIVATE",repr(x))
    def test_unsafe_http_rejected(self):
        self.assertRaises(m.RedirectGateError,m.safe_destination,"http://storage.example.org/data")
    def test_userinfo_rejected(self):
        self.assertRaises(m.RedirectGateError,m.safe_destination,"https://u:pass@storage.example.org/file")
    def test_foreign_port_rejected(self):
        self.assertRaises(m.RedirectGateError,m.safe_destination,"https://storage.example.org:8443/file")
    def test_no_redirect_follow(self):
        handler=m.NeverFollow()
        req=urllib.request.Request(m.ORIGINAL)
        self.assertIsNone(handler.redirect_request(req,None,302,"Moved",{},"https://other.example/x"))
    def test_oversized_url_rejected(self):
        self.assertRaises(m.RedirectGateError,m.safe_destination,"https://storage.example.org/"+"x"*10000)
    def test_invalid_path_rejected(self):
        self.assertRaises(m.RedirectGateError,m.safe_destination,"https://storage.example.org/"+"x/"*40)
    def test_raw_token_not_exposed(self):
        x=m.safe_destination("https://s3.amazonaws.com/data/private?AccessKey=SUPERSECRET&sig=PRIVATE123")
        self.assertNotIn("SUPERSECRET",repr(x))
        self.assertNotIn("PRIVATE123",repr(x))
        self.assertEqual(x["redirect_target_path_first_segment_class"],"data")

if __name__=="__main__":
    unittest.main()
