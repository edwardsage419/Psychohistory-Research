"""All sample XLSX data and IDs here are invented, not human observations."""
from __future__ import annotations
from collections import Counter
from unittest.mock import patch
import hashlib,io,unittest
from zipfile import ZipFile,ZIP_DEFLATED
import r072_plos_s8_column_domains_rev004 as m

NS="http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def workbook(rows,header=("service history","request","another"),extra=None):
    contents=[
      '<row r="1">'+''.join(
         f'<c r="{chr(65+i)}1" t="inlineStr"><is><t>{s}</t></is></c>'
         for i,s in enumerate(header))+'</row>'
    ]
    for rid,cols in rows.items():
        body=""
        for j,item in cols.items():
            col=chr(65+j-1)
            if item is None:continue
            if isinstance(item,str):
                body+=f'<c r="{col}{rid}" t="inlineStr"><is><t>{item}</t></is></c>'
            else:
                body+=f'<c r="{col}{rid}"><v>{item}</v></c>'
        contents.append(f'<row r="{rid}">{body}</row>')
    f=io.BytesIO()
    with ZipFile(f,"w",compression=ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",b"<Types/>")
        z.writestr("xl/workbook.xml",f'<workbook xmlns="{NS}"/>'.encode())
        z.writestr("xl/worksheets/sheet1.xml",
            f'<worksheet xmlns="{NS}"><sheetData>{"".join(contents)}</sheetData></worksheet>'.encode())
        for item,data in (extra or []):z.writestr(item,data)
    return f.getvalue()


def scan(raw):
    with patch.object(m,"EXACT_SHA",hashlib.sha256(raw).hexdigest()):
        return m.scan_rows(raw)


class R072OriginalDomainSafetyTests(unittest.TestCase):
    def test_three_anonymous_nonheader_rows_no_automatic_189(self):
        x=scan(workbook({2:{1:1,2:0},3:{1:0},4:{2:"synthetic-secret"}}))
        self.assertEqual(x["physical_nonheader_rows"],3)
        self.assertEqual(x["nonheader_rows_with_any_nonempty"],3)
        self.assertEqual(x["observed_row_universe_vs_published_n"],
                         "ROW_UNIVERSE_MISMATCH_NOT_LICENSE_TO_DELETE_ROWS")

    def test_no_data_rows_ignored_to_force_publication(self):
        x=scan(workbook({2:{1:1},3:{},4:{2:0}}))
        self.assertEqual(x["physical_nonheader_rows"],3)
        self.assertEqual(x["nonheader_rows_with_any_nonempty"],2)

    def test_unmapped_anonymous_column_must_not_be_named_treatment(self):
        x=scan(workbook({2:{1:1},3:{1:0}}))
        self.assertEqual(x["serving_profile_encoding"],"NOT_MAPPED_TO_AUTHOR_CODEBOOK")
        self.assertEqual(x["author_table3_replication"],"NOT_PERFORMED")

    def test_private_text_never_emitted(self):
        x=scan(workbook({2:{1:"PRIVATE_USER_NAME_198712",2:"REAL_PROFILE_HANDLE_BOB"}}))
        self.assertNotIn("PRIVATE_USER_NAME_198712",str(x))
        self.assertNotIn("REAL_PROFILE_HANDLE_BOB",str(x))
        self.assertFalse(x["raw_header_or_category_values_exported"])

    def test_numeric_01_only_nonmissing_emits_aggregate_if_both_values(self):
        v=m.column_report([(0 and m.Decimal(0),"numeric"),
                           (m.Decimal(1),"numeric")],2)
        self.assertEqual(v["complete_binary_01_histogram_only_if_all_rows_and_both_codes_present"],
                         {"zero":1,"one":1})

    def test_binary_column_missing_does_not_publish_distribution(self):
        v=m.column_report([(m.Decimal(0),"numeric"),(None,"empty")],2)
        self.assertIsNone(v["complete_binary_01_histogram_only_if_all_rows_and_both_codes_present"])

    def test_numeric_integer_domain_predefined_only(self):
        v=m.column_report([(m.Decimal(2),"numeric"),(m.Decimal(3),"numeric")],2)
        self.assertFalse(v["fixed_small_integer_numeric_domains"]["all_nonempty_numeric_in_(0, 1, 2)"])

    def test_arbitrary_numeric_identifiers_not_printed(self):
        x=scan(workbook({2:{1:87654321},3:{1:87654322}}))
        self.assertNotIn("87654321",str(x))
        self.assertNotIn("87654322",str(x))

    def test_duplicate_column_within_row_fails(self):
        xml=f'<worksheet xmlns="{NS}"><sheetData><row r="1"><c r="A1"><v>1</v></c></row><row r="2"><c r="A2"><v>1</v></c><c r="A2"><v>0</v></c></row></sheetData></worksheet>'
        a=workbook({2:{1:0}})
        with ZipFile(io.BytesIO(a)) as z:
            files={n:z.read(n) for n in z.namelist()}
        files["xl/worksheets/sheet1.xml"]=xml.encode()
        buffer=io.BytesIO()
        with ZipFile(buffer,"w") as z:
            for n,v in files.items():z.writestr(n,v)
        with self.assertRaisesRegex(ValueError,"DUPLICATE_COLUMN"):
            scan(buffer.getvalue())

    def test_duplicate_row_fails(self):
        a=workbook({2:{1:1}},extra=[("xl/worksheets/sheet2.xml",b"bogus")])
        with self.assertRaisesRegex(ValueError,"EXPECTED_ONE"):
            scan(a)

    def test_source_hash_drift_rejected(self):
        raw=workbook({2:{1:1}})
        with self.assertRaisesRegex(ValueError,"SOURCE_SHA"):
            m.scan_rows(raw)

    def test_no_real_xlsx_original_data_written(self):
        x=scan(workbook({2:{1:"faked_person",2:1}}))
        self.assertFalse(x["raw_S8_bytes_in_research_repository"])
        self.assertFalse(x["participant_rows_exported"])

    def test_cell_coordinate_ref_rejects_fake_header(self):
        with self.assertRaisesRegex(ValueError,"INVALID_CELL_COORDINATE"):
            m.cell_column("AA1x")

    def test_unknown_cell_type_fails_closed(self):
        from xml.etree import ElementTree as ET
        elt=ET.fromstring(f'<c xmlns="{NS}" t="other"><v>x</v></c>')
        with self.assertRaisesRegex(ValueError,"UNKNOWN_SAFE_CELL_TYPE"):
            m.decode_cell(elt,[])

    def test_reject_formula_even_if_cached(self):
        raw=workbook({2:{1:1}})
        with ZipFile(io.BytesIO(raw)) as z:
            files={n:z.read(n) for n in z.namelist()}
        files["xl/worksheets/sheet1.xml"]=files["xl/worksheets/sheet1.xml"].replace(
            b"<v>1</v>",b"<f>RAND()</f><v>1</v>",1)
        buff=io.BytesIO()
        with ZipFile(buff,"w") as z:
            for n,v in files.items():z.writestr(n,v)
        with self.assertRaisesRegex(ValueError,"FORMULAS"):
            scan(buff.getvalue())

    def test_invalid_raw_numeric_raises_fixed_error_no_PII(self):
        from xml.etree import ElementTree as ET
        elt=ET.fromstring(f'<c xmlns="{NS}"><v>private_identifier</v></c>')
        with self.assertRaisesRegex(ValueError,"UNSAFE_NUMERIC_CELL"):
            m.decode_cell(elt,[])

    def test_empty_string_cell_is_empty_not_valid_record(self):
        raw=workbook({2:{1:"   "}})
        x=scan(raw)
        self.assertEqual(x["nonheader_rows_with_any_nonempty"],0)

    def test_is_not_human_causal_model(self):
        x=scan(workbook({2:{1:1,2:0},3:{1:0,2:1}}))
        self.assertEqual(x["R072_IMAGE_STANDING_STERN_REAL_HUMAN_MODEL"],"NOT_FITTED")
        self.assertEqual(x["independent_E3"],"OPEN")


if __name__=="__main__":unittest.main()
