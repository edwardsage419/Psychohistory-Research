"""Synthetic-only tests: no respondent rows or original survey files shipped."""
import io
import zipfile
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from r066_larson_lewis_public_schema import (
    scan_tabular,scan_r_script,scan_docx,digest,safe_header,parse_metadata,audit_files,
    FILES,DATE_RELEASED
)


def docx_fixture():
    b=io.BytesIO()
    with zipfile.ZipFile(b,"w") as f:
        f.writestr("word/document.xml",
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:body><w:p><w:r><w:t>Attitude codebook</w:t></w:r></w:p>'
            '<w:tbl><w:tr><w:tc><w:p><w:r><w:t>baseline</w:t></w:r></w:p></w:tc></w:tr></w:tbl>'
            '</w:body></w:document>')
    return b.getvalue()


def metadata(sizes):
    return {"status":"OK","data":{"latestVersion":{
        "versionNumber":1,"versionMinorNumber":0,"versionState":"RELEASED",
        "releaseTime":DATE_RELEASED,"license":{"name":"CC0 1.0"},
        "files":[{"restricted":False,"dataFile":{"id":id_,"filename":name,
                                              "filesize":sizes[key]}}
                 for key,(name,id_,_) in FILES.items()]}}}


class FileSchemaSyntheticTests(unittest.TestCase):
    def test_tab_valid(self):
        x=scan_tabular(b"subject_id\tbaseline_attitude\tendline_attitude\nfake1\t2\t4\nfake2\t3\t5\n")
        self.assertEqual(x["rows"],2)
        self.assertEqual(x["columns"],3)
        self.assertEqual(x["candidate_fieldnames"],["subject_id","baseline_attitude","endline_attitude"])

    def test_tab_does_not_publish_values(self):
        x=scan_tabular(b"subject_id\tbaseline\nSECRET_ID_012\t8\n")
        self.assertNotIn("SECRET_ID_012",str(x))

    def test_duplicate_columns_fails(self):
        with self.assertRaises(ValueError):
            scan_tabular(b"attitude\tattitude\n1\t2\n")

    def test_row_width_fails(self):
        with self.assertRaises(ValueError):
            scan_tabular(b"a\tb\n1\n")

    def test_empty_columns_fails(self):
        with self.assertRaises(ValueError):
            scan_tabular(b"a\t\n1\t2\n")

    def test_empty_table_fails(self):
        with self.assertRaises(ValueError):
            scan_tabular(b"column_a\tcolumn_b\n")

    def test_bad_binary_fails(self):
        with self.assertRaises(UnicodeError):
            scan_tabular(b"a\n\xff")

    def test_safe_header_redacts_unusual_names(self):
        self.assertEqual(safe_header("sensitive@email"),"[unusual-header-redacted]")

    def test_r_script_aggregate_counts_only(self):
        q=scan_r_script(b"# read.csv network attitude network\n")
        self.assertEqual(q["safe_search_counts"]["network"],2)
        self.assertEqual(q["line_count"],1)

    def test_docx_valid(self):
        q=scan_docx(docx_fixture())
        self.assertEqual(q["tables"],1)
        self.assertEqual(q["safe_keyword_counts"]["attitude"],1)

    def test_docx_bad_zip(self):
        with self.assertRaises(ValueError):
            scan_docx(b"not-a-ZIP")

    def test_catalog_version_drift_fails(self):
        x=metadata({k:v[2] for k,v in FILES.items()})
        x["data"]["latestVersion"]["versionNumber"]=2
        with self.assertRaises(ValueError):
            parse_metadata(x)

    def test_catalog_license_drift_fails(self):
        x=metadata({k:v[2] for k,v in FILES.items()})
        x["data"]["latestVersion"]["license"]["name"]="unknown"
        with self.assertRaises(ValueError):
            parse_metadata(x)

    def test_catalog_missing_file_fails(self):
        x=metadata({k:v[2] for k,v in FILES.items()})
        x["data"]["latestVersion"]["files"].pop()
        with self.assertRaises(ValueError):
            parse_metadata(x)

    def test_aggregate_audit_only_source_structure(self):
        raw={
            "data":b"subject_id\tbaseline_attitude\nSECRET_A\t2\n",
            "script":b"read.table network\n",
            "codebook":docx_fixture(),
        }
        with TemporaryDirectory() as temp:
            root=Path(temp)
            for label,(name,_,_) in FILES.items():
                (root/name).write_bytes(raw[label])
            altered={key:(value[0],value[1],len(raw[key]))
                     for key,value in FILES.items()}
            # The pinned sizes cannot be changed silently in production. A
            # synthetic fixture replaces them only within this controlled test.
            with patch("r066_larson_lewis_public_schema.FILES",altered):
                x=audit_files(root,metadata({k:len(v) for k,v in raw.items()}))
        self.assertEqual(x["source_integrity"],"SOURCE_SCHEMA_PASS")
        self.assertEqual(x["files"]["data"]["sha256"],digest(raw["data"]))
        self.assertNotIn("SECRET_A",str(x))
        self.assertFalse(x["fit_performed"])


if __name__=="__main__":
    unittest.main()
