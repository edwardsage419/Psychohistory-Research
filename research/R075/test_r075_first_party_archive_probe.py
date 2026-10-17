"""R075 source probing cases; all fixtures invented, no participant data."""
import io
import zipfile
import unittest
from r075_first_party_archive_probe import summarize_archive,probe_one,LIMIT,CANDIDATES

def zipped(members):
    b=io.BytesIO()
    with zipfile.ZipFile(b,"w") as z:
        for name,data in members.items():z.writestr(name,data)
    return b.getvalue()

def mock(data,ctype="application/zip",status=200):
    return lambda:(status,ctype,data,"https://www.aeaweb.org/final.zip")

class SourceTests(unittest.TestCase):
    def test_01_expected_official_endpoints(self):
        self.assertGreaterEqual(len(CANDIDATES),4)
    def test_02_nonzip_detected(self):
        self.assertFalse(summarize_archive(b"hello")["is_zip"])
    def test_03_zip_integrity(self):
        a=summarize_archive(zipped({"x/data.csv":"a,b\n1,2\n"}))
        self.assertTrue(a["is_zip"])
        self.assertEqual(a["extension_counts"],{".csv":1})
    def test_04_no_member_names_leak(self):
        result=summarize_archive(zipped({"person_00001.csv":"1","x/session_101.do":"code"}))
        self.assertNotIn("person_00001",str(result))
        self.assertNotIn("session_101",str(result))
    def test_05_html_classified(self):
        self.assertEqual(probe_one("a","https://www.aeaweb.org/",
            reader=mock(b"<html></html>","text/html"))["status"],"HTML_NOT_RAW_ARCHIVE")
    def test_06_zip_classified(self):
        d=probe_one("a","https://www.aeaweb.org/",
            reader=mock(zipped({"x/readme.txt":"abc"})))
        self.assertEqual(d["status"],"ZIP_STRUCTURALLY_ACCESSIBLE_ORIGIN_BYTE_HASHED")
        self.assertEqual(len(d["sha256"]),64)
    def test_07_empty_blocked(self):
        self.assertEqual(probe_one("a","https://www.aeaweb.org/",
            reader=mock(b""))["status"],"EMPTY_RESPONSE")
    def test_08_oversize_blocked(self):
        self.assertEqual(probe_one("a","https://www.aeaweb.org/",
            reader=mock(b"x"*(LIMIT+1)))["status"],"BLOCKED_RESPONSE_TOO_LARGE")
    def test_09_zip_bomb_blocked(self):
        d=probe_one("a","https://www.aeaweb.org/",
            reader=mock(zipped({"large.csv":b"x"*50000001})))
        self.assertEqual(d["status"],"ARCHIVE_VALIDATION_FAILURE")
    def test_10_zip_member_names_unpublished(self):
        d=probe_one("a","https://www.aeaweb.org/",
            reader=mock(zipped({"private/session_993.csv":"participant_id,action"})))
        self.assertNotIn("session_993",str(d))
if __name__=="__main__":unittest.main()
