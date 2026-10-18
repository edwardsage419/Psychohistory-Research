"""R109 A1 2016 true publisher MD5 and exact Figshare S3 source synthetic checks."""
import hashlib,unittest
from unittest.mock import patch
import r109_phase_a1_2016_true_Guelph_Figshare_5611125_publisher_MD5_double_SHA_header_only as s

def metadata():
    return {"id":3545937,"files":[{"id":5611125,
        "name":"Barclay_Raihani_data supplement.csv","size":13127,
        "computed_md5":"86970b375515176e299686b1b6f70310",
        "download_url":s.ORIGINAL,"PRIVATE_AUTHOR_ID":"PRIVATE_PERSON"}]}
def fake():
    return (b"actor,partner,round,action\n"+(b"PRIVATE_PERSON,PRIVATE_PEER,1,PRIVATE_ACTION\n"*60))
def fake_verified(b):
    with patch.object(s,"PUBLISHED_SIZE",len(b)),patch.object(s,"PUBLISHED_MD5",hashlib.md5(b).hexdigest()):
        return s.source_header_only(b)

class R109Pub(unittest.TestCase):
    def test_source_API_exact(self):s.exact_meta(s.META)
    def test_source_file_exact(self):s.exact_downloader(s.ORIGINAL)
    def test_untrusted_API_host_refused(self):
        self.assertRaises(s.SourceError,s.exact_meta,s.META.replace("api.figshare.com","untrusted.example"))
    def test_wrong_file_refused(self):
        self.assertRaises(s.SourceError,s.exact_downloader,s.ORIGINAL.replace("5611125","5611126"))
    def test_article_official_meta_matches(self):
        self.assertTrue(s.official_metadata_accept(metadata()))
    def test_altered_official_MD5_refused(self):
        m=metadata();m["files"][0]["computed_md5"]="a"*32
        self.assertRaises(s.SourceError,s.official_metadata_accept,m)
    def test_signed_delegate_from_exact_host_accepted(self):
        self.assertEqual(s.approved_final("https://s3-eu-west-1.amazonaws.com/ob?SIGNED_PRIVATE=token"),"verified_figshare_s3_delegate")
    def test_unknown_delegate_host_refused(self):
        self.assertRaises(s.SourceError,s.approved_final,"https://s3-us-west-2.amazonaws.com/ob")
    def test_fake_MD5_cannot_pass(self):
        self.assertRaises(s.SourceError,s.source_header_only,fake())
    def test_valid_synthetic_hash_header_no_actor_cells(self):
        x=fake_verified(fake())
        self.assertEqual(x["header_column_count_no_original_header_labels_exported"],4)
        self.assertFalse(x["original_source_human_actor_partner_action_cells_accessed"])
        self.assertNotIn("PRIVATE_PEER",repr(x))
    def test_full_double_original_identical_source(self):
        b=fake()
        with patch.object(s,"PUBLISHED_SIZE",len(b)),patch.object(s,"PUBLISHED_MD5",hashlib.md5(b).hexdigest()):
            x=s.two_authenticated_originals(b,b)
        self.assertTrue(x["two_official_full_original_downloads_identical"])
    def test_double_different_bytes_blocked(self):
        b=fake();bad=b.replace(b"PRIVATE_ACTION",b"PRIVATE_ACTI0N")
        with patch.object(s,"PUBLISHED_SIZE",len(b)),patch.object(s,"PUBLISHED_MD5",hashlib.md5(b).hexdigest()):
            self.assertRaises(s.SourceError,s.two_authenticated_originals,b,bad)
    def test_html_source_blocked_even_if_digest_synthetic(self):
        b=b"<html>unauthorized</html>\n"*60
        self.assertRaises(s.SourceError,fake_verified,b)
    def test_header_empty_and_duplicate_class_only(self):
        b=b"x,,x,choice\n"+b"P,0,0,1\n"*100
        x=fake_verified(b)
        self.assertEqual(x["anonymous_header_empty_name_count"],1)
        self.assertEqual(x["anonymous_header_duplicate_name_count"],1)
    def test_original_source_private_values_not_exported(self):
        r=repr(fake_verified(fake()))
        self.assertNotIn("PRIVATE_PERSON",r)
        self.assertNotIn("PRIVATE_ACTION",r)
if __name__=="__main__":unittest.main()
