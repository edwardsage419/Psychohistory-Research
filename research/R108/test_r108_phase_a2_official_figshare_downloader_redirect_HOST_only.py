"""R108 A2 no-body Figshare downloader redirect host-only privacy synthetics."""
import unittest
import r108_phase_a2_official_figshare_downloader_redirect_HOST_only as a

class HostOnly(unittest.TestCase):
    def test_figshare_delegate(self):
        x=a.summarize_location(302,"https://downloads.figshare.com/files/18370526?token=PRIVATE")
        self.assertEqual(x["redirect_target_host_family"],"figshare")
        self.assertNotIn("PRIVATE",str(x))
    def test_s3_delegate(self):
        x=a.summarize_location(302,"https://bucket.s3.eu-west-1.amazonaws.com/path?signature=PRIVATE")
        self.assertEqual(x["redirect_target_host_family"],"amazon_s3")
        self.assertNotIn("PRIVATE",str(x))
    def test_cloudfront(self):
        self.assertEqual(a.summarize_location(307,"https://abc.cloudfront.net/obj")["redirect_target_host_family"],"cloudfront")
    def test_unrecognized_only_not_authorized(self):
        self.assertEqual(a.summarize_location(302,"https://external.example/files/1")["redirect_target_host_family"],"unrecognized")
    def test_http_refused(self):
        self.assertRaises(a.SourceError,a.summarize_location,302,"http://bucket.s3.amazonaws.com/secret")
    def test_userinfo_refused(self):
        self.assertRaises(a.SourceError,a.summarize_location,302,"https://username:pass@amazonaws.com/x")
    def test_fragment_refused(self):
        self.assertRaises(a.SourceError,a.summarize_location,301,"https://bucket.s3.amazonaws.com/file#secret")
    def test_wrong_port_refused(self):
        self.assertRaises(a.SourceError,a.summarize_location,302,"https://bucket.s3.amazonaws.com:444/x")
    def test_nolocation_success_no_body(self):
        x=a.summarize_location(200,None)
        self.assertEqual(x["source_original_body_bytes_read"],0)
        self.assertFalse(x["publisher_redirect_target_host_observed"])
    def test_auth_refusal_metadata_only(self):
        x=a.summarize_location(401,None)
        self.assertEqual(x["initial_official_downloader_HTTP_code"],401)
    def test_private_signed_url_not_exported(self):
        x=a.summarize_location(302,"https://signed.s3.amazonaws.com/personal/path?X-Amz-Signature=PRIVATE_SENSITIVE")
        self.assertNotIn("PRIVATE_SENSITIVE",str(x))
        self.assertFalse(x["download_target_full_URL_path_or_signed_query_exported"])
if __name__=="__main__":unittest.main()
