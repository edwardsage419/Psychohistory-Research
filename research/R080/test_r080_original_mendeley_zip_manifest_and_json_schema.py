"""R080 original network ZIP safe schema-only audit tests (no humans)."""
from __future__ import annotations
import io,zipfile,json,unittest
from r080_original_mendeley_zip_manifest_and_json_schema import (
 URL,MAX_COMPRESSED,classify_zip,summarize_json_structure,summarize_archive,read_original_zip,
)
def fixture(files):
 f=io.BytesIO()
 with zipfile.ZipFile(f,"w",compression=zipfile.ZIP_DEFLATED) as z:
  for p,d in files.items():z.writestr(p,d)
 return f.getvalue()
class Tests(unittest.TestCase):
 def test_01_source_locked(self):self.assertEqual(URL,"https://data.mendeley.com/datasets/t963ktp6ft/1/files/download.zip")
 def test_02_source_guard(self):
  with self.assertRaisesRegex(ValueError,"MUST_BE_FIXED_OFFICIAL"):
   read_original_zip("https://evil.example/people.zip")
 def test_03_size_guard(self):self.assertLessEqual(MAX_COMPRESSED,200_000_000)
 def test_04_raw_exp1_path(self):
  x=classify_zip("v1/data/raw/exp1/s1.json")
  self.assertTrue(x["exp1"]);self.assertTrue(x["raw"]);self.assertEqual(x["extension"],"json")
 def test_05_raw_exp2_path(self):
  x=classify_zip("v1/data/raw/exp2/s1.json")
  self.assertTrue(x["exp2"]);self.assertTrue(x["raw"])
 def test_06_r_script(self):self.assertTrue(classify_zip("code/stats.R")["code"])
 def test_07_other_unknown_extension(self):self.assertEqual(classify_zip("readme.toy")["extension"],"OTHER")
 def test_08_safely_parse_top_level_dict(self):
  r=summarize_json_structure(json.dumps({"experiment":"person-secret","action":[{"id":"danger"}]}).encode())
  self.assertIn("experiment",r["top_level_keys"])
  self.assertNotIn("person-secret",str(r))
  self.assertNotIn("danger",str(r))
 def test_09_nested_length_without_values(self):
  r=summarize_json_structure(b'{"nodes":[{"person":"x"}],"events":[{},{}]}')
  self.assertEqual(r["top_level_container_cardinalities"]["nodes"],1)
  self.assertEqual(r["top_level_container_cardinalities"]["events"],2)
 def test_10_list_records_keys_no_person_values(self):
  r=summarize_json_structure(b'[{"id": "person_private", "bot":true}]')
  self.assertEqual(r["first_record_field_value_types"]["bot"],"bool")
  self.assertNotIn("person_private",str(r))
 def test_11_sanitizes_top_keys(self):
  r=summarize_json_structure(json.dumps({"private/person123":"n","good":"x"}).encode())
  self.assertEqual(r["top_level_keys"],["good"])
 def test_12_invalid_json_clean(self):
  self.assertEqual(summarize_json_structure(b"{oops}")["parses_as_json"],False)
 def test_13_simple_list(self):
  self.assertEqual(summarize_json_structure(b"[1,2,3]")["top_level_length"],3)
 def test_14_no_zip_false(self):
  with self.assertRaisesRegex(ValueError,"NOT_VALID_ARCHIVE"):
   summarize_archive(b"fake")
 def test_15_real_fixture_manifest(self):
  f=fixture({"v1/data/raw/exp1/g1.json":b'{"nodes":{},"people":[1,2]}',
     "v1/data/raw/exp2/g2.json":b'{"bots":[1,2]}',
     "v1/code/main.R":b"# Human bot node edge network choice cooperate\n"})
  r=summarize_archive(f)
  self.assertEqual(r["file_extension_count"]["json"],2)
  self.assertTrue(r["has_exp1_raw_JSON"]);self.assertTrue(r["has_exp2_raw_JSON"])
 def test_16_archive_emits_zero_raw_ids(self):
  f=fixture({"data/raw/exp1/private_person_identifier_123.json":b'{"private_id":"HIDDEN","events":[42]}'})
  r=summarize_archive(f)
  self.assertNotIn("private_person_identifier",str(r))
  self.assertNotIn("HIDDEN",str(r))
 def test_17_source_hash_stable(self):
  b=fixture({"code/a.R":b"# test"})
  self.assertEqual(summarize_archive(b)["original_zip_sha256"],summarize_archive(b)["original_zip_sha256"])
 def test_18_no_causal_claims_from_archive(self):
  r=summarize_archive(fixture({"data/raw/exp1/x.json":b'{"human":"x"}'}))
  self.assertFalse(r["original_human_node_types_independently_mapped"])
  self.assertFalse(r["original_network_edges_and_partner_timings_independently_mapped"])
 def test_19_no_model_score_from_archive(self):
  r=summarize_archive(fixture({"data/raw/exp2/z.json":b'{"bot":true}'}))
  self.assertEqual(r["first_real_model_or_network_scores"],"NOT_RUN")
 def test_20_garbage_member_json_flag(self):
  r=summarize_archive(fixture({"data/raw/exp1/z.json":b"not-json"}))
  self.assertFalse(r["sanitized_one_per_area_JSON_schema_without_values"]["exp1"]["parses_as_json"])
 def test_21_no_raw_zip_path_echoed(self):
  r=summarize_archive(fixture({"data/raw/exp1/study-person-161.json":b'[]'}))
  self.assertNotIn("study-person-161",str(r))
 def test_22_code_R_hash_no_R_content_echo(self):
  r=summarize_archive(fixture({"code/scripts.R":b"# secret_file_content\nbot node edge network\n"}))
  self.assertNotIn("secret_file_content",str(r))
 def test_23_no_faking_64_networks(self):
  r=summarize_archive(fixture({"data/raw/exp1/x.json":b"[]"}))
  self.assertFalse(r["human_64_networks_recounted"])
 def test_24_no_person_rows_exported(self):
  r=summarize_archive(fixture({"data/raw/exp1/x.json":b'[{"id":123}]'}))
  self.assertFalse(r["raw_participant_ids_or_actions_exported"])
if __name__=="__main__":unittest.main()
