import io
import unittest
from unittest.mock import patch
import r067_dryad_ipd_source_schema as m

class DataAuditTests(unittest.TestCase):
    def test_synthetic_schema_without_person_rows(self):
        a=m.summarize_csv(b"user,round,choice\nSECRET1,1,C\nSECRET2,2,D\n")
        self.assertEqual(a["record_rows"],2)
        self.assertEqual(a["safe_column_names"],["user","round","choice"])
        self.assertNotIn("SECRET",str(a))
        self.assertFalse(a["individual_actions_interpreted"])

    def test_reject_duplicate_column(self):
        with self.assertRaises(ValueError):m.summarize_csv(b"user,user\n1,2\n2,3\n")

    def test_reject_ragged_records(self):
        with self.assertRaises(ValueError):m.summarize_csv(b"a,b\n1\n1,2\n")

    def test_reject_empty_table(self):
        with self.assertRaises(ValueError):m.summarize_csv(b"a,b\n")

    def test_nonstandard_header_redacts(self):
        a=m.summarize_csv(b"user@email.com,round\n1,2\n2,3\n")
        self.assertEqual(a["safe_column_names"][0],"[nonstandard-field]")

    def test_http_error_does_not_become_source(self):
        def fake(url,opener=m.request.urlopen):
            return None,"HTTP_403"
        with patch.object(m,"bounded_get",side_effect=fake):
            result=m.audit_download("fix.csv",1514373)
        self.assertEqual(result["status"],"SOURCE_DOWNLOAD_UNRESOLVED")
        self.assertEqual(len(result["download_paths_tried"]),2)

    def test_valid_fake_source_labeled_not_model_fit(self):
        payload=b"user,round,choice\nFAKE,1,C\nFAKE,2,D\n"
        with patch.object(m,"bounded_get",return_value=(payload,"OK")):
            v=m.audit_download("fix.csv",1514373)
        self.assertEqual(v["status"],"SOURCE_BYTES_PARSED")
        self.assertFalse(v["structure"]["individual_actions_interpreted"])
        self.assertNotIn("FAKE",str(v))

    def test_html_payload_not_counted(self):
        with patch.object(m,"bounded_get",return_value=(b"<html>Login required</html>","OK")):
            v=m.audit_download("fix.csv",1514373)
        self.assertEqual(v["status"],"SOURCE_DOWNLOAD_UNRESOLVED")


if __name__=="__main__":
    unittest.main()
