"""R108 B0 synthetic original source delimiter width, no human cells."""
import hashlib
import unittest
from unittest.mock import patch
import r108_phase_b0_2017_original_CSV_body_row_WIDTH_only as b
import r108_phase_a1_original_2017_Leicester_fixed_pair_CSV_MD5_double_SHA_header_only as a

def specimen(lines=50,change=False):
    head="meta,,,,\n"
    data=[]
    for i in range(lines):
        data.append("PRIVATE_PERSON,PRIVATE_ACTION,PRIVATE_PAIR,PRIVATE_ROUND," if not change or i%2==0 else "PRIVATE_PERSON,PRIVATE_ACTION")
    return (head+"\n".join(data)+"\n").encode()

def run(fake):
    with patch.object(a,"EXPECTED_SIZE",len(fake)),patch.object(a,"EXPECTED_MD5",hashlib.md5(fake).hexdigest()):
        return b.width_only(fake)

class B0(unittest.TestCase):
    def test_50_rows_constant_width(self):
        x=run(specimen())
        self.assertEqual(x["original_CSV_logical_data_row_count_no_cells_read"],50)
        self.assertEqual(x["source_body_row_width_histogram"],{"5":50})
        self.assertFalse(x["original_CSV_cell_values_application_dereferenced"])
        self.assertNotIn("PRIVATE_PERSON",repr(x))
    def test_two_widths_anonymized(self):
        x=run(specimen(change=True))
        self.assertEqual(x["source_body_row_width_histogram"],{"2":25,"5":25})
        self.assertEqual(x["original_row_width_transition_count"],49)
    def test_source_md5_rejected(self):
        self.assertRaises(a.SourceError,b.width_only,specimen())
    def test_wrong_published_source_size_rejected(self):
        f=specimen()
        with patch.object(a,"EXPECTED_MD5",hashlib.md5(f).hexdigest()):
            self.assertRaises(a.SourceError,b.width_only,f)
    def test_no_field_names_and_private_values_export(self):
        x=run(specimen(change=True))
        self.assertNotIn("PRIVATE_ACTION",repr(x))
        self.assertNotIn("meta",repr(x))
        self.assertFalse(x["raw_person_round_partner_acts_exported"])
    def test_empty_body_rejected(self):
        f=b"meta,,,,\n"
        with patch.object(a,"EXPECTED_SIZE",len(f)),patch.object(a,"EXPECTED_MD5",hashlib.md5(f).hexdigest()):
            self.assertRaises(a.SourceError,b.width_only,f)
    def test_nonzero_physical_lines(self):
        x=run(specimen())
        self.assertGreater(x["original_CSV_physical_data_line_count"],0)
    def test_first_and_last_are_just_width_counts(self):
        x=run(specimen(change=True))
        self.assertEqual(len(x["anonymous_first_ten_data_row_widths_only"]),10)
        self.assertEqual(len(x["anonymous_last_ten_data_row_widths_only"]),10)
        self.assertTrue(all(type(z)==int for z in x["anonymous_first_ten_data_row_widths_only"]))
    def test_original_model_zero(self):
        self.assertEqual(run(specimen())["original_human_model_scores"],0)
    def test_source_original_md5_still_bound(self):
        x=run(specimen())
        self.assertEqual(len(x["original_source_SHA256"]),64)
if __name__=="__main__":unittest.main()
