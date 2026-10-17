"""R101 A7 pure synthetic bounded final HTTP metadata output tests."""
import unittest
import r101_phase_a7_original_final_http_headers_only as m

class TestA7(unittest.TestCase):
    def test_200_direct_official(self):
        x=m.bounded_final_metadata("https://dataverse.nl/api/access/datafile/383977",200,0,"application/zip","2247187")
        self.assertEqual(x["final_http_host_class"],"dataverse.nl")
        self.assertEqual(x["original_zip_body_bytes_read"],0)
    def test_200_surf_followed(self):
        x=m.bounded_final_metadata("https://objectstore.surf.nl/store/opaque/path/token?X-Amz-Signature=SECRET",200,1,"application/octet-stream","2247187")
        self.assertEqual(x["final_http_host_class"],"objectstore.surf.nl")
        self.assertNotIn("SECRET",str(x))
    def test_nonpublisher_hostname_masked(self):
        x=m.bounded_final_metadata("https://evil.example/path",302,0,"text/html","5")
        self.assertEqual(x["final_http_host_class"],"OTHER")
    def test_invalid_content_type_masked(self):
        x=m.bounded_final_metadata("https://dataverse.nl/x",200,0,"garbage-123","5")
        self.assertEqual(x["final_content_type_class"],"OTHER")
    def test_malformed_length_hidden(self):
        x=m.bounded_final_metadata("https://dataverse.nl/x",200,0,"application/zip","notint")
        self.assertIsNone(x["final_content_length_if_safe"])
    def test_two_redirects_rejected(self):
        with self.assertRaises(m.ArchiveGateError):
            m.bounded_final_metadata("https://dataverse.nl/x",200,2,"application/zip","5")
    def test_noninteger_status_rejected(self):
        with self.assertRaises(m.ArchiveGateError):
            m.bounded_final_metadata("https://dataverse.nl/x","200",0,"application/zip","5")
    def test_source_token_hidden(self):
        x=m.bounded_final_metadata("https://objectstore.surf.nl/path?signed=PRIVATEKEY",200,1,"application/zip","225")
        self.assertNotIn("PRIVATEKEY",repr(x))

if __name__=="__main__":
    unittest.main()
