"""Pure synthetic tests for the R100 B0 source worksheet tag census."""
import io
import unittest
import r100_phase_b0_zenodo_xlsx_ab_tag_structure_only as b

N = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def xml(rows):
    return io.BytesIO(('<worksheet xmlns="' + N + '"><sheetData>' +
                       rows + '</sheetData></worksheet>').encode("utf-8"))


def row(number, cells):
    return '<row r="' + str(number) + '">' + cells + '</row>'


def cell(reference, value="SECRET_HUMAN_DATA_MUST_NEVER_BE_EMITTED"):
    return '<c r="' + reference + '"><v>' + value + '</v></c>'


class B0PureSynthetic(unittest.TestCase):
    def test_two_rows(self):
        fake = xml(row(1, cell("A1") + cell("B1") + cell("C1")) +
                   row(2, cell("A2") + cell("B2") + cell("Z2")))
        x = b.structure_of_worksheet(fake)
        self.assertEqual((x["row_tag_count"], x["column_A_cell_tag_count"],
                          x["column_B_cell_tag_count"], x["rows_with_both_A_and_B_cell_tags"]),
                         (2, 2, 2, 2))
        self.assertNotIn("SECRET_HUMAN", repr(x))
    def test_one_column_each_on_different_row(self):
        x = b.structure_of_worksheet(xml(row(1, cell("A1")) + row(2, cell("B2"))))
        self.assertEqual(x["rows_with_both_A_and_B_cell_tags"], 0)
    def test_other_column_does_not_increment_id(self):
        x = b.structure_of_worksheet(xml(row(7, cell("C7") + cell("Z7") + cell("A7") + cell("B7"))))
        self.assertEqual(x["column_A_cell_tag_count"], 1)
        self.assertEqual(x["column_B_cell_tag_count"], 1)
    def test_only_A_rejected(self):
        with self.assertRaises(b.SourceError):
            b.structure_of_worksheet(xml(row(1, cell("A1"))))
    def test_only_B_rejected(self):
        with self.assertRaises(b.SourceError):
            b.structure_of_worksheet(xml(row(1, cell("B1"))))
    def test_empty_rejected(self):
        with self.assertRaises(b.SourceError):
            b.structure_of_worksheet(xml(""))
    def test_duplicate_A_rejected(self):
        with self.assertRaises(b.SourceError):
            b.structure_of_worksheet(xml(row(1, cell("A1") + cell("A1") + cell("B1"))))
    def test_wrong_row_cell_ref_rejected(self):
        with self.assertRaises(b.SourceError):
            b.structure_of_worksheet(xml(row(1, cell("A2") + cell("B1"))))
    def test_nonincreasing_row_rejected(self):
        with self.assertRaises(b.SourceError):
            b.structure_of_worksheet(xml(row(2, cell("A2") + cell("B2")) +
                                        row(1, cell("A1") + cell("B1"))))
    def test_missing_row_number_rejected(self):
        with self.assertRaises(b.SourceError):
            b.structure_of_worksheet(xml('<row>'+cell("A1")+cell("B1")+'</row>'))
    def test_far_beyond_allowed_row_rejected(self):
        with self.assertRaises(b.SourceError):
            b.structure_of_worksheet(xml(row(100001, cell("A100001") + cell("B100001"))))
    def test_broken_xml_rejected(self):
        with self.assertRaises(b.SourceError):
            b.structure_of_worksheet(io.BytesIO(b"<invalid"))
    def test_nested_row_rejected(self):
        with self.assertRaises(b.SourceError):
            b.structure_of_worksheet(xml('<row r="1"><row r="2">'+cell("A2")+cell("B2")+'</row></row>'))
    def test_modified_original_bytes_rejected(self):
        with self.assertRaises(b.SourceError):
            b.source_structure_only(b"FAKE_ORIGINAL")
    def test_does_not_expose_sensitive_strings(self):
        x = b.structure_of_worksheet(xml(row(3, cell("A3", "ORIGINAL_PERSON_92922") +
                                                  cell("B3", "PAIR_CODE_332") +
                                                  cell("C3", "SECRET_CONTRIBUTION_9"))))
        self.assertNotIn("ORIGINAL_PERSON", str(x))
        self.assertNotIn("PAIR_CODE", str(x))
        self.assertNotIn("SECRET_CONTRIBUTION", str(x))


if __name__ == "__main__":
    unittest.main()
