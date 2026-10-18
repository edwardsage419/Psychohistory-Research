"""R108 A0 university publisher Figshare file metadata only pure synthetics."""
import unittest
import r108_phase_a0_2017_Leicester_Figshare_publisher_files_metadata_only as a

def fixture():
    return {
        "id":10194938,
        "email":"PRIVATE_AUTHOR_EMAIL",
        "files":[
            {"id":123456,"name":"Repeated Prisoner's Dilemma_raw data-data.csv",
             "size":35670,"computed_md5":"a"*32,"download_url":"https://UNTRUSTED/private"},
            {"id":123457,"name":"Repeated Prisoner's Dilemma_instructions.pdf","size":10100},
        ],
    }

class FigshareMetadata(unittest.TestCase):
    def test_original_UK_metadata_URL(self):a.safe_url(a.URL)
    def test_untrusted_API_host(self):
        self.assertRaises(a.SourceError,a.safe_url,a.URL.replace("api.figshare.com","untrusted.example"))
    def test_untrusted_item_id(self):
        self.assertRaises(a.SourceError,a.safe_url,a.URL.replace("10194938","10194935"))
    def test_nonhttps_source(self):
        self.assertRaises(a.SourceError,a.safe_url,a.URL.replace("https:","http:"))
    def test_query_token_refused(self):
        self.assertRaises(a.SourceError,a.safe_url,a.URL+"?token=private")
    def test_synthetic_official_public_file_catalog(self):
        x=a.sanitize_publisher_metadata(fixture())
        self.assertEqual(x["official_file_count"],2)
        self.assertEqual(x["source_publishable_sanitized_file_metadata"][0]["publisher_file_bytes"],35670)
        self.assertFalse(x["original_csv_entire_bytes_downloaded"])
        self.assertEqual(x["actual_human_model_scores"],0)
    def test_private_author_or_download_URL_not_exported(self):
        x=a.sanitize_publisher_metadata(fixture())
        self.assertNotIn("PRIVATE_AUTHOR_EMAIL",repr(x))
        self.assertNotIn("UNTRUSTED",repr(x))
    def test_official_md5_only_reported_not_source_verified(self):
        x=a.sanitize_publisher_metadata(fixture())
        p=x["source_publishable_sanitized_file_metadata"][0]
        self.assertEqual(p["original_publisher_reported_MD5_not_yet_verified"],"a"*32)
        self.assertNotIn("verified_against_source",p)
    def test_malformed_publisher_md5_not_released(self):
        o=fixture();o["files"][0]["computed_md5"]="unsafe_tag"
        x=a.sanitize_publisher_metadata(o)
        self.assertNotIn("original_publisher_reported_MD5_not_yet_verified",x["source_publishable_sanitized_file_metadata"][0])
    def test_wrong_publisher_record_denied(self):
        o=fixture();o["id"]=42
        self.assertRaises(a.SourceError,a.sanitize_publisher_metadata,o)
    def test_bad_filename_denied(self):
        o=fixture();o["files"][0]["name"]="../../private.csv"
        self.assertRaises(a.SourceError,a.sanitize_publisher_metadata,o)
    def test_absent_original_csv_denied(self):
        o=fixture();o["files"]=o["files"][1:]
        self.assertRaises(a.SourceError,a.sanitize_publisher_metadata,o)
    def test_file_id_wrong_type_denied(self):
        o=fixture();o["files"][0]["id"]="42"
        self.assertRaises(a.SourceError,a.sanitize_publisher_metadata,o)

if __name__=="__main__":unittest.main()
