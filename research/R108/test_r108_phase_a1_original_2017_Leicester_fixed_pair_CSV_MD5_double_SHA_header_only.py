"""R108 A1 2017 UK publisher source full-MD5 synthetic gates before human choice."""
from __future__ import annotations
import hashlib
import unittest
from unittest.mock import patch

import r108_phase_a1_original_2017_Leicester_fixed_pair_CSV_MD5_double_SHA_header_only as a

def source(header="session,pair,round,decision"):
    return (header+"\n"+("PRIVATE_SESSION,PRIVATE_PAIR,1,PRIVATE_ACTION\n"*60)).encode()

def synthetic_verified(blob):
    with patch.object(a,"EXPECTED_SIZE",len(blob)),\
         patch.object(a,"EXPECTED_MD5",hashlib.md5(blob).hexdigest()):
        return a.authentic_original_header_only(blob)

def article():
    return {"id":10194938,"files":[
        {"id":18370526,"name":a.FILENAME,"size":a.EXPECTED_SIZE,
         "computed_md5":a.EXPECTED_MD5,"download_url":a.SOURCE}
    ]}

class R108PublisherExactOriginal(unittest.TestCase):
    def test_exact_article_route(self):a.strict_url(a.METADATA,"metadata")
    def test_exact_source_route(self):a.strict_url(a.SOURCE,"source")
    def test_wrong_origin(self):
        self.assertRaises(a.SourceError,a.strict_url,a.SOURCE.replace("ndownloader.figshare.com","evil.example"),"source")
    def test_query_rejected(self):
        self.assertRaises(a.SourceError,a.strict_url,a.SOURCE+"?secret=1","source")
    def test_cross_article_source(self):
        self.assertRaises(a.SourceError,a.strict_url,a.METADATA.replace("10194938","10194935"),"metadata")
    def test_author_official_catalog_verified(self):
        self.assertTrue(a.validate_article_original_file_catalog(article()))
    def test_unexpected_author_download_link_refused(self):
        x=article();x["files"][0]["download_url"]="https://unknown.org/private"
        self.assertRaises(a.SourceError,a.validate_article_original_file_catalog,x)
    def test_author_md5_tamper_refused(self):
        x=article();x["files"][0]["computed_md5"]="f"*32
        self.assertRaises(a.SourceError,a.validate_article_original_file_catalog,x)
    def test_fake_actual_MD5_never_accepted(self):
        self.assertRaises(a.SourceError,a.authentic_original_header_only,source())
    def test_syn_verified_header_only_no_human_row(self):
        x=synthetic_verified(source())
        self.assertEqual(x["original_CSV_physical_data_lines_unparsed"],60)
        self.assertFalse(x["original_participant_or_choice_cells_dereferenced"])
        self.assertNotIn("PRIVATE_PAIR",repr(x))
        self.assertEqual(x["original_human_model_scores"],0)
    def test_two_complete_independent_source_replay(self):
        b=source()
        with patch.object(a,"EXPECTED_MD5",hashlib.md5(b).hexdigest()),\
             patch.object(a,"EXPECTED_SIZE",len(b)):
            x=a.verified_source_pair(b,b)
        self.assertTrue(x["two_independent_official_publisher_downloads_byte_identical"])
    def test_different_data_fails_even_if_size_same(self):
        b=source();other=b.replace(b"PRIVATE_ACTION",b"PRIVATE_ACTI0N")
        with patch.object(a,"EXPECTED_MD5",hashlib.md5(b).hexdigest()),\
             patch.object(a,"EXPECTED_SIZE",len(b)):
            self.assertRaises(a.SourceError,a.verified_source_pair,b,other)
    def test_header_duplicate_refused(self):
        self.assertRaises(a.SourceError,synthetic_verified,source(header="session,pair,round,pair"))
    def test_binary_embedded_nul_refused(self):
        self.assertRaises(a.SourceError,synthetic_verified,source()+b"\x00")
    def test_html_source_refused(self):
        self.assertRaises(a.SourceError,synthetic_verified,b"<html>Unauthorized</html>\n"*50)
if __name__=="__main__":unittest.main()
