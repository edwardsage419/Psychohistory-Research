"""R100 Phase A: synthetic-only; never access real Zenodo participants."""
import hashlib
import io
import unittest
import zipfile

import r100_2025_original_threshold_pgg_zenodo_xlsx_source_directory_only as a


def synthetic_xlsx(names=None, workbook=None, extra=None):
    names = names if names is not None else [f"synthetic_{i}" for i in range(10)]
    workbook = workbook if workbook is not None else ('<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheets>' + "".join(f'<sheet name="{n}" sheetId="{i+1}"/>' for i,n in enumerate(names)) + '</sheets></workbook>').encode()
    out = io.BytesIO()
    with zipfile.ZipFile(out, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "<Types/>")
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/worksheets/sheet1.xml", "<sheet>PRIVATE_ACTION_123</sheet>")
        for n, value in extra or []:
            z.writestr(n, value)
    return out.getvalue()


class PureSyntheticTests(unittest.TestCase):
    def test_official_url(self): a.validate_url(a.URL)
    def test_external_host(self):
        with self.assertRaises(a.SourceError): a.validate_url(a.URL.replace("zenodo.org", "evil.example"))
    def test_redirect_rejected_before_following_external_host(self):
        handler = a.ExactOfficialOriginRedirect()
        req = __import__("urllib.request", fromlist=["Request"]).Request(a.URL)
        with self.assertRaises(a.SourceError):
            handler.redirect_request(req, None, 302, "Moved", {}, "https://untrusted.example/secret")

    def test_redirect_rejected_before_following_wrong_official_path(self):
        handler = a.ExactOfficialOriginRedirect()
        req = __import__("urllib.request", fromlist=["Request"]).Request(a.URL)
        with self.assertRaises(a.SourceError):
            handler.redirect_request(req, None, 302, "Moved", {}, "https://zenodo.org/other/path")

    def test_wrong_http(self):
        with self.assertRaises(a.SourceError): a.validate_url(a.URL.replace("https:", "http:"))
    def test_unapproved_query(self):
        with self.assertRaises(a.SourceError): a.validate_url(a.URL + "&token=a")
    def test_fragment(self):
        with self.assertRaises(a.SourceError): a.validate_url(a.URL + "#x")
    def test_fake_original_rejected(self):
        with self.assertRaises(a.SourceError): a.verify_bytes(synthetic_xlsx())
    def test_synthetic_md5_sha(self):
        b = synthetic_xlsx()
        x = a.verify_bytes(b, hashlib.md5(b).hexdigest())
        self.assertTrue(x["publisher_MD5_verified"])
        self.assertEqual(x["computed_original_SHA256"], hashlib.sha256(b).hexdigest())
    def test_zero_size(self):
        with self.assertRaises(a.SourceError): a.verify_bytes(b"")
    def test_file_too_large(self):
        with self.assertRaises(a.SourceError): a.verify_bytes(b"x" * (a.MAX_SOURCE + 1))
    def test_sheets_and_no_private_action(self):
        x = a.workbook_directory_only(synthetic_xlsx())
        self.assertEqual(x["original_workbook_sheet_count"], 10)
        self.assertNotIn("PRIVATE_ACTION_123", repr(x))
        self.assertFalse(x["worksheet_xml_read"])
    def test_only_nine_sheets(self):
        with self.assertRaises(a.SourceError): a.workbook_directory_only(synthetic_xlsx(names=[str(i) for i in range(9)]))
    def test_duplicate_sheet_name(self):
        with self.assertRaises(a.SourceError): a.workbook_directory_only(synthetic_xlsx(names=["dup"] * 10))
    def test_corrupt_zip(self):
        with self.assertRaises(a.SourceError): a.workbook_directory_only(b"PKfail")
    def test_zip_path_traversal(self):
        with self.assertRaises(a.SourceError): a.workbook_directory_only(synthetic_xlsx(extra=[("../outside", "x")]))
    def test_zip_duplicate_path(self):
        with self.assertRaises(a.SourceError): a.workbook_directory_only(synthetic_xlsx(extra=[("xl/workbook.xml", "x")]))
    def test_zip_bomb_many_files(self):
        with self.assertRaises(a.SourceError): a.workbook_directory_only(synthetic_xlsx(extra=[(f"junk{i}", "x") for i in range(310)]))
    def test_xml_entity(self):
        with self.assertRaises(a.SourceError): a.workbook_directory_only(synthetic_xlsx(workbook=b'<!DOCTYPE root [<!ENTITY foo "bar">]><workbook/>'))
    def test_no_namespace(self):
        with self.assertRaises(a.SourceError): a.workbook_directory_only(synthetic_xlsx(workbook=b"<workbook><sheets/></workbook>"))


if __name__ == "__main__":
    unittest.main()
