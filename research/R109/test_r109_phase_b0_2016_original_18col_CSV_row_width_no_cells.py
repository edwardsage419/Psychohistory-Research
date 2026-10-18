"""R109 B0 source 2016 original CSV row WIDTH synthetic with no human data."""
import hashlib,unittest
from unittest.mock import patch
import r109_phase_a1_2016_true_Guelph_Figshare_5611125_publisher_MD5_double_SHA_header_only as a
import r109_phase_b0_2016_original_18col_CSV_row_width_no_cells as b

def fixture(wide=True):
    head=",".join(["field"]+[""]*17)
    lines=[head]
    for i in range(156):
        vals=["PRIVATE_PERSON"]*18
        if not wide and i==8:vals=vals[:-1]
        lines.append(",".join(vals))
    return ("\n".join(lines)+"\n").encode()

def audited(raw):
    with patch.object(a,"PUBLISHED_SIZE",len(raw)),\
         patch.object(a,"PUBLISHED_MD5",hashlib.md5(raw).hexdigest()),\
         patch.object(b,"PINNED_SHA",hashlib.sha256(raw).hexdigest()):
        return b.original_widths(raw)

class R109RowWidth(unittest.TestCase):
    def test_valid_156_row_18_field_full_csv(self):
        x=audited(fixture())
        self.assertEqual(x["original_CSV_logical_body_row_count"],156)
        self.assertEqual(x["source_CSV_header_column_count"],18)
        self.assertEqual(x["anonymous_source_body_row_width_counts"],{"18":156})
        self.assertTrue(x["all_original_CSV_body_rows_width_18"])
    def test_one_shrunk_row_never_silently_discarded(self):
        x=audited(fixture(wide=False))
        self.assertEqual(x["anonymous_source_body_row_width_counts"],{"17":1,"18":155})
        self.assertFalse(x["all_original_CSV_body_rows_width_18"])
        self.assertGreater(x["original_body_row_width_transition_count"],0)
    def test_only_widths_no_private_human_cells(self):
        x=audited(fixture())
        self.assertNotIn("PRIVATE_PERSON",repr(x))
        self.assertFalse(x["actual_human_source_data_cell_values_accessed"])
        self.assertEqual(x["actual_human_model_scores"],0)
    def test_published_md5_rejects_unpinned(self):
        self.assertRaises(a.SourceError,b.original_widths,fixture())
    def test_publisher_MD5_match_still_needs_exact_full_SHA(self):
        raw=fixture()
        with patch.object(a,"PUBLISHED_MD5",hashlib.md5(raw).hexdigest()),\
             patch.object(a,"PUBLISHED_SIZE",len(raw)):
            self.assertRaises(a.SourceError,b.original_widths,raw)
    def test_csv_without_data_rejected(self):
        raw=(",".join(["field"]+[""]*17)+"\n").encode()
        with patch.object(a,"PUBLISHED_MD5",hashlib.md5(raw).hexdigest()),\
             patch.object(a,"PUBLISHED_SIZE",len(raw)),\
             patch.object(b,"PINNED_SHA",hashlib.sha256(raw).hexdigest()):
            self.assertRaises(a.SourceError,b.original_widths,raw)
    def test_anonymous_first_last_eight_only_width_numbers(self):
        x=audited(fixture())
        self.assertEqual(x["source_anonymous_first_8_data_row_widths"],[18]*8)
        self.assertEqual(x["source_anonymous_last_8_data_row_widths"],[18]*8)
    def test_independent_lab_session_not_proven_by_row_count(self):
        x=audited(fixture())
        self.assertFalse(x["source_independent_original_lab_session_ID_verified"])
        self.assertFalse(x["source_person_opponent_round_mapping_verified"])
    def test_uniform_row_source_no_E2(self):
        x=audited(fixture())
        self.assertEqual(x["actual_human_model_scores"],0)
        self.assertEqual(x["PESEN_v0_1"],"FROZEN")
    def test_not_unexpected_behavioral_row_export(self):
        x=audited(fixture(wide=False))
        self.assertTrue(all(isinstance(k,str) and k.isdigit() for k in x["anonymous_source_body_row_width_counts"]))
        self.assertNotIn("PRIVATE_PERSON",str(x))
if __name__=="__main__":unittest.main()
