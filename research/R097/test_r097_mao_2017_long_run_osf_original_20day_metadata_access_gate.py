#!/usr/bin/env python3
"""R097 OSF source-only synthetic; no original actions or IDs."""
import pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r097_mao_2017_long_run_osf_original_20day_metadata_access_gate import (
 NODE,BASE,LIST,validate_catalog_url,extension_group,safe_project_metadata,safe_file_catalog)
def metadata():
 return {"data":{"id":"64z8u","type":"nodes","attributes":{"public":True,"title":"PRIVATE_PROJECT"}}}
def catalog():
 return {"data":[
  {"type":"files","attributes":{"kind":"file","name":"ORIGINAL.csv","size":1200,"extra":{"hashes":{"md5":"abc"}}}},
  {"type":"files","attributes":{"kind":"folder","name":"PRIVATE_ACTOR_FOLDER","size":0}},
  {"type":"files","attributes":{"kind":"file","name":"PRIVATE_UNIQUE_ACTOR_00001.txt","size":300,"extra":{}}}],
  "links":{"next":None}}
class OSFOriginal(unittest.TestCase):
 def test_original_project_id(self):self.assertEqual(NODE,"64z8u")
 def test_project_endpoint(self):self.assertTrue(validate_catalog_url(BASE))
 def test_listing_endpoint(self):self.assertTrue(validate_catalog_url(LIST))
 def test_scope_external_node_rejected(self):
  with self.assertRaises(ValueError):validate_catalog_url(BASE.replace("64z8u","12345"))
 def test_url_http_rejected(self):
  with self.assertRaises(ValueError):validate_catalog_url(BASE.replace("https","http",1))
 def test_url_forged_host(self):
  with self.assertRaises(ValueError):validate_catalog_url(BASE.replace("api.osf.io","api.osf.io.evil"))
 def test_osf_action_download_url_rejected_in_source_phase(self):
  with self.assertRaises(ValueError):validate_catalog_url("https://files.osf.io/v1/resources/64z8u")
 def test_project_true_identity(self):self.assertTrue(safe_project_metadata(metadata())["original_OSF_public_project"])
 def test_project_false_identity_refused(self):
  v=metadata();v["data"]["id"]="other"
  with self.assertRaises(ValueError):safe_project_metadata(v)
 def test_no_project_title_in_output(self):
  self.assertNotIn("PRIVATE_PROJECT",str(safe_project_metadata(metadata())))
 def test_catalog_observation_count(self):
  r,_=safe_file_catalog(catalog());self.assertEqual(r["publisher_listing_file_objects"],3)
 def test_catalog_tabular_count(self):
  r,_=safe_file_catalog(catalog());self.assertEqual(r["publisher_tabular_or_archive_file_candidates"],2)
 def test_catalog_sha_publisher_only(self):
  r,_=safe_file_catalog(catalog());self.assertEqual(r["publisher_hashed_file_count"],1)
 def test_file_name_secret_not_exported(self):
  r,_=safe_file_catalog(catalog());self.assertNotIn("PRIVATE_UNIQUE_ACTOR",str(r))
 def test_source_microdata_not_downloaded(self):
  r,_=safe_file_catalog(catalog());self.assertFalse(r["original_OSF_file_contents_downloaded_or_examined"])
 def test_unsafe_extension(self):self.assertEqual(extension_group("../private.csv"),"UNSAFE_OR_FOLDER")
 def test_unknown_file_extension(self):self.assertEqual(extension_group("actor.image"),"OTHER_FILE_TYPE")
 def test_pagination_next_restricted(self):
  c=catalog();c["links"]["next"]="https://attacker.com/file"
  with self.assertRaises(ValueError):safe_file_catalog(c)
 def test_pagination_original_node_allowed(self):
  c=catalog();c["links"]["next"]=LIST+"&page=2"
  r,n=safe_file_catalog(c);self.assertTrue(n)
 def test_non_files_object_rejected(self):
  c=catalog();c["data"][0]["type"]="users"
  with self.assertRaises(ValueError):safe_file_catalog(c)
 def test_invalid_kind_rejected(self):
  c=catalog();c["data"][0]["attributes"]["kind"]="unknown"
  with self.assertRaises(ValueError):safe_file_catalog(c)
 def test_negative_size_not_added(self):
  c=catalog();c["data"][0]["attributes"]["size"]=-2
  r,_=safe_file_catalog(c);self.assertEqual(r["publisher_total_size_of_files_with_reported_size"],300)
 def test_no_participants_or_sessions_estimated_from_OSF_files(self):
  r,_=safe_file_catalog(catalog())
  self.assertNotIn("participant_count",r)
if __name__=="__main__":unittest.main()
