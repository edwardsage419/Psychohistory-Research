"""R107 A3 pure original Dryad API publisher-MD5 and double source checks."""
import hashlib
import unittest
from unittest.mock import patch
import r107_phase_a3_publisher_md5_official_Dryad_API_alternate_header_only as a

def fake():
    return (b"experiment,person,round,action\n"+b"SYNTHETIC_ONLY,SYNTHETIC_PERSON,1,0\n"*60)

def audited(blob):
    with patch.object(a,"PUBLISHER_MD5",hashlib.md5(blob).hexdigest()),\
         patch.object(a,"PUBLISHER_BYTE_SIZE",len(blob)):
        return a.verify_firstparty_original_blob(blob)

class A3SourceSynthetic(unittest.TestCase):
    def test_exact_url(self):a.validate_url(a.URL)
    def test_http_denied(self):self.assertRaises(a.SourceError,a.validate_url,a.URL.replace("https:","http:"))
    def test_host_denied(self):self.assertRaises(a.SourceError,a.validate_url,a.URL.replace("datadryad.org","evil.example"))
    def test_other_file_denied(self):self.assertRaises(a.SourceError,a.validate_url,a.URL.replace("296893","296894"))
    def test_query_denied(self):self.assertRaises(a.SourceError,a.validate_url,a.URL+"?token=1")
    def test_no_publisher_md5_fake_source(self):self.assertRaises(a.SourceError,a.verify_firstparty_original_blob,fake())
    def test_exact_synthetic_md5_and_size(self):
        x=audited(fake())
        self.assertEqual(x["original_csv_field_count"],4)
        self.assertFalse(x["any_original_human_action_or_person_or_session_value_accessed"])
        self.assertEqual(x["human_model_scores"],0)
    def test_publisher_md5_mismatch_fails(self):
        b=fake()
        with patch.object(a,"PUBLISHER_BYTE_SIZE",len(b)):
            self.assertRaises(a.SourceError,a.verify_firstparty_original_blob,b)
    def test_publisher_byte_count_mismatch_fails(self):
        self.assertRaises(a.SourceError,a.verify_firstparty_original_blob,b"header,field\n")
    def test_publisher_double_byte_identical(self):
        b=fake()
        with patch.object(a,"PUBLISHER_MD5",hashlib.md5(b).hexdigest()),\
             patch.object(a,"PUBLISHER_BYTE_SIZE",len(b)):
            x=a.verified_twice(b,b)
        self.assertTrue(x["two_separate_exact_official_API_downloads_match"])
        self.assertTrue(x["publisher_independent_MD5_available_and_verified"])
    def test_double_mismatch_even_with_synthetic_patched_first_MD5(self):
        b=fake();another=b.replace(b"SYNTHETIC_ONLY",b"SYNTHETIC_ELSE")
        with patch.object(a,"PUBLISHER_MD5",hashlib.md5(b).hexdigest()),\
             patch.object(a,"PUBLISHER_BYTE_SIZE",len(b)):
            self.assertRaises(a.SourceError,a.verified_twice,b,another)
    def test_html_payload_fails_after_synthetic_hash(self):
        b=b"<html><title>denied</title></html>\n"*150
        with patch.object(a,"PUBLISHER_MD5",hashlib.md5(b).hexdigest()),\
             patch.object(a,"PUBLISHER_BYTE_SIZE",len(b)):
            self.assertRaises(a.SourceError,a.verify_firstparty_original_blob,b)
    def test_unsafe_header_fails_after_synthetic_hash(self):
        b=(b"../../secret,person,action\n"+b"p,p,0\n"*500)
        with patch.object(a,"PUBLISHER_MD5",hashlib.md5(b).hexdigest()),\
             patch.object(a,"PUBLISHER_BYTE_SIZE",len(b)):
            self.assertRaises(a.SourceError,a.verify_firstparty_original_blob,b)
    def test_output_no_synthetic_person_values(self):
        s=repr(audited(fake()))
        self.assertNotIn("SYNTHETIC_PERSON",s)

if __name__=="__main__":unittest.main()
