"""R101 A4 pure synthetic full-source size, archive safety and zero-value tests."""
import io
import unittest
import zipfile
from unittest.mock import patch
import r101_phase_a4_real_original_zip_sha_directory_only as s

def fakezip(files, *, compression=zipfile.ZIP_DEFLATED):
    out=io.BytesIO()
    with zipfile.ZipFile(out,"w",compression=compression) as z:
        for name, data in files:
            z.writestr(name,data)
    return out.getvalue()

def evaluate(blob):
    with patch.object(s,"OFFICIAL_BYTES",len(blob)):
        return s.directory_only(blob)

class TestR101A4(unittest.TestCase):
    def test_exact_official_url_accepted(self):
        s.validate_source_url(s.URL)
    def test_untrusted_datafile_id_rejected(self):
        with self.assertRaises(s.ArchiveGateError):
            s.validate_source_url(s.URL.replace("383977","383978"))
    def test_bad_domain_rejected(self):
        with self.assertRaises(s.ArchiveGateError):
            s.validate_source_url(s.URL.replace("dataverse.nl","fake.example"))
    def test_extra_query_rejected(self):
        with self.assertRaises(s.ArchiveGateError):
            s.validate_source_url(s.URL+"?format=original")
    def test_anonymous_extension_directory_only(self):
        b=fakezip([("data/group.csv","PERSON123,PRIVATEACTION123"),("docs/codebook.txt","SECRET123")])
        out=evaluate(b)
        self.assertEqual(out["candidate_csv_tsv_txt_member_count"],2)
        self.assertEqual(out["zip_central_directory_members"],2)
        self.assertFalse(out["any_archive_member_content_read"])
        self.assertNotIn("PERSON123",repr(out))
        self.assertNotIn("group.csv",repr(out))
    def test_duplicate_member_name_rejected(self):
        b=fakezip([("data.csv","a"),("data.csv","b")])
        with self.assertRaises(s.ArchiveGateError):evaluate(b)
    def test_traversal_rejected(self):
        b=fakezip([("../private.csv","person")])
        with self.assertRaises(s.ArchiveGateError):evaluate(b)
    def test_absolute_path_rejected(self):
        b=fakezip([("/private.csv","person")])
        with self.assertRaises(s.ArchiveGateError):evaluate(b)
    def test_wrong_binary_rejected(self):
        with self.assertRaises(s.ArchiveGateError):
            with patch.object(s,"OFFICIAL_BYTES",7):
                s.verified_identity(b"abcdefg")
    def test_size_mismatch_rejected(self):
        b=fakezip([("data.csv","x")])
        with self.assertRaises(s.ArchiveGateError):
            s.verified_identity(b)
    def test_safe_double_source_digest(self):
        b=fakezip([("data.csv","private sample")])
        with patch.object(s,"OFFICIAL_BYTES",len(b)):
            out=s.compare_two_source_copies(b,b)
        self.assertTrue(out["independent_source_download_SHA256_identical"])
        self.assertEqual(out["original_human_scores"],0)
        self.assertEqual(out["PESEN_v0_1"],"FROZEN")
    def test_mismatched_source_sha_rejected(self):
        a=fakezip([("data.csv","1")])
        b=fakezip([("data.csv","2")])
        self.assertEqual(len(a),len(b))
        with patch.object(s,"OFFICIAL_BYTES",len(a)):
            with self.assertRaises(s.ArchiveGateError):
                s.compare_two_source_copies(a,b)
    def test_zip_bomb_ratio_rejected(self):
        b=fakezip([("data.csv","A"*3000000)])
        with self.assertRaises(s.ArchiveGateError):evaluate(b)
    def test_more_than_300_entries_rejected(self):
        b=fakezip([(f"{i}.csv","x") for i in range(301)])
        with self.assertRaises(s.ArchiveGateError):evaluate(b)

if __name__=="__main__":
    unittest.main()
