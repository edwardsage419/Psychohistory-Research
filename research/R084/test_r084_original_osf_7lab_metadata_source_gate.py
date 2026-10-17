#!/usr/bin/env python3
"""R084 22 fully synthetic metadata schema and capability-redaction source gates."""
import json,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from r084_original_osf_7lab_metadata_source_gate import (
 PUBLISHED_TOKENS,OSF_NODE,OSF_FILE,OSF_COMPONENT,EXPECTED_UTRECHT_SHA256,
 allow_public_original_https,official_url,metadata_summary,list_summary,
 sanitized_error,urllib,MAX_FILES_PER_PAGE)

def mockfile(sha=EXPECTED_UTRECHT_SHA256):
 return {"data":{"id":OSF_FILE,"type":"files","attributes":{
 "name":"Utrecht_sbj.csv","hashes":{"sha256":sha},"size":142000,"version":1},
 "relationships":{"owner":{"data":None}}}}

class SafeURLSource(unittest.TestCase):
 def test_two_published_tokens(self):self.assertEqual(len(PUBLISHED_TOKENS),2)
 def test_api_url_carries_token_privately(self):
  s=official_url("/v2/nodes/tyxfm/",PUBLISHED_TOKENS[0])
  self.assertIn("view_only=",s)
  self.assertTrue(allow_public_original_https(s))
 def test_unknown_token_rejected(self):
  with self.assertRaises(ValueError):official_url("/v2/nodes/tyxfm/","random")
 def test_non_api_path_rejected(self):
  with self.assertRaises(ValueError):official_url("/v1/foo/",PUBLISHED_TOKENS[0])
 def test_http_denied(self):
  with self.assertRaises(ValueError):allow_public_original_https("http://api.osf.io/v2/nodes/tyxfm/")
 def test_github_not_accepted_as_authentic(self):
  with self.assertRaises(ValueError):allow_public_original_https("https://github.com/v2/nodes/tyxfm/")
 def test_userinfo_rejected(self):
  with self.assertRaises(ValueError):allow_public_original_https("https://x@api.osf.io/v2/nodes/tyxfm/")
 def test_wrong_path_rejected(self):
  with self.assertRaises(ValueError):allow_public_original_https("https://api.osf.io/human_data.csv")
 def test_download_osf_not_accepted_in_metadata_only(self):
  with self.assertRaises(ValueError):allow_public_original_https("https://files.osf.io/v1/resources/tyxfm/providers/osfstorage/file")
 def test_fragment_rejected(self):
  with self.assertRaises(ValueError):allow_public_original_https("https://api.osf.io/v2/nodes/tyxfm/#evil")
 def test_port_rejected(self):
  with self.assertRaises(ValueError):allow_public_original_https("https://api.osf.io:443/v2/nodes/tyxfm/")
 def test_replicated_component_allowed(self):
  self.assertTrue(allow_public_original_https("https://api.osf.io/v2/nodes/r7y9n/files/"))
 def test_original_search_card_allowed(self):
  self.assertTrue(allow_public_original_https("https://share.osf.io/trove/index-card/eccbea3d-0a61-4584-92c5-2dec9dd84f6f"))

class MetaParsing(unittest.TestCase):
 def test_authentic_file_metadata_identified(self):
  s=metadata_summary(OSF_FILE,{"http_status":200,"metadata_json":True},mockfile())
  self.assertTrue(s["original_id_match"])
  self.assertTrue(s["indexed_file_sha256_matches"])
 def test_wrong_hash_not_established(self):
  s=metadata_summary(OSF_FILE,{"http_status":200,"metadata_json":True},mockfile("f"*64))
  self.assertFalse(s["indexed_file_sha256_matches"])
 def test_wrong_file_id_not_established(self):
  s=metadata_summary(OSF_FILE,{"http_status":200,"metadata_json":True},{"data":{"id":"wrong","attributes":{}}})
  self.assertFalse(s["original_id_match"])
 def test_null_response(self):
  s=metadata_summary(OSF_FILE,{"http_status":403,"metadata_json":False},None)
  self.assertFalse(s["original_id_match"])
 def test_missing_hash_flag_false(self):
  s=metadata_summary(OSF_FILE,{"http_status":200,"metadata_json":True},{"data":{"id":OSF_FILE,"attributes":{"name":"Utrecht_sbj.csv"}}})
  self.assertFalse(s["indexed_file_sha256_matches"])
 def test_no_release_human_id_in_meta_summary(self):
  s=metadata_summary(OSF_FILE,{"http_status":200,"metadata_json":True},{"data":{"id":OSF_FILE,"attributes":{
    "name":"Utrecht_sbj.csv","raw_participant_id":"private-person"}, "relationships":{}}})
  self.assertNotIn("private-person",json.dumps(s))
 def test_directory_only_allowed_lab_filenames(self):
  obj={"data":[{"attributes":{"name":"Utrecht_sbj.csv"}},
               {"attributes":{"name":"private_subject_123.csv"}},
               {"attributes":{"name":"Oxford_sbj.csv"}}],"links":{"next":None}}
  s=list_summary({"http_status":200,"metadata_json":True},obj)
  self.assertEqual(s["observed_public_csv_filenames"],["Oxford_sbj.csv","Utrecht_sbj.csv"])
 def test_empty_listing_valid(self):
  s=list_summary({"http_status":200,"metadata_json":True},{"data":[]})
  self.assertEqual(s["original_file_listing_count"],0)
 def test_pagination_nonzero(self):
  s=list_summary({"http_status":200,"metadata_json":True},{"data":[],"links":{"next":"https://api.osf.io/v2/nodes"}})
  self.assertTrue(s["original_file_listing_first_page_only"])
 def test_oversize_listing_fails(self):
  s=list_summary({"http_status":200,"metadata_json":True},
        {"data":[{"attributes":{}}]*(MAX_FILES_PER_PAGE+1)})
  self.assertEqual(s["source_gate"],"BAD_OR_OVERSIZE_OSF_FILES_COLLECTION")
 def test_no_echo_published_tokens_in_failure(self):
  try:raise urllib.error.URLError(PUBLISHED_TOKENS[0])
  except urllib.error.URLError as err:r=sanitized_error(err)
  self.assertNotIn(PUBLISHED_TOKENS[0],json.dumps(r))
 def test_sanitized_network_error_has_no_location(self):
  r=sanitized_error(TimeoutError("contains participant-id number 902"))
  self.assertNotIn("902",json.dumps(r))
 def test_http_403_is_explicit_failure(self):
  err=urllib.error.HTTPError("https://api.osf.io",403,"Forbidden",{},None)
  self.assertEqual(sanitized_error(err)["http_status"],403)

if __name__=="__main__":unittest.main()
