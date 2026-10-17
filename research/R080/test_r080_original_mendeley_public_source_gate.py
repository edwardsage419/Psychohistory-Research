"""R080 no-real-human public API metadata access test suite."""
from __future__ import annotations
import unittest,json
from r080_original_mendeley_public_source_gate import (
 SOURCE_DOI,SOURCE_ID,HTTP_LIMIT,TARGET_VERSION,PROBE_URLS,ZIP_PROBE_URLS,
 safe_file_descriptor,summarize_official_json,metadata_gate_report,request_public,
)
class Tests(unittest.TestCase):
 def test_01_original_DOI(self):self.assertEqual(SOURCE_DOI,"10.17632/t963ktp6ft.1")
 def test_02_original_ID(self):self.assertEqual(SOURCE_ID,"t963ktp6ft")
 def test_03_original_version_one(self):self.assertEqual(TARGET_VERSION,1)
 def test_04_small_limit(self):self.assertLessEqual(HTTP_LIMIT,1_000_000)
 def test_05_no_synthetic_private_host(self):
  with self.assertRaisesRegex(ValueError,"HOST_NOT_OFFICIAL"):
   request_public("https://evil.example/people.json")
 def test_06_no_synthetic_file_RPI_in_descriptor(self):
  d=safe_file_descriptor({"filename":"raw/exp1/session_192_person_xyz.json","size":500})
  self.assertNotIn("session_192_person_xyz",str(d))
  self.assertEqual(d["extension"],"json")
  self.assertTrue(d["raw_json_candidate"])
 def test_07_detect_exp1_raw_nested(self):
  d=safe_file_descriptor({"path":"data/raw/exp1/p01.json","checksum":"md5:abcdef"})
  self.assertTrue(d["exp1_path_indicator"])
  self.assertTrue(d["raw_path_indicator"])
  self.assertTrue(d["published_hash_present"])
 def test_08_detect_exp2_raw_nested(self):
  d=safe_file_descriptor({"path":"data/raw/exp2/p02.json"})
  self.assertTrue(d["exp2_path_indicator"])
 def test_09_distinguish_analysis_R(self):
  d=safe_file_descriptor({"name":"code/analysis.R","size":120})
  self.assertTrue(d["R_analysis_candidate"])
  self.assertFalse(d["raw_json_candidate"])
 def test_10_do_not_emit_signed_download_links(self):
  d=safe_file_descriptor({"path":"data/raw/exp1/example.json",
   "download_url":"https://signed-storage/?credential=SENSITIVE","size":1})
  self.assertNotIn("SENSITIVE",str(d))
  self.assertNotIn("http",str(d))
 def test_11_bad_descriptor_type_fails(self):
  with self.assertRaisesRegex(ValueError,"INVALID_OFFICIAL_FILE_DESCRIPTOR"):safe_file_descriptor("dangerous")
 def test_12_unknown_extension_sanitized(self):
  self.assertEqual(safe_file_descriptor({"name":"participant_private_dat"})["extension"],"OTHER")
 def test_13_file_metadata_dict_shapes(self):
  d=summarize_official_json({"id":"t963ktp6ft","version":1,"doi":{"id":"10.17632/t963ktp6ft.1"},
   "name":"Bot Cooperation Experiment Dataset","files":[{"path":"data/raw/exp1/session.json","size":100}]})
  self.assertEqual(d["file_descriptors_total"],1)
  self.assertTrue(d["doi_exact_match"])
 def test_14_top_level_leaky_values_not_serialized(self):
  d=summarize_official_json({"id":"t963ktp6ft","my_fake_person":"PERSON_SECRET",
   "files":[{"name":"secret/session.csv"}]})
  self.assertNotIn("PERSON_SECRET",str(d))
  self.assertNotIn("secret/session.csv",str(d))
 def test_15_flat_list_descriptors(self):
  d=summarize_official_json([{"filename":"exp1/a.json","size":5}])
  self.assertEqual(d["outer_count"],1)
  self.assertEqual(len(d["file_descriptors"]),1)
 def test_16_invalid_source_response_fail(self):
  with self.assertRaisesRegex(ValueError,"OFFICIAL_METADATA_NOT_CONTAINER"):summarize_official_json("raw")
 def test_17_null_content_does_not_claim_source_recovered(self):
  p={"official":{"http_status":503,"content_type":"text/html","payload":b""}}
  r=metadata_gate_report(p)
  self.assertFalse(r["exact_full_original_network_JSON_bytes_verified"])
  self.assertEqual(r["metadata_file_descriptors_total"],0)
 def test_18_html_only_does_not_claim_full_source(self):
  r=metadata_gate_report({"official":{"http_status":200,"payload":b"<html>empty</html>"}})
  self.assertEqual(r["R080_real_behavior_model_scores"],"NOT_RUN")
 def test_19_metadata_success_does_not_claim_humans(self):
  p={"api":{"http_status":200,
      "payload":json.dumps({"files":[{"filename":"data/raw/exp1/p.json"}]}).encode()}}
  r=metadata_gate_report(p)
  self.assertEqual(r["descriptors_json_files"],1)
  self.assertFalse(r["human_vs_bot_node_classification_verified"])
  self.assertFalse(r["exact_full_original_network_JSON_bytes_verified"])
 def test_20_no_secret_cache_or_participant_rows(self):
  r=metadata_gate_report({})
  self.assertEqual(r["human_person_rows_exported"],0)
  self.assertEqual(r["PESEN_v0.1"],"FROZEN")
 def test_21_api_probe_has_metadata_and_zip(self):
  self.assertGreaterEqual(len(PROBE_URLS),5)
  self.assertGreaterEqual(len(ZIP_PROBE_URLS),1)
 def test_22_safe_json_no_signed_url_under_typical_shapes(self):
  mock={"id":"t963ktp6ft","files":[{"name":"data/raw/exp2/people_2020.json","download_url":"TOKEN_DO_NOT_PRINT"}]}
  r=metadata_gate_report({"api":{"http_status":200,"payload":json.dumps(mock).encode()}})
  self.assertNotIn("TOKEN_DO_NOT_PRINT",json.dumps(r))
 def test_23_json_disallowed_file_descriptor_fields_hidden(self):
  d=safe_file_descriptor({"name":"data/raw/exp1/f.json","internal_identity":"sensitive_secret"})
  self.assertNotIn("sensitive_secret",str(d))
 def test_24_yet_no_real_score_even_200_api(self):
  mock={"id":"t963ktp6ft","files":[]}
  r=metadata_gate_report({"api":{"http_status":200,"payload":json.dumps(mock).encode()}})
  self.assertEqual(r["R080_real_network_E2"],"OPEN_UNTIL_ORIGINAL_BYTES_AND_HUMAN_BOT_ROLE_GATE")
if __name__=="__main__":unittest.main()
