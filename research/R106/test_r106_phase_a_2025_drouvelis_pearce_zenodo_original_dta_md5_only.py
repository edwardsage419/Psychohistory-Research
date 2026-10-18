"""R106 A synthetic official checksum and no DTA record processing."""
import hashlib
import unittest
from unittest.mock import patch
import r106_phase_a_2025_drouvelis_pearce_zenodo_original_dta_md5_only as a

class SourceSynthetic(unittest.TestCase):
    def test_original_url(self): a.validate_url(a.URL)
    def test_wrong_record_rejected(self):
        self.assertRaises(a.SourceError,a.validate_url,a.URL.replace("15462528","0"))
    def test_host_rejected(self):
        self.assertRaises(a.SourceError,a.validate_url,a.URL.replace("zenodo.org","untrusted.example"))
    def test_http_rejected(self):
        self.assertRaises(a.SourceError,a.validate_url,a.URL.replace("https","http"))
    def test_added_query_rejected(self):
        self.assertRaises(a.SourceError,a.validate_url,a.URL+"&token=secret")
    def test_wrong_file_rejected(self):
        self.assertRaises(a.SourceError,a.validate_url,a.URL.replace("cleandata.dta","other.dta"))
    def test_fake_md5_cannot_be_forged(self):
        self.assertRaises(a.SourceError,a.verify_only,b"<stata_dta>"+b"x"*400)
    def test_synthetic_md5_identity_no_rows(self):
        raw=b"<stata_dta>"+b"x"*400
        with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()):
            out=a.verify_only(raw)
        self.assertTrue(out["original_first_bytes_stata_XML_header_class"])
        self.assertFalse(out["original_human_data_records_or_variables_parsed"])
        self.assertFalse(out["new_independent_recruited_cohort_verified"])
        self.assertEqual(out["real_human_scores"],0)
    def test_binary_class_not_assumed_to_be_XML(self):
        raw=b"\x72\x00"+b"\x00"*400
        with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()):
            out=a.verify_only(raw)
        self.assertFalse(out["original_first_bytes_stata_XML_header_class"])
    def test_zero_bytes_rejected(self):
        self.assertRaises(a.SourceError,a.verify_only,b"")
    def test_oversize_rejected(self):
        self.assertRaises(a.SourceError,a.verify_only,b"x"*(a.CAP+1))
    def test_consent_and_source_cohort_never_inferred(self):
        raw=b"<stata_dta>"+b"PRIVATE_PERSON_ACTION"*50
        with patch.object(a,"OFFICIAL_MD5",hashlib.md5(raw).hexdigest()):
            out=a.verify_only(raw)
        self.assertNotIn("PRIVATE_PERSON_ACTION",repr(out))
        self.assertFalse(out["original_person_session_opponent_cohort_verified"])

if __name__=="__main__":
    unittest.main()
