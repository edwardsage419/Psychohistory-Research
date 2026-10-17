"""R100 B1a pure synthetic identity-code formatting and privacy tests; no real data."""
import io
import unittest
import zipfile
import r100_phase_b1a_only_AB_literal_source_code_diagnostic as m

NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"


def cell(col, row, val=None, typ="n"):
    addr = f"{col}{row}"
    if val is None:
        return f'<c r="{addr}"/>'
    return f'<c r="{addr}" t="{typ}"><v>{val}</v></c>'


def sample_sheet(aval="11", bval="22", cells=None, rows=5):
    items = []
    for i in range(1, rows + 1):
        if i == 1:
            items.append(f'<row r="1">{cell("A", 1, "HEADER", "str")}{cell("B", 1, "PAIR", "str")}</row>')
        else:
            c = cells[i-2] if cells is not None else cell("A",i,aval)+cell("B",i,bval)
            items.append(f'<row r="{i}">{c}</row>')
    return ('<worksheet xmlns="'+NS+'"><sheetData>'+"".join(items)+'</sheetData></worksheet>').encode()


class B1aSynthetic(unittest.TestCase):
    def test_four_row_block(self):
        x=m.raw_ab_cells(sample_sheet())
        self.assertEqual(len(x), 5)
        self.assertEqual(x[1]["A"],("n","11"))
        self.assertEqual(x[-1]["B"],("n","22"))
    def test_sparse_A_and_B_tags(self):
        x=m.raw_ab_cells(sample_sheet(cells=[
            cell("A",2,"11")+cell("B",2,"22"),
            cell("A",3)+cell("B",3),
            cell("A",4)+cell("B",4),
            cell("A",5)+cell("B",5)]))
        self.assertEqual(x[-1]["A"],("n",""))
    def test_no_real_source_values_in_return(self):
        x=m.raw_ab_cells(sample_sheet(aval="111",bval="222"))
        self.assertEqual(x[2]["B"],("n","222"))
        # Export protection is enforced only by analyze_source(), never print raw_ab_cells().
    def test_bad_block_count(self):
        self.assertRaises(m.SourceError,m.raw_ab_cells,sample_sheet(rows=6))
    def test_missing_A(self):
        self.assertRaises(m.SourceError,m.raw_ab_cells,sample_sheet(cells=[
            cell("B",2,"11"),cell("A",3)+cell("B",3),cell("A",4)+cell("B",4),cell("A",5)+cell("B",5)]))
    def test_formula_in_A(self):
        row=cell("B",2,"22")+'<c r="A2"><f>SUM(1,2)</f><v>3</v></c>'
        self.assertRaises(m.SourceError,m.raw_ab_cells,sample_sheet(cells=[row]+[cell("A",i,"11")+cell("B",i,"22") for i in (3,4,5)]))
    def test_duplicate_A(self):
        row=cell("A",2,"11")+cell("A",2,"33")+cell("B",2,"22")
        self.assertRaises(m.SourceError,m.raw_ab_cells,sample_sheet(cells=[row]+[cell("A",i,"11")+cell("B",i,"22") for i in (3,4,5)]))
    def test_wrong_A_row_number(self):
        row=cell("A",9,"11")+cell("B",2,"22")
        self.assertRaises(m.SourceError,m.raw_ab_cells,sample_sheet(cells=[row]+[cell("A",i,"11")+cell("B",i,"22") for i in (3,4,5)]))
    def test_reject_prohibited_literal(self):
        self.assertRaises(m.SourceError,m.sanitized_token,"https://evil.example/private")
    def test_reject_long_literal(self):
        self.assertRaises(m.SourceError,m.sanitized_token,"z"*65)
    def test_valid_identifier(self):
        self.assertEqual(m.sanitized_token("P 2.3"),"P 2.3")
    def test_numeric_identity(self):
        self.assertEqual(m.resolved_value(("n","456"),{}),"456")
    def test_noninteger_identity(self):
        self.assertRaises(m.SourceError,m.resolved_value,("n","2.5"),{})
    def test_empty_identity(self):
        self.assertIsNone(m.resolved_value(("n",""),{}))
    def test_shared_string_reference(self):
        out=io.BytesIO()
        with zipfile.ZipFile(out,"w") as z:
            z.writestr("xl/sharedStrings.xml",
                '<sst xmlns="'+NS+'"><si><t>FOCAL11</t></si><si><t>PAIR22</t></si></sst>')
        with zipfile.ZipFile(io.BytesIO(out.getvalue())) as z:
            got=m.referenced_shared_strings(z,{0,1})
        self.assertEqual(got,{0:"FOCAL11",1:"PAIR22"})
    def test_shared_unreferenced_secret_not_emitted(self):
        out=io.BytesIO()
        with zipfile.ZipFile(out,"w") as z:
            z.writestr("xl/sharedStrings.xml",'<sst xmlns="'+NS+'"><si><t>A11</t></si><si><t>UNUSED_SECRET_29</t></si></sst>')
        with zipfile.ZipFile(io.BytesIO(out.getvalue())) as z:
            got=m.referenced_shared_strings(z,{0})
        self.assertNotIn("UNUSED_SECRET",repr(got))
    def test_shared_missing(self):
        with zipfile.ZipFile(io.BytesIO(self.zip_with_no_shared())) as z:
            self.assertRaises(m.SourceError,m.referenced_shared_strings,z,{0})
    @staticmethod
    def zip_with_no_shared():
        o=io.BytesIO()
        with zipfile.ZipFile(o,"w") as z:z.writestr("xl/workbook.xml","x")
        return o.getvalue()
    def test_fake_source_must_fail_before_any_parse(self):
        self.assertRaises(m.SourceError,m.analyze_source,b"fake original")


if __name__=="__main__":
    unittest.main()
