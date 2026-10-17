"""R101 A3 synthetic-only public ZIP index contract tests."""
import copy
import json
import unittest
import r101_phase_a3_official_dataverse_nine_zip_public_catalog_only as s


def fixture():
    sizes=[4000000]*8+[11631177]
    files=[]
    for i,n in enumerate(sizes):
        files.append({"dataFile":{"id":100+i,"filename":f"research_{i+1}.zip","filesize":n},"description":"Archive of study files"})
    return {"status":"OK","data":{"latestVersion":{"datasetPersistentId":"doi:10.34894/EYFM5L","files":files}}}


def serialized(x):
    return json.dumps(x).encode()


class PublicSourceIndexSynthetic(unittest.TestCase):
    def test_good_catalog(self):
        x=s.public_zip_inventory(serialized(fixture()))
        self.assertEqual(x["official_file_count"],9)
        self.assertEqual(x["official_total_file_bytes"],43631177)
        self.assertEqual(len(x["public_file_metadata"]),9)
        self.assertFalse(x["accessed_original_human_action_values"])
        self.assertEqual(x["score_count_actual_human"],0)
    def test_duplicate_id_rejected(self):
        f=fixture()
        f["data"]["latestVersion"]["files"][1]["dataFile"]["id"]=100
        self.assertRaises(s.GateError,s.public_zip_inventory,serialized(f))
    def test_wrong_doi_rejected(self):
        f=fixture()
        f["data"]["latestVersion"]["datasetPersistentId"]="doi:10.34894/FAKE"
        self.assertRaises(s.GateError,s.public_zip_inventory,serialized(f))
    def test_bad_filename_traversal_rejected(self):
        f=fixture()
        f["data"]["latestVersion"]["files"][0]["dataFile"]["filename"]="../danger.zip"
        self.assertRaises(s.GateError,s.public_zip_inventory,serialized(f))
    def test_filename_abs_rejected(self):
        self.assertIsNone(s.FILENAME.fullmatch("/outside.zip"))
    def test_missing_one_file_rejected(self):
        f=fixture()
        f["data"]["latestVersion"]["files"].pop()
        self.assertRaises(s.GateError,s.public_zip_inventory,serialized(f))
    def test_mismatched_total_rejected(self):
        f=fixture()
        f["data"]["latestVersion"]["files"][0]["dataFile"]["filesize"]=3
        self.assertRaises(s.GateError,s.public_zip_inventory,serialized(f))
    def test_non_zip_rejected(self):
        f=fixture()
        f["data"]["latestVersion"]["files"][0]["dataFile"]["filename"]="private.csv"
        self.assertRaises(s.GateError,s.public_zip_inventory,serialized(f))
    def test_unsafe_description_withheld(self):
        f=fixture()
        f["data"]["latestVersion"]["files"][0]["description"]="alice@example.com"
        x=s.public_zip_inventory(serialized(f))
        target=[z for z in x["public_file_metadata"] if z["official_public_datafile_id"]==100][0]
        self.assertTrue(target["description_withheld_due_to_safety"])
        self.assertIsNone(target["official_public_file_description_sanitized"])
        self.assertNotIn("alice@",str(x))
    def test_strict_official_api_host(self):
        self.assertRaises(s.GateError,s.validate_url,"https://bad.example/api/datasets/:persistentId?persistentId=doi%3A10.34894%2FEYFM5L")
    def test_fabricated_checksum_rejected(self):
        f=fixture()
        f["data"]["latestVersion"]["files"][0]["dataFile"]["md5"]="NOT_MD5"
        self.assertRaises(s.GateError,s.public_zip_inventory,serialized(f))
    def test_metadata_does_not_become_real_file(self):
        x=s.public_zip_inventory(serialized(fixture()))
        self.assertEqual(x["downloaded_original_file_payload_bytes"],0)
        self.assertEqual(x["PESEN_v0_1"],"FROZEN")


if __name__=="__main__":
    unittest.main()
