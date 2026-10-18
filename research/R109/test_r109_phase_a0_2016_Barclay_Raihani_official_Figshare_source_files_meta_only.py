"""R109 pure synthetic official 2016 human repeated PD dataset Figshare catalog tests."""
import unittest
import r109_phase_a0_2016_Barclay_Raihani_official_Figshare_source_files_meta_only as a

def sample():
    return {"id":3545937,"private_email":"PRIVATE_AUTHOR_CONTACT",
        "files":[
            {"id":13559321,"name":"Partner choice human game raw data.csv","size":200000,
             "computed_md5":"A"*32,
             "download_url":"https://private.invalid/SIGNED_PII"},
            {"id":13559322,"name":"Instructions.pdf","size":60000}
        ]}

class R109OriginalPublisherOnly(unittest.TestCase):
    def test_pinned_publisher_api(self):a.exact_publisher_url(a.URL)
    def test_wrong_host_denied(self):
        self.assertRaises(a.SourceError,a.exact_publisher_url,a.URL.replace("api.figshare.com","untrusted.example"))
    def test_http_denied(self):
        self.assertRaises(a.SourceError,a.exact_publisher_url,a.URL.replace("https:","http:"))
    def test_wrong_record_denied(self):
        self.assertRaises(a.SourceError,a.exact_publisher_url,a.URL.replace("3545937","3545938"))
    def test_token_query_denied(self):
        self.assertRaises(a.SourceError,a.exact_publisher_url,a.URL+"?token=PRIVATE")
    def test_exact_dataset_file_meta(self):
        r=a.source_catalog_only(sample())
        self.assertEqual(r["official_record_file_count"],2)
        self.assertEqual(r["allowlisted_publisher_source_files_meta_only"][0]["published_original_source_bytes"],200000)
        self.assertFalse(r["original_human_action_or_pair_rows_accessed"])
        self.assertEqual(r["actual_human_model_scores"],0)
    def test_private_contact_and_signed_url_not_exported(self):
        s=str(a.source_catalog_only(sample()))
        self.assertNotIn("SIGNED_PII",s)
        self.assertNotIn("PRIVATE_AUTHOR_CONTACT",s)
    def test_MD5_metadata_not_verified_source(self):
        x=a.source_catalog_only(sample())["allowlisted_publisher_source_files_meta_only"][0]
        self.assertEqual(x["published_original_MD5_unverified_against_source"],"a"*32)
        self.assertNotIn("MD5_verified_against_original",x)
    def test_wrong_article_id_refused(self):
        m=sample();m["id"]=999
        self.assertRaises(a.SourceError,a.source_catalog_only,m)
    def test_bad_filename_refused(self):
        m=sample();m["files"][0]["name"]="../private.csv"
        self.assertRaises(a.SourceError,a.source_catalog_only,m)
    def test_missing_behavior_data_asset_refused(self):
        m=sample();m["files"]=m["files"][1:]
        self.assertRaises(a.SourceError,a.source_catalog_only,m)
    def test_invalid_file_id_refused(self):
        m=sample();m["files"][0]["id"]="private"
        self.assertRaises(a.SourceError,a.source_catalog_only,m)
    def test_malformed_md5_not_exported(self):
        m=sample();m["files"][0]["computed_md5"]="PRIVATE_HASH"
        r=a.source_catalog_only(m)
        self.assertNotIn("PRIVATE_HASH",repr(r))
if __name__=="__main__":unittest.main()
