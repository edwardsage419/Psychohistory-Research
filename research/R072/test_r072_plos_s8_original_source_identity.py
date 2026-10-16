"""Publisher-source binary-only supplementary XLSX safety tests; NO real participants."""
import io
import unittest
from zipfile import ZipFile,ZIP_DEFLATED
from r072_plos_s8_original_source_identity import audit_bytes,allowed_official_url


def sample(missing_workbook=False,extra=None,large=False):
    f=io.BytesIO()
    with ZipFile(f,"w",compression=ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",b"<Types/>")
        if not missing_workbook:z.writestr("xl/workbook.xml",b"<workbook/>")
        if extra:
            for name,value in extra:
                z.writestr(name,value)
        if large:z.writestr("xl/huge_blob.txt",b"X"*3_000_001)
    return f.getvalue()


URL="https://journals.plos.org/plosone/article/file?id=10.1371/journal.pone.0152076.s008&type=supplementary"


class S8ByteGateTests(unittest.TestCase):
    def test_synthetic_ooxml_package_bytes_only(self):
        x=audit_bytes(sample(),URL)
        self.assertEqual(x["status"],"E2_PUBLISHED_HUMAN_SOURCE_BYTES_VERIFIED")
        self.assertFalse(x["original_sheet_or_member_rows_read"])
        self.assertFalse(x["R072_four_agent_indirect_reciprocity_mechanism_fitted"])

    def test_publisher_and_doi_https_hosts_only(self):
        for x in (URL,"https://doi.org/10.1371/journal.pone.0152076.s008",
                  "https://plos.org/a"):
            self.assertTrue(allowed_official_url(x))
        for x in ("http://doi.org/x","https://plos.org.evil.org",
                  "https://private.example.org","file:///tmp/a"):
            self.assertFalse(allowed_official_url(x))

    def test_fake_publisher_url_rejected(self):
        with self.assertRaises(ValueError):
            audit_bytes(sample(),"https://archive.example.com/real.xlsx")

    def test_html_instead_of_xlsx_rejected(self):
        with self.assertRaisesRegex(ValueError,"NOT_OPEN_XML"):
            audit_bytes(b"<html>"+b"x"*100,URL)

    def test_empty_source_does_not_pass(self):
        with self.assertRaisesRegex(ValueError,"SHORT"):
            audit_bytes(b"",URL)

    def test_missing_workbook_rejected(self):
        with self.assertRaisesRegex(ValueError,"NOT_XLSX_WORKBOOK"):
            audit_bytes(sample(missing_workbook=True),URL)

    def test_macros_not_accepted_even_if_zip_valid(self):
        raw=sample(extra=[("xl/vbaProject.bin",b"bad")])
        with self.assertRaisesRegex(ValueError,"ACTIVE_OR_EXTERNAL"):
            audit_bytes(raw,URL)

    def test_external_links_not_accepted(self):
        raw=sample(extra=[("xl/externalLinks/externalLink1.xml",b"x")])
        with self.assertRaisesRegex(ValueError,"ACTIVE_OR_EXTERNAL"):
            audit_bytes(raw,URL)

    def test_large_uncompressed_payload_rejected_even_if_small_zip(self):
        raw=sample(large=True)
        with self.assertRaisesRegex(ValueError,"UNCOMPRESSED"):
            audit_bytes(raw,URL)

    def test_many_zip_members_rejected(self):
        raw=sample(extra=[(f"xl/x{i}",b"a") for i in range(59)])
        with self.assertRaisesRegex(ValueError,"MEMBER_COUNT"):
            audit_bytes(raw,URL)

    def test_unexpected_large_raw_bytes_rejected(self):
        with self.assertRaisesRegex(ValueError,"OVER_BUDGET"):
            audit_bytes(b"PK\x03\x04"+b"X"*600_000,URL)

    def test_full_binary_sha_is_not_a_row_or_user_id(self):
        x=audit_bytes(sample(),URL)
        self.assertEqual(len(x["raw_publisher_file_sha256"]),64)
        self.assertNotIn("rows",x)
        self.assertFalse(x["participant_rows_exported"])

    def test_no_google_or_third_party_scraped_filename(self):
        with self.assertRaisesRegex(ValueError,"SOURCE_NOT_OFFICIAL"):
            audit_bytes(sample(),"https://cdn.thirdparty.net/reputation-data.xlsx")


if __name__=="__main__":
    unittest.main()
