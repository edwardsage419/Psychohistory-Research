"""R110 B0 public first-party header and 12000 original source row WIDTH tests."""
import hashlib,unittest
from unittest.mock import patch
import r110_phase_b0_2015_PLOS_original_12000_CSV_row_width_and_18_public_headers_only as b
import r110_phase_a1_2015_PLOS_S1_verified_google_storage_original_doubleSHA_header_only as a

def make_data(names=None,bad_row=False,rows=12000):
    head=",".join(names or ["field"+str(i) for i in range(18)])
    one=",".join(["PRIVATE_ORIGINAL_HUMAN_ACTION"]*18)
    lines=[head]+[one]*rows
    if bad_row and rows>=2:
        lines[8]=",".join(["PRIVATE_HUMAN_ACTION"]*17)
    return ("\n".join(lines)+"\n").encode("utf8")
def audited(raw):
    with patch.object(b,"PINNED_SHA",hashlib.sha256(raw).hexdigest()),\
         patch.object(b,"EXPECTED_BYTES",len(raw)):
        return b.original_public_source_headers_and_widths(raw)

class R110B0Source(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=make_data()
    def test_true_12000x18_structure(self):
        x=audited(self.data)
        self.assertTrue(x["all_source_rows_12000x18_structurally"])
        self.assertEqual(x["original_logical_CSV_data_rows"],12000)
        self.assertEqual(x["source_anonymous_row_width_histogram"],{"18":12000})
    def test_anonymous_public_header_names(self):
        x=audited(self.data)
        self.assertEqual(x["author_original_public_field_names_only"],["field"+str(i) for i in range(18)])
        self.assertFalse(x["original_individual_behavior_or_person_ID_values_read"])
    def test_private_row_token_not_exported(self):
        x=audited(self.data)
        self.assertNotIn("PRIVATE_ORIGINAL_HUMAN_ACTION",repr(x))
    def test_source_MD5_not_invented_and_SHA_required(self):
        self.assertRaisesRegex(a.SourceError,"WHOLEFILE_SHA_SIZE_NOT_PINNED",b.original_public_source_headers_and_widths,self.data)
    def test_bad_row_width_not_silently_excluded(self):
        x=audited(make_data(bad_row=True))
        self.assertFalse(x["all_source_rows_12000x18_structurally"])
        self.assertEqual(x["source_anonymous_row_width_histogram"],{"17":1,"18":11999})
        self.assertGreater(x["source_row_width_transition_count"],0)
    def test_source_public_email_column_not_exported(self):
        names=["field"+str(i) for i in range(17)]+["PRIVATE@email.example"]
        self.assertRaisesRegex(a.SourceError,"FIELDS_NOT_SAFE",audited,make_data(names))
    def test_duplicate_public_label_denied(self):
        names=["x"]*18
        self.assertRaisesRegex(a.SourceError,"FIELDS_NOT_SAFE",audited,make_data(names))
    def test_empty_column_label_denied(self):
        names=["field"+str(i) for i in range(17)]+[""]
        self.assertRaisesRegex(a.SourceError,"FIELDS_NOT_SAFE",audited,make_data(names))
    def test_nonascii_field_denied(self):
        names=["field"+str(i) for i in range(17)]+["姓名"]
        self.assertRaisesRegex(a.SourceError,"FIELDS_NOT_SAFE",audited,make_data(names))
    def test_eight_row_width_only(self):
        x=audited(self.data)
        self.assertEqual(x["source_first_eight_anonymous_row_widths"],[18]*8)
        self.assertEqual(x["source_last_eight_anonymous_row_widths"],[18]*8)
    def test_true_header_not_private_values(self):
        x=audited(self.data)
        self.assertEqual(x["real_human_model_scores"],0)
        self.assertEqual(x["PESEN_v0_1"],"FROZEN")
    def test_lower_sample_number_does_not_forge_real_12000(self):
        x=audited(make_data(rows=700))
        self.assertFalse(x["all_source_rows_12000x18_structurally"])
        self.assertEqual(x["original_logical_CSV_data_rows"],700)
    def test_wrong_actual_publisher_byte_count_denied(self):
        with patch.object(b,"PINNED_SHA",hashlib.sha256(self.data).hexdigest()):
            self.assertRaisesRegex(a.SourceError,"WHOLEFILE_SHA_SIZE_NOT_PINNED",b.original_public_source_headers_and_widths,self.data)

if __name__=="__main__":unittest.main()
