"""All tests use entirely invented nonhuman OOXML only, never PLOS subjects."""
import io,hashlib,unittest
from unittest.mock import patch
from zipfile import ZipFile,ZIP_DEFLATED
import r072_plos_s8_anonymous_schema_rev003 as m

NS="http://schemas.openxmlformats.org/spreadsheetml/2006/main"
def fake(rows,shared=None,extra=None):
    f=io.BytesIO()
    with ZipFile(f,"w",compression=ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",b"<Types/>")
        z.writestr("xl/workbook.xml",f'<workbook xmlns="{NS}"/>'.encode())
        z.writestr("xl/worksheets/sheet1.xml",f'<worksheet xmlns="{NS}"><sheetData>{rows}</sheetData></worksheet>'.encode())
        if shared:
            strings="".join(f"<si><t>{item}</t></si>" for item in shared)
            z.writestr("xl/sharedStrings.xml",f'<sst xmlns="{NS}">{strings}</sst>'.encode())
        for name,data in (extra or []):
            z.writestr(name,data)
    return f.getvalue()

ROW1='<row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1" t="s"><v>1</v></c></row>'
ROW2='<row r="2"><c r="A2"><v>7</v></c><c r="B2" t="s"><v>2</v></c></row>'
def approved(raw):
    with patch.object(m,"EXACT_SHA",hashlib.sha256(raw).hexdigest()):
        return m.scan_workbook(raw)


class R072AnonymousHumanSchemaTests(unittest.TestCase):
    def test_two_rows_two_columns_anonymous(self):
        z=approved(fake(ROW1+ROW2,["treatment","response","FAKE PRIVATE HANDLE"]))
        self.assertEqual(z["total_anonymous_worksheets"],1)
        s=z["anonymous_sheet_metadata"][0]
        self.assertEqual(s["physical_row_tags"],2)
        self.assertEqual(s["nonempty_cell_total"],4)
        self.assertEqual(s["whitelisted_semantic_header_matches"]["response"],1)

    def test_original_header_titles_never_exported(self):
        z=approved(fake(ROW1+ROW2,["treatment","response","SECRET_WORKBOOK_USER_1234"]))
        self.assertNotIn("SECRET_WORKBOOK_USER_1234",str(z))
        self.assertFalse(z["raw_header_values_exported"])
        self.assertFalse(z["real_participant_values_exported"])

    def test_no_original_sheet_names_exported(self):
        z=approved(fake(ROW1,["request","response"]))
        self.assertNotIn("sheet1.xml",str(z))
        self.assertEqual(z["anonymous_sheet_metadata"][0]["sheet_anonymous_index"],1)

    def test_mismatch_between_known_source_hash_and_fake(self):
        with self.assertRaisesRegex(ValueError,"SOURCE_SHA"):
            m.scan_workbook(fake(ROW1,["request","response"]))

    def test_first_row_not_actual_row1_is_not_guessed_header(self):
        raw=fake('<row r="2"><c r="A2" t="inlineStr"><is><t>response</t></is></c></row>')
        z=approved(raw)
        s=z["anonymous_sheet_metadata"][0]
        self.assertEqual(s["header_mapping_status"],"MAPPING_NOT_ESTABLISHED")

    def test_shared_header_only_whitelisted_anonymous_count(self):
        z=approved(fake(ROW1,["donor_ID_SECRET","response"]))
        c=z["anonymous_sheet_metadata"][0]["whitelisted_semantic_header_matches"]
        self.assertEqual(c["response"],1)
        self.assertFalse(any("SECRET" in key for key in c))

    def test_inline_str_reputation_header_matched(self):
        raw=fake('<row r="1"><c r="A1" t="inlineStr"><is><t>Reputation Score</t></is></c></row>')
        z=approved(raw)
        self.assertEqual(z["anonymous_sheet_metadata"][0]["whitelisted_semantic_header_matches"]["reputation"],1)

    def test_no_relevant_schema_is_explicit_unknown(self):
        z=approved(fake(ROW1,["field_a","field_b"]))
        self.assertEqual(z["anonymous_sheet_metadata"][0]["header_mapping_status"],"MAPPING_NOT_ESTABLISHED")

    def test_duplicate_shared_string_invalid_reference_fails(self):
        raw=fake('<row r="1"><c r="A1" t="s"><v>999</v></c></row>',["header"])
        with self.assertRaisesRegex(ValueError,"SHARED_STRING_INDEX"):
            approved(raw)

    def test_malformed_sheet_XML_fails_without_content(self):
        raw=fake(ROW1,["header_a","header_b"],[("xl/worksheets/sheet2.xml",b"broken <")])
        with self.assertRaisesRegex(ValueError,"OOXML_MALFORMED"):
            approved(raw)

    def test_worksheet_missing_sheetData_fails_closed(self):
        raw=fake(ROW1,["request","response"],[("xl/worksheets/sheet2.xml",
                                  f'<worksheet xmlns="{NS}"/>'.encode())])
        with self.assertRaisesRegex(ValueError,"SHEETDATA"):
            approved(raw)

    def test_macro_lure_rejected_by_rev002(self):
        raw=fake(ROW1,["response","request"],[("xl/vbaProject.bin",b"fake")])
        with self.assertRaisesRegex(ValueError,"ACTIVE_OR_EXTERNAL"):
            approved(raw)

    def test_formulas_not_evaluated_from_human_sheets(self):
        raw=fake('<row r="1"><c r="A1"><f>1+1</f><v>2</v></c></row>')
        with self.assertRaisesRegex(ValueError,"FORMULAS"):
            approved(raw)

    def test_excel_cell_ref_malformed_fails_closed(self):
        raw=fake('<row r="1"><c r="A_1" t="inlineStr"><is><t>request</t></is></c></row>')
        with self.assertRaisesRegex(ValueError,"CELL_REF"):
            approved(raw)

    def test_excel_column_index_over_limit(self):
        raw=fake('<row r="1"><c r="ZZ1"><v>20</v></c></row>')
        with self.assertRaisesRegex(ValueError,"COLUMN_LIMIT"):
            approved(raw)

    def test_too_many_sheets_rejected(self):
        extra=[(f"xl/worksheets/sheet{i}.xml",
                f'<worksheet xmlns="{NS}"><sheetData/></worksheet>'.encode()) for i in range(2,23)]
        with self.assertRaisesRegex(ValueError,"SHEET_COUNT"):
            approved(fake(ROW1,["response"],extra))

    def test_worksheet_with_DTD_rejected(self):
        raw=fake(ROW1,["response"],[("xl/worksheets/sheet2.xml",b'<!DOCTYPE p><worksheet/>')])
        with self.assertRaisesRegex(ValueError,"DTD"):
            approved(raw)

    def test_status_cannot_upgrade_to_behavior_model(self):
        z=approved(fake(ROW1,["response","treatment"]))
        self.assertFalse(z["causal_reputation_model_fitted"])
        self.assertEqual(z["human_R072_exact_model_E2"],"BLOCKED_RULE_EXPOSURE_AND_DATA_DICTIONARY")

    def test_numeric_cells_not_reproduced(self):
        raw=fake(ROW1+ROW2,["request","response","VERY_SECRET"])
        z=approved(raw)
        self.assertNotIn("VERY_SECRET",str(z))
        self.assertNotIn("r=\"A2\"",str(z))
        self.assertEqual(z["anonymous_sheet_metadata"][0]["cells_stored_as_numeric"],1)


if __name__=="__main__":unittest.main()
