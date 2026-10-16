"""R072 REV002 synthetic strict publisher signed-object chain and XLSX audit."""
import io
import unittest
from zipfile import ZipFile,ZIP_DEFLATED
from urllib.parse import quote

from r072_plos_s8_signed_redirect_rev002 import (
  valid_delegated_target,permitted_redirect,INITIAL_URL,
  NarrowPublisherRedirect,audit,
)

SIGNED_BASE=("https://storage.googleapis.com"
             "/plos-corpus-prod/10.1371/journal.pone.0152076/1/pone.0152076.s008.xlsx")
SIGNATURE="?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=plos-synthetic%40example&X-Goog-Date=20261016T101500Z&X-Goog-Expires=86400&X-Goog-Signature=abcdef123"
TARGET=SIGNED_BASE+SIGNATURE


def synthetic_zip():
    f=io.BytesIO()
    with ZipFile(f,"w",compression=ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",b"<Types/>")
        z.writestr("xl/workbook.xml",b"<workbook/>")
    return f.getvalue()


class PublisherOriginRev002Tests(unittest.TestCase):
    def test_exact_plos_bucket_version_and_file(self):
        self.assertTrue(valid_delegated_target(TARGET))

    def test_version_may_be_two_digits_but_only_numeric(self):
        self.assertTrue(valid_delegated_target(TARGET.replace("/1/","/23/")))
        self.assertFalse(valid_delegated_target(TARGET.replace("/1/","/head/")))

    def test_different_bucket_rejected(self):
        self.assertFalse(valid_delegated_target(TARGET.replace("plos-corpus-prod","untrusted-bucket")))

    def test_different_paper_rejected(self):
        self.assertFalse(valid_delegated_target(TARGET.replace("0152076/1","0159999/1")))

    def test_different_supplement_rejected(self):
        self.assertFalse(valid_delegated_target(TARGET.replace(".s008.xlsx",".s007.xlsx")))

    def test_unsigned_object_not_permitted(self):
        self.assertFalse(valid_delegated_target(SIGNED_BASE))

    def test_missing_signature_key_rejected(self):
        self.assertFalse(valid_delegated_target(TARGET.replace("&X-Goog-Signature=abcdef123","")))

    def test_duplicated_signature_param_rejected(self):
        self.assertFalse(valid_delegated_target(TARGET+"&X-Goog-Signature=evil"))

    def test_wrong_signed_algorithm_rejected(self):
        self.assertFalse(valid_delegated_target(TARGET.replace("GOOG4-RSA-SHA256","UNVERIFIED")))

    def test_expiration_over_single_day_rejected(self):
        self.assertFalse(valid_delegated_target(TARGET.replace("Expires=86400","Expires=86401")))

    def test_expiration_zero_rejected(self):
        self.assertFalse(valid_delegated_target(TARGET.replace("Expires=86400","Expires=0")))

    def test_http_downgrade_rejected(self):
        self.assertFalse(valid_delegated_target(TARGET.replace("https://","http://")))

    def test_html_path_escape_rejected(self):
        self.assertFalse(valid_delegated_target(TARGET.replace("/1/","/%2E%2E/")))

    def test_impersonator_custom_google_host_rejected(self):
        self.assertFalse(valid_delegated_target(TARGET.replace("storage.googleapis.com","storage.googleapis.com.attacker.test")))

    def test_signed_link_only_when_from_trusted_publisher_origin(self):
        self.assertTrue(permitted_redirect(INITIAL_URL,TARGET))
        self.assertFalse(permitted_redirect("https://evil.test/file",TARGET))
        self.assertFalse(permitted_redirect(TARGET,TARGET))

    def test_other_random_cloud_object_never_whitelisted(self):
        self.assertFalse(permitted_redirect(INITIAL_URL,"https://storage.googleapis.com/unrelated/x.xlsx"))
        self.assertFalse(permitted_redirect(INITIAL_URL,SIGNED_BASE))

    def test_same_publisher_redirect_allowed(self):
        self.assertTrue(permitted_redirect(INITIAL_URL,"https://dx.plos.org/10.1371/journal.pone.0152076.s008"))

    def test_redirect_handler_rejects_second_cloud_redirect(self):
        # If cloud object redirects to another URL, this must fail without
        # any HTTP fetch or user-provided signed link becoming trusted.
        h=NarrowPublisherRedirect()
        from urllib.request import Request
        r=Request(TARGET)
        with self.assertRaisesRegex(ValueError,"REJECTED_REDIRECT"):
            h.redirect_request(r,None,302,"move",{},TARGET)

    def test_binary_receipt_contains_no_signed_query_or_spreadsheet_rows(self):
        x=audit(synthetic_zip(),"PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT")
        self.assertEqual(x["status"],"E2_PLOS_S8_SOURCE_BYTES_VERIFIED")
        self.assertEqual(x["raw_original_bytes"],len(synthetic_zip()))
        self.assertNotIn("X-Goog-Signature",str(x))
        self.assertFalse(x["real_workbook_cells_read"])
        self.assertEqual(x["real_human_behavior_model_e2"],
                         "BLOCKED_EXPERIMENT_RULE_AND_DATA_DICTIONARY")

    def test_no_fake_source_mode(self):
        with self.assertRaises(ValueError):
            audit(synthetic_zip(),"SOME_THIRD_PARTY_ARCHIVE")

    def test_bogus_html_not_xlsx(self):
        with self.assertRaises(ValueError):
            audit(b"<html>forbidden</html>"+b"x"*80,
                  "PLOS_PUBLISHER_DELEGATED_SIGNED_OBJECT")

    def test_legacy_failure_not_rewritten(self):
        z=audit(synthetic_zip(),"PLOS_DIRECT_PUBLISHER")
        self.assertEqual(z["original_previous_run_38921163855"],
                         "HISTORIC_SOURCE_UNRESOLVED_NOT_REWRITTEN")


if __name__=="__main__":unittest.main()
