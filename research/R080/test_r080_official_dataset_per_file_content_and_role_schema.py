"""R080 original published Mendeley v1 metadata/content safe fixture checks."""
import unittest,json
from r080_official_dataset_per_file_content_and_role_schema import (
 safe_official_download_url,metadata_overview,safe_structure,
 parse_script_semantics,DOI,MAX_ITEM,BASE
)
def md(files,version=1,doi=DOI):
 return {"version":version,"doi":{"id":doi},"files":files}
def fil(name,folder="x",size=200,sha="a"*64):
 return {"filename":name,"folder_id":folder,"id":"fake-1234",
         "size":size,"content_details":{"sha256_hash":sha,
          "download_url":"https://prod-source.s3.amazonaws.com/signed?Authorization=SECRET"}}
class SafeSourceTests(unittest.TestCase):
 def test_01_DOI(self):self.assertEqual(DOI,"10.17632/t963ktp6ft.1")
 def test_02_metadata_endpoint_official(self):self.assertEqual(BASE,"https://data.mendeley.com/public-api/datasets/t963ktp6ft")
 def test_03_size_cap(self):self.assertLessEqual(MAX_ITEM,6_000_000)
 def test_04_official_s3(self):self.assertTrue(safe_official_download_url("https://s3.amazonaws.com/public/a?X-Amz-Secret=abc"))
 def test_05_official_mendeley(self):self.assertTrue(safe_official_download_url("https://data.mendeley.com/file"))
 def test_06_evil_url_rejected(self):self.assertFalse(safe_official_download_url("https://evil.com/track"))
 def test_07_evil_mendeley_subdomain_suffix_rejected(self):self.assertFalse(safe_official_download_url("https://mendeley.com.bad.com/"))
 def test_08_http_rejected(self):self.assertFalse(safe_official_download_url("http://data.mendeley.com/file"))
 def test_09_bad_type_rejected(self):self.assertFalse(safe_official_download_url({}))
 def test_10_basic_metadata(self):
  r=metadata_overview(md([fil("research/raw/exp1/a.json")]))
  self.assertEqual(r["file_extensions"]["json"],1)
  self.assertEqual(r["sha256_published_in_file_content_details_count"],1)
 def test_11_duplicate_file_in_different_folder_allowed(self):
  self.assertEqual(metadata_overview(md([fil("a.json","f1"),fil("a.json","f2")]))["original_file_count"],2)
 def test_12_duplicate_same_folder_rejected(self):
  with self.assertRaisesRegex(ValueError,"DUPLICATE"):
   metadata_overview(md([fil("a.json","f1"),fil("a.json","f1")]))
 def test_13_version_two_failclosed(self):
  with self.assertRaisesRegex(ValueError,"REQUIRED_MENDELEY_PUBLIC_V1"):
   metadata_overview(md([],version=2))
 def test_14_wrong_doi_failclosed(self):
  with self.assertRaisesRegex(ValueError,"ORIGINAL_AUTHOR_DOI"):
   metadata_overview(md([],doi="10.17632/other.1"))
 def test_15_missing_files_failclosed(self):
  with self.assertRaisesRegex(ValueError,"ORIGINAL_AUTHOR_DOI"):
   metadata_overview({"doi":{"id":DOI},"version":1})
 def test_16_no_published_signed_urls_echo(self):
  s=str(metadata_overview(md([fil("a.json")])))
  self.assertNotIn("SECRET",s)
  self.assertNotIn("Authorization",s)
 def test_17_file_names_not_published(self):
  s=str(metadata_overview(md([fil("person_id_423.json")])))
  self.assertNotIn("person_id_423",s)
 def test_18_json_dict_no_values(self):
  x=safe_structure(b'{"persons":[{"name":"SECRET_HUMAN"}],"links":[[1,2]]}')
  self.assertNotIn("SECRET_HUMAN",str(x))
  self.assertIn("persons",str(x))
 def test_19_json_list_no_values(self):
  x=safe_structure(b'[{"patient":"secret"}]')
  self.assertNotIn("secret",str(x))
 def test_20_mask_numeric_identity_as_key(self):
  x=safe_structure(b'{"person123456":{"age":20},"group":[1]}')
  self.assertNotIn("person123456",str(x))
 def test_21_invalid_json(self):
  self.assertFalse(safe_structure(b"{broken}")["valid_JSON"])
 def test_22_script_sees_bot_terms(self):
  a=parse_script_semantics(b"# human bot node network\nexp1 bot human")
  self.assertEqual(a["keyword_source_statement_occurrences"]["bot"],2)
 def test_23_source_script_no_content_lines(self):
  a=parse_script_semantics(b"foo = 'SECRET_PASSWORD'\nnode=1")
  self.assertNotIn("SECRET_PASSWORD",str(a))
 def test_24_folder_partition_not_identity(self):
  o=metadata_overview(md([fil("x.json","session1"),fil("x.json","session2")]))
  self.assertEqual(len(o["folder_partition_extension_counts_unnamed"]),2)
  self.assertNotIn("session1",str(o))
if __name__=="__main__":unittest.main()
