"""R108 A3 original official Figshare verified delegated S3 host, pure synthetic."""
import unittest
import urllib.request
import r108_phase_a3_verified_Figshare_publisher_S3_delegate_MD5_double_source as r
import r108_phase_a1_original_2017_Leicester_fixed_pair_CSV_MD5_double_SHA_header_only as a

def check(link):
    request=urllib.request.Request(a.SOURCE)
    return r.VerifiedSingleDelegate().redirect_request(
        request,None,302,"Found",{},link)

class FrozenOfficialS3(unittest.TestCase):
    def test_exact_observed_302_host(self):
        req=check("https://s3-eu-west-1.amazonaws.com/object?X-Amz-Signature=SYNTH")
        self.assertEqual(req.get_method(),"GET")
    def test_wrong_storage_host_fails(self):
        self.assertRaises(a.SourceError,check,"https://s3-us-west-2.amazonaws.com/object")
    def test_spoofed_host_fails(self):
        self.assertRaises(a.SourceError,check,"https://s3-eu-west-1.amazonaws.com.evil.org/object")
    def test_unsigned_http_fails(self):
        self.assertRaises(a.SourceError,check,"http://s3-eu-west-1.amazonaws.com/object")
    def test_redirect_with_credentials_fails(self):
        self.assertRaises(a.SourceError,check,"https://user:pass@s3-eu-west-1.amazonaws.com/object")
    def test_redirect_with_fragment_fails(self):
        self.assertRaises(a.SourceError,check,"https://s3-eu-west-1.amazonaws.com/object#secret")
    def test_wrong_port_fails(self):
        self.assertRaises(a.SourceError,check,"https://s3-eu-west-1.amazonaws.com:404/object")
    def test_chained_second_redirect_fails(self):
        deleg=r.VerifiedSingleDelegate()
        new_req=urllib.request.Request("https://s3-eu-west-1.amazonaws.com/temporary?token=SYNTH")
        self.assertRaises(a.SourceError,deleg.redirect_request,new_req,None,302,"Found",{},"https://s3-eu-west-1.amazonaws.com/other")
    def test_final_exact_host_verified_without_releasing_query(self):
        self.assertTrue(r.allowed_final_url("https://s3-eu-west-1.amazonaws.com/path?Secret=PRIVATE"))
        self.assertRaises(a.SourceError,r.allowed_final_url,"https://other.example/path")
    def test_initial_source_still_publisher_pinned(self):
        a.strict_url(a.SOURCE,"source")
        self.assertEqual(r.SIGNED_DELEGATE,"s3-eu-west-1.amazonaws.com")
if __name__=="__main__":unittest.main()
