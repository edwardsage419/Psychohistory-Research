"""R101 A6 pure synthetic SURF S3 signer and redirect fail-closed tests."""
import unittest
import urllib.request
from unittest.mock import patch
import r101_phase_a6_dataverse_surf_signed_zip_sha_only as s

def signed(**overrides):
    params={
        "X-Amz-Algorithm":"AWS4-HMAC-SHA256",
        "X-Amz-Credential":"fake/synthetic/credential",
        "X-Amz-Date":"20261017T120000Z",
        "X-Amz-Expires":"3600",
        "X-Amz-Signature":"a"*64,
        "X-Amz-SignedHeaders":"host",
        "response-content-disposition":"attachment",
        "response-content-type":"application/zip",
    }
    params.update(overrides)
    from urllib.parse import urlencode
    return "https://objectstore.surf.nl/store/dataset/folder/opaque?"+urlencode(params)

class TestA6(unittest.TestCase):
    def test_exact_pub_signed_target(self):
        self.assertTrue(s.validate_signed_target(signed()))
    def test_untrusted_host(self):
        self.assertRaises(s.ArchiveGateError,s.validate_signed_target,signed().replace("objectstore.surf.nl","evil.example"))
    def test_bad_scheme(self):
        self.assertRaises(s.ArchiveGateError,s.validate_signed_target,signed().replace("https:","http:"))
    def test_signed_key_disallowed(self):
        self.assertRaises(s.ArchiveGateError,s.validate_signed_target,signed(Forbidden="secret"))
    def test_bad_signature(self):
        self.assertRaises(s.ArchiveGateError,s.validate_signed_target,signed(**{"X-Amz-Signature":"garbage"}))
    def test_bad_expiry(self):
        self.assertRaises(s.ArchiveGateError,s.validate_signed_target,signed(**{"X-Amz-Expires":"999999"}))
    def test_wrong_path(self):
        self.assertRaises(s.ArchiveGateError,s.validate_signed_target,signed().replace("/store/","/private/"))
    def test_wrong_number_of_segments(self):
        self.assertRaises(s.ArchiveGateError,s.validate_signed_target,signed().replace("/folder/","/"))
    def test_additional_port(self):
        self.assertRaises(s.ArchiveGateError,s.validate_signed_target,signed().replace("surf.nl","surf.nl:8443"))
    def test_once_only(self):
        handler=s.OneExactPublisherRedirect()
        req=urllib.request.Request(s.URL)
        redirect=handler.redirect_request(req,None,303,"See Other",{},signed())
        self.assertEqual(handler.count,1)
        self.assertEqual(redirect.full_url,signed())
        self.assertRaises(s.ArchiveGateError,handler.redirect_request,redirect,None,303,"Again",{},signed())
    def test_unrelated_initiator_rejected(self):
        req=urllib.request.Request("https://dataverse.nl/api/access/datafile/383978")
        self.assertRaises(s.ArchiveGateError,s.OneExactPublisherRedirect().redirect_request,req,None,303,"See Other",{},signed())
    def test_302_rejected(self):
        req=urllib.request.Request(s.URL)
        self.assertRaises(s.ArchiveGateError,s.OneExactPublisherRedirect().redirect_request,req,None,302,"Moved",{},signed())
    def test_no_source_attempt_in_testing(self):
        self.assertEqual(s.OFFICIAL_BYTES,2247187)
        self.assertEqual(s.TARGET,"objectstore.surf.nl")

if __name__=="__main__":
    unittest.main()
