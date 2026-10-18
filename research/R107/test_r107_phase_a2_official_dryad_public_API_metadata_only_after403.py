"""R107 A2 synthetic official Dryad public JSON metadata-only source safety."""
import unittest
import r107_phase_a2_official_dryad_public_API_metadata_only_after403 as d

class A2Tests(unittest.TestCase):
    def test_dataset_url_exact(self):d.validate_url(d.ROOT+d.PATHS[0])
    def test_file_url_exact(self):d.validate_url(d.ROOT+d.PATHS[1])
    def test_untrusted_host(self):
        self.assertRaises(d.SourceError,d.validate_url,"https://bad.example"+d.PATHS[0])
    def test_untrusted_file_ID(self):
        self.assertRaises(d.SourceError,d.validate_url,d.ROOT+d.PATHS[1].replace("296893","296894"))
    def test_query_block(self):
        self.assertRaises(d.SourceError,d.validate_url,d.ROOT+d.PATHS[0]+"?token=foo")
    def test_published_md5_is_only_unverified_metadata(self):
        row=d.clean_api_response(d.PATHS[1],200,{"digestType":"md5","digest":"a"*32,"path":"DataSet.csv","size":220000})
        self.assertEqual(row["published_digest_algorithm"],"md5")
        self.assertTrue(row["official_file_name_exact_match"])
        self.assertEqual(row["official_file_size_if_published"],220000)
        self.assertNotIn("actual_source_MD5_verified",row)
    def test_bad_digest_refused(self):
        self.assertEqual(d.digest_fields({"digestType":"md5","digest":"PRIVATE_PERSON"}),{})
    def test_different_checksum_sha256(self):
        self.assertEqual(d.digest_fields({"digestType":"sha256","digest":"F"*64})["publisher_reported_unverified_digest"],"f"*64)
    def test_private_author_metadata_not_released(self):
        row=d.clean_api_response(d.PATHS[0],200,{"identifier":"doi:10.5061/dryad.7fq25s8","email":"PRIVATE_EMAIL","human":"PRIVATE_PERSON"})
        self.assertNotIn("PRIVATE_EMAIL",str(row))
        self.assertNotIn("PRIVATE_PERSON",str(row))
        self.assertTrue(row["official_dataset_identifier_exact_match"])
    def test_untrusted_link_not_downloaded_or_exported(self):
        row=d.clean_api_response(d.PATHS[1],200,{"_links":{"bad":{"href":"https://external.example/download/SECRET"}}})
        self.assertFalse(row["published_file_download_exact_official_link_metadata_present"])
        self.assertNotIn("SECRET",str(row))
    def test_original_link_metadata_only(self):
        row=d.clean_api_response(d.PATHS[1],200,{"_links":{"download":{"href":"/downloads/file_stream/296893"}}})
        self.assertTrue(row["published_file_download_exact_official_link_metadata_present"])
    def test_http403_only_safe_code(self):
        row=d.clean_api_response(d.PATHS[1],403,None)
        self.assertEqual(row["public_api_http_code"],403)
        self.assertFalse(row["public_api_response_is_json_object"])
if __name__=="__main__":unittest.main()
