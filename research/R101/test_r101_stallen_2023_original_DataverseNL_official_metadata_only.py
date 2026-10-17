"""Pure synthetic R101 DataverseNL original metadata validation; no human source."""
import json
import unittest
import r101_stallen_2023_original_DataverseNL_official_metadata_only as s

def good():
    return json.dumps({"status":"OK","data":{"persistentId":"doi:10.34894/EYFM5L",
        "latestVersion":{"files":[{"dataFile":{"filename":"sample.csv","filesize":100,"md5":"a"*32}},
            {"dataFile":{"filename":"analysis.R","filesize":200}}]}}}).encode()

class SourceMetadataGate(unittest.TestCase):
    def test_url_accepted(self):s.validate_url(s.URL)
    def test_host_not_accepted(self):
        self.assertRaises(s.GateError,s.validate_url,s.URL.replace("dataverse.nl","bad.example"))
    def test_http_not_accepted(self):
        self.assertRaises(s.GateError,s.validate_url,s.URL.replace("https:","http:"))
    def test_wrong_persistent_doi_url_rejected(self):
        self.assertRaises(s.GateError,s.validate_url,s.URL.replace("EYFM5L","OTHER"))
    def test_url_token_rejected(self):
        self.assertRaises(s.GateError,s.validate_url,s.URL+"&key=SECRET")
    def test_actual_shape_synthetic_accepted(self):
        x=s.metadata_only(good())
        self.assertEqual(x["official_dataset_file_count"],2)
        self.assertEqual(x["candidate_text_csv_tsv_count"],1)
        self.assertEqual(x["official_file_metadata_MD5_fields_count"],1)
        self.assertEqual(x["real_file_bytes_downloaded"],0)
        self.assertEqual(x["original_human_model_scores"],0)
        self.assertNotIn("sample.csv",repr(x))
    def test_wrong_response_doi(self):
        self.assertRaises(s.GateError,s.metadata_only,good().replace(b"EYFM5L",b"INTRUDER"))
    def test_not_ok_status(self):
        self.assertRaises(s.GateError,s.metadata_only,good().replace(b'"OK"',b'"ERROR"'))
    def test_missing_files(self):
        self.assertRaises(s.GateError,s.metadata_only,b'{"status":"OK","data":{"persistentId":"doi:10.34894/EYFM5L","latestVersion":{}}}')
    def test_bad_json(self):
        self.assertRaises(s.GateError,s.metadata_only,b"{BAD")
    def test_oversized_metadata(self):
        self.assertRaises(s.GateError,s.metadata_only,b"x"*(s.CAP+1))
    def test_bad_filesize(self):
        self.assertRaises(s.GateError,s.metadata_only,good().replace(b'"filesize": 100',b'"filesize": -10').replace(b'"filesize":100',b'"filesize":-10'))
    def test_wrong_md5(self):
        self.assertRaises(s.GateError,s.metadata_only,good().replace(b'a'*32,b'b'*30))
    def test_traversal_file(self):
        self.assertRaises(s.GateError,s.safe_extension,"../secret.csv")
    def test_unknown_extension_masked(self):
        self.assertEqual(s.safe_extension("samples.unknownx"),"other")

if __name__=="__main__":
    unittest.main()
