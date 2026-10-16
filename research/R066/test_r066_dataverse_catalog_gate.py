"""R066 catalog availability synthetic tests, no HTTP."""
import unittest
from unittest.mock import patch
from r066_dataverse_catalog_gate import (
    DATASETS, parse_dataset_api, sanitize_public_filename, citation_field, fetch_dataset
)


def fixture():
    return {
        "status":"OK",
        "data":{"persistentUrl":"https://doi.org/10.7910/DVN/RAHSVM",
            "latestVersion":{
                "versionNumber":1,"versionMinorNumber":0,
                "versionState":"RELEASED","releaseTime":"2026-10-01T12:00:00Z",
                "license":{"name":"CC0 1.0","uri":"https://creativecommons.org/publicdomain/zero/1.0/"},
                "metadataBlocks":{"citation":{"fields":[
                    {"typeName":"title","value":"Sample replication metadata"}]}},
                "files":[{"label":"network.tsv",
                          "restricted":False,
                          "dataFile":{"filename":"network.tsv","id":7,
                                      "filesize":12345,"contentType":"text/tab-separated-values"}}],
            },
        },
    }


class CatalogContracts(unittest.TestCase):
    def test_released_version_verified(self):
        r=parse_dataset_api(200,fixture(),DATASETS["larson_lewis_2026"])
        self.assertEqual(r["status"],"PUBLIC_PUBLISHED_METADATA_VERIFIED")
        self.assertEqual(r["file_count"],1)
        self.assertEqual(r["files"][0]["filename"],"network.tsv")
        self.assertEqual(r["version_major"],1)

    def test_valid_control_uses_same_contract(self):
        r=parse_dataset_api(200,fixture(),DATASETS["klar_2016_control"])
        self.assertEqual(r["status"],"PUBLIC_PUBLISHED_METADATA_VERIFIED")

    def test_missing_http404_explicit_api(self):
        r=parse_dataset_api(404,{"status":"ERROR","message":"No such dataset"},
                            DATASETS["larson_lewis_2026"])
        self.assertEqual(r["status"],"NOT_FOUND_OR_UNREGISTERED")

    def test_404_without_valid_api_is_unresolved(self):
        r=parse_dataset_api(404,None,DATASETS["larson_lewis_2026"])
        self.assertEqual(r["status"],"RESPONSE_SCHEMA_UNRESOLVED")

    def test_api_500_does_not_become_missing(self):
        self.assertEqual(parse_dataset_api(503,None,"doi:x")["status"],
                         "NETWORK_OR_UPSTREAM_UNRESOLVED")

    def test_rate_limit(self):
        self.assertEqual(parse_dataset_api(429,None,"doi:x")["status"],
                         "NETWORK_OR_UPSTREAM_UNRESOLVED")

    def test_forbidden(self):
        self.assertEqual(parse_dataset_api(403,None,"doi:x")["status"],
                         "DRAFT_OR_RESTRICTED_METADATA")

    def test_draft_is_not_published(self):
        x=fixture()
        x["data"]["latestVersion"]["versionState"]="DRAFT"
        self.assertEqual(parse_dataset_api(200,x,"doi:x")["status"],
                         "DRAFT_OR_RESTRICTED_METADATA")

    def test_no_latest_version_schema_fails(self):
        x=fixture()
        del x["data"]["latestVersion"]
        self.assertEqual(parse_dataset_api(200,x,"doi:x")["status"],
                         "RESPONSE_SCHEMA_UNRESOLVED")

    def test_no_files_cannot_publish_claim(self):
        x=fixture()
        del x["data"]["latestVersion"]["files"]
        self.assertEqual(parse_dataset_api(200,x,"doi:x")["status"],
                         "RESPONSE_SCHEMA_UNRESOLVED")

    def test_unverified_status_fails_closed(self):
        x=fixture()
        x["status"]="ERROR"
        self.assertEqual(parse_dataset_api(200,x,"doi:x")["status"],
                         "RESPONSE_SCHEMA_UNRESOLVED")

    def test_untrusted_filename_redacted(self):
        self.assertEqual(sanitize_public_filename("user@example.org/file.csv"),
                         "[redacted-nonstandard-filename]")

    def test_normal_filename_safe(self):
        self.assertEqual(sanitize_public_filename("survey_1.tab"),"survey_1.tab")

    def test_only_approved_DOIs(self):
        with self.assertRaises(ValueError):
            fetch_dataset("doi:10.7910/DVN/DOESNOTEXIST",
                          opener=lambda *args,**kwargs:None)

    def test_metadata_limit(self):
        x=fixture()
        x["data"]["latestVersion"]["files"]*=205
        v=parse_dataset_api(200,x,"doi:x")
        self.assertEqual(len(v["files"]),200)
        self.assertTrue(v["file_metadata_truncated"])

    def test_metadata_title_fetch(self):
        self.assertEqual(citation_field(fixture()["data"]["latestVersion"],"title"),
                         "Sample replication metadata")


if __name__=="__main__":
    unittest.main()
